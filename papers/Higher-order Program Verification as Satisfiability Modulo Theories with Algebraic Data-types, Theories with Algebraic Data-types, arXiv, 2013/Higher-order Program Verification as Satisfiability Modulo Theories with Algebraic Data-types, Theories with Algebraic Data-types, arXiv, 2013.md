                                             Higher-order Program Verification as Satisfiability Modulo
                                                       Theories with Algebraic Data-types

                                                                      Nikolaj Bjørner                   Ken McMillan
                                                                     Microsoft Research                Microsoft Research

                                                                                  Andrey Rybalchenko
                                                                  Microsoft Research & Technische Universität München
arXiv:1306.5264v1 [cs.LO] 21 Jun 2013




                                                                                            Abstract

                                                   We report on work in progress on automatic procedures for proving properties of programs writ-
                                              ten in higher-order functional languages. Our approach encodes higher-order programs directly as
                                              first-order SMT problems over Horn clauses. It is straight-forward to reduce Hoare-style verification
                                              of first-order programs into satisfiability of Horn clauses. The presence of closures offers several
                                              challenges: relatively complete proof systems have to account for closures; and in practice, the effec-
                                              tiveness of search procedures depend on encoding strategies and capabilities of underlying solvers.
                                              We here use algebraic data-types to encode closures and rely on solvers that support algebraic data-
                                              types. The viability of the approach is examined using examples from [14].


                                        1 Background
                                        Automatic verification of programs in higher-order languages has received significant attention in recent
                                        years. The Liquid Type systems have been used successfully on a large set of challenges from Ocaml [12]
                                        and Haskell [15]. Liquid types rely checking program properties as type checking of refinement types.
                                        Not all refinement types need to be provided fully, instead users can supply a space of templates that the
                                        type inference engine instantiates and refines the template invariants (using the Houdini approach [4]). A
                                        very different approach is taken in HALO [16] where the denotational semantics of Haskell, using types
                                        that include error states, is encoded using quantified equalities. HALO relies on quantifier instantiation
                                        engines and finite model building capabilities to discharge correctness proof conditions. Unno et.al. [14]
                                        develop a custom engine that realizes proof rules for Hoare logic for programs with procedure parame-
                                        ters [5]. There are several other systems that use first-order/SMT technologies for establishing properties
                                        of higher-order languages. They typically rely on user-annotated refinement types. The executable subset
                                        of the PVS specification language uses decision procedures for discharging type checking conditions and
                                        the F⋆ system includes verification condition generation from a higher-order language with higher-order
                                        refinement types.
                                            These systems have in common that they rely on SMT solvers, CVC4, Yices and Z3. We are here
                                        examining whether program verification (in the presence of closures) can be reduced directly to SMT
                                        solving.


                                        2 Program Verification as Horn Clause Satisfiability
                                        Consider the McCarthy function:

                                        let mc x = if x > 100 then x - 10 else mc (mc (x + 11))
                                        assert x <= 101 => mc(x) = 91

                                                                                                1
HOPA as SMT with Algebraic Data-types                                    Bjørner, McMillan, Rybalchenko


    We can check partial correctness of mc by representing the summary as a binary relation between in-
put and outputs, and describing the function and assertion equivalently as a conjunction of Horn clauses:

                                                 ∀x . x > 100 → mc(x, x − 10)
                      ∀x, y, z . x ≤ 100 ∧ mc(x + 11, y) ∧ mc(y, z) → mc(x, y)
                                          ∀x, y . x ≤ 101 ∧ mc(x, y) → y = 91

These Horn clauses are satisfiable if and only if the original partial correctness assertion holds. A satis-
fying assignment to the Horn clauses (found by Z3) is:

                      mc(x, y) ≡ (y ≤ x − 10 ∨ y ≤ 91) ∧ y ≥ 91 ∧ (x ≤ y + 10)

The assignment is an inductive summary for mc.
   This example illustrates a central claim made in [3] and [7]:

Claim 1. Satisfiability of Horn clauses modulo theories is an adequate basis for program correctness.

    Synthesis of ranking functions can also be encoded into Horn clauses [7], so Horn clause solving
extends also to establishing total correctness.
    The challenge is of course to solve Horn clauses and a number of tools are being developed for solv-
ing Horn clauses at scale. These include the Duality [11], HSF [7], Eldarica [13], PDR implementation
in Z3 [8], and SPACER [10]. The Horn clause format is also a convenient interchange format for sym-
bolic software verification benchmarks. We have collected benchmarks from symbolic software model
checking as Horn clauses in an online repository 1 . There are currently around 10,000 benchmarks from
various sources. There are several possible strategies for encoding model checking problems into Horn
clauses and consequently some benchmarks use different encodings of the same problems.
    The repository also includes problems from the tools for liquid types. The liquid type system lever-
ages the Hindley Milner type system for extracting Horn clauses for closures.


3 Closures as Algebraic Data-types
We will here consider a direct encoding of problems from a simply typed higher-order programming
language into Horn clauses. The basic idea is to encode functions as relations and higher-order closures
as algebraic data-types. The Horn clauses encode an interpreter, suitably specialized to the programs that
are analyzed. We use examples from [14] to illustrate the approach.
    To warm up, consider the program

let f x y = assert (not (x() > 0 && y() < 0))
let h x y = x
let g n = f (h n) (h n)

The curried function h is partially applied to the same integer n, and f is applied to two functions with
signature unit → int. This is the only closure type used in this program, so we introduce algebraic
data-types to encode the possible closures that are used in the program:

                                             clo ::= h int
                                            unit ::= unit

   1 https://svn.sosy-lab.org/software/sv-benchmarks/trunk/clauses/



                                                     2
HOPA as SMT with Algebraic Data-types                                     Bjørner, McMillan, Rybalchenko


The closure clo has a single constructor h that takes an integer. It is evaluated to arguments of type unit.
We assign meaning to the closure by defining an evaluator. A canonical evaluator can be formulated as a
relation over (1) a closure, (2) the argument of the closure, (3) the output value, and (4) a flag to indicate
successful termination of the evaluation. For our example, there is only a single relevant rule for the
evaluator; it reduces to evaluating the function h

                           ∀x, r, ok . h(x, unit, r, ok) → Ev(h(x), unit, r, ok)

The other functions translate in a straight-forward way to Horn clauses:
                                                               
                         Ev(x, unit, r1 , ok1 )
                 ∧      Ev(y, unit, r2 , ok2 )                  →         f (x, y, unit, ok)
                  ∧      (ok ≡ ¬(r1 > 0 ∧ r2 < 0) ∧ ok1 ∧ ok2 )
                                                                            h(x, y, x, true)
                                                 f (h(n), h(n), r, ok) → g(n, r, ok)
                                                      g(n, r, false) → false

where x, y, r, r1 , r2 , ok, ok1 , ok2 , n are variables.
     We used this example to sketch a systematic encoding from functional programs to Horn clauses. It
already contains some shortcuts (alternatively, we could have considered defining a generic interpreter).
It can still be simplified by specializing the program to the correctness assertion and removing arguments.
Since h(x) is the only closure passed to Ev it can furthermore be removed entirely. The simpler, equi-
satisfiable set of clauses is:

                                                      h(x, unit, r) → Ev(x, r)
                          Ev(x, r1 ) ∧ Ev(y, r2 ) ∧ r1 > 0 ∧ r2 < 0 →      f (x, y)
                                                                           h(x, y, x)
                                                            f (n, n) → g(n, r)
                                                            g(n, r) → false

where x, y, r1 , r2 , n, r are variables. The Horn clauses are non-recursive and Z3’s engines for Horn clauses
can easily establish satisfiability (e.g., that the assertion holds).
    A significantly more challenging example is suggested in [14] to illustrate their method (that com-
prises of adding extra parameters to closures).

let app1 f g = if * then app1 (succ f) g else g f
let app2 i f = f i
let succ f x = f (x + 1)
let check x y = assert (x <= y)
let main i = app1 (check i) (app2 i)

   We use the shortcuts used in the previous example to encode the recursive functions in an economical
way. The example uses two closures corresponding to the types check(i) : int → unit and app2(i) :
(int → int) → unit.

                                    clo1 ::= app2 int
                                    clo2 ::= check int | succ clo2

                                                      3
HOPA as SMT with Algebraic Data-types                                      Bjørner, McMillan, Rybalchenko


Similar to the previous example, the closure clo1 is superfluous and does not need to appear in the
generated Horn clauses. The second closure is recursive and therefore essential, and we include this
in the corresponding Horn clauses. Let x, y, f , i be variables, then safety of the example program is
equivalent to satisfiability of the following set of clauses:

                                  app1 (succ( f ), i) → app1 ( f , i)
                                            Ev( f , i) → app1 ( f , i)
                                       Ev( f , x + 1) → succ( f , x)
                                              x > y → check(x, y)
                                 app1 (check(i), i) → main(i)
                                            main(i) → false
                                         succ( f , x) → Ev(succ( f ), x)
                                        check(x, y) → Ev(check(x), y)

     Z3 accepts recursive Horn clauses with algebraic data-types as input, but is unable to establish sat-
isfiability of these clauses directly. In a nutshell, it lacks the ability to synthesize properties that select
leaves in algebraic data-types. We will here examine a couple of approaches that could be used to solve
such problems.

3.1 In-lining by resolution
Our first approach is to inline definitions by resolving Horn clauses and merge predicates. The result is
given below where app1 and Ev are merged into Ev.


                                   Ev(succ( f ), i) → Ev( f , i)
                                           Ev( f , i) → Ev( f , i)
                                  Ev(check(i), i) → false
                                      Ev( f , x + 1) → Ev(succ( f ), x)
                                             x > y → Ev(check(x), y)

    The second clause is a tautology and the two clauses that contain succ( f ) can be resolved (and then
removed, assuming a suitably strong, but not entirely unrealistic, redundancy elimination mechanism)
leaving an equi-satisfiable set of Horn clauses:


                                  Ev(check(i), i) → false
                                      Ev( f , x + 1) → Ev( f , x)
                                             x > y → Ev(check(x), y)

Z3 can immediately establish satisfiability of this set of clauses.

3.2 Quantified abstraction
In [2] we consider synthesis of intermediary assertions using quantified invariants for array manipulating
programs. Our approach from [2] is to search over solutions over a template space of quantified invari-
ants. The idea is to supply additional arguments to recursive predicates and bind these in quantifiers.

                                                      4
HOPA as SMT with Algebraic Data-types                                        Bjørner, McMillan, Rybalchenko


Using the running example, the modified problem is:

                          (∀~z . Ev(~z, succ( f ), i)) → (∀~z . Ev(~z, f , i))
                          (∀~z . Ev(~z, check(i), i)) → false
                             (∀~z . Ev(~z, f , x + 1)) → (∀~z . Ev(~z, succ( f ), x))
                                              x > y → (∀~z . Ev(~z, check(x), y))

where ~z is a tuple of integer variables. The number of variables in ~z is a parameter to the abstraction
procedure. The instantiation heuristic suggested in [2] is very simple and will not produce useful instan-
tiations for this case. Instantiation heuristics that are more powerful for arithmetic are used in [1], and of
course the template method of [14].
     Let us for the sake of illustrating the idea (but not the practicality) pretend an instantiation procedure
produces the following set of clauses:

                             Ev(u, v, succ( f ), i) → Ev(u, v, f , i)
                             Ev(i, i, check(i), i) → false
                                Ev(u, v, f , x + 1) → Ev(u, v + 1, succ( f ), x)
                                            x > y → Ev(u, v, check(x), y)

    With some struggle, Z3 can produce the inductive invariant:

                                        Ev(u, v, , i) ≡ 2 · u = v + i

More specifically, the invariant is obtained by analyzing the program obtained by reversing the rules
(corresponding to a Magic set transformation)

                             Ev(u, v, succ( f ), i) ← Ev(u, v, f , i)
                             Ev(i, i, check(i), i) ← false
                                Ev(u, v, f , x + 1) ← Ev(u, v + 1, succ( f ), x)
                                            x > y ← Ev(u, v, check(x), y)

Karr’s algorithm [9] for computing all affine relations for Horn clauses produces the useful congruence.


4 Summary
We have examined using algebraic data-types to encode closures directly in Horn clauses. Algebraic
data-types (Herbrand terms) can be used to provide a simple encoding of higher-order programs into
Horn clauses. Existing Horn clause solvers currently emphasize solving clauses over integers, reals, and
more lately arrays. Solving Horn clauses with algebraic data-types (Herbrand terms) pose a set of new
challenges for such solvers, but we have illustrated a couple of independent approaches that can be used
to solve such Horn clauses directly.


References
 [1] Tewodros Beyene, Corneliu Popeea, and Andrey Rybalchenko. Solving Existentially Quantified Horn
     Clauses. In CAV, 2013.
 [2] Nikolaj Bjørner, Ken McMillan, and Andrey Rybalchenko. On Solving Quantified Horn Clauses. In SAS,
     2013.

                                                       5
HOPA as SMT with Algebraic Data-types                                      Bjørner, McMillan, Rybalchenko


 [3] Nikolaj Bjørner, Kenneth L. McMillan, and Andrey Rybalchenko. Program verification as Satisfiability
     Modulo Theories. In SMT, 2012.
 [4] Cormac Flanagan and K. Rustan M. Leino. Houdini, an annotation assistant for esc/java. In José Nuno
     Oliveira and Pamela Zave, editors, FME, volume 2021 of Lecture Notes in Computer Science, pages 500–
     517. Springer, 2001.
 [5] Steven M. German, Edmund M. Clarke, and Joseph Y. Halpern. Reasoning about procedures as parameters
     in the language l4. Inf. Comput., 83(3):265–359, 1989.
 [6] Roberto Giacobazzi and Radhia Cousot, editors. The 40th Annual ACM SIGPLAN-SIGACT Symposium on
     Principles of Programming Languages, POPL ’13, Rome, Italy - January 23 - 25, 2013. ACM, 2013.
 [7] Sergey Grebenshchikov, Nuno P. Lopes, Corneliu Popeea, and Andrey Rybalchenko. Synthesizing software
     verifiers from proof rules. In PLDI, 2012.
 [8] Kryštof Hoder and Nikolaj Bjørner. Generalized property directed reachability. In SAT, 2012.
 [9] Michael Karr. Affine relationships among variables of a program. Acta Inf., 6:133–151, 1976.
[10] Anvesh Komuravelli, Arie Gurfinkel, Sagar Chaki, and Edmund Clarke. Automatic Abstraction in SMT-
     Based Unbounded Software Model Checking. In CAV, 2013.
[11] Kenneth L. McMillan and Andrey Rybalchenko. Computing relational fixed points using interpolation. Tech-
     nical Report MSR-TR-2013-6, Microsoft Research, 2013. http://research.microsoft.com/apps/-
     pubs/?id=180055.
[12] Patrick Maxim Rondon, Ming Kawaguchi, and Ranjit Jhala. Liquid types. In Rajiv Gupta and Saman P.
     Amarasinghe, editors, PLDI, pages 159–169. ACM, 2008.
[13] Philipp Rümmer, Hossein Hojjat, and Viktor Kuncak. Disjunctive interpolants for horn-clause verification.
     In CAV, 2013.
[14] Hiroshi Unno, Tachio Terauchi, and Naoki Kobayashi. Automating relatively complete verification of higher-
     order functional programs. In Giacobazzi and Cousot [6], pages 75–86.
[15] Niki Vazou, Patrick Maxim Rondon, and Ranjit Jhala. Abstract refinement types. In Matthias Felleisen
     and Philippa Gardner, editors, ESOP, volume 7792 of Lecture Notes in Computer Science, pages 209–228.
     Springer, 2013.
[16] Dimitrios Vytiniotis, Simon L. Peyton Jones, Koen Claessen, and Dan Rosén. Halo: haskell to logic through
     denotational semantics. In Giacobazzi and Cousot [6], pages 431–442.




                                                      6
