                                                                                                      Technical Report, April 2013


                                              On Integrating Deductive Synthesis and Verification Systems

                                                                       Etienne Kneuss                 Viktor Kuncak      Ivan Kuraj        Philippe Suter
                                                                                  École Polytechnique Fédérale de Lausanne (EPFL), Switzerland
                                                                                                 firstname.lastname@epfl.ch
arXiv:1304.5661v1 [cs.PL] 20 Apr 2013




                                        Abstract                                                                       of delivering verified software has been explored through
                                        We describe techniques for synthesis and verification of re-                   a number of different approaches, in a number of success-
                                        cursive functional programs over unbounded domains. Our                        ful cases the development relies heavily on a functional lan-
                                        techniques build on top of an algorithm for satisfiability                     guage. In some cases [19] the researchers have even written
                                        modulo recursive functions, a framework for deductive syn-                     the entire software system once in a functional language for
                                        thesis, and complete synthesis procedures for algebraic data                   verifiability, and once in a lower-level language for execu-
                                        types. We present new counterexample-guided algorithms                         tion efficiency.
                                        for constructing verified programs. We have implemented                           Based on the ideas of suitability of a functional paradigm
                                        these algorithms in an integrated environment for interac-                     and the importance of rapid feedback, we have developed
                                        tive verification and synthesis from relational specifications.                a verifier that quickly detects errors in functional programs
                                        Our system was able to synthesize a number of useful recur-                    and reports concrete counterexamples, but can also prove the
                                        sive functions that manipulate unbounded numbers and data                      correctness of programs [42–44]. Furthermore, we have in-
                                        structures.                                                                    tegrated such countexample-generating verifier into a web-
                                                                                                                       browser-based IDE, resulting in a tool for convenient devel-
                                        1. Introduction                                                                opment of verified functional programs. This verifier is the
                                                                                                                       starting point of the tool we present in this paper.
                                        Software construction is a difficult problem-solving activity.                    Moving beyond verification, we believe that a produc-
                                        It remains a largely manual effort today, despite significant                  tive development of verified software requires techniques
                                        progress in software development environments and tools.                       for synthesis from specifications. Specifications in terms of
                                        The development becomes even more difficult when the goal                      properties generalize existing declarative programming lan-
                                        is to deliver verified software, which must satisfy specifica-                 guage paradigms by allowing the statement of constraints
                                        tions such as assertions, pre-conditions, and post-conditions.                 between inputs and outputs as opposed to always specifying
                                            We believe that quick feedback and error reports are                       outputs as functions of inputs [13, 20]. Unlike deterministic
                                        essential for practical verification. Verifying programs af-                   specifications, constraints can be composed using conjunc-
                                        ter they have been developed is extremely time-consuming                       tions, which enables description of the problem as a combi-
                                        [19, 24] and it is difficult to argue its cost-effectiveness.                  nation of orthogonal requirements.
                                        Our research therefore explores approaches that support in-                       This paper introduces synthesis algorithms, techniques
                                        tegrated software construction and verification. An impor-                     and tools that integrate synthesis into the development pro-
                                        tant aspect of such approaches are modular verification tech-                  cess for functional program. We present a synthesizer that
                                        niques which can check that a function conforms to its local                   can construct the bodies of functions starting solely from
                                        specification. In such approach, the verification of an indi-                  their postconditions. The programs that our synthesizer pro-
                                        vidual function against its specification can start before the                 duces typically manipulate unbounded data types, such as
                                        entire software system is completed, so tools can provide                      algebraic data types and unbounded integers. Thanks to the
                                        rapid feedback that allows specifications and implementa-                      use of deductive synthesis and the availability of a verifier,
                                        tions to be developed simultaneously. Quoting [3], who re-                     when the synthesizer succeeds, the generated code is guar-
                                        port on the experience with Spec#,                                             anteed to be correct for all possible input values.
                                            “If verification ever makes it into the daily rhythm of                       Our synthesizer uses specifications as the description of
                                            mainstream programming, it will be through a design-                       the synthesis problems. While it could additionally accept
                                            time interface providing online verification.”                             input/output examples to illustrate the desired functionality,
                                                                                                                       we view such illustration as a special form of input/output
                                            We choose a functional language as the core language for
                                                                                                                       relation: whereas input/output examples correspond to tests
                                        the development of verified software. Functional languages
                                                                                                                       and provide a description of a finite portion of the desired
                                        strike an appealing balance between executability and ver-
                                                                                                                       functionality, we primarily focus on symbolic descriptions,
                                        ifiability, predicted already in [28]. Although the problem

                                        On Integrating Deductive Synthesis and Verification Systems                1                                                         2018/11/4
which ensure the desired behavior over an arbitrarily large            Verifier. Our automated verification environment is the en-
or even infinite domain. From such descriptions, our syn-              abler of synthesis. We use SMT solvers, specifically Z3 [29],
thesizer can automatically generate input/output examples              and a fair function unfolding strategy that is effective for suf-
when needed, but can also use them and transform them di-              ficiently surjective abstractions [43, 44]. We have achieved
rectly into executable code.                                           substantial speed-ups of this technique for satisfiable con-
    A notable degree of automation in our synthesizer comes            straints through the use of code generation and fair enu-
from synthesis procedures [12, 21, 22], which compile spec-            meration of structured values. The improvements in verifi-
ification fragments expressed in decidable logics. Our work            cation and falsification have transferred to the improvements
is the first implementation of the synthesis procedure for al-         in synthesis times.
gebraic data types [42].
    Note however, that, to capture a variety of scenarios in           Implemented synthesis framework. We developed a de-
software development, we also support the general problem              ductive synthesis framework that can accept a given set of
of synthesis of Turing-complete programs. The result is a              synthesis rules and applies them according to a cost function.
framework for cost-guided application of deductive synthe-             The framework accepts 1) a path conditions that encode pro-
sis rules, which decompose the problems into subproblems.              gram context, and 2) a relational specifications. It returns the
    Our synthesizer tightly cooperates with the underlying             function from inputs to outputs as a solution, as well as any
verifier, which allows it to achieve orders of magnitude bet-          necessary strengthening of the precondition needed for the
ter performance than using simpler generate-and-test ap-               function to satisfy the specification. We have deployed the
proaches. Techniques we use include symbolic transforma-               framework in a web-browser-based environment with con-
tion based on synthesis procedures, as well as synthesis of            tinuous compilation and the ability to interrupt the synthesis
recursive functions using counterexample-guided strategies.            to obtain a partial solution in the form of a new program with
We have evaluated a number of system architectures and                 a possibly simpler synthesis problem.
trade-offs between symbolic and concrete reasoning in our
implementation and arrived at an implementation that is suc-           Data type synthesis. Within the above framework we have
cessful despite the large space of possible programs.                  implemented rules for synthesis of algebraic data type equa-
    We believe that we have achieved a new level of automa-            tions and disequations [42], as well as a number of general
tion for a broad domain of recursive functional programs.              rules for decomposing specifications based on their logical
We consider a particular strength of our system that it can            structure or case splits on commonly useful conditions. We
synthesize code that satisfies a given relational specification        have developed program simplification techniques that post-
for all values of inputs, and not only given input/output pairs.       process the generated code and make it more readable.
    Despite aiming at a high automation level, we are aware
that any general-purpose automated synthesis procedure will            Support for recursion schemas and symbolic term genera-
ultimately face limitations of scalability and the ability to          tors. One of the main strengths in our framework is a new
control the development process. We deployed the synthesis             form of counterexample-guided synthesis that arises from a
algorithm as an interactive assistance that allows the devel-          combination of several rules.
oper to interleave manual and automated development steps.              • A set of built-in recursion schemas can solve a problem
In our system, the developer can decompose a function and                 by generating a fresh recursive function. To ensure well-
leave the subcomponents to the synthesizer, or, conversely,               foundedness we have extended our verifier with termi-
the synthesizer can decompose the problem, solve some of                  nation checking, and therefore generate only terminating
the subproblems, and leave the remaining open cases for the               function calls in this rule.
developer. To facilitate such synergy, we deploy an anytime
                                                                        • To generate bodies of functions, we have symbolic term
synthesis procedure, which maintains a ranked list of current
problem decompositions. The user can interrupt the synthe-                generators that systematically generate well-typed pro-
sizer at any time to display the current solution and continue            grams built from selected set of operators (such as alge-
manual development. This is possible thanks to the fact that              braic data type constructors and selectors). To test candi-
synthesis problems and specification problems are both ex-                date terms against specifications we use the Leon’s veri-
pressed in a unified language based on the construct resem-               fier. To speed up this search, the rule accumulates previ-
bling non-deterministic choice.                                           ously found counterexamples. Moreover, to quickly boot-
                                                                          strap the set of examples it uses systematic generators
1.1 Contributions                                                         that can enumerate in a fair way any finite prefix of a
The overall contribution of this paper is an integrated syn-              countable set of structured values. The falsification of
thesis and development system for automated and interac-                  generated bodies is done by direct execution of code. For
tive development of verified programs. A number of tech-                  this purpose, we have developed a lightweight compiler
niques from deductive and inductive reasoning need to come                for our subset of Scala into bytecodes, replacing many
together to make such system usable.                                      constraint reasoning steps by code execution.


On Integrating Deductive Synthesis and Verification Systems        2                                                            2018/11/4
Function generation by condition abduction. We also                   sealed abstract class Num
present and evaluate an alternative counterexample-guided             case object Z extends Num
rule tailored towards synthesis of recursive conditional func-        case class S(pred: Num) extends Num
tions, with the following characteristics.
                                                                      Because it is more convenient to think of these numerals
 • Instead of specialized term evaluators, the rule uses a            in term of their integer value, we can define an abstraction
    general expression enumerator based on generating all             function that computes it:
    expressions of a given type [10]. This results in a broad
                                                                      def value(n:Num) : Int = (n match {
    coverage of expressions that the rule can synthesize. It            case Z ⇒ 0
    uses a new lazy enumeration algorithm for such expres-              case S(p) ⇒ 1 + value(p)
    sions with polynomial-time access to the next term to             }) ensuring ( ≥ 0)
    enumerate [23]. Similarly to the previous rule, it filters
    well-typed expressions using counterexamples generated                The ensuring clause is Scala notation for a postcondi-
    from specifications and previous function candidates, as          tion [32]. These postconditions are defined by an anonymous
    well as based on structured value genererators.                   function, whose single argument denotes the result of the
                                                                      function. The underscore notation is a shorthand for x⇒x≥0,
 • The most distinctive aspect of this rule is the handling of
                                                                      so this annotation simply specifies that the integer represen-
    conditional expressions. The expressions are synthesized
                                                                      tation of a unary numeral is never negative, and Leon in-
    by collecting relevant terms that satisfy a notable number
                                                                      stantly proves this simple verification condition.
    of derived test inputs, and then trying to synthesize pred-
                                                                          Using our (verified) abstraction function, we can start
    icates that imply the correctness of candidate terms. This
                                                                      specifying operations on unary numerals. Consider for in-
    is an alternative to relying on existing rules to perform
                                                                      stance the addition operation. Its contract in terms of the
    splitting on simple conditions. Effectively, the additional
                                                                      value function is clear, so we can write it as:
    rule performs abduction of conditions until it covers the
    entire input space with a partition of conditions, where          def add(x : Num, y : Num) : Num = choose { (r: Num) ⇒
    each partition is associated with a term.                           value(r) == value(x) + value(y)
                                                                      }
Evaluation. We evaluate the current reach of our synthe-
sizer in fully automated mode by synthesizing functions               Here, choose is a special function defined by Leon to rep-
such as those that merge, partition, and sort lists of objects,       resent a computation that needs to be synthesized. Similarly
where lists are defined using a general mechanism for alge-           to the postcondition, it is defined by an anonymous func-
braic data types. This paper presents a description of all the        tions whose result represents the desired output. Contrary to
above techniques and a snapshot of our results. We believe            postconditions, though, the function (or synthesis predicate)
that the individual techniques are interesting by themselves,         can admit multiple arguments, in which case the synthesized
but we also believe that having a system that combines them           program should return a tuple of values of the appropriate
is essential to understand the potential of these techniques          types.
in addressing the difficult problem as synthesis. To gain full           Upon invocation of the Leon synthesis component, the
experience of the feeling of such development process, we             following recursive implementation is derived:
therefore invite the reader to explore the system themselves.         def add(x : Num, y : Num) : Num = (x match {
                                                                        case Z ⇒ y
2. Interactive Synthesis and Verification in                            case S(p) ⇒ add(p, S(y))
                                                                      }) ensuring(r ⇒ value(r) == value(x) + value(y))
   the Leon System
We start by illustrating through a series of examples how             We can continue expanding on these results, and define a
developers can leverage our system to write programs that             synthesis predicate for multiplication:
are correct by construction.                                          def mult(x : Num, y : Num) : Num = choose { (r: Num) ⇒
Unary numerals. As a first example, we will consider                    value(r) == value(x) ∗ value(y)
                                                                      }
tasks related to Unary numerals. While these examples are
simple in nature, they illustrate some very important points.         Leveraging the previous results for add, our synthesis algo-
In particular, they show how, using a combination of veri-            rithm derives the following program:
fication and synthesis, one can program functions manipu-
lating data types in one representation while specifying the          def mult(x : Num, y : Num) : Num = (x match {
                                                                        case Z ⇒ Z
operations using an abstract view.
                                                                        case S(p) ⇒ add(y, mult(p, y))
    Consider a standard definition of unary numerals as a re-         }) ensuring(r ⇒ value(r) == value(x) ∗ value(y))
cursive data type, with a base case “zero” and a “successor”
constructor.                                                          Both functions are generated within three seconds.

On Integrating Deductive Synthesis and Verification Systems       3                                                         2018/11/4
List manipulation. We believe this rapid feedback is                     We observe that in this programming style, users can write
mandatory when developing from specifications. One rea-                  (or generate) code by conjoining orthogonal requirements,
son is that, since contracts are typically partial, results ob-          such as constraints on the sizes and contents, which are only
tained from under-specifications can be remote from the de-              indirectly related. The rapid feedback make it possible to
sired output. Thus, a desirable strategy is to rapidly iterate           go through multiple candidates rapidly, strengthening the
and refine specifications until the output matches the expec-            specification as required.
tations.
    As an example, we will consider the task of synthesizing             Sorting. A typical example of a task that is easier to spec-
the split function necessary in merge sort. We start from                ify than to implement is sorting. We conclude this overview
a standard recursive definition of lists, and we assume the              of Leon’s synthesis capabilities by showing how to derive
existence of recursive functions computing their size (as a              an insertion sorting algorithm. We start from the straightfor-
non-negative integer), and their content (as a set of integers).         ward definition of isSorted, a function that checks whether a
                                                                         list is sorted:
sealed abstract class List
case class Cons(head: Int, tail: List) extends List                      def isSorted(lst : lst) : Boolean = lst match {
case object Nil extends List                                               case Nil ⇒ true
                                                                           case Cons( , Nil) ⇒ true
def size(lst : List) : Int = . . .                                         case Cons(x1, xs @ Cons(x2, )) ⇒ x1 ≤ x2 && isSorted(xs)
def content(lst : List) : Set[Int] = . . .                               }
   As a first attempt to synthesize split, we try the following          Using this function, the problem of sorting can be stated as
specification:                                                           simply as:
def split(lst : List) : (List,List) = choose { (r : (List,List)) ⇒
  content(lst) == content(r. 1) ++ content(r. 2)                         def sort(lst : List): List = choose { (r: List) ⇒
}                                                                          isSorted(r) && content(r) == content(lst)
                                                                         }
Leon instantly generates the following function which, while
it satisfies the contract, is not particularly useful:                   To achieve this goal, we start by specifying the helper func-
                                                                         tion insertSorted:
def split(lst : List) : (List,List) = (lst, Nil)
                                                                         def insertSorted(lst : List, v: Int): List = {
To avoid getting a single list with an empty one, we can
                                                                           require(isSorted(lst))
refine the specification by enforcing that the sizes of the                choose { (r: List) ⇒
resulting lists should not differ by more than one:                          isSorted(r) && content(r) == content(lst) ++ Set(v)
def split(lst : List) : (List,List) = choose { (r : (List,List)) ⇒         }
  content(lst) == content(r. 1) ++ content(r. 2)                         }
  && abs(size(r. 1)−size(r. 2)) ≤ 1
}                                                                        From this, Leon generates the following solution:

Again, Leon instantly generates a correct, useless, program:             def insertSorted(lst: List, v: Int): List = {
                                                                           require(isSorted(lst))
def split(lst : List) : (List,List) = (lst, lst)                           lst match {
We can further refine the specification by stating that the sum               case Nil ⇒ Cons(v, Nil)
of the sizes of the two lists should match the size of the input              case Cons(h, tail) ⇒
one:                                                                            val r = insertSorted(t, v)
                                                                                if (v > h) Cons(h, r)
def split(lst : List) : (List,List) = choose { (r : (List,List)) ⇒              else if (h == v) r
  content(lst) == content(r. 1) ++ content(r. 2)                                else Cons(v, Cons(h, t))
  && abs(size(r. 1) − size(r. 2)) ≤ 1                                    }
  && (size(r. 1) + size(r. 2)) == size(lst)
}                                                                        With the help of this insertion function, we can proceed to
                                                                         synthesizing sort with the simple specification mentioned
We then finally obtain a useful split function:
                                                                         above. Within five seconds, Leon generates the following
def split(lst: List): (List, List) = lst match {                         implementation of insertion sort:
  case Nil ⇒ (Nil, Nil)
  case Cons(h, Nil) ⇒ (Nil, Cons(h, Nil))                                def sort(lst : List): List = lst match {
  case Cons(h1, Cons(h2, t2)) ⇒                                            case Nil ⇒ Nil
    val r = split(t2)                                                      case Cons(h, t) ⇒ insertSorted(sort(t), h)
    (Cons(h1, r. 1), Cons(h2, r. 2))                                     }
}


On Integrating Deductive Synthesis and Verification Systems          4                                                         2018/11/4
3. The Leon Verifier                                                            4. Deductive Synthesis Framework
The results presented in this paper focus on the synthesis                      The approach to synthesis we follow in this paper is to derive
component of Leon. The language of Leon is a subset of                          programs by a succession of independently validated steps.
Scala, as illustrated through the examples of Section 2. Be-                    In this section, we briefly describe the formal reasoning be-
sides integers and user-defined recursive data types, Leon                      hind these constructive steps and provide some illustrative
supports booleans, sets and maps.                                               examples. A more extended exposition of this formal frame-
                                                                                work is available in [12].
Solver algorithm. At the core of Leon is an algorithm to
                                                                                4.1 Synthesis Problems
reason about formulas that include user-defined recursive
functions, such as size, content, and isSorted in Section 2.                    A synthesis problem is given by a predicate describing a
The algorithm proceeds by iteratively examining longer and                      desired relation between a set of input and a set of output
longer execution traces through the recursive functions. It al-                 variables, as well as the context (program point) at which
ternates between an over-approximation of the executions,                       the synthesis problem appears. We represent such a problem
where only unsatisfiability results can be trusted, and an                      as a quadruple
under-approximation, where only satisfiability results can be                                          Jā hΠ ✄ φi x̄K
concluded. The status of each approximation is checked us-                      where:
ing the state-of-the-art SMT solver Z3 from Microsoft Re-
                                                                                 • ā denotes the set of input variables,
search [29]. The algorithm is a semi-decision procedure,
meaning that it is theoretically complete for counterexam-                       • x̄ denotes the set of output variables,
ples: if a formula is satisfiable, Leon will eventually produce                  • φ is the synthesis predicate, and
a model [44]. Additionally, the algorithm works as a decision
                                                                                 • Π is the path condition to the synthesis problem.
procedure for a certain class of formulas [43].
   In the past, we have used this core algorithm in the con-                    The free variables of φ must be a subset of ā ∪ x̄. The
text of verification [44], but also as part of an experiment in                 path condition denotes a property that holds for input at the
providing run-time support for declarative programming us-                      program point where synthesis is to be performed, and the
ing constructs similar to choose [20]. We have in both cases                    free variables of Π should therefore be a subset of ā.
found the performance in finding models to be suitable for                         As an example, consider the following call to choose:
the task at hand. 1                                                             def f(a : Int) : Int = {
   Throughout this paper, we will assume the existence of an                      if(a ≥ 0) {
algorithm for deciding formulas containing arbitrary recur-                          choose((x : Int) ⇒ x ≥ 0 && a + x ≤ 5)
sive functions. Whenever completeness is an issue, we will                        } else . . .
mention it and describe the steps to be taken in case of, e.g.                  }
timeout.
                                                                                The representation of the corresponding synthesis problem
                                                                                is:
Compilation-based evaluator. Another component of                                          Ja ha ≥ 0 ✄ x ≥ 0 ∧ a + x ≤ 5i xK           (1)
Leon on which we rely in this paper is an interpreter based
on on-the-fly compilation to the JVM. Function definitions                      4.2 Synthesis Solutions
are typically compiled once and for all, and can therefore be                   We represent a solution to a synthesis problem as a pair
optimized by the JIT compiler. This component is used dur-
ing the search in the core algorithm, to validate models and                                                 hP | T̄ i
to sometimes optimistically obtain counterexamples. We use
                                                                                where:
it to quickly reject candidate programs during synthesis (see
sections 6 and 7).                                                               • P is the precondition, and
                                                                                 • T̄ is the program term.
Ground term generator. Our system also leverages Leon’s
generator of ground terms and its associated model finder.                      The free variables of both P and T̄ must range over ā. The
Based on a generate-and-test approach, it can generate                          intuition is that, whenever the path condition and the precon-
small models for formulas by rapidly and fairly enu-                            dition are satisfied, evaluating φ[x̄ 7→ T̄ ] should evaluate to
merating values of any type. For instance, enumerating                          true, i.e. T̄ are realizers for a solution to x̄ in φ given the
Lists will produce a stream of values Nil(), Cons(0, Nil()),                    inputs ā. Furthermore, for a solution to be as general as pos-
Cons(0, Cons(0, Nil())), Cons(1, Nil()), . . .                                  sible, the precondition must be as weak as possible.
                                                                                   Formally, for such a pair to be a solution to a synthesis
                                                                                problem, denoted as
1 We should also note that since the publication of [44], our engineering

efforts as well as the progress on Z3 have improved running times by 40%.                         Jā hΠ ✄ φi x̄K ⊢ hP | T̄ i

On Integrating Deductive Synthesis and Verification Systems                 5                                                           2018/11/4
the following two properties must hold:                                    The validity of each rule can be established independently
 • Relation refinement:                                                 from its instantiations, or from the context in which they it
                                                                        is used. This in turn guarantees that the programs obtained
                             Π ∧ P |= φ[x̄ 7→ T̄ ]                      by successive applications of validated rules are correct by
                                                                        construction.
    This property states that whenever the path- and precon-
                                                                        Generic reductions. As a first example, consider the rule
    dition hold, the program T̄ can be used to generate values
                                                                        O NE - POINT in Figure 1. It intuitively reads as follows; “if
    for the output variables x̄ such that the predicate φ is sat-
                                                                        the predicate of a synthesis problem contains a top-level
    isfied.
                                                                        atom of the form x0 = t, where x0 is an output variable not
 • Domain preservation:                                                 appearing in the term t, then we can solve a simpler problem
                                                                        where t is substituted for x0 , obtain a solution hP | T̄ i and
                              Π ∧ (∃x̄ : φ) |= P                        reconstruct a solution for the original one by first computing
                                                                        the value for t and then assigning as the result for x0 ”.
    This property states that the precondition P cannot ex-                Another, perhaps simpler, example is given by G ROUND
    clude inputs for which an output would exist such that φ            in Figure 1. This rule simply states that if a synthesis prob-
    is satisfied.                                                       lem does not refer to any input variable, then it can be treated
   As an example, a valid solution to the synthesis problem             as a satisfiability problem: any model for the predicate φ can
(1) is given by:                                                        then be used as a ground solution term for x̄.
                        ha ≤ 5 | 0i
                                                                        Conditionals. The rules we have seen so far generate
The precondition a ≤ 5 characterizes exactly the input                  straight-line, unconditional expressions. In order to synthe-
values for which a solution exists, and for all such values,            size programs that include conditional expressions, we need
the constant 0 is a valid solution term for x. Note that the            rules such as C ASE - SPLIT in Figure 1. The intuition behind
solution is in general not unique; alternative solutions for            C ASE - SPLIT is that a disjunction in the synthesis predicate
this particular problem include for instance ha ≤ 5 | 5 − ai,           can be handled by an if-then-else expression in the synthe-
or ha ≤ 5 | if(a < 5) a + 1 else 0i.                                    sized code, and each subproblem (corresponding to predi-
                                                                        cates φ1 and φ2 in the rule) can be treated separately. As
A note on path conditions. Strictly speaking, the inclusion
                                                                        one would expect, the precondition for the final program is
of the path condition does not add expressive power to the
                                                                        obtained by taking the disjunction of the preconditions for
representation of synthesis problems. One can easily verify
                                                                        the subproblems. This matches the intuition that the disjunc-
that the space of solution terms for Jā hΠ ✄ φi x̄K is isomor-
                                                                        tive predicate should be realizable if and only if one of its
phic to the one for Jā htrue ✄ Π ∧ φi x̄K. In the latter case,
                                                                        disjunct is. Note as well that even though the disjunction is
the path condition Π, is simply included in the precondition
                                                                        symmetrical, in the final program we necessarily privilege
of the solution. On the other hand, from the definition it fol-
                                                                        one branch over the other one. This has the interesting side-
lows that if hP | T̄ i is a solution and Π ∧ P is equivalent
                                                                        effect that we can, as shown in the rule, add the negation
to Π ∧ P ′ then hP ′ | T̄ i is also a solution to the synthe-
                                                                        of the precondition P1 to the path condition of the second
sis problem. We can let, P ′ be, for example, Π ∧ P , or, as
                                                                        problem. This has the potential of triggering simplifications
another extreme, Π → P . We have therefore found it con-
                                                                        in the solution of φ2 . An extreme case being when the first
venient in the implementation to explicitly keep track of the
                                                                        precondition is true and the “else” branch becomes unreach-
path conditions and allow freedom in the representation of
                                                                        able.
the returned precondition P .
                                                                           The C ASE - SPLIT rule as we presented it applies to dis-
4.3 Inference Rules for Synthesis                                       junctions in synthesis predicates. We should note that it is
                                                                        sometimes desirable to explicitly introduce such disjunc-
Building on our correctness criteria for synthesis solutions,           tions. For instance, our system includes rules to introduce
we now describe inference rules for synthesis. Such rules de-           branching on the equality of two variables, to perform case
scribe relations between synthesis problems, capturing how              analysis on the types of variables (pattern-matching), etc.
some problems can be solved by reduction to others. We                  These rules can be thought of as introducing first a disjunct,
have shown in previous work how to design a set of rules to             e.g. a = b ∨ a 6= b, then applying C ASE - SPLIT.
ensure completeness of synthesis for a well-specified class
of formulas, e.g. integer linear arithmetic relations [21] or           Recursion Schemas. We now show an example of an in-
simple term algebras [12]. In the interest of remaining self-           ference rule that produces a recursive function. A common
contained, we shortly describe some generic rules. We then              paradigm in functional programming is to perform a compu-
proceed to presenting inference rules which allowed us to               tation by recursively traversing a structure. The rule L IST-
derive synthesis solutions to problem that go beyond such               REC captures one particular form of such a traversal for the
decidable domains.                                                      List recursive type used in the examples of Section 2. The


On Integrating Deductive Synthesis and Verification Systems         6                                                           2018/11/4
                      Jā hΠ ✄ φ[x0 7→ t]i x̄K ⊢ hP | T̄ i    x0 ∈/ vars(t)                         M |= φ      vars(φ) ∩ ā = ∅
    O NE - POINT                                                                          G ROUND
                    Jā hΠ ✄ x0 = t ∧ φi x0 , x̄K ⊢ hP | val x̄ := T̄ ; (t , x̄)i                   Jā hΠ ✄ φi x̄K ⊢ htrue | Mi

                                        Jā hΠ ✄ φ1 i x̄K ⊢ hP1 | T̄1 i   Jā hΠ ∧ ¬P1 ✄ φ2 i x̄K ⊢ hP2 | T̄2 i
                      C ASE - SPLIT
                                             Jā hΠ ✄ φ1 ∨ φ2 i x̄K ⊢ hP1 ∨ P2 | if(P1 ) {T̄1 } else {T̄2 }i

           (Π1 ∧ P ) =⇒ Π2               Π2 [a0 7→ Cons(h,t)] =⇒ Π2 [a0 7→ t]         Jā hΠ2 ✄ φ[a0 7→ Nil]i x̄K ⊢ htrue | T̄1 i
                  Jr̄ , h , t , ā hΠ2 [a0 7→ Cons(h,t)] ∧ φ[a0 7→ t, x̄ 7→ r̄] ✄ φ[a0 7→ Cons(h,t)]i x̄K ⊢ htrue | T̄2 i
L IST- REC
                                                    Ja0 , ā hΠ1 ✄ φi x̄K ⊢ hP | rec(a0 ,ā)i


                                                         Figure 1. Selected synthesis inference rules.


 goal of the rule is to derive a solution consists of a single in-                 5. Exploring the Space of Subproblems
 vocation to a recursive function rec. The recursive function                      In the previous section, we described a general formal frame-
 has the following form:                                                           work in which we can describe what constitutes a synthe-
 def rec(a0 , ā) = {                                                              sis problem and a solution. In particular, we have shown
   require(Π2 )                                                                    how synthesis rules decompose synthesis problems into sub-
   a0 match {                                                                      problems. In this section, we describe how we automatically
     case Nil ⇒ T̄1                                                                search across rule instantiations to derive a complete solu-
     case Cons(h, t) ⇒
                                                                                   tion to a problem.
       val r̄ = rec(t, ā)
                                                                                       Inference rules are non-deterministic by nature. They jus-
       T̄2
   }                                                                               tify the correctness of a solution, but do not by themselves
 } ensuring(r̄ ⇒ φ[x̄ 7→ r̄])                                                      describe how one finds that solution. Our search for a solu-
                                                                                   tion alternates between considering 1) which rules apply to
 where a0 is of type List. The function iterates over the list a0                  given problems, and 2) which subproblems are generated by
 while preserving the rest of the input variables (the environ-                    rule instantiations.
 ment) ā. Observe that its postcondition corresponds exactly                          The task of finding rules that apply to a problem intu-
 to the synthesis predicate of the original problem. We now                        itively correspond to finding an inference rule whose con-
 go over the premises of the rule in detail:                                       clusion matches the structure of a problem. For instance,
   • The condition (Π1 ∧ P ) =⇒ Π2 is necessary to ensure                          to apply G ROUND, the problem needs to mention only out-
     that the initial call to rec in the final program will satisfy                put variables. Similarly, to apply L IST- REC to a problem, it
     its precondition.                                                             needs to contain at least one input variable of type List.
   • The condition Π2 [a0 7→ Cons(h,t)] =⇒ Π2 [a0 7→ t]                                Computing the subproblems resulting from the applica-
     states that the precondition of rec should be inductive,                      tion of a rule is in general straightforward, as they corre-
     i.e. whenever it holds for a list, it should also hold for its                spond to problems appearing in its premise. The G ROUND
     tail. This is necessary to ensure that the recursive call will                rule, for instance, generates no subproblem, while L IST- REC
     satisfy the precondition.                                                     generates two.
   • The subproblem Jā hΠ2 ✄ φ[a0 7→ Nil]i x̄K corresponds                        AND / OR search. To solve one problem, it suffices to find
     to the base case (Nil), and thus does not contain the input                   a complete derivation from one rule application to that prob-
     variable a0 .                                                                 lem. However, to fully apply a rule, we need to solve all
                                                                                   generated subproblems. This corresponds to searching for a
   • The final subproblem is the most interesting, and corre-
                                                                                   closed branch in an AND / OR tree [27].
     sponds to the case where a0 is a Cons, represented by
                                                                                       We now describe the expansion of such a tree using an
     the fresh input variables h and t. Because the recursive
                                                                                   example. Consider the problem of removing a given element
     structure is fixed, we can readily represent the result of
                                                                                   e from a list a. In our logical notation –using α as an abbre-
     the invocation rec(t,ā) by another fresh variable r. We
                                                                                   viation for content– the problem is:
     can assume that the postcondition of rec holds for that
     particular call, which we represent in the path condition                                Ja , e htrue ✄ α(x) = α(a) \ {e}i xK
     as φ[a0 7→ t, x̄ 7→ r̄]. The rest of the problem is obtained
     by substituting a0 for Cons(h,t) in the path condition and                    We denote this problem by 1 in the tree of Figure 2. While
     in the synthesis predicate.                                                   we haven’t given an exhaustive list of all rules used in our

 On Integrating Deductive Synthesis and Verification Systems                   7                                                         2018/11/4
                                                                  system, it is fair to assume that more than one can apply to
                                                                  this problem. For instance, we could case-split on the type of
                                                                  a, or apply L IST- REC to a. We represent these two options
                                                                  by A and B respectively in the tree.
                                                                     Following the option B and applying L IST- REC with the
                                                                  path condition Π2 ≡ true trivially satisfies the first two
                                                                  premises of the rules, and generates two new problems (5
                                                                  and 6). Problem 5 is:

                                   ...                                        Je htrue ✄ α(x) = α(Nil) \ {e}i xK
                           C       ...
                   2
                           D
                                   ...
                                                                  where the predicate simplifies to α(x) = ∅. This makes it
          A                        ...
                                                                  possible to apply the G ROUND rule (node G). This generates
                   3       E                                      no subproblem, and closes the subbranch with the solution
  1
                   4
                           ...
                                    6       H                     solution htrue | Nili. Problem 4 has the form:
                           F
          B                         7       I                                   Jr , h , t , e hα(r) = α(t) \ {e}✄
                   5       G                                                     α(x) = α(Cons(h,t)) \ {e}i xK

                                                                  Among the many possible rule applications, we can choose
                                                                  to case-split on the equality h = e (node F). This generates
                                                                  two subproblems. Problem 6

                                                                            Jr , h , t , e hα(r) = α(t) \ {e} ∧ e = h✄
                                                                                     α(x) = α(Cons(h,t)) \ {e}i xK

                                                                  and a similar problem 7, where e 6= h appears in the path
                                                                  condition instead of e = h. Both subproblems can be solved
                                                                  by using a technique we will describe in Section 6 to derive
                                                                  a term satisfying the synthesis predicate, effectively closing
                                                                  the complete branch from the root. The solutions for prob-
                                                                  lem 6 and 7 are htrue | ri and htrue | Cons(h,r)i respec-
                                                                  tively. A complete reconstruction of the solution given by
                                                                  the branch in gray yields the program:
                                                                  def rec(a : List) : List = a match {
                                                                    case Nil ⇒ Nil
                                                                    case Cons(h,t) ⇒
                                                                      val r = rec(t)
                                                                      if(e == h) r
                                                                      else Cons(h,r)
                                                                  }
                                                                      In the interest of space, we have only described the
                                                                  derivations that lead to the search. In practice of course, not
                                                                  all correct steps are taken in the right order. The interleaving
                                                                  of expansions of AND and OR nodes is driven by the esti-
                                                                  mated cost of problems and solutions.
                                                                  Cost models. In order to drive the search, we assign to
                                                                  each problem and to each rule application an estimated cost,
                                                                  which is supposed to under-approximate to actual final cost
                                                                  of a closed branch. For OR nodes (problems), the cost is
                                                                  simply the minimum of all remaining viable children, while
Figure 2. An AND / OR search tree used to illustrate our          for AND nodes (rule applications) we take the sum of the cost
search mechanism. Circles are OR nodes and represent prob-        of each children plus a constant. That constant intuitively
lems, while boxes are and nodes and represent our rule ap-        corresponds to the extra complexity inherent to a particular
plications. Nodes in grey are closed (solved).                    rule.

On Integrating Deductive Synthesis and Verification Systems   8                                                           2018/11/4
   A perfect measure for cost would be the running time                 We describe our non-deterministic programs as a set of
of the corresponding program. However, this is particularly          recursive non-deterministic generators. Intuitively, a gener-
hard to estimate, and valid under-approximations would               ator for a given type is a program that produces arbitrary
most likely be useless. We chose to measure program size             values of that type. For instance, a generator for positive in-
instead, as we expect it to be an reasonable proxy for com-          tegers could be given by:
plexity. We measure the size of the program as the number of
                                                                     def genInt() : Int = if(⋆) 0 else (1 + genInt())
branches, weighted by their proximity to the root. We found
this to be have a positive influence on the quality of solu-         where ⋆ represents a non-deterministic boolean value. Sim-
tions, as it discourages near-top-level branching.                   ilarly a non-deterministic generator for the List type could
   Using this metric, the cost inherent to a rule application        take the form:
roughly corresponds to the extra branches it introduces in the
program. We use a standard algorithm for searching for the           def genList() : List = if(⋆) Nil else Cons(genInt(), genList())
best solution [27], and the search thus always focuses on the            It is not required that generators can produce every value
current most promising solution. In our example in Figure 2,         for a given type; we could hypothesize for instance that our
we could imagine that after the case split at F, the B branch        synthesis solutions will only need some very specific con-
temporarily became less attractive. The search then focuses          stants, such as 0, 1 or −1. What is more likely is that our
for a while on the A branch, until expansion on that side (for       synthesis solutions will need to use input variables and ex-
instance by case-splitting on the type of the list) reached a        isting functions. Our generators therefore typically include
point where the minimal possible solution was worse than             variables of the proper type that are accessible in the synthe-
the B branch. We note that the complete search takes about           sis environment. Taking these remarks into account, if a and
two seconds.                                                         b are integer variables in the scope, and f is a function from
Anytime synthesis. Because we maintain the search tree               Int to Int, a typical generator for integers would be:
and know the current minimal solution at all times, we can
                                                                     def genInt() : Int = if(⋆) 0 else if(⋆) 1 else if(⋆) −1
stop the synthesis at any time and obtain a partial program                  else if(⋆) a else if(⋆) b else f(genInt())
that is likely to be good. This option is available in our im-
plementation, both from the console mode and the web in-
                                                                     From generators to formulas. Generators can in principle
terface. In such cases, Leon will return a program containing
                                                                     be any function with unresolved non-deterministic choices.
new invocations of choose corresponding to the open sub-
                                                                     For the sake of the presentation, we assume that they are
problems.
                                                                     “flat”, that is, they consist of a top-level non-deterministic
6. Symbolic Term Exploration                                         choice between n alternatives. (Note that the examples given
                                                                     above all have this form.)
In previous sections, we have introduced the notion of syn-             Encoding a generator into an SMT term is straightfor-
thesis inference rules, and described how to search over rule        ward: introduce for each invocation of a generator an un-
applications that generate subproblems. In this section, we          interpreted constant c of the proper type, and for each non-
describe one of our most important rules, which is responsi-         deterministic choice as many boolean variables b̄ as there are
ble for closing most of the branches in search trees. We call        alternatives. Encode that exactly one of the b̄ variables must
it Symbolic Term Exploration (STE).                                  be true, and constrain the value of c using the b̄ variables.
    The core idea behind STE is to symbolically represent               Recursive invocations of generators can be handled simi-
many possible terms (programs), and to iteratively prune             larly, by inserting another c variable to represent their value
them out using counterexamples and test case generation              and constraining it appropriately. Naturally, these recursive
until either 1) a valid term is proved to solve the synthesis        instantiations must stop at some point: we then speak of
problem or 2) all programs in the search spaces have been            an instantiation depth. As an example, the encoding of the
shown to be inadequate. Since we already have rules that             genList generator above with an instantiation depth of 1 and
take care of introducing branching constructs or recursive           assuming that genInt generates 0 or a is:
functions, we focus STE on the search for terms consisting
only of constructors and calls to existing functions.                           (b1 ∨ b2 ) ∧ (¬b1 ∨ ¬b2 )
Recursive generators. We start from a universal non-                         ∧ b1 ⇒ c1 = Nil ∧ b2 ⇒ c1 = Cons(c2 ,c3 )
deterministic program that captures all the (deterministic)
                                                                             ∧ (b3 ∨ b4 ) ∧ (¬b3 ∨ ¬b4 )
programs which we wish to consider as potential solutions.
We then try to resolve the non-deterministic choices in such                 ∧ b 3 ⇒ c2 = 0 ∧ b 4 ⇒ c2 = a
a way that the program realizes the desired property. Resolv-                ∧ (b5 ∨ b6 ) ∧ (¬b5 ∨ ¬b6 )
ing the choices consists in fixing some values in the pro-                   ∧ b5 ⇒ c3 = Nil ∧ b6 ⇒ c3 = Cons(c4 ,c5 )
gram, which we achieve by running a counterexample driven
search.                                                                      ∧ ¬b6


On Integrating Deductive Synthesis and Verification Systems      9                                                             2018/11/4
The clauses encode the following possible values for c1 : Nil,           non-deterministic program typically grows exponentially as
Cons(0, Nil) and Cons(a, Nil). Note the constraint ¬b6 which             instantiation depth increases. As the number of programs
encodes the instantiation depth of 1, by preventing the values           grows, the difficulty for the solver to satisfy (2) or (3) also
beyond that depth (namely c4 and c5 ) to participate in the              increases. As an alternative to symbolic elimination, we can
expression.                                                              often use concrete execution on a set of inputs to rule out
   For a given instantiation depth, a valuation for the b̄ vari-         many programs. We rely on Leon’s capability for small
ables encodes a determinization of the generators, and as a              model finding (see Section 3) to generate inputs that satisfy
consequence a program. We solve for such a program by                    the path condition. We then use on-the-fly code generation
running a refinement loop.                                               to compile the symbolic program into a function that takes
                                                                         as arguments the input variables as well as a boolean ar-
Refinement loop: discovering programs. Consider a syn-
                                                                         ray encoding the non-deterministic choices. This allows us
thesis problem Jā hΠ ✄ φi x̄K, where we speculate that a
                                                                         to rapidly discard hundreds or even thousand of programs.
generator for the types of x̄ can produce a program that real-
                                                                         Whenever the change is substantial, we regenerate a new
izes φ. We start by encoding the non-deterministic execution
                                                                         formula for (2) with much fewer boolean variables and con-
of the generator for a fixed instantiation depth (typically, we
                                                                         tinue from there. Note that very often, when STE is applied
start with 0). Using this encoding, the problem has the form:
                                                                         to a problem it cannot solve, concrete execution rules out all
                        φ ∧ B(ā, b̄, c̄) ∧ C(c̄, x̄)         (2)        programs in a fraction of a second and symbolic reasoning
                                                                         is never applied.
where φ is the synthesis problem, B is the set of clauses
obtained by encoding the execution of the generator and C                7. Type-Driven Counterexample-Guided
is a set of equalities tying x̄ to a subset of the c̄ variables.            Synthesis with Condition Abduction
Note that by construction, the values for c̄ (and therefore for
                                                                         Our second larger rule focuses on synthesizing recursive
x̄) are uniquely determined when ā and b̄ are fixed.
                                                                         functions that satisfy a given specification. We assume that
    We start by finding values for ā and b̄ such that (2) holds.
                                                                         we are given a function header and a postcondition, and that
If no such values exist, then our generators at the given
                                                                         we aim to synthesize a recursive function body. Note that
instantiation depth are not expressive enough to encode a
                                                                         the expression must be 1) a well-typed term with respect
solution to the problem. Otherwise, we extract for the model
                                                                         to the context of the program and 2) valid according to
the values b̄0 . They describe a candidate program, which we
                                                                         the imposed formal specification. Therefore, an approach
put to the test.
                                                                         to solve this kind of synthesis problems could be based on
Refinement loop: falsifying programs. We search for a                    searching the space of all expressions that can be built from
solution to the problem:                                                 all declarations visible at the corresponding place in the
                                                                         program, i.e. in the scope of choose, while limiting attention
                      ¬φ ∧ B(ā, b̄0 , c̄) ∧ C(c̄, x̄)        (3)        to those that type-check, have the desired type, and satisfy
                                                                         the given formal specification.
Note that b̄0 are constants, and that c̄ and x̄ are therefore               An obvious drawback of such approach is that, unless the
uniquely determined by ā this intuitively comes from the                process is carefully guided, the search becomes unfeasible
fact that b̄0 encodes a deterministic program, that c̄ encodes           due to search space explosion. In practice we indeed found
intermediate values in the execution of that program, and                that trivial generate-and-test strategies scale poorly with the
that x̄ encodes the result. With this in mind, it becomes clear          number of visible declarations and the search becomes prac-
that we are really solving for ā.                                       tically unfeasible even for small programs.
    If no such ā exist, then we have found a program that
realizes φ and we are done. If on the other hand we can                  7.1 Condition Abduction
find ā0 , then this constitutes an input that witnesses that our
                                                                         Our idea for guiding the search and incremental construction
program does not meet the specification.V In this case, we can           of correct expressions comes from the area of abductive
discard the program by asserting ¬ b̄, and going back to
                                                                         reasoning [16, 17]. Abductive reasoning, sometimes also
(2).
                                                                         called “inference to the best explanation”, is a method of
    Eventually, because the set of possible assignments to b̄ is
                                                                         reasoning in which one chooses a hypothesis that would
finite (for a given instantiation depth) this terminates. If we
                                                                         explain the observed evidence in the best way.
have not found a program, we can increase the instantiation
                                                                            The motivation behind the approach to applying abduc-
depth and try again. When the maximal depth is reached, we
                                                                         tive reasoning to program synthesis comes from examining
give up.
                                                                         implementations of practical purely functional, recursive al-
Filtering with concrete execution. While termination is                  gorithms. The key observation is that recursive functional al-
in principle guaranteed just by successive elimination of                gorithms share a similar pattern. They implement behaviour
programs in the refinement loop, the formula encoding the                through a combination of case analysis with control flow ex-

On Integrating Deductive Synthesis and Verification Systems         10                                                          2018/11/4
pressions (e.g. if-then-else) and recursive calls. This pattern         plementation for an expanding partition of inputs. The input
is encoded with a branching control flow expression that par-           to the algorithm is a path condition Π, a predicate φ (defined
titions the space of input values such that each branch repre-          by synthesis problem Jā hΠ ✄ φi x̄K), and a collection of
sents a correct implementation for a certain partition. Such            expressions s.
partitions are defined by conditions that guard branches in                 Condition p′ defines which inputs are left to consider at
the control flow.                                                       any given point in the algorithm; these are the inputs that
    This allows synthesizing branches separately by search-             belong to the current partition. The initial value of p′ is
ing for implementations that evaluate correctly only for cer-           true, so the algorithm starts with a partition that covers the
tain inputs while restricting the search space. Rather than             whole initial input space constrained only by the path con-
speculatively applying C ASE - SPLIT rule to obtain subprob-            dition Π. Let p1 , . . . , pk , where k > 0, be conditions ab-
lems and finding solutions for each branch by case analy-               duced up to a certain point in the algorithm. Then p′ repre-
sis (as described in Section 4), this idea applies a similar            sents the conjunction of negations of abduced conditions, i.e.
strategy in the reverse order – getting a candidate program             p′ = ¬p1 ∧ . . . ∧ ¬pk . Together with the path condition, it
and searching for a condition that would make it correct.               defines the current partition which includes all input values
Thus, the idea of abductive reasoning can be applied to guess           for which there is no condition abduced (nor correct imple-
the condition that defines a valid partition, i.e. “abduce” the         mentation found). Thus, the guard condition for the current
explanation for a partial implementation, with respect to a             partition is defined by Π ∧ p′ . The algorithm maintains the
given candidate program. The rule progressively applies this            partial solution sol, encoded as a function. sol encodes an
technique and enables effective search and construction of a            expression which is correct for all input values that satisfy
control flow expression that represents a correct implemen-             any of the abduced conditions and this expression can be re-
tation for more and more input cases, eventually construct-             turned as a partial solution at any point. Additionally, the al-
ing an expression that is a solution to the synthesis problem.          gorithm accumulates example models in the set M. Ground
                                                                        term generator, described in Section 3, is used to construct
7.2 The Algorithm Used in the Rule                                      the initial set of models in M. To construct a model, for each
Based on these observations, we present our rule that em-               variable in ā, the algorithm assigns a value sampled from the
ploys a new technique for guiding the search with ranking               ground term generator. Note that more detailed discussion
and filtering based on counterexamples, as well as construct-           on how examples are used to guide the search is deferred to
ing expressions from partially correct implementations. It is           Section 7.3.
presented in Algorithm 1.                                                   The algorithm repeats enumerating all possible expres-
                                                                        sions from the given collection until it finds a solution. In
Algorithm 1 Synthesis with condition abduction                          each iteration, a batch of expressions E is enumerated and
Require: path condition Π, predicate φ, a collection of                 evaluated on all models from M. The results of such eval-
    expressions s        ⊲ synthesis problem Jā hΠ ✄ φi x̄K            uation are used to rank expressions from E. The algorithm
 1: p′ = true                  ⊲ maintain the current partition         considers the expression of the highest rank r̄ as a candidate
 2: sol = (λx.x)                   ⊲ maintain a partial solution        solution and checks it for validity. If r̄ represents a correct
 3: M = S AMPLE M ODELS (ā)           ⊲ set of example models          implementation for the current partition, i.e. if hΠ ∧ p′ | r̄i
 4: repeat                                                              is a valid solution, then the expression needed to complete
 5:   get a set of expressions E from s             ⊲ candidates        a valid control flow expression is found. The algorithm re-
 6:   for each e in E do ⊲ count passed examples pe for e               turns it as solution for which Jā hΠ ✄ φi x̄K ⊢ hΠ | (sol r̄)i
 7:      pe = |{m ∈ M | e(m) is correct}|             ⊲ evaluate        holds. Otherwise, the algorithm extracts the counterexample
 8:   r̄ = arg max e∈E pe ⊲ the highest ranked expression               model m, adds it to the set M, and continues by trying to
 9:   if solution hΠ ∧ p′ | r̄i is valid then                           synthesize a branch with expression r̄ (it does so by call-
10:      return hΠ | (sol r̄)i             ⊲ a solution is found        ing Algorithm 2 which will be explained later). If B RANCH -
11:   else                                                              S YN returns a valid branch condition, the algorithm updates
12:      extract new counterexample model m                             the partial solution to include the additional branch (thus ex-
13:      M =M∪m                         ⊲ accumulate examples           tending extending the space of inputs covered by the partial
14:      c = B RANCH S YN(r̄, p, q, s)       ⊲ call Algorithm 2         solution), and refines the current partition condition. New
15:      if c 6= FALSE then           ⊲ a branch is synthesized         partition condition reduces the synthesis to a subproblem,
16:         sol = (λx. (sol (if c then r̄ else x)))                     ensuring that the solution in the next iteration covers cases
17:         p′ = p′ ∧ ¬c              ⊲ update current partition        where c does not hold. The algorithm eventually, given the
                                                                        appropriate terms from s, finds an expression that forms a
18: until s is not empty
                                                                        complete correct implementation for the synthesis problem.
                                                                            Algorithm 2 tries to synthesize a new branch by abducing
   The algorithm applies the idea of abducing conditions to             a valid branch condition c. It does this by enumerating a set
progressively synthesize and verify branches of a correct im-

On Integrating Deductive Synthesis and Verification Systems        11                                                           2018/11/4
Algorithm 2 Synthesize a branch                                        Using (counter-)examples. A technique that brings signif-
Require: expression r̄, condition p′ , predicate q, and a              icant performance improvements when dealing with large
    collection of expressions s ⊲ passed from Algorithm 1              search spaces is guiding the search and even avoid con-
 1: function B RANCH S YN (r̄, p′ , q, s)                              sidering candidate expressions according to the information
 2:   M′ = ∅           ⊲ set of accumulated counterexamples            from examples generated during synthesis. As described ear-
 3:   get a set of expressions E ′ from s          ⊲ candidates        lier, after checking an unsatisfiable formula, the rule queries
 4:   for each c in E ′ do                                             Leon for the witness model and accumulates examples that
 5:     if for each model m in M′ , c(m) = f alse then                 are used to narrow down the search space.
 6:        if solution hΠ ∧ c | r̄i is valid then                          Algorithm 2 uses accumulated counterexamples to filter
 7:          return c                  ⊲ a condition is abduced        out unnecessary candidate expressions when synthesizing a
 8:        else                                                        branch. It makes sense to consider a candidate expression
 9:          extract the new counterexample model m                    for a branch condition, c, for a check whether c makes r̄ a
10:          M′ = M′ ∪ m ⊲ accumulate counterexamples                  correct implementation, only if c prevents all accumulated
                                                                       counterexamples that already witnessed unsatisfiability of
11:   return FALSE                      ⊲ no condition is found
                                                                       the correctness formula for r̄, i.e. if ∀m ∈ M′ . c → ¬m.
                                                                       Otherwise, if ∃m ∈ M′ .¬(c → ¬m), then m is a valid
of expressions E ′ from s and checking whether it can find a           counterexample to the verification of hΠ ∧ c | r̄i. This ef-
valid condition expression, that would guard a partition for           fectively guides the search by the results of previous veri-
which the candidate expression r̄ is correct.The algorithm             fication failures while filtering out candidates before more
accumulates counterexamples models in M′ and considers                 expensive verification check are made.
a candidate expression c only if it prevents all accumulated               Algorithm 1 uses accumulated models to quickly test
counterexamples.The algorithm checks this by evaluating c              and rank expressions by evaluating models according to the
on m, i.e. c(m), for each accumulated counterexample m.                specification. The current set of candidate expressions E is
If a candidate expression c is not filtered out, the algorithm         evaluated on the set of accumulated examples M and re-
checks if c represents a valid branch condition, i.e. whether          sults of such evaluation are used to rank the candidates. We
hΠ ∧ c | r̄i is a valid solution. If yes, the algorithm returns        call an evaluation of a candidate e on a model m correct, if
c which, together with r̄, comprises a valid branch in the             m satisfies path condition Π and the result of the evaluation
solution to Jā hΠ ✄ φi x̄K. Otherwise, it adds a new coun-            satisfies given predicate q. The algorithm counts the num-
terexample model to M′ and continues with the search. If               ber of correct evaluations, ranks the candidates accordingly
no valid condition is in E ′ , the algorithm returns FALSE.            and considers only the candidate of the highest rank. The ra-
                                                                       tionale is that the more correct evaluations, the more likely
7.3 Organization of the Search
                                                                       the candidate represents a correct implementation for some
For getting the collection of expressions s, the rule uses             partition of inputs. Note that evaluation results may be used
term generators that generate all well typed terms accord-             only for ranking but not for filtering, because each candidate
ing to type constraints derived from the context of a pro-             may represent a correct implementation for a certain parti-
gram [10, 23]. This has the advantage of initial search space          tion of inputs, thus incorrect evaluations are expected even
restriction inherent to the generator that limits enumerated           for valid candidates. Since the evaluation amounts to execut-
expressions only to those that are well typed. The complete-           ing the specification this technique is efficient in guiding the
ness property of such generators ensures systematic enumer-            search toward correct correct implementations while avoid-
ation of all candidate solutions that are defined by the set           ing unnecessary verification checks.
of given type constraints. For verification, the rule uses the
Leon verifier, that allows checking validity of expressions
that are supported by the underlying theories and obtaining            8. Implementation and Results
counterexample models.                                                 We have implemented these techniques in Leon, a system
    The context of the algorithm as a rule in the Leon synthe-         for verification and synthesis of functional program, thus
sis framework imposes limits on the portion of search space            extending it from the state described in Section 3. Our im-
explored by each rule instantiation. This allows incremental           plementation and the online interface are available from
and systematic progress in search space exploration and, due           http://lara.epfl.ch/leon/.
to the mixture with other synthesis rules, offers benefits in             The front end to Leon is the standard Scala compiler (for
both expressiveness and performance of synthesis. The rule             Scala 2.9). Scala compiler performs type checking and tasks
offers flexibility in adjusting necessary parameters and thus          such as the expansion of implicit conversions, from which
a fine-grain control over the search - for our experiments, the        Leon directly benefits. Leon programs also execute as valid
size of candidate sets of expressions enumerated in each it-           Scala programs. Leon checks that the syntax trees produced
eration n is 50 (and is doubled in each iteration) and 20, in          conform to the subset that it expects and then performs
the case of Algorithm 1 and 2, respectively.                           verification and synthesis.

On Integrating Deductive Synthesis and Verification Systems       12                                                           2018/11/4
  Operation                Syn Size Calls sec. Proved                   }
                            √                      √
  List.Insert
                            √ 3      0     0.3     √                    would result in vastly different programs depending on the
  List.Delete
                            √ 19 1         2.0     √                    implementation of Number.
  List.Union
                            √ 12 1         2.0     √                       Our set of benchmarks displayed in Figure 3 covers the
  List.Diff
                            √ 12 2         7.0     √                    synthesis of various operations over custom data-structures
  List.Split                    27 1       2.0                          with invariants, specified through the lens of abstraction
                            √                      √
  SortedList.Insert
                            √ 34 1         8.9     √                    functions. These benchmarks use specifications with are
  SortedList.InsertAlways
                            √   36   1    12.5                          both easy to understand and much shorter than resulting pro-
  SortedList.Delete
                            √ 23 1         8.7     √                    grams (except in trivial cases). We believe these are key fac-
  SortedList.Union
                            √   19   2     5.0                          tors in the evaluation of any synthesis procedure. The defini-
  SortedList.Diff
                            √ 13 2         6.8     √                    tions and specifications of all the benchmarks can be found
  SortedList.InsertionSort
                            √   10   2     5.1     √                    in appendix.
  SortedList.MergeSort          11 4 87.7                                  Synthesis is performed in order, meaning that an opera-
                            √                      √
  StrictSortedList.Insert
                            √ 34 1         9.9                          tion will be able to reuse all previously synthesized ones,
  StrictSortedList.Delete
                            √   21   1    16.1     √                    thus mimicking the usual development process.
  StrictSortedList.Union        19 2       4.1                             We can see in Figure 3 the list of programs we success-
                            √                      √
  UnaryNumerals.Add
                            √ 11 1         1.6     √                    fully synthesized. Each synthesized program has been man-
  UnaryNumerals.Distinct
                            √   12   0     1.9     √                    ually validated to be a solution that a programmer might ex-
  UnaryNumerals.Mult            12 1       2.5                          pect. Our system typically also proves automatically that the
                                                                        resulting program matches the specification for all inputs. In
Figure 3. We consider a problem as synthesized if the so-               certain cases, the lack of inductive invariants prevents such
lution generated is correct after manual inspection. For each           fully-automated proof, which is a limitation of our verifier.
generated program, we provide the size of its syntax tree and           Note that we stop verification after a timeout of 3 seconds.
the number of function calls it contains. Proved problems are              In almost all cases, the synthesis succeeds sufficiently fast
those for which the synthesized program can be automati-                for a reasonable interactive experience.
cally proven to match its specification.
                                                                        9. Related Work
    We have developed several interfaces for Leon. Leon                 Our approach blends deductive synthesis [25, 26, 36], which
can be invoked as a batch command-line tool that accepts                incorporates transformation of specifications, inductive rea-
verification and synthesis tasks and outputs the results of the         soning, recursion schemes and termination checking, with
requested tasks. If desired, there is also a console mode that          modern SMT techniques and constraint solving for exe-
allows applying synthesis rules in a step-by-step fashion and           cutable constraints. As one of our subroutines we include
is useful for debugging purposes.                                       complete functional synthesis for integer linear arithmetic
    To facilitate interactive experiments and the use of the            [22] and extend it with complete functional synthesis for al-
system in teaching, we have also developed an interface that            gebraic data types [12, 42]. This gives us building blocks
executes in the web browser, using the Play framework of                for synthesis of recursion-free code. To synthesize recursive
Scala as well as JavaScript editors. Our browser-based in-              code we build on and further advance the counterexample-
terface supports continuous compilation of Scala code, al-              guided approach to synthesis [37].
lows verifying individual functions with a single keystroke
                                                                        Deductive synthesis frameworks. Early work on synthesis
or click, as well as synthesizing any given choose expres-
                                                                        [25, 26] focused on synthesis using expressive and undecid-
sion. In cases when the synthesis process is interrupted, the
                                                                        able logics, such as first-order logic and logic containing the
synthesizer can generate a partial solution that contains a
                                                                        induction principle.
program with further occurrences of the choose statement.
                                                                            Programming by refinement has been popularized as a
8.1 Results                                                             manual activity [2, 46]. Interactive tools have been devel-
                                                                        oped to support such techniques in HOL [4]. A recent exam-
In order to evaluate our system, we developed benchmarks
                                                                        ple of deductive synthesis and refinement is the Specware
with reusable abstraction functions. These abstraction func-
                                                                        system from Kesterel [36]. We were not able to use the sys-
tions allow for a concise specification of each operation
                                                                        tem first-hand due to its availability policy, but it appears to
without requiring any insight on its resulting implementa-
                                                                        favor expressive power and control, whereas we favor au-
tion. It is interesting to notice that these functions generally
                                                                        tomation.
abstract any structural invariant inherent to the underlying
                                                                            A combination of automated and interactive development
data-structure. For instance, the synthesis of
                                                                        is analogous to the use of automation in interactive theorem
def add(a: Num, b: Num) = choose {                                      provers, such as Isabelle [31]. However, whereas in verifica-
    (res: Num) ⇒ value(r) == value(a) + value(b)                        tion it is typically the case that the program is available, the

On Integrating Deductive Synthesis and Verification Systems        13                                                           2018/11/4
emphasis here is on constructing the program itself, starting        extended to repair that preserves good behaviors [6], which
from specifications.                                                 is related to our notion of partial programs that have remain-
    Work on synthesis from specifications [40] resolves some         ing choose statements.
of these difficulties by decoupling the problem of inferring
program control structure and the problem of synthesizing            10. Conclusions and Analysis
the computation along the control edges. The work lever-             Software synthesis is a difficult problem but we believe
ages verification techniques that use both approximation and         it can provide substantial help in software development.
lattice theoretic search along with decision procedures, but         We have presented a new framework for synthesis that
appears to require more detailed information about the struc-        combines transformational and counterexample-guided ap-
ture of the expected solution than our approach.                     proaches. Our implemented system can synthesize and prove
Synthesis with input/output examples. One of the first               correct functional programs that manipulate unbounded data
works that addressed synthesis with examples and put induc-          structures such as algebraic data types. We have used the
tive synthesis on a firm theoretical foundation is the one by        system to synthesized algorithms that manipulate list and
Summers [41]. Subsequent work presents extensions of the             tree structures. The algorithm can be combined with manual
classical approach to induction of functional Lisp-programs          transformations or run-time constraint solving to cover the
[11, 18]. These extensions include synthesizing a set of             cases where static synthesis does not fully solve the prob-
equations (instead of just one), multiple recursive calls and        lem. Our current counterexample-guided synthesis steps are
systematic introduction of parameters. Our current system            domain-agnostic, while somewhat limits their scalability, so
lifts several restrictions of previous approaches by supprot-        we expect improved results using domain-specific genera-
ing reasoning about arbitrary datatypes, supporting multiple         tors, such as the ones used in testing tools UDITA [8] and
parameters in concrete and symbolic I/O examples, and al-            Quickcheck [5]. Our framework leverages the state of the
lowing nested recursive calls and user-defined declarations.         art SMT solving technology and an effective mechanism
    Inductive (logic) programming that explores automatic            for solving certain classes of recursive functions. Thanks to
synthesis of (usually recursive) programs from incomplete            this technology, it was able to synthesize programs over un-
specifications, most often being input/output examples [7,           bounded domains that are guaranteed to be correct for all
30], influenced our work. Recent work in the area of pro-            inputs.
gramming by demonstration has shown that synthesis from
examples can be effective in a variety of domains, such as           Acknowledgments
spreadsheets [35]. Advances in the field of SAT and SMT              We thank Regis Blanc for his contribution to the Leon veri-
solvers inspired counter-example guided iterative synthe-            fication infrastructure. We thank Tihomir Gvero and Ruzica
sis [9, 37], which can derive input and output examples              Piskac for many discussions on synthesis.
from specifications. Our tool uses and advances these tech-
niques through two new counterexample-guided synthesis               References
approaches.                                                           [1] E. Asarin, O. Maler, and A. Pnueli. Symbolic controller
                                                                          synthesis for discrete and timed systems. In Hybrid Systems
Synthesis based on finitization techniques. Program                       II, pages 1–20, 1995.
sketching has demonstrated the practicality of program syn-
                                                                      [2] R.-J. Back and J. von Wright. Refinement Calculus. Springer-
thesis by focusing its use on particular domains [37–39].
                                                                          Verlag, 1998.
The algorithms employed in sketching are typically focused
on appropriately guided search over the syntax tree of the            [3] M. Barnett, M. Fähndrich, K. R. M. Leino, P. Müller,
                                                                          W. Schulte, and H. Venter. Specification and verification: the
synthesized program. The tool we presented shows one way
                                                                          Spec# experience. Commun. ACM, 54(6), June 2011.
to move the ideas of sketching towards infinite domains. In
this generalization we leverage reasoning about equations as          [4] M. Butler, J. Grundy, T. Langbacka, R. Ruksenas, and J. von
                                                                          Wright. The refinement calculator: Proof support for program
much as SAT techniques.
                                                                          refinement. In Proc. Formal Methods Pacific ’97, 1997.
Reactive synthesis. Synthesis of reactive systems gener-              [5] K. Claessen and J. Hughes. Quickcheck: a lightweight tool for
ates programs that run forever and interact with the envi-                random testing of haskell programs. In ICFP, pages 268–279,
ronment. However, known complete algorithms for reac-                     2000.
tive synthesis work with finite-state systems [34] or timed           [6] C. V. Essen and B. Jobstmann. Program repair without regret.
systems [1]. Such techniques have applications to control                 In CAV, 2013.
the behavior of hardware and embedded systems or concur-              [7] P. Flener and D. Partridge. Inductive programming. Autom.
rent programs [45]. These techniques usually take specifi-                Softw. Eng., 8(2):131–137, 2001.
cations in a fragment of temporal logic [33] and have re-             [8] M. Gligoric, T. Gvero, V. Jagannath, S. Khurshid, V. Kuncak,
sulted in tools that can synthesize useful hardware compo-                and D. Marinov. Test generation through programming in
nents [14, 15]. Recently such synthesis techniques have been              UDITA. In ICSE, pages 225–234, 2010.


On Integrating Deductive Synthesis and Verification Systems     14                                                              2018/11/4
 [9] S. Gulwani, S. Jha, A. Tiwari, and R. Venkatesan. Synthesis            [33] N. Piterman, A. Pnueli, and Y. Sa’ar. Synthesis of reactive(1)
     of loop-free programs. In PLDI, pages 62–73, 2011.                          designs. In VMCAI, 2006.
[10] T. Gvero, V. Kuncak, I. Kuraj, and R. Piskac. Complete                 [34] A. Pnueli and R. Rosner.     On the synthesis of a reactive
     completion using types and weights. In PLDI, 2013.                          module. In POPL, 1989.
[11] M. Hofmann. IgorII - an analytical inductive functional pro-           [35] R. Singh and S. Gulwani. Synthesizing number transforma-
     gramming system (tool demo). In PEPM, pages 29–32, 2010.                    tions from input-output examples. In CAV, pages 634–651,
[12] S. Jacobs, V. Kuncak, and P. Suter. Reductions for synthesis                2012.
     procedures. In VMCAI, pages 88–107, 2013.                              [36] D. R. Smith. Generating programs plus proofs by refinement.
[13] J. Jaffar and J.-L. Lassez. Constraint logic programming. In                In VSTTE, 2005.
     POPL, 1987.                                                            [37] A. Solar-Lezama, L. Tancau, R. Bodı́k, S. A. Seshia, and V. A.
[14] B. Jobstmann and R. Bloem. Optimizations for LTL synthesis.                 Saraswat. Combinatorial sketching for finite programs. In
     In FMCAD, 2006.                                                             ASPLOS, 2006.

[15] B. Jobstmann, S. Galler, M. Weiglhofer, and R. Bloem. Anzu:            [38] A. Solar-Lezama, G. Arnold, L. Tancau, R. Bodı́k, V. A.
     A tool for property synthesis. In CAV, 2007.                                Saraswat, and S. A. Seshia. Sketching stencils. In PLDI, pages
                                                                                 167–178, 2007.
[16] J. R. Josephson. Abductive Inference: Computation, Philoso-
     phy, Technology. Cambridge University Press, 1994.                     [39] A. Solar-Lezama, C. G. Jones, and R. Bodı́k.       Sketching
                                                                                 concurrent data structures. In PLDI, 2008.
[17] A. C. Kakas, R. A. Kowalski, and F. Toni. Abductive logic
                                                                            [40] S. Srivastava, S. Gulwani, and J. S. Foster. From program
     programming. J. Log. Comput., 2(6):719–770, 1992.
                                                                                 verification to program synthesis. In POPL, 2010.
[18] E. Kitzelmann and U. Schmid. Inductive synthesis of func-
                                                                            [41] P. D. Summers. A methodology for LISP program construc-
     tional programs: An explanation based generalization ap-
                                                                                 tion from examples. JACM, 24(1):161–175, 1977.
     proach. JMLR, 7:429–454, 2006.
                                                                            [42] P. Suter. Programming with Specifications. PhD thesis, EPFL,
[19] G. Klein, J. Andronick, K. Elphinstone, G. Heiser, D. Cock,
                                                                                 December 2012.
     P. Derrin, D. Elkaduwe, K. Engelhardt, R. Kolanski, M. Nor-
     rish, T. Sewell, H. Tuch, and S. Winwood. seL4: Formal veri-           [43] P. Suter, M. Dotta, and V. Kuncak. Decision procedures for
     fication of an OS kernel. In SOSP, pages 207–220, 2009.                     algebraic data types with abstractions. In POPL, pages 199–
                                                                                 210, 2010.
[20] A. S. Köksal, V. Kuncak, and P. Suter. Constraints as control.
     In POPL, pages 151–164, 2012.                                          [44] P. Suter, A. S. Köksal, and V. Kuncak. Satisfiability modulo
                                                                                 recursive programs. In SAS, pages 298–315, 2011.
[21] V. Kuncak, M. Mayer, R. Piskac, and P. Suter. Complete
     functional synthesis. In PLDI, pages 316–329, 2010.                    [45] M. T. Vechev, E. Yahav, and G. Yorsh. Inferring synchroniza-
                                                                                 tion under limited observability. In TACAS, 2009.
[22] V. Kuncak, M. Mayer, R. Piskac, and P. Suter. Software
     synthesis procedures. CACM, 55(2):103–111, 2012.                       [46] N. Wirth. Program development by stepwise refinement
                                                                                 (reprint). Commun. ACM, 26(1):70–74, 1983.
[23] I. Kuraj. Interactive code generation. Master’s thesis, EPFL,
     February 2013.
[24] D. Leinenbach and T. Santen. Verifying the microsoft hyper-v
     hypervisor with VCC. In FM, 2009.
[25] Z. Manna and R. J. Waldinger. Toward automatic program
     synthesis. Commun. ACM, 14(3):151–165, 1971.
[26] Z. Manna and R. J. Waldinger. A deductive approach to
     program synthesis. ACM Trans. Program. Lang. Syst., 2(1):
     90–121, 1980.
[27] A. Martelli and U. Montanari. Additive AND/OR graphs. In
     IJCAI, pages 1–11, 1973.
[28] J. McCarthy. Recursive functions of symbolic expressions and
     their computation by machine, part 1. Comm. A.C.M., 3:184–
     195, 1960.
[29] L. de Moura and N. Bjørner. Z3: An efficient SMT solver. In
     TACAS, 2008.
[30] S. Muggleton and L. D. Raedt. Inductive logic programming:
     Theory and methods. J. Log. Program., 19/20:629–679, 1994.
[31] T. Nipkow, L. C. Paulson, and M. Wenzel. Isabelle/HOL:
     A Proof Assistant for Higher-Order Logic, volume 2283 of
     LNCS. Springer-Verlag, 2002.
[32] M. Odersky. Contracts for scala. In RV, pages 51–57, 2010.


On Integrating Deductive Synthesis and Verification Systems            15                                                              2018/11/4
A. Benchmarks Definitions                                            A.2 SortedList
A.1 List                                                             object SortedListBenchmark {
                                                                       sealed abstract class List
object ListBenchmark {                                                 case class Cons(head: Int, tail: List) extends List
  sealed abstract class List                                           case object Nil extends List
  case class Cons(head: Int, tail: List) extends List
  case object Nil extends List                                         def size(l: List) : Int = (l match {
                                                                           case Nil ⇒ 0
    def size(l: List) : Int = (l match {                                   case Cons( , t) ⇒ 1 + size(t)
        case Nil ⇒ 0                                                   }) ensuring(res ⇒ res ≥ 0)
        case Cons( , t) ⇒ 1 + size(t)
    }) ensuring(res ⇒ res ≥ 0)                                         def content(l: List): Set[Int] = l match {
                                                                         case Nil ⇒ Set.empty[Int]
    def content(l: List): Set[Int] = l match {                           case Cons(i, t) ⇒ Set(i) ++ content(t)
      case Nil ⇒ Set.empty[Int]                                        }
      case Cons(i, t) ⇒ Set(i) ++ content(t)
    }                                                                  def isSorted(list : List) : Boolean = list match {
                                                                         case Nil ⇒ true
    def abs(i : Int) : Int = {                                           case Cons( , Nil) ⇒ true
      if(i < 0) −i else i                                                case Cons(x1, Cons(x2, )) if(x1 > x2) ⇒ false
    } ensuring( ≥ 0)                                                     case Cons( , xs) ⇒ isSorted(xs)
                                                                       }
    def insert(in1: List, v: Int) = choose {
      (out : List) ⇒                                                   def insert(in1: List, v: Int) = choose {
        content(out) == content(in1) ++ Set(v)                           (out : List) ⇒
    }                                                                      isSorted(in1) &&
                                                                           (content(out) == content(in1) ++ Set(v)) &&
    def delete(in1: List, v: Int) = choose {                               isSorted(out)
      (out : List) ⇒                                                   }
        content(out) == content(in1) -- Set(v)
    }                                                                  def insertAlways(in1: List, v: Int) = choose {
                                                                         (out : List) ⇒
    def union(in1: List, in2: List) = choose {                             isSorted(in1) &&
      (out : List) ⇒                                                       (content(out) == content(in1) ++ Set(v)) &&
        content(out) == content(in1) ++ content(in2)                       isSorted(out) &&
    }                                                                      size(out) == size(in1) + 1
                                                                       }
    def diff(in1: List, in2: List) = choose {
      (out : List) ⇒                                                   def delete(in1: List, v: Int) = choose {
        content(out) == content(in1) -- content(in2)                     (out : List) ⇒
    }                                                                      isSorted(in1) &&
                                                                           (content(out) == content(in1) -- Set(v)) &&
    def split(list : List) : (List,List) = {                               isSorted(out)
      choose { (res : (List,List)) ⇒                                   }
          val s1 = size(res. 1)
          val s2 = size(res. 2)                                        def union(in1: List, in2: List) = choose {
          abs(s1 − s2) ≤ 1 && s1 + s2 == size(list) &&                   (out : List) ⇒
          content(res. 1) ++ content(res. 2) == content(list)              isSorted(in1) &&
       }                                                                   isSorted(in2) &&
    }                                                                      (content(out) == content(in1) ++ content(in2)) &&
}                                                                          isSorted(out)
                                                                       }

                                                                       def diff(in1: List, in2: List) = choose {
                                                                         (out : List) ⇒
                                                                           isSorted(in1) &&
                                                                           isSorted(in2) &&
                                                                           (content(out) == content(in1) -- content(in2)) &&
                                                                           isSorted(out)


On Integrating Deductive Synthesis and Verification Systems     16                                                           2018/11/4
    }                                                              A.4 UnaryNumerals

    // In order to synthesize insertionSort, we let                object UnaryNumeralsBenchmark {
    // insert in the scope. Similarly for mergeSort,                 sealed abstract class Num
    // we keep only split and union in the scope.                    case object Z extends Num
    def sort(list: List): List = choose {                            case class S(pred: Num) extends Num
      (res: List) ⇒
           isSorted(res) &&                                            def value(n:Num) : Int = {
           content(res) == content(list)                                 n match {
    }                                                                      case Z ⇒ 0
                                                                           case S(p) ⇒ 1 + value(p)
}                                                                        }
                                                                       } ensuring ( ≥ 0)
A.3 StrictlySortedList
                                                                       def add(x: Num, y: Num): Num = {
object Complete {                                                        choose { (r : Num) ⇒
  sealed abstract class List                                               value(r) == value(x) + value(y)
  case class Cons(head: Int, tail: List) extends List                    }
  case object Nil extends List                                         }
    def size(l: List) : Int = (l match {                               def distinct(x: Num, y: Num): Num = {
        case Nil ⇒ 0                                                     choose { (r : Num) ⇒
        case Cons( , t) ⇒ 1 + size(t)                                      value(r) != value(x) &&
    }) ensuring(res ⇒ res ≥ 0)                                             value(r) != value(y)
                                                                         }
    def content(l: List): Set[Int] = l match {                         }
      case Nil ⇒ Set.empty[Int]
      case Cons(i, t) ⇒ Set(i) ++ content(t)                           def mult(x: Num, y: Num): Num = {
    }                                                                    choose { (r : Num) ⇒
                                                                           value(r) == value(x) ∗ value(y)
    def isSorted(list : List) : Boolean = list match {                   }
      case Nil ⇒ true                                                  }
      case Cons( , Nil) ⇒ true                                     }
      case Cons(x1, Cons(x2, )) if(x1 ≥ x2) ⇒ false
      case Cons( , xs) ⇒ isSorted(xs)
    }

    def insert(in1: List, v: Int) = choose {
      (out : List) ⇒
        isSorted(in1) &&
        (content(out) == content(in1) ++ Set(v)) &&
        isSorted(out)
    }

    def delete(in1: List, v: Int) = choose {
      (out : List) ⇒
        isSorted(in1) &&
        (content(out) == content(in1) -- Set(v)) &&
        isSorted(out)
    }

    def union(in1: List, in2: List) = choose {
      (out : List) ⇒
        isSorted(in1) &&
        isSorted(in2) &&
        (content(out) == content(in1) ++ content(in2)) &&
        isSorted(out)
    }
}



On Integrating Deductive Synthesis and Verification Systems   17                                               2018/11/4
