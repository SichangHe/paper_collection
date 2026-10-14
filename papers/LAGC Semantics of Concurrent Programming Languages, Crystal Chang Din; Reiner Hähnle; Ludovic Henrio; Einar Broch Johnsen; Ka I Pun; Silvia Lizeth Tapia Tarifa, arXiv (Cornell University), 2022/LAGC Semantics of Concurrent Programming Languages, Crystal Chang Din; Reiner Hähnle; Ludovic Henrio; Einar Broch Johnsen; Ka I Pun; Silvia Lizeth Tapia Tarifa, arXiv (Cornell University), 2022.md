                                                   LAGC Semantics of Concurrent Programming Languages

                                                         Crystal Chang Din1 , Reiner Hähnle2 , Ludovic Henrio3 , Einar Broch Johnsen4 ,
                                                                           Ka I Pun5 , and S. Lizeth Tapia Tarifa4
                                                                     1
                                                                       Department of Informatics, University of Bergen, Norway
                                                                                     Crystal.Din@uib.no
                                                          2
                                                            Department of Computer Science, Technische Universität Darmstadt, Germany
                                                                               haehnle@cs.tu-darmstadt.de
                                                                       3
                                                                         CNRS, Inria, LIP, Univ Lyon, EnsL, UCBL, France
                                                                                  ludovic.henrio@cnrs.fr
                                                                     4
                                                                        Department of Informatics, University of Oslo, Norway
                                                                              {einarj,sltarifa}@ifi.uio.no
                                                        5
                                                          Department of Computing, Western Norway University of Applied Sciences, Norway
                                                                                  Violet.Ka.I.Pun@hvl.no
arXiv:2202.12195v1 [cs.PL] 24 Feb 2022




                                               Abstract. Formal, mathematically rigorous programming language semantics are the essential prereq-
                                               uisite for the design of logics and calculi that permit automated reasoning about concurrent programs.
                                               We propose a novel modular semantics designed to align smoothly with program logics used in deductive
                                               verification and formal specification of concurrent programs. Our semantics separates local evaluation of
                                               expressions and statements performed in an abstract, symbolic environment from their composition into
                                               global computations, at which point they are concretised. This makes incremental addition of new language
                                               concepts possible, without the need to revise the framework. The basis is a generalisation of the notion
                                               of a program trace as a sequence of evolving states that we enrich with event descriptors and trailing
                                               continuation markers. This allows to postpone scheduling constraints from the level of local evaluation
                                               to the global composition stage, where well-formedness predicates over the event structure declaratively
                                               characterise a wide range of concurrency models. We also illustrate how a sound program logic and calculus
                                               can be defined for this semantics.


                                         1   Introduction
                                         We propose a trace semantics that scales flexibly to a range of concurrent, imperative programming paradigms,
                                         as found, for example, in C, Java, ProMeLa [44], Actors [41], or Active Objects [22]. Specifically, given a
                                         program P , running on a collection of communicating processors or cores, we want to obtain the set of all global
                                         system traces that P can produce starting from some initial state. Our overall goal is to provide a semantics that
                                         aligns well with contract-based deductive verification [35]. To this end, it is essential that the semantics cleanly
                                         separates local computations (one statement on one core) from global ones; i.e., there must be a suitable notion
                                         of composition that can generate the global traces from the local ones. It is known [16,58] that compositionality
                                         in denotational semantics shifts the flavour of the semantics in the direction of operational semantics [64], by
                                         transitioning from state transformers [42,9] to traces of execution states [39,17,15] or communication events
                                         [21,43,48,26]. We propose a hybrid notion of trace that combines states and events, and show that the ensuing
                                         semantic framework is well-suited to compositionally capture different forms of concurrency for imperative
                                         languages.
                                             The envisaged semantics should also be modular in the following sense: it must be possible to support a new
                                         language construct without the need to revise the whole framework. Ideally, there is a single evaluation rule for
                                         each construct of the target language that can be applied independently from all other rules: the recursive call
                                         to evaluate subsequent statements is not inside the semantic evaluation of each statement. This is not only a
                                         good match with deductive verification rules of program logics [35], but also with formal specification languages
                                         for concurrent programs that have a trace semantics [65,12,27,67,51].
                                             A trace semantics for a given target language, satisfying the requirements sketched above, can be defined in
                                         three phases:
                                          1. Declare local evaluation rules for each syntax construct of the target language.
                                          2. Declare composition rules that combine local evaluation and process creation into global traces. Scheduling
                                             is expressed declaratively as well-formedness constraints over traces.
                                          3. Define the generation of all global traces with the help of the composition rules from a suitable initial
                                             configuration.
2                               C. C. Din et al.

    To achieve the desired degree of modularity, we generalise the standard notion of a program trace [45], i.e.
a sequence of evolving system configurations, starting in some initial state. We make two generalisations. The
first is that local states σ can be abstract. This means the value σ(x) of a memory location x is permitted to be
unspecified. One can think of an abstract value σ(x) as a Skolem constant x0 whose interpretation is determined
by an external context. Alternatively, think of symbolic execution [19,54], where the value of a memory location x
may be a symbolic term x0 representing an unknown value. States containing abstract values are called symbolic,
otherwise they are called concrete.
    Symbolic states allow us to evaluate local code independently of its call context. For example, when evaluating
the semantics of a statement s that receives a message from another process, then the value of that message
cannot possibly be known independently of the call context. In this case, the local evaluation of s can be
expressed in a trace with symbolic states. These symbolic states are concretised when the global context of the
local computations (here, the sender) is resolved, i.e. in the composition rules during phase (2) above. Hence,
the resulting global traces are concrete. Thus, the name of our semantic framework: locally abstract, globally
concrete (LAGC).
    The second generalisation of traces concerns scheduling: concurrency models differ in the exact locations at
which a local computation can be interrupted (aka preempted) and how exactly the computation is continued
afterwards, i.e. which scheduling decision is taken next. To achieve maximum modularity, we do not build
scheduling into a fixed set of rules. Instead, we use continuation markers to specify when scheduling and
preemption is possible.
    As a result, local traces are not merely abstract, but as well contain events used in the composition rules
as interaction points. With the event mechanism, various concurrency models can be defined easily in two
parts: first, ensure that local evaluation rules generate suitable synchronisation events. Second, define a well-
formedness predicate on concrete traces restricting the global traces that can be generated to those reflecting
the targeted concurrency model. Now it is sufficient to add the well-formedness predicate as a premise to each
composition rule. Events turn out to be a flexible and intuitive mechanism, which can be used to express a
range of dependencies between processes beyond synchronous communication (for example, object generation).
    An LAGC-style trace semantics was pioneered for the active object language ABS [27]. Here we show
that, due to its modularity, LAGC semantics constitutes a general semantic framework for a wide range of
concurrent programming models: it is easy to add new syntactic constructs and to accommodate different
concurrency paradigms. We will demonstrate this as follows: starting with a simple WHILE-language, we define
LAGC semantics for an increasingly complex series of languages by successively adding new features, sequential
as well as parallel ones. In the end we cover a representative set of language features and concurrency models
and instantiate our semantic framework to two quite different concurrent programming languages.
    The paper is organised as follows: In Section 2 we set up the formal framework that the LAGC semantics
is based upon. As explained above, we need symbolic states and traces that may contain abstract values for
memory locations. We also need a concretisation operator that instantiates a symbolic trace to match a concrete
context. In addition, we equip traces with states and continuation markers. Section 3 introduces the LAGC
framework along phases (1)–(3) for a WHILE-language. We substantiate the claim made above, that an LAGC
semantics is a good match for deductive verification calculi, by defining in Section 4 a program logic for WHILE
with a concise soundness proof. In Section 5, we gradually extend the semantics to local parallelism (with
atomicity), local memory, and procedure calls. In Section 6, we take the step to multiple processors that send
and receive messages among each other. We show that a wide range of communication patterns can be intuitively
and declaratively characterised via well-formedness, including synchronous and asynchronous communication,
bounded and unbounded FIFO, as well as causality. Section 7 instantiates the LAGC framework to the rather
different concurrency models found in the languages ProMeLa and ABS, respectively. For the latter, we need
to add objects and futures, as well as to change the interleaving semantics, which turns out to be easily possible.
Related work is discussed in Section 8, while Section 9 considers future directions for work and concludes.

2     Basics
2.1   States
We assume given standard basic types, including integers, Booleans and process identifiers, with standard value
domains and associated operators. In addition, we allow starred expressions, representing unknown, symbolic
values.
Definition 1 (Variables, Values, (Starred) Expressions). Let Var be a set of program variables, Val a
set of values, and Op a set of operators, with typical elements x, v, and op, respectively. The sets Val and Op
                                                                                           LAGC Semantics        3

                                   x ∈ Var ::= identifier
                                   v ∈ Val ::= tt | ff | 0 | 1 | ...
                                  op ∈ Op ::= == | < | > | ≤ | ≥ | + | - | * | / | . . .
                                   e ∈ Exp ::= x | v | e op e
                                 se ∈ Sexp ::= e | ∗

                                           Fig. 1: Syntax of expressions.


include the values and operators of the basic types (see Figure 1). The set Exp contains expressions, with typical
element e, obtained from variables, values, and by applying operators to expressions. The set Sexp contains
starred expressions, with typical element se, obtained by extending expressions with an additional symbol ∗.

    We assume that all expressions are well-typed; i.e., in expressions, operators are only applied to subex-
pressions which can be reduced to values of appropriate types. Let op denote an evaluation function for the
operators op defined over the values of the basic types, such that v op v ′ is a value in the basic types. A
Boolean expression is an expression that evaluates to a Boolean value when its arguments are values of the
basic types, and similarly for expressions of other basic types. Overline notation is used for lists of different
syntactic categories; e.g., v and e represent lists of values and expressions, respectively. Let vars(e) denote the
set of variables in an expression e, which has a straightforward inductive definition.
    We now define computation states. Usually, states are mappings from variables to concrete values. To permit
symbolic expressions (i.e., expressions containing variables) occurring as values in states, the starred expression
∗ is used to represent a value for symbolic variables that cannot be further evaluated. The ∗ symbol does not
occur in programs, it is part of the semantic domain.

Definition 2 (Symbolic State, State Update). A symbolic state σ is a partial mapping

                                                   σ : Var → Sexp

from variables to starred expressions. The notation σ[x 7→ se] expresses the update of state σ at x with expression
se:                                                       
                                                            se x = y
                                         σ[x 7→ se](y) =
                                                            σ(y) x 6= y .
    In a symbolic state, a symbolic variable is defined as a variable bound to an unknown value, represented by
the starred expression ∗. Symbolic variables play a different role than ordinary variables: they act as parameters,
relative to which a local computation is evaluated. To distinguish them syntactically, we adopt the convention
of using capital letters for symbolic variables as much as possible. Note that the set of symbolic and non-
symbolic variables are not two distinct categories and a variable that is symbolic can become non-symbolic after
substitution (see Example 2 below).

Definition 3 (Symbolic Variable). Symbolic variables in a state σ are variables mapped to ∗:

                                       symb(σ) = {X ∈ Var | σ(X) = ∗} .

   We will also need the concept of the extension of a state:

Definition 4 (State Extension). We say that a state σ ′ extends a state σ if (i) dom(σ) ⊆ dom(σ ′ ) and (ii) σ(x) = σ ′ (x)
for all x ∈ dom(σ). We overload the subset symbol and write σ ⊆ σ ′ .

Example 1. Consider a state σ0 = [x0 7→ Y0 + w0 , Y0 7→ ∗, w0 7→ 42, x1 7→ Y1 ]. Observe that (1) the expressions
in the range of σ0 can be simplified and (2) there are dangling references, such as Y1 , not in the domain of σ0 .

    The example shows that symbolic states are slightly too general for our purpose, motivating the following
definition, which constrains the variables that may occur in value expressions of states to symbolic variables:

Definition 5 (Well-Formed State). A state σ is well-formed if it fulfils the following condition:

                                   {x ∈ vars(σ(y)) | y ∈ dom(σ)} ⊆ symb(σ) .

   A well-formed state σ is concrete if symb(σ) = {}. For a concrete, well-formed state σ and all x ∈ dom(σ),
there is a value v such that σ(x) = v.
4                                 C. C. Din et al.

Example 2. The state σ0 in Example 1 can be turned into a well-formed state σ1 by simplifying the expression
Y0 + w0 , and binding Y1 to a star, obtaining σ1 = [x0 7→ Y0 + 42, Y0 7→ ∗, w0 7→ 42, x1 7→ Y1 , Y1 7→ ∗]. We have
that σ1 = σ0 [x0 7→ Y0 +42, Y1 7→ ∗] and symb(σ1 ) = {Y0 , Y1 }. Let σ2 = σ1 [Y0 7→ 3, Y1 7→ 2]. After simplification,
σ2 is a concrete, well-formed state that can be written as σ2 = [x0 7→ 45, Y0 7→ 3, w0 7→ 42, x1 7→ 2, Y1 7→ 2].

    Henceforth, all states are assumed to be well-formed. We always assume states to be simplified by propagation
of concrete values, similar to σ2 in Example 2, otherwise non-symbolic variables might occur as values. Symbolic
states, i.e. states with symbolic variables, are close to states in symbolic execution as used in path exploration
[33], but simplified and with an additional restriction (Definition 11 below).

2.2     Evaluation
The evaluation of expressions in the context of a symbolic state reduces known variables to their values and
keeps the symbolic variables inside the expression, reducing an expression as much as currently possible. The
evaluation function is defined as follows:

Definition 6 (Evaluation Function). Let σ be a symbolic state. The evaluation function valσ : Exp → Exp
for expressions in the context of σ is defined inductively:
                                     
                                       x      if σ(x) = ∗
                         valσ (x) =
                                       σ(x) otherwise
                         valσ (v) = v
                                       valσ (e1 ) op valσ (e2 ) if valσ (e1 ) ∈ Val and valσ (e2 ) ∈ Val
                                     
                  valσ (e1 op e2 ) =
                                       valσ (e1 ) op valσ (e2 ) otherwise

      In the following we will ensure that vars(e) ⊆ dom(σ) holds, such that valσ is a total function.

Example 3. Using state σ1 of Example 2, we evaluate valσ1 (x0 + Y0 + Y1 ) = (Y0 + 42) + Y0 + Y1 .

   Let valσ (e) denote the element-wise application of the evaluation function to all expressions in the list e,
and likewise for sets.

2.3     Traces and Events
Traces are sequences over states and structured events. The presence of events makes it easy to ensure global
properties of traces via well-formedness conditions over events. Since states may be symbolic, traces will be
symbolic as well and it is necessary to constrain traces by symbolic path conditions. We start with a general
definition of events. Their specific structure will be added later.

Definition 7 (Event Marker). Let ev(e) be an event marker over expressions e.

Definition 8 (Path Condition). A path condition pc is a finite set of Boolean expressions. If pc contains no
variables, then we can assume it to be fully evaluated; i.e. it is either ∅, {ff, tt}, {ff}, or {tt}. A fully evaluated
path condition is consistent if and only if it does not contain ff.

      For any concrete state σ, valσ (pc) is a path condition with no variables that can be fully evaluated.

Definition 9 (Conditioned Symbolic Trace). A symbolic trace τ is defined co-inductively by the following
rules (ε denotes the empty trace):
                                        τ ::= ε | τ y t
                                        t ::= σ | ev(e)
A conditioned symbolic trace has the form pc ⊲ τ , where pc is a path condition and τ is a symbolic trace. If pc
is consistent, we simply write τ for pc ⊲ τ .

   Traces can be finite or infinite. For simplicity, let hσi denote the singleton trace ε y σ. Concatenation of
two traces τ1 , τ2 is written as τ1 · τ2 and only defined when τ1 is finite. The final state of a non-empty, finite
trace τ is selected with last(τ ), the first state of a non-empty trace τ with first(τ ).

Example 4. Continuing Example 2, we define a conditioned symbolic trace pc0 ⊲ τ0 = {Y0 > Y1 } ⊲ hσ1 i y
σ1 [x0 7→ 17].
                                                                                                LAGC Semantics     5

Sequential Composition It is important that traces can semantically model the sequential composition of program
statements. Assume that τ1 is a trace of a statement r and τ2 a trace of another statement s. To obtain the
trace corresponding to the sequential composition of r and s, the traces corresponding to r and s should be
concatenated, but the last state of the first trace and the first state of the second trace are generally identical.
We generalize such a concatenation in case the states are not exactly the same: to concatenate two traces τ1
and τ2 the first state of τ2 should be an extension of the last state of τ1 , but the resulting trace should only
contain the largest of the two states. This motivates the semantic chop ∗∗ on traces (following [60], who in turn
were inspired by interval temporal logic [36]):
Definition 10 (Chop on Traces). Let pc1 , pc2 be path conditions and τ1 , τ2 be symbolic traces, and assume
that τ1 is a non-empty, finite trace. The semantic chop (pc1 ⊲ τ1 ) ∗∗ (pc2 ⊲ τ2 ) is defined as follows:

           (pc1 ⊲ τ1 ) ∗∗ (pc2 ⊲ τ2 ) = (pc1 ∪ pc2 ) ⊲ τ · τ2 where τ1 = τ y σ, τ2 = hσ ′ i · τ ′ and σ ⊆ σ ′ .

    For infinite and empty traces τ1 , the chop operator is undefined. Whenever the final state of the first trace
cannot be extended to the first state of the second trace, the operator is undefined.
    The definition can be specialised to traces without path conditions in the obvious way: τ1 ∗∗ τ2 is (∅ ⊲ τ1 ) ∗∗
(∅ ⊲ τ2 ).

Traces with Events. Events will be uniquely associated with the state in a trace at which they occurred. The
events do not update the values in a state, but they may extend a state with fresh symbolic variables. To this
aim, an event ev(e) is inserted into a trace after a state σ and the state is then augmented by a set V of symbolic
variables. The notation we use for this operation is an event trace evVσ (e) of length three:

                            evVσ (e) = hσi y ev(valσ′ (e)) y σ ′ where σ ′ = σ[V 7→ ∗].

Given a trace of the form τ1 y σ and event ev(e), appending the event is achieved by the trace τ1 · evVσ (e).
The preceding definition ensures that events in traces are “choppable”; τ ∗∗ evVσ (e) is well-defined whenever
last(τ ) = σ. If V is empty then the state is unchanged, in this case we omit the set of symbolic variables:

                                                    evσ (e) = ev∅σ (e)

Example 5. Event traces can be inserted at the middle of a trace. To insert an event ev(Y0 ) that does not intro-
duce symbolic variables at σ1 to trace τ0 in Example 4, we use the event trace evσ1 (Y0 ) = hσ1 i y ev(valσ1 (Y0 )) y
σ1 = hσ1 i y ev(Y0 ) y σ1 . This results in the trace: τ2 = {Y0 > Y1 } ⊲ hσ1 i y ev(Y0 ) y σ1 y σ1 [x0 7→ 17]. To
                                                                                                  {Y }
insert an event ev(Y2 ) that introduces the symbolic variable Y2 , we use the event trace evσ1 2 (Y2 ) = hσ1 i y
ev(Y2 ) y σ1 [Y2 7→ ∗]. The trace in Example 4 results in the trace:

                    τ2′ = {Y0 > Y1 } ⊲ hσ1 i y ev(Y2 ) y σ1 [Y2 7→ ∗] y σ1 [Y2 7→ ∗, x0 7→ 17].

Well-Formed Traces. Similar to the values of well-formed states, the expressions in events and path conditions
of a well-formed trace should only contain symbolic variables. This requires all states in a trace to agree upon
which variables are symbolic. We also impose an additional well-formedness condition on events: any event
occurring in a trace must be immediately preceded and followed by the same state σ; i.e., it can be obtained
by inserting an event trace at σ. This implies that a trace always starts and ends with a state, never with an
event. Well-Formed traces are formalised as follows:
                                                                                                  S
Definition 11 (Well-Formed Trace). Let pc ⊲ τ be a conditioned symbolic trace and let V = σ∈τ symb(σ).
The trace pc ⊲ τ is well-formed if the following conditions hold:

                                               ∀σ ∈ τ. σ is well-formed                                           (1)
                                        ∀σ ∈ τ. (dom(σ) \ symb(σ)) ∩ V = ∅                                        (2)
                                                   vars(pc) ⊆ V                                                   (3)
                                               ∀ev(e) ∈ τ. vars(e) ⊆ V                                            (4)
                     ∀ev(e), τ1 , τ2 . (τ = τ1 y ev(e) · τ2 =⇒ ∃σ. last(τ1 ) = σ ∧ first(τ2 ) = σ)                (5)

   Equation (2) states that a variable that is symbolic in a state cannot be non-symbolic in another state of the
trace. Equations (3)–(4) ensure that any variable to occur in a path condition or event is a symbolic variable
from some state. Equation (5) guarantees that any event in a trace is surrounded by identical states.
6                                C. C. Din et al.

Example 6. The traces τ2 and τ2′ in Example 5 have well-formed states. Only symbolic variables occur in path
conditions and events, and the events were added by inserting event traces. Hence, they are well-formed.

Definition 12 (Concrete Traces). A concrete trace is a well-formed trace containing only concrete states
and events, as well as a fully evaluated, consistent path condition. We use sh for concrete traces, where the
letters stand for “shining” trace.

Example 7. Let σ3 = [x0 7→ 45, Y0 7→ 3, w0 7→ 42, x1 7→ 2, Y1 7→ 2], then a concrete trace of length two is
τ3 = hσ3 i y σ3 [x0 7→ 17]. The path condition Y0 > Y1 is evaluated to 3 > 2 = tt in σ3 and thus consistent.

   Observe that τ3 can be obtained from τ0 in Example 4 by a suitable instantiation of its symbolic variables.
The precise definition of this operation is the purpose of the following subsection.


2.4     Concretisation

A concretisation mapping is defined relative to a state. It associates a concrete value to each symbolic variable
of the state.

Definition 13 (State Concretisation Mapping). A mapping ρ : Var → Val is a concretisation mapping
for a state σ if dom(ρ) ∩ dom(σ) = symb(σ).

      A concretisation mapping ρ may additionally define the value of variables that are not in the domain of σ.

Example 8. Consider σ1 of Example 2 where symb(σ1 ) = {Y0 , Y1 }. We define the concretisation mapping
ρ1 = [Y0 7→ 3, Y1 7→ 2] for σ1 .
   Let σ4 = [X 7→ ∗, z 7→ 3]. Then a concretisation mapping must give a value to X, but not to z, for example,
ρ2 = [X 7→ 2, Y 7→ 0] is a concretisation mapping for σ4 .

  A symbolic state can be concretised using the values assigned to its symbolic variables in a concretisation
mapping to evaluate the symbolic expressions.

Definition 14 (State Concretisation). Let σ be a state and ρ a concretisation mapping for σ. The concreti-
sation of σ with ρ is defined as follows:

                              ρ • σ = ρ ∪ {x 7→ valρ (σ(x)) | x ∈ dom(σ) \ dom(ρ)} .

Example 9. Continuing Examples 7 and 8, we obtain ρ1 • σ1 = σ3 .

    To concretise a symbolic trace pc ⊲ τ , we must apply a concretisation mapping ρ to all states and events
of the trace. This means the domain of ρ must comprise all symbolic variables that occur in the trace. This
is the case for well-formed traces, whose states must agree on which variables are symbolic (equation (2) in
Definition 11).

Definition 15 (Trace Concretisation Mapping). A mapping ρ is a trace concretisation mapping for τ if
it is a concretisation mapping for all the states in τ . We say that ρ concretises τ .

Definition 16 (Symbolic Trace Concretisation). Let pc ⊲ τ be a well-formed trace and ρ a concretisation
mapping for τ . The concretisation ρ(pc ⊲ τ ) of pc ⊲ τ is obtained as ρ(pc) ⊲ ρ(τ ), where ρ(pc) = valρ (pc) and ρ(τ )
is defined as follows:
                                       ρ(t1 · · · tn · · · ) = ρ(t1 ) · · · ρ(tn ) · · ·
                                                    ρ(σ) = ρ • σ
                                               ρ(ev(e)) = ev(valρ (e))

Proposition 1. The concretisation of a state is a concrete state. The concretisation of a well-formed trace is
a concrete, well-formed trace. Any concrete state or trace is a concretisation of itself.

Example 10. We continue to use the symbolic trace pc0 ⊲ τ0 of Example 4 and concretise it with the mapping
ρ1 of Example 8. The resulting concrete trace is τ3 from Example 7 with path condition {tt}.
                                                                                               LAGC Semantics        7

                              s ∈ Stmt ::= skip | x := e | if e { s } | s; s | while e { s }

                                    Fig. 2: The syntax for statements in WHILE.


2.5    Continuations

To capture the local semantics of a language, below we define an evaluation function valσ (s) that evaluates a
single statement s in a—possibly symbolic—state σ to a set of conditioned, symbolic traces. Compositional local
evaluation rules can then be defined for each statement by adding a continuation marker at the end. Continuation
markers are needed, if s is a composite statement that requires separate evaluation of its constituent parts. In
particular, s might not terminate, but this should not jeopardise parallel computations when computing a
sequential trace for a global system. We avoid this issue by stopping the evaluation after a finite number of
steps by means of a continuation marker, defined as follows:

Definition 17 (Continuation Marker). Let s be a program statement. The continuation marker K(s) ex-
presses that a given trace is extended by the traces resulting from computing s. The empty continuation, denoted
K( ), expresses that nothing remains to be computed.6

    The argument to the continuation marker is the code on which evaluation is continued. When atomic
statements are evaluated, there is no continuation code but only a return of control. In this case, we end the
trace with an empty continuation (see Section 3.1). Local evaluation (corresponding to phase (1) in Section 1)
is defined below such that for each statement s and symbolic state σ the result of valσ (s) is a set of conditioned,
symbolic traces of the form pc ⊲ τ · K(s′ ) where τ is a finite trace. These traces are called continuation traces;
we denote by CTr the type of continuation traces.


3     LAGC Semantics of WHILE

We define a LAGC semantics for WHILE, a language with basic sequential constructs that can be seen as a kernel
of imperative programming languages [9]. The statements of WHILE consist of skip, assignment, conditional,
sequential composition, and while-loops. The syntax for statements is given in Figure 2, where we assume given
standard expressions e. Assignment binds the value of an expression to a variable. Conditionals and while-loops
depend on the value of a Boolean expression e. We assume the standard semantics of this language to be known,
and use it to illustrate our trace semantics. Local rules (phase (1)) unfold the traces until the next possible
scheduling point, marked by a continuation. Composition rules (phase (2)) select the next trace to be unfolded
at the scheduling point; for the sequential language, there is only one trace so the latter selection is deterministic.
Due to its simplicity, WHILE merely needs state-based traces, the use of events is covered in Section 5.4.


3.1    Local Evaluation

Local evaluation rules a single statement in the context of a symbolic state, and return a set of finite continuation
traces. Each evaluation rule represents the execution of a single statement, producing a set of continuations
traces. The evaluation rules are reminiscent of small-step reduction rules, but work in a denotational setting
and with a symbolic context. We overload the symbol valσ and declare it with the type valσ : Stmt → 2CTr .
   The rule for skip generates an empty path condition, returns the state it was called in, and continues with
the empty continuation. The result is a set containing one singleton trace:

                                           valσ (skip) = {∅ ⊲ hσi · K( )} .                                        (6)

   The assignment rule generates an empty path condition and a trace from the current state σ to a state which
updates σ at x, and continues with an empty continuation. The result is one trace of length two:

                                 valσ (x := e) = {∅ ⊲ hσi y σ[x 7→ valσ (e)] · K( )} .                             (7)

    The rule for the conditional statement branches on the value of the condition, resulting in two traces with
different path conditions. The first trace is obtained from the current state and the continuation with the
6
    The mnemonics of the symbol is that from an empty bottle nothing can be consumed.
8                                 C. C. Din et al.

statements in the if-branch, and the second trace has the empty continuation (corresponding to the empty
else-branch):
                 valσ (if e { s }) = {{ valσ (e) = tt} ⊲ hσi · K(s), {valσ (e) = ff} ⊲ hσi · K( ) } . (8)
    The semantics of while is similar to the semantics for the conditional statement. This gives us the opportu-
nity to illustrate that the semantics of a statement can easily be expressed in terms of the semantics of another
statement, without having to expose intermediate states:
                               valσ (while e { s }) = valσ (if e { s; while e { s }}) .                           (9)
   The rule for sequential composition r; s is obtained by first evaluating r to traces of the form pc ⊲ τ · K(r′ )
with continuation r′ . The statement s can simply be added to this continuation:
                              valσ (r; s) = {pc ⊲ τ · K(r′ ; s) | pc ⊲ τ · K(r′ ) ∈ valσ (r)} .                  (10)
    A subtle point concerns the propagation of empty continuations: r′ might be the empty continuation ,
which should be ignored. This behavior is captured in the following rewrite rule, which is exhaustively applied
to statements occurring inside continuations:
                                                     s; s′   s′ if s = .
   This rewrite rule reflects that the empty continuation is an identity element for sequential composition.
Similar rewrite rules will be added to handle identity elements for other composition operators in the sequel.
Example 11. Consider the sequential statement sseq = (x := 1; y := x + 1). To explain how its evaluation is
performed, we start from an arbitrary symbolic state σ (to be instantiated later by a composition rule). The
equation for sequential composition yields
                                 valσ (sseq ) = {∅ ⊲ hσi y σ[x 7→ 1] · K(y := x + 1)} .                          (11)
To perform this evaluation, we need the result of evaluating the first assignment in the context of σ:
                                    valσ (x := 1) = {∅ ⊲ hσi y σ[x 7→ 1] · K( )} .
    In the composition rules it might be necessary to evaluate the empty continuation, so we must define it. It
is simply the empty set of traces:
                                                 valσ ( ) = {} .                                          (12)
Proposition 2. Given a concrete state σ and a program s such that vars(s) ⊆ dom(σ), then valσ (s) is a set of
concrete continuation traces of the form pc ⊲ τ · K(s′ ). There is exactly one continuation trace with a consistent
path condition.

3.2    Trace Composition
Local traces are composed into concrete global ones. As WHILE is sequential and deterministic, we expect to
obtain exactly one trace, provided that the execution starts in a concrete state that assigns values to all the
variables of a program. Proposition 2 ensures that all local evaluation rules produce concrete traces in this case.
   The task of the composition rule for WHILE-programs is to repeatedly evaluate one statement at a time in a
concrete state until the next continuation, then stitch the resulting concrete traces together. Given a concrete
trace sh with final state σ and a continuation K(s), we evaluate s starting in σ. The result is a set of conditioned
traces from which one trace with a consistent path condition and a trailing continuation K(s′ ) is chosen.7 The
chosen trace τ is chopped with the given trace sh. Afterwards, the composition rule can be applied again to the
extended concrete trace and K(s′ ).
                                σ = last(sh) pc ⊲ τ · K(s′ ) ∈ valσ (s)        pc consistent
                                                                                                                 (13)
                                                                           ′
                                                sh, K(s) → sh ∗∗ τ, K(s )
     The rule assumes that s is evaluated to a concrete trace so that sh∗∗τ stays concrete. At this stage, symbolic
traces do not yet figure. This works as long as Proposition 2 ensures that pc ⊲ τ is a concrete trace, however, in
general the proviso vars(s) ⊆ dom(σ) does not hold. There are several approaches to address this. For example,
it is sufficient to consider the non-initialised variables of s, instead of all of them. We avoid a lengthy definition
to address this technicality by simply assuming that last(sh) defines all variables of s. This can be easily achieved
by initialising all variables to default values at program start, as done below.
7
    For a deterministic language like WHILE, there is exactly one trace, but the rule is designed to work for the non-
    deterministic extension below as well.
                                                                                                 LAGC Semantics        9

3.3     Global Trace Semantics
                ∗
Let sh, K(s) → sh′ , K(s′ ) denote the transitive closure of applying rule (13), expressing that sh′ , K(s′ ) can be
reached from sh, K(s) in zero or more steps.

Definition 18 (Program Semantics). Given a program s and a state σ, let

                                             sh0 , K(s0 ) → sh1 , K(s1 ) → · · ·

be a maximal sequence obtained by the repeated application of rule (13), starting from hσi, K(s). If the sequence
is finite, then it must have the form8
                                                      ∗
                                            hσi, K(s) → sh, K( ) .

If the sequence is infinite, let sh = limi→∞ shi . The set of all such traces sh for a program s starting from a
state σ is denoted Tr(s, σ).

   For any statement s, let Is be the state, where [x 7→ 0] for all x ∈ vars(s) (for simplicity, assume all variables
are of integer type—the generalisation is obvious). To help readability, we sometimes omit such default values
from the states in the following examples.

Example 12. We apply rule (13) to hIseq i, K(sseq ), the program from Example 11. To obtain the premise, we
instantiate equation (11) with σ = Iseq .

                                             Iseq = last(hIseq i)   ∅ consistent
                        ∅ ⊲ hIseq i y Iseq [x 7→ 1] · K(y := x + 1) ∈ valIseq (x := 1; y := x + 1)                  (14)
                         hIseq i, K(x := 1; y := x + 1) → hIseq i y Iseq [x 7→ 1], K(y := x + 1)

  For the subsequent rule application, it is necessary to evaluate the program y := x + 1 in the continuation.
Again, we do this for a general state, while in the rule we use σ = Iseq [x 7→ 1] (from now on we omit Iseq ):

                               valσ (y := x + 1) = {∅ ⊲ hσi y σ[y 7→ valσ (x + 1)] · K( )}


                                    [x 7→ 1] = last(hIseq i y [x 7→ 1])     ∅ consistent
                      ∅ ⊲ h[x 7→ 1]i y [x 7→ 1][y 7→ val[x7→1] (x + 1)] · K( ) ∈ val[x7→1] (y := x + 1)             (15)
                     hIseq i y [x 7→ 1], K(y := x + 1) → hIseq i y [x 7→ 1] y [x 7→ 1, y 7→ 2], K( )

      Hence, Tr(x:=1; y:=x+1, Iseq ) = {hIseq i y [x 7→ 1] y [x 7→ 1, y 7→ 2]}.


3.4     Discussion

As mentioned, as long as we start semantic evaluation in a sufficiently initialised concrete state, Proposition 2
ensures that only concrete traces will be generated by local rules. Consequently, we have a semantics that can
be aptly called modular and compositional (exactly one independent rule per language construct and a uniform
composition rule), but the overhead introduced with symbolic traces is not yet justified.
   The advantages offered by symbolic traces and states are realised in the following two sections. In Section 4
we define a program logic for WHILE that employs symbolic traces at the level of the calculus. This close
correspondence between semantics and deduction system is the basis for an intuitive soundness proof for the
deductive system.
   In Sections 5–7 we extend WHILE with a number of complex instructions, in particular, for parallel pro-
gramming. It will be seen that a wide range of concurrency paradigms fit naturally into the LAGC semantic
framework.
8
    Observe that sh, K( ) is the end of the execution because the evaluation of K( ) returns {} such that the composition
    rule (13) is no longer applicable. The empty continuation is obtained once the whole program has been evaluated.
10                                  C. C. Din et al.

4     A Program Logic and Sound Calculus for WHILE
We provide a dynamic logic (DL) [37] as well as a calculus for reasoning about the correctness of WHILE-programs
that is sound relative to our semantics. In deductive verification dynamic logic [11,4] offers technical advantages
over Hoare logic [42]: it is syntactically closed with respect to first-order logic, more expressive, and cleanly
separates first-order (“logical”) from program variables [4, p. 50]. Below we define program formulas of the form
ψ → τ [s] φ, where τ is a finite symbolic trace, s any WHILE-statement, ψ a first-order formula, and φ a formula
that in turn may contain programs. The intuitive meaning is that any terminating execution of s continuing a
trace that concretises τ and started in a state that satisfies ψ, must end in a state that satisfies φ. The modality
[s] corresponds to a continuation in the semantics of WHILE, represented symbolically.
     The unusual aspect of this setup is the presence of a symbolic trace τ inside a formula. It aligns with our
locally abstract semantics, but it is also justified, because—unlike a semantics—rule schemata in calculus rules
necessarily deal with symbolic values: a verification calculus aims at proving a property that holds for all inputs
of a program, not merely for a single run. Nevertheless, the presence of symbolic traces inside formulas may
appear as insufficiently syntactic or as an inappropriate intrusion of the semantics into the calculus. However,
efficient syntactic representations of symbolic assignments are fairly common and well understood: for example,
the deductive verification system KeY uses symbolic updates 9 [4] and in the B-method explicit generalised
substitutions play a comparable role [1]. To keep the calculus as general as possible, we do not commit to a
particular implementation of symbolic traces.
     The calculus rules given below will symbolically execute a program s in a sequent of the form ψ → τ [s] φ
and produce verification conditions of the form Γ ⇒ τ φ, where φ is a first-order formula and τ a symbolic trace.

4.1   Dynamic Logic
Given a signature Σ with typed function and predicate symbols and a set V of logical variables which is
disjoint from the symbols in Σ, let Terms(Σ, V ) denote the well-formed terms over Σ and V (respecting type
compatibility). Note that the logical variables in V are disjoint from program variables Var. Unlike the latter,
the logical variables can be bound by quantifiers and do not change their value during program execution.
Definition 19 (DL Formula). Let Σ be a signature and V a set of logical variables disjoint from Σ. The
language DL(Σ, V ) of formulas in dynamic logic is defined inductively as follows:
 1. B ∈ DL(Σ, V ) if B ∈ Terms(Σ, V ) and the type of B is Boolean
 2. ¬φ1 , φ1 ∧ φ2 , φ1 ∨ φ2 , φ1 → φ2 , φ1 ↔ φ2 ∈ DL(Σ, V ) if φ1 , φ2 ∈ DL(Σ, V )
 3. ∃x · φ, ∀x · φ ∈ DL(Σ, V ) if x ∈ V and φ ∈ DL(Σ, V )
 4. [s] φ ∈ DL(Σ, V ) if s is a, possibly empty, WHILE-program and φ ∈ DL(Σ, V )
We often omit the signature and variable set of φ ∈ DL(Σ, V ) and simply write φ ∈ DL.
   There is a subtle point about empty programs. As explained above, the program s in the modality can
be viewed as the continuation of the current trace. The rules of the calculus defined below will symbolically
execute s from left to right, until the program remaining to be executed is empty. For this reason, we allow
empty programs, denoted ◦, in clause (4). The empty program is the identity element for the composition
operators (i.e., ◦; s = s; ◦ = s). However, the continuation with the empty program is not the same as the empty
continuation; it requires a semantics that amounts to an empty trace, which is reflected in Definition 21 below.
Definition 20 (Substitution). Given a language DL(Σ, V ) and a set of logical variables V ′ = {x1 , . . . , xn }
such that V ′ ⊆ V , a substitution [x1 /t1 , . . . , xn /tn ] is a function V ′ → Terms(Σ, V ) which associates with
every xi ∈ V ′ a type-compatible term ti ∈ Terms(Σ, V ).
    Denote by φ[x1 /t1 , . . . , xn /tn ] the application of a substitution [x1 /t1 , . . . , xn /tn ] to a logical formula φ ∈
DL(Σ, V ). Observe that applying a substitution removes occurrences of logical variables in a formula and
does not affect programs. The application of the substitution has a straightforward inductive definition over φ
(omitted here).
    We write τ |= φ and σ |= φ to denote10 that a formula φ is valid for a concrete trace τ and in a concrete
state σ, respectively (equivalently, τ and σ satisfy φ). Formally, satisfiability can be defined as follows:
9
   Updates can be viewed as a syntactic, efficient, lazy representation of symbolic traces: concrete values are not eagerly
   substituted and assignments are kept in single static (SSA) shape.
10
   To simplify presentation, we assume a fixed standard interpretation of the symbols in Σ. It is straightforward to
   accommodate undefined symbols and relativise satisfiability to first-order models.
                                                                                                 LAGC Semantics   11

                                                                             (Cond)
                                     (Assign)
                               ′                                           last(τ ) = σ
                               σ = σ[x 7→ valσ (e)]
                                                                Γ, pc ∪ {valσ (e) = ff} ⇒ τ [s’] φ
                      last(τ ) = σ     Γ, pc ⇒ τ y σ ′ [s] φ
                                                               Γ, pc ∪ {valσ (e) = tt} ⇒ τ [s; s’] φ
                               Γ, pc ⇒ τ [x:=e; s] φ
                                                                   Γ, pc ⇒ τ [if e { s }; s’] φ

                        (skip)                             (While)                            (Empty)
                    Γ, pc ⇒ τ [s] φ       Γ, pc ⇒ τ [if e { s; while e { s } }; s’] φ       Γ, pc ⇒ τ φ
                Γ, pc ⇒ τ [skip; s] φ           Γ, pc ⇒ τ [while e { s }; s’] φ            Γ, pc ⇒ τ [◦] φ

                                   Fig. 3: Dynamic logic sequent rules for WHILE.


Definition 21 (Satisfiability of DL Formulas). Let φ ∈ DL(Σ, V ) be a DL formula, B ∈ Terms(Σ, V ) a
Boolean term, σ a concrete state and τ a concrete trace.

       σ |= B ⇐⇒ valσ (B) = tt
       σ |= ¬φ ⇐⇒ σ 6|= φ
       σ |= φ1 ∧ φ2 ⇐⇒ σ |= φ1 and σ |= φ2 (analogous for the remaining propositional connectives)
       σ |= ∃x · φ ⇐⇒ σ |= φ[x/t] for some substitution [x/t] where t ∈ Terms(Σ, V ), variable-free
       σ |= ∀x · φ ⇐⇒ σ |= φ[x/t] for all substitutions [x/t] where t ∈ Terms(Σ, V ), variable-free
       σ |= [s] φ ⇐⇒ τ |= φ for all finite τ ∈ Tr(s, σ)
       σ |= [◦] φ ⇐⇒ σ |= φ
       τ |= φ ⇐⇒ τ finite, non-empty, last(τ ) = σ, and σ |= φ

Observe that the third but last clause implies a partial correctness semantics.

4.2   Calculus
As usual in deductive verification [35], we define a calculus operating on sequents. These have the form Γ ⇒ τ φ,
where Γ is a set of formulas thought to be implicitly conjoined (called the antecedent ), the symbol ⇒ can be
read as implication, τ is a non-empty, finite symbolic trace, and φ is a DL formula. Without loss of generality,
we can assume that Γ consists of a single formula ψ.

Definition 22 (Valid Sequent). A sequent is valid, denoted |= ψ ⇒ τ φ, iff for all concretisation mappings
ρ such that first(ρ(τ )) |= ψ, we have that
                                            last(ρ(τ )) |= φ .

    To make the correspondence with the semantics of WHILE more immediate, we represent path conditions as
a separate set in the antecedent of the sequents. The rules for programs are shown in Figure 3. Observe that
this rule set is incomplete as it leaves open how a sequent of the form Γ, pc ⇒ τ φ should be derived, where
φ is a first-order formula. For generality, we do not commit to a specific representation of symbolic traces and
how they are applied to first-order formulas. For example, if symbolic traces are represented with updates as
in KeY, then the rules in [4, Ch. 2] can be used. In the soundness proof below we assume that there is a sound
calculus able to derive Γ, pc ⇒ τ φ.
    We denote by ⊢ ψ ⇒ τ [s] φ that the DL sequent ψ ⇒ τ [s] φ can be derived in the proof system. To prove
that a postcondition Post holds after termination of program s under a precondition Pre, it is sufficient to derive
the sequent
                                               Pre ⇒ hσ∗ i [s] Post ,
where σ∗ (x) 7→ ∗ for all x ∈ Var. By construction, the only symbolic variables that occur in a well-formed
symbolic trace τ are introduced in the initial state of τ . Thus, all path conditions are expressed in terms of the
initial symbolic state σ∗ .

Theorem 1 (Soundness). Let τ be a well-formed symbolic trace and let φ, ψ be DL formulas. If ⊢ ψ ⇒ τ φ,
then |= ψ ⇒ τ φ.

Proof. The proof is by induction over the structure of φ. We assume the soundness of first-order (or “program-
free”) formulas; i.e., if ⊢ B then |= B for B ∈ Terms(Σ, V ).
Case Empty. Assume ⊢ ψ ⇒ τ [◦] φ. By rule (Empty), we get ⊢ ψ ⇒ τ φ.
12                                 C. C. Din et al.

   For the base case, we may assume that φ is a first-order formula. Then, by assumption, |= ψ ⇒ τ φ,
which means that for any concretisation mapping ρ, if first(ρ(τ )) |= ψ, then last(ρ(τ )) |= φ. The latter is, by
Definition 21, equivalent to last(ρ(τ )) |= [◦] φ. Since ρ was arbitrary, this yields |= ψ ⇒ τ [◦] φ.
   For the inductive case, we may assume that φ is any DL formula. Then, |= ψ ⇒ τ φ follows from the induction
hypothesis (hereafter, IH), and the rest of the proof is analogous to the base case.
Case Skip. Assume ⊢ ψ ⇒ τ [skip; s] φ. By rule (Skip), we get ⊢ ψ ⇒ τ [s] φ, and by IH we have |= ψ ⇒ τ [s] φ.
Hence, for any concretisation mapping ρ, if first(ρ(τ )) |= ψ, then last(ρ(τ )) |= [s] φ. Then τ ′ |= [◦] φ for all
τ ′ ∈ Tr(s, last(ρ(τ ))). By equations (13), (10) and (6), we have Tr(s, σ) = Tr(skip; s, σ) for any σ. Therefore,
for all τ ′′ ∈ Tr(skip; s, last(ρ(τ ))) we have τ ′′ |= [◦] φ, and it follows that |= ψ ⇒ τ [skip; s] φ.
Case Assign. Assume ⊢ ψ ⇒ τ [x:=e; s] φ. By rule (Assign), we get ⊢ ψ ⇒ τ y σ ′ [s] φ where last(τ ) = σ
and σ ′ = σ[x 7→ valσ (e)]. By IH we have |= ψ ⇒ τ y σ ′ [s] φ. Hence, for any concretisation mapping ρ, if
first(ρ(τ y σ ′ )) |= ψ, then last(ρ(τ y σ ′ )) |= [s] φ, i.e. ρ(σ ′ ) |= [s] φ. By equations (13), (10) and (7), we have
Tr(x:=e; s, σ) = {hσi y σ ′ ∗∗ τ ′ | τ ′ ∈ Tr(s, σ ′ )}. Therefore, last(ρ(τ )) |= [x:=e; s] φ and, since ρ was arbitrary
and first(ρ(τ y σ ′ )) = first(ρ(τ )), we have |= ψ ⇒ τ [x:=e; s] φ.
Case Cond. Assume ⊢ ψ ⇒ τ [if e {s’}; s] φ. By rule (Cond), we get ⊢ ψ, valσ (e) = ff ⇒ τ [s] φ and
⊢ ψ, valσ (e) = tt ⇒ τ [s’; s] φ, where last(τ ) = σ. Correspondingly, we have two induction hypotheses: |=
ψ, valσ (e) = ff ⇒ τ [s] φ (hereafter, IH1) and |= ψ, valσ (e) = tt ⇒ τ [s’; s] φ (hereafter, IH2). Let ρ be any
concretisation mapping and assume first(ρ(τ )) |= ψ. Depending on the value of valρ(σ) (e), exactly one of the
subcases applies.
    Subcase IH1. We can assume valρ(σ) (e) = ff and, by IH1, |= ψ, valσ (e) = ff ⇒ τ [s] φ, which together gives
last(ρ(τ )) |= [s] φ. By definition, τ ′ |= [s] φ for all τ ′ ∈ Tr(s, last(ρ(τ ))). By Equations (13), (10) and (8), we have
Tr(s, σ) = Tr(if e {s’}; s, σ), observing that the path condition is consistent. Therefore, τ ′ |= [if e {s’}; s] φ for
all τ ′ ∈ Tr(if e {s’}; s, last(ρ(τ ))) and so |= ψ ⇒ τ [if e {s’}; s] φ.
   Subcase IH2. We can assume valρ(σ) (e) = tt and proceed by a completely analogous argument as in the
other subcase.
Case While. Follows directly from the case for Cond.


5     Semantics for a Shared-Variable Parallel Programming Language

In this and the following section we show that the LAGC semantics naturally extends to cover advanced language
constructs. We gradually extend WHILE with parallel programming constructs: parallel execution, procedure
calls, distributed memory, dynamic process creation, and communication between procedures. To cater for
interleaved execution of parallel instructions, and to allow for the compositional definition of semantics, the
traces of the sequential language are gradually unfolded by means of continuations.


5.1   Local Parallelism

We extend WHILE with a statement for parallel execution, such that the syntax for statements from Figure 2
becomes:
                                    s ∈ Stmt ::= co s || s oc | . . . .
The semantics of this statement consists in interleaving the evaluation of the two parallel branches at the
granularity of atomic statements, as exemplified below.

Example 13. The execution of the program sco = co x := 1; y := x + 1 || x := 2 oc produces one of three
possible traces that correspond to the traces of the following sequential programs: x := 1; y := x + 1; x := 2,
or x := 1; x := 2; y := x + 1, or x := 2; x := 1; y := x + 1.


Local Evaluation The evaluation rule for the parallel execution statement co r || s oc branches on the
statement which first gets to execute, resulting in two sets of traces where the first set contains traces with the
path condition of r and the continuation of r in parallel with s and the second set contains traces with the path
condition of s and the continuation of s in parallel with r. The valuation rule is formalised as follows:

                     valσ (co r || s oc) = {pcr ⊲τr · K(co r′ || s oc) | pcr ⊲τr · K(r′ ) ∈ valσ (r)}
                                                                                                                       (16)
                                           ∪{pcs ⊲τs · K(co r || s′ oc) | pcs ⊲τs · K(s′ ) ∈ valσ (s)} .
                                                                                              LAGC Semantics      13

As with sequential composition in rule (10), we need to ensure that empty continuations are not propagated.
To this end we define the following rewrite rule for parallel composition inside continuations (observe that the
case s = s′ = cannot occur):                           ′
                                              ′         s if s = , s′ 6=
                                     co s || s oc                                                           (17)
                                                         s if s 6= , s′ = .

Trace Composition The composition rule (13) can be kept unchanged (although the abstract variant in
rule (23) below can be used as well). Its effect is that all combinations of execution sequences of atomic statements
in the parallel branches can be generated. This behaviour corresponds to the classical interleaving semantics
(e.g., [8]), as demonstrated below.
Example 14. Consider program sco from Example 13, its evaluation is

                       valσ (sco ) = {∅ ⊲ hσi y σ[x 7→ 1] · K(co y := x + 1 || x := 2 oc)}∪
                                     {∅ ⊲ hσi y σ[x 7→ 2] · K(co x := 1; y := x + 1 || oc)}
                                   = {∅ ⊲ hσi y σ[x 7→ 1] · K(co y := x + 1 || x := 2 oc)}∪
                                     {∅ ⊲ hσi y σ[x 7→ 2] · K(x := 1; y := x + 1)} ,

using the following sub-evaluations: valσ (x := 1; y := x + 1) = {∅ ⊲ hσi y σ[x 7→ 1] · K(y := x + 1)} and
valσ (x := 2) = {∅ ⊲ hσi y σ[x 7→ 2] · K( )}. For trace composition, we first need to evaluate the continuation
co y := x + 1 || x := 2 oc:

           valσ (co y := x + 1 || x := 2 oc) = {∅ ⊲ hσi y σ[y 7→ valσ (x + 1)] · K(co || x := 2 oc)}∪
                                               {∅ ⊲ hσi y σ[x 7→ 2] · K(co y := x + 1 || oc)}
                                             = {∅ ⊲ hσi y σ[y 7→ valσ (x + 1)] · K(x := 2)}∪
                                               {∅ ⊲ hσi y σ[x 7→ 2] · K(y := x + 1)} ,

using the following sub-evaluations: valσ (y := x + 1) = {∅ ⊲ hσi y σ[y 7→ valσ (x + 1)] · K( )} and valσ (x := 2) =
{∅ ⊲ hσi y σ[x 7→ 2] · K( )}.
    To illustrate trace composition, let us consider the trace where statement x := 1 is executed first and explore
the remaining possible traces. We start from the state Ico . The first application of rule (13) results in the
following concrete trace and continuation:

                                 hIco i y [x 7→ 1], K(co y := x + 1 || x := 2 oc) .

At this point, two different instances of the composition rule are applicable, corresponding to the two possible
interleavings; i.e., there is a choice between the two continuations in val[x7→1] (co y := x + 1 || x := 2 oc) as
shown above. The first possible instance of the composition rule is:
                                 [x 7→ 1] = last(hIco i y [x 7→ 1])      ∅ consistent
                              ∅ ⊲ h[x 7→ 1]i y [x 7→ 1][y 7→ val[x7→1] (x + 1)] · K(x := 2)
                                 ∈ val[x7→1] (co y := x + 1 || x := 2 oc)                                       (18)
                                hIco i y [x 7→ 1], K(co y := x + 1 || x := 2 oc) →
                                   hIco i y [x 7→ 1] y [x 7→ 1, y 7→ 2], K(x := 2)
   One further rule application is possible, which results in the final step:
                           hIco i y [x 7→ 1] y [x 7→ 1, y 7→ 2], K(x := 2) →
                           hIco i y [x 7→ 1] y [x 7→ 1, y 7→ 2] y [x 7→ 2, y 7→ 2], K( ) .
   The second possible instance of the composition rule is similar and yields:
                               hIco i y [x 7→ 1] y [x 7→ 2], K(y := x + 1) →
                               hIco i y [x 7→ 1] y [x 7→ 2] y [x 7→ 2, y 7→ 3], K( ) .
   The third possible trace is obtained analogously by starting with the second branch. After this, only one
continuation is possible. Altogether, the following traces are obtained:
                      Tr(sco , Ico ) = { hIco i y [x 7→ 1] y [x 7→ 1, y 7→ 2] y [x 7→ 2, y 7→ 2],
                                         hIco i y [x 7→ 1] y [x 7→ 2] y [x 7→ 2, y 7→ 3],
                                         hIco i y [x 7→ 2] y [x 7→ 1] y [x 7→ 1, y 7→ 2] } .
14                                 C. C. Din et al.

Calculus Let ar and as range over the atomic statements of WHILE (i.e., assignment and skip). It is straightfor-
ward to realise a set of DL rules directly inspired by rule (16). Local parallelism introduces a new composition
operator, and the rules need to cover the different cases of nested statements.

                           (Par)
            Γ, pc ⇒ τ [ar; co r′ || as; s′ oc] φ           (Par-Empty1 )                (Par-Empty2 )
            Γ, pc ⇒ τ [as; co ar; r′ || s′ oc] φ           Γ, pc ⇒ τ [s] φ              Γ, pc ⇒ τ [r] φ
            Γ, pc ⇒ τ [co ar; r′ || as; s′ oc] φ      Γ, pc ⇒ τ [co ◦ || s oc] φ   Γ, pc ⇒ τ [co r || ◦ oc] φ

                            (Par-If1 )                                             (Par-If2 )
                            last(τ ) = σ                                          last(τ ) = σ
           Γ, pc ∪ {valσ (e) = ff} ⇒ τ [co r′ || s oc] φ         Γ, pc ∪ {valσ (e) = ff} ⇒ τ [co r || s′ oc] φ
          Γ, pc ∪ {valσ (e) = tt} ⇒ τ [co r; r′ || s oc] φ      Γ, pc ∪ {valσ (e) = tt} ⇒ τ [co r || s; s′ oc] φ
               Γ, pc ⇒ τ [co if e {r}; r′ || s oc] φ                 Γ, pc ⇒ τ [co r || if e {s}; s′ oc] φ

    The base cases are covered by rules (Par), (Par-Empty1 ) and (Par-Empty2 ). Rule (Par), where ar and
as match atomic statements, splits the proof into two cases, depending on the first executed atomic statement
in the interleaved execution. The two rules (Par-Empty1 ) and (Par-Empty2 ) correspond to rewriting with
empty continuations in rule (17). The remaining rules deal with the case when the statement inside the parallel
statement is not atomic. We illustrate these rules with (Par-If1 ) and (Par-If2 ), which resolve a conditional
inside the parallel statement. Similar rules are required for inner loops, which unfold a while-statement in either
branch into a conditional, and for nested parallel statements, which split the proof by recursively unfolding
different branches. While the soundness of these rules, relative to the LAGC semantics, is evident, they are
impractical because they quickly lead to path explosion. Numerous approaches to mitigate this effect have been
proposed in the literature (e.g., [63,10,62,32]), but here is not the place to dwell on them.


5.2   Atomic

We extend WHILE with atomic blocks to control interleaving in the execution of parallel statements, such that
the syntax for statements from Figure 2 becomes

                                   s ∈ Stmt ::= co s || s oc | atomic(st) | . . . ,

where st is a statement without while loops.


Local Evaluation The atomic statement protects its argument against interleaving computations from other
branches of a parallel execution operator. A (loop-free) statement st can be made to execute atomically, i.e.
without preemption, written atomic(st). Atomic execution requires interleaving points to be removed during
trace composition.

             valσ (atomic(st)) = {pc1 ∪ pc2 ⊲ τ1 ∗∗ τ2 · K( ) | pc1 ⊲ τ1 · K(st′ ) ∈ valσ (st) ∧ st′ 6= ∧
                                           pc2 ⊲ τ2 · K( ) ∈ valσ′ (atomic(st′ )) ∧ σ ′ = last(τ1 )} ∪             (19)
                                 {pc ⊲ τ · K( ) | pc ⊲ τ · K( ) ∈ valσ (st)}

   The main idea behind rule (19) is to recursively unfold the execution of its atomic argument st, while remov-
ing continuation markers. During trace composition, this will prevent the atomic code from being interleaved.
The rule has two cases, depending on whether the evaluation of st contains a non-empty continuation or not: if
the continuation is not empty, we need to evaluate it immediately, as the execution cannot be interrupted before
the end of the atomic statement. Note the structural similarity in the definition of the first trace set above and
the composition rule (13). The difference is that the consistency check and concretisation are deferred until the
actual trace composition.

Discussion. In this execution model, the semantics valσ of non-terminating atomic statements is undefined,
which is the reason for excluding loops. This is a design choice and not a principal limitation: It is possible to
define the semantics of non-terminating atomic programs with suitable scheduling events that allow to process
non-terminating code piece-wise [27]. However, that approach is more complex than the adopted solution and
breaks with the modularity we aim at with only one rule per syntactic construct. A different solution is to equip
                                                                                             LAGC Semantics         15

atomic with a path condition argument (using pc1 in the recursive call) and only keep consistent traces. When
σ is concrete, this would suffice for terminating loops.
    Another solution, presented in Section 7.3 below, is to define a trace composition rule with run-to-completion
semantics: atomic execution of any statement is the default, which can be interrupted only at explicit suspension
points.
    Observe that the semantics of non-terminating non-atomic programs is well-defined: infinite traces are
produced by an infinite number of applications of the composition rule.


Trace Composition The trace composition rule (13) is unchanged, but it is worthwhile to observe how it works
in the presence of atomic. When rule (13) processes a continuation of the form atomic(st), it needs to evaluate
valσ (atomic(st)) for the concrete state σ = last(sh). Rule (19) evaluates s until it reaches a continuation s′ ,
then recursively evaluates s′ , until s is completely executed. No interleaving can occur during the evaluation,
which reflects the intended semantics of atomic statements.

Example 15. To illustrate the evaluation of interleaved execution with atomic, we modify Example 14 as follows:
let sat = co atomic(x := 1; y := x+1) || x := 2 oc. The evaluation branches into either atomic(x := 1; y := x+1)
and then x := 2, or x := 2 and then atomic(x := 1; y := x + 1). In either case, the final value of y is 2, as shown
in the following evaluation:

                       valσ (sat ) ={∅ ⊲ hσi y σ[x 7→ 1][y 7→ valσ[x7→1] (x + 1)] · K(x := 2)} ∪
                                    {∅ ⊲ hσi y σ[x 7→ 2] · K(atomic(x := 1; y := x + 1))} .

Now the trace in which y has the final value 3, is no longer produced; starting from state Iat = Ico we have
Tr(sat , Iat ) = {hIat i y [x 7→ 1] y [x 7→ 1, y 7→ 2] y [x 7→ 2, y 7→ 2], hIat i y [x 7→ 2] y [x 7→ 1] y [x 7→ 1, y 7→
2]}.


Calculus Rules for atomic are remarkably simple, because non-interleaved execution is the default in the
calculus while interleaving is modeled with a case distinction. We let atomic(st) be an atomic statement which
matches ar and as in Section 5.1, such that rule (Par) applies, and introduce a rule which captures that an
atomic statement is equivalent to the statement itself in a sequential setting:

                                                      (Atomic)
                                                  Γ, pc ⇒ τ [st; s] φ
                                             Γ, pc ⇒ τ [atomic(st); s] φ

5.3   Local Memory

We extend WHILE with local variable declarations by introducing a syntactic category of variable declarations
VarDecl and add blocks to the syntax for statements from Figure 2:

                                               s ∈ Stmt ::= { d s } | . . .
                                            d ∈ VarDecl ::= ε | x; d

For simplicity, we omit an empty list of variable declarations in a scope { ε s } and just write { s }.


Local Evaluation A block { d s } introduces a local variable scope such that the program variables d should
only be accessible for the statement s. To avoid interference among variable declarations in different scopes,
possibly introducing the same variable name, the evaluation rule renames the variables in d to unused names
and adds the renamed program variables to the state. The local program variables are correspondingly renamed
in s. The local evaluation rules cover a non-empty and empty list of local variable declarations, respectively.

                   valσ ({ x; d s }) = {∅ ⊲ hσi y σ[x′ 7→ 0] · K({ d s[x ← x′ ] }) | x′ ∈
                                                                                        / dom(σ)}                 (20)


                                                valσ ({ s }) = valσ (s)                                           (21)
Here, s[x ← x′ ] denotes the textual substitution of program variable x by x′ in the statement s.
16                              C. C. Din et al.

Trace Composition Trace composition in rule (13) is unchanged. It will gradually extend the state with fresh
variables, bound to the default value 0, until the local variable declarations of the scope have been reduced to
an empty list, at which point the scope is removed and execution can continue as normal.


Calculus The rules are straightforward. We model initialisation by an assignment to the default value, for
which a rule already exists. Actually, this requires a slight generalisation of the language syntax, such that
variable declarations can occur anywhere in a block, not just at the beginning.

                                       (local1 )                                         (local2 )
                 Γ, pc ⇒ τ [x′ := 0; {s′ }] φ x′ fresh s′ = s[x ← x′ ]                Γ, pc ⇒ τ [s] φ
                                 Γ, pc ⇒ τ [{x; s}] φ                                Γ, pc ⇒ τ [{s}] φ


5.4   Introducing Events and Symbolic Traces

Symbolic traces can contain states in which variables may be bound to unknown values. A simple case where
this become necessary is when WHILE is extended with a statement to express user input, such that the syntax
for statements from Figure 2 becomes

                                             s ∈ Stmt ::= input(x) | . . . .

   For the input-statement, Proposition 2 does not hold, because we do not know the value of the user input
x when locally evaluating the statement. To represent these unknown values in the local semantics, we use
symbolic variables introduced in Definition 3. Events can be used to introduce a point of interaction; we define
an event type inpEv(Y ) that captures the introduction of a symbolic variable Y by an input-statement. The
local evaluation rule for input(x) can be formalised as follows:

                valσ (input(x)) = {∅ ⊲ inpEv{Y }
                                            σ (Y ) y σ[Y 7→ ∗][ x 7→ Y ] · K( ) | Y 6∈ dom(σ)} .              (22)

The trace is well-formed, because the variable Y inside the event is symbolic.
   The composition rule accommodates Proposition 2 by using a concretisation mapping to concretise the
emitted trace. Concretisation captures the actual user input when the statement is executed in a concrete trace.

                    σ = last(sh)   pc ⊲ τ · K(s′ ) ∈ valσ (s) ρ concretises τ      ρ(pc) consistent
                                                                                                              (23)
                                             sh, K(s) → sh ∗∗ ρ(τ ), K(s′ )

   The concretisation mapping ρ ensures that the resulting trace sh ∗∗ ρ(τ ) is concrete.
   The previous composition rule (13) is a special case of this one, when all the states are concrete (this follows
from Proposition 1).

Example 16. Tr(input(x), Iseq ) = {hIseq i ∗∗ inpEv{Y    }
                                                       σ (Y ) y σ[Y 7→ v][ x 7→ v] | v ∈ Val } = {hIseq i y
inpEv(v) y Iseq [Y 7→ v] y Iseq [Y 7→ v, x 7→ v] | v ∈ Val }. All possible values v may occur as an input. Variable
Y has a concrete value now; x, Y are needed to propagate the input value correctly, for example, in subsequent
code of the form “ if (x > 0) then ...”.


Calculus The calculus rule directly follows the local evaluation rule (22) by introducing a fresh variable Y to
model the unknown user input. By definition we have σ∗ (Y ) = ∗, so we do not need this assignment.

                              last(τ ) = σ     Γ, pc ⇒ τ ∗∗ inpEvσ{Y } (Y ) [x := Y ; s] φ   Y fresh
                   (Input)
                                                    Γ, pc ⇒ τ [input(x); s] φ

Interestingly, the abstract composition rule (23) has no effect on the calculus, which is already symbolic, but
the soundness proof needs to be adapted.
                                                                                               LAGC Semantics    17

                              P ∈ Prog ::= M {s}
                             M ∈ Meth ::= m(x){s}
                              s ∈ Stmt ::= skip | x := e | if e { s } | s; s | while e { s }
                                           | co s || s oc | atomic(s) | call(m, e)

                                  Fig. 4: Program Syntax with Procedure Calls.


5.5   Procedure Calls

Figure 4 introduces procedure11 calls with the statement call(m, e): A program is a set of method declarations
M with main block {s}. We consider M to be a method table that is implicitly provided with a program. Each
method declaration associates a unique name m with the statement in its body. To reduce technicalities, we
assume without loss of generality that a method call has one argument and no return value on which the caller
needs to synchronise.12
    In contrast to parallel co s || s oc statements, where parallelism is explicit in the program syntax, procedure
calls introduce implicit parallel execution: there is a context switch between the syntactic call site and the
processor, whereupon the call is executed in parallel. This decoupling has an important consequence: according
to the local evaluation principle, method bodies are evaluated independently of the call context. This necessitates
a new composition rule that starts the execution of a called method. We also need to ensure that a method is
not executed before it is called, requiring the introduction of suitable events.


Local Evaluation The new events are invEv(m, valσ (e)) and invREv(m, valσ (e)) for a given state σ. These
events denote the invocation and the activation (also called the invocation reaction) of a method m with
argument e, respectively. Recall from Section 2.3 that events inserted into a trace at a state σ are preceded
and succeeded by that state. The local evaluation rule (24) for a call to m with argument e has an empty
path condition, inserts an invocation event invEv(m, valσ (e)) into the trace, and continues with the empty
continuation. This means that the call is non-blocking: the code following the call could be executed immediately,
if scheduled. The rule is formalised as follows:

                               valσ (call(m, e)) = {∅ ⊲ invEvσ (m, valσ (e)) · K( )} .                          (24)


Trace Composition: Concrete Variant The concurrency model so far is still very simple: method invocations
and processors are anonymous, there is no way to distinguish between two calls to the same method: these execute
identical code and all executions can be interleaved. For this reason, it is sufficient to represent continuation
candidates for the next execution step as a multiset q. We denote with “+” the disjoint multiset union. We add
a rewrite rule to simplify empty continuations in the multisets of tasks; this rule is applied exhaustively when
adding tasks in multisets.
                                                q+{K( )}      q.
    The judgment representing trace extension by one step has the form: sh, q → sh′ , q ′ where q, q ′ are multisets
of continuations of the form K(s).

                               σ = last(sh) pc ⊲ τ · K(s′ ) ∈ valσ (s)     pc consistent
                                                                                                                (25)
                                        sh, q+{K(s)} → sh ∗∗ τ, q+{K(s′ )}
    The difference between rule (13) and rule (25) is that we no longer commit to one possible continuation,
because the continuation code is now located in a method. Therefore, the rule selects and removes one matching
continuation from the pool q, executes it to the next continuation marker, exactly like rule (13), and then puts
the code remaining to be executed back into q. We also need a new composition rule that adds method bodies
to the pool q.
                     m(x){s} ∈ M σ = last(sh) wf (sh ∗∗ invREvσ (m, v)) y 6∈ dom(σ)
                                                                                                            (26)
                          sh, q → sh ∗∗ invREvσ (m, v) y σ[y 7→ v], q+{K(s[x ← y])}
11
   Historically, it is more common to use the term procedure, whereas in object-oriented programming the term method
   is usual, which is where the LAGC concept originated from. We use both terms interchangeably.
12
   Synchronisation on return values is discussed in Section 7.3.
18                                  C. C. Din et al.

The rule handles the creation of a new execution thread. We select a method with body s from table M and
create a new continuation K(s[x ← y]), where the call parameter x is substituted with a fresh variable y for
disambiguation. The new continuation is added to the pool q. Next, we need to record that a new method with
argument v has started to execute, as a consequence of a previous method call. The existence of this call is
ensured by the premise expressing the well-formedness of the extended trace, which requires an invocation event
of the form invEv(m, v) to be present in sh. We extend the current trace with the invocation reaction event13
invREvσ (m, v) to mark the start of method execution and record the extension of the current state in which
the parameter y has the value v. It remains to formalise well-formedness.

Well-Formedness A trace is well-formed if its events obey certain ordering restrictions. Whenever a trace sh is
extended with an invocation reaction event of the form invREv(m, v), there must be a corresponding invocation
event invEv(m, v) in sh. This ordering restriction can be captured by counting the number of occurrences of both
event forms in sh using the comprehension expression #sh (ev(e)). In all other cases, the trace stays well-formed
when it is extended with a new event. We formalise well-formedness as a predicate on traces.

Definition 23 (Well-Formedness). The well-formedness of a concrete trace sh is formalised by a predicate
wf (sh), defined inductively over the length of sh:

                                      wf (ε) = true
                                wf (sh y σ) = wf (sh)
                      wf (sh y invEv(m, v)) = wf (sh)
                     wf (sh y invREv(m, v)) = wf (sh) ∧ #sh (invEv(m, v)) > #sh (invREv(m, v))


    The well-formedness predicate is used in the global composition rules to ensure that only a valid concrete
trace for a given program can be generated during the trace composition. Any trace emitted by the trace
composition rules is well-formed, because it is an invariant established each time a trace is extended. It is
sufficient to define well-formedness on concrete traces, because in the end it has to hold for them. It follows that
well-formedness is always a simple, decidable property.

Global Trace Semantics
Definition 24 (Program Semantics with Procedure Calls). Given a finite program P with a method
table M and a main block smain . Let sh0 , q0 → sh1 , q1 → · · · be a maximal sequence obtained by the repeated
application of the composition rules (25)–(26), starting with hIP i, {K(smain )}. If the sequence is finite, then it
must have the form
                                       hIP i, {K(smain )} → · · · → sh, ∅ .
    If the sequence is infinite, let sh = limi→∞ shi . In either case, sh is a trace of P . The set of all such traces
is denoted by Tr(P, IP ).

Example 17. Consider the following program P :

                                                m(x) {y := x; x := x + 1}
                                                {call(m, 1); z := 2}

The method table for this program is M = {m(x) {y := x; x := x + 1}}. The evaluation of the main method is
as follows:
                             valσ (call(m, 1)) = {∅ ⊲ hσi y invEv(m, 1) y σ · K( )}
                                   valσ (z := 2) = {∅ ⊲ hσi y σ[z 7→ 2] · K( )}
                     valσ (call(m, 1); z := 2) = {∅ ⊲ hσi y invEv(m, 1) y σ · K(z := 2)}
To prepare the evaluation of the method body of m(x) (where x is any integer):

                                       valσ (y := x) = {∅ ⊲ hσi y σ[y 7→ valσ (x)] · K( )}
                                  valσ (x := x + 1) = {∅ ⊲ hσi y σ[x 7→ valσ (x + 1)] · K( )}                    (27)
                         valσ (y := x; x := x + 1) = {∅ ⊲ hσi y σ[y 7→ valσ (x)] · K(x := x + 1)}
13
     Recall that invREvσ (m, v) is a triple with two copies of σ around invREv(m, v).
                                                                                               LAGC Semantics       19

   Let IP be the initial state of P . We consider the state where the statement call(m, 1) in main has already
been executed, and explore the possible traces. The concrete trace and the continuation pool at this point are
sh = hIP i y invEv(m, 1) y IP and q = {K(z := 2)}, respectively. Let sm be the method body of m. Both
composition rules (25) and (26) are applicable and yield different interleavings: the execution continues either
with the main method or with the creation of a new execution thread. In the following, we assume that the
execution continues with thread creation, i.e. we apply rule (26):

                   m(x){sm } ∈ M        IP = last(sh)   wf (sh ∗∗ invREvIP (m, 1))    w 6∈ dom(IP )
                                                                                                                  (28)
                              sh, q → sh ∗∗ invREvIP (m, 1) y [w 7→ 1], q+{K(sm [x ← w])}

   At this point, both composition rules are again applicable, but only rule (25) is useful: since only one
invocation event is present in sh, well-formedness will not allow more than one instance of m to execute. We
use some abbreviations:
                         sh′ = sh ∗∗ invREvIP (m, 1) y [w 7→ 1]
                              = hIP i y invEv(m, 1) y IP y invREv(m, 1) y IP y [w 7→ 1]
                         s′m = {sm [x ← w]} = {y := w; w := w + 1}
                          q ′ = q+{K(sm [x ← w])} = {K(z := 2), K(y := w; w := w + 1)}

The two continuations in q ′ indicate two possible interleavings. We assume execution continues with the body
of m:
                                         [w 7→ 1] = last(sh′ )  ∅ consistent
                 ∅ ⊲ h[w 7→ 1]i y [w 7→ 1][y 7→ val[w7→1] (w)] · K(w := w + 1) ∈ val[w7→1] (s′m )
                                                                                                          (29)
                                  sh′ , {K(z := 2)}+{K(y := w; w := w + 1)} →
                      sh′ ∗∗ h[w 7→ 1]i y [w 7→ 1, y 7→ 1], {K(z := 2)}+{K(w := w + 1)}
where val[w7→1] (s′m ) is taken from equation (27). We introduce the abbreviations:

              sh′′ = hIP i y invEv(m, 1) y IP y invREv(m, 1) y IP y [w 7→ 1] y [w 7→ 1, y 7→ 1]
               q ′′ = {K(z := 2)}+{K(w := w + 1)}

  At this point, rule (25) is again applicable and the two continuations in q ′′ indicate two possible interleavings.
We assume the execution continues with the main method body.

                                     [w 7→ 1, y 7→ 1] = last(sh′′ )    ∅ consistent
                  {∅ ⊲ h[w 7→ 1, y 7→ 1]i y [w 7→ 1, y 7→ 1, z 7→ 2] · K( )} ∈ val[w7→1,y7→1] (z := 2)            (30)
                    ′′   ′′       ′′
                  sh , q → sh ∗∗ h[w 7→ 1, y 7→ 1]i y [w 7→ 1, y 7→ 1, z 7→ 2], {K(w := w + 1)}

   At this point only one continuation is possible, which results in the concrete trace:

                     hIP i y invEv(m, 1) y IP y invREv(m, 1) y IP y [w 7→ 1]
                       y [w 7→ 1, y 7→ 1] y [w 7→ 1, y 7→ 1, z 7→ 2] y [w 7→ 2, y 7→ 1, z 7→ 2] .

    There are two other possible interleavings that all result in the same final state. If, for example, the assignment
in the main method of P were changed to y := 2, then traces with different final states would be generated. ⊓        ⊔

Trace Composition: Symbolic Variant The trace composition in rule (26) works “eagerly” or “on demand”
in the sense that a concrete trace extending σ and a continuation containing the local parameter y, whose value
is fixed in σ[y 7→ v], are generated on the spot. In the presence of multiple calls to the same method, this leads
to multiple evaluation of the same code, i.e. the method body. A deductive verification calculus would avoid this
and evaluate each method only once, but symbolically [4]. We demonstrate that abstract traces allow semantic
evaluation that works similarly by defining a local evaluation function for methods which combines the use of
symbolic variables from the input-statement in Section 5.4 with the variable renaming used for local memory
in Section 5.3. We first introduce a symbolic variable Y to act as a placeholder for the value of the substituted
call parameter y and then substitute the call parameter x with a fresh variable y for disambiguation, as done
in rule (26):

                valσ (m(x){s}) =
                                                                                                                  (31)
                     {∅ ⊲ invREv{Y }
                                σ (m, Y ) y σ[Y 7→ ∗, y 7→ Y ] · K(s[x ← y]) | y, Y 6∈ dom(σ)} .
20                                      C. C. Din et al.

We conventionally write y, Y 6∈ dom(σ) to express that no element in a list of variables is in the domain of σ.
   The concrete composition rule (26) needs to be adapted to a composition rule which takes the evaluation of
a method declaration and concretises the resulting symbolic trace in a well-formed and consistent way:

                                   m(x){s} ∈ M       ρ concretises τ     ρ(pc) consistent
                             σ = last(sh)   pc ⊲ τ · K(s′ ) ∈ valσ (m(x){s})    wf (sh ∗∗ ρ(τ ))                               (32)
                                                                                      ′
                                                   sh, q → sh ∗∗ ρ(τ ), q+{K(s )}

The definition of well-formedness stays the same. Definition 24 of trace semantics of P stays the same, except
that rule (32) is used instead of rule (26). It is interesting to note that, while we need one more local rule (to
evaluate method declarations), the composition rule becomes simpler, more uniform with rule (25), and more
modular (not referring to events) as a consequence.

Example 18. Consider the program P from Example 17. Let sm be the method body of m. The evaluation of
the method declaration with rule (31) is as follows:

          valσ (m(x){sm })
                = {∅ ⊲ invREv{W
                             σ
                                }
                                  (m, W ) y σ[W 7→ ∗, w 7→ W ] · K(sm [x ← w]) | w, W 6∈ dom(σ)}
                             {W }
                = {∅ ⊲ invREvσ (m, W ) y σ[W 7→ ∗, w 7→ W ] · K(y := w; w := w + 1) | w, W 6∈ dom(σ)} .

Calculus There are several ways to model procedure calls in a calculus. The expressiveness of DL permits a
simple method that suffices for the language at hand. The basic insight is that the DL formula φ occurring in
a sequent Γ ⇒ τ φ may contain more than one modality. This can be used to model the process pool q as
a conjunction of indexed modal formulas in a sequent of the form Γ ⇒ τ ([s1 ]1 φ1 ∧ · · · ∧ [sn ]n φn ) (i ∈ N),
which is still well-formed. Each modality of the form [·]i in the sequent represents one process in the pool
q, distinguished from each other by a unique index i. All calculus rules introduced so far are assumed to be
equipped with indexed modalities. This can be done in a completely uniform manner.
    We need a way to model multi-process execution like in rule (25). Since the computations of the si might
interfere with each other, there may in the general case be many interleavings of the si that need to be considered.
The meta rule schema (Interleave) branches into different premises, depending on which of the si is scheduled,
thus unfolding all possible different interleavings:

                                           (Interleave)
           V all 1 ≤ i ≤ n : V
           For                                                                               Such that
                                                                                                     V there is a rule
            j∈Zi wf (τj ) Γ, pc, j∈Zi (pc ∪ pcj → τj [sj ]i φi ) ⇒ τ [s          i ]i φi            j∈Zi wf (τj )
            Γ, pc ∪ pcj ⇒ τj [s1 ]1 φ1 ∧ · · · ∧ [sj ]i φi ∧ · · · ∧ [sn ]n φn j∈Zi           Γ, pc ∪ pcj ⇒ τj [sj ]i φ j∈Zi
                  Γ, pc ⇒ τ ([s1 ]1 φ1 ∧ · · · ∧ [si ]i φi ∧ · · · ∧ [sn ]n φn )                   Γ, pc ⇒ τ [si ]i φ

    The rule schema (Interleave) takes the form of a context rule, replacing a conjunct in the conclusion
with a formula from which that conjunct can be derived with an appropriate path condition (thus generalising
the rules for local parallelism in Section 5.1). The schema unfolds the premises for each conjunct [si ]i φi in the
conclusion, such that there is a rule in the calculus which is applicable to Γ, pc ⇒ τ [si ]i φ with premise(s)
Γ, pc ∪ pcj ⇒ τj [sj ]i φ for j ∈ Zi and constraint wf (τj ).14 We use the notation {φj }j∈Zi to denote a set of
formulas indexed by j from the index set Zi . Thus in the rule schema shown on the right, the bracketed sequent
denotes the set of sequent premises to the rule for Γ, pc ⇒ τ [si ]φ (for example, rule (Cond) has a set containing
two premises).
    The second premise of (Interleave) is discharged by the rule corresponding to the schema on the right.
Well-formedness becomes a separate proof obligation for every trace τj , that can be dealt with by a fairly
straightforward translation into first-order logic (see [30] for the details).
    This approach rests on two assumptions about the rule displayed above on the right: first, it must follow the
required syntactic form, second, it must be sound. For the composition of more general calculi, it is necessary
to define syntactic restrictions and soundness constraints [52].
    It remains to design calculus rules modeling rule (24) and rules (31)–(32). The first is straightforward,
resulting in rule (MtdCall). We can combine rules (31)–(32) into a single rule (MtdRun) by wrapping the
body of m into a block and declaring its formal parameter x as a local variable. This allows us to re-use the
14
     The discussion of the efficiency of the rules for local parallelism in Section 5.1 also applies to rule (Interleave).
                                                                                                  LAGC Semantics    21

previously declared rules. We assume given method specifications in the form of a formula φ associated with
each method. In the new conjunct, the modality must have a fresh index. The call argument e must be supplied
at the time the rule is applied. One heuristics is to look for matching invocation events in τ .
                                                                                 (MtdRun)
                      (MtdCall)                                   last(τ ) = σ     i fresh in ψ
                      last(τ ) = σ                         m(x){s} ∈ M        wf (τ ∗∗ invREvσ (m, e))
            Γ, pc ⇒ τ ∗∗ invEvσ (m, e) [s]i φ         Γ, pc ⇒ τ ∗∗ invREvσ (m, e) ([{x; x := e; s}]i φ ∧ ψ)
             Γ, pc ⇒ τ [call(m, e); s]i φ                                  Γ, pc ⇒ τ ψ

5.6   Guarded Statements
Guarded statements are a common synchronisation mechanism in concurrent languages [24,44,49]. A statement
is preceded by a Boolean guard expression that blocks execution of the current process, until the guard is
evaluated to true. This can be used, for example, to ensure that the result of a computation is ready before it
is used, a message has arrived, etc. Our syntax for guarded commands is inspired by ProMeLa; the syntax for
statements from Figure 2 becomes (where g is a Boolean expression):
                                                s ∈ Stmt ::= :: g; s | . . . .

Local Evaluation A local evaluation rule for a guarded statement is straightforward to design. If the Boolean
guard g evaluates to true, the execution continues normally. If the guard g evaluates to false, the execution
is blocked until g evaluates to true. Blocking is modeled by re-scheduling the entire guarded statement in the
continuation.
                  valσ (:: g; s) = {{valσ (g) = tt} ⊲ hσi · K(s)},    {valσ (g) = ff} ⊲ hσi · K(:: g; s)}}         (33)

Trace Composition The trace composition rule (13) is unchanged, but it is interesting to observe how it
works in the presence of :: g; s. When rule (13) processes a continuation with a guarded statement, it may result
in a deadlocked trace due to the second alternative, where from some point onward no progress is made on
some non-empty continuations in the process pool. How to detect and, possibly, to avoid deadlocks is a question
outside the scope of this paper.

Calculus Structurally, the local rule (33) for guarded statements is very similar to the rule (8) for the conditional
(in fact, the case when the guard is true, is actually identical). Indeed, we can design a calculus rule modeled
after (Cond):
                                                        (GrdStmt)
             last(τ ) = σ     Γ, pc ∪ {valσ (g) = tt} ⇒ τ [s] φ      Γ, pc ∪ {valσ (g) = ff} ⇒ τ [:: g; s] φ
                                                 Γ, pc ⇒ τ [:: g; s] φ
While this rule is certainly sound, it is clearly incomplete, because it admits infinitely many possible interleavings.
To achieve completeness, one would need to establish a suitable invariant that holds whenever the guard is
evaluated and that is strong enough to render the proof finite (for example, by excluding a branch when the
guard is false). For details on such techniques, we refer the reader to the literature [30,53].

6     Semantics For A Shared-Memory Multiprocessor Language
We consider a multiprocessor extension to the programming language of Section 5. This goes some way to realize
a concurrent, object-oriented setting: We will now spawn processes, each with its own identity and its own task
queue to execute, but memory is still shared among the processes. In addition, processes may exchange values by
sending and receiving messages, which have their own identity and thus provide the capability to impose ordering
constraints among them. Tasks are method invocations similar to the ones defined in the previous section. In
particular, we use the second variant of the semantics, defined in Section 5.5 with the rules (31)–(32).
    Expressions on the right-hand side of assignments are extended with spawn(m, e), which creates a new
(virtual) process where task m is called with an actual value e. It returns the identifier of the newly created
process. Furthermore, two statements send(e1 , e2 ), to send a value e1 to a process with identifier e2 , and
receive(x, e), to bind a value received from e to the variable x, are introduced such that processes may
exchange values. The syntax is shown in Figure 5.
22                                   C. C. Din et al.

                        P ∈ prog ::= M {s}
                       M ∈ Meth ::= m(x){s}
                        s ∈ Stmt ::= skip | x := rhs | if e { s } | s; s | while e { s } | co s || s oc
                                      | atomic(st) | call(m, e) | send(e, e) | receive(x, e)
                       rhs ∈ Rhs ::= e | spawn(m, e)

                           Fig. 5: Syntax for the Shared-Memory Multiprocessor Language.


6.1     LAGC Semantics
In a multiprocessor setting it is necessary to keep track of what each process does, in particular, about the
origins and destinations of messages. This is achieved by introducing process identifiers and tagging each event
in a trace with the identifier of the process that produced it. remark that this tagging is orthogonal to the local
semantic evaluation.

Definition 25 (Tagged Trace, Projection). Let ev(e) be an event, τ, τ1 , τ2 traces, and p ∈ PId a process
identifier. A tagged trace τ p is defined inductively as follows:

                                                     (ev(e)) p = ev p (e)
                                                     σp = σ
                                                     (τ1 · τ2 ) p = τ1p · τ2p

Local Evaluation In the following, let PId be a set of process identifiers with typical element p and MId a set
of message identifiers with typical element i. We start with the evaluation rule for send. The rule evaluates the
arguments to send and creates a trace from the current state σ with an event sendEv(v, p, i) expressing that a
value v is sent to the process p by a message with the identifier i. The message can have any possible identifier,
so the rule provides traces for all of them:

                        valσ (send(e, e′ )) = {∅ ⊲ sendEvσ (valσ (e), valσ (e′ ), i) · K( )} | i ∈ MId} .          (34)

    The local semantics of receive and spawn is more complex, because the values received in these statements
are not known in the local evaluation. We employ the technique using symbolic variables introduced in Sec-
tion 5.4. In contrast to the case for method calls (Section 5.5), we do not have the option to compose concrete
continuations “on demand”, because the return values for receive and spawn are going to be resolved later.15
The rules evaluate to a trace with the event receiveEv(v, p, i), expressing that the value v is received from a
process p by a message with identifier i, and a trace with the event spawnEv(m, v, p), expressing that a new
process with identifier p is created to execute the task m with the parameter value v. In each rule, the symbolic
variable Y represents the (as yet) unknown received value.

                   valσ (receive(x, e)) = {∅ ⊲ receiveEvσ{Y } (Y, valσ (e), i) y σ[x 7→ Y, Y 7→ ∗] · K( )
                                                                                                                   (35)
                                          | Y 6∈ dom(σ), i ∈ MId}

                 valσ (x := spawn(m, e)) = {∅ ⊲ spawnEv{Y }
                                                       σ (m, valσ (e), Y ) y σ[x 7→ Y, Y 7→ ∗] · K( )              (36)
                                           | Y 6∈ dom(σ)}
All previous local rules are unchanged.

Trace Composition The trace composition rules generalize rules (25) and (32). There are three main differ-
ences: First, both composition rules now work on symbolic traces, simply because rules (35)–(36) are symbolic.
Second, to account for having several processes, we introduce a mapping Ω from process identifiers p to mul-
tisets of continuations q, i.e. Ω(p) gives the current task list for a given process. As before, we denote with +
the disjoint multiset union on task lists. The judgment representing trace extension by one step has the form:
sh, Ω → sh′ , Ω ′ . Third, we tag the generated concrete trace with the process identifier that created it.
    The following rule selects a processor p with non-empty task list and from there a continuation s, evaluated
in last(sh). The resulting symbolic trace τ must be concretizable such that, after tagging, it extends sh in a
15
     It would be possible to introduce symbolic values for message identifiers as well in the rule for send and receive.
     However, since programs do not manipulate message identifiers, there is no reason to do so.
                                                                                              LAGC Semantics         23

well-formed manner. Observe that sh is tagged already. The remaining continuation K(s′ ) is added back to p’s
task list.
                                       p ∈ dom(Ω)       Ω(p) = q+{K(s)}
    σ = last(sh)     pc ⊲ τ · K(s′ ) ∈ valσ (s)   ρ concretizes τ      ρ(pc) consistent        wf (sh ∗∗ ρ(τ )p )
                                                                                                                    (37)
                                     sh, Ω → sh ∗∗ ρ(τ )p , Ω[p 7→ q+{K(s′ )}]

    The following rule is similar and follows the pattern established in rule (32). It starts to evaluate a method
body on a processor p and adds the remaining continuation K(s′ ) to its task list. If p 6∈ dom(Ω), we use the
notational convention Ω(p) = ∅ and avoid a special operation to create a process. The following rule thus
either creates a task inside an existing process or spawns a new process if necessary, similar to rule (32). Well-
formedness ensures that the correct number of tasks is created, relying on the fact that valσ (m(x){s}) starts
with an invocation reaction event.
                        m(x){s} ∈ M       σ = last(sh)     pc ⊲ τ · K(s′ ) ∈ valσ (m(x){s})
                            ρ concretizes τ     ρ(pc) consistent     wf (sh ∗∗ ρ(τ )p )                             (38)
                                                           p                       ′
                                    sh, Ω → sh ∗∗ ρ(τ ) , Ω[p 7→ Ω(p)+{K(s )}]

Well-formedness We need to establish the basic properties of sending and receiving as well as to ensure that
each process has the right number of tasks.
Definition 26 (Well-formedness). The following rules are added to the rules in Definition 23, except the
final one, which replaces the final rule in Definition 23. The first rule ensures no two messages will be sent
with the same message identifier, the second one states that each message is received only once. Similarly, the
third rule guarantees that each spawn allocates a new process identifier. The final rule reflects the fact that the
code executed on a processor p can be the reaction to either a call or a spawn event, i.e. spawnEv p acts as a
particular invocation event.
                                                                              ′′
              wf (sh y sendEv p (e, p′ , i)) = wf (sh)∧ 6 ∃p′′ , e′ , p′′′ . sendEv p (e′ , p′′′ , i) ∈ sh
                                                                                        ′′
           wf (sh y receiveEv p (e, p′ , i)) = wf (sh)∧ 6 ∃p′′ , e′ , p′′′ . receiveEv p (e′ , p′′′ , i) ∈ sh
                                                                                       ′′
           wf (sh y spawnEv p (m, v, p′ )) = wf (sh)∧ 6 ∃p′′ , m′ , v ′ . spawnEv p (m′ , v ′ , p′ ) ∈ sh
                                p
               wf (sh y invREv (m, v)) = wf (sh)    X∧                          ′
                        #sh (invEv p (m, v)) +           #sh (spawnEv p (m, v, p)) > #sh (invREv p (m, v))
                                                 p′ ∈PId

    Message identifiers are used to avoid sending or receiving the same message (i.e. two messages with the same
identifier) twice. This rule set is incomplete as it does not specify when a message is received. This aspect is
discussed in Section 6.2 and will also use message identifiers. For example, the basic correctness criterion that
states that “all received messages have been sent” is captured by the well-formedness condition in Definition 28;
this criterion should be used in addition to the wf predicate defined above.

Global Trace Semantics
Definition 27 (Program Semantics with Multiprocessors). Given a program P with a method table M
and a main block smain , let sh0 , Ω0 → sh1 , Ω1 → · · · be a maximal sequence obtained by the repeated application
of the composition rules (37)–(38), starting with

                               hIP i y spawnEv0 (main, 0, 0), Ω[0 7→ {K(smain )}] .                                 (39)

If the sequence is finite, then it must have the form

                      hIP i y spawnEv0 (main, 0, 0), Ω[0 7→ {K(smain )}] → · · · → sh, Ω ,

where Ω (p) = ∅ for all p ∈ dom(Ω). If the sequence is infinite, let sh = limi→∞ shi . In either case, sh is a
trace of P . The set of all such traces is denoted with Tr(P, IP ).
    The spawn event at the start of a trace represents the creation of an initial process that runs the main
method. The well-formedness of traces ensures that subsequently spawned processes will not erroneously be
assigned index 0, which is reserved for the code executed in the main method.
24                                     C. C. Din et al.

6.2      Communication Patterns
We now unleash the power of traces with events and show that several well-known communication patterns
can be defined simply by adding well-formedness constraints to Definition 26. Imposing such patterns in the
LAGC semantics is modular in the sense that all other rules are unaffected by the enforced patterns. The well-
formedness constraints defined in this section are to be added conjunctively to the well-formedness predicate wf
over concrete traces sh (Definition 26) to achieve the desired semantic properties. We recall for the definitions
below that e is an expression, p, p′ ∈ PId process identifiers, and i ∈ MId a message identifier.
   We first consider the basic tenet of asynchronous communication, stipulating that received messages must
have been sent.
Definition 28 (Asynchronous Communication Constraint). Well-formed asynchronous communication
is captured by the constraint wf ac , defined as follows :
                                                                                          ′
                             wf ac (sh y receiveEv p (e, p′ , i)) = wf (sh) ∧ sendEv p (e, p, i) ∈ sh
   Next, we consider the FIFO (first-in, first-out) ordering principle, which stipulates that messages between
the same processors must be received in the same order as they were sent; i.e. messages may not overtake each
                                         ′                                                ′
other. Let the notation ev P (v) <sh ev′P (v ′ ) express that ev P (v) appears before ev′P (v ′ ) in a trace sh.
Definition 29 (FIFO Communication Constraint). Well-formed FIFO communication is captured by the
constraint wf fifo , defined as follows :

     wf fifo (sh y receiveEv p (e, p′ , i)) = wf ac (sh y receiveEv p (e, p′ , i)) ∧
                                          ′                           ′                          ′
                               ∀sendEv p (e′ , p, i′ ) ∈ sh. sendEv p (e′ , p, i′ ) <sh sendEv p (e, p, i)
                                                                                              =⇒ receiveEv p (e′ , p′ , i′ ) ∈ sh .
                                                                                                                                 

    A channel is an ordered pair (p, p′ ) of processor identifiers (not necessarily distinct) such that p sends
messages to p′ and p′ receives messages sent by p. The messages in a channel after a trace sh can be given as a
set of message identifiers, defined by the following function:
Definition 30 (Channel). Given a concrete trace sh and a channel ch = (p, p′ ), we define by inChannel(sh, ch)
the messages in ch that have been sent, but not yet received within sh:
                                                                                                     ′
                   inChannel(sh, (p, p′ )) = {i | ∃e.sendEv p (e, p′ , i) ∈ sh ∧ receiveEv p (e, p, i) 6∈ sh} .
   We can detect that a fixed bound N > 0, the capacity of a FIFO channel, has been reached by the following
condition, which blocks a send event if the channel is full, i.e. the channel already contains N −1 messages.
Definition 31 (Bounded FIFO Communication Constraint). Let N be an integer. Well-formed N -bound
FIFO, ensured by the predicate wf bd(N ) , is captured by extending the constraint wf fifo for standard (unbound)
FIFO by a check on the bound of the channel as follows. Well-formedness of a trace ending by a reception event
is given by wf fifo , and an additional rule checks well-formedness of message sending:
                       wf bd(N) (sh y sendEv p (e, p′ , i)) = wf (sh) ∧ | inChannel(sh, (p, p′ )) | < N .
    Causally ordered (CO) messages are harder to characterize than the previous communication patterns,
because in the most simple definition of CO found in [20], the receiving events must occur in the right order
provided that sending events are causally ordered. Our event structure does not record causal ordering. This
could certainly be realized, but it would add considerable complexity to the evaluation rules. Instead, we use
the information that is already provided by the events in a given trace, based on an alternative characterization
of CO [20]: “a computation is CO if and only if no message is bypassed by a chain of other messages”. We first
define a chain predicate such that Chain(e, e′ , sh) is true if there is a chain of messages inside sh that asserts
the causal ordering of e and e′ induced by messages.
Definition 32 (Communication Chain). The predicate Chain holds for two events e and e′ in a given trace
sh, if there is a chain of messages asserting the causal ordering between e and e′ :
                              ∃n, e1 , . . . , en , i1 , . . . , in , p1 , . . . , pn+1 .
                               ∀1 ≤ k ≤ n. sendEv pk (ek , pk+1 , ik ) ∈ sh ∧ receiveEv pk+1 (ek , pk , ik ) ∈ sh ∧
                                                                                                                  
                       ′
           Chain(e, e , sh) =
                               ∀1 < k ≤ n. receiveEv pk (ek−1 , pk−1 , ik−1 ) <sh sendEv pk (ek , pk+1 , ik )
                              such that e <sh sendEv p1 (e1 , p2 , i1 ) ∧ receiveEv pn+1 (en , pn , in ) <sh e′ .
                                                                                                            LAGC Semantics               25

    We now define a well-formedness constraint that checks the absence of a message sent in the past (according
to the definition of Chain) but not yet received. The following definition generalises Definition 29 to messages
causally ordered (according to the Chain predicate) instead of messages originating from the same process:

Definition 33 (CO Communication Constraint). Well-formed CO communication is captured by the con-
straint wf co , defined as follows :
                                                                 ′
    wf co (sh y receiveEv p (e, p′ , i)) = wf (sh) ∧ sendEv p (e, p, i) ∈ sh ∧
                                                                ′′                       ′
                               ∀e′′ , p′′ , i′′ . Chain(sendEv p (e′′ , p, i′′ ), sendEv p (e, p, i), sh)
                                                                                              =⇒ receiveEv p (e′′ , p′′ , i′′ ) ∈ sh .

   Finally, we have a look at synchronous call patterns. Several definitions can be found in [20]. We adopt
a definition that constrains well-formed traces rather strongly: any send event is immediately followed by the
corresponding receive event.
Definition 34 (Strict Synchronous Communication Constraint). Well-formed strict synchronous com-
munication is captured by the constraint wf sync , defined as follows :
                                                                                            ′
                     wf sync (sh y receiveEv p (e, p′ , i)) = wf (sh) ∧ sh = sh′ ∗∗ sendEvσp (e, p, i)
                                                                                                      


    The above constraint is realized, for example, by rendez-vous channels in ProMeLa [44], see Section 7.1.
    One can define more liberal notions of synchronous communication that accept the presence of independent
events between the sending and the reception of the message. The crown criterion [20], for example, can be used
for this purpose. Its definition is global over traces and requires to define wf in a non-inductive manner (as an
invariant holding for the trace at any time). We omit a detailed elaboration, because this would distract from
the main point of this paper.


7       Case Studies

7.1     ProMeLa



    1    chan r e q u e s t = [ 0 ] of {byte } ;                      9   active proctype S e r v e r ( ) {
    2                                                                10     byte n ;
    3    active proctype C l i e n t 0 ( ) {                         11
    4      request !0;                                               12       do
    5    }                                                           13       : : r e q u e s t ?n ;
    6    active proctype C l i e n t 1 ( ) {                         14           printf ( " c l i e n t %d\n" , n )
    7      request !1;                                               15       od
    8    }                                                           16   }


                                            Fig. 6: A simple ProMeLa program.


    ProMeLa [44] is a concurrent modeling language that has been used to model and analyse numerous
industrial systems. It comes with an industry-strength model checker [13]. We do not give a full LAGC-style
semantics of ProMeLa, but we discuss its main features and illustrate that they can be formalised using minor
variations of the concepts discussed above. We also do not give the DL calculus for ProMeLa, which mostly
follows the calculus developed in Sections 4–5, since ProMeLa is designed for model checking. We assume the
reader is familiar with ProMeLa. A simple example of a ProMeLa program is shown in Figure 6.

Types, Variables, Expressions All ProMeLa datatypes are mapped into finite integer types, including Booleans,
process and channel identifiers, enumerations, arrays, etc. Strings occur only as literals in print statements.
Variables declared outside a process are global and can be accessed by any process, such as the request channel
in Figure 6, line 1. Like in WHILE, ProMeLa expressions are side effect-free and their evaluation is standard.
26                                C. C. Din et al.

Processes Methods and method calls do not exist in ProMeLa, so call is not present. All ProMeLa processes
are declared and started in the beginning by a—possibly implicit—initial process, so spawn does not occur in
the ProMeLa syntax either. In Figure 6, three processes are declared and started upfront. It is easy to create
an initial judgment similar to rule (39) from the process declarations of a ProMeLa program P :

                                                      hIP i, ΩP ,

where ΩP (p) = {K({sp })} for each process p ∈ P with program code sp . The code is wrapped in a scope to
handle local variable declarations as in Section 5.3.
    There is no need for a method table, because there are no method calls. For the same reason, the range of
Ω is a singleton. ProMeLa processes execute in parallel and interleave on global variables. The granularity of
interleaving in ProMeLa is the same as in Section 5.1, so the continuations in the local rules are unchanged.
Composition rule (37) is adequate for the ProMeLa semantics, while rule (38) is not needed, because there are
no method calls and the program code of all processes is part of the initial judgment. In consequence, neither
spawn, nor invocation, nor invocation reaction events occur in ProMeLa traces.

Statements There is a print statement with no effect on states, we decide not to observe the effect on the
trace, we can thus give it the semantics of skip in rule (6). Assignments are exactly as in WHILE, discussed
in Section 3. Instead of if- and while-statements, ProMeLa has selection and repetition statements over
guarded commands, which may occur only there. The semantics of guarded statements is as in Section 5.6. The
semantics of a selection if :: g1 ; s1 · · · :: gn ; sn fi is a straightforward generalisation of rules (8) and (33) with
n + 1 premisses; one for each guarded statement and one premiss if no guard is true. The path condition of the
i-th guarded statement is gi . When more than one guard is true, any one of them can be taken.
    More generally, in ProMeLa, any statement s can serve as a guard, so a guard can have a side effect.
This can be modeled simply by putting s into the continuation of its premise. All statements except send and
receive (see below) are executable, their path condition simply becomes tt. This can be assumed even for send
and receive, because their execution is modeled by well-formedness constraints (see below), not by guards.
    A repetition loops infinitely over its body and executes any of the statements whose guard is true; in the
loop on the lines 12–15 of Figure 6, line 13 has an empty guard, which defaults to true. A repetition can only be
exited by break or goto statements (see below). The local evaluation of repetitions can be reduced to selection
in a similar manner as while is reduced to if in rule (9).

Jumps ProMeLa features a goto statement, whose argument is a label within the same process. Such un-
conditional jumps without a (process) context switch are easy to characterise semantically via continuations:

                        valσ (goto l) = {∅ ⊲ hσi · K(s)}      where s is the code following l .                     (40)
     The break statement is equivalent to a goto with an implicit label that points to the code after the repetition
it is contained in.

Atomic ProMeLa has an atomic statement16 , which works as in Section 5.2, except it may contain a guard
that can cause blocking. In this case, interleaving is possible. In case the guard g evaluates to true, statement s
is simply atomically executed according to rule (19).17 Otherwise, it puts the whole guarded atomic block into
a continuation, so that the guard can be re-evaluated later.

           valO,F
              σ   (atomic{:: g; s}) = {{valσ (g) = ff} ⊲ hσi · K(atomic{:: g; s})}
                                                                                                                    (41)
                                       ∪{{valσ (g) = tt}∪pc ⊲ τ · K( ) | pc⊲τ · K( ) ∈ valO,F
                                                                                          σ   (atomic(s))}

Channels In ProMeLa, the send and receive commands have the syntax seen in Figure 6: if c is a channel
identifier and e a list of expressions, then the current process uses c ! e to send the value of e to c. Dually, with
c ? e it receives e from c.18 In contrast to Definition 30 (Section 6), ProMeLa channels are explicitly declared,
and the address of a send (the origin of a receive) statement is not the recipient (sender) process, but a channel.
A message can be read by anyone who has access to the channel identifier it was sent to. In the case of globally
16
   Although ProMeLa permits loops to occur inside atomic, these are actually discouraged; if loops occur, they must
   always terminate.
17
   Rule (19) for unguarded atomic blocks ensures that the derived trace always ends with an empty continuation.
18
   ProMeLa allows either a variable, which is then set to the received value or an expression that is matched against it.
                                                                                                        LAGC Semantics    27

declared channels (line 1), this is any process. For locally declared channels the receiving process must have
received or declared the channel identifier.
   The semantics of ProMeLa’s send and receive can be modeled in analogy to Section 6.1, but one uses
send and receive events of the form sendEv p (e, c, i) and receiveEv p (e, c, i), respectively, where the address is a
channel.19

Well-formedness Only the first two rules of Definition 26 (with obvious adaptations) are needed, because there
are no method calls or dynamically created processes. On the other hand, the option of local channels requires
to model the visibility of channels. This can be done by well-formedness constraints of the following form:

          wf ch (sh y receiveEv p (e, c, i)) = wf (sh) ∧ (isLocal(p, c) ∨ isGlobal(c) ∨ receiveEv p (c, c′ , i) ∈ sh) .

    The predicate isLocal(p, c) holds if the process p declares a local channel named c, isGlobal(c) holds if channel
c is declared globally. These predicates can be easily checked by inspecting the code of a ProMeLa program.
The constraint expresses that each channel used in a receive statement in process p must be visible at that
point. This is the case if it is either global, or locally declared in p, or it was received earlier. There is a similar
constraint for send statements.
    There are two channel variants in ProMeLa: rendez-vous channels impose strictly synchronous communi-
cation. For those channels the well-formedness constraint in Definition 34 is used. The other channel type are
buffered channels with a capacity N > 0. These are characterised by the bound FIFO pattern in Definition 31.
    The standard ProMeLa semantics stipulates that received messages are consumed, i.e. they can be read
only once, which is ensured by the following constraint:
                                                                                            ′
                       wf (sh y receiveEv p (e, c, i)) = wf (sh)∧ 6 ∃ e′ , p′ . receiveEv p (e′ , c, i) ∈ sh .

   It is possible to change certain features of ProMeLa channels, for example, reception can be made non-
consumptive, out-of-order reception can be permitted, send and receive can be made non-blocking. All of these
can be characterised by suitable well-formedness constraints, but we refrain from spelling out details.

Synchronisation Channels, like guarded commands, are often used for synchronisation purposes in ProMeLa.
The receive statement on a buffered channel is only executable if it contains a message; one can only send to a
channel that is not full. Non-executable statements block a process until they become executable. In contrast
to guarded commands, no specific evaluation rule is required to model blocking senders and receivers, because
the correct communication order is already guaranteed by the well-formedness constraints.
    This consideration suggests that blocking guards might as well be modeled by suitable “waiting” events.
Indeed, this is possible, but less natural in that case.


7.2      Actors

We define a pure, object-based actor language based on the language in Section 6; Figure 7 shows the syntax.
There is a one-to-one mapping between objects and actors. Each actor has its own process with local memory
and executes calls to its methods with run-to-completion semantics (in consequence, non-terminating method
calls render an actor unresponsive). Each actor can only access its own local memory. The state of another actor
can only be modified via a method call.


                                      P ∈ Prog ::= CD sc
                               CD ∈ ClassDecl ::= class C {fd M }
                                M ∈ MethDecl ::= m(x) sc
                                  d ∈ VarDecl ::= ε | x; d
                                    sc ∈ Scope ::= {d atomic(s)}
                                      s ∈ Stmt ::= skip | x := rhs | if e { s } | x!m(e) | s; s
                                     rhs ∈ Rhs ::= e | new C (e)

                                    Fig. 7: Syntax of the Actor Language in Section 7.2
19
     In case one of the e is not a variable, but a match expression, the assignment in the local evaluation rule (34) has the
     variables occurring in e in its domain.
28                                   C. C. Din et al.

    In this actor language, a program P consists of a set of class declarations CD with a main block sc. Each
class has a name C, which also becomes the type of the class, with a sequence of field declarations fd and
method declarations M . Field declarations have the same syntax as local variable declarations d. For simplicity,
we let each method declaration associate a unique name m to a list of arguments x and a method body sc.
    A method body starts with local variable declarations followed by an atomic statement wrapping a sequence
of statements s. Recall from Section 5.2 that we excluded loops inside atomic, and thus exclude the while
statement from the syntax. This is no fundamental restriction, because actors may call each other and permit
unbounded recursion.
    The effect of atomic is to enforce a run-to-completion semantics. Rather than changing the semantics of the
programs discussed in Sections 3–6, we here make atomicity explicit. In most actor languages [22], the atomic
keyword is not used because actors are single threaded, and thus “locally atomic” by default.
    We extend the statements of WHILE, given in Figure 2, with asynchronous method calls x!m(e) on a caller
object x. The semantics of asynchronous calls combines the semantics of sending a message and a method call.
These calls are not blocking, so in the absence of futures or promises, there is no direct way to return a value
to the caller (return values via futures are modeled in Section 7.3 below).20 The right-hand side of assignments
includes expressions and new C (e). The latter creates a new actor object of class C with constructor arguments
e.
    In the following, let OId be a set of object identifiers with typical element o. We represent a program P
in terms of a global lookup table G: A set of triples each consisting of a class name with its field and method
declarations:
                        G = {hC, fd , m(x) sci | fd ∈ fields(C), m ∈ methods(C), C ∈ P } .
    In the above expression we use selector functions with obvious definitions: fields(C) returns the field names
of a class C, methods(C) returns the methods declared in a class C. We also define class(X), where X is either
an object identifier or a variable of type OId, that returns the class of X, as well as lookup(m, G) that returns
the declaration of a method with name m in G.


Local Evaluation When following the principle of local evaluation, we face the problem that a statement
s, which is locally evaluated, cannot possibly know the object it is running on. We address this issue in the
same manner as we dealt with unknown values before, i.e. by introducing a parameter O that is instantiated
during trace composition. Since this parameter must be instantiated consistently for all statements an object O
executes, it becomes a parameter of the semantic evaluation function, denoted valO σ (s), where O is a symbolic
variable. The evaluation function valO
                                     σ (s) produces the traces when s is running on object O; in particular, we
let valO
       σ (this) = O.
    The evaluation rule for new below introduces an event newEvσ (o, v) to capture that a new object o with
arguments v is created. Similar to Rule (36) that spawns a task, the local evaluation Rule (42) for object
creation creates a fresh symbolic variable X to represent the unknown object identity that is returned. Hence,
Rule (42) has an empty path condition, extends the trace by the new object creation event followed by an
updated state, where x is mapped to symbolic variable X and object fields are mapped to the constructor
arguments. We suppose that G is pre-populated with enough variables of each class. Consequently, Rule (42)
can pick a symbolic variable X that is fresh in σ and such that class(X) = C.

                   valO
                      σ (x := new C (e)) =
                              {∅ ⊲ newEvσ{X} (X, valO                                     O
                                                    σ (e)) y σ[x 7→ X, X 7→ ∗, X.fd 7→ valσ (e)] · K( )
                                                                                                                         (42)
                               | X 6∈ dom(σ), class(X) = C, fd ∈ fields(C)}
    Rule (43) for non-blocking asynchronous method calls is similar to Rule (24), but the invocation event
invEvσ (v, x, m, i) also includes the callee object x and a message identifier i ∈ MId. Thus, asynchronous method
calls can be viewed as a combination of procedure calls and message sending.

                          valO                            O         O
                             σ (x!m(e)) = {∅ ⊲ invEvσ (valσ (e), valσ (x), m, i) · K( )} | i ∈ MId}                      (43)

   The following rule evaluates the body of a method and corresponds to Rule (31) but adapted to a list of
arguments instead of a single one. The invocation reaction event inserted by the rule includes symbolic variables
20
     It is possible to pass the caller’s identity as a call argument, which the callee could then use to return a value to the
     caller’s state via a separate callback. But this does not give the caller a handle to access the result.
                                                                                                                  LAGC Semantics        29

which represent the method’s actual parameters, which are unknown in the local context. Since there are no
return values, it does not need to know the caller.

                    valO                          Z
                       σ (m(x) sc) = {∅ ⊲ invREvσ (Z, m, i) y σ[z 7→ Z, Z 7→ ∗] · K(sc[x ← z])                                         (44)
                                      | z, Z 6∈ dom(σ), i ∈ MId}


Trace Composition As explained above, the local evaluation is parameterised with the executing object O.
During trace composition, this parameter is instantiated by a concrete object identifier o. To associate events
with the object they originate from, traces are tagged with that object. This works exactly like the process
identifier tags in Definition 25 of Section 6.
   We use a mapping Ω into multisets of possible continuations like in Section 6, with the difference that its
domain is object identifiers instead of process identifiers. We use the same notation for multiset operations as
before.
   Trace composition in Rule (45) follows Rule (37) closely , with two small modifications: instead of process
identifiers, objects identifiers are used and the evaluation of the continuation s is performed on the object o,
where it is scheduled. The first two premises of the rule capture the scheduling decision to continue the trace
by executing task s on object o.

                                            o ∈ dom(Ω)       Ω[o] = q+{K(s)}
    σ = last(sh)         pc ⊲ τ · K(s′ ) ∈ valoσ (s)  ρ concretizes τ     ρ(pc) consistent                        wf (sh ∗∗ ρ(τ )o )
                                                                                                                                       (45)
                                         sh, Ω → sh ∗∗ ρ(τ ) , Ω[o 7→ q+{K(s′ )}]
                                                            o


    Likewise, Rule (46) exactly follows the pattern established with Rule (38). The rule picks a method m and
an object o, on which it is supposed to be executed. If that object is not yet in the domain of Ω, then we use
the notational convention Ω(o) = ∅. This corresponds to object creation. Either way, the method declaration
is evaluated on o. Observe that Rule (44) issues an invocation reaction event. Well-formedness ensures that
an invocation event of the form invEv(v, o, m, i) is present in sh that matches the message identifier, method
parameters, and callee.

                   lookup(m, G) = m(x) sc     σ = last(sh)      pc ⊲ τ · K(s′ ) ∈ valoσ (m(x) sc)
                          ρ concretizes τ   ρ(pc) consistent      wf (sh ∗∗ ρ(τ )o )
                                                                                                                                       (46)
                                  sh, Ω → sh ∗∗ ρ(τ ) , Ω[o 7→ Ω[o]+{K(s′ )}]
                                                     o




Well-formedness Well-formedness must essentially ensure two aspects:
    1. the uniqueness of events, for example, there is at most one newEv(o, _) per object, i.e. an object cannot
be created twice; 2. the event sequence related to a call to a method m on object o with parameters v has the
following form:
                                   ′′                           ′
                   ···     newEvo (o, v)       ···     invEvo (v ′ , o, m, i)       ···    invREvo (v ′ , m, i)       ···

where o′ and o′′ can be the same object. This is achieved with the equations in Figure 8 (we do not repeat the
first two lines of Definition 23, which are always assumed to be part of well-formedness).

                                                ′                                           ′′
                         wf (sh y newEvo (o, v)) = wf (sh)∧ 6 ∃o′′ , v ′ . newEvo (o, v ′ ) ∈ sh
                                    ′                                                      ′′
                     wf (sh y invEvo (v, o, m, i)) = wf (sh) ∧ ∃o′′ , v ′ .newEvo (o, v ′ ) ∈ sh ∧
                                                                                          ′′′
                                                      6 ∃o′′′ , v ′′ , o′′′′ , m′ . invEvo (v ′′ , o′′′′ , m′ , i) ∈ sh
                                      o′
                     wf (sh y invREv (v, m, i)) = wf (sh) ∧ ∃o.invEvo (v, o′ , m, i) ∈ sh ∧
                                                                                       ′′
                                                     6 ∃o′′ , v ′ , m′ . invREvo (v ′ , m′ , i) ∈ sh

                                        Fig. 8: Well-formedness for Actor language.




Global Trace Semantics
30                                  C. C. Din et al.

Definition 35 (Program Semantics for Actors). Given a finite program P with a lookup table G and
a main block main, i.e., Ωinit (omain ) = {K(main)}. Let σε denote the empty state, i.e. dom(σε ) = ∅. Let
sh0 , Ω0 → sh1 , Ω1 → · · · be a maximal sequence obtained by the repeated application of the composition rules
(Rules (45)–(46)), starting with21
                                          hσε i y newEvomain (omain , ε), Ωinit .
If the sequence is finite, then it must have the form

                                 hσε i y newEvomain (omain , ε), Ωinit → · · · → sh, Ω ,

where Ω (o) = ∅ for all o ∈ dom(Ω). If the sequence is infinite, let sh = limi→∞ shi . In either case, sh is a
trace of P . The set of all such traces is denoted with Tr(P, σε ).
   The new event at the start of a trace represents creation, by the system, of an initial object that runs the
main method. The well-formedness of events ensures that subsequently created objects will not erroneously be
the initial object, which is reserved for the code executed in the main method.

7.3     Active Objects
Active object languages [22] have a mechanism like futures or promises that provides a reference to the value
computed by an asynchronous method call. This makes it possible for a task to free its processor resource while
waiting for a result to be finished (so-called cooperative multi-tasking). We modify the syntax from Section 7.2
and introduce futures, a return statement, and get-expressions to retrieve the value stored in a future; the
resulting syntax is given in Figure 9. Note that the latter can block if this value is not yet available.


                      P ∈ Prog ::= CD sc
               CD ∈ ClassDecl ::= class C {fd M }
                M ∈ MethDecl ::= m(x) sc
                  d ∈ VarDecl ::= ε | x; d
                    sc ∈ Scope ::= {d s; return e}
                     g ∈ guard ::= e? | e
                      s ∈ Stmt ::= skip | x := rhs | if e { s } | while e { s } | this.m(e) | await g | s; s
                     rhs ∈ Rhs ::= e | new C (e) | x!m(e)| e.get

                                    Fig. 9: Syntax of Active Objects with Futures.


    We need to capture cooperative multi-tasking and the blocking of future access into the semantics. This
cannot be done with atomic, as in the previous section, because the suspending statements might occur nested
inside loops and recursive calls. It is more appropriate to switch to a semantics where a task runs to completion by
default, unless it suspends or blocks. As a consequence we will specify a semantics with finer-grained, explicitly
controlled interleaving between tasks. For this reason, we now consider both while-loops and synchronous
self-calls this.m(e) in the syntax.
    Task suspension takes place in await g statements, where the guard g suspends the execution of a task;
it works similarly to the guarded statements of Section 5.6. An await releases its object’s process, such that
other tasks may be executed. The execution of the statements following the guard can resume when the guard
evaluates to true. Even when the guard evaluates to true, the execution may be suspended. Guard expressions
either have the form x?, which synchronize with the future referenced by x receiving a value (the future thereby
gets resolved ), or they are Boolean expressions e.
    The second difference to the Actor language of Section 7.2 is that asynchronous method calls return values
to their associated future.22 The return statement terminates the execution of an asynchronous method and
returns its argument. The syntax enforces that the return statement is at the end of a method body. Asyn-
chronous method calls now appear on the right hand side of an assignment, the variable on the left is a future
associated with the call. The future’s value can be retrieved with get, whose argument expression must evaluate
to a future. To avoid blocking, one can precede x.get with await x?. Futures are first-class values and may be
passed as method arguments to other objects.
21
     Note that we denote by ε an empty list of method arguments.
22
     Obviously, synchronous calls can also be equipped with return values in a straightforward manner.
                                                                                                     LAGC Semantics    31

Local Evaluation For similar reasons as for objects in Section 7.2, we need to provide the future towards
whose value a local statement is contributing, as a parameter of the evaluation function. This future, sometimes
called the destiny of the executing code [23], cannot possibly be known locally. Hence, the form of the semantic
evaluation function becomes valO,F σ  (s), where F is a symbolic variable of type future with values in FId; the
evaluation function captures that s is running on object O and has destiny F . To keep track of the destiny, we
store it together with the continuations; in the configurations, continuations now take the form Kf (s).
    The rule for assignment with an asynchronous call on the right-hand side first emits an invocation event
invEv(e, o, m, f ), similar to Rule (43). The difference is that now the future F ′ , that is the destiny of the call,
must be recorded both in the left-hand-side variable on the left and in the invocation event. That future can
also be used to identify the call, thus replacing the message identifier. Since the value of F ′ cannot be known
locally, it is modeled as a fresh symbolic variable, similarly as in Rules (35)–(36).

                   valO,F
                      σ    (x := e!m(e′ )) =
                                     ′
                        {∅ ⊲ invEv{F
                                   σ
                                       }
                                         (valO,F
                                             σ   (e′ ), valO,F
                                                           σ   (e), m, F ′ ) y σ[x 7→ F ′ , F ′ 7→ ∗] · K( )          (47)
                             ′
                         | F 6∈ dom(σ)}

   To ensure that only futures with an available value are retrieved, we introduce new events compEvσ (f, v) and
compREvσ (f, v). These events denote the completion (the value of future f is available) and completion reaction
(the value of f is retrieved) of an asynchronous method. The evaluation rule for returning the completed result
simply inserts a completion event for the current future.

                               valO,F
                                  σ   (return e) = {∅ ⊲ compEvσ (F, valO,F
                                                                       σ   (e)) · K( )}                               (48)

   To retrieve the returned value stored in a future, Rule (49) inserts a completion reaction event and extends
the current state with a symbolic variable V that holds the as yet unknown return value.

                 valO,F
                    σ   (x := e.get) = {∅ ⊲ compREvσ{V } (valO,F
                                                             σ   (e), V ) y σ[x 7→ V, V 7→ ∗] · K( )
                                                                                                                      (49)
                                        | V 6∈ dom(σ)}

   The rule for evaluating a method body is similar to Rule (44), except that the future variable f of the freshly
running process is unified with the variable f of the invocation reaction event. It also must contain the (as yet
unknown) caller Y . Well-formedness of the trace containing invREv(X, Y, m, f ) will ensure that the f of the
invocation reaction is matched with the same f for a matching invocation event (see the definition of wf (sh)
below).
                valO,F
                   σ    (m(x) sc) =
                                       }
                     {∅ ⊲ invREvX∪{Y
                                   σ     (X, Y, m, F ) y σ[x′ 7→ X, X 7→ ∗, Y 7→ ∗] · K(sc[x ← x′ ])          (50)
                         ′
                      | x , X, Y 6∈ dom(σ)}
   For while-loops, we can use Rule (9). Rule (51) handles synchronous self-calls (no other synchronous calls
are considered here) by inlining the method body. It obtains the method declaration of m with body sc using
the auxiliary function lookup().and turns the formal parameters x into local variable declarations bound to the
argument values e. The entire statement sequence is wrapped into a scope for name disambiguation.

             valO,F
                σ   (this.m(e)) = valO,F
                                     σ   ({x; x := valO,F
                                                      σ   (e); sc}), where lookup(m, G) = m(x) sc                     (51)

   Suspended tasks are introduced by await statements. We only need to specify how to progress after an
await—the trace composition semantics will deal with actual task suspension by checking for the presence of
an await guard. There are two syntactically distinct cases. The first corresponds to a guarded command in
Rule (33), the second requires that the guarded future is resolved and thus introduces a completion reaction
event. This event must match a previous completion event involving the same future, which will be ensured by
well-formedness in the global rules.

                     valO,F
                        σ   (await e) = {{valσ (e) = tt} ⊲ hσi · K( )}
                                                                                                                      (52)
                    valO,F
                       σ   (await e?) = {∅ ⊲ compREv{V }  O,F
                                                    σ (valσ   (e), V ) · K( ) | V 6∈ dom(σ)}

Trace Composition We extend the continuations in the configuration with a future identifier that corresponds
to the future to be resolved by the considered task (thus, continuations take the form Kf (s)). With active objects,
there is no data-race among concurrent tasks, because each data item belongs to one single active object and
32                                   C. C. Din et al.

there is at most a single active task for each active object. One way to realize this in the semantics is to assign
a single process to each active object and make sure that among all the tasks of this process, only one is not
waiting for its turn. In other words, for each object identifier o, all continuations, except possibly one, are of
the form Kf (await g; s).
    We use the symbol Q to denote a multiset of suspended or empty continuations of the form Kf (await g; s)
or Kf ( ). The current global state of a program trace is represented by a mapping Σ from object identifiers to
multisets of continuations. For all object identifiers o, Σ[o] is either empty or of the form Q+{Kf (s)}, which
reflects that there is at most one active task. If s is of the form await g; s′ , then no task is currently executing
on object o and any task can be activated; otherwise, s must be the only continuation that can be executed
in object o. It is called the active task. The rewrite rule for empty trace simplification is extended to the new
continuations: Q + Kf ( )      Q. The trace composition rule closely follows Rule (45):
                                                  Σ[o] = Q+{Kf (s)}
                                 ′
     σ = last(sh)     pc ⊲ τ · K(s ) ∈ valo,f
                                          σ (s)       ρ concretizes τ     ρ(pc) consistent   wf (sh ∗∗ ρ(τ )o )
                                                                                                                  (53)
                                      sh, Σ → sh ∗∗ ρ(τ )o , Σ[o 7→ Q+{Kf (s′ )}]
    The main difference is that the global state has a different signature and the nature of Q enforces the
selection of the current task. Observe that this rule either evaluates the current active task or activates a new
task in o when there is no active task.
    Rule (54) follows Rule (46) except that the evaluation function is now tagged with a concrete future identity
f . The correctness of the concretisation is ensured by the well-formedness premise that requires an invocation
event of the form invEv(v, o, m, f ) to be present in sh. Note that we only run a new method if there is no active
task (Σ[o] = Q). Here, the destiny of the created thread is the future that was created during the evaluation of
the invocation event invEv(v, o, m, f ). As no other task is active, the method can start running immediately.23
                                                Σ[o] = Q
     lookup(m, G) = m(x) sc     σ = last(sh)    f ∈ FId      o ∈ OId     pc ⊲ τ · K(s′ ) ∈ valo,f
                                                                                              σ (m(x) sc)
                          ρ concretizes τ    ρ(pc) consistent    wf (sh ∗∗ ρ(τ )o )
                                                                                                                  (54)
                                      sh, Σ → sh ∗∗ ρ(τ )o , Σ[o 7→ Q+{Kf (s′ )}]
   This last rule can be triggered when Q is empty, i.e. when a newly created object handles its first invocation
or when an object has no task currently running.
Proposition 3. The property that Σ[o] contains at most one active task for any o ∈ OId is an invariant
preserved by applications of Rules (53)–(54).
Proof. When an object o is created, Σ[o] is empty. Every time one of the Rules (53)–(54) is applied to o, a
continuation is added to Σ[o]. As long as Σ[o] contains only suspended continuations, either rule can be applied
to o. Consequently, a suspended task on o can be activated or a new method invocation on o can start to be
executed. If there is one active task Kf (s) in Σ[o], only Rule (53) can be applied to o. In this case, execution
on o is forced by Rule (53) to continue with this specific K(s), i.e., the active task on o.
   The proposition guarantees that each object has at most one active task at any time. This captures the
semantics of sequential execution on an object between two suspension points.

Well-Formedness Compared to Section 7.2, well-formedness must reflect the life cycle of asynchronous method
calls with completion and completion reaction events to ensure that return values are not delivered and retrieved
too early:
                            ′′                     ′
                · · · newEvo (o, v) · · · invEvo (v ′ , o, m, f ) · · · invREvo (v ′ , o′ , m, f ) · · ·
                                                                       ′′′
                               · · · compEvo (f, v) · · · compREvo (f, v) · · ·
where o′ and o′′ can be the same object, and o′′′ can be any object except o. Up to tagging, the first four events
are unique in each trace, but not so the final completion reaction event. This is, because any object can retrieve
the value stored in a future as long as it possesses the future’s identifier.
    The fourth equation in Figure 10 is straightforward, because (i) a return can only be encountered after an
invocation reaction event, which is guaranteed to be unique by the third equation, and (ii) Rule (53) makes
sure that it is evaluated on the matching future and object.
    The final equation ensures the value of a future can only be fetched after the future is resolved.
23
     Running the method immediately allows us, for example, to encode a FIFO service policy by composing with the
     communication ordering rules of Section 6.2
                                                                                                                    LAGC Semantics             33

                                                    ′                                           ′′
                             wf (sh y newEvo (o, v)) = wf (sh)∧ 6 ∃o′′ , v ′ . newEvo (o, v ′ ) ∈ sh
                                         ′                                                     ′′
                        wf (sh y invEvo (v, o, m, f )) = wf (sh) ∧ ∃o′′ , v ′ .newEvo (o, v ′ ) ∈ sh ∧
                                                                                              ′′′
                                                         6 ∃o′′′ , v ′′ , o′′′′ , m′ . invEvo (v ′′ , o′′′′ , m′ , f ) ∈ sh
                                        o′                                           o    ′
                       wf (sh y invREv (v, o, m, f )) = wf (sh) ∧ invEv (v, o , m, f ) ∈ sh ∧
                                                                                              ′′
                                                          6 ∃o′′ , v ′ , o′′′ , m′ . invREvo (v ′ , o′′′ , m′ , f ) ∈ sh
                                             o
                             wf (sh y compEv (f, v)) = wf (sh)
                                                                                            ′
                           wf (sh y compREvo (f, v)) = wf (sh) ∧ ∃o′ , compEvo (f, v) ∈ sh

                                       Fig. 10: Well-Formedness for Actors with Futures.


Global Trace Semantics

Definition 36 (Program Semantics for Active Objects). Given a program P with a method table G and
a main block main, i.e., Σinit (omain ) = {Kfinit (main)}. Let σε denote the empty state, i.e. dom(σε ) = ∅. Let
sh0 , Σ0 → sh1 , Σ1 → · · · be a maximal sequence obtained by the repeated application of the composition rules
(Rules (53)–(54)), starting with
                                       hσε i y newEvomain (omain , ε), Σinit .
If the sequence is finite, then it must have the form

                                     hσε i y newEvomain (omain , ε), Σinit → · · · → sh, Σ ,

where Σ (o) = ∅ for all o ∈ dom(Σ). If the sequence is infinite, let sh = limi→∞ shi . In either case, sh is a
trace of P . The set of all such traces is denoted with Tr(P, σε ).

   The new event at the start of a trace represents the creation, by the system, of an initial object that runs
the main method. The well-formedness of events ensures that subsequently created objects will not erroneously
be the initial object, which is reserved for code executed in the main method.

Example 19. Consider the following program P :


    1   class C {                                                             7    { // main block
    2     m(n) {                                                              8      a; x; f ; y;
    3       n := n + 1;                                                       9      a := 1;
    4       return n;                                                        10      x := new C();
    5     }                                                                  11      f := x!m(a);
    6   }                                                                    12      await f ?;
                                                                             13      y := f .get;
                                                                             14    }



   Let the global lookup table G for this program be {hC, ε, m(n){n := n + 1; return n; }i}. In the following,
we use si to indicate the sequence of statements of a method body starting from line i.
   We first show the abstract local traces. The evaluation of the main method is as follows, where smain
represents the body in main, and s9 corresponds to smain [a ← a′ , x ← x′ , f ← f ′ , y ← y ′ ].

     valO,F
        σ   ({ a; x; f ; y; smain }) = {∅ ⊲ hσi y σ[a′ 7→ 0, x′ 7→ 0, f ′ 7→ 0, y ′ 7→ 0] · K({ s9 })
                                            | a′ , x′ , f ′ , y ′ ∈/ dom(σ)}
                   valσ ({ s9 }) = valO,F
                       O,F
                                              σ     (s 9 )
                  valO,F
                      σ     (a′ := 1) = {∅ ⊲ hσi y σ[a′ 7→ 1] · K( )}
          valO,F
             σ   (x′ := new C()) = {∅ ⊲ newEvσ{X} (X, ε) y σ[x′ 7→ X, X 7→ ∗] · K( )
                                            | X 6∈ dom(σ), class(X) = C}
                                                               ′
          valO,F
             σ   (f ′
                      :=  x  ′
                               !m(a ′
                                      )) = {∅ ⊲ invEv{F   σ
                                                                 }
                                                                   (valO,F
                                                                       σ   (a′ ), valO,F
                                                                                       σ   (x′ ), m, F ′ ) y σ[f ′ 7→ F ′ , F ′ 7→ ∗] · K( )
                                                ′
                                            | F 6∈ dom(σ)}
               valσ (await f ?) = {∅ ⊲ compREv{V
                  O,F              ′                                 }
                                                                  σ (valσ
                                                                           O,F
                                                                                (f ′ ), V ) y σ[V 7→ ∗] · K( ) | V 6∈ dom(σ)}
                O,F                                               {V }     O,F
            valσ (y := f .get) = {∅ ⊲ compREvσ (valσ (f ′ ), V ) y σ[y ′ 7→ V, V 7→ ∗] · K( )
                       ′        ′

                                            | V 6∈ dom(σ)}
34                                   C. C. Din et al.

The evaluation of the body of method m is shown below, where sc represents {n := n + 1; return n; } and s3
the content of the block sc[n ← n′ ].
                                                           ′
             valO,F
                σ   (m(n) sc) = {∅ ⊲ invREvσ{N,X,F } (N, X, m, F ′ )
                                    y σ[n′ 7→ N, N 7→ ∗, X 7→ ∗, F ′ 7→ ∗]·K(sc[n ← n′ ]) | n′ ,N,X,F ′6∈ dom(σ)}
                  O,F               O,F
               valσ ({ s3 }) = valσ (s3 )
           valO,F
              σ   (n′:= n′ +1) = {∅ ⊲ hσi y σ[n′ 7→ valO,F
                                                       σ   (n′ + 1)] · K( )}
              O,F                                    O,F
           valσ (return n ) = {∅ ⊲ compEvσ (F, valσ (n′ )) · K( )}
                            ′


   We now continue with the computation of a global concrete trace. Let IP be the initial state of P . We
consider the state where the statements in lines 8–9 have already been executed. At this point, the concrete
trace is sh = hIP i y [a′ 7→ 0, x′ 7→ 0, f ′ 7→ 0, y ′ 7→ 0] y σ with σ = [a′ 7→ 1, x′ 7→ 0, f ′ 7→ 0, y ′ 7→ 0], and the
mapping Σ is [omain 7→ {Kfmain (s10 )}]. Only Rule (53) is applicable:

                                       Σ[omain ] = {Kfmain (s10 )} σ = last(sh)
                        ∅ ⊲ newEvσ{X} (X, _) y σ[x′ 7→ X, X 7→ ∗] · K(s11 ) ∈ valoσmain ,fmain (s10 )
                                        ρ = [X 7→ om ] ∅ consistent wf (sh′ )                                       (55)

                                           sh, Σ → sh′ , Σ[omain 7→ {Kfmain (s11 )}]
where sh′ is the concrete trace

                         sh ∗∗ ρ(newEvσ{X} (X, ε) y σ[x′ 7→ X, X 7→ ∗])omain
                       = sh ∗∗ ρ(hσi y newEvσ{X} (X, ε) y σ[X 7→ ∗] y σ[x′ 7→ X, X 7→ ∗])omain
                       = hIP i y . . . y σ y newEvomain (om , ε) y σ y σ ′

with σ ′ = σ[x′ 7→ om ] = [a′ 7→ 1, x′ 7→ om , f ′ 7→ 0, y ′ 7→ 0].24 We must continue with s11 by applying Rule (53):

                                         Σ[omain ] = {Kfmain (s11 )} σ ′ = last(sh′ )
                                           ρ = [F ′ 7→ fm ] ∅ consistent wf (sh′′ )
                                      ′
                                   {F }
                        ∅ ⊲ invEvσ′ (1, om , m, F ′ ) y σ ′ [f ′ 7→ F ′ , F ′ 7→ ∗] · K(await f ′ ?; s13 )          (56)
                                omain ,fmain
                           ∈ valσ′           (s11 )
                                  sh′ , Σ → sh′′ , Σ[omain 7→ {Kfmain (await f ′ ?; s13 )}]
where sh′′ is the concrete trace
                                                  {F ′ }
                              sh′ ∗∗ ρ(invEvσ′ (1, om , m, F ′ ) y σ ′ [f ′ 7→ F ′ , F ′ 7→ ∗])omain
                            = hIP i y . . . y σ ′ y invEvomain (1, om , m, fm ) y σ ′ y σ ′′

with σ ′′ = σ ′ [f ′ 7→ fm ] = [a′ 7→ 1, x′ 7→ om , f ′ 7→ fm , y ′ 7→ 0].
    At this point, one could in principle choose to continue with the await statement in main with Rule (53)
or to start executing method m on object om with Rule (54). However, Rule (53) is not applicable, because it
does not result in a well-formed trace before method m returns. Therefore, we proceed with the second option:

                           Σ[om ] = ∅ lookup(m, G) = m(n) sc σ ′′ = last(sh′′ ) fm ∈ FId
                                   {N,X ′ ,F ′′ }
                      ∅ ⊲ invREvσ′′               (N, X ′ , m, F ′′ )
                          y σ ′′ [n′ 7→ N, N 7→ ∗, X ′ 7→ ∗, F ′′ 7→ ∗] · K({ s3 }) ∈ valσom
                                                                                           ′′
                                                                                              ,fm
                                                                                                  (m(n) sc)         (57)
                             ρ = [N 7→ 1, X ′ 7→ omain , F ′′ 7→ fm ] ∅ consistent wf (shm )
                                          sh′′ , Σ → shm , Σ[om 7→ {Kfm ({ s3 })}]
where the mapping Σ is updated to [omain 7→ {Kfmain (await f ?; s13 )}, om 7→ {Kfm ({ s3 })}], and shm is the
concrete trace
                                   {N,X ′ ,m,F ′′ }
                sh′′ ∗∗ ρ(invREvσ′′       (N, X ′ , m, F ′′ ) y σ ′′ [n′ 7→ N, N 7→ ∗, X ′ 7→ ∗, F ′′ 7→ ∗])om
                                          om
                                 ′′
              = hIP i y . . . y σ y invREv (1, omain , m, fm ) y σ ′′ y σm

with σm = σ ′′ [n′ 7→ 1].
24
     We simplify the states in the concrete trace by removing the symbolic variables once they are instantiated.
                                                                                                          LAGC Semantics     35

    We have to continue with { s3 } from the method m. Executing n′ := n′ + 1 in s3 updates σm to σm                    ′
                                                                                                                          =
             o  ,f
σm [n′ 7→ valσmm
                  m
                    (n ′
                         + 1)] = [a ′
                                      →
                                      7 1, x′
                                              →
                                              7  om  , f ′
                                                           →
                                                           7  f m , y ′
                                                                        →
                                                                        7 0,  n ′
                                                                                   →
                                                                                   7 2], which extends the concrete trace to
sh′m as follows:
                                                                            ′
                                                hIP i y . . . y σm y σm          .
We proceed with the return statement in method m by applying Rule (53) once again:

                                   Σ[om ] = {Kfm (return n′ )} σm   ′
                                                                      = last(sh′m )
                                                  om ,fm
                ∅ ⊲ compEvσm
                           ′ (fm , 2) · K( ) ∈ valσ ′
                                                   m
                                                         (return n ) ρ = [] ∅ consistent wf (sh′′m )
                                                                  ′
                                                                                                                            (58)
                                                  sh′m , Σ → sh′′m , Σ[om 7→ ∅]
where Σ[om 7→ ∅] is the result of simplifying Σ[om 7→ ∅ + Kfm ( )]. The resulting concrete trace sh′′m is:

                                        sh′m ∗∗ ρ(compEvσm ′ (fm , 2))
                                                                      om
                                                       ′            om        ′
                                      = hIP i y . . . σm y compEv (fm , 2) y σm .

    The mapping Σ is now updated to [omain 7→ {Kfmain (await f ′ ?; s13 )}, om 7→ ∅]. Executing the await
statement in main at this point produces a well-formed trace by Rule (53):

                             Σ[omain ] = {Kfmain (await f ′ ?; s13 )} σm ′
                                                                             = last(sh′′m )
                              {V }
                   ∅ ⊲ compREvσm
                               ′
                                                ′
                                   (fm , V ) y σm [V 7→ ∗] · K(s13 ) ∈ valoσmain
                                                                            ′
                                                                                  ,fmain
                                                                                         (await f ′ ?; s13 )
                                        ρ = [V 7→ 2] ∅ consistent wf (sh )
                                                                            m
                                                                              ′′′                                           (59)

                                         sh′′m , Σ → sh′′′ , Σ[omain 7→ {Kfmain (s13 )}]
with the concrete trace sh′′′ :
                                                         {V }
                                sh′′m ∗∗ ρ(compREvσm′  (fm , V ) y σm  ′
                                                                         [V 7→ ∗])omain
                                                 ′              omain              ′     ′
                              = hIP i y . . . y σm y compREv          (fm , 2) y σm   y σm .
                 ′                                   ′
The final state σm  is actually a simplification of σm [V 7→ 2] by removing the concretised symbolic variable V
                        ′
and thus identical to σm  .
   Finally, we execute the get statement, again by Rule (53):
                                                                          ′
                                    Σ[omain ] = {Kfmain (s13 )} σm             = last(sh′′′ )
                        {V ′ }     omain ,fmain
             ∅ ⊲ compREvσm
                         ′     (valσm
                                    ′           (f ), V ′ ) y σm
                                                               ′
                                                                 [y ′ 7→ V ′ , V ′ 7→ ∗] · K( ) ∈ valoσmain
                                                                                                       ′
                                                                                                            ,fmain
                                                                                                                   (s13 )
                                         ρ = [V ′ 7→ 2] ∅ consistent wf (shP )
                                                                                                       m
                                                                                                                            (60)

                                                sh′′′ , Σ → shP , Σ[omain 7→ ∅]
which results the mapping Σ = [omain 7→ ∅, om 7→ ∅], and produces the concrete trace shP :
                                     {V ′ }
              sh′′′ ∗∗ ρ(compREvσm   ′ (valoσmain
                                               ′
                                               m
                                                  ,fmain
                                                         (f )}, V ′ ) y σm
                                                                         ′
                                                                           [y ′ 7→ V ′ , V ′ 7→ ∗])omain
            = hIP i y [a′ 7→ 0, x′ 7→ 0, f ′ 7→ 0, y ′ 7→ 0] y σ y newEvomain (om , _) y σ y σ ′
              y invEvomain (1, om , m, fm ) y σ ′ y σ ′′ y invREvom (1, omain , m, fm ) y σ ′′ y σm y σm ′

              y compEvom (fm , 2) y σm    ′
                                              y compREvomain (fm , 2) y σm        ′
                                                                                    y σm   ′

              y compREvomain (fm , 2) y σm      ′
                                                  y σP

with σP = [a′ 7→ 1, x′ 7→ om , f ′ 7→ fm , y ′ 7→ 2, n′ 7→ 2].


ABS ABS is an actor-based executable modeling language [49,34,2] that falls in the class of Active Object
languages [22]. ABS is closely related to the language in Figure 9. Before we make this relation precise, we
mention the main features of ABS that have not been discussed in this paper:

Functional Expressions ABS lets the user declare algebraic datatypes and provides a pure, functional lan-
   guage with pattern matching over these. An evaluation semantics for such a language is standard [57]. It is
   easily incorporated into states and their evaluation.
Interfaces ABS supports multiple implementations of interfaces, but no inheritance or dynamic dispatch. It
   is sufficient to equip the lookup table G with suitable selectors.
36                               C. C. Din et al.

Modules, Traits ABS has a simple module system. Modules do not have an operational semantics, but manage
   the name space. One can remove them by replacing relative with absolute names. ABS supports code reuse
   via traits: sets of method declarations that can be added to a class via a uses clause. Like modules, traits
   can be assumed to have been resolved.
Error Handling ABS can throw and catch exceptions. The semantics of the corresponding statements is a
   combination of the case distinction rule (8) and the local jump rule (40). The design of the corresponding
   local evaluation rules is left as an exercise.
   Otherwise, ABS is identical to the Active Object language discussed in the present section. Specifically, ABS
tasks are atomic by default. Their execution is only suspended explicitly, either at the end of a method, or with
a suspend statement (equivalent to “ await true”), or by await g.


8    Related Work
We position our work within denotational semantics. The discussion focuses on three different strands of work
on trace semantics: Semantics based on execution traces, on communication traces, and on hybrid traces com-
bining execution states and communication events. To first motivate the use of traces semantics, we start by
drawing some lines from state-transformer semantics. We then consider related work on execution traces and
communication traces. We finally discuss related work on hybrid traces, combining these directions.

State-transformer semantics. State-transformer semantics explain a program statement as a transition from one
program state to another [42,9]. This style of semantics elegantly hides intermediate states in the transition,
thereby providing an abstraction from the inner, intermediate states visited in the actual execution of state-
ments. State-transformer semantics is fully abstract for sequential while-programs, resulting in a compositional
semantics with respect to, for example, partial correctness behavior. However, for parallel shared-variable lan-
guages the final outcome of a program may depend on the scheduling of the different atomic sections, leading to
non-deterministic behavior. For a parallel statement, the state transformer that results from the parallel compo-
sition of component statements cannot be determined from the transformer for these statements alone [58,16].
Hence, state-transformer semantics for parallel languages are not compositional; it is necessary to capture the
intermediate states at which interleaving may occur. Mosses observes [58] that by capturing these intermediate
states as so-called resumptions [39], the resulting denotational semantics corresponds much more closely to
operational semantics [64].
    Early work on verification of concurrent systems extended state-transformer semantics with additional side-
conditions, and is as such non-compositional; for example, interference freedom tests were used for shared
variable concurrency [63] and cooperation tests for synchronous message passing [10]. Compositional approaches
were introduced for shared variables in the form of rely-guarantee [50] and for synchronous message passing
in the form of assumption-commitment [56]. Extending these principles for compositional verification, object
invariants can be used to achieve modularity (for example, [46]).

Execution traces The use of execution traces to describe program behavior can be motivated by the need for
additional structure in the semantics of statements, such that parallel statements can be described composition-
ally from the semantics of their components. Brookes developed a trace semantics for a shared-variable parallel
language based on transition traces [16]. In his work, a command is described by a sequence of state transformers
reflecting the different atomic blocks in the execution of the command, but abstracting from the inner states of
these blocks. Transition traces are thus more abstract than resumptions that are discussed above. The semantics
of parallel commands then corresponds to the union of these segments, obtained by stitching together the state
transitions corresponding to the different atomic sections in different ways. Brookes shows that this semantics,
which can be realised at different levels of granularity, is fully abstract. In fact, we considered this solution in
our work, but decided against it because it constructs infinitely large mathematical objects in order to include
all possible states in which the next atomic block can start. Instead, we opted for continuation markers, to be
resolved in the composition, as well as symbolic traces that are concretised on demand during the composition
phase. This ensures that all semantic elements are finite, which makes the LAGC semantics easy and effective
to compute.

Communication traces Communication traces first appeared in the object-oriented setting [21] and then for
CSP [43]. Soundararajan developed an axiomatic proof system for CSP using histories and projections [66],
which was compositional and removed the need for cooperation tests. Zwiers developed the first sound and
                                                                                           LAGC Semantics        37

complete proof system using communication traces [70]. Jeffrey and Rathke introduced a semantics for object-
oriented programs based on communication traces, and showed full abstraction for testing equivalence [47,48].
Reasoning about asynchronous method calls and cooperative scheduling using histories was first done for Creol
[31] and later adapted to Dynamic Logic [5]. Din introduced a proof system based on four communication events,
significantly simplifying the proof rules [26], and extended the approach to futures [28,29]. This four-event proof
system, which forms the basis for KeY-ABS [25], was the starting point for the communication events used in
our paper. This way, communication events can always be local to one semantic object, and their ordering is
captured by well-formedness predicates. Compared to this line of work, we introduce continuation markers and
locally symbolic traces. This allows us to constructively derive global traces, in contrast to, for example, Din’s
work which, building on Soundararajan’s work, simply eliminates global traces which do not project correctly
to the local trace sets of the components.

Hybrid traces. Brookes’ action traces [17] bear some similarity to our work. He aims at denotational seman-
tics using collecting semantics, explicitly represents divergence, synchronises communication using events, and
captures parallel execution of two components by means of a so-called mutex fairmerge which ensures that
both components get the chance to be executed. Action traces were used to develop a semantics for concurrent
separation logic [15], where scheduling is based on access to shared resources with associated invariants and data
races are exposed. Brookes’ work elegantly develops a trace semantics for low-level programming mechanisms
with lock resources. However, it does not cover the dynamic spawning of processes, procedure calls, method in-
vocations, and similar topics covered in our work, which led to the locally abstract, globally concrete formulation
of hybrid trace semantics. In previous work [27] we used scheduling events and well-formedness properties over
scheduling events to capture all legal interleavings among concurrent objects at a granularity similar to that of
action traces. In contrast, parallel execution in the present paper is based on a more fine-grained interleaving of
processes, exploiting continuations, by means of different composition rules (for example, (53) and (54)) to cap-
ture global and local interleaving of processes. The approach of Brookes [17,27] is easily expressible within our
framework. We obtain the equivalent of the fairmerge operator by collecting all traces that can be constructed
by the composition rules from a given concrete initial state.
    In trace semantics, the composition of traces from parallel executions can be formalised in different ways;
e.g., as continuation semantics, erasure semantics or collecting semantics. We have opted for the first approach
and captured the interleaved execution by means of local continuations, such that the global trace is obtained by
gradually unfolding traces that correspond to local execution by means of continuations. Kamburjan has explored
erasure semantics in a hybrid trace semantics developed as a foundation for behavioral program logic [52,51];
this work uses an explicit representation of the heap which is exploited for composition by introducing a fresh
symbolic heap as a local placeholder for execution in other objects at the scheduling points. The introduction
of fresh symbolic states for merging local behaviors can equivalently be replaced by a set collecting all possible
concrete states after the scheduling point, such that the composition of local behaviors can be done by selecting
the appropriate, compatible concrete traces rather than by instantiating a symbolic trace. This approach has
been studied in the context of hybrid trace semantics in [53].
    Recent work [6] on similar communication structures for ASP/ProActive uses parameterised labelled tran-
sition systems with queues to model interaction with futures in a fine-grained, operational manner. In contrast,
our work with traces allows futures to be abstracted into communication events and well-formedness conditions.
We are unaware of previous work on programming language semantics that captures different communication
patterns as well-formedness constraints over trace semantics; these constraints are in fact orthogonal to the
building blocks of the trace semantics and allow to study language behavior ranging over architectures that
support different forms of communication within a single semantic framework.
    More recently, [68] [68] defined a data structure called interaction trees that enable a denotational and
somehow functional definition of the semantics for imperative programs where interaction trees encode the
interaction with the environment. An interaction tree constitutes a form of trace that expresses the effects
of the program but abstract away from states. The authors provide co-inductive principles for reasoning on
diverging programs, which is more precise than our current handling of infinite traces. Their semantics can be
considered as more compositional than ours, because no concretisation is needed, but the approach is only valid
for sequential programs.
    The pure trace-based proof system of ABS [28,29] requires strong hiding of local state: the state of other
objects can only be accessed through method calls, so shared state is internal and controlled by cooperative
scheduling. Consequently, specifications can be purely local. More expressive specifications require significantly
more complex proof systems, for example modifies clauses in Boogie [46], fractional permissions [40] in Chal-
ice [55], or dynamic frames in KeY [59]. To specify fully abstract interface behavior these systems need to simulate
38                               C. C. Din et al.

histories in an ad hoc manner, see [46, Figure 1]. A combination of permission-based separation logic [7] and
histories has recently been proposed for modular reasoning about multi-threaded concurrency [69]. The motiva-
tion for our work stems from our aim to devise compositional proof systems to verify protocol-like behavior for
object-oriented languages [27] by combining communication histories for ABS with the trace modality formulas
of Nakata et al. [60,18].


9     Future Work and Conclusion
9.1     Future Work
The original motivation for the present work was to create a modular semantics that aligns well with the kind
of program logics used in deductive verification [35]. In Sections 4 and 5 we reached this goal by providing a
program logic and calculus for the shared variable language and by giving a compact soundness proof (Thm. 1)
for the sequential fragment. This result can and should be extended to a state-of-art calculus for the language
in Section 7.3 [53].
    An obvious direction for future work is to fully mechanize the LAGC semantics in a proof assistant [61,14]. In
fact, all definitions and theorems from Sections 2, 3, and 5 have been mechanized and proven25 in Isabelle/HOL.
The mechanization is executable in the sense that all traces in the examples of the mentioned sections can be
generated automatically from the HOL theories. We plan to extend the Isabelle/HOL mechanization to cover
also Sections 6, 7.2, and 7.3.
    In Sections 5–7 we showed that a wide variety of parallel programming concepts can be formalised in LAGC
style with relative ease. It would be interesting to explore how far this can be carried. On the one hand, one could
try to formalise the semantics of a major programming language, such as Java or C. On the other hand, one
could try to apply the LAGC framework to weakly consistent memory models [3] or to the target the language of
concurrent separation logic [15]. A further possible extension concerns programs with non-terminating, atomic
segments, see Section 5.2. A mechanized, executable LAGC semantics opens the possibility of early prototyping
new semantics of concurrent and distributed languages with relative ease.
    We rely heavily on well-formedness of traces, but we did not discuss how to define properties on possibly
infinite sets of infinite traces with events, for example, notions related to fairness. This is a complementary
problem to trace generation, and not the focus of the present paper.
    Our approach makes composition of local rules easy, and extension of the language straightforward. Global
trace composition on the contrary relies on well-formedness criteria for the whole trace; even if this criteria
is defined modularly, it is not compositional in the sense that a trace can become invalid by extension of the
criteria or parallel composition. This is often unavoidable because the semantics of many concurrent models
like CCS and π-calculus are by nature very much sensitive to the execution context. However, depending on
the language and the form of concurrency, different compromises could be found, defining a greater part of
the concurrent semantics in a symbolic and compositional way. For example our semantics of futures is similar
to message passing but one could probably specify new composition tools that better take into account the
single-assignment property ensured by futures.

9.2     Conclusion
The semantics of concurrent programming languages is inherently a technically demanding subject. In the best
case, a formal semantics can illuminate the design space created by the choice of different concurrency concepts,
it shows the consequences of these choices, and it makes different version comparable. This is only possible
in a semantic framework that enforces uniform and modular definitions, and it is what we strove to achieve
with LAGC: the central design decision is to strictly separate local, sequential computations and their parallel
composition. Also, we decided to render local evaluations abstract. In this way, one and the same schematic
semantic evaluation rule can be re-used for any initial state, executing processor, and destiny of the result.
While abstract local rules are not a theoretical necessity, they drastically simplify the complexity of definitions.
    A central technical problem to address in a locally-globally divided setup is to ensure that enough context
information is available when composing concurrent behavior. Instead of computing all possible states, in which
an atomic segment can continue, we pass the remaining code to be executed as a continuation. Again, this
constitutes a considerable technical simplification compared to the former option. For example, in Section 7.3
we characterised the behavior of active objects concisely with a suitable definition of a continuation pool.
25
     See https://gitlab.com/Niklas_Heidler/mechanization-of-lagc-semantics-in-isabelle and [38].
                                                                                             LAGC Semantics         39

    But mere continuation is not sufficient: one needs to orchestrate different local evaluations within a global
trace, for example, to ensure a method is called before it is being executed. This is achieved by suitable events
emitted during local evaluation. Orchestration of local computations by events leads to a further separation of
concerns: many concurrency models can be characterised in a declarative manner by well-formedness of events
inside traces, as shown in Section 6.2.
    We believe the achieved separation of concerns, locally abstract evaluation—trace composition with a contin-
uation pool—orchestration of computations by well-formedness, provides a flexible and usable semantic frame-
work to formalise and compare concurrent languages in. It is close modern deductive verification calculi and
could even be fully mechanised.

Acknowledgment
We would like to thank the following people for carefully reading drafts of this paper and for spotting several
omissions, errors, typos, and inaccuracies: Lukas Grätz, Dilian Gurov, Niklas Heidler, Eduard Kamburjan, and
Marco Scaletta.


References
 1. Jean-Raymond Abrial. The B Book: Assigning Programs to Meanings. Cambridge University Press, Cambridge, UK,
    August 1996.
 2. ABS Development Team. ABS Documentation, 1.9.1 edition, January 2018. https://abs-models.org/manual.
 3. Sarita V. Adve and Mark D. Hill. A unified formalization of four shared-memory models. IEEE Trans. Parallel
    Distributed Syst., 4(6):613–624, 1993.
 4. Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, Reiner Hähnle, Peter H. Schmitt, and Mattias Ulbrich, editors.
    Deductive Software Verification - The KeY Book - From Theory to Practice, volume 10001 of LNCS. Springer-Verlag,
    Cham, Switzerland, 2016.
 5. Wolfgang Ahrendt and Maximilian Dylla. A system for compositional verification of asynchronous objects. Science
    of Computer Programming, 77(12):1289–1309, 2012.
 6. R. Ameur-Boulifa, L. Henrio, O. Kulankhina, E. Madelaine, and A. Savu. Behavioural semantics for asynchronous
    components. J. Logical and Algebraic Methods in Programming, 89:1–40, June 2017.
 7. Afshin Amighi, Christian Haack, Marike Huisman, and Clément Hurlin. Permission-based separation logic for
    multithreaded Java programs. LMCS, 11:1–66, 2015.
 8. Gregory Andrews. Multithreading, parallel, and concurrent programming. Addison-Wesley, One Jacob Way, Reading,
    MA 01867-3999, 2nd edition, 1999.
 9. Krzysztof R. Apt, Frank S. de Boer, and Ernst-Rüdiger Olderog. Verification of Sequential and Concurrent Programs.
    Texts in Computer Science. Springer, Heidelberg, 2009.
10. Krzysztof R. Apt, Nissim Francez, and Willem P. de Roever. A proof system for communicating sequential processes.
    ACM Transactions on Programming Languages and Systems, 2(3):359–385, 1980.
11. M. Balser, W. Reif, G. Schellhorn, K. Stenzel, and A. Thums. Formal system development with KIV. In T. Maibaum,
    editor, Fundamental Approaches to Software Engineering, volume 1783 of LNCS, pages 363–366, Heidelberg, 2000.
    Springer.
12. Bernhard Beckert and Daniel Bruns. Dynamic logic with trace semantics. In Maria Paola Bonacina, editor, Automated
    Deduction, 24th International Conference on Automated Deduction, Lake Placid, USA, volume 7898 of LNCS, pages
    315–329, Heidelberg, 2013. Springer.
13. Mordechai Ben-Ari. Principles of the Spin Model Checker. Springer, Heidelberg, 2008.
14. Yves Bertot and Pierre Castéran. Interactive Theorem Proving and Program Development—Coq’Art: The Calculus
    of Inductive Constructions. Texts in Theoretical Computer Science. An EATCS Series. Springer, Berlin Heidelberg,
    2004.
15. Stephen Brookes. A semantics for concurrent separation logic. Theor. Comput. Sci., 375(1-3):227–270, 2007.
16. Stephen D. Brookes. Full abstraction for a shared-variable parallel language. Inf. Comput., 127(2):145–163, 1996.
17. Stephen D. Brookes. Traces, pomsets, fairness and full abstraction for communicating processes. In Lubos Brim, Petr
    Jancar, Mojmír Kretínský, and Antonín Kucera, editors, Proc. 13th Intl. Conf. on Concurrency Theory (CONCUR
    2002), volume 2421 of LNCS, pages 466–482, Berlin Heidelberg, 2002. Springer.
18. Richard Bubel, Crystal Chang Din, Reiner Hähnle, and Keiko Nakata. A dynamic logic with traces and coinduc-
    tion. In Hans De Nivelle, editor, Intl. Conf. on Automated Reasoning with Analytic Tableaux and Related Methods,
    Wroclaw, Poland, volume 9323 of LNCS, pages 303–318, Cham, Switzerland, 2015. Springer.
19. Rod M. Burstall. Program proving as hand simulation with a little induction. In Information Processing ’74, pages
    308–312. Elsevier/North-Holland, Amsterdam, 1974.
20. Bernadette Charron-Bost, Friedemann Mattern, and Gerard Tel. Synchronous, asynchronous, and causally ordered
    communication. Distributed Computing, 9(4):173–191, 1996.
40                                C. C. Din et al.

21. Ole-Johan Dahl. Can program proving be made practical? In M. Amirchahy and D. Néel, editors, Les Fondements
    de la Programmation, pages 57–114. Institut de Recherche d’Informatique et d’Automatique, Toulouse, France,
    December 1977.
22. Frank de Boer, Crystal Chang Din, Kiko Fernandez-Reyes, Reiner Hähnle, Ludovic Henrio, Einar Broch Johnsen,
    Ehsan Khamespanah, Justine Rochas, Vlad Serbanescu, Marjan Sirjani, and Albert Mingkun Yang. A survey of
    active object languages. ACM Computing Surveys, 50(5):76:1–76:39, October 2017. Article 76.
23. Frank S. de Boer, Dave Clarke, and Einar Broch Johnsen. A complete guide to the future. In Rocco De Nicola,
    editor, Proceedings of the 16th European Symposium on Programming, (ESOP 2007), volume 4421 of LNCS, pages
    316–330, Berlin, Heidelberg, 2007. Springer-Verlag.
24. Edsger W. Dijkstra. Guarded commands, nondeterminacy and formal derivation of programs. Commun. ACM,
    18(8):453–457, 1975.
25. Crystal Chang Din, Richard Bubel, and Reiner Hähnle. KeY-ABS: A deductive verification tool for the concurrent
    modelling language ABS. In Amy Felty and Aart Middeldorp, editors, Proc. 25th Intl. Conf. on Automated Deduction
    (CADE), Berlin, Germany, volume 9195 of LNCS, pages 517–526, Cham, 2015. Springer.
26. Crystal Chang Din, Johan Dovland, Einar Broch Johnsen, and Olaf Owe. Observable behavior of distributed systems:
    Component reasoning for concurrent objects. Journal of Logic and Algebraic Programming, 81(3):227–256, 2012.
27. Crystal Chang Din, Reiner Hähnle, Einar Broch Johnsen, Violet Ka I Pun, and Silvia Lizeth Tapia Tarifa. Locally
    abstract, globally concrete semantics of concurrent programming languages. In Cláudia Nalon and Renate Schmidt,
    editors, Proc. 26th Intl. Conf. on Automated Reasoning with Tableaux and Related Methods, volume 10501 of LNCS,
    pages 22–43, Cham, Switzerland, September 2017. Springer.
28. Crystal Chang Din and Olaf Owe. A sound and complete reasoning system for asynchronous communication with
    shared futures. J. Log. Algebraic Methods Program., 83(5–6):360–383, 2014.
29. Crystal Chang Din and Olaf Owe. Compositional reasoning about active objects with shared futures. Formal Aspects
    of Computing, 27(3):551–572, 2015.
30. Crystal Chang Din, Silvia Lizeth Tapia Tarifa, Reiner Hähnle, and Einar Broch Johnsen. History-based specification
    and verification of scalable concurrent and distributed systems. In Michael Butler, Sylvain Cochon, and Fatiha Zaïdi,
    editors, Proc. 17th International Conference on Formal Engineering Methods, ICFEM, Paris, volume 9407 of LNCS,
    pages 217–233, Cham, Switzerland, 2015. Springer-Verlag.
31. Johan Dovland, Einar Broch Johnsen, and Olaf Owe. Verification of concurrent objects with asynchronous method
    calls. In Proc. IEEE Intl. Conference on Software Science, Technology & Engineering(SwSTE’05), pages 141–150,
    Los Alamitos, CA, February 2005. IEEE Computer Society Press.
32. Patrice Godefroid. Model checking for programming languages using Verisoft. In Peter Lee, Fritz Henglein, and
    Neil D. Jones, editors, Proc. 24th Symp. on Principles of Programming Languages (POPL), pages 174–186, New
    York, NY, 1997. ACM.
33. Patrice Godefroid. Test generation using symbolic execution. In Deepak D’Souza, Telikepalli Kavitha, and Jaiku-
    mar Radhakrishnan, editors, IARCS Annual Conference on Foundations of Software Technology and Theoretical
    Computer Science, FSTTCS, Hyderabad, India, volume 18 of LIPIcs, pages 24–33, Schloss Dagstuhl, 2012. Leibniz-
    Zentrum fuer Informatik.
34. Reiner Hähnle. The Abstract Behavioral Specification language: A tutorial introduction. In Marcello Bonsangue,
    Frank de Boer, Elena Giachino, and Reiner Hähnle, editors, International School on Formal Models for Components
    and Objects: Post Proceedings, volume 7866 of LNCS, pages 1–37, Cham, Switzerland, 2013. Springer.
35. Reiner Hähnle and Marieke Huisman. Deductive verification: from pen-and-paper proofs to industrial tools. In Bern-
    hard Steffen and Gerhard Woeginger, editors, Computing and Software Science: State of the Art and Perspectives,
    volume 10000 of LNCS, pages 345–373. Springer, Cham, Switzerland, 2019.
36. Joseph Y. Halpern, Zohar Manna, and Ben C. Moszkowski. A hardware semantics based on temporal intervals.
    In Josep Díaz, editor, Automata, Languages and Programming, 10th Colloquium, Barcelona, Spain, volume 154 of
    LNCS, pages 278–291, Berlin, Heidelberg, 1983. Springer.
37. David Harel, Dexter Kozen, and Jerzy Tiuryn. Dynamic Logic. Foundations of Computing. MIT Press, Boston, MA,
    USA, October 2000.
38. Niklas Heidler. Mechanization of LAGC semantics in Isabelle. Bachelor thesis, Technical University of Darmstadt,
    Department of Computer Science, November 2021.
39. Matthew Hennessy and Gordon D. Plotkin. Full abstraction for a simple parallel programming language. In Jirí
    Becvár, editor, Proc. 8th Symposium on the Mathematical Foundations of Computer Science, volume 74 of LNCS,
    pages 108–120, Heidelberg, 1979. Springer.
40. Stefan Heule, K.Rustan M. Leino, Peter Müller, and AlexanderJ. Summers. Abstract read permissions: Fractional
    permissions without the fractions. In Roberto Giacobazzi, Josh Berdine, and Isabella Mastroeni, editors, Verification,
    Model Checking, and Abstract Interpretation, volume 7737 of LNCS, pages 315–334. Springer, Berlin Heidelberg, 2013.
41. Carl Hewitt, Peter Boehler Bishop, and Richard Steiger. A universal modular ACTOR formalism for artificial
    intelligence. In Nils J. Nilsson, editor, Proc. 3rd Intl. Joint Conf. on Artificial Intelligence. Standford, CA, USA,
    pages 235–245, San Francisco, CA, USA, 1973. William Kaufmann.
42. C. A. R. Hoare. An axiomatic basis for computer programming. Comm. of the ACM, 12(10):576–580, 583, October
    1969.
                                                                                             LAGC Semantics         41

43. C. A. R. Hoare. Communicating Sequential Processes. International Series in Computer Science. Prentice Hall,
    Upper Saddle River, NJ, 1985.
44. Gerard J. Holzmann. The SPIN Model Checker. Pearson Education, Boston, MA, USA, 2003.
45. Michael Huth and Mark Ryan. Logic in Computer Science: Modelling and Reasoning about Systems. Cambridge
    University Press, Cambridge, UK, 2nd edition, 2004.
46. Bart Jacobs, Frank Piessens, K. Rustan M. Leino, and Wolfram Schulte. Safe concurrency for aggregate objects with
    invariants. In Bernhard K. Aichernig and Bernhard Beckert, editors, Third IEEE Intl. Conf. on Software Engineering
    and Formal Methods (SEFM 2005), pages 137–147, Los Alamitos, CA, 2005. IEEE Computer Society.
47. Alan Jeffrey and Julian Rathke. A fully abstract may testing semantics for concurrent objects. Theor. Comput. Sci.,
    338(1-3):17–63, 2005.
48. Alan Jeffrey and Julian Rathke. Java Jr: Fully abstract trace semantics for a core java language. In Shmuel Sagiv,
    editor, Proc. 14th European Symposium on Programming (ESOP 2005), volume 3444 of LNCS, pages 423–438, Berlin
    Heidelberg, 2005. Springer.
49. Einar Broch Johnsen, Reiner Hähnle, Jan Schäfer, Rudolf Schlatte, and Martin Steffen. ABS: A core language for
    abstract behavioral specification. In Bernhard K. Aichernig, Frank de Boer, and Marcello M. Bonsangue, editors,
    Proc. 9th International Symposium on Formal Methods for Components and Objects (FMCO 2010), volume 6957 of
    LNCS, pages 142–164, Heidelberg, 2011. Springer.
50. C. B. Jones. Development Methods for Computer Programmes Including a Notion of Interference. PhD thesis, Oxford
    University, UK, June l981.
51. Eduard Kamburjan. Behavioral program logic. In Serenella Cerrito and Andrei Popescu, editors, Proc. 28th In-
    ternational Conference on Automated Reasoning with Analytic Tableaux and Related Methods (TABLEAUX 2019),
    volume 11714 of LNCS, pages 391–408, Cham, Switzerland, 2019. Springer.
52. Eduard Kamburjan. Modular Verification of a Modular Specification: Behavioral Types as Program Logics. PhD
    thesis, Darmstadt University of Technology, Germany, 2020.
53. Eduard Kamburjan, Crystal Chang Din, Reiner Hähnle, and Einar Broch Johnsen. Behavioral contracts for coop-
    erative scheduling. In Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, Reiner Hähnle, and Mattias Ulbrich,
    editors, Deductive Software Verification: Future Perspectives, volume 12345 of LNCS, pages 85–121. Springer, Cham,
    2020.
54. James C. King. Symbolic execution and program testing. Communications of the ACM, 19(7):385–394, July 1976.
55. K.Rustan M. Leino, Peter Müller, and Jan Smans. Verification of concurrent programs with chalice. In Alessandro
    Aldini, Gilles Barthe, and Roberto Gorrieri, editors, Foundations of Security Analysis and Design V, volume 5705
    of LNCS, pages 195–222. Springer, Berlin Heidelberg, 2009.
56. Jayadev Misra and K. Mani Chandy. Proofs of networks of processes. IEEE Transactions on Software Engineering,
    7(4):417–426, 1981.
57. John C. Mitchell. Foundations for programming languages. Foundation of computing. MIT Press, Boston, MA, USA,
    1996.
58. Peter D. Mosses. Formal semantics of programming languages: — an overview —. Electron. Notes Theor. Comput.
    Sci., 148(1):41–73, 2006.
59. Wojciech Mostowski. From explicit to implicit dynamic frames in concurrent reasoning for Java. In Wolfgang Ahrendt,
    Bernhard Beckert, Richard Bubel, Reiner Hähnle, and Mattias Ulbrich, editors, Deductive Software Verification:
    Future Perspectives - Reflections on the Occasion of 20 Years of KeY, volume 12345 of LNCS, pages 177–203.
    Springer, Cham, 2020.
60. Keiko Nakata and Tarmo Uustalu. A Hoare logic for the coinductive trace-based big-step semantics of While. Logical
    Methods in Computer Science, 11(1):1–32, 2015.
61. Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. Isabelle/HOL — A Proof Assistant for Higher-Order
    Logic, volume 2283 of LNCS. Springer, Berlin Heidelberg, 2002.
62. Peter W. O’Hearn. Resources, concurrency, and local reasoning. Theoretical Computer Science, 375(1-3):271–307,
    2007.
63. Susan S. Owicki and David Gries. An axiomatic proof technique for parallel programs I. Acta Informatica, 6:319–340,
    1976.
64. Gordon D. Plotkin. A structural approach to operational semantics. J. Log. Algebr. Program., 60–61:17–139, 2004.
65. A.P. Sistla and E.M. Clarke. The complexity of propositional linear temporal logics. Journal of the ACM, 32(3):733–
    749, 1985.
66. Neelam Soundararajan. Axiomatic semantics of communicating sequential processes. ACM Transactions on Pro-
    gramming Languages and Systems, 6(4):647–662, 1984.
67. Dominic Steinhöfel and Reiner Hähnle. The trace modality. In Alexandru Baltag and Luis S. Barbosa, editors, 2nd
    Intl. Workshop on Dynamic Logic: New Trends and Applications, volume 12005 of LNCS, pages 124–140, Cham,
    January 2020. Springer.
68. Li-yao Xia, Yannick Zakowski, Paul He, Chung-Kil Hur, Gregory Malecha, Benjamin C. Pierce, and Steve Zdancewic.
    Interaction trees: representing recursive and impure programs in Coq. Proceedings of the ACM on Programming
    Languages, 4(POPL):1–32, Jan 2020.
42                               C. C. Din et al.

69. Marina Zaharieva-Stojanovski, Marieke Huisman, and Stefan Blom. Verifying functional behaviour of concurrent
    programs. In Proceedings of 16th Workshop on Formal Techniques for Java-like Programs, FTfJP’14, pages 4:1–4:6,
    New York, NY, USA, 2014. ACM.
70. Job Zwiers. Compositionality, Concurrency and Partial Correctness: Proof Theories for Networks of Processes, and
    Their Relationship, volume 321 of LNCS. Springer-Verlag, Heidelberg, 1989.
