                                                     Cuvée: Blending SMT-LIB with
                                                   Programs and Weakest Preconditions

                                                                            Gidon Ernst

                                                             LMU Munich, Germany, gidon.ernst@lmu.de
arXiv:2010.05023v1 [cs.LO] 10 Oct 2020




                                               Abstract. Cuvée is a program verification tool that reads SMT-LIB-
                                               like input files where terms may additionally contain weakest precondi-
                                               tion operators over abstract programs. Cuvée translates such inputs into
                                               first-order SMT-LIB by symbolically executing these programs. The in-
                                               put format used by Cuvée is intended to achieve a similar unification of
                                               tools for that for example synthesize loop summaries. A notable technical
                                               aspect of Cuvée itself is the consequent use of loop pre-/postconditions
                                               instead of invariants, and we demonstrate how this lowers the annotation
                                               burden on some simple while programs.


                                         Keywords: Program Verification, SMT-LIB, Weakest Precondition

                                         1   Introduction
                                         Intermediate verification languages and tools such as Boogie [7], Why3 [5], and
                                         Viper [10] have had a significant impact on the state-of-the-art of (deductive)
                                         program verification. At the annual competition on interactive program verifi-
                                         cation VerifyThis [6], tools like these are put to practice on small but intricate
                                         verification problems. Currently, VerifyThis lacks a common input format. This
                                         is fine for hard challenges where efficiency of the tool and seamless interaction
                                         are required. SMT-LIB [2] is a standardized interchange format for verification
                                         tasks in first-order logic that is widely used in many different application domains
                                         such as constraint-solving, program verification, and model-checking. Many ma-
                                         ture tools are available, and the annual SMT-COMP evaluates and compares
                                         their performance on benchmark problems. Part of the success of the SMT-LIB
                                         format is its regular syntax and its precise standardization. SV-COMP [4] is a
                                         competition where the participating tools analyze C code fully automatically. It
                                         is therefore restricted to less complex properties that cannot be solved without
                                         the guidance of a proof engineer.
                                              The goal of this work is to occupy the spot between these communities, as
                                         well as the different technologies involved [3]. How to make use, e.g., of tools that
                                         can infer invariants? The input format that is described here and implemented
                                         in Cuvée takes deliberate trade-offs to position itself between the highly expres-
                                         sive logic of e.g. Dafny, and stressing the interoperability that made SMT-LIB
                                         successful. As such one design goal, for example, is to re-use the existing logical
                                         data types of that format, even if it might be less convenient as a front-end for
                                         humans.
hvar_bindingi ::= ( hsymbol i htermi )

htermi         ::= (wp hprogrami htermi)
                 | (box hprogrami htermi)
                 | (dia hprogrami htermi)
                 | (old htermi )
                 | ...

hprogrami      ::= (assign (hvar_bindingi)+ )
                 | (spec ( hsymbol i+ ) htermi htermi )
                 | (block hprogrami+ )
                 | (if htermi htermi htermi )
                 | (while htermi htermi hattributei+ )

hcommand i     ::= (assert-counterexample htermi hprogrami htermi )
                 | ...


Fig. 1. Extension of the SMT-LIB supported by Cuvée: Weakest-precondition oper-
ators, simple nondeterministic While programs, and a top-level command to specify
Hoare triples (hvar _bindingi is from the SMT-LIB grammar).


2   Syntax

The new constructs accepted by Cuvée are shown in Fig. 1.
    Terms htermi of SMT-LIB are extended by three weakest-precondition oper-
ators, (wp p t), (box p t), (dia p t) for programs p (see below) and postcondi-
tions t (terms of sort Bool, which state slightly different correctness criteria with
respect to termination and nondeterministic choices.
    The first one, wp denotes Dijkstra’s well-known weakest precondition: All
executions of p, when started in the current state, terminate and lead to a state
that satisfies t. For instance, a Hoare triple for total correctness [φ] p [ψ] can be
written as the implication (=> φ (wp p ψ ))
    Similarly, box does not require termination (i.e., it expresses the weakest
liberal precondition), i.e., {φ} p {ψ} can be written as (=> φ (box p ψ )).
    The operator dia reflects angelic execution instead of demonic execution: For
(dia p t) it is required that there is at least one execution of p that terminates
and leads to a state that satisfies t. The names of the latter two operators is
taken from Dynamic Logic.
    The expression (old t) is intended for use in loop annotations. It refers to
previous states of the execution at the beginning of loop iterations.
    Programs hprogrami provide familiar constructs from a simple sequential
While language.
    Parallel assignments evaluate all right-hand-sides simultaneously, e.g. (assign
(x y) (y x)) swaps the values stored in the variables x and y. Note that there
is no syntactic difference between program variables and logical ones, and the
former ones may range over arbitrary SMT-LIB data types.

                                         2
     Specification statements (spec (x1 · · · xn ) φψ ) (see [9]) encode arbitrary,
possibly nondeeterministic transitions. The effect of executing such a statement
is that the precondition φ of the statement is asserted (i.e., needs to hold in the
current state), then the variables x1 · · · xn are given fresh arbitrary values, and
the postcondition ψ is assumed for the remainder of the execution.
     Specification statements can encode assertions (assert φ becomes (spec ()
φ true)), assumptions (assume ψ becomes (spec () true ψ )), and the state-
ment havoc x1 · · · xn from e.g. Boogie (which becomes (spec (x1 · · · xn ) true
true)).
     Within the postcondition of a specification statement, old refers to the pre-
state of the statement itself. This admits elegant encoding of transition relations,
i.e., (spec (x) true (> x (old x))) specifies that the new value of x is strictly
larger than the previous one.
     Specification statements are useful internally, too, to encode the inductive
hypothesis of the loop rule implemented in Cuvée (see Section 2).
     Sequential composition is written as (block p1 · · · pn ), where (block) denotes
the empty statement. Conditional statements (if b p1 p2 ) execute either p1
or p2 depending of the evaluation of the test b (a boolean term) in the current
state.
While loops

    (while b p :termination t :precondition φ :postcondition ψ )

execute p as long as the test b holds true. Cuvée supports some attributes that
can be used to specify loop annotations, namely, a termination measure t, a loop
precondition φ, and a loop postcondition ψ. All three annotations are optional.
    A new top-level command (assert-counterexample φ p ψ ) asserts that the
Hoare triple [φ] p [ψ] is not valid. This command roughly translates to (assert
(not (=> φ (wp p ψ )))), however, Cuvée implements special cases when p is
a while loop without a pre-/postcondition annotation to derive the loop speci-
fication from such a contract. Moreover, within a assert-counterexample com-
mand, old in the postcondition ψ refers to the pre-state. Note that this feature
is currently not expressible in the expression/program language alone, but can
be emulated if needed by introducing additional logical variables capturing this
pre-state explicitly.
    Consistent with the standard pattern in SMT-LIB, where formulas are proved
by searching for satisfying assignments of the negation, an unsat from the un-
derlying SMT solver on the problem translated by Cuvée indicates that there
is no counterexample i.e., the program is correct with respect to the specified
contract.


3   Proof Rules
The predicate transformer semantics [8] of the input language is shown in Fig. 2
for the wp operator, with the exception of the loop rule, which is shortened to

                                         3
    (wp (assign ((x1 t1 ) · · · (xn tn ))) Q) ≡ Q[x1 , . . . , xn ← t1 , . . . , tn ]
                       (wp (block p1 · · · pn Q) ≡ (wp p1 · · · (wp pn Q))
                          (wp (if b p1 p2 ) Q) ≡ (and (=> b (wp p1 Q))
                                                             (=> (not b) (wp p2 Q)))



    φ     (forall (y ) ψ[(old x) ← x, x ← y] → Q[x ← y])
                      (wp (spec (x) φ ψ ) Q)


                                    (box (spec (x) φ ψ ) Q)
                    (forall (x) (=> (and φ (not b)) Q[(old x) ← x]))
    (forall (x) (=> (and φ b) (box (block p (spec (x) φ ψ )) ψ )[(old x) ← x]))
                                       (box (while b p) Q)
         where φ is the precondition of the loop and ψ is the postcondition,
         x are the variables modified by the loop body p and y are fresh.


Fig. 2. Predicate transformer semantics for the programming language in Fig. 1. The
rules for the specification statement and loops are given as inference rules to improve
readability (these could be equally formulated as equivalences).



omit the termination conditions and therefore expressed using box. The rules for
box and dia are similar. Note that Q is a term that may again contain weakest-
precondition operators.
   The first three equivalences are standard. Assignments propagate as a si-
multaneous substitution into the postcondition Q. Sequential execution simply
nests the weakest precondition operator. Conditionals produce two branches that
evaluate the test positively resp. negatively.
   The specification statement binds fresh copies y for the havoc’ed variables x,
and substitutes old expressions in the postcondition ψ. The first premise simply
asserts the precondition φ.
    The loop rule is more involved and proceeds by induction on the number
of loop iterations, see Alexandru’s bachelor thesis [1]. It has three premises:
The first, abstracts the entire execution of the loop loop with a specification
statement, after which the postcondition Q needs to hold.
    The second premise corresponds to the base case of the induction and estab-
lishes Q upon termination (when b is false). Old values in Q refer to the current
state.
    The third premise corresponds to the inductive case, where b holds. Then,
the condition to show is that after executing the loop body p once, the inductive
hypothesis about the remaining iterations is sufficient to establish ψ after the
entire loop. This hypothesis is encoded as a specification statement (spec (x)
φ ψ ) that abstracts the remaining iterations, similarly as in the first premise.

                                                4
    The interaction between the different occurrences of old is somewhat intri-
cate: Within the specification statement, old refers to the state after the first
iteration, according to the corresponding proof rule. Hence, the it encodes that
it is possible at that point to turn the precondition φ into an arbitrary state
after the remaining iterations that satisfies ψ for fresh copies of the modified
variables x introduced by the specification statement. Ultimately, this knowl-
edge needs to suffice to establish ψ after the loop with all iterations, where old
refers to the state before executing the first iteration p.


4     Tool Description

Cuvée is implemented in the Scala programming language1 and relies on SMT
solvers as back-ends to solve the first-order verification conditions.
    Cuvée is open source under the MIT License at https://github.com/gernst/cuvee.
    It reads one or more input files, reduces the weakest-precondition operators
according to the rules in Fig. 2 using symbolic execution (i.e., the substitutions
are delayed and propagated down the term structure).
    The tool can be invoked from the command line in different ways as exem-
plified below:

./cuvee                                        # read from stdin, write to stdin
./cuvee <file> -o <out>                        # read from file,     write to out
./cuvee <file1> ... <filen> -- ./z3 -in # invoke SMT solver directly

It can either save the generated SMT-LIB script to a file, or invoke an SMT
solver, whose command line is appended after --, Z3 in this case. In this mode of
operation, it pipes the generated verification task directly to the solver. There are
builtin abbreviations -z3 and -cvc4 that pass the necessary arguments, assuming
those solvers are present in $PATH.


5     Example

We demonstrate Cuvée on a simple example, shown in Fig. 3, which is taken
from the VerifyThis competition 2012. It is an algorithm that searches the max-
imum element in an array by elimination. It maintains two indices, x ≤ y and
moves the one pointing to the smaller element in each iteration. The postcondi-
tion asserts that for any valid index z, the returned index x contains an element
that is in fact at least as large.
    Cuvée infers the precondition and postcondition of the loop from the spec-
ified contract, such that the example is solved without further interaction.
    A few more examples are contained in the examples subfolder on github,
including GCD, and mapping an array range by an unspecified function.
1
    https://scala-lang.org



                                         5
(declare-const x Int)
(declare-const y Int)
(declare-const a (Array Int Int))


(assert-counterexample
    (<= x y)
    (while (not (= x y))
           (if (<= (select a x) (select a y))
               (assign (x (+ x 1)))
               (assign (y (- y 1))))
           :termination (- y x))
    (forall ((z Int))
      (=> (and (<= (old x) z)
               (<= z (old y)))
          (<= (select a z) (select a x)))))


(check-sat)



               Fig. 3. Finding the maximum in an array by elimination.


6     Conclusion and Outlook
Cuvée is a tool that aims to bridge the gap between fully automated program
verification and approaches that have the human in the loop. It does so by
extending SMT-LIB to cover weakest precondition statements about abstract
programs, which tightly integrate into the existing standard.
    There are plenty of opportunities for future development. For one, it is hoped
that the format will be taken up by others, supported by standardization efforts.
Extension to recursive procedures is planned as well.
    Ultimately, following this approach opens up the possibility to evaluate and
compare verification tools that can handle complex functional correctness con-
ditions involving quantifiers, arrays, and other data types.




                                         6
                               Bibliography


 [1] Alexandru, G.: Specifying loops with contracts (2019), Bachelor’s Thesis,
     LMU Munich
 [2] Barrett, C., Stump, A., Tinelli, C., et al.: The smt-lib standard: Version 2.0.
     In: Proceedings of the 8th International Workshop on Satisfiability Modulo
     Theories (Edinburgh, England). vol. 13, p. 14 (2010)
 [3] Bartocci, E., Beyer, D., Black, P.E., Fedyukovich, G., Garavel, H., Hart-
     manns, A., Huisman, M., Kordon, F., Nagele, J., Sighireanu, M., et al.:
     Toolympics 2019: an overview of competitions in formal methods. In: In-
     ternational Conference on Tools and Algorithms for the Construction and
     Analysis of Systems. pp. 3–24. Springer (2019)
 [4] Beyer, D.: Advances in automatic software verification: Sv-comp 2020. In:
     International Conference on Tools and Algorithms for the Construction and
     Analysis of Systems. pp. 347–367. Springer (2020)
 [5] Bobot, F., Filliâtre, J.C., Marché, C., Paskevich, A.: Why3: Shepherd your
     herd of provers. In: Boogie 2011: First International Workshop on Interme-
     diate Verification Languages. pp. 53–64 (2011)
 [6] Ernst, G., Huisman, M., Mostowski, W., Ulbrich, M.: VerifyThis–
     verification competition with a human factor. In: International Conference
     on Tools and Algorithms for the Construction and Analysis of Systems. pp.
     176–195. Springer (2019)
 [7] Leino, K.R.M.: This is Boogie 2 (2008), microsoft RiSE
 [8] Manes, E.G.: Predicate transformer semantics, vol. 33. Cambridge Univer-
     sity Press (2004)
 [9] Morgan, C.: The specification statement. ACM Transactions on Program-
     ming Languages and Systems (TOPLAS) 10(3), 403–419 (1988)
[10] Müller, P., Schwerhoff, M., Summers, A.J.: Viper: A verification infrastruc-
     ture for permission-based reasoning. In: International Conference on Veri-
     fication, Model Checking, and Abstract Interpretation. pp. 41–62. Springer
     (2016)
