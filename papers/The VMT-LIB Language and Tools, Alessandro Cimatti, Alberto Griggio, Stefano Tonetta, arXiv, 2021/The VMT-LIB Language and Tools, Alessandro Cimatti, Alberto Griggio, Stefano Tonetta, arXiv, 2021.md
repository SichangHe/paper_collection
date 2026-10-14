                                               The VMT-LIB Language and Tools
arXiv:2109.12821v1 [cs.LO] 27 Sep 2021




                                                  Alessandro Cimatti, Alberto Griggio, Stefano Tonetta

                                                                  Fondazione Bruno Kessler


                                                                            Abstract
                                                   We present VMT-LIB, a language for the representation of veri-
                                               fication problems of linear-time temporal properties on infinite-state
                                               symbolic transition systems. VMT-LIB is an extension of the stan-
                                               dard SMT-LIB language for SMT solvers, developed with the goal of
                                               facilitating the interoperability and exchange of benchmark problems
                                               among different verification tools. Besides describing its syntax and
                                               semantics, we also present a set of open-source tools to work with the
                                               language.


                                         1    Introduction
                                         In this paper we describe VMT-LIB, a language for the representation of ver-
                                         ification problems of linear-time temporal properties on infinite-state sym-
                                         bolic transition systems. VMT-LIB was designed with the main goal of
                                         being simple to use (i.e. to parse and generate) for verification tools, with
                                         the aim of facilitating the interoperability among different tools and the col-
                                         lection of verification benchmarks for infinite-state systems. As such, it is
                                         similar in spirit to the Aiger [3] language for finite-state systems, and to the
                                         BTOR [16] language for word-level systems with arrays, with the difference
                                         that VMT-LIB supports arbitrary background SMT theories, including e.g.
                                         linear and nonlinear arithmetic, uninterpreted functions, and quantifiers.
                                              VMT-LIB was developed as an extension of the standard SMT-LIB [2]
                                         language for SMT solvers, by exploiting the capability of SMT-LIB of at-
                                         taching metadata to terms and formulas via annotations. In particular, a
                                         valid VMT-LIB file is also a valid SMT-LIB file. This allows to reuse all the
                                         libraries for manipulating SMT-LIB formulas that are available for various
                                         languages (e.g. [10, 15, 1]). Besides these generic libraries, we have also de-
                                         veloped a set of tools to work with the language, including converters to and
                                         from other formats and formalisms (including Aiger, BTOR and Constrained

                                                                                 1
Horn Clauses). All the tools are open source and available at the VMT-LIB
webpage [18]. VMT-LIB is fully supported by the nuXmv [4] model checker,
and it has been used as a benchmark format in several publications over the
last few years (e.g. [6, 14, 11, 7, 5]).
    The rest of the report is structured as follows. After providing the nec-
essary theoretical background in §2, we describe the VMT-LIB syntax in §3,
and its semantics in §4. In §5 we describe a set of open-source tools that we
have developed to work with the language. Finally, we conclude in §6.


2    Theoretical Background and Definitions
Our setting is many-sorted first order logic. We use the standard notions
of theory, satisfiability, validity, and logical consequence. We refer to the
SMT-LIB specifications [2] for more details. We denote generic theories as
T . We write ϕ |=T ψ to denote that the formula ψ is a logical consequence
of ϕ in the theory T ; when clear from context, we omit T and simply write
ϕ |= ψ.
     We refer to 0-arity predicates as Boolean variables, and to 0-arity unin-
terpreted functions as (theory) variables.
     Given a set of variables X, a signature Σ, a domain M , an interpretation
function I of the symbols in Σ on the domain M , an assignment σ to the
variables in X on the domain M , and a σ-formula φ(X) with free variables
in X, the satisfaction relation hM, Ii |= φ is defined in the usual way.
     For each variable x, we assume that there exists a corresponding variable
x′ , called the primed version of x. If X is a set of variables, X ′ is the set
obtained by replacing each element x with its primed version (X ′ = {x′ |
x ∈ X}). ϕ′ is the formula obtained by replacing each occurrence variable
in ϕ with the corresponding primed.
     In the following, the signature Σ and the theory T are implicitly given.
A transition system (TS) S is a tuple hX, I(X), T (Y, X, X ′ )i where X is a
set of state variables, I(X) is a formula representing the initial states, and
T (Y, X, X ′ ) is a formula representing the transitions, where Y is a set of
input variables.


3    Syntax
VMT-LIB exploits the capability offered by the SMT-LIB language of at-
taching metadata to terms and formulas in order to specify the components



                                      2
of the transition system and the properties to verify. More specifically, we
use the following SMT-LIB annotations:

:next name is used to represent state variables. For each variable x in
     the model, the VMT-LIB file contains a pair of variables, xc and xn ,
     representing respectively the current and next version of x. The two
     variables are linked by annotating xc with the attribute :next xn .
     All the variables that are not in relation with another by means of a
     :next attribute are considered inputs. Note that :next must define
     an injective function (i.e. it is an error if there are two variables with
     the same :next value), and that the names of the variables are not
     important.

:init is used to specify the formula for the initial states of the model. This
     formula should contain neither next-state variables nor input variables.
     Multiple formulas annotated with :init are implicitly conjoined. As
     a convenience, the annotation can also use a “dummy” value true.

:trans is used to specify the formula for the transition relation. As in the
     case for :init, multiple :trans formulas are conjoined together, and
     also in this case the annotation can be written as :trans true.

:invar-property idx is used to specify invariant properties, i.e. formulas
     of the form Gp, where p is the formula annotated with :invar-property.
     The non-negative integer idx is a unique identifier for the property.

:live-property idx is used to specify an LTL property of the form FGp,
     where p is the formula annotated with :live-property. The non-
     negative integer idx is a unique identifier for the property.

    In a VMT-LIB file, only annotated terms and their sub-terms are mean-
ingful. Any other term is ignored. Moreover, only the following com-
mands are allowed to occur in VMT-LIB files: set-logic, set-option,
declare-sort, define-sort, declare-fun, define-fun.(For convenience,
an additional (assert true) command is allowed to appear at the end of
the file.)
The following example shows a simple model in the syntax of nuXmv [4] on
the left, and its corresponding VMT-LIB translation on the right.




                                      3
           nuXmv                                  VMT
                             ; declaring the state variable x
                             (declare-const x Int)
  MODULE main                (declare-const x.next Int)
  -- declaring the state     (define-fun sv.x () Int (! x :next x.next))
  -- variable x
  VAR x : integer;           (declare-const b Bool)
  IVAR b : boolean;          (define-fun init () Bool
  INIT x = 1;                         (! (= x 1) :init))
  TRANS                      (define-fun trans () Bool
  next(x) = b ? x + 1 : x;      (! (= x.next (ite b (+ x 1) x)) :trans)
  INVARSPEC x > 0;           (define-fun p1 () Bool
  LTLSPEC FG x > 10;                       (! (> x 0) :invar-property 1))
                             (define-fun p2 () Bool
                                           (! (> x 10) :live-property 2))



    Since the SMT-LIB format (and thus also the VMT-LIB one that inherits
from SMT-LIB) does not allow to annotate the declaration of variables, it is
a good practice to insert immediately after the declaration of the variables
a set of defines to specify the relations among variables. See for instance
the define sv.x in the example above that introduces the relation between
x and x.next.

LTL Properties, Invariant Constraints and Fairness Conditions.
Since one of the main goals of VMT-LIB is that of simplicity, the language
does not provide any direct support for high-level constructs such as spec-
ifications written in full LTL, invariant constraints or fairness conditions.
However, this is not a limitation in terms of expressiveness, as all such con-
structs can be easily encoded in VMT-LIB:

LTL properties can be compiled into invariant and/or live properties us-
    ing standard algorithms from the literature (e.g. [17, 9, 8]);

invariant constraints can be straightforwardly embedded into init and
     trans formulas;

fairness conditions can be embedded into live properties using a symbolic
     version of standard degeneralization procedures for Büchi automata
     (e.g. [12]).




                                      4
4     Semantics
Given a transition system S =               ˙ hX, I(X), T (Y, X, X ′ )i over a background
theory T with a signature Σ and an interpretation I, a state s of S is
an interpretation of the state variables X. A (finite) path of S is a finite
sequence π =s   ˙ 0 , s1 , . . . , sk of states, with the same domain and interpretation
of symbols in the signature Σ, such that I, s0 |= I(X) and for all i, 0 ≤ i < k,
I, si , s′i+1 |= ∃Y.T (Y, X, X ′ ). We say that a state s is reachable in S iff there
exists a path of S ending in s. Note that, since the interpretation I is
unique, uninterpreted function and predicate symbols are rigid, i.e. they
are not allowed to change across states.

Invariant Properties
An invariant property p is a symbolic representation of a set of states that
must be a superset of the reachable states of S. In other words, S |= p iff
∀s.s is reachable in S, s |= p. Consequently, a counterexample for p is a
finite path s0 , . . . , sk of S such that sk |= ¬p.

Live Properties
A live property p represents a set of states that is eventually invariant. In
LTL syntax, it would be denoted with FGp. More formally, S |= p iff for
all paths s0 , . . . , si , . . ., ∃i.∀j > i.sj |= p. (Note that finite paths s0 , . . . , sk
vacuously satisfy a live property, because we can always take i = k to satisfy
the previous definition.) Consequently, a counterexample for p is an infinite
path s0 , . . . , si , . . . of S such that ∀i.∃j > i.sj |= ¬p.


5     VMT-LIB Tools
VMT-LIB support in verification tools. The VMT-LIB language is
fully supported by nuXmv [4], a state-of-the-art symbolic model checker for
finite- and infinite-state systems. Recently, the language has been adopted
also by the AVR [11] model checker. VMT-LIB is also the native language
of ic3ia [13], an efficient open-source model checker for invariant and LTL
properties, as well as its recent extensions ProphIC3 [14] (for discovering
universally quantified invariants over arrays) and Lambda [7] (for the veri-
fication of parametric systems).




                                             5
Tools for working with VMT-LIB. We provide a set of tools (mainly
written in the Python programming language) to work with the VMT-LIB
language. They are all available from the VMT-LIB webpage [18]. Cur-
rently, the following tools are provided:

 vmt.py: parsing and printing of transition systems in VMT-LIB.

 vmt2btor.py: converter from VMT-LIB to the BTOR format.

 btor2vmt.py: converter from BTOR to VMT-LIB.

 vmt2horn.py: converter from VMT-LIB to Constrained Horn Clauses.

 vmt2nuxmv.py: converter from VMT-LIB to the SMV dialect of nuXmv.

 ltl2vmt.py: a tool to convert arbitrary LTL properties into VMT-LIB
      :live-property specifications, by compiling them into symbolic tableaux
      which are then put in product with the transition system.

Moreover, further converters to VMT-LIB are available through nuXmv and
ic3ia. In particular, ic3ia provides a horn2vmt tool for converting Con-
strained Horn Clauses to VMT-LIB, whereas nuXmv can be used to convert
from VMT-LIB to Aiger and vice versa.


6    Conclusions
We have presented VMT-LIB, a language and a set of tools for the specifi-
cation of verification problems over infinite-state transition systems aimed
at simplicity and interoperability. In the future, we plan to extend the
format to support the representation of counterexample traces for violated
properties, and possibly also proof certificates for verified properties.


References
 [1] Daniel Baier, Dirk Beyer, and Karlheinz Friedberger. JavaSMT 3: In-
     teracting with SMT Solvers in Java. In Alexandra Silva and K. Rus-
     tan M. Leino, editors, Computer Aided Verification - 33rd International
     Conference, CAV 2021, Virtual Event, July 20-23, 2021, Proceedings,
     Part II, volume 12760 of Lecture Notes in Computer Science, pages
     195–208. Springer, 2021.



                                     6
[2] Clark Barrett, Pascal Fontaine, and Cesare Tinelli.     The
    SMT-LIB Standard:    Version 2.6.    Technical report, 2021.
    https://smtlib.cs.uiowa.edu/papers/smt-lib-reference-v2.6-r2021-05-12.pdf.

[3] Armin Biere, Keijo Heljanko, and Siert Wieringa. AIGER 1.9 and
    beyond. Technical Report 11/2, Institute for Formal Models and Ver-
    ification, Johannes Kepler University, Altenbergerstr. 69, 4040 Linz,
    Austria, 2011.

[4] Roberto Cavada, Alessandro Cimatti, Michele Dorigatti, Alberto Grig-
    gio, Alessandro Mariotti, Andrea Micheli, Sergio Mover, Marco Roveri,
    and Stefano Tonetta. The nuXmv Symbolic Model Checker. In Armin
    Biere and Roderick Bloem, editors, Computer Aided Verification - 26th
    International Conference, CAV 2014, Held as Part of the Vienna Sum-
    mer of Logic, VSL 2014, Vienna, Austria, July 18-22, 2014. Proceed-
    ings, volume 8559 of Lecture Notes in Computer Science, pages 334–342.
    Springer, 2014.

[5] Alessandro Cimatti, Alberto Griggio, Ahmed Irfan, Marco Roveri, and
    Roberto Sebastiani. Incremental Linearization for Satisfiability and
    Verification Modulo Nonlinear Arithmetic and Transcendental Func-
    tions. ACM Trans. Comput. Log., 19(3):19:1–19:52, 2018.

[6] Alessandro Cimatti, Alberto Griggio, Sergio Mover, and Stefano
    Tonetta. Infinite-state invariant checking with IC3 and predicate ab-
    straction. Formal Methods Syst. Des., 49(3):190–218, 2016.

[7] Alessandro Cimatti, Alberto Griggio, and Gianluca Redondi. Universal
    Invariant Checking of Parametric Systems with Quantifier-free SMT
    Reasoning. In André Platzer and Geoff Sutcliffe, editors, Automated
    Deduction - CADE 28 - 28th International Conference on Automated
    Deduction, Virtual Event, July 12-15, 2021, Proceedings, volume 12699
    of Lecture Notes in Computer Science, pages 131–147. Springer, 2021.

[8] Koen Claessen, Niklas Eén, and Baruch Sterin. A circuit approach to
    LTL model checking. In Formal Methods in Computer-Aided Design,
    FMCAD 2013, Portland, OR, USA, October 20-23, 2013, pages 53–60.
    IEEE, 2013.

[9] Edmund M. Clarke, Orna Grumberg, and Kiyoharu Hamaguchi. An-
    other look at LTL model checking. Formal Methods in System Design,
    10(1):47–71, 1997.


                                   7
[10] Marco Gario and Andrea Micheli. PySMT: a solver-agnostic library for
     fast prototyping of SMT-based algorithms. In SMT Workshop 2015,
     2015.

[11] Aman Goel and Karem A. Sakallah. AVR: Abstractly Verifying Reach-
     ability. In Armin Biere and David Parker, editors, Tools and Algorithms
     for the Construction and Analysis of Systems - 26th International Con-
     ference, TACAS 2020, Held as Part of the European Joint Conferences
     on Theory and Practice of Software, ETAPS 2020, Dublin, Ireland,
     April 25-30, 2020, Proceedings, Part I, volume 12078 of Lecture Notes
     in Computer Science, pages 413–422. Springer, 2020.

[12] Alberto Griggio, Marco Roveri, and Stefano Tonetta. Certifying proofs
     for SAT-based model checking. Form Methods Syst Des, 2021.

[13] Ic3ia. https://es-static.fbk.eu/people/griggio/ic3ia/.

[14] Makai Mann, Ahmed Irfan, Alberto Griggio, Oded Padon, and
     Clark W. Barrett. Counterexample-Guided Prophecy for Model Check-
     ing Modulo the Theory of Arrays. In Jan Friso Groote and Kim Guld-
     strand Larsen, editors, Tools and Algorithms for the Construction and
     Analysis of Systems - 27th International Conference, TACAS 2021,
     Held as Part of the European Joint Conferences on Theory and Prac-
     tice of Software, ETAPS 2021, Luxembourg City, Luxembourg, March
     27 - April 1, 2021, Proceedings, Part I, volume 12651 of Lecture Notes
     in Computer Science, pages 113–132. Springer, 2021.

[15] Makai Mann, Amalee Wilson, Cesare Tinelli, and Clark W. Barrett.
     Smt-Switch: A Solver-agnostic C++ API for SMT Solving. In François
     Bobot and Tjark Weber, editors, Proceedings of the 18th International
     Workshop on Satisfiability Modulo Theories co-located with the 10th In-
     ternational Joint Conference on Automated Reasoning (IJCAR 2020),
     Online (initially located in Paris, France), July 5-6, 2020, volume 2854
     of CEUR Workshop Proceedings, pages 48–58. CEUR-WS.org, 2020.

[16] Aina Niemetz, Mathias Preiner, Clifford Wolf, and Armin Biere.
     BTOR2 , BtorMC and Boolector 3.0. In Hana Chockler and Georg
     Weissenbacher, editors, Computer Aided Verification - 30th Interna-
     tional Conference, CAV 2018, Held as Part of the Federated Logic Con-
     ference, FloC 2018, Oxford, UK, July 14-17, 2018, Proceedings, Part
     I, volume 10981 of Lecture Notes in Computer Science, pages 587–595.
     Springer, 2018.

                                     8
[17] Moshe Y. Vardi. An automata-theoretic approach to linear temporal
     logic. In Banff Higher Order Workshop, volume 1043 of LNCS, pages
     238–266. Springer, 1995.

[18] VMT-LIB. http://vmt-lib.org.




                                  9
