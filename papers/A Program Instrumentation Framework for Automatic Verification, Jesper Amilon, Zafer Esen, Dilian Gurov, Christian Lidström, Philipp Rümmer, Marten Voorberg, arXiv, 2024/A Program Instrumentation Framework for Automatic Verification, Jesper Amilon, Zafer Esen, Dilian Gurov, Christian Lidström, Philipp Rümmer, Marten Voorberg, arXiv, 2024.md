                                             A Program Instrumentation Framework for Automatic
                                                                Verification
                                            Jesper Amilon1,‡ , Zafer Esen2,‡ , Dilian Gurov1,‡ , Christian Lidström1,‡ , Philipp
                                                                 Rümmer2,3,‡ , and Marten Voorberg1,‡
arXiv:2412.06431v1 [cs.LO] 9 Dec 2024




                                                        1
                                                            KTH Royal Institute of Technology, Stockholm, Sweden
                                                                     2
                                                                       Uppsala University, Uppsala, Sweden
                                                              3
                                                                University of Regensburg, Regensburg, Germany
                                                               ‡
                                                                 These authors contributed equally to this work.

                                                                                  December 10, 2024


                                                                                          Abstract
                                            In deductive verification and software model checking, dealing with certain specification language
                                        constructs can be problematic when the back-end solver is not sufficiently powerful or lacks the required
                                        theories. One way to deal with this is to transform, for verification purposes, the program to an equivalent
                                        one not using the problematic constructs, and to reason about this equivalent program instead. In this
                                        article, we propose program instrumentation as a unifying verification paradigm that subsumes various
                                        existing ad-hoc approaches, has a clear formal correctness criterion, can be applied automatically, and can
                                        transfer back witnesses and counterexamples. We illustrate our approach on the automated verification of
                                        programs that involve quantification and aggregation operations over arrays, such as the maximum value
                                        or sum of the elements in a given segment of the array, which are known to be difficult to reason about
                                        automatically. We implement our approach in the MonoCera tool, which is tailored to the verification
                                        of programs with aggregation, and evaluate it on example programs, including SV-COMP programs.


                                        1      Introduction
                                        Program specifications are often written in expressive, high-level languages: for instance, in temporal
                                        logic [14], in first-order logic with quantifiers [28], in separation logic [40], or in specification languages
                                        that provide extended quantifiers for computing the sum or maximum value of array elements [33, 7].
                                        Specifications commonly also use a rich set of theories; for instance, specifications could be written
                                        using full Peano arithmetic, as opposed to bit-vectors or linear arithmetic used in the program. Rich
                                        specification languages make it possible to express intended program behaviour in a succinct form, and
                                        as a result reduce the likelihood of mistakes being introduced in specifications.
                                            There is a gap, however, between the languages used in specifications and the input languages of
                                        automatic verification tools. Software model checkers, in particular, usually require specifications to be
                                        expressed using program assertions and Boolean program expressions, and do not directly support any of
                                        the more sophisticated language features mentioned. In fact, rich specification languages are challenging
                                        to handle in automatic verification, since satisfiability checks can become undecidable (i.e., it is no longer
                                        decidable whether assertion failures can occur on a program path), and techniques for inferring program
                                        invariants usually focus on simple specifications only.
                                            To bridge this gap, it is common practice to encode high-level specifications in the low-level asser-
                                        tion languages understood by the tools. For instance, temporal properties can be translated to Büchi
                                        automata, and added to programs using ghost variables and assertions [14]; quantified properties can
                                        be replaced with non-determinism, ghost variables, or loops [13, 37]; sets used to specify the absence


                                                                                              1
1 typedef struct {
2     int batt_volt [10];
3     int max_voltage ; // Maximum voltage value in pack
4 } BATTERY_PACK ;

5

6    extern BATTERY_PACK nondet_BAT T ER Y _P A CK () ;
7    BATTERY_PACK bpack ;
8

9  void calc_pack_max () {
10   bpack . max_voltage = bpack . batt_volt [0];
11   for ( int i = 1; i < 10; i ++)
12     if ( bpack . batt_volt [ i ] > bpack . max_voltage )
13       bpack . max_voltage = bpack . batt_volt [ i ];
14 }

15 void main () {

16   bpack = nondet_BATT E RY _ PA C K () ; // non - det initializati o n
17   calc_pack_max () ;
18   assert ( bpack . max_voltage == \ max ( bpack . batt_volt , 0 , 10) ) ;
19 }




     Figure 1: Example program calculating the maximum voltage in a battery pack consisting of
     an array of batteries


 of data-races can be represented using non-deterministically initialized variables [18]. By adding ghost
 variables and bespoke ghost code to programs [22], many specifications can be made effectively checkable.
     The translation of specifications to assertions or ghost code is today largely designed, or even carried
 out, by hand. This is an error-prone process, and for complex specifications and programs it is hard to
 ensure that the low-level encoding of a specification faithfully models the original high-level properties to
 be checked. Mistakes have been found even in industrial, very carefully developed specifications [39], and
 can result in assertions that are vacuously satisfied by any program. Naturally, the manual translation
 of specifications also tends to be an ad-hoc process that does not easily generalise to other specifications.
     This article proposes the first general framework to automate the translation of rich program specifi-
 cations to simpler program assertions, using a process called instrumentation. Our approach models the
 semantics of specific complex operations using program-independent instrumentation operators, consist-
 ing of (manually designed) rewriting rules that define how the evaluation of the operator can be achieved
 using simpler program statements and ghost variables. The instrumentation approach is flexible enough
 to cover a wide range of different operators, including operators that are best handled by weaving their
 evaluation into the program to be analysed. While instrumentation operators are manually written,
 their application to programs can be performed in a fully automatic way by means of a search procedure.
 The soundness of an instrumentation operator can be shown formally, once and for all, by providing an
 instrumentation invariant that ensures that the operator can never be used to show correctness of an
 incorrect program.

 Comparison to CAV paper This article extends our previous work [4] by including new instrumen-
 tation operators, now covering the full set of extended quantifiers in the specification language ACSL [7].
 Instrumentation operators for extended quantifiers are presented more systematically using monoid ho-
 momorphisms. A more comprehensive correctness result is included, where completeness in the typical
 sense is shown for certain classes of programs. Several existing sections of the CAV paper have been
 extended by adding more thorough explanations or discussions.

 1.1      Motivating Examples
 We illustrate our approach on two simple examples.




                                                      2
   Ωmax (Instrumentation operator)
     Gmax (Ghost variables)
     ag_lo, ag_hi, ag_max : Int, ag_ar : Array Int
     init(ag_lo) = init(ag_hi) = 0, init(ag_max) = −∞, init(ag_ar) = _

     Rmax (Rewrite rules)
     a’ = store(a, i, x)
         1   if ( i == ag_lo - 1 && ag_lo != ag_hi ) {
         2        assert ( ag_ar == a ) ;
         3        ag_lo = ag_lo = i ;
         4        ag_max = max ( ag_max , x ) ;
         5   } else if ( i == ag_hi && ag_lo != ag_hi ) {
         6        assert ( ag_ar == a ) ;
         7        ag_hi = i ;
         8        ag_max = max ( ag_val , x ) ;
         9   } else {
        10        ag_max = -∞;
        11        ag_lo = i ;
        12        ag_hi = i + 1;
        13   }
        14   a ’ = store (a , i , x ) ;
        15   ag_ar = a ’
      x = select(a, i)                 code similar to rewrites of store
      r = \max(a, l, u)
         1   if ( u <= l ) {
         2     r = −∞;
         3   } else {
         4     assert ( ag_ar == a && l == ag_lo && u == ag_hi ) ;
         5     r = ag_max ;
         6   }


     Imax (Instrumentation invariant)
     ag_lo = ag_hi ∨ ag_max = \max(ag_ar, ag_lo, ag_hi)



                     Figure 2: Definition of the instrumentation operator Ωmax


Array Aggregation Consider first the program shown in Figure 1, which operates on a battery
pack powering the electric engine of a vehicle. Although this particular implementation is written by us,
it is conceptually close to (significantly more complicated) code we encountered in collaborations with
automotive companies. The battery pack is represented as a C struct, consisting of an array of batteries
(representing the measured voltage at each battery) and a field for the maximum voltage value among
the batteries. In the program, the calc_pack_max function calculates the maximum value by looping
through the array, and in the main function, correctness of calc_pack_max is asserted by relying on the
\max operator. Intuitively, \max(a, l, u) extracts the maximum value of the array a in the interval
[l, u).
    Although simple in principle, the program in Figure 1 is non-trivial to handle for automatic ap-
proaches. Software model checkers, in particular, tend to infer loop invariants for the program that
explicitly refer to all array elements, resulting in high computational complexity. Hardness is increased
further when considering larger arrays, or even unbounded arrays, where more compact representations
of the loop invariant are needed. In the industry, programs calculating some aggregate measure over
an array are ubiquitous, wherefore there is a clear need for verification tools to support aggregation
operators like \max.
    To verify the program, we define the instrumentation operator Ωmax , shown in Figure 2. For sake
of presentation, all instrumentation operators in this article are defined using functional arrays, using
select and store to access and update the fields of an array, respectively. It is clear that the program in
Figure 1 can be rewritten to this style, but we leave this transformation implicit. Like all instrumentation


                                                     3
operators, Ωmax is comprised of three parts, the ghost variables, the rewrite rules, and the instrumentation
invariant. While instrumentation operators for array properties are discussed at length in Section 3, we
summarise here the key features of Ωmax in the context of Figure 1.
    The essential function of Ωmax is to induce, by applying the rewrite rules, a program transforma-
tion that mitigates the verification tasks. For this, assignments in a program that include the functions
select, store, or \max can rewritten to more complex pieces of code that, in addition to accessing
the array, also update the ghost variables of the instrumentation operator. The goal is to rewrite the
program in such a way that its correctness can be checked without having to evaluate the problematic
function \max; to this end, the instrumentation operator introduces ghost variables that track the max-
imum value of the array in an interval [ag_lo, ag_hi). The rewrite rules have to be applied to some
selection of the read/write statements, so that the ghost variables are updated appropriately. For ex-
ample, if the program reads from position ag_hi in the array, then the tracked interval [ag_lo, ag_hi)
can be extended by incrementing the ghost variable ag_hi for the upper interval bound, and similarly
for the lower bound for accesses at position ag_lo − 1. Moreover, if the value read is greater than the
previously tracked maximum value ag_max, this ghost variable is updated as well.
    Instrumentation operators do not, for a given program, produce a unique instrumentation, but instead
give rise to a set of instrumented programs, which we call the instrumentation space. Essentially, the
instrumentation space is formed by considering all possible sets of statements to which the rewrite rules
can be applied. In this example, we need to rewrite the array reads at lines 10 and 13. Thereafter, we
also rewrite the \max aggregation in terms of the ghost variables. As manifested in our experiments
(Section 7), this shifting of verification domain, from array elements to ghost variables, significantly
reduces the complexity for automatic verification tools to infer loop invariants, thus allowing programs
such as this one to be verified.
    The soundness of the instrumentation operator is tied tightly to the instrumentation invariant. In-
strumentation invariants are formulas that can (only) refer to the ghost variables introduced by an
instrumentation operator, and are formulated in such a way that they hold in every reachable state of
every program in the instrumentation space. To maintain their invariants, instrumentation operators use
shadow variables that duplicate the values of program variables. For Ωmax , the invariant is that, if the
ghost variables track some non-empty interval, then the tracked maximum value is indeed the maximum
value of the shadow ghost array ag_ar in that interval. The connection between the shadow variable
and the underlying program variable is established by letting the rewrite rules assert their equality.

Non-linear Arithmetic Our main focus are instrumentation operators for verification of properties
over arrays. However, instrumentation operators also generalise to other verification tasks, as illustrated
here for the purpose of verifying non-linear arithmetic properties.
    Consider the program on the left-hand side of Figure 3, computing the triangular numbers sN = (N 2 +
N )/2. For reasons of presentation, the program has been normalised by representing the square N*N using
an auxiliary variable NN. While mathematically simple, verifying the post-condition s == (NN+N)/2 in
the program turns out to be challenging even for state-of-the-art model checkers, since such tools are
usually thrown off course by the non-linear term N*N. Computing the value of NN by adding a loop in
line 16 is not sufficient for most tools either, since the program in any case requires a non-linear invariant
0 <= i <= N && 2*s == i*i + i to be derived for the loop in lines 4–12.
    The insight needed to elegantly verify this program is that the value i*i can be tracked during the
program execution using a ghost variable x_sq. An instrumentation operator for this purpose is defined
in Figure 4, instrumenting the program to maintain the relationship x_sq == i*i. The instrumented
program is shown in the right-hand side of Figure 3. Initially, i == x_sq == 0, and each time the
value of i is modified, also the variable x_sq is updated accordingly. In particular, we rewrite the
assignments C, D of the left-hand side program using rewrite rules (R2) and (R4), respectively, resulting
in the instrumented and correct program on the right-hand side. With the value x_sq == i*i available,
both the loop invariant and the post-condition turn into formulas over linear arithmetic, and automatic
program verification becomes largely straightforward.

1.2     Automatic Program Instrumentation
While the above examples illustrate the applicability of our instrumentation idea, we are still left with a
major challenge, namely how to automatically discover the appropriate program transformation, without


                                                      4
1 // Triangular numbers                               1 // Instrumented program
2 i = 0; /* A */ s = 0; /* B */                       2 i =0; s =0; x_sq =0; x_shad =0;
3 assume (N >0) ;                                     3 assume (N >0) ;

4 while ( i < N ) {                                   4 while ( i < N ) {

5                                                     5      // Begin - instrumentat i on
6                                                     6      assert ( i == x_shad ) ;
7                                                     7      x_sq     = x_sq + 2* i + 1;
8         i = i + 1; /* C */                          8      i        = i + 1;
9                                                     9      x_shad = i ;
10                                                   10      // End - instrumentat io n
11        s = s + i;                                 11      s        = s + i;
12   }                                               12 }

13                                                   13 // Begin - instrumentat io n

14                                                   14 assert ( N == x_shad ) ;

15   NN = N * N ; /* D */                            15 NN = x_sq ;

16                                                   16 // End - instrument at io n

17   assert ( s == ( NN + N ) /2) ;                  17 assert ( s == ( NN + N ) /2) ;




          Figure 3: Program computing triangular numbers, and its instrumented counterpart


 having to select manually the subset of statements to which the rewrite rules should be applied. To this
 end, we split the process of program instrumentation into two parts:
     (i) Choosing an instrumentation operator, which is defined manually, designed to be program-independent,
         and inducing a space of possible program transformations.
     (ii) Carrying out an automatic application strategy to find, among the possible program transformations,
          one that enables verification of the program at hand.
      The first step is illustrated in the examples above. The second step relies on that instrumentation
 operators are designed to be sound, which means that rewriting a wrong selection of program state-
 ments might lead to an instrumented program that cannot be verified, i.e., in which assertions might
 fail, but instrumentation can never turn an incorrect program into a correct instrumented program. This
 opens up the possibility to systematically search for the right program instrumentation. We propose
 a counterexample-guided algorithm for this purpose, which starts from some arbitrarily chosen instru-
 mentation, checks whether the instrumented program can be verified, and otherwise attempts to fix the
 instrumentation using a refinement loop. As soon as a verifiable instrumented program has been found,
 the search can stop and the correctness of the original program has been shown.

 1.3       Contributions and Outline
 The two operators shown so far are simple and do not apply to all programs, but they can easily be
 generalised. The framework presented in this article provides the foundation for developing a library of
 formally verified instrumentation operators. In the scope of this article, we focus on two specification
 constructs that have been identified as particularly challenging in the literature: existential and universal
 quantifiers over arrays, and aggregation (or extended quantifiers), which includes computing the sum or
 maximum value of elements in an array. Our experiments on benchmarks taken from the SV-COMP [8]
 show that even relatively simple instrumentation operators can significantly extend the capabilities of a
 software model checker, and often make the automatic verification of otherwise hard specifications easy.
     The contributions of the article are: (i) a general framework for program instrumentation, which
 defines a space of program transformations that work by rewriting individual statements (Section 2 and
 Section 4); (ii) a library of concrete operators defined within the framework, obtaining full coverage of the
 quantifiers (Section 3.1) and extended quantifiers (Section 3.2) in ACSL [7]; (iii) machine-checked proofs
 of the correctness of the instrumentation operators for quantifiers and extended quantifiers; (iv) cor-
 rectness results showing soundness and weak completeness for all instrumentation operators, and com-
 pleteness for certain classes of programs (Section 5); (v) an application strategy search algorithm in this



                                                          5
     Ωsquare (Instrumentation operator)
      Gsquare (Ghost variables)
      x_sq, x_shad : Int
      init(x_sq) = 0, init(x_shad) = 0

       Rsquare (Rewrite rules)
       y=α           y = α; x_sq = α2 ; x_shad = y                                        (R1)
       y=x+α             assert(x == x_shad);                                             (R2)
                         x_sq = x_sq + 2α * x + α2 ; y = x + α; x_shad = y
       y=α*x             assert(x == x_shad);                                             (R3)
                         x_sq = α2 * x_sq; y = α * x; x_shad = y
       y=x*x             assert(x == x_shad); y = x_sq                                    (R4)

      Isquare (Instrumentation invariant)
      x_sq = x_shad2



                  Figure 4: Instrumentation operator Ωsquare for tracking squares


space, for a given program (Section 6); (vi) a new verification tool, MonoCera, that is tailored to the
verification of programs with aggregation; and (vii) an evaluation of our method and tool on a set of
examples, including such from SV-COMP [8] (Section 7).


2      Instrumentation Framework
We now formally introduce the instrumentation framework. The instrumentation of a program requires
two main ingredients:
    1. An instrumentation operator that defines how to rewrite program statements with the purpose
       of eliminating language constructs that are difficult to reason about automatically, but leaves the
       choice of which occurrences of these statements to rewrite to the second part (this section).
    2. An application strategy for the instrumentation operator, which can be implemented using heuristics
       or systematic search, among others. The strategy is responsible for selecting the right (if any)
       program instrumentation from the many possible ones. Section 6 is dedicated to the second part.
Even though instrumentation operators are non-deterministic, we shall guarantee their soundness: if
the original program has a failing assertion, so will any instrumented program, regardless of the chosen
application strategy; that is, instrumentation of an incorrect program will never yield a correct program.
This aspect is discussed in Section 5.
    We shall also guarantee a weak form of completeness, to the effect that if an assertion that has not
been added to the program by the instrumentation fails in the instrumented program, then it will also
fail in the original program. As a result, any counterexample (for such an assertion) produced when
verifying the instrumented program can be transformed into a counterexample for the original program.
    Finally, for certain classes of programs, in Section 5.2 we shall guarantee completeness in the typical,
stricter sense. That is, if a program is correct and adheres to certain conditions, then there is an
instrumented program that is also correct, such that automatic verification has been made easier.

2.1      The Core Language
A simple programming language, containing loops and arrays, is used to present the instrumentation
framework.


                                                     6
     hTypei ::= Int | Bool | Array hTypei
     hExpr i ::= hDecimalNumber i | true | false | hVariablei
                |   hExpr i == hExpr i | hExpr i <= hExpr i | !hExpr i | hExpr i && hExpr i
                |   hExpr i || hExpr i | hExpr i + hExpr i | hExpr i * hExpr i | hExpr i/hExpr i
              | const(hExpr i) | select(hExpr i,hExpr i) | store(hExpr i,hExpr i,hExpr i)
     hProgi ::= skip | hVariablei = hExpr i | hProg i; hProgi | while (hExpr i) hProgi
                |   assert(hExpr i) | assume(hExpr i) | if (hExpr i) hProgi else hProgi


                                Figure 5: Syntax of the core language


                                                                                 x ∈ X , α(x) = σ
          hDecimalNumber i : Int         true : Bool         false : Bool             x:σ
              s:σ t:σ           s : Int t : Int          s : Int t : Int     s : Int t : Int
             s == t : Bool        s <= t : Bool              s + t : Int        s * t : Int
            s : Int t : Int         c : Bool      s : Bool t : Bool         s : Bool t : Bool
               s / t : Int         !c : Bool          s && t : Bool             s || t : Bool

                 t:σ                  a : Array σ t : Int         a : Array σ s : Int t : σ
           const(t) : Array σ           select(a,t) : σ            store(a,s,t) : Array σ


                             Figure 6: Typing rules of the core language


Syntax While our implementation works on programs represented as constrained Horn clauses [12],
i.e., is language-agnostic, for readability purposes we present our approach in the setting of an imperative
core programming language with data-types for unbounded integers, Booleans, and arrays, and assert
and assume statements. The language is deliberately kept simple, but is still close to standard C. The
main exception is the semantics of arrays: they are defined here to be functional and therefore represent
a value type. A notable deviation from C-like, imperative-style arrays is that the equality of two arrays
depends on the array contents, and not on a pointer value. Arrays have integers as index type and
are unbounded, and their signature and semantics are otherwise borrowed from the SMT-LIB theory of
extensional arrays [6]:
   • Constructing a constant array filled with x:                           const(x);
   • Reading the value of an array a at index i:                            select(a, i);
   • Updating an array a at index i with a new value x:                     store(a, i, x);
   • Comparing array a and b for equality:                                  a == b.
    The complete syntax of the core language is given in Figure 5. Programs are written using a vocabu-
lary X of typed program variables; the typing rules of the language are shown in Figure 6. As syntactic
sugar, we sometimes write a[i] instead of select(a, i), and a[i] = x instead of a = store(a, i, x).
We also use a = _ to mean that a is assigned to some constant array, for which we do not care about
the value of the elements.

Semantics We assume the Flanagan-Saxe extended execution model of programs with assume and
assert statements (see, e.g., [23]), in which executing an assert statement with an argument that
evaluates to false fails, i.e., terminates abnormally. An assume statement with an argument that evaluates
to false has the same semantics as a non-terminating loop. We denote by Dσ the domain of a program
                                                                             Z
type σ. The domain of an array type Array σ is the set of functions f : → Dσ . Partial correctness


                                                     7
properties of programs are expressed using Hoare triples {Pre} P {Post }, which state that an execution
of P , starting in a state satisfying Pre, never fails, and may only terminate in states that satisfy Post .
As usual, a program P is considered (partially) correct if the Hoare triple {true } P {true } holds.
    The evaluation of program expressions is modelled using a function J·Ks that maps program expres-
sions t of type σ to their value JtKs ∈ Dσ in the state s.

2.2     Instrumentation Operators
An instrumentation operator defines schemes to rewrite programs while preserving the meaning of the
existing program assertions. Without loss of generality, we restrict program rewriting to assignment
statements. Instrumentation can introduce ghost state by adding arbitrary fresh variables to the program.
The main part of an instrumentation consists of rewrite rules, which are schematic rules r = t    s, where
the meta-variable r ranges over program variables, t is an expression that can contain further meta-
variables (but not the left-hand side variable r), and s is a schematic program in which the meta-variables
from r = t might occur. Any assignment that matches r = t can be rewritten to s.
Definition 1 (Instrumentation Operator). An instrumentation operator is a tuple Ω = (G, R, I), where:
 (i) G = h(x1 , init 1 ), . . . , (xk , init k )i is a tuple of pairs of ghost variables and their initial values;
(ii) R is a set of rewrite rules r = t s, where s is a program operating on the ghost variables x1 , . . . , xk
     (and containing meta-variables from r = t);
(iii) I is a formula over the ghost variables x1 , . . . , xk , called the instrumentation invariant.
The rewrite rules R and the invariant I must adhere to the following constraints:
  1. The instrumentation invariant I is satisfied by the initial ghost values, i.e., it holds in the state
     {x1 7→ init 1 , . . . , xk 7→ init k }.
  2. For all rewrites r = t      s ∈ R the following conditions hold:
      (a) s terminates (normally or abnormally) for pre-states satisfying I, assuming that all meta-
          variables are ordinary program variables.
      (b) s does not assign to variables other than r or the ghost variables x1 , . . . , xk .
      (c) s preserves the instrumentation invariant: {I} s′ {I}, where s′ is s with every assert(e)
          statement replaced by an assume(e) statement.
      (d) s preserves the semantics of the assignment r = t, in the sense that the Hoare triple {I} z = t; s′ {z =
          r}, where z is a fresh variable, holds.
    The conditions imposed in the definition ensure that all instrumentations are correct, in the sense
that they are sound and weakly complete, as we show below. In particular, the instrumentation invariant
guarantees that the rewrites of program statements are semantics-preserving w.r.t. the original program,
and thus, the execution of any assert statement of the original program has the same effect before and
after instrumentation. The conditions can themselves be deductively verified to hold for each concrete
instrumentation operator, and that this check is independent of the programs to be instrumented, so
that an instrumentation operator can be proven correct once and for all.
    Importantly, an instrumentation operator Ω does itself not define which occurrences of program
statements are to be rewritten, but only how they are rewritten.
Definition 2 (Rewriting a program statement). A program statement v = e matches a rewrite rule
r=t     s if there is a substitution σ, replacing each meta-variable with a program expression, that maps
r to σ(r) = v and t to σ(t) = e.
    The result of rewriting v = e using the rule r = t    s is defined as follows:
 (i) If v does not occur in e, the result of rewriting v = e is the program σ(s), i.e., the right-hand side s
     of the rule, with meta-variables substituted with the expressions occurring in the assignment v = e.
 (ii) If v occurs in e, we first replace v = e with the two statements v’ = e; v = v’, for some
      fresh variable v’ that has the same type as v, and then rewrite the new assignment v’ = e using
      r=t     s.




                                                           8
          hExpr i ::= (λ(hVariablei,hVariablei).hExpr i) (hExpr i, hExpr i) |
                      quantQ (hExpr i,hExpr i,hExpr i,λ(hVariablei, hVariablei).hExpr i) |


                 Figure 7: Extension of the core language with quantified expressions

1  Int N = nondet ;
2  assume ( N > 0) ;
 3 Array Int a = const (0) ;

 4 Int i = 0;

 5 while ( i < N ) {

 6     a = store (a , i , i ) ;
 7     i = i + 1;
 8 }

 9 Bool b = \ forall (a , 0 , N , λ(i , x ) .( x == i ) ) ;

10 assert ( b ) ;




          Figure 8: Example of program to be verified using a quantified assert statement


     The procedure in second case (ii) has the purpose of ensuring that the right-hand side e is stable in
 s; otherwise, carrying out the assignment could have the effect of changing the value of expressions in e.
     Given a program P and the operator Ω, an instrumented program P ′ is derived by carrying out the
 following two steps: (i) variables x1 , . . . , xk and the assignments x1 = init 1 ; . . . ; xk = init k are added at
 the beginning of the program, and (ii) some of the assignments in P that match rewrite rules r = t                  s
 in Ω are rewritten as defined in Definition 2. We denote by Ω(P ) the set of all instrumented programs P ′
 that can be derived in this way.
     Two simplified examples of instrumentation operators were already given in Section 1. The reader is
 advised to return to those examples, and convince herself that the operators indeed satisfy the conditions
 required in Definition 1.


 3     Instrumentation Operators for Arrays
 We will now instantiate our framework for several classes of functions over arrays, targeting, in particular,
 the different kinds of quantifiers over arrays provided by ACSL [7]. Among others, we will obtain a more
 general and more precise version of the operator for the extended quantifier \max from Section 1.

 3.1     Instrumentation Operators for Quantification over Arrays
 To handle quantifiers in a programming setting, we extend the language defined in Figure 5 by adding
 quantifier expressions over arrays, as shown in Figure 7, where Q ranges over {∀, ∃}. We shall often use
 \forall for quant∀ , and \exists for quant∃ . We also extend the language with a lambda expression over
 two variables. The rationale is that quantified properties can often be expressed as a binary predicate,
 with the first argument corresponding to the value of an element and the second to the index.
     Using P(x0 ,i0 ) as shorthand for (λ(x,i).P)(x0 ,i0 ), the semantics of the new expressions can be
 defined formally as:

                        JquantQ (a, l, u, λ(x,i).P)Ks = Qi ∈ [l, u). JP(a[i],i)Ks

     As an example, consider the program in Figure 8, which uses forall to specify that every element
 in the array should equal its index. To verify this program, we define the instrumentation operator
 Ω∀,P in Figure 9. The operator is similar to Ωmax , which was introduced in Section 1.1, but, instead of
 tracking the maximum value, we use the ghost variable qu_P to track if the given property P holds for all



                                                          9
   Ω∀,P (Instrumentation operator)
     G∀,P (Ghost variables)
     qu_ar : Array Int, qu_lo, qu_hi : Int, qu_P : Bool
     init(qu_ar) = _, init(qu_lo) = 0, init(qu_hi) = 0
     init(qu_P) = true

     R∀,P (Rewrite rules)
     a’ = store(a, i, x);
        1   if ( qu_lo == qu_hi ||        i < qu_lo - 1 || i > qu_hi ||
        2        ( P (x , i ) && ! qu_P   && qu_lo <= i && i < qu_hi ) ) {
        3      qu_lo = i ;                // Reset , because either :
        4      qu_hi = i + 1;             // - tracking empty interval
        5      qu_P = P (x , i ) ;        // - storing far outside interval
        6   } else {                      // - might o v e r w r i t e sole false
        7      assert ( qu_ar == a ) ;
        8      qu_P = qu_P && P (x ,      i);
        9      if ( qu_lo - 1 == i )      {
       10            qu_lo = i ;          // D e c r e m e n t lower bound by 1
       11      } else if ( qu_hi ==       i) {
       12            qu_hi = i + 1;       // I n c r e m e n t upper bound by 1
       13      }
       14   }
       15   a ’ = store (a , i , x ) ;
       16   qu_ar = a ’;
     x = select(a, i);    similar to store
     b = \forall(a, l, u, λ(x,i).P);
        1   if ( u <= l ) {
        2     b = true ;
        3   } else {
        4     if ( qu_P ) {
        5        assert ( qu_ar == a && l >= qu_lo && u <= qu_hi ) ;
        6     } else {
        7        assert ( qu_ar == a && l <= qu_lo && u >= qu_hi ) ;
        8     }
        9     b = qu_P ;
       10   }


     I∀,P (Instrumentation Invariant)
     qu_lo = qu_hi ∨
         (qu_lo < qu_hi ∧ qu_P = forall(qu_ar, qu_lo, qu_hi,λ(x, i).P))



                     Figure 9: Instrumentation operator for universal quantification


elements in the tracked interval [qu_lo, qu_hi). Naturally, an instrumentation operator for existential
quantification can be defined in a similar fashion. When applying instrumentation operators for array
properties, such as Ω∀,P , we assume for simplicity a normal form of programs, into which every program
can be rewritten by introducing additional variables. In the normal form, store, select and forall
can only occur in simple assignment statements. For example, store is restricted to occur in statements
of the form: a’ = store(a, i, x).
    The rewrite rules can be justified as follows. For store, the first if-branch resets the tracking to
the singleton interval [i, i + 1) when accessing elements far outside of the currently tracked interval, or
if we are tracking the empty interval (as is the case at initialisation). If an access occurs immediately
adjacent to the currently tracked interval (e.g., if i = qu_lo − 1), then that element is added to the
tracked interval, and the value of qu_P is updated to also account for the value of P at index i. If instead
the access is within the tracked interval, then we either reset the interval (if qu_P is false) or keep the
interval unchanged (if qu_P is true). Rewrites of select are similar to store, except tracking does
not need to be reset when reading inside the tracked interval. For rewrites of quantified expressions, if


                                                            10
1  Int qu_lo = 0; qu_hi = 0; Int qu_ar = []; Bool qu_P = true ;
2  Int N = nondet ; assume ( N > 0) ; Array Int a = const (0) ; Int i = 0;
 3 while ( i < N ) {

 4      // Begin - instrumenta t io n
 5      if ( qu_lo == qu_hi || i < qu_lo - 1 || i > qu_hi ||
 6            ( i == i && ! qu_P && qu_lo <= i && i < qu_hi ) ) {
 7         qu_lo = i ; qu_hi = i + 1; qu_P = ( i == i ) ;
 8      } else {
 9         assert ( qu_ar == a ) ; qu_P = qu_P && i == i ;
10         if ( qu_lo - 1 == i ) {
11                qu_lo = i ;
12         } else if ( qu_hi == i ) {
13                qu_hi = i + 1;
14         }
15      }
16      a ’ = store (a , i , i ) ;
17      qu_ar = a ’;
18      // End - instrumenta ti o n
19      a = a ’; i = i + 1;
20 }

21 Bool b ;

22 // Begin - instrumenta ti on

23 if ( N <= 0) {

24   b = true ;
25 } else {

26   if ( qu_P ) {
27      assert ( qu_ar == a && 0 >= qu_lo && N <= qu_hi ) ;
28   } else {
29      assert ( qu_ar == a && 0 <= qu_lo && N >= qu_hi ) ;
30   }
31   b = qu_P ;
32 }

33 // End - instrumenta ti on

34 assert ( b ) ;




    Figure 10: Resulting program from applying the instrumentation Ω∀,λ(i,x).x=i to the program
    in Figure 8


 the quantified interval is empty, b is assigned true. Otherwise, assertions check that the tracked interval
 matches the quantified interval before assigning t to qu_P. If qu_P is true, then it is sufficient that
 quantification occurs over a sub-interval of the tracked interval, and vice versa if qu_P is false.
      The result of applying Ω∀,λ(i,x).x=i to the program in Figure 8 is shown in Figure 10. In the process
 of rewriting, we renamed the left-hand side of a = store(a, i, i) by introducing a fresh variable a’,
 following case (ii) of Definition 2. As exhibited by the experiments in Section 7, the resulting program
 is, in many cases, easier to handle for state-of-the-art verification tools. Note that the proposed instru-
 mentation operator is only one possibility among many. For example, one could track simultaneously
 several ranges over the array in question, or also track the index of some element in the array over which
 P holds, or make different choices on store operations outside of the tracked interval.

 3.2     Instrumentation Operators for Aggregations
 We now turn to defining instrumentation operators for any aggregation that can be formalised using
 monoid homomorphisms. As we shall show, this not only generalises ∀ and ∃, but also allows defining in-
 strumentation operators for the aggregations \sum, \product, \numof, \max, and \min. Such aggregation



                                                     11
   is supported in the specification languages JML [33] and ACSL [7] in the form of extended quantifiers,
   and is frequently needed for the specification of functional correctness properties. Although commonly
   available in specification languages, most verification tools do not support the verification of proper-
   ties specified using aggregation. Such properties instead typically have to be manually rewritten using
   standard quantifiers, pure recursive functions, or ghost code involving loops. This reduction step is
   error-prone, and represents an additional complication for automatic verification approaches, but can be
   elegantly handled using our proposed instrumentation framework.
   Definition 3 (Monoid). A monoid is a structure (M, ◦, e) consisting of a non-empty set M , a binary
   associative operation ◦ on M , and a neutral element e ∈ M . A monoid is called commutative if ◦ is
   commutative.
       We model finite intervals of arrays as strings over the monoid (D∗ , ·, ǫ) of finite sequences over some
   data domain D. The concatenation operator · is non-commutative. The aggregation or quantification
   of finite intervals of an array is then defined as a monoid homomorphism from (D∗ , ·, ǫ) to some target
   monoid.
   Definition 4 (Monoid Homomorphism). A monoid homomorphism is a function h : M1 → M2 between
   monoids (M1 , ◦1 , e1 ) and (M2 , ◦2 , e2 ) such that h(x ◦1 y) = h(x) ◦2 h(y) for all x, y ∈ M1 and h(e1 ) = e2 .
       For example, universal quantification can be modelled as a homomorphism to the monoid (B, ∧, true).
   A second example is the computation of the maximum (similarly, minimum) value in a sequence. For the
                                                                        Z
   domain of integers, the natural monoid to use is the algebra ( −∞ , max, −∞) of integers extended with
   −∞1 . A third example is the computation of the element sum of an integer sequence, modelled by the
                                                    Z
   homomorphism hsum to the target monoid ( , +, 0). The monoid in the last example, the computation
   of element sums, has the special property of being cancellative.
   Definition 5 (Cancellative Monoid). A monoid (M, ◦, e) is cancellative if one of the following equivalent
   properties hold:
      1. x ◦ y = x ◦ z implies y = z, and y ◦ x = z ◦ x implies y = z, for all x, y, z ∈ M .
      2. there are partial operations ◦−1   −1
                                       l , ◦r  : M × M ⇀ M such that (x ◦ y) ◦−1             −1
                                                                              r y = x and x ◦l (x ◦ y) = y,
         for all x, y ∈ M .
       In the case of a commutative cancellative monoid, it is not necessary to distinguish two separate
   functions ◦−1
              l , ◦r
                    −1
                        for left- and right-cancellation. We use the notation (x ◦ y) ◦−1 y in the commutative
   case.
       Cancellative monoids generalise the notion of a group, and are a useful special case in the context
   of instrumentation: aggregation operators based on cancellative monoids can be represented using a
   particularly efficient kind of instrumentation. An example of a cancellative (commutative) monoid is the
           Z
   group ( , +, 0) used to model \sum, which calculates the sum of the elements in an array.

   3.2.1    Programming Language with Aggregation
   We extend our core programming language a second time, this time adding support for aggregation
   of array values. We introduce the expressions aggregateM,h (hExpr i,hExpr i,hExpr i), and use monoid
   homomorphisms to formalise them. Recall that we use Dσ to denote the domain of a program type σ.
   Definition 6. Let Array σ be an array type, σM a program type, M a commutative monoid that is a
   subset of DσM , and h : Dσ∗ → M a monoid homomorphism. Let furthermore ar be an expression of type
   Array σ, and l and u be integer expressions. Then, aggregateM,h (ar ,l,u) is an expression of type σM ,
   defined as:

               JaggregateM,h (ar ,l,u)Ks = h(hJar Ks (JlKs ), Jar Ks (JlKs + 1), . . . , Jar Ks (JuKs − 1)i)     (1)

       Intuitively, the expression aggregateM,h (ar ,l,u) denotes the result of applying the homomorphism h
   to the slice ar [l .. u − 1] of the array ar . As a convention, in case u < l we assume that the result of
   aggregate is h(hi). As with array accesses, we assume also that aggregate only occurs in normalised
   statements of the form t = aggregateM,h (ar ,l,u).
       We define aggregation operators corresponding to all extended quantifiers found in ACSL, with the
   homomorphism h being uniquely defined by how it acts on singleton sequences. For example, for sum,
1 For machine integers, −∞ could be replaced with INT_MIN.




                                                            12
             (Extended) Quantifier                      Target Monoid             h generated by
             \sum(ar,l,u)                                (Z, +, 0)                    hxi 7→ x
             \min(ar,l,u)                             (Z+∞ , min, +∞)                 hxi 7→ x
             \max(ar,l,u)                             (Z−∞ , max , −∞)                hxi 7→ x
             \product(ar,l,u)                             (Z, ·, 1)                   hxi 7→ x
             \numof(ar,l,u,λ(x,i).P)                     (Z, +, 0)                 hbi 7→ b ? 1 : 0
             \forall(ar,l,u,λ(x,i).P)                     (B, ∧, true)           h(x, i)i 7→ P (x, i)
             \exist(ar,l,u,λ(x,i).P)                      (B, ∨, false )         h(x, i)i 7→ P (x, i)

   Table 1: Target monoid and homomorphism generator for all ACSL (extended) quantifiers


the homomorphism hsum is generated by the mapping hni 7→ n. Table 1 shows, for each operator, the
homomorphism and its domain monoid.
   One may observe here that aggregate, in a slightly extended form, subsumes the operator quantQ
previously introduced for ordinary quantifiers. For this, consider a generalised aggregate’ operator
that passes not only array elements, but also their indexes to a homomorphism:

          Jaggregate’M,h (ar ,l,u)Ks = h(h(Jar Ks (JlKs ), JlKs ), . . . , (Jar Ks (JuKs − 1), JuKs − 1)i)

For the quantifier \forall, we can then let M∀ be the monoid (B, ∧, true) and h∀ the homomorphism
generated by mapping value-index pairs h(x, i)i to the Boolean P (x, i).

3.2.2    An Instrumentation Operator for Non-Cancellative Monoids
We are now ready to define instrumentation operators that work for any aggregation that is based on a
monoid homomorphism. We start by considering the general case of monoids that are not (necessarily)
cancellative, and define an instrumentation operator that is parameterised on the target monoid (M, ◦, e)
and homomorphism h : Dσ∗ → M , as shown in Figure 11. The operator can be instantiated to obtain
instrumentation operators for any ACSL extended quantifier, with the respective target monoid and
homomorphism being as defined in Table 1. In such instances of the parameterised instrumentation
operator, (M, ◦, e) and h have to be replaced with their respective programming language implementation.
    The operator Ωnc is largely similar to the ones already defined for \max and \forall, wherefore
we refer the reader to Section 3.1 for an explanation of the intuition behind the operator. The main
difference is that the statements on lines 4 and 8 now use ◦ and h.
Theorem 1 (Correctness of Ωnc ). For any target monoid (M, ◦, e) and monoid homomorphism h : Dσ∗ →
M with implementations of ◦ and h that terminate and do not assign to any variables, the instrumentation
operator Ωnc ((M, ◦, e), h) is correct, i.e., it adheres to the constraints imposed by Definition 1.

Proof. Let (M, ◦, e) and h be such a target monoid and homomorphism. We will show that the instru-
mentation operator created by implementing Ωnc ((M, ◦, e), h) with terminating implementations of ◦ and
h that do not assign to any variables is correct.
    First, observe that qu_lo and qu_hi are initialised to the same value. Since the value of aggregation
over an empty interval is the monoid identity e, and ag_val is initialised to e, the invariant I is established
by the initial values assigned by G. It now remains to show that the rewrite rules adhere to the remaining
constraints.
    We will first show that a rewritten store terminates and satisfies the constraints in Definition 1.
It is easy to see that the instrumentation terminates, since no loop or recursion is introduced and the
implementations of ◦ and h are assumed to terminate. It is also easy to see that we only assign to
ghost variables and a’, and not to any other program variables, since ◦ and h do not assign to any
variables. Thus, the semantics is preserved, since the original store statement remains unchanged on
line 14 and the instrumentation code only assigns to ghost variables. Lastly, we must establish that the
invariant is preserved, i.e., that the new values of ag_val, ag_hi, ag_lo, and ag_ar satisfy the invariant.
For this, we distinguish three cases, each of which corresponds to a conditional block. In the first case,



                                                        13
   Ωnc ((M, ◦, e), h) (Instrumentation operator)
     Gnc (Ghost variables)
     ag_lo, ag_hi : Int, ag_ar : Array σ, ag_val : M
     init(ag_lo) = init(ag_hi) = 0, init(ag_val) = e, init(ag_ar) = _

     Rnc (Rewrite rules)
     a’ = store(a, i, x)
         1   if ( i == ag_lo - 1 && ag_lo != ag_hi ) {
         2        assert ( ag_ar == a ) ;
         3        ag_lo = ag_lo = i ;
         4        ag_val = h( x ) ◦ ag_val ;
         5   } else if ( i == ag_hi && ag_lo != ag_hi ) {
         6        assert ( ag_ar == a ) ;
         7        ag_hi = i ;
         8        ag_val = ag_val ◦ h( x ) ;
         9   } else {
        10        ag_val = h( x ) ;
        11        ag_lo = i ;
        12        ag_hi = i + 1;
        13   }
        14   a ’ = store (a , i , x ) ;
        15   ag_ar = a ’
      x = select(a, i)                          code similar to rewrites of store
      r = \aggregateM,h (a, l, u)
         1   if ( u <= l ) {
         2     t = e;
         3   } else {
         4     assert ( ag_ar == a && l == ag_lo && u == ag_hi ) ;
         5     t = gh_val ;
         6   }


     Inc (Instrumentation invariant)
     ag_lo ≤ ag_hi ∧ ag_val = aggregateM,h (ag_ar, ag_lo, ag_hi)



 Figure 11: Instrumentation operator for aggregation parameterised on a non-cancellative target
 monoid (M, ◦, e) and homomorphism h


we assume that i = ag_lo − 1 and ag_lo 6= ag_hi. Since the value of ag_lo is decreased, the first
conjunct, ag_lo ≤ ag_hi, is preserved. The following derivation shows that the second conjunct of the
invariant, ag_val = aggregateM,h (ag_ar, ag_lo − 1, ag_hi), is also preserved:

       ag_valnew = h(x) ◦ ag_valold
                   = h(x) ◦ aggregateM,h (ag_ar, ag_lo, ag_hi)                           {By Inc }
                   = h(x) ◦ h(hag_ar[ag_lo], . . . , ag_ar[ag_hi − 1]i)          {By Equation 1}
                   = h(hxi · hag_ar[ag_lo], . . . , ag_ar[ag_hi − 1]i)         {h homomorphism}
                   = h(hag_ar[ag_lo − 1], . . . , ag_ar[ag_hi − 1]i)            {x = ag_ar[i] and
                                                                                  i = ag_lo − 1}}
                   = aggregateM,h (ag_ar, ag_lo − 1, ag_hi)                      {By Equation 1}

The second case, in which i = gh_hi and ag_lo 6= ag_hi, follows symmetrically. In the last case, in
which i is different from gh_hi, gh_lo − 1, or it is the case that ag_lo = ag_hi, we reset the ghost
variables to track the singleton sequence. The invariant clearly holds afterwards.
    We omit the case for select statements as it is similar to store.
    Lastly, the instrumentation code for aggregate also satisfies the constraints in Definition 1: (a) The
instrumentation code obviously terminates. (b) It only assigns to the variable t. (c) Since the ghost


                                                   14
variables are not updated, the invariant is trivially preserved. (d) To show that the semantics is pre-
served, we distinguish two cases. In the case u <= l, we have defined the value of the aggregation
aggregateM,h (a, u, l) as equal to e in subsubsection 3.2.1, and therefore the semantics is preserved.
In the other case, the value of aggregateM,h (a, u, l) is equal to ag_val by the instrumentation in-
variant and therefore, by assigning ag_val to t, the semantics is preserved.

3.2.3    An Instrumentation Operator for Cancellative Monoids
When the target monoid is commutative and cancellative, we can track aggregate values faithfully even
when storing inside of the tracked interval, unlike in the non-cancellative case. Examples of cancellative
operators are the aggregates \sum and \numof.


   Ωc ((M, ◦, e), h) (Instrumentation operator)
     Gc (Ghost variables)
     ag_lo, ag_hi : Int, ag_ar : Array σ, ag_val : M
     init(ag_lo) = init(ag_hi) = 0, init(ag_val) = e, init(ag_ar) = _

     Rc (Rewrite rules)
     a’ = store(a, i, x)
          1   if ( i == ag_lo - 1 && ag_lo != ag_hi ) {
          2        assert ( ag_ar == a ) ;
          3        ag_lo = i ;
          4        ag_val = ag_val ◦ h( x ) ;
          5   } else if ( i == ag_hi && ag_lo != ag_hi ) {
          6        assert ( ag_ar == a ) ;
          7        ag_hi = i ;
          8        ag_val = ag_val ◦ h( x ) ;
          9   } else if ( ag_lo <= i && i < ag_hi ) {
         10        assert ( ag_ar == a ) ;
         11        ag_val =
         12          ag_val ◦−1 h( select (a , i ) ) ◦ (h( x ) ) ;
         13   } else {
         14        ag_val = h( x ) ;
         15        ag_lo = i ;
         16        ag_hi = i + 1;
         17   }
         18   a ’ = store (a , i , x ) ;
         19   ag_ar = a ’
        x = select(a, i)                             code similar to rewrites of store
        r = \aggregateM,h (a, l, u)
          1   if ( u <= l ) {
          2     t = e;
          3   } else {
          4     assert ( ag_ar == a && l == ag_lo && u == ag_hi ) ;
          5     t = gh_val ;
          6   }


     Ic (Instrumentation invariant)
     ag_lo ≤ ag_hi ∧ ag_val = aggregateM,h (ag_ar, ag_lo, ag_hi)



 Figure 12: Instrumentation operator for aggregation parameterised on a cancellative target
 monoid (M, ◦, e) and homomorphism h

    To this end, we have defined the instrumentation operator Ωc in Figure 12. This instrumentation
operator can be instantiated with a cancellative monoid (M, ◦, e) and a homomorphism h. The operator
differs from Ωnc in the rewrite rule for store operations, by adding a new else if branch (lines 9–12).
Since the monoid is cancellative and commutative, when storing inside of the tracked interval, we first
remove the current value at the index being written to using ◦−1 , and then add the new value using ◦.


                                                         15
Instrumentation operators for \sum and \numof can be defined in terms of Ωc , using the definitions in
Table 1. The following result establishes correctness.
Theorem 2 (Correctness of Ωc ). Ωc ((M, ◦, e), h) is an instrumentation operator, i.e., it adheres to the
constraints imposed in Definition 1.

Proof. Similar to the proof of Theorem 1.

Corollary 1. There are correct instrumentation operators for all ACSL (extended) quantifiers.

Proof. The non-cancellative cases (\forall, \exists, \product, \min, \max) follow from Theorem 1,
by instantiating (M, ◦, e) and h according to Table 1. The cancellative cases (\sum, \numof) follow
similarly from Theorem 2.

    It is worth pointing out that we view Ωnc and Ωc as a base recipe for how to implement instrumentation
operators for aggregation, but that one can further tailor the instrumentation to specific aggregations.
For example, the instrumentation operator for \forall in Figure 9 specialises the rewriting of the
aggregation, utilising that if a property holds for some portion of the array, then it also holds for a subset
of that portion.

3.2.4    Cancelling the Non-cancellative
Up until now, we have been using the same monoid to define the instrumentation operator, hence-
forth denoted as (Maggr , ◦aggr , eaggr ), as we used to define the semantics of the extended quantifier
itself. In this section, we create instrumentation operators using a different, cancellative monoid, de-
noted as (Minstr , ◦instr , einstr ), and parameterise our instrumentation operator on another homomor-
phism g : Minstr → Maggr to map from the instrumentation monoid to the aggregation monoid when
instrumenting an assignment using aggregate. This means we slightly alter the definition of Ωc in
Figure 12 to be parameterised on a homomorphism g and we change line 5 of the rewrite rule for
r = aggregateM,h (a, u, l) to t = g(ag_val).
    We can use this technique to create a cancellative instrumentation operator for universal and existen-
tial quantification, instead of the non-cancellative operator we defined in subsubsection 3.2.2. By noting
that an existential quantifier for a predicate P is true for an interval if the number of elements satisfying P
in that interval is larger than 0, we can reuse the cancellative monoid we defined for \numof. Whenever
we instrument an assignment using \exists, we use the homomorphism g∃,P (see Equation 2) to map
the number of elements satisfying the predicate to the result of the existential quantifier. This now allows
us to define a stronger instrumentation operator for existential quantification as in Equation 3.

                                                            if c > 0
                                                    
                                                def   true
                                       g∃,P (c) =                                                            (2)
                                                      false otherwise
                                           def
                                                     Z
                                     Ω∃,P = Ωc (( , +, 0) , hnumof ,P , g∃,P )                              (3)

A similar technique can be used to create a cancellative operator for \product. By noting that mul-
tiplication is cancellative over integers if we explicitly exclude 0, it makes sense to define a monoid for
multiplication in which the elements are tuples (p, c) where p is the product of the non-zero elements and
c is the number of elements equal to zero. This cancellative monoid can then be used to define Ωprod :

                                                                               Z         N
                                                             n                     o
                                                         def
                                                 Mprod = (p, c) | p ∈ 6=0 , c ∈
                                                            def
                                  (p1 , c1 ) ◦prod (p2 , c2 ) = (p1 · p2 , c1 + c2 )
                                                            def
                                              eprod = (1, 0)
                                                           (x, 0) if x 6= 0
                                                         
              hprod homomorphism generated by hxi 7→
                                                           (1, 1) otherwise
                                                                 if c = 0
                                                         
                                                     def   p
                                      gprod ((p, c)) =
                                                           0     otherwise
                                                    Ωprod = Ωc ((Mprod , ◦prod , eprod ), hprod , gprod )



                                                         16
3.3    Deductive Verification of Instrumentation Operators
As stated in Section 2.2, instrumentation operators may be verified independently of the programs to
be instrumented. The operators described in this article, i.e., operators for the (extended) quantifiers
listed in Table 1 and the operator in Figure 4, have been verified in the verification tool Frama-C [15].
The verification checks that the operators adhere to the constraints listed in Definition 1. The verified
instrumentations are adaptations for the C language semantics and execution model. More specifically,
the adapted operators assume C native arrays, rather than functional ones.


4     Application of Multiple Instrumentation Operators
The instrumentation operators considered so far have instrumented programs for a single, specific type
of property, such as the Ωmax operator for programs containing the \max extended quantifier. In many
cases this is sufficient, and the appropriate operator can be selected manually or by some simple syntactic
analysis of the program to be verified. It is also common, however, that programs have to be rewrit-
ten multiple times to obtain an instrumented program that can be verified easily. This happens, for
instance, whenever a program contains occurrences of multiple different extended quantifiers, or multiple
occurrences of the same quantifier.
    There are several ways to handle such cases in our framework. Naturally, instrumentation can be
iterated: starting with a program P = P0 , a chain P0 , P1 , P2 , . . . , Pk can be constructed in which each
Pi+1 is obtained by applying some instrumentation operator to Pi . If the final program Pk can successfully
be verified, the correctness of P = P0 follows.
    Multiple instrumentation operators can also be composed to create new operators, which can instru-
ment a program for many different properties, or many different occurrences of the same type of property,
at once.
Definition 7 (Composition of Instrumentation Operators). Two instrumentation operators Ω = (G, R, I)
and Ω′ = (G′ , R′ , I ′ ), with distinct ghost variables, can be composed to create a new instrumentation op-
erator Ω′′ = Ω k Ω′ :
                                                 def
                                          Ω′ k Ω = (G ∪ G′ , R ∪ R′ , I ∧ I ′ )                           (4)
   The operators having distinct ghost variables means that, if vars (G) is a function returning all the
variable names in G (i.e., the first element of each tuple), then vars(G) ∩ vars(G′ ) = ∅. Note that it is
possible to compose two operators of the same type, as long as the ghost variable names are substituted
with fresh ones.
Lemma 1 (Correctness of Ω k Ω′ ). If Ω = (G, R, I) and Ω′ = (G′ , R′ , I ′ ) are both correct instrumentation
operators (i.e., they adhere to Definition 1), then the composed instrumentation operator Ω k Ω′ is also
correct, i.e., it adheres to the conditions imposed in Definition 1.

Proof. Let Ω = (G, R, I), Ω′ = (G′ , R′ , I ′ ) and Ω′′ = Ω k Ω′ = (G′′ , R′′ , I ′′ ).
    By Definition 1, I and I ′ are invariants over only the the variables in G and G′ , respectively. Since
the sets of variables defined G and G′ are disjoint, then it follows that their initial values also establish
I ∧ I ′.
    Since the rewrite rules are not changed, it follows that that they still terminate and assign only to
the allowed variables.
    For the remaining two constraints, we consider the rewrite rules from R (the proof is symmetrical for
the rules from R′ ). Since the rules in R preserve the invariant I and we start from a stronger invariant
I ∧ I ′ , it follows I must hold afterwards. Since the rules in R do not mention the variables in G′ , I ′
must also still hold, and I ∧ I ′ is preserved. Similarly, since the rules in R preserve the semantics of the
original statement under I, it must also do so under the stronger I ∧ I ′ .


5     Correctness of Instrumentation Operators
This section explains how we can reason about the correctness of instrumentation operators. For this, in
Section 5.1 we introduce the two notions of soundness and weak completeness, which are properties that
hold by construction for every instrumentation operator. In Section 5.2 we show that for certain classes
of programs, the instrumentation operators are also complete in a stronger sense.


                                                     17
5.1    Soundness and Weak Completeness
Verification of an instrumented program produces one of two possible results: a witness if verification
is successful, or a counterexample otherwise. A witness consists of the inductive invariants needed to
verify the program, and is presented in the context of the programming language: it is translated back
from the back-end theory used by the verification tool, and is a formula over the program variables and
the ghost variables added during instrumentation. A counterexample is an execution trace leading to a
failing assertion.
Definition 8 (Soundness). An instrumentation operator Ω is called sound if for every program P and
instrumented program P ′ ∈ Ω(P ), whenever there is an execution of P where some assert statement
fails, then there also is an execution of P ′ where some assert statement fails.
    Equivalently, existence of a witness for an instrumented program entails existence of a witness for
the original program, in the form of a set of inductive invariants solely over the program variables.
Notably, because of the semantics-preserving nature of the rewrites under the instrumentation invariant,
a witness for the original program can be derived from one for the instrumented program. One such
back-translation is to add the instrumentation invariant as a conjunct to the original witness, and to add
existential quantifiers for the ghost variables.
Example 1. To illustrate the back-translation, we return to the instrumentation operator from Figure 4
and the example program from Figure 3. The witness produced by our verification tool in this case is the
formula:

                  i = x_shad ∧ x_sq + x_shad = 2s ∧ N ≥ i ∧ N ≥ 1 ∧ 2s ≥ i ∧ i ≥ 0

After conjoining the instrumentation invariant x_sq = x_shad2 and adding existential quantifiers, we
obtain an inductive invariant that is sufficient to verify the original program:
                           ∃xsq , xshad . (i = xshad ∧ xsq + xshad = 2s ∧
                                  N ≥ i ∧ N ≥ 1 ∧ 2s ≥ i ∧ i ≥ 0 ∧ xsq = x2shad )
Definition 9 (Weak Completeness). The operator Ω is called weakly complete if for every program P
and instrumented program P ′ ∈ Ω(P ), whenever an assert statement that has not been added to the
program by the instrumentation fails in the instrumented program P ′ , then it also fails in the original
program P .
    Similarly to the back-translation of invariants, when verification fails, counterexamples for assertions
of the original program, found during verification of the instrumented program, can be translated back
to counterexamples for the original program. We thus obtain the following result.
Theorem 3 (Soundness and weak completeness). Every instrumentation operator Ω is sound and weakly
complete.

Proof. Let Ω = (G, R, I) be an instrumentation operator. Since I is a formula over ghost variables only,
which holds initially and is preserved by all rewrites, I is an invariant of the fully instrumented program.
This entails that rewrites of assignments are semantics-preserving. Furthermore, since instrumentation
code only assigns to ghost variables or to r (i.e., the left-hand side of the original statement), program
variables have the same valuation in the instrumented program as in the original one. Furthermore, since
all rewrites are terminating under I, the instrumented program will terminate if and only if the original
program does.
     In the case when verification succeeds, and a witness is produced, weak completeness follows vacuously.
A witness consists of the inductive invariants sufficient to verify the instrumented program. Thus, they are
also sufficient to verify the assertions existing in the original program, since assertions are not rewritten
and all program variables have the same valuation in the original and the instrumented programs. Since
a witness for the instrumented program can be back-translated to a witness for the original program, any
failing assertion in the original program must also fail after instrumentation, and Ω is therefore sound.
     In the case when verification fails, soundness follows vacuously, and if the failing assertion was added
during instrumentation, also weak completeness follows. If the assertion existed in the original program,
since such assertions are not rewritten, and since program variables have the same valuation in the
instrumented program as in the original program, then any counterexample for the instrumented program
is also a counterexample for the original program, when projected onto the program variables.


                                                     18
5.2     Completeness
Weak completeness of an instrumentation operator only guarantees that instrumentation does not affect
the validity of assertions that are left intact by the instrumentation. A “proper” notion of completeness
would state something considerably stronger, namely, that for any correct program, there is a program in
the instrumentation space of the operator that is also correct – with the intention that the instrumented
program can be automatically verified. This latter aspect can be captured by restricting the operators
or instructions that the instrumented program is allowed to contain.
    To formalise this notion of completeness, let A denote a class of programs; A could, for instance,
contain all programs that do not use certain aggregation operators, and which will therefore be handled
well by a given back-end solver. For a program P and an instrumentation operator Ω, we then denote
by ΩA (P ) = Ω(P ) ∩ A the set of instrumented versions of P that belong to A.
Definition 10 (A-Relative Completeness). Let Ω be an instrumentation operator, A a class of programs,
and P a program. We say that Ω is complete for P and A if and only if the correctness of P implies the
correctness of some instrumented program P ′ ∈ ΩA (P ):

                                 correct(P ) ⇒ ∃P ′ ∈ ΩA (P ). correct(P ′ )

We denote with PΩA the class of programs for which Ω is complete for A.
    Note that the above notion of A-relative completeness assumes that a single application of an instru-
mentation operator suffices to eliminate, in the program P , all problematic constructs of the type for
which the operator is defined. This, of course, is a strong assumption. In many cases, a single application
will not suffice, but a series of applications of the same operator may achieve the task. Fortunately, it
is straightforward to generalise the definition of A-relative completeness for this case. Let Ω∗ (P ) denote
the set of programs that result from applying the instrumentation operator Ω to the program P any
finite number of times in a sequence. One can then define Ω∗A (P ) = Ω∗ (P ) ∩ A, and adapt Definition 10
accordingly. We do not lose any generality by iteratively applying the same operator a finite number of
times, since we can leverage Definition 7 to compose multiple, different operators into a single operator
that subsumes its parts.
    The notion of A-relative completeness can only be of practical value if one can formulate conditions
on programs that are sufficient for a program to belong to the class PΩA . The approach we take here is
to formulate, for concrete instrumentation operators Ω and program classes A, conditions on programs P
that ensure that there is a program P ′ in the instrumentation space ΩA (P ) in which none of the assertions
added to P by the instrumentation fails. By virtue of weak completeness, Ω must then be complete for P
and A.

5.2.1    Completeness Conditions for Non-Cancellative Operators
As the base case, we focus on the class AB of programs in our core language that do not contain any
aggregation expressions. Completeness with respect to the class AB captures the ability of an operator
to eliminate aggregation expressions from a program; the resulting program can then be processed by
many existing software verification tools, which may be unable to handle aggregation, but are otherwise
fully automatic.
Definition 11 (Class Pnc ((M, ◦, e), h)). For given target monoid (M, ◦, e) and monoid homomorphism
h : Dσ∗ → M , we define Pnc ((M, ◦, e), h) as the class of programs P satisfying the following conditions:
  1. The program P contains exactly one statement r = \aggregateM,h (a, l, u) involving aggregation, for
     an array variable a : Array σ.
  2. In any execution of P , prior to aggregation the array elements a[i] between l and u − 1 are either
     read using select(a, i) or updated with a = store(a, i, x).
  3. These selects and stores occur sequentially, starting at l and ending at u − 1.
  4. No other accesses or assignments to a occur in P .
    It should be pointed out that the class Pnc is a semantic class; in fact, it is not decidable whether a
given program belongs to Pnc or not, since conditions 2–4 cannot be checked effectively in the general
case. The criteria are still useful to characterise cases in which the non-cancellative instrumentation
operator can succeed. For instance, our motivating example in Figure 1 satisfies our conditions, which


                                                     19
tells us that we successfully apply the instrumentation operator Ωmax to obtain an instrumented program
without extended quantifiers.
Theorem 4 (Completeness of Pnc ((M, ◦, e), h)). For a given target monoid (M, ◦, e) and monoid ho-
momorphism h : Dσ∗ → M , let Ω = Ωnc ((M, ◦, e), h). Then, Ω is complete for every program in the
class Pnc ((M, ◦, e), h) and AB , i.e., Pnc ((M, ◦, e), h) ⊆ PΩAB .

Proof. Let (M, ◦, e) be a target monoid, h : Dσ∗ → M be a monoid homomorphism and Ω = Ωnc ((M, ◦, e), h).
Let P be a program satisfying the conditions of Definition 11, i.e., let P ∈ Pnc . Assume that P is correct,
i.e., that correct(P ) holds.
     Let P ′ ∈ Ω(P ) be the instrumented program in which the statement r = \aggregateM,h (a, l, u) and
all select and store operations have been rewritten. Clearly, P ′ ∈ AB , and hence P ′ ∈ ΩAB (P ).
     Next assume, for the sake of obtaining a contradiction, that P ′ is not correct, i.e., that ¬correct(P ′ )
holds. By virtue of the definition of Ω (see Figure 11), and by weak completeness of Ω, one of the
following assertions, added by the instrumentation, must have failed:
  1. an assert(ag_ar == a) in an instrumentation of store,
  2. an assert(ag_ar == a) in an instrumentation of select, or
  3. an assert(ag_ar == a && l == ag_lo && h == ag_hi).
The next step of the proof is a case analysis on each of the 5 conjuncts. We show here one case, as the
other cases follow similarly.
    Assume that the assertion in an instrumented store statement failed. This means that the ghost
array and actual array must be unequal. Since the interval is non-empty whenever ag_ar == a, this
means that there must be some assignment to a that does not update the ghost variable. The former
contradicts our choice of P ′ that says that all store and select operations to a have been rewritten.
Since the interval is non-empty and we only increase the size of the interval through store or select
statements, the latter implies that there is an assignment to a after a store or select, which contradicts
condition 4.
    Hence, P ′ must be correct, i.e., correct(P ′ ) holds, and therefore, by Definition 10, P ∈ PΩAB .

5.2.2    Completeness Conditions for Cancellative Operators
We can give a similar characterisation as in Definition 11 also for cancellative operators. As in the
previous section, let AB be the programs that do not contain aggregation expressions.
Definition 12 (Class Pc ((M, ◦, e), h)). For given cancellative and commutative target monoid (M, ◦, e)
and monoid homomorphism h : Dσ∗ → M , we define Pc ((M, ◦, e), h) as the class of programs P satisfying
the following conditions:
  1. The program P contains exactly one statement r = \aggregateM,h (a, l, u) involving aggregation, for
     an array variable a : Array σ.
  2. In any execution of P , prior to aggregation, each index i between l and u − 1 is either read using
     select(a, i) or written to using a = store(a, i, x). We distinguish the first operation that
     writes to a specific index from all subsequent operations and call the first operation that writes to a
     specific index a frontier-expanding operation.
  3. The indices that are accessed by frontier-expanding operations occur sequentially, starting at index
     l and ending at u − 1.
  4. All other accesses to a only operate on indices which have already been accessed by frontier-expanding
     operations.
Theorem 5 (Completeness of Pc ((M, ◦, e), h)). For given cancellative and commutative target monoid
(M, ◦, e) and monoid homomorphism h : Dσ∗ → M , let Ω = Ωc ((M, ◦, e), h). Then, Ω is complete for the
class Pc ((M, ◦, e), h) and AB , i.e., Pc ((M, ◦, e), h) ⊆ PΩAB .

Proof. The proof of Theorem 5 follows closely that of Theorem 4.




                                                    20
    Input: Program P ; statements S; instrumentation space R; oracle correct.
    Result: Instrumentation r ∈ R with correct(Pr ); Incorrect; or Inconclusive.
  1 begin
  2    Cand ← R;
  3    while Cand 6= ∅ do
  4       pick r ∈ Cand ;
  5       if correct(Pr ) then
  6           return r;
  7       else
  8           cex ← counterexample path for Pr ;
  9           if failing assertion in cex also exists in P then
                  /* cex is also a counterexample for P                                              */
 10               return Incorrect;
 11           else
                  /* instrumentation on cex may have been incorrect                                  */
 12               C ′ ← {p ∈ C | ins r (p) occurs on cex };
 13               Cand ← Cand \ {r′ ∈ Cand | r(s) = r′ (s) for all p ∈ C ′ };
 14           end
 15       end
 16    end
 17    return Inconclusive;
 18 end

            Algorithm 1: Counterexample-guided instrumentation search


6     Instrumentation Application Strategies
We will now define a counterexample-guided search procedure to discover applications of instrumentation
operators that make it possible to verify a program.
    For our algorithm, we assume again that we are given an oracle correct that is able to check the
correctness of programs after instrumentation. Such an oracle could be approximated, for instance,
using a software model checker. The oracle is free to ignore all functions, like aggregation, we are trying
to eliminate by instrumentation; for instance, in Figure 3, the oracle can over-approximate the term N*N
by assuming that it can have any value. We further assume that C is the set of control points of a
program P corresponding to the statements to which a given set of instrumentation operators can be
applied. For each control point p ∈ C, let Q(p) be the set of rewrite rules applicable to the statement
at p, including also a distinguished value ⊥ that expresses that p is not modified. For the program in
Figure 3, for instance, the choices could be defined by Q(A) = Q(B) = {(R1), ⊥}, Q(C)          S = {(R2), ⊥},
and Q(D) = {(R4), ⊥}, referring to the rules in Figure 4. Any function r : C → p∈C Q(p) with
r(p) ∈ Q(p) willSthen define one possible program instrumentation. We will denote the set of well-typed
functions C → p∈C Q(p) by R, and the program obtained by rewriting P according to r ∈ R by Pr .
We further denote the control point in Pr corresponding to some p ∈ C in P by ins r (p).
    Algorithm 1 presents our algorithm to search for instrumentations that are sufficient to verify a
program P . The algorithm maintains a set Cand ⊆ R of remaining ways to instrument P , and in each
loop considers one of the remaining elements r ∈ Cand (line 4). If the oracle manages to verify Pr in
line 5, due to soundness of instrumentation the correctness of P has been shown (line 6); if Pr is incorrect,
there has to be a counterexample ending with a failing assertion (line 8). There are two possible causes
of assertion failures: if the failing assertion in Pr already existed in P , then due to the weak completeness
of instrumentation also P has to be incorrect (line 10). Otherwise, the program instrumentation has to
be refined, and for this from Cand we remove all instrumentations r ′ that agree with r regarding the
instrumentation of the statements occurring in the counterexample (line 13).
    Since R is finite, and at least one element of Cand is eliminated in each iteration, the refinement
loop terminates. The set Cand can be exponentially big, however, and therefore should be represented


                                                     21
symbolically; using BDDs, or using an SMT solver managing the set of blocking constraints from line 13.
   We can observe soundness and completeness of the algorithm w.r.t. the considered instrumentation
operators.
Lemma 2 (Correctness of Algorithm 1). Algorithm 1 is sound and, in a certain sense, complete:
    1. If Algorithm 1 returns an instrumentation r ∈ R, then Pr and P are correct.
    2. If Algorithm 1 returns Incorrect , then P is incorrect.
    3. If there is r ∈ R such that Pr is correct, then Algorithm 1 will return r ′ such that Pr′ is correct.

Proof. Algorithm 1 will return an instrumentation r of when it has derived that Pr is correct; due to the
soundness of instrumentation operators, then also P is correct.
    Algorithm 1 will return Incorrect only when it has discovered a counterexample for Pr that ends in
a failing assertion that also occurs in P , i.e., that has not been introduced as a part of instrumentation.
Due to the weak completeness of instrumentation operators, then also P is incorrect.
    Assuming that there is an r such that Pr is correct, the correctness also of P follows. Algorithm 1 can
then not return the result Incorrect . To see that Algorithm 1 will eventually find some instrumentation r ′
such that Pr′ is correct, note that the algorithm will in lines 12–13 only eliminate instrumentations r ′′
such that Pr′′ is incorrect.


7      Evaluation
To evaluate our instrumentation framework, we have implemented the instrumentation operators for
quantifiers and aggregation over arrays. We evaluate this implementation on benchmarks taken from
SV-COMP, as well as a set of C programs by ourselves that use \min, \max, \sum, and \forall.

7.1      Implementation
Our implementation is done in the setting of constrained Horn clauses (CHCs), by adding the rewrite
rules defined in Section 3 to Eldarica [30], an open-source solver for CHCs. We also implemented the
automatic application of the instrumentation operators, largely following Algorithm 1, but with a few
minor changes due to the CHC setting. The CHC setting makes our implementation available to various
CHC-based verification tools, for instance JayHorn (Java) [32], Korn (C) [19], RustHorn (Rust) [36],
SeaHorn (C/LLVM) [26], and TriCera (C) [20].
    In order to evaluate our approach at the level of C programs, we extended TriCera, an open-source
assertion-based model checker that translates C programs into a set of CHCs and relies on Eldarica
as back-end solver. TriCera is extended to parse quantifiers and aggregation operators in C programs
and to encode them as part of the translation into CHCs. We call the resulting tool chain MonoCera.
An artefact that includes MonoCera and the benchmarks is available online [5].
    To handle complicated access patterns, for instance a program processing an array simultaneously
from the beginning and from the end, the implementation can simultaneously apply multiple instrumen-
tation operators; the number of operators is incremented when Algorithm 1 returns Inconclusive.

7.2      Experiments and Comparisons
To assess our implementation, we assembled a test suite and carried out experiments comparing Mono-
Cera with the state-of-the-art C model checkers CPAchecker 2.1.1 [11], SeaHorn 10.0.0 [26] and
TriCera 0.2. It should be noted that deductive verification frameworks, such as Dafny and Frama-C,
can handle, for example, the program in Figure 8, if they are provided with a manually written loop
invariant. Since MonoCera relies on automatic techniques for invariant inference, we only benchmark
against tools using similar automatic techniques. We also excluded VeriAbs [1], since its licence does
not permit its use for scientific evaluation.
   The tools were set up, as far as possible, with equivalent configurations; for instance, to use the
SMT-LIB theory of arrays [6] in order to model C arrays, and a mathematical (as opposed to machine-
based) semantics of integers. CPAchecker was configured to use k-induction [10], which was the only
configuration that worked in our tests using mathematical integers. SeaHorn was run using the default



                                                      22
                   Verification results                    Ver. time           Inst. space     Inst. steps
            #Tests Mono Tri       Sea CPA               Min Max     Avg          Max Avg        Max    Avg
     \min    17      9       2     2    2               22     59    33           27   11        55     24
     \max    12      8       2     3    3               21    285    76          108   21        96     30
     \sum    26     16       3     3    3               26    245    78          2916 188       284     36
     \forall 96     30       1     0    2               14    236    91         59049 2446      334     59

     Table 2: Results for MonoCera (Mono), TriCera (Tri), SeaHorn (Sea), and CPA-
     checker (CPA). For MonoCera, also statistics are given for verification time (s), size of
     the instrumentation search space, and search iterations.

    settings. All tests were run on a Linux machine with AMD Opteron 2220 SE @ 2.8 GHz and 6 GB RAM
    with a timeout of 300 seconds.

    Test Suite The comparison includes a set of programs calculating properties related to the quantifi-
    cation and aggregation properties over arrays. The benchmarks and verification results are summarised
    in Table 2. The benchmark suite contains programs ranging from 16 to 117 LOC, and is comprised of
    two parts: (i) 117 programs taken from the SV-COMP repository [9], and (ii) 26 programs crafted by
    the authors (\min: 6, \max: 8, \sum: 9, \forall: 3).
        To construct the SV-COMP benchmark set for MonoCera, we gathered all test files from the
    directories prefixed with array or loop, and singled out programs containing some assert statement
    that could be rewritten using a quantifier or an aggregation operator over a single array. For example,
    loops of the shape:
1   for ( int i = 0; i < N ; i ++)
2     assert ( a [ i ] <= 0)
    can be rewritten using \forall or \max. We created a benchmark for each possible rewriting; for
    instance, in the case of \max, by rewriting the loop into
1   assert (\ max (a , 0 , N ) <= 0)

    The original benchmarks were used for the evaluation of the other tools, none of which supported (ex-
    tended) quantifiers.
        In (ii), we crafted 12 programs that make use of aggregation or quantifiers, and derived further bench-
    marks by considering different array sizes (10, 100 and unbounded size). One combination (unbounded
    array inside a struct) had to be excluded, as it is not valid C. In order to evaluate other tools on our
    crafted benchmarks, we reversed the process described for the SV-COMP benchmarks and translated
    the operators into corresponding loop constructs.

    Results In Table 2, we present the number of verified programs per instrumentation operator for each
    tool, as well as further statistics for MonoCera regarding verification times and instrumentation search
    space. The “Inst. space” column indicates the size of the instrumentation search space (i.e., number
    of instrumentations producible by applying the non-deterministic instrumentation operator). The “Inst.
    steps” column indicates the number of attempted instrumentations, i.e., number of iterations in the
    while-loop in Algorithm 1. In our implementation, the check in Algorithm 1, line 5, can time out and
    cause the check to be repeated at a later time with a greater timeout, which can lead to more iterations
    than the size of the search space. In Appendix A, we list results per benchmark for each tool.
        For the SV-COMP benchmarks, CPAchecker managed to verify 1 program, while SeaHorn and
    TriCera could not verify any programs. MonoCera verified in total 42 programs from SV-COMP.
    Regarding the crafted benchmarks, several tools could verify the examples with array size 10. However,
    when the array size was 100 or unbounded, only MonoCera succeeded. This is because only MonoCera
    could infer the quantified invariants needed to prove unbounded safety of those benchmarks.


    8     Related Work
    It is common practice, in both model checking and deductive verification, to translate high-level spec-
    ifications to low-level specifications prior to verification (e.g., [14, 18, 13, 37]). Such translations often


                                                         23
make use of ghost variables and ghost code, although relatively little systematic research has been done
on the required properties of ghost code [22]. The addition of ghost variables to a program for track-
ing the value of complex expressions also has similarities with the concept of term abstraction in Horn
solving [3]. To the best of our knowledge, we are presenting the first general framework for automatic
program instrumentation.
     A lot of research in software model checking considered the handling of standard quantifiers ∀, ∃ over
arrays. In the setting of constrained Horn clauses, properties with universal quantifiers can sometimes
be reduced to quantifier-free reasoning over non-linear Horn clauses [13, 37]. Our approach follows the
same philosophy of applying an up-front program transformation, but in a more general setting. Various
direct approaches to infer quantified array invariants have been proposed as well: e.g., by extending
the IC3 algorithm [27], syntax-guided synthesis [21], learning [24], by solving recurrence equations [29],
backward reachability [3], or superposition [25]. To the best of our knowledge, such methods have not
been extended to aggregation.
     Deductive verification tools usually have rich support for quantified specifications, but rely on auxiliary
assertions like loop invariants provided by the user, and on SMT solvers or automated theorem provers
for quantifier reasoning. Although several deductive verification tools can parse extended quantifiers, few
offer support for reasoning about them. Our work is closest to the method for handling comprehension
operators in Spec# [35], which relies on code annotations provided by the user, but provides heuristics to
automatically verify such annotations. The code instrumentation presented in this article has similarity
with the proof rules in Spec#; the main differences are that our method is based on an upfront program
transformation, and that we aim at automatically finding required program invariants, as opposed to
only verifying their correctness. The KeY tool provides proof rules similar to the ones in Spec# for some
of the JML extended quantifiers [2]; those proof rules can be applied manually to verify human-written
invariants. The Frama-C system [15] can parse ACSL extended quantifiers [7], but, to the best of our
knowledge, none of the Frama-C plugins can automatically process such quantifiers. Other systems, e.g.,
Dafny [34], require users to manually define aggregation operators as recursive functions.
     In the theory of algebraic data-types, several transformation-based approaches have been proposed
to verify properties that involve recursive functions or catamorphisms [31, 17]. Aggregation over arrays
resembles the evaluation of recursive functions over data-types; a major difference is that data-types are
more restricted with respect to accessing and updating data than arrays.
     Array folds logic (AFL) [16] is a decidable logic in which properties on arrays beyond standard quan-
tification can be expressed: for instance, counting the number of elements with some property. Similar
properties can be expressed using automata on data words [41], or in variants of monadic second-order
logic [38]. Such languages can be seen as alternative formalisms to aggregation or extended quantifiers;
they do not cover, however, all kinds of aggregation we are interested in. Array sums cannot be expressed
in AFL or data automata, for instance.


9     Conclusion
We have presented a framework for automatic and provably correct program instrumentation, allowing
the automatic verification of programs containing certain expressive language constructs, which are not
directly supported by the existing automatic verification tools. Our experiments with a prototypical im-
plementation, in the tool MonoCera, show that our method is able to automatically verify a significant
number of benchmark programs involving quantification and aggregation over arrays that are beyond
the scope of other tools.
    There are still various other benchmarks that MonoCera (as well as other tools) cannot verify.
We believe that many of those benchmarks are in reach of our method, because of the generality of
our approach. Ghost code is known to be a powerful specification mechanism; similarly, in our setting,
more powerful instrumentation operators can be easily formulated for specific kinds of programs. In
future work, we therefore plan to develop a library of instrumentation operators for different language
constructs (including arithmetic operators), non-linear arithmetic, other types of structures with regular
access patterns such as binary heaps, and general linked-data structures. We also plan to refine our
method for showing incorrectness of programs more efficiently, as the approach is currently applicable
mainly for verifying correctness.




                                                      24
References
 [1] Mohammad Afzal, Supratik Chakraborty, Avriti Chauhan, Bharti Chimdyalwar, Priyanka Darke,
     Ashutosh Gupta, Shrawan Kumar, Charles Babu M, Divyesh Unadkat, and R. Venkatesh. Veriabs
     : Verification by abstraction and test generation (competition contribution). In Armin Biere and
     David Parker, editors, Tools and Algorithms for the Construction and Analysis of Systems - 26th
     International Conference, TACAS 2020, Held as Part of the European Joint Conferences on Theory
     and Practice of Software, ETAPS 2020, Dublin, Ireland, April 25-30, 2020, Proceedings, Part II,
     volume 12079 of Lecture Notes in Computer Science, pages 383–387. Springer, 2020.
 [2] Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, Reiner Hähnle, Peter H. Schmitt, and Mattias
     Ulbrich, editors. Deductive Software Verification - The KeY Book - From Theory to Practice, volume
     10001 of Lecture Notes in Computer Science. Springer, 2016.
 [3] Francesco Alberti, Roberto Bruttomesso, Silvio Ghilardi, Silvio Ranise, and Natasha Sharygina.
     Lazy abstraction with interpolants for arrays. In Nikolaj S. Bjørner and Andrei Voronkov, edi-
     tors, Logic for Programming, Artificial Intelligence, and Reasoning - 18th International Conference,
     LPAR-18, Mérida, Venezuela, March 11-15, 2012. Proceedings, volume 7180 of Lecture Notes in
     Computer Science, pages 46–61. Springer, 2012.
 [4] Jesper Amilon, Zafer Esen, Dilian Gurov, Christian Lidström, and Philipp Rümmer. Automatic
     program instrumentation for automatic verification. In Constantin Enea and Akash Lal, editors,
     Computer Aided Verification, pages 281–304, Cham, 2023. Springer Nature Switzerland.
 [5] Jesper Amilon, Zafer Esen, Dilian Gurov, Christian Lidström, and Philipp Rümmer. Artifact for
     the CAV 2023 paper "Automatic Program Instrumentation for Automatic Verification", April 2023.
 [6] Clark Barrett, Pascal Fontaine, and Cesare Tinelli. The SMT-LIB Standard: Version 2.6. Tech-
     nical report, Department of Computer Science, The University of Iowa, 2017. Available at
     www.SMT-LIB.org.
 [7] P. Baudin, J.-C. Filliâtre, C. Marché, B. Monate, Y. Moy, and V. Prevosto.
     ACSL: ANSI/ISO C specification language. Technical report, CEA-List, Inria, 2024.
     https://frama-c.com/download/acsl.pdf.
 [8] Dirk Beyer. Progress on software verification: SV-COMP 2022. In Dana Fisman and Grigore Rosu,
     editors, Tools and Algorithms for the Construction and Analysis of Systems - 28th International
     Conference, TACAS 2022, Held as Part of the European Joint Conferences on Theory and Practice
     of Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part II, volume 13244
     of Lecture Notes in Computer Science, pages 375–402. Springer, 2022.
 [9] Dirk Beyer. SV-Benchmarks: Benchmark Set for Software Verification and Testing (SV-COMP 2022
     and Test-Comp 2022), January 2022.
[10] Dirk Beyer, Matthias Dangl, and Philipp Wendler. Boosting k-induction with continuously-refined
     invariants. In Daniel Kroening and Corina S. Pasareanu, editors, Computer Aided Verification -
     27th International Conference, CAV 2015, San Francisco, CA, USA, July 18-24, 2015, Proceedings,
     Part I, volume 9206 of Lecture Notes in Computer Science, pages 622–640. Springer, 2015.
[11] Dirk Beyer and M. Erkan Keremoglu. CPAchecker: A tool for configurable software verification. In
     Ganesh Gopalakrishnan and Shaz Qadeer, editors, Computer Aided Verification - 23rd International
     Conference, CAV 2011, Snowbird, UT, USA, July 14-20, 2011. Proceedings, volume 6806 of Lecture
     Notes in Computer Science, pages 184–190. Springer, 2011.
[12] Nikolaj Bjørner, Arie Gurfinkel, Kenneth L. McMillan, and Andrey Rybalchenko. Horn clause
     solvers for program verification. In Lev D. Beklemishev, Andreas Blass, Nachum Dershowitz, Bernd
     Finkbeiner, and Wolfram Schulte, editors, Fields of Logic and Computation II - Essays Dedicated
     to Yuri Gurevich on the Occasion of His 75th Birthday, volume 9300 of Lecture Notes in Computer
     Science, pages 24–51. Springer, 2015.
[13] Nikolaj S. Bjørner, Kenneth L. McMillan, and Andrey Rybalchenko. On solving universally quan-
     tified Horn clauses. In Francesco Logozzo and Manuel Fähndrich, editors, Static Analysis - 20th
     International Symposium, SAS 2013, Seattle, WA, USA, June 20-22, 2013. Proceedings, volume
     7935 of Lecture Notes in Computer Science, pages 105–125. Springer, 2013.


                                                   25
[14] Edmund M. Clarke, Thomas A. Henzinger, Helmut Veith, and Roderick Bloem, editors. Handbook
     of Model Checking. Springer, 2018.
[15] Pascal Cuoq, Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris
     Yakobowski. Frama-C - A software analysis perspective. In George Eleftherakis, Mike Hinchey, and
     Mike Holcombe, editors, Software Engineering and Formal Methods - 10th International Conference,
     SEFM 2012, Thessaloniki, Greece, October 1-5, 2012. Proceedings, volume 7504 of Lecture Notes in
     Computer Science, pages 233–247. Springer, 2012.
[16] Przemyslaw Daca, Thomas A. Henzinger, and Andrey Kupriyanov. Array folds logic. In Swarat
     Chaudhuri and Azadeh Farzan, editors, Computer Aided Verification - 28th International Confer-
     ence, CAV 2016, Toronto, ON, Canada, July 17-23, 2016, Proceedings, Part II, volume 9780 of
     Lecture Notes in Computer Science, pages 230–248. Springer, 2016.
[17] Emanuele De Angelis, Maurizio Proietti, Fabio Fioravanti, and Alberto Pettorossi. Verifying
     catamorphism-based contracts using constrained Horn clauses. Theory Pract. Log. Program.,
     22(4):555–572, 2022.
[18] Alastair F. Donaldson, Daniel Kroening, and Philipp Rümmer. Automatic analysis of scratch-pad
     memory code for heterogeneous multicore processors. In Javier Esparza and Rupak Majumdar,
     editors, Tools and Algorithms for the Construction and Analysis of Systems, volume 6015 of LNCS,
     pages 280–295. Springer, 2010.
[19] Gidon Ernst. Korn - software verification with Horn clauses (competition contribution). In Sriram
     Sankaranarayanan and Natasha Sharygina, editors, Tools and Algorithms for the Construction and
     Analysis of Systems - 29th International Conference, TACAS 2023, Held as Part of the European
     Joint Conferences on Theory and Practice of Software, ETAPS 2022, Paris, France, April 22-27,
     2023, Proceedings, Part II, volume 13994 of Lecture Notes in Computer Science, pages 559–564.
     Springer, 2023.
[20] Zafer Esen and Philipp Rümmer. Tricera: Verifying C programs using the theory of heaps. In Alberto
     Griggio and Neha Rungta, editors, 22nd Formal Methods in Computer-Aided Design, FMCAD 2022,
     Trento, Italy, October 17-21, 2022, pages 380–391. IEEE, 2022.
[21] Grigory Fedyukovich, Sumanth Prabhu, Kumar Madhukar, and Aarti Gupta. Quantified invariants
     via syntax-guided synthesis. In Isil Dillig and Serdar Tasiran, editors, Computer Aided Verification -
     31st International Conference, CAV 2019, New York City, NY, USA, July 15-18, 2019, Proceedings,
     Part I, volume 11561 of Lecture Notes in Computer Science, pages 259–277. Springer, 2019.
[22] Jean-Christophe Filliâtre, Léon Gondelman, and Andrei Paskevich. The spirit of ghost code. Formal
     Methods Syst. Des., 48(3):152–174, 2016.
[23] Cormac Flanagan and James B. Saxe. Avoiding exponential explosion: generating compact ver-
     ification conditions. In Chris Hankin and Dave Schmidt, editors, Proceedings of: Symposium on
     Principles of Programming Languages (POPL’01), pages 193–205. ACM, 2001.
[24] Pranav Garg, Christof Löding, P. Madhusudan, and Daniel Neider. Learning universally quantified
     invariants of linear data structures. In Natasha Sharygina and Helmut Veith, editors, Computer
     Aided Verification - 25th International Conference, CAV 2013, Saint Petersburg, Russia, July 13-
     19, 2013. Proceedings, volume 8044 of Lecture Notes in Computer Science, pages 813–829. Springer,
     2013.
[25] Pamina Georgiou, Bernhard Gleiss, and Laura Kovács. Trace logic for inductive loop reasoning. In
     2020 Formal Methods in Computer Aided Design, FMCAD 2020, Haifa, Israel, September 21-24,
     2020, pages 255–263. IEEE, 2020.
[26] Arie Gurfinkel, Temesghen Kahsai, Anvesh Komuravelli, and Jorge A. Navas. The SeaHorn Verifica-
     tion Framework. In Daniel Kroening and Corina S. Pasareanu, editors, Computer Aided Verification
     - 27th International Conference, CAV 2015, San Francisco, CA, USA, July 18-24, 2015, Proceed-
     ings, Part I, volume 9206 of Lecture Notes in Computer Science, pages 343–361. Springer, 2015.
[27] Arie Gurfinkel, Sharon Shoham, and Yakir Vizel. Quantifiers on demand. In Shuvendu K. Lahiri
     and Chao Wang, editors, Automated Technology for Verification and Analysis - 16th International
     Symposium, ATVA 2018, Los Angeles, CA, USA, October 7-10, 2018, Proceedings, volume 11138 of
     Lecture Notes in Computer Science, pages 248–266. Springer, 2018.


                                                    26
[28] John Harrison. Handbook of Practical Logic and Automated Reasoning. Cambridge University Press,
     2009.
[29] Thomas A. Henzinger, Thibaud Hottelier, Laura Kovács, and Andrey Rybalchenko. Aligators for
     arrays (tool paper). In Christian G. Fermüller and Andrei Voronkov, editors, Logic for Program-
     ming, Artificial Intelligence, and Reasoning - 17th International Conference, LPAR-17, Yogyakarta,
     Indonesia, October 10-15, 2010. Proceedings, volume 6397 of Lecture Notes in Computer Science,
     pages 348–356. Springer, 2010.
[30] Hossein Hojjat and Philipp Rümmer. The ELDARICA Horn solver. In FMCAD 2018, pages 1–7,
     2018.
[31] Hari Govind V. K., Sharon Shoham, and Arie Gurfinkel. Solving constrained Horn clauses modulo
     algebraic data types and recursive functions. Proc. ACM Program. Lang., 6(POPL):1–29, 2022.
[32] Temesghen Kahsai, Rody Kersten, Philipp Rümmer, and Martin Schäf. Quantified heap invari-
     ants for object-oriented programs. In Thomas Eiter and David Sands, editors, LPAR-21, 21st
     International Conference on Logic for Programming, Artificial Intelligence and Reasoning, Maun,
     Botswana, May 7-12, 2017, volume 46 of EPiC Series in Computing, pages 368–384. EasyChair,
     2017.
[33] Gary T. Leavens, Albert L. Baker, and Clyde Ruby. JML: A notation for detailed design. In Haim
     Kilov, Bernhard Rumpe, and Ian Simmonds, editors, Behavioral Specifications of Businesses and
     Systems, volume 523 of The Kluwer International Series in Engineering and Computer Science,
     pages 175–188. Springer, 1999.
[34] K. Rustan M. Leino. Dafny: An automatic program verifier for functional correctness. In Edmund M.
     Clarke and Andrei Voronkov, editors, Logic for Programming, Artificial Intelligence, and Reasoning
     - 16th International Conference, LPAR-16, Dakar, Senegal, April 25-May 1, 2010, Revised Selected
     Papers, volume 6355 of Lecture Notes in Computer Science, pages 348–370. Springer, 2010.
[35] K. Rustan M. Leino and Rosemary Monahan. Reasoning about comprehensions with first-order SMT
     solvers. In Sung Y. Shin and Sascha Ossowski, editors, Proceedings of the 2009 ACM Symposium on
     Applied Computing (SAC), Honolulu, Hawaii, USA, March 9-12, 2009, pages 615–622. ACM, 2009.
[36] Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. RustHorn: CHC-based verification for
     Rust programs. ACM Trans. Program. Lang. Syst., 43(4):15:1–15:54, 2021.
[37] David Monniaux and Laure Gonnord. Cell morphing: From array programs to array-free Horn
     clauses. In Xavier Rival, editor, Static Analysis - 23rd International Symposium, SAS 2016, Edin-
     burgh, UK, September 8-10, 2016, Proceedings, volume 9837 of Lecture Notes in Computer Science,
     pages 361–382. Springer, 2016.
[38] Frank Neven, Thomas Schwentick, and Victor Vianu. Finite state machines for strings over infinite
     alphabets. ACM Trans. Comput. Log., 5(3):403–435, 2004.
[39] Siddharth Priya, Xiang Zhou, Yusen Su, Yakir Vizel, Yuyan Bao, and Arie Gurfinkel. Verifying
     verified code. In Zhe Hou and Vijay Ganesh, editors, Automated Technology for Verification and
     Analysis - 19th International Symposium, ATVA 2021, Gold Coast, QLD, Australia, October 18-22,
     2021, Proceedings, volume 12971 of Lecture Notes in Computer Science, pages 187–202. Springer,
     2021.
[40] John C. Reynolds. Separation logic: A logic for shared mutable data structures. In 17th IEEE
     Symposium on Logic in Computer Science (LICS 2002), 22-25 July 2002, Copenhagen, Denmark,
     Proceedings, pages 55–74. IEEE Computer Society, 2002.
[41] Luc Segoufin. Automata and logics for words and trees over an infinite alphabet. In Zoltán Ésik,
     editor, Computer Science Logic, 20th International Workshop, CSL 2006, 15th Annual Conference
     of the EACSL, Szeged, Hungary, September 25-29, 2006, Proceedings, volume 4207 of Lecture Notes
     in Computer Science, pages 41–57. Springer, 2006.




                                                  27
Appendix A                 Detailed Evaluation Results
We list all evaluated benchmarks in Table 3 (forall ), Table 4 (max ), Table 5 (min) and Table 6 (sum) for
all evaluated tools: MonoCera (Mono), TriCera (Tri), SeaHorn (Sea), and CPAchecker (CPA).
The list includes mostly SV-COMP benchmarks and the first column indicates their original directories
(should be prepended with “c/”). There are some crafted benchmarks that are not from SV-COMP; for
these we only state the name of the benchmark (for instance forall1-10).
    The expected result for all benchmarks in the tables is True. Durations are given next to the returned
result for benchmarks which did not time out.
    On top of quantifying over arrays, many of the benchmarks have assertions over nonlinear integer
arithmetic (NIA). Decision procedures for NIA are incomplete, and we have seen errors in the presence
of such assertions in some of the evaluated tools.
    The result “Unknown” is returned by MonoCera when the instrumentation search space is exhausted.
                Table 3: forall benchmark results for all tools. Timeout (T/O) is 300.0 s.
                                                           CPA         Sea          Tri           Mono
   array-cav19/array_doub_access_init_const.c              T/O         T/O         T/O        True (111)
   array-cav19/array_init_nondet_vars.c                    T/O         T/O         T/O         True (14)
   array-cav19/array_init_pair_sum_const.c                 T/O         T/O         T/O              T/O
   array-cav19/array_init_pair_symmetr.c                   T/O         T/O         T/O              T/O
   array-cav19/array_init_pair_symmetr2.c                  T/O         T/O         T/O              T/O
   array-cav19/array_init_var_plus_ind.c                   T/O         T/O     Error (2)       True (23)
   array-cav19/array_init_var_plus_ind2.c                  T/O         T/O     Error (2)   Unknown (109)
   array-cav19/array_init_var_plus_ind3.c                  T/O         T/O     Error (3)       True (60)
   array-industry-pattern/array_ptr_partial_init.c         T/O         T/O         T/O              T/O
   array-industry-pattern/array_shadowinit.c               T/O         T/O         T/O         True (19)
   array-cav19/array_tiling_poly6.c                        T/O     Error (0)       T/O              T/O
   array-cav19/array_tripl_access_init_const.c             T/O         T/O         T/O        True (199)
   array-fpi/condg.c                                       T/O         T/O         T/O              T/O
   array-fpi/condm.c                                       T/O         T/O         T/O          Error (8)
   array-fpi/condn.c                                       T/O         T/O         T/O         True (88)
   array-fpi/eqn1.c                                        T/O     Error (0)       T/O              T/O
   array-fpi/eqn2.c                                        T/O     Error (0)       T/O              T/O
   array-fpi/eqn3.c                                        T/O     Error (0)       T/O              T/O
   array-fpi/eqn4.c                                        T/O     Error (0)       T/O              T/O
   array-fpi/eqn5.c                                        T/O     Error (0)       T/O              T/O
   forall1-10                                         True (23)    Error (0)   True (55)       True (37)
   forall1-100                                             T/O     Error (2)       T/O         True (31)
   forall1-UB                                              T/O     Error (0)       T/O         True (32)
   array-fpi/ifcomp.c                                      T/O     Error (0)       T/O              T/O
   array-fpi/ifeqn1.c                                      T/O     Error (0)       T/O              T/O
   array-fpi/ifeqn2.c                                      T/O     Error (0)       T/O              T/O
   array-fpi/ifeqn3.c                                      T/O     Error (0)       T/O              T/O
   array-fpi/ifeqn4.c                                      T/O     Error (0)       T/O              T/O
   array-fpi/ifeqn5.c                                      T/O     Error (0)       T/O              T/O
   array-fpi/ifncomp.c                                Error (20)   Error (0)       T/O              T/O
   array-fpi/indp1.c                                       T/O     Error (0)       T/O              T/O
   array-fpi/indp2.c                                       T/O     Error (0)       T/O              T/O
   array-fpi/indp3.c                                       T/O     Error (0)       T/O              T/O
   array-fpi/indp4.c                                       T/O     Error (0)       T/O              T/O
   array-tiling/mbpr2.c                                    T/O         T/O         T/O              T/O
   array-tiling/mbpr3.c                                    T/O         T/O         T/O              T/O




                                                     28
                                                          CPA          Sea         Tri        Mono
array-tiling/mbpr4.c                                      T/O         T/O         T/O          T/O
array-tiling/mbpr5.c                                      T/O         T/O         T/O          T/O
loop-lit/mcmillan2006.c                                True (7)       T/O         T/O      True (19)
array-tiling/mlceu2.c                                     T/O         T/O     Error (3)    Error (4)
array-fpi/modn.c                                   Error (20)     Error (0)       T/O          T/O
array-fpi/modp.c                                   Error (17)     Error (0)       T/O      Error (9)
array-fpi/mods.c                                          T/O     Error (0)       T/O          T/O
array-fpi/ncomp.c                                         T/O     Error (0)       T/O          T/O
array-tiling/nr2.c                                        T/O         T/O         T/O      True (93)
array-tiling/nr3.c                                        T/O         T/O         T/O     True (123)
array-tiling/nr4.c                                        T/O         T/O         T/O     True (156)
array-tiling/nr5.c                                        T/O         T/O         T/O     True (223)
array-fpi/nsqm.c                                          T/O     Error (0)       T/O          T/O
array-fpi/nsqm-if.c                                Error (15)     Error (0)       T/O          T/O
array-lopstr16/partial_lesser_bound.c              T/O (108)          T/O         T/O          T/O
array-lopstr16/partial_lesser_bound-1.c                   T/O     Error (1)   Error (2)    True (89)
array-fpi/pcomp.c                                         T/O     Error (0)       T/O          T/O
array-tiling/pnr2.c                                       T/O         T/O         T/O     True (227)
array-tiling/pnr3.c                                       T/O         T/O         T/O     True (236)
array-tiling/pnr4.c                                       T/O         T/O         T/O          T/O
array-tiling/pnr5.c                                       T/O         T/O         T/O          T/O
array-tiling/poly1.c                                      T/O     Error (0)       T/O      True (25)
array-tiling/poly2.c                                      T/O     Error (0)       T/O          T/O
array-tiling/pr2.c                                        T/O     Error (0)       T/O     True (117)
array-tiling/pr3.c                                        T/O     Error (0)       T/O     True (143)
array-tiling/pr4.c                                        T/O     Error (0)       T/O          T/O
array-tiling/pr5.c                                        T/O     Error (0)       T/O          T/O
array-tiling/rew.c                                        T/O         T/O         T/O          T/O
array-tiling/rewnif.c                                     T/O         T/O         T/O      True (55)
array-tiling/rewnifrev.c                                  T/O         T/O         T/O      True (60)
array-tiling/rewnifrev2.c                                 T/O         T/O         T/O      True (97)
array-examples/sanfoundry_27_ground.c                     T/O         T/O         T/O     Error (19)
loop-crafted/simple_array_index_value_2.c                 T/O     Error (1)   Error (2)    True (39)
loop-crafted/simple_array_index_value_3.c                 T/O     Error (1)   Error (3)    True (33)
array-fpi/sina1.c                                         T/O         T/O         T/O     True (199)
array-fpi/sina2.c                                         T/O         T/O         T/O          T/O
array-fpi/sina3.c                                         T/O         T/O         T/O          T/O
array-fpi/sina4.c                                         T/O         T/O         T/O          T/O
array-fpi/sina5.c                                         T/O         T/O         T/O          T/O
array-tiling/skipped.c                                    T/O         T/O         T/O          T/O
array-fpi/sqm.c                                           T/O     Error (0)       T/O          T/O
array-fpi/sqm-if.c                                        T/O     Error (0)       T/O          T/O
array-fpi/ss2.c                                    Error (65)     Error (0)       T/O          T/O
array-fpi/ssina.c                                  Error (38)     Error (0)       T/O          T/O
array-examples/standard_copyInitSum2_ground-2.c           T/O         T/O         T/O          T/O
array-examples/standard_copyInitSum3_ground.c             T/O         T/O         T/O          T/O
array-examples/standard_copyInit_ground.c                 T/O         T/O         T/O          T/O
array-examples/standard_init1_ground-2.c                  T/O         T/O         T/O      True (32)
array-examples/standard_init2_ground-2.c                  T/O         T/O         T/O      True (82)
array-examples/standard_init3_ground-2.c                  T/O         T/O         T/O          T/O




                                                  29
                                                       CPA         Sea          Tri            Mono
array-examples/standard_init4_ground-2.c                T/O        T/O         T/O              T/O
array-examples/standard_init5_ground-1.c                T/O        T/O         T/O              T/O
array-examples/standard_init6_ground-2.c                T/O        T/O         T/O              T/O
array-examples/standard_init7_ground-2.c                T/O        T/O         T/O              T/O
array-examples/standard_init8_ground-2.c                T/O        T/O         T/O              T/O
array-examples/standard_init9_ground-2.c                T/O        T/O         T/O              T/O
array-examples/standard_maxInArray_ground.c             T/O        T/O         T/O              T/O
array-examples/standard_minInArray_ground-2.c           T/O        T/O         T/O              T/O
array-examples/standard_partition_ground-2.c            T/O        T/O         T/O              T/O
array-examples/standard_vararg_ground.c                 T/O        T/O         T/O         True (57)



         Table 4: max benchmark results for all tools. Timeout (T/O) is 300.0 s.
                                                      CPA        Sea          Tri            Mono
 array-cav19/array_init_var_plus_ind3.c               T/O        T/O     Error (2)    Unknown (277)
 battery_diag-10                                 True (155)   True (0)       T/O               T/O
 battery_diag-100                                     T/O        T/O         T/O               T/O
 array-fpi/condn.c                                    T/O        T/O         T/O         True (129)
 max_eq-10                                        True (21)   True (0)   True (78)        True (21)
 max_eq-100                                           T/O        T/O         T/O          True (38)
 max_eq-UB                                            T/O        T/O         T/O          True (27)
 max_leq-10                                       True (25)   True (0)   True (90)        True (23)
 max_leq-100                                          T/O        T/O         T/O          True (30)
 max_leq-UB                                           T/O        T/O         T/O          True (52)
 array-examples/sanfoundry_27_ground.c                T/O        T/O         T/O         True (285)
 array-examples/standard_maxInArray_ground.c          T/O        T/O         T/O               T/O



         Table 5: min benchmark results for all tools. Timeout (T/O) is 300.0 s.
                                                       CPA        Sea          Tri           Mono
 array-cav19/array_doub_access_init_const.c            T/O        T/O         T/O             T/O
 array-cav19/array_init_pair_sum_const.c               T/O        T/O         T/O             T/O
 array-cav19/array_init_pair_symmetr2.c                T/O        T/O         T/O             T/O
 array-cav19/array_init_var_plus_ind.c                 T/O        T/O     Error (3)   Unknown (67)
 array-cav19/array_init_var_plus_ind2.c                T/O        T/O     Error (2)   Unknown (64)
 array-cav19/array_tripl_access_init_const.c           T/O        T/O         T/O             T/O
 min_eq-10                                        True (25)   True (0)   True (61)        True (28)
 min_eq-100                                            T/O        T/O         T/O         True (22)
 min_eq-UB                                             T/O        T/O         T/O         True (25)
 min_geq-10                                       True (26)   True (0)   True (51)        True (26)
 min_geq-100                                           T/O        T/O         T/O         True (28)
 min_geq-UB                                            T/O        T/O         T/O         True (24)
 array-tiling/rew.c                                    T/O        T/O         T/O         True (40)
 array-tiling/rewnifrev.c                              T/O        T/O         T/O         True (41)
 array-examples/standard_minInArray_ground-2.c         T/O        T/O         T/O             T/O
 array-examples/standard_partition_ground-2.c          T/O        T/O         T/O             T/O
 array-examples/standard_vararg_ground.c               T/O        T/O         T/O         True (59)




                                                 30
Table 6: sum benchmark results for all tools. Timeout (T/O) is 300.0 s.
                              CPA           Sea          Tri        Mono
     array-fpi/brs1.c         T/O           T/O         T/O      True (26)
     array-fpi/brs2.c          T/O      Error (0)       T/O      True (34)
     array-fpi/brs3.c          T/O          T/O         T/O      True (41)
     array-fpi/brs4.c          T/O          T/O         T/O      True (38)
     array-fpi/brs5.c          T/O          T/O         T/O      True (58)
     array-fpi/conda.c         T/O          T/O         T/O          T/O
     array-fpi/indp5.c    Error (17)    Error (0)       T/O          T/O
     array-fpi/ms1.c           T/O          T/O         T/O      True (26)
     array-fpi/ms2.c           T/O          T/O         T/O      True (46)
     array-fpi/ms3.c           T/O          T/O         T/O      True (31)
     array-fpi/ms4.c           T/O          T/O         T/O      True (33)
     array-fpi/ms5.c           T/O          T/O         T/O      True (32)
     array-fpi/s1lif.c         T/O          T/O         T/O          T/O
     array-fpi/s2lif.c         T/O          T/O         T/O          T/O
     array-fpi/s3lif.c         T/O          T/O         T/O          T/O
     array-fpi/s4lif.c         T/O          T/O         T/O          T/O
     array-fpi/s5lif.c         T/O          T/O         T/O          T/O
     sum_eq-10            True (50)     True (0)    True (45)   True (245)
     sum_eq-100                T/O          T/O         T/O          T/O
     sum_eq-UB                 T/O          T/O         T/O      True (55)
     sum_geq-10           True (45)     True (0)    True (98)   True (200)
     sum_geq-100               T/O          T/O         T/O     True (221)
     sum_geq-UB                T/O          T/O         T/O      True (59)
     two_arrays_sum-10    True (26)     True (0)    True (46)        T/O
     two_arrays_sum-100        T/O          T/O         T/O          T/O
     two_arrays_sum-UB         T/O          T/O         T/O     True (106)




                                       31
