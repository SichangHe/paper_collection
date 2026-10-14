                                                Automatic Program Instrumentation for
                                                       Automatic Verification
                                                    (Extended Technical Report)

                                         Jesper Amilon1 , Zafer Esen2 , Dilian Gurov1 , Christian Lidström1 , and Philipp
arXiv:2306.00004v1 [cs.SE] 26 May 2023




                                                                            Rümmer2,3
                                                      1
                                                          KTH Royal Institute of Technology, Stockholm, Sweden
                                                                    2
                                                                      Uppsala University, Sweden
                                                               3
                                                                 University of Regensburg, Germany


                                               Abstract. In deductive verification and software model checking, deal-
                                               ing with certain specification language constructs can be problematic
                                               when the back-end solver is not sufficiently powerful or lacks the re-
                                               quired theories. One way to deal with this is to transform, for verification
                                               purposes, the program to an equivalent one not using the problematic
                                               constructs, and to reason about its correctness instead. In this paper, we
                                               propose instrumentation as a unifying verification paradigm that sub-
                                               sumes various existing ad-hoc approaches, has a clear formal correctness
                                               criterion, can be applied automatically, and can transfer back witnesses
                                               and counterexamples. We illustrate our approach on the automated ver-
                                               ification of programs that involve quantification and aggregation opera-
                                               tions over arrays, such as the maximum value or sum of the elements in
                                               a given segment of the array, which are known to be difficult to reason
                                               about automatically. We implement our approach in the MonoCera
                                               tool, which is tailored to the verification of programs with aggregation,
                                               and evaluate it on example programs, including SV-COMP programs.


                                         1   Introduction

                                         Overview Program specifications are often written in expressive, high-level
                                         languages: for instance, in temporal logic [13], in first-order logic with quan-
                                         tifiers [27], in separation logic [39], or in specification languages that provide
                                         extended quantifiers for computing the sum or maximum value of array ele-
                                         ments [32,6]. Specifications commonly also use a rich set of theories; for instance,
                                         specifications could be written using full Peano arithmetic, as opposed to bit-
                                         vectors or linear arithmetic used in the program. Rich specification languages
                                         make it possible to express intended program behaviour in a succinct form, and
                                         as a result reduce the likelihood of mistakes being introduced in specifications.
                                              There is a gap, however, between the languages used in specifications and
                                         the input languages of automatic verification tools. Software model checkers, in
                                         particular, usually require specifications to be expressed using program assertions
                                         and Boolean program expressions, and do not directly support any of the more
                                         sophisticated language features mentioned. In fact, rich specification languages
are challenging to handle in automatic verification, since satisfiability checks
can become undecidable (i.e., it is no longer decidable whether assertion failures
can occur on a program path), and techniques for inferring program invariants
usually focus on simple specifications only.
    To bridge this gap, it is common practice to encode high-level specifica-
tions in the low-level assertion languages understood by the tools. For instance,
temporal properties can be translated to Büchi automata, and added to pro-
grams using ghost variables and assertions [13]; quantified properties can be
replaced with non-determinism, ghost variables, or loops [12,36]; sets used to
specify the absence of data-races can be represented using non-deterministically
initialized variables [17]. By adding ghost variables and bespoke ghost code to
programs [21], many specifications can be made effectively checkable.
    The translation of specifications to assertions or ghost code is today largely
designed, or even carried out, by hand. This is an error-prone process, and for
complex specifications and programs it is very hard to ensure that the low-level
encoding of a specification faithfully models the original high-level properties to
be checked. Mistakes have been found even in industrial, very carefully developed
specifications [38], and can result in assertions that are vacuously satisfied by
any program. Naturally, the manual translation of specifications also tends to
be an ad-hoc process that does not easily generalise to other specifications.
    This paper proposes the first general framework to automate the translation
of rich program specifications to simpler program assertions, using a process
called instrumentation. Our approach models the semantics of specific complex
operations using program-independent instrumentation operators, consisting of
(manually designed) rewriting rules that define how the evaluation of the opera-
tor can be achieved using simpler program statements and ghost variables. The
instrumentation approach is flexible enough to cover a wide range of different
operators, including operators that are best handled by weaving their evaluation
into the program to be analysed. While instrumentation operators are manually
written, their application to programs can be performed in a fully automatic way
by means of a search procedure. The soundness of an instrumentation operator is
shown formally, once and for all, by providing an instrumentation invariant that
ensures that the operator can never be used to show correctness of an incorrect
program.


Motivating Example We illustrate our approach on the computation of tri-
angular numbers sN = (N 2 + N )/2, see left-hand side of Figure 1. For reasons of
presentation, the program has been normalised by representing the square N*N
using an auxiliary variable NN. While mathematically simple, verifying the post-
condition s==(NN+N)/2 in the program turns out to be challenging even for
state-of-the-art model checkers, as such tools are usually thrown off course by
the non-linear term N*N. Computing the value of NN by adding a loop in line 16
is not sufficient for most tools either, since the program in any case requires
a non-linear invariant 0 <= i <= N && 2*s == i*i + i to be derived for the
loop in lines 4–12.

                                        2
1 // Triangular numbers                     1 // Instrumented program
2 i = 0; /* A */ s = 0; /* B */             2 i =0; s =0; x_sq =0; x_shad =0;
3 assume (N >0) ;                           3 assume (N >0) ;

4 while ( i < N ) {                         4 while ( i < N ) {

5                                           5      // Begin - instrumentat i on
6                                           6      assert ( i == x_shad ) ;
7                                           7      x_sq     = x_sq + 2* i + 1;
8         i = i + 1; /* C */                8      i        = i + 1;
9                                           9      x_shad = i ;
10                                         10      // End - instrumentat io n
11        s = s + i;                       11      s        = s + i;
12   }                                     12 }

13                                         13 // Begin - instrumentat io n

14                                         14 assert ( N == x_shad ) ;

15   NN = N * N ; /* D */                  15 NN = x_sq ;

16                                         16 // End - instrumenta t io n

17   assert ( s == ( NN + N ) /2) ;        17 assert ( s == ( NN + N ) /2) ;




     Fig. 1: Program computing triangular numbers, and its instrumented counterpart



         The insight needed to elegantly verify the program is that the value i*i can
     be tracked during the program execution using a ghost variable x_sq. For this,
     the program is instrumented to maintain the relationship x_sq == i*i: initially,
     i == x_sq == 0, and each time the value of i is modified, also the variable x_sq
     is updated accordingly. With the value x_sq == i*i available, both the loop
     invariant and the post-condition turn into formulas over linear arithmetic, and
     program verification becomes largely straightforward. The challenge, of course,
     is to discover this program transformation automatically, and to guarantee the
     soundness of the process. For the example, the transformed program is shown
     on the right-hand side of Figure 1, and discussed in the next paragraphs.
         Our method splits the process of program instrumentation into two parts:
     (i) choosing an instrumentation operator, which is defined manually, designed to
     be program-independent, and induces a space of possible program transforma-
     tions; and (ii) carrying out an automatic application strategy to find, among the
     possible program transformations, one that enables verification of a program.
         An instrumentation operator for tracking squares is shown in Figure 2, and
     consists of the declaration of two ghost variables (x_sq, x_shad) with initial
     value 0, respectively; four rules for rewriting program statements; and the in-
     strumentation invariant witnessing correctness of the operator. The rewrite rules
     use formal variables x, y, which can represent arbitrary variables in the program
     (i, N, NN). An application of the operator to a program will declare the ghost
     variables in the form of global variables, and then rewrite some chosen set of pro-
     gram statements using the provided rules. Since the statements to be rewritten
     can be chosen arbitrarily, and since moreover multiple rewrite rules might apply
     to some statements, rewriting can result in many different variants of a program.

                                                3
  Ωsquare (Instrumentation operator)
    Gsquare (Ghost variables)
    x_sq, x_shad : Int
    init(x_sq) = 0, init(x_shad) = 0

    Rsquare (Rewrite rules)
    x=α           x = α; x_sq = α2 ; x_shad = x                         (R1)
    x=x+α          assert(x == x_shad);                                 (R2)
                   x_sq = x_sq + 2α * x + α2 ; x = x + α; x_shad = x
    x=α*x          assert(x == x_shad);                                 (R3)
                   x_sq = α2 * x_sq; x = α * x; x_shad = x
    y=x*x          assert(x == x_shad); y = x_sq                        (R4)

    Isquare (Instrumentation invariant)
    x_sq = x_shad2



 Fig. 2: Definition of an instrumentation operator Ωsquare for tracking squares

In the example, we rewrite the assignments C, D of the left-hand side program
using rewrite rules (R2) and (R4), respectively, resulting in the instrumented
and correct program on the right-hand side.
    Instrumentation operators are designed to be sound, which means that rewrit-
ing a wrong selection of program statements might lead to an instrumented pro-
gram that cannot be verified, i.e., in which assertions might fail, but instrumen-
tation can never turn an incorrect source program into a correct instrumented
program. This opens up the possibility to systematically search for the right
program instrumentation. We propose a counterexample-guided algorithm for
this purpose, which starts from some arbitrarily chosen instrumentation, checks
whether the instrumented program can be verified, and otherwise attempts to
fix the instrumentation using a refinement loop. As soon as a verifiable instru-
mented program has been found, the search can stop and the correctness of the
original program has been shown.
    The concept of instrumentation invariants is essential for guaranteeing sound-
ness of an operator. Instrumentation invariants are formulas that can (only) re-
fer to the ghost variables introduced by an instrumentation operator, and are
formulated in such a way that they hold in every reachable state of every in-
strumented program. To maintain their invariants, instrumentation operators use
shadow variables that duplicate the values of program variables. In the operator
in Figure 2, the purpose of the shadow variable x_shad is to reproduce the value
of the program variable whose square is tracked (i). The rewriting rules intro-
duce guards to detect incorrect instrumentation (the assertions in (R2), (R3),
(R4)), which are particular cases in which some update of a relevant variable
was missed and not correctly instrumented. The use of shadow variables and

                                        4
guards make instrumentation operators very flexible; in our example, note that
instrumentation tracks the square of the value of i during the loop, but is also
used later to simplify the expression N*N. This is possible because of the instru-
mentation invariant and because i == N holds after termination of the loop,
which is verified through the assertion introduced in line 14.


Contributions and Outline The operator shown in Figure 2 is simple, and
does not apply to all programs, but it can easily be generalised to other arith-
metic operators and program statements. The framework presented in this pa-
per provides the foundation for developing a (extendable) library of formally
verified instrumentation operators. In the scope of this paper, we focus on two
specification constructs that have been identified as particularly challenging in
the literature: existential and universal quantifiers over arrays, and aggrega-
tion (or extended quantifiers), which includes computing the sum or maximum
value of elements in an array. Our experiments on benchmarks taken from the
SV-COMP [7] show that even relatively simple instrumentation operators can
significantly extend the capabilities of a software model checker, and often make
the automatic verification of otherwise hard specifications easy.
    The contributions of the paper are: (i) a general framework for program
instrumentation, which defines a space of program transformations that work by
rewriting individual statements (Section 2); (ii) an application strategy search
algorithm in this space, for a given program (Section 3); (iii) two instantiations
of the framework—one for instrumentation operators to handle specifications
with quantifiers (Section 4.1), and one for extended quantifiers (Section 4.2);
(iv) machine-checked proofs of the correctness of the instrumentation operators
for quantifiers ∀ and the extended quantifier \max; (v) a new verification tool,
MonoCera, that is tailored to the verification of programs with aggregation;
and (vi) an evaluation of our method and tool on a set of examples, including
such from SV-COMP [7] (Section 5).


2   Instrumentation Framework

The next two sections formally introduce the instrumentation framework. Later,
we instantiate the framework for quantification and aggregation over arrays. We
split the instrumentation process into two parts:

1. An instrumentation operator that defines how to rewrite program statements
   with the purpose of eliminating language constructs that are difficult to
   reason about automatically, but leaves the choice of which occurrences of
   these statements to rewrite to the second part (this section).
2. An application strategy for the instrumentation operator, which can be im-
   plemented using heuristics or systematic search, among others. The strategy
   is responsible for selecting the right (if any) program instrumentation from
   the many possible ones, Section 3 is dedicated to the second part.

                                        5
                      Table 1: Syntax of the core language.

  hTypei ::= Int | Bool | Array hTypei
  hExpr i ::= hDecimalNumber i | true | false | hVariablei
           |   hExpr i == hExpr i | hExpr i <= hExpr i | !hExpr i | hExpr i && hExpr i
           |   hExpr i || hExpr i | hExpr i + hExpr i | hExpr i * hExpr i
           |   select(hExpr i,hExpr i) | store(hExpr i,hExpr i,hExpr i)
  hProgi ::= skip | hVariablei = hExpr i | hProg i; hProg i | while (hExpr i) hProg i
           |   assert(hExpr i) | assume(hExpr i) | if (hExpr i) hProgi else hProg i

Even though instrumentation operators are non-deterministic, we shall guaran-
tee their soundness: if the original program has a failing assertion, so will any
instrumented program, regardless of the chosen application strategy; that is,
instrumentation of an incorrect program will never yield a correct program.
    We shall also guarantee a weak form of completeness, to the effect that if an
assertion that has not been added to the program by the instrumentation fails
in the instrumented program, then it will also fail in the original program. As
a result, any counter-example (for such an assertion) produced when verifying
the instrumented program can be transformed into a counter-example for the
original program.

2.1   The Core Language
While our implementation works on programs represented as constrained Horn
clauses [11], i.e., is language-agnostic, for readability purposes we present our
approach in the setting of an imperative core programming language with data-
types for unbounded integers, Booleans, and arrays, and assert and assume
statements. The language is deliberately kept simple, but is still close to stan-
dard C. The main exception is the semantics of arrays: they are defined here
to be functional and therefore represent a value type. Arrays have integers as
index type and are unbounded, and their signature and semantics are otherwise
borrowed from the SMT-LIB theory of extensional arrays [5]:
 – Reading the value of an array a at index i:        select(a, i);
 – Updating an array a at index i with a new value x: store(a, i, x).
    The complete syntax of the core language is given in Table 1. Programs are
written using a vocabulary X of typed program variables; the typing rules of the
language are given in Appendix A. As syntactic sugar, we sometimes write a[i]
instead of select(a, i), and a[i] = x instead of a = store(a, i, x).
    We denote by Dσ the domain of a program type σ. The domain of an array
                                            Z
type Array σ is the set of functions f : → Dσ .

Semantics. We assume the Flanagan-Saxe extended execution model of pro-
grams with assume and assert statements (see, e.g., [22]), in which executing

                                            6
an assert statement with an argument that evaluates to false fails, i.e., termi-
nates abnormally. An assume statement with an argument that evaluates to false
has the same semantics as a non-terminating loop. Partial correctness proper-
ties of programs are expressed using Hoare triples {Pre} P {Post}, which state
that an execution of P , starting in a state satisfying Pre, never fails, and may
only terminate in states that satisfy Post . As usual, a program P is considered
(partially) correct if the Hoare triple {true} P {true} holds.
    The evaluation of program expressions is modelled using a function J·Ks that
maps program expressions t of type σ to their value JtKs ∈ Dσ in the state s.


2.2   Instrumentation Operators

An instrumentation operator defines schemes to rewrite programs while preserv-
ing the meaning of the existing program assertions. Without loss of generality,
we restrict program rewriting to assignment statements. Instrumentation can
introduce ghost state by adding arbitrary fresh variables to the program. The
main part of an instrumentation consists of rewrite rules, which are schematic
rules r = t   s, where the meta-variable r ranges over program variables, t is
an expression that can contain further meta-variables, and s is a schematic pro-
gram in which the meta-variables from r = t might occur. Any assignment that
matches r = t can be rewritten to s.

Definition 1 (Instrumentation Operator). An instrumentation operator is
a tuple Ω = (G, R, I), where:

(i) G = h(x1 , init 1 ), . . . , (xk , init k )i is a tuple of pairs of ghost variables and
     their initial values;
(ii) R is a set of rewrite rules r = t             s, where s is a program operating on the
     ghost variables x1 , . . . , xk (and containing meta-variables from r = t);
(iii) I is a formula over the ghost variables x1 , . . . , xk , called the instrumenta-
     tion invariant.

The rewrite rules R and the invariant I must adhere to the following constraints:

 1. The instrumentation invariant I is satisfied by the initial ghost values, i.e.,
    it holds in the state {x1 7→ init 1 , . . . , xk 7→ init k }.
 2. For all rewrites r = t    s ∈ R the following hold:
    (a) s terminates (normally or abnormally) for pre-states satisfying I, as-
        suming that all meta-variables are ordinary program variables.
    (b) s does not assign to variables other than r or the ghost variables x1 , . . . , xk .
    (c) s preserves the instrumentation invariant: {I} s′ {I}, where s′ is s with
        every assert(e) statement replaced by an assume(e) statement.
    (d) s preserves the semantics of the assignment r = t: the Hoare triple
        {I} z = t; s′ {z = r}, where z is a fresh variable, holds.

   The conditions imposed in the definition ensure that all instrumentations
are correct, in the sense that they are sound and weakly complete, as we show

                                            7
below. In particular, the instrumentation invariant guarantees that the rewrites
of program statements are semantics-preserving w.r.t. the original program, and
thus, the execution of any assert statement of the original program has the
same effect before and after instrumentation. Observe that the conditions can
themselves be deductively verified to hold for each concrete instrumentation
operator, and that this check is independent of the programs to be instrumented,
so that an instrumentation operator can be proven correct once and for all.
    An instrumentation operator Ω does itself not define which occurrences of
program statements are to be rewritten, but only how they are rewritten. Given
a program P and the operator Ω, an instrumented program P ′ is derived by
carrying out the following two steps: (i) variables x1 , . . . , xk and the assignments
x1 = init 1 ; . . . ; xk = init k are added at the beginning of the program, and
(ii) some of the assignments in P , to which a rewriting rule r = t            s in Ω is
applicable, are replaced by s, substituting meta-variables with the actual terms
occurring in the assignment. We denote by Ω(P ) the set of all instrumented
programs P ′ that can be derived in this way. An example of an instrumentation
operator and its application was shown Figure 1 and Figure 2.


2.3   Instrumentation Correctness

Verification of an instrumented program produces one of two possible results:
a witness if verification is successful, or a counter-example otherwise. A wit-
ness consists of the inductive invariants needed to verify the program, and is
presented in the context of the programming language: it is translated back
from the back-end theory used by the verification tool, and is a formula over
the program variables and the ghost variables added during instrumentation. A
counter-example is an execution trace leading to a failing assertion.

Definition 2 (Soundness). An instrumentation operator Ω is called sound
if for every program P and instrumented program P ′ ∈ Ω(P ), whenever there
is an execution of P where some assert statement fails, then there also is an
execution of P ′ where some assert statement fails.

    Equivalently, existence of a witness for an instrumented program entails ex-
istence of a witness for the original program, in the form of a set of inductive
invariants solely over the program variables. Notably, because of the semantics-
preserving nature of the rewrites under the instrumentation invariant, a witness
for the original program can be derived from one for the instrumented program.
One such back-translation is to add the instrumentation invariant as a conjunct
to the original witness, and to existentially quantify over the ghost variables.

Example. To illustrate the back-translation, we return to the instrumentation
operator from Figure 2 and the example program from Figure 1. The witness
produced by our verification tool in this case is the formula:

      i = x_shad ∧ x_sq + x_shad = 2s ∧ N ≥ i ∧ N ≥ 1 ∧ 2s ≥ i ∧ i ≥ 0


                                           8
After conjoining the instrumentation invariant x_sq = x_shad2 and existen-
tially quantifying over the involved ghost variables, we obtain an inductive in-
variant that is sufficient to verify the original program:

               ∃xsq , xshad . (i = xshad ∧ xsq + xshad = 2s ∧
                     N ≥ i ∧ N ≥ 1 ∧ 2s ≥ i ∧ i ≥ 0 ∧ xsq = x2shad )



Definition 3 (Weak Completeness). The operator Ω is called weakly com-
plete if for every program P and instrumented program P ′ ∈ Ω(P ), whenever an
assert statement that has not been added to the program by the instrumentation
fails in the instrumented program P ′ , then it also fails in the original program P .

Similarly to the back-translation of invariants, when verification fails, counter-
examples for assertions of the original program, found during verification of
the instrumented program, can be translated back to counter-examples for the
original program. We thus obtain the following result.

Theorem 1 (Soundness and weak completeness). Every instrumentation
operator Ω is sound and weakly complete.

Proof. Let Ω = (G, R, I) be an instrumentation operator. Since I is a formula
over ghost variables only, which holds initially and is preserved by all rewrites,
I is an invariant of the fully instrumented program. This entails that rewrites of
assignments are semantics-preserving. Furthermore, since instrumentation code
only assigns to ghost variables or to r (i.e., the left-hand side of the original
statement), program variables have the same values in the instrumented program
as in the original one. Furthermore, since all rewrites are terminating under I,
the instrumented program will terminate if and only if the original program does.
     In the case when verification succeeds, and a witness is produced, weak com-
pleteness follows vacuously. A witness consists of the inductive invariants suffi-
cient to verify the instrumented program. Thus, they are also sufficient to verify
the the assertions existing in the original program, since assertions are not rewrit-
ten and all program variables have the same valuation in the original and the
instrumented programs. Since a witness for the instrumented program can be
back-translated to a witness for the original program, any failing assertion in the
original program must also fail in the instrumented program, and Ω is therefore
sound.
     In the case when verification fails, soundness follows vacuously, and if the
failing assertion was added during instrumentation, also weak completeness fol-
lows. If the assertion existed in the original program, since such assertions are
not rewritten, and since program variables have the same values in the instru-
mented program as in the original program, then any counter-example for the
instrumented program is also a counter-example for the original program, when
projected onto the program variables.                                              ⊓
                                                                                   ⊔

                                          9
   Input: Program P ; statements S; instrumentation space R; oracle IsCorrect .
   Result: Instrumentation r ∈ R with IsCorrect (Pr ); Incorrect ; or Inconclusive.
 1 begin
 2    Cand ← R;
 3    while Cand 6= ∅ do
 4        pick r ∈ Cand ;
 5        if IsCorrect (Pr ) then
 6            return r;
 7        else
 8            cex ← counterexample path for Pr ;
 9            if failing assertion in cex also exists in P then
                  /* cex is also a counterexample for P                          */
10                return Incorrect ;
11            else
                  /* instrumentation on cex may have been incorrect              */
12                C ′ ← {p ∈ C | ins r (p) occurs on cex };
13                Cand ← Cand \ {r ′ ∈ Cand | r(s) = r ′ (s) for all p ∈ C ′ };
14            end
15        end
16    end
17    return Inconclusive;
18 end

     Algorithm 1: Counterexample-guided instrumentation search

3   Instrumentation Application Strategies
We will now define a counterexample-guided search procedure to discover appli-
cations of instrumentation operators that make it possible to verify a program.
    For our algorithm, we assume that we are given an oracle IsCorrect that is
able to check the correctness of programs after instrumentation. Such an ora-
cle could be approximated, for instance, using a software model checker. The
oracle is free to ignore the complex functions we are trying to eliminate by in-
strumentation; for instance, in Figure 1, the oracle can over-approximate the
term N*N by assuming that it can have any value. We further assume that C
is the set of control points of a program P corresponding to the statements to
which a given set of instrumentation operators can be applied. For each control
point p ∈ C, let Q(p) be the set of rewrite rules applicable to the statement
at p, including also a distinguished value ⊥ that expresses that p is not modi-
fied. For the program in Figure 1, for instance, the choices could be defined by
Q(A) = Q(B) = {(R1), ⊥}, Q(C) = {(R2), ⊥}, andSQ(D) = {(R4), ⊥}, referring
to the rules in Figure 2. Any function r : C → p∈C Q(p) with r(p) ∈ Q(p)
will then define one possible program
                                S       instrumentation. We will denote the set
of well-typed functions C → p∈C Q(p) by R, and the program obtained by
rewriting P according to r ∈ R by Pr . We further denote the control point in
Pr corresponding to some p ∈ C in P by ins r (p).
    Algorithm 1 presents our algorithm to search for instrumentations that are
sufficient to verify a program P . The algorithm maintains a set Cand ⊆ R of

                                         10
       Table 2: Extension of the core language with quantified expressions.

    hExpr i ::= (λ(hVariablei,hVariablei).hExpr i) (hExpr i, hExpr i) |
                 forall(hExpr i,hExpr i,hExpr i,λ(hVariablei, hVariablei).hExpr i) |
                 exists(hExpr i,hExpr i,hExpr i,λ(hVariablei, hVariablei).hExpr i)



remaining ways to instrument P , and in each loop considers one of the remaining
elements r ∈ Cand (line 4). If the oracle manages to verify Pr in line 5, due to
soundness of instrumentation the correctness of P has been shown (line 6); if
Pr is incorrect, there has to be a counterexample ending with a failing assertion
(line 8). There are two possible causes of assertion failures: if the failing assertion
in Pr already existed in P , then due to the weak completeness of instrumentation
also P has to be incorrect (line 10). Otherwise, the program instrumentation
has to be refined, and for this from Cand we remove all instrumentations r′ that
agree with r regarding the instrumentation of the statements occurring in the
counterexample (line 13).
    Since R is finite, and at least one element of Cand is eliminated in each
iteration, the refinement loop terminates. The set Cand can be exponentially
big, however, and therefore should be represented symbolically (using BDDs, or
using an SMT solver managing the set of blocking constraints from line 13).
    We can observe soundness and completeness of the algorithm w.r.t. the con-
sidered instrumentation operators (proof in Appendix B):

Lemma 1 (Correctness). If Algorithm 1 returns an instrumentation r ∈ R,
then Pr and P are correct. If Algorithm 1 returns Incorrect, then P is incorrect.
If there is r ∈ R such that Pr is correct, then Algorithm 1 will return r′ such
that Pr′ is correct.


4     Instrumentation Operators for Arrays

4.1    Instrumentation Operators for Quantification over Arrays

To handle quantifiers in a programming setting, we extend the language defined
in Table 1 by adding quantified expressions over arrays, as shown in Table 2. As
seen, we also extend the language with a lambda expression over two variables.
The rationale for this is that a quantified property can be expressed as a binary
predicate with the first argument corresponding to the value of an element and
the second to the index. This allows us to express properties over both the value
of an element and its index. For example, we can express that each element
should be equal to its index, as is done in the example program in Figure 3. In
the program, each element in the array is assigned the value corresponding to
its index, after which it is asserted that this property indeed holds.

                                          11
1  Int N = nondet ;
2  assume ( N > 0) ;
 3 Array Int a = const (0 , N ) ;

 4 Int i = 0;

 5 while ( i < N ) {

 6     a = store (a , i , i ) ;
 7     i = i + 1;
 8 }

 9 Bool b = forall (a , 0 , N , λ(i , x ) .( x == i ) ) ;

10 assert ( b ) ;




    Fig. 3: Example of program to be verified using a quantified assert statement.


       Using P(x0 ,i0 ) as shorthand for (λ(x,i).P)(x0,i0 ), the new expressions
    can be defined formally as:

             Jforall(a, l, u, λ(x,i).P)Ks = ∀i ∈ [l, u). JP(a[i],i)Ks
             Jexists(a, l, u, λ(x,i).P)Ks = ∃i ∈ [l, u). JP(a[i],i)Ks

    Note that the types of x and a must be compatible and P a Boolean-valued
    expression.
        To handle programs such as the one in Figure 3, we turn to the instrumenta-
    tion framework outlined in Section 2.2, which we use here to define an instrumen-
    tation operator for universal quantification. The general idea is to instrument
    programs with a ghost variable, tracking if some predicate holds for all elements
    in an interval of the array, with shadow variables representing the tracked array,
    and the bounds of the interval. Naturally, an instrumentation operator for exis-
    tential quantification can be defined in a similar fashion. For simplicity, we shall
    assume a normal form of programs, into which every program can be rewrit-
    ten by introducing additional variables. In the normal form, store, select and
    forall can only occur in simple assignment statements. For example, stores are
    restricted to occur in statements of the form: a’ = store(a, i, x).
        Over such normalised programs, and for a universally quantified expression
    forall(a, l, u, λ(x,i)(P)), we define the instrumentation operator Ω∀,P =
    (G∀,P , R∀,P , I∀,P ) as shown in Figure 4 over four ghost variables. The array
    over which quantification occurs is tracked by qu_ar and the variables qu_lo,
    qu_hi represent the bounds of the currently tracked interval. The result of the
    quantified expression is tracked by qu_P, whose value is true iff P holds for
    all elements in a in the interval [qu_lo, qu_hi). The rewrite rules for stores,
    selects and assignments of universally quantified expressions are then defined
    as follows. For stores, the first if-branch resets the tracking to the one element
    interval [i, i + 1) when accessing elements far outside of the currently tracked
    interval, or if we are tracking the empty interval (as is the case at initialisation).
    If an access occurs immediately adjacent to the currently tracked interval (e.g.,
    if i = qu_lo − 1), then that element is added to the tracked interval, and the

                                             12
  Ω∀,P (Instrumentation operator)
    G∀,P (Ghost variables)
    qu_ar : Array Int, qu_lo, qu_hi : Int, qu_P : Bool
    init(qu_ar) = [ ], init(qu_lo) = 0, init(qu_hi) = 0
    init(qu_P)   = true

    R∀,P (Rewrite rules)
    a’ = store(a, i, x);
      1    a ’ = store (a , i , x ) ;
      2    if ( qu_lo == qu_hi ||        i < qu_lo - 1 || i > qu_hi ||
      3         ( P (x , i ) && ! qu_P   && qu_lo <= i && i < qu_hi ) ) {
      4       qu_lo = i ;                   // Reset , because either :
      5       qu_hi = i + 1;                // - tracking empty interval
      6       qu_P = P (x , i ) ;           // - storing far outside interval
      7    } else {                         // - possibly o v e r w r i t i n g sole false
      8       assert ( qu_ar == a ) ;
      9       qu_P = qu_P && P (x ,      i);
      10      if ( qu_lo - 1 == i )      {
      11            qu_lo = i ;                 // D e c r e m e n t lower bound by 1
      12      } else if ( qu_hi ==       i) {
      13            qu_hi = i + 1;              // I n c r e m e n t upper bound by 1
      14      }
      15   }
      16   qu_ar = a ’;
    x = select(a, i);             similar to store
    b = forall(a, l, u,λx.P);
      1    if ( u <= l ) {
      2      b = true ;
      3    } else {
      4      if ( qu_P ) {
      5         assert ( qu_ar == a && l >= qu_lo && u <= qu_hi ) ;
      6      } else {
      7         assert ( qu_ar == a && l <= qu_lo && u >= qu_hi ) ;
      8      }
      9      b = qu_P ;
      10   }

    I∀,P (Instrumentation Invariant)
    qu_lo = qu_hi ∨
        (qu_lo < qu_hi ∧ qu_P = forall(qu_ar, qu_lo, qu_hi,λ(x, i).P))



 Fig. 4: Definition of an instrumentation operator for universal quantification




value of qu_P is updated to also account for the value of P at index i. If instead
the access is within the tracked interval, then we either reset the interval (if
qu_P is false) or keep the interval unchanged (if qu_P is true). Rewrites of
selects are similar to stores, except tracking does not need to be reset when
reading inside the tracked interval. For rewrites of quantified expressions, if the
quantified interval is empty, b is assigned true. Otherwise, assertions check that
the tracked interval matches the quantified interval before assigning t to qu_P.

                                                    13
If qu_P is true, then it is sufficient that quantification occurs over a sub-interval
of the tracked interval, and vice versa if qu_P is false.
    The result of applying Ω∀,P to the program in Figure 3 is shown in Ap-
pendix C. As exhibited by the experiments in Section 5, the resulting program
is in many cases easier to verify by state-of-the-art verification tools. Note that
the instrumentation operator defined is only one possibility among many. For
example, one could track several ranges simultaneously over the array in ques-
tion, or also track the index of some element in the array over which P holds, or
make different choices on stores outside of the tracked interval.
    The following lemma establishes correctness of the instrumentation operator.
The proof can be found in Appendix D.
Lemma 2 (Correctness of Ω∀,P ). Ω∀,P is an instrumentation operator, i.e.,
it adheres to the constraints imposed in Definition 1.


4.2   Instrumentation Operators for Aggregation over Arrays

We now turn to the verification of safety properties with aggregation. As ex-
amples of aggregation, we consider in particular the operators \sum and \max,
calculating the sum and maximum value of an array, respectively. Aggregation
is supported in the form of extended quantifiers in the specification languages
JML [32] and ACSL [6], and is frequently needed for the specification of func-
tional correctness properties. Although commonly used, most verification tools
do not support aggregation, so that properties involving aggregation have to
be manually rewritten using standard quantifiers, pure recursive functions, or
ghost code involving loops. This reduction step is error-prone, and represents an
additional complication for automatic verification approaches, but can be han-
dled elegantly using the instrumentation framework. For generality, we formalise
aggregation over arrays with the help of monoid homomorphisms.
Definition 4 (Monoid). A monoid is a structure (M, ◦, e) consisting of a non-
empty set M , a binary associative operation ◦ on M , and a neutral element e ∈
M . A monoid is commutative if ◦ is commutative. A monoid is cancellative if
x ◦ y = x ◦ z implies y = z, and y ◦ x = z ◦ x implies y = z, for all x, y, z ∈ M .
   For aggregation, we model finite intervals of arrays using the cancellative
monoid (D∗ , ·, ǫ) of finite sequences over some data domain D. The concatenation
operator · is non-commutative.

Definition 5 (Monoid Homomorphism). A monoid homomorphism is a
function h : M1 → M2 between monoids (M1 , ◦1 , e1 ) and (M2 , ◦2 , e2 ) with the
properties h(x ◦1 y) = h(x) ◦2 h(y) and h(e1 ) = e2 .

    Ordinary quantifiers can be modelled as homormorphisms D∗ → , so thatB
the instrumentation in this section strictly generalizes Section 4.1. A second clas-
sical example is the computation of the maximum (similarly, minimum) value
in a sequence. For the domain of integers, the natural monoid to use is the

                                         14
           Z
algebra ( −∞ , max, −∞) of integers extended with −∞,4 and the homomor-
phism hmax is generated by mapping singleton sequences hni to the value n. A
third example is the computation of the element sum of an integer sequence,
corresponding to the monoid (Z , +, 0) and the homomorphism hsum . Similarly,
the number of occurrences of some element can be computed. The considered
monoid in the last two cases of aggregation is even cancellative.

Programming Language with Aggregation We extend our core program-
ming language with expressions aggregateM,h (hExpr i,hExpr i,hExpr i), and use
monoid homomorphisms to formalise them. Recall that we denote by Dσ the do-
main of a program type σ.
Definition 6. Let Array σ be an array type, σM a program type, M a commuta-
tive monoid that is a subset of DσM , and h : Dσ∗ → M a monoid homomorphism.
Let furthermore ar be an expression of type Array σ, and l and u integer expres-
sions. Then, aggregateM,h (ar ,l,u) is an expression of type σM , with semantics
defined by:

JaggregateM,h (ar ,l,u)Ks = h(hJar Ks (JlKs ), Jar Ks (JlKs +1), . . . , Jar Ks (JuKs −1)i)

Intuitively, the expression aggregateM,h (ar ,l,u) denotes the result of applying
the homomorphism h to the slice ar [l .. u − 1] of the array ar . As a convention,
in case u < l we assume that the result of aggregate is h(hi). As with array
accesses, we assume also that aggregate only occurs in normalised statements
of the form t = aggregateM,h (ar ,l,u).
    In our examples, we use derived operations as found in ACSL: \max as short-
hand notation for aggregate(Z−∞ ,max,−∞),hmax 5 , and \sum as short-hand nota-
tion for aggregate(Z,+,0),hsum .

An Instrumentation Operator for Maximum For \max, an operator Ωmax =
(Gmax , Rmax , Imax ) can be defined similarly to the operator Ω∀,P from Section 4.1,
in that the maximum value in a particular interval of the array is tracked. One
key difference is that an extra ghost variable ag_max_idx is added to track an
array index where the maximum value of the array interval is stored, in order
to not have to reset tracking on every store inside of the tracked interval. A
complete definition is proposed in Appendix E.

An instrumentation operator for Sum Cancellative aggregation is aggrega-
tion based on a cancellative monoid. Cancellative aggregation makes it possible
to track aggregate values faithfully even when storing inside of the tracked in-
terval, unlike \max and universal quantification. An example of a cancellative
operator is the aggregate \sum.
4
    For machine integers, −∞ could be replaced with INT_MIN.
5
    With a slight abuse of the framework, we assume that Z−∞ is represented by the pro-
    gram type Int, mapping −∞ to some fixed integer number. More elegant solutions
    are not difficult to devise, but add unnecessary complexity.


                                            15
  Ωsum (Instrumentation operator)
    Gsum (Ghost variables)
    ag_lo, ag_hi, ag_sum : Int, ag_ar : Array Int
    init(ag_lo) = init(ag_hi) = init(ag_sum) = 0, init(ag_ar) = [ ]

    Rsum (Rewrite rules)
    a’ = store(a, i, x)
       1   a ’ = store (a , i , x ) ;
       2   if ( ag_lo == ag_hi || i < ag_lo - 1 || i > ag_hi ) {
       3        ag_lo         = i;         // Reset , because either :
       4        ag_hi         = i + 1;     // - tracking empty interval
       5        ag_sum        = x;         // - storing far outside interval
       6   } else {
       7        assert ( ag_ar == a ) ;
       8        if ( ag_lo <= i && i < ag_hi ) {
       9             // Subtract previous value from sum
      10             ag_sum = ag_sum - select ( ag_ar , i ) ;
      11        } else if ( ag_lo - 1 == i ) {
      12             ag_lo = i ;           // Decrease lower bound by 1
      13        } else if ( ag_hi == i ) {
      14             ag_hi = i + 1;        // Increase upper bound by 1
      15        }
      16        ag_sum = ag_sum + x ;      // Add new value to sum
      17   }
      18   ag_ar = a ’;
    x = select(a, i)              code similar to rewrites of store
    r = \sum(a, l, u)
       1   if ( u <= l ) {
       2     t = 0;
       3   } else {
       4     assert ( ag_ar == a && l == ag_lo && u == ag_hi ) ;
       5     t = ag_sum ;
       6   }

    Isum (Instrumentation invariant)
    ag_lo = ag_hi ∨ ag_sum = sum(ag_ar, ag_lo, ag_hi)



                 Fig. 5: Definition of an instrument operator Ωsum



    The instrumentation operator Ωsum = (Gsum , Rsum , Isum ) is defined in Figure 5.
The instrumentation code tracks the sum of values in the interval, and when in-
creasing the bounds of the tracked interval, the new values are simply added to
the tracked sum. Since \sum is cancellative, when storing inside of the tracked
interval, the previous value at the index being written to is first subtracted from
the sum, before adding the new value, ensuring that the correct aggregate value
is computed. The following correctness result is shown in Appendix F.


Lemma 3 (Correctness of Ωsum ). Ωsum is an instrumentation operator, i.e.,
it adheres to the constraints imposed in Definition 1.


                                          16
Deductive Verification of Instrumentation Operators As stated in Section 2.2,
instrumentation operators may be verified independently of the programs to
be instrumented. The operators described in this paper, i.e. square, universal
quantification, maximum, and sum, have been verified in the verification tool
Frama-C [14]. The verified instrumentations are adaptations for the C language
semantics and execution model. More specifically, the adapted operators assume
C native arrays, rather than functional ones.


5     Evaluation
5.1   Implementation
To evaluate our instrumentation framework, we have implemented the instru-
mentation operators for quantifiers and aggregation over arrays. The implemen-
tation is done over constrained Horn clauses (CHCs), by adding the rewrite rules
defined in Section 4 to Eldarica [29], an open-source solver for CHCs. We also
implemented the automatic application of the instrumentation operators, largely
following Algorithm 1 but with a few minor changes due to the CHC setting.
The CHC setting makes our implementation available to various CHC-based ver-
ification tools, for instance JayHorn (Java) [31], Korn (C) [18], RustHorn
(Rust) [35], SeaHorn (C/LLVM) [25] and TriCera (C) [19].
    In order to evaluate our approach at the level of C programs, we extended
TriCera, an open-source assertion-based model checker that translates C pro-
grams into a set of CHCs and relies on Eldarica as back-end solver. TriCera
is extended to parse quantifiers and aggregation operators in its input C pro-
grams and to encode them as part of the translation into CHCs. We call the
resulting toolchain MonoCera. An artefact that includes MonoCera and the
benchmarks is available online [4].
    To handle complicated access patterns, for instance a program processing
an array from the beginning and end at the same time, the implementation
can apply multiple instrumentation operators simultaneously; the number of
operators is incremented when Algorithm 1 returns Inconclusive.

5.2   Experiments and Comparisons
To assess our implementation, we assembled a test suite and carried out ex-
periments comparing MonoCera with the state-of-the-art C model checkers
CPAchecker 2.1.1 [10], SeaHorn 10.0.0 [25] and TriCera 0.2. It should be
noted that deductive verification frameworks, such as Dafny and Frama-C, can
handle, for example, the program in Figure 3 if they are provided with a man-
ually written loop invariant; however, since MonoCera relies on automatic
techniques for invariant inference, we only benchmark against tools using simi-
lar automatic techniques. We also excluded VeriAbs [1], since its licence does
not permit its use for scientific evaluation.
    The tools were set up, as far as possible, with equivalent configurations; for
instance, to use the SMT-LIB theory of arrays [5] in order to model C arrays, and

                                       17
          Verification results           Ver. time  Inst. space Inst. steps
       #Tests Mono Tri Sea CPA          Min Max Avg Max Avg      Max Avg
 min    17      9     2   2    2        22 59 33      27    11    55    24
 max    12      8     2   3    3        21 285 76     108 21      96    30
 sum    26      16    3   3    3        26 245 78    2916 188    284 36
 forall 96      30    1   0    2        14 236 91   59049 2446   334 59

Table 3: Results for MonoCera (Mono), TriCera (Tri), SeaHorn (Sea),
and CPAchecker (CPA). For MonoCera, also statistics are given for verifi-
cation time (s), size of the instrumentation search space, and search iterations.


a mathematical (as opposed to machine) semantics of integers. CPAchecker
was configured to use k-induction [9], which was the only configuration that
worked in our tests using mathematical integers. SeaHorn was run using the
default settings. All tests were run on a Linux machine with AMD Opteron 2220
SE @ 2.8 GHz and 6 GB RAM with a timeout of 300 seconds.

Test Suite. The comparison includes a set of programs calculating properties
related to the quantification and aggregation properties over arrays. The bench-
marks and verification results are summarised in Table 3. The benchmark suite
contains programs ranging between 16 to 117 LOC and is comprised of two parts:
(i) 117 programs taken from the SV-COMP repository [8], and (ii) 26 programs
crafted by the authors (min: 6, max: 8, sum: 9, forall: 3).
     To construct the SV-COMP benchmark set for MonoCera we gathered
all test files from the directories prefixed with array or loop, and singled out
programs containing some assert statement that could be rewritten using a quan-
tifier or an aggregation operator over a single array. For example, loops

               for (int i = 0; i < N; i++) assert(a[i] <= 0);

can be rewritten using forall or max operators. We created a benchmark for
each possible rewriting; for instance, in the case of max, by rewriting the loop
into assert(\max(a, 0, N) <= 0). The original benchmarks were used for the
evaluation of the other tools, none of which supported (extended) quantifiers.
    In (ii), we crafted 9 programs that make use of aggregation or quantifiers,
and derived further benchmarks by considering different array sizes (10, 100 and
unbounded size); one combination (unbounded array inside a struct) had to be
excluded, as it is not valid C. In order to evaluate other tools on our crafted
benchmarks, we reversed the process described for the SV-COMP benchmarks
and translated the operators into corresponding loop constructs.

Results. In Table 3, we present the number of verified programs per instrumenta-
tion operator for each tool, as well as further statistics for MonoCera regarding
verification times and instrumentation search space. The “Inst. space” column
indicates the size of the instrumentation search space (i.e., number of instrumen-
tations producible by applying the non-deterministic instrumentation operator).

                                       18
“Inst. steps” column indicates the number of attempted instrumentations, i.e.,
number of iterations in the while-loop in Algorithm 1. In some cases there are
more iterations than the size of the search space, which is because the check in
Algorithm 1, line 5 can time out, and might be attempted again at a later point
in our implementation. In Appendix G, we provide tables listing all results per
benchmark for each tool.
    For the SV-COMP benchmarks, CPAchecker managed to verify 1 program,
while SeaHorn and TriCera could not verify any programs. MonoCera ver-
ified in total 42 programs from SV-COMP. Regarding the crafted benchmarks,
several tools could verify the examples with array size 10. However, when the
array size was 100 or unbounded, only MonoCera succeeded.


6   Related Work

It is common practice, in both model checking and deductive verification, to
translate high-level specifications to low-level specifications prior to verification
(e.g., [13,17,12,36]). Such translations often make use of ghost variables and ghost
code, although relatively little systematic research has been done on the required
properties of ghost code [21]. The addition of ghost variables to a program for
tracking the value of complex expressions also has similarities with the concept
of term abstraction in Horn solving [3]. To the best of our knowledge, we are
presenting the first general framework for automatic program instrumentation.
    A lot of research in software model checking considered the handling of stan-
dard quantifiers ∀, ∃ over arrays. In the setting of constrained Horn clauses,
properties with universal quantifiers can sometimes be reduced to quantifier-free
reasoning over non-linear Horn clauses [12,36]. Our approach follows the same
philosophy of applying an up-front program transformation, but in a more gen-
eral setting. Various direct approaches to infer quantified array invariants have
been proposed as well: e.g., by extending the IC3 algorithm [26], syntax-guided
synthesis [20], learning [23], by solving recurrence equations [28], backward reach-
ability [3], or superposition [24]. To the best of our knowledge, such methods have
not been extended to aggregation.
    Deductive verification tools usually have rich support for quantified specifi-
cations, but rely on auxiliary assertions like loop invariants provided by the user,
and on SMT solvers or automated theorem provers for quantifier reasoning. Al-
though several deductive verification tools can parse extended quantifiers, few
offer support for reasoning about them. Our work is closest to the method for
handling comprehension operators in Spec# [34], which relies on code annota-
tions provided by the user, but provides heuristics to automatically verify such
annotations. The code instrumentation presented in this paper has similarity
with the proof rules in Spec#; the main differences are that our method is based
on an upfront program transformation, and that we aim at automatically find-
ing required program invariants, as opposed to only verifying their correctness.
The KeY tool provides proof rules similar to the ones in Spec# for some of the
JML extended quantifiers [2]; those proof rules can be applied manually to verify

                                         19
human-written invariants. The Frama-C system [14] can parse ACSL extended
quantifiers [6], but, to the best of our knowledge, none of the Frama-C plug-
ins can automatically process such quantifiers. Other systems, e.g., Dafny [33],
require users to manually define aggregation operators as recursive functions.
    In the theory of algebraic data-types, several transformation-based approaches
have been proposed to verify properties that involve recursive functions or cata-
morphisms [30,16]. Aggregation over arrays resembles the evaluation of recur-
sive functions over data-types; a major difference is that data-types are more
restricted with respect to accessing and updating data than arrays.
    Array folds logic (AFL) [15] is a decidable logic in which properties on arrays
beyond standard quantification can be expressed: for instance, counting the num-
ber of elements with some property. Similar properties can be expressed using
automata on data words [40], or in variants of monadic second-order logic [37].
Such languages can be seen as alternative formalisms to aggregation or extended
quantifiers; they do not cover, however, all kinds of aggregation we are interested
in. Array sums cannot be expressed in AFL or data automata, for instance.


7   Conclusion

We have presented a framework for automatic and provably correct program
instrumentation, allowing the automatic verification of programs containing cer-
tain expressive language constructs, which are not directly supported by the
existing automatic verification tools. Our experiments with a prototypical im-
plementation, in the tool MonoCera, show that our method is able to automat-
ically verify a significant number of benchmark programs involving quantification
and aggregation over arrays that are beyond the scope of other tools.
    At this point, there are still various other benchmarks that MonoCera
(as well as other tools) cannot verify. We believe that many of those bench-
marks are in reach of our method, because of the generality of our approach.
Since adding ghost code is known to be a powerful specification paradigm, more
powerful instrumentation operators can be easily formulated. Our approach is
also parameterised on the applied instrumentation operators, meaning it can be
adapted to any kind of program by tailoring the right instrumentation operator.
    In future work, we plan to develop a library of instrumentation operators
for a wide range of problematic language constructs, including various classes of
arithmetic expressions such as non-linear arithmetic, other types of structures
with regular access patterns such as binary heaps, and general linked-data struc-
tures. We also plan to improve the evaluation by extending the benchmark suite.
In a preliminary evaluation on a set of unsafe test programs from the SV-COMP
library, the results show that using the instrumentation framework does not
outperform state-of-the art model checkers for such programs and further exper-
iments are needed to identify how our framework can be used in this context.
Another line of work is the establishment of stronger completeness results than
the weak completeness result presented here, for specific programming language
fragments.

                                        20
Acknowledgements. This work has been partially funded by the Swedish Vin-
nova FFI Programme under grant 2021-02519, the Swedish Research Council
(VR) under grant 2018-04727, the Swedish Foundation for Strategic Research
(SSF) under the project WebSec (Ref. RIT17-0011), and the Wallenberg project
UPDATE. We are also grateful for the opportunity to discuss the research at
the Dagstuhl Seminar 22451 on “Principles of Contract Languages.”




                                    21
References
 1. Afzal, M., Chakraborty, S., Chauhan, A., Chimdyalwar, B., Darke, P., Gupta, A.,
    Kumar, S., M, C.B., Unadkat, D., Venkatesh, R.: Veriabs : Verification by ab-
    straction and test generation (competition contribution). In: Biere, A., Parker, D.
    (eds.) Tools and Algorithms for the Construction and Analysis of Systems - 26th
    International Conference, TACAS 2020, Held as Part of the European Joint Con-
    ferences on Theory and Practice of Software, ETAPS 2020, Dublin, Ireland, April
    25-30, 2020, Proceedings, Part II. Lecture Notes in Computer Science, vol. 12079,
    pp. 383–387. Springer (2020), https://doi.org/10.1007/978-3-030-45237-7_25
 2. Ahrendt, W., Beckert, B., Bubel, R., Hähnle, R., Schmitt, P.H., Ulbrich, M.
    (eds.): Deductive Software Verification - The KeY Book - From Theory to
    Practice, Lecture Notes in Computer Science, vol. 10001. Springer (2016),
    https://doi.org/10.1007/978-3-319-49812-6
 3. Alberti, F., Bruttomesso, R., Ghilardi, S., Ranise, S., Sharygina, N.: Lazy ab-
    straction with interpolants for arrays. In: Bjørner, N.S., Voronkov, A. (eds.)
    Logic for Programming, Artificial Intelligence, and Reasoning - 18th Interna-
    tional Conference, LPAR-18, Mérida, Venezuela, March 11-15, 2012. Proceed-
    ings. Lecture Notes in Computer Science, vol. 7180, pp. 46–61. Springer (2012),
    https://doi.org/10.1007/978-3-642-28717-6_7
 4. Amilon, J., Esen, Z., Gurov, D., Lidström, C., Rümmer, P.: Artifact for the CAV
    2023 paper "Automatic Program Instrumentation for Automatic Verification" (Apr
    2023), https://doi.org/10.5281/zenodo.7875416
 5. Barrett, C., Fontaine, P., Tinelli, C.: The SMT-LIB Standard: Version 2.6. Tech.
    rep., Department of Computer Science, The University of Iowa (2017), available
    at www.SMT-LIB.org
 6. Baudin, P., Filliâtre, J.C., Marché, C., Monate, B., Moy, Y., Prevosto, V.: ACSL:
    ANSI/ISO C Specification Language, http://frama-c.com/acsl.html
 7. Beyer, D.: Progress on software verification: SV-COMP 2022. In: Fisman, D., Rosu,
    G. (eds.) Tools and Algorithms for the Construction and Analysis of Systems - 28th
    International Conference, TACAS 2022, Held as Part of the European Joint Confer-
    ences on Theory and Practice of Software, ETAPS 2022, Munich, Germany, April
    2-7, 2022, Proceedings, Part II. Lecture Notes in Computer Science, vol. 13244,
    pp. 375–402. Springer (2022), https://doi.org/10.1007/978-3-030-99527-0_20
 8. Beyer, D.: SV-Benchmarks: Benchmark Set for Software Verifica-
    tion and Testing (SV-COMP 2022 and Test-Comp 2022) (Jan 2022),
    https://doi.org/10.5281/zenodo.5831003
 9. Beyer, D., Dangl, M., Wendler, P.: Boosting k-induction with continuously-refined
    invariants. In: Kroening, D., Pasareanu, C.S. (eds.) Computer Aided Verification
    - 27th International Conference, CAV 2015, San Francisco, CA, USA, July 18-
    24, 2015, Proceedings, Part I. Lecture Notes in Computer Science, vol. 9206, pp.
    622–640. Springer (2015), https://doi.org/10.1007/978-3-319-21690-4_42
10. Beyer, D., Keremoglu, M.E.: CPAchecker: A tool for configurable software verifi-
    cation. In: Gopalakrishnan, G., Qadeer, S. (eds.) Computer Aided Verification -
    23rd International Conference, CAV 2011, Snowbird, UT, USA, July 14-20, 2011.
    Proceedings. Lecture Notes in Computer Science, vol. 6806, pp. 184–190. Springer
    (2011), https://doi.org/10.1007/978-3-642-22110-1_16
11. Bjørner, N., Gurfinkel, A., McMillan, K.L., Rybalchenko, A.: Horn clause
    solvers for program verification. In: Beklemishev, L.D., Blass, A., Dershowitz,
    N., Finkbeiner, B., Schulte, W. (eds.) Fields of Logic and Computation II


                                          22
    - Essays Dedicated to Yuri Gurevich on the Occasion of His 75th Birthday.
    Lecture Notes in Computer Science, vol. 9300, pp. 24–51. Springer (2015),
    https://doi.org/10.1007/978-3-319-23534-9_2
12. Bjørner, N.S., McMillan, K.L., Rybalchenko, A.: On solving universally quanti-
    fied Horn clauses. In: Logozzo, F., Fähndrich, M. (eds.) Static Analysis - 20th
    International Symposium, SAS 2013, Seattle, WA, USA, June 20-22, 2013. Pro-
    ceedings. Lecture Notes in Computer Science, vol. 7935, pp. 105–125. Springer
    (2013), https://doi.org/10.1007/978-3-642-38856-9_8
13. Clarke, E.M., Henzinger, T.A., Veith, H., Bloem, R. (eds.): Handbook of Model
    Checking. Springer (2018), https://doi.org/10.1007/978-3-319-10575-8
14. Cuoq, P., Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski,
    B.: Frama-C - A software analysis perspective. In: Eleftherakis, G., Hinchey, M.,
    Holcombe, M. (eds.) Software Engineering and Formal Methods - 10th Interna-
    tional Conference, SEFM 2012, Thessaloniki, Greece, October 1-5, 2012. Proceed-
    ings. Lecture Notes in Computer Science, vol. 7504, pp. 233–247. Springer (2012),
    https://doi.org/10.1007/978-3-642-33826-7_16
15. Daca, P., Henzinger, T.A., Kupriyanov, A.: Array folds logic. In: Chaudhuri,
    S., Farzan, A. (eds.) Computer Aided Verification - 28th International Confer-
    ence, CAV 2016, Toronto, ON, Canada, July 17-23, 2016, Proceedings, Part II.
    Lecture Notes in Computer Science, vol. 9780, pp. 230–248. Springer (2016),
    https://doi.org/10.1007/978-3-319-41540-6_13
16. De Angelis, E., Proietti, M., Fioravanti, F., Pettorossi, A.: Verifying catamorphism-
    based contracts using constrained Horn clauses. Theory Pract. Log. Program.
    22(4), 555–572 (2022), https://doi.org/10.1017/S1471068422000175
17. Donaldson, A.F., Kroening, D., Rümmer, P.: Automatic analysis of scratch-pad
    memory code for heterogeneous multicore processors. In: Esparza, J., Majumdar,
    R. (eds.) Tools and Algorithms for the Construction and Analysis of Systems.
    LNCS, vol. 6015, pp. 280–295. Springer (2010)
18. Ernst, G.: Korn - software verification with Horn clauses (competition contribu-
    tion). In: Sankaranarayanan, S., Sharygina, N. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems - 29th International Conference, TACAS
    2023, Held as Part of the European Joint Conferences on Theory and Practice
    of Software, ETAPS 2022, Paris, France, April 22-27, 2023, Proceedings, Part
    II. Lecture Notes in Computer Science, vol. 13994, pp. 559–564. Springer (2023),
    https://doi.org/10.1007/978-3-031-30820-8_36
19. Esen, Z., Rümmer, P.: TriCera: Verifying C programs using the theory of heaps.
    In: 2022 Formal Methods in Computer Aided Design, FMCAD 2022, Trento, Italy,
    October 17 - October 21, 2022 (2022), (To appear)
20. Fedyukovich, G., Prabhu, S., Madhukar, K., Gupta, A.: Quantified invariants via
    syntax-guided synthesis. In: Dillig, I., Tasiran, S. (eds.) Computer Aided Verifica-
    tion - 31st International Conference, CAV 2019, New York City, NY, USA, July
    15-18, 2019, Proceedings, Part I. Lecture Notes in Computer Science, vol. 11561,
    pp. 259–277. Springer (2019), https://doi.org/10.1007/978-3-030-25540-4_14
21. Filliâtre,   J.,    Gondelman,       L.,    Paskevich,      A.:     The     spirit of
    ghost code. Formal Methods Syst. Des. 48(3), 152–174 (2016),
    https://doi.org/10.1007/s10703-016-0243-x
22. Flanagan, C., Saxe, J.B.: Avoiding exponential explosion: generating compact ver-
    ification conditions. In: Hankin, C., Schmidt, D. (eds.) Proceedings of: Symposium
    on Principles of Programming Languages (POPL’01). pp. 193–205. ACM (2001).
    https://doi.org/10.1145/360204.360220


                                           23
23. Garg, P., Löding, C., Madhusudan, P., Neider, D.: Learning universally
    quantified invariants of linear data structures. In: Sharygina, N., Veith,
    H. (eds.) Computer Aided Verification - 25th International Conference,
    CAV 2013, Saint Petersburg, Russia, July 13-19, 2013. Proceedings. Lec-
    ture Notes in Computer Science, vol. 8044, pp. 813–829. Springer (2013),
    https://doi.org/10.1007/978-3-642-39799-8_57
24. Georgiou, P., Gleiss, B., Kovács, L.: Trace logic for inductive loop rea-
    soning. In: 2020 Formal Methods in Computer Aided Design, FMCAD
    2020, Haifa, Israel, September 21-24, 2020. pp. 255–263. IEEE (2020),
    https://doi.org/10.34727/2020/isbn.978-3-85448-042-6_33
25. Gurfinkel, A., Kahsai, T., Komuravelli, A., Navas, J.A.: The SeaHorn Verification
    Framework. In: Kroening, D., Pasareanu, C.S. (eds.) Computer Aided Verification
    - 27th International Conference, CAV 2015, San Francisco, CA, USA, July 18-
    24, 2015, Proceedings, Part I. Lecture Notes in Computer Science, vol. 9206, pp.
    343–361. Springer (2015), https://doi.org/10.1007/978-3-319-21690-4_20
26. Gurfinkel, A., Shoham, S., Vizel, Y.: Quantifiers on demand. In: Lahiri, S.K., Wang,
    C. (eds.) Automated Technology for Verification and Analysis - 16th International
    Symposium, ATVA 2018, Los Angeles, CA, USA, October 7-10, 2018, Proceed-
    ings. Lecture Notes in Computer Science, vol. 11138, pp. 248–266. Springer (2018),
    https://doi.org/10.1007/978-3-030-01090-4_15
27. Harrison, J.: Handbook of Practical Logic and Automated Reasoning. Cambridge
    University Press (2009)
28. Henzinger, T.A., Hottelier, T., Kovács, L., Rybalchenko, A.: Aligators for ar-
    rays (tool paper). In: Fermüller, C.G., Voronkov, A. (eds.) Logic for Pro-
    gramming, Artificial Intelligence, and Reasoning - 17th International Confer-
    ence, LPAR-17, Yogyakarta, Indonesia, October 10-15, 2010. Proceedings. Lec-
    ture Notes in Computer Science, vol. 6397, pp. 348–356. Springer (2010),
    https://doi.org/10.1007/978-3-642-16242-8_25
29. Hojjat, H., Rümmer, P.: The ELDARICA Horn solver. In: FMCAD 2018. pp. 1–7
    (2018). https://doi.org/10.23919/FMCAD.2018.8603013
30. K., H.G.V., Shoham, S., Gurfinkel, A.: Solving constrained Horn clauses modulo
    algebraic data types and recursive functions. Proc. ACM Program. Lang. 6(POPL),
    1–29 (2022), https://doi.org/10.1145/3498722
31. Kahsai, T., Kersten, R., Rümmer, P., Schäf, M.: Quantified heap invariants for
    object-oriented programs. In: Eiter, T., Sands, D. (eds.) LPAR-21, 21st Interna-
    tional Conference on Logic for Programming, Artificial Intelligence and Reasoning,
    Maun, Botswana, May 7-12, 2017. EPiC Series in Computing, vol. 46, pp. 368–384.
    EasyChair (2017), https://easychair.org/publications/paper/Pmh
32. Leavens, G.T., Baker, A.L., Ruby, C.: JML: A notation for detailed de-
    sign. In: Kilov, H., Rumpe, B., Simmonds, I. (eds.) Behavioral Specifica-
    tions of Businesses and Systems, The Kluwer International Series in En-
    gineering and Computer Science, vol. 523, pp. 175–188. Springer (1999),
    https://doi.org/10.1007/978-1-4615-5229-1_12
33. Leino, K.R.M.: Dafny: An automatic program verifier for functional correct-
    ness. In: Clarke, E.M., Voronkov, A. (eds.) Logic for Programming, Ar-
    tificial Intelligence, and Reasoning - 16th International Conference, LPAR-
    16, Dakar, Senegal, April 25-May 1, 2010, Revised Selected Papers. Lec-
    ture Notes in Computer Science, vol. 6355, pp. 348–370. Springer (2010),
    https://doi.org/10.1007/978-3-642-17511-4_20


                                          24
34. Leino, K.R.M., Monahan, R.: Reasoning about comprehensions with first-order
    SMT solvers. In: Shin, S.Y., Ossowski, S. (eds.) Proceedings of the 2009 ACM
    Symposium on Applied Computing (SAC), Honolulu, Hawaii, USA, March 9-12,
    2009. pp. 615–622. ACM (2009), https://doi.org/10.1145/1529282.1529411
35. Matsushita, Y., Tsukada, T., Kobayashi, N.: RustHorn: CHC-based verification
    for Rust programs. ACM Trans. Program. Lang. Syst. 43(4), 15:1–15:54 (2021),
    https://doi.org/10.1145/3462205
36. Monniaux, D., Gonnord, L.: Cell morphing: From array programs to array-
    free Horn clauses. In: Rival, X. (ed.) Static Analysis - 23rd International Sym-
    posium, SAS 2016, Edinburgh, UK, September 8-10, 2016, Proceedings. Lec-
    ture Notes in Computer Science, vol. 9837, pp. 361–382. Springer (2016),
    https://doi.org/10.1007/978-3-662-53413-7_18
37. Neven, F., Schwentick, T., Vianu, V.: Finite state machines for strings
    over infinite alphabets. ACM Trans. Comput. Log. 5(3), 403–435 (2004),
    https://doi.org/10.1145/1013560.1013562
38. Priya, S., Zhou, X., Su, Y., Vizel, Y., Bao, Y., Gurfinkel, A.: Verifying verified code.
    In: Hou, Z., Ganesh, V. (eds.) Automated Technology for Verification and Anal-
    ysis - 19th International Symposium, ATVA 2021, Gold Coast, QLD, Australia,
    October 18-22, 2021, Proceedings. Lecture Notes in Computer Science, vol. 12971,
    pp. 187–202. Springer (2021), https://doi.org/10.1007/978-3-030-88885-5_13
39. Reynolds, J.C.: Separation logic: A logic for shared mutable data structures. In:
    17th IEEE Symposium on Logic in Computer Science (LICS 2002), 22-25 July 2002,
    Copenhagen, Denmark, Proceedings. pp. 55–74. IEEE Computer Society (2002),
    https://doi.org/10.1109/LICS.2002.1029817
40. Segoufin, L.: Automata and logics for words and trees over an infinite alphabet. In:
    Ésik, Z. (ed.) Computer Science Logic, 20th International Workshop, CSL 2006,
    15th Annual Conference of the EACSL, Szeged, Hungary, September 25-29, 2006,
    Proceedings. Lecture Notes in Computer Science, vol. 4207, pp. 41–57. Springer
    (2006), https://doi.org/10.1007/11874683_3




                                            25
A    Typing Rules of the Core Language

The typing rules of the core language are presented in Table 4.



                   Table 4: Typing rules of the core language.
                                                                  x ∈ X , α(x) = σ
       hDecimalNumber i : Int     true : Bool     false : Bool         x:σ
           s:σ t:σ        s : Int t : Int    s : Int t : Int     s : Int t : Int
          s == t : Bool     s <= t : Bool       s + t : Int         s * t : Int
                  c : Bool    s : Bool t : Bool     s : Bool t : Bool
                  !c : Bool      s && t : Bool         s || t : Bool
                  a : Array σ t : Int       a : Array σ s : Int t : σ
                    select(a,t) : σ          store(a,s,t) : Array σ




B    Correctness of Instrumentation Search
Proof of Lemma 1 Algorithm 1 will return an instrumentation r of when it has
derived that Pr is correct; due to the soundness of instrumentation operators,
then also P is correct.
    Algorithm 1 will return Incorrect only when it has discovered a counterex-
ample for Pr that ends in a failing assertion that also occurs in P , i.e., that has
not been introduced as a part of instrumentation. Due to the weak completeness
of instrumentation operators, then also P is incorrect.
    Assuming that there is an r such that Pr is correct, the correctness also
of P follows. Algorithm 1 can then not return the result Incorrect . To see that
Algorithm 1 will eventually find some instrumentation r′ such that Pr′ is correct,
note that the algorithm will in lines 12–13 only eliminate instrumentations r′′
such that Pr′′ is incorrect.


C    Example of Instrumented Program for Universal
     Quantification
An example of an instrumentation using the instrumentation operator Σ∀,P is
presented in Figure 6.




                                            26
1  Int qu_lo = 0; qu_hi = 0;
2  Int qu_ar = [];
 3 Bool qu_P = true ;

 4 Int N = nondet ;

 5 assume ( N > 0) ;

 6 Array Int a = const (0 , N ) ;

 7 Int i = 0;

 8 while ( i < N ) {

 9      a ’ = store (a , i , x ) ;
10      if ( qu_lo == qu_hi || i < qu_lo - 1 || i > qu_hi ||
11            ( P (x , i ) && ! qu_P && qu_lo <= i && i < qu_hi ) ) {
12         qu_lo = i ;              // Reset , because either :
13         qu_hi = i + 1;           // - tracking empty interval
14         qu_P = P (x , i ) ;      // - storing far outside interval
15      } else {                    // - possibly overwriting sole false
16         assert ( qu_ar == a ) ;
17         qu_P = qu_P && P (x , i ) ;
18         if ( qu_lo - 1 == i ) {
19                qu_lo = i ;            // Decrement lower bound by 1
20         } else if ( qu_hi == i ) {
21                qu_hi = i + 1;         // Increment upper bound by 1
22         }
23      }
24      qu_ar = a ’;
25      a = store (a , i , i ) ;
26      i = i + 1;
27 }

28 Bool b ;

29 if ( u <= l ) {

30   b = true ;
31 } else {

32   if ( qu_P ) {
33      assert ( qu_ar == a ∧ l >= qu_lo ∧ u <= qu_hi ) ;
34   } else {
35      assert ( qu_ar == a ∧ l <= qu_lo ∧ u >= qu_hi ) ;
36   }
37   b = qu_P ;
38 }

39 assert ( b ) ;




    Fig. 6: Resulting program from applying the instrumentation Ω∀,P to the pro-
    gram in Figure 3.




                                        27
D    Correctness of Instrumentation Operator for Universal
     Quantification

Proof (Lemma 2). First, observe that qu_lo and qu_hi are initialised to the
same value, so the instrumentation invariant is established. It then remains to
show that the rewrite rules adhere to the remaining constraints. The case where
we rewrite normalised select statements is left out, as it is similar to store.
    It is clear that all the instrumented code terminates, and that rewrites of
store only assign to ghost variables and to a’, and rewrites of forall expres-
sions only to the assigned variable b.
    Rewrites of forall do not assign to ghost variables, and so preserve I. For
rewrites of store, we assume I, and for the proof we treat the assertion in the
rewrite rule as an assumption. In the cases of an empty interval, a store outside of
the tracked interval, and when possibly overwriting a sole false value, since we
reset the bounds, and the tracked Boolean value, to only track a single element,
then qu_P has the correct value in the resulting array with the new bounds, and
since we assign qu_ar the result of the store, I is preserved. In the remaining
cases, by the invariant and the assertions qu_P is assigned the correct truth
value of the array being stored to, within the given bounds, by conjunction of
the previous quantified truth value and the evaluation of the predicate on the
new element. If the store occurs just outside the tracked bounds, also the bounds
are updated, and I is preserved.
    Finally, in rewrites of store, the assignment a’ = store(a, i, x); is not
changed, but only additional code is added that does not assign to program
variables, and so the semantics is preserved. In rewrites of forall, we assume I
and the assertion in the rewrite rule. Since by the invariant qu_P is the correct
value before the store, over qu_ar in the tracked interval, and since by the
assertion qu_ar is the same array as in the quantified expression, then qu_P is
also the correct truth value in a within the tracked bounds. Then, if tracked
value is true for the tracked interval, it must also be true for smaller intervals,
and if it is false it is also false for large intervals, and we assert this relation
between the tracked bounds and the actual bounds of the quantified expression.
Thus, b is assigned the result of the quantified expression, and the semantics is
preserved.                                                                         ⊓
                                                                                   ⊔


E    An Instrumentation Operator for \max

    The instrumentation operator Ωmax = (Gmax , Rmax , Imax ) is defined in Figure 7.
We assume here that the language has the special value −∞ or a similar con-
struct denoting the least possible value.2 Initialisation of a variable to _ means
it can be set to an arbitrary value. The rewrite rule for select statements is
similar to rewrites of store statements, except that the line 1 would be the orig-
inal select statement, and the reset (lines 4–7) is not necessary when reading
inside of the tracked interval.

                                        28
  Ωmax (Instrumentation operator)
    Gmax (Ghost variables)
    ag_lo, ag_hi, ag_max_idx, ag_max : Int, ag_ar : Array Int
    init(ag_lo) = init(ag_hi) = init(ag_max) = init(ag_max_idx) = 0,
    init(ag_ar) = _

    Rmax (Rewrite rules)
    a’ = store(a, i, x)
       1   a ’ = store (a , i , x ) ;
       2   if ( ag_lo == ag_hi || i        < ag_lo - 1 || i > ag_hi ||
       3        ( x < ag_max && i ==       a g _ m a x _ i d x) ) {
       4        ag_lo         = i;                 // Reset , because either :
       5        ag_hi         = i + 1;             // - tracking empty interval
       6        ag_max        = x;                 // - storing far outside interval
       7        ag_max_idx = i;                    // - o v e r w r i t i n g prev . max value
       8   } else {
       9        assert ( ag_ar == a ) ;
      10        if ( ag_max <= x ) {
      11             ag_max         = x;          // Track new max value ,
      12             ag_max_idx = i;              // and its index .
      13        }
      14        if ( ag_lo - 1 == i )      {
      15             ag_lo = i ;                  // Decrease lower bound by 1
      16        } else if ( ag_hi ==       i) {
      17             ag_hi = i + 1;               // Increase upper bound by 1
      18        }
      19   }
      20   ag_ar = a ’;
    x = select(a, i)                   code similar to rewrites of store
    r = \max(a, l, u)
       1   if ( u <= l ) {
       2     t = −∞;
       3   } else {
       4     assert ( ag_ar == a && l == ag_lo && u == ag_hi ) ;
       5     t = ag_max ;
       6   }

    Imax (Instrumentation invariant)
    ag_lo = ag_hi ∨ (ag_lo ≤ ag_max_idx < ag_hi ∧
                     ag_max = \max(ag_ar, ag_lo, ag_hi) ∧
                     ag_max = ag_ar[ag_max_idx])


                  Fig. 7: Definition of an instrument operator Ωmax



    The idea behind Ωmax is to keep track of the aggregate value in some interval
of the array as it is read from and written to. Uses of the aggregate function can
be replaced with this tracked value, asserting that the array and the bounds of
the interval of the array are equal to the array and bounds of the aggregate.
   In the instrumentation code for store, we have two main cases. In one case,
we reset the tracking of the max value, by setting bounds to only track the most
recent value. This is done because either the tracked interval is empty, and we are

                                                   29
not yet tracking any value, or an access is happening that is not adjacent to the
currently tracked interval, or the previously tracked max value is overwritten.
    In the other case, there is a store in an already tracked interval, or just
adjacent to it. If that is the case, we assert that the tracked array coincides with
the one being accessed. If the stored value is larger than the previous max value,
then we update the variables accordingly, and if the access is adjacent to the
previously tracked interval, we increase the interval to include it.
    Various design choices have been made in the instrumentation operator. For
example, when writing far outside of the interval, instrumentation could also
choose to ignore this access, and keep tracking the old interval. Another alter-
native is to assert that such writes do not occur, i.e., treating it as a failed
instrumentation, and try another one. There could also be several rewrite rules
matching this case, with a non-deterministic choice of which to use (if any), and
all choices could then be tried in a search for the most fitting instrumentation
(see Section 3). Assertions added in the instrumentation code could often be
replaced by conditionals, for instance ignoring an instrumented store in case the
array or bounds do not match. And instead of tracking a single array interval,
also more complicated subsets of an array could be tracked. All those choice are
possible, and can be analysed for correctness, within the framework introduced
in Section 2.
Lemma 4 (Correctness of Ωmax ). Ωmax is an instrumentation operator, i.e.,
it adheres to the constraints imposed in Definition 1.

Proof. To start with, observe that ag_lo and ag_hi are initialised to the same
value, so the instrumentation invariant is established. Next, we will show that
the rewrite rules adhere to the remaining constraints. The case where we rewrite
normalised select statements is left out, as it is similar to store.
     It is clear that all the instrumented code terminates, and that rewrites of
store only assign to ghost variables and to a’, and rewrites of \max only to the
assigned variable r.
     Rewrites of \max do not assign to ghost variables, and so preserve Imax . For
rewrites of store, we assume Imax , and for the proof we treat the assertion in
rewrite rule for stores as an assumption. In the cases of an empty interval, a
store outside of the tracked interval, and when overwriting the previous max
value, since we reset the bounds, the max value, and the index to only track
this element, then ag_max is the max value in the resulting array with the new
bounds, and since we assign ag_ar the result of the store, Imax is preserved. In
the remaining cases, by the invariant and the assertions ag_max is assigned the
max value of the array being stored to, within the given bounds. If the new value
is larger, we update ag_max and ag_max_idx accordingly, and if the store occurs
just outside the tracked bounds, also the bounds are updated. Then, ag_max
must now be the max value after the store, within the new bounds, and Imax is
preserved.
     Finally, in rewrites of store, the assignment a’ = store(a, i, x); is not
changed, but only additional code is added that does not assign to program
variables, and so the semantics is preserved. In rewrites of \max, we assume

                                        30
Imax and the assertion in the rewrite rule. Since by the invariant ag_max is the
max value in ag_ar in the tracked interval, and since by the assertion ag_ar is
the same array as in the aggregate expression, and the bounds for the tracked
interval are the same as in the aggregate expression, then ag_max is also the
max value in a within those bounds (and ag_max_idx is a position where the
value occurs). Thus, r is assigned the result of the aggregate function, and the
semantics is preserved.                                                        ⊓
                                                                               ⊔


F    Correctness of Instrumentation Operator for Sum
Here, we show the correctness of Ωsum .

Proof (Lemma 3). Firstly, the ghost variables ag_lo and ag_hi are initialised
to the same value, so Isum is established. Now, it remains to be shown that
the rewrite rules adheres to the additional constraints. Rewrites of normalised
select statements are similar to those of store, so that case is left out.
    Clearly, all the instrumented code terminates, and rewrites of store only
assign to ghost variables and a′ , and rewrites of \sum only to the assigned vari-
able r. Thus, all rewrites fulfill the first two conditions.
    Rewrites of \sum do not assign to ghost variables, so they preserve Isum .
For rewrites of store, we assume Isum and for the proof treat the assertion in
the rewrite rules as an assumption. In the cases of an empty interval, or when
storing far outside the tracked interval, since we reset the bounds, the sum, and
the index to only track the single stored element, then ag_sum is the sum of the
resulting array with the new bounds, and since we assign ag_ar the result of
the store, Isum is preserved. In the remaining cases, by the invariant and the
assertions ag_sum is assigned the sum of the array being stored to, within the
given bounds. When storing inside the tracked interval, we update ag_sum by
first subtracting the previous value stored at that index, and then adding the
new value. When storing adjacent to the tracked interval, we only add the new
value to ag_sum, and update the bounds accordingly. Then, ag_sum must now
be the sum after the store, within the new bounds, and Imax is preserved.
    Finally, in rewrites of store, the assignment a’ = store(a, i, x); is not
changed, but only additional code is added that does not assign to program
variables, and so the semantics is preserved. In rewrites of \sum, we assume Isum
and the assertion in the rewrite rule. Since by the invariant ag_sum is the sum of
ag_ar in the tracked interval, and since by the assertion ag_ar is the same array
as in the aggregate expression, and the bounds for the tracked interval are the
same as in the aggregate expression, then ag_sum is also the sum of a within those
bounds. In the special case when tracking an empty interval, we immediately
assign the value 0, which is the neutral element in the corresponding monoid.
Thus, r is assigned the result of the aggregate function, and the semantics is
preserved.                                                                      ⊓
                                                                                ⊔




                                       31
G     Detailed Evaluation Results

We list all evaluated benchmarks in Table 5 (forall ), Table 6 (max ), Table 7
(min) and Table 8 (sum) for all evaluated tools: MonoCera (Mono), TriCera
(Tri), SeaHorn (Sea), and CPAchecker (CPA). The list includes mostly
SV-COMP benchmarks and the first column indicates their original directories
(should be prepended with “c/”). There are some crafted benchmarks that are
not from SV-COMP; for these we only state the name of the benchmark (for
instance forall1-10).
    The expected result for all benchmarks in the tables is True. Durations are
given next to the returned result for benchmarks which did not time out.
    On top of quantifying over arrays, many of the benchmarks have assertions
over nonlinear integer arithmetic (NIA). Decision procedures for NIA are incom-
plete, and we have seen errors in the presence of such assertions in some of the
evaluated tools.
    The result “Unknown” is returned by MonoCera when the instrumentation
search space is exhausted.
     Table 5: forall benchmark results for all tools. Timeout (T/O) is 300.0 s.
                                                       CPA       Sea        Tri        Mono
array-cav19/array_doub_access_init_const.c             T/O       T/O       T/O     True (111)
array-cav19/array_init_nondet_vars.c                    T/O      T/O       T/O      True (14)
array-cav19/array_init_pair_sum_const.c                 T/O      T/O       T/O          T/O
array-cav19/array_init_pair_symmetr.c                   T/O      T/O       T/O          T/O
array-cav19/array_init_pair_symmetr2.c                  T/O      T/O       T/O          T/O
array-cav19/array_init_var_plus_ind.c                   T/O      T/O Error (2)      True (23)
array-cav19/array_init_var_plus_ind2.c                  T/O      T/O Error (2) Unknown (109)
array-cav19/array_init_var_plus_ind3.c                  T/O      T/O Error (3)      True (60)
array-industry-pattern/array_ptr_partial_init.c         T/O      T/O       T/O          T/O
array-industry-pattern/array_shadowinit.c               T/O      T/O       T/O      True (19)
array-cav19/array_tiling_poly6.c                        T/O Error (0)      T/O          T/O
array-cav19/array_tripl_access_init_const.c             T/O      T/O       T/O     True (199)
array-fpi/condg.c                                       T/O      T/O       T/O          T/O
array-fpi/condm.c                                       T/O      T/O       T/O      Error (8)
array-fpi/condn.c                                       T/O      T/O       T/O      True (88)
array-fpi/eqn1.c                                        T/O Error (0)      T/O          T/O
array-fpi/eqn2.c                                        T/O Error (0)      T/O          T/O
array-fpi/eqn3.c                                        T/O Error (0)      T/O          T/O
array-fpi/eqn4.c                                        T/O Error (0)      T/O          T/O
array-fpi/eqn5.c                                        T/O Error (0)      T/O          T/O
forall1-10                                         True (23) Error (0) True (55)    True (37)
forall1-100                                             T/O Error (2)      T/O      True (31)
forall1-UB                                              T/O Error (0)      T/O      True (32)
array-fpi/ifcomp.c                                      T/O Error (0)      T/O          T/O
array-fpi/ifeqn1.c                                      T/O Error (0)      T/O          T/O




                                              32
                                                      CPA        Sea     Tri        Mono
array-fpi/ifeqn2.c                                    T/O Error (0)      T/O         T/O
array-fpi/ifeqn3.c                                    T/O Error (0)      T/O         T/O
array-fpi/ifeqn4.c                                    T/O Error (0)      T/O         T/O
array-fpi/ifeqn5.c                                    T/O Error (0)      T/O         T/O
array-fpi/ifncomp.c                              Error (20) Error (0)    T/O         T/O
array-fpi/indp1.c                                     T/O Error (0)      T/O         T/O
array-fpi/indp2.c                                     T/O Error (0)      T/O         T/O
array-fpi/indp3.c                                     T/O Error (0)      T/O         T/O
array-fpi/indp4.c                                     T/O Error (0)      T/O         T/O
array-tiling/mbpr2.c                                  T/O       T/O      T/O         T/O
array-tiling/mbpr3.c                                  T/O       T/O      T/O         T/O
array-tiling/mbpr4.c                                  T/O       T/O      T/O         T/O
array-tiling/mbpr5.c                                  T/O       T/O      T/O         T/O
loop-lit/mcmillan2006.c                           True (7)      T/O      T/O     True (19)
array-tiling/mlceu2.c                                 T/O       T/O Error (3)    Error (4)
array-fpi/modn.c                                 Error (20) Error (0)    T/O         T/O
array-fpi/modp.c                                 Error (17) Error (0)    T/O     Error (9)
array-fpi/mods.c                                      T/O Error (0)      T/O         T/O
array-fpi/ncomp.c                                     T/O Error (0)      T/O         T/O
array-tiling/nr2.c                                    T/O       T/O      T/O     True (93)
array-tiling/nr3.c                                    T/O       T/O      T/O    True (123)
array-tiling/nr4.c                                    T/O       T/O      T/O    True (156)
array-tiling/nr5.c                                    T/O       T/O      T/O    True (223)
array-fpi/nsqm.c                                      T/O Error (0)      T/O         T/O
array-fpi/nsqm-if.c                              Error (15) Error (0)    T/O         T/O
array-lopstr16/partial_lesser_bound.c            T/O (108)      T/O      T/O         T/O
array-lopstr16/partial_lesser_bound-1.c               T/O Error (1) Error (2)    True (89)
array-fpi/pcomp.c                                     T/O Error (0)      T/O         T/O
array-tiling/pnr2.c                                   T/O       T/O      T/O    True (227)
array-tiling/pnr3.c                                   T/O       T/O      T/O    True (236)
array-tiling/pnr4.c                                   T/O       T/O      T/O         T/O
array-tiling/pnr5.c                                   T/O       T/O      T/O         T/O
array-tiling/poly1.c                                  T/O Error (0)      T/O     True (25)
array-tiling/poly2.c                                  T/O Error (0)      T/O         T/O
array-tiling/pr2.c                                    T/O Error (0)      T/O    True (117)
array-tiling/pr3.c                                    T/O Error (0)      T/O    True (143)
array-tiling/pr4.c                                    T/O Error (0)      T/O         T/O
array-tiling/pr5.c                                    T/O Error (0)      T/O         T/O
array-tiling/rew.c                                    T/O       T/O      T/O         T/O
array-tiling/rewnif.c                                 T/O       T/O      T/O     True (55)
array-tiling/rewnifrev.c                              T/O       T/O      T/O     True (60)
array-tiling/rewnifrev2.c                             T/O       T/O      T/O     True (97)
array-examples/sanfoundry_27_ground.c                 T/O       T/O      T/O    Error (19)
loop-crafted/simple_array_index_value_2.c             T/O Error (1) Error (2)    True (39)




                                            33
                                                        CPA        Sea      Tri         Mono
loop-crafted/simple_array_index_value_3.c               T/O Error (1) Error (3)      True (33)
array-fpi/sina1.c                                       T/O       T/O      T/O      True (199)
array-fpi/sina2.c                                       T/O       T/O      T/O            T/O
array-fpi/sina3.c                                       T/O       T/O      T/O            T/O
array-fpi/sina4.c                                       T/O       T/O      T/O            T/O
array-fpi/sina5.c                                       T/O       T/O      T/O            T/O
array-tiling/skipped.c                                  T/O       T/O      T/O            T/O
array-fpi/sqm.c                                         T/O Error (0)      T/O            T/O
array-fpi/sqm-if.c                                      T/O Error (0)      T/O            T/O
array-fpi/ss2.c                                    Error (65) Error (0)    T/O            T/O
array-fpi/ssina.c                                  Error (38) Error (0)    T/O            T/O
array-examples/standard_copyInitSum2_ground-2.c         T/O       T/O      T/O            T/O
array-examples/standard_copyInitSum3_ground.c           T/O       T/O      T/O            T/O
array-examples/standard_copyInit_ground.c               T/O       T/O      T/O            T/O
array-examples/standard_init1_ground-2.c                T/O       T/O      T/O       True (32)
array-examples/standard_init2_ground-2.c                T/O       T/O      T/O       True (82)
array-examples/standard_init3_ground-2.c                T/O       T/O      T/O            T/O
array-examples/standard_init4_ground-2.c                T/O       T/O      T/O            T/O
array-examples/standard_init5_ground-1.c                T/O       T/O      T/O            T/O
array-examples/standard_init6_ground-2.c                T/O       T/O      T/O            T/O
array-examples/standard_init7_ground-2.c                T/O       T/O      T/O            T/O
array-examples/standard_init8_ground-2.c                T/O       T/O      T/O            T/O
array-examples/standard_init9_ground-2.c                T/O       T/O      T/O            T/O
array-examples/standard_maxInArray_ground.c             T/O       T/O      T/O            T/O
array-examples/standard_minInArray_ground-2.c           T/O       T/O      T/O            T/O
array-examples/standard_partition_ground-2.c            T/O       T/O      T/O            T/O
array-examples/standard_vararg_ground.c                 T/O       T/O      T/O       True (57)



    Table 6: max benchmark results for all tools. Timeout (T/O) is 300.0 s.
                                                     CPA       Sea      Tri         Mono
array-cav19/array_init_var_plus_ind3.c               T/O       T/O Error (2) Unknown (277)
battery_diag-10                                True (155) True (0)        T/O          T/O
battery_diag-100                                      T/O      T/O        T/O          T/O
array-fpi/condn.c                                     T/O      T/O        T/O     True (129)
max_eq-10                                        True (21) True (0) True (78)      True (21)
max_eq-100                                            T/O      T/O        T/O      True (38)
max_eq-UB                                             T/O      T/O        T/O      True (27)
max_leq-10                                       True (25) True (0) True (90)      True (23)
max_leq-100                                           T/O      T/O        T/O      True (30)
max_leq-UB                                            T/O      T/O        T/O      True (52)
array-examples/sanfoundry_27_ground.c                 T/O      T/O        T/O     True (285)
array-examples/standard_maxInArray_ground.c           T/O      T/O        T/O          T/O




                                            34
   Table 7: min benchmark results for all tools. Timeout (T/O) is 300.0 s.
                                                       CPA      Sea        Tri       Mono
array-cav19/array_doub_access_init_const.c             T/O      T/O       T/O         T/O
array-cav19/array_init_pair_sum_const.c                 T/O     T/O       T/O         T/O
array-cav19/array_init_pair_symmetr2.c                  T/O     T/O       T/O         T/O
array-cav19/array_init_var_plus_ind.c                   T/O     T/O Error (3) Unknown (67)
array-cav19/array_init_var_plus_ind2.c                  T/O     T/O Error (2) Unknown (64)
array-cav19/array_tripl_access_init_const.c             T/O     T/O       T/O         T/O
min_eq-10                                          True (25) True (0) True (61)   True (28)
min_eq-100                                              T/O     T/O       T/O     True (22)
min_eq-UB                                               T/O     T/O       T/O     True (25)
min_geq-10                                         True (26) True (0) True (51)   True (26)
min_geq-100                                             T/O     T/O       T/O     True (28)
min_geq-UB                                              T/O     T/O       T/O     True (24)
array-tiling/rew.c                                      T/O     T/O       T/O     True (40)
array-tiling/rewnifrev.c                                T/O     T/O       T/O     True (41)
array-examples/standard_minInArray_ground-2.c           T/O     T/O       T/O         T/O
array-examples/standard_partition_ground-2.c            T/O     T/O       T/O         T/O
array-examples/standard_vararg_ground.c                 T/O     T/O       T/O     True (59)



   Table 8: sum benchmark results for all tools. Timeout (T/O) is 300.0 s.
                                          CPA        Sea        Tri   Mono
                array-fpi/brs1.c          T/O        T/O       T/O True (26)
                array-fpi/brs2.c          T/O Error (0)        T/O True (34)
                array-fpi/brs3.c          T/O        T/O       T/O True (41)
                array-fpi/brs4.c          T/O        T/O       T/O True (38)
                array-fpi/brs5.c          T/O        T/O       T/O True (58)
                array-fpi/conda.c         T/O        T/O       T/O       T/O
                array-fpi/indp5.c   Error (17) Error (0)       T/O       T/O
                array-fpi/ms1.c           T/O        T/O       T/O True (26)
                array-fpi/ms2.c           T/O        T/O       T/O True (46)
                array-fpi/ms3.c           T/O        T/O       T/O True (31)
                array-fpi/ms4.c           T/O        T/O       T/O True (33)
                array-fpi/ms5.c           T/O        T/O       T/O True (32)
                array-fpi/s1lif.c         T/O        T/O       T/O       T/O
                array-fpi/s2lif.c         T/O        T/O       T/O       T/O
                array-fpi/s3lif.c         T/O        T/O       T/O       T/O
                array-fpi/s4lif.c         T/O        T/O       T/O       T/O
                array-fpi/s5lif.c         T/O        T/O       T/O       T/O
                sum_eq-10           True (50) True (0) True (45) True (245)
                sum_eq-100                T/O        T/O       T/O       T/O
                sum_eq-UB                 T/O        T/O       T/O True (55)
                sum_geq-10          True (45) True (0) True (98) True (200)
                sum_geq-100               T/O        T/O       T/O True (221)




                                              35
                         CPA       Sea       Tri    Mono
sum_geq-UB                T/O     T/O       T/O True (59)
two_arrays_sum-10    True (26) True (0) True (46)     T/O
two_arrays_sum-100        T/O     T/O       T/O       T/O
two_arrays_sum-UB         T/O     T/O       T/O True (106)




                             36
