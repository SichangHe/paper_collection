                                                                                                                                                                            1


                                                Optimization of Lyapunov Invariants in Verification of
                                                                                       Software Systems
                                               Mardavij Roozbehani, Member, IEEE, Alexandre Megretski , Member, IEEE, and Eric Feron Member, IEEE

                                                                                                      Abstract

                                                  The paper proposes a control-theoretic framework for verification of numerical software systems, and puts

                                              forward software verification as an important application of control and systems theory. The idea is to transfer

                                              Lyapunov functions and the associated computational techniques from control systems analysis and convex op-
arXiv:1108.0170v1 [cs.SY] 31 Jul 2011




                                              timization to verification of various software safety and performance specifications. These include but are not

                                              limited to absence of overflow, absence of division-by-zero, termination in finite time, presence of dead-code, and

                                              certain user-specified assertions. Central to this framework are Lyapunov invariants. These are properly constructed

                                              functions of the program variables, and satisfy certain properties—resembling those of Lyapunov functions—along

                                              the execution trace. The search for the invariants can be formulated as a convex optimization problem. If the

                                              associated optimization problem is feasible, the result is a certificate for the specification.

                                                                                                   Index Terms

                                                  Software Verification, Lyapunov Invariants, Convex Optimization.

                                                                                              I. I NTRODUCTION

                                                OFTWARE in safety-critical systems implement complex algorithms and feedback laws that control

                                        S       the interaction of physical devices with their environments. Examples of such systems are abundant

                                        in aerospace, automotive, and medical applications. The range of theoretical and practical issues that arise

                                        in analysis, design, and implementation of safety-critical software systems is extensive, see, e.g., [26],

                                        [37] , and [22]. While safety-critical software must satisfy various resource allocation, timing, scheduling,

                                        and fault tolerance constraints, the foremost requirement is that it must be free of run-time errors.

                                        A. Overview of Existing Methods

                                           1) Formal Methods: Formal verification methods are model-based techniques [44], [41], [36] for

                                        proving or disproving that a mathematical model of a software (or hardware) satisfies a given specification,

                                          Mardavij Roozbehani and Alexandre Megretski are with the Laboratory for Information and Decision Systems (LIDS), Massachusetts
                                        Institute of Technology, Cambridge, MA. E-mails: {mardavij,ameg}@mit.edu. Eric Feron is professor of aerospace software engineering at
                                        the School of Aerospace Engineering, Georgia Institute of Technology, Atlanta, GA. E-mail: feron@gatech.edu.
                                                                                                           2


i.e., a mathematical expression of a desired behavior. The approach adopted in this paper too, falls under

this category. Herein, we briefly review model checking and abstract interpretation.

     a) Model Checking: In model checking [14] the system is modeled as a finite state transition system

and the specifications are expressed in some form of logic formulae, e.g., temporal or propositional logic.

The verification problem then reduces to a graph search, and symbolic algorithms are used to perform

an exhaustive exploration of all possible states. Model checking has proven to be a powerful technique

for verification of circuits [13], security and communication protocols [33], [38] and stochastic processes

[3]. Nevertheless, when the program has non-integer variables, or when the state space is continuous,

model checking is not directly applicable. In such cases, combinations of various abstraction techniques

and model checking have been proposed [2], [17], [54]; scalability, however, remains a challenge.

     b) Abstract Interpretation: is a theory for formal approximation of the operational semantics of

computer programs in a systematic way [15]. Construction of abstract models involves abstraction of

domains—typically in the form of a combination of sign, interval, polyhedral, and congruence abstractions

of sets of data—and functions. A system of fixed-point equations is then generated by symbolic for-

ward/backward executions of the abstract model. An iterative equation solving procedure, e.g., Newton’s

method, is used for solving the nonlinear system of equations, the solution of which results in an inductive

invariant assertion, which is then used for checking the specifications. In practice, to guarantee finite

convergence of the iterates, narrowing (outer approximation) operators are used to estimate the solution,

followed by widening (inner approximation) to improve the estimate [16]. This compromise can be a

source of conservatism in analysis. Nevertheless, these methods have been used in practice for verification

of limited properties of embedded software of commercial aircraft [7].

  Alternative formal methods can be found in the computer science literature mostly under deductive

verification [32], type inference [45], and data flow analysis [23]. These methods share extensive similar-

ities in that a notion of program abstraction and symbolic execution or constraint propagation is present

in all of them. Further details and discussions of the methodologies can be found in [16], and [41].
                                                                                                           3


  2) System Theoretic Methods: While software analysis has been the subject of an extensive body of

research in computer science, treatment of the topic in the control systems community has been less

systematic. The relevant results in the systems and control literature can be found in the field of hybrid

systems [11]. Much of the available techniques for safety verification of hybrid systems are explicitly

or implicitly based on computation of the reachable sets, either exactly or approximately. These include

but are not limited to techniques based on quantifier elimination [29], ellipsoidal calculus [27], and

mathematical programming [5]. Alternative approaches aim at establishing properties of hybrid systems

through barrier certificates [46], numerical computation of Lyapunov functions [10], [24], or by combined

use of bisimulation mechanisms and Lyapunov techniques [20], [28], [54], [2].

  Inspired by the concept of Lyapunov functions in stability analysis of nonlinear dynamical systems

[25], in this paper we propose Lyapunov invariants for analysis of computer programs. While Lyapunov

functions and similar concepts have been used in verification of stability or temporal properties of system

level descriptions of hybrid systems [48], [10], [24], to the best of our knowledge, this paper is the first

to present a systematic framework based on Lyapunov invariance and convex optimization for verification

of a broad range of code-level specifications for computer programs. Accordingly, it is in the systematic

integration of new ideas and some well-known tools within a unified software analysis framework that we

see the main contribution of our work, and not in carrying through the proofs of the underlying theorems

and propositions. The introduction and development of such framework provides an opportunity for the

field of control to systematically address a problem of great practical significance and interest to both

computer science and engineering communities. The framework can be summarized as follows:

  1) Dynamical system interpretation and modeling (Section II). We introduce generic dynamical system

      representations of programs, along with specific modeling languages which include Mixed-Integer

      Linear Models (MILM), Graph Models, and MIL-over-Graph Hybrid Models (MIL-GHM).
  2) Lyapunov invariants as behavior certificates for computer programs (Section III). Analogous to a

      Lyapunov function, a Lyapunov invariant is a real-valued function of the program variables, and

      satisfies a difference inequality along the trace of the program. It is shown that such functions can
                                                                                                            4


      be formulated for verification of various specifications.
  3) A computational procedure for finding the Lyapunov invariants (Section IV). The procedure is

      standard and constitutes these steps: (i) Restricting the search space to a linear subspace. (ii) Using

      convex relaxation techniques to formulate the search problem as a convex optimization problem,

      e.g., a linear program [6], semidefinite program [9], [55], or a SOS program [42]. (iii) Using convex

      optimization software for numerical computation of the certificates.

       II. DYNAMICAL S YSTEM I NTERPRETATION AND M ODELING OF C OMPUTER P ROGRAMS
  We interpret computer programs as discrete-time dynamical systems and introduce generic models that

formalize this interpretation. We then introduce MILMs, Graph Models, and MIL-GHMs as structured

cases of the generic models. The specific modeling languages are used for computational purposes.

A. Generic Models
  1) Concrete Representation of Computer Programs: We will consider generic models defined by a

finite state space set X with selected subsets X0 ⊆ X of initial states, and X∞ ⊂ X of terminal states,

and by a set-valued state transition function f : X 7→ 2X , such that f (x) ⊆ X∞ , ∀x ∈ X∞ . We denote

such dynamical systems by S(X, f, X0 , X∞ ).

  Definition 1: The dynamical system S(X, f, X0 , X∞ ) is a C-representation of a computer program

P, if the set of all sequences that can be generated by P is equal to the set of all sequences X =

(x(0), x(1), . . . , x(t), . . . ) of elements from X, satisfying

                           x (0) ∈ X0 ⊆ X,          x (t + 1) ∈ f (x (t))   ∀t ∈ Z+                       (1)

The uncertainty in x(0) allows for dependence of the program on different initial conditions, and the

uncertainty in f models dependence on parameters, as well as the ability to respond to real-time inputs.

  Example 1: Integer Division (adopted from [44]): The functionality of Program 1 is to compute the

result of the integer division of dd (dividend) by dr (divisor). A C-representation of the program is

displayed alongside. Note that if dd ≥ 0, and dr ≤ 0, then the program never exits the “while” loop and

the value of q keeps increasing, eventually leading to either an overflow or an erroneous answer. The

program terminates if dd and dr are positive.
                                                                                                                           5




   int IntegerDivision ( int dd, int dr )     Z = Z∩ [−32768, 32767]
   {int q = {0}; int r = {dd};                X = Z4
   while (r >= dr)                            X0 = {(dd, dr, q, r) ∈ X | q = 0, r = dd}
   { q = q + 1;                               X∞ = {(dd, dr, q, r) ∈ X | r < dr}
                                                                    (
        r = r − dr; }                                                 (dd, dr, q + 1, r − dr),   (dd, dr, q, r) ∈ X\X∞
                                              f : (dd, dr, q, r) 7→
   return r; }                                                        (dd, dr, q, r),            (dd, dr, q, r) ∈ X∞

                 Program 1: The Integer Division Program (left) and its Dynamical System Model (right)

  2) Abstract Representation of Computer Programs: In a C-representation, the elements of the state

space X belong to a finite subset of the set of rational numbers that can be represented by a fixed

number of bits in a specific arithmetic framework, e.g., fixed-point or floating-point arithmetic. When

the elements of X are non-integers, due to the quantization effects, the set-valued map f often defines

very complicated dependencies between the elements of X, even for simple programs involving only

elementary arithmetic operations. An abstract model over-approximates the behavior set in the interest of

tractability. The drawbacks are conservatism of the analysis and (potentially) undecidability. Nevertheless,

abstractions in the form of formal over-approximations make it possible to formulate computationally

tractable, sufficient conditions for a verification problem that would otherwise be intractable.

  Definition 2: Given a program P and its C-representation S(X, f, X0 , X∞ ), we say that S(X, f , X 0 , X ∞ )

is an A-representation, i.e., an abstraction of P, if X ⊆ X, X0 ⊆ X 0 , and f (x) ⊆ f (x) for all x ∈ X,

and the following condition holds:
                                                 X ∞ ∩ X ⊆ X∞ .                                                          (2)


  Thus, every trajectory of the actual program is also a trajectory of the abstract model. The definition

of X ∞ is slightly more subtle. For proving Finite-Time Termination (FTT), we need to be able to infer

that if all the trajectories of S eventually enter X ∞ , then all trajectories of S will eventually enter X∞ .

It is tempting to require that X ∞ ⊆ X∞ , however, this may not be possible as X∞ is often a discrete set,

while X ∞ is dense in the domain of real numbers. The definition of X ∞ as in (2) resolves this issue.
                                                                                                           6


  Construction of S(X, f , X 0 , X ∞ ) from S(X, f, X0 , X∞ ) involves abstraction of each of the elements

X, f, X0 , X∞ in a way that is consistent with Definition 2. Abstraction of the state space X often involves

replacing the domain of floats or integers or a combination of these by the domain of real numbers.

Abstraction of X0 or X∞ often involves a combination of domain abstractions and abstraction of functions

that define these sets. Semialgebraic set-valued abstractions of some commonly-used nonlinearities are

presented in Appendix I. Interested readers may refer to [49] for more examples including abstractions

of fixed-point and floating point operations.

B. Specific Models of Computer Programs

  Specific modeling languages are particularly useful for automating the proof process in a computational

framework. Here, three specific modeling languages are proposed: Mixed-Integer Linear Models (MILM),

Graph Models, and Mixed-Integer Linear over Graph Hybrid Models (MIL-GHM).

  1) Mixed-Integer Linear Model (MILM): Proposing MILMs for software modeling and analysis is

motivated by the observation that by imposing linear equality constraints on boolean and continuous

variables over a quasi-hypercube, one can obtain a relatively compact representation of arbitrary piecewise

affine functions defined over compact polytopic subsets of Euclidean spaces (Proposition 1). The earliest

reference to the statement of universality of MILMs appears to be [39], in which a constructive proof is

given for the one-dimensional case. A constructive proof for the general case is given in [49].

  Proposition 1: Universality of Mixed-Integer Linear Models. Let f : X 7→ Rn be a piecewise affine

map with a closed graph, defined on a compact state space X ⊆ [−1, 1]n , consisting of a finite union of

compact polytopes. That is:
                      f (x) ∈ 2Ai x + 2Bi       subject to     x ∈ Xi , i ∈ Z (1, N )

where, each Xi is a compact polytopic set. Then, f can be specified precisely, by imposing linear

equality constraints on a finite number of binary and continuous variables ranging over compact intervals.
                                                                                                            7


Specifically, there exist matrices F and H, such that the following two sets are equal:

      G1 = {(x, f (x)) | x ∈ X}
                                     T                      T
      G2 = {(x, y) | F [ x w v 1 ] = y, H[ x w v 1 ] = 0, (w, v) ∈ [−1, 1]nw × {−1, 1}nv }

  Mixed Logical Dynamical Systems (MLDS) with similar structure were considered in [4] for analysis

of a class of hybrid systems. The main contribution here is in the application of the model to software

analysis. A MIL model of a computer program is defined via the following elements:

  1) The state space X ⊂ [−1, 1]n .

  2) Letting ne = n + nw + nv + 1, the state transition function f : X 7→ 2X is defined by two matrices

      F, and H of dimensions n-by-ne and nH -by-ne respectively, according to:
                                                                                   
                                  T                 T                       nw   nv
             f (x) ∈ F [ x w v 1 ] | H[ x w v 1 ] = 0, (w, v) ∈ [−1, 1] × {−1, 1}     .                   (3)

  3) The set of initial conditions is defined via either of the following:
        a) If X0 is finite with a small cardinality, then it can be conveniently specified by its elements.

           We will see in Section IV that per each element of X0 , one constraint needs to be included

           in the set of constraints of the optimization problem associated with the verification task.

        b) If X0 is not finite, or |X0 | is too large, an abstraction of X0 can be specified by a matrix

           H0 ∈ RnH0 ×ne which defines a union of compact polytopes in the following way:
                                                       T
                      X0 = {x ∈ X | H0 [ x w v 1 ] = 0, (w, v) ∈ [−1, 1]nw × {−1, 1}nv }.                 (4)


  4) The set of terminal states X∞ is defined by
                                                   T
                   X∞ = {x ∈ X | H[ x w v 1 ] 6= 0, ∀w ∈ [−1, 1]nw , ∀v ∈ {−1, 1}nv }.                    (5)

  Therefore, S(X, f, X0 , X∞ ) is well defined. A compact description of a MILM of a program is either

of the form S (F, H, H0 , n, nw , nv ) , or of the form S (F, H, X0 , n, nw , nv ). The MILMs can represent a

broad range of computer programs of interest in control applications, including but not limited to control

programs of gain scheduled linear systems in embedded applications. In addition, generalization of the

model to programs with piecewise affine dynamics subject to quadratic constraints is straightforward.
  Example 2: A MILM of an abstraction of the IntegerDivision program (Program 1: Section II-A), with
                                                                                                                  8


all the integer variables replaced with real variables, is given by S (F, H, H0 , 4, 3, 0) , where

 H0 =                                       H=                     F =
                                                                                                           
    1     0   0 −1      0   0   0   0                              1  0 0 0 0 0 0                      0
                                  0               2 0 −2 1 0 0 1
  0      0   1    0    0   0
                           0  0                                  0  1 0 0 0 0 0                      0 
                                                                                                        
                              ,
                               0               −2 0  0 0 1 0 1,                                        
  0     −2   0    0 0 1 0 1                                       0  0 1 0 0 0 0                   1/M 
                                 −2               0 0  0 0 0 1 1
    −2    0   0    0 0 0 1 1                                         0 −1 0 1 0 0 0                      0

Here, M is a scaling parameter used for bringing all the variables within the interval [−1, 1] .
  2) Graph Model: Practical considerations such as universality and strong resemblance to the natural

flow of computer code render graph models an attractive and convenient model for software analysis.

Before we proceed, for convenience, we introduce the following notation: Pr (i, x) denotes the projection

                                                   n} , and all x ∈ Rn .
operator defined as Pr (i, x) = x, for all i ∈ Z∪ {o

  A graph model is defined on a directed graph G (N , E) with the following elements:

  1) A set of nodes N = {∅} ∪ {1, . . . , m} ∪ {o
                                                n} . These can be thought of as line numbers or code

      locations. Nodes ∅ and o
                             n are starting and terminal nodes, respectively. The only possible transition

      from node o                                    n.
                n is the identity transition to node o

  2) A set of edges E = {(i, j, k) | i ∈ N , j ∈ O (i)} , where the outgoing set O (i) is the set of all

      nodes to which transition from node i is possible in one step. Definition of the incoming set I (i)

      is analogous. The third element in the triplet (i, j, k) is the index for the kth edge between i and

      j, and Aji = {k | (i, j, k) ∈ E} .

  3) A set of program variables xl ∈ Ω ⊆ R, l ∈ Z (1, n) . Given N and n, the state space of a graph

      model is X = N × Ωn . The state x
                                      e = (i, x) of a graph model has therefore, two components: The

      discrete component i ∈ N , and the continuous component x ∈ Ωn ⊆ Rn .
                                        k                                           k                     k
  4) A set of transition labels T ji assigned to every edge (i, j, k) ∈ E, where T ji maps x to the set T ji x =

      {Tjik (x, w, v) | (x, w, v) ∈ Sji
                                     k
                                        }, where (w, v) ∈ [−1, 1]nw × {−1, 1}nv , and Tjik : Rn+nw +nv 7→ Rn
                                    k                                  k                                k
      is a polynomial function and Sji is a semialgebraic set. If T ji is a deterministic map, we drop Sji
                    k
      and define T ji ≡ Tjik (x).

  5) A set of passport labels Πkji assigned to all edges (i, j, k) ∈ E, where Πkji is a semialgebraic set. A

      state transition along edge (i, j, k) is possible if and only if x ∈ Πkji .
                                                                                                          9


  6) A set of semialgebraic invariant sets Xi ⊆ Ωn , i ∈ N are assigned to every node on the graph,

      such that Pr (i, x) ∈ Xi . Equivalently, a state x
                                                       e = (i, x) satisfying x ∈ X\Xi is unreachable.

  Therefore, a graph model is a well-defined specific case of the generic model S(X, f, X0 , X∞ ), with

X = N × Ωn , X0 = {∅} × X∅ , X∞ = {o n} × Xno and f : X 7→ 2X defined as:
                                     n      k
                                                                             o
                      x) ≡ f (i, x) = (j, T ji x) | j ∈ O (i) , x ∈ Πkji ∩ Xi .
                   f (e                                                                                 (6)

  Conceptually similar models have been reported in [44] for software verification, and in [1], [12]

for modeling and verification of hybrid systems. Interested readers may consult [49] for further details

regarding treatment of graph models with time-varying state-dependent transitions labels which arise in

modeling operations with arrays.

  Remarks

   – The invariant set of node ∅ contains all the available information about the initial conditions of the

      program variables: Pr (∅, x) ∈ X∅ .

   – Multiple edges between nodes enable modeling of logical ”or” or ”xor” type conditional transitions.

      This allows for modeling systems with nondeterministic discrete transitions.
                            k
   – The transition label T ji may represent a simple update rule which depends on the real-time input.
                                                                            T
      For instance, if T = Ax + Bw, and S = Rn × [−1, 1] , then x 7→ {Ax + Bw | w ∈ [−1, 1]} .
                        k
      In other cases, T ji may represent an abstraction of a nonlinearity. For instance, the assignment
                                            T
      x 7→ sin (x) can be abstracted by x 7→ {T (x, w) | (x, w) ∈ S} (see Eqn. (46) in Appendix I).

  Before we proceed, we introduce the following notation: Given a semialgebraic set Π, and a polynomial

function τ : Rn 7→ Rn , we denote by Π (τ ) , the set: Π(τ ) = {x | τ (x) ∈ Π} .
    a) Construction of Simple Invariant Sets: Simple invariant sets can be included in the model if they

are readily available or easily computable. Even trivial invariants can simplify the analysis and improve

the chances of finding stronger invariants via numerical optimization.

   – Simple invariant sets may be provided by the programmer. These can be trivial sets representing

      simple algebraic relations between variables, or they can be more complicated relationships that

      reflect the programmer’s knowledge about the functionality and behavior of the program.
                                                                                                                 10


   – Invariant Propagation: Assuming that Tijk are deterministic and invertible, the set
                                                                 −1 
                                                        Πkij Tijk
                                                 S
                                     Xi =                                                                      (7)
                                                  j∈I(i), k∈Aij

      is an invariant set for node i. Furthermore, if the invariant sets Xj are strict subsets of Ωn for all

      j ∈ I (i) , then (7) can be improved. Specifically, the set
                                                                        
                                                   k      k −1           k −1
                                          S
                                 Xi =           Πij Tij           ∩ Xj Tij                                     (8)
                                        j∈I(i), k∈Aij


      is an invariant set for node i. Note that it is sufficient that the restriction of Tijk to the lower

      dimensional spaces in the domains of Πkij and Xj be invertible.

   – Preserving Equality Constraints: Simple assignments of the form Tijk : xl 7→ f (ym ) result in invariant

      sets of the form Xi = {x | xl − f (ym ) = 0} at node i, provided that Tijk does not simultaneously

      update ym . Formally, let Tijk be such that (Tijk x)l −xl is non-zero for at most one element ˆl ∈ Z (1, n) ,

      and that (Tijk x)l̂ is independent of xl̂ . Then, the following set is an invariant set at node i :

                                                                 x | Tijk − I x = 0
                                                  S                        
                                      Xi =
                                             j∈I(i), k∈Aij

  3) Mixed-Integer Linear over Graph Hybrid Model (MIL-GHM): The MIL-GHMs are graph models

in which the effects of several lines and/or functions of code are compactly represented via a MILM. As

a result, the graphs in such models have edges (possibly self-edges) that are labeled with matrices F and

H corresponding to a MILM as the transition and passport labels. Such models combine the flexibility

provided by graph models and the compactness of MILMs. An example is presented in Section V.

C. Specifications

  The specification that can be verified in our framework can generically be described as unreachability

and finite-time termination.
  Definition 3: A Program P ≡ S(X, f, X0 , X∞ ) is said to satisfy the unreachability property with

respect to a subset X− ⊂ X, if for every trajectory X ≡ x (·) of (1), and every t ∈ Z+ , x(t) does

not belong to X− . A program P ≡ S(X, f, X0 , X∞ ) is said to terminate in finite time if every solution

X = x (·) of (1) satisfies x(t) ∈ X∞ for some t ∈ Z+ .
  Several critical specifications associated with runtime errors are special cases of unreachability.
                                                                                                         11


  1) Overflow: Absence of overflow can be characterized as a special case of unreachability by defining:

                                               α−1 x ∞ > 1, α = diag {αi }
                                
                            X− = x ∈ X |

where αi > 0 is the overflow limit for variable i.
  2) Out-of-Bounds Array Indexing: An out-of-bounds array indexing error occurs when a variable

exceeding the length of an array, references an element of the array. Assuming that xl is the corresponding

integer index and L is the array length, one must verify that xl does not exceed L at location i, where

referencing occurs. This can be accomplished by defining X− = {(i, x) ∈ X | |xl | > L} over a graph

model and proving that X− is unreachable. This is also similar to “assertion checking” defined next.
  3) Program Assertions: An assertion is a mathematical expression whose validity at a specific location

in the code must be verified. It usually indicates the programmer’s expectation from the behavior of the

program. We consider assertions that are in the form of semialgebraic set memberships. Using graph

models, this is done as follows:

              at location i : assert x ∈ Ai ⇒ define X− = {(i, x) ∈ X | x ∈ X\Ai } ,

              at location i : assert x ∈
                                       / Ai ⇒ define X− = {(i, x) ∈ X | x ∈ Ai } .

In particular, safety assertions for division-by-zero or taking the square root (or logarithm) of positive

variables are standard and must be automatically included in numerical programs (cf. Sec. III-A, Table I).

  4) Program Invariants: A program invariant is a property that holds throughout the execution of the

program. The property indicates that the variables reside in a semialgebraic subset XI ⊂ X. Essentially,

any method that is used for verifying unreachability of a subset X− ⊂ X, can be applied for verifying

invariance of XI by defining X− = X\XI , and vice versa.

D. Implications of the Abstractions

  For mathematical correctness, we must show that if an A-representation of a program satisfies the

unreachability and FTT specifications, then so does the C-representation, i.e., the actual program. This is

established in the following proposition. The proof is omitted for brevity but can be found in [49].

  Proposition 2: Let S(X, f , X 0 , X ∞ ) be an A-representation of program P with C-representation

S(X, f, X0 , X∞ ). Let X− ⊂ X and X − ⊂ X be such that X− ⊆ X − . Assume that the unreachability
                                                                                                         12


property w.r.t. X − has been verified for S. Then, P satisfies the unreachability property w.r.t. X− .

Moreover, if the FTT property holds for S, then P terminates in finite time.

   Since we are not concerned with undecidability issues, and in light of Proposition 2, we will not

differentiate between abstract or concrete representations in the remainder of this paper.


                      III. LYAPUNOV I NVARIANTS AS B EHAVIOR C ERTIFICATES

   Analogous to a Lyapunov function, a Lyapunov invariant is a real-valued function of the program

variables satisfying a difference inequality along the execution trace.

   Definition 4: A (θ, µ)-Lyapunov invariant for S(X, f, X0 , X∞ ) is a function V : X 7→ R such that

                       V (x+ ) − θV (x) ≤ −µ        ∀x ∈ X, x+ ∈ f (x) : x ∈
                                                                           / X∞ .                       (9)

where (θ, µ) ∈ [0, ∞) × [0, ∞). Thus, a Lyapunov invariant satisfies the difference inequality (9) along

the trajectories of S until they reach a terminal state X∞ .

   It follows from Definition 4 that a Lyapunov invariant is not necessarily nonnegative, or bounded from

below, and in general it need not be monotonically decreasing. While the zero level set of V defines an

invariant set in the sense that V (xk ) ≤ 0 implies V (xk+l ) ≤ 0, for all l ≥ 0, monotonicity depends on

θ and the initial condition. For instance, if V (x0 ) ≤ 0, ∀x0 ∈ X0 , then (9) implies that V (x) ≤ 0 along

the trajectories of S, however, V (x) may not be monotonic if θ < 1, though it will be monotonic for

θ ≥ 1. Furthermore, the level sets of a Lyapunov invariant need not be bounded closed curves.

   Proposition 3 (to follow) formalizes the interpretation of Definition 4 for the specific modeling lan-

guages. Natural Lyapunov invariants for graph models are functions of the form

                                      x) ≡ V (i, x) = σi (x) ,
                                   V (e                          i ∈ N,                               (10)

which assign a polynomial Lyapunov function to every node i ∈ N on the graph G (N , E) .

   Proposition 3: Let S (F, H, X0 , n, nw , nv ) and properly labeled graph G (N , E) be the MIL and graph

models for a computer program P. The function V : [−1, 1]n 7→ R is a (θ, µ)-Lyapunov invariant for P

if it satisfies:
                         V (F xe ) − θV (x) ≤ −µ,       ∀ (x, xe ) ∈ [−1, 1]n × Ξ,
                                                                                                      13


where                                                T
               Ξ = {(x, w, v, 1) | H[ x w v 1 ] = 0, (w, v) ∈ [−1, 1]nw × {−1, 1}nv }.

The function V : N ×Rn 7→ R, satisfying (10) is a (θ, µ)-Lyapunov invariant for P if
                                                                                           k
                  σj (x+ ) − θσi (x) ≤ −µ, ∀ (i, j, k) ∈ E, (x, x+ ) ∈ (Xi ∩ Πkji ) × T ji x.       (11)

Note that a generalization of (9) allows for θ and µ to depend on the state x, although simultaneous

search for θ (x) and V (x) leads to non-convex conditions, unless the dependence of θ on x is fixed

a-priori. We allow for dependence of θ on the discrete component of the state in the following way:

                             k                                                                 k
                 σj (x+ ) − θji σi (x) ≤ −µji , ∀ (i, j, k) ∈ E, (x, x+ ) ∈ (Xi ∩ Πkji ) × T ji x   (12)

A. Behavior Certificates

  1) Finite-Time Termination (FTT) Certificates: The following proposition is applicable to FTT analysis
of both finite and infinite state models.

  Proposition 4: Finite-Time Termination. Consider a program P, and its dynamical system model

S(X, f, X0 , X∞ ). If there exists a (θ, µ)-Lyapunov invariant V : X 7→ R, uniformly bounded on X\X∞ ,

satisfying (9) and the following conditions

                                              V (x) ≤ −η ≤ 0,          ∀x ∈ X0                      (13)

                                µ + (θ − 1) kV k∞ > 0                                               (14)

                                         max (µ, η) > 0                                             (15)

where kV k∞ =     sup V (x) < ∞, then P terminates in finite time, and an upper-bound on the number
                x∈X\X∞

of iterations is given by
                           
                             log (µ + (θ − 1) kV k∞ ) − log (µ)
                                                                , θ 6= 1, µ > 0
                           
                           
                           
                           
                           
                           
                                           log θ
                           
                      Tu =   log (kV k∞ ) − log (η)                                                 (16)
                                                                , θ 6= 1, µ = 0
                                      log θ
                           
                           
                           
                           
                           
                           
                            kV k /µ
                           
                                                                , θ=1
                                  ∞




     Proof: The proof is presented in Appendix II.
                                                                                                            14


  When the state-space X is finite, or when the Lyapunov invariant V is only a function of a subset of

the variables that assume values in a finite set, e.g., integer counters, it follows from Proposition 4 that V

being a (θ, µ)-Lyapunov invariant for any θ ≥ 1 and µ > 0 is sufficient for certifying FTT, and uniform

boundedness of V need not be established a-priori.

  Example 3: Consider the IntegerDivision program presented in Example 1. The function V : X 7→ R,

defined according to V : (dd, dr, q, r) 7→ r is a (1, dr)-Lyapunov invariant for IntegerDivision: at every

step, V decreases by dr > 0. Since X is finite, the program IntegerDivision terminates in finite time. This,

however, only proves absence of infinite loops. The program could terminate with an overflow.

  2) Separating Manifolds and Certificates of Boundedness: Let V be a Lyapunov invariant satisfying
                                                         def
(9) with θ = 1. The level sets of V, defined by Lr (V ) = {x ∈ X : V (x) < r}, are invariant with respect

to (1) in the sense that x(t + 1) ∈ Lr (V ) whenever x(t) ∈ Lr (V ). However, for r = 0, the level sets

Lr (V ) remain invariant with respect to (1) for any nonnegative θ. This is an important property with

the implication that θ = 1 (i.e., monotonicity) is not necessary for establishing a separating manifold

between the reachable set and the unsafe regions of the state space (cf. Theorem 1).

  Theorem 1: Lyapunov Invariants as Separating Manifolds. Let V denote the set of all (θ, µ)-

Lyapunov invariants satisfying (9) for program P ≡ S(X, f, X0 , X∞ ). Let I be the identity map, and for

h ∈ {f, I} define
                                  h−1 (X− ) = {x ∈ X|h (x) ∩ X− 6= ∅} .

A subset X− ⊂ X, where X− ∩ X0 = ∅ can never be reached along the trajectories of P, if there exists

V ∈ V satisfying
                                        sup V (x) <       inf        V (x)                                (17)
                                       x∈X0            x∈h−1 (X− )


and either θ = 1, or one of the following two conditions hold:

                                 (I) θ < 1      and            inf     V (x) > 0.                         (18)
                                                         x∈h−1 (X− )


                                (II) θ > 1      and        sup V (x) ≤ 0.                                 (19)
                                                          x∈X0
                                                                                                                      15


     Proof: The proof is presented in Appendix II.

  The following corollary is based on Theorem 1 and Proposition 4 and presents computationally

implementable criteria for simultaneously establishing FTT and absence of overflow.

  Corollary 1: Overflow and FTT Analysis Consider a program P, and its dynamical system model

S(X, f, X0 , X∞ ). Let α > 0 be a diagonal matrix specifying the overflow limit, and let X− = {x ∈

X | kα−1 xk∞ > 1}. Let q ∈ N∪{∞} , h ∈ {f, I} , and let the function V : X 7→ R be a (θ, µ)-Lyapunov

invariant for S satisfying

                                 V (x) ≤ 0                    ∀x ∈ X0 .                                            (20)
                                                n                o
                                                     −1
                                 V (x) ≥ sup        α h (x) q − 1   ∀x ∈ X.                                        (21)

Then, an overflow runtime error will not occur during any execution of P. In addition, if µ > 0 and

µ + θ > 1, then, P terminates in at most Tu iterations where Tu = µ−1 if θ = 1, and for θ 6= 1 we have:

                             log (µ + (θ − 1) kV k∞ ) − log µ   log (µ + θ − 1) − log µ
                     Tu =                                     ≤                                                    (22)
                                          log θ                          log θ

where kV k∞ =          sup         |V (x)| .
                 x∈X\{X− ∪X∞ }



     Proof: The proof is presented in Appendix II.

  Application of Corollary 1 with h = f typically leads to much less conservative results compared with

h = I, though the computational costs are also higher. See [49] for remarks on variations of Corollary 1

to trade off conservativeness and computational complexity.

     a) General Unreachability and FTT Analysis over Graph Models: The results presented so far in

this section (Theorem 1, Corollary 1, and Proposition 4) are readily applicable to MILMs. These results

will be applied in Section IV to formulate the verification problem as a convex optimization problem.

Herein, we present an adaptation of these results to analysis of graph models.

  Definition 5: A cycle Cm on a graph G (N , E) is an ordered list of m triplets (n1 , n2 , k1 ) , (n2 , n3 , k2 ) , ...,

(nm , nm+1 , km ) , where nm+1 = n1 , and (nj , nj+1 , kj ) ∈ E, ∀j ∈ Z (1, m) . A simple cycle is a cycle

with no strict sub-cycles.
                                                                                                                   16


  Corollary 2: Unreachability and FTT Analysis of Graph Models. Consider a program P and its

graph model G (N , E) . Let V (i, x) = σi (x) be a Lyapunov invariant for G (N , E) , satisfying (12) and

                                               σ∅ (x) ≤ 0,     ∀x ∈ X∅                                           (23)

and either of the following two conditions:

            (I) : σi (x) > 0,            ∀x ∈ Xi ∩ Xi− , i ∈ N \ {∅}                                             (24)
                                                                                              n ko
           (II) : σi (x) > 0,            ∀x ∈ Xj ∩ T −1 (Xi− ) , i ∈ N \ {∅} , j ∈ I (i) , T ∈ T ij              (25)


where
                                        T −1 (Xi− ) = {x ∈ Xi |T (x) ∩ Xi− 6= ∅}

Then, P satisfies the unreachability property w.r.t. the collection of sets Xi− , i ∈ N \ {∅} . In addition,

if for every simple cycle C ∈ G, we have:

                 (θ (C) − 1) kσ (C)k∞ + µ (C) > 0, and µ (C) > 0, and kσ (C)k∞ < ∞,                              (26)
where

                                 k
                                         µ (C) = max µkij ,
                      Q
          θ (C) =               θij ,                            kσ (C)k∞ = max             sup       |σi (x)|   (27)
                    (i,j,k)∈C                    (i,j,k)∈C                    (i,.,.)∈C   x∈Xi \Xi−


then P terminates in at most Tu iterations where

                  X          log ((θ (C) − 1) kσ (C)k∞ + µ (C)) − log µ (C)               X       kσ (C)k∞
        Tu =                                                                +                              .
                                                log θ (C)                                           µ (C)
               C∈G:θ(C)6=1                                                          C∈G:θ(C)=1




     Proof: The proof is presented in Appendix II.

  For verification against an overflow violation specified by a diagonal matrix α > 0, Corollary 2 is

applied with X− = {x ∈ Rn | kα−1 xk∞ > 1}. Hence, (24) becomes σi (x) ≥ p (x) (kα−1 xkq − 1),

∀x ∈ Xi , i ∈ N \ {∅} , where p (x) > 0. User-specified assertions, as well as many other standard safety

specifications such as absence of division-by-zero can be verified using Corollary 2 (See Table I).

     – Identification of Dead Code: Suppose that we wish to verify that a discrete location i ∈ N \ {∅} in

a graph model G (N , E) is unreachable. If a function satisfying the criteria of Corollary 2 with Xi− = Rn

can be found, then location i can never be reached. Condition (24) then becomes σi (x) ≥ 0, ∀x ∈ Rn .
                                                                                                             17


                                                     TABLE I
                A PPLICATION OF C OROLLARY 2 TO THE VERIFICATION OF VARIOUS SAFETY SPECIFICATIONS .


                                                               apply Corollary 2 with:
                        At location i:     assert x ∈ Xa   ⇒   Xi− := {x ∈ Rn | x ∈ Rn \Xa }
                        At location i:     assert x ∈
                                                    / Xa   ⇒   Xi− := {x ∈ Rn | x ∈ Xa }
                        At location i:     (expr.)/xo      ⇒   Xi− := {x ∈ Rn | xo = 0}
                                             √
                        At location i:      2k x
                                                 o         ⇒   Xi− := {x ∈ Rn | xo < 0}
                        At location i:     log (xo )       ⇒   Xi− := {x ∈ Rn | xo ≤ 0}
                        At location i:     dead code       ⇒   Xi− := Rn




  Example 4: Consider the following program

                      void ComputeTurnRate (void)
               L0 : {double x = {0}; double y = {∗PtrToY};
               L1 :   while (1)
               L2 : {      y = ∗PtrToY;
               L3 :        x = (5 ∗ sin(y) + 1)/3;
               L4 :        if x > −1 {
               L5 :               x = x + 1.0472;
               L6 :               TurnRate = y/x; }
               L7 :        else {
               L8 :               TurnRate = 100 ∗ y/3.1416 }}


                                         Program 3.                   Graph of an abstraction of Program 3



 Note that x can be zero right after the assignment x = (5 sin(y) + 1)/3. However, at location L6, x

cannot be zero and division-by-zero will not occur. The graph model of an abstraction of Program 3

is shown next to the program and is defined by the following elements: T65 : x 7→ x + 1.0472, and

T41 : x 7→ [−4/3, 2] . The rest of the transition labels are identity. The only non-universal passport labels

are Π54 and Π84 as shown in the figure. Define

               σ6 (x) = −x2 − 100x + 1, σ5 (x) = −(x + 1309/1250)2 − 100x − 2543/25

               σ0 (x) = σ1 (x) = σ4 (x) = σ8 (x) = −x2 + 2x − 3.

It can be verified that V (x) = σi (x) is a (θ, 1)-Lyapunov invariant for Program 3 with variable rates:
                                                                                                       18


θ65 = 1, and θij = 0 ∀ (i, j) 6= (6, 5). Since

                                    −2 = sup σ0 (x) < inf σ6 (x) = 1
                                            x∈X0            x∈X−


the state (6, x = 0) cannot be reached. Hence, a division by zero will never occur. We will show in the

next section how to find such functions in general.

                             IV. C OMPUTATION OF LYAPUNOV I NVARIANTS

  It is well known that the main difficulty in using Lyapunov functions in system analysis is finding

them. Naturally, using Lyapunov invariants in software analysis inherits the same difficulties. However,

the recent advances in hardware and software technology, e.g., semi-definite programming [18], [53],

and linear programming software [19] present an opportunity for new approaches to software verification

based on numerical optimization.

A. Preliminaries

  1) Convex Parameterization of Lyapunov Invariants: The chances of finding a Lyapunov invariant are

increased when (9) is only required on a subset of X\X∞ . For instance, for θ ≤ 1, it is tempting to

replace (9) with

                      V (x+ ) − θV (x) ≤ −µ, ∀x ∈ X\X∞ : V (x) < 1, x+ ∈ f (x)                      (28)

In this formulation V is not required to satisfy (9) for those states which cannot be reached from X0 .

However, the set of all functions V : X 7→ R satisfying (28) is not convex and finding a solution for

(28) is typically much harder than (9). Such non-convex formulations are not considered in this paper.

  The first step in the search for a function V : X 7→ R satisfying (9) is selecting a finite-dimensional

linear parameterization of a candidate function V :
                                         Xn
                       V (x) = Vτ (x) =       τk Vk (x) ,           τ = (τk )nk=1 , τk ∈ R,         (29)
                                             k=1

where Vk : X 7→ R are fixed basis functions. Next, for every τ = (τk )N
                                                                      k=1 let


                                 φ(τ ) =           max          Vτ (x+ ) − θVτ (x),
                                           x∈X\X∞ , x+ ∈f (x)


(assuming for simplicity that the maximum does exist). Since φ (·) is a maximum of a family of linear
                                                                                                          19


functions, φ (·) is a convex function. If minimizing φ (·) over the unit disk yields a negative minimum,

the optimal τ ∗ defines a valid Lyapunov invariant Vτ ∗ (x). Otherwise, no linear combination (29) yields

a valid solution for (9).

  The success and efficiency of the proposed approach depend on computability of φ (·) and its subgra-

dients. While φ (·) is convex, the same does not necessarily hold for Vτ (x+ ) − θVτ (x). In fact, if X\X∞

is non-convex, which is often the case even for very simple programs, computation of φ (·) becomes a

non-convex optimization problem even if Vτ (x+ ) − Vτ (x) is a nice (e.g. linear or concave and smooth)

function of x. To get around this hurdle, we propose using convex relaxation techniques which essentially

lead to computation of a convex upper bound for φ (τ ).

  2) Convex Relaxation Techniques: Such techniques constitute a broad class of techniques for construct-

ing finite-dimensional, convex approximations for difficult non-convex optimization problems. Some of

the results most relevant to the software verification framework presented in this paper can be found

in [31] for SDP relaxation of binary integer programs, [34] and [40] for SDP relaxation of quadratic

programs, [56] for S-Procedure in robustness analysis, and [43],[42] for sum-of-squares relaxation in

polynomial non-negativity verification. We provide a brief overview of the latter two techniques.

     a) The S-Procedure : The S-Procedure is commonly used for construction of Lyapunov functions

for nonlinear dynamical systems. Let functions φi : X 7→ R, i ∈ Z (0, m) , and ψj : X 7→ R, j ∈ Z (1, n)

be given, and suppose that we are concerned with evaluating the following assertions:

          (I): φ0 (x) > 0, ∀x ∈ {x ∈ X | φi (x) ≥ 0, ψj (x) = 0, i ∈ Z (1, m) , j ∈ Z (1, n)}          (30)
                                                               m
                                                               X                   n
                                                                                   X
                             +
                (II): ∃τi ∈ R , ∃µj ∈ R, such that φ0 (x) >          τi φi (x) +         µj ψj (x) .   (31)
                                                               i=1                 j=1


The implication (II) → (I) is trivial. The process of replacing assertion (I) by its relaxed version (II) is

called the S-Procedure. Note that condition (II) is convex in decision variables τi and µj . The implication

(I) → (II) is generally not true and the S-Procedure is called lossless for special cases where (I) and (II)

are equivalent. A well-known such case is when m = 1, n = 0, and φ0 , φ1 are quadratic functionals. A

comprehensive discussion of the S-Procedure as well as available results on its losslessness can be found
                                                                                                                          20


in [21]. Other variations of S-Procedure with non-strict inequalities exist as well.

     b) Sum-of-Squares (SOS) Relaxation : The SOS relaxation technique can be interpreted as the

generalized version of the S-Procedure and is concerned with verification of the following assertion:

          fj (x) ≥ 0, ∀j ∈ J,               gk (x) 6= 0, ∀k ∈ K,                    hl (x) = 0, ∀l ∈ L ⇒ −f0 (x) ≥ 0,   (32)

where fj , gk , hl are polynomial functions. It is easy to see that the problem is equivalent to verification

of emptiness of a semialgebraic set, a necessary and sufficient condition for which is given by the Posi-

tivstellensatz Theorem [8]. In practice, sufficient conditions in the form of nonnegativity of polynomials

are formulated. The non-negativity conditions are in turn relaxed to SOS conditions. Let Σ [y1 , . . . , ym ]

denote the set of SOS polynomials in m variables y1 , ..., ym , i.e. the set of polynomials that can be
                     t
                       p2i , pi ∈ Pm , where Pm is the polynomial ring of m variables with real coefficients.
                     P
represented as p =
                     i=1

Then, a sufficient condition for (32) is that there exist SOS polynomials τ0 , τi , τij ∈ Σ [x] and polynomials

ρl , such that                    X                   X                    X                     Y
                           τ0 +             τi fi +         τij fi fj +             ρl hl + (        gk )2 = 0
                                        i             i,j                       l

Matlab toolboxes SOSTOOLS [47], or YALMIP [30] automate the process of converting an SOS problem

to an SDP, which is subsequently solved by available software packages such as LMILAB [18], or SeDumi

[53]. Interested readers are referred to [42], [35], [43], [47] for more details.

B. Optimization of Lyapunov Invariants for Mixed-Integer Linear Models

  Natural Lyapunov invariant candidates for MILMs are quadratic and affine functionals.
  1) Quadratic Invariants: The linear parameterization of the space of quadratic functionals mapping

Rn to R is given by:                (                                     T                             )
                                                                       x                x
                            Vx2 =              n
                                    V : R 7→ R | V (x) =                        P               ,P ∈S n+1
                                                                                                                ,       (33)
                                                                       1                1

where Sn is the set of n-by-n symmetric matrices. We have the following lemma.

  Lemma 1: Consider a program P and its MILM S (F, H, X0 , n, nw , nv ) . The program admits a quadratic

(θ, µ)-Lyapunov invariant V ∈ Vx2 , if there exists a matrix Y ∈ Rne ×nH , ne = n + nw + nv + 1, a
                                                                          n+nw
diagonal matrix Dv ∈ Dnv , a positive semidefinite diagonal matrix Dxw ∈ D+    , and a symmetric
                                                                                                                       21


matrix P ∈ Sn+1 , satisfying the following LMIs:

                  LT1 P L1 − θLT2 P L2  He (Y H) + LT3 Dxw L3 + LT4 Dv L4 − (λ + µ) LT5 L5

                                      λ = Trace Dxw + Trace Dv
where
                                                                       T                          T                   T
                                                                                     0(n+nw )×nv
                                                                                                       
     F            In           0n×(ne −n)          In+nw                                                0(ne −1)×1 
L1 =      , L2 =                           , L3 =                    , L4 =  Inv             , L5 = 
                                                                                                 
                                                                                                                         
       L5            01×(ne −1)            1            0(nv +1)×(n+nw )            0                              1
                                                                                      1×nv




     Proof: The proof is presented in Appendix II

  The following theorem summarizes our results for verification of absence of overflow and/or FTT for

MILMs. The result follows from Lemma 1 and Corollary 1 with q = 2, h = f, though the theorem is

presented without a detailed proof.

  Theorem 2: Optimization-Based MILM Verification. Let α : 0 ≺ α  In be a diagonal positive

definite matrix specifying the overflow limit. An overflow runtime error does not occur during any

execution of P if there exist matrices Yi ∈ Rne ×nH , diagonal matrices Div ∈ Dnv , positive semidefinite

diagonal matrices Dixw ∈ Dn+n
                          +
                             w
                               , and a symmetric matrix P ∈ Sn+1 satisfying the following LMIs:

               [ x0 1 ]P [ x0 1 ]T ≤ 0,            ∀x0 ∈ X0                                                          (34)

                 LT1 P L1 − θLT2 P L2  He (Y1 H) + LT3 D1xw L3 + LT4 D1v L4 − (λ1 + µ) LT5 L5                       (35)

                   LT1 ΛL1 − LT2 P L2  He (Y2 H) + LT3 D2xw L3 + LT4 D2v L4 − λ2 LT5 L5                             (36)

where Λ = diag {α−2 , −1} , λi = Trace Dixw + Trace Div , and 0  Dixw , i = 1, 2. In addition, if

µ + θ > 1, then P terminates in a most Tu steps where Tu is given in (22).

  2) Affine Invariants: Affine Lyapunov invariants can often establish strong properties, e.g., bound-

edness, for variables with simple uncoupled dynamics (e.g. counters) at a low computational cost. For

variables with more complicated dynamics, affine invariants may simply establish sign-invariance (e.g.,

xi ≥ 0) or more generally, upper or lower bounds on some linear combination of certain variables. As

we will observe in Section V, establishing these simple behavioral properties is important as they can

be recursively added to the model (e.g., the matrix H in a MILM, or the invariant sets Xi in a graph
                                                                                                            22


model) to improve the chances of success in proving stronger properties via higher order invariants. The

linear parameterization of the subspace of linear functionals mapping Rn to R, is given by:
                             n                                                 o
                        Vx1 = V : Rn 7→ R | V (x) = K T [x       1]T , K ∈ Rn+1 .                         (37)

It is possible to search for the affine invariants via semidefinite programming or linear programming.

  Proposition 5: SDP Characterization of Linear Invariants: There exists a (θ, µ)-Lyapunov invariant

V ∈ Vx1 for a program P ≡ S (F, H, X0 , n, nw , nv ) , if there exists a matrix Y ∈ Rne ×nH , a diagonal
                                                                     (n+nw )×(n+nw )
matrix Dv ∈ Dnv , a positive semidefinite diagonal matrix Dxw ∈ D+                     , and a matrix K ∈ Rn+1

satisfying the following LMI:

             He(LT1 KL5 − θLT5 K T L2 ) ≺ He(Y H) + LT3 Dxw L3 + LT4 Dv L4 − (λ + µ) LT5 L5               (38)

where λ = Trace Dxw + Trace Dv and 0  Dxw .

  Proposition 6: LP Characterization of Linear Invariants: There exists a (θ, µ)-Lyapunov invariant

for a program P ≡ S (F, H, X0 , n, nw , nv ) in the class Vx1 , if there exists a matrix Y ∈ R1×nH , and

nonnegative matrices Dv , Dv ∈ R1×nv , Dxw , Dxw ∈ R1×(n+nw ) , and a matrix K ∈ Rn+1 satisfying:

             K T L1 − θK T L2 − Y H − (Dxw − Dxw )L3 − (Dv − Dv )L4 − (D1 + µ) L5 = 0                    (39a)
                                                                       
                                             D1 + Dv + Dv 1r + Dxw + Dxw 1n+nw ≤ 0                       (39b)

                                                                     Dv , Dv , Dxw , Dxw ≥ 0             (39c)

where D1 is either 0 or −1. As a special case of (39), a subset of all the affine invariants is characterized

by the set of all solutions of the following system of linear equations:

                                        K T L1 − θK T L2 + L5 = 0                                         (40)


  Remark 1: When the objective is to establish properties of the form Kx ≥ a for a fixed K, (e.g., when

establishing sign-invariance for certain variables), matrix K in (38)−(40) is fixed and thus one can make

θ a decision variable subject to θ ≥ 0. Exploiting this convexity is extremely helpful for successfully

establishing such properties.
                                                                                                            23


  The advantage of using semidefinite programming is that efficient SDP relaxations for treatment of

binary variables exists, though the computational cost is typically higher than the LP-based approach.

In contrast, linear programming relaxations of the binary constraints are more involved than the corre-

sponding SDP relaxations. Two extreme remedies can be readily considered. The first is to relax the

binary constraints and treat the variables as continuous variables vi ∈ [−1, 1] . The second is to consider

each of the 2nv different possibilities (one for each vertex of {−1, 1}nv ) separately. This approach can be

useful if nv is small, and is otherwise impractical. More sophisticated schemes can be developed based

on hierarchical linear programming relaxations of binary integer programs [52].

C. Optimization of Lyapunov Invariants for Graph Models

  A linear parameterization of the subspace of polynomial functionals with total degree less than or equal

to d is given by:
                                                                                   
                                                                              n+d
                    Vxd =       n                    T
                          V : R 7→ R | V (x) = K Z (x) , K ∈ R , N =  N
                                                                                                       (41)
                                                                                 d

where Z (x) is a vector of length n+d
                                      
                                   d
                                       , consisting of all monomials of degree less than or equal to d in n

variables x1 , ..., xn . A linear parametrization of Lyapunov invariants for graph models is defined according
                                                     d(i)
to (10), where for every i ∈ N , we have σi (·) ∈ Vx , where d (i) is a selected degree bound for σi (·) .

Depending on the dynamics of the model, the degree bounds d (i) , and the convex relaxation technique,

the corresponding optimization problem will become a linear, semidefinite, or SOS optimization problem.

  1) Node-wise Polynomial Invariants: We present generic conditions for verification over graph models

using SOS programming. Although LMI conditions for verification of linear graph models using quadratic

invariants and the S-Procedure for relaxation of non-convex constraints can be formulated, we do not

present them here due to space limitations. Such formulations are presented in the extended report [49],

along with executable Matlab code in [57]. The following theorem follows from Corollary 2.

  Theorem 3: Optimization-Based Graph Model Verification. Consider a program P, and its graph
                                                                             d(i)
model G (N , E) . Let V : Ωn 7→ R, be given by (10), where σi (·) ∈ Vx . Then, the functions σi (·) ,
                                                                                                                                     24


i ∈ N define a Lyapunov invariant for P, if for all (i, j, k) ∈ E we have:

  −σj (Tjik (x, w)) + θji
                       k
                          σi (x) − µkji ∈ Σ [x, w] subject to (x, w) ∈                                             k
                                                                                          Xi ∩ Πkji × [−1, 1]nw ∩ Sji
                                                                                                              
                                                                                                                               (42)

Furthermore, P satisfies the unreachability property w.r.t. the collection of sets Xi− , i ∈ N \ {∅} , if there

exist εi ∈ (0, ∞) , i ∈ N \ {∅} , such that

                              −σ∅ (x) ∈ Σ [x] subject to x ∈ X∅                                                                (43)

                           σi (x) − εi ∈ Σ [x] subject to x ∈ Xi ∩ Xi− , i ∈ N \ {∅}                                           (44)

As discussed in Section IV-A2b, the SOS relaxation techniques can be applied for formulating the search

problem for functions σi satisfying (42)–(44) as a convex optimization problem. For instance, if

                   Xi ∩ Πkji × [−1, 1]nw ∩ Sji
                                            k
                                       
                                               = {(x, w) | fp (x, w) ≥ 0, hl (x, w) = 0} ,

then, (42) can be formulated as an SOS optimization problem of the following form:
                                            X                X                   X
  −σj (Tjik (x, w)) + θji
                       k
                          σi (x) − µkji −         τ p fp −         τpq fp fq −       ρl hl ∈ Σ [x, w] , s.t. τp , τpq ∈ Σ [x, w] .
                                            p                p,q                 l
Software packages such as SOSTOOLS [47] or YALMIP [30] can then be used for formulating the SOS

optimization problems as semidefinite programs.

                                                     V. C ASE S TUDY
  In this section we apply the framework to the analysis of Program 4 displayed below.

         / ∗ EuclideanDivision.c ∗ /
 F0 :    int IntegerDivision ( int dd, int dr )
 F1 :    {int q = {0}; int r = {dd};
 F2 :    while (r >= dr) {
 F3 :        q = q + 1;
 F4 :        r = r − dr;
 Fo
  n:     return r; }

 L0 :    int main ( int X, int Y ) {
 L1 :    int rem = {0};
 L2 :    while (Y > 0) {
 L3 :        rem = IntegerDivision (X , Y);
 L4 :        X = Y;
 L5 :        Y = rem;
 Lo
  n:     return X; }}



                                    Program 4: Euclidean Division and its Graph Model
                                                                                                                25


Program 4 takes two positive integers X ∈ [1, M] and Y ∈ [1, M] as the input and returns their greatest

common divisor by implementing the Euclidean Division algorithm. Note that the M AIN function in

Program 4 uses the I NTEGER D IVISION program (Program 1).

A. Global Analysis

   A global model can be constructed by embedding the dynamics of the I NTEGER D IVISION program

within the dynamics of M AIN. A labeled graph model is shown alongside the text of the program. This

model has a state space X = N × [−M, M]7 , where N is the set of nodes as shown in the graph, and the

global state x = [X, Y, rem, dd, dr, q, r] is an element of the hypercube [−M, M]7 . A reduced graph

model can be obtained by combining the effects of consecutive transitions and relabeling the reduced

graph model accordingly. While analysis of the full graph model is possible, working with a reduced

model is computationally advantageous. Furthermore, mapping the properties of the reduced graph model

to the original model is algorithmic. Interested readers may consult [51] for further elaboration on this

topic. For the graph model of Program 4, a reduced model can be obtained by first eliminating nodes

Fno, L4 , L5 , L3 , F0 , F1 , F3 , F4 , and L1 , (Figure 1 Left) and composing the transition and passport labels.

Node L2 can be eliminated as well to obtain a further reduced model with only three nodes: F2 , L0 , Lno.

(Figure 1 Right). This is the model that we will analyze. The passport and transition labels associated

with the reduced model are as follows:




Fig. 1.   Two reduced models of the graph model of Program 4.
                                                                                                                                      26


       1                                                                                    2
      T F2F2 : x 7→ [X, Y, rem, dd, dr, q + 1, r − dr]                                     T F2F2 : x 7→ [Y, r, r, Y, r, 0, Y]

      T L0F2 : x 7→ [X, Y, 0, X, Y, 0, X]                                                    n : x 7→ [Y, r, r, dd, dr, q, r]
                                                                                        T F2Lo

      Π2F2F2 : {x | 1 ≤ r ≤ dr − 1}                        Π1F2F2 : {x | r ≥ dr}                       n : {x | r ≤ dr − 1, r ≤ 0}
                                                                                                   ΠF2Lo

Finally, the invariant sets that can be readily included in the graph model (cf. Section II-B2a) are:

XL0 = {x | M ≥ X, M ≥ Y, X ≥ 1, Y ≥ 1} , XF2 = {x | dd = X, dr = Y} , XLo
                                                                        n = {x | Y ≤ 0} .


We are interested in generating certificates of termination and absence of overflow. First, by recursively

searching for linear invariants we are able to establish simple lower bounds on all variables in just two

rounds (the properties established in the each round are added to the model and the next round of search

begins). For instance, the property X ≥ 1 is established only after Y ≥ 1 is established. These results,

which were obtained by applying the first part of Theorem 3 (equations (42)-(43) only) with linear

functionals are summarized in Table II.
                                                                      TABLE II

                                    Property      q≥0       Y≥1       dr ≥ 1     rem ≥ 0        dd ≥ 1   X≥1      r≥0

                            Proven in Round         I          I        I           I             II      II       II

                                 σF2 (x) =         −q       1−Y       1 − dr      −rem          1 − dd   1−X       −r
                              1    , µ1F2F2
                                         
                             θF2F2                (1, 1)     (1, 0)   (1, 0)      (1, 0)        (0, 0)   (0, 0)   (0, 0)
                              2    , µ2F2F2
                                              
                             θF2F2                (0, 0)     (0, 0)   (0, 0)      (0, 0)        (0, 0)   (0, 0)   (0, 0)


We then add these properties to the node invariant sets to obtain stronger invariants that certify FTT and

boundedness of all variables in [−M, M]. By applying Theorem 3 and SOS programming using YALMIP

[30], the following invariants are found1 (after post-processing, rounding the coefficients, and reverifying):


       σ1F2 (x) = 0.4 (Y − M) (2 + M − r)                               σ2F2 (x) = (q × Y + r)2 − M2

       σ3F2 (x) = (q + r)2 − M2                                         σ4F2 (x) = 0.1 (Y − M + 5Y × M + Y2 − 6M2 )

       σ5F2 (x) = Y + r − 2M + Y × M − M2                               σ6F2 (x) = r × Y + Y − M2 − M

The properties proven by these invariants are summarized in the Table III. The specifications that the

  1
   Different choices of polynomial degrees for the Lyapunov invariant function and the multipliers, as well as different choices for θ, µ
and different rounding schemes lead to different invariants. Note that rounding is not essential.
                                                                                                                                            27


program terminates and that x ∈ [−M, M]7 for all initial conditions X, Y∈ [1, M] , could not be established

in one shot, at least when trying polynomials of degree d ≤ 4. For instance, σ1F2 certifies boundedness

of all the variables except q, while σ2F2 and σ3F2 which certify boundedness of all variables including q

do not certify FTT. Furthermore, boundedness of some of the variables is established in round II, relying

on boundedness properties proven in round I. Given σ (x) ≤ 0 (which is found in round I), second

round verification can be done by searching for a strictly positive polynomial p (x) and a nonnegative

polynomial q (x) ≥ 0 satisfying:
                                                 2                                                 1           2
                        q (x) σ (x) − p (x) ( T x i − M2 ) ≥ 0,                          T ∈ {T F2F2 , T F2F2 }                           (45)

where the inequality (45) is further subject to boundedness properties established in round I, as well as

the usual passport conditions and basic invariant set conditions.

                                                                   TABLE III

                    Invariant σF2 (x) =          σ1F2 (x)          σ2F2 (x) , σ3F2 (x)        σ4F2 (x)              σ5F2 (x) , σ6F2 (x)
                        1    , µ1F2F2
                                        
                       θF2F2                       (1, 0)                (1, 0)                 (1, 0)                    (1, 1)

                        2    , µ2F2F2
                                        
                       θF2F2                      (1, 0.8)               (0, 0)                (1, 0.7)                   (1, 1)

            Round I: x2i ≤ M2 for xi =      Y, X, r, dr, rem, dd      q, Y, dr, rem      Y, X, r, dr, rem, dd           Y, dr, rem

            Round II: x2i ≤ M2 for xi =                                 X, r, dd                                         X, r, dd

                     Certificate for FTT            NO                    NO                     NO                  YES, Tu = 2M2


In conclusion, σ2F2 (x) or σ3F2 (x) in conjunction with σ5F2 (x) or σ6F2 (x) prove finite-time termination

of the algorithm, as well as boundedness of all variables within [−M, M] for all initial conditions X, Y ∈

[1, M] , for any M ≥ 1. The provable bound on the number of iterations certified by σ5F2 (x) and σ6F2 (x)

is Tu = 2M2 (Corollary 2). If we settle for more conservative specifications, e.g., x ∈ [−kM, kM]7 for

all initial conditions X, Y ∈ [1, M] and sufficiently large k, then it is possible to prove the properties in

one shot. We show this in the next section.

B. MIL-GH Model

  For comparison, we also constructed the MIL-GH model associated with the reduced graph in Figure 1.

The corresponding matrices are omitted for brevity, but details of the model along with executable Matlab
                                                                                                                                       28


verification codes can be found in [57]. The verification theorem used in this analysis is an extension of

Theorem 2 to analysis of MIL-GHM for specific numerical values of M, though it is certainly possible to

perform this modeling and analysis exercise for parametric bounded values of M. The analysis using the

MIL-GHM is in general more conservative than SOS optimization over the graph model presented earlier.

This can be attributed to the type of relaxations proposed (similar to those used in Lemma 1) for analysis

of MILMs and MIL-GHMs. The benefits are simplified analysis at a typically much less computational

cost. The certificate obtained in this way is a single quadratic function (for each numerical value of
                                                                                                                           1/2
M), establishing a bound γ (M) satisfying γ (M) ≥ X2 + Y2 + rem2 + dd2 + dr2 + q2 + r2                                            . Table

IV summarizes the results of this analysis which were performed using both Sedumi 1 3 and LMILAB

solvers.

                                                                TABLE IV

                                              M     102             103           104            105           106

                  Solver: LMILAB [18]: γ (M)       5.99M          6.34M          6.43M          6.49M         7.05M

                  Solver: SEDUMI [53]: γ (M)       6.00M          6.34M          6.44M          6.49M         NAN
                              1    , µ1F2F2       1, 10−3         1, 10−3       1, 10−3        1, 10−3       1, 10−3
                                                                                                                  
                             θF2F2

                              2    , µ2F2F2       1, 10−3         1, 10−3       1, 10−3        1, 10−3       1, 10−3
                                                                                                                  
                             θF2F2

                      Upperbound on iterations    Tu = 2e4       Tu = 8e4       Tu = 8e5      Tu = 1.5e7     Tu = 3e9



C. Modular Analysis
  The preceding results were obtained by analysis of a global model which was constructed by embedding

the internal dynamics of the program’s functions within the global dynamics of the Main function. In

contrast, the idea in modular analysis is to model software as the interconnection of the program’s

”building blocks” or ”modules”, i.e., functions that interact via a set of global variables. The dynamics

of the functions are then abstracted via Input/Output behavioral models, typically constituting equality

and/or inequality constraints relating the input and output variables. In our framework, the invariant sets

of the terminal nodes of the modules (e.g., the set Xno associated with the terminal node Fno in Program

4) provide such I/O model. Thus, richer characterization of the invariant sets of the terminal nodes of the

modules are desirable. Correctness of each sub-module must be established separately, while correctness
                                                                                                         29


of the entire program will be established by verifying the unreachability and termination properties w.r.t.

the global variables, as well as verifying that a terminal global state will be reached in finite-time.

This way, the program variables that are private to each function are abstracted away from the global

dynamics. This approach has the potential to greatly simplify the analysis and improve the scalability

of the proposed framework as analysis of large size computer programs is undertaken. In this section,

we apply the framework to modular analysis of Program 4. Detailed analysis of the advantages in terms

of improving scalability, and the limitations in terms of conservatism the analysis is an important and

interesting direction of future research.

  The first step is to establish correctness of the I NTEGER D IVISION module, for which we obtain

                                      σ7F2 (dd, dr, q, r) = (q + r)2 − M2

The function σ7F2 is a (1, 0)-invariant proving boundedness of the state variables of I NTEGER D IVISION.

Subject to boundedness, we obtain the function

                                     σ8F2 (dd, dr, q, r) = 2r − 11q − 6Z

which is a (1, 1)-invariant proving termination of I NTEGER D IVISION . The invariant set of node Fno can

thus be characterized by
                               Xno = (dd, dr, q, r) ∈ [0, M]4 | r ≤ dr − 1
                                    


The next step is construction of a global model. Given Xno, the assignment at L3:

                                    L3 : rem = IntegerDivision (X , Y)

can be abstracted by
                                   rem = W, s.t. W ∈ [0, M] , W ≤ Y − 1,

allowing for construction of a global model with variables X, Y, and rem, and an external state-dependent

input W ∈ [0, M] , satisfying W ≤ Y − 1. Finally, the last step is analysis of the global model. We obtain

the function σ9L2 (X, Y, rem) = Y ×M−M2 , which is (1, 1)-invariant proving both FTT and boundedness

of all variables within [M, M] .
                                                                                                         30


                                        VI. C ONCLUDING R EMARKS

  We took a systems-theoretic approach to software analysis, and presented a framework based on convex

optimization of Lyapunov invariants for verification of a range of important specifications for software

systems, including finite-time termination and absence of run-time errors such as overflow, out-of-bounds

array indexing, division-by-zero, and user-defined program assertions. The verification problem is reduced

to solving a numerical optimization problem, which when feasible, results in a certificate for the desired

specification. The novelty of the framework, and consequently, the main contributions of this paper are in

the systematic transfer of Lyapunov functions and the associated computational techniques from control

systems to software analysis. The presented work can be extended in several directions. These include

understanding the limitations of modular analysis of programs, perturbation analysis of the Lyapunov

certificates to quantify robustness with respect to round-off errors, extension to systems with software in

closed loop with hardware, and adaptation of the framework to specific classes of software.


                                                  A PPENDIX I

  Semialgebraic Set-Valued Abstractions of Commonly-Used Nonlinearities:
   – Trigonometric Functions:
  Abstraction of trigonometric functions can be obtained by approximation of the Taylor series expan-

sion followed by representation of the absolute error by a static bounded uncertainty. For instance, an
abstraction of the sin (·) function can be constructed as follows:

                       Abstraction of sin (x)                     x ∈ [− π2 , π2 ]   x ∈ [−π, π]

                       sin (x) ∈ {x + aw | w ∈ [−1, 1]}           a = 0.571          a = 3.142

                       sin (x) ∈ {x − 16 x3 + aw | w ∈ [−1, 1]}   a = 0.076          a = 2.027


 Abstraction of cos (·) is similar. It is also possible to obtain piecewise linear abstractions by first

approximating the function by a piece-wise linear (PWL) function and then representing the absolute

error by a bounded uncertainty. Section II-B (Proposition 1) establishes universality of representation of

generic PWL functions via binary and continuous variables and an algorithmic construction can be found

in [49]. For instance, if x ∈ [0, π/2] then a piecewise linear approximation with absolute error less than
                                                                                                           31


0.06 can be constructed in the following way:

      S = (x, v, w) |x = 0.2 [(1 + v) (1 + w2 ) + (1 − v) (3 + w2 )] ,(w, v) ∈ [−1, 1]2 × {−1, 1}
         
                                                                                                       (46a)

 sin (x) ∈ {T xE | xE ∈ S} , T : xE 7→ 0.45 (1 + v) x + (1 − v) (0.2x + 0.2) + 0.06w1                  (46b)


   – The Sign Function (sgn) and the Absolute Value Function (abs):

  The sign function (sgn(x) = 1I[0,∞) (x) − 1I(−∞,0) (x)) may appear explicitly or as an interpretation of

if-then-else blocks in computer programs (see [49] for more details). A particular abstraction of sgn (·)

is as follows: sgn(x) ∈ {v | xv ≥ 0, v ∈ {−1, 1}}. Note that sgn (0) is equal to 1, while the abstraction

is multi-valued at zero: sgn (0) ∈ {−1, 1} . The absolute value function can be represented (precisely)

over [−1, 1] in the following way:

                     abs (x) = {xv | x = 0.5 (v + w) , (w, v) ∈ [−1, 1] × {−1, 1}}

More on the systematic construction of function abstractions including those related to floating-point,

fixed-point, or modulo arithmetic can be found in the report [49].

                                               A PPENDIX II

     of Proposition 4: Note that (13)−(15) imply that V is negative-definite along the trajectories of S,

except possibly for V (x (0)) which can be zero when η = 0. Let X be any solution of S. Since V is

uniformly bounded on X, we have:

                              − kV k∞ ≤ V (x (t)) < 0, ∀x (t) ∈ X , t > 1.

Now, assume that there exists a sequence X ≡ (x(0), x(1), . . . , x(t), . . . ) of elements from X satisfying

(1), but not reaching a terminal state in finite time. That is, x (t) ∈
                                                                      / X∞ , ∀t ∈ Z+ . Then, it can be

verified that if t > Tu , where Tu is given by (16), we must have: V (x (t)) < − kV k∞ , which contradicts

boundedness of V.


     of Theorem 1: Assume that S has a solution X =(x (0) , ..., x (t− ) , ...) , where x (0) ∈ X0 and

x (t− ) ∈ X− . Let
                                           γh =      inf        V (x)
                                                  x∈h−1 (X− )
                                                                                                             32


First, we claim that γh ≤ max {V (x (t− )), V (x (t− − 1))} . If h = I, we have x (t− ) ∈ h−1 (X− ) and

γh ≤ V (x (t− )). If h = f, we have x (t− − 1) ∈ h−1 (X− ) and γh ≤ V (x (t− − 1)), hence the claim.

Now, consider the θ = 1 case. Since V is monotonically decreasing along solutions of S, we must have:


            γh =      inf     V (x) ≤ max {V (x (t− )), V (x (t− − 1))} ≤ V (x (0)) ≤ sup V (x)           (47)
                   x∈h−1 (X− )                                                          x∈X0


which contradicts (17). Note that if µ > 0 and h = I, then (47) holds as a strict inequality and we can

replace (17) with its non-strict version. Next, consider case (I) , for which, V need not be monotonic

along the trajectories. Partition X0 into two subsets X 0 and X 0 such that X0 = X 0 ∪ X 0 and


                            V (x) ≤ 0 ∀x ∈ X 0 ,      and      V (x) > 0 ∀x ∈ X 0


Now, assume that S has a solution X = (x (0) , ..., x (t− ) , ...) , where x (0) ∈ X 0 and x (t− ) ∈ X− . Since

V (x (0)) > 0 and θ < 1, we have V (x (t)) < V (x (0)) ,       ∀t > 0. Therefore,

            γh =      inf     V (x) ≤ max {V (x (t− )), V (x (t− − 1))} ≤ V (x (0)) ≤ sup V (x)
                   x∈h−1 (X− )                                                          x∈X0


which contradicts (17). Next, assume that S has a solution X = (x (0) , ..., x (t− ) , ...) , where x (0) ∈ X 0

and x (t− ) ∈ X− . In this case, regardless of the value of θ, we must have V (x (t)) ≤ 0, ∀t, implying that

γh ≤ 0, and hence, contradicting (18). Note that if h = I and either µ > 0, or θ > 0, then (18) can be

replaced with its non-strict version. Finally, consider case (II). Due to (19), V is strictly monotonically

decreasing along the solutions of S. The rest of the argument is similar to the θ = 1 case.


     of Corollary 1: It follows from (21) and the definition of X− that:
                             n                  o
                                 α−1 h (x) q − 1 ≥ sup α−1 h (x) ∞ − 1 > 0,
                                                      
             V (x) ≥ sup                                                                ∀x ∈ X.           (48)

It then follows from (48) and (20) that:

                                          inf    V (x) > 0 ≥ sup V (x)
                                       x∈h−1 (X− )            x∈X0

Hence, the first statement of the Corollary follows from Theorem 1. The upperbound on the number of
                                                                                                              33


iterations follows from Proposition 4 and the fact that supx∈X\{X− ∪X∞ } |V (x)| ≤ 1.

     of Corollary 2: The unreachability property follows directly from Theorem 1. The finite time

termination property holds because it follows from (12), (23) and (26) along with Proposition 4, that

the maximum number of iterations around every simple cycle C is finite. The upperbound on the number

of iterations is the sum of the maximum number of iterations over every simple cycle.

     of Lemma 1: Define xe = (x, w, v, 1)T , where x ∈ [−1, 1]n , w ∈ [−1, 1]nw , v ∈ {−1, 1}nv . Recall

that (x, 1)T = L2 xe , and that for all xe satisfying Hxe = 0, there holds: (x+ , 1) = (F xe , 1) = L1 xe . It

follows from Proposition 3 that (9) holds if:

    xTe LT1 P L1 xe − θxTe LT2 P L2 xe ≤ −µ, s.t. Hxe = 0, L3 xe ∈ [−1, 1]n+nw , L4 xe ∈ {−1, 1}nv .       (49)


Recall from the S-Procedure ((30) and (31)) that the assertion σ (y) ≤ 0, ∀y ∈ [−1, 1]n holds if there exists

                                                                     τi (yi2 − 1) = y T τ y − Trace (τ ) , where
                                                                 P
nonnegative constants τi ≥ 0, i = 1, ..., n, such that σ (y) ≤

τ = diag (τi )  0. Similarly, the assertion σ (y) ≤ 0, ∀y ∈ {−1, 1}n holds if there exists a diagonal

                                 µi (yi2 − 1) = y T µy − Trace (µ) . Applying these relaxations to (49), we
                             P
matrix µ such that σ (y) ≤

obtain sufficient conditions for (49) to hold:

xTe LT1 P L1 xe −θxTe LT2 P L2 xe ≤ xTe Y H + H T Y T xe +xTe LT3 Dxw L3 xe +xTe LT4 Dv L4 xe −µ−Trace(Dxw +Dv )
                                                     


Together with 0  Dxw , the above condition is equivalent to the LMIs in Lemma 1.
                                                                                                                                             34


                                                              R EFERENCES

 [1] R. Alur, C. Courcoubetis, N. Halbwachs, T. A. Henzinger, P.-H. Ho X. Nicollin, A. Oliviero, J. Sifakis, and S. Yovine. The algorithmic

     analysis of hybrid systems, Theoretical Computer Science, vol. 138, pp. 3–34, 1995.

 [2] R. Alur, T. Dang, and F. Ivancic. Reachability analysis of hybrid systems via predicate abstraction. In Hybrid Systems: Computation

     and Control. LNCS v. 2289, pp. 35–48. Springer Verlag, 2002.

 [3] C. Baier, B. Haverkort, H. Hermanns, and J.-P. Katoen. Model-checking algorithms for continuous-time Markov chains. IEEE Trans.

     Soft. Eng., 29(6):524–541, 2003.

 [4] A. Bemporad, and M. Morari. Control of systems integrating logic, dynamics, and constraints. Automatica, 35(3):407–427, 1999.

 [5] A. Bemporad, F. D. Torrisi, and M. Morari. Optimization-based verification and stability characterization of piecewise affine and

     hybrid systems. LNCS v. 1790, pp. 45–58. Springer-Verlag, 2000.

 [6] D. Bertsimas, and J. Tsitsikilis. Introduction to Linear Optimization. Athena Scientific, 1997.

 [7] B. Blanchet, P. Cousot, R. Cousot, J. Feret, L. Mauborgne, A. Miné, D. Monniaux, and X. Rival. Design and implementation of a

     special-purpose static program analyzer for safety-critical real-time embedded software. LNCS v. 2566, pp. 85–108, Springer-Verlag,

     2002.

 [8] J. Bochnak, M. Coste, and M. F. Roy. Real Algebraic Geometry. Springer, 1998.

 [9] S. Boyd, L.E. Ghaoui, E. Feron, and V. Balakrishnan. Linear Matrix Inequalities in Systems and Control Theory, SIAM, 1994.

[10] M. S. Branicky. Multiple Lyapunov functions and other analysis tools for switched and hybrid systems. IEEE Trans. Aut. Ctrl.,

     43(4):475–482, 1998.

[11] M. S. Branicky, V. S. Borkar, and S. K. Mitter. A unified framework for hybrid control: model and optimal control theory. IEEE

     Trans. Aut. Ctrl., 43(1):31–45, 1998.

[12] R. W. Brockett. Hybrid models for motion control systems. Essays in Control: Perspectives in the Theory and its Applications,

     Birkhauser, 1994.

[13] E. M. Clarke, O. Grumberg, H. Hiraishi, S. Jha, D.E. Long, K.L. McMillan, and L.A. Ness. Verification of the Future-bus+cache

     coherence protocol. In Formal Methods in System Design, 6(2):217–232, 1995.

[14] E. M. Clarke, O. Grumberg, and D. A. Peled. Model Checking. MIT Press, 1999.

[15] P. Cousot, and R. Cousot. Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation

     of fixpoints. In 4th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, pages 238–252, 1977.

[16] P. Cousot. Abstract interpretation based formal methods and future challenges. LNCS, v. 2000:138–143, Springer, 2001.

[17] D. Dams. Abstract Interpretation and Partition Refinement for Model Checking. Ph.D. Thesis, Eindhoven University of Technology,

     1996.

[18] P. Gahinet, A. Nemirovskii, and A. Laub. LMILAB: A Package for Manipulating and Solving LMIs. South Natick, MA: The Mathworks,

     1994.

[19] ILOG Inc. ILOG CPLEX 9.0 User’s guide. Mountain View, CA, 2003.

[20] A. Girard, and G. J. Pappas. Verification using simulation. LNCS, v. 3927, pp. 272–286 , Springer, 2006.
                                                                                                                                           35


[21] S. V. Gusev, and A. L. Likhtarnikov. Kalman–Popov–Yakubovich Lemma and the S-procedure: A historical essay. Journal of

     Automation and Remote Control, 67(11):1768–1810, 2006.

[22] B. S. Heck, L. M. Wills, and G. J. Vachtsevanos. Software technology for implementing reusable, distributed control systems. IEEE

     Control Systems Magazine, 23(1):21–35, 2003.

[23] M. S. Hecht. Flow Analysis of Computer Programs. Elsevier Science, 1977.

[24] M. Johansson, and A. Rantzer. Computation of piecewise quadratic Lyapunov functions for hybrid systems. IEEE Tran. Aut. Ctrl.

     43(4):555–559, 1998.

[25] H. K. Khalil. Nonlinear Systems. Prentice Hall, 2002.

[26] H. Kopetz. Real-Time Systems Design Principles for Distributed Embedded Applications. Kluwer, 2001.

[27] A. B. Kurzhanski, and I. Valyi. Ellipsoidal Calculus for Estimation and Control. Birkhauser, 1996.

[28] G. Lafferriere, G. J. Pappas, and S. Sastry. Hybrid systems with finite bisimulations. LNCS, v. 1567, pp. 186–203, Springer, 1999.

[29] G. Lafferriere, G. J. Pappas, and S. Yovine. Symbolic reachability computations for families of linear vector fields. Journal of Symbolic

     Computation, 32(3):231–253, 2001.

[30] J. Löfberg. YALMIP : A Toolbox for Modeling and Optimization in MATLAB. In Proc. of the CACSD Conference, 2004. URL:

     http://control.ee.ethz.ch/˜joloef/yalmip.php

[31] L. Lovasz, and A. Schrijver. Cones of matrices and set-functions and 0-1 optimization. SIAM Journal on Optimization, 1(2):166–190,

     1991.

[32] Z. Manna, and A. Pnueli. Temporal Verification of Reactive Systems: Safety. Springer-Verlag, 1995.

[33] W. Marrero, E. Clarke, and S. Jha. Model checking for security protocols. In Proc. DIMACS Workshop on Design and Formal

     Verification of Security Protocols, 1997.

[34] A. Megretski. Relaxations of quadratic programs in operator theory and system analysis. Operator Theory: Advances and Applications,

     v. 129, pp. 365–392. Birkhauser -Verlag, 2001.

[35] A. Megretski. Positivity of trigonometric polynomials. In Proc. 42nd IEEE Conference on Decision and Control, pages 3814–3817,

     2003.

[36] S. Mitra. A Verification Framework for Hybrid Systems. Ph.D. Thesis. Massachusetts Institute of Technology, September 2007.

[37] C. S. R. Murthy, and G. Manimaran. Resource Management in Real-Time Systems and Networks. MIT Press, 2001.

[38] G. Naumovich, L. A. Clarke, and L. J. Osterweil. Verification of communication protocols using data flow analysis. In Proc. 4-th

     ACM SIGSOFT Symposium on the Foundation of Software Engineering, pages 93–105, 1996.

[39] G. L. Nemhauser and L. A. Wolsey. Integer and Combinatorial Optimization. Wiley-Interscience, 1988.

[40] Y.E. Nesterov, H. Wolkowicz, and Y. Ye. Semidefinite programming relaxations of nonconvex quadratic optimization. In Handbook

     of Semidefinite Programming: Theory, Algorithms, and Applications. Dordrecht, Kluwer Academic Press, pp. 361–419, 2000.

[41] F. Nielson, H. Nielson, and C. Hank. Principles of Program Analysis. Springer, 2004.

[42] P. A. Parrilo. Minimizing polynomial functions. In Algorithmic and Quantitative Real Algebraic Geometry. DIMACS Series in Discrete

     Mathematics and Theoretical Computer Science, v. 60, pp. 83-100, 2003.
                                                                                                                                        36


[43] P. A. Parrilo. Structured Semidefinite Programs and Semialgebraic Geometry Methods in Robustness and Optimization. Ph.D. Thesis,

     California Institute of Technology, 2000.

[44] D. A. Peled. Software Reliability Methods. Springer-Verlag, 2001.

[45] B. C. Pierce. Types and Programming Languages. MIT Press, 2002.

[46] S. Prajna. Optimization-Based Methods for Nonlinear and Hybrid Systems Verification. Ph.D. Thesis, California Institute of Technology,

     2005.

[47] S. Prajna, A. Papachristodoulou, P. Seiler, and P. A. Parrilo, SOSTOOLS: Sum of squares optimization toolbox for MATLAB, 2004.

     http://www.mit.edu/˜parrilo/sostools.

[48] S. Prajna, and A. Rantzer, Convex programs for temporal verification of nonlinear dynamical systems, SIAM Journal on Control and

     Opt., 46(3):999–1021, 2007.

[49] M. Roozbehani, A. Megretski and, E. Feron. Optimization of lyapunov invariants in analysis of software systems, Available at

     http://web.mit.edu/mardavij/www/publications.html Also available at http://arxive.org

[50] M. Roozbehani, A. Megretski, E. Feron. Safety verification of iterative algorithms over polynomial vector fields. In Proc. 45th IEEE

     Conference on Decision and Control, pages 6061–6067, 2006.

[51] M. Roozbehani, A. Megretski, E. Frazzoli, and E. Feron. Distributed Lyapunov Functions in Analysis of Graph Models of Software.

     In Hybrid Systems: Computation and Control, Springer LNCS 4981, pp 443-456, 2008.

[52] H. D. Sherali, and W. P. Adams. A hierarchy of relaxations and convex hull characterizations for mixed-integer zero-one programming

     problems. Discrete Applied Mathematics, 52(1):83–106, 1994.

[53] J. F. Sturm. Using SeDuMi 1.02, a MATLAB toolbox for optimization over symmetric cones. Optimization Methods and Software,

     11–12:625–653, 1999. URL: http://sedumi.mcmaster.ca

[54] A. Tiwari, and G. Khanna. Series of abstractions for hybrid automata. In Hybrid Systems: Computation and Control, LNCS, v. 2289,

     pp. 465–478. Springer, 2002.

[55] L. Vandenberghe, and S. Boyd. Semidefinite programming. SIAM Review, 38(1):49–95, 1996.

[56] V. A. Yakubovic. S-procedure in nonlinear control theory. Vestnik Leningrad University, 4(1):73–93, 1977.

[57] http://web.mit.edu/mardavij/www/Software
