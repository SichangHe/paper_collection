                                                  Forward Invariant Cuts to Simplify Proofs of Safety

                                                                              Nikos Aréchiga                      James Kapinski
                                                                        Carnegie Mellon University             Toyota Technical Center
                                                                       Toyota InfoTechnology Center                1630 W. 186th
                                                                            Mountain View, CA                    Gardena, CA 90248
                                                                           narechig@us.toyota-itc.com          jim.kapinski@tema.toyota.com

                                                    Jyotirmoy V. Deshmukh                        André Platzer                        Bruce Krogh
arXiv:1507.05133v2 [cs.LO] 10 Aug 2015




                                                      Toyota Technical Center              Carnegie Mellon University          Carnegie Mellon University
                                                          1630 W. 186th                        5000 Forbes Ave                     5000 Forbes Ave
                                                        Gardena, CA 90248                       Pittsburgh, PA                      Pittsburgh, PA
                                                  jyotirmoy.deshmukh@tema.toyota.com            aplatzer@cs.cmu.edu                krogh@rwanda.cmu.edu


                                         ABSTRACT                                                           states reachable over a fixed time horizon [18, 9, 10, 6].
                                         The use of deductive techniques, such as theorem provers,          While these approaches enjoy a high degree of automation,
                                         has several advantages in safety verification of hybrid sys-       they are restricted in scope and scalability. Tools such as
                                         tems; however, state-of-the-art theorem provers require ex-        SpaceEx [10] and Flow* [6] are susceptible to approxima-
                                         tensive manual intervention. Furthermore, there is often a         tion error that worsens when the reachable set estimation
                                         gap between the type of assistance that a theorem prover           over continuous state-space interacts with discrete switch-
                                         requires to make progress on a proof task and the assis-           ing, leading to false positives. The theorem prover PVS
                                         tance that a system designer is able to provide. This paper        has been used to reason about hybrid systems as compos-
                                         presents an extension to KeYmaera, a deductive verification        able hybrid automata in [2] [1]. However, the continuous
                                         tool for differential dynamic logic; the new technique allows      components are modeled by the explicit solutions of the dif-
                                         local reasoning using system designer intuition about per-         ferential equations. Explicit solutions can only be obtained
                                         formance within particular modes as part of a proof task.          for restricted classes of differential equations, e.g. linear.
                                         Our approach allows the theorem prover to leverage for-            On the other hand, dL allows reasoning about continuous
                                         ward invariants, discovered using numerical techniques, as         dynamics by using only the differential equations.
                                         part of a proof of safety. We introduce a new inference rule          An alternative approach is to employ deductive techniques
                                         into the proof calculus of KeYmaera, the forward invariant         that attempt to construct a symbolic proof of safety us-
                                         cut rule, and we present a methodology to discover useful          ing a semi-interactive theorem prover [23]. This approach
                                         forward invariants, which are then used with the new cut           has several advantages in safety verification of hybrid sys-
                                         rule to complete verification tasks. We demonstrate how            tems. Unlike explicit reach-set computation techniques, the-
                                         our new approach can be used to complete verification tasks        orem provers can handle nonlinear dynamics directly, with-
                                         that lie out of the reach of existing deductive approaches us-     out introducing approximation artifacts. Further, theorem
                                         ing several examples, including one involving an automotive        provers can handle proof tasks that involve symbolic param-
                                         powertrain control system.                                         eters, with only the minimal constraints required to guaran-
                                                                                                            tee safety. This makes the verification result reusable across
                                         Keywords                                                           systems with parameter variations. In the context of dy-
                                                                                                            namical or hybrid systems verification, a human may pro-
                                         hybrid systems, formal verification, theorem provers               vide insight to the theorem proving tool in the form of a
                                                                                                            safety certificate, i.e., a symbolic expression representing a
                                         1.   INTRODUCTION                                                  set containing all reachable states from a given initial set,
                                            Modern physical systems such as automobile engines, avion-      while excluding unsafe states [3, 23]. The tool can then use
                                         ics, and medical devices are controlled by software running        this certificate to automatically prove system safety.
                                         on embedded computing platforms. In the software domain,              In [25], the authors propose an approach that begins with
                                         techniques such as model checking, theorem proving, and ab-        a global candidate certificate (in the form of a differential
                                         stract interpretation have had success verifying purely soft-      invariant) that overapproximates the reachable set of states.
                                         ware systems. For physical systems, techniques from dynam-         Constraints are iteratively added until the overapproxima-
                                         ical systems theory and control theory such as Lyapunov            tion is small enough to exclude the unsafe set, at which point
                                         analysis have long been used to help characterize system           the invariant becomes a safety certificate. This approach has
                                         performance. Most cyberphysical systems, however, are hy-          had success in verifying aircraft roundabout maneuvers us-
                                         brid, i.e., have both continuous state evolution governed by       ing the KeYmaera theorem prover. The notable aspects of
                                         differential equations and discrete mode transitions. Most         this approach are: the initial input is in the form of a global
                                         interesting analyses for such systems (e.g., reachable set esti-   certificate of system safety, which is eagerly constructed and
                                         mation) are undecidable [14], and most software verification       then (globally) refined.
                                         techniques are not directly applicable.                               Cyberphysical system designs have distinct modes of oper-
                                            Many extant approaches to hybrid system verification fo-        ation, with each mode corresponding to an (often) indepen-
                                         cus on creating an overapproximation of the set of system          dently designed controller operating regime. Consequently,
a designer has much more nuanced information about mode-           modes at arbitrary instants. The third system is a simpli-
specific behaviors rather than overarching knowledge about         fied model of an automotive subsystem that is responsible
the entire system. The central thesis of this paper is that        for maintaining the air-to-fuel (A/F) ratio in an engine near
when available, such additional information can be useful          an optimal setpoint. In the automotive context, this is one
for a theorem prover compared to a technique relying on            of the most important control problems with significant im-
construction of a global safety certificate. Our approach en-      plications on fuel efficiency and exhaust gas emissions. We
courages local reasoning and lazy construction of certificates.    are able to prove that the A/F ratio remains within 10% of
   As an example of augmented local information, consider          the optimal setpoint value using KeYmaera.
the scenario where a designer knows that from a given set             The paper is organized as follows. In Sec. 2, we introduce
of modes, there are no discrete transitions to unsafe system       the terminology and review material on hybrid programs
modes. This is a form of local certificate; in this case derived   (the syntactic form used by KeYmaera to express hybrid
purely by reasoning over the finite transition structure of        systems). We introduce the forward invariant cut rule in
the discrete modes. Also consider the designer insight that        Sec. 3, and in Sec. 4 we describe techniques for obtaining
a system is expected to be stable in a certain mode. This          local certificates. We show how the forward invariant cut
is another form of local information that makes it possible        rule can be applied to specific case studies in Sec. 5. Finally,
to employ Lyapunov analysis-based techniques to obtain a           we conclude and discuss related and future work in Sec. 6.
forward invariant set or barrier certificate that provides a
local certificate for that mode.                                   2. HYBRID SYSTEMS AND HYBRID PRO-
   To support local reasoning, we introduce a new proof rule
that we call the forward invariant cut rule in the calculus of        GRAMS
KeYmaera. Given a region of operation and a safe forward             A hybrid system is a dynamical system with continuous-
invariant for the behaviors of that mode, the forward invari-      valued state variables x that take values from a domain X ⊆
ant cut rule allows us to decompose the overall global safety      Rn and a discrete-valued state variable q taken from a finite
proof into three proof obligations: (1) a proof of invariance of   set Q. The system evolves in continuous or discrete time,
the proposed certificate, (2) a proof that the certificate guar-   and the configuration of a hybrid system at time t can be
antees safety, and (3) a proof of safety of everything but the     described by the values of its continuous and discrete state
behaviors associated with the region covered by the certifi-       variables. The discrete-valued states are called modes of
cate. This makes it possible to carve out safe behavior and        operation. The hybrid state is given by the ordered pair
focus analysis only on the remaining part of the system. An        (x, q) ∈ X × Q. In a discrete mode q, the evolution of the
advantage of the decompositional approach is that it allows        continuous-valued state variables is described by ordinary
us to defer the process of producing a local certificate until     differential equations (ODEs)
we reach the relevant sub-goal in the safety proof. In other
                                                                                        ẋ(t) = fq (x(t)),                      (1)
words, it allows lazy construction of safe forward invariants,
which is convenient as certificates for system components          where fq is a function from X to X, often called the vec-
are often easier to obtain than certificates for the aggregate     tor field. Though hybrid systems are often described with
system.                                                            external inputs, in this paper we consider only autonomous
   We demonstrate how our methodology can be used to               systems, i.e., systems in which all transitions depend only
complete verification tasks that lie out of the reach of ex-       on the system states. The state-dependent conditions that
isting deductive techniques. The systems we consider are           allow the system to transition from one discrete state to
hybrid and contain examples with continuous dynamical be-          another (possibly same) discrete state are called guards.
haviors that are described by nonlinear ordinary differential         Hybrid systems are often modeled using hybrid automata.
equations (ODEs). Deductive approaches exist for address-          We use Fig. 1 as a running example. This example has four
ing this class of systems, but the existing frameworks alone       modes and two continuous-valued state variables, with asso-
are insufficient to complete the proof tasks for the exam-         ciated ODEs. Modes are represented by nodes in the graph;
ples herein. For example, the framework in [25] provides a         each mode q has associated a unique set of ODEs (fq ). There
means to address the examples we present using differen-           is a guard on the outgoing transition from q0 to q1 , and the
tial invariants, but the authors provide no general method         transition from q0 to q2 is unguarded, so it can always be
of computing the required differential invariant candidates.       taken. The transition from q0 to q2 has a nondeterministic
Further, their technique requires reasoning about the global       reset allowing a jump from current state values x1 and x2
behavior of the system, as opposed to the local invariant          to any pair of values within the circle of radius two. The
property that we require (a much weaker requirement). The          set of feasible initial conditions is indicated on the default
deductive proof system presented in [8] uses local safety cer-     transition. Mode q0 and q2 have stable linear dynamics, and
tificates to reason about behaviors but applies to continuous      q1 has stable nonlinear dynamics, as in Example 4.10 of [19].
(as opposed to hybrid) systems. Also, [8] provides no con-            While hybrid automata are a convenient formalism, in this
structive means of generating the necessary local safety cer-      paper we use the formalism of hybrid programs in order to
tificates. This is in contrast to our approach, which provides     facilitate the use of the KeYmaera theorem prover, which
methodologies for generating the local safety certificates and     is the workhorse for our deductive approach. Note that any
including them in the proof task.                                  hybrid automaton can be transformed into a hybrid program
   We present three examples that demonstrate the practi-          [23], therefore there is no loss of generality in considering hy-
cal application of the forward invariant cut rule. The first       brid programs. KeYmaera uses the formalism of differential
hybrid system is a hybrid system with three stable modes           dynamic logic, denoted by dL .1
and one fail mode. The second system is a non-autonomous           1
switched system, in which a user has the freedom to switch           The syntax and semantics of dL are described in detail in
                                                                   [23]; we provide only a minimal overview here.
                                                                               q1                     
                                                                h
                                                                    x˙1
                                                                          i             −(x2 + 1)x1
                                                                               =
                                                                    x˙2                     x21                       (x1 < −10 ∨ x1 > 10)∨
                                       x21 + x22 < 1/
                                                                                                                      (x2 < −10 ∨ x2 > 10)/


                   x21 + x22 ≤ 10/                   q0
                                           x˙1                −x1
                                       h         i        h         i
                                                     =                                                         fail
                                           x˙2                −x2             (x1 < −10 ∨ x1 > 10)∨
                                                                              (x2 < −10 ∨ x2 > 10)/

                      /(x1 , x2 ) :=                                                                                  (x1 < −10 ∨ x1 > 10)∨
                      {(v1 , v2 ) | (v12 + v22 < 4)}                           q2                                     (x2 < −10 ∨ x2 > 10)/
                                                                    x˙1                 −3x1 + 13x2
                                                                h         i         h                   i
                                                                    x˙2        =        −5x1 − x2


Figure 1: A running example: All the modes have stable continuous dynamics, and there is a special “fail”
mode.


2.1 The logic dL                                                                        the transition into q2 , which indicates that the state resets
  A hybrid program is specified by the grammar                                          anywhere in the circle of radius two. Line 10 checks the
                                                                                        incoming guard to q2 and Line 11 specifies the associated
  α, β ::= x := θ | x := ∗ | {x′1 = θ1 , . . . , x′n = θn &H}                 (2)       differential equations. Line 13 specifies the guard that al-
           |?H | α ∪ β | α; β | α∗                                            (3)       lows transitions into the failure mode. Note that the guard
                                                                                        does not check the current mode, since all of the modes may
where α, β are hybrid programs, θ, θ1 , . . . , θn are terms, and                       transition into the failure mode if the continuous states leave
H is a logical formula. Intuitively, the program x := θ means                           their prescribed bounds. Line 15 specifies that once the fail-
that x is assigned the value of the term θ. The program                                 ure mode is entered, it is not possible to leave it, and states
x := ∗ means that x is nondeterministically assigned an ar-                             x1 , x2 maintain their previous values and do not evolve.
bitrary real value. The program {x′1 = θ1 , . . . , x′n = θn &H}
means that the variables x1 , . . . , xn evolve continuously for                             Model 1: Hybrid program for the running example
some duration, with derivatives θ1 , . . . , θn , subject to the
                                                                                         1                Ex ≡ I → [(m0 ∪ s07→1 ∪ m1 ∪ s07→2 ∪ m2
constraint that x1 , . . . , xn satisfy H during the entire flow.                       2                              ∪s{0,1,2}7→f ail ∪ mf ail )∗ ]S
The hybrid program ?H behaves as a skip if the logical for-
                                                                                        3                  I ≡ x21 + x22 ≤ 10 ∧ M = q0
mula H is true, and as an abort otherwise.                                              4                 m0 ≡ ?(M = q0 ); {x′1 = −x1 , x′2 = −x2 }
   The nondeterministic choice α ∪ β means that either α or                             5              s07→1 ≡ ?(M = q0 ); ?(x21 + x22 < 1); (M := q1 );
β may be executed. The sequential composition α; β means                                6                 m1 ≡ ?(M = q1 );
that α is executed, then β. The nondeterministic repetition                             7                       {x′1 = −(x2 + 1) ∗ x1 , x′2 = x21 }
α∗ means that α is executed an arbitrary (possibly zero)                                8              s07→2 ≡ ?(M = q0 );
number of times. The logic dL itself is a multimodal logic,                             9                        x1 := ∗; x2 := ∗; ?(x21 + x22 < 4); (M := q2 )
in which the modalities are annotated with hybrid programs.                             10                m2 ≡ ?(M = q2 );
The formulas of dL are described by the grammar:                                        11                      {x′1 = −3x1 + 13x2 , x′2 = −5x1 − x2 }
                                                                                        12    s{0,1,2}7→f ail ≡ ?(−10 > x1 ∨ x1 > 10
           φ, ψ ::= θ1 = θ2 | θ1 ≥ θ2 | ¬φ | φ ∧ ψ                            (4)       13                      ∨ − 10 > x2 ∨ x2 > 10);
                                                                                        14                      M := f ail
                     | φ ∨ ψ | φ → ψ | [α]φ | hαi φ                           (5)       15             mf ail ≡ ?(M = f ail);
                                                                                        16                 S ≡ M 6= f ail
where φ, ψ are formulas of dL , θ1 , θ2 are terms, and α is a
hybrid program. The box modality [α]φ means that φ holds
after all traces of the hybrid program α, and hαi φ means
that φ holds after some execution of hybrid program α.                                  3. SAFETY VERIFICATION WITH THE FOR-
  In the sequel, we will abuse notation and use a formula                                  WARD INVARIANT CUT RULE
interchangeably with the set that it represents.
                                                                                        3.1 The safety verification problem
2.2 Example
                                                                                          The safety verification problem is to decide whether the
   Model 1 shows a hybrid program representation of the                                 state of a system is always contained within a given safe set
running example. Line 2 shows how the subprograms are                                   when starting from a designated initial set, or equivalently,
assembled into the overall program. The system starts at a                              whether none of the behaviors enter an unsafe set.
set I (Line 3), and at each iteration of the loop, one of the                             To formalize this problem in dL , suppose α is a hybrid
subprograms is nondeterministically chosen for attempted                                program representation of the system of interest. Suppose
execution. If the guard of the subprogram succeeds, execu-                              S is the safe set and I is the set of initial states. Then the
tion proceeds. The verification task is to show that when                               behaviors of α are contained in S if the following formula is
this loop is executed any (finite) number of times, the state                           a theorem of dL .
remains in the set S (Line 16). Line 4 is the guard and
differential equations of q0 . Line 5 is the transition from q0                                              I → [α∗ ]S.
to q1 and the required guard. Line 7 proceeds to specify                                The theorem prover KeYmaera can be used to attempt to
the continuous evolution of q1 . Line 9 applies the reset of                            prove this.
   To solve this problem, one might construct a set that con-       and νn = ω, n ∈ N, and (νi , νi+1 ) ∈ ρI,η (α; ?¬C) for each
tains all of the system behaviors from the initial set and is       0 ≤ i ≤ n − 1, it is the case that ω ∈ S.
contained in the safe set. We call such a set a safety cer-            The proof is to show by induction that any state reachable
tificate. A safety certificate must contain the initial state       by α∗ from I in n ≥ 0 executions of α must be contained
set, exclude the unsafe set, and be invariant for system be-        in S. For the base case, let n = 0. Then given ν ∈ I, the
haviors. We say that a set is initialized if it includes the        only reachable state by a sequence of length zero is ν itself.
initial set, safe if it excludes the unsafe set, and invariant if   If ν ∈ C, then ν ∈ S by semantics of the third premise. If
whenever a system behavior enters it, the behavior remains          ν ∈/ C, we have that (ν, ν) ∈ ρI,η ((α; ?¬C)∗ ) by a chain of
in the set for all future time. Arguments with safety cer-          length zero, so that by semantics of the first premise, ν ∈ S.
tificates are captured in dL using the invariant proof rule,           As an inductive hypothesis, suppose that for every ω reach-
where C is a safety certificate:                                    able by a chain of length n, ω ∈ S (i.e., there exists ν0 , . . . , νn
                                                                    with ν0 = ν and ω = νn such that (νi , νi+1 ) ∈ ρI,η (α), for
                 I→C      C → [α]C C → S                            0 ≤ i ≤ n − 1. Now choose any state ξ such that there is a
                          I → [α∗ ]S                                chain of length n+1, ν0 , . . . , νn+1 with ν0 = ν and νn+1 = ξ,
The general task of finding a safety certificate is difficult. In   such that (νi , νi+1 ) ∈ ρI,η (α), for 0 ≤ i ≤ n).
this work, we propose instead a procedure that incremen-               First suppose that νn ∈ C. Then by semantics of the
tally works towards a proof. Instead of a safety certificate,       second premise, νn+1 ∈ C, and then νn+1 ∈ S by semantics
we use knowledge of system structure to propose sets that           of the third premise. On the other hand, suppose νn ∈           / C.
are invariant and safe, but not necessarily initialized, and        We claim that for all j ≤ n, νj ∈    / C. To see this, note that
leverage them in the proof procedure.                               if νj ∈ C for some j ≤ n, then νn ∈ C by semantics of
                                                                    the second premise, which would contradict our assumption
   In our running example, modes q1 and q2 have stable dy-
                                                                    on νn . Then we have that (νi , νi+1 ) ∈ ρI,η (α; ?¬C) for all
namics. If a Lyapunov function can be computed for ei-
                                                                    0 ≤ i ≤ n. By semantics of the first premise, it follows that
ther of these modes, its sublevel sets (i.e., sets of the form
                                                                    ξ ∈ S. This establishes the theorem.
{x | V (x) ≤ ℓ}, for some ℓ ≥ 0) will be invariant. The sub-
level sets will be safe if they exclude the transition to the
fail mode, but they will not be initialized, since they do not
contain mode zero.
                                                                    3.3 Example
3.2 The forward invariant cut rule                                     For the running example, mode q1 has a Lyapunov func-
   A cut in a logical proof allows introducing a lemma. The         tion of the form V1 (x1 , x2 ) = 12 x21 + 21 (x2 − 2)2 as described
main contribution of this paper is a type of cut that sim-          in Example 4.10 of [19] (we discuss Lyapunov functions as
plifies the proof procedure by leveraging knowledge of local        sources of invariants in Section 4). The sublevel set V1 (x1 , x2 ) ≤
invariance properties.                                              5 contains the reset into mode q1 . We apply the forward in-
   The following theorem establishes that if it can be shown        variant cut rule with C1 = V1 (x1 , x2 ) ≤ 5 ∧ M = M1 ,
that a predicate (C) is locally invariant (C → [α]C) and            a set that is invariant and safe, but not initialized since it
safe (C → S), then the remaining conditions (¬C) can be             does not contain the initial mode q0 of the hybrid system.
separately addressed to prove safety.                               The rule application causes the proof tree to split into three
                                                                    branches. The first branch requires showing that whenever
Theorem 1 (Forward Invariant Cut Rule). The following               the system begins in C1 , it remains in C1 . The only por-
is a sound inference rule for the logic dL.                         tions of the model that may run in this case correspond to
       I ∧ ¬C → [(α; ?¬C)∗ ]S C → [α]C           C→S                q1 and the transition into the fail mode (programs m1 and
                                                             (6)    s0,1,27→f ail . KeYmaera can readily check that since the pro-
                       I → [α∗ ]S
                                                                    posed sublevel set excludes the guard into fail, C1 will in
Proof. We first provide a sketch in natural language. Let           fact be satisfied by the end of each system trace. The sec-
ν0 , ν1 , . . . , νn be any sequence of states of any length that   ond branch of the proof tree requires showing C → S, which
are connected by runs of the hybrid program α.                      is trivial, since S is simply M 6= Mf ail and C stipulates
   Case a: Suppose that none of the states in this sequence         M = M1 . We now turn our attention to the third branch.
satisfy C. Then this sequence is a run of the hybrid program           Mode q2 has a Lyapunov function V (x1 , x2 ) = 2x21 + 4x22 ,
(α; ?¬C)∗ , and is safe by the first premise.                       computed using standard Lyapunov techniques for linear
   Case b: On the other hand, suppose νi ∈ C for some               systems. The sublevel set V2 (x1 , x2 ) ≤ 16 contains the cir-
0 ≤ i ≤ n. Then the subsequence νi , . . . , νn is a run of the     cle of radius 2; all incoming transitions to mode q2 make
program α starting from C. Then from the second and third           the system state to be reset to somewhere within this circle.
premises of the rule, νj ∈ C ⊆ S for all j ≥ i. Note that the       By applying a forward invariant cut with C2 = V2 (x1 , x2 ) ≤
subsequence ν1 , . . . , νi−1 is a run of program α∗ such that no   16 ∧ M = M2 , we again get three branches. As before,
state satisfies C, and is therefore safe by the previous case.      C2 is invariant because the only portions of the model that
   The formal proof follows. Fix an interpretation I and            may run from C2 are the programs m2 and s0,1,27→f ail . Since
an assignment η. From semantics of the second premise,              V2 (x1 , x2 ) ≤ 16 excludes the guard to fail, KeYmaera can
if ν ∈ C and (ν, ω) ∈ ρI,η (α), then ω ∈ C. From the                show that C2 represents a safe set. The next branch is to
semantics of the third premise, if ω ∈ C, then ω ∈ S. From          prove that C2 implies safety, which is easy because C2 re-
the semantics of the first premise, if ν ∈ I and ν ∈        / C,    quires M = M2 , which implies M 6= Mf ail .
and ω is such that (ν, ω) ∈ ρI,η ((α; ?¬C)∗ ), then ω ∈ S.             The third branch can now be easily proved with the stan-
This is equivalent to saying that for any ω such that there         dard tools of KeYmaera, using the loop invariant M =
is a sequence of states ν0 , . . . , νn , with ν0 = ν ∈ I ∧ ¬C      M0 ∧ x21 + x22 ≤ 10.
4.     OBTAINING SAFE FORWARD INVARI-                              of states X0 , no system trajectory ever enters an unsafe set
       ANTS                                                        U [26, 27, 28]. The main step is to identify a barrier function
                                                                   B from the domain X to R, with the following properties:
   This section describes various techniques to generate safe
forward invariants, which are invariant sets that are safe but
not necessarily initialized. Let x(t) denote any solution tra-                              ∀x ∈ X0 : B(x) ≤ 0               (10)
jectory for a given (hybrid) dynamical system. A set S is
forward invariant if for all x(0) ∈ S, for all t, x(t) ∈ S. The                              ∀x ∈ U : B(x) > 0               (11)
general problem of identifying safe forward invariant sets                                         ∂B
                                                                             ∀x ∈ X s.t.B(x) = 0 :    f (x) < 0.             (12)
that are useful is hard, but the techniques that we present                                        ∂x
can, in some cases, automatically identify safe forward in-
                                                                      Given a local Lyapunov function V valid in the domain X,
variant sets that can be used to complete safety proofs.
                                                                   if an ℓ can be selected such that (10) and (11) are satisfied,
4.1 Safe forward invariants based on Lyapunov                      then B(x) = V (x) − ℓ is a barrier certificate. This follows
    analysis                                                       from the definition of barrier certificates and the Lyapunov
                                                                   conditions (7) and (8).
   Lyapunov analysis provides one way to construct forward
invariant sets for hybrid systems. We briefly review the           Discovering Barrier Certificates. To discover barrier
basics of Lyapunov analysis to aid our presentation. Lya-          certificates, we employ a modification of a technique from
punov’s direct method is a well-known method used to prove         [29], which uses concrete system executions to generate a se-
stability of dynamical systems within a region of interest.        ries of candidate Lyapunov functions. Our technique, which
In this method, the user provides a local Lyapunov function        is based on [17], uses concrete executions to generate a set of
V : X → R that over the domain of interest X satisfies the         linear constraints. A candidate Lyapunov function is then
following properties:                                              generated by solving a linear program (LP) associated with
                                                                   the constraints. A series of candidates is iteratively im-
     1. Positive definiteness: for all x in X,                     proved upon, using a global optimizer to search the region
                                                                   of interest for executions that violate the condition (8) for
                                V (x) > 0,                  (7)
                                                                   the given candidate. The search is guided by a cost function
        and V (0) = 0;                                             that is based on the Lie derivative of the candidate Lyapunov
                                                                   function; if this cost function can be minimized below 0, then
     2. Derivative negative semidefiniteness: for all x in X,      the minimizing argument provides a witness (which we call a
                                      d                            counterexample) showing the candidate Lyapunov function
                           V̇ (x) =      V (x) ≤ 0,         (8)    is invalid. Once such counterexamples are obtained, we in-
                                      dt
                                                                   clude the associated linear constraints in the LP problem
        and V̇ (0) = 0.                                            and update the candidate Lyapunov function. The process
   Existing techniques from dynamical systems theory use           terminates when the global optimizer is unable to find coun-
sum-of-squares optimization [22] and semidefinite program-         terexamples to the candidate Lyapunov function. We then
ming [4, 30] to identify Lyapunov functions [21] for systems       define the candidate barrier function B(x) = V (x)−l, where
described by polynomial differential equations. A Lyapunov         l is selected such that (10) and (11) are satisfied.
function V is analogous to a ranking function for a discrete          Because there are no optimality guarantees from the global
system, and it maps each continuous state x to a positive          optimizer used to generate the candidate barrier function,
real number, with the property that along any system tra-          the resulting candidate may not strictly satisfy the desired
jectory the quantity V (x) monotonically decreases until it        constraints. To check whether the candidates satisfy (10)
reaches 0 at the equilibrium point. It is well-known that the      through (12), we rely on a satisfiability modulo theories
sublevel set of a Lyapunov function, Sℓ = {x|V (x) ≤ ℓ} is a       (SMT) solver that can handle nonlinear theories over the
forward invariant set, i.e., given any initial condition in Sℓ ,   reals. We use the dReal tool, which uses interval constraint
all future states remain in Sℓ . Thus, any sublevel set of a       propagation (ICP) [11]. dReal supports various nonlinear el-
Lyapunov function that includes the initial set and excludes       ementary functions in the framework of δ-complete decision
the unsafe set serves as a safety certificate [16, 26].            procedures, and returns “unsat” or “δ-sat” for a given query,
Remark: It is well known that for stable linear systems, a         where δ is a precision value specified by the user. When the
quadratic Lyapunov function of the form V = xT P x, where          answer is “unsat”, dReal produces a proof of unsatisfiability;
P is a positive definite matrix, always exists and can be          when it returns “δ-SAT”, it gives an interval of size δ, which
computed by solving the matrix equation                            contains points that may possibly satisfy the query.
                                                                      When a “δ-SAT” result is returned from a query to check
                          AT P + P A = −Q                   (9)    (10) through (12), we do the following: 1.) construct a new
                                                                   linear constraint based on the interval returned, 2.) add
where Q is a positive definite matrix. Several scientific com-
                                                                   the new constraint to the existing set of linear constraints,
puting tools have built-in commands to solve this equation,
                                                                   and 3.) re-solve the LP to obtain an updated (improved)
such as lyap in MATLABand LyapunovSolve in Mathemat-
                                                                   Lyapunov function candidate. If this process terminates,
ica.
                                                                   then the result is a barrier certificate.
   We now show how we can use Lyapunov-like functions to
                                                                      Our technique attempts to use discovered barrier certifi-
construct local certificates.
                                                                   cates locally, that is, for each mode we attempt to construct
Barrier Certificates. In the hybrid systems community,             a certificate that proves that the system will not leave the
barrier certificates have been proposed as a Lyapunov-like         mode. If such a local barrier certificate is found, then the
analysis technique to prove that starting from an initial set      forward invariant cut rule can be applied to the mode to
           x := R21 x                                                 Model 2: A dL model of the nonautonomous switched
                           x := R12 x                                 system
             ẋ = A1 x                    ẋ = A2 x               1          TS ≡ I → [(s ∪ m1 ∪ m2 )∗ ]S
                           x := R21 x                            2            I ≡ M = 1 ∧ x21 + x22 ≤ 0.49
                                                                 3            s ≡ M := 1 ∪ M := 2
                                                                 4           m1 ≡ (?M = 1);
Figure 2: Hybrid automaton for the nonautonomous                 5                 x1 := −0.0658x1 + 0.1965x2 ;
                                                                 6                 x2 := −0.0123x1 − 0.0658x2 ;
switched system.                                                 7                 {x′1 = −x1 + 4x2 , x′2 = −(1/4)x1 − x2 }
                                                                 8           m2 ≡ (?M = 2);
                                                                 9                 x1 := −0.0658x1 − 0.0123x2
simplify the safety proof for the system, which may be com-      10                x2 := 0.1965x1 − 0.0658x2
posed of several modes.                                          11                {x′1 = −x1 − (1/4)x2 , x′2 = 4x1 − x2 }
                                                                 12           S ≡ x1 > −2 ∧ x1 < 2 ∧ x2 > −2 ∧ x2 < −2
4.2 Other Techniques
Bounded-time Invariant Certificates. Inspired by the
success of reachability analysis using bounded model check-        Figure 2 shows a hybrid automaton for the system, and
ing for verifying software systems, there has been significant   Model 2 defines the corresponding hybrid program. For
research in estimating the reachable set of states for hy-       both modes, the continuous-time dynamics given by A1 and
brid and continuous-time dynamical systems. See [10] and         A2 are stable and linear. It is well known that even for
references therein. A common theme among various ap-             switched-mode systems with stable linear continuous dy-
proaches is to compute a flowpipe, or an overapproximation       namics, switching conditions exists that lead to instability
of the reachable states over a bounded time horizon τ . If       for the switched system [5]. We wish to prove that it is not
the computed flowpipe does not intersect with the unsafe         possible to switch between A1 and A2 to create unstable be-
set, then it is safe, and it is invariant over bounded-time,     havior. The safety property for this system is that it should
as the initial states lie within it as wells as the set of all   remain within kxk∞ < 2.0. We apply the forward invari-
future states reachable within a fixed time bound also lie       ant cut rule to the example to successfully prove the safety
within it. The general form of a bounded-time invariant set      property. Below, we describe the steps of the proof.
is Sreach = (R(x) < 0) ∧ (tl < t < tu ), where R(x) < 0 is         Here, the designer provided two forward invariants of the
some compact subset of the domain, and (tl , tu ) is the time    system by independently solving the Lyapunov equation (9)
interval over which the set R(x) < 0 is invariant.               for the linear dynamics of the system in each of the modes.
                                                                 The designer then picked level set sizes to ensure that the
Discrete Transition-based Certificates. These certifi-           resulting forward invariant is contained within the safe set
cates are useful to prove unreachability of certain modes be-    S. The invariants are given below:
cause of the transition structure of an underlying hybrid au-
tomaton. Standard techniques from automata theory such
as identifying strongly connected components can be used                            C1 = {x | V1 (x) < l1 }                   (13)
to obtain such certificates.
                                                                                    C2 = {x | V2 (x) < l2 }                   (14)

5.   CASE STUDIES                                                   Here, V1 (x) = 0.3828x21 + 0.9375x1 x2 + 2.3750x22 , and l1 =
                                                                 1.0, and V2 (x) = 2.3750x21 + 0.9375x1 x2 + 0.3828x22 , and
5.1 Non-autonomous Switched System                               l2 = 1.0.
                                                                    We sequentially apply two forward invariant cuts in order
  Consider an open two-mode system, where an external            to prove Model 2 safe. The first forward invariant cut rule
input can cause the system to arbitrarily switch between the     uses the set C1 as the cut. After applying C1 , the proof tree
system modes. This example is significant, because neither       has three branches: I ∧ ¬C1 → [(α; ?¬C1 )∗ ]S, C1 → [α]C1 ,
of the two modes is invariant, so the proof cannot rely on       and C1 → S. Of these, the third branch is trivially true as
cutting out entire modes.                                        C1 ⊆ S. To prove the second branch valid, KeYmaera needs
  The continuous dynamics are defined by matrices A1 and         to prove that C1 is invariant for the disjuncts.
A2 , as given below:                                                For the hybrid program m1 , KeYmaera computes the for-
                        
                          −1.0    4.0
                                                                ward image of the set C1 when transformed by the linear
                  A1 =                     ,                     transformation R21 , i.e., the set F = {y | y = R21 x ∧
                          −0.25 −1.0
                                                               V1 (x) < l1 }. Note that this step requires performing quan-
                          −1.0 −0.25                             tifier elimination, and KeYmaera utilizes Mathematica for
                  A2 =                     .
                          4.0    −1.0                            this purpose. It then uses C1 as a differential invariant to
                                                                 prove that F → [{x′ = A1 x}]C1 . This is facilitated by
Linear reset maps are applied to the state when a transition
                                                                 the fact that C1 is in fact invariant for the linear system
is made between Modes 1 and 2. The resets are defined by
                                                                 ẋ = A1 x.
matrices R12 and R21 :
                                                                    The difficult branch is the one requiring us to prove that
                                                                 C1 is invariant for mode m2 . To do so, we assist KeYmaera
                                           
                       −0.0658 −0.0123
              R12 =                           ,                  with certain lemmas; the intuition for these lemmas is as
                       0.1965     −0.0658
                                                               follows: Any state in set C1 upon executing the program m2
                       −0.0658 0.1965                            is linearly transformed by R12 . Let Ĉ1 = {x̂ | x ∈ C1 ∧ x̂ =
              R21 =                           .
                       −0.0123 −0.0658                           R12 x} represent the forward image of C1 under R12 . Next,
                                                                       gine subsystems responsible for air intake and A/F ratio
              2                                                        measurement, along with a computer control system tasked
                                                      C1
                                                      C1∗              with regulating the A/F ratio. The objective of the con-
             1.5                                      Ĉ1              troller is to maintain the A/F ratio within 10% of the nom-
                                                      C2
                                                      C2∗              inal operating conditions. The experiment that we model
              1                                       Ĉ2
                                                      I
                                                                       involves an engine connected to a dynamometer – a device
                                                                       that can control the speed of the engine and measure the
             0.5
                                                                       output torque. In our setting, the dynamometer maintains
                                                                       the engine at a constant rotational velocity. The controller
       x2




              0
                                                                       has two modes of operation: (1) a recovery mode, which
            −0.5
                                                                       controls fuel in an open-loop manner, i.e., with only feedfor-
                                                                       ward control action, where the system runs for at most 8ms,
             −1                                                        and (2) a normal run mode, which uses feedback control to
                                                                       regulate the A/F ratio.
            −1.5                                                          The controller measures both the air flow through the air-
                                                                       intake manifold, which it uses to estimate the air pressure
             −2                                                        in the manifold, and the oxygen content of the exhaust gas,
              −2       −1          0           1            2
                                   x1                                  which it uses to compute the A/F ratio. The recovery mode
                                                                       represents the behavior of the controller when recovering
                                                                       from a sensor fault (e.g., aberrant sensor readings, environ-
Figure 3: Illustration of forward invariant sets for                   mental conditions that cause suspicion of the sensor read-
Example 5.1.                                                           ings). During the recovery mode, the controller has no ac-
                                                                       cess to oxygen sensor measurements and so must operate
                                                                       in a feedforward manner (i.e., using only the manifold air
                                                                       flow rate). The normal mode is the typical mode of opera-
we show that the set Ĉ1 is a subset of a specific sublevel set        tion, where the oxygen sensor measurements are used to do
C2∗ of V2 (x). As C2∗ is a sublevel set of V2 (x), it is invariant     feedback control.
under the dynamics ẋ = A2 x; thus, any state beginning                   Model 3 is a hybrid program representing this system.
in C2∗ will remain in C2∗ . Finally, we choose C2∗ in such a           The ODEs representing the continuous dynamics in each
way that C2∗ ⊆ C1 . This essentially proves that any state             mode and the model parameters are presented in the Ap-
starting in the set C1 will be contained in set Ĉ1 , of which         pendix. The state variables p̂, r̂, p̂est , and î represent the
any state will under the dynamics ẋ = A2 x remain in the              manifold pressure, the ratio between actual air-fuel ratio
set C2∗ , i.e., in the state C1 .                                      and the stoichiometric value, the controller estimate of the
  Formally, we establish the following:                                manifold pressure, and the internal state of the PI controller;
                    C1 → [x := R12 x]Ĉ1                        (15)   these variables have all been translated so that the equilib-
                                                                       rium point coincides with the origin. In the recovery mode,
                              Ĉ1 ⊆ C2∗                         (16)   the continuous-time state x is the tuple (p̂, r̂, p̂est , î, τ ). The
                   C2 → [{x = A2 x}]C2∗
                    ∗      ′
                                                                (17)   additional state variable in the recovery mode represents the
                              C2∗ ⊆ C1                          (18)   state of a timer that evolves according to the ODE τ̇ = 1.
                                                                       In the normal mode, the state is given by (p̂, r̂, p̂est , î).
   We can combine these to infer that C1 → [m2 ]C1 .                      We assume the system is within 1.0% of the nominal value
   Finally, the first branch of the proof considers I ∧¬C1 ; this      at the initialization of the recovery mode. This represents
contains the set of initial states not in C1 . These can now           the case where the system was previously in a mode of oper-
be addressed by the second forward invariant cut (set C2 )             ation that accurately regulated the A/F ratio to the desired
following a symmetric argument as above. After applying                setpoint. A domain of interest for the state variables is given
the second cut C2 , the first branch has an empty antecedent           by kxk∞ < 0.2.
(I ∧ ¬C1 ∧ ¬C2 is empty), i.e., the proof has accounted for
                                                                       Safety proof using forward invariant cut. The verifica-
all initial states, which closes the proof. The sets we have
                                                                       tion goal is to ensure that in the given experimental setting,
discussed are shown in Figure 3.
                                                                       the system always remains within 10% of the nominal A/F
5.2 Engine fuel control                                                ratio after a fixed recovery time of 0.8 ms has passed. In
                                                                       other words, we wish to show that the system begins in the
Model. Our second case study is a hybrid system represent-             recovery mode, with the initial set of continuous states de-
ing an automotive fuel control application. Environmental              fined by init = {x | kxk∞ < 0.01}; the system transitions
concerns and government legislation require that the fuel              to the normal mode after at most 8.0 ms; and the system
economy be maximized and the exhaust gas emissions (e.g.,              never transitions to the unsafe set, where |r| > 0.1, within
hydrocarbons, carbon monoxide, and nitrogen oxides) be                 the domain of interest kxk∞ < 0.2.
minimized. At the ideal air-to-fuel (A/F) ratio, also known               In previous work [17], the authors had established a for-
as the stoichiometric value, both these quantities are op-             ward invariant set for the normal mode of operation using a
timized. We present an automotive control system whose                 barrier certificate formulation. The authors formulated the
purpose is to accurately regulate the A/F ratio.                       barrier certificate using simulation-guided techniques to ob-
  The system dynamics and parameters were derived from                 tain a candidate Lyapunov function V and a number ℓ to
a published model [15] and then simplified, as in [17]. The            propose a barrier function of the form B(x) = V (x) − ℓ.
model consists of a simplified version of the physics of en-           Here, V (x) = zT P z, and z is a vector of all monomials of
     Model 3: A dL model of a closed-loop fuel control sys-          the remaining (middle) proof obligation KeYmaera uses the
     tem                                                             SMT solver dReal [11]. In particular, it asks dReal if the
 1         EFC ≡                                                     query (B(x) = 0) ∧ ( ∂B ∂x
                                                                                                · fnormal (x) > −ǫ) is unsatisfiable,
                                                 ∗
   I → [ m1 ∪ m2 ∪ s17→2 ∪ s{1,2}7→f ail ∪ mf ail ]S                 where ǫ is a small positive number.
 2             I ≡ (−0.001 ≤ p ≤ 0.001)                                 In order to discharge the proof obligation for m2 , s{1,2}7→f ail ,
 3                 ∧ (−0.001 ≤ r ≤ 0.001) ∧                          KeYmaera needs to show that if B(x) < 0 holds, either of
 4                 ∧ (pest = 0 ∧ i = 0 ∧ M = 1)                      these programs cannot invalidate C by transitioning to mode
 5           m1 ≡ (?M = recovery ; ?τ ≤ 0.008;                       f ail. It proves this by showing that the set B(x) < 0 is a
 6                 {∃ℓ1 .∃ℓ2 .∃ℓ3                                    subset of the safe set using dReal.
 7                   (−0.86 ≤ ℓ1 ≤ 0.74)
 8                   (−0.17 ≤ ℓ2 ≤ 0.18)                             Obligation 2. C → S
 9                   (−0.81 ≤ ℓ3 ≤ 0.68)                             This obligation is trivial as S requires the mode to be f ail,
10                   ∧ (p′ = ℓ1 ) ∧ (r ′ = ℓ2 ) ∧ (p′est = ℓ3 ) ∧
                                                                     while C says that the mode is normal mode.
11                   i′ = 0 & τ ′ = 1 ∧ τ ≤ 0.008}
12        s17→2 ≡ (?M = recovery ; ?τ ≥ 0.008;                       Obligation 3. I ∧ ¬C → [(α; ?¬C)∗ ]S
13                  M := normal ; )
14           m2 ≡ (?M = normal ;
15                  {p′ = fp ,
                                                                        To prove this obligation, we use the lemma that the set
16                  r ′ = fr ,                                       C1 is an invariant for all states remaining in I ∧ ¬C . This
17                  p′est = fpest ,                                  is a bounded-time invariant certificate.
18                  i′ = f i ,
19                  & − 0.02 ≤ p ≤ 0.02 ∧ − 0.02 ≤ r ≤ 0.02
20                  ∧ − 0.02 ≤ pest ≤ 0.02 ∧ − 0.02 ≤ i ≤ 0.02}        C1 ≡ (M 6= mf ail ) ∧ (0 ≤ τ ≤ 0.008) ∧ (x ∈ Sreach )        (22)
21 s{1,2}7→f ail ≡ (?(r < −0.1 ∨ r > 0.1);
22                   M := f ail)                                       Here Sreach is an overapproximation of reachable sets by
23        mf ail ≡ (?(r < −0.1 ∨ r > 0.1);                           using upper and lower bounds on ṗ and ṙ computed using
24                   M := f ail)                                     dReal. The proof for this branch continues using standard
25      S        ≡ M 6= f ail                                        KeYmaera deduction procedures. There is one additional
                                                                     barrier certificate application to show that the normal mode,
                                                                     when starting from this set, lands within the barrier certifi-
 degree ≤ 2 of the state variables p̂, r̂, p̂est and î. Note that   cate and therefore also respects this invariant. This requires
 z thus contains 14 monomials, and P is a 14x14 matrix. We           a derivative negativity argument, which KeYmaera again
 omit the resulting P matrix for brevity.                            handles via an external dReal query.
    We use the set enclosed by the barrier function to formu-
 late the forward invariant cut                                      6. RELATED WORK AND CONCLUSIONS
                C ≡ (M = normal) ∧ (B(x) ≤ 0).               (19)    Lazy abstraction. In software verification using conser-
                                                                     vative abstractions, an abstract program can be viewed as
   Application of the forward invariant cut inference rule (6),      a proof of program correctness if it satisfies the correctness
 generates three proof obligations that KeYmaera has to dis-         property of interest. A popular paradigm is that of lazy
 charge.                                                             abstraction [13], where the abstract program is not derived
 Obligation 1. C → [α]C                                              from a global set of predicates, but is an abstract model
 Note that once we define C, the hybrid programs m1 , s17→2          in which predicates change from state to state. Such an
 can be excised by KeYmaera, as both have the hybrid pro-            abstraction is obtained through the process of lazy refine-
 gram ?M = recovery as their first item, which is inconsistent       ment, where abstraction is done on-the-fly with a goal of
 with C. Thus, KeYmaera can then focus on proving this               eliminating local spurious counterexamples. While the ex-
 obligation only for the programs m2 , s{1,2}7→f ail and mf ail .    act mechanics of our technique are different, our technique
   In order to discharge the obligation for the program m2 ,         also generates correctness proofs consisting of lazily gener-
 we first perform some trivial simplifications with KeYmaera         ated local invariants.
 that leaves us with the following proof goal:                       Logical cuts. In classical logic, a cut serves the role of
                                                                     a lemma. In Gentzen’s sequent calculus [12], the cut rule
 (B(x) ≤ 0) → [{x′ = f (x)&H}](B(x) ≤ 0) ∧ (M = normal )             splits the proof tree into two branches, one in which the
                                                         (20)        lemma can be used as an assumption, and another in which
   To discharge (20), we can use the barrier certificate rule        it must be proved. The cut-elimination theorem, states that
 shown in (21) that we have added to KeYmaera’s proof cal-           any proof of the sequent calculus that uses the cut rule has
 culus.                                                              another proof that does not use the cut rule. Ideas similar
                                                                     to Gentzen’s cut rule have been developed for other reason-
                                                                     ing frameworks. Craig interpolants [7] have been used to
  init → B(x) ≤ 0 B(x) = 0 → ∂B   ∂x
                                     ·f (x) < 0 B(x) ≤ 0 → safe      compute cuts in frameworks that leverage first-order logic,
                    init → [{x′ = f (x)}]safe                        and they have been used successfully in a model checking
                                                              (21)   framework [20]. The differential cut rule of dL makes it
 where H is the domain of evolution of the continuous dy-            possible to introduce lemmas about the continuous evolu-
 namics. In our application of the barrier certificate rule,         tion of differential equations. It has been shown that there
 we substitute init with (B(x) ≤ 0) and safe with (B(x) ≤            are theorems that cannot be proved without differential cuts,
 0)∧(M = normal). The first and the third proof obligations          i.e., the differential cut strictly adds deductive power [24].
 in the barrier certificate rule are then trivially satisfied. For   Overall, the approach provides an iterative method to find a
safety certificate, by proposing sets that are initialized and         (2013)
invariant, and repeating the differential cut procedure until      [7] Craig, W.: Three uses of the Herbrand-Gentzen
safety can be proved. This work proposes a forward invari-             theorem in relating model theory and proof theory. J.
ant cut rule, in which a lemma is proved about the evolution           Sym. Logic 3, 269–285 (1957)
of a hybrid system model. The proof rule requires showing          [8] Dimitrova, R., Majumdar, R.: Deductive control
that a certain set is safe and invariant, and allows the proof         synthesis for alternating-time logics. In: Proc. of the
to continue for the behaviors that are not initialized within          International Conference on Embedded Software. p. 14
the set. The forward invariant cut may be repeated, until              (2014)
a proof of overall system safety is attained. Most crucially,      [9] Frehse, G.: PHAVer: Algorithmic verification of
the proposed cuts allow the verification process to leverage           hybrid systems past HyTech. STTT 10(3), 263–279
a designer’s knowledge of local system properties.                     (2008)
Deductive Proof System for Temporal Logic. In [8],                [10] Frehse, G., Le Guernic, C., Donzé, A., Cotton, S.,
the authors present a deductive proof system for proving               Ray, R., Lebeltel, O., Ripado, R., Girard, A., Dang,
alternating-time temporal logic assertions on a continuous             T., Maler, O.: SpaceEx: Scalable verification of hybrid
dynamical system. Some of the proof rules presented require            systems. In: CAV. pp. 379–395 (2011)
the user to provide auxilary predicates to establish proof-       [11] Gao, S., Avigad, J., Clarke, E.M.: δ-complete decision
subgoals. These predicates are essentially logical cuts, and           procedures for satisfiability over the reals. In: J.
in particular can be barrier certificates. The key feature of          Automated Reasoning. pp. 286–300 (2012)
our approach is that we provide an automated mechanism            [12] Gentzen, G.: Untersuchungen Ãijber das logische
to leverage user insight about parts of the system to obtain           Schließen I,II. Mathematische Zeitschrift 39(2), 39(3):
localized forward invariant cuts. It would be interesting to           176–210, 405–431 (1935)
see if the automation that we develop in this paper could be      [13] Henzinger, T.A., Jhala, R., Majumdar, R., Sutre, G.:
used to mechanize the proof system presented in [8].                   Lazy abstraction. In: ACM SIGPLAN Notices.
Conclusions. This paper presents a method to leverage                  vol. 37, pp. 58–70 (2002)
knowledge of local system behavior within a deductive frame-      [14] Henzinger, T.A., Kopke, P.W., Puri, A., Varaiya, P.:
work. In this framework, designer knowledge of system be-              What’s Decidable about Hybrid Automata? JCSS
havior can be leveraged lazily as part of a proof of global            57(1), 94 – 124 (1998)
system safety. The designer proposes sets that are invariant      [15] Jin, X., Deshmukh, J.V., Kapinski, J., Ueda, K.,
and safe, which allows certifying the safety of some region of         Butts, K.: Powertrain Control Verification
state space. In future work, we would like to investigate the          Benchmark. In: Hybrid Systems: Computation and
use of sets that are safe, but not initialized or invariant, as        Control (2014)
part of a proof effort. An example of this is when a collec-      [16] Johansson, M., Rantzer, A.: Computation of piecewise
tion of modes have continuous barriers that the differential           quadratic Lyapunov functions for hybrid systems.
equations may not cross, but the set is not invariant because          IEEE Tran. on Automatic Control 43(4), 555–559
there are outgoing transitions that are not excluded by the            (1998)
set.                                                              [17] Kapinski, J., Deshmukh, J.V., Sankaranarayanan, S.,
                                                                       Aréchiga, N.: Simulation-guided Lyapunov analysis
7.   REFERENCES                                                        for hybrid dynamical systems. In: Hybrid Systems:
 [1] Abraham-Mumm, E., Hannemann, U., Steffen, M.:                     Computation and Control (2014)
     Verification of hybrid systems: formalization and            [18] Kapinski, J., Krogh, B.H.: Verifying asymptotic
     proof rules in pvs. In: Engineering of Complex                    bounds for discrete-time sliding mode systems with
     Computer Systems, 2001. Proceedings. Seventh IEEE                 disturbance inputs. In: ACC. vol. 3, pp. 2852–2857
     International Conference on. pp. 48–57 (2001)                     (2004)
 [2] Abraham-Mumm, E., Hannemann, U., Steffen, M.:                [19] Khalil, H.K.: Nonlinear Systems. Prentice Hall (2002)
     Assertion-based analysis of hybrid systems with pvs.         [20] McMillan, K.L.: Lazy abstraction with interpolants.
     In: Moreno-Diaz, R., Buchberger, B., Luis Freire, J.              In: Computer Aided Verification. pp. 123–136 (2006)
     (eds.) Computer Aided Systems Theory, EUROCAST
                                                                  [21] Meiss, J.D.: Differential Dynamical Systems
     2001, Lecture Notes in Computer Science, vol. 2178,
                                                                       (Monographs on Mathematical Modeling and
     pp. 94–109. Springer Berlin Heidelberg (2001),
                                                                       Computation). SIAM (2007)
     http://dx.doi.org/10.1007/3-540-45654-6_8
                                                                  [22] Parrilo, P.A.: Structured Semidefinite Programs and
 [3] Beckert, B., Hähnle, R., Schmitt, P.H.: Verification of
                                                                       Semialgebraic Geometry Methods in Robustness and
     object-oriented software: The KeY approach.
                                                                       Optimization. Ph.D. thesis, California Institute of
     Springer-Verlag (2007)
                                                                       Technology (2000)
 [4] Boyd, S., Ghaoui, L.E., Feron, E., Balakrishnan, V.:         [23] Platzer, A.: Logical Analysis of Hybrid Systems.
     Linear Matrix Inequalities in System and Control
                                                                       Springer (2010)
     Theory, vol. 15. SIAM (1994)
                                                                  [24] Platzer, A.: The structure of differential invariants
 [5] Branicky, M.S.: Stability of switched and hybrid
                                                                       and differential cut elimination. Logical Methods in
     systems. In: Decision and Control, 1994., Proceedings             Computer Science 8(4), 1–38 (2012)
     of the 33rd IEEE Conference on. vol. 4, pp.
                                                                  [25] Platzer, A., Clarke, E.M.: Computing differential
     3498–3503. IEEE (1994)
                                                                       invariants of hybrid systems as fixedpoints. In:
 [6] Chen, X., Abraham, E., Sankaranarayanan, S.: Flow*:
                                                                       Computer Aided Verification (2008)
     An Analyzer for Non-Linear Hybrid Systems. In: CAV
[26] Prajna, S.: Optimization-based methods for nonlinear
     and hybrid systems verification. Ph.D. thesis,
     California Institute of Technology, Caltech, Pasadena,
     CA, USA (2005)
[27] Prajna, S.: Barrier certificates for nonlinear model
     validation. Automatica 42(1), 117–126 (2006)
[28] Prajna, S., Jadbabaie, A.: Safety Verification of
     Hybrid Systems Using Barrier Certificates. In: Hybrid
     Systems: Computation and Control. pp. 477–492
     (2004)
[29] Topcu, U., Seiler, P., Packard, A.: Local stability
     analysis using simulations and sum-of-squares
     programming. Automatica 44, 2669–2675 (2008)
[30] Vandenberghe, L., Boyd, S.: Semidefinite
     Programming. SIAM Review 38(1), 49–95 (March
     1996)
APPENDIX                                                                            8. valI,η (ν, [α]φ) = true iff valI,η (ω, φ) = true for all
                                                                                       states ω for which the transition relation (defined below)
Appendix                                                                               satisfies (ν, ω) ∈ ρI,η (α).
A Semantics of dL                                                                   9. valI,η (ν, hαi φ) = true iff valI,η (ω, φ) for some state
  We follow the development of [23], Chapter 2. Symbols                                ω such that the transition relation satisfies (ν, ω) ∈
in dL are classified into three different syntactic categories,                        ρI,η (α).
depending on their role.
                                                                                     We now define the transition semantics of hybrid pro-
  1. Σr represents a set of rigid symbols that cannot change                      grams. We already saw a glimpse of it in the definition
     their value, such as 0, 1, +, ·;                                             of valuation of formulas, since the formulas and programs of
  2. Σf l represents a set of flexible symbols, also called state                 dL are constructed coinductively.
     variables, which change their value as the system evolves;                   Definition 3 (Transition semantics of hybrid programs ([23],
  3. V represents a set of logical variables, which do not                        Defn. 2.7)). The valuation of a hybrid program α, denoted
     change as the system evolves, but can be quantified                          ρI,η (α) is a transition relation on states that specifies which
     over universally and existentially; they often serve the                     states are reachable from a state ν under the program α, and
     role of parameters.                                                          is defined inductively as follows.
An interpretation is a function I that associates functions                         1. (ν, ω) ∈ ρI,η (x1 := θ1 , . . . , xn := θn ) iff the state ω
and relations over the reals to function and relation sym-                              equals the state obtained by modification of ν as ν[x1 7→
bols in Σr . The standard arithmetic operators and relations                            valI,η (ν, θ1 )], . . . , ν[xn 7→ valI,η (ν, θn )].
symbols, such as +, ·, ≥, are interpreted as usual.A state is                       2. (ν, ω) ∈ ρI,η ({x′1 = θ1 , . . . , x′n = θn &H}) iff there is a
a map ν : Σf l 7→ R, which maps a real value to each state                             flow f of some duration r ≥ 0 from ν to ω along the
variable. An assignment η : V 7→ R is a map that prescribes                            differential equations x′1 = θ1 , . . . , x′n = θn that always
the value of the logical variables. Note that the value of the                         respects the invariant H.
logical variables does not depend on the state.                                     3. ρI,η (?χ) = {(ν, ν) | valI,η (ν, χ) = true}
   A state variable is a term, and a logical variable is also a
term. The result of applying a function of arity n to n terms                       4. ρI,η (α ∪ β) = ρI,η (α) ∪ ρI,η (β)
is also a term. Nothing else is a term.                                             5. ρI,η (α; β) = ρI,η (α) ◦ ρI,η (β)
                                                                                    6. (ν, ω) ∈ ρI,η (α∗ ) iff there is a sequence of states states
Definition 1 (Valuation of terms ([23], Defn. 2.5)). The
                                                                                       ν0 , . . . , νn with n ≥ 0, ν = ν0 , and νn = ω such that
valuation of terms with respect to interpretation I, assign-
                                                                                       (νi , νi+1 ) ∈ ρI,η (α) for each 0 ≤ i ≤ n − 1.
ment η, and state ν is defined as
  1. valI,η (ν, p) = η(p) if p is a logical variable.                             B Soundness proof for forward invariant cut
  2. valI,η (ν, x) = ν(x) if x is a state variable.                                       Fix an interpretation I and an assignment η. From seman-
                                                                                       tics of the first premise, if ν ∈ C and (ν, ω) ∈ ρI,η (α), then
   3. valI,η (ν, f (θ1 , . . . , θn )) = I(f )(valI,η (θ1 ), . . . , valI,η (θ2 ))     ω ∈ C. From the semantics of the second premise, if ω ∈ C,
      if f is a function of arity n ≥ 0 and θ1 , . . . , θn are                        then ω ∈ S From the semantics of the third premise, if ν ∈ I
      terms.                                                                           and ν ∈ / C, and ω is such that (ν, ω) ∈ ρI,η ((α; ?¬C)∗ ), then
   The notation η[x 7→ d] represents the function that agrees                          ω  ∈ S.  This is equivalent to saying that for any ω such that
with η except for the interpretation of x, where it takes the                          there  is a sequence of states ν0 , . . . , νn , with ν0 = ν ∈ I
value d. The notation ν[x 7→ d] denotes the modification of                            and νn = ω, n ∈ N, and (νi , νi+1 ) ∈ ρI,η (α; ?¬C) for each
a state ν, that agrees with ν everywhere except the inter-                             0 ≤ i ≤ n − 1, it is the case that ω ∈ S.
pretation of the state variable x, where it takes the value                               The proof is to show by induction that any state reachable
d.                                                                                     by α∗ from I in n ≥ 0 executions of α must be contained in
                                                                                       S.
Definition 2 (Valuation of dL formulas ([23], Defn. 2.6).                                 For the base case, let n = 0. Then given ν ∈ I, the only
The valuation valI,η (ν, ·) of formulas with respect to inter-                         reachable state by a sequence of length zero is ν itself. If
pretation I, assignment η, and state ν is defined as                                   ν ∈ C, then νinS by semantics of the second premise. If
                                                                                       ν ∈/ C, we have that (ν, ν) ∈ ρI,η ((α; ?¬C)∗ ) by a chain of
   1. valI,η (ν, p(θ1 , . . . , θn ) = I(p)(valI,η (ν, θ1 ), . . . , valI,η (ν, θn )). length zero, so that by semantics of the third premise, ν ∈ S.
   2. valI,η (ν, φ ∧ ψ) = true iff valI,η (ν, φ) = true and                               As an inductive hypothesis, suppose that for every ω reach-
      valI,η (ν, ψ) = true.                                                            able by a chain of length n, ω ∈ S (i.e., there exists ν0 , . . . , νn
   3. valI,η (ν, φ ∨ ψ) = true iff valI,η (ν, φ) = true or                             with ν0 = ν and ω = νn such that (νi , νi+1 ) ∈ ρI,η (α), for
      valI,η (ν, ψ) = true.                                                            0 ≤ i ≤ n − 1. Now choose any state ξ such that there is a
                                                                                       chain of length n+1, ν0 , . . . , νn+1 with ν0 = ν and νn+1 = ξ,
   4. valI,η (ν, ¬φ) = true iff valI,η (ν, φ) 6= true.                                 such that (νi , νi+1 ) ∈ ρI,η (α), for 0 ≤ i ≤ n).
   5. valI,η (ν, φ → ψ) = true iff valI,η (ν, φ) 6= true or                               First suppose that νn ∈ C. Then by semantics of the first
      valI,η (ν, ψ) = true.                                                            premise, νn+1 ∈ C, and then νn+1 ∈ S by semantics of the
                                                                                       second premise. On the other hand, suppose νn ∈          / C. We
   6. valI,η (ν, ∀xφ) = true iff valI,η[x7→d] (ν, φ) = true for                        claim that for all j ≤ n, νj ∈      / C. To see this, note that
      all d ∈ R.                                                                       if νj ∈ C for some j ≤ n, then νn ∈ C by semantics of
   7. valI,η (ν, ∃xφ) = true iff valI,η[x7→d] (ν, φ) = true for                        the first premise, which would contradict our assumption
      some d ∈ R.                                                                      on νn . Then we have that (νi , νi+1 ) ∈ ρI,η (α; ?¬C) for all
Table 1: Model Parameters for the Engine Fuel Con-
trol System.
               Parameter    Value
                   c1      0.41328
                   c2       200.0
                   c3      −0.366
                   c4      0.08979
                   c5      −0.0337
                   c6       0.0001
                   c7       2.821
                   c8     −0.05231
                   c9      0.10299
                  c10     −0.00063
                  c11         1.0
                  c12        14.7
                  c13         0.9
                  c14         0.4
                  c15         0.4
                  c16         1.0
                  uˆ1      23.0829


0 ≤ i ≤ n. By semantics of the third premise, it follows that
ξ ∈ S. This establishes the theorem.

C    System dynamics for the Engine Fuel Con-
     trol Model
   We now present the model parameters and the ODEs for
the Engine Fuel Control model. Figure 4 details the equa-
tions for the recovery mode, and Fig. 5 provides the dynamic
equations for the normal mode. In the figures, dp   dt
                                                        = fp ,
dr          dpest               di
dt
   =  f r ,  dt
                  = fpest , and dt
                                   = fi .
   We translate the system so that the origin coincides with
the normal equilibrium point p ≈ 0.8987, r = 1.0, pest ≈
1.077, i ≈ 0.0 and call the translated variables p̂, r̂, p̂est ,
and, î, respectively.
                                   s                                                                        
                                                            2
                                         p              p                                       2
                                                                                                    + c6 c22 p 
                                                                                                              
        fp      =    c1 2uˆ1               −                     − c3 + c4 c2 p + c5 c2 p
                                        c11            c11

                                    c3 + c4 c2 p + c5 c2 p2 + c6 c22 p
                                                                                            
        fr      =    4                                                           −r
                             c13 (c3 + c4 c2 p2est + c5 c2 p2est + c6 c22 pest )
                                  r                                                                                        !
                                                           2
                                        p              p
                                                                         c3 + c4 c2 pest + c5 c2 p2est + c6 c22 pest
                                                                                                                       
        fpest   =    c1      2uˆ1       c11
                                              −       c11
                                                                 − c13

        fi      =    0

Figure 4: System dynamics for the Engine Fuel Control System in the recovery mode.




                                s                                                                          
                                                           2
                                      p                p                                    2
                                                                                                + c6 c22 p 
                                                                                                          
       fp       = c1 2uˆ1               −                       − c3 + c4 c2 p + c5 c2 p
                                     c11              c11

                                               c3 + c4 c2 p + c5 c2 p2 + c6 c22 p
                                                                                                                          
       fr       = 4                                                                                  −r
                                           2
                          c13 (c3 + c4 c2 pest + c5 c2 p2est + c6 c22 pest )(1 + i + c14 (r − c16 ))
                               r                                                                      !
                                          2
                                   p         p                                       2         2
                                                                                                     
       fpest    = c1       2uˆ1 c11 − c11 − c13 c3 + c4 c2 pest + c5 c2 pest + c6 c2 pest

       fi       = c15 (r − c16 )

Figure 5: System dynamics for the Engine Fuel Control System in the normal mode.
