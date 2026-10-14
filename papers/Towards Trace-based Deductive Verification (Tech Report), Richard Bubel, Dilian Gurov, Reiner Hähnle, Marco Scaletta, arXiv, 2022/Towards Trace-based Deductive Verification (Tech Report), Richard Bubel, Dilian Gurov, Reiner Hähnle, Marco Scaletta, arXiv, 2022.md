                                             Towards Trace-based Deductive Verification
                                                          (Tech Report)

                                              Richard Bubel1 , Dilian Gurov2 , Reiner Hähnle1 , and Marco Scaletta1
                                                           1
arXiv:2211.09487v2 [cs.SE] 21 Nov 2022




                                                              Technical University of Darmstadt, Germany,
                                                             <firstName>.<lastName>@tu-darmstadt.de
                                                    2
                                                      KTH Royal Institute of Technology, Sweden, dilian@kth.se
                                               Abstract. Contracts specifying a procedure’s behavior in terms of pre-
                                               and postconditions are essential for scalable software verification, but
                                               cannot express any constraints on the events occurring during execution
                                               of the procedure. This necessitates to annotate code with intermediate
                                               assertions, preventing full specification abstraction. We propose a logic
                                               over symbolic traces able to specify recursive procedures in a modular
                                               manner that refers to specified programs only in terms of events. We
                                               also provide a deduction system based on symbolic execution and induc-
                                               tion that we prove to be sound relative to a trace semantics. Our work
                                               generalizes contract-based to trace-based deductive verification.


                                         1   Introduction
                                         To make deductive verification scale, modular specification and verification is
                                         of essence [14]. In imperative programming languages modularity manifests it-
                                         self at the granularity of procedure calls. A procedure’s behavior is specified in
                                         terms of a contract [27,28]: a pair of first-order pre- and postconditions. During
                                         verification each procedure call in the code is replaced with a check that the
                                         contract’s precondition holds at this point, the call’s effect is approximated by
                                         assuming the postcondition. In consequence, verification of the called code is
                                         replaced (or approximated) by first-order constraints. The overall verification
                                         effort for a program is proportional to its length, instead of the unfolded (and
                                         unbounded) call graph. The contract-based approach works for recursive pro-
                                         cedures [19,37]. It requires an induction principle [5,26] and is realized in most
                                         state-of-art deductive verification systems, such as [1,22,25].
                                             The fundamental limitation of pre-/postcondition contracts, which in the fol-
                                         lowing are called state-based contracts, is the inability to specify events happen-
                                         ing during execution of a procedure. This is not only problematic for specifying
                                         concurrent programs, but already an issue for interactive programs or loop spec-
                                         ification: It is necessary to annotate code with intermediate assertions, which
                                         worsens readability and impedes full abstraction from the implementation dur-
                                         ing specification. Indeed, contracts written in most specification languages in
                                         deductive verification [3,24] cannot be used independently of the specified code.
                                             Lack of the ability to create abstract specifications motivates the design of
                                         a logic serving as an abstract, trace-based contract language that is sufficiently
                                         expressive to model recursive calls (and loops). The central idea is to represent
                                         the control structures embodied in the control flow graph (CFG) of a program.
2      Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta

From the CFG view two requirements on a trace-based contract language can
be derived: (i) it must be possible to specify scopes relating to procedure calls
and other control structures: to this end we employ events that are semantically
connected with the specified code; (ii) one must represent cyclic edges in the
CFG in a finite manner: this is achieved by a least fixed-point operator. Both
aspects are not new, of course. We draw from ideas first expressed in interval
temporal logic [15] and the modal µ-calculus [23], respectively.

    However, we use the resulting logic of trace contracts differently from tempo-
ral/modal logic: like in Hoare logic [18,19] and dynamic logic [17,33], we admit
explicit judgments about a concrete program: if s is a program and Φ a trace
contract, then s : Φ expresses that any execution of s results in one of the traces
characterized by Φ. As mentioned above, we incorporate events into contracts
to enable full abstraction from the specified code (cf. [21] who use actions to de-
sign an abstract semantics). Consequently, our logic generalizes Hoare/dynamic
logic from state-based to trace-based contracts via events (which permit scoping)
and recursive specifications. This sounds more complex than it is. Still, to keep
the presentation intuitive and manageable, it is crucial to choose (i) a suitable
deductive framework and (ii) an adequate semantics to demonstrate soundness.

    Regarding the first point, we adapt a symbolic execution calculus for de-
ductive verification in dynamic logic [1]: it reduces a program s via symbolic
execution to a sequence of elementary symbolic state updates Us (plus path con-
ditions), hence, it reduces judgments of the form s : Φ to Us : Φ. Adding events
to this formalism is easy. Dynamic logic is closed under propositional and first-
order operators, which enables formulation of a fixed-point induction rule over
the syntactic structure of programs. Concerning the second issue, an adequate
semantics must be trace-based, i.e. it provides (a) for a given state σ and program
s the trace of s when started in σ and (b) for a given trace formula Φ the set
of all traces it characterizes. Since the deduction rules resemble symbolic execu-
tion of a program s; s′ , where s is the leading statement and s′ the remaining
code, an adequate semantics is defined locally for each kind of statement s and
continuation s′ . A general local, trace-based semantic framework was suggested
in [8,9]—here, we specialize it to sequential programs with recursive procedures.

   To summarize, the main contributions of this paper are: (1) A trace-based
specification language that permits fully abstract, modular specification of re-
cursive procedures; (2) the extension of a symbolic execution calculus for pro-
cedure-modular verification by structural induction and trace abstraction; (3) a
soundness proof of the deduction rules based on a local trace semantics.

    In Sect. 2 we present the local trace semantics, then define syntax and se-
mantics of trace contracts in Sect. 3. The deductive verification system is given
in Sect. 4 (for space reasons, the soundness proofs are in the appendix). Related
work is in Sect. 5, conclusion with future work in Sect. 6.
                  Towards Trace-based Deductive Verification (Tech Report)           3

2   Local Trace Semantics of Recursive Procedures

We provide a LAGC-style [8,9] trace semantics for a sequential language with
recursive procedures. Its grammar is shown in Fig. 1.


          P ∈ Prog ::= M {d s}             M ∈ ProcDecl ::= m(x){sc}
       d ∈ VarDecl ::= ε | x; d               sc ∈ Scope ::= {d s; return e}
          s ∈ Stmt ::= skip | x = e | x = m(e) | if e { s } | s; s | while e { s }
             Global lookup table: G = {hm(x) sci | m ∈ procedures(P )}


         Fig. 1. Syntax of an imperative language with recursive procedures


    The definition of integer and boolean expressions is standard, they are as-
sumed to be well-typed. Scopes of procedure bodies may only write to local
integer variables, initialized to zero, i.e. procedure calls have no side effects. We
stress that this is not a fundamental limitation, but to deal with side effects and
aliasing [1,32] is orthogonal to the goals of our paper and the restriction greatly
simplifies the technical issues.

Example 1.                                         m(k) {
We illustrate the concepts in this paper             r ; // initialized to 0
with the running example shown on the                if (k != 0)
right. The behavior of procedure m is the               { r = m(k−1); r = r + 1 };
identity function for input k, but the result        return r
is computed by k (non tail-)recursive calls.       }

Definition 1 (State, Update). Let Var be a set of program variables and
Val a set of values, with typical elements x and v, respectively. A state σ ∈ Σ
is a partial mapping σ : Var ⇀ Val from variables to values. The notation
σ[x 7→ v] expresses the update of state σ at x with value v and is defined as
σ[x 7→ v](y) = v if x = y and σ[x 7→ v](y) = σ(y) otherwise.

    There is a standard evaluation function valσ for expressions, for example, in
a state σ = [x 7→ 0, y 7→ 1] we have valσ (x + y) = valσ (x) + valσ (y) = 0 + 1 = 1.

Definition 2 (Context). A (call) context is a pair ctx = (m, id), where m is
a procedure name and id is a call identifier. Given a call identifier id we denote
with res id the unique name of the return variable associated with the call.

   We define events sufficient to characterize the scope and call structure of
recursive procedures, but one could define further event types, for example, input
events or, in a concurrent setting, suspension events.

Definition 3 (Event Marker). Let m be a procedure name, e a parameter, id a
call identifier, and v a return value. Then callEv(m, e, id) and retEv(v) are event
4        Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta

markers associated with a procedure call and a return statement, respectively. We
also introduce event markers associated with the start and end of a computation
in context ctx, defined as pushEv(ctx) and popEv(ctx), respectively. We denote
with ev(e) a generic event marker over expressions e.
Definition 4 (Trace). A trace τ is defined by the following rules (where ε
denotes the empty trace):  τ ::= ε | τ y t    t ::= σ | ev(e)
    This definition declares traces as sequences over events and states, but we
need to uniquely associate an event ev(e) with a state σ. This is done by inserting
event ev(e) into a trace between two copies of σ.3 We define the event trace evσ (e)
as evσ (e) = hσi y ev(valσ (e)) y σ. Events do not change a state.
    Sequential composition “r ; s” of statements is semantically modeled as trace
composition, where the trace from executing r ends in a state from which the
execution trace of s proceeds. Thus the trace of r ends in the same state as where
the trace of s begins. This motivates the semantic chop “∗∗” on traces [15,16,29]
that we often use, instead of the standard concatenation operator “·”.
Definition 5 (Semantic Chop on Traces). Let τ1 , τ2 be traces, assume τ1
is non-empty and finite. The semantic chop τ1 ∗∗τ2 is defined as τ1 ∗∗τ2 = τ · τ2 ,
where τ1 = τ y σ, τ2 = hσ ′ i·τ ′ , and σ = σ ′ . When σ 6= σ ′ the result is undefined.
We overload the semantic chop symbol for sets of traces:
             T1 ∗∗T2 = {τ1 ∗∗τ2 | τ1 ∈ T1 , τ2 ∈ T1 , last(τ1 ) = first(τ2 )} .
Example 2. Let τ1 = hσi y σ[x 7→ 1] and τ2 = hσ[x 7→ 1]i y σ[x 7→ 1, y 7→ 2],
then τ1 ∗∗τ2 = hσi y σ[x 7→ 1] y σ[x 7→ 1, y 7→ 2].
    Our language is deterministic, so we design local evaluation valσ (s) of a
statement s in state σ to return a single trace: The result of valσ (s) is of the
form τ · K(s′ ), where τ is an initial (small-step) trace of s and K(s′ ) contains
the remaining, possibly empty, statement s′ yet to be evaluated.
Definition 6 (Continuation Marker). Let s be a program statement, then
K(s) is a continuation marker. The empty continuation is denoted with K( )
and expresses that nothing remains to be evaluated.
    The local evaluation rules defining valσ (s) are in Fig. 2. The rules for call and
return emit suitable events, the rule for sequential composition assumes empty
leading continuations are discarded, the remaining rules are straightforward.
    We define schematic traces that allow us to succinctly characterize sets of
                                                                       ev
traces (not) containing certain events via matching. The notation · · · represents
the set of all non-empty, finite traces without events of type ev ∈ ev. Symbol
                        ∅                                                          ev
· · · is shorthand for · · · and Ev includes all event types in Def. 3. With τ1 · · · τ3
                                                                        ev
we denote the set of well defined traces τ1 ∗∗τ2 ∗∗τ3 so that τ2 ∈ · · ·. Schematic
traces make it easy to retrieve the most recent event and the current call context
from a given trace:
3
    Alternatively, one could use state transitions labeled with (possibly empty) events.
                   Towards Trace-based Deductive Verification (Tech Report)                  5


          valσ (skip) = hσi · K( )            valσ (x = e) = hσi y σ[x 7→ valσ (e)] · K( )
           valσ ({ s }) = valσ (s)             valσ (return e) = retEvσ (valσ (e)) · K( )
                          (
                            hσi · K(s), if valσ (e) = tt
     valσ ( if e { s }) =
                            hσi · K( ) otherwise
 valσ (while e { s }) = valσ ( if e { s; while e { s }})
           valσ (r; s) = τ · K(r ′ ; s), where valσ (r) = τ · K(r ′ ) and ; s   s
     valσ ({ x; d s }) = hσi y σ[x′ 7→ 0] · K({d s[x ← x′ ] }) with x′ 6∈ dom(σ)
     valσ (x = m(e)) = callEvσ (m, valσ (e), id) · K(x = res id ) where res id 6∈ dom(σ)


                           Fig. 2. Local Program Semantics


Definition 7 (Last Event, Current Context). Let τ be a non-empty trace.
                            (
                                                         Ev
                              evσ (v)  τ ∈ · · · evσ (v) · · ·
               lastEv(τ ) =
                              N oEvent otherwise
                                                                pushEv,popEv
               ctx
                                      τ ∈ · · · pushEvσ (ctx)    ···           pushEv
                                                                                popEv
  currCtx(τ ) = currCtx(τ ′ )               ′
                                       τ ∈ τ ∗∗pushEvσ (ctx) · · · popEvσ′ (ctx) · · ·
               
               
                (main, nul)            otherwise

    Local evaluation of a statement s yields a small step τ of s plus a continua-
tion K(s′ ). Therefore, traces can be extended by evaluating the continuation and
stitching the result to τ . This is performed by composition rules that operate on
a configuration of the form τ, K(s). The process terminates when all statements
are evaluated, i.e. K(s) = K( ). In this case τ is the semantics resulting from
evaluation of a program. There are three composition rules. The following rule
evaluates a statement that has not been directly preceded by a call or return
and extends the current trace accordingly.

                   τ 6∈ · · · callEvσ ( , , )                  τ 6∈ · · · retEvσ ( )
        (Progress)        σ = last(τ )                 valσ (s) = τ ′ · K(s′ )              (1)
                                                            ′     ′
                                         τ, K(s) → τ ∗∗τ , K(s )
    Procedure calls and returns must be handled differently to model the change
of call context and the return of the computed result. Right after a call statement
was evaluated, i.e. when τ ends with a call event, the call context is switched to
the new context ctx and the body s′ of the called procedure is inlined:

                    ctx = (m, id)           τ ∈ · · · callEvσ (m, v, id)
                      ′
             (Call) s   = sc[x ← v], where lookup(m,     G) = m(x) sc                       (2)
                                                                      ′
                             τ, K(s) → τ ∗∗pushEvσ (ctx), K(s ; s)
6       Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta

   Immediately after a return statement the returned value is assigned to the
result variable associated with the current context and the context is switched
back to the old context ctx retrieved from τ via matching. Together, rules (2)–(3)
model synchronous semantics of procedure calls.
                    ctx = currCtx(τ ) = (m, id)            τ ∈ · · · retEvσ (v)
      (Return)                                                                    (3)
                  τ, K(s) → τ y σ[res id 7→ v]∗∗popEvσ[ res id 7→v] (ctx), K(s)

Example 3. We evaluate configuration hσ0 i, K(x = m(1)) for empty σ0 , with m
as defined in Expl. 1. Let s = mb[k ← 1], where mb is the body of m. Applying
the progress and call rule we obtain the initial rule sequence:
              hσ0 i, K(x = m(1)) → callEvσ0 (m, 1, 0), K(x = res 0 )
              → callEvσ0 (m, 1, 0)∗∗pushEvσ0 ((m, 0)), K(s; x = res 0 )
    It is straightforward to see that the local evaluation and the composition
rules are exhaustive and deterministic, which justifies the following definition:
Definition 8 (Program Trace). Given a program s and a state σ, the trace
of s (with implicit lookup table) is the maximal sequence obtained by repeated
application of composition rules, starting from hσi, K(s). If finite, it has the
                                                         ∗
form hσi, K(s) → · · · → τ, K( ), also written hσi, K(s) → τ, K( ).
Definition 9 (Program Semantics). The semantics of a program s is only
                                                            ∗
defined for terminating programs as [[s]]τ = τ ′ if τ, K(s) → τ ∗∗τ ′ , K( ).
From this definition and the local semantics of sequential statements it is easy
to prove Proposition 1 in the appendix by straightforward induction.
Example 4 (Continuing Example 3). Fig. 3 visualizes the semantics [[x = m(1)]]hσ0 i
with the intermediate states σ1 = σ0 [r ′ 7→ 0], σ2 = σ1 [r ′′ 7→ 0], σ3 = σ2 [res 1 7→
0], σ4 = σ3 [r ′ 7→ 0], σ5 = σ4 [r ′ 7→ 1], and σ6 = σ5 [res 0 7→ 1].
We only consider traces that are adequate, i.e. consistent with local evaluation
and composition rules: context switches can only occur in event pairs callEv-
pushEv and retEv-popEv consistently with the current context, and the freshness
of call identifiers has to be preserved. We define Traces as the set of all adequate
traces. For details, see Appendix A.2.


3   A Logic for Trace Contracts
We present a logic for specifying properties over finite program traces. The logic
is a temporal µ-calculus [35] with two binary temporal operators, correspond-
ing to concatenation and chop over sets of traces, respectively. We consider the
syntax fragment without negation, which guarantees that fixed-point formulas
indeed denote fixed points of the corresponding sematic transformers, and with
least fixed-point recursion only. Then we show this logic to be suitable for ex-
pressing relevant finite-trace properties of recursive programs.
                   Towards Trace-based Deductive Verification (Tech Report)          7



              callEv σ0 (m, 1, 0)∗∗
              pushEvσ0 ((m, 0))
              y σ0 [r ′ 7→ 0]
              ∗∗callEvσ1 (m, 0, 1)
              ∗∗pushEvσ1 ((m, 1))                   [[x = m(1)]]hσ0 i =
                       ′′
              y σ1 [r        →
                             7
                     call m(1)    0]            currCtx=(m,  1)
              ∗∗retEv   σ2 (0)
             switch to context (m, 0)
              y  popEvσ2 [ res
               initializing
                       ′
                                   fresh     r((m,
                                        1 7→0]
                                               ′      1))
              y σ3 [rcall  →
                           7     0]
                               m(0)                     currCtx=(m, 0)
                       ′
              y σ4 [r
             switch       7→ 1] (m, 1)
                     to context
              ∗∗retEv   σ5 (1)fresh r ′′
               initializing
              y popEv
                    return          r ′′0 7→1] ((m, 0))
                             σ5 [ res                           currCtx=(Main,nul)
              y σ6 [x 7→ 1]

            switch from context (m, 1)
                     r ′ = res 1
                    r ′ = r′ + 1
                     return r ′
            switch from context (m, 0)
                      x = res 0

              Fig. 3. Visualization of the semantics of x = m(1) in σ 0


3.1   Syntax
The formulas of our logic are built from a set LVar of first-order (“logical”)
variables and a set RecVar of recursion variables. The syntax of the logic is
defined by the following grammar:

      Φ ::= ⌈P ⌉ | X(t) | Ev | Φ ∧ Φ | Φ ∨ Φ | Φ · Φ | Φ ∗∗ Φ | (µX(y).Φ)(t)

where P ranges over first-order predicates, X over recursion variables, y over
tuples of first-order variables, t over tuples of terms over first-order variables,
and where in the last clause the arities of y and t agree.
    Events Ev have the form startEv(m, e, i) or finishEv(m, e, i). There are no
push or pop events, but the finish events record the context. As stated in the
introduction, we aim at procedure-modular specification and verification. There-
fore, it is not necessary to record all context switches in a global trace, as long
as corresponding calls and returns can be uniquely identified.

Remark 1. Events Ev in the logic are syntactic representations of events in the
local semantics (Sect. 2), thus different entities. This permits to tailor events
to the desired degree of abstraction of specifications and the deduction system.
For example, if one is only interested in the interface behavior of a program,
but not in internal state changes, one might choose abstract events of the form
callEv(m)/retEv(m), where call identifiers and arguments are dropped.
8          Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta


                   [[⌈P ⌉]]β,ρ = {hσi | σ ∈ Σ ∧ σ |= P }                 [[X(t)]]β,ρ = ρ(X)(β(t))
      [[startEv(m, e, i)]]β,ρ = {callEvσ (m, e, i)∗∗pushEvσ ((m, i)) | σ ∈ Σ}
      [[finishEv(m, e, i)]]β,ρ = {retEvσ (valσ (e)) · popEvσ[ res i 7→valσ (e)] ((m, i)) | σ ∈ Σ}
              [[Φ1 ∧ Φ2 ]]β,ρ = [[Φ1 ]]β,ρ ∩ [[Φ2 ]]β,ρ        [[Φ1 ∨ Φ2 ]]β,ρ = [[Φ1 ]]β,ρ ∪ [[Φ2 ]]β,ρ
               [[Φ1 · Φ2 ]]β,ρ = {τ1 · τ2 | τ1 ∈ [[Φ1 ]]β,ρ ∧ τ2 ∈ [[Φ2 ]]β,ρ }
             [[Φ1 ∗∗ Φ2 ]]β,ρ = {τ1 ∗∗ τ2 | τ1 ∈ [[Φ1 ]]β,ρ ∧ τ2 ∈ [[Φ2 ]]β,ρ }
        [[(µX(y).Φ)(t)]]β,ρ = [[µX(y).Φ]]β,ρ (β(t))
             [[µX(y).Φ]]β,ρ = ⊓ {F : D → 2Traces | λd.[[Φ]]β[y7→d],ρ[X7→F ] ⊑ F }
           ⊑ and ⊓ denote point-wise set inclusion and intersection, respectively


                                   Fig. 4. Semantics of formulas


Example 5. To illustrate our logic, we introduce a formula template (or pattern)
that we make extensive use of later. Let m be a procedure name, and let NoEv (m)
be a predicate that is true of a state if the latter is not an event that involves m.
Consider the recursive formula:

                            Ψm = µX.(NoEv (m) ∨ NoEv (m) · X)

It is true for any trace that is either a singleton trace which is not an event in-
volving m (base case), or else for a trace that starts with a singleton trace that is
not an event involving m and continues as a trace satisfying Ψm (induction case).
Equivalently, Ψm holds for finite traces not containing any event involving m.
                                                                                   m
    With help of Ψm , we define the binary logic operator Φ1 ·· Φ2 as shorthand
for Φ1 ∗∗ Ψm ∗∗ Φ2 , expressing the trace property of satisfying Φ1 initially, satis-
fying Φ2 in the end, and not containing any event involving m in between. This
                                                  ev
is the logic equivalent of the semantic operator · · · on traces introduced earlier.


3.2      Semantics

To define the semantics of our logic, we need a first-order variable assignment
β : LVar → D and a recursion variable assignment ρ : RecVar → (D → 2Traces )
that assigns each recursion variable to a set of traces. The (finite-trace) seman-
tics [[Φ]]β,ρ of formulas as a set of traces is inductively defined in Fig. 4.
     By a trace formula we mean a formula of our logic that is closed with respect
to both first-order and recursion variables. Since the semantics of a trace formula
does not depend on any variable assignments, we sometimes use [[Φ]] to denote
[[Φ]]β,ρ for arbitrary β and ρ. We also permit a slight extension, where we allow
trace formulas to be syntactically closed with respect to first-order operators, as
long as fixed-point formulas occur only in positive positions.
                  Towards Trace-based Deductive Verification (Tech Report)              9

3.3   Specifying Procedure Contracts

In general, a (finite-trace) procedure contract should capture the sequences of
states and events that are allowed to occur as a result of a call to that procedure.
Since the procedure may recursively call other procedures, such contracts need
to be stated recursively. The base case(s) of a recursive contract should specify
the traces that do not involve any procedure calls. The induction case(s), on
the other hand, should specify the remaining traces, and use recursion variables,
properly applied to arguments, at the points where calls to procedures are made.
    While it can be cumbersome to propose a general pattern for procedure con-
tracts, we illustrate the idea on a particular class of contracts that generalize
traditional, Hoare-style state-based contracts to trace-based ones. As usual, we
use state predicates over logical variables to formulate pre- and postconditions
that express the intended relationship between the values of the program vari-
ables upon procedure call and return, but in addition, we capture the structure
and arguments of recursive procedure calls. We propose the following pattern,
where m is the name of the specified procedure, n the value of its (sole) formal
parameter with which it is called, and i the call identifier:

Hm = µXm (n, i).
                                      m                                  .
         ⌈pre base
              m ⌉ ∗∗ startEv(m, n, i) ·· finishEv(m, fm (n), i) ∗∗⌈res i = fm (n)⌉ ∨
                                       m          −1
         ⌈pre step
              m ⌉ ∗∗ startEv(m, n, i) ·· Xm (step    (n), #(i))
                                       m                                 .         
                                       ·· finishEv(m, fm (n), i) ∗∗⌈resi = fm (n)⌉

                                                               base/step
   Both base and inductive case use state predicates pre m              to establish
                                                               .
the precondition. Both cases use the state predicate res i = fm (n) to specify
the return value res i of m as a function fm depending on the value n of the
formal parameter. The inductive case also specifies a recursive call to m. The first
argument is the inverse of the recursive step function, for example, step −1 = n−1
when step = n + 1. The symbol # ensures that the call context identifier is fresh.

Example 6. We illustrate the use of pattern Hm to provide a contract for the
procedure m from Example 1. To specify that the returned value equals the
                                                      .
value of the parameter, we should define pre base
                                               m  = n = 0, fm as the identity
function, pre step
              m    = n > 0, and step(n) = n + 1:
                .                       m                            .
 µXm (n, i). ⌈n = 0⌉ ∗∗startEv(m, 0, i) ·· finishEv(m, 0, i) ∗∗⌈resi = 0⌉ ∨
                             m                   m                             .    
  ⌈n > 0⌉ ∗∗startEv(m, n, i) ·· Xm (n − 1, #(i)) ·· finishEv(m, n, i) ∗∗⌈res i = n⌉

    The traditional big-step semantics of state-based contracts can be expressed
                                              .
simply as Hm ⊆ ⌈pre base
                     m    ∨ pre step
                                m ⌉ ·· ⌈res i = fm (n)⌉.
    In addition to the final state, we can also specify behavior related to inter-
mediate states. The contract in Example 6 can be extended to relate the result
of the internal recursive call to the final state by replacing the trace after the
10      Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta

recursive call Xm (n − 1, #(i)) with
                                m                             .
          ∗∗ ⌈res #(i) = n − 1⌉ ·· finishEv(m, n, i) ∗∗⌈res i = res #(i) + 1⌉
    Trace formulas (by design) completely abstract away from a specified pro-
gram, to which they are only connected via events. The set Ev of events can be
extended if needed. It is also conceivable to expose parts of the program state
in traces: Let predicate expose(l, e, i) be true in all states σ, such that local vari-
able l in the call identified by i has value β(e). Then one can, for example, insert
“∗ ∗ ⌈expose(r, n − 1, i)⌉” right after the recursive call to Xm above to express
that r has the value n − 1 immediately after the call returns.

4     A Calculus for Deductive Verification
To verify whether a program fulfills its trace contract, we design a symbolic
execution calculus that reduces programs to a sequence of syntactic state updates
containing recursive calls. These are matched against a trace contract formula
with a novel abstraction rule.

4.1    Updates
Updates [1] can be seen as explicit substitutions recording state changes. An
elementary update assigns an expression e to variable v, denoted by {v := e}.
We also admit event updates {Ev(e)} to record that event Ev with parameters e
occurred (here, Ev is startEv or finishEv, but this is generalizable). A composite
update U is a (possibly empty) sequence of elementary/event updates, see the
grammar on top of Fig. 5. Updates U precede statements s with the meaning
that in Us statement s is evaluated under the state changes embodied by U.
Example 7. An expression like “ {startEv(m′ , 0, i)}{r := 0} return r ” results
after partial symbolic execution of a procedure m′ , where only the return state-
ment is left to be executed in a state where r is assigned value 0.

Local Evaluation. We extend the local semantic evaluation rules to programs
with leading updates. Fig. 5 contains semantic rules for expressions of the form
uUs, where u is either an elementary update or an event update. If U is empty
then after the evaluation of u the rules from Sect. 2 apply. The rules are sim-
ilar to those for statements. The first rule is similar to the rule for sequen-
tial composition. Three rules evaluate elementary updates: (a) the case cor-
responding to assignments; (b) if a result variable res i is assigned, then the
update is simply ignored: it is redundant, because its evaluation always follows
finishEv(m, e, i); (c) the semantics of procedure calls invokes the program se-
mantics. The last two rules evaluate event updates occurring in the deduction
rules. They represent the start and end of the execution of m, respectively, and
generate suitable events.
Example 8. One step of local evaluation of Example 7 in a state σ yields the
expression “callEvσ (m′ , 0, i)∗∗pushEvσ ((m′ , i)) · K({r := 0}return r)”.
                     Towards Trace-based Deductive Verification (Tech Report)                  11


                       U ::= ǫ | {v := e}U | {Ev(e)}U         (ǫ empty sequence of updates)

  valσ (uUs) = τ · K(Us), if valσ (u) = τ · K( )
  valσ ({v := e}) = valσ (v = e), with v 6= res i               valσ ({res i := e}) = hσi · K( )
  valσ ({v := m(e)}) = [[v = m(e)]]hσi · K( ), when [[v = m(e)]]hσi is defined
  valσ ({startEv(m, e, i)}) = callEvσ (m, e, i)∗∗pushEvσ ((m, i)) · K( )
  valσ ({finishEv(m, e, i)}) = retEvσ (valσ (e)) · popEvσ[ res i 7→valσ (e)] ((m, i)) · K( )


   Fig. 5. Update syntax and local evaluation of statements with leading updates


Updates over Expressions. Expressions e are evaluated in the current program
state, represented by a preceding composite update U. To evaluate e under U,
written U(e), we apply updates from inner- to outermost. Applying an elemen-
tary update {v := e′ } to an expression e corresponds to syntactic substitution.
Events have no effect on the value of expressions. We obtain the following rules:

      U ′ u(e) = U ′ (u(e))      {v := e′ }(e) = e[v/e′ ])         {Ev( )}(e) = ǫ(e) = e

The trace composition is performed by applying rule (1) (PROGRESS ), overloaded
to support the occurrence of updates. Therefore, the semantics is defined in a
similar manner as in Def. 9:
Definition 10 (Semantics of Programs with Updates). We define the se-
mantics of a terminating program (undefined else) with leading updates as
                                          ∗
           [[U s]]τ = τ ′ , if τ, K(U s) → τ ∗∗τ ′ , K( ), with s possibly empty.

     When symbolically executing the return statement we need to generate a
finishEv whose context matches the current context of the leading update. We
retrieve the call context from the leading update with a helper function:
Definition 11 (Current Context for Updates).
              
              
               (m, i)        U = U ′ {startEv(m, , i)}
              
               currCtx(U ′ ) U = U ′ {v := e}
 currCtx(U) =
              
              
               currCtx(U ′ ) U = U ′ {startEv(m, , i)}U ′′ {finishEv(m, , i)}
              
                (main, nul)   otherwise

Example 9. The context in which the return statement of Example 7 executes
is: currCtx({startEv(m′ , 0, i)}{r:=0}) = currCtx({startEv(m′ , 0, i)}) = (m′ , i).

4.2     Calculus for Straight-line Programs
First we present a calculus for programs that do neither contain loops nor pro-
cedure calls. Our deductive proof system is a Gentzen-style sequent calculus,
12       Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta

where partial symbolic execution of a program is represented by Us, with U the
executed part and s the remaining part. If we judge Us to conform to a trace
specification Φ we write U s : Φ, where the judgment U s : Φ is evaluated in a
current state σ, formally:
Definition 12 (Judgment, Assertion, Sequent). A judgment has the shape
U s : Φ, where U is an update, s a program statement, and Φ a trace formula.
An assertion is either a closed first-order predicate P or a judgment. A sequent
has the shape Γ ⊢ U s : Φ, where Γ is a set of assertions.

Definition 13 (Semantics of Sequents). Let σ be a state. A first-order pred-
icate P is true in σ if σ |= P , as usual in first-order logic. A judgment U s : Φ
is true in σ, denoted σ |= U s : Φ, when [[U s]]hσi is undefined or [[U s]]hσi ∈ [[Φ]].
A sequent Γ ⊢ U s : Φ is true in σ if one of the assertions in Γ is not true in σ
or σ |= U s : Φ. A sequent is valid if it is true in all states σ.

Rules. The rules of our calculus for the symbolic execution of straight-line pro-
grams are shown in Fig. 6. For space reasons, we omit the standard rules for


              Γ ⊢ U{v := e}s : Φ                         Γ, P ⊢ Q      Γ, P ⊢ Us : Φ
     Assign                                   Prestate
              Γ ⊢ U v = e; s : Φ                           Γ, P ⊢ Us : ⌈Q⌉ ∗∗ Φ
                 Γ ⊢ Us : Φ                   Γ, U(e) ⊢ Us; s′ : Φ       Γ, U(!e) ⊢ Us′ : Φ
        Scope                          Cond
                Γ ⊢ U{s} : Φ                             Γ ⊢ U if e { s }; s′ : Φ
                   currCtx(U) = (m, i)        Γ ⊢ U{finishEv(m, e, i)}res i = e : Φ
          Return
                                         Γ ⊢ U return e : Φ
                          Γ ⊢ U{v := 0}{s[v ′ /v]} : Φ
                                   ′
                                                             v ′ fresh for s, Γ, Φ
                VarDecl
                                           Γ ⊢ U{v; s} : Φ

                     Fig. 6. Sequent rules for straight-line programs


Gentzen-style first-order sequent calculi. In the following we present a number
of specific rules, starting with the rule for unfolding fixed-point formulas:
                                                            
                               Γ ⊢ Us : Φ (µX(y).Φ)/X, t/y
                       Unfold
                                   Γ ⊢ Us : (µX(y).Φ)(t)

Example 10. We show the first step of the symbolic execution of the straight-
line program “ if (k!=0) { r=k−1; r=r+1; } return r” with premise Γ ≡ k > 0
and under a similar event update U ≡ {startEv(m, k, i ′ )} as in Example 7. The
first statement is a conditional, so rule Cond is applied. Observe that U(k!=0)
evaluates to k != 0 and is subsumed by k > 0. We show only the left premise
as the right premise is immediately closed due to k > 0. The final sequent is
the result of applying rule Assign twice, followed by an application of the Return
rule. An unabbreviated version is in appendix B.
                     Towards Trace-based Deductive Verification (Tech Report)               13

                             (symbolic execution finished)
           k > 0 ⊢ U{r := k − 1}{r := r + 1}{finishEv(m, r, i ′ )}{res 0 := r} : Φ
                                           ..
            Cond                            .
                  k > 0 ⊢ U if (k!=0) {r=k−1; r=r+1;} return r : Φ

4.3     Procedure Contracts
Specifying and verifying trace contracts for each procedure allows us to verify
procedure calls in a modular way. First we show how to specify a procedure m
with a contract Cm , then we present the rule ProcedureContract that is used to
prove Cm in our calculus. Let
                                                             .
            Cm = ∀n, i.(prem (n) → m(n) : Φm (n, i) ∗∗⌈res i = fm (n)⌉) ,                  (4)

where fm (n) is the result of m given input n.4 Eq. (4) can be seen as the
                                             .
generalization of ∀n.({prem (n)}m(n){res = fm (n)}), a state-based contract,
where n is a first-order parameter. When proving correctness of trace contracts
Cm of recursive procedures m [1,20,37], one establishes that Φm is a specification
invariant for the implementation of m. One proves that the inlined body of m
respects Cm and when symbolic execution arrives at a recursive call to m, one
can assume that m holds already. This yields partial correctness. We generalize
this approach to traces in the following rule for recursive self-calls:

                      Γ, prem (n′ ), Cm ⊢ inline(m, n′ , i′ ) : Φm (n′ , i′ )    i′ , n′ fresh
ProcedureContract
                                                 Γ ⊢ Cm

    The rule expresses that for any parameter n′ and any recursion depth i′ ,
the trace specification Φm (n′ , i′ ) is an invariant for the inlined procedure body,
where Cm can be assumed in recursive calls. To represent inlining succinctly, we
use
               inline(m, e, i) = {startEv(m, e, i)} e′ = e; mb[e′ /p] ,           (5)
where p is the procedure parameter, and e′ is fresh.
    In general, there might be more than
                                     V one procedure call, so the assumption
in (ProcedureCall) should actually be m∈procedures(P ) Cm .

Example 11. Symbolic execution for procedure m from Example 1 with contract
                                      .
Cm = ∀n, i.(m(n) : Φm (n, i) ∗∗⌈res i = n⌉), with U = {startEv(m, n′ , i ′ )}:

                          (here symbolic execution of procedure body starts)
                    n′ ≥ 0, Cm ⊢ U{k′ := n′ }{r ′ := 0}s[k/k′ , r/r ′ ] : Φm (n′ , i ′ )
                                                 ..
                                                  .
                            n′ ≥ 0, Cm ⊢ inline(m, n′ , i ′ ) : Φm (n′ , i ′ )
          ProcedureContract
                                             ⊢ Cm
4
    For technical reasons, the formalization of contract Cm uses a procedure call outside
    of an assignment. Its local trace semantics valσ (m(e)) = callEvσ (m, valσ (e), id) · K( )
    is the same as for procedure calls with assignment, except for the empty continuation.
14        Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta

4.4      Procedure Calls

As Example 11 shows, after applying rule (ProcedureContract), a procedure body
can be fully symbolically executed, where recursive calls in assignments are sim-
ply handled by the (Assign) rule. The semantics of elementary updates with a
call on the right ensures that this is sound provided that we make the assumption
that a procedure call has no side effects. In this way, we can retrofit standard,
state-based verification into our trace-based framework.5 Complete symbolic ex-
ecution of a procedure body with a recursive call yields a judgment of the form

                        U1 {r := m(e)} U2 : Φ1 ∗∗ Φm (e, k) ∗∗ Φ2 .                          (6)

The updates are here followed by the “empty” program. For the trace spec-
ification the above shape is also justified, because typically we have Φm =
µX(y).(Φ1 (y)∨· · ·∨Φn (y)). This specification one strengthens into µX(y).Φi (y),
where Φi is the specification case corresponding to the current symbolic execution
path. At this point, and after symbolic execution finished, we can use pattern (6)
and assumption Cm in the following trace abstraction rule:

             Γ ⊢ U1 : Φ1    Γ ⊢ U1 (prem (e))     Cm ⊢ {v := fm (U1 (e))}U2 : Φ2
     TrAbs
                       Γ, Cm ⊢ U1 {v := m(e)} U2 : Φ1 ∗∗ Φm (e, k) ∗∗ Φ2

where fm (·) is the function computed by m. The trace abstraction rule decom-
poses the conclusion into three premises. The first premise verifies that the trace
represented by U1 conforms to Φ1 . The second premise guarantees that the pre-
condition of contract Cm is satisfied. Contract Cm is now implicitly used to
guarantee that the trace of update {v := m(e)} conforms to Φm (e, k), up to
assignment of the procedure’s result to program variable v. The task of the
third premise is then to ensure that the trace consisting of the latter assignment
followed by update U2 conforms to Φ2 .

Example 12. Trace abstraction is applied in the continuation of Example 11,
after the recursive call in the body was symbolically executed and moved to an
update. At this point the goal sequent has the form
                                                           m                       m
         n′ > 0, Cm ⊢ {U1 }{r′ := m(n′ − 1)}U2 : Φ1 ·· Φm (n′ − 1, #(i ′ )) ·· Φ2

with U1 ≡ {startEv(m, n′ , i ′ )}, U2 ≡ {r ′ := r′ + 1}{finishEv(m, r ′ , i ′ )}{res i ′ := r′ },
                                        m
Φ1 ≡ ⌈n′ > 0⌉ ∗∗startEv(m, n′ , i ′ ) ··, Φm (n′ − 1, #(i ′ )) ≡ Xm (n′ − 1, #(i ′ )), and
     m                                 .
Φ2 ≡ ··finishEv(m, n′ , i ′ )·⌈res i ′ = n′ ⌉. Applying the trace abstraction rule results

5
     We stress that the absence of side effects is for ease of presentation and not a funda-
     mental limitation of our approach. How to model side effects in symbolic execution
     is well-known [1].
                     Towards Trace-based Deductive Verification (Tech Report)                     15

in the following three sequents:
                                                                                m
         n′ > 0 ⊢ {startEv(m, n′ , i ′ )} : ⌈n′ > 0⌉ ∗∗startEv(m, n′ , i ′ ) ··
         n′ > 0 ⊢ n′ > 0
        .
res i ′ = n′ − 1 ⊢ {r ′ := res i ′ }{r′ := r ′ + 1}{finishEv(m, r ′ , 0)}{res i ′ := r ′ } :
                                                         m                                     .
                                                          ·· finishEv(m, n′ , i ′ ) · ⌈res i ′ = n′ ⌉

The first subgoal is provable with rule (Prestate) and a simplification rule, the
second is trivial, the third requires simplification rules found in Appendix B.

Loops. For space reasons, we do not provide rules for dealing with loops. Concep-
tually, it is well-known that contracts can be used to specify loops. A systematic
overview and comparison between invariant-based and contract-based loop spec-
ification is in [10]. A suitable adaptation of our contract rules to the case of loops
will be the topic of future work.

4.5    Soundness
Definition 14 (Soundness). A rule of the calculus is sound if the validity of
the conclusion follows from the validity of the premises. A calculus is sound if it
can prove only valid statements.
Theorem 1 (Calculus soundness). The presented sequent calculus is sound.
Proof. Direct consequence of the local soundness of each rule. Proof sketches for
the soundness of the rules are given in Appendix A.


5     Related Work
We specify symbolic traces, so it is not surprising to find related work in exten-
sions of LTL model checking and program synthesis. CaReT logic [2] can specify
the call structure of programs which is modeled as pushdown automata. It has
abstract versions of the temporal next and until operators that jump over bal-
anced calls. The call and event structure is fixed. In [12] Systems of Procedural
Automata model procedure calls with context-free rules for atomic actions and
procedure calls. The goal is to learn automata from observed traces. Temporal
Stream Logic [11] features uninterpreted function terms and updates in addi-
tion to standard LTL operators, aiming at program synthesis of Büchi stream
automata and FPGA programs. In each case the setup is finite or propositional,
not first-order. Matching and fixed-point specifications are not possible.
    Process logic [16] and interval temporal logic [15] feature the chop operator,
which was taken up by Nakata & Uustalu [29], who used infinite symbolic traces
to characterize non-terminating loops. These were extended to a rich dynamic
logic [6] and equipped with events and a local trace semantics [9].
    Cyclic proof systems to prove inductive claims, including contracts of re-
cursive procedures, date back to Hoare’s axiomatization of recursive procedures
16      Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta

[19]. Gurov & Westman [13] provide an abstract framework based on denota-
tional semantics to formally justify (cyclic) procedure-modular verification, while
Brotherston & Simpson [5] investigate the expressive power of sequent calculi for
cyclic and infinite arguments that are often used as a basis in deductive verifica-
tion. Recursive predicate specifications are standard, for example, in separation
logic [31], but not used to specify program traces. Several papers [7,34] present
a first-order µ-calculus, but do not feature explicit programs or events.
    Constructive logical frameworks [4,30] feature abstract specifications in terms
of typed higher-order logic formulas, but they target functional languages and
feature neither events nor traces.


6    Conclusion and Future Work
In this paper we established the fundamental theory of trace-based contracts,
generalizing specification and deductive verification with state-based contracts.
The ingredients are (i) an expressive fixed-point logic to characterize complex
event structures over recursive procedures; (ii) a uniform, local trace-event se-
mantics for programs, state updates, and the trace logic; (iii) a sound symbolic
execution calculus with rules to prove trace contracts and programs with recur-
sive procedures. Programs and trace contracts communicate semantically via a
configurable set of events. This permits fully abstract specification of programs
and a highly flexible approach to specify concepts like user input, concurrency,
etc. Indeed, to harvest these opportunities arising from an expressive, trace-based
specification and verification approach, will be the topic of follow-up papers,
where we will look at concurrent programs, loops, and complex case studies.
    Further interesting questions concern the precise expressivity of our trace
logic, in particular, which events are required for completeness.


References
 1. W. Ahrendt, B. Beckert, R. Bubel, R. Hähnle, P. Schmitt, and M. Ulbrich, editors.
    Deductive Software Verification—The KeY Book: From Theory to Practice, volume
    10001 of LNCS. Springer, 2016.
 2. R. Alur, K. Etessami, and P. Madhusudan. A temporal logic of nested calls and
    returns. In K. Jensen and A. Podelski, editors, Tools and Algorithms for the Con-
    struction and Analysis of Systems, 10th Intl. Conf., TACAS, Barcelona, Spain,
    volume 2988 of LNCS, pages 467–481. Springer, 2004.
 3. P. Baudin, J.-C. Filliâtre, C. Marché, B. Monate, Y. Moy, and V. Prevosto. ACSL:
    ANSI/ISO C Specification. Technical Report Version 1.17, CEA and INRIA, 2021.
 4. Y. Bertot and P. Castéran.           Interactive Theorem Proving and Program
    Development—Coq’Art: The Calculus of Inductive Constructions. Texts in Theo-
    retical Computer Science. An EATCS Series. Springer, 2004.
 5. J. Brotherston and A. Simpson. Sequent calculi for induction and infinite descent.
    J. Logic and Computation, 21(6):1177–1216, 2011.
 6. R. Bubel, C. C. Din, R. Hähnle, and K. Nakata. A dynamic logic with traces and
    coinduction. In H. D. Nivelle, editor, Intl. Conf. on Automated Reasoning with
                  Towards Trace-based Deductive Verification (Tech Report)          17

    Analytic Tableaux and Related Methods, Wroclaw, Poland, volume 9323 of LNCS,
    pages 303–318. Springer, 2015.
 7. M. Dam and D. Gurov. µ-calculus with explicit points and approximations. J. of
    Logic and Computation, 12(2):255–269, Apr. 2002.
 8. C. C. Din, R. Hähnle, L. Henrio, E. B. Johnsen, V. K. I. Pun, and S. L. Tapia Tar-
    ifa. LAGC semantics of concurrent programming languages, 2022. arXiv preprint
    2202.12195.
 9. C. C. Din, R. Hähnle, E. B. Johnsen, V. K. I. Pun, and S. L. Tapia Tarifa. Locally
    abstract, globally concrete semantics of concurrent programming languages. In
    C. Nalon and R. Schmidt, editors, Proc. 26th Intl. Conf. on Automated Reasoning
    with Tableaux and Related Methods, volume 10501 of LNCS, pages 22–43. Springer,
    Sept. 2017.
10. G. Ernst. Loop verification with invariants and contracts. In B. Finkbeiner and
    T. Wies, editors, Verification, Model Checking, and Abstract Interpretation: 23rd
    Intl. Conf., VMCAI, Philadelphia, PA, USA, volume 13182 of LNCS, pages 69–92.
    Springer, 2022.
11. B. Finkbeiner, F. Klein, R. Piskac, and M. Santolucito. Temporal stream logic:
    Synthesis beyond the bools. In I. Dillig and S. Tasiran, editors, Computer Aided
    Verification: 31st Intl. Conf., CAV, New York City, NY, USA, Part I, volume
    11561 of LNCS, pages 609–629. Springer, 2019.
12. M. Frohme and B. Steffen. Compositional learning of mutually recursive procedural
    systems. Intl. J. Software Tools for Technology Transfer, 23(4):521–543, 2021.
13. D. Gurov and J. Westman. A Hoare logic contract theory: An exercise in de-
    notational semantics. In P. Müller and I. Schaefer, editors, Principled Software
    Development - Essays Dedicated to Arnd Poetzsch-Heffter on the Occasion of his
    60th Birthday, pages 119–127. Springer, 2018.
14. R. Hähnle and M. Huisman. Deductive verification: from pen-and-paper proofs to
    industrial tools. In B. Steffen and G. Woeginger, editors, Computing and Software
    Science: State of the Art and Perspectives, volume 10000 of LNCS, pages 345–373.
    Springer, Cham, Switzerland, 2019.
15. J. Y. Halpern and Y. Shoham. A propositional modal logic of time intervals.
    Journal of the ACM, 38(4):935–962, 1991.
16. D. Harel, D. Kozen, and R. Parikh. Process logic: Expressiveness, decidability,
    completeness. In 21st Annual Symposium on Foundations of Computer Science,
    Syracuse, New York, USA, 13-15 October 1980, pages 129–142. IEEE Computer
    Society, 1980.
17. D. Harel, D. Kozen, and J. Tiuryn. Dynamic Logic. Foundations of Computing.
    MIT Press, Oct. 2000.
18. C. A. R. Hoare. An axiomatic basis for computer programming. Comm. of the
    ACM, 12(10):576–580, 583, Oct. 1969.
19. C. A. R. Hoare. Procedures and parameters: An axiomatic approach. In E. Engeler,
    editor, Symposium on Semantics of Algorithmic Languages, volume 188 of Lecture
    Notes in Mathematics, pages 102–116. Springer, 1971.
20. M. Hofmann. Semantik und Verifikation. Lecture notes, Technical Univer-
    sity Darmstadt, Fachbereich Mathematik, 64289 Darmstadt, 1997. In German,
    http://www.dcs.ed.ac.uk/home/mxh/teaching/marburg.ps.gz.
21. A. Jeffrey and J. Rathke. Java Jr: Fully Abstract Trace Semantics for a Core
    Java Language. In S. Sagiv, editor, Programming Languages and Systems, 14th
    European Symp. on Programming, ESOP, Edinburgh, UK, volume 3444 of LNCS,
    pages 423–438. Springer, 2005.
18      Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta

22. F. Kirchner, N. Kosmatov, V. Prevosto, J. Signoles, and B. Yakobowski. Frama-
    C: a software analysis perspective. Formal Aspects of Computing, 27(3):573–609,
    2015.
23. D. Kozen. Results on the propositional mu-calculus. Theoretical Computer Science,
    27:333–354, 1983.
24. G. T. Leavens, E. Poll, C. Clifton, Y. Cheon, C. Ruby, D. Cok, P. Müller, J. Kiniry,
    P. Chalin, D. M. Zimmerman, and W. Dietl. JML Reference Manual, May 2013.
    Draft revision 2344.
25. K. R. M. Leino and V. Wüstholz. The Dafny integrated development environment.
    In C. Dubois, D. Giannakopoulou, and D. Méry, editors, Proc. 1st Workshop on
    Formal Integrated Development Environment, F-IDE, Grenoble, France, volume
    149 of EPTCS, pages 3–15, 2014.
26. C. Lidström and D. Gurov. An abstract contract theory for programs with proce-
    dures. In E. Guerra and M. Stoelinga, editors, Fundamental Approaches to Software
    Engineering: 24th Intl. Conf., FASE, Luxembourg City, Luxembourg, volume 12649
    of LNCS, pages 152–171. Springer, 2021.
27. B. H. Liskov. Modular program construction using abstractions. In D. Bjørner,
    editor, Abstract Software Specifications, 1979 Copenhagen Winter School, Proceed-
    ings, volume 86 of LNCS, pages 354–389. Springer, 1979.
28. B. Meyer. Applying “design by contract”. IEEE Computer, 25(10):40–51, Oct.
    1992.
29. K. Nakata and T. Uustalu. A Hoare logic for the coinductive trace-based big-step
    semantics of While. Logical Methods in Computer Science, 11(1):1–32, 2015.
30. T. Nipkow, L. C. Paulson, and M. Wenzel. Isabelle/HOL — A Proof Assistant for
    Higher-Order Logic, volume 2283 of LNCS. Springer-Verlag, 2002.
31. M. J. Parkinson and G. M. Bierman. Separation logic and abstraction. In J. Pals-
    berg and M. Abadi, editors, Proc. 32nd ACM SIGPLAN-SIGACT Symposium on
    Principles of Programming Languages, POPL, Long Beach, California, USA, pages
    247–258. ACM, 2005.
32. M. J. Parkinson and A. J. Summers. The relationship between separation logic
    and implicit dynamic frames. Logićal Methods in Computer Science, 8(3), 2012.
33. V. R. Pratt. Semantical considerations on Floyd-Hoare logic. In 17th Annual Symp.
    on Found. of Comp. Sci., Houston, Texas, USA, pages 109–121. IEEE Computer
    Society, 1976.
34. C. Sprenger and M. Dam. On global induction mechanisms in a µ-calculus with
    explicit approximations. Theoretical Informatics and Applications, 37(4):365–391,
    2003.
35. C. Stirling. Modal and Temporal Logics, pages 477–563. Oxford University Press,
    Inc., USA, 1993.
36. A. Tarski. A lattice-theoretical fixedpoint theorem and its applications. Pacific
    Journal of Mathematics, 5:285–309, 1955.
37. D. von Oheimb. Hoare logic for mutual recursion and local variables. In C. P. Ran-
    gan, V. Raman, and R. Ramanujam, editors, Foundations of Software Technology
    and Theoretical Computer Science, 19th Conf., Chennai, India, volume 1738 of
    LNCS, pages 168–180. Springer, 1999.
                   Towards Trace-based Deductive Verification (Tech Report)          19

A     Proofs
A.1    Trace Adequacy
We only consider traces consistent with local evaluation and composition rules:
at most one variable update occurs between two consecutive states and the events
in a trace properly record call events, context switches, and return events.
Definition 15 (Trace Adequacy). We say τ = τ1 ∗∗τ2 is an adequate trace
if either τ1 = τ2 = hσi or τ1 is adequate and exactly one of the following holds:
1. τ2 = hσi y σ[x 7→ v]
                                 pushEv(( ,id)), popEv(( ,id)), callEv( , ,id)
2. τ2 = callEvσ ( , , id), τ1 ∈                   ···                 and
   lastEv(τ1 ) 6∈ {callEv, retEv}
3. τ2 = retEvσ ( ), lastEv(τ1 ) 6∈ {callEv, retEv}
4. τ2 = pushEvσ ((m, id)), τ1 ∈ · · · callEvσ (m, , id)
5. τ2 = popEvσ ((m, id)), τ1 ∈ · · · retEvσ (m), currCtx(τ1 ) = (m, id).
Traces is the set of all adequate traces.
    The second clause expresses that call identifiers are unique as well as one part
of the requirement that call/return events are followed immediately by push/pop
events. That requirement is ensured together with the remaining clauses.
    The events callEv and retEv are always followed by pushEv and popEv respec-
tively. Therefore they can be the last event of a trace only if they occur at the
end of the trace. This result is formalized in the following lemma.
                           n
Lemma 1. If hσi, K(s) → τ, K(s′ ) and callEv = lastEv(τ ), or retEv = lastEv(τ ),
then τ = · · · callEvlast(τ ) or τ = · · · retEvlast(τ ) , respectively.
               ∗                                                                 n
    If τ, K(s) → τ ′ , K(s′ ) in exactly n steps then we write τ, K(s) → τ ′ , K(s′ ).
                                                   n
Lemma 2. Given a program s, if hσi, K(s) → τ, K(s′ ) then τ is adequate.
Proof. We prove the lemma by induction on n, i.e. on the number of applications
of composition rules.
    Base case (n=1). For non trivial programs, s has the form “x d; r”, i.e. at
least a variable x is declared. Otherwise, assignment and procedures calls cannot
occur. Therefore if n = 1 then the rule applied is the progress rule.

                     hσi, K(x d; r) → hσi y σ[x 7→ 0], K(d; s)

where hσi y σ[x 7→ 0] satisfies condition (1) of Def. 15.
                                                           n
   Inductive Step. Let’s assume as IH that hσi, K(s) → τ, K(s′ ) with τ
              ′                 ′
adequate and s 6= . Let also σ = last(τ ). There are three main cases:
 – τ = τ ′ ∗∗callEvσ′ (m, , i): condition (4) is satisfied since applying call rule
   we have

              τ, K(s′ ) → τ ′ ∗∗callEvσ′ (m, , i)∗∗pushEvσ′ ((m, i)), K(s′′ )
20       Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta

 – τ = τ ′ ∗∗retEvσ′ ( ): condition (5) is satisfied since applying return rule we
   have
                τ, K(s′ ) → τ ′ ∗∗retEvσ′ ( )∗∗popEvσ′ ((m, id)), K(s′′ )
   where currCtx(τ ′ ) = (m, id) by definition.
 – τ 6= τ ′ ∗∗callEvσ′ and τ 6= τ ′ ∗∗retEvσ′ : the progress rule applies and we have
   three cases
                     n
     • hσi, K(s) → τ, K(x := m(e); r)): a callEv with a fresh call identifier
       is generated. Since, by Lemma 1 we have that last(τ ) 6∈ {callEv, retEv}
       condition (2) is satisfied.
                    n
     • hσi, K(s) → τ, K(return e; r)): a retEv is generated. Since, by Lemma 1
       we have that last(τ ) 6∈ {callEv, retEv} condition (2) is satisfied.
                                         n
     • Otherwise we have τ, K(s′ ) → τ ′ , K(s′′ )) where either τ ′ = τ adequate
       by IH, or τ ′ = τ y σ ′ [x 7→ v], that satisfies condition (1).

Therefore, given
                                                n
                                   hσi, K(s) → τ, K(s′ )
with τ adequate we have
                                              n+1
                                  hσi, K(s) → τ ′ , K(s′′ )

where τ ′ is adequate.                                                                        ⊓
                                                                                              ⊔

Theorem 2 (Adequacy of Program Semantics). The program semantics
[[s]]hσi is an adequate trace for any state σ and terminating program s.

                                                                                    ∗
Proof. From Lemma 2 it follows that given a program s if hσi, K(s) → τ, K( )
then τ is adequate. In other words [[σ]]s is adequate.                    ⊓
                                                                          ⊔


A.2     Soundness of the Calculus

Proposition 1. [[r; s]]τ = τ ′ ∗∗[[s]]τ ′ , with τ ′ = [[r]]τ .

Proposition 2. [[Us]]τ = [[U]]τ ∗∗ [[s]][[U ]]τ and [[UU ′ ]]τ = [[U]]τ ∗∗ [[U ′ ]][[U ]]τ , and
[[{v := m(e)}]]τ = [[{v := m(e)}]]last(τ ) .

Theorem 3 (Soundness). The presented sequent calculus is sound.

Proof. The result is a direct consequence of the (local) soundness of each rule,
which we show here for selected rules. Recall that a rule is sound if its conclusion
is a valid sequent whenever all its premises are. For some rules we also show
reversibility (also called backward soundness), which means that whenever the
conclusion of the rule is a valid sequent, the rule can be applied backwards in a
way so that all premises are valid.
                    Towards Trace-based Deductive Verification (Tech Report)             21

Rule Assign. We shall prove soundness and reversibility of the rule. Let σ be a
state. We have, with τ = [[U]]hσi :

            σ |= U{v := e}s : Φ
      ⇔     [[U{v := e}s]]hσi ∈ [[Φ]]                           {Def. 13}
      ⇔     τ ∗∗ [[{v := e}]]τ ∗∗ [[s]][[{v:=e}]]τ ∈ [[Φ]]      {Prop. 2}
      ⇔     τ ∗∗ [[v = e]]τ ∗∗ [[s]][[v=e]]τ ∈ [[Φ]]            {Def. valσ ({v := e})}
      ⇔     [[Uv = e; s]]hσi ∈ [[Φ]]                            {Prop. 1,2}
      ⇔     σ |= Uv = e; s : Φ                                  {Def. 13}
We therefore have that the sequent Γ ⊢ {v := e}s : Φ is valid if and only if the
sequent Γ ⊢ v = e; s : Φ is valid.                                             ⊓
                                                                               ⊔

Rule Cond. We shall prove soundness and reversibility of the rule. Let σ be a
state. We have, with τ = [[U]]hσi :

                 σ |= U(e) ⇒ σ |= Us; s′ : Φ
              ∧ σ |= U(!e) ⇒ σ |= Us′ : Φ
        ⇔        σ |= U(e) ⇒ [[U s; s′ ]]hσi ∈ [[Φ]]
              ∧ σ |= U(!e) ⇒ [[U s′ ]]hσi ∈ [[Φ]]                   {Def. 13}
        ⇔        σ |= U(e) ⇒ τ ∗∗ [[s; s′ ]]τ ∈ [[Φ]]
              ∧ σ |= U(!e) ⇒ τ ∗∗ [[s′ ]]τ ∈ [[Φ]]                  {Prop. 2}
        ⇔        vallast (τ ) (e) = tt ⇒ τ ∗∗ [[s; s′ ]]τ ∈ [[Φ]]
              ∧ vallast (τ ) (e) = ff ⇒ τ ∗∗ [[s′ ]]τ ∈ [[Φ]]       {Def. σ |= U(e)}
        ⇔     τ ∗∗ [[ if e { s }; s′ ]]τ ∈ [[Φ]]                    {Fig. 2, Def. 9}
        ⇔     [[U if e { s }; s′ ]]hσi ∈ [[Φ]]                      {Prop. 2}
        ⇔     σ |= U if e { s }; s′ : Φ                             {Def. 13}

Explanation: Given Fig. 2, Def. 9 we have
                                     ∗
            τ, K( if e { s }; s′ ) → τ, K(s; s′ ), if vallast(τ ) (e) = tt, and
                                     ∗
            τ, K( if e { s }; s′ ) → τ, K(s′ ), if vallast(τ ) (e) = ff
Therefore
                 [[ if e { s }; s′ ]]τ = [[s; s′ ]]τ if vallast(τ ) (e) = tt, and
                 [[ if e { s }; s′ ]]τ = [[s′ ]]τ if vallast(τ ) (e) = ff
We therefore have that the sequent Γ ⊢ U if (e) s; s′ : Φ is valid if and only if the
sequents Γ, U(e) ⊢ Us; s′ : Φ and Γ, U(!e) ⊢ Us′ : Φ are valid.

Rule Unfold. We shall prove soundness and reversibility of the rule. By Tarski’s
fixed-point theorem for complete lattices [36], the semantics [[(µX(y).Φ)(t)]]β,ρ
of a fixed-point predicate µX(y).Φ is indeed a fixed point of the trace predicate
transformer λF.λd.[[Φ]]β[y7→d],ρ[X7→F ] . We therefore have the following fixed-point
unfolding equivalence:
                                                             
                     (µX(y).Φ)(t) ≡ Φ (µX(y).Φ)/X, t/y
22      Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta

where Φ1 ≡ Φ2 is defined to hold whenever [[Φ1 ]]β,ρ = [[Φ2 ]]β,ρ for all β and ρ.
The soundness and reversibility of the rule are a direct consequence of this
equivalence.

Rule ProcedureContract. Because the details are somewhat technical, soundness
is only be sketched here. We follow the approach taken in [37] to prove the
soundness of a similar rule, but in the context of Hoare logic. The essence of
the approach is to find a suitable notion of validity of sequents that allows
to capture an inductive argument on the recursive depth of procedure calls.
In [37], this is achieved by augmenting the notion of sequent validity with an
explicit parameter n of that depth, in turn relying on a modified version of the
operational semantics that is also parameterised on n as a bound on the maximal
recursion depth when going from an initial state to a final one. Here, we follow
the same approach, and apply it to traces.

Rule TrAbs. We prove soundness of the rule.

             Γ ⊢ U1 : Φ1 Γ ⊢ U1 (prem (e)) Cm ⊢ {v := fm (U1 (e))}U2 : Φ2
     TrAbs
                    Γ, Cm ⊢ U1 {v := m(e)} U2 : Φ1 ∗∗ Φm (e, k) ∗∗ Φ2

where fm (·) is the function computed by m.
   Assuming the premisses (I)–(III) (from left to right) are valid, we have to
show that the conclusion is valid. This means that for all states σ

             σ |= (Γ ∧ Cm ) → U1 {v := m(e)} U2 : Φ1 ∗∗ Φm(e, k) ∗∗ Φ2

holds. We consider only the non-trivial case where σ |= Γ ∧ Cm holds. This
means we have to prove that

                   [[U1 {v := m(e)} U2 ]]hσi ∈ [[Φ1 ∗∗ Φm (e, k) ∗∗ Φ2 ]]

We can decompose the left side as follows:

[[U1 {v := m(e)} U2 ]]hσi = τ · [[v = m(e)]]τ ·τ ′′ , with [[U1 ]]hσi = τ and [[U2 ]]τ ′ = τ ′′
                            |       {z      }
                                       τ′

Validity of premise (I) ensures already that τ ∈ [[Φ1 ]]hσi .
For the middle part, we observe that
                                            τ̄
                z                       }|                      {
[[v = m(e)]]τ = callEvlast(τ ) (m, e, k)∗∗pushEvlast(τ ) ((m, i)) ∗∗[[mb[p 7→ e]; v = res k ]]τ̄
              = [[m(e); ]]τ ∗∗[[v = res k ; ]]τ̂

with τ̂ = [[m(e); ]]τ .
By assumption σ |= Cm , i.e.,
                                                              .
             σ |= ∀n, i.(prem (n) → m(n) : Φm (n, i) ∗∗⌈res i = fm (n)⌉)
                    Towards Trace-based Deductive Verification (Tech Report)                  23

and hence,
                                                               .
              σ |= (prem (e1 ) → m(e1 ) : Φm (e1 , k) ∗∗⌈res k = fm (e1 )⌉)

with valσ (e1 ) = valσ (U1 e) and e1 fresh rigid constant symbol and i instantiated
with k. Validity of premise (II) asserts that

                σ |= U1 prem (e) ⇔ σ |= prem (U1 e) ⇔ σ |= prem (e1 ) .

    Consequently (modus ponens),
                                                        .
                   σ |= m(e1 ) : Φm (e1 , k) ∗∗⌈res k = fm (e1 )⌉
                                                          .
                  ⇔[[m(e1 )]]hσi ∈ [[Φm (e1 , k) ∗∗⌈resk = fm (e1 )⌉]]hσi
                  ⇒[[m(e1 )]]hσi ∈ [[Φm (e1 , k)]]hσi

   Because there are no side effects from procedure calls on the state, we have
that if for any two states σ, σ ′

                     valσ (e) = valσ′ (e) and valσ (k) = valσ′ (k)

then

          [[m(e)]]hσi = [[m(e)]]hσ′ i     and [[Φm (e, k)]]hσi = [[Φm (e, k)]]hσ′ i .

    Thus we can deduce:

 [[m(e1 )]]hσi = [[m(e)]]hlast(τ )i = [[m(e)]]τ = τ̂        , and further, τ̂ ∈ [[Φm (e, k)]]τ .

   In summary, we have now that τ · τ̂ ∈ [[Φ1 ∗∗Φm (e, k)]]hσi We have not yet
considered the whole trace of the procedure call update. Remember:

            [[v = m(e)]]τ = [[m(e); v = res k ]]τ = [[m(e); ]]τ ∗∗[[v = res k ; ]]τ̂

    It remains to show that

                              [[v = res k ; ]]τ̂ ∗∗[[U2 ]]τ ′ ∈ [[Φ2 ]]τ̂

    This is a direct consequent of premise (III), the only critical point being the
equality of the value of variable v. This follows from the fact that in the conclu-
sion v has the value computed by the procedure when called with parameters
U1 (e) which is the same value to which fm (U1 (e)) evaluates by definition of fm .
                                                                                  ⊓
                                                                                  ⊔


B      Extended Examples
Example 13 (Extended Version of Example 10). Here is the symbolic execution
of the straight-line program “s = if (k!=0) {r=k−1; r=r+1;} return r” with
premise Γ := k > 0. For well-formedness, since the program ends with a return
statement it has to be preceded by a leading update {startEv(m, k, i ′ )}U. We
assume U to be empty.
24       Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta

                                (symbolic execution finished)
            k > 0 ⊢ U1 {r := k − 1}{r := r + 1}{finishEv(m, r, i ′ )}{res i ′ := r} : Φ
  Assign
                k > 0 ⊢ U1 {r := k−1}{r := r+1}{finishEv(m, r, i ′ )}res i ′ =r : Φ
      Return
                     k > 0 ⊢ U1 {r := k − 1}{r := r+1}return r : Φ
             Assign
                       k > 0 ⊢ U1 {r := k−1}r=r+1; return r : Φ
               Assign
                        k > 0 ⊢ U1 r=k−1; r=r+1; return r : Φ
     Cond
          k > 0 ⊢ {startEv(m, k, i ′ )} if (k!=0) {r=k−1; r=r+1;} return r : Φ
                  |       {z          }
                               U1

Example 14 (Extended Version of Example 11). Symbolic execution for proce-
                                                                         .
dure m from Example 1 with contract Cm = ∀n, i.(m(n) : Φm (n, i)∗∗⌈res i = n⌉),
                      ′ ′
with U = {startEv(m, n , i )}:

                           (symbolic execution of procedure body starts)
                     n′ ≥ 0, Cm ⊢ U{k′ := n′ }{r′ := 0}s[k/k′ , r/r ′ ] : Φm (n′ , i ′ )
           VarDecl
                       n′ ≥ 0, Cm ⊢ U{k′ := n′ }{r; s[k/k′ ]} : Φm (n′ , i ′ )
                Assign
                        n′ ≥ 0, Cm ⊢ Uk′ = n′ ; {r ; s[k/k′ ]} : Φm (n′ , i ′ )
                              n′ ≥ 0, Cm ⊢ inline(m, n′ , i ′ ) : Φm (n′ , i ′ )
       ProcedureContract
                                               ⊢ Cm
Example 15 (Extended Version of Example 12). We provide some of the needed
update simplification rules:

                   Γ ⊢ U : Φ, ∆    Γ ⊢ U{x := e}ϕ, ∆
     elimUpdate1
                        Γ ⊢ U{x := e} : Φ · ⌈ϕ⌉, ∆
                                                .             .                .
                   Γ ⊢ U : Φ, ∆     Γ ⊢ (Um) = m′ ∧ (Ue) = e′ ∧ (Ui) = i′ , ∆
     elimUpdate2
                       Γ ⊢ U{finishEv(m, e, i)} : Φ ∗∗finishEv(m′ , e′ , i′ ), ∆

                           Γ ⊢ U1 : Φ, ∆             if U2 does not contain
     subsumeUpdates1                    m
                        Γ ⊢ U1 U2 : Φ ··, ∆          any update involving m
