                                               Safety Verification and Refutation by
                                         k-invariants and k-induction (extended version)⋆

                                                 Martin Brain, Saurabh Joshi, Daniel Kroening, Peter Schrammel

                                                                        University of Oxford, UK
arXiv:1506.05671v2 [cs.LO] 29 Jun 2015




                                                Abstract. Most software verification tools can be classified into one of
                                                a number of established families, each of which has their own focus and
                                                strengths. For example, concrete counterexample generation in model
                                                checking, invariant inference in abstract interpretation and completeness
                                                via annotation for deductive verification. This creates a significant and
                                                fundamental usability problem as users may have to learn and use one
                                                technique to find potential problems but then need an entirely different
                                                one to show that they have been fixed. This paper presents a single,
                                                unified algorithm kIkI, which strictly generalises abstract interpretation,
                                                bounded model checking and k-induction. This not only combines the
                                                strengths of these techniques but allows them to interact and reinforce
                                                each other, giving a ‘single-tool’ approach to verification.


                                         1     Introduction

                                         The software verification literature contains a wide range of techniques which
                                         can be used to prove or disprove safety properties. These include:

                                         Bounded Model Checking Given sufficient time and resource, BMC will give
                                             counterexamples for all false properties, which are often of significant value
                                             for understanding the fault. However only a small proportion of true prop-
                                             erties can be proven by BMC.
                                         k-Induction Generalising Hoare logic’s ideas of loop invariants, k-induction can
                                             prove true properties, and, in some cases provide counterexamples to false
                                             ones. However it requires inductive invariants, which can be expensive (in
                                             terms of user time, expertise and maintenance).
                                         Abstract Interpretation The use of over-approximations makes it easy to
                                             compute invariants which allow many true propositions to be proven. How-
                                             ever false properties and true-but-not-provable properties may be indistin-
                                             guishable. Tools may have limited support for a more complete analysis.

                                            The range and variety of tools and techniques available is a sign of a healthy
                                         and vibrant research community but presents challenges for non-expert users.
                                         ⋆
                                             This research was supported by the ARTEMIS Joint Undertaking under grant
                                             agreement number 295311 (VeTeSS), the Toyota Motor Corporation and ERC
                                             project 280053 (CPROVER).
The choice of which tools to use and where to expend effort depends on whether
the properties are true or not – which is exactly what they want to find out.
    To build a robust and usable software verification system it is necessary
to combine a variety of techniques. One option would be to run a series of
independent tools, in parallel (as a portfolio, for example) or in some sequential
order. However this limits the information that can be exchanged between the
algorithms – what is needed is a genuine compound rather than a simple mixture.
Another option would be to use monolithic algorithms such as CEGAR [5],
IMPACT [21] or IC3/PDR [3,18] which combine some of the ideas of simpler
systems. These are difficult to implement well as their components interact in
complex and subtle ways. Also they require advanced solver features such as
interpolant generation that are not widely available for all theories (bit-vectors,
arrays, floating-point, etc.). In this paper, we argue for a compound with simple
components and well-understood interaction.
    This paper draws together a range of well-known techniques and combines
them in a novel way so that they strengthen and reinforce each other. k-induction
[28] uses syntactically restricted or simple invariants (such as those generated by
abstract interpretation) to prove safety. Bounded model checking [2] allows us
to test k-induction failures to see if they are real counter-examples or, if not, to
build up a set of assumptions about system behaviour. Template-based abstract
interpretation is used for invariant inference [25,24,16] with unrolling produc-
ing progressively stronger invariants. Using a solver and templates to generate
invariants allows the assumptions to be used without the need for backwards
propagators and ‘closes the loop’ allowing the techniques to strengthen each
other. Specifically, the paper makes the following contributions:
 1. A new, unified, simple and elegant algorithm, kIkI, for integrated invariant
     inference and counterexample generation is presented in Section 2. Incremen-
     tal bounded model checking, k-induction and classical over-approximating
     abstract interpretation are shown to be restrictions of kIkI.
 2. The techniques required to efficiently implement kIkI are given in Section 3
     and an implementation, 2LS, is described in Section 4.
 3. A series of experiments are given in Section 5. We show that kIkI verified
     more programs and is faster than a portfolio approach using incremental
     BMC, k-induction and abstract interpretation, showing genuine synergy be-
     tween components.

2     Algorithm Concepts
This section reviews the key concepts behind kIkI. Basic familiarity with tran-
sition systems and first and second order logic will be assumed. As we intend to
use kIkI to verify software using bit-vectors, we will focus on finite state systems.

2.1   Program Verification as Second Order Logic
To ease formalisation we view programs as symbolic transition systems. The
state of a program is described by a logical interpretation with logical variables
corresponding to each program variable, including the program counter. Formu-
lae can be used to describe sets of states – the states in the set are the models
of the formulae. Given x, a vector of variables, Start (x) is the predicate describ-
ing the start states. A transition relation, Trans(x, x′ ) is formula describing a
relation between pairs of such interpretations which describes the (potentially
non-deterministic) progression relations between states. From these we can de-
rive the set of reachable states as the least fixed-point of the transition relation
starting from the states described by Start(x). Although this set is easily de-
fined, computing a predicate that describes it (from Start and Trans) is often
difficult and we will focus on the case when it is not practical. Instead inductive
invariant are used; Inv is an inductive invariant if it has the following property:

                    ∀x0 , x1  (Inv (x0 ) ∧ Trans(x0 , x1 ) ⇒ Inv(x1 ))                   (1)

Each inductive invariant is a description of a fixed-point of the transition relation
but is not necessarily guaranteed to be the least one, nor is it guaranteed to
include Start (x) although many of the inductive invariants we use will do. For
example, the predicate true is an inductive invariant for all systems as it describes
the complete state space. From an inductive invariant we can find loop invariants
and function and thread summaries by projecting on to a subset of variables x.
    Many verification tasks can be reduced to showing that the reachable states
do not intersect with a set of error states, denoted by the predicate Err (x). Tech-
niques for proving systems safe can be seen as computing an inductive invariant
that is disjoint from the error set. Using existential second order quantification
(denoted ∃2 ) we can formalise this as:

               ∃2 Inv  ∀x0 , x1  (Start(x0 ) ⇒ Inv (x0 ))∧
                                   (Inv (x0 ) ∧ Trans(x0 , x1 ) ⇒ Inv (x1 ))∧             (2)
                                   (Inv (x0 ) ⇒ ¬Err (x0 ))

Alternatively, if the system is not safe, then there is a reachable error state. One
way of showing this is to find a concrete, n-step counterexample1 :
                                                 ^
            ∃x0 , . . . , xn  Start(x0 ) ∧               Trans(xi , xi+1 ) ∧ Err (xn )   (3)
                                              i∈[0,n−1]



2.2     Existing Techniques

Viewing program verification as existential second-order logic allows a range of
existing tools to be characterised in a common framework and thus compared
and contrasted. This section reviews some of the more widely used approaches.
1
    If the state space is finite and the system is not safe there is necessarily a finite,
    concrete counterexample. For infinite state spaces there are additional issues such
    as errors only reachable via infinite counterexamples and which fixed-points can be
    described by a finite formulae.
The following abbreviations, corresponding to k steps of the transition system
and the first k states being error free, will be used:
                   ^                                      ^
        T [k] =          Trans(xi , xi+1 )        P [k] =    ¬Err (xi )
                i∈[0,k−1]                                       i∈[0,k−1]


Bounded Model Checking (BMC) [2] focuses on refutation by picking a unwinding
limit k and solving:

                    ∃x0 , . . . , xk  Start(x0 ) ∧ T [k] ∧ ¬P [k + 1]            (4)

Models of this formula correspond to concrete counterexamples of some length
n 6 k. The unwinding limit gives an under-approximation of the set of reach-
able states and thus can fail to find counterexamples that take a large number
of transition steps. In practice BMC works well as the formula is existentially
quantified and thus is in a fragment handled well by SAT and SMT solvers.
There are also various simplifications that can reduce the number of variables
(see Section 3.1).

Incremental BMC (IBMC) (e.g. [10]) uses repeated BMC (often optimised by
using the solver incrementally) checks with increasing bounds to avoid the need
for a fixed bound. If the bound starts at 0 (i.e. checking ∃x0 Start (x0 )∧Err (x0 ))
and is increased linearly (this is the common use-case), then it can be assumed
that there are no errors at previous states, giving a simpler test:

                 ∃x0 , . . . , xk  Start(x0 ) ∧ T [k] ∧ P [k] ∧ Err (xk )        (5)

K-Induction [28] can be viewed as an extension of IBMC that can show system
safety as well as produce counterexamples. It makes use of k-inductive invariants,
which are predicates that have the following property:

                        ∀x0 . . . xk  I [k] ∧ T [k] ⇒ KInv(xk )                  (6)

where                                      ^
                              I [k] =               KInv(xi )
                                        i∈[0,k−1]

k-inductive invariants have the following useful properties:

 – Any inductive invariant is a 1-inductive invariant and vice versa.
 – Any k-inductive invariant is a (k + 1)-inductive invariant.
 – A (finite) system is safe if and only if there is a k-inductive invariant KInv
   which satisfies:
                        ∀x0 . . . xk  (Start (x0 ) ∧ T [k] ⇒ I [k]) ∧
                                       (I [k] ∧ T [k] ⇒ KInv (xk )) ∧             (7)
                                       (KInv (xk ) ⇒ ¬Err (xk ))
Showing that a k-inductive invariant exists is sufficient to show that an induc-
tive invariant exists but it does not imply that the k-inductive invariant is an
inductive invariant. Often the corresponding inductive invariant is significantly
more complex. Thus k-induction can be seen as a trade-off between invariant
generation and checking as it is a means to benefit as much as possible from
simpler invariants by using a more complex property check.
    Finding a candidate k-inductive invariant is hard so implementations often
use ¬Err (x). Similarly to IBMC, linearly increasing k can be used to simplify
the expression by assuming there are no errors at previous states:

                 ∃x0 , . . . , xk  (Start (x0 ) ∧ T [k] ∧ P [k] ∧ Err (xk ))∨
                                                                                   (8)
                                    (T [k] ∧ P [k] ∧ Err (xk ))

A model of the first part of the disjunct is a concrete counterexample (k-
induction subsumes IBMC) and if the whole formula has no models, then ¬Err (x)
is a k-inductive invariant and the system is safe.

Abstract Interpretation [6] While BMC and IBMC compute under-approximations
of the set of reachable states, the classical use of abstract interpretation is to com-
pute inductive invariants that include Start(x) and thus are over-approximations
of the set of reachable states. Elements of an abstract domain can be understood
as sets or conjuncts of formulae [8], so abstract interpretation can be seen as:

           ∃2 AInv ∈ A  ∀x, x1  (Start(x) ⇒ AInv(x))∧
                                                                                   (9)
                                  (AInv (x) ∧ Trans(x, x1 ) ⇒ AInv (x1 ))

where A is the set of formulae described by the chosen abstract domain. As a
second step then one checks:

                               ∀x  AInv (x) ⇒ ¬Err (x)                           (10)

If this has no models then the system is safe, otherwise the safety cannot be
determined without finding a more restrictive AInv or increasing the set A , i.e.
choosing a more expressive abstract domain.


2.3     Our Algorithm: kIkI

The phases of the kIkI algorithm are presented as a flow chart in Figure 1 with
black arrows denoting transitions. Initially, k = 1 and T is a set of predicates
that can be used as invariant with ⊤ ∈ T (see Section 3 for details of how this
is implemented).
    After an initial test to see if any start states are errors2, kIkI computes a
k-inductive invariant that covers the initial state and includes the assumption
that there are no errors in earlier states. The invariant is then checked to see
2
    If the transition system is derived from software and the errors are generated from
    assertions this will be impossible and the check can be skipped.
IBMC                            k-induction                                           Abstract
                                                                                   Interpretation

                  Test ∃x0 
           Start (x0 ) ∧ Err (x0 )

  SAT                    UNSAT                           Find KInv ∈ T  ∀x0 , . . . , xk 
                                                      (Start (x0 ) ∧ P [k] ∧ T [k] ⇒ I [k])∧
                                                       (P [k] ∧ I [k] ∧ T [k] ⇒ KInv (xk ))

                    k++

             UNSAT

      Test ∃x0 , . . . , xk  Start (x0 )∧                      Test ∃xo , . . . , xk 
    P [k] ∧ I [k + 1] ∧ T [k] ∧ Err (xk )         SAT P [k] ∧ I [k + 1] ∧ T [k] ∧ Err (xk )
                 SAT                                            UNSAT


                   C/E                        ?                        Safe


               Fig. 1: The kIkI algorithm (colours in online version)


whether it is sufficient to show safety. If there are possible reachable error states
then a second check is needed to see if the error is reachable in k steps (a genuine
counterexample) or whether it is a potential artefact of a too weak invariant. In
the latter case, k is incremented so that a stronger (k-)invariant can be found
and the algorithm loops.
    Also displayed in Figure 1 are the steps of incremental BMC, k-induction
and classical over-approximating abstract interpretation, given, respectively by
the red dotted, blue dashed and green dashed/dotted boxes and arrows. kIkI
can simulate k-induction by having T = {⊤} and incremental BMC by over-
approximating the first SAT check. Classical over-approximate abstract inter-
pretation can be simulated by having T = A and terminating with the result
“unknown” if the first SAT check finds a model. These simulations give an in-
tuition for the proof of the following results:

Theorem 1.

 – When kIkI terminates it gives either a k-inductive invariant sufficient to
   show safety or a length k counterexample.
              void main ( )
              {                            guard #0 == TRUE
                unsigned x = 0 ;           x #0 == 0u

                                           guard #1 == guard #0
                  while ( x<10)            x # phi1 == ( guard # l s 0 ? x # l b 1 : x # 0 )
                  {                        guard #2 == ( x# phi1 < 1 0 ) && guard #1
                    ++x ;                  x #2 == 1u + x# phi1
                  }
                                           guard #3 == ! ( x# phi1 < 1 0 ) && guard #1
                  a s s e r t ( x ==10);   x # phi1 == 10u | | ! guard #3
              }


              (a) The program                     (b) The annotated SSA

                       Fig. 2: Conversion from program to SSA


 – If IBMC or k-induction terminate with a length k counterexample, then kIkI
   will terminate with a length k counterexample.
 – If k-induction terminates with a k-inductive invariant sufficient to show
   safety, then kIkI will terminate with a k-inductive invariant sufficient to
   show safety.
 – If an (over-approximating) abstract interpreter returns an inductive invari-
   ant AInv that is sufficient to show safety and A ⊆ T , then kIkI will termi-
   nate with k = 1 and an inductive invariant sufficient to show safety.

    Hence kIkI strictly generalises its components by exploiting the following
synergies between them: unrolling k times helps abstract interpretation to gen-
erate stronger invariants, namely k-invariants, which are further strengthened
by the additional facts known from not having found a counterexample for k − 1
iterations; stronger invariants help k-induction to successfully prove properties
more often; and constraining the state space by invariants ultimately accelerates
the countermodel search in BMC. We will observe these synergies also experi-
mentally in Section 5.


3     Algorithm Details

Section 2 introduced kIkI but omitted a number of details which are important
for implementing the algorithm efficiently. Key amongst these are the encoding
from program to transition system and the generation of k-inductive invariants.


3.1   SSA Encoding

The presentation of kIkI used transition systems and it is possible to implement
this directly. However the symbolic transition systems generated by software
have structural properties that can be exploited. In most states the value of
the program counter uniquely identifies its next value (i.e. most instructions
do not branch) and most transitions update a single variable. Thus states in
                                                           before the loop (x#0)


                                                     loop head 1 multiplexer (x#phi1%0)

                                                                loop body 1

                                                         end of loop body 1 (x#2%0)
              before the loop (x#0)                                                     (x#lb1)
                                                       loop head 0 (x#phi1%1 = x#2%0)
         loop head multiplexer (x#phi1)                         loop body 0

                   loop body          (x#lb1)            end of loop body 0 (x#2%1)
             end of loop body (x#2)
                                                              merge loop exits

                   after loop                                    after loop

        (a) The SSA form of a loop.                   (b) The SSA loop unwinding

                     Fig. 3: Illustrations of various SSA encodings


the transition can be merged by substituting in the symbolic values of updated
variables, so reducing the size of the formulae generated.
    Rather than building the transition system and then reducing it, it is equiv-
alent and more efficient to convert the program to single static assignment
form (SSA). For acyclic code, the SSA is a formula that exactly represents the
strongest post condition of running the code and generation of this is a standard
technique found in most software BMC and Symbolic Execution tools. We ex-
tend this with an over-approximate conversion of loops so that the SSA allows
us to reason about abstractions of a program with a solver.
    Figure 2 gives an example of the conversion. The SSA has been made acyclic
by cutting loops at the end of the loop body: the variable3 x#2 at the end of the
loop body (“poststate”) corresponds to x#lb1, which is fed back into the loop
head (“prestate”). A non-deterministic choice (using the free Boolean variable
guard#ls0) is introduced at the loop head in order to join the values coming
from before the loop and from the end of the loop body. Figure 3a illustrates
how the SSA statements express control flow.
    It is easy to see that this representation “havocs” loops because x#lb1 is a
free variable – this is why its models are an over-approximation of actual program
traces. Precision can be improved by constraining the feedback variable x#lb1
by means of a loop invariant which we are going to infer. Any property that
holds at loop entry (x#0) and at the end of the body (x#2) can then be assumed
to hold on the feedback variable x#lb1.
    Loop unwinding is performed in the usual fashion; the conversion to SSA
simply repeats the conversion of the body of the loop. Figure 3b illustrates an
example of this. The top-most loop head multiplexer is kept and its feedback
variable is constrained with the bottom-most loop unwinding. The only subtlety
3
    Variable name suffixes are use to denote the multiple logical variables that correspond
    to a single program variable at different points in the execution.
is that the value of variables from different loop exits must be merged. This
can be achieved by use of the guard variables which track the reachability of
various program points for a given set of values. The unwinding that we perform
is incremental, in the sense that the construction of the formula is monotonic.
Assumptions have to be used to deal with the end of loop merges as there always
has to be a case for “value is merged from an unwinding that has not been added
yet” and this has to be assumed false.
    A more significant example is given in Appendix A.


3.2   Invariant Inference via Templates

A key phase of kIkI is the generation of KInv , a k-inductive invariant. Perhaps
the most obvious approach is to use an off-the-shelf abstract interpreter. This
works but will fail to exploit the real power of kIkI. Each iteration, kIkI unrolls
loops one more step (which can improve the invariant given by an abstract
interpreter) and adds assumptions that previous unwindings do not give errors.
Without backwards propagation it is difficult for an abstract interpreter to make
significant use of these assumptions. For example, an abstract interpretation
with intervals would need backwards propagation to make use of assume(x +
y < 10). Thus we use a solver-based approach to computing KInv as it can
elegantly exploit the assumptions that are added without needing to (directly)
implement transformers.
    Directly using a solver we would need to handle (the existential fragment of)
second-order logic. As these are not currently available, we reduce to a problem
that can be solved by iterative application of a first-order solver. We restrict
ourselves to finding invariants KInv of the form T (x, δ) where T is a fixed
expression, a so-called template, over program variables x and template param-
eters δ (see Section 3.3). This restriction is analogous to choosing an abstract
domain in an abstract interpreter and has similar effect – T only contains a
the formulae that can be described by the template. Fixing a template reduces
the second-order search for an invariant to the first-order search for template
parameters:
                  ∃δ ∀x0 . . . xk  (Start(x0 ) ∧ T [k] ⇒ T [k](δ)) ∧
                                                                               (11)
                                     (T [k](δ) ∧ T [k] ⇒ T (xk , δ))
                   V
with T [k](δ) = i∈[0,k−1] T (xi , δ). Although the problem is now expressible
in first-order logic, it contains quantifier alternation which poses a problem for
current SMT solvers. However, we can solve this problem by iteratively checking
the negated formula (to turn ∀ into ∃) for different choices of constants d for the
parameters δ; as for the second conjunct in (11):
                                                                 
                   ∃x0 . . . xk  ¬ T [k](d) ∧ T [k] ⇒ T (xk , d)              (12)
    The resulting formula can be expressed in quantifier-free logics and efficiently
solved by SMT solvers. Using this as a building block, one can solve this ∃∀
problem (see Section 3.4).
3.3   Guarded Template Domains
As discussed in the previous section, we use templates and repeated calls (with
quantifier-free formulae) to a first-order solver to compute k-inductive invariants.
   An abstract value d represents, i.e. concretises to, the set of all x that satisfy
the formula T (x, d). We require an abstract value ⊥ denoting the empty set
T (x, ⊥) ≡ false, and ⊤ for the whole domain of x: T (x, ⊤) ≡ true.

Template polyhedra We use template polyhedra [25], a class of templates for
numerical variables which have the form T = (Ax ≤ δ) where A is a matrix
with fixed coefficients.
                     Subclasses
                                 of such templates include Intervals, which
                       1          δi1
require constraints        xi ≤         for each variable xi , Zones (differences),
                      −1          δi2
                         th
and Octagons [22]. The r row of the template are the constraint generated by
the rth row of matrix A.
    In our template expressions, variables x are bit-vectors representing signed
or unsigned integers. These variables can be mixed in template constraints. Type
promotion rules are applied such that the bit-width of the types of the expres-
sions are extended in order to avoid arithmetic under- and overflows in the
template expressions. ⊤ corresponds to the respective maximum values in the
promoted type, whereas ⊥ must be encoded as a special symbol.

Guarded templates Since we use SSA form rather than control flow graphs, we
cannot use numerical templates directly. Instead we use guarded templates. In a
guarded template each row r is of the form Gr ⇒ Tbr for the rth row Tbr of the
base template domain (e.g. template polyhedra). Gr is the conjunction of the
SSA guards gi associated with the definition of variables xi occurring in Tbr . Gr
denotes the guard associated to variables x appearing at the loop head, and G′r
the guard associated to the variables x′ at the end of the respective loop body.
Hence, template rows for different loops have different guards.
    A guarded templateV     in terms of the variables at the loop head is hence of the
form T (x0 , δ) = r Gr (x0 ) ⇒ Tbr (x0 , δ). Replacing parameters δ by the values
d we get the invariants T (x, d) at the loop heads.
    For the example program in Section 3.1, we have the following guarded in-
terval template:
                                  
                                    guard#1 ∧ guard#ls0 ⇒ x#lb1 ≤ δ1
          T (x#lb1, (δ1 , δ2 )) =
                                    guard#1 ∧ guard#ls0 ⇒ −x#lb1 ≤ δ2
                                 V
    We denote T ′ (x1 , δ) = r G′r (x1 ) ⇒ Tbr (x1 , δ) the guarded template ex-
pressed in terms of the variables at the end of the loop body. Here, we have to
express the join of the initial value at the loop head (like x#0) and the values
that are fed back into the loop head (like x#2). For the example above, the
corresponding guarded template is as follows:
                          
                           (pg ⇔ guard#2) ∧ (ig ⇔ guard#1 ∧ ¬guard#ls0)∧
   T ′ (x#2, (δ1 , δ2 )) = ((ig ⇒ x′ = x#0) ∧ (pg ∧ ¬ig ⇒ x′ = x#2))∧
                          
                            (pg ∨ ig ⇒ x′ ≤ δ1 ) ∧ (pg ∨ ig ⇒ −x′ ≤ δ2 )
      3.4   Accelerated Solving of the ∃∀ Problem
      As discussed in Section 3.2, it is necessary to solve an ∃∀ problem to find values
      for template parameters δ to infer invariants.

      Model enumeration. The well-known method [24,4] for solving this problem in
      formula (12) using SMT solvers repeatedly checks satisfiability of the formula
      for an abstract value d (starting with d = ⊥):
                                T [k](d) ∧ T [k] ∧ ¬T ′ (xk , d)                   (13)
      If it is unsatisfiable, then we have found an invariant; otherwise we join the
      model returned by the solver with the previous abstract value d.
          However, this method corresponds to performing a classical Kleene iteration
      on the abstract lattice up to convergence. Convergence is guaranteed because
      our abstract domains are finite. Though, the height of the lattice is enormous
      and even for a one loop program incrementing an unconstrained 64-bit integer
      variable the naı̈ve algorithm will not terminate within human life time. Hence,
      we are not going to use this method.

      Optimisation. What we need is a convergence acceleration that makes the com-
      putational effort independent from the number of states and loop iterations. To
      this end, we use a technique that is inspired by an encoding used by max-strategy
      iteration methods [13,12,23]. These methods state the invariant inference prob-
      lem over template polyhedra as a disjunctive linear optimisation problem, which
      is solved iteratively by an upward iteration in the lattice of template polyhedra:
      using SMT solving, a conjunctive subsystem (“strategy”) whose solution extends
      the current invariant candidate is selected. This subsystem is then solved by an
      LP solver; the procedure terminates as soon as an inductive invariant is found.
          This method can only be used if the domain is convex and the parameter
      values are ordered and monotonic w.r.t. concretisation, which holds true, for
      example, for template polyhedra Ax ≤ d where d is a parameter, but not
      for those where A is a parameter. If the operations in the transition relation
      satisfy certain properties such as monotonicity of condition predicates, then the
      obtained result is the least fixed point, i.e. the same result as the one returned
      by the naı̈ve model enumeration above, but much faster on average.

    Our algorithm. We adapt this method to our setting with bit-vector variables
    and guarded templates. Since we deal with finite domains (bit-vectors) we can
    use binary search as optimisation method instead of an LP solver.
       The algorithm proceeds as follows: We start by checking whether the current
    abstract value d (starting from d = ⊥) is inductive (Equ. (13)). If so, we have
    found an invariant; otherwise there are template rows R whose values are not
    inductive yet. We construct the system
        V                                   
   ^          / Gr (xi ) ⇒ (er (xi ) ≤ dr ) 
             r ∈R                                      ^
           V                                   ∧T [k]∧   G′r (xk )∧(δr ≤ er (xk )) (14)
        ∧ r∈R Gr (xi ) ⇒ (er (xi ) ≤ δr ) 
i∈[0,k−1]                                                r∈R
where er is the left-hand side of the inequality corresponding to the rthProw of
the template. Then we start the binary search
                                         P      for the optimal value of  r∈R δr
over this system. The initial bounds for r∈R δr are as follows:
                          P
 – The lower bound ℓ is r∈R d′r where d′r is the value of er (xk ) in the model
    of the inductivity check (13)
                             P above;
 – The upper bound u is         r∈R max value(r) where max value returns the
    maximum value that er (xk ) may have (dependent on variable type).

    The binary search isPperformed by iteratively checking (14) for satisfiability
under the assumption r∈R δr ≥ m where m = median(ℓ, u). If satisfiable, set
ℓ := m, otherwise set u := m and repeat until ℓ = u. The values of δr in the
last satisfiable query are assigned to dr to obtain the new abstract value. The
procedure is then repeated by testing whether d is inductive (13). Note that this
algorithm uses a similar encoding for bound optimisation as strategy iteration,
but potentially requires a higher number of iterations than strategy iteration.
This choice has been made deliberately in order to keep the size of the generated
SMT formulas small, at the cost of a potentially increased number of iterations.
    A worked example is given in Appendix A.


4     Implementation

We implemented kIkI in 2LS,4 a verification tool built on the CPROVER frame-
work, using MiniSAT-2.2.0 as a back-end solver (although other SAT and SMT
solvers with incremental solving support can also be used). 2LS currently inlines
all functions when running kIkI. The techniques described in Section 3 enable
a single solver instance to be used where constraints and unwindings are added
incrementally. This is essential because kIkI makes thousands of solver calls for
invariant inference and property checks.
    Our implementation is generic w.r.t. matrix A of the template polyhedral
domain. In our experiments, we observed that very simple matrices A generating
interval invariants are sufficient to compete with other state-of-the-art tools.
    The tool can handle unrestricted sequential C programs (with the exception
of programs with irreducible control flow). However, currently, invariants are not
inferred over array contents or dynamically allocated data structures.


5     Experiments

We performed a number of experiments to demonstrate the utility and applica-
bility of kIkI. All experiments were performed on an Intel Xeon X5667 at 3 GHz
running Fedora 20 with 64-bit binaries. Each individual run was limited to 13 GB
4
    Version 0.2. The source code of the tool and instructions for its usage can be found on
    http://www.cprover.org/wiki/doku.php?id=2ls_for_program_analysis. In the
    experiments we ran it with the option --competition-mode.
of memory and 900 seconds of CPU time, enforced by the operating system ker-
nel. We took the loops meta-category (143 benchmarks) from the SV-COMP’15
benchmark set.5

5.1    kIkI Verifies More Programs Than the Algorithms it Simulates
Table 1 gives a comparison between 2LS running kIkI (column 6) and the same
system running as an incremental bounded model checker (IBMC) (column 2),
incremental k-induction (i.e. without invariant inference, column 3) and as an
abstract interpreter (AI) (column 4). kIkI is more complete than each of the
restricted modes. This is not self-evident since it could be much less efficient
and, thus, fail to solve the problems within the given time or memory limits.
k-induction can solve 60.8% of the benchmarks, 13 more than IBMC. 32% of the
benchmarks can be solved by abstract interpretation (bugs are only exposed if
they are reachable with 0 loop unwindings). kIkI solves 62.9% of the benchmarks,
proving 3 more properties than k-induction.


                   IBMC k-induction AI portfolio kIkI CPAchecker ESBMC
    counterexamples 38      38       17   38      38     36         35
    proofs           36      49      30   51      52     59        91
    false proofs      0       0       0    0       0      2         12
    false alarms      2       2       0    2       2      2          0
    inconclusive      0       0      93    0       0      4          2
    timeout          65      53       3   50      51     38          2
    memory out        2       1       0    2       0      2          1
    total runtime   17.1h  13.8h   0.89h 13.3h 13.2h    10.9h     0.54h
Table 1: Comparison between kIkI, the algorithms it subsumes, the portfolio,
and CPAchecker. The rows false alarms and false proofs indicate soundness bugs
of the tool implementations.




5.2    kIkI is at Least as Good as Their Naı̈ve Portfolio
To show that kIkI is more than a mixture of three techniques and that they
strengthen each other, consider column 5 of Table 1. This gives the results of
an ideal portfolio in which the three restricted techniques are run in parallel
on and the portfolio terminates when the first returns a conclusive result. Thus
the CPU time taken is three times the time taken by the fastest technique for
each benchmark (in practice these could be run in parallel, giving a lower wall
clock time). In our setup, kIkI had a disadvantage as each component of virtual
portfolio had the same memory restriction as kIkI, thus effectively giving the
portfolio three times as much memory.
5
    http://sv-comp.sosy-lab.org/2015/benchmarks.php
                               103                                                                                        103
                                                        timeout                                                                                timeout




                                                                                          CPAchecker (time in seconds)
portfolio (time in seconds)


                               102                                                                                        102




                                                                                                                                                                        timeout
                                              kIkI faster                                                                            kIkI faster


                               101                                                                                        101




                                                                                timeout
                                                             portfolio faster                                                                       CPAchecker faster

                               100                                                                                        100

                                                                      Safe Unsafe                                                                           Safe Unsafe
                              10−1 −1                                                                                    10−1 −1
                                 10         100            101        102          103                                      10     100            101       102            103
                                                  kIkI (time in seconds)                                                                 kIkI (time in seconds)

                                                     (a)                                                                                    (b)

                                                                    Fig. 4: Runtime Comparison


                                  Still, kIkI is slightly faster and more accurate than the portfolio as can be seen
                              in Table 1. The scatter plot in Figure 4a shows the results for each benchmark:
                              one can observe that kIkI is up to one order of magnitude slower on many unsafe
                              benchmarks, which is obviously due to the additional work of invariant inference
                              that kIkI has to perform in contrast to IBMC. However, note that kIkI is faster
                              than the portfolio on some safe and even one unsafe benchmarks. This suggests
                              that kIkI is more than the sum of its parts.

                              5.3       kIkI is Comparable with State-of-the-Art Approaches
                              We compared our implementation of kIkI with CPAchecker6, and ESBMC7 ,
                              which uses k-induction. The results are shown in the last three columns in Table
                              1 and in the scatter plot in Figure 4b. Additional results are given in Appendix B.
                              In comparison to CPAchecker, the winner of SVCOMP’15, our prototype of kIkI
                              is overall a bit slower and proves fewer properties (due to more timeouts), but as
                              Figure 4b shows, it significantly outperforms CPAchecker on most benchmarks.
                              ESBMC exposes fewer bugs, but proves many more properties and is significantly
                              faster. However, it has 6 times more soundness bugs than our implementation.8
                              These results show that our prototype implementation of kIkI can keep up with
                              state-of-the-art verification tools.

                              6      Related Work
                              Our work elucidates the connection between three well-studied techniques. Hence
                              we can only give a brief overview of the vast amount of relevant literature.
                              6
                                SVCOMP’15 version, http://cpachecker.sosy-lab.org/
                              7
                                SVCOMP’15 version, http://www.esbmc.org/
                              8
                                The two false alarms in our current implementation are due to limited support for
                                dynamic memory allocation.
    Since it was observed [28] that k-induction for finite state systems (e.g. hard-
ware circuits) can be done by using an (incremental) SAT solver [10], it has be-
come more and more popular also in the software community as a tool for safety
proofs. Using SMT solvers, it has been applied to Lustre models [17] (monolithic
transition relations) and C programs [7] (multiple and nested loops).
    The idea of synthesising abstractions with the help of solvers can be traced
back to predicate abstraction [14]; Reps et al. [24] proposed a method for sym-
bolically computing best abstract transformers; these techniques were later re-
fined [4,19,29] for application to various template domains. Using binary search
for optimisation in this context was proposed by Gulwani et al. [16]. Similar tech-
niques using LP solving for optimisation originate from strategy iteration [13].
Recently, SMT modulo optimisation [27,20] techniques were proposed that foster
application to invariant generation by optimisation.
    k-induction often requires additional invariants to succeed, which can be ob-
tained by abstract interpretation. For example, Garoche et al. [11] use SMT
solving to infer intermediate invariants over templates for the use in k-induction
of Lustre models. As most of these approaches (except [4]), they consider (linear)
arithmetic over rational numbers only, whereas our target are C programs with
bit-vectors (representing machine integers, floating-point numbers, etc). More-
over, they do not exploit the full power of the approach because they compute
only 1-invariants instead of k-invariants. Another distinguishing feature of our
algorithm is that it operates on a single logical representation and hence enables
maximum information reuse by incremental SAT solving using a single solver.
    Formalising program analysis problems such as invariant inference in second
order logic and suggesting to solve these formulae with generic solvers has been
considered by [15]. In this paper we provide an implementation that solves the
second order formula describing the invariant inference problem by reduction
to quantifier elimination of a first order formula. Our approach can also solve
other problems stated in [15], e.g., termination, by considering different abstract
domains, e.g., for ranking functions.


7   Conclusions

This paper presents kIkI and shows that it can simulate incremental BMC, k-
induction and classical, over-approximating abstract interpretation. Experiments
performed with an implementation, 2LS, show that it is not only “more” com-
plete than each individual technique – but it also suggests that it is stronger than
their naı̈ve combination. In other words, the components of the algorithm syner-
gistically interact and enhance each other. Moreover, our combination enables a
clean, homogeneous, tightly integrated implementation rather than a loose, het-
erogeneous combination of isolated building blocks or a pipeline of techniques
where each only strengthens the next.
    There are many possible future directions for this work. Enhancing 2LS to
support additional kinds of templates, possibly including disjunctive template
and improving the optimisation techniques used for quantifier elimination is one
area of interest. In another direction, kIkI could be enhance to support function
modular, intraprocedural, thread modular and possibly multi-threaded analysis.
Automatic refinement of the template domains is another tantalising possibility.


References

 1. Beyer, D., Dangl, M., Wendler, P.: Combining k-induction with
    continuously-refined       invariants.      CoRR        abs/1502.00096       (2015),
    http://arxiv.org/abs/1502.00096
 2. Biere, A., Cimatti, A., Clarke, E.M., Zhu, Y.: Symbolic model checking without
    BDDs. In: TACAS. LNCS, vol. 1579, pp. 193–207. Springer (1999)
 3. Bradley, A.R., Manna, Z.: Checking safety by inductive generalization of counterex-
    amples to induction. In: Formal Methods in Computer-Aided Design. pp. 173–180.
    IEEE Computer Society (2007)
 4. Brauer, J., King, A., Kriener, J.: Existential quantification as incremental SAT.
    In: CAV. LNCS, vol. 6806, pp. 191–207. Springer (2011)
 5. Clarke, E.M., Grumberg, O., Jha, S., Lu, Y., Veith, H.: Counterexample-guided
    abstraction refinement. In: CAV. LNCS, vol. 1855, pp. 154–169. Springer (2000)
 6. Cousot, P., Cousot, R.: Abstract interpretation: A unified lattice model for static
    analysis of programs by construction or approximation of fixpoints. In: POPL. pp.
    238–252 (1977)
 7. Donaldson, A., Haller, L., Kroening, D., Rümmer, P.: Software Verification Using
    k-Induction. In: SAS. LNCS, vol. 6887, pp. 351–368. Springer (2011)
 8. D’Silva, V., Kroening, D.: Abstraction of syntax. In: VMCAI. pp. 396–413 (2013)
 9. Eén, N., Sörensson, N.: An Extensible SAT-solver. In: SAT. LNCS, vol. 2919, pp.
    502–518. Springer (2003)
10. Eén, N., Sörensson, N.: Temporal induction by incremental SAT solving. ENTCS
    89:4, 543–560 (2003)
11. Garoche, P.L., Kahsai, T., Tinelli, C.: Incremental invariant generation using logic-
    based automatic abstract transformers. In: NASA Formal Methods. LNCS, vol.
    7871, pp. 139–154. Springer (2013)
12. Gawlitza, T.M., Monniaux, D.: Improving strategies via SMT solving. In: ESOP.
    LNCS, vol. 6602, pp. 236–255. Springer (2011)
13. Gawlitza, T.M., Seidl, H.: Precise relational invariants through strategy iteration.
    In: Computer Science Logic. LNCS, vol. 4646, pp. 23–40. Springer (2007)
14. Graf, S., Saı̈di, H.: Construction of abstract state graphs with PVS. In: CAV.
    LNCS, vol. 1254, pp. 72–83. Springer (1997)
15. Grebenshchikov, S., Lopes, N.P., Popeea, C., Rybalchenko, A.: Synthesizing soft-
    ware verifiers from proof rules. In: PLDI. pp. 405–416. ACM (2012)
16. Gulwani, S., Srivastava, S., Venkatesan, R.: Program analysis as constraint solving.
    In: PLDI. pp. 281–292. ACM (2008)
17. Hagen, G., Tinelli, C.: Scaling up the formal verification of Lustre programs with
    SMT-based techniques. In: FMCAD. pp. 1–9. IEEE Computer Society (2008)
18. Hoder, K., Bjørner, N.: Generalized property directed reachability. In: Theory
    and Applications of Satisfiability Testing. LNCS, vol. 7317, pp. 157–171. Springer
    (2012)
19. Kahsai, T., Ge, Y., Tinelli, C.: Instantiation-based invariant discovery. In: NASA
    Formal Methods. LNCS, vol. 6617, pp. 192–206. Springer (2011)
20. Li, Y., Albarghouthi, A., Kincaid, Z., Gurfinkel, A., Chechik, M.: Symbolic opti-
    mization with SMT solvers. In: POPL. pp. 607–618. ACM (2014)
21. Mcmillan, K.L.: Lazy abstraction with interpolants. In: CAV. LNCS, vol. 4144, pp.
    123–136. Springer (2006)
22. Miné, A.: The octagon abstract domain. In: Working Conference on Reverse En-
    gineering. pp. 310–319. IEEE Computer Society (2001)
23. Monniaux, D., Schrammel, P.: Speeding up logico-numerical strategy iteration. In:
    Static Analysis Symposium. LNCS, vol. 8723, pp. 253–267. Springer (2014)
24. Reps, T.W., Sagiv, S., Yorsh, G.: Symbolic implementation of the best transformer.
    In: VMCAI. LNCS, vol. 2937, pp. 252–266. Springer (2004)
25. Sankaranarayanan, S., Sipma, H.B., Manna, Z.: Scalable analysis of linear sys-
    tems using mathematical programming. In: VMCAI. LNCS, vol. 3385, pp. 25–41.
    Springer (2005)
26. Schrammel, P., Kroening, D., Brain, M., Martins, R., Teige, T., Bienmüller, T.:
    Successful use of incremental BMC in the automotive industry. In: Formal Methods
    for Industrial Critical Systems. LNCS, vol. 9128, pp. 62–77. Springer (2015)
27. Sebastiani, R., Tomasi, S.: Optimization in SMT with LA cost functions. In: IJ-
    CAR. LNCS, vol. 7364, pp. 484–498. Springer (2012)
28. Sheeran, M., Singh, S., Stålmarck, G.: Checking safety properties using induction
    and a SAT-solver. In: FMCAD. LNCS, vol. 1954, pp. 108–125. Springer (2000)
29. Thakur, A.V., Reps, T.W.: A method for symbolic computation of abstract oper-
    ations. In: CAV. LNCS, vol. 7358, pp. 174–192. Springer (2012)
A    A Worked Example
We explain the kIkI algorithm step by step on the following example:
void main ( ) {
  i n t w=0 , x , y , z ;
    CPROVER assume ( x==y && y==z && −10<=x && x < 0 ) ;
  while ( 1 ) {
     z = −y ;
     y = −x ;
     w++;
     x = x + w;
      i f (w%2 ! = 1 ) w /= 3 ;
      i f ( x>=10) x = y = z = 0 ;
      a s s e r t ( x<=z + 3 ) ;
} }


SSA construction. We first perform a lighweight static analysis in order to trans-
late to program into our SSA form:
w#0 == 0
guard#1 == (x#0 < 0 && x#0 == y#0 && y#0 == z#0 && x#0 >= -10)

//loop head
w#phi1 == (guard#ls5 ? w#lb5 : w#0)
x#phi1 == (guard#ls5 ? x#lb5 : x#0)
y#phi1 == (guard#ls5 ? y#lb5 : y#0)
z#phi1 == (guard#ls5 ? z#lb5 : z#0)

guard#2 == TRUE && guard#1 //in the loop
z#2 == -y#phi1
y#2 == -x#phi1
w#2 == 1 + w#phi1
x#2 == w#2 + x#phi1

guard#3 == (!(w#2 % 2 == 1) && guard#2)
w#3 == w#2 / 3
w#phi4 == (guard#3 ? w#3 : w#2)

guard#4 == ((x#2 >= 10) && guard#2)
z#4 == 0
y#4 == z#4
x#4 == y#4
x#phi5 == (guard#4 ? x#4 : x#2)
y#phi5 == (guard#4 ? y#4 : y#2)
z#phi5 == (guard#4 ? z#4 : z#2)

guard#6 == !TRUE && guard#1 //after loop

guard#2 ==> 3 + z#phi5 >= x#phi5 //assertion
   It is important to note here that the loop is cut at the end of the loop
body in order to make the SSA acyclic. For this reason, we replace variables
w#phi4, x#phi5, y#phi5, and z#phi5 by free variables w#lb5, x#lb5, y#lb5,
and z#lb5 at the loop head. Since these variables are free we obtain the effect of
“havocking” these loop variables. The invariants that we compute will constrain
these variables.

Invariant inference over the interval domain uses the following guarded template
on our example;

guard#2 && guard#ls5 ==>
   w#lb5 <= delta#11 && -((signed __CPROVER_bitvector[33])w#lb5) <= delta#12 &&
   x#lb5 <= delta#21 && -((signed __CPROVER_bitvector[33])x#lb5) <= delta#22 &&
   y#lb5 <= delta#31 && -((signed __CPROVER_bitvector[33])y#lb5) <= delta#32 &&
   z#lb5 <= delta#41 && -((signed __CPROVER_bitvector[33])z#lb5) <= delta#42

    The casts such as (signed CPROVER bitvector[33])w#lb5) are necessary
to extend the bitwidth in order to prevent from arithmetic overflows in template
expressions (which would be unsound). For intervals, the bitwidth extension
could be avoided, but our algorithms are generic for template polyhedra.
    Invariant inference using intervals on above program is not very precise. We
obtain the following result, which does not allow us to prove the property.
guard#2 && guard#ls5 ==>
   w#lb5 <= 2147483647 && -((signed __CPROVER_bitvector[33])w#lb5) <= 715827882 &&
   x#lb5 <= 9          && -((signed __CPROVER_bitvector[33])x#lb5) <= 2147483648 &&
   y#lb5 <= 2147483647 && -((signed __CPROVER_bitvector[33])y#lb5) <= 2147483648 &&
   z#lb5 <= 2147483647 && -((signed __CPROVER_bitvector[33])z#lb5) <= 2147483648

Loop unwinding We perform incremental loop unwinding on SSA formula level.
Since formula construction for incremental loop unwinding is non-monotonic
[26], we have to introduce Boolean variables such as enable#0 which allow us to
switch on/off certain parts of the formula as needed and use incremental SAT
solving under assumptions [9] to solve these formulae efficiently.

w#0 == 0

//loop head of 0th unwinding
enable#0 ==> (guard#1%0 == (x#0 < 0 && x#0 == y#0 && y#0 == z#0 && x#0 >= -10))
enable#0 ==> (w#phi1%0 == (guard#ls5%0 ? w#lb5%0 : w#0))
enable#0 ==> (x#phi1%0 == (guard#ls5%0 ? x#lb5%0 : x#0))
enable#0 ==> (y#phi1%0 == (guard#ls5%0 ? y#lb5%0 : y#0))
enable#0 ==> (z#phi1%0 == (guard#ls5%0 ? z#lb5%0 : z#0))

//last unwinding
guard#2%0 == (TRUE && guard#1%0)
z#2%0 == -y#phi1%0
y#2%0 == -x#phi1%0
w#2%0 == 1 + w#phi1%0
x#2%0 == w#2%0 + x#phi1%0

guard#3%0 == (!(w#2%0 % 2 == 1) && guard#2%0)
w#3%0 == w#2%0 / 3
w#phi4%0 == (guard#3%0 ? w#3%0 : w#2%0)

guard#4%0 == ((x#2%0 >= 10) && guard#2%0)
z#4%0 == 0
y#4%0 == z#4%0
x#4%0 == y#4%0
x#phi5%0 == (guard#4%0 ? x#4%0 : x#2%0)
y#phi5%0 == (guard#4%0 ? y#4%0 : y#2%0)
z#phi5%0 == (guard#4%0 ? z#4%0 : z#2%0)

//merge variables from various loop exits
enable#1 ==> (guard#1 == guard#1%0)
enable#1 ==> (w#phi1 == w#phi1%0)
enable#1 ==> (x#phi1 == x#phi1%0)
enable#1 ==> (y#phi1 == y#phi1%0)
enable#1 ==> (z#phi1 == z#phi1%0)

guard#34 == (!TRUE && guard#1) //after loop exit

guard#2%0 ==> 3 + z#phi5%0 >= x#phi5%0 //assertion

   For a further iteration we add the following. Note that we unwind backwards
by inserting new unwindings before the old ones. Also note that formula un-
winding generates an exponential blow-up of the SSA formula in the depth of
loop nesting.
//loop head of 1st unwinding
enable#1 ==> (guard#1%1 == (x#0 < 0 && x#0 == y#0 && y#0 == z#0 && x#0 >= -10))
enable#1 ==> (w#phi1%1 == (guard#ls5%1 ? w#lb5%1 : w#0))
enable#1 ==> (x#phi1%1 == (guard#ls5%1 ? x#lb5%1 : x#0))
enable#1 ==> (y#phi1%1 == (guard#ls5%1 ? y#lb5%1 : y#0))
enable#1 ==> (z#phi1%1 == (guard#ls5%1 ? z#lb5%1 : z#0))

guard#2%1 == (TRUE && guard#1%1)
z#2%1 == -y#phi1%1
y#2%1 == -x#phi1%1
w#2%1 == 1 + w#phi1%1
x#2%1 == w#2%1 + x#phi1%1

guard#3%1 == (!(w#2%1 % 2 == 1) && guard#2%1)
w#3%1 == w#2%1 / 3
w#phi4%1 == (guard#3%1 ? w#3%1 : w#2%1)

guard#4%1 == ((x#2%1 >= 10) && guard#2%1)
z#4%1 == 0
y#4%1 == z#4%1
x#4%1 == y#4%1
x#phi5%1 == (guard#4%1 ? x#4%1 : x#2%1)
y#phi5%1 == (guard#4%1 ? y#4%1 : y#2%1)
z#phi5%1 == (guard#4%1 ? z#4%1 : z#2%1)

//stitch together 0th and 1st unwinding
enable#1 ==> (guard#1%0 == guard#2%1)
enable#1 ==> (w#phi1%0 == w#phi4%1)
enable#1 ==> (x#phi1%0 == x#phi5%1)
enable#1 ==> (y#phi1%0 == y#phi5%1)
enable#1 ==> (z#phi1%0 == z#phi5%1)

//merge variables from various loop exits
enable#1 ==> (guard#1 == (!guard#2%1 ? guard#1%1 : guard#1%0))
enable#1 ==> (w#phi1 == (!guard#2%1 ? w#phi1%1 : w#phi1%0))
enable#1 ==> (x#phi1 == (!guard#2%1 ? x#phi1%1 : x#phi1%0))
enable#1 ==> (y#phi1 == (!guard#2%1 ? y#phi1%1 : y#phi1%0))
enable#1 ==> (z#phi1 == (!guard#2%1 ? z#phi1%1 : z#phi1%0))

guard#2%1 ==> 3 + z#phi5%1 >= x#phi5%1 //assertion


  Obviously, unwinding further does not help for this example. This is why
IBMC will not prove the property.

k-induction. For proving that the property is k-inductive, we assume the prop-
erty for each unwinding j < k by adding guard#ls5%j && (guard#2%j ==>
3 + z#phi5%j >= x#phi5%j) to the formula. However, the property is not k-
inductive on this example.

kIkI additionally uses k-inductive invariants. We infer the following invariant,
which, together with the assumptions from k-induction above, allows us to prove
the property for k = 2 on this example.
guard#2%2 && guard#ls5%2 ==>
   w#lb5%2 <= 1 && -((signed __CPROVER_bitvector[33])w#lb5%2) <= 0 &&
   x#lb5%2 <= 9 && -((signed __CPROVER_bitvector[33])x#lb5%2) <= 10 &&
   y#lb5%2 <= 7 && -((signed __CPROVER_bitvector[33])y#lb5%2) <= 10 &&
   z#lb5%2 <= 6 && -((signed __CPROVER_bitvector[33])z#lb5%2) <= 10
B    Further Results

In addition to Table 1, Table 2 gives results for an extension of CPAchecker
supporting k-induction discussed in the research report [1]. They use a classical
abstract interpreter to generate auxiliary invariants. Their run times are simi-
lar to the CPAchecker SVCOMP-15 version, but much less complete regarding
proofs than kIkI. They only use 1-invariants instead of k-invariants, yet they use
increasingly more precise abstract domains. Moreover, the extension seems to
be still under development as the number of false proofs and alarms suggests.


               IBMC k-induction AI portfolio kIkI CPAchecker ESBMC CPAchecker-k-ind
counterexamples 38      38       17   38      38     36         35       36
proofs           36      49      30   51      52     59        91        45
false proofs      0       0       0    0       0      2         12        3
false alarms      2       2       0    2       2      2          0       22
inconclusive      0       0      93    0       0      4          2        1
timeout          65      53       3   50      51     38          2       36
memory out        2       1       0    2       0      2          1        0
total runtime   17.1h  13.8h   0.89h 13.3h 13.2h    10.9h     0.54h     9.1h
Table 2: Comparison between kIkI, the algorithms it subsumes, the portfolio,
CPAchecker (SVCOMP’15), ESBMC and CPAchecker (k-induction). The rows
false alarms and false proofs indicate soundness bugs of the tool implementations.
