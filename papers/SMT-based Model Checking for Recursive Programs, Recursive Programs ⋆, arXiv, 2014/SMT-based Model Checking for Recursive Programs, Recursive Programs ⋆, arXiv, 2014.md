                                                      SMT-based Model Checking for
                                                         Recursive Programs ⋆

                                                     Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki
arXiv:1405.4028v2 [cs.LO] 25 May 2014




                                                         Carnegie Mellon University, Pittsburgh, PA, USA



                                              Abstract. We present an SMT-based symbolic model checking algo-
                                              rithm for safety verification of recursive programs. The algorithm is
                                              modular and analyzes procedures individually. Unlike other SMT-based
                                              approaches, it maintains both over- and under-approximations of pro-
                                              cedure summaries. Under-approximations are used to analyze procedure
                                              calls without inlining. Over-approximations are used to block infeasi-
                                              ble counterexamples and detect convergence to a proof. We show that
                                              for programs and properties over a decidable theory, the algorithm is
                                              guaranteed to find a counterexample, if one exists. However, efficiency
                                              depends on an oracle for quantifier elimination (QE). For Boolean Pro-
                                              grams, the algorithm is a polynomial decision procedure, matching the
                                              worst-case bounds of the best BDD-based algorithms. For Linear Arith-
                                              metic (integers and rationals), we give an efficient instantiation of the
                                              algorithm by applying QE lazily. We use existing interpolation techniques
                                              to over-approximate QE and introduce Model Based Projection to under-
                                              approximate QE. Empirical evaluation on SV-COMP benchmarks shows
                                              that our algorithm improves significantly on the state-of-the-art.


                                        1   Introduction

                                        We are interested in the problem of safety of recursive programs, i.e., deciding
                                        whether an assertion always holds. The first step in Software Model Checking is
                                        to approximate the input program by a program model where the program op-
                                        erations are terms in a first-order theory D. Many program models exist today,
                                        e.g., Boolean Programs [6] of SLAM [5], Goto programs of CBMC [14], Boo-
                                        giePL of Boogie [7], and, indirectly, internal representations of many tools
                                        such as UFO [1], HSF [21], etc. Given a safety property and a program model
                                        over D, it is possible to analyze bounded executions using an oracle for Satisfi-
                                        ability Modulo Theories (SMT) for D. However, in the presence of unbounded
                                        recursion, safety is undecidable in general. Throughout this paper, we assume
                                        that procedures cannot be passed as parameters.
                                            There exist several program models where safety is efficiently decidable1 ,
                                        e.g., Boolean Programs with unbounded recursion and the unbounded use of
                                        ⋆
                                          This paper is originally published by Springer-Verlag as part of the proceedings of
                                          CAV 2014. The final publication is available at link.springer.com.
                                        1
                                          This is no longer true when we allow procedures as parameters [12].
2        A. Komuravelli et al.

stack [35,6]. The general observation behind these algorithms is that one can
summarize the input-output behavior of a procedure. A summary of a proce-
dure is an input-output relation describing what is currently known about its
behavior. Thus, a summary can be used to analyze a procedure call without
inlining or analyzing the body of the callee [11,36]. For a Boolean Program, the
number of states is finite and hence, a summary can only be updated finitely
many times. This observation led to a number of efficient algorithms that are
polynomial in the number of states, e.g., the RHS framework [35], recursive state
machines [4], and symbolic BDD-based algorithms of Bebop [6] and Moped [19].
When safety is undecidable (e.g., when D is Linear Rational Arithmetic (LRA) or
Linear Integer Arithmetic (LIA)), several existing software model checkers work
by iteratively obtaining Boolean Program abstractions using Predicate Abstrac-
tion [13,5]. In this paper, we are interested in an alternative algorithm that works
directly on the original program model without an explicit step of Boolean ab-
straction. Despite the undecidability, we are interested in an algorithm that is
guaranteed to find a counterexample to safety, if one exists.
    Several algorithms have been recently proposed for verifying recursive pro-
grams without predicate abstraction. Notable examples are Whale [2], HSF [21],
GPDR [27], Ultimate Automizer [24,25] and Duality [32]. With the exception of
GPDR, these algorithms are based on a combination of Bounded Model Checking
(BMC) [8] and Craig Interpolation [16]. First, they use an SMT-solver to check
for a bounded counterexample, where the bound is on the depth of the call stack
(i.e., the number of nested procedure calls). Second, they use (tree) interpolation
to over-approximate procedure summaries. This is repeated with increasing val-
ues of the bound until a counterexample is found or the approximate summaries
are inductive. The reduction to BMC ensures that the algorithms are guaran-
teed to find a counterexample. However, the size of the SMT instance grows
exponentially with the bound on the call-stack (i.e., linear in the size of the call
tree). Therefore, for Boolean Programs, these algorithms are at least worst-case
exponential in the number of states.
    On the other hand, GPDR follows the approach of IC3 [9] by solving BMC
incrementally without unrolling the call-graph. Interpolation is used to over-
approximate summaries and caching is used to indirectly under-approximate
them. For some configurations, GPDR is worst-case polynomial for Boolean Pro-
grams. However, even for LRA, GPDR might fail to find a counterexample. 2
    In this paper, we introduce RecMC, the first SMT-based algorithm for model
checking safety of recursive programs that is worst-case polynomial (in the num-
ber of states) for Boolean Programs while being a co-semidecision procedure for
programs over decidable theories (see Section 4). Our main insight is to maintain
not only over-approximations of procedure summaries (which we call summary
facts), but also their under-approximations (which we call reachability facts).
While summary facts are used to block spurious counterexamples, reachability
facts are used to analyze a procedure call without inlining or analyzing the body
of the callee. Our use of reachability facts is similar to that of summary edges
2
    See appendix for an example.
                          SMT-based Model Checking for Recursive Programs                 3

                                               n := n + 1
                                                                    N
                           A                                  B
                              M |=n ϕsafe ?         Y
                            (update ρ and σ)                σ inductive?
               n := 0
               ρ := ∅
                                                            proof   Y
               σ := ∅
                                  N cex ρ                     σ

                                UNSAFE                          SAFE

             Fig. 1: Flow of the algorithm RecMC to check if M |= ϕsafe .

of the RHS [35] algorithm. This explains our complexity result for Boolean Pro-
grams. However, our summary facts make an important difference. While the
use of summary facts is an interesting heuristic for Boolean Programs that does
not improve the worst-case complexity, it is crucial for richer theories.
    Almost every step of RecMC results in existential quantification of variables.
RecMC tries to eliminate these variables, as otherwise, they would accumulate
and the size of an inferred reachability fact, for example, grows exponentially in
the bound on the call-stack. But, a naïve use of quantifier elimination (QE) is
expensive. Instead, we develop an alternative approach that under-approximates
QE. However, obtaining arbitrary under-approximations can lead to divergence
of the algorithm. We introduce the concept of Model Based Projection (MBP),
for covering ∃x · ϕ(x, y) by finitely-many quantifier-free under-approximations
obtained using models of ϕ(x, y). We developed efficient MBPs (see Section 5)
for Linear Arithmetic based on the QE methods by Loos-Weispfenning [30] for
LRA and Cooper [15] for LIA. We use MBP to under-approximate reachability
facts in RecMC. In the best case, only a partial under-approximation is needed
and a complete quantifier elimination can be avoided.
    We have implemented RecMC as part of our tool Spacer using the frame-
work of Z3 [17] and evaluated it on 799 benchmarks from SV-COMP [37]. Spacer
significantly outperforms the implementation of GPDR in Z3 (see Section 6).
    In summary, our contributions are: (a) an efficient SMT-based algorithm for
model checking recursive programs, that analyzes procedures individually using
under- and over-approximations of procedure summaries, (b) MBP functions
for under-approximating quantifier elimination for LRA and LIA, (c) a new,
complete algorithm for Boolean Programs, with complexity polynomial in the
number of states, similar to the best known method [6], and (d) an implemen-
tation and an empirical evaluation of the approach.


2    Overview
In this section, we give an overview of RecMC and illustrate it on an example.
Let A be a recursive program. For simplicity of presentation, assume no loops, no
global variables and that arguments are passed by reference. Let P (v) ∈ A be a
procedure with parameters v and let v 0 be fresh variables not appearing in P with
|v| = |v 0 |. A safety property for P is an assertion ϕ(v 0 , v). We say that P satisfies
ϕ, denoted P (v) |= ϕ(v 0 , v), iff the Hoare-triple {v = v 0 } P (v) {ϕ(v 0 , v)} is valid.
4       A. Komuravelli et al.



                         1                        2                    3
    P |=b ϕ ?                            N                         N   refine ρ and σ
                    falsified using ρ?       satisfied using σ?
                                                                       for bounds < b

                             Y                           Y
                          False                       True
                   update ρ for (P, b)       update σ for (P, b)

                Fig. 2: Flow of the algorithm BndSafety to check P |=b ϕ.

Note that every Hoare-triple corresponds to a safety property in this sense, as
shown by Clarke [11], using a Rule of Adaptation. Given a safety property ϕ
and a natural number n ≥ 0, the problem of bounded safety is to determine
whether all executions of P using a call-stack bounded by n satisfy ϕ. We use
P (v) |=n ϕ(v 0 , v) to denote bounded safety.
     The key steps of RecMC are shown in Fig. 1. RecMC decides safety for the
main procedure M of A. RecMC maintains two assertion maps ρ and σ. The
reachability map ρ maps each procedure P (v) ∈ A to a set of assertions over
v 0 ∪ v that under-approximate its behavior. Similarly, the summary map σ maps
a procedure P to a set of assertions that over-approximate its behavior. Given
P , the maps are partitioned according to the bound on the call-stack. That is,
if δ(v 0 , v) ∈ ρ(P, n) for n ≥ 0, then for every model m of δ, there is an execution
of P that begins in m(v 0 ) and ends in m(v), using a call-stack bounded by n.
Similarly, if δ(v 0 , v) ∈ σ(P, n), then P (v) |=n δ(v 0 , v).
     RecMC alternates between two steps: (A) deciding bounded safety (that
also updates ρ and σ maps) and (B) checking whether the current proof of
bounded safety is inductive (i.e., independent of the bound). It terminates when
a counterexample or a proof is found.
     Bounded safety, P |=b ϕ, is decided using BndSafety shown in Fig. 2. Step 1
checks whether ϕ is falsified by current reachability facts in ρ of the callees of P .
If so, it infers a new reachability fact for P at bound b witnessing the falsification
of ϕ. Step 2 checks whether ϕ is satisfied using current summary facts in σ of
the callees. If so, it infers a new summary fact for P at bound b witnessing the
satisfaction of ϕ. If the prior two steps fail, there is a potential counterexample
π in P with a call to some procedure R such that the reachability facts of R are
too strong to witness π, but the summary facts of R are too weak to block it.
Step 3 updates ρ and σ by creating (and recursively deciding) a new bounded
safety problem for R at bound b − 1.
     We conclude this section with an illustration of RecMC on the program in
Fig. 3 (adapted from [11]). The program has 3 procedures: the main procedure M,
and procedures T and D. M calls T and D. T modifies its argument t and calls itself
recursively. D decrements its argument d. Let the property be ϕ = m0 ≥ 2m + 4.
     The first iteration of RecMC is trivial. The bound n = 0 and since M has
no call-free executions it vacuously satisfies any bounded safety property. Fig. 4
shows the four iterations of BndSafety for the second iteration of RecMC
where n = 1. For this bound, the maps ρ and σ are initially empty. The first
                              SMT-based Model Checking for Recursive Programs                 5

                                      T (t) {
              M (m) {
                                          if (t>0) {                     D (d) {
                  T (m);
                                              t := t-2;                      d := d-1;
                  D (m);
                                              T (t);                     }
                  D (m); }
                                              t := t+1; } }

                         Fig. 3: A recursive program with 3 procedures.

              M(m) |=1 m0 ≥ 2m + 4 ?
     iter 1       1: N        2: N      3
                                            D(d) |=0 ⊥ ?
                                               1: Y        ρ(D, 0) ← {d = d0 − 1}
     iter 2       1: N        2: N      3
                                            T(t) |=0 t0 ≥ 2t ?
                                               1: N        2: Y      σ(T, 0) ← {t0 ≥ 2t}
     iter 3       1: N        2: N      3
                                            D(d) |=0 d ≤ d0 − 1 ?
                                               1: N        2: Y      σ(D, 0) ← {d ≤ d0 − 1}
     iter 4       1: N       2: Y      σ(M, 1) ← {m0 ≥ 2m + 4}

Fig. 4: A run of BndSafety on program in Fig. 3 and a bound 1 on the stack depth.
Numbers in bold refer to the steps in Fig. 2.

iteration of BndSafety finds a potential counterexample path in M and the
approximation for D is updated with a new reachability fact: d = d0 − 1. In the
second iteration, the approximation for T is updated. Note that the two calls
to D are “jumped over” using the reachability fact for D computed in the first
iteration. The new summary fact for T is: t0 ≥ 2t. In the third iteration, the
approximation for D is updated again, now with a summary fact d ≤ d0 − 1.
Finally, the summary facts for T and D at bound 0 are sufficient to establish
bounded safety at n = 1. At this point, the summary map σ is:

    σ(M, 1) = {m0 ≥ 2m + 4}            σ(T, 0) = {t0 ≥ 2t}          σ(D, 0) = {d ≤ d0 − 1}

Ignoring the bounds, σ is inductive. For example, we can prove that the body of
T satisfies t0 ≥ 2t, assuming that the calls do. Thus, step B of RecMC succeeds
and the algorithm terminates declaring the program SAFE. In the rest of the
paper, we show how to automate RecMC using an SMT-oracle.


3    Preliminaries
Consider a first-order language with equality and let S be its signature, i.e.,
the set of non-logical function and predicate symbols (including equality). An
S-structure I consists of a domain of interpretation, denoted |I|, and assigns
elements of |I| to variables, and functions and predicates on |I| to the symbols
of S. Let ϕ be a formula. We assume the usual definition of satisfaction of ϕ by
I, denoted I |= ϕ. I is called a model of ϕ iff I |= ϕ and this can be extended
to a set of formulas. A first-order S-theory Th is a set of deductively closed
S-sentences. I satisfies ϕ modulo Th, denoted I |=Th ϕ, iff I |= Th ∪ {ϕ}. ϕ is
valid modulo Th, denoted |=Th ϕ, iff every model of Th is also a model of ϕ.
6         A. Komuravelli et al.

    Let I be an S-structure and w be a list of fresh function/predicate symbols
not in S. A (S ∪ w)-structure J is called an expansion of I to w iff |J| = |I| and
J agrees with I on the assignments to all variables and the symbols of S. We
use the notation I{w 7→ u} to denote the expansion of I to w that assigns the
function/predicate ui to the symbol wi . For an S-sentence ϕ, we write I(ϕ) to
denote the truth value of ϕ under I. For a formula ϕ(x) with free variables x, we
overload the notation I(ϕ) to mean {a ∈ |I||x| | I{x 7→ a} |= ϕ}. For simplicity
of presentation, we sometimes identify the truth value true with |I| and false
with ∅.
    We assume that programs do not have internal procedures and that proce-
dures cannot be passed as parameters. Furthermore, without loss of generality,
we assume that programs do not have loops or global variables. In the following,
we define programs using a logical representation, as opposed to giving a concrete
syntax. A program A is a finite list of procedures with a designated main proce-
dure M where the program begins. A procedure P is a tuple hιP , oP , ΣP , ℓP , βP i,
where (a) ιP is the finite list of variables denoting the input values of the pa-
rameters, (b) oP is the finite list of variables denoting the output values of the
parameters, (c) ΣP is a fresh predicate symbol of arity |ιP | + |oP |, (d) ℓP is
the finite list of local variables, and (e) βP is a quantifier-free sentence over the
signature (S ∪ {ΣQ | Q ∈ A} ∪ ιP ∪ oP ∪ ℓP ) in which a predicate symbol ΣQ
appears only positively. We use v P to denote ιP ∪ oP .
    Intuitively, for a procedure P , ΣP is used to denote its semantics and βP
encodes its body using the predicate symbol ΣQ for a call to the procedure Q.
We require that a predicate symbol ΣQ appears only positively in βP to ensure a
fixed-point characterization of the semantics as shown later on. For example, for
the signature S = h0, Succ, −, +, ≤, >, =i, the program in Fig. 3 is represented as
hM, T, Di with M = hm0 , m, ΣM , hℓ0 , ℓ1 i, βM i, T = ht0 , t, ΣT , hℓ0 , ℓ1 i, βT i and
D = hd0 , d, ΣD , ∅, βD i, where

    βM = ΣT (m0 , ℓ0 ) ∧ ΣD (ℓ0 , ℓ1 ) ∧ ΣD (ℓ1 , m)    βD = (d = d0 − 1)
                                                                                      (1)
    βT = (t0 ≤ 0 ∧ t0 = t) ∨ (t0 > 0 ∧ ℓ0 = t0 − 2 ∧ ΣT (ℓ0 , ℓ1 ) ∧ t = ℓ1 + 1)

    Here, we abbreviate Succ i (0) by i and (m0 , t0 , d0 ) and (m, t, d) denote the
input and the output values of the parameters of the original program, respec-
tively. For a procedure P , let Paths(P ) denote the set of all prime-implicants of
βP . Intuitively, each element of Paths(P ) encodes a path in the procedure.
    Let A = hP0 , . . . , Pn i be a program and I be an S-structure. Let X be a list of
length n such that each Xi is either (i) a truth value if |v Pi | = 0, or (ii) a subset of
|I||vPi | if |v Pi | ≥ 1. Let J(I, X) denote the expansion I{ΣP0 7→ X0 } . . .{ΣPn 7→
Xn }. The semantics of a procedure Pi given I, denoted JPi KI , characterizes all
the terminating executions of Pi and is defined as follows. hJP0 KI , . . . , JPn KI i is
the (pointwise) least X such that for all Q ∈ A, J(I, X) |= ∀v Q ∪ ℓQ · (βQ ⇒
ΣQ (v Q )). This has a well-known least fixed-point characterization [11].
    For a bound b ≥ 0 on the call-stack, the bounded semantics of a procedure
Pi given I, denoted JPi KbI , characterizes all the executions using a stack of depth
                            SMT-based Model Checking for Recursive Programs                      7

bounded by b and is defined by induction on b:

JPi K0I = J(I, h∅, . . . , ∅i)(∃ℓPi · βPi ), JPi KbI = J(I, hJP0 Kb−1
                                                                  I   , . . . , JPn Kb−1
                                                                                     I   i)(∃ℓPi · βPi )

   An environment is a function that maps a predicate symbol ΣP to a formula
over v P . Given a formula τ and an environment E, we abuse the notation J·K
and write Jτ KE for the formula obtained by instantiating every predicate symbol
ΣP by E(ΣP ) in τ .
   Let Th be an S-theory. A safety property for a procedure P ∈ A is a formula
over v P . P satisfies a safety property ϕ w.r.t Th, denoted P |=Th ϕ, iff for all
models I of Th, JP KI ⊆ I(ϕ). A safety property ψ of the program A is a safety
property of its main procedure. A safety proof for ψ(v M ) is an environment Π
that is both safe and inductive:

    |=Th J∀x · ΣM (x) ⇒ ψ(x)KΠ , ∀P ∈ A· |=Th J∀v P ∪ ℓP · (βP ⇒ ΣP (v P ))KΠ

    Given a formula ϕ(v P ) and b ≥ 0, a procedure P satisfies bounded safety
w.r.t Th, denoted P |=b,Th ϕ, iff for all models I of Th, JP KbI ⊆ I(ϕ). In this
case, we also call ϕ a summary fact for hP, bi. We call ϕ a reachability fact for
hP, bi iff I(ϕ) ⊆ JP KbI , for all models I of Th. Intuitively, summary facts and
reachability facts for hP, bi, respectively, over- and under-approximate JP KbI for
every model I of Th.
    A bounded assertion map maps a procedure P and a natural number b ≥ 0
to a set of formulas over v P . Given a bounded assertion map m and b ≥ 0, we
                                     b        b
define two special environments Um      and Om   as follows.
                _                                                  ^
  b
 Um : ΣP 7→      {δ ∈ m(P, b′ ) | b′ ≤ b}            b
                                                    Om : ΣP 7→         {δ ∈ m(P, b′ ) | b′ ≥ b}

         b        b
We use Um  and Om   to under- and over-approximate the bounded semantics. For
                   −1      −1
convenience, let Um   and Om   be environments that map every symbol to ⊥.


4     Model Checking Recursive Programs

In this section, we present our algorithm RecMC(A, ϕsafe ) that determines
whether a program A satisfies a safety property ϕsafe . Let S be the signature
of the first-order language under consideration and assume a fixed S-theory
Th. To avoid clutter, we drop the subscript Th from the notation |=Th and
|=b,Th . We also establish the soundness and complexity of RecMC. An efficient
instantiation of RecMC to Linear Arithmetic is presented in Section 5.
Main Loop. RecMC maintains two bounded assertion maps ρ and σ for reach-
ability and summary facts, respectively. For brevity, for a first-order formula
τ , we write Jτ Kbρ and Jτ Kbσ to denote Jτ KUρb and Jτ KOσb , respectively, where the
environments Uρb and Oσb are as defined in Section 3. Intuitively, Jτ Kbρ and Jτ Kbσ ,
respectively, under- and over-approximate τ using ρ and σ.
8            A. Komuravelli et al.

        RecMC(A, ϕsafe )
    1   n←0;ρ←∅;σ ←∅                                        CheckInductive(A, σ, n)
    2   while true do                                  10   ind ← true
    3      res, ρ, σ ← BndSafety(A, ϕsafe , n, ρ, σ)   11   foreach P ∈ A do
    4      if res is UNSAFE then                       12       foreach δ ∈ σ(P, n) do
    5           return UNSAFE, ρ                       13           if |= JβP Kn
                                                                               σ ⇒ δ then
                                                       14                σ ← σ ∪ (hP, n + 1i 7→ δ)
            else
    6              ind , σ ← CheckInductive(A, σ, n)                 else
    7              if ind then                         15                   ind ← false
    8                    return SAFE, σ
    9              n←n+1                               16   return (ind , σ)

                                    Fig. 5: Pseudo-code of RecMC.

     The pseudo-code of the main loop of RecMC (corresponding to the flow di-
agram in Fig. 1) is shown in Fig. 5. RecMC follows an iterative deepening strat-
egy. In each iteration, BndSafety (described below) checks whether all execu-
tions of A satisfy ϕsafe for a bound n ≥ 0 on the call-stack, i.e., if M |=n ϕsafe .
BndSafety also updates the maps ρ and σ. Whenever BndSafety returns
UNSAFE , the reachability facts in ρ are sufficient to construct a counterexample
and the loop terminates. Whenever BndSafety returns SAFE , the summary
facts in σ are sufficient to prove the absence of a counterexample for the current
bound n on the call-stack. In this case, if σ is also inductive, as determined
by CheckInductive, Oσn is a safety proof and the loop terminates. Otherwise,
the bound on the call-stack is incremented and a new iteration of the loop be-
gins. Note that, as a side-effect of CheckInductive, some summary facts are
propagated to the bound n + 1. This is similar to push generalization in IC3 [9].
Bounded safety. We describe the routine BndSafety(A, ϕsafe , n, ρInit , σInit )
as an abstract transition system [33] defined by the inference rules shown in
Fig. 6. Here, n is the current bound on the call-stack and ρInit and σInit are
the maps of reachability and summary facts input to the routine. A state of
BndSafety is a triple Q k ρ k σ, where ρ and σ are the current maps and Q is
a set of triples hP, ϕ, bi for a procedure P , a formula ϕ over v P , and a number
b ≥ 0. A triple hP, ϕ, bi ∈ Q is called a bounded reachability query and asks
whether P 6|=b ¬ϕ, i.e., whether there is an execution in P using a call-stack
bounded by b where the values of v P satisfy ϕ.
     BndSafety starts with a single query hM, ¬ϕsafe , ni and initializes the maps
of reachability and summary facts (rule Init). It checks whether M |=n ϕsafe by
inferring new summary and reachability facts to answer existing queries (rules
Sum and Reach) and generating new queries (rule Query). When there are
no queries left to answer, i.e., Q is empty, it terminates with a result of either
UNSAFE or SAFE (rules Unsafe and Safe).
Sum infers a new summary fact when a query hP, ϕ, bi can be answered nega-
tively. In this case, there is an over-approximation of the bounded semantics of
P at b, obtained using the summary facts of callees at bound b − 1, that is unsat-
isfiable with ϕ. That is, |= JβP Kb−1
                                  σ   ⇒ ¬ϕ. The inference of the new fact is by in-
terpolation [16] (denoted by Itp in the side-condition of the rule). Thus,
                                                                            the new
summary fact ψ is a formula over v P such that |= JβP Kb−1
                                                         σ  ⇒  ψ(v   P )  ∧ (ψ(v P) ⇒
¬ϕ). Note that ψ over-approximates the bounded semantics of P at b. Every
                          SMT-based Model Checking for Recursive Programs                    9


                          Init
                                 {hM, ¬ϕsafe , ni} k ρInit k σInit

                      Qkρkσ           hP, ϕ, bi ∈ Q   |= JβP Kb−1
                                                              σ   ⇒ ¬ϕ
       Sum                                   c
             Q \ {hP, η, ci | c ≤ b, |= JΣP Kσ ∧ ψ ⇒ ¬η} k ρ k σ ∪ {hP, bi 7→ ψ}

                                                              where ψ = Itp(JβP Kb−1
                                                                                 σ , ¬ϕ)


              Qkρkσ          hP, ϕ, bi ∈ Q       π ∈ Paths(P )       6|= JπKb−1
                                                                            ρ   ⇒ ¬ϕ
      Reach
                   Q \ {hP, η, ci | c ≥ b, 6|= ψ ⇒ ¬η} k ρ ∪ {hP, bi 7→ ψ} k σ

                                                                     where ψ = ∃ℓP · JπKb−1
                                                                                        ρ


              Qkρkσ         hP, ϕ, bi ∈ Q     |= JβP Kb−1
                                                      ρ   ⇒ ¬ϕ         π ∈ Paths(P )
              π = πu ∧ ΣR (a) ∧ πv      |= Jπu Kb−1
                                                σ   ∧ JΣ R (a)K b−1
                                                                ρ   ∧ Jπ    b−1
                                                                         v Kρ   ⇒ ¬ϕ
                                   b−1            b−1       b−1
                         6|= Jπu Kσ ∧ JΣR (a)Kσ ∧ Jπv Kρ ⇒ ¬ϕ
     Query
                                    Q ∪ {hR, ψ, b − 1i} k ρ k σ
                            (
                                ψ = ∃ v P ∪ ℓP \ a · Jπu Kb−1    ∧ Jπv Kb−1
                                                                              
                                                              σ         ρ   ∧ ϕ [a ← v R ]
                    where
                                for all hR, η, b − 1i ∈ Q, |= ψ ⇒ ¬η

          ∅kρkσ        6|= JΣM Kn
                                ρ ⇒ ϕsafe                 ∅kρkσ         |= JΣM Kn
                                                                                σ ⇒ ϕsafe
 Unsafe                                            Safe
                     UNSAFE                                            SAFE


              Fig. 6: Rules defining BndSafety(A, ϕsafe , n, ρInit , σInit ).

query hP, η, ci ∈ Q such that η is unsatisfiable with the updated environment
Oσc (ΣP ) is immediately answered and removed.
Reach infers a new reachability fact when a query hP, ϕ, bi can be answered
positively. In this case, there is an under-approximation of the bounded semantics
of P at b, obtained using the reachability facts of callees at bound b − 1, that is
satisfiable with ϕ. That is, 6|= JβP Kb−1
                                       ρ  ⇒ ¬ϕ. In particular, there exists a path π
                                 b−1
in Paths(P ) such that 6|= JπKρ ⇒ ¬ϕ. The new reachability fact ψ is obtained
by choosing such a π non-deterministically and existentially quantifying all local
variables from JπKb−1ρ . Note that ψ under-approximates the bounded semantics
of P at b. Every query hP, η, ci ∈ Q such that η is satisfiable with the updated
environment Uρc (ΣP ) is immediately answered and removed.
Query creates a new query when a query hP, ϕ, bi cannot be answered using
current ρ and σ. In this case, the current over-approximation of the bounded
semantics of P at b is satisfiable with ϕ while its current under-approximation
is unsatisfiable with ϕ. That is, 6|= JβP Kb−1
                                             σ   ⇒ ¬ϕ and |= JβP Kb−1ρ    ⇒ ¬ϕ. In
particular, there exists a path π in Paths(P ) such that 6|= JπKb−1 σ    ⇒   ¬ϕ and
|= JπKρb−1 ⇒ ¬ϕ. Intuitively, π is a potential counterexample path that needs to
be checked for feasibility. Such a π is chosen non-deterministically. π is guaran-
teed to have a call ΣR (a) to a procedure R such that the under-approximation
JΣR (a)Kb−1
         ρ    is too strong to witness π but the over-approximation JΣR (a)Kb−1σ   is
10        A. Komuravelli et al.

                                      πi           Jπi K0ρ Jπi K0σ
                            i = 1 ΣT (m0 , ℓ0 )      ⊥       ⊤
                            i = 2 ΣD (ℓ0 , ℓ1 ) ℓ1 = ℓ0 − 1 ⊤
                            i = 3 ΣD (ℓ1 , m) m = ℓ1 − 1 ⊤

         Fig. 7: Approximations of the only path π of the procedure M in Fig. 3.

too weak to block it. That is, π can be partitioned into a prefix πu , a call ΣR (a)
to R, and a suffix πv such that the following hold:

                 |= JΣR (a)Kb−1  ⇒ (Jπu Kb−1  ∧ Jπv Kb−1
                                                                
                             ρ            σ          ρ ) ⇒ ¬ϕ

                 6|= JΣR (a)Kb−1 ⇒ (Jπu Kb−1  ∧ Jπv Kb−1
                                                                
                             σ            σ          ρ ) ⇒ ¬ϕ

Note that the prefix πu and the suffix πv are over- and under-approximated,
respectively. A new query hR, ψ, b − 1i is created where ψ is obtained by existen-
tially quantifying all variables from Jπu Kb−1 σ   ∧ Jπv Kb−1
                                                          ρ   ∧ ϕ except the arguments
a of the call, and renaming appropriately. If the new query is answered nega-
tively (using Sum), all executions along π where the values of v P ∪ ℓP satisfy
Jπv Kb−1
     ρ   are spurious counterexamples. An additional side-condition requires that
ψ “does not overlap” with η for any other query hR, η, b − 1i in Q. This is neces-
sary for termination of BndSafety (Theorem 2). In practice, the side-condition
is trivially satisfied by always applying the rule to hP, ϕ, bi with the smallest b.
    For example, consider the program in Fig. 3 represented by (1) and the
query hM, ϕ, 1i where ϕ ≡ m0 < 2m + 4. Let σ = ∅, ρ(D, 0) = {d = d0 − 1}
and ρ(T, 0) = ∅. Let π = (ΣT (m0 , ℓ0 ) ∧ ΣD (ℓ0 , ℓ1 ) ∧ ΣD (ℓ1 , m)) denote the only
path in the procedure M . Fig. 7 shows Jπi K0ρ and Jπi K0σ for each conjunct πi of
π. As the figure shows, JπK0σ is satisfiable with ϕ, witnessed by the execution
e ≡ hm0 = 3, ℓ0 = 3, ℓ1 = 2, m = 1i. Note that this execution also satisfies
Jπ2 ∧ π3 K0ρ . But, Jπ1 K0ρ is too strong to witness it, where π1 is the call ΣT (m0 , ℓ0 ).
To create a new query for T , we first existentially quantify all variables other
than the arguments m0 and ℓ0 from π2 ∧ π3 ∧ ϕ, obtaining m0 < 2ℓ0 . Renaming
the arguments by the parameters of T results in the new query hT, t0 < 2t, 0i.
Further iterations of BndSafety would answer this query negatively making
the execution e spurious. Note that this would also make all other executions
where the values to hm0 , ℓ0 , ℓ1 , mi satisfy Jπ2 ∧ π3 K0ρ spurious.
Soundness and Complexity. Soundness of RecMC follows from that of
BndSafety, which can be shown by a case analysis on the inference rules3 .
Theorem 1. BndSafety and RecMC are sound.

    BndSafety is complete relative to an oracle for satisfiability modulo Th.
Even though the number of reachable states of a procedure is unbounded in
general, the number of reachability facts inferred by BndSafety is finite. This
is because a reachability fact corresponds to a path (see Reach) and given
a bound on the call-stack, the number of such facts is bounded. This further
bounds the number of queries that can be created.
3
     Proofs of all of the theorems are in the Appendix.
                        SMT-based Model Checking for Recursive Programs         11

Theorem 2. Given an oracle for Th, BndSafety(A, ϕ, n, ∅, ∅) terminates.

    As a corollary of Theorem 2, RecMC is a co-semidecision procedure for
safety, i.e., RecMC is guaranteed to find a counterexample if one exists. In con-
trast, the closest related algorithm GPDR [27] is not a co-semidecision procedure
(see Appendix). Finally, for Boolean Programs RecMC is a complete decision
procedure. Unlike the general case, the number of reachable states of a Boolean
Program, and hence the number of reachability facts, is finite and independent
of the bound on the call-stack. Let N = |A| and k = max{|v P | | P ∈ A}.

Theorem 3. Let A be a Boolean Program. Then RecMC(A, ϕ) terminates in
O(N 2 · 22k )-many applications of the rules in Fig. 6.

    Note that due to the iterative deepening strategy of RecMC, the complexity
is quadratic in the number of procedures (and not linear as in [6]). In contrast,
other SMT-based algorithms, such as Whale [2], are worst-case exponential in
the number of states of a Boolean Program.
    In summary, RecMC checks safety of a recursive program by inferring the
necessary under- and over-approximations of procedure semantics and using
them to analyze procedures individually.


5   Model Based Projection

RecMC, as presented in Section 4, can be used as-is, when Th is Linear Arith-
metic. But, note that the rules Reach and Query introduce existential quan-
tifiers in reachability facts and queries. Unless eliminated, these quantifiers ac-
cumulate and the size of the formulas grows exponentially in the bound on the
call-stack. Using quantifier elimination (QE) to eliminate the quantifiers is ex-
pensive. Instead, we suggest an alternative approach that under-approximates
existential quantification with quantifier-free formulas lazily and efficiently. We
first introduce a model-based under-approximation of QE, which we call a Model
Based Projection (MBP). Second, we give an efficient (linear in the size of for-
mulas involved) MBP procedure for Linear Rational Arithmetic (LRA). Due to
space limitations, MBP for Linear Integer Arithmetic (LIA) is described in the
Appendix. Finally, we show a modified version of BndSafety that uses MBP
instead of existential quantification and show that it is sound and terminating.
Model Based Projection (MBP). Let λ(y) be the existentially quantified for-
mula ∃x · λm (x, y) where λm is quantifier free. A function Proj λ from models
(modulo Th) of λm to quantifier-freeW  formulas over y is a Model Based Projection
(for λ) iff it has a finite image, λ ≡ M|=λm Proj λ (M ), and for every model M
of λm , M |= Proj λ (M ).
     In other words, Proj λ covers the space of all models of λm (x, y) by a finite
set of quantifier-free formulas over y. MBP exists for any theory that admits
quantifier elimination, because one can first obtain an equivalent quantifier-free
formula and map every model to it.
12      A. Komuravelli et al.

MBP for Linear Rational Arithmetic. We begin with a brief overview
of Loos-Weispfenning (LW) method [30] for quantifier elimination in LRA. We
borrow our presentation from Nipkow [34] to which we refer the reader for more
details. Let λ(y) = ∃x · λm (x, y) as above. Without loss of generality, assume
that x is singleton, λm is in Negation Normal Form, and x only appears in the
literals of the form ℓ < x, x < u, and x = e, where ℓ, u, and e are x-free. Let
lits(λ) denote the literals of λ. The LW-method states that
                                                                         
                        _                   _
  ∃x · λm (x) ≡                λm [e] ∨           λm [ℓ + ǫ] ∨ λm [−∞] (2)
                    (x=e)∈lits(λ)          (ℓ<x)∈lits(λ)


where λm [·] denotes a virtual substitution for the literals containing x. Intuitively,
λm [e] covers the case when a literal (x = e) is true. Otherwise, the set of ℓ’s in
the literals (ℓ < x) identify intervals in which x can lie which are covered by
the remaining substitutions. We omit the details of the substitution and instead
illustrate it on an example. Let λm be (x = e∧φ1 )∨(ℓ < x∧x < u)∨(x < u∧φ2 ),
where ℓ, e, u, φ1 , φ2 are x-free. Then,

∃x · λm (x) ≡ λm [e] ∨ λm [ℓ + ǫ] ∨ λm [−∞]
                                                                         
            ≡ φ1 ∨ (ℓ < e ∧ e < u) ∨ (e < u ∧ φ2 ) ∨ ℓ < u ∨ (ℓ < u ∧ φ2 ) ∨ φ2
            ≡ φ1 ∨ (ℓ < u) ∨ φ2

    We now define an MBP LRAProj λ for LRA as a map from models of λm
to disjuncts in (2). Given M |= λm , LRAProj λ picks a disjunct that covers
M based on values of the literals of the form x = e and ℓ < x in M . Ties
are broken by a syntactic ordering on terms (e.g., when M |= ℓ′ = ℓ for two
literals ℓ < x and ℓ′ < x).
                 
                 
                  λm [e],          if (x = e) ∈ lits(λ) ∧ M |= x = e
                 
                 λ [ℓ + ǫ],
                    m               else if (ℓ < x) ∈ lits(λ) ∧ M |= ℓ < x ∧
LRAProj λ (M ) =
                 
                 
                                   ∀(ℓ′ < x) ∈ lits(λ) · M |= ((ℓ′ < x) ⇒ (ℓ′ ≤ ℓ))
                   λm [−∞],         otherwise
                 

Theorem 4. LRAProj λ is a Model Based Projection.

    Note that LRAProj λ is linear in the size of λ. An MBP for LIA can be defined
similarly (see Appendix) based on Cooper’s method [15].
Bounded Safety with MBP. Intuitively, each quantifier-free formula in the
image of Proj λ under-approximates λ. As above, we use λm for the quantifier-
free matrix of λ. We modify the side-condition ψ = λ of Reach and Query
to use quantifier-free under-approximations as follows: (i) for Reach, the new
side-condition is ψ = Proj λ (M ) where M |= λm ∧ ϕ, (ii) for Query, the new
side-condition is ψ = Proj λ (M ) where M |= λm ∧ JΣR (a)Kb−1  σ . Note that to
avoid redundant applications of the rules, we require M to satisfy a formula
stronger than λm . Intuitively, (i) ensures that the newly inferred reachability
                         SMT-based Model Checking for Recursive Programs             13

                       Slam      Svcomp-1    Svcomp-2    Svcomp-3
                  SAFE UNSAFE SAFE UNSAFE SAFE UNSAFE SAFE UNSAFE
           Spacer 1,721   985  249    509  213    497  234    482
           Z3     1,722   997  245    509  208    493  234    477
           VBS    1,727   998  252    509  225    500  240    482

    Fig. 8: Number of programs verified by Spacer, Z3 and the Virtual Best Solver.

fact answers the current query and (ii) ensures that the new query cannot be
immediately answered by known facts. In both cases, the required model M can
be obtained as a side-effect of discharging the premises of the rules. Soundness
of BndSafety is unaffected and termination of BndSafety follows from the
image-finiteness of Proj λ .
Theorem 5. Assuming an oracle and an MBP for Th, BndSafety is sound
and terminating with the modified rules.
    Thus, BndSafety with a linear-time MBP (such as LRAProj λ ) keeps the
size of the formulas small by efficiently inferring only the necessary under-
approximations of the quantified formulas.


6     Implementation and Experiments
We have implemented RecMC for analyzing C programs as part of the tool
Spacer. The back-end is based on Z3 [18] which is used for SMT-solving and
interpolation. It supports propositional logic, linear arithmetic, and bit-vectors
(via bit-blasting). The front-end is based on UFO [3]. It converts C programs to
the Horn-SMT format of Z3, which corresponds to the logical program represen-
tation of Section 3. The implementation and benchmarks are available online4 .
    We evaluated Spacer on two sets of benchmarks. The first set contains 2,908
Boolean Programs obtained from the SLAM toolkit5 . The second contains 799
C programs from the Software Verification Competition (SVCOMP) 2014 [37].
We call this set Svcomp-1. We also evaluated on two variants of Svcomp-1,
which we call Svcomp-2 and Svcomp-3, obtained by factoring out parts of
the program into procedures and introducing more modularity. We compared
Spacer against the implementation of GPDR in Z3. We used a time limit of
30 minutes and a memory limit of 16GB, on an Ubuntu machine with a 2.2
GHz AMD Opteron(TM) Processor 6174 and 516GB RAM. The results are
summarized in Fig. 8. Since there are programs verified by only one of the tools,
Fig. 8 also reports the number of programs verified by at least one, i.e., the
Virtual Best Solver (VBS).
Boolean Program Benchmarks. On most of the SLAM benchmarks, the
runtimes of Spacer and Z3 are similar (within 2 minutes). We then evaluated on
a Boolean Program from [6] in which the size of the call-tree grows exponentially
in the number of procedures. As Fig. 9(a) shows, Spacer handles the increasing
complexity in the example significantly better than Z3.
4
    http://www.cs.cmu.edu/~akomurav/projects/spacer/home.html.
5
    https://svn.sosy-lab.org/software/sv-benchmarks/trunk/clauses/BOOL/slam.zip
14                         A. Komuravelli et al.

                5000                                                                                  1800
                                                                       Z3                             1600
                                                                       Spacer
                4000                                                                                  1400




                                                                                      Spacer (secs)
                                                                                                      1200
 Time (secs)

                3000                                                                                  1000
                                                                                                      800
                2000
                                                                                                      600
                                                                                                      400
                1000
                                                                                                      200
                   0                                                                                    0
                       100          200               300        400            500                          0   200   400   600    800 1000 1200 1400 1600 1800
                                          Number of Procedures                                                                      Z3 (secs)

                                                (a)                                                                                (b)

                 Fig. 9: Spacer vs. Z3 for (a) Bebop example and (b) Svcomp-1 benchmarks.

                1800                                                                                  1800
                1600                                                                                  1600
                1400                                                                                  1400
Spacer (secs)




                                                                                      Spacer (secs)
                1200                                                                                  1200
                1000                                                                                  1000
                800                                                                                   800
                600                                                                                   600
                400                                                                                   400
                200                                                                                   200
                  0                                                                                     0
                       0     200   400    600    800 1000 1200 1400 1600 1800                                0   200   400   600    800 1000 1200 1400 1600 1800
                                                 Z3 (secs)                                                                          Z3 (secs)

                                                (a)                                                                                (b)

                 Fig. 10: Spacer vs. Z3 for the benchmarks (a) Svcomp-2 and (b) Svcomp-3.

SVCOMP 2014 Benchmarks. Fig. 9(b), 10(a) and 10(b) show the scatter
plots for Svcomp-1, Svcomp-2 and Svcomp-3 benchmarks. A diamond indi-
cates a time-out and a star indicates a mem-out. The plots show that Spacer is
significantly better on most of the programs. This shows the practical advantage
of the approximations and MBP of RecMC.


7                 Related Work

There is a large body of work on interprocedural program analysis. It was
pointed out early on that verification of recursive programs is reducible to the
computation of a fixed-point over relations (called summaries) representing the
input-output behavior of each procedure [11,36]. Such procedure summaries are
called partial correctness relations in [11], and are part of the functional approach
of [36]. Reps, Horwitz, and Sagiv [35] showed that for a large class of finite inter-
procedural dataflow problems the summaries can be computed in time polyno-
mial in the number of facts and procedures. Ball and Rajamani [6] adapted the
RHS algorithm to the verification of Boolean Programs. Following the SLAM
project, other software model checkers – such as blast [26] and magic [10]
                        SMT-based Model Checking for Recursive Programs         15

– also implemented the CEGAR loop with predicate abstraction. None used
under-approximations of procedure semantics as we do.
    Recently, several SMT-based algorithms have been proposed for safety ver-
ification of recursive programs, including Whale [2], HSF [21], Duality [32],
Ultimate Automizer [24], and Corral [29]. While these algorithms have been de-
veloped independently, they share a similar structure. They use SMT-solvers
to look for counterexamples and interpolation to over-approximate summaries.
Corral is an exception, which relies on user input and heuristics to supply the
summaries. The algorithms differ in the SMT encoding and the heuristics used.
However, in the worst-case, they completely unroll the call graph into a tree.
    The work closest to ours is Generalized Property Driven Reachability (GPDR)
of Hoder and Bjørner [27]. GPDR extends the hardware model checking algo-
rithm IC3 of Bradley [9] to SMT-supported theories and recursive programs.
Unlike RecMC, GPDR does not maintain reachability facts. In the context of
Fig. 6, this means that ρ is always empty and there is no Reach rule. Instead,
the Query rule is modified to use a model M that satisfies the premises (instead
of our use of the path π when creating a query). Furthermore, the answers to
the queries are cached. In the context of Boolean Programs, this ensures that
every query is asked at most once (and either cached or blocked by a summary
fact). Since there are only finitely many models, the algorithm always termi-
nates. However, in the case of Linear Arithmetic, a formula can have infinitely
many models and GPDR might end up applying the Query rule indefinitely. In
contrast, RecMC creates only finitely many queries for a given bound on the
call-stack and is guaranteed to find a counterexample if one exists.
    Combination of over- and under-approximations for analysis of procedural
programs has also been explored in [23,20]. However, our notion of an under-
approximation is very different. Both [23,20] under-approximate summaries by
must transitions. A must transition is a pair of formulas hϕ, ψi that under-
approximates the summary of a procedure P iff for every state that satisfies ϕ,
P has an execution that ends in a state satisfying ψ. In contrast, our reachability
facts are similar to summary edges of RHS [35]. A reachability fact is a single
formula ϕ such that every satisfying assignment to ϕ captures a terminating
execution of P .


8   Conclusion

We presented RecMC, a new SMT-based algorithm for model checking safety
properties of recursive programs. For programs and properties over decidable
theories, RecMC is guaranteed to find a counterexample if one exists. To our
knowledge, this is the first SMT-based algorithm with such a guarantee while
being polynomial for Boolean Programs. The key idea is to use a combination
of under- and over-approximations of the semantics of procedures, avoiding re-
exploration of parts of the state-space. We described an efficient instantiation
of RecMC for Linear Arithmetic (over rationals and integers) by introducing
Model-Based Projection to under-approximate the expensive quantifier elimina-
16     A. Komuravelli et al.

tion. We have implemented it in our tool Spacer and shown empirical evidence
that it significantly improves on the state-of-the-art.
    In the future, we would like to explore extensions to other theories. Of par-
ticular interest are the theory EUF of uninterpreted functions with equality and
the theory of arrays. The challenge is to deal with the lack of quantifier elim-
ination. Another direction of interest is to combine RecMC with Proof-based
Abstraction [31,22,28] to explore a combination of the approximations of proce-
dure semantics with transition-relation abstraction.
                        SMT-based Model Checking for Recursive Programs           17

Acknowledgment

We thank Edmund M. Clarke and Nikolaj Bjørner for many helpful discussions.
Our definition of MBP is based on the idea of projected implicants co-developed
with Nikolaj. We thank Cesare Tinelli and the anonymous reviewers for insight-
ful comments. This research was sponsored by the National Science Founda-
tion grants no. DMS1068829, CNS0926181 and CNS0931985, the GSRC under
contract no. 1041377, the Semiconductor Research Corporation under contract
no. 2005TJ1366, the Office of Naval Research under award no. N000141010188
and the CMU-Portugal Program. This material is based upon work funded and
supported by the Department of Defense under Contract No. FA8721-05-C-0003
with Carnegie Mellon University for the operation of the Software Engineer-
ing Institute, a federally funded research and development center. Any opinions,
findings and conclusions or recommendations expressed in this material are those
of the author(s) and do not necessarily reflect the views of the United States De-
partment of Defense. This material has been approved for public release and
unlimited distribution. DM-0000973.


References

 1. A. Albarghouthi, A. Gurfinkel, and M. Chechik. From Under-Approximations to
    Over-Approximations and Back. In TACAS, 2012.
 2. A. Albarghouthi, A. Gurfinkel, and M. Chechik. Whale: An Interpolation-Based
    Algorithm for Inter-procedural Verification. In VMCAI, pages 39–55, 2012.
 3. A. Albarghouthi, A. Gurfinkel, Y. Li, S. Chaki, and M. Chechik. UFO: Verification
    with Interpolants and Abstract Interpretation - (Competition Contribution). In
    TACAS, 2013.
 4. R. Alur, M. Benedikt, K. Etessami, P. Godefroid, T. Reps, and M. Yannakakis.
    Analysis of Recursive State Machines. TOPLAS, 27(4):786–818, 2005.
 5. T. Ball, R. Majumdar, T. Millstein, and S. K. Rajamani. Automatic Predicate
    Abstraction of C Programs. SIGPLAN Not., 36(5):203–213, 2001.
 6. T. Ball and S. K. Rajamani. Bebop: A Symbolic Model Checker for Boolean
    Programs. In SPIN, pages 113–130, 2000.
 7. M. Barnett, B.-Y. E. Chang, R. DeLine, B. Jacobs, and K. R. M. Leino. Boogie:
    A Modular Reusable Verifier for Object-Oriented Programs. In FMCO, pages
    364–387, 2005.
 8. A. Biere, A. Cimatti, E. M. Clarke, O. Strichman, and Y. Zhu. Bounded Model
    Checking. Advances in Computers, 58:117–148, 2003.
 9. A. R. Bradley. SAT-Based Model Checking without Unrolling. In VMCAI, 2011.
10. S. Chaki, E. M. Clarke, A. Groce, S. Jha, and H. Veith. Modular Verification of
    Software Components in C. IEEE Trans. Software Eng., 30(6):388–402, 2004.
11. E. M. Clarke. Program Invariants as Fixed Points. Computing, 21(4):273–294,
    1979.
12. E. M. Clarke. Programming Language Constructs for Which It Is Impossible To
    Obtain Good Hoare Axiom Systems. JACM, 26(1):129–147, 1979.
13. E. M. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith. Counterexample-Guided
    Abstraction Refinement. In CAV, 2000.
18      A. Komuravelli et al.

14. E. M. Clarke, D. Kroening, and F. Lerda. A Tool for Checking ANSI-C Programs.
    In TACAS, 2004.
15. D. C. Cooper. Theorem Proving in Arithmetic without Multiplication. Machine
    Intelligence, pages 91–100, 1972.
16. W. Craig. Three uses of the Herbrand-Gentzen theorem in relating model theory
    and proof theory. Symbolic Logic, 22(3):269–285, 1957.
17. L. De Moura and N. Bjørner. Z3: An Efficient SMT Solver. In TACAS, 2008.
18. L. M. de Moura and N. Bjørner. Z3: An Efficient SMT Solver. In C. R. Ramakr-
    ishnan and J. Rehof, editors, TACAS, volume 4963 of Lecture Notes in Computer
    Science, pages 337–340. Springer, 2008.
19. J. Esparza, D. Hansel, P. Rossmanith, and S. Schwoon. Efficient Algorithms for
    Model Checking Pushdown Systems. In CAV, CAV ’00, pages 232–247, 2000.
20. P. Godefroid, A. V. Nori, S. K. Rajamani, and S. Tetali. Compositional May-Must
    Program Analysis: Unleashing the Power of Alternation. In POPL, pages 43–56,
    2010.
21. S. Grebenshchikov, N. P. Lopes, C. Popeea, and A. Rybalchenko. Synthesizing
    Software Verifiers from Proof Rules. In PLDI, pages 405–416, 2012.
22. A. Gupta, M. K. Ganai, Z. Yang, and P. Ashar. Iterative Abstraction using SAT-
    based BMC with Proof Analysis. In ICCAD, pages 416–423, 2003.
23. A. Gurfinkel, O. Wei, and M. Chechik. Model checking recursive programs with
    exact predicate abstraction. In S. D. Cha, J.-Y. Choi, M. Kim, I. Lee, and
    M. Viswanathan, editors, ATVA, volume 5311 of Lecture Notes in Computer Sci-
    ence, pages 95–110. Springer, 2008.
24. M. Heizmann, J. Christ, D. Dietsch, E. Ermis, J. Hoenicke, M. Lindenmann,
    A. Nutz, C. Schilling, and A. Podelski. Ultimate Automizer with SMTInterpol
    - (Competition Contribution). In N. Piterman and S. A. Smolka, editors, TACAS,
    volume 7795 of Lecture Notes in Computer Science, pages 641–643. Springer, 2013.
25. M. Heizmann, J. Hoenicke, and A. Podelski. Nested Interpolants. SIGPLAN Not.,
    45(1)(1):471–482, 2010.
26. T. A. Henzinger, R. Jhala, R. Majumdar, and G. Sutre. Lazy abstraction. In Proc.
    of POPL, pages 58–70, 2002.
27. K. Hoder and N. Bjørner. Generalized Property Directed Reachability. In SAT,
    2012.
28. A. Komuravelli, A. Gurfinkel, S. Chaki, and E. M. Clarke. Automated Abstraction
    in SMT-based Unbounded Software Model Checking. In CAV, pages 846–862,
    2013.
29. A. Lal, S. Qadeer, and S. K. Lahiri. A solver for reachability modulo theories. In
    P. Madhusudan and S. A. Seshia, editors, CAV, volume 7358 of Lecture Notes in
    Computer Science, pages 427–443. Springer, 2012.
30. R. Loos and V. Weispfenning. Applying Linear Quantifier Elimination. Computing,
    36(5):450–462, 1993.
31. K. L. McMillan and N. Amla. Automatic Abstraction without Counterexamples.
    In TACAS, 2003.
32. K. L. McMillan and A. Rybalchenko. Solving Constrained Horn Clauses using
    Interpolation. Technical Report MSR-TR-2013-6, Microsoft Research, 2013.
33. R. Nieuwenhuis, A. Oliveras, and C. Tinelli. Solving SAT and SAT Mod-
    ulo Theories: From an abstract Davis–Putnam–Logemann–Loveland procedure to
    DPLL(T). J. ACM, 53(6):937–977, 2006.
34. T. Nipkow. Linear Quantifier Elimination. J. Autom. Reason., 45(2):189–212,
    2010.
                        SMT-based Model Checking for Recursive Programs          19

35. T. W. Reps, S. Horwitz, and S. Sagiv. Precise Interprocedural Dataflow Analysis
    via Graph Reachability. In POPL, pages 49–61, 1995.
36. M. Sharir and A. Pnueli. Program Flow Analysis: Theory and Applications, chapter
    “Two Approaches to Interprocedural Data Flow Analysis”, pages 189–233. Prentice-
    Hall, 1981.
37. Software      Verification     Competition.                 TACAS,         2014.
    http://sv-comp.sosy-lab.org.
20     A. Komuravelli et al.

A    Divergence of GPDR for Bounded Call-Stack

Consider the program hhM, L, Gi, M i with M = hy0 , y, ΣM , hx, ni, βM i, L =
hn, hx, y, ii, ΣL , hx0 , y0 , i0 i, βL i, G = hx0 , x1 , ΣG , ∅, βG i, where


     βM = ΣL (x, y0 , n, n) ∧ ΣG (x, y) ∧ n > 0
      βL = (i = 0 ∧ x = 0 ∧ y = 0) ∨
          (ΣL (x0 , y0 , i0 , n) ∧ x = x0 + 1 ∧ y = y0 + 1 ∧ i = i0 + 1 ∧ i > 0)
     βG = (x = x0 + 1)

   The GPDR [27] algorithm can be shown to diverge when checking M |=2
y0 ≤ y, for e.g., by inferring the diverging sequence of over-approximations of
JLK1 :
                      (x < 2 ⇒ y ≤ 1), (x < 3 ⇒ y ≤ 2), . . .
We also observed this behavior experimentally (Z3 revision d548c51 at http://z3.codeplex.com).
The Horn-SMT file for the example is available at

http://www.cs.cmu.edu/~akomurav/projects/spacer/gpdr_diverging.smt2.


B    Soundness of RecMC and BndSafety (Proof of
     Theorem 1)

We first restate the theorem.

Theorem 1. RecMC and BndSafety are sound.

Proof. We only show the soundness of BndSafety; the soundness of RecMC
easily follows. In particular, for BndSafety(M, ϕsafe , n, ∅, ∅) we show the fol-
lowing:

 1. if the premises of Unsafe hold, M 6|=n ϕsafe , and
 2. if the premises of Safe hold, M |=n ϕsafe .

   It suffices to show that the environments Uρb and Oσb , respectively, under- and
over-approximate the bounded semantics of the procedures, for every 0 ≤ b ≤ n.
In particular, we show that the following is an invariant of BndSafety: for
every model I of the background theory Th, for every Q ∈ A and b ∈ [0, n],

                        I(Uρb (ΣQ )) ⊆ JQKbI ⊆ I(Oσb (ΣQ )).                       (3)

    Initially, ρ and σ are empty and the invariant holds trivially. BndSafety
updates σ and ρ in the rules Sum and Reach, respectively. We show that these
rules preserve (3). We only show the case of Sum. The case of Reach is similar.
                             SMT-based Model Checking for Recursive Programs            21

   Let hP, ϕ, bi ∈ Q be such that Sum is applicable, i.e., |= JβP Kσb−1 ⇒ ¬ϕ. Let
ψ = Itp(JβP Kb−1
               σ , ¬ϕ). Note that ϕ, and hence ψ, does not depend on the local
variables ℓP . Hence, we know that

                            |= ∃ℓP · JβP Kb−1
                                              
                                          σ     ⇒ ψ.                          (4)

The case of b = 0 is easy and we will skip it. Let I be an arbitrary model of Th.
Assume that (3) holds at b − 1 before applying the rule. In particular, assume
that for all Q ∈ A, JQKb−1
                        I   ⊆ I(Oσb−1 (ΣQ )).
   We will first show that the new summary fact ψ over-approximates JP KbI . Let
J(I, X) be an expansion of I as defined in Section 3.


JP KbI = J(I, hJP0 Kb−1
                    I   , . . . , JPn Kb−1
                                       I   i)(∃ℓPi · βPi )
      = J(I, hI(Oσb−1 (ΣP0 )), . . . , I(Oσb−1 (ΣPn ))i)(∃ℓPi · βPi )             (hypothesis)
      = I(J∃ℓP · βP KOσb−1 )                                            (Oσb−1 is FO-definable)
      = I(∃ℓP · JβP KOσb−1 )                                                            (logic)
      = I(∃ℓP · JβP Kb−1
                     σ )                                                            (notation)
      ⊆ I(ψ)                                                                        (from (4))

Next, we show that the invariant continues to hold. The map of summary facts is
updated to σ ′ = σ ∪ {hP, bi 7→ ψ}. Now, σ ′ differs from σ only for the procedure
P and every bound in [0, b]. Let b′ ∈ [0, b] be arbitrary. Since (3) was true before
                                     ′        ′                 ′
applying Sum, we know that JP KbI ⊆ I(Oσb (ΣP )). As JP KbI ⊆ JP KbI ⊆ I(ψ), it
                   ′       ′                      ′                   ′
follows that JP KbI ⊆ I(Oσb (ΣP )) ∩ I(ψ) ⊆ I(Oσb (ΣP ) ∧ ψ) = I(Oσb ′ (ΣP )).    ⊓
                                                                                  ⊔


C     Termination of BndSafety (Proof of Theorem 2)
We first restate the theorem:
Theorem 2. Given an oracle for Th, BndSafety(A, ϕ, n, ∅, ∅) terminates.
    We begin with showing some useful lemmas. Let p be the maximum number
of paths in P ∈ A, c be the maximum number of procedure calls along any path
in A, N be the number of procedures in A and assume an oracle for SAT modulo
Th.
    The following lemma shows that when a query is removed from Q, it is
actually answered. The proof is immediate from the definitions of Oσb and Uρb
given in Section 3.

Lemma 1 (Answered Queries). Whenever BndSafety removes a query
from Q, it is answered using the known summary and reachability facts. In par-
ticular, let Sum or Reach be applied to hP, ϕ, bi. Then, for every hP, η, bi ∈ Q
removed from Q by the rule,
 1. after Sum is applied, |= JΣP Kbσ ⇒ ¬η, and
22      A. Komuravelli et al.

2. after Reach is applied, 6|= JΣP Kbρ ⇒ ¬η.
   Next, we show that new facts need to be inferred to answer queries remaining
in Q.
Lemma 2 (Pending Queries). Q only has the queries which cannot be im-
mediately answered by ρ or σ, i.e., as long as hP, η, ℓi is in Q, the following are
invariant across iterations of BndSafety.
1. 6|= JΣP Kℓσ ⇒ ¬η, and
2. |= JΣP Kℓρ ⇒ ¬η.
Proof. We first show that the invariants hold when a query is newly created
by Query. Let P , η and ℓ be, respectively, R, ψ[a ← v R ] and b − 1, as in the
conclusion of the rule. The last-but-one premise of Query is

                     |= Jπu Kb−1
                             σ   ∧ JΣR (a)Kb−1
                                           ρ   ∧ Jπv Kb−1
                                                      ρ   ⇒ ¬ϕ

which implies that

                  |= JΣR (a)Kb−1 ⇒ ¬ Jπu Kb−1 ∧ Jπv Kρb−1 ∧ ϕ .
                                                             
                             ρ            σ

The variables not in common, viz., (v P ∪ℓP )\a, can be universally quantified from
the right hand side resulting in |= JΣR Kb−1
                                           ρ   ⇒ ¬η. Similarly, 6|= JΣR Kb−1σ   ⇒ ¬η
follows from the last premise of the rule. Next, we show that Sum and Reach
preserve the invariants.
    Let Sum answer a query hP, ϕ, ℓi with a new summary fact ψ and let the
updated map of summary facts be σ ′ = σ ∪ {hP, ℓi 7→ ψ}. Now, consider
                                                                    ′       ′
hP, η, ℓ′ i ∈ Q after the application of the rule. If ℓ′ > ℓ, Oσℓ ′ = Oσℓ and the
invariant continues to hold. So, assume ℓ′ ≤ ℓ. From the conclusion of Sum, we
                ′                       ′          ′
have 6|= JΣP Kℓσ ∧ ψ ⇒ ¬η. Now, JΣP Kℓσ′ = JΣP Kℓσ ∧ ψ. So, the invariant continues
to hold.
    Similarly, let Reach answer a query hP, ϕ, ℓi with a new reachability fact ψ
and let the updated map of reachability facts be ρ′ = ρ ∪ {ψ 7→ hP, ℓi}. Now,
                                                                          ′      ′
consider hP, η, ℓ′ i ∈ Q after the application of the rule. If ℓ′ < ℓ, Uρℓ′ = Uρℓ and
the invariant continues to hold. So, assume ℓ′ ≥ ℓ. From the conclusion of Reach,
we have |= ψ ⇒ ¬η. Assuming the invariant holds before the rule application,
                         ′                                        ′
we also have |= JΣP Kℓρ ⇒ ¬η. Therefore, we have |= JΣP Kℓρ ∨ ψ ⇒ ¬η. Now,
       ′          ′
JΣP Kℓρ′ = JΣP Kℓρ ∨ ψ. So, the invariant continues to hold.                        ⊓
                                                                                    ⊔
   The next few lemmas show that the rules of the algorithm cannot be applied
indefinitely, leading to a termination argument. Let N be the number of pro-
cedures in the program, p be the maximum number of paths in a procedure, c
be the maximum number of procedure calls along any path in A and n be the
current bound on the call-stack.
Lemma 3 (Finite Reach Facts). The environment Uρb is updated for a given
predicate symbol ΣP and a bound b on the call-stack only O(N b · pb+1 )-many
times.
                        SMT-based Model Checking for Recursive Programs           23

Proof. The environment Uρb can be updated for ΣP and b whenever a reachability
fact is inferred for P at a bound b′ ≤ b. Now, a reachability fact is obtained per
path (after eliminating the local variables) of a procedure, using the currently
known reachability facts about the callees. Moreover, Lemmas 1 and 2 imply
that no reachability fact is inferred twice. This is because whenever a query is
answered using Reach, the query could not have been answered using already
existing reachability facts and a new reachability fact is inferred.
    This gives the following recurrence Reach(b) for the number of updates to
Uρb for a given ΣP :
                             (
                                 p,                          b=0
                Reach(b) =
                                 (p · N + 1) · Reach(b − 1), b > 0.

In words, for b = 0, the number of updates is given by the number of reachability
facts that can be inferred, which is bounded by the number of paths p in the
procedure P . For b > 0, the environment Uρb−1 is updated when a reachability
fact is learnt at b or at a bound smaller than b. The latter is simply Reach(b − 1).
For the former, a new reachability fact is inferred at b along a path whenever
Uρb−1 changes for a callee. For N procedures and p paths, this is given by (p · N ·
Reach(b − 1)).
    This gives us Reach(b) = O(N b · pb+1 ).                                      ⊓
                                                                                  ⊔

Lemma 4 (Finite Queries). For hP, ϕ, bi ∈ Q, Query is applicable only O(c·
N b · pb+1 )-many times.

Proof. First, assume that the environments Uρb−1 and Oσb−1 are fixed. The num-
ber of possible queries that can be created for a given path of P is bounded by
the number of ways the path can be divided into a prefix, a procedure call, and
a suffix. This is bounded by c, the maximum number of calls along the path. For
p paths, this is bounded by c · p.
    Consider a path π and its division, and let a query be created for a callee R
along π. Now, while the query is still in Q, updates to the environments Oσb−1
and Uρb−1 do not result in a new query for R for the same division along π.
This is because, the new query would overlap with the existing one and this is
disallowed by the second side-condition of Query.
    Suppose that the new query is answered by Sum. With the updated map of
summary facts, the last premise of Query can be shown to fail for the current
division of π. If Oσb−1 is updated, the last premise continues to fail. So, a new
query can be created for the same prefix and suffix along π only if Uρb−1 is updated
for some callee along π. The other possibility is that the query is answered by
Reach which updates Uρb−1 as well.
    Thus, for a given path, and a given division of it into prefix and suffix, the
number of queries that can be created is bounded by the number of updates to
Uρb−1 which is (N ·Reach(b−1)). Here, Reach is as in Lemma 3. So, the number of
times Query is applicable for a given query hP, ϕ, bi is O(p · c · N · Reach(b − 1)).
As Reach(b) = N b · pb+1 , we obtain the bound O(c · N b · pb+1 ).                 ⊓
                                                                                   ⊔
24      A. Komuravelli et al.

Lemma 5 (Progress). As long as Q is non-empty in BndSafety, either
Sum, Reach or Query is always applicable.

Proof. First, we show that for every query in Q, either of the three rules is
applicable, without the second side-condition in Query. Let hP, ϕ, bi ∈ Q.
If |= JβP Kb−1
           σ    ⇒ ¬ϕ, then Sum is applicable. Otherwise, there exists a path
π ∈ Paths(P ) such that JπKb−1 σ    is satisfiable with ϕ, i.e., 6|= JπKb−1
                                                                        σ   ⇒ ¬ϕ. Now,
if JπKρ is also satisfiable with ϕ, i.e., 6|= JπKρb−1 ⇒ ¬ϕ, Reach is applicable.
      b−1

Otherwise, |= JπKb−1
                   ρ   ⇒ ¬ϕ. Note that this can only happen if b > 0, as other-
wise, there will not be any procedure calls along π and JπKb−1     σ   and JπKb−1
                                                                              ρ   would
be equivalent.
    Let π = π0 ∧ π1 ∧ . . . πl for some finite l. Then, JπKσb−1 is obtained by taking
the conjunction of the formulas

                                hJπ0 Kb−1      b−1
                                      σ , Jπ1 Kσ , . . . i.

Similarly, JπKb−1
              ρ   is obtained by taking the conjunction of the formulas

                                hJπ0 Kρb−1 , Jπ1 Kb−1
                                                  ρ , . . . i.

From Theorem 1, we can think of obtaining the latter sequence of formulas
by conjoining Jπi Kb−1
                   ρ    to Jπi Kb−1
                                σ   for every i. When this is done backwards for
decreasing values of i, an intermediate sequence looks like

                       hJπ0 Kb−1                b−1      b−1
                             σ , . . . , Jπj−1 Kσ , Jπj Kρ   . . . i.

As JπKb−1
       ρ    is unsatisfiable with ϕ, there exists a maximal j such that the con-
junction of constraints in such an intermediate sequence are unsatisfiable with ϕ.
Moreover, πj must be a literal of the form ΣR (a) as otherwise, Jπj Kb−1
                                                                      σ  = Jπj Kρb−1
violating the maximality condition on j. Thus, all premises of Query hold and
the rule is applicable.
    Now, the second side-condition in Query can be trivially satisfied by always
choosing a query in Q with the smallest bound for the next rule to apply. This
is because, if hR, η, b − 1i is the newly created query, there is no other query in
Q for R and b − 1.                                                                 ⊓
                                                                                   ⊔

   Lemmas 4 and 5 imply that every query in Q is eventually answered by Sum
or Reach, as shown below.

Lemma 6 (Eventual Answer). Every hP, ϕ, bi ∈ Q is eventually answered by
                                    2
Sum or Reach, in O(b · cb · (N p)O(b ) ) applications of the rules.

Proof. Firstly, to answer any given query in Q, Lemma 4 guarantees that the
algorithm can only create finitely many queries. Lemma 5 guarantees that some
rule is always applicable, as long as Q is non-empty. Thus, when Query cannot
be applied for any query in Q, either Sum or Reach must be applicable for some
query. Thus, eventually, all queries are answered.
                        SMT-based Model Checking for Recursive Programs        25

   The total number of rule applications to answer hP, ϕ, bi is then linear in the
cumulative number of applications of Query, which has the following recurrence:
                            (
                              Q(0),                 b=0
                    T (b) =
                              Q(b)(1 + T (b − 1)), b > 0.

where Q(b) denotes the number of applications of Query for a fixed query in
Q at bound b. From Lemma 4, Q(b) = O(c · N b · pb+1 ). This gives us T (b) =
                   2
O(b · cb · (N p)O(b ) ).                                                   ⊓
                                                                           ⊔

Main Proof. Follows immediately from Lemma 6.                                   ⊓
                                                                                ⊔


D    Complexity of RecMC for Boolean Programs (Proof
     of Theorem 3)

We first restate the theorem:
Theorem 3. Let A be a Boolean Program. Then RecMC(A, ϕ) terminates in
O(N 2 · 22k )-many applications of the rules in Fig. 6.

Proof. First, assume a bound n on the call-stack. The number of queries that can
be created for a procedure at any given bound is O(2k ), the number of possible
valuations of the parameters (note that Query disallows overlapping queries to
be present simultaneously in Q). For N procedures and n possible values of the
bound, the complexity of BndSafety(A, ϕ, n, ∅, ∅), for a Boolean Program, is
O(N · 2k · n).
    Now, the total number of summary facts that can be inferred for a procedure
is also bounded by O(2k ). As Oσb is monotonic in b, the number of iterations
of RecMC is bounded by O(N · 2k ), the cumulative number of states of all
procedures. Thus, we obtain the complexity of RecMC as O(N 2 · 22k ).          ⊓
                                                                               ⊔


E    BndSafety with MBP (Proof of Theorem 5)

Here, we show that BndSafety with MBP is sound and terminating.
    First of all, in presence of MBP, Sum is unaffected and a reachability fact
inferred by Reach is only strengthened. Thus, soundness of BndSafety (The-
orem 1) is preserved.
    Then, it is easy to show that the modified side-conditions to Reach and
Query preserve Lemmas 1 and 2 and we skip the proof.
    Then, we will show that the finite-image property of an MBP preserves the
finiteness of the number of reachability facts inferred and the number of queries
generated by the algorithm. Let d be the size of the image of an MBP. In the
proof of Lemma 3, the recurrence relation has an extra factor of d. The rest
of the proof of finiteness of the number of reachability facts remains the same.
Similarly, in the proof of Lemma 4, the number of times Query can be applied
26       A. Komuravelli et al.

along a path for a fixed division and fixed environments Oσb−1 and Uρb−1 increases
by a factor of d. Again, the rest of the proof of finiteness of the number of queries
generated remains the same. That is, Lemmas 3 and 4, and hence, Lemma 6,
are preserved with scaled up complexity bounds.
   Note that Theorem 5 is unaffected by under-approximations.
   Together, we have that Theorem 2 is preserved, with a scaled up complexity
bound.                                                                             ⊓
                                                                                   ⊔


F     LRAProj λ is an MBP (Proof of Lemma 4)

First, we restate the theorem:

Theorem 4. LRAProj λ is a Model Based Projection.

Proof. By definition, LRAProj λ has a finite image, as there are only finitely
many disjuncts in (2). Thus, it suffices to show that for every M |= λm , M |=
LRAProj λ (M ).
    Each disjunct in the LW decomposition (2) is obtained by a virtual substi-
tution of the literals in λm containing x. As in Section 5, we assume that λm
is in NNF with the only literals containing x of the form (x = e), (ℓ < x) or
(x < u) for x-free terms e, ℓ and u. Let Sub t denote the virtual substitution map
of literals when t is either e, ℓ + ǫ or −∞. The LW method [30] defines:

     Sub e (x = e) = ⊤, Sub e (ℓ < x) = (ℓ < e), Sub e (x < u) = (e < u)           (5)
     Sub ℓ+ǫ (x = e) = ⊥, Sub ℓ+ǫ (ℓ′ < x) = (ℓ′ ≤ ℓ), Sub ℓ+ǫ (x < u) = (ℓ < u)   (6)
     Sub −∞ (x = e) = ⊥, Sub −∞ (ℓ < x) = ⊥, Sub −∞ (x < u) = ⊤                    (7)

   Let M |= λm and LRAProj λ (M ) = λm [t] where t is either e or ℓ + ǫ or −∞.
As λm is in NNF, it suffices to show that for every literal µ of λm containing x,
the following holds:
                              M |= (µ ⇒ Sub t (µ))                            (8)

   We consider the different possibilities of t below. For a term η, let M [η]
denote the value of η in M .

 Case t = e. In this case, we know that M |= x = e. Now, for a literal ℓ < x,

              M [ℓ < x] ⇒ M [ℓ] < M [x]
                        = M [ℓ] < M [e]
                        = M [ℓ < e]
                        = M [Sub t (ℓ < x)]        {Sub t (ℓ < x) = (ℓ < e)}.

     Similarly, literals of the form x < u and x = e′ can be considered.
                           SMT-based Model Checking for Recursive Programs           27

 Case t = ℓ + ǫ. In this case, we know that M [ℓ < x] is true, i.e., M [ℓ] < M [x]
   and whenever M [ℓ′ < x] is true, M [ℓ′ ≤ ℓ] is also true. Now, for a literal
   ℓ′ < x,

           M [ℓ′ < x] ⇒ M [ℓ′ ≤ ℓ]
                      = M [Sub t (ℓ′ < x)]           {Sub t (ℓ′ < x) = (ℓ′ ≤ ℓ)}.

    For a literal x < u,

            M [x < u] ⇒ M [x] < M [u]
                      ⇒ M [ℓ] < M [u]                          {M [ℓ] < M [x]}
                      ⇒ M [ℓ < u]
                      = M [Sub t (x < u)]            {Sub t (x < u) = (ℓ < u)}

   For a literal x = e, (8) vacuously holds as M [x = e] is false.
 Case t = −∞. In this case, we know that M [x = e] and M [ℓ < x] are false for
   every literal of the form x = e and ℓ < x. So, for such literals (8) vacuously
   holds. For a literal x < u, Sub t (x < u) = ⊤ and hence, (8) holds again.
                                                                               ⊓
                                                                               ⊔


G    Model Based Projection for Linear Integer Arithmetic
In this section, we present our MBP LIAProj λ for LIA. It is based on Cooper’s
method for Quantifier Elimination procedure [15]. Let λ(y) = ∃x·λm (x, y), where
λm is quantifier free and in negation normal form. Without loss of generality, let
the only literals containing x be the form ℓ < x, x < u, x = e or (d | ±x + w),
where a | b denotes that a divides b, the terms ℓ, u, e and w are x-free, and
d ∈ Z \ {0}. Let E = {e | (x = e) ∈ lits(λm )} be the set of equality terms of
x and L = {ℓ | (ℓ < x) ∈ lits(λm )} be the set of lower-bounds of x. Then, by
Cooper’s method,
                                                D−1
                                                                  ! D−1
                     _                 _        _                    _
∃x·λm (x, y) ≡              λm [e]∨                 λm [ℓ + 1 + i] ∨     λ−∞
                                                                           m [i].
               (x=e)∈lits(λ)         (ℓ<x)∈lits(λ)   i=0                    i=0
                                                                             (9)
where D is the least common multiple of all the divisors in the divisibility lit-
erals of λm , [·] denotes a substitution for x and λ−∞ m is obtained from λm by
substituting all non-divisibility literals as follows:

          (ℓ < x) 7→ ⊥              (x < u) 7→ ⊤               (x = e) 7→ ⊥         (10)

   Intuitively, the disjunction partitions the space of the possible values of x.
A disjunct for (x = e) covers the case when x is equal to an equality term.
Otherwise, the lower-bounds identify various intervals in which x can be present.
The disjuncts for (ℓ < x) cover the case when x satisfies a lower-bound, and
the last disjunct is for the case when x is smaller than all lower-bounds. The
28      A. Komuravelli et al.

disjunction over the possible values of i covers the different ways in which the
divisibility literals can be satisfied.
    Model-based projection LIAProj λ is defined as follows, conflicts are resolved
by some arbitrary, but fixed, syntactic ordering on terms:
                    
                    
                     λm [e],           if x = e ∈ lits(λ) ∧ M |= (x = e)
                    
                    λ [ℓ + 1 + i ], else if (ℓ < x) ∈ lits(λ) ∧ M |= (ℓ < x) ∧
                        m          ℓ
LIAProj λ (M ) =
                    
                    
                                       ∀(ℓ′ < x) ∈ lits(λ) · (M |= ((ℓ′ < x) ⇒ (ℓ′ ≤ ℓ)))
                     −∞
                      λm [i−∞ ],        otherwise
                                                                                 (11)
where iℓ = M [x − (ℓ + 1)] mod D, i−∞ = M [x] mod D, and M [x] is the value
of x in M . The following lemma shows that LIAProj λ is indeed a model based
projection. The proof is similar to that of LRAProj λ .

Lemma 7. LIAProj λ is a Model-Based Projection.
