                                        Bilateral Proofs of Safety and Progress Properties
                                                     of Concurrent Programs
arXiv:1704.01814v1 [cs.PL] 5 Apr 2017




                                                                    Jayadev Misra
                                                   University of Texas at Austin, misra@utexas.edu
                                                                          April 5, 2017


                                                                             Abstract
                                                 This paper suggests a theomisra@utexas.edury of composable specifi-
                                             cation of concurrent programs that permits: (1) verification of program
                                             code for a given specification, and (2) composition of the specifications of
                                             the components to yield the specification of a program. The specification
                                             consists of both terminal properties that hold at the end of a program ex-
                                             ecution (if the execution terminates) and perpetual properties that hold
                                             throughout an execution. We devise (1) proof techniques for verification,
                                             and (2) composition rules to derive the specification of a program from
                                             those of its components. We employ terminal properties of components
                                             to derive perpetual properties of a program and conversely. Hence, this
                                             proof strategy is called bilateral. The compositional aspect of the theory
                                             is important in assembling a program out of components some of whose
                                             source code may not be available, as is increasingly the case with cross-
                                             vendor program integration.

                                             Keywords: Program specification, concurrent programming, verification,
                                             composition, safety and progress properties.


                                        1    Introduction
                                        Four decades of intensive research has failed to yield a scalable solution to the
                                        problem of concurrent program design and verification. While there have been
                                        vast improvements in our understanding, the theory and practice in this area
                                        lag considerably behind what has been achieved for sequential programs. Very
                                        small programs, say for synchronization, are proved manually, though the proof
                                        methods are mostly unscalable. Larger programs of practical significance, say
                                        cache coherence protocols, are typically proved using model checking, which
                                        imposes size limitations. Programs from different vendors are rarely assembled
                                        to run concurrently.
                                            We believe that the problem stems from the lack of a theory of composable
                                        specification for concurrent programs. Sequential imperative programs enjoy


                                                                                  1
such a theory, introduced by Hoare [7], in which a program is specified by a pair
of predicates, called its pre- and postcondition. The theory successfully permits:
(1) verification of program code for a given specification, and (2) composition of
the specifications of the components to yield the specification of a program. A
fundamental concept is invariant that holds at specific program points, though
invariant is not typically part of the program specification. Termination of a
program is proved separately.
    A specification of a concurrent program typically includes not just the pre-
and postconditions but properties that hold of an entire execution, similar to
invariants. A typical specification of a thread that requests a resource, for ex-
ample, may state that: (1) once it requests a resource the thread waits until the
resource is granted, and (2) once the resource is granted the thread will even-
tually release it. The first property is an instance of a safety property and the
second of a progress property, see Lamport [10] and Owicki and Lamport [14].
    Call the postcondition of a program for a given precondition to be a termi-
nal property. And a property that holds throughout an execution a perpetual
property. Terminal properties compose only for sequential programs, though
not for concurrent programs, and they constitute the essence of the assertional
proof method of Hoare. Safety and progress are typical perpetual properties.
    This paper suggests a theory of composable specification of concurrent pro-
grams with similar goals as for sequential programs. The specification consists of
both terminal and perpetual properties. We devise (1) proof techniques to ver-
ify that program code meets a given specification, and (2) composition rules to
derive the specification of a program from those of its components. We employ
terminal properties of components to derive perpetual properties of a program
and conversely. Hence, this proof strategy is called bilateral. The compositional
aspect of the theory is important in assembling a program out of components
some of whose source code may not be available, as is increasingly the case with
cross-vendor program integration.
    The Hoare-proof theory for sequential programs is known to be sound and
relatively-complete. A sound and relatively-complete proof theory for concur-
rent programs that use a very limited set of program constructs, known as
Unity, appears in Chandy and Misra [2] and Misra [11]. This paper combines
both approaches to yield a theory applicable to concurrent programs written
in conventional languages. (The soundness and relatively-completeness of this
theory has not been proved yet.)
    We treat three examples of varying complexity in detail in this paper. First,
a program that implements a distributed counter is used to illustrate the various
concepts of the theory in stages through out the paper. Appendix B includes a
proof of a mutual exclusion program, a system of tightly-coupled components.
Unlike traditional proofs, it is based on composing the specifications of the
components. Appendix C includes proof of a recursively-defined concurrent
program, where code of one component is only implicit, again using composable
specifications. We know of no other proof technique that can be used to prove
this example program.



                                        2
2      Program and Execution Model
2.1     Program Structure
The syntax for programs and its components is given below.

              action    ::= guard → body
      f, g :: component ::= action | f [] g | seq(f0 , f1 , · · · fn )
              program   ::= f

   An action has a guard, which is a predicate, and a body which is a piece of
code. Execution of the body in a state in which the guard holds is guaranteed to
terminate; we assume that this guarantee is independently available. Details of
execution semantics is given Section 2.2. A guard that is true is often dropped.
An action without a guard is non-blocking and a guarded action blocking.
   A structured component is either: (1) a join of the form f [] g where f
and g are its direct subcomponents, or (2) seq(f0 , f1 , · · · fn ) where the direct
subcomponents, fi , are combined using some sequential language construct.
A join models concurrent execution, as we describe in Section 2.2. And seq
denotes any sequential language construct for which proof rules are available.
Thus, the typical constructs of sequencing, if-then-else and do-while are seq
constructs. A subcomponent of any component is either its direct subcomponent
or a subcomponent of some direct subcomponent. Note that a component is
never empty.
   Join construct is commutative and associative. The syntax permits arbitrary
nesting of sequential and concurrency constructs, so, “(f [] g) ; (f ′ [] g ′ )” is a
program with f, f ′ , g and g ′ as components.
   A program is a component that is meant to be executed alone.

Access rights to variables A variable named in a component is accessible
to it. Variable x is local to f if f has exclusive write-access to x during any of
its executions. Therefore, any accessible variable of a component in a sequential
program is local to it. However, a local variable of f [] g may not be local to
either f or g. An accessible non-local variable x of f is shared ; x is shared with
g if x is also accessible to g. Note that x is local to f and shared in g if f has
exclusive write-access to x and g can only read x.
    A program is executed alone, so, all its accessible variables are local to it.
    A local predicate of f is a predicate in which every variable is a local variable
of f . Therefore, true and false are local to all components. It follows that the
value of a local predicate of f remains unchanged in any execution as long as f
does not take a step.

2.2     Program execution
A step is an instance of the execution of an action. A step of action b → α is
executed as follows: evaluate b without preemption and if it is true, immediately
execute α to completion, again without preemption —this is called an effective

                                            3
execution of the action— else the program state (and its control point) are
unaltered —this is called an ineffective execution. Thus, in an effective execution
of b → α, b holds when the execution of α begins. Ineffective execution models
busy-waiting whereby the action execution is retried at some future moment.
    Execution of a join starts simultaneously for all its direct subcomponents,
and terminates when they all do. At any moment during the execution, the
program control may reside simultaneously in many of its subcomponents. Ex-
ecution rules for a seq are the traditional ones from sequential programming,
which ensures that the program control is within one direct subcomponent at
any moment. The subcomponent itself may be a join which may have multiple
control points of its own.
    Initially the program control is at the entry point of the program. In any
given state the program takes a step by choosing a control point before an action
and executing, effectively or ineffectively, the action. If there is no such control
point, the program has terminated. The choice of control point for a step is
arbitrary, but subject to the following fairness constraint: every control point is
chosen eventually for execution, so that no component is ignored forever. This
is the same constraint advocated by Dijkstra [5] in his classic paper. In contrast
to a terminated execution a deadlocked execution attempts executions of certain
actions ineffectively forever, and the control resides permanently at the points
preceding each of these actions.
    An execution is a sequence of steps that can not be extended. Infinite
executions do not have an end state. A finite execution either terminates or is
deadlocked, and it has an end state. It simplifies the proof theory considerably
to imagine that every execution is infinite, by extending each finite execution
by an infinite number of stutter steps that repeat the end state forever.

2.3      Example: Distributed counter
We consider an abstraction of a distributed counter protocol in Blumofe [1].
The proof in this paper is based on a proof by Rajeev Joshi and the one given
in Chapter 6 of Misra [11].
    The protocol f that implements counter ctr is the join of a finite number
of threads, fj , given below. Each fj has local variables oldj and newj . Below,
each assignment statement and guarded statement is an action. The following
form of the if statement was introduced by Dijkstra [4]; in each execution of the
statement an alternative whose guard holds is executed without preemption.

initially ctr = 0
fj ::
   initially oldj , newj = 0, 0
  loop
         newj := oldj + 1;
         if [ ctr = oldj → ctr := newj
             | ctr 6= oldj → oldj := ctr ]
  forever


                                             4
   It is required to show that ctr behaves as a counter, that is: (1) ctr never
decreases and it increases only by 1, and (2) ctr increases eventually. Both of
these are perpetual properties. There is no terminal property of interest since
the program never terminates.


3     Introduction to the proof theory
3.1     Specification
A specification of component f is of the form {r} f {Q          s} where r and
s are the pre- and postconditions, and Q is a set of perpetual properties. The
meaning of such a specification is as follows. For any execution of f starting in
an r-state,
    1. if the execution terminates, the end state is an s-state, and
    2. every property in Q holds for the execution.
   We give proof rules for pre- and postconditions in the following section.
Proof rules for perpetual properties appear in subsequent sections, for safety
properties in Section 4 and for progress properties in Section 5.

Terminology Write {r} f {s} when Q is irrelevant in the discussion, and
{r} f {Q     } when s is irrelevant. Further for q ∈ Q, write “q in f ” when r is
understood from the context, and just “q” when both f and r are understood.
An inference rule without explicit mention of f or r denotes that the rule applies
for any f and r.

Variables named in properties A property of component f includes pred-
icates that name accessible variables of f , and other variables, called free vari-
ables. A property is implicitly universally quantified over its free variables. Any
inaccessible variable named in a property denotes a free variable, and, being a
bound variable, may be renamed.

3.2     Local Annotation
Local Annotation of component f associates assertions with program points
such that each assertion holds whenever program control reaches the associated
point in every execution of any program in which f is a component. Thus, a
local annotation yields precondition for the execution of each action of f , and
valid pre- and postcondition of f in any environment. Since the execution envi-
ronment of f is arbitrary, only the predicates that are local to f are unaffected
by executions of other components. Therefore, a local annotation associates
predicates local to each point of f , as explained below.
    Local annotation is defined by the program structure. First, the proof rule
for an action is as follows:



                                         5
       {p ∧ b} α {q}
       {p} b → α {q}
    To construct a local annotation of f = seq(f0 , f1 , · · · fn ), construct local
annotation of each fi using only the local variables of fi as well as those of
f . Then construct an annotation of f using the proof rules for seq from the
sequential program proof theory. Observe that the local variables of f are local
to each fi because in a sequential execution among the direct subcomponents
of f each fi has exclusive write-access to these variables during its execution.
    To construct a local annotation of f = g [] h, construct local annotations of
each of g and h using only their local variables. Then construct an annotation
of f using the proof rule given below. Note that the proof rule is valid only
because the assertions in g and h are local to those components.

              {r} g {s}
             {r′ } h {s′ }
       {r ∧ r′ } g [] h {s ∧ s′ }
    Observe that a local variable of f is not necessarily local to g or h unless
they have exclusive write-access to it. Henceforth, all annotations in this paper
are local annotations.
    A shortcoming of local annotation is that a variable that is local to f [] g but
shared by both f and g can not appear in a local annotation by the application
of these rules alone. The invariance meta-rule, given in Section 3.4, overcomes
this problem.

3.3      Example: Distributed Counter, contd.
Construct a local annotation of fj for the example of Section 2.3. Below, we
have labeled the actions to refer to them in subsequent proofs.

fj ::
   initially oldj , newj = 0, 0
   {true}
  loop
      {true}
         αj :: newj := oldj + 1;
      {newj = oldj + 1}
         if [ βj :: {newj = oldj + 1} ctr = oldj → ctr := newj {true}
              | γj :: {newj = oldj + 1} ctr 6= oldj → oldj := ctr {true}
            ]
      {true}
  forever




                                         6
3.4    Meta-rules
The following general rules apply for specifications.

    • (lhs strengthening; rhs weakening)
                         {r} f {Q   s}
       r′ ⇒ r, s ⇒ s′ , Q′ ⊆ Q, r′ and s′ are local to f
                        {r′ } f {Q′  s′ }
    • (Conjunction; Disjunction)
               {r} f {Q    s}
             {r′ } f {Q′   s′ }
             ′           ′
       {r ∧ r } f {Q ∪ Q      s ∧ s′ }
             ′           ′
       {r ∨ r } f {Q ∩ Q      s ∨ s′ }

Justifications for the meta-rules The lhs strengthening and rhs weakening
rules are inspired by similar rules for Hoare-triples. Additionally, since the
properties in Q are independent, any number of them may be removed.
    For the conjunction rule, let the set of executions of f starting in r-state be r-
executions, and, similarly r′ -executions. The r ∧r′ -executions is the intersection
of r-executions and r′ -executions. Therefore, the postcondition of any execution
in r ∧ r′ -executions satisfies s ∧ s′ and every property in Q or Q′ , justifying the
conjunction rule. The arguments for the disjunction rule are similar.


4     Safety Properties
A safety property is perpetual. We develop a safety property, co, and its special
cases, taken from Misra [11]. Safety properties are derived from local annota-
tions and/or safety properties of the subcomponents of a component.

4.1    Safety Property co
Write p co q in component f , for predicates p and q that may not be local to
f , to mean that effective execution of any action of f in a p-state establishes a
q-state. Observe that an ineffective execution preserves p. Thus, given p co q:
(1) in any execution of f once p holds it continues to hold until q is established,
though q may never be established, and (2) as a composition rule, p co q holds
in component iff it holds in every subcomponent of it.
     For an annotated component, co is defined by the following proof rule.

                                 {r} f {s}
      For every action b → α with precondition pre in the annotation :
                            {pre ∧ b ∧ p} α {q}
                            {r} f {p co q    s}



                                          7
    As an example, the statement “every change in integer variable ctr can only
increment its value” may be formalized as ctr = m co ctr = m ∨ ctr = m + 1,
for all integer m.

4.2     Special cases of co
Define special cases of co for component f : stable, constant and invariant.
Given predicate p and expression e, in any execution of f : (1) stable p means
that p remains true once it becomes true, (2) constant e that the value of
e never changes, and (3) invariant p that p is always true, including after
termination, if the program terminates. Formally, in f
      stable p        ≡ p co p
      constant e      ≡ (∀c :: stable e = c)
      invariant p     ≡ initially p and stable p
    Observe that invariant true (hence, stable true) and stable false are prop-
erties of every component. A variable for which f has no write-access is constant
in f , and so is any expression constructed out of such variables.
    Derived rules for co and some of its special cases, which are heavily used
in actual proofs, are given in Appendix A.1. It follows from the derived rules
that a safety property of a program is a property of all its components, and
conversely, as given by the inheritance rule below.

4.3     Meta-rules
  1. (Inheritance) If any safety property (co or any of its special cases) holds
     in all subcomponents of f then it holds in f . More formally, for safety
     properties σ,
                    (∀i :: {ri } fi {si })                   (∀i :: {ri } fi {σ    si })
          Given:                                   Assert:
                          {r} f {s}                                {r} f {σ     s}
  2. (Invariance) A local invariant of a component, i.e., a local predicate that is
     invariant in the component, can be substituted for true, and vice versa, in
     any predicate in an annotation or property of the component. In particu-
     lar, for a program all variables are local, so any invariant can be conjoined
     to an assertion including the postcondition.

Justifications for the meta-rules Inheritance rule is based on the fact that
if a safety property holds for all components of f it holds for f as well. Given
the proof rule at left the inheritance proof rule at right can be asserted for any
set of safety properties σ.
    The invariance rule is from Chandy and Misra [2] where it is called the
“substitution axiom”. One consequence of the rule is that a local invariant of
f [] g, that may not be a local predicate of either f or g, could be conjoined to
predicates in an annotation of f [] g. Additionally, all variables in a program
are local; so, any invariant can be substituted for true in a program.

                                             8
4.4    Example: Distributed Counter, contd.
For the example of Section 2.3 we prove that ctr behaves as a counter in that
its value can only be incremented, i.e., ctr = m co ctr = m ∨ ctr = m + 1 in
f . Using the inheritance rule, it is sufficient to prove this property in every
component fj . In fj , only βj may change the value of ctr; so we need only show
the following whose proof is immediate:

{ctr = m ∧ newj = oldj + 1 ∧ ctr = oldj } ctr := newj {ctr = m ∨ ctr = m + 1}


5     Progress Properties
We are mostly interested in progress properties of the form “if predicate p holds
at any point during the execution of a component, predicate q holds eventually”.
Here “eventually” includes the current and all future moments in the execution.
This property, called leads-to, is defined in Section 5.3 (page 12). First, we
introduce two simpler progress properties, transient and ensures. Transient is a
fundamental progress property, the counterpart of the safety property stable.
It is introduced because its proof rules are easy to justify and it can be used
to define ensures. However, it is rarely used in program specification because
ensures is far more useful in practice. Ensures is used to define leads-to.

5.1    Progress Property: transient
In contrast to a stable predicate that remains true once it becomes true, a
transient predicate is guaranteed to be falsified eventually. That is, predicate
p is transient in component f implies that if p holds at any point during an
execution of f , ¬p holds then or eventually in that execution. In temporal logic
notation p is transient is written as ✷✸¬p. Note that ¬p may not continue to
hold after p has been falsified. Predicate false is transient because false ⇒ true,
and, hence ¬false holds whenever false holds. Note that given p transient in f ,
¬p holds at the termination point of f because, otherwise, f can take no further
steps to falsify p.
    The proof rules are given in Figure 5.1. Below, postf is a local predicate of
f that is initially false and becomes true only on the termination of f . Such a
predicate always exists, say, by encoding the termination control point into it.
For a non-terminating program, postf is false. Proof of postf is a safety proof.

Justifications The formal justification is based on induction on the program
structure: show that the basis rule is justified and then inductively prove the
remaining rules. We give informal justifications below.
    In the basis rule the hypotheses guarantee that each action of f is effectively
executed whenever p holds, and that the execution establishes ¬p. If no action
can be executed effectively, because precondition of no action holds, the program
has terminated and postf holds. Hence, ¬p ∨ postf , i.e.¬(p ∧ ¬postf ), hold
eventually in all cases. Note that if pre ⇒ ¬p then pre ∧ p is false and the


                                        9
--------------------------------------------------------------------------------

   • (Basis)
                            {r} f {s}
        For every action b → α of f with precondition pre :
                           pre ∧ p ⇒ b
                        {pre ∧ p} α {¬p}
               {r} f {transient p ∧ ¬postf     s}
   • (Sequencing)
       {r} f {transient p ∧ ¬postf        postf }
            {postf } g {transient p       }
            {r} f ; g {transient p        }
   • (Concurrency)
        {r} f {transient p    }
      {r} f [] g {transient p   }
   • (Inheritance)
                (∀i :: {ri } fi {si })                    (∀i :: {ri } fi {transient p    si })
       Given:                                   Assert:
                      {r} f {s}                                 {r} f {transient p     s}

                         Figure 1: Definition of transient
--------------------------------------------------------------------------------



hypotheses are vacuously satisfied. If f never terminates, ¬postf always holds
and ¬p is guaranteed eventually.
    The next two rules, for sequential and concurrent composition, have weaker
hypotheses. The sequencing rule is based on an observation about a sequence
of actions, α; β. To prove transient p it is sufficient that α establish ¬p
or that it execute effectively, thus establishing postα , and that β establish ¬p.
The sequencing rule generalizes this observation to components. Being a local
predicate, postf can not be falsified by any concurrently executing component,
so it holds as long as the control remains at the termination point of f .
    In the concurrency rule, as a tautology g either establishes ¬p eventually,
thus guaranteeing the desired result, or preserves p forever. In the latter case,
f establishes ¬p since transient p holds in f .
    The inheritance rule applies to a program with multiple components. It
asserts that if the property holds in each component fi then it holds in program
f . To see this consider two cases: f is seq or join, and argue by induction on
the program structure.
    For seq f : if p holds at some point before termination of f it is within exactly
one direct subcomponent fi , or will do so without changing any variable value.
For example, if control precedes execution of “ifb then f0 else f1 ” then it will
move to a point preceding f0 or f1 after evaluation of b without changing the


                                         10
state. Note that fi may be a join, so there may be multiple program points
within it where control may reside simultaneously, but all controls reside within
one direct subcomponent of seq f at any moment. From the hypothesis, that
component, and hence, the program establishes ¬p eventually.
    For a join, say f [] g: Consider an execution in which, say, f has not ter-
minated when p holds. From the arguments for the concurrency rule, using
that transient p in f , eventually ¬p is established in that execution. Similar
remarks apply for all executions in which g has not terminated. And, if both
f and g have terminated, then ¬p holds from the definition of transient for
each component.                                                                ✷

Notes
  1. The basis rule by itself is sufficient to define an elementary form of tran-
     sient. However, the transient predicate then has to be extremely elaborate,
     typically encoding control point of the program, so that it is falsified by
     every action of the component. The other rules permit simpler predicates
     to be proven transient.
  2. Basis rule is the only rule that needs program code for its application,
     others are derived from properties of the components, and hence, permit
     specification composition.
  3. It is possible that p is eventually falsified in every execution of a component
     though there is no proof for transient p. To see this consider the program
     f [] g in which every action of f falsifies p only if for some predicate q,
     p ∧ q holds as a precondition, and every action of g falsifies p only if p ∧ ¬q
     holds as a precondition, and neither component modifies q. Clearly, p
     will be falsified eventually, but this fact can not be proved as a transient
     property; only p ∧ q and p ∧ ¬q can be shown transient. As we show later,
     p leads-to ¬p.

5.2     Progress Property: ensures
Property ensures for component f , written as p en q with predicates p and q,
says that if p holds at any moment in an execution of f then it continues to
hold until q holds, and q holds eventually. This claim applies even if p holds
after the termination of f . For initial state predicate r, it is written formally as
{r} f {p en q     } and defined as follows:

                {r} f {p ∧ ¬q co p ∨ q, transient p ∧ ¬q           }
                              {r} f {p en q   }

    We see from the safety property in the hypothesis that once p holds it con-
tinues until q holds, and from the transient property that eventually q holds.
    Corresponding to each proof rule for transient, there is a similar rule for en-
sures. These rules and additional derived rules for en are given in Appendix A.3
(page 16).

                                         11
Example: Distributed counter, contd. We prove a progress property of
the annotated program from Section 3.3, reproduced below.

fj ::
   initially oldj , newj = 0, 0
   {true}
  loop
      {true}
         αj :: newj := oldj + 1;
      {newj = oldj + 1}
         if [ βj :: {newj = oldj + 1} ctr = oldj → ctr := newj {true}
              | γj :: {newj = oldj + 1} ctr 6= oldj → oldj := ctr {true}
            ]
      {true}
  forever

    Our ultimate goal is to prove that for any integer m if ctr = m at some
point during an execution of f , eventually ctr > m. To this end let auxiliary
variable nb be the number of threads fj for which ctr 6= oldj . We prove the
following ensures property, (E), that says that every step of f either increases
ctr or decreases nb while preserving ctr’s value. Proof uses the inheritance rule
from Appendix A.3 (page 16). For every fj and any m and N :

      ctr = m ∧ nb = N en ctr = m ∧ nb < N ∨ ctr > m in fj                      (E)

    We use the rules for en given in Appendix A.3 (page 16). First, to prove
(E) in g; h, for any g and h, it is sufficient to show that g terminates and (E) in
h. Hence, it is sufficient to show that (E) holds only for the loop in fj , because
initialization always terminates. Next, using the inheritance rule, it is sufficient
to show that (E) holds only for the body of the loop in fj . Further, since
αj always terminates, (E) needs to be shown only for the if statement. Using
inheritance, prove (E) for βj and γj . In each case, assume the precondition
ctr = m ∧ nb = N of if and the preconditions of βj and γj . The postcondition
ctr = m ∧ nb < N ∨ ctr > m is easy to see in each of the following cases:

      βj :: {ctr = m ∧ nb = N ∧ newj = oldj + 1 ∧ ctr = oldj }
                 ctr := newj
            {ctr = m ∧ nb < N ∨ ctr > m}
      γj :: {ctr = m ∧ nb = N ∧ newj = oldj + 1 ∧ ctr 6= oldj }
                oldj := ctr
            {ctr = m ∧ nb < N ∨ ctr > m}

5.3      Progress Property: Leads-to
The informal meaning of p 7→ q (read: p leads-to q) is “if p holds at any point
during an execution, q holds eventually”. Unlike en, p is not required to hold
until q holds.

                                        12
   Leads-to is defined by the following three rules, taken from Chandy and
Misra [2]. The rules are easy to justify intuitively.
                p en q
    • (basis)
                p 7→ q
                        p 7→ q , q 7→ r
    • (transitivity)
                            p 7→ r
    • (disjunction)    For any (finite or infinite) set of predicates S
                       (∀p : p ∈ S : p 7→ q)
                       (∨p : p ∈ S : p) 7→ q

   Derived rules for 7→ are given in Appendix A.4 (page 18). leads-to is not
conjunctive, nor does it obey the inheritance rule, so even if p 7→ q holds in both
f and g it may not hold in f [] g.

Example: Distributed counter, contd. We show that for the example of
Section 2.3 the counter ctr increases without bound. The proof is actually quite
simple. We use the induction rule for leads-to given in Appendix Section A.4.2.
   The goal is to show that for any integer C, true 7→ ctr > C. Below, all
properties are in f .

ctr = m ∧ nb = N en ctr = m ∧ nb < N ∨ ctr > m
     proven in Section 5.2
ctr = m ∧ nb = N 7→ ctr = m ∧ nb < N ∨ ctr > m
     Applying the basis rule of leads-to
ctr = m 7→ ctr > m
     Induction rule, use the well-founded order < over natural numbers
true 7→ ctr > C, for any integer C
     Induction rule, use the well-founded order < over natural numbers.


6     Related Work
The earliest proof method for concurrent programs appears in Owicki and
Gries [13]. The method works well for small programs, but does not scale
up for large ones. Further it is limited to proving safety properties only. There
is no notion of component specification and their composition. Lamport [10]
first identified leads-to for concurrent programs as the appropriate generaliza-
tion of termination for sequential programs (“progress” is called liveness in that
paper). Owicki and Lamport [14] is a pioneering paper.
    The first method to suggest proof rules in the style of Hoare [7], and thus a
specification technique, is due to Jones [8, 9]. Each component is annotated as-
suming that its environment preserves certain predicates. Then the assumptions
are discharged using the annotations of the various components. The method
though is restricted to safety properties only. A similar technique for message
communicating programs was proposed in Misra and Chandy [12].


                                         13
    The approaches above are all based on specifying allowed interface behav-
iors using compositional temporal logics. Since 2000, a number of proposals[6, 3]
have instead used traditional Hoare triples and resource/object invariants, but
extending state predicates to include permissions describing how locations can
be used, and suitably generalizing the Hoare rule for disjoint parallel compo-
sition. However, these proposals typically address only global safety and local
termination properties, not global progress properties (as this paper does).
    A completely different approach is suggested in the UNITY theory of Chandy
and Misra [2], and extended in Misra [11]. A restricted language for describing
programs is prescribed. There is no notion of associating assertions with pro-
gram points. Instead, the safety and progress specification of each component
is given by a set of properties that are proved directly. The specifications of
components of a program can be composed to derive program properties. The
current paper extends this approach by removing the syntactic constraints on
programs, though the safety and progress properties of UNITY are the ones
used in this paper.
    One of the essential questions in these proof methods is to propose the appro-
priate preconditions for actions. In Owicki and Gries [13] theory it is postulated
and proved. In UNITY the programmer supplies the preconditions, which are
often easily available for event-driven systems. Here, we derive preconditions
that remain valid in any environment; so there can be no assertion about shared
variables. The theory separates local precondition (obtained through annota-
tion) from global properties that may mention shared variables.
    The proof strategy described in the paper is bilateral in the following sense.
An invariant, a perpetual property, may be used to strengthen a postcondition,
a terminal property, using the invariance rule. Conversely, a terminal property,
postcondition postf of f , may be employed to deduce a transient predicate, a
perpetual property.
    Separation logic [16] has been effective in reasonong about concurrently ac-
cessed data structures. We are studying its relationship to the work described
here.

Acknowledgment I am truly grateful to Ernie Cohen of Amazon and José
Meseguer of the Univ. of Illinois at Urbana, for reading the manuscript thor-
oughly and several times, endless discussions and substantive comments that
have shaped the paper. Presenting this work at the IFIPS Working Group 2.3
and the Programming Languages lunch at the University of Texas at Austin
has sharpened my understanding; I am grateful to the students and the other
attendees, in particular to Dhananjay Raju.




                                       14
 A       Appendix: Derived Rules
 A.1       Derived Rules for co and its special cases
 The derived rules for co are given in Figure 2 and for the special cases in
 Figure 3. The rules are easy to derive; see Chapter 5 of Misra [11].

      false co q                                           p co true
           ′         ′
p co q , p co q                                       p co q , p′ co q ′
                         (conjunction)                                     (disjunction)
 p ∧ p′ co q ∧ q ′                                     p ∨ p′ co q ∨ q ′
  p co q                                                   p co q
               (lhs strengthening)                                      (rhs weakening)
p ∧ p′ co q                                              p co q ∨ q ′

                               Figure 2: Derived rules for co

     The top two rules in Figure 2 are simple properties of Hoare triples. The
 conjunction and disjunction rules follow from the conjunctivity, disjunctivity
 and monotonicity properties of the weakest precondition, see Dijkstra [4] and
 of logical implication. These rules generalize in the obvious manner to any set
 —finite or infinite— of co-properties, because weakest precondition and logical
 implication are universally conjunctive and disjunctive.
     The following rules for the special cases are easy to derive from the definition
 of stable , invariant and constant . Special Cases of co

     • (stable conjunction, stable disjunction)
           p co q , stable r
             p ∧ r co q ∧ r
             p ∨ r co q ∨ r
                                         stable p , stable q
     • (Special case of the above)
                                            stable p ∧ q
                                            stable p ∨ q
           invariant p , invariant q
     •
                invariant p ∧ q
                invariant p ∨ q
               {r} f {stable p }                                 {r} f {constant e }
     •
                  {r ∧ p} f {p}                                   {r ∧ e = c} f {e = c}
     • (constant formation)       Any expression built out of constants is constant.

                  Figure 3: Derived rules for the special cases of co




                                             15
A.2     Derived Rules for transient
   • transient false.
   • (Strengthening) Given transient p, transient p ∧ q for any q.
    To prove transient false use the basis rule. The proof of the strengthening
rule uses induction on the number of applications of the proof rules in deriving
transient p. The proof is a template for proofs of many derived rules for ensures
and leads-to. Consider the different ways by which transient p can be proved
in a component. Basis rule gives the base case of induction.
  1. (Basis) In component f , p is of the form p′ ∧ ¬postf for some p′ . Then in
     some annotation of f where action b → α has the precondition pre:
     (1) pre ∧ p′ ⇒ b, and (2) {pre ∧ p′ } α {¬p′ }.
     (1’) From predicate calculus pre ∧ p′ ∧ q ⇒ b, and
     (2’) from Hoare logic {pre ∧ p′ ∧ q} α {¬p′ }. Applying the basis rule,
     transient p′ ∧ q ∧ ¬postf , i.e., transient p ∧ q.
  2. (Sequencing) In f ; g, transient p ∧ ¬postf in f and transient p in g. In-
     ductively, transient p∧q ∧¬postf in f and transient p∧q in g. Applying
     the sequencing rule, transient p ∧ q.
  3. (Concurrency, Inheritance) Similar proofs.

A.3     Derived Rules for en
A.3.1   Counterparts of rules for transient
This set of derived rules correspond to the similar rules for transient. Their
proofs are straight-forward using the definition of en.
   • (Basis)
                                   {r} f {s}
        For every action b → α with precondition pre in the annotation :
                              pre ∧ p ∧ ¬q ⇒ b
                             {pre ∧ p ∧ ¬q} α {q}
                          {r} f {p en p ∧ s ∨ q   s}

   • (Sequencing)

            {r} f {p en p ∧ postf ∨ q       postf }
                  {postf } g {p en q    }
                  {r} f ; g {p en q     }
   • (Concurrency)

                 p en q in f
            p ∧ ¬q co p ∨ q in g
               p en q in f [] g

                                        16
   • (Inheritance) Assuming the proof rule at left the inheritance proof rule at
     right can be asserted.
                                            Assert:
              (∀i :: {ri } fi {si })        (∀i :: {ri } fi {p en q    si })
       Given:
                    {r} f {s}                     {r} f {p en q     s}

A.3.2     Additional derived rules
The following rules are easy to verify by expanding each ensures property by its
definition, and using the derived rules for transient and co. We show one such
proof, for the PSP rule. Observe that ensures is only partially conjunctive and
not disjunctive, unlike co.
                     p⇒q
  1. (implication)
                     p en q
     Consequently, false en q and p en true for any p and q.
                               p en q
  2. (rhs weakening)
                             p en q ∨ q ′
                                   p en q
                                   p′ en q
  3. (partial conjunction)
                                 p ∧ p′ en q
                              p ∧ ¬q ⇒ p′ ⇒ p ∨ q
  4. (lhs manipulation)
                               p en q ≡ p′ en q
     Observe that p ∧ ¬q ≡ p′ ∧ ¬q and p ∨ q ≡ p′ ∨ q. So, p and q are
     interchangeable in all the proof rules. As special cases, p ∧ ¬q en q ≡
     p en q ≡ p ∨ q en q.
  5. (PSP) The general rule is at left, and a special case at right using stable r
     as r co r.

           (PSP)                             (Special case)
                  p en q                        p en q
                  r co s                        stable r
         p ∧ r en (q ∧ r) ∨ (¬r ∧ s)         p ∧ r en q ∧ r
  6. (Special case of Concurrency)
          p en q in f
         stable p in g
                                                                                ✷
        p en q in f [] g
Proof of (PSP): From the hypotheses:
    transient p ∧ ¬q                                                           (1)
    p ∧ ¬q co p ∨ q                                                            (2)
    r co s                                                                     (3)
   We have to show:

                                        17
    transient p ∧ r ∧ ¬(q ∧ r) ∧ ¬(¬r ∧ s)                                         (4)
    p ∧ r ∧ ¬(q ∧ r) ∧ ¬(¬r ∧ s) co p ∧ r ∨ q ∧ r ∨ ¬r ∧ s                         (5)
   First, simplify the term on the rhs of (4) and lhs of (5) to p ∧ r ∧ ¬q ∧ s.
Proof of (4) is then immediate, as a strengthening of (1). For the proof of (5),
apply conjunction to (2) and (3) to get:

          p ∧ r ∧ ¬q co p ∧ s ∨ q ∧ s
      ≡ {expand both terms in rhs}
          p ∧ r ∧ ¬q co p ∧ r ∧ s ∨ p ∧ ¬r ∧ s ∨ q ∧ r ∧ s ∨ q ∧ ¬r ∧ s
      ⇒ {lhs strengthening and rhs weakening}
          p ∧ r ∧ ¬q ∧ s co p ∧ r ∨ q ∧ r ∨ ¬r ∧ s

A.4       Derived Rules for leads-to
The rules are taken from Misra [11] where the proofs are given. The rules are
divided into two classes, lightweight and heavyweight. The former includes rules
whose validity are easily established; the latter rules are not entirely obvious.
Each application of a heavyweight rule goes a long way toward completing a
progress proof.

A.4.1   Lightweight rules
                   p ⇒ q
  1. (implication)
                   p 7→ q
  2. (lhs strengthening, rhs weakening)
          p 7→ q
       p′ ∧ p 7→ q
       p 7→ q ∨ q ′

                           (∀i :: pi 7→ qi )
  3. (disjunction)
                       (∀i :: pi ) 7→ (∀i :: qi )

      where i is quantified over an arbitrary finite or infinite index set, and pi , qi
      are predicates.
                       p 7→ q ∨ r , r 7→ s
  4. (cancellation)
                           p 7→ q ∨ s

A.4.2     Heavyweight rules
                        p 7→ false
  1. (impossibility)
                            ¬p
  2. (PSP) The general rule is at left, and a special case at right using stable r
     as r co r.




                                          18
          (PSP)                              (Special case)
                 p 7→ q                         p 7→ q
                 r co s                         stable r
        p ∧ r 7→ (q ∧ r) ∨ (¬r ∧ s)          p ∧ r 7→ q ∧ r
   3. (induction) Let M be a total function from program states to a well-
      founded set (W, ≺). Variable m in the following premise ranges over W .
      Predicates p and q do not contain free occurrences of variable m.

           (∀m :: p ∧ M = m 7→ (p ∧ M ≺ m) ∨ q)
                           p 7→ q

   4. (completion) Let pi and qi be predicates where i ranges over a finite set.
              (∀i ::
                  pi 7→ qi ∨ b
                  qi co qi ∨ b
              )
       (∀i :: pi ) 7→ (∀i :: qi ) ∨ b

A.4.3    Lifting Rule
This rule permits lifting a leads-to property of f to f [] g with some modifi-
cations. Let x be a tuple of some accessible variables of f that includes all
variables that f shares with g. Below, X is a free variable, therefore universally
quantified. Predicates p and q name accessible variables of f and g. Clearly,
any local variable of g named in p or q is treated as a constant in f .

                 p 7→ q in f
        r ∧ x = X co x = X ∨ ¬r in g
(L)
             p 7→ q ∨ ¬r in f [] g
    An informal justification of this rule is as follows. Any p-state in which
¬r holds, q ∨ ¬r holds. We show that in any execution of f [] g starting in a
(p ∧ r)-state q or ¬r holds eventually. If r is falsified by a step of f then ¬r
holds. Therefore, assume that every step of f preserves r. Now if any step of
g changes the value of x then it falsifies r from the antecedent, i.e., ¬r holds.
So, assume that no step of g modifies x. Then g does not modify any accessible
variable of f ; so, f is oblivious to the presence of g, and it establishes q.
    As a special case, we can show

                   p 7→ q in f
(L’)
        p ∧ x = M 7→ q ∨ x 6= M in f [] g
    The formal proof of (L) is by induction on the structure of the proof of
p 7→ q in f . See
http://www.cs.utexas.edu/users/psp/unity/notes/UnionLiftingRule.pdf
for details.


                                        19
B     Example: Mutual exclusion
We prove a coarse-grained version of a 2-process mutual exclusion program due
to Peterson [15]. The given program has a finite number of states, so it is
amenable to model-checking. In fact, model-checking is a simpler alternative
to an axiomatic proof. We consider this example primarily because this is an
instance of a tightly-coupled system where the codes of all the components are
typically considered together to construct a proof. In contrast, we construct a
composable specification of each component and combine the specifications to
derive a proof.

B.1     Program
The program has two processes M and M ′ . Process M has two local boolean
variables, try and cs where try remains true as long as M is attempting to enter
the critical section or in it and cs is true as long as it is in the critical section;
M ′ has try ′ and cs′ . They both have access to a shared boolean variable turn.
It simplifies coding and proof to postulate an additional boolean variable turn′
that is the complement of turn, i.e., turn′ ≡ ¬turn.
    The global initialization and the code for M , along with a local annota-
tion, is given below. The code of M ′ is the dual of M , obtained by replacing
each variable in M by its primed counterpart. Henceforth, the primed and the
unprimed versions of the same variable re duals of each other.
    The “unrelated computation” below refers to computation preceding the
attempt to enter the critical section that does not access any of the relevant
variables. This computation may or may not terminate in any iteration.

    initially cs, cs′ = false, false — global initialization

    M : initially try = false
    {¬try, ¬cs}
    loop
       — unrelated computation that may not terminate;
       {¬try, ¬cs} α:       try, turn := true, true;
       {try, ¬cs}      β:   ¬try ′ ∨ turn′ → cs := true; — Enter critical section
       {try, cs}       γ: try, cs := false, false — Exit critical section
    forever

   Given that M ′ is the dual of M , from any property of M obtain its dual as
a property of M ′ . And, for any property of M [] M ′ its dual is a property of
M ′ [] M , i.e., M [] M ′ , thus reducing the proof length by around half.

Remarks on the program The given program is based on a simplification
of an algorithm in Peterson [15]. In the original version the assignment in α


                                         20
may be decoupled to the sequence try := true; turn := true. The tests in β
may be made separately for each disjunct in arbitrary order. Action γ may
be written in sequential order try := false; cs := false. These changes can be
easily accommodated within our proof theory by introducing auxiliary variables
to record the program control.

B.2     Safety and progress properties
It is required to show in M [] M ′ (1) the safety property: both M and M ′ are
never simultaneously within their critical sections, i.e., invariant ¬(cs ∧ cs′ ),
and (2) the progress property: any process attempting to enter its critical section
will succeed eventually, i.e., try 7→ cs and try ′ 7→ cs′ ; we prove just try 7→ cs
since its dual also holds.

B.2.1    Safety proof: invariant ¬(cs ∧ cs′ )
We prove below:
    invariant cs ⇒ try in M [] M ′                                            (S1)
    invariant cs′ ∧ try ⇒ turn in M [] M ′                                    (S2)
   Mutual exclusion is immediate from (S1) and (S2), as follows.
          cs ∧ cs′
      ⇒ {from (S1) and its dual}
          cs ∧ try ∧ cs′ ∧ try ′
      ≡ {rewriting}
          (cs′ ∧ try) ∧ (cs ∧ try ′ )
      ⇒ {from (S2) and its dual}
          turn ∧ turn′
      ≡ {turn and turn′ are complements}
          false

Proofs of (S1) and (S2) First, we show the following stable properties of
M , which constitute its safety specification, from which (S1) and (S2) follow.

    stable cs ⇒ try in M                                                      (S3)
    stable try ⇒ turn in M                                                    (S4)
    stable cs ∧ try ′ ⇒ turn′ in M                                            (S5)

    The proofs of (S3), (S4) and (S5) are entirely straight-forward, but each
property has to be shown stable for each action. We show the proofs in Table 1,
where each row refers to one of the predicates in (S3 – S5) and each column
to an action. An entry in the table is either: (1) “post: p” claiming that since
p is a postcondition of this action the given predicate is stable, or (2) “unaff.”
meaning that the variables in the given predicate are unaffected by this action
execution. The only entry that is left out is for the case that β preserves (S5):
cs ∧ try ′ ⇒ turn′ ; this is shown as follows. The guard of β can be written as

                                        21
try ′ ⇒ turn′ and execution of β affects neither try ′ nor turn′ , so try ′ ⇒ turn′
is a postcondition, and so is cs ∧ try ′ ⇒ turn′ .

                                    α                 β                 γ
   (S3)        cs ⇒ try         post: ¬cs        post: try         post: ¬cs
   (S4)       try ⇒ turn        post: turn    unaff.: try, turn    post: ¬try
   (S5)    cs ∧ try ′ ⇒ turn′   post: ¬cs         see text         post: ¬cs

                      Table 1: Proofs of (S3), (S4) and (S5)


   Now we are ready to prove (S1) and (S2). The predicates in (S1) and (S2)
hold initially because initially cs, cs′ = false, false. Next, we show these predi-
cates to be stable. The proof is compositional, by proving each predicate to be
stable in both M and M ′ . The proof is simplified by duality of the codes.

• (S1) stable cs ⇒ try in M [] M ′ :
      stable cs ⇒ try in M       , (S3)
      stable cs ⇒ try in M ′     , cs and try are constant in M ′
                               ′
      stable cs ⇒ try in M [] M , Inheritance rule

• (S2) stable cs′ ∧ try ⇒ turn in M [] M ′ :
      stable try ⇒ turn in M                     , (S4)
      stable cs′ ∧ try ⇒ turn in M               , cs′ constant in M
      stable cs′ ∧ try ⇒ turn in M ′             , dual of (S5)
      stable cs′ ∧ try ⇒ turn in M [] M ′        , Inheritance rule

B.2.2     Progress proof: try 7→ cs in M [] M ′
First, we prove a safety property:
    try ∧ ¬cs co try ∨ cs in M [] M ′                                           (S6)
    To prove (S6) first prove try∧¬cs co try∨cs in M , which is entirely straight-
forward. Now variables try and cs are local to M , therefore stable try ∧ ¬cs in
M ′ , and through rhs weakening, try ∧ ¬cs co try ∨ cs in M ′ . Using inheritance
(S6) follows.                                                                   ✷
    Next we prove a progress property:

    try ∧ (¬try ′ ∨ turn′ ) 7→ ¬try in M [] M ′                                  (P)

    First, prove try ∧(¬try ′ ∨turn′ ) en ¬try in M , using the sequencing rule for
 en ; intuitively, in a try ∧ (¬try ′ ∨ turn′ )-state the program control is never at
α, execution of β terminates while preserving try ∧(¬try ′ ∨turn′ ), and execution
of γ establishes ¬try.
    Using duality on (S4) get stable try ′ ⇒ turn′ in M ′ , i.e., stable ¬try ′ ∨
turn′ in M ′ . And try is local to M , so stable try in M ′ . Conjoining these two

                                         22
properties, stable try ∧ (¬try ′ ∨ turn′ ) in M ′ . Apply the concurrency rule for
 en with stable try ∧ (¬try ′ ∨ turn′ ) in M ′ and try ∧ (¬try ′ ∨ turn′ ) en ¬try
in M to conclude that try ∧ (¬try ′ ∨ turn′ ) en ¬try in M [] M ′ .
   Now apply the basis rule for 7→ to conclude the proof of (P).                 ✷

    Proof of try 7→ cs in M [] M ′ : All the properties below are in M [] M ′ .
    Conclude from (P), using lhs strengthening,
     try ∧ ¬try ′ 7→ ¬try                                                      (P1)
     try ∧ turn′ 7→ ¬try                                                       (P2)
    The main proof:

      try ′ ∧ turn 7→ ¬try ′          , duality applied to (P2)
      try ∧ try ′ ∧ turn 7→ ¬try ′    , lhs strengthening
      try ∧ ¬(try ′ ∧ turn) 7→ ¬try   , rewriting (P) using ¬turn ≡ turn′
      try 7→ ¬try ∨ ¬try ′            , disjunction of the above two
      try 7→ ¬try ∨ (¬try ′ ∧ try)    , rewriting the rhs
      try 7→ ¬try                     , cancellation using (P1)
      try ∧ ¬cs co try ∨ cs           , (S6)
      try ∧ ¬cs 7→ cs                 , PSP of above two
      try 7→ cs                       , disjunction with try ∧ cs 7→ cs


C     Example: Associative, Commutative fold
We consider a recursively defined program f where the code of f1 is given and
fk+1 is defined to be f1 [] fk . This structure dictates that the specification sk
of fk must permit proof of (1) s1 from the code of f1 , and (2) sk+1 from s1
and sk , using induction on k. This example illustrates the usefulness of the
various composition rules for the perpetual properties. The program is not easy
to understand intuitively; it does need a formal proof.

C.1     Informal Problem Description
Given is a bag u on which ⊕ is a commutative and associative binary operation.
Define Σu, fold of u, to be the result of applying ⊕ repeatedly to all pairs of
elements of u until there is a single element. It is required to replace all the
elements of u by Σu. Program fk , for k ≥ 1, decreases the size of u by k while
preserving its fold. That is, fk transforms the original bag u′ to u such that:
(1) Σu = Σu′ , and (2) |u| + k = |u′ |, provided |u′ | > k, where |u| is the size of
u. Therefore, execution of fn−1 , where n is the size of u′ and n > 1, computes
a single value in u that is the fold of the initial bag.
    Below, get(x) removes an item from u and assigns its value to variable x.
This operation can be completed only if u has an item. And put(x ⊕ y), a
non-blocking action, stores x ⊕ y in u. The formal semantics of get and put are
given by the following assertions where u′ is constant:


                                        23
    {u = u′ } get(z) {u′ = u ∪ {z}}
    {u = u′ } put(z) {u = u′ ∪ {z}}
   The fold program fk for all k, k ≥ 1, is given by:
    f1 = |u| > 0 → get(x); |u| > 0 → get(y); put(x ⊕ y)
    fk+1 = f1 [] fk , k ≥ 1
   Specification and proof of safety properties appear in Section C.2, next, and
progress properties in Section C.3. Observe that

C.2     Terminal property
The relevant safety property of fk , for all k, k ≥ 1, is a terminal property:
    {u = u′ } fk {Σu = Σu′ , |u| + k = |u′ |}
   This property can not be proved from a local annotation alone because it
names the shared variable u in its pre- and postconditions. We suggest an
enhanced safety property using certain auxiliary variables.

Auxiliary variables      The following auxiliary variables of fk are local to it:

  1. wk : the bag of items removed from u that are, as yet, unfolded. That is,
     every get from u puts a copy of the item in wk , and put(x ⊕ y) removes x
     and y from wk . Initially wk = {}.
  2. nhk : the number of halted threads where a thread halts after completing a
     put. A get does not affect nhk and a put increments it. Initially nhk = 0.

    Introduction of any auxiliary variable auxk for fk follows a pattern: (1)
specify the initial value of auxk , (2) define aux1 by modifying the code of f1 ,
corresponding to the basis of a recursive definition, and (3) define auxk+1 in
terms of aux1 and auxk .
    We adopt this pattern for defining wk and nhk for all k, k ≥ 1. First, the
initial values of wk and nhk are {} and 0, respectively. Second, w1 and nh1 are
defined below in f1 . Third, wk+1 = w1 ∪ wk and nhk+1 = nh1 + nhk , for all k.
The modified program for f1 is as follows where h· · · i is an action.

    f1 = |u| > 0 → hget(x); w1 := w1 ∪ {x}i;
        |u| > 0 → hget(y); w1 := w1 ∪ {y}i;
        hput(x ⊕ y); w1 := w1 − {x, y}; nh1 := 1i

Note: The definition of auxiliary variables is problematic for nh2 , for instance;
by definition, nh2 = nh1 + nh1 . However, these are two different instances of
nh1 referring to the local variables of the two instances of f1 in f2 . This is not
a problem in the forthcoming proofs because the proofs always refer to indices
1, k and k + 1, and, nhk is treated as being different from nh1 .


                                        24
Specification of safety property The safety specification of fk , for all k,
k ≥ 1, is given by:

          {u = u′ , wk = {}, nhk = 0}
                        fk
    {constant Σ(u ∪ wk ), constant |u| + |wk | + nhk
       wk = {}, nhk = k}                                                        (S)


• Proof of (S) for f1 : Construct the following local annotation of f1 .

            {w1 = {}, nh1 = 0}
    |u| > 0 → hget(x); w1 := w1 ∪ {x}i;
            {w1 = {x}, nh1 = 0}
       |u| > 0 → hget(y); w1 := w1 ∪ {y}i;
            {w1 = {x, y}, nh1 = 0}
          hput(x ⊕ y); w1 := w1 − {x, y}; nh1 := 1i
            {w1 = {}, nh1 = 1}

    The perpetual and terminal properties of f1 in (S) are easily shown using
this annotation and employing the semantics of get and put.

• Proof of (S) for fk+1 : by induction on k. Use the following abbreviations in
the proof.

    ak ≡ wk = {} ∧ nhk = 0
    bk ≡ constant Σ(u ∪ wk ), constant |u| + |wk | + nhk
    ck ≡ wk = {} ∧ nhk = k

     {a1 } f1 {b1      c1 }                    , from the annotation of f1
     {a1 } f1 {bk+1       c1 }                 , wk , nhk constant in f1         (1)
     {ak } fk {bk      ck }                    , inductive hypothesis
     {ak } fk {bk+1        ck }                , w1 , nh1 constant in fk         (2)
     {a1 ∧ ak } f1 [] fk {c1 ∧ ck }            , join proof rule on (1,2)
     {a1 ∧ ak } f1 [] fk {bk+1        c1 ∧ ck }, inheritance on (1,2)
     {ak+1 } fk+1 {bk+1         ck+1 }         , ak+1 ⇒ a1 ∧ ak and c1 ∧ ck ⇒ ck+1

    The terminal property {u = u′ } fk {Σu = Σu′ , |u| + k = |u′ |} follows
from (S) as follows. The initial values of Σ(u ∪ wk ) and |u| + |wk | + nhk are,
respectively, Σu′ and |u′ |, so deduce that invariant Σ(u ∪ wk ) = Σu′ and also
invariant |u| + |wk | + nhk = |u′ |. Given that fk is a program whose terminal
properties are being proved, we may apply the invariance rule of Section 4.3
with these invariants. So, deduce Σu = Σu′ , |u| + k = |u′ | as a postcondition
of fk with the given precondition.



                                        25
C.3     Specification and proof of progress property
The relevant progress property is that if u has more than k elements initially,
fk terminates eventually. That is, |u′ | > k 7→ nhk = k in fk . Initially |u′ | =
|u| + |wk | + nhk , so it is enough to prove |u| + |wk | + nhk > k 7→ nhk = k.
Abbreviate |u| + |wk | + nhk > k by pk and nhk = k by qk so that for all k,
k ≥ 1, the required progress property is:

    pk 7→ qk in fk                                                                (P)

   The proof of (P) is by induction on k, as shown in Sections C.3.1 and C.3.2.

C.3.1    Progress proof, p1 7→ q1 in f1
We show that p1 en q1 , from which p1 7→ q1 follows by applying the basis rule
of leads-to. We reproduce the annotation of f1 for easy reference.

            {w1 = {}, nh1 = 0}
    |u| > 0 → hget(x); w1 := w1 ∪ {x}i;
            {w1 = {x}, nh1 = 0}
       |u| > 0 → hget(y); w1 := w1 ∪ {y}i;
            {w1 = {x, y}, nh1 = 0}
          hput(x ⊕ y); w1 := w1 − {x, y}; nh1 := 1i
            {w1 = {}, nh1 = 1}

    Next, prove p1 en q1 using the sequencing rule of en, from Section A.3.1.
It amounts to showing that if p1 holds before any action then the action is
effectively executed and q1 holds on completion of f1 . As shown in Section C.2
p1 is stable, and from the annotation q1 holds on completion of f1 . Therefore, it
suffices to show that if p1 holds initially then every action is effectively executed.
The put action is always effectively executed. Using the given annotation, the
verification conditions for the two get actions are shown below in full:

    w1 = {} ∧ nh1 = 0 ∧ |u| + |w1 | + nh1 > 1 ⇒ |u| > 0, and
    w1 = {x} ∧ nh1 = 0 ∧ |u| + |w1 | + nh1 > 1 ⇒ |u| > 0

These are easily proved.

C.3.2    Progress proof, pk+1 7→ qk+1 in fk+1
The main part of the proof uses the observation that every action, put and
get, reduces a well-founded metric. The metric is the pair (|u| + |wk |, |u|) and
the order relation is lexicographic. Clearly, the metric is bounded from below
because each set size is at least 0. The crux of the proof is to show that if
program fk is not terminated there is some action that can be executed, i.e.,
there is no deadlock. Henceforth, abbreviate (|u| + |wk |, |u|) by zk and any pair
of non-negative integers by n.


                                         26
     First, observe that zk can only decrease or remain the same in fk , that is,
stable zk  n in fk , where  is the lexicographic ordering. The proof is by
induction on k and it follows the same pattern as all other safety proofs. In f1 ,
informally, every effective get preserves |u| + |w1 | and decreases |u|, and a put
decreases |u|+ |w1 |. For the proof in fk+1 : from above, stable z1  n in f1 , and
inductively stable zk  n in fk . Since constant wk in f1 and constant w1 in
fk , stable zk+1  n in both f1 and fk . Apply the inheritance rule to conclude
that stable zk+1  n in fk+1 .
     The progress proof of pk+1 7→ qk+1 in fk+1 is based on two simpler progress
results, (P1) and (P2). (P1) says that any execution starting from pk+1 re-
sults in the termination of either f1 or fk . And, (P2) says that once either
f1 or fk terminates the other component also terminates. The desired result,
pk+1 7→ qk+1 , follows by using transitivity on (P1) and (P2).

    pk+1 7→ pk+1 ∧ (q1 ∨ qk ) in fk+1                                         (P1)
    pk+1 ∧ (q1 ∨ qk ) 7→ qk+1 in fk+1                                         (P2)

    The proofs mostly use the derived rules of leads-to from Section A.4. Note
that zk+1 includes all the shared variables between f1 and fk , namely u, so that
the lifting rule can be used with zk+1 . Also note that
pk+1 ⇒ (p1 ∨ pk ), pk+1 ∧ q1 ⇒ pk , pk+1 ∧ qk ⇒ p1 and q1 ∧ qk ⇒ qk+1 . As shown
in Section C.2 pk is constant, hence stable, and qk is also stable in fk .

Proof of (P1) pk+1 7→ pk+1 ∧ (q1 ∨ qk ) in fk+1 : Below all properties are in
fk+1 . Lifting rule refers to rule (L’) of Section A.4.3. We have already shown
p1 7→ q1 and, inductively, pk 7→ qk .

    p1 ∧ zk+1 = n 7→ q1 ∨ zk+1 6= n           , Lifting rule on p1 7→ q1 in f1
    pk ∧ zk+1 = n 7→ qk ∨ zk+1 6= n           , Lifting rule on pk 7→ qk in fk
    (p1 ∨ pk ) ∧ zk+1 = n 7→ (q1 ∨ qk ) ∨ zk+1 6= n
                                              , disjunction
    (p1 ∨ pk ) ∧ zk+1 = n 7→ (q1 ∨ qk ) ∨ zk+1 ≺ n
                                              , (PSP) with stable zk+1  n
    pk+1 ∧ (p1 ∨ pk ) ∧ zk+1 = n 7→ pk+1 ∧ (q1 ∨ qk ) ∨ pk+1 ∧ zk+1 ≺ n
                                              , conjunction with stable pk+1
    pk+1 ∧ zk+1 = n 7→ pk+1 ∧ zk+1 ≺ n ∨ pk+1 ∧ (q1 ∨ qk )
                                              , pk+1 ⇒ (p1 ∨ pk )
    pk+1 7→ pk+1 ∧ (q1 ∨ qk )                 , induction rule of leads-to




                                        27
Proof of (P2) pk+1 ∧ (q1 ∨ qk ) 7→ qk+1 in fk+1 : Below all properties are in
fk+1 .

    p1 ∧ zk+1 = n 7→ q1 ∨ zk+1 6= n         , Lifting rule on p1 7→ q1 in f1
    p1 ∧ zk+1 = n 7→ q1 ∨ zk+1 ≺ n          , conjunction with stable zk+1  n
    qk ∧ p1 ∧ zk+1 = n 7→ qk ∧ q1 ∨ qk ∧ zk+1 ≺ n
                                            , conjunction with stable qk
    pk+1 ∧ qk ∧ p1 ∧ zk+1 = n 7→ pk+1 ∧ qk ∧ q1 ∨ pk+1 ∧ qk ∧ zk+1 ≺ n
                                            , conjunction with stable pk+1
    pk+1 ∧ qk ∧ zk+1 = n 7→ pk+1 ∧ qk ∧ zk+1 ≺ n ∨ pk+1 ∧ qk ∧ q1
                                            , pk+1 ∧ qk ⇒ p1
    pk+1 ∧ qk 7→ pk+1 ∧ q1 ∧ qk             , induction rule of leads-to
    pk+1 ∧ qk 7→ q1 ∧ qk                    , rhs weakening
    pk+1 ∧ q1 7→ q1 ∧ qk                    , similarly
    pk+1 ∧ (q1 ∨ qk ) 7→ qk+1               , disjunction and q1 ∧ qk ⇒ qk+1


D     References
References
 [1] Robert D. Blumofe. Executing Multithreaded Programs Efficiently. PhD
     thesis, Massachusetts Institute Of Technology, September 1995.
 [2] K. Mani Chandy and Jayadev Misra. Parallel Program Design: A Foun-
     dation. Addison-Wesley, 1988.
 [3] Ernie Cohen, Michal Moskal, Wolfram Schulte, and Stephan Tobies. Local
     verification of global invariants in concurrent programs. In Computer Aided
     Verification, 22nd International Conference, CAV 2010, Edinburgh, UK,
     July 15-19, 2010. Proceedings, pages 480–494, 2010.

 [4] Edsger W. Dijkstra. Guarded commands, nondeterminacy, and the formal
     derivation of programs. Communications of the ACM, 8:453–457, 1975.
 [5] E.W. Dijkstra. Cooperating sequential processes. In F. Genuys, editor,
     Programming Languages, pages 43–112. Academic Press, 1968.
 [6] Thomas Dinsdale-Young, Mike Dodds, Philippa Gardner, Matthew J.
     Parkinson, and Viktor Vafeiadis. Concurrent abstract predicates. In Pro-
     ceedings of the 24th European Conference on Object-oriented Programming,
     ECOOP’10, pages 504–528, Berlin, Heidelberg, 2010. Springer-Verlag.
 [7] C.A.R. Hoare. An axiomatic basis for computer programming. Communi-
     cations of the ACM, 12:576–580,583, 1969.
 [8] C. B. Jones. Specification and design of (parallel) programs. In Proceedings
     of IFIP83, pages 321–332. North-Holland, 1983.


                                       28
 [9] C. B. Jones. Tentative steps toward a development method for interfering
     programs. TOPLAS, 5(4):596–619, 1983.
[10] Leslie Lamport. Proving the correctness of multiprocess programs. IEEE
     Trans. on Software Engineering, SE-3(2):125–143, Mar 1977.
[11] Jayadev Misra. A Discipline of Multiprogramming. Monographs in Com-
     puter Science. Springer-Verlag New York Inc., New York, 2001.
[12] Jayadev Misra and K. Mani Chandy. Proofs of networks of processes. IEEE,
     SE,7(4):417–426, July 1981.
[13] S. Owicki and D. Gries. Verifying properties of parallel programs: an
     axiomatic approach. Communications of the ACM, 19:279–285, May 1976.
[14] S. Owicki and Leslie Lamport. Proving liveness properties of concurrent
     programs. ACM Transactions on Programming Languages and Systems,
     4(3):455–495, July 1982.
[15] G.L. Peterson. Myths about the mutual exclusion problem. Information
     Processing Letters, 12(3):115–116, June 1981.
[16] John C. Reynolds. Separation logic: A logic for shared mutable data struc-
     tures. In Proceedings of the 17th Annual IEEE Symposium on Logic in
     Computer Science, IEEE Computer Society, Washington, DC, USA, 2002.




                                      29
