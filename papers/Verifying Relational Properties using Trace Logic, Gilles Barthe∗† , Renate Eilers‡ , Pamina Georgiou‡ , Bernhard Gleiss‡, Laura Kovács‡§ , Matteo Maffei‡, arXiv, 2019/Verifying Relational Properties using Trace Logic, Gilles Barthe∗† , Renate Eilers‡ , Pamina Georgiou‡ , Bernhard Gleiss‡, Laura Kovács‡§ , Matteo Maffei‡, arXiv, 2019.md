                                            Verifying Relational Properties using Trace Logic
                                               Gilles Barthe∗† , Renate Eilers‡ , Pamina Georgiou‡ , Bernhard Gleiss‡, Laura Kovács‡§ , Matteo Maffei‡
                                                                              ∗ Max Planck Institute for Security and Privacy, Germany
                                                                                           † IMDEA Software Institute, Spain
                                                                                                    ‡ TU Wien, Austria
                                                                                     § Chalmers University of Technology, Sweden




                                            Abstract—We present a logical framework for the verification
arXiv:1906.09899v3 [cs.LO] 12 Aug 2019




                                                                                                                 1    func main()
                                         of relational properties in imperative programs. Our frame-
                                                                                                                 2   {
                                         work reduces verification of relational properties of imperative
                                                                                                                 3       const Int[] a;
                                         programs to a validity problem in trace logic, an expressive
                                                                                                                 4       const Int alength;
                                         instance of first-order predicate logic. Trace logic draws its
                                                                                                                 5
                                         expressiveness from its syntax, which allows expressing properties
                                                                                                                 6           Int i = 0;
                                         over computation traces. Its axiomatization supports fine-grained
                                                                                                                 7           Int hw = 0;
                                         reasoning about intermediate steps in program execution, notably
                                                                                                                 8
                                         loop iterations. We present an algorithm to encode the semantics
                                                                                                                 9           while (i < alength)
                                         of programs as well as their relational properties in trace logic,
                                                                                                                10           {
                                         and then show how first-order theorem proving can be used
                                                                                                                11              hw = hw + a[i];
                                         to reason about the resulting trace logic formulas. Our work
                                                                                                                12              i = i + 1;
                                         is implemented in the tool R APID and evaluated with examples
                                                                                                                13           }
                                         coming from the security field.
                                                                                                                14       }
                                                                I. I NTRODUCTION
                                                                                                                                 Fig. 1: Motivating example.
                                            Program verification generally focuses on proving that all
                                         executions of a program lie within a specified set of execu-
                                         tions, that is, properties are seen as sets of traces. However, this   (2) We encode the semantics of programs as well as relational
                                                                                                                program properties in L (Section IV). Specifically, given
                                         approach is not general enough to capture various fundamental
                                                                                                                a program P and a relational property F , we construct a
                                         properties, such as non-interference [1] and robustness [2].
                                         These notions are naturally modelled as relational properties,         first-order formula ξ in L such that validity of ξ entails
                                                                                                                that P satisfies F . Note that this semantic characterization
                                         that is as properties over sets of pairs of traces. Relational
                                                                                                                stands in contrast with methods based on product programs,
                                         properties are special instances of hyperproperties [3], which
                                         are formally defined as sets of sets of traces.                        Hoare logics, and relational Hoare logics, where verification
                                                                                                                is syntax-directed.
                                            Verification of relational properties can be achieved in
                                         different ways. One approach is by reduction to program veri-          (3) We show that relational properties, such as non-
                                         fication: given a program P and a hyperproperty φ, construct a         interference, can naturally be encoded in trace logic
                                         program Q and a property ψ, such that: (i) Q verifies ψ and (ii)       (Section V).
                                         Q verifies ψ implies P verifies φ. The main advantage of this          (4) We implemented our approach in the R APID tool, which
                                         approach is that (i) can be verified using standard verification       relies on the first-order theorem prover Vampire [10]. We
                                         tools, whereas (ii) is proved generically for the method used          conducted experiments on security-relevant hyperproperties,
                                         for constructing Q, for instance self-composition [4], [5]             such as non-interference and sensitivity. Our results show
                                         and product programs [6], [7]. Another approach to verify              that R APID is more expressive than state-of-the-art non-
                                         relational properties is to use relational Hoare logic [8] or          interference verification tools and that Vampire is better suited
                                         specialized logics that target specific properties [9]. While both     to the verification of security-relevant hyperproperties than
                                         approaches have been applied successfully in several use cases,        state-of-the-art SMT-solvers like Z3 and CVC4.
                                         they suffer from fundamental limitations: (i) they are typically
                                         not efficient enough to scale to large programs and (ii) they                           II. M OTIVATING E XAMPLE
                                         are only partly automated and tailored to specific properties.         We motivate our work with the simple program of Figure 1.
                                         Contributions.In this paper, we develop a new approach                 This program iterates over an integer-valued array a and stores
                                         based on reduction to first-order reasoning, with the intent           in the variable hw the sum of array elements. If a is a bitstring,
                                         of reconciling expressiveness and automation.                          then this program leaks the so-called Hamming weight of a in
                                         (1) We introduce and formally characterize trace logic L, an           the variable hw. Our aim is to prove the following relational
                                         instance of many-sorted first-order logic with equality, which         property over two arbitrary computation traces t1 and t2 of
                                         allows expressing properties over program locations, loop              Figure 1: if the elements of the array variable a in t1 are
                                         iterations, and computation traces (Section IV).                       component-wise equal to the elements of a in t2 except for
two consecutive positions k and k + 1, for some k, and the              we can precisely express the value of each program variable
elements of a in t1 at positions k, k + 1 are swapped versions          at any program execution timepoint, without introducing
of the elements of a in t2 (that is, the k-th element of a in t1        abstractions. For Figure 1, for example, we write hw(end, t1 )
is the (k + 1)-th element of a in t2 and vice-versa), then the          to denote to the value of hw in trace t1 at timepoint end.
program variable hw is the same at the end of t1 and t2 . We
formalize this property as                                              (ii) Trace logic further allows arbitrary quantification over
                                                                       iterations and values of program variables. In particular,
     ∀kI . ∀pos I .((pos 6≃ k ∧ pos 6≃ k + 1) →                         we can express and reason about iterations that depend
     a(pos, t1 ) ≃ a(pos, t2 )) ∧ a(k, t1 ) ≃ a(k + 1, t2)             on (possibly non-ground) expressions involving program
                                                             (1)
     ∧ a(k, t2 ) ≃ a(k + 1, t1 ) ∧ 0 ≤ k + 1 < alength                 variables. We use superposition-based first-order reasoning to
          → hw(end, t1 ) ≃ hw(end, t2 ) ,                               automate static analysis with trace logic and derive first-order
                                                                        properties about loop iterations, possibly with quantifier
where kI and pos I respectively specify that k and pos are              alternations. For Figure 1, we generate for example the
of sort integer I. Further, a(pos, ti ) denotes the value of the        property ∃itN . it < n9 ∧ i(l9 (it), t1 ) ≃ k , where l9 denotes
element at position pos of a in trace ti , whereas end refers to        the location where the loop condition is tested and n9 denotes
the last program location of Figure 1 (that is, line 14).               the first iteration of the loop upon which the loop condition
   Property (1) is challenging to verify, since it requires             does not hold anymore.
theory-specific reasoning over integers and it involves alterna-
tion of quantifiers, as the length of the array a is unbounded          (iii) We guide superposition reasoning in trace logic by using a
and the k-th position (corresponding to the swap) is arbitrary.         set of lemmas statically inferred from the program semantics.
To understand the difficulty in automating such kind of reason-         These lemmas express inductive properties about the program
ing, let us first illustrate how humans would naturally prove           behavior. To illustrate such lemmas, we first introduce the
property (1). First, split the iterations of the loop of Figure 1       following notation. For an arbitrary program variable v, let
into three intervals: (i) The interval from the first iteration of      Eqv (it) denote that v has the same value in both traces
the loop to the iteration where i has value k, (ii) the interval        at iteration it of the loop. For example, for every program
from the iteration where i has value k to the iteration where i         variable v of Figure 1, we introduce the following definition:
has value k + 2, and (iii) the interval from the iteration where                    Eqv (it) := v(l9 (it), t1 ) ≃ v(l9 (it), t2 ).
i has value k + 2 to the last iteration of the loop. Next, for
each of the intervals above, one proves that the equality of            In particular, for variable hw, we introduce:
the value of hw in traces t1 and t2 is preserved; that is, if
                                                                                 Eqhw (it) := hw(l9 (it), t1 ) ≃ hw(l9 (it), t2 ).
hw has the same value in t1 and t2 at the beginning of the
interval, then hw also has the same value in t1 and t2 at the           We then derive the following inductive lemma for each pro-
end of the interval. In particular, for the first and third intervals   gram variable v:
one uses inductive reasoning, to conclude the preservation                            
of the equality across the whole interval from the step-wise                  ∀itBN . Eqv (0) ∧ ∀itN .((it < itB ∧ Eqv (it))
preservation in the interval of the equality of the value hw                                                                 (2)
                                                                                      → Eqv (succ(it))) → Eqv (itB) ,
in traces t1 and t2 . Further, for the second interval, one uses
commutativity of addition to prove that the value of hw in              where itBN and itN denote iterations itB, it and succ(it)
traces t1 and t2 is preserved. By combining that the values             denotes the successor of it. Lemma (2) asserts that if v has
of hw in traces t1 and t2 are preserved in each of the three            the same value in traces t1 and t2 at the beginning of the loop
intervals, one finally concludes that property (1) is valid.            (that is, at iteration 0) and if the values of v are step-wise
   While the above proof might be natural for humans, it is             equal in traces t1 and t2 up to an arbitrary iteration itB, then
challenging for automated reasoners for the following reasons:          the values of v are equal in traces t1 and t2 at iteration itB
(i) one needs to express and relate different iterations in the         (and hence the values of v are preserved in t1 and t2 for the
execution of the loop in Figure 1 and use these iterations              entire interval up to itB). For Figure 1, we generate lemma (2)
to split the reasoning about loop intervals; (ii) one needs to          for hw as:
automatically synthesize the loop intervals whose boundaries                         
depend on values of program variables; and (iii) one needs to                ∀itBN . Eqhw (0) ∧ ∀itN .((it < itB ∧ Eqhw (it))
                                                                                                                                      (3)
combine theory-specific reasoning with induction for proving                                                              
                                                                                     → Eqhw (succ(it))) → Eqhw (itB) .
quantified properties, possibly with alternations of quantifiers.
In our work we address these challenges: we introduce trace             Note that lemma (2), and in particular lemma (3) for hw, is
logic, allowing us to express and automatically prove relational        crucial for proving that the values of hw in traces t1 and t2
properties, including property (1). The key advantages of trace         are the same up to iteration k, as considered in the relational
logic are as follows.                                                   property of (1). With this lemma at hand, we automatically
(i) In trace logic, program variables are encoded as unary and          prove property (1) of Figure 1, using superposition reasoning
binary functions over program execution timepoints. This way,           in trace logic.
                       III. P RELIMINARIES                           A. Locations and Timepoints
  This section fixes our terminology and programming model.
                                                                        We consider a program in W as a set of locations, where
A. First-order logic                                                 each location intuitively corresponds to a point in the program
                                                                     at which an interpreter can stop. That is, for each program
   We consider standard many-sorted first-order logic with
                                                                     statement s, we introduce a program location ls . We denote
equality, where equality is denoted by ≃ . We allow all
                                                                     by lend the location corresponding to the end of the program.
standard boolean connectives and quantifiers in the language
and write s 6≃ t instead of ¬(s ≃ t), for two arbitrary first-          As program locations can be revisited during program
order terms s and t. A signature is any finite set of symbols.       executions, for example due to the presence of loops, we model
We consider equality ≃ as part of the language; hence, ≃             locations as follows. For each location ls corresponding to a
is not a symbol. We write F1 , . . . , Fn  F to denote that the     program statement s, we introduce a function symbol ls with
formula F1 ∧ . . . ∧ Fn → F is a tautology. In particular, we        target sort L in our language, denoting the timepoint where the
write  F , if F is valid.                                           interpreter visits the location. For each enclosing loop of the
   By a first-order theory, or simply just theory, we mean the       statement s, the function symbol ls has an argument of type
set of all formulas valid on a class of first-order structures.      N; this way, we distinguish between different iterations of the
When we discuss a theory, we call symbols occurring in the           enclosing loop of s. We denote the set of all such function-
signature of the theory interpreted, and all other symbols           symbols ls as SigT p . When s is a loop, we additionally
uninterpreted. In our work, we consider the combination              include a function symbol ns with target sort N and an
(union) N ∪ I of the theory N of natural numbers and the one I       argument of sort N for each enclosing loop of s. This way, ns
of integers. The signature of N consists of standard symbols 0,      denotes the iteration in which s terminates for given iterations
succ, pred and <, respectively interpreted as zero, successor,       of the enclosing loops of s. We denote the set of all such
predecessor and less. Note that N does not contain interpreted       function symbols ns as Sign .
symbols for (arbitrary) addition and multiplication. We use
the theory N to represent and reason about loop iterations              Example 1: Consider Figure 1. We abbreviate each state-
(see Section IV). The signature of I consists of the standard        ment s by the line number of the first line of s. We use l6 to
integer constants 0, 1, 2, . . . and integer operators +, ∗ and <.   refer to the timepoint corresponding to the first assignment
We use the theory I to represent and reason about integer-           of i in the program. We denote by l9 (0) and l9 (n9 ) the
valued program variables (see Section IV). Additionally we           timepoints corresponding to evaluating the loop condition in
use two (uninterpreted) sorts as two sets of uninterpreted           the first and, respectively, last loop iteration. Further, we write
symbols: (i) the sort Timepoint, written as L, for denoting          l11 (it) and l11 (succ(0)) for the timepoint corresponding to
(unique) timepoints in the execution of the program and (ii)         the beginning of the loop body in the it-th and, respectively,
the sort Trace, written as T, for denoting computation traces        second iteration of the loop. Note that succ(0) is a term
of a program.                                                        algebra expression of N.                                         
   Given a logical variable x and sort S, we write xS to
denote that the sort of x is S. We use standard first-order             For simplicity, let us define terms over the most commonly
interpretations/models modulo a theory T , for example modulo        used timepoints. First, define its to be a function, which
N ∪ I. We write T F to denote that F holds in all models of         returns for each while-statement s a unique variable of sort N.
T (and hence valid). If I is a model of T , we write I T F          Second, let s be a statement, let w1 , . . . , wk be the enclosing
if F holds in the interpretation I.                                  loops of s and let it be an arbitrary term of sort N.

B. Programming Model W                                                   tps := ls (itw1 , . . . , itwk )        if s is not while-statement
   We consider programs written in a standard while-like             tps (it) := ls (itw1 , . . . , itwk , it)   if s is while-statement
programming language, denoted as W, with mutable and
                                                                     lastIt s := ns (itw1 , . . . , itwk )       if s is while-statement
constant integer- and integer-array-variables. The language W
includes standard side-effect free expressions over booleans
and integers. Each program in W consists of a single top-level       Third, let s be an arbitrary statement. We refer to the timepoint
function main, with arbitrary nestings of if-then-else and           where the execution of s has started (parameterized by the
while-statements. For simplicity, whenever we refer to loops,        enclosing iterators) by
we mean while-loops. For each statement s, we refer to while-
statements in which s is nested in as enclosing loops of s.                                  (
                                                                                                 tps (0)     if s is while-statement
The semantics of W is formalized in Section IV-C.                              start s :=
                                                                                                 tps         otherwise
                       IV. T RACE L OGIC
  We now introduce the concept of trace logic for expressing         Fourth, for an arbitrary statement s, let end s denote the time-
both the semantics and (relational) properties of W-programs.        point which follows immediately after s has been evaluated
completely (including the evaluation of substatements of s):           C. Semantics of W
                                                                          We now describe the semantics of W expressed in our
        
        start s
                ′         if s′ occurs after s in a context
                                                                       trace logic L. To do so, we state trace axioms of L capturing
        
        end s′            if s is last st. in if-branch of s′
        
        
                                                                       the behavior of possible program computation traces and then
        
end s := end s′            if s is last st. in else-branch of s′       define L.
        tp w (succ(it )) if s is last st. in body of w
                      w
                                                                          In what follows, we consider an arbitrary but fixed program
        
        
        
                           otherwise                                   P in W, and give all definitions relative to P . Note that our
        
        l
           end
                                                                       semantics defines arbitrary executions, which are modeled by
B. Program Variables and Expressions                                   a free variable tr of sort T.
   In our setting, we reason about program behavior by ex-                   a) Main-function: Let s1 , . . . , sk be statements and P
pressing properties over program variables v. To do so, we             be a program with top-level function func main {s1 ; . . . ;s
capture the value of program variables v at timepoints (from           k }. The semantics of P is defined by the conjunction of the

L) in arbitary program execution traces (from T). Hence, we            semantics of the statements si in the top-level function and
model program variables v as functions v : (L × T) 7→ I,               is the same for each trace. That is:
where v(tp, tr) gives the value of v at timepoint tp, in trace                                           k
                                                                                                         ^
tr. If the program variable v is an array, we add an additional                                JP K :=         Jsi K.                  (6)
argument of sort I, which corresponds to the position at which                                           i=1
the array is accessed. We denote by SV the set of such
                                                                          The semantics of P is then defined by structural induction,
introduced function symbols denoting program variables. We
                                                                       by asserting trace axioms for each program statement s, as
finally model arithmetic constants and program expressions
                                                                       follows.
using integer functions.
                                                                            b) Skip: Let s be a statement skip. The evaluation of s
   Note that our setting can be simplified for (i) non-mutable
                                                                       has no effect on the value of the program variables. Hence:
variables – in this case we omit the timepoint argument in the
function representation of the variable; (ii) for non-relational
                                                                                               ^
                                                                                       JsK :=       Eq(v, end s , tps )           (7)
properties about programs – in this case, we only focus on                                      v∈SV
one computation trace and hence the trace argument in the
function from SV can be omitted.                                            c) Integer assignments: Let s be an assignment v = e,
   Example 2: Consider again Figure 1. By i(l6 , tr) we refer to       where v is an integer program variable and e is an expression.
the value of program variable i in trace tr at the moment be-          We reason as follows. The assignment s is evaluated in one
fore i is first assigned. We use alength(tr) to refer to the value     step. After the evaluation of s, the variable v has the same
of variable alength in trace tr. As a is unchanged in the              value as e before the evaluation, and all other variables remain
program, we write a(i(l11 (it), tr), tr) for the value of array a      unchanged. Hence:
in trace tr at position pos, where pos is the value of i in trace                                           ^
                                                                         JsK := v(end s ) ≃ JeK(tps , tr) ∧     Eq(v ′ , end s , tps ) (8)
tr at timepoint l11 (it). In case a would have changed during
                                                                                                          v ′ ∈SV \{v}
the loop, we would have written a(l11 (it), i(l11 (it), tr), tr)
instead. We denote by i(l12 (it), tr) + 1 the value of the                   d) Array assignments: Let s be an assignment a[e1 ] =
expression i+1 in trace tr at timepoint l12 (it).                      e2 , where a is an array variable and e1 , e2 are expressions.
   Consider now an arbitrary program expression e. We write            We consider that the assignment is evaluated in one step. After
JeK(tp, tr) to denote the value of e at timepoint tp, in trace         the evaluation of s, the array a has the same value as before
tr. With these notations at hand, we introduce two definitions         the evaluation, except for the position pos corresponding to
expressing properties about values of expressions e at arbitrary       the value of e1 before the evaluation, where the array now
timepoints and traces. Consider now v ∈ SV , that is a function        has the value of e2 before the evaluation. All other program
denoting a program variable v, and let tp1 , tp2 denote two            variables remain unchanged and we have:
timepoints. We define: Eq(v, tp1 , tp2 ) :=
                                                                            JsK :=         ∀pos I .(pos 6≃ e1 (tps , tr) →
  (
     ∀pos I . v(tp1 , pos, tr) ≃ v(tp2 , pos, tr), if v is array                           a(end s , pos, tr) ≃ a(tps , pos, tr))     (9a)
                                                                 (4)
                   v(tp1 , tr) ≃ v(tp2 , tr),      otherwise                        ∧      a(end s , e1 (tps , tr)) ≃ e2 (tps , tr)   (9b)
                                                                                              ^
That is, Eq(v, tp1 , tp2 ) in (4) states that the program variable                  ∧                 Eq(v, end s , tps )             (9c)
                                                                                            v∈SV \{a}
v has the same values at tp1 and tp2 . We also define:
                                   ^                                         e) Conditional if-then-else Statements: Let s be the
           EqAll(tp1 , tp2 ) :=        Eq(v, tp1 , tp2 ),      (5)
                                                                       statement: if(Cond){s1 ; . . . ;sk } else {s1 ‘; . . . ;sk‘ ‘}. The
                                v∈SV
                                                                       semantics of s is defined by the following two properties:
asserting that all program variables have the same values at           (i) entering the if-branch and/or entering the else-branch does
the two timepoints tp1 and tp2 .                                       not change the values of the variables, (ii) the evaluation in the
branches proceeds according to the semantics of the statements              Theorem 1 (W-Soundness of Semantics of W): For a given
in each of the branches. Thus:                                           terminating program p, the trace axioms (7)-(11) are W-sound.
                                                                            As a consequence, the semantics of any terminating program
   JsK :=         JCondK(tps ) → EqAll (start s1 , tps )       (10a)     p expressed in L, as defined in (6), is W-sound.
            ∧    ¬JCondK(tps ) → EqAll (start ′s1 , tps )      (10b)
                                                                         E. Program Correctness in Trace Logic L
            ∧     JCondK(tps ) → Js1 K ∧ · · · ∧ Jsk K         (10c)
                                                                           Let P be a program and F be a first-order property of P ,
            ∧    ¬JCondK(tps ) → Js1 ′ K ∧ · · · ∧ Jsk′ ′ K    (10d)
                                                                         with F expressed in L. We use L to express and prove that P
    f) While-Loops: Let s be the while-statement while(                  “satisfies” F , that is P is partially correct w.r.t. F , as follows:
Cond){s1 ; . . . ;sk }.We refer to Cond as the loop condition.             1) We express JP K in L, as discussed in Section IV-C;
We use the following four properties to defined the semantics              2) We prove the partial correctness of P with respect to F ;
of s: (i) the iteration lastIt s is the first iteration where the loop          that is, we prove
condition does not hold, (ii) entering the loop body does not
change the values of the variables, (iii) the evaluation in the                                        JP K N∪I F.
body proceeds according to the semantics of the statements                 In what follows, we first discuss (relational) properties F
in the body, (iv) the values of the variables at the end of              expressed in L (Section V) and then focus on proving partial
evaluating s are the same as the variable values at the loop             correctness using L (Section VI).
condition location in iteration lastIt(s). We then have:
   JsK :=                                                                           V. H YPERPROPERTIES IN T RACE L OGIC
                                                                            We demonstrate the expressiveness of trace logic L by
    ∀itsN . (its < lastIt s → JCondK(tps (its )))              (11a)
                                                                         encoding non-interference [11] and sensitivity [12], two fun-
  ∧ ¬JCondK(tp(lastIt s ))                                     (11b)     damental security properties. This secition also showcases the
  ∧ ∀itsN . (its < lastIt s → EqAll (start s1 , tps (its )) (11c)        generic lemmas, similar to property (2), introduced by our
  ∧ ∀itsN . (its < lastIt s → (Js1 K ∧ · · · ∧ Jsk K)       (11d)        work to automate the verification of hyperproperties. The
                                                                         examples considered in this section are deemed as insecure
  ∧ EqAll (end s , tps (lastIt s ))                             (11e)
                                                                         by existing syntax-driven, non-interference verification tech-
D. Trace Logic L                                                         niques, such as [11], [13].
   We now have all ingredients to define our trace logic L,                   a) Non-interference: Non-interference [1] is a security
allowing us to reason about both relational and non-relational           property that prevents information flow from confidential data
properties of programs.                                                  to public channels. It is a so-called 2-safety property express-
   Let ST r be a set {t1 , t2 , . . . } of nullary function symbols      ing that, given two runs of a program containing high and low
                                                                         confidentiality variables, denoted by H and L respectively, if
of sort T. Intuitively, these symbols denote traces and allow us
                                                                         the input for all L variables is the same in both runs, the
to express relational properties. The signature of L contains
the symbols of the theories N and I together with symbols                output of the computation should result in the same values for
                                                                         L variables in both traces regardless of the initial value of any
introduced in Section IV-A-IV-B, that is symbols denoting
timepoints, last iterations in loops, program variables and              H variable. Intuitively, this means that no private input leaks
traces. Formally,                                                        to any public sink. In what follows, we let lo denote an L
                                                                         variable and hi an H variable.
    Sig(L) := (SN ∪ SI ) ∪ (ST p ∪ Sn ∪ SV ∪ ST r ).                        We formalize non-interference in trace logic L as follows.
                                                                         Let l0 denote the first timepoint of the execution and let
   Recall that the semantics of W is defined by the trace                EqTr (v, tp) denote that v has the same value(s) in both traces
axioms (7)-(11). By extending standard small-step operational            at timepoint tp, that is:
semantics with timepoints and traces, we obtain the small-step              EqTr (v, tp) :=
semantics of W. For proving soundness, of this semantics,
                                                                            ∀posI .v(tp, pos, t1 ) ≃ v(tp, pos, t2 )) if v is mutable array
                                                                          
we rely on so-called execution-interpretation of a program                
                                                                          
execution E: such an interpretation is a model in which for                                                           if v is constant array
                                                                          
                                                                          ∀pos .v(pos, t ) ≃ v(pos, t ))
                                                                                  I         1            2
every (array) variable v the term v(tpi ) resp. v(tpi , pos)               v(tp, t1 ) ≃ v(tp, t2 ))                  if v is mutable var.
is interpreted as the value of v at the execution step in
                                                                          
                                                                          
                                                                            v(t1 ) ≃ v(t2 )                           if v is constant var.
                                                                          
E corresponding to timepoint tpi – see our Appendix for
more details. We then introduce W-soundness defining the                 We then express non-interference as:
soundness of the semantics of W, as follows:                                        ^                    ^
   Definition 1 (W-Soundness): Let p be a program and let A                       (   EqTr (v, l0 )) → (    EqTr (v, lend )).            (12)
be a trace logic property. We say that A is W-sound, if for                         v∈L                     v∈L

any execution-interpretation M we have M  A.                              Example 3: Consider the program illustrated in Figure 2a,
   By using structural induction over program statements, we             which branches on an H guard. In the two branches, however,
derive W-soundness of the semantics of W. That is:                       the L variable is updated in the same way, thereby not leaking
   1     func main()                                                 1   func main()
   2     {                                                           2   {
   3         const Int hi;                                           3      const Int[] a;
   4         Int lo;                                                 4      const Int alength;
   5                                                                 5      const Int z;
   6          if(hi > 0)                                             6      Int x = 0;
   7          {                                                      7      Int i = 0;
   8               lo = lo + 1;                                      8
   9          }                                                      9        while(i < alength)
  10          else                                                  10        {
  11          {                                                     11             x = x + a[i];
  12               lo = lo + 1;                                     12            i = i + 1;
  13          }                                                     13        }
  14     }                                                          14        x = x + z;
                                                                    15   }
                (a) Branching on a high variable.
   1     func main()
                                                                                 Fig. 3: Example adhering sensitivity
   2     {
   3         const Int k;                                           Figure 2b. proving it to be secure. Specifically, we prove the
   4         const Int lo;                                          following property, stating that if all variables in L are equal at
   5         Int hi = lo;
   6         Int i = 0;                                             the beginning of the execution, then the values of the output
   7         Int[] output;                                          array are equal after the execution:
   8
   9          while(hi < k)                                            (EqTr (k, l11 ) ∧ EqTr (lo, l11 ) ∧ EqTr (output , l11 ))
  10          {                                                                                                                     (14)
                                                                        → EqTr (output, lend )
  11               output[i] = hi;
                                                                                                                                       
  12               hi = hi + 1;
  13               i = i + 1;                                            b) Sensitivity: Sensitivity is a property describing how
  14          }                                                     much a program amplifies the distance of its inputs, which is at
  15     }                                                          the core of the Laplace mechanism used to enforce differential
                                                                    privacy [12]. Let the integer k denote the deviation, and let
                        (b) Explicit flow.
                                                                    OU T be the set of program variables that appear in the output
       Fig. 2: Examples with non-interference behaviour.            after the execution of the program. We can then formally
                                                                    define sensitivity as follows:
anything about the guard. The non-interference property for
this program is a special instance of property (12), as follows:                ∀kI , v∈OUT . |v(l0 , t1 ) − v(l0 , t2)| < k
                                                                                                                                    (15)
                                                                                → |v(lend , t1 ) − v(lend , t2 )| < k
                EqTr (lo, l0 ) → EqTr (lo, lend ).          (13)
                                                                       Example 5: In Figure 3, the contents of an array a are
   By adjusting superposition reasoning to trace logic L (see       summed up into a variable x. We prove that if the values of
Section VI), we can automatically verify the property above.        some variable z differ by at most k between two traces while
Traditional information-flow type systems [11] would however        all other array elements are equal, then the final values of x
fail to prove this program secure, as they prevent any branch-      in these two traces will differ from each other by at most k
ing on H guards. More permissive static analysis techniques         as well. We express this property in trace logic L as:
based on program dependency graphs, such as J OANA [13],
would also classify this program as insecure.                       ∀kI . EqT (a, l6 ) ∧ EqT (alength,     l6) ∧ |z(t1 ) − z(t2 )| < k
   Let us now focus on another interesting security example.         → |x(lend , t1 ) − x(lend , t2 )| < k
   Example 4: Figure 2b models an interactive program out-                                                                           (16)
putting on a public channel. The array variable output ∈ L                                                                             
models the number and content of these outputs, which is               Our framework generates and relies upon a set of generic
determined by the loop. At a first glance, this program might       trace lemmas for hyperproperties, similar to lemma (2). We
look insecure because of the explicit flow at l11 . Furthermore,    now illustrate two further such lemmas.
the number of outputs, as well as their content, could also               c) Simultaneous-loop-termination: Our semantic formal-
leak information about the secret. Indeed, value-insensitive        ization of W in trace logic L defines ns (t1 ) to be the smallest
information-flow type systems [11] would consider this pro-         iteration, in which the loop condition does not hold in trace t1 .
gram to be insecure. In this specific case, however, the H          Due to well-founded orderings over naturals, there can only be
variable in the loop guard is reset with an L input, and the        one iteration with such a property. Thus, if we can conclude
program satisfies non-interference. As our semantic reasoning       this property for any other trace, say t2 , then it must be the
in trace logic L is value sensitive, our work correctly validates   case that ns (t2 ) ≃ ns (t1 ). In our work we therefore generate
and use the following trace lemma in L (for simplicity, we                     b) Theory Reasoning: Reasoning with theories in the
omit the enclosing iterators):                                            presence of quantifiers is yet another challenge for automated
                                                                          reasoners, and hence for VAMPIRE. Different theory encodings
                                                                          lead to very different results. In R APID, we model integers
                                                
        ∀it. it < ns (t1 ) → JCondK(ls (it), t2 ) ∧
                                                                  (17)   using the built-in support for integers in VAMPIRE. We exper-
       ¬JCondK(ls (ns (t1 )), t2 ) → ns (t2 ) ≃ ns (t1 )                  imented with various sound but incomplete axiomatization of
Property (17) is essential to prove that the loops in both traces         integers. We used VAMPIRE with all its built-in theory axioms
have the same last iteration, and therefore terminate after the           (option -tha on, default), as well as with a partial, but most
same number of iterations.                                                relevant set of theory axioms (option -tha some) which we
     d) Equality-preservation-arrays: For an array variable a             extended with specific integer theory axioms. Natural numbers
and loop location l, let Eqa (it, pos) denote that a at position          are modeled in R APID as a term algebra (0, succ, pred), for
pos has the same value in both traces at iteration it of the loop:        which efficient reasoning engines already exist [15]. In order
                                                                          to express the ordering of natural numbers, we manually add
       Eqa (it, pos) := a(l(it), pos, t1 ) ≃ a(l(it), pos, t2 ).          the symbol <, together with an (incomplete) axiomatization. In
The following lemma over array variables is similar to the                R APID, we also experimented with clause splitting by calling
equality-preservation-lemma (2):                                          VAMPIRE both with and without its AVATAR framework [16]
              ′                                                           (options -av on/off, with on as default).
    ∀pos
       I .∀itN .
         Eqa (0, pos) ∧ ∀itN .((it < it′ ∧ Eqa (it, pos))          (18)   B. Benchmarks and Experimental Results
                                                                             To compensate the lack of general benchmarks for first-
                                                        
            → Eqa (succ(it), pos)) → Eqa (it′ , pos)
                                    
                                                                          order hyperproperties, we collected a set of 27 verification
  We conclude by emphasizing that trace lemmas, such as (17)              problems for evaluating our work in R APID. Our benchmarks
and (18), are expressed in trace logic L and automatically                describe 2-safety properties relevant in the security domain,
generated by our approach.                                                such as non-interference and sensitivity. The individual bench-
         VI. I MPLEMENTATION AND E XPERIMENTS                             mark programs consist of up to 50 lines of code each.
A. Implementation                                                            R APID produced the SMT- LIB-encodings for each bench-
                                                                          mark in less than a second. These encodings were passed
   We implemented our approach in the tool R APID1 , which
                                                                          to VAMPIRE, as well as to the SMT solvers Z3 [17] and
consists of nearly 13,000 lines of C++ code. R APID takes as
                                                                          CVC4 [18] for comparison purposes, to establish the cor-
input a program written in W and a property expressed in
                                                                          rectness of the input property. We ran each prover with a 60
trace logic L. It then generates axioms written in trace logic
                                                                          seconds time limit. All experiments were carried out on an
L corresponding to the semantics of the program and outputs
                                                                          Intel Core i5 3.1Ghz machine with 16 GB of RAM.
both the axioms and the property in the SMT- LIB syntax [14].
                                                                             Our experimental results are summarized in Table I. The
The produced SMT- LIB encoding is further passed within
                                                                          first four columns report on results by running VAMPIRE
R APID to the first-order theorem prover VAMPIRE for proving
                                                                          on the R APID output. The columns denoted with S/F refer
validity of the property (i.e. partial correctness). VAMPIRE
                                                                          to VAMPIRE options for partial/full theory reasoning (option
searches for a refutation of the desired property by saturating
                                                                          -tha some/on) respectively. A refers to the use of the
the provided encoding with respect to a set of inference rules
                                                                          AVATAR (option -av on) in conjunction with one of the
such as resolution and superposition [10].
                                                                          theory options, hence columns S+A and F+A. The last two
      a) Inductive Reasoning: Trace logic L encodes loop-
                                                                          columns of Table I summarize our results of running Z3
iterations using counters of sort N. Hence, there are conse-
                                                                          and CVC4 on the R APID output. The rows denoted To-
quences of the semantics which can only be derived using
                                                                          tal VAMPIRE and Unique VAMPIRE sum up the total and
inductive reasoning. Automating induction is however chal-
                                                                          unique numbers of examples proven with the setting of the
lenging: state-of-the-art SMT solvers and theorem-provers are
                                                                          corresponding column. Example 4-hw-swap-in-array
not able to automatically infer and prove most (inductive)
                                                                          in Table I is our running example from Figure 1, whereas
consequences needed by R APID. In order to address this
                                                                          the benchmarks 3-ni-high-guard-equal-branches
problem, (i) we identified some of the most important ap-
                                                                          and 9-ni-equal-output correspond to Figure 2a and
plications of induction that are useful for many programs and
                                                                          Figure 2b, respectively.
(ii) formulated the corresponding inductive properties in trace
                                                                             VAMPIRE proved 25 R APID encodings out of the 27 bench-
logic as trace lemmas. Some of these lemmas are described
                                                                          mark problems. Table I shows that the option S+A seems to
in Section II and Section V. Each trace lemma is logically
                                                                          be the most successful, with four unique benchmarks proven.
implied by standard induction axioms of natural numbers and
                                                                          While two of our benchmarks were not proven by VAMPIRE
the semantics of the program. R APID generates trace lemmas
                                                                          with our current set of automatically generated R APID lemmas,
for each variable and each loop of the program and adds them
                                                                          these problems could actually be proved by VAMPIRE by using
as axioms to its SMT- LIB output.
                                                                          only a subset of trace lemmas, i.e. by removing unnecessary
  1 https://github.com/gleiss/rapid                                       lemmas manually. Improving theory reasoning in VAMPIRE,
                                          Vampire
            Benchmarks
                                       S S+A F F+A
                                                      CVC4   Z3    in full first-order logic, such as over unbounded arrays, existing
            1-hw-equal-arrays          X  X     - X    X     X     methods are yet not able to automatically verify program
      2-hw-last-position-swapped        - X     - -    X     X     correctness. We argue that the missing expressiveness is the
       3-hw-swap-and-two-arrays         - X     - -    -     -
                                                                   problem here, since one usually needs to be able to express
       4-hw-swap-in-array-lemma         - X     - -    -     -
         4-hw-swap-in-array-full        - X     - -    -     -     arbitrary dependencies of timepoints and values, if custom
            1-ni-assign-to-high        X  X     X X    X     X     code is used to iterate through an array or more generally
       2-ni-branch-on-high-twice       X  X     X X    X     X     through a data structure. Our trace logic supports such kind
    3-ni-high-guard-equal-branches     X  X     X X    X     X
   4-ni-branch-on-high-twice-prop2     X  X     - -    X     X
                                                                   of first-order reasoning.
           5-ni-temp-impl-flow          -  -    X X    X     X        Our approach to automate induction using trace lemmas is
      6-ni-branch-assign-equal-val      -  -    X X    X     X     related to template-based invariant generation methods [22],
             7-ni-explicit-flow        X  X     X X    X     X     [23]. Our trace lemmas are however more expressive than
         8-ni-explicit-flow-while      X  X     - X    X     X
             9-ni-equal-output         X   -    - -    -     X     existing templates and we automatically derive trace lemmas.
         10-ni-rsa-exponentiation      X  X     X X    X     -        Program analysis by first-order reasoning is also studied
            1-sens-equal-sums          X  X     X X    X     X     in [24], where program semantics is expressed in extensions
     2-sens-equal-sums-two-arrays      X  X     X X    -     -
          3-sens-abs-diff-up-to-k       -  -    - -    X     X
                                                                   of Hoare Logic with explicit timepoints. Unlike [24], we do
  4-sens-abs-diff-up-to-k-two-arrays    -  -    - -    -     -     not rely on an intermediate program (Hoare) logic, but reason
        5-sens-two-arrays-equal-k      X  X     X X    -     -     also about relational properties. While [24] can only handle
       6-sens-diff-up-to-explicit-k    X  X     X X    -     -     simple loops, our work supports a standard while-language
   7-sens-diff-up-to-explicit-k-sum     -  -    X X    -     -
           8-sens-explicit-swap         -  -    X X    -     -     with explicit locations and arbitrary nestings of statements.
       9-sens-explicit-swap-prop2       -       X X    -     -        First-order reasoning for program analysus is also addressed
              10-sens-equal-k          X  X     X X    -     -     in [25], by introducing dynamic trace logic: an extension of
          11-sens-equal-k-twice        X  X     X X    -     -     dynamic logic with modalities for reasoning about traces. A
       12-sens-diff-up-to-forall-k      -  -    X X    X     -
              Total VAMPIRE            15 18 17 19                 custom sequent calculus is proposed in [25], implying that
            Unique VAMPIRE             1   4    0 0                automating the work would require the design of specialised
                   Total                     25        14    13    sequent calculus provers. Unlike [25], our work is fully auto-
  TABLE I: R APID results with VAMPIRE, Z3 and CVC4.               mated. Further, our work preserves the control-flow structure
                                                                   of programs by introducing function symbols and automates
and in general in superposition proving, would further im-         inductive reasoning using trace lemmas.
prove the efficiency of R APID. In particular, designing better    Relational verification. Verification of relational- and hyper-
reasoning support for transitive relations like <N and <I is an    properties is an active area of research, with applications in
interesting further line of research.                              programming languages and compilers, security and privacy;
   We also compared the performance of VAMPIRE on the              see [26] for an overview. Various static analysis techniques
R APID examples to the performance of Z3 and CVC4. Unlike          have been proposed to analyze non-interference, such as
VAMPIRE, Z3 and CVC4 proved only 13 and 14 examples,               type systems [11] and graph dependency analysis [13]. Type
respectively. Our results thus showcase that superposition         systems proved also effective in the verification of privacy
reasoning, in particular VAMPIRE, is better suited for proving     properties for cryptographic protocols [27]–[31]. Relational
first-order hyperproperties, as many of these properties involve   Hoare logic was introduced in [8] and further extended in [6],
heavy use of quantifiers, including alternations of quantifiers    [32] for defining product programs to reduce relational verifi-
(such as for example 4-hw-swap-in-array correspond-                cation to standard verification. All these works closely tie ver-
ing to Figure 1). Moreover, R APID proved security of exam-        ification to the syntactic program structure, thus limiting their
ples that were classified insecure by existing techniques [11],    applicability and expressiveness. As already argued, our work
[13], such as 3-ni-high-guard-equal-branches and                   allows proving security of examples that were so far classified
9-ni-equal-output.                                                 as insecure by some of the aforementioned methods [11], [13].
                                                                   Recently, [33] encodes relational properties through refinement
                       VII. R ELATED W ORK                         types in F* [34]. While still being syntax driven, [33] can
Deductive verification. Most verification approaches use a         potentially verify semantic properties by using SMT solving,
state-based language to express programs and properties about      although this typically requires the manual insertion and proof
them, and use invariants to establish program correctness [19].    of program-dependent lemmas, which is not the case for us.
Such invariants loosely correspond to a fragment of trace             In [35] bounded model checking is proposed for program
logic, where formulas only feature universal quantification        equivalence. Program equivalence is reduced in [36] to proving
over time – but no existential quantification. The lack of         a set of Horn clauses, by combining a relational weakest
existential, and thus alternating, quantification makes these      precondition calculus with SMT-based reasoning. However,
works suitable for automation via SMT-solving [20], [21] and       when addressing programs with different control flow as
hence applicable for programs where full first-order logic is      in [36], user guidance is required for proving program equiv-
not needed, for instance programs involving mainly integer         alence. Program equivalence is also studied in [37], [38] for
variables and function calls. For program properties expressed     proving information flow properties. Unlike these works, we
are not limited to SMT solving but automate the verification                   [5] Á. Darvas, R. Hähnle, and D. Sands, “A Theorem Proving Approach to
of relational properties expressed in full first-order theories,                   Analysis of Secure Information Flow,” in SPC, 2005, pp. 193–209.
                                                                               [6] G. Barthe, J. M. Crespo, and C. Kunz, “Relational Verification Using
possibly with alternations of quantifiers.                                         Product Programs,” in FM, 2011, pp. 200–214.
   Motivated by applications to translation validation, the work               [7] B. Churchill, O. Padon, R. Sharma, and A. Aiken, “Semantic Program
of [39] develops powerful techniques for proving correctness                       Alignment for Equivalence Checking,” in PLDI, 2019, pp. 1027–1040.
                                                                               [8] N. Benton, “Simple Relational Correctness Proofs for Static Analyses
of loop transformations. Relational methods for reasoning                          and Program Transformations,” in POPL, 2004, pp. 14–25.
about program versions and semantic differences are also                       [9] T. Amtoft, S. Bandhakavi, and A. Banerjee, “A Logic for Information
introduced in [40], [41]. Going beyond relational properties,                      Flow in Object-Oriented Programs,” in POPL, 2006, pp. 91–102.
                                                                              [10] L. Kovács and A. Voronkov, “First-Order Theorem Proving and Vam-
an SMT-based framework for verifying k-safety properties                           pire,” in CAV, 2013, pp. 1–35.
is introduced in [42] and further extended [43] for proving                   [11] A. Sabelfeld and A. C. Myers, “Language-Based Information-Flow
correctness of 3-way merge. While these works focus on high-                       Security,” IEEE J. on Selected Areas in Communications, vol. 21, no. 1,
level languages, many others consider low-level languages,                         pp. 5–19, 2003.
                                                                              [12] C. Dwork, F. McSherry, K. Nissim, and A. Smith, “Calibrating Noise
see [44]–[47] for some exemplary approaches. Further afield,                       to Sensitivity in Private Data Analysis,” in Theory of Cryptography
several authors have introduced logics for modelling hyper-                        Conference, 2006, pp. 265–284.
properties. Unlike these works, trace logic allows expressing                 [13] J. Graf, M. Hecker, and M. Mohr, “Using Joana for Information Flow
                                                                                   Control in Java Programs – A Practical Guide,” Software Engineering
first-order relational properties and automates reasoning about                    2013 – Workshopband, 2013.
such properties by first-order theorem proving, overcoming                    [14] C. Barrett, P. Fontaine, and C. Tinelli, “The SMT-LIB Standard: Version
thus the SMT-based limitations of quantified reasoning.                            2.6,” Department of Computer Science, The University of Iowa, Tech.
                                                                                   Rep., 2017, available at www.SMT-LIB.org.
   Finally, in [48] HyperLTL and HyperCTL∗ is introduced to                   [15] L. Kovács, S. Robillard, and A. Voronkov, “Coming to Terms with
model temporal and relational properties properties. However,                      Quantified Reasoning,” in POPL, 2017, pp. 260–270.
these logics support only decidable fragments of first-order                  [16] A. Voronkov, “AVATAR: The Architecture for First-Order Theorem
                                                                                   Provers,” in CAV, 2014, pp. 696–710.
logic and thus cannot handle relational properties with non-                  [17] L. De Moura and N. Bjørner, “Z3: An Efficient SMT Solver,” in TACAS,
constant function symbols. As such, security and privacy prop-                     2008, pp. 337–340.
erties over unbounded data structures/uninterpreted functions                 [18] C. Barrett, C. L. Conway, M. Deters, L. Hadarean, D. Jovanović, T. King,
cannot be encoded or verified.                                                     A. Reynolds, and C. Tinelli, “CVC4,” in CAV, 2011, pp. 171–177.
                                                                              [19] N. Bjørner, A. Gurfinkel, K. McMillan, and A. Rybalchenko, “Horn
                                                                                   Clause Solvers for Program Verification,” in Fields of Logic and Com-
                        VIII. C ONCLUSION                                          putation II, 2015, pp. 24–51.
   We introduced trace logic for automating the verification                  [20] K. Hoder and N. Bjørner, “Generalized Property Directed Reachability,”
                                                                                   in SAT, 2012, pp. 157–171.
of relational program properties of imperative programs. We                   [21] A. Gurfinkel, S. Shoham, and Y. Meshman, “SMT-based Verification of
showed that program semantics as well as relational properties                     Parameterized Systems,” in FSE, 2016, pp. 338–348.
can naturally be encoded in trace logic as first-order properties             [22] M. A. Colón, S. Sankaranarayanan, and H. B. Sipma, “Linear Invariant
                                                                                   Generation Using Non-Linear Constraint Solving,” in CAV, 2003, pp.
over program locations, loop iterations and computation traces.                    420–432.
We combined trace logic with superposition proving and                        [23] A. Gupta and A. Rybalchenko, “InvGen: An Efficient Invariant Gener-
implemented our work in the R APID tool. While our work                            ator,” in CAV, 2009, pp. 634–640.
already outperforms SMT-based approaches, we are convinced                    [24] B. Gleiss, L. Kovács, and S. Robillard, “Loop Analysis by Quantification
                                                                                   over Iterations,” in LPAR, 2018, pp. 381–399.
that improving superposition reasoning with both theories and                 [25] B. Beckert and S. Schlager, “A Sequent Calculus for First-Order
quantifiers would further strengthen the use of trace logic for                    Dynamic Logic with Trace Modalities,” in IJCAR, 2001, pp. 626–641.
relational verification.                                                      [26] B. Beckert and M. Ulbrich, “Trends in Relational Program Verifica-
                                                                                   tion,” in Principled Software Development - Essays Dedicated to Arnd
Acknowledgements.                                                                  Poetzsch-Heffter on the Occasion of his 60th Birthday, 2018, pp. 41–58.
                                                                              [27] F. Eigner and M. Maffei, “Differential Privacy by Typing in Security
  This work was funded by the ERC Starting Grant 2014                              Protocols,” in CSF, 2013, pp. 272–286.
SYMCAR 639270, the ERC Proof of Concept Grant 2018                            [28] G. Barthe, C. Fournet, B. Grégoire, P.-Y. Strub, N. Swamy, and
                                                                                   S. Zanella-Béguelin, “Probabilistic Relational Verification for Crypto-
SYMELS 842066, the Wallenberg Academy Fellowship 2014                              graphic Implementations,” in POPL, 2014, pp. 193–205.
TheProSE, the Austrian FWF research projects W1255-N23                        [29] V. Cortier, F. Eigner, S. Kremer, M. Maffei, and C. Wiedling, “Type-
and RiSE S11409-N23, the ERC Consolidator Grant 2018                               Based Verification of Electronic Voting Protocols,” in POST, 2015, pp.
                                                                                   303–323.
BROWSEC 771527, by the Netidee projects EtherTrust 2158                       [30] V. Cortier, N. Grimm, J. Lallemand, and M. Maffei, “A Type System
and PROFET P31621, and by the FFG projects PR4DLT                                  for Privacy Properties,” in CCS, 2017, pp. 409–423.
13808694 and COMET K1 SBA.                                                    [31] ——, “Equivalence Properties by Typing in Cryptographic Branching
                                                                                   Protocols,” in POST, 2018, pp. 160–187.
                             R EFERENCES                                      [32] G. Barthe, J. M. Crespo, and C. Kunz, “Beyond 2-Safety: Asymmetric
                                                                                   Product Programs for Relational Program Verification,” in LFCS, 2013,
 [1] J. A. Goguen and J. Meseguer, “Security Policies and Security Models,”        pp. 29–43.
     in IEEE Symposium on Security and Privacy, 1982, pp. 11–20.              [33] N. Grimm, K. Maillard, C. Fournet, C. Hriţcu, M. Maffei, J. Protzenko,
 [2] S. Chaudhuri, S. Gulwani, and R. Lublinerman, “Continuity analysis of         T. Ramananandro, A. Rastogi, N. Swamy, and S. Zanella-Béguelin, “A
     programs,” in POPL, 2010, pp. 57–70.                                          Monadic Framework for Relational Verification: Applied to Information
 [3] M. R. Clarkson and F. B. Schneider, “Hyperproperties,” in CSF, 2008,          Security, Program Equivalence, and Optimizations,” in CPP, 2018, pp.
     pp. 51–65.                                                                    130–145.
 [4] G. Barthe, P. R. D’Argenio, and T. Rezk, “Secure Information Flow by     [34] N. Swamy, C. Hritcu, C. Keller, A. Rastogi, A. Delignat-Lavaud, S. For-
     Self-Composition,” in CSFW, 2004, pp. 100–114.                                est, K. Bhargavan, C. Fournet, P. Strub, M. Kohlweiss, J. K. Zinzindo-
     houe, and S. Z. Béguelin, “Dependent Types and Multi-Monadic Effects                                          σ′ = σ
     in F,” in POPL, 2016, pp. 256–270.                                                            [skip]
[35] B. Godlin and O. Strichman, “Regression Verification: Proving the                                      hskip; p, σi =≫ hp, σ ′ i
     Equivalence of Similar Programs,” Softw. Test., Verif. Reliab., vol. 23,
     no. 3, pp. 241–258, 2013.                                                                                σ ′ = σ[v 7→ JeK(σ)]
[36] D. Felsing, S. Grebing, V. Klebanov, P. Rümmer, and M. Ulbrich,                              [asg]
                                                                                                            hv := e; p, σi =≫ hp, σ ′ i
     “Automating Regression Verification,” in ASE, 2014, pp. 349–360.
[37] Q. Zhou, D. Heath, and W. Harris, “Completely Automated Equivalence
     Proofs,” CoRR, vol. abs/1705.03110, 2017.                                                         JcK(σ) = true          σ′ = σ
                                                                                        [iteT ]
[38] H. Kwon, W. Harris, and H. Esmaeilzadeh, “Proving Flow Security of                           hif(c)then{p1 }else{p2 }; p, σi =≫
     Sequential Logic via Automatically-Synthesized Relational Invariants,”
     in CSF, 2017, pp. 420–435.                                                                                hp1 ; p, σ ′ i
[39] K. S. Namjoshi and N. Singhania, “Loopy: Programmable and Formally
     Verified Loop Transformations,” in SAS, 2016, pp. 383–402.                                        JcK(σ) = false         σ′ = σ
[40] N. Partush and E. Yahav, “Abstract Semantic Differencing via Specula-              [iteF ]
                                                                                                  hif(c)then{p1 }else{p2 }; p, σi =≫
     tive Correlation,” in OOPSLA, 2014, pp. 811–828.
[41] S. K. Lahiri, C. Hawblitzel, M. Kawaguchi, and H. Rebêlo, “SYMDIFF:                                       hp2 ; p, σ ′ i
     A Language-Agnostic Semantic Diff Tool for Imperative Programs,” in
     CAV, 2012, pp. 712–717.                                                                                 JcK(σ) = true        σ′ = σ
[42] M. Sousa and I. Dillig, “Cartesian Hoare Logic for Verifying k-Safety               [whileT ]
     Properties,” in PLDI, 2016, pp. 57–69.                                                            hwhilei (c)do{p1 }; p, σi =≫
[43] M. Sousa, I. Dillig, and S. K. Lahiri, “Verified Three-Way Program                               hp1 ; whilei+1 (c)do{p1 }; p, σ ′ i
     Merge,” in OOPSLA, 2018, pp. 165:1–165:29.
[44] E. W. Smith and D. L. Dill, “Automatic Formal Verification of Block
     Cipher Implementations,” in FMCAD, 2008, pp. 1–7.
                                                                                                            JcK(σ) = false        σ′ = σ
                                                                                       [whileF ]
[45] M. Stepp, R. Tate, and S. Lerner, “Equality-Based Translation Validator                        hwhilei (c)do{p1 }; p, σi =≫ hp, σ ′ i
     for LLVM,” in CAV, 2011, pp. 737–742.
[46] R. Sharma, E. Schkufza, B. R. Churchill, and A. Aiken, “Data-Driven
     Equivalence Checking,” in OOPSLA, 2013, pp. 391–406.                               Fig. 4: Small-step operational semantics of W
[47] M. Balliu, M. Dam, and R. Guanciale, “Automating Information Flow
     Analysis of Low Level Code,” in CCS, 2014, pp. 1080–1091.
[48] M. R. Clarkson, B. Finkbeiner, M. Koleini, K. K. Micinski, M. N. Rabe,
     and C. Sánchez, “Temporal Logics for Hyperproperties,” in POST, 2014,         Definition 5: Let p be a program and C, C1 , C2 be configu-
     pp. 265–284.                                                               rations. A partial execution from C1 to C2 is a derivation in the
                                                                                inference system of small-step operational semantics starting
                               A PPENDIX                                        at C1 and ending in C2 . An execution of p is a partial execution
A. Small-step operational semantics of W                                        from an initial configuration to a configuration hend, σi for an
   In this subsection, we recall standard definitions from small-               arbitrary state σ. If there exists a partial execution starting at
step operational semantics.                                                     the initial configuration and ending in C, we say that C is
   Definition 2: Let p be a program. Then a state σ is a function               reachable.
which (i) maps each integer-variable v of p to a concrete value
                                                                                B. Separating subprograms and state
σ(v) ∈ I and (ii) maps each array-variable v and each value
pos ∈ I to a value σ(v, pos) ∈ I.                                                  Our presentation of operational semantics features counters.
   Definition 3: A configuration is a pair hp, σi, where we refer               We now show that as a result, if r1 and r2 are continuations
to p as the continuation and σ is a state.                                      occuring in the same execution, then r1 and r2 are different.
   The execution of a single step in the program is defined                     This implies that we do not need to know about the state to
by the rules of Figure 4. Our presentation is semantically                      distinguish different configurations and allows us to separate
equivalent to standard small-step operational semantics, but                    the continuation from the state.
differs syntactically in three points, in order to simplify                        Theorem 2 (Uniqueness): Let p be a program and let hr1 , σ1 i
later definitions and theorems: (i) program-expressions are                     and hr2 , σ2 i be configurations occuring in the execution of p.
evaluated on the fly without introducing explicit steps (ii) the                Then r1 6= r2 .
relation between the state σ in the original configuration and                        Proof: Let p, p1 , p2 be subprograms, let s be a single
the state σ ′ in the resulting configuration is explicitly described            statement and let C be a condition. Consider the minimal re-
using a formula (in contrast to using the same variable σ                       lation >1 which satisfies the following conditions and consider
twice) and (iii) we annotate while-statements with counters to                  its transitive closure >.
ensure the uniqueness of continuations during the execution,
                                                                                                                     s; p >1 p
see Section B.
   A program is executed by iteratively transforming the initial                  if(C)then{p1 }else{p2 }; p >1 p1 ; p
configuration according to the rules of Figure 4 until the                        if(C)then{p1 }else{p2 }; p >1 p2 ; p
continuation becomes end. We annotate each while-statement                                  whilei (C)do{p1 }; p >1
in the initial configuration of the execution with counter 0:
   Definition 4: Let p be a program, let p′ be the result of                                                        p1 ; whilei+1 (C)do{p1 }; p
annotating each while-loop in p with counter 0 and let σ be                     It is an easy exercise to establish that > is a strict partial
an arbitrary state. Then hp′ , σi is called initial configuration.              order on continuations. Next, skip, asg, whileF and end
reduce the ordering according to the first condition, iteT                 Let s be a skip-statement. Instantiating the skip-rule with p :=
and iteF reduce the ordering according to the second resp.                 R(end s ) yields
third condition and whileT reduce the ordering according to
                                                                                       [skip]                   σ′ = σ
the fourth condition. In particular, we are able to conclude
                                                                                                 hR(start s ), σi =≫ hR(end s ), σ ′ i
r1 > r2 , which immediately implies r1 6= r2 due to the
irreflexivity of >.                                                        Let s be an assignment v = e. Instantiating the asg-rule with
   Having established the uniqueness, we are now able to                   p := R(end s ) yields
speak of the state at a given continuation p (and annotate
                                                                                                       σ ′ = σ[v 7→ JeK(σ)]
it as σ(p)). As a result, a configuration is fully described                           [asg]
by the continuation. We therefore omit the state σ(p) in                                         hR(start s ), σi =≫ hR(end s ), σ ′ i
any configuration hp, σ(p)i and write hpi instead. Finally we              Let p1 and p2 be s1 ; . . . ;sk resp. s’1 ; . . . ;s’k‘ and let s
use the fact that we have finitely many program variables                  be if(Cond) {p1 } else {p2}. Instantiating the rules iteT and
v1 , . . . , vn , and split up σ(p) into σv1 (p), . . . , σvn (p), which   iteF with p := R(end s ) yields the two rules
we simply write as v1 (p), . . . , vn (p).
                                                                                                    JcK(σ) = true       σ′ = σ
                                                                                      [iteT ]
C. Mapping timepoints to continuations                                                          hR(start s ), σi =≫ hR(start s1 ), σ ′ i
   Small-step operational semantics describes only the next
                                                                                                   JcK(σ) = false       σ′ = σ
step in an execution, whereas structural semantics, and trace                         [iteF ]
logic semantics in particular, also describes the complete                                      hR(start s ), σi =≫ hR(start s′1 ), σ ′ i
execution of each substatement.                                            Let p1 be s1 ; . . . ;sk and let s be while(Cond) {p1 }. Instan-
   Recall that the definitions of start s and end s from Sec-              tiating the rules whileT and whileF with p := end s yields
tion IV-A describe the timepoints of the start, respectively end           the two rules
of a partial execution of a statement s. To connect the two
worlds of operational and structural semantics we provide a                                           JcK(σ) = true       σ′ = σ
                                                                                   [whileT ]
mapping R from such timepoints to continuations:                                                 hR(tps (its )), σi =≫ hR(start s1 ), σ ′ i
   Definition 6: Let R be
                                                                                                     JcK(σ) = false       σ′ = σ
                                                                                    [whileF ]
            R(tps ) := s; R(end s )          if s is non-loop                                     hR(tps (its )), σi =≫ hR(end s ), σ ′ i
                          it
        R(tps (it)) := s ; R(end s )         if s is loop
                                                                           Fig. 5: Small-step operational semantics using tp, start, end .
   We are now able to describe configurations using tps , start s
and end s . In particular, we are able to instantiate each rule
to a new rule, whose configurations can be described using                       Proof: Consider an arbitrary trace tr and let E be the
tps , start s and end s . The instantiated rules produce the               execution denoted by tr. Let M be an execution-interpretation
same reachable configurations as the original rules, and are               of E. We proceed by structural induction on the program-
presented in Figure 5.                                                     structure with the induction hypothesis that for a subprogram
D. W-Soundness                                                             p′ = s1 ; . . . ; sk , if hR(start s1 )i is reachable our semantics
                                                                           Jp′ K instantiated with tr are W-sound.
   Operational semantics describe the execution of a program.
Such an execution correseponds to a model where the terms                     Case distinction on the type of the statement s:
describing variable values are interpreted according to the                  • Let s be of the form skip. Assume hR(start s )i
states in the corresponding configurations.                                    is reachable. Then the only rule which applies
   Definition 7 (Execution-interpretation): Let p be a program.                is skip, so hR(end s )i is also reachable and
For an arbitrary execution E of p containing configurations                    σ(R(end s )) = σ(R(start s )). By the definition of
hR(tp1 ), σ1 i, . . . , hR(tpn ), σn i, let an execution-interpretation        execution-interpretations, we therefore conclude that
be any interpretation M , such that for any integer/array                      axiom 7 is W-sound.
variable v the term v(tpi ) resp. v(tpi , pos) is interpreted as             • Let s be of the form v := e. Assume hR(start s )i is
σi (v) resp. σi (v[pos]) in M .                                                reachable. Then the only rule which applies is asg,
   With the above definition of execution-interpretations,                     so hR(end s )i is also reachable and σ(R(end s )) =
soundness is captured as follows:                                              σ(R(start s ))[v 7→ JeK(σ(R(start s )))]. By the definition
   Definition 8 (W-Soundness): Let p be a program and let A                    of execution-interpretations, we therefore conclude that
be a trace logic axiom. Then A is called W-sound, if for any                   axiom 8 is W-sound.
execution-interpretation M we have M  A.                                    • Let s be of the form if(c)then{p1 }else{p2 }, where
   We show that the axioms of trace logic are W-sound.                         p1 is s1 ; . . . ; sk . Assume hR(start s )i is reachable. Each
   Theorem 3 (W-Soundness of Semantics of W): For a given                      axiom 10a,10c is an implication with JcK(start s ) as posi-
terminating program p, the axioms of Figure 5 defining the                     tive premise, so assume that JcK(start s ) holds in M . Then
semantics of W are W-sound.                                                    the only applicable rule is iteT . Therefore hR(start s1 )i is
  reachable and σ(R(start s1 )) = σ(R(start s )). From the             trivial sub-induction to conclude that hR(tps (it))i is
  latter fact and the definition of execution-interpretations          reachable. Since JcK(tps (it)) holds, the only applicable
  we conclude that axiom 10a is W-sound. Furthermore,                  rule is whileT , so hR(start s1 (it))i is reachable and
  since p1 is a subprogram of s, we are able to combine the            σ(R(start s1 (it))) = σ(R(tpwhile (it))). From this we
  reachability of hR(start p1 )i with the induction hypoth-            conclude that axiom 11c is W-sound by the definition
  esis to derive that Jp1 K is W-sound. In particular axiom            of execution-interpretations. Next, p1 is a subexpression
  10c is W-sound. Analogously we are able to prove the                 of s, so we are able to combine the reachability of
  W-soundness of axioms 10b,10d.                                       hR(start p1 (it))i with the induction hypothesis to con-
• Let s be of the form while(c)do{p1 }, where p1                       clude that Jp1 K is W-sound. Therefore, axiom 11d is W-
  is s1 ; . . . ; sk . Assume hR(start s )i is reachable. Axiom        sound.
  11a and 11b define lastIt s as the smallest iteration it             Finally, for any iteration it < lastIt s , we know that
  where JcK(tps (it)) does not hold in M . Since we assume             JcK(tps (it)) holds in M , so a similar trivial sub-induction
  termination, such an iteration needs to exist, and in                yields that hR(tps (lastIt s ))i is reachable. By definition
  particular the definition is well-defined, so axiom 11a and          of lastIt s , JcK(tps (it′ )) does not hold in M , so the
  11b are W-sound.                                                     only applicable rule is whileF . Therefore, hR(end s )i
  Now let it be an arbitrary iteration such that it <                  is reachable and σ(R(end s )) = σ(R(tps (lastIt s ))). In
  lastIt s holds in M . By definition, for any iteration               particular, Axiom 11e is W-sound.
  it′ < it, we know that JcK(tps (it′ )) holds in M ,             Finally the initial state of an execution is reachable, so we can
  in particular the only applicable rule for hR(tps (it′ ))i      apply the induction hypothesis to establish the W-soundness
  is whileT . Furthermore hR(start s )i is reachable and          of our semantics.
  equal to hR(tps (0))i. Combining both facts we use a
