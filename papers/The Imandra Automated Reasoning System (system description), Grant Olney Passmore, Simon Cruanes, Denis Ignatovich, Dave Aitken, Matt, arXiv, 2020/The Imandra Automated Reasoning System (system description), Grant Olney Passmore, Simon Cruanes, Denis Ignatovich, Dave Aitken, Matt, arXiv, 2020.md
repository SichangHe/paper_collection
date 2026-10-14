                                             The Imandra Automated Reasoning System
                                                       (system description)

                                         Grant Olney Passmore, Simon Cruanes, Denis Ignatovich, Dave Aitken, Matt
                                            Bray, Elijah Kagan, Kostya Kanishev, Ewen Maclean, Nicola Mometto

                                                                          Imandra Inc., USA
arXiv:2004.10263v1 [cs.LO] 21 Apr 2020




                                               Abstract. We describe Imandra, a modern computational logic theo-
                                               rem prover designed to bridge the gap between decision procedures such
                                               as SMT, semi-automatic inductive provers of the Boyer-Moore family
                                               like ACL2, and interactive proof assistants for typed higher-order log-
                                               ics. Imandra’s logic is computational, based on a pure subset of OCaml
                                               in which all functions are terminating, with restrictions on types and
                                               higher-order functions that allow conjectures to be translated into multi-
                                               sorted first-order logic with theories, including arithmetic and datatypes.
                                               Imandra has novel features supporting large-scale industrial applications,
                                               including a seamless integration of bounded and unbounded verification,
                                               first-class computable counterexamples, efficiently executable models and
                                               a cloud-native architecture supporting live multiuser collaboration. The
                                               core reasoning mechanisms of Imandra are (i) a semi-complete proce-
                                               dure for finding models of formulas in the logic mentioned above, cen-
                                               tered around the lazy expansion of recursive functions, (ii) an inductive
                                               waterfall and simplifier which “lifts” many Boyer-Moore ideas to our
                                               typed higher-order setting. These mechanisms are tightly integrated and
                                               subject to many forms of user control.


                                         1   Introduction
                                         Imandra is a modern computational logic theorem prover built around a pure,
                                         higher-order subset of OCaml. Mathematical models and conjectures are writ-
                                         ten as executable OCaml programs, and Imandra may be used to reason about
                                         them, combining models, proofs and counterexamples in a unified computational
                                         environment. Imandra is designed to bridge the gap between decision proce-
                                         dures such as SMT [2], semi-automatic inductive provers of the Boyer-Moore
                                         family like ACL2 [1, 6], and interactive proof assistants for typed higher-order
                                         logics [4, 5, 7, 8]. Our goal is to build a friendly, easy to use system by lever-
                                         aging strong automation in proof search that can also robustly provide coun-
                                         terexamples for false conjectures. Imandra has novel features supporting large-
                                         scale industrial applications, including a seamless integration of bounded and
                                         unbounded verification, first-class computable counterexamples, efficiently exe-
                                         cutable models and a cloud-native architecture supporting live multiuser collab-
                                         oration. Imandra is already in use by major companies in the financial sector,
                                         including Goldman Sachs, Itiviti and OneChronos [9].
                                             An online version may be found at https://try.imandra.ai.
Fig. 1: An example Imandra session illustrating recursive definitions, computable
counterexamples (CX), bounded verification (verify upto), unbounded verification
with automated induction (@@auto), and higher-order instance synthesis.
                                        2
2     Logic

Imandra’s logic is built on a mechanized formal semantics for a pure, higher-
order subset of OCaml. Foundationally, the subset of OCaml Imandra supports
(called the ‘Imandra Modelling Language’) corresponds to a (specializable) com-
putational fragment of HOL equivalent to multi-sorted first-order logic with in-
duction up to 0 extended with theories of datatypes, integer and real arithmetic.
Theorems are implicitly universally quantified and expressed as Boolean-valued
functions. Proving a theorem establishes that the corresponding function al-
ways evaluates to true. As in PRA (Primitive Recursive Arithmetic) and Boyer-
Moore logics, existential goals are expressed with explicit computable Skolem
functions [1, 3, 11].


2.1   Definitional Principle

Users work with Imandra by incrementally extending its logical world through
definitions of types, functions, modules and theorems. Each extension is governed
by a definitional principle designed to maintain the consistency of Imandra’s cur-
rent logical theory through a discipline of conservative extensions. Types must be
proved well-founded. Functions must be proved terminating. These termination
proofs play a dual role: Their structure is mined in order to instruct Imandra
how to construct induction principles tailored to the recursive function being
admitted when it later appears in conjectures.
    Imandra’s definitional principle is built upon the ordinals up to 0 . Ordinals
are encoded as a datatype (Ordinal.t) in Imandra using a variant of Cantor normal
form, and the well-foundedness of Ordinal.(<<) — the strict less-than relation on
Ordinal.t values — is an axiom of Imandra’s logic.
    To prove a function f terminating, an ordinal-valued measure is required.
Measures can often be inferred (e.g., for structural recursions) and may be spec-
ified by the user. To establish termination, all recursive calls of f are collected
together with their guards, and their arguments must be proved to conditionally
map to strictly smaller ordinals via the measure. Imandra provides a shorthand
annotation for specifying lexicographic orders (@@adm), and explicit measure
functions may be given using the @@measure annotation.

Example 1 (Ackermann). We can define the Ackermann function and prove it
terminating with the attribute [@@adm m,n] which maps ack m n to the ordinal
m · ω + n. Alternatively, we could use [@@measure Ordinal.(pair (of int m) (of int n))]
to give an explicit measure via helper functions in Imandra’s Ordinal module.
let rec ack m n =
  if m <= 0 then n + 1 else if n <= 0 then ack (m−1) 1 else ack (m−1) (ack m (n−1))
[@@adm m,n]


Example 2. Here we have a naive version of the classic left-pad function [13],
where termination depends on both arguments in a non-lexicographic manner:


                                          3
let rec left pad c n xs =
  if List.length xs >= n then xs else left pad c n (c :: xs)
[@@measure Ordinal.of int (n − List.length xs)]


2.2    Lifting, Specialization and Monomorphization
Imandra definitions may be polymorphic and higher-order. However, once Iman-
dra is tasked with determining the truth value of a conjecture, the goal and its
transitive dependencies are transformed into a family of ground, monomorphic
first-order (recursive) definitions. These transformations include lambda lifting,
specialization and monomorphization. Imandra’s supported fragment of OCaml
is designed so that all admitted definitions may be transformed in this way.
Example 3. To prove the following higher-order theorem
theorem same len l =
  List.length (List.map (fun x −> x+1) l) = List.length l
we obtain a set of lower level definitions, where the anonymous function was
lifted, the type list was monomorphised, and map and length were specialised:
type int list = Nil int | Cons int of int ∗ int list
let rec length int = function
  | Nil int −> 0
  | Cons int ( , tl) −> 1 + length int tl
let map lambda0 x = x+1
let rec map1 = function
  | Nil int −> Nil int
  | Cons int (x, tl) −> Cons int (map lambda0 x, map1 tl)
theorem same len (l:int list) : bool =
  length int (map1 l) = length int l


3     Unrolling of Recursive Functions
A major feature of Imandra is its ability to automatically search for proofs and
counterexamples in a logic with recursive functions. When a counterexample is
found, it is reflected as a first-class value in Imandra’s runtime and can be directly
computed with and run through the model being analysed. In fact, the state-
ment verify (fun x −> ...) does not try any inductive proving unless requested;
the default strategy is recursive function unrolling for a fixed number of steps,
a form of bounded symbolic model-checking.
    Our core unrolling algorithm is similar in spirit to the work of Suter et al. [12]
but with crucial strategic differences. In essence, Imandra uses the assumption
mechanism of SMT to block all Boolean assignments that involve the evaluation
of a (currently) uninterpreted ground instance of a recursive function. A refine-
ment loop, based on extraction of unsat-cores from this set of assumptions, then
expands (interprets) the function calls one by one until a model is found, an
empty unsat-core is obtained, or a maximal number of steps is reached.


                                             4
Definition 1 (Function template). A function template for f is a set of
tuples (g, t, p) such that the body of f contains a call to g(t) under the path p.
Example 4.
 – fact(x) = if x > 1 (x∗fact(x−1)) 1 has as template {(fact, (x − 1), (x > 1))}
 – f (x) = 1 + if g(0) h(g(x)) h(42)
   has as template
   {(g, (0), >), (h, (g(x)), (g(0) = >)), (g, (x), g(0) = >), (h, (42), (g(0) = ⊥))}
    We use what we call reachability literals to prevent the SMT solver from
picking assignments that use function calls that are not expanded yet. A reacha-
bility literal is a Boolean atom that doesn’t appear in the original problem, and
that we associate to a given function call f (t) regardless of where it occurs. This
is to be contrasted with Suter et al.’s notion of control literals associated with
individual occurrences of function calls within the expanded body of another
function call. We denote by b[f (t)] the unique reachability literal for f (t).

 1   def calls of term(t: Term):
 2    return {b[f (u)] | f (u) / t}
 3
 4   def subcalls of call(f (t): Term,
                                    V expanded: Set[Term]):
 5    return {(b[g(u)], p) | (g, u, p) ∈ template(f )[t/x] ∧ g(u) 6∈ expanded}
 6
 7   def unroll(goal: Formula) −> SAT|UNSAT:
 8    q = calls of V  term(goal), expanded = ∅
 9    F = goal ∧ a∈q a
10    while True:
11      is sat, unsat core = check sat(F, assume={¬a | a ∈ q})
12      if is sat == SAT: return SAT
13      else if is sat == UNSAT:
14        if unsat core == ∅: return UNSAT
15        b[f (t)] = pick from(unsat core) # next call to expand
16        expanded = {f (t)} ∪ expanded
17        {(ai , pi )}i = subcalls of call(f (t), expanded)
18        q = q ∪ {ai }i \ b[f (t)]                   V
19        F = F ∧ b[f (t)] ∧ f (t) = bodyf [t/x] ∧ i (b[f (t)] ∧ pi ⇒ ai )
                               Fig. 2: Unrolling algorithm

    The main search loop is presented in Figure 2, where bodyf is the body of f
            def
(i.e. f (x) = bodyf ) and t / u means t is a proper subterm of u. We start with F
initialized to the original goal, and the queue q containing function calls in the
goal (computed by calls of term). Each iteration of the loop starts by checking
validity under the assumption that all reachability literals in q are false (line 11).
If no model is found, we pick an unexpanded function call f (t) from the unsat
core (line 15). Selection must be fair : all function calls must eventually be picked.
    To expand f (t), the corresponding reachability literal becomes true, we in-
stantiate the body of f on t, and use subcalls of call to compute the set of subcalls


                                             5
along with their control path within f (t) (using f ’s template). For each b[g(u)]
occurring under path p inside bodyf (t), we need toV
                                                   block models that would make
p valid until g(u) gets expanded. The assertions i (b[f (t)] ∧ pi ⇒ ai ) delegate
to SMT the work of tracking which paths are forbidden. This way, expanding
one function call might lead to many paths becoming “unlocked” at once.


4     Induction

Imandra has extensive support for automated induction built principally around
Imandra’s inductive waterfall 1 . This combines techniques such as symbolic exe-
cution, lemma-based conditional rewriting, forward-chaining, generalization and
the automatic synthesis of goal-specific induction principles. Induction principle
synthesis depends upon data computed about a function’s termination obtained
when it was admitted via our definitional principle. Imandra’s waterfall is deeply
inspired by the pioneering work of Boyer-Moore [1, 6], and is in many ways a
“lifting” of the Boyer-Moore waterfall to our typed, higher-order setting.




                        Fig. 3: Imandra’s inductive waterfall

   Imandra’s waterfall contains a simplifier which automatically makes use of
previously proved lemmas. Once proved, lemmas may be installed as rewrite,
forward-chaining, elimination or generalization rules. Imandra gives users feed-
back in order to help them design efficient collections of rules. With a good
1
    More details about Imandra’s waterfall and rule classes may be found in our online
    documentation at https://docs.imandra.ai.


                                           6
collection of rules (especially rewrite rules), it is hoped that “most” useful theo-
rems over a given domain will be provable by simplification alone, and induction
will only be applied as a last resort. In these cases, the subsequent waterfall
moves are designed to prepare the simplified conjecture for induction (via, e.g.,
generalization) before goal-specific induction principles are synthesized.
    Imandra’s inductive waterfall plays an important role in what we believe to be
a robust verification strategy for applying Imandra to real-world systems. Recall
that all Imandra goals may be subjected to bounded verification via unrolling (cf.
Sec 3). In practice, we almost always attack a goal by unrolling first, attempting
to verify it up to a bound before we consider trying to prove it by induction.
Typically, for real-world systems, models and conjectures will have flaws, and
unrolling will uncover many counterexamples, confusions and mistakes. As all
models are executable and all counterexamples are reflected in Imandra’s run-
time, they can be directly run through models facilitating rapid investigation.
It is typically only after iterating on models and conjectures until all (bounded)
counterexamples have been eliminated that we consider trying to prove them by
induction. Imandra’s support for counterexamples also plays another important
role: as a filter on heuristic waterfall steps such as generalization.

5   Architecture and User Interfaces
Imandra is developed in OCaml and integrates with its compiler libraries. Ar-
bitrary OCaml code may interact with Imandra models and counterexamples
through the use of Imandra’s program mode and reflection machinery. Iman-
dra integrates with Z3 [2] for checking satisfiability of various classes of ground
formulas. Imandra has a client-server architecture: (i) the client parses and exe-
cutes models with an integrated toplevel; (ii) the server, typically in the cloud,
performs all reasoning. Imandra’s user interfaces include:
Command line for power users, with tab-completion, hints, and colorful mes-
   sages. This interface is similar in some ways to OCaml’s utop.
Jupyter notebooks hosted online or via local installation through Docker [10].
   This presents Imandra through interactive notebooks in the browser.
VSCode plugin where documents are checked on the fly and errors are under-
   lined in the spirit of Isabelle’s Prover IDE [14].

6   Conclusion
Imandra is an industrial-strength reasoning system combining ideas from SMT,
Boyer-Moore inductive provers, and ITPs for typed higher-order logics. Imandra
delivers an extremely high degree of automation and has novel techniques such as
reflected computable counterexamples that we now believe are indispensible for
the effective industrial application of automated reasoning. We are encouraged
by Imandra’s success in mainstream finance [9], and share a deep conviction
that further advances in automation and UI — driven in large part by meeting
the demands of industrial users — will lead to a (near-term) future in which
automated reasoning is a widely adopted foundational technology.

                                         7
References
 1. Robert S. Boyer and J Strother Moore. A Computational Logic. Academic Press
    Professional, Inc., USA, 1979.
 2. Leonardo de Moura and Nikolaj Bjørner. Z3: An efficient SMT solver. In C. Ra-
    makrishnan and Jakob Rehof, editors, Tools and Algorithms for the Construction
    and Analysis of Systems, volume 4963 of Lecture Notes in Computer Science, chap-
    ter 24, pages 337–340. Springer, Berlin, Heidelberg, 2008.
 3. Reuben L. Goodstein. Recursive number theory: a development of recursive arith-
    metic in a logic-free equation calculus. North-Holland Pub. Co., Amsterdam, 1957.
 4. M. J. C. Gordon and T. F. Melham. Introduction to HOL: A Theorem Proving
    Environment for Higher Order Logic. Cambridge University Press, USA, 1993.
 5. John Harrison. HOL Light: An overview. In Stefan Berghofer, Tobias Nipkow,
    Christian Urban, and Makarius Wenzel, editors, Proceedings of the 22nd Interna-
    tional Conference on Theorem Proving in Higher Order Logics, TPHOLs 2009,
    volume 5674 of Lecture Notes in Computer Science, pages 60–66, Munich, Ger-
    many, 2009. Springer-Verlag.
 6. Matt Kaufmann and J Strother Moore. ACL2: An industrial strength version of
    Nqthm. In Computer Assurance, 1996. COMPASS’96, pages 23–34. IEEE, 1996.
 7. Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. Isabelle/HOL — A
    Proof Assistant for Higher-Order Logic, volume 2283 of LNCS. Springer, 2002.
 8. S. Owre, J. M. Rushby, , and N. Shankar. PVS: A prototype verification system.
    In Deepak Kapur, editor, 11th International Conference on Automated Deduction
    (CADE), volume 607 of Lecture Notes in Artificial Intelligence, pages 748–752,
    Saratoga, NY, jun 1992. Springer-Verlag.
 9. Grant Olney Passmore and Denis Ignatovich. Formal verification of financial
    algorithms. In International Conference on Automated Deduction, pages 26–41.
    Springer, 2017.
10. Fernando Pérez and Brian E. Granger. IPython: a system for interactive scientific
    computing. Computing in Science and Engineering, 9(3):21–29, May 2007.
11. Thoralf Skolem. The foundations of elementary arithmetic established by means of
    the recursive mode of thought, without the use of apparent variables ranging over
    infinite domains. In Jean van Heijenoort, editor, From Frege to Gödel. Harvard
    University Press, Cambridge, MA, USA, 1967.
12. Suter, Philippe and Köksal, Ali Sinan and Kuncak, Viktor. Satisfiability modulo
    recursive programs. In International Static Analysis Symposium, pages 298–315.
    Springer, 2011.
13. Wayne, Hillel. The Great Theorem Prover Showdown, 2018. https://www.
    hillelwayne.com/post/theorem-prover-showdown/.
14. Makarius Wenzel. Isabelle/jedit - A prover IDE within the PIDE framework. In
    Johan Jeuring, John A. Campbell, Jacques Carette, Gabriel Dos Reis, Petr Sojka,
    Makarius Wenzel, and Volker Sorge, editors, Intelligent Computer Mathematics -
    11th International Conference, Calculemus 2012, volume 7362 of Lecture Notes in
    Computer Science, pages 468–471. Springer, 2012.




                                          8
