                                         Unifying Model Execution and Deductive Verification with
                                         Interaction Trees in Isabelle/HOL
                                         SIMON FOSTER, University of York, UK
                                         CHUNG-KIL HUR, Seoul National University, South Korea
arXiv:2408.15817v2 [cs.LO] 30 Oct 2024




                                         JIM WOODCOCK, Southwest University, China, Aarhus University, Denmark, and University of
                                         York, UK
                                         Model execution allows us to prototype and analyse software engineering models by stepping
                                         through their possible behaviours, using techniques like animation and simulation. On the other
                                         hand, deductive verification allows us to construct formal proofs demonstrating satisfaction of
                                         certain critical properties in support of high-assurance software engineering. To ensure coherent
                                         results between execution and proof, we need unifying semantics and automation. In this paper,
                                         we mechanise Interaction Trees (ITrees) in Isabelle/HOL to produce an execution and verification
                                         framework. ITrees are coinductive structures that allow us to encode infinite labelled transition
                                         systems, yet they are inherently executable. We use ITrees to create verification tools for stateful
                                         imperative programs, concurrent programs with message passing in the form of the CSP and Circus
                                         languages, and abstract system models in the style of the Z and B methods. We demonstrate how
                                         ITrees can account for diverse semantic presentations, such as structural operational semantics, a
                                         relational program model, and CSP’s failures-divergences trace model. Finally, we demonstrate how
                                         ITrees can be executed using the Isabelle code generator to support the animation of models.

                                         CCS Concepts: • Theory of computation → Semantics and reasoning; Program reasoning; •
                                         Computing methodologies → Concurrent computing methodologies; Simulation tools; Modeling
                                         methodologies; Model verification and validation; • Software and its engineering → Formal methods;
                                         Software verification and validation; Software verification.

                                         Additional Key Words and Phrases: Interaction Trees (ITrees), Isabelle/HOL, Model Execution,
                                         Deductive Verification, Coinductive Structures, Formal Methods, CSP (Communicating Sequential
                                         Processes), Circus Language, Z and B Methods, Structural Operational Semantics, Theorem Proving,
                                         Proof Automation, Software Engineering Models, Model Execution, High-Assurance Software,
                                         Automated Program Verification, Code Generation, Animation and Simulation, UTP (Unifying
                                         Theories of Programming), Imperative Programming Verification

                                         ACM Reference Format:
                                         Simon Foster, Chung-Kil Hur, and Jim Woodcock. 2024. Unifying Model Execution and Deductive
                                         Verification with Interaction Trees in Isabelle/HOL. ACM Trans. Softw. Eng. Methodol. 1, 1
                                         (October 2024), 41 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn

                                         Authors’ addresses: Simon Foster, University of York, York, YO10 5GH, UK, simon.foster@york.ac.uk;
                                         Chung-Kil Hur, Seoul National University, Seoul, 08826, South Korea, gil.hur@sf.snu.ac.kr; Jim Woodcock,
                                         Southwest University, Chongqing, 400751, China and Aarhus University, Aarhua, 8200 Aarhus N, Denmark
                                         and University of York, York, YO10 5GH, UK, jim.woodcock@york.ac.uk.


                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted
                                         without fee provided that copies are not made or distributed for profit or commercial advantage and that
                                         copies bear this notice and the full citation on the first page. Copyrights for components of this work
                                         owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise,
                                         or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee.
                                         Request permissions from permissions@acm.org.
                                         © 2024 Association for Computing Machinery.
                                         1049-331X/2024/10-ART $15.00
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn


                                                      ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
2                                                           Simon Foster, Chung-Kil Hur, and Jim Woodcock


1   INTRODUCTION
Model-based software engineering uses models to produce software with a high level of
assurance [23, 47, 69]. Typically, engineers create behavioural models, such as state machines
and activity diagrams, which abstractly specify a system’s behaviour and can be subjected
to prototyping using animation, simulation, and testing. These techniques require that
models are executable, so we can step through their behaviour [14, 19]. When models
are accompanied by suitable formal semantics, they can be further subjected to formal
verification to ensure they satisfy the requirements in every possible state [53]. The models
can be refined further to produce verified code and related artefacts, creating high-integrity
software with traceable links to the original requirements.
   To ensure that these heterogeneous artefacts and analysis results can be applied coherently,
there is a need to tie them together using unifying formal semantics to avoid semantic gaps
that can introduce weaknesses [37, 58]. This semantics should allow us to give a formal
mathematical meaning to each model used in the development hierarchy and account for
the relations between them. It should also support execution to support early-stage proto-
typing [14]. Moreover, the semantics must have tool support with a high level of automation
to minimise the expertise engineers require. Whilst semantic frameworks exist that support
such a unification, such as Hoare and He’s Unifying Theories of Programming [44] (UTP),
the models are expressive but not usually executable. For formal methods to be accessible,
we, therefore, need to support models that are inherently executable and verifiable.
   Theorem proving is a powerful technique for analysing models and code by automating
deductive proof steps. Proof assistants like Coq [7], Isabelle [56], and Lean [21] provide a
flexible foundation for mathematical reasoning. They can be applied to many engineering
paradigms, from high-level design models [31, 33], potentially including interactions with the
physical environment [34], to low-level code [45]. Moreover, theorem provers can support the
verification of systems with a very large, or even infinite, state space through symbolic logic
techniques and compositional reasoning. However, unlike simulation and model-checking
techniques, formal proof typically has a high entry bar and requires significant investment
before meaningful results can be obtained. Consequently, to harness the benefits of theorem
proving in software engineering, we need to improve access with early-stage prototyping
techniques, such as animation1 and simulation, and high levels of proof automation.
   The contribution of this article is an Isabelle-based framework to support model-based
engineering called Isabelle/ITrees, which implements a variant of the Interaction Tree
(ITree) formalism of Xia et al. [75]. ITrees are coinductive data structures that allow us to
encode labelled transition systems symbolically as trees of infinite breadth and depth. They
intrinsically support mutable states, events, and communication and so can model complex
infinite behaviours. Crucially, and uniquely to ITrees, these formal models are both directly
executable and subject to verification by proof [76]. ITrees thus provide a natural encoding
of operational semantics using coinductive techniques, where we can step through a model’s
behaviour in terms of its internal steps and external interactions and communications.
Though ITrees are intrinsically elementary structures, they have the potential to act as a
unifying semantic model for a variety of software engineering artefacts.
   Our mechanisation of ITrees in Isabelle/HOL generalises the original work [75] in Coq
by using partial functions to model visible events. This allows us to support both external
choice and deadlock in the style of the CSP process algebra [15, 42, 62], along with the
1 In this context, animation refers to the interactive probing of a model’s behaviour. Simulation is similar

but is typically less interactive and, on the whole, more sophisticated.


ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL          3


algebraic semantics of these operators, which broadens our implementation’s application.
Our general, highly extensible framework can be applied to software engineering artefacts
at various abstraction levels. We use this to provide shallow embeddings of imperative
programs, communicating processes, and high-level system models in the style of the Z [65]
and B [1] specification languages. This is supported through results from UTP [28, 44]
to unify denotational, operational and axiomatic semantics, and in particular, the UTP
semantics for the Circus process language [29, 32, 73]. Our tool benefits from Isabelle’s proof
tools, notably the sledgehammer theorem prover integration [10], which we use out-of-box
to automate the discharge of verification conditions and other proof obligations. Moreover,
we employ Isabelle’s code generator [40] to provide execution of programs and animation of
high-level models. Our tool thus supports a tight development cycle where animation and
verification activities can be intertwined.
   The structure of our paper is as follows. In §3, we show how ITrees are mechanised in
Isabelle/HOL, including the core operators. We show how to derive structural operational
semantics from ITrees, characterise weak bisimulation, which allows the abstraction of silent
events, and provide theorems for reasoning about process iteration using chains. In §4, we
show how to model and verify imperative programs using ITrees, demonstrate a link with
our previous UTP-based relation semantics, and provide program verification support using
Hoare logic. In §5, we show how deterministic CSP and Circus processes can be semantically
embedded into ITrees, including operators like external choice and parallel composition.
We also link ITrees with the standard failures-divergences semantic model for CSP, which
justifies their integration with other CSP-based techniques. In §6, we show how the code
generator can be used to generate animations. In §7, we apply our library to develop a
simple tool for modelling systems, similar to the B-method [1]. In §8, we consider related
work, and in §9, we conclude.
   This paper extends our previous CONCUR 2021 paper [30]. We add results in the new
section on imperative programming (§4), including total correctness Hoare logic and UTP-
style predicative semantics, a new section on modelling with Z-Machines (§7), new theorems
on iteration chains (§3), and additional narrative and more minor results throughout. All
our results have been mechanised and can be found in the accompanying repository2 , and
clickable icon links     next to each specific result.

  Notation. Our presentation uses both textbook-style notation and Isabelle code, though
we generally prefer the former. This mixture is unavoidable, as the Isabelle code, though
ultimately the single source of truth, is often more pedantic than necessary for a human reader
and less accessible. We largely restrict Isabelle’s code to modelling and verification examples
to support the use of our tools. The reader interested in how the textbook mathematics is
mechanised can follow the Isabelle links ( ).

2   BACKGROUND
This section introduces the foundational concepts used in this paper: Isabelle/HOL and the
Circus language. Circus is used to motivate the value of ITrees in providing formal semantics
for process algebraic languages. We also use the Z mathematical toolkit in our semantic
definitions, which is used in Circus.


2 https://github.com/isabelle-utp/interaction-trees



            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
4                                                       Simon Foster, Chung-Kil Hur, and Jim Woodcock


2.1   Isabelle/HOL
Isabelle/HOL [56], at its core, is a proof assistant for Higher Order Logic (HOL)3 . It
implements a Gentzen-style natural deduction system, which can be used to prove or
falsify the validity of arguments formalised using predicate logic. The language of HOL
is a strongly typed polymorphic 𝜆-calculus, which can be used to formalise mathematical
theories in a functional programming style. In particular, Isabelle/HOL provides a typed set
theory, arithmetic theories (natural numbers, integers, real numbers, etc.), and various data
structures, such as lists and records. As in functional programming languages, programs
can be specified using algebraic data types and recursive functions, with termination checks
provided. These features give an expressive and extensible mathematical language in which
various programming and modelling notations can be described [71].
   The development of theories in Isabelle is centred around theory documents, which are
used for modelling and proof. Theory documents (extension .thy) are written using the Isar
language [70], and consist of a sequence of commands manipulating Isabelle’s state. Such
commands may be used to define a function or start a proof, for example. The document
model has two levels of syntax: (1) outer-syntax, which gives the syntax to individual
commands, and (2) inner-syntax, which gives syntax to terms of the logic in typed 𝜆-calculus.
An example definition command is given below:

definition square :: "nat ⇒ nat" where
" square x = x * x"

The command begins with a major keyword (definition), which is highlighted, followed
by a type declaration for a new constant, square, which is a total function from natural
numbers to natural numbers (nat ⇒ nat). Following the type declaration, there is a minor
keyword (where) and then the definitional equation for the function. Speech marks delimit
this definitional equation since it is inner-syntax formed using the term language. The
document model of Isabelle is extensible so that new commands can be implemented for
bespoke modelling tasks using the meta-language Isabelle/ML [71].
   Several facilities complement Isabelle’s modelling features for automating proof. Isabelle
provides a simplifier (simp) for equational rewriting of terms and a classical reasoner (blast),
which implements the tableaux method for automating natural deduction. Additionally, there
is a resolution prover (metis) for first-order predicate calculus and access to several SMT
solvers, such as CVC4 and Z3, in the smt method. These proof methods can be coordinated
using the sledgehammer tool [10], which constructs proofs using external tools.
   For example, with the definition above, we can pose a binomial expansion theorem:

theorem square_plus: " square (x+y) = square x + square y + 2*x*y"

The theorem command asserts that the given property can be derived by proof. In this
case, we give the posed theorem a name (square plus) and the proposition that we wish
to prove: square(x+y) = square x + square y + 2*x*y. Implicitly, this means that this
equational property is valid for any natural numbers x and y. In order for Isabelle to accept
this as a theorem, we need to provide a proof. In this case, the proof can be provided
automatically with sledgehammer. Running this calls several external automated theorem
provers, and CVC4 comes back with a proof. We can then complete the proof as follows:

3 Isabelle/HOL website: https://isabelle.in.tum.de/



ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL           5


theorem square_plus: " square (x+y) = square x + square y + 2*x*y"
  by ( metis power2_eq_square power2_sum square_def )

The command by states that the property can be proved by the following proof method. The
sledgehammer supplied proof uses the metis resolution prover, with two theorems from the
HOL theorem library, and the definitional equation for square. Isabelle accepts the proof,
and so the property is certified as a theorem for use in further proof.
  The combination of an expressive and rigorous mathematical language with extensible
proof automation make Isabelle ideally suited to formal verification. This requires that the
semantics of the target language first be formalised as an Isabelle theory package and a
suitable proof calculus (such as Hoare logic [55]) be provided to form specifications and
verify programs. Isabelle also provides a code generator [39, 40] for mathematical programs,
which can be used to automate code production from verified artefacts.

2.2     Circus and Z
Circus [57, 73] is a formal language for modelling imperative and concurrent systems. It
combines the communication primitives from the CSP process algebra with imperative
programming primitives from Dijkstra’s guarded command language (GCL) and rich state
modelling facilities as provided by the Z notation [65].
  Z is a formal language for specifying software using set theory and relational calculus [65,
74]. CSP is a language for modelling concurrent systems, such as protocols. It provides
several modelling primitives, including.
      • event prefix (a → P): perform event a and then enable P;
      • guard (B & P): enable P only when condition B is true;
      • external choice (P 2 Q): allow the environment to choose P or Q;
      • parallel composition (P |[ A ]| Q): run P and Q in parallel synchronising on events in A;
      • hiding (P \ A): internalise events in set A.
Events are typically input events a?x → P (x) or output events b!v → Q, where a and b
are channels carrying typed data. The standard semantics for CSP is called the failures-
divergences model [62], a denotational semantics based on traces, which we cover in §5.3.
  In addition to these CSP operators, Circus also contains typical imperative programming
operators from GCL like assignment (x := e), sequential composition (P # Q), and iteration
(while B do C od). From Z, it gains a mathematical toolkit, including data structures like
sets, partial functions (A →
                           ↦ B), finite functions (A →
                                                     ↦ ↦ B), and sequences (lists), and also
the ability to form abstract data types using Z schemas.
  We also use the Z mathematical toolkit for partial functions in our semantic definitions.
We can specify partial functions using 𝜆 x ∈ A • f (x), which restricts a function f to the
domain A4 . We can calculate the domain of a partial function f with dom(f ). An empty
partial function {↦→} has an empty domain. We also use the domain restriction (◁) and
override operators (⊕) from the Z mathematical toolkit, which have the following definitions:

               A ◁ f ≜ (𝜆 x ∈ A ∩ dom(f ) • f (x))
               f ⊕ g ≜ (𝜆 x ∈ dom(f ) ∪ dom(g) • if x ∈ dom(g) then g (x) else f (x))


4 This is distinguished from the total function notation 𝜆 x. g (x ) by a different separator (•)



             ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
6                                                           Simon Foster, Chung-Kil Hur, and Jim Woodcock



                                         (4)
                                               𝜏   / (5)   Input.y
                                                                     / (6)     𝜏        / (7)   Input.z
                                                                                                          /
                                     @                       Output.x                             Output.x

                   Input.x                                           &                                        %
                                                                         (8)       State.[x,y]
                                                    State.[x ]
                                                                               𝜏

                                                                                   &                             
 (1)
          𝜏     / (2)                / (3)     𝜏   / (2)                                (2)
                        State.[ ]


                    Fig. 1. An ITree fragment for the buffer example (approximate)


We have implemented the Z mathematical toolkit in an Isabelle library as a hierarchy of
types5 . With the associated theorems, we can use Isabelle’s simplifier to automate the
calculation of a partial function’s domain and other properties.
  As an example Circus process, we formalise a simple reactive buffer. We introduce three
channels: Input to accept a new input, Output to offer an output, and State to show the
current state of the buffer. We consider a buffer containing a sequence of natural numbers N
for simplicity. We also introduce a single variable, buf , which stores the values present in
the buffer. The reactive behaviour of the buffer is then specified below:
    Example 2.1 (Unbounded Buffer in Circus).
              buf := [] # while true do
                                    Input?(i) → buf := buf @ [i]
                               2 (length (buf ) > 0) & Output!(hd buf ) → buf := tl buf
                               2 State!(buf ) → Skip
                         od
The buffer enters a reactive infinite loop after initially setting the buffer to be an empty list
([]). The buffer provides three options using the external choice operator (2). It can accept
an input over Input, extending the buffer using the list append operator (xs @ ys). If the
buffer is not empty (its length is non-zero), it can offer the head (i.e. first element) of the
buffer over Output and contract the buffer with the tl function, which removes the head.
Finally, it can display the current state of the buffer over the State channel.

3      INTERACTION TREES AND OPERATIONAL SEMANTICS
This section introduces Interaction Trees (ITrees), develops the main theory in Isabelle/HOL,
derives operational semantics, and provides several novel results. ITrees were originally
mechanised in Coq by Xia et al. [75]. Our mechanisation in Isabelle/HOL brings unique
advantages, including a flexible front-end syntax, automated proof tools, and code generation
to several languages.

3.1     Interaction Trees as Codatatypes
ITrees are potentially infinite trees whose edges are decorated with events, representing the
interactions between a process and its environment. For intuition, an example ITree is shown
in Figure 1 for the buffer in Example 2.1. The nodes are labelled with numbers for reference,
and the edges with events, including visible events, such as Input.x, and invisible events (𝜏).
5 Z-Toolkit library: https://github.com/isabelle-utp/Z_Toolkit.



ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL          7


   From the initial node (1), a single 𝜏 event is possible, which corresponds to assigning []
to the buf state variable (buf := []). Two visible events are presented to the environment,
Input.x and State.[]. The latter event, State.[] indicates that the buffer is empty, so an
Output event is unavailable. The former event, Input.x, corresponds to an infinite family of
events for each possible value the channel can carry, such as x = 0, x = 1, x = 3 and so on.
We can describe such infinite families in Isabelle/HOL symbolically as a term containing a
free variable (x), such that ITrees can have infinite breadth.
   If an input is received, we transition to node (4), from which a single 𝜏 event occurs, which
corresponds to the assignment appending x to the buffer (buf := buf @ [x]). From node (5),
three events are possible: Input.y, Output.x, and State.[x]. At this point, the buffer contains
a single value x, which we can output, or input another value y. Again, x and y are families
of possible values carried by channels Input and Output. If another value y is input, the
buffer is updated accordingly, leading to node (7). The tree continues in this manner and
thus has an infinite depth. It can alternatively be considered as an unfolding of a labelled
transition system.
   We now describe the type in Isabelle that allows us to denote ITrees formally. ITrees
are parametrised over two sorts (types): E of events and R of return values (or states).
There are three possible interactions: (1) termination, returning a value in R; (2) an internal
event (𝜏) followed by a successor ITree; or (3) a choice between several visible events. In
Isabelle/HOL, we encode ITrees using a codatatype [9, 12]. A codatatype is similar to an
algebraic datatype, having several disjoint constructors. However, the crucial difference is
that whereas elements of a datatype are finite, elements of a codatatype may be infinite.

  Definition 3.1 (Interaction Tree Codatatype).
  codatatype ('e, 'r) itree =
    Ret 'r | Sil "('e, 'r) itree" |                          ↦ ('e, 'r) itree"
                                                     Vis "'e →

The codatatype command creates a type called itree, with two type parameters ’e and ’r,
and three constructors. Type parameters ’e and ’r encode the sorts E and R. Constructor
Ret represents a return value, and Sil is an internal event that evolves to a further ITree.
A visible event choice (Vis) is represented by a partial function (A →  ↦ B) from events to
ITrees, with a potentially infinite domain. For example, in Figure 1 at node (2), a visible
event choice is presented whose domain is {Input.x | x ∈ N} ∪ {State.[]}.
  The representation of visible events is the main deviation from ITrees in Coq [75], which
has visible events composed of an output to the environment, followed by the answer. The
benefit of using a partial function is to allow a straightforward encoding of deadlock and
external choice, where the ITree offers several events to the environment (for a more detailed
comparison, see §8). Moreover, a side effect of this design decision is that we only need
rank-1 polymorphism for the encoding, which makes the development in Isabelle possible.
  We use the notation 𝜆 c.x | B (x) • P (x) for a partial function which pattern matches on
events over channel c, and whose parameters x also satisfy predicate B. With this notation,
we can describe the main choice block of the buffer example:

  Example 3.2 (Buffer: Single Step ITree).

                              (𝜆 Input.x • Ret (buf @ [x]))
       BufBody (buf ) ≜ Vis ­ ⊕ (𝜆 Output.v | #buf > 0 ∧ v = hd (buf ) • Ret (tl (buf ))) ®
                            ©                                                             ª

                            « ⊕ (𝜆 State.s | s = buf • Ret (buf ))                        ¬

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
8                                                       Simon Foster, Chung-Kil Hur, and Jim Woodcock


This constructs a visible event choice over a partial function composed of three parts using
the override operator (⊕). Here, parameter buf is a list of natural numbers, which is the
current contents of the buffer. The first function accepts a value x over channel Input and
returns the buffer with x appended. The second function allows us to output a value v over
Output, but only when the buffer is non-empty (#buf > 0) and v is the head of the buffer.
This being the case, the function returns the contracted buffer (tl (buf )), which effectively
updates the state. The third function allows us to advertise the current values in the buffer
but leaves the buffer unchanged. Since the three functions have disjoint domains, they can
be commuted over the override operator. Such an example is encoded more naturally using
the Circus operators, but we defer denoting these to §5.
   We sometimes use ✓v to denote Ret v, 𝜏P to denote Sil P, and [] e ∈ E → P (e) to denote
Vis (𝜆 e ∈ E • P (e)), which are more concise and suggestive of their process algebra equiv-
alents. We write e1 → P1 [] · · · [] en → Pn for an enumerated choice with E = {e1, · · · , en }.
We use 𝜏 n P for an ITree prefixed by n ∈ N internal events. We define stop ≜ Vis {↦→}, a
deadlock situation where no event is possible. An example is a → 𝜏 (✓x ) [] b → stop, which
can either perform the event a followed by a 𝜏, and then terminate returning x, or perform
the event b and then deadlock.
   We call an ITree unstable if it has the form 𝜏P, and stable otherwise. The ITree in Figure 1
is stable in nodes (2), (5), and (7) and unstable in all other numbered nodes. An ITree
stabilises, written P ⇓ , if it becomes stable after a finite sequence of 𝜏 events, that is
∃ n P ′ • P = 𝜏 n P ′ ∧ stable (P ′ ). An ITree that does not stabilise is divergent, written
P ⇑ ≜ ¬(P ⇓). A divergent ITree can only perform an infinite sequence of internal 𝜏 events,
and so corresponds to an infinite loop.

3.2   ITree Combinators
Using the constructors mentioned so far, we can only specify ITrees of finite depth. Infinite
ITrees can be specified using primitive corecursion [9], which is the dual of recursion but
allows non-terminating productive definitions. We define such an ITree below:
    Definition 3.3 (Divergent ITree).
    primcorec div :: "('e, 's) itree" where "div = 𝜏 div"
The primcorec command creates a typed constant which obeys several corecursive equations
(following the where). Each definition requires that a constructor guards every corecursive
call on the right-hand side of an equation, ensuring it is productive. This means that, though
the definition does not terminate, it is always possible to strip off the next constructor.
   ITree div represents the divergent ITree that does not terminate and only performs internal
activity. Though self-referential and non-terminating, its definition is productive since we
can always remove the next 𝜏. Since div never stabilises, it is divergent, div ⇑ . Moreover,
we can show that div is the unique fixed-point of 𝜏 n+1 for any n ∈ N, 𝜏 n+1 P = P ⇔ P = div ,
and consequently div is the only divergent ITree: P ⇑ → P = div .
   We call an ITree pure if it has the form of 𝜏 n P, where P has the form of either ✓x , stop, or
div . The external environment cannot influence a pure ITree, which must either terminate,
deadlock (abort) or diverge. Intuitively, a pure ITree can perform all the computation it
wants without needing to communicate. We give another infinite ITree below:
    Definition 3.4 (Run ITree).
    primcorec run :: "'e set ⇒ ('e, 's) itree" where
    "run E = Vis (map_pfun (𝜆 x. run E) (pId_on E))"

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL                 9


Here, the type 'e set denotes the set of all subsets of type 'e. ITree run E can repeatedly
perform any e ∈ E without ceasing. It has the equivalent definition of run E ≜ []e ∈ E →
run E, an ITree that can repeatedly choose any event in E. It also has the case run ∅ = stop.
The formulation above uses the function map pfun :: (’b ⇒ ’c) ⇒ (’a →    ↦ ’b) ⇒ (’a →  ↦ ’c)
which maps a total function over every output of a partial function. The function pId on E
is the identity partial function with domain E. This formulation is required to satisfy the
syntactic guardedness requirements. For the sake of readability, we omit these details in the
following definitions.
   Corecursive definitions can have several equations ordered by priority, like a recursive
function. Using such a set of equations, we specify a monadic bind operator for ITrees [75].
   Definition 3.5 (Interaction Tree Bind). We fix P, P ′ : (E, R)itree, K : R ⇒ (E, S)itree,
r : R, and F : E →↦ (E, S)itree. Then, P >>= K is defined corecursively by the equations
                              ✓r >>= K = K r
                             𝜏P ′ >>= K = 𝜏 (P ′ >>= K )
                           Vis F >>= K = Vis (𝜆 e ∈ dom(F ) • F (e) >>= K )
The intuition of P >>= K is to execute P, and whenever it terminates (✓r ), pass the given
value r on to the continuation K , yielding K r. If the first ITree can perform a 𝜏 event, this
is performed first, and the remaining ITree is bound to K . If the first ITree can perform a
visible event e ∈ dom(F ), then we perform e, pass this on to F , and bind the result to K .
   We term K a Kleisli tree [75], or KTree since it is a Kleisli lifting of an ITree. KTrees are
important for defining processes that depend on a previous state. For this, we define the type
synonym (E, S)htree ≜ (S ⇒ (E, S)itree) for a homogeneous KTree. For example, BufBody
is homogeneous Kleisli tree of type int list ⇒ (E, int list)itree. Intuitively, the construction
K (s) can be read as “the Klesli tree K started in the initial state s”. We define the Kleisli
composition operator P # Q ≜ (𝜆 x. P x >>= Q), symbolised because it is used as a sequential
composition. Bind satisfies several algebraic laws:
  Theorem 3.6 (Interaction Tree Bind Laws).
              Ret x >>= K = K x                                           Ret # K = K
                 P >>= Ret = P                                            K # Ret = K
            P >>= (Q # R) = (P >>= Q) >>= R                        K1 # (K2 # K3 ) = (K1 # K2 ) # K3
                 div >>= K = div                                      run E >>= K = run E
Bind satisfies the three monad laws: it has Ret as left and right units and is essentially
associative. Moreover, both div and run are left annihilators for bind since they do not
terminate. The monad laws show that (#, Ret) also forms a monoid; # is commutative and
has Ret as its left and right units.
  The laws of Theorem 3.6 are proved by coinduction, using the following derivation rule.
  Theorem 3.7 (ITree Coinduction). We fix a relation R : (E, R)itree ↔ (E, R)itree.
Then, given (P, Q) ∈ R we can deduce P = Q provided that the following conditions hold:
 (1) ∀(P ′, Q ′ ) ∈ R. is Ret(P ′ ) = is Ret(Q ′ ) ∧ is Sil(P ′ ) = is Sil(Q ′ ) ∧ is Vis(P ′ ) = is Vis(Q ′ );
 (2) ∀(x, y). (Ret x, Ret y) ∈ R → x = y;
 (3) ∀(P ′, Q ′ ) (Sil P ′, Sil Q ′ ) ∈ R → (P ′, Q ′ ) ∈ R;
 (4) ∀(F, G) (Vis F, Vis G) ∈ R → (dom(F ) = dom(G) ∧ (∀ e ∈ dom(F ) • (F (e), G (e)) ∈ R)).

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
10                                                      Simon Foster, Chung-Kil Hur, and Jim Woodcock


To show that P = Q, we need to construct a (strong) bisimulation relation R, which intuitively
relates two ITrees, and show that (P, Q) ∈ R. There are four provisos to show that R is a
bisimulation. The first requires that only ITrees of the same kind are related; that is, a Ret is
only related to a Ret, a Sil with a Sil, and a Vis with a Vis. Here, is Ret, is Sil, and is Vis
distinguish the three cases. The second proviso states that if (✓x , ✓y ) ∈ R then x = y, two
related ITrees must return equal values. The third proviso states that internal events must
yield bisimilar continuations: (𝜏P, 𝜏Q) ∈ R → (P, Q) ∈ R. The final proviso states that for
two visible interactions, the two functions must have the same domain (dom(F ) = dom(G)),
and every event e ∈ dom(F ) must lead to bisimilar continuations. Most of our ITree proofs
in Isabelle apply this law and then use a mixture of equational simplification and automated
reasoning with sledgehammer to generate proofs that discharge the resulting provisos.
   Next, we define an operator for iterating ITrees in the style of a while-loop:
     Definition 3.8 (Iteration).
     corec while :: "('s ⇒ bool) ⇒ ('e, 's) htree ⇒ ('e, 's) htree" where
     "while b P s = (if (b s) then Sil (P s >>= while b P) else Ret s)."
This is not primitively corecursive since the corecursive call uses >>=, and so we define it
using the corec command [8, 11] instead of primcorec. This requires us to show that
>>= is a “friendly” corecursive function [8]: it consumes at most one input constructor to
produce one output constructor. A while loop iterates whilst the condition b is satisfied
by state s. In this case, a 𝜏 event is followed by the loop body and the corecursive call.
If the condition is false, the current state is returned. We introduce the exceptional cases
loop F ≜ while (𝜆 s. True) F and iter P ≜ loop (𝜆 s. P) (), which represent infinite loops with
and without state, respectively. We can show that iter (✓() ) = div since it never terminates
and has no visible behaviour.
   With while, we can easily complete the definition of the buffer: Buffer ≜ while BufBody [].
This iterates the buffer body in Example 3.2 over and over to provide the complete ITree
shown in Figure 1. The initial empty state of the buffer is provided with the parameter [].

3.3     Structural Operational Semantics and Weak Bisimulation
The ITree model allows us to describe structural operational semantics for our abstract
language naturally. We give big-step operational semantics to ITrees using an inductive
predicate.
     Definition 3.9 (Big-Step Operational Semantics).
                        −             tr                               tr
                                  P −→ P ′         e∈E           F (e) −→ P ′
                        []              tr                               e#tr
                      P −→ P       𝜏P −→ P ′         ( [] x ∈ E • F (x)) −−−→ P ′
                 tr
The relation P −→ Q means that P can perform the trace of visible events contained in the
list tr : E list and evolve to the ITree Q. This relation skips over 𝜏 events. The first rule
states that any ITree may perform an empty trace ([]) and remain in the same state. We
sometimes omit the trace and write P →    − P ′ . The second rule states that if P can evolve
      ′
to P by performing tr, then so can 𝜏P. The final rule states that if e is an enabled visible
event, and P (e) can evolve to P ′ by doing tr, then the event choice can evolve to P ′ via e#tr,
which is tr with e inserted at the head. This inductive predicate is different from the trace
                                               tr
predicate (is trace of) in [75], since P −→ P ′ records both the trace and the continuation
ITree. It is, therefore, more general and provides the foundation for characterising structural
operational and denotational semantics.

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL              11


  We next prove some important theorems of the transition relation.
  Theorem 3.10 (Transition Relation Properties).
                       tr1            tr2              tr1 @ tr2
                (P −−→ Q ∧ Q −−→ R) → (P −−−−−−−→ R)                       (sequential transitions)
          tr                   tr @ [e]
     (P −→ Vis F ∧ P −−−−−−→ P ′ ) → e ∈ dom(F )                           (events resolve choices)
               tr                tr
        (P −→ Ret x ∧ P −→ Ret y) → x = y                           (termination is deterministic)
                       tr1                                   tr2
                    (P −−→ Q ∧ tr2 ≤ tr1 ) → (∃ R. P −−→ R)                          (prefix closure)
A pair of sequential transitions can be combined by appending the two traces, tr1 and tr2 .
Whenever an event e follows a visible choice over F , that event must have been enabled by
F . If we can reach two return ITrees by the same trace, then the two values returned must
be equal – termination is deterministic. Finally, whenever P can reach Q by performing tr1 ,
every prefix of tr2 must also have an intermediate successor ITree R.
   With these laws, we can prove the usual operational laws for sequential composition as
theorems:
  Theorem 3.11 (Sequential Operational Semantics).
                                                  tr                 tr1               tr2
                     −                       P −→ P ′              P −−→ ✓x    Q(x) −−→ Q ′
                                                  tr                           tr1 @ tr2
                skip → ✓( )           (P >>= Q) −→ (P ′ >>= Q)      (P >>= Q) −−−−−−−→ Q ′
The skip process immediately terminates, returning (). If the left-hand side P of >>= can
evolve to P ′ performing the events in tr, the overall bind evolves similarly. If P can terminate
after doing tr1 , returning x, and the continuation Q(x) can evolve over tr2 to Q ′ then the
overall >>= can also evolve over the concatenation of tr1 and tr2 , tr1 @ tr2 , to Q ′ .
  Strong bisimulation is a useful equivalence, but we often wish to abstract over 𝜏s. We,
therefore, also introduce weak bisimulation, P ≈ Q, as a coinductive-inductive predicate.
Given a relation R, we define ≈ R inductively:
  Definition 3.12 (Weak Bisimulation).

           −                  P ≈R Q        P ≈R Q               ∀ e ∈ E • R (F (e), G (e))
       ✓x ≈ R ✓x             𝜏P ≈ R Q      P ≈ R 𝜏Q    ([] x ∈ E • F (x)) ≈ R ( [] x ∈ E • G (x))
                                           Ð
                                      (≈) ≜ {R | R ⊆ {(div, div )} ∪ (≈ R )}
  It requires us to construct a relation R such that whenever (P, Q) in R both stabilise, all
their visible event continuations are also related by R. For example, 𝜏 m P ≈ 𝜏 n Q whenever
P ≈ Q. We have proved that ≈ is an equivalence relation, and P ≈ div → P = div .

3.4 Iteration Chains
To reason about iteration (while b do P od), as usual, we need to characterise iteration chains.
This, for example, is necessary for us to verify the properties of the buffer example. A chain
is typically a sequence of states reached during an iteration’s successive stages. For ITrees,
we also need to consider the events that occur during iteration.
                                            chn
  We adopt the notation s ⊢ P −−−→ ∗ s ′ to mean that state s ′ :: S can be reached when
the loop body P :: (E, S)htree is started in state s :: S, by following the chain chn. Here,
chn :: (E list × S) list is a list of trace and state pairs, each element of which denotes a single

               ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
12                                                             Simon Foster, Chung-Kil Hur, and Jim Woodcock


terminating execution of P. The formal definition of an iteration chain is given using the
inductive predicate below.

     Definition 3.13 (Iteration Chains).
                                                     tr                        chn
                                 —              P (s) −→ ✓s0         s0 ⊢ P −−−→∗ s1
                                   []                          (tr,s0 )#chn
                            s ⊢ P −→∗ s               s ⊢ P −−−−−−−−−→∗ s1
This does not yet consider the loop condition, which will be added subsequently. The first
rule states that P can complete execution at state s by performing zero iterations starting
in s. This occurs when the condition of a loop is false initially. The second rule allows a
chain extension by a single execution of P. If P, when started in state s, terminates in the
intermediate state s0 having performed the trace tr, and P can further transition to s1 ,
when started from s0 via chain chn, then we can prefix chn with the element (tr, s0 ). For
example, s0 may result from the loop body’s first iteration with the trace tr, and then chn
characterises all subsequent iterations.
                                                                              tr
  Next, we use chains to define a partial iteration (b, s) ⊢ P −→∗✓ s ′ , which intuitively means
that P is executed several times, starting in s and reaching s ′ , whilst yielding trace tr.
Moreover, in each intermediate state, the condition b remains satisfied. We define this
operator directly using iteration chains:

     Definition 3.14 (Partial Iteration).
                                                                   chn
                                                                                                         !
                 tr                               b(s) ∧ s ⊢ P −−−→∗ s0 ∧ (∀ s ∈ states(chn) • b(s))
     (b, s) ⊢ P −→∗✓ s ′ ⇔ ∃(chn, s0, tr0 ) •              tr0
                                                  ∧ P (s0 ) −−→ ✓s′ ∧ tr = trace(chn) @ tr0

Here, the function states extracts the set of all states a chain encounters, and trace is the
concatenated trace described by the whole chain. Using this definition, we can now state the
main theorem for reasoning about terminating loops.

     Theorem 3.15 (Terminating Loops).
                            tr
                                                                                tr
                                                                                                    
     (while b do P od) (s) −→ ✓s′ ⇔ (¬b(s) ∧ s = s ′ ∧ tr = []) ∨ b(s) ∧ (b, s) −→∗✓ s ′ ∧ ¬b(s ′ )

If a loop terminates in state s ′ , when started in initial state s, then there are two possibilities.
Firstly, s does not satisfy the condition, so s ′ is the same as s, and an empty trace is emitted.
Secondly, s does satisfy the condition; there is a partial iteration from P to s ′ emitting tr,
and s ′ does not satisfy the condition. In other words, the loop is executed several times, with
each intermediate satisfying b, and ends in a state that exits the loop. A consequence of this
theorem is that a chain leads to the existing terminating state whenever a loop terminates.
This theorem equips us to reason about the partial and total correctness of programs in §4.
   The proof of this theorem is complex and requires induction on the structure of the
transition relation in Definition 3.9. Our approach is to show that every transition of an
iteration leads to an ITree of the form Q >>= while b do P od, that is a prefixed iteration, where
the prefix Q is a partial execution of the loop body. The interested reader is directed to our
proofs in Isabelle/HOL, which total about 300 lines of Isar.
   We have now completed the foundational mechanisation of ITrees. In the next section,
we will apply our theory to the modelling and verification of imperative programs before
further considering reactive and concurrent programs in §5.

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL         13


4     IMPERATIVE PROGRAMS AND AXIOMATIC SEMANTICS
This section builds on ITrees to develop a theory of Dijkstra-style imperative programs
and an associated Hoare logic for partial and total correctness, which can be used to verify
programs. The language is implemented as a “shallow embedding” [13, 35] in Isabelle/ITrees.
This essentially means that we reuse Isabelle’s modelling and proof facilities in the language
semantics, which maximises the scope for proof automation. We also develop the weakest
precondition calculus and a link with a UTP-style predicative semantics [44], which provides
the basis for a refinement calculus.

4.1    Modelling Imperative Programs
Imperative programs can be modelled as homogeneous Kleisli trees, S ⇒ (E, S)itree, where
S is the program’s store type. Programs are typically pure for every initial state, meaning
they depend only on their internal store for computation. An exception is nondeterministic
programs, which we model using a special event to resolve any internal choices (see §4.3).
   The store of an imperative program consists of a finite set of mutable state variables. In
our work [28, 29, 32], each state variable is modelled as a lens [26], x :: V =⇒ S, where V
is the variable’s type, and S is the store type. A lens is a pair of functions get :: V ⇒ S
and put :: S ⇒ V ⇒ S, which query and update the variables present in state S, and
satisfy intuitive algebraic laws [28]. They allow an abstract representation of stores, where no
explicit model is required to support the laws of programming [43]. Lenses can be designated
as independent, x ⊲⊳ y, meaning they refer to different regions of S.
   An expression or assertion over the state variables is a function e :: S ⇒ V, where V is the
return type. For example, if x and y are state variables, then the expression x + y is denoted
by 𝜆 s. getx s + gety s. This function retrieves the values of x and y from the state s and adds
them together. We can check whether an expression e uses a lens x using unrestriction,
written x ♯ e. If x ♯ e, then e does not use x in its valuation, for example x ♯ (y + 1), when
x ⊲⊳ y. Updates to variables can be expressed as a sequence of maplets using the notation
[x1 { e1, x2 { e2, · · · ], with xi :: Vi =⇒ S and ei :: S ⇒ Vi , which represents a function
S ⇒ S.
   Creation of program store types is facilitated by a new command called zstore, which
we have implemented on top of our lens library [28]:

    zstore S = x 1 ::T1 1          x 2 ::T 2 ... x n ::T n where "P(x 1 , x 2 , ... , x n )"

This generates a set of lenses x1 · · · xn , which have type Ti =⇒ S, for i ∈ {1..n}. An
independence property is also generated for each pair of lenses: xi ⊲⊳ xj where i ≠ j. Our
expression parser automates the lifting of terms containing such lenses so that expressions
like x + y are semantically interpreted as 𝜆 s. getx s + gety s. Optional invariant predicates
following the where clause can also accompany store types, which is useful to facilitate
invariant-based reasoning (see §7). Internally, a store is compiled into a record type S with
a collection of lenses and an invariant assertion S inv : S ⇒ B.
   We can now denote the operators of an idealised imperative programming language.
Sequential composition is modelled by Kleisli composition (P # Q). The remaining operators
are given below:

    Definition 4.1 (Imperative Program Operators).

                         C1 ⊳ P ⊲ C2 ≜ (𝜆 s. if P (s) then C1 (s) else C2 (s))

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
14                                                          Simon Foster, Chung-Kil Hur, and Jim Woodcock


                                    ⟨𝜎⟩ ≜ (𝜆 s. Ret (𝜎 (s)))
                                 x := e ≜ ⟨[x { e]⟩
                                   Skip ≜ ⟨[{]⟩
                                  Stop ≜ (𝜆 s. stop)
                                   Div ≜ (𝜆 s. div )
                                   ¿P? ≜ Skip ⊳ P ⊲ Stop
C1 ⊳ P ⊲ C2 is our algebraic notation for a conditional statement (if-then-else), where P is
the condition. Operator ⟨𝜎⟩ lifts a function 𝜎 : S ⇒ S to a KTree. It is principally used
to represent assignments, which can be constructed using our maplet notation, such that
a single assignment x := e is ⟨[x { e]⟩. Since substitutions can assign multiple variables,
they can also represent simultaneous assignment, (x, y) := (e, f ). Similarly, the vacuous Skip
statement is denoted by an empty assignment. Stop is simply a Kleisli-lifted version of the
ITree stop, which deadlocks (or aborts) in any initial state, and Div similarly diverges in
every initial state. Finally, ¿P? is a test operator, which deadlocks when P is false and
otherwise has no effect. These operators satisfy all the usual laws of programming [43], a
small selection of which is shown below. These laws give equational algebraic semantics for
imperative programs.
     Theorem 4.2 (Laws of programming).
          Skip # C = C # Skip = C
                x := e # y := f = y := f # x := e                                if x ⊲⊳ y, x ♯ f , y ♯ e
                      ⟨𝜎⟩ # ⟨𝜌⟩ = ⟨𝜌 ◦ 𝜎⟩
        x := e # (C1 ⊳ P ⊲ C2 ) = (x := e # C1 ) ⊳ P [e/x] ⊲ (x := e # C2 )
        C1 ⊳ P ⊲ (C2 ⊳ P ⊲ C3 ) = C1 ⊳ P ⊲ C3
Skip is the unit of sequential composition. Two variable assignments commute provided their
variables are independent (x ⊲⊳ y), and their respective expressions do not depend on the
adjacent variable. More generally, the sequential composition of two state updates 𝜎 and 𝜌
entails their functional composition. Assignment can be pushed into a conditional by first
substituting the assignment into the condition P. Finally, an outer conditional masks an
inner one, meaning that C2 is an unreachable branch. Such laws can be used for symbolic
execution and optimisation of imperative programs.

4.2      Concrete and Symbolic Execution
A particular benefit of our ITree-based semantics is that imperative programs can be directly
executed. A non-divergent and non-aborting pure ITree reduces to the form of 𝜏 n (✓s′ ), for
n ∈ N, where s ′ is the final state of the program. This is a particular case of a stable ITree.
Consequently, an imperative program can be executed by supplying an initial state s and
stripping off all the 𝜏s (internal steps) until s ′ is reached. If the program is divergent (i.e.,
non-terminating) it will never get a final state, so execution will hang.
   To aid the modelling of programs in our tool, we provide the following command:
     Definition 4.3 (Program command).
     s                                          {                                                    
       program Pr (x1 :: T1, · · · , xn :: Tn )     Pr :: T1 × · · · × Tn ⇒ S ⇒ (E, S)htree)
                                                 =
         over S = Body (x1, · · · , xn )            Pr ≜ (𝜆(x1, · · · , xn ). Body (x1, · · · , xn ))

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL         15


A program takes a tuple of parameters (x1, · · · , xn ) and operates over a store S. The program’s
body is a parametric ITree in x1 · · · xn . These parameters are not program variables (lenses)
but logical variables. Intuitively, they are constants that cannot be written to.
  As an example, below is the definition of a simple imperative program for reversing a list:
  Example 4.4 (List Reversal Program).

   program reverse (xs :: int list) over state =
   "ys := []; i := 0;
    while i < length xs
    do
        ys := xs!i # ys;
        i := i + 1
    od"

We define the program reverse, with input parameter xs :: int list. It operates over
the store type state, containing the variables i :: nat and ys :: int list. The program
iterates through the input xs, pushing each element on ys, with the result that xs is reversed.
   Next, we define a command execute that executes an ITree-based program with given
argument. For example, we can execute reverse with the following command:

   execute " reverse [1 ,2 ,3 ,4 ,5]"},

This executes reverse with the input list [1,2,3,4,5]. The command generates code using
the aforementioned ITree semantics, executes it, and then reports termination with the final
state [y { [5, 4, 3, 2, 1], i { 5].
   A terminating program with no nondeterminism is denoted by a pure ITree of the form
𝜏 n ✓v , where v is the final state or return value. Since we do not generally know how many 𝜏
events a program may perform, execution involves stripping off all the 𝜏 events until a return
value is encountered. Since programs in general can fail to terminate, it is necessary to place
an upper bound on the number of 𝜏 events that can be skipped. We therefore provide a
global constant called MAX SIL STEPS :: nat, which acts as a timeout for execution. Then,
we use the function un Sils n :: nat ⇒ (E, S)itree ⇒ (E, S)itree to strips a number n of 𝜏
events of an ITree, with n ≤ MAX SIL STEPS.
   We can finally realise program execution using Isabelle’s evaluation mechanism, as present
in the value command, which evaluates an executable term [2, 40]. The evaluator can
perform concrete execution using the SML code generator, when the program contains no
free variables (as in the above example), and symbolic execution using normalisation by
evaluation or the simplifier. The former is most efficient, and so is the default behaviour for
execute.
   An execution can produce one of four possible results: (1) termination with a final state,
(2) an abort, (3) a visible event, and (4) a timeout. A timeout occurs if MAX SIL STEPS
𝜏 events have occurred without producing a return or visible event. For example, execute
"Div" results in a timeout. A termination results if execution encounters a Ret before
reaching the maximum number of 𝜏s. This being the case, the interface displays the final
state of each variable.
   Abortion occurs when an empty visible event is encountered (i.e. stop), following a finite
number of 𝜏 events. Thus, if the execute command encounters a Vis constructor, it checks

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
16                                                      Simon Foster, Chung-Kil Hur, and Jim Woodcock


whether the choice function is empty. If it is empty, then the execution has aborted. Otherwise,
it indicates that an event choice was encountered and goes no further. For ITrees that use
visible events, we typically cannot use such a non-interactive execution. We must instead
rely on animation (§6), which allows further user input when a visible event is presented.

4.3   Nondeterminism
The operators given so far allow us to model only deterministic programs, which typically
reduce to pure functions on the state. However, nondeterminism is useful both as a specifica-
tion device and where design choices are deferred. Nondeterministic decisions can be encoded
by introducing a special channel nd, which the environment can conceptually use to resolve,
acting as an oracle. Here, I is an index type, which denotes the maximum cardinality of
any choices. Whilst, in theory, I can be any type, we can typically only animate countable
choices, and therefore, for now, we set I ⊆ N. We can now use this to define the internal
choice operator.
  Definition 4.5 (Countable nondeterminism).
  Assume a channel nd carrying a value of type N and a set I ⊂ N exists. Then, we encode
nondeterministic choice as
                         l
                            • C (i) ≜ Vis (𝜆 nd.i | i ∈ I • P (i)).
                             i ∈I

This constructs a visible event choice over nd events parameterised by the elements of
I . The particular index chosen is passed to P as a parameter. We        can then define a
                                            d
binary nondeterministic choice as C1 ⊓ C2 ≜   i ∈ {0,1} • C1 ⊳ i = 0 ⊲ C2 . Programs containing
nondeterministic choices cannot be directly executed using the execute command, as the
events must be resolved using animation (see §6).

4.4   Predicative Semantics and Refinement
We now focus on a predicative semantic interpretation for ITrees, which allows us to link
with the established UTP predicative semantics for imperative programs [17, 44]. This
semantics has many uses, but one particular use is to provide a notion of refinement for
nondeterministic imperative programs.
    UTP uses predicate calculus as a unifying language for programs and specifications.
Dijkstra-style programs can be denoted as alphabetised relations, predicates that relate the
initial values of variables to their final values. For example, assuming a store with three
integer variables x, y, and z, an assignment x := x + 1 can be denoted by the predicate
x ′ = x + 1 ∧ y ′ = y ∧ z ′ = z, where x is the initial value of x and x ′ is its final value.
    Central to UTP is a notion of refinement P ⊑ Q for alphabetised relations P and Q, which
means that Q is more deterministic or concrete than Q. For example, we can write the
specification x ′ > x, which means that in the final state, x should be strictly greater than its
initial value. Then, using refinement, we can demonstrate that x ′ > x ⊑ x := x + 1, meaning
that the program on the right implements the specification on the left. The refinement order
induces a complete lattice of alphabetised relations. It gives rise to fixed-point operators 𝜇 F
(least fixed point) and 𝜈F (greatest fixed point), which can specify iterative and recursive
behaviour. UTP provides the predicative semantics for the Circus language [57].
    To relate our ITree-based semantics with such predicative semantics, we must distinguish
a program’s terminating states from divergence. We can reason about termination and
                                                  tr
divergence with our transition relation, P −→ Q. Terminating imperative programs are

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL         17


characterised by pure ITrees that eventually reach a Ret. We define the set of return values
of an ITree using the following function:
                                                                  tr
  Definition 4.6 (Return Values). R(P) = {x | ∃ tr . P −→ ✓x }.
R(P) induces the set of possible values a process P may return, whenever P terminates.
In other words, R(P) is the set of reachable final states. If R(P) = ∅, then P can never
terminate. R(P) abstracts over all possible traces through existential quantification, and
therefore, it does not distinguish return values that arise from different event interactions. All
events are, therefore, effectively treated as nondeterminism in this semantic interpretation.
Below, we give the valuations of R(P) for the main ITree constructors.
  Theorem 4.7 (Return Values for ITree Constructors).
                                    R(✓x ) = {x }
                                  R(𝜏P) = R(P)
                                            Ø
                               R(Vis(F )) =   {R(P) | P ∈ ran(F )}
                                            Ø
                               R(P >>= Q) =   {R(Q(x)) | x ∈ R(P)}
                                  R(stop) = R(div) = ∅
A Ret returns a single value. A Sil returns the values following the 𝜏 event. A visible event
(Vis) returns all possible values returned by the continuation ITrees, P ∈ ran(F ). If we view
the ITree as a transition graph, we take the values returned on all paths. A bind P >>= Q first
calculates the return values of P, then uses these as the possible inputs for Q, and calculates
all the resulting return values. Neither stop or div have any return values because they do
not successfully terminate. We can now use this function to provide a predicative semantic
interpretation for ITrees.
  Definition 4.8 (Predicative semantics). JPKp = (𝜆(s, s ′ ). s ′ ∈ R(P (s)))
The function JPKp induces a predicate of type S × S ⇒ B for the homogeneous ITree P,
which corresponds to a binary relation. Thus, JPKp (s, s ′ ) holds whenever s ′ is reachable from
the start state s. With this function, we can show that our imperative programs respect a
UTP-style predicative semantics [44].
  Theorem 4.9 (Predicative semantics of loop-free imperative programs).

                           J⟨𝜎⟩Kp (s, s ′ ) = (s ′ = 𝜎 (s))
                         JP # QKp (s, s ′ ) = ∃ s0 • JPKp (s, s0 ) ∧ JQKp (s0, s ′ )
                                                                                     

                          JP ⊳ B ⊲ QKp = B (s) ∧ JPKp (s, s ′ ) ∨ ¬B (s) ∧ JQKp (s, s ′ )
                                                                                         

        JStopKp (s, s ′ ) = JDivKp (s, s ′ ) = False
                        JP ⊓ QKp (s, s ′ ) = JPKp (s, s ′ ) ∨ JQKp (s, s ′ )
                                                                               

A state update applies the update function to the initial state s to obtain the final state s ′ .
The semantics of an assignment x := e is a special case, conceptually x ′ = e(s) ∧ y ′ = y, for
all other variables y in S. The predicative semantics for P # Q yields the usual definition of
relational composition: an intermediate state s0 , a final state for P and an initial state for
Q. Conditional behaves as P when B is true in the initial state and Q otherwise. Both Stop

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
18                                                           Simon Foster, Chung-Kil Hur, and Jim Woodcock


and Div have the same interpretation False, as this semantics cannot distinguish between
deadlock and divergence. Finally, a state pair is satisfied by a nondeterministic choice P ⊓ Q
if it is satisfied by either P or Q, which is the usual UTP interpretation of nondeterministic
choice as disjunction [44].
   Next, we consider the predicative semantics of iteration. First of all, we note the following
corollary of Theorem 3.15:
     Corollary 4.10 (Iteration return values).
                                                                                     tr
     R((while b do P od) (s)) = {s ′ | (¬P (s) ∧ s = s ′ ) ∨ (∃ tr . B (s) ∧ (B, s) −→∗✓ s ′ ∧ ¬B (s ′ ))}
The return values for a loop started in state s is precisely the set of states for which there
is a number of iterations of P yielding some trace tr. Whilst we could now express the
predicative semantics in these terms, it is more convenient and concise to do this in terms of
the reflexive transitive closure operation R∗ . We first reiterate a result of the Isabelle/HOL
standard library:
     Theorem 4.11 (Reflexive Transitive Closure paths).
            R∗ (s, s ′ ) ⇔ s = s ′ ∨ (∃ xs. ∀ i < length (xs). R((s#xs)!i, xs!i) ∧ x ′ = last (xs))
A pair of states (s, s ′ ) are related by R∗ either when s = s ′ , or there is a path xs leading
from s to s ′ through several iterations of R. Here, the path is a list of states, where each
consecutive pair of states, starting from s and ending with s ′ , are related by R. With this
result, we can now express the predicative semantics of iteration:
     Theorem 4.12 (Predicative semantics of iteration).
                               Jwhile B do C odKp = (¿B? ; JC Kp ) ∗ ; ¿¬B?
For conciseness, the predicate semantics for while is expressed point-free. The notation ¿P?
denotes a test, i.e. 𝜆(s, s ′ ). P (s) ∧ s ′ = s, which skips states that satisfy P. The semicolon
operator (P ; Q) denotes relational composition, such that JP # QKp = (JPKp ; JQKp ). In this
relational context, a while loop iterates C when B is true and ends when B is false. This
corresponds to the usual Kleene algebra interpretation of iteration [3, 38].
   The predicative interpretation in Theorem 4.9 induces a homomorphism between the ITree
semantics and the relational semantics for each of the imperative programming operators (:=,
#, ⊳ b ⊲, etc.). This homomorphism is not only of theoretical interest but also practical benefit.
Using the equations as code equations for the Isabelle/HOL code generator [40] allows us to
employ the ITree semantics as a means to generate code for and execute relational imperative
programs (see §6). We can also use our predicative semantics to obtain a notion of refinement
for ITrees. We first recall the usual definition of refinement for relational programs in UTP:
     Definition 4.13 (Predicative refinement). (P ⊑ Q) ≜ (∀(s, s ′ ). Q(s, s ′ ) → P (s, s ′ ))
This is the usual UTP definition of refinement as a universally closed reverse implication.
Specifically, P is refined by Q (P ⊑ Q) if Q contains no more observable behaviours than
P. Since we can interpret an ITree as a predicate, we can define (P ⊑p Q) ≜ JPKp ⊑ JQKp .
In particular, we can now use refinement to reduce nondeterminism: P ⊓ Q ⊑p P. This
refinement relation forms a preorder, but it is not antisymmetric. This is because the
predicative semantics is too coarse and does not, for example, distinguish Stop and Div ,
which are both False. For antisymmetry, we would need a finer predicative interpretation,
such as the UTP theory of designs [17] or reactive designs [29], but this is out of the scope
of this paper.

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL                19


4.5    Hoare logic and Weakest Preconditions
We can now use our predicative interpretation of ITrees to define a partial correctness Hoare
logic.
  Definition 4.14 (Partial Correctness Hoare Logic).
                                                                       tr
                   { P } C { Q } ≜ (∀(s, s ′, tr) • P (s) ∧ C (s) −→ ✓s′ → Q(s ′ ))
Whenever P is satisfied by initial state s, and C when started in s terminates in final
state s ′ , it follows that Q is satisfied by s ′ . This is partial correctness because we do not
commit if C aborts or does not terminate. We can handle these additional aspects separately
through deadlock-freedom and termination checks or by a total correctness Hoare logic. Our
definition of the Hoare triple can alternatively be characterised directly using refinement in
the UTP style, as the following theorem demonstrates.
  Theorem 4.15. { P } C { Q } if and only if (P ◀ → Q ▶ ) ⊑ JC Kp
  Here, P ◀ and Q ▶ are shorthands for 𝜆(s, s ′ ). P (s) and 𝜆(s, s ′ ).Q(s ′ ) lift these predicate
expressions to pre- and postconditions. We construct a relational specification for the program
and then use it to assert a refinement. This allows us to obtain all the laws of Hoare logic
for straight-line programs (cf. [28]), for example:
  Theorem 4.16 (Hoare logic laws).
       P → Q [e/x]           { P } C1 { Q }     { Q } C2 { R }              { P } C1 { Q }     { P } C2 { Q }
      { P } x := e { Q }            { P } C1 # C2 { R }                            { P } C1 ⊓ C2 { Q }
  For while loops, using the construct introduced in Definition 3.8, there is a little more
work to be done. Recall the partial correctness law for Hoare logic:
  Theorem 4.17 (Partial Correctness While law).
                                          {P ∧ B}C {P }
                                   { P } while B do C od { ¬B ∧ P }
Here, P is the loop invariant, which must remain true whenever the body C is executed. We
outline the mechanised proof below, which uses Theorem 3.15.
   Proof. From Definition 4.14, we need to show that given an initial state s satisfying
P, whenever ( while B do S od) (s) →− ✓s′ , then it follows that s ′ satisfies ¬B and P (partial
correctness). From Theorem 3.15, we know that the loop terminates immediately or executes
several times. Suppose it terminates immediately, then clearly P (s) and ¬B (s). Suppose it
executes, a chain chn leads to s ′ such that ¬B (s ′ ). The premises of the loop invariant law
tell us that for any state s0 , such that P (s0 ) and B (s0 ), whenever C (s0 ) →− ✓s1 then also
P (s1 ). As a result, we can deduce that any s0 ∈ states(chn) and subsequent state s1 must
maintain the invariant. This being the case, it also particularly follows that P (s ′ ), since s ′ is
such an s1 state. This completes the proof.                                                        □
  In addition to Hoare logic, we can also characterise the weakest (liberal) preconditions:
  Definition 4.18 (Weakest Preconditions).
                               wp C P ≜ (𝜆 s. ∃ s ′ . JC Kp (s, s ′ ) ∧ P (s ′ ))
                              wlp C P ≜ (𝜆 s. ∀ s ′ . JC Kp (s, s ′ ) → P (s ′ ))

             ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
20                                                      Simon Foster, Chung-Kil Hur, and Jim Woodcock


The weakest precondition wp C P obtains the weakest precondition required for C to reach
a state satisfying P. It formally requires that for any initial state s, there is a final state s ′ ,
such that P (s ′ ). In particular, we can use the weakest precondition to calculate the domain
or “precondition” of a program: pre (C ) ≜ wp C true. For ITrees, this is the set of initial
states that do not lead to deadlock or divergence. For imperative programs specifically, this
can be considered the initial states for which the program terminates. The weakest liberal
precondition is similar, but for any final state s ′ of C that P (s ′ ) holds, it does not require
such an s ′ exists. Both of these laws satisfy the standard laws [22], which we have previously
presented for Isabelle/UTP [28].
   As usual, we can use the simplifier to calculate the weakest preconditions for a program in
Isabelle/HOL equationally. Moreover, we also prove the following standard theorem linking
Hoare logic and wlp:
     Theorem 4.19. { P } C { Q } ⇔ (P → wlp C Q)
We can prove a Hoare triple by calculating the wlp, and then proving the precondition P
satisfies the resulting predicate. Finally, we can use wp to define the total correctness Hoare
triple:
     Definition 4.20 (Total Correctness Hoare Logic).
                                                                           
                         [ P ] C [ Q ] ≜ { P } C { Q } ∧ (P → pre (C )
This follows the usual intuition of total correctness = partial correctness + termination.
Here, P → pre (C ) means that the precondition is a sufficient condition to ensure that C
terminates. With this definition, we can obtain the corresponding laws to those in 4.16, and
also the total correctness law for loops, which requires a decreasing variant expression V :
     Theorem 4.21 (Total Correctness While law).
                               [P ∧ B ∧ V = z]C [P ∧ V < z]
                                [ P ] while B do C od [ ¬B ∧ P ]
The proof of this depends on Theorem 3.15.
  We will make further use of the weakest preconditions when we develop our Z-Machine
tool in Section 7. For now, we are turning our attention to the automation of program
verification.

4.6     Verification Condition Generation
Automation of program verification is conducted, as usual, through a verification condition
generator (VCG). Our VCG method repeatedly applies Hoare logic laws to obtain a collection
of verification condition predicates, following a standard approach [3, 38]. The resulting
predicates can often be discharged by Isabelle’s automated proof methods, like blast, metis,
and smt, with the help of sledgehammer . If verification fails, we can find errors using
counterexample finders, like nitpick and quickcheck.
   For automated reasoning, we need laws that avoid the introduction of meta-variables,
as these can introduce backtracking and hamper automation. For example, the general
sequential composition law in Theorem 4.16 and iteration law in Theorem 4.17 introduce
variables that only appear in the hypotheses, and a suitable witness must be supplied.
Instead, we specialise the Hoare logic theorems to avoid this. In particular, we introduce the
following two corollaries for assignment.

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL         21


  Corollary 4.22 (Forward and Backward Assignment Laws).
             { x = e[x0 /x] ∧ P [x0 /x] } C { Q }                       { P } C { Q [e/x] }
                                                  x0 ∉ fv (e, P )
                    { P } x := e # C { Q }                             { P } C # x := e { Q }
The forward law allows us to push the effect of the assignment into the precondition. We
introduce a new fixed logical variable, x0 , which stands for the initial value of x before the
assignment occurred. We substitute x for x0 in the assigned expression e and the precondition
P. The backward law similarly applies the assignment to the postcondition.
   VCG, as usual, depends on the annotation of loops with invariants. We adopt the approach
of Armstrong et al. [3] and introduce the syntax while B invariant I do C od, which annotates
with the invariant I . This annotation is semantically vacuous and exists only to help proof
automation using the following derived law.

  Theorem 4.23 (Loop Invariant Annotation).
                           {I ∧ B}C {I }         P→I          ¬B ∧ I → Q
                               { P } while B invariant I do C od { Q }
This requires we prove that I is an invariant of the loop body, I weakens precondi-
tion P, and I strengthens postcondition Q when the loop condition does not hold. The
proof combines the consequence law and the partial correctness law for while loops. Sim-
ilarly, we derive a corresponding total correctness law, which uses a variant annotation:
while B invariant I variant V do C od, where V is the variant expression.
   Finally, we implement the vcg proof method, which implements the following steps:
  (1) Atomise assignments and conditionals where possible, using the Theorem 4.2;
  (2) Repeatedly apply specialised Hoare logic laws as introduction rules to decompose goal;
  (3) Evaluate substitutions in resulting expressions and convert them to HOL proof obliga-
      tions.
   The result is a set of VCs for which discharge can be attempted. We can now annotate
our imperative list reversal program from Example 4.4 with an invariant and a variant to
allow its verification:

  Example 4.24 (Annotated List Reversal Program).

program reverse (xs :: int list) over state =
"ys := []; i := 0;
 while i < length xs
 invariant ys = rev (take i xs)
 variant length xs - i
 do
     ys := xs!i # ys;
     i := i + 1
 od"


We supply the invariant ys = rev(take i xs), since ys is always the first i elements of
xs in reverse. The functions take and rev are defined in Isabelle/HOL. The variant length
xs - i counts down from the length of xs to zero.

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
22                                                      Simon Foster, Chung-Kil Hur, and Jim Woodcock


  With this, we want to prove the Hoare triple [ True ] reverse(xs) [ ys = rev (xs) ] : the
imperative program satisfies the functional specification provided by the rev function.
Applying the vcg method to this proof goal yields a single verification condition:
        xs ! i # rev (take i xs) = rev (take (i + 1) xs) for i < length(xs).
This states that taking the first i + 1 elements of xs and then reversing it can be achieved
by appending the ith element of xs at the beginning of the reversed i elements. This can be
discharged by sledgehammer using the built-in laws from Isabelle/HOL. The variant proof is
straightforward and discharged simply by the simplifier.
   Although this is a trivial example, we have verified more substantial benchmark examples,
such as sorting algorithms, with a high level of automation provided by sledgehammer .

5     REACTIVE AND CONCURRENT PROGRAMMING
In this section, we move on from imperative programs and give an ITree semantics to
deterministic fragments of the CSP [15, 42] and Circus [57, 73] process languages. Our
deterministic CSP fragment is consistent with the one identified by Roscoe [63, Section 10.5].
The standard CSP denotational semantics is provided by the failures-divergences model [15,
63], and we provide preliminary results on linking to this in §5.3.

5.1     CSP
CSP processes are parametrised by an event alphabet (Σ), which specifies the possible ways a
process communicates with its environment. For ITrees, Σ is provided by the type parameter
E. Whilst the event sort of an ITree E is typically infinite, in process algebraic languages,
like CSP, it is usually expressed with a finite set of channels, which can carry data of various
types. Here, we characterise channels abstractly using prisms [59], a concept well known in
the functional programming world:
  Definition 5.1 (Prisms). A prism is a quadruple (V, Σ, match, build) where V and Σ are
non-empty sets. Functions match : Σ →
                                    ↦ V and build : V ⇒ Σ satisfy the following laws:
                match(build x) = x         y ∈ dom(match) → build (match y) = y
                  Δ
               − E if X is a prism with ΣX = E and VX = V .
We write X : V →
Intuitively, a prism abstractly characterises a datatype constructor, E, taking a value of
type V. Then, build is the constructor, and match is the destructor, which is partial due
to the possibility of several disjoint constructors. For CSP, each prism models a channel in
E carrying a value of type V. We have created a command chantype, which automates
the creation of prism-based event alphabets. Technically, this is achieved by creating an
algebraic data type with a constructor for each channel and a corresponding prism for each
constructor.
   CSP processes typically do not return data, though their components may, and so they
are typically denoted as ITrees of type (E, ())itree, returning the unit type (). An example
is skip ≜ Ret (), which is a degenerate form of Ret. We now define the basic CSP operators.

     Definition 5.2 (Basic CSP Constructs).

                              Δ
                   inp :: (V →
                             − E) ⇒ V set ⇒ (E, V )itree
               inp c A ≜ Vis (𝜆 e ∈ dom(matchc ) ∩ buildc (| A )| • Ret (matchc e))

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL              23


                         Δ
         outp :: (V →
                    − E) ⇒ V ⇒ (E, ())itree                      guard b :: B ⇒ (E, ())itree
      outp c v ≜ Vis {build c v ↦→ Ret ()}                       guard b ≜ (if b then skip else stop)
An input event (inp c A) permits any event over the channel c, that is e ∈ dom(matchc ),
provided that its parameter is in A (e ∈ buildc (| A )| ). It returns the value received for use
by a continuation. It corresponds to the trigger construct in [75]. With this and monadic
bind, the usual CSP input prefix can be denoted as
                                  c?x → P (x) ≜ (inp c UNIV >>= P)
where UNIV is the set of all values of a particular type. The input prefix receives any value
over c and then passes it on to P.
   An output event (outp c v) permits a single event, v, on channel c and returns a null value
of type (). We can then denote the standard CSP output prefix as
                                   c!v → Q ≜ (outp c v >>= (𝜆 x. Q)
                                                                                             Δ
We also define the special case sync e ≜ outp e () for a basic event e :: () →− E. A guard b
behaves as skip if b = true and otherwise deadlocks. It corresponds to the guard in CSP,
which can be defined as b & P ≜ (guard b >>= (𝜆 x. P)).
  Using the monadic “do” notation, which boils down to applications of >>=, we can now
write simple reactive programs such as do{x ← inp c; outp d (2 · x); Ret x }, which inputs x
                    Δ
over channel c : N →− E, outputs 2 · x over channel d, and finally terminates, returning x.
  Next, we define the external choice operator, P 2 Q, where the environment resolves the
choice with an initial event of P or Q. In CSP, 2 can also introduce nondeterminism; for
example, (a → P) 2 (a → Q) introduces an internal choice since the a event can lead to
P or Q, and is equal to a → (P ⊓ Q). Since we explicitly wish to avoid introducing such
nondeterminism, we make a design choice to exclude this possibility by construction. There
are other possibilities for handling nondeterminism in ITrees, which we consider in §9. As
for >>=, we define external choice corecursively using a set of ordered equations.
  Definition 5.3 (External choice). P 2 Q, is defined by the following set of equations:
  (Vis F ) 2 (Vis G) = Vis (F ⊙ G)             (Ret x) 2 (Vis G) = Ret x
         (Sil P ′ ) 2 Q = Sil (P ′ 2 Q)        (Vis F ) 2 (Ret y) = Ret y
         P 2 (Sil Q ) = Sil (P 2 Q )
                     ′                 ′
                                                (Ret x) 2 (Ret y) = (if x = y then (Ret x) else stop)
  where F ⊙ G ≜ (dom(G) −
                        ◁ F ) ⊕ (dom(F ) −
                                         ◁ G)
   An external choice between two functions, F and G, essentially combines all the choices
presented using F ⊙ G. The caveat is that if the domains of F and G overlap, then any
events in common are excluded. Thus, ⊙ restricts the domain of F to maplets e ↦→ P where
e ∉ dom(G), and vice-versa. This has the effect that (a → P) 2 (a → Q) = stop, for example.
In the special case that dom(F ) ∩ dom(G) = ∅, P ⊙ Q = P ⊕ Q. We chose this behaviour to
ensure that 2 is commutative, though we could alternatively bias one side.
   Internal steps on either side of 2 are greedily consumed. Due to the equation order, 𝜏
events have the highest priority, following a maximal progress assumption [41]. Return events
also have priority over visible events. If two returns are present, then they must agree on
the value. Otherwise, they deadlock. External choice satisfies several essential properties:
  Theorem 5.4 (External Choice Properties).
  P2Q=Q2P                stop 2 P = P      div 2 P = div    P 2 (𝜏 n Q) = (𝜏 n P) 2 Q = 𝜏 n (P 2 Q)

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
24                                                      Simon Foster, Chung-Kil Hur, and Jim Woodcock




                      (Vis F 2 Vis G) >>= H = (Vis F >>= H ) 2 (Vis G >>= H )
  The external choice is commutative and has stop as a unit. It has div as an annihilator
because the 𝜏 events mean no other activity is chosen. A finite number of 𝜏 events on the left
or right can be extracted to the front. Finally, bind distributes from the left across a visible
event choice. We prove these properties using coinduction (Theorem 3.7), case analysis
on stability of constituent processes, followed by several invocations of sledgehammer to
discharge the resulting provisos.
  Using the operators defined so far, we can implement the buffer from Examples 2.1 using
a monadic syntax:
chantype Chan = Input::int Output::int State::"int list"

definition buffer :: "int list ⇒ (Chan, int list) itree" where
"buffer = loop (𝜆 s.
                      do { i ← inp Input {0..}; Ret (s @ [i]) }
                   2 do { guard(length s > 0); outp Output (hd s); Ret (tl s) }
                   2 do { outp State s; Ret s })"
We first create a channel type Chan, which has channels (prisms) for inputs and outputs
and to view the current buffer state. We define the buffer process as a simple loop with
a choice of three branches inside. The variable s::int list denotes the state. The first
branch allows a value to be received over Input, and then returns s with the new i value
appended, and then iterates. The second branch is only active when the buffer is not empty.
It outputs the head on Output and returns the tail. The final branch outputs the current
state. In §6, we will see how such an example can be animated.
   Next, we tackle parallel composition. The objective is to define the usual CSP operator
P |[ E ]| Q, which requires that P and Q synchronise on the events in E and can otherwise
evolve independently. We first define an auxiliary operator for merging choice functions.
               mergeE (F, G) = (𝜆 e ∈ dom(F ) \ (dom(G) ∪ E) • Left (F (e)))
                              ⊕ (𝜆 e ∈ dom(G) \ (dom(F ) ∪ E) • Right (G (e)))
                              ⊕ (𝜆 e ∈ dom(F ) ∩ dom(G) ∩ E • Both(F (e), G (e))
Operator mergeE (F, G) merges two event functions, which are being offered by two parallel
composed ITrees. Each event is tagged depending on whether it occurs on the Left, Right,
or Both sides of a parallel composition. An event in dom(F ) can occur independently when
not in E or dom(G). The latter proviso is required, like for 2, to prevent nondeterminism
by disallowing the same event from occurring independently on both sides. An event in
dom(G) can occur independently through the symmetric case for dom(F ). An event can
synchronise provided it is in the domain of choice functions and the set E. We use this
operator to define the generalised parallel composition. For the sake of presentation, we
present partial functions as sets.
     Definition 5.5. P ∥ E Q is defined corecursively by the following equations:
                               {e ↦→ (P ′ ∥ E (Vis G)) | (e ↦→ Left (P ′ )) ∈ mergeA (F, G)}
 (Vis F ) ∥ E (Vis G) = Vis ­ ⊕ {e ↦→ ((Vis F ) ∥ E Q ′ ) | (e ↦→ Right (Q ′ )) ∈ mergeE (F, G)} ®
                             ©                                                                   ª
                                           ′      ′                  ′    ′
                             « ⊕ {e ↦→ (P ∥ E Q ) | (e ↦→ Both(P , Q )) ∈ mergeE (F, G)} ¬
              ′                ′
       (Sil P ) ∥ E Q = Sil (P ∥ E Q)        P ∥ E (Sil Q ) = Sil (P ∥ E Q ′ )
                                                         ′


ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL         25


  (Ret x) ∥ E (Ret y) = Ret (x, y)
 (Ret x) ∥ E (Vis G) = Vis {e ↦→ Ret x ∥ E Q ′ | (e ↦→ Q ′ ) ∈ G}
  (Vis F ) ∥ E (Ret y) = Vis {e ↦→ P ′ ∥ E Ret y | (e ↦→ P ′ ) ∈ F }

   The most complex case is for Vis, which constructs a new choice function by merging
F and G. Three partial functions again represent the three cases. The first two allow the
left and right to evolve independently to P ′ and Q ′ , respectively, using one of their enabled
events, leaving their opposing side, Vis G and Vis F , respectively, unchanged. The third case
allows them both to evolve simultaneously on a synchronised event.
   The Sil cases allow 𝜏 events to happen independently and with priority. If both sides can
return a value, x and y, respectively, then the parallel composition returns a pair, which can
later be merged if desired. The final two cases show what happens when only one side has
a return value and the other has visible events. In this case, the Ret value is retained and
pushed through the parallel composition until the other side also terminates.
   We use ∥ E to define two special cases for CSP: P |[ E ]| Q ≜ (P ∥ E Q) >>= (𝜆(x, y). Ret ())
and P ||| Q ≜ P |[ ∅ ]| Q. As usual in CSP, these operators do not return any values, and so
P, Q :: (E, ())itree. The P |[E ]| Q operator is similar to ∥ E , except if both sides terminate, any
resultant values are discarded, and a null value is returned. This is achieved by binding to a
simple merge function. P and Q do not return values, so this does not affect the behaviour,
just the typing. The interleaving operator P ||| Q, where there is no synchronisation, is
defined as P |[ ∅ ]| Q. We prove several algebraic laws:

                  (P ∥ E Q) = (Q ∥ E P) >>= (𝜆(x, y). Ret (y, x))       div ∥ E P = div

                     P |[ E ]| Q = Q |[ E ]| P    P ||| Q = Q ||| P    skip ||| P = P
Parallel composition is commutative, except that we must swap the outputs, and so |[E]| and
||| are commutative as well. Parallel has div as an annihilator for similar reasons to 2. For |||,
skip is a unit since there is no possibility of communication and no values are returned.
    The final operator we consider is hiding, P \ A, which turns the events in A into 𝜏s:

  Definition 5.6 (Hiding). P \ A is defined corecursively by the following equations:
                             
                             
                              Sil (F (e) \ A)                      if A ∩ dom(F ) = {e}
                             
                             
               Vis (F ) \ A = Vis {(e, P \ A) | (e, P) ∈ F }        if A ∩ dom(F ) = ∅
                             
                              stop
                             
                                                                    otherwise
                             
                Sil (P) \ A = Sil (P \ A)        Ret x \ A = Ret x

We consider a restricted version of hiding where only one event can be hidden at a time
to avoid nondeterminism. When hiding the events of A in the choice function F , there are
three cases: (1) there is precisely one event e ∈ A enabled, in which case it is hidden; (2) no
enabled event is in A, in which case the event remains visible; (3) more than one e ∈ A is
enabled, and so we deadlock. We again impose maximal progress here so that an enabled
event to be hidden is prioritised over other visible events: (a → P [] b → Q) \ {a} = 𝜏P, for
example. Despite the significant restrictions on hiding, it supports the typical pattern where
one output event is matched with an input event. Moreover, a priority can be placed on the
order in which events are hidden, rather than deadlocking, by sequentially hiding events.
Hiding can introduce divergence, as the following theorem shows: (iter (sync e)) \ e = div .

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
26                                                             Simon Foster, Chung-Kil Hur, and Jim Woodcock


5.2     Circus
While CSP processes can be parametrised to allow modelling states, there is no support
for explicit state operators like assignment. The do notation somewhat allows variables,
but these are immutable and are not preserved across iterations. Circus [57, 73] is a CSP
extension allowing state variables.
   We can characterise Circus through a Kleisli lifting of CSP processes that return values so
that Circus actions are homogeneous KTrees. Then, thanks to the compositionality of our
ITree-based semantics, we can use the operators defined in §4, such as assignment x := e, to
allow manipulation of the state. Then, we define the core operators for concurrency:
     Definition 5.7 (Circus Operators).
                 c?x:A → F (x) ≜ (𝜆 s. inp c A >>= (𝜆 x. F (x) s))
                        c!e → P ≜ (𝜆 s. outp c (e s) >>= (𝜆 x. P s))
                          P 2 Q ≜ (𝜆 s. P (s) 2 Q(s))
                                                                                                 
             P |[ns1 |E |ns2 ]| Q ≜ 𝜆 s. (P (s) ∥ E Q(s)) >>= (𝜆(s1, s2 ). s ◁ns1 s1 ◁ns2 s2 )
The operators are defined by the lifting of their CSP equivalents. An output c!e → P carries
an expression e rather than a value, which can depend on the state variables. The main
complexity is the Circus parallel operator, P |[ns1 |E |ns2 ]| Q, which allows P and Q to act on
disjoint portions of the state, characterised by the name sets ns1 and ns2 . We represent ns1
and ns2 as independent lenses, ns1 ⊲⊳ ns2 , though they can be thought of as sets of variables
with ns1 ∩ ns2 = ∅. The definition of the operator first lifts ∥ E and composes this with a
merge function. The merge function constructs a state consisting of the ns1 region from the
final state of P, the ns2 region from Q, and the remainder from the initial state s. This is
achieved using the lens override operator s1 ◁X s2 , which extracts the region described by X
from s2 and overwrites the corresponding region in s1 , leaving the complement unchanged.
   We can now model the buffer from Example 2.1 with these operator definitions. Given a
state variable buf::int list, the buffer can be expressed in Isabelle/HOL as follows:
     Example 5.8. Buffer in ITree-based Circus

     buf := [];
     loop (( Input ?(i) → buf := buf @ [i])
           2 ( length (buf) > 0 & Output !( hd buf) → buf := tl buf)
           2 State !( buf) → Skip)
We update the state with assignments threaded through sequential composition.
  Our Circus operators satisfy several standard laws [32, 57], beyond the CSP laws, for
example:
                    ⟨𝜎⟩ # (P 2 Q) = (⟨𝜎⟩ # P) 2 (⟨𝜎⟩ # Q)
                 P |[ns1 |E |ns2 ]| Q = Q |[ns2 |E |ns1 ]| P                    if ns1 ⊲⊳ ns2
State updates are distributed through external choice from the left. Circus parallel composi-
tion is commutative, provided that we also switch the name sets.

5.3     Denotational Semantics
Next, we show how ITrees are related to the standard failures-divergences semantics of
CSP [15]. The utility of this link is to both allow symbolic verification of ITrees and

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL                  27


allow them to act as a target of step-wise refinement. In this way, we can use the existing
mechanisation of the CSP set-based and relational semantics [32, 67] to capture and reason
about nondeterministic specifications and use ITrees to provide executable implementations.
   In the failures-divergences model, a process is characterised by two sets: F :: (E ✓ list ×
E set) set and D :: P(E list), which are, respectively, the set of failures and divergences. A
failure is a trace of events plus a set of events that can be refused at the end of the interaction.
A divergence is a trace of events that leads to divergent behaviour. A distinguished event
✓ ∈ E is used as the final element of a trace to indicate that this is a terminating observation.
   For example, consider the process a → c → skip 2 b → div , which initially permits an a
or b event, and following a permits a c event. It exhibits the failure ( [], {c}) since before
any events are performed, the event c is being refused. A second failure is ( [a], {a, b}), since
after performing an a, only c is enabled, and the other events are refused. A third failure is
([a, c, ✓], {a, b, c}), which represents successful termination, after which all events are refused.
This process also has a divergence trace [b] since the process diverges after performing event
b. If a divergent state is unreachable, then D is empty. Here, we show how to extract F and
D from any ITree, and thus processes constructed from the operators of §5.
   In CSP, one likes to show that there are no divergent states, a property called divergence
freedom. The following inductive-coinductive definition captures it:
  Definition 5.9 (Divergence Freedom).
               −          P       R       ran(F ) ⊆ R
                            ⇒ ⇒




                                                                         Ð
                                                            div-free ≜       {R | R ⊆ {P | P       R}}



                                                                                               ⇒
          ✓x       R     𝜏P       R       Vis F    R
               ⇒




                                               ⇒




   Predicate P      R is defined inductively. It requires that P stabilises to a Ret or a Vis
                   ⇒




whose continuations are all contained in R. Then, div-free is the largest set consisting of
all sets R = {P | P      R} and is coinductively defined. If we can find an R such that for
                        ⇒




every P ∈ R, it follows that P     R, that is R is closed under stabilisation, then any P ∈ R
                                      ⇒




is divergence-free. Essentially, R needs to enumerate the symbolic post-stable states of an
ITree; for example, R = {run E } satisfies the provisos and so run E is divergence-free. We
                                           s
have proved that P ∈ div-free ⇔ (s • P → − div ), which gives the operational meaning.
   With our transition relation, we can define Roscoe’s step relation, which links the opera-
tional and denotational semantics of CSP [63, Section 9.5]. The utility of this definition and
the following theorems is to permit symbolic verification of CSP processes by calculating
their set-based characterisation.
  Definition 5.10 (Roscoe’s Step Relation).
      s                                                 t                                               s
    ⇒ P ′ ) ≜ ((∃ t ∈ Σ list • s = t @ [✓x ] ∧ P →
 (P =                                            − ✓x ∧ P ′ = stop) ∨ (set (s) ⊆ Σ ∧ P →
                                                                                       − P ′ ))
                                                                                                    s
  Here, set (s) extracts the set of elements from a list. The step relation is similar to →
                                                                                          − , except
that the event type is adjoined with a special termination event ✓. We define the enlarged
set Σ ✓ ≜ Σ ∪ {✓x | x ∈ S}, which adds a family of events parametrised by return values, as in
the semantics of Occam [61], which derives from CSP. A termination is signalled when the
transition relation reaches a Ret x in the ITree, where the trace is augmented with ✓x and
the successor state is set to stop. We often use a condition of the form set (s) ⊆ Σ to mean
that no ✓x event is in s. We can now define the sets of traces, failures, and divergences [63]:
  Definition 5.11 (Traces, Failures, and Divergences).
                                                            s
          traces (P) ≜ {s | set (s) ⊆ Σ ✓ ∧ (∃ P ′ • P =
                                                       ⇒ P ′ )}

               ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
28                                                         Simon Foster, Chung-Kil Hur, and Jim Woodcock


              P ref E ≜ ((∃ F • P = Vis F ∧ E ∩ dom(F ) = ∅) ∨ (∃ x • P = Ret x ∧ ✓x ∉ E))
                                                            s
                        n                                                   o
          failures (P) ≜ (s, X ) | set (s) ⊆ Σ ✓ ∧ (∃ Q • P =
                                                            ⇒ Q ∧ Q ref X )
                                                                           s
     divergences (P) ≜ {s @ t | set (s) ⊆ Σ ∧ set (t) ⊆ Σ ∧ (∃ Q • P =
                                                                     ⇒ Q ∧ Q ⇑ )}

The set traces (P) is the set of all possible event sequences that P can perform. For failures (P),
we need to determine the set of events that an ITree is refusing, P ref E. If P is a visible
event, Vis F , then any set of events E outside of dom(F ) is refused. If P is a return event,
Ret x, then every event other than ✓x is refused. With this, we can implement Roscoe’s form
for the failures. Finally, the divergences is simply a trace s leading to a divergent state Q ⇑ ,
followed by any trace t. We exemplify these definitions with two calculations of failures:
                            {( [], E) | ∀ x ∈ A • c.x ∉ E } ∪ {( [c.x], E) | x ∈ A ∧ ✓ ∉ E }
     failures (inp c A) =
                            ∪ {( [c.x, ✓( ) ], E) | x ∈ A}

                            {(s, X ) | set (s) ⊆ Σ ∧ (s, X ∪ {✓x | x ∈ S}) ∈ failures (P)}
     failures (P >>= Q) =
                            ∪ {(s @ t, X ) | ∃ v • s @ [✓v ] ∈ traces (P) ∧ (t, X ) ∈ failures (Q(v))}
The failures of inp c A consist of (1) the empty trace, where no valid input on c is refused;
(2) the trace where an input event c.x occurred, and ✓() is not being refused; and (3) the
trace where both c.x and ✓( ) occurred, and every event is refused. The failures of P >>= Q
consist of (1) the failures of P that do not reach a return, and (2) the terminating traces
of P, ending in ✓v appended with a failure of Q(v), the continuation. With the help of
Isabelle’s simplifier, these equations can be used to calculate the failures and divergences
automatically, which can be easier to reason with than directly applying coinduction.
   We conclude this section with some important properties of our semantic model:
     Theorem 5.12 (Semantic Model Properties).
       (s, X ) ∈ failures(P) ∧ (Y ∩ {x | s @ [x] ∈ traces(P)} = ∅) → (s, X ∪ Y ) ∈ failures(P)
       s ∈ divergences(P) ∧ set (t) ⊆ Σ → s @ t ∈ divergences(P)
       P ≈ Q → (failures(P) = failures(Q) ∧ divergences(P) = divergences(Q))
       P ∈ div-free ⇔ divergences(P) = ∅
       P ∈ div-free → (∀ s a • s @ [a] ∈ traces(P) → (s, {a}) ∉ failures(P))
  The first two are standard healthiness conditions of the failures-divergences model [63],
called F3 and D1, respectively. F3 states that if (s, X ) is a failure of P then any event
that cannot subsequently occur after s, according to the traces, must also be refused. D1
states that the set of divergences is extension closed. We have also proved that two weakly
bisimilar processes have the same divergences and failures. The following result links the
coinductive definition of divergence freedom and the set of divergences. The final result
demonstrates that ITrees satisfy Roscoe’s definition of determinism for CSP [63]. If an ITree
P is divergence-free, there is no trace after which an event can be accepted and refused.
  Finally, we have stronger results relating weak bisimulation with the trace and divergence
semantics.
     Theorem 5.13. P ≈ Q ⇔ (traces(P) = traces(Q) ∧ divergences(P) = divergences(Q))
We can prove a weak bisimulation between P and Q by showing that these processes have
the same traces and divergences. We do not need to consider the refusals because this level
has no nondeterminism. Alternatively, we could consider nondeterminism similarly to that

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL         29




                                    Fig. 2. Animating the CSP buffer

shown in §4.3 by introducing a distinguished event that the semantic model abstracts. In
this case, the refusal information is vital, and this particular result would no longer hold.

6   ANIMATION BY CODE GENERATION
This section shows how ITrees can be animated by code generation and develops a command
called animate. This command can be used to execute and probe the behaviour of an
ITree-based model. In contrast to the execute command of §4, it is interactive and requires
the user to select a visible event to proceed.
   The Isabelle code generator [39, 40] can be used to extract code from (co)datatypes,
functions, and other constructs to functional languages like SML, Haskell, and Scala. Although
ITrees can be infinite, this is not a problem for languages with lazy evaluation so that we
can step through the ITree’s behaviour. Code generation then allows us to support the
generation of verified animators and provides a potential route to correct implementations.
   The main challenge is to find a suitable computable representation of partial functions.
Whilst A → ↦ B is partly computable, we can only apply it to a value and see whether it yields
an output. For animations and implementations, however, we typically want to determine
a menu of enabled events for the user to select. Moreover, calculating semantics for CSP
operators like 2 and ∥ requires us to compute with partial functions. For this, we need a
way of calculating values for functions dom, ◁, and ⊕, which is impossible for arbitrary
partial functions. Instead, we need a concrete implementation and a data refinement [39].
We choose associative lists as an implementation, A →    ↦ B ≈ (A × B) list, which limits us to
finite constructions. However, it has the benefit of being easily printed, making the animator
easier to implement. ITrees then have the following representation in Haskell:

data Pfun a b = Pfun_alist [(a, b)];
data Itree a b = Ret b | Sil( Itree a b) | Vis(Pfun a ( Itree a b))

Each of the semantic definitions detailed in sections 4 and 5, including corecursive functions,
automatically map to Haskell functions operating over this structure. For constructs like inp
(Definition 5.2), there is more work to support code generation since these can potentially

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
30                                                         Simon Foster, Chung-Kil Hur, and Jim Woodcock


produce an infinite number of events which an associative list cannot capture. Consider,
                                    Δ
for example, inp c {0..}, for c : N →
                                    − E, which can produce any event c.i for i ≥ 0. We can
code generate this by limiting the value set to be finite, for example, {0..3}. Then, the code
generator maps this to a list [0, 1, 2, 3], which is computable.
   The code for the animator steps through 𝜏s until it reaches either a ✓x , in which case
we terminate, or a Vis, in which case the user can choose an option. Since divergence is a
possibility, we limit the number of 𝜏s that will be skipped. The user can continue or abort
the animation after n = 20 𝜏 steps. If an empty event choice is encountered, the animation
terminates due to deadlock. Otherwise, it displays a menu of events, allows the user to
choose one, and recurses following the given continuation.
   We only need to augment the generated code for a particular ITree with the animator
code to generate an animator. We develop a command animate ( ), which inputs a defined
ITree and performs an animation. The command (1) runs the code generator, (2) adds the
animator code, (3) compiles the code using the Glasgow Haskell Compiler (GHC), and (4)
finally runs the binary on a console. This required us to modify Isabelle to add functionality
in the PIDE editor interface to start the animation. Technically, this is provided by a new
“active area”6 , which is a clickable part of the Output tab in the interface. When the user
places their cursor over the animate command in the editor, a “Start animation” link is
shown, which the user can click to start the animation using the jEdit command-line console.
   Fig. 2 shows an animation of the CSP buffer in §5, with the possible inputs limited to
{0..3}. We provide an empty list as a parameter for the initial state. The animator tells us
the events enabled and allows us to pick one by typing a number into the console. Since
lenses and expressions can also be code generated, we can also animate the Circus version of
the buffer with very similar output.
   As a more sophisticated example, we have implemented a distributed ring buffer adapted
from the original Circus paper [73]. The idea is to represent a buffer as a ring of one-place
cells and a controller that manages reading and writing to the ring.
   It has the following form:
     (Controller |[ {rd.c, wrt.c | c ∈ N} ]| ( ||| i ∈ {0..maxbuf } • Cell (i))) \ {rd.c, wrt.c | c ∈ N}
where rd.c and wrt.c are internal channels for the controller to communicate with the ring,
hidden in the overall process network. The individual cells do not communicate with each
other, hence the use of interleaving |||, but the controller communicates with all cells. Channel
rd.c is used to read the current value of cell c, and wrt.c is used to write a value. Each cell
is a single place buffer with a state variable val and has the following form:
     Definition 6.1 (Ring Buffer Cell).
               Cell (i) ≜ wrt?v → val := v # loop (wrt?v → val := v 2 rd!val → Skip)
Initially, the cell is empty, awaiting a write command over channel wrt. Following this, the
cell can either overwrite its current value or advertise its current value over channel rd.
The cells are arranged through indexed interleaving, and the buffer size is maxbuf + 1. The
channels input and output communicate with the overall buffer.
  The controller has four state variables: (1) sz :: N, the current buffer size; (2) rtop :: N ∫a
pointer to the next available cell; (3) rbot :: N the index of the first value stored; (4) cache ::
the cached first element of the buffer. The controller is described using the following actions:
6 Please see src/Pure/PIDE/active.ML in the Isabelle source code for more information.



ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL          31


    Definition 6.2 (Ring Buffer Controller).


                    < maxbuf & input?x →
                   sz                                                                       
     InputCtrl ≜      sz = 0 & sz := 1 # cache := x
                      2 sz > 0 & wrt.rtop!x → sz := sz + 1 # rtop := (rtop + 1) mod maxring


                   sz > 0 & output!cache →
                                        sz := sz − 1 # cache := x #
    OutputCtrl ≜ © sz > 1 & rd.rbot?x →
                                        rbot := (rbot + 1) mod maxring
                                                                                       ª
                 ­                                                                     ®
                 « 2  sz = 1 & sz := 0                                                 ¬

    Controller ≜ sz := 0 # rtop := 0 # rbot := 0 # loop (InputCtrl 2 OutputCtrl)

InputCtrl represents a controller input. An input can be accepted if the size is less than
maxbuf . If the buffer is empty (sz = 0), the element is placed in the cache. Otherwise, it is
sent to the next available cell at rtop. The index rtop is updated using modulo arithmetic
to characterise the circular nature of the buffer. OutputCtrl represents a controller output.
If the buffer is non-empty, then the buffer can output the cached head. Following this, if
there is more than one element, the controller retrieves the element at rbot, decreases the
buffer size, updates that cache, and finally updates the rbot index. If the buffer only had one
element, there is no buffer head to cache. The overall behaviour of the controller is to start
empty, with both rtop and rbot pointing to index 0, and then to iterate a choice between
InputCtrl and OutputCtrl.
   We tested the animator on the ring buffer, using an Apple M3 Pro with 18GB of memory
as the platform. We set up the example so that we can vary maxbuf to observe the scalability
of the animator. On this platform, we can efficiently animate this example for a relatively
small ring of 100 cells, with a similar output to Figure 2, which is a very satisfying result.
   We were also able to animate with a much larger ring with 850 cells, which requires about
3 seconds to compute the next step. With 5000 cells, the animator takes around 50 seconds
to calculate the next transition. The highest number of cells we could reasonably animate is
around 2000. However, we have not attempted to optimise the code, and several data types
could be replaced with efficient implementations to improve scalability. Thus, this approach
to animation and potential implementation is very promising.

7     SYSTEM MODELLING WITH Z-MACHINES
In this section, we apply our ITree and Circus library to create a formal modelling language
and tool called “Z-Machines”, which is in the style of the Z specification language [65, 74],
and B method [1]. Z-Machines are a form of abstract machine, similar to B machines [1], that
use our Z toolkit as the underlying expression language. The implementation of Z-Machines
acts as a case study for our ITrees library by demonstrating its applicability in creating
accessible verification tools. We implement several Isabelle commands for creating Z-Machine
artefacts and a technique for verifying invariants. We illustrate these commands using a
variant of the buffer example (Example 2.1), which is bounded to a specific size and can be
considered as a specification for the ring buffer in §6.
  A Z-Machines consists of a set of operations that act over a state, formally:

             ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
32                                                      Simon Foster, Chung-Kil Hur, and Jim Woodcock


  Definition 7.1 (Z-Machine). A Z-Machine consists of (1) a state space type S; (2) a
set of state invariants Pi : S ⇒ B; (3) a set of operations Opj : Tj ⇒ ((), S)htree, each
parametrised by Tj ; and (4) an initialisation I : S.
Operations are used to update the value of state variables deterministically and can optionally
take inputs and produce outputs. Each operation in a Z-Machine is given a semantics as a
parametric homogeneous Kleisli tree. The parameters are used to encode inputs and outputs
for the operation. The operations are composed in an action system [5] to produce the
overall Z-Machine ITree, which can be verified and animated.
  We consider each command to create the Z-Machine components and their formal semantics.
Each command is interpreted as a set of updates on the Isabelle document model, which
creates definitions and other formal artefacts.
  We use the zstore command (§4.1), to create the bounded buffer state space:
     Example 7.2 (Bounded Buffer Store).

     consts MAX_SIZE :: "nat" and VAL :: "int set"

     zstore Buffer =
       sz :: "nat"
       buf :: "int list"
     where
       "sz = length buf"
       "sz ≤ MAX_SIZE "

This creates two variables: sz and buf , and links them using an invariant. Variable sz
represents the size of the buffer, and buf is its contents. Using the consts command, we
also declare two abstract constants. MAX SIZE characterises the maximum size of the
buffer. VAL is a finite set of integers representing the possible values we can insert into the
buffer. These abstract constants can be assigned concrete definitions later for animation and
verification. The store also has two invariants, requiring (1) that the buffer size is the same
as the length and (2) that the size is no greater than the maximum size.
   Operations are defined using the zoperation command, which has the following syntax:
     Definition 7.3 (Operation Syntax).
              param ::= name ∈ term
           operation ::= zoperation name params param ∗ pre term update assignment
An operation consists of a name, a set of parameters, a precondition term, and an update.
A parameter consists of a name and a term, characterising the set of values from which
the parameter is drawn. We use this set to bound the possible inputs to an operation to
allow animation, similar to §6. The precondition acts as a guard for the operation, which
must be satisfied for the operation to be executed. The update is a sequence of simultaneous
assignments to variables in state space.
   As part of generating the Z-Machine semantics, each operation is assigned a unique event
                   Δ
channel, Opjc : Tj →
                   − E, sharing the same name and as part of a generated channel type E.
The semantics of an operation is shown below:
     Definition 7.4 (Operation Semantics).

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL         33

  u                                    }
    zoperation Opj
  w params x1 ∈ A1 · · · xn ∈ An                                              
                                        = Opj ≜ Opc ?®      ®
                                                       j x ∈ A | P (®
                                                                    x ) → 𝜎 (®
                                                                             x)
  w
  v pre P                              ~
     update 𝜎
                                   ® = A1 × · · · × An
  where x® = (x1, · · · , xn ) and A
Here, A × B denotes the Cartesian product of the two sets A and B. An operation accepts
parameters that inhabit the corresponding parameter sets (A)   ® and satisfies the precondition
P in the context of the current state. The operation update is executed when such parameters
are provided, with the parameters as inputs (®  x ). Parameter sets are specified as expressions,
meaning the acceptable parameters can vary from state to state. When the Z-Machine is in a
state that satisfies the precondition P of an operation for a particular valuation of parameters
 x ), the event Opjc .®
(®                    x is enabled. If the current state cannot satisfy the precondition, an
operation’s behaviour is Stop.
   Below, we define three operations for the bounded buffer:
  Example 7.5 (Buffer Operations).

   zoperation Input =
     params v∈VAL
     pre "sz < MAX_SIZE "
     update "[ sz' = sz + 1, buf' = buf @ [v] ]"

   zoperation Output =
     params v∈VAL
     pre "sz > 0" "v = hd buf"
     update "[ sz' = sz - 1, buf' = tl buf ]"

   zoperation Size =
     emit sz
The first operation, Input, adds a value to the buffer. It has one parameter, v, drawn from
VAL, to enumerate the possible events. The precondition requires that the size is strictly less
than the maximum size. The update increases the size and adds the new value to the buffer.
The second operation, Output, likewise has a single parameter, but this time represents an
output. The precondition requires that the buffer is non-empty and that the output value is
at the buffer’s head. The update decreases the size and removes the head from the buffer.
The third operation, Size, allows us to view the current size of the buffer. It uses the keyword
emit, which is shorthand for an operation of a single output parameter equal to the given
expression, in this case sz.
  Once semantics have been assigned for each of the operations, we can give the overall
semantics for the Z-Machine itself:
  Definition 7.6 (Z-Machine Syntax and Semantics).
                     zmachine ::= zmachine name init term operations name ∗
  u                              }
    zmachine M
  v init 𝜎                    ~ = (M ≜ ⟨𝜎⟩ # loop(Op1 2 Op2 2 · · · 2 Opn ))
     operations Op1 · · · Opn

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
34                                                      Simon Foster, Chung-Kil Hur, and Jim Woodcock




                          Fig. 3. Animating the Bounded Buffer Z-Machine


A Z-Machine consists of an initialisation assignment (𝜎) and a set of operations. The Z-
Machine initialises the state using 𝜎 and then enters a loop where the user can choose an
enabled operation for execution. Below is the Z-Machine for the bounded buffer:
     Example 7.7 (Bounded Buffer Z-Machine).

zmachine Bounded_Buffer =
  init "[sz' = 0, buf' = []]"
  operations Input Output Size

This Z-Machine initialises sz and buf , and collects together the operations.
   Z-Machines can be animated using the animate command developed in §6, provided each
operation draws parameters from finite sets or enumerable types. If this is not the case, the
code generator will give an error message, and similarly, if any operation uses an undefined
abstract constant. An example animation is shown in Figure 3. The animator displays the
enabled operations and parameter combinations at each point, and the user can select one.
Since the animator needs to enumerate all possibilities, we supply a finite set VAL and limit
the buffer to size 3.
   Verification of Z-Machines involves identifying invariants that characterise specific critical
properties. We then need to show that the initialisation establishes the invariants and that
each operation preserves them, meaning that the machine satisfies them in any reachable
state. Using the weakest preconditions, we can calculate the proof obligations (POs) necessary
for an operation to maintain invariants. Specifically, we need to show that P → wp Opj P for
each operation. Typically, this involves showing that if the invariant holds for some state,
then once all the updates of an operation are applied, the invariant still holds.
   For example, if we consider operation Input, one PO is to show that if sz = length buf
then also sz + 1 = length (buf @ [v]), after the updates for sz and buf are applied.

ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL         35


This follows, since sz + 1 = length buf + 1 = length (buf @ [v]), a proof that can
be automated by the simplifier.
   We contribute a proof method called zpog full (Z proof obligation generator), which
generates the set of POs required for an operation to satisfy the specification ( ). This
method is implemented by application of the weakest precondition laws using the simplifier
(see §4.5), and by Isabelle’s automated deduction methods. The POs can typically be
discharged with the help of the sledgehammer tool. Below, we verify that the bounded buffer
Z-Machine satisfies the invariants.
    Example 7.8 (Bounded Buffer Invariant Verification).

    lemma Init_correct: "Init establishes Buffer_inv "
      by zpog_full

    lemma Size_correct: "Size(n) preserves Buffer_inv "
      by zpog_full

    lemma Input_correct: " Input (v) preserves Buffer_inv "
      by zpog_full

    lemma Output_correct: " Output (v) preserves Buffer_inv "
      apply zpog_full
      apply ( metis diff_le_self dual_order . trans )
      done
Here, C establishes P is short-hand for the Hoare triple { True } C { P }, and C preserves P is
short-hand for { P } C { P }. The proofs proceed by application of the weakest precondition
laws by zpog full. For the first three proofs, the simplifier can solve the POs automatically.
For the fourth proof obligation, some arithmetic reasoning is required, which we automate
with a call to sledgehammer. This produces a proof using the resolution prover metis and
several laws relating to the order on natural numbers.

8    RELATED WORK
Infinite trees are a ubiquitous model for concurrency [68]. In particular, ITrees can be seen
as a restricted encoding of Milner’s synchronisation trees [51, 52, 72]. In contrast to ITrees,
synchronisation trees allow multiple events from each node, including visible and 𝜏 events.
They have seen several generalisations, most recently by Ferlez et al. [24], who formalise
Generalized Synchronisation Trees based on partial orders, define bisimulation relations [25],
and apply them to hybrid systems. Our work differs because ITrees use explicit computation
and corecursion, but mutual insights will likely be gained.
   ITrees [75], and their mechanisation in Coq, have been applied in various projects as a
way of defining abstract yet executable semantics [46, 49, 50, 64, 79–81]. They have been
used to verify C programs [46] and an HTTP key-value server [49]. Chappe et al. [18]
introduce Choice Trees as a conservative extension of ITrees. The main innovation is to add
nondeterminism support through constructors brS and brD, which replace the Sil constructor.
Whereas Sil is deterministic, these two constructors allow a finite number of internal choices.
Constructor brS represents “stepped” branching, where a 𝜏 transition accompanies the
resolution of an internal choice. In contrast, brD is “delayed” branching, where deadlocked

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
36                                                      Simon Foster, Chung-Kil Hur, and Jim Woodcock


(“stuck” in [18]) branches are eliminated from the choice. The latter choice is similar to the
external choice since deadlocked branches are likewise pruned but more closely resembles
angelic nondeterminism [60].
   The Coq mechanisation of ITrees uses features unavailable in Isabelle, notably type
constructor variables (rank-n polymorphism). Though this is an apparent weakness, the
quest to implement ITrees in the more restrictive type system of Isabelle/HOL has entailed
several unique advantages. In [75], the Vis constructor has two parameters, rather than one,
for the output event e : E A and k : A → itree E R, a total function, for the continuation.
There, E is a type constructor representing the output sent to the environment, which is
parametric over A, the type of answers received back from the environment. In contrast,
our work instead (1) fixes a non-parametric event universe E; (2) uses a partial function of
type E →  ↦ (E, R) itree; and (3) uses prisms [59] to characterise channels.
   Our one-parameter version of Vis is, in some respects, more general than the two-parameter
one since it allows a variety of communication paradigms and a natural encoding of external
choice [15]. In [75], the focus is on a communication scheme where (1) the process sends an
output to the environment in E A, and (2) the environment then answers back with a value
in A. In CSP, such a scheme can be encoded either with a single event (e.g. c!y?x → P (x)),
where the outputs and inputs are present as parameters, or via two separate events for the
input and output communication (e.g. c!y → d?x → P (x)).
   Additionally, Coq ITrees [75] only permit choices to be made by the environment when
the answer is returned, not in the output event itself. CSP’s external choice operator has yet
to be encoded in Coq ITrees, and [18] has only nondeterministic (i.e. internal) choice. Such
an encoding could be achieved via a special event in choose : E I to represent that the ITree
is asking the environment to resolve a choice, with I being the possible inputs. Similarly,
modelling deadlock could use a special event deadlock : E ∅ with an empty return type. The
disadvantage of such an encoding is that a custom notion of equality is required to reproduce
algebraic laws such as P 2 stop = P. We see our natural encoding of external choice as
the central contribution of our work. At the same time, this additional generality comes at
a cost since the interpretation combinator of the original works [75], which harnesses the
output-input pattern to interpret events as monadic actions, requires more effort to encode.
   The use of partial functions in our work means that external choice operators can be
straightforwardly implemented by the composition of the underlying choice functions (e.g.
using P ⊙ Q). This, in turn, means that the algebraic properties of the choice combinator
lift to ITrees directly and allow flexible algebraic semantics. One technical exception to the
generality of our work is the situation where an empty answer is used (A = ∅), which in
the Coq work allows a Vis that performs an output but has no continuations. Isabelle/HOL
has no empty type since all types must exhibit one element and cannot support empty
answers. This behaviour requires a slightly different encoding where the output is sent,
and the process immediately deadlocks, though this requires two Vis operators rather than
one. Aside from this situation, we can usually encode the two-parameter version Vis e k as
                                                  Δ
[] x ∈ dom(matche ) → k (matche (x)) with e : A →− E.
   A further benefit of having a fixed E is that ITrees become simpler semantic objects. For
example, traces can be represented simply as lists of events rather than the bespoke type
used in [75]. These are amenable to first-order automated proof [10], which has allowed us
to develop our library quickly and with minimal effort.
   Previously, we have demonstrated an Isabelle-based theory library and verification tool
for reactive systems [29, 32]. This supports verification and step-wise development of


ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL         37


nondeterministic and infinite-state systems based on the CSP [15, 42] and Circus [73]
process languages. This includes a specification mechanism called reactive contracts and
a calculational proof strategy. Extensions of our theory support reasoning about hybrid
dynamical systems, which makes it ideal for verifying autonomous robots.
   The Z notation has been implemented in a HOL-based theorem prover several times,
notably in ProofPower-Z [4] and HOL-Z [16]. HOL-Z is also implemented in Isabelle/HOL and
includes a parser for Z schemas, formal semantics, and proof support. Our implementation
is less advanced, does not have the Z schema calculus, and uses types rather than sets to
characterise the hierarchy of data structures in Z. This aids proof automation through the
type system but at the expense of fidelity to the Z standard. Nevertheless, our implementation
of Z-Machines provides proof and animation support, provided that a Z model can be encoded
in our restricted subset.
   Several tools are available to analyse CSP processes, including the FDR refinement
checker [36], and the PAT model checker [66]. These tools offer a more automated approach
to analysis than formal proof, though they require the generation of explicitly labelled
transition systems, which is hampered by the state explosion problem. FDR has a simple
tool, ProBE, for exploring process behaviour by stepping through their definitions. PAT
has a more feature-rich CSP simulator that allows users to perform various simulation
tasks: (1) complete finite-state generation based on the execution graph; (2) automatic
random simulation; (3) user interactive simulation with step-by-step execution and trace
display and replay. These tools are valuable complements that co-exist in the verification
ecosystem. Our focus is on symbolic analysis of processes using proof, though our ITree
animator can be applied to search-based analysis, similar to model checking. Moreover, tools
like sledgehammer increase automation, making verification via proof a realistic possibility.
   Recently, the set-based theory of CSP has also been mechanised in the Isabelle-based
HOL-CSP tool [20, 67], which is also based on the failures-divergences model [62, 63]. They
have used their library to verify the deadlock-freedom of the famous “dining philosophers”
example for an arbitrary number of philosophers N ≥ 2. A further application is modelling
and verifying autonomous vehicles, including the continuous dynamics [20]. This work is
complementary to our library since HOL-CSP is not limited to deterministic constructions,
but on the other hand, HOL-CSP process specifications are not executable. We hope to
combine these libraries to realise these mutual benefits.

9   CONCLUSIONS
In this paper, we have demonstrated how Interaction Trees [75] can be used to unify animation
and deductive verification of software models, from high-level system models to lower-level
program models, in Isabelle/HOL. Our approach harnesses the codatatype package [9] to
encode infinite transition systems, and the code generator [39, 40] to provide animation
and execution. Our results indicate that the technique provides both tractable verification,
with the help of Isabelle’s proof automation [10], and efficient execution. Though ITrees
are intrinsically deterministic, we have shown how to model nondeterministic behaviour
using special events. We applied our technique to simple imperative programs, the CSP and
Circus process languages [57], and to an abstract machine notation based on Z [65]. We note,
however, that our library applies to various other process algebraic and modelling languages.
   Our work has many practical applications in producing verified simulations, and we have
several associated lines of ongoing work. In a parallel paper [78], we have used our ITree
library to mechanise semantics for the RoboChart language [53], a formal UML-like language
for modelling robots with denotational semantics based on CSP. However, this semantics

            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
38                                                        Simon Foster, Chung-Kil Hur, and Jim Woodcock


does not yet consider the real-time operators, which will require us to consider discrete
time, which we believe can be supported using a dedicated time event in ITrees, similar
to tock-CSP [62], a timed version of CSP. This will build on our colleagues’ work with
✓-tock [6], a new semantics for tock-CSP.
   Separately, we have also used our Z-Machine formalism to give a simplified semantics to
RoboChart state machines [77], for the purpose of compositional invariant-based verification,
including deadlock checking. We plan to link Isabelle/HOL with the Eclipse-based RoboTool
modelling environment to allow seamless verification and feedback for software engineers.
This link will open up a pathway from graphical models to verified implementations of
autonomous robotic controllers. In concert with this, we will also explore links to our other
theories for hybrid systems [27, 54], to allow verification of controllers in the presence of a
continuously evolving environment.
   The work described in this paper has also been used pedagogically to support two
courses on assured software engineering, one for third-year undergraduates and one for
external industrial participants. Our courses use our implementation of imperative programs
and Hoare logic to teach program verification and Z-Machines to teach Z-based formal
specification. The benefit of this approach is that students need only learn a single tool
(Isabelle) to support the different pedagogical goals. Moreover, Isabelle’s document model
has allowed us to create DSLs that support appropriate abstraction levels to minimise the
technical detail we expose to students. Our students’ feedback has been universally positive,
and we plan to report further on this when we have more data.
   In the future, we plan to link ITrees to our formalisation of reactive contracts [29, 32],
which provides both denotational semantics for Circus and a refinement calculus for reactive
systems, building on our link with failures-divergences. We will also continue to expand our
imperative program verification tool by considering more advanced concepts, like memory
management and associated separation logics. We will also consider generating imperative
code using a suitable mechanised semantics for a language target. Finally, we will provide a
more user-friendly interface for our animator, as found in tools like FDR4’s probe tool [36]
and ProB [48] for Event-B.


REFERENCES
 [1] Jean-Raymond Abrial. The B-Book: Assigning programs to meanings. Cambridge University Press,
     1996.
 [2] K. Aehlig, F. Haftmann, and T. Nipkow. A compiled implementation of normalisation by evaluation.
     Journal of Functional Programming, 22(1):9–30, 2012.
 [3] A. Armstrong, V. Gomes, and G. Struth. Building program construction and verification tools from
     algebraic principles. Formal Aspects of Computing, 28(2), 2015.
 [4] R. Arthan. On formal specification of a proof tool. In Formal Software Development Methods, volume
     551 of LNCS. Springer, 1991.
 [5] R.-J. Back and R. Kurki-Suonio. Decentralization of process nets with centralized control. Distributed
     Computing, 3:73–87, June 1989.
 [6] J. Baxter, P. Ribeiro, and A. Cavalcanti. Sound reasoning in tock-CSP. Acta Informatica, April 2021.
     doi:10.1007/s00236-020-00394-3.
 [7] Y. Bertot and P. Castéran. Coq’Art: the calculus of inductive constructions. Springer, 2004.
 [8] J. C. Blanchette, A. Bouzy, A. Lochbihler, A. Popescu, and D. Traytel. Friends with Benefits: Imple-
     menting Corecursion in Foundational Proof Assistants. In Programming Languages and Systems, 26th
     European Symposium on Programming (ESOP), April 2017.
 [9] J. C. Blanchette, J. Hölzl, A. Lochbihler, L. Panny, A. Popescu, and D. Traytel. Truly modular
     (co)datatypes for Isabelle/HOL. In Gerwin Klein and Ruben Gamboa, editors, 5th Intl. Conf. on
     Interactive Theorem Proving (ITP), volume 8558 of LNCS, pages 93–110. Springer, 2014.


ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL                39


[10] J. C. Blanchette, C. Kaliszyk, L. C. Paulson, and J. Urban. Hammering towards QED. Journal of
     Formalized Reasoning, 9(1), 2016. doi:10.6092/issn.1972-5787/4593.
[11] J. C. Blanchette, A. Popescu, and D. Traytel. Foundational extensible corecursion: a proof assistant
     perspective. In 20th Intl. Conf. on Functional Programming (ICFP), pages 192–204. ACM, August
     2015. doi:10.1145/2858949.2784732.
[12] J. C. Blanchette, A. Popescu, and D. Traytel. Soundness and completeness proofs by coinductive
     methods. Journal of Automated Reasoning, 58:149–179, 2017. doi:10.1007/s10817-016-9391-3.
[13] R. Boulton, A. Gordon, M. Gordon, J. Harrison, J. Herbert, and J. van Tassel. Experience with
     embedding hardware description languages in hol. In Proc. IFIP Intl. Conf. on Theorem Provers in
     Circuit Design, pages 129–156, 1993.
[14] E. Bousse, T. Degueule, D. Vojtisek, T. Mayerhofer, J. Deantoni, and B. Combemale. Execution
     framework of the GEMOC studio (tool demo). In Proceedings of the 2016 ACM SIGPLAN International
     Conference on Software Language Engineering, SLE 2016, pages 84–89. Association for Computing
     Machinery, October 2016. doi:10.1145/2997364.2997384.
[15] S. D. Brookes, C. A. R. Hoare, and A. W. Roscoe. A theory of communicating sequential processes.
     Journal of the ACM, 31(3):560–599, 1984. doi:10.1145/828.833.
[16] A. D. Brucker, F. Rittinger, and B. Wolff. HOL-Z 2.0: A proof environment for Z-specifications. Journal
     of Universal Computer Science, 9(2), February 2003.
[17] A. Cavalcanti and J. Woodcock. A tutorial introduction to designs in unifying theories of programming.
     In Proc. 4th Intl. Conf. on Integrated Formal Methods (IFM), volume 2999 of LNCS, pages 40–66.
     Springer, 2004.
[18] N. Chappe, P. He, L. Henrio, Y. Zakowski, and S. Zdancewic. Choice trees: Representing nondeterministic,
     recursive, and impure programs in Coq. In Proc. ACM Programming Lang. (POPL), volume 61. ACM,
     January 2023.
[19] F. Ciccozzi, I. Malavolta, and B. Selic. Execution of UML models: A systematic review of research and
     practice. Software & Systems Modeling, 18(3):2313–2360, June 2019. doi:10.1007/s10270-018-0675-4.
[20] P. Crisafulli, S. Taha, and B. Wolff. Modeling and analysing cyber-physical systems in HOL-CSP.
     Robotics and Autonomous Systems, 170, 2023.
[21] L. de Moura, S. Kong, J. Avigad, F. van Doorn, and J. von Raumer. The Lean theorem prover (system
     description). In Proc. 25th Intl. Conf. on Automated Deduction (CADE), 2015.
[22] E. W. Dijkstra. Guarded commands, nondeterminacy and formal derivation of programs. Communica-
     tions of the ACM, 18(8):453–457, 1975.
[23] P. H. Feiler and D. P. Gluch. Model-Based Engineering with AADL: An Introduction to the SAE Archi-
     tecture Analysis & Design Language. SEI Series in Software Engineering. Addison-Wesley Professional,
     2012.
[24] J. Ferlez, R. Cleaveland, and S. Marcus. Generalized synchronization trees. In Proc. 17th Intl. Conf.
     on Foundations of Software Science and Computation Structures (FOSSACS), volume 8412 of LNCS,
     pages 304–319. Springer, 2014. doi:10.1007/978-3-642-54830-7_20.
[25] J. Ferlez, R. Cleaveland, and S. I. Marcus. Bisimulation in behavioral dynamical systems and generalized
     synchronization trees. In Proc. 2018 IEEE Conf. on Decision and Control (CDC), pages 751–758.
     IEEE, 2018. doi:10.1109/CDC.2018.8619607.
[26] J. Foster. Bidirectional programming languages. PhD thesis, University of Pennsylvania, 2009.
[27] S. Foster. Hybrid relations in Isabelle/UTP. In 7th Intl. Symp. on Unifying Theories of Programming
     (UTP), volume 11885 of LNCS, pages 130–153. Springer, 2019.
[28] S. Foster, J. Baxter, A. Cavalcanti, J. Woodcock, and F. Zeyda. Unifying semantic foundations for
     automated verification tools in Isabelle/UTP. Science of Computer Programming, 197, October 2020.
     doi:10.1016/j.scico.2020.102510.
[29] S. Foster, A. Cavalcanti, S. Canham, J. Woodcock, and F. Zeyda. Unifying theories of reactive design
     contracts. Theoretical Computer Science, 802:105–140, January 2020. doi:10.1016/j.tcs.2019.09.017.
[30] S. Foster, C.-K. Hur, and J. Woodcock. Formally verified simulations of state-rich processes using
     interaction trees in Isabelle/HOL. In 32nd Intl. Conf. on Concurrency Theory (CONCUR), volume
     203 of LIPIcs. Schloss Dagstuhl – Leibniz-Zentrum für Informatik, 2021.
[31] S. Foster, Y. Nemouchi, M. Gleirscher, R. Wei, and T. Kelly. Integration of formal proof into unified
     assurance cases with Isabelle/SACM. Formal Aspects of Computing, 2021.
[32] S. Foster, K. Ye, A. Cavalcanti, and J. Woodcock. Automated verification of reactive and concurrent
     programs by calculation. Journal of Logical and Algebraic Methods in Programming, 121, June 2021.
     doi:10.1016/j.jlamp.2021.100681.


            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
40                                                          Simon Foster, Chung-Kil Hur, and Jim Woodcock


[33] Simon Foster, Yakoub Nemouchi, Colin O’Halloran, Karen Stephenson, and Nick Tudor. Formal
     model-based assurance cases in Isabelle/SACM: An autonomous underwater vehicle case study. In
     Proceedings of the 8th International Conference on Formal Methods in Software Engineering, pages
     11–21, 2020.
[34] Simon Foster, Jonathan Julián Huerta y Munive, Mario Gleirscher, and Georg Struth. Hybrid systems
     verification with Isabelle/HOL: Simpler syntax, better models, faster proofs. In FM 2021, volume 13047
     of LNCS, pages 367–386, Heidelberg, 2021. Springer. doi:10.1007/978-3-030-90870-6\_20.
[35] J. Gibbons and N. Wu. Folding domain-specific languages: deep and shallow embeddings. In Proc. 19th
     Intl. Conf. on Functional Programming (ICFP), pages 339–347. ACM, 2014.
[36] T. Gibson-Robinson, P. Armstrong, A. Boulgakov, and A. W. Roscoe. FDR3 — A Modern Refinement
     Checker for CSP. In Erika Ábrahám and Klaus Havelund, editors, Tools and Algorithms for the
     Construction and Analysis of Systems, volume 8413 of LNCS, pages 187–201, 2014.
[37] M. Gleirscher, S. Foster, and J. Woodcock. New opportunities for integrated formal methods. ACM
     Comput. Surv., 52(6), 2019.
[38] V. B. F Gomes and G. Struth. Modal Kleene algebra applied to program correctness. In Formal
     Methods, volume 9995 of LNCS, pages 310–325. Springer, 2016.
[39] F. Haftmann, A. Krauss, O. Kuncar, and T. Nipkow. Data refinement in Isabelle/HOL. In Proc. 4th
     Intl. Conf. on Interactive Theorem Proving (ITP), volume 7998 of LNCS, pages 100–115. Springer,
     2013.
[40] F. Haftmann and T. Nipkow. Code generation via higher-order rewrite systems. In 10th Intl. Symp. on
     Functional and Logic Programming (FLOPS), volume 6009 of LNCS, pages 103–117. Springer, 2010.
[41] Matthew Hennessy and Tim Regan. A process algebra for timed systems. Information and Computation,
     117(2):221–239, 1995.
[42] C. A. R. Hoare. Communicating Sequential Processes. Prentice-Hall, 1985.
[43] C. A. R. Hoare, I. Hayes, J. He, C. Morgan, A. Roscoe, J. Sanders, I. Sørensen, J. Spivey, and B. Sufrin.
     The laws of programming. Communications of the ACM, 30(8):672–687, August 1987.
[44] C. A. R. Hoare and J. He. Unifying Theories of Programming. Prentice-Hall, 1998.
[45] G. Klein et al. seL4: Formal verification of an OS kernel. In Proc. 22nd Symp. on Operating Systems
     Principles (SOSP), pages 207–220. ACM, 2009.
[46] Nicolas Koh, Yao Li, Yishuai Li, Li yao Xia, Lennart Beringer, Wolf Honoré, William Mansky, Benjamin C.
     Pierce, and Steve Zdancewic. From C to Interaction Trees: Specifying, Verifying, and Testing a Networked
     Server. In Proc. 8th ACM SIGPLAN International Conference on Certified Programs and Proofs
     (CPP), 2019. doi:10.1145/3293880.3294106.
[47] Dimitrios S. Kolovos, Richard F. Paige, and Fiona A. C. Polack. The Epsilon Transformation Language.
     In Antonio Vallecillo, Jeff Gray, and Alfonso Pierantonio, editors, Theory and Practice of Model
     Transformations, pages 46–60, Berlin, Heidelberg, 2008. Springer. doi:10.1007/978-3-540-69927-9_4.
[48] M. Leuschel and M. Butler. ProB: An automated analysis toolset for the B method. Int J Softw Tools
     Technol Transf, 10:185–203, 2008. doi:10.1007/s10009-007-0063-9.
[49] Yishuai Li, Benjamin C. Pierce, and Steve Zdancewic. Model-based testing of networked applications.
     In Proc. 30th ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA),
     2021.
[50] William Mansky, Wolf Honoré, and Andrew W. Appel. Connecting higher-order separation logic to a
     first-order outside world. In Proc. 29th European Symposium on Programming (ESOP), 2020.
[51] Robin Milner. A Calculus of Communicating Systems, volume 92 of Lecture Notes in Computer Science.
     Springer, 1980.
[52] Robin Milner. Communication and Concurrency. Prentice Hall, 1989.
[53] A. Miyazawa, P. Ribeiro, W. Li, A. Cavalcanti, J. Timmis, and J. Woodcock. RoboChart: Modelling
     and verification of the functional behaviour of robotic applications. Software and Systems Modelling,
     January 2019. doi:10.1007/s10270-018-00710-z.
[54] J. H. Y. Munive, G. Struth, and S. Foster. Differential Hoare logics and refinement calculi for hybrid
     systems with Isabelle/HOL. In RAMiCS, volume 12062 of LNCS. Springer, April 2020. doi:10.1007/978-
     3-030-43520-2_11.
[55] T. Nipkow. Hoare logics in isabelle/hol. In Proof and System-Reliability. Springer, 2002.
[56] T. Nipkow, M. Wenzel, and L. C. Paulson. Isabelle/HOL: a proof assistant for higher-order logic.
     Springer, 2002.
[57] M. Oliveira, A. Cavalcanti, and J. Woodcock. A UTP semantics for Circus. Formal Aspects of Computing,
     21:3–32, 2009. doi:10.1007/s00165-007-0052-5.


ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
Unifying Model Execution and Deductive Verification with Interaction Trees in Isabelle/HOL                41


[58] R. F. Paige. A meta-method for formal method integration. In Proc. 4th. Intl. Symp. on Formal
     Methods Europe (FME), volume 1313 of LNCS, pages 473–494. Springer, 1997.
[59] M. Pickering, J. Gibbons, and N. Wu. Profunctor optics: Modular data accessors. The Art, Science,
     and Engineering of Programming, 1(2), 2017. doi:10.22152/programming-journal.org/2017/1/7.
[60] P. Ribeiro and A. Cavalcanti. Angelic processes for CSP via the UTP. Theoretical Computer Science,
     2019.
[61] A. W. Roscoe. Denotational semantics for textsfoccam. In Intl. Seminar on Concurrency, volume 197
     of LNCS, pages 306–329. Springer, 1984.
[62] A. W. Roscoe. The Theory and Practice of Concurrency. Prentice-Hall, 2005.
[63] A. W. Roscoe. Understanding Concurrent Systems. Springer, 2010.
[64] Lucas Silver and Steve Zdancewic. Dijkstra monads forever: Termination-sensitive specifications for
     Interaction Trees. Proceedings of the ACM on Programming Languages, 5(POPL), January 2021.
     doi:10.1145/3434307.
[65] M. Spivey. The Z Notation — A Reference Manual. Prentice Hall, Englewood Cliffs, N. J., 1989.
[66] Jun Sun, Yang Liu, Jin Song Dong, and Jun Pang. Pat: Towards flexible verification under fairness.
     Proceedings of the 21th International Conference on Computer Aided Verification (CAV’09), 5643:709–
     714, 2009.
[67] S. Taha, B. Wolff, and L. Ye. Philosophers may dine — definitively! In Proc. 16th Intl. Conf. on
     Integrated Formal Methods, LNCS. Springer, 2020. doi:10.1007/978-3-030-63461-2_23.
[68] R. J. van Glabbeek. Notes on the methodology of CCS and CSP. Theoretical Computer Science, 1997.
[69] Ran Wei, Simon Foster, Haitao Mei, Fang Yan, Ruizhe Yang, Ibrahim Habli, Colin O’Halloran, Nick
     Tudor, Tim Kelly, and Yakoub Nemouchi. Access: Assurance case centric engineering of safety–critical
     systems. Journal of Systems and Software, 213, 2024. URL: https://www.sciencedirect.com/science/
     article/pii/S0164121224000773, doi:10.1016/j.jss.2024.112034.
[70] M. Wenzel. Interaction with formal mathematical documents in Isabelle/PIDE. In CICM, LNCS 11617,
     pages 1–15. Springer, 2019.
[71] M. Wenzel and B. Wolff. Building formal method tools in the Isabelle/Isar framework. In TPHOLs,
     volume 4732 of LNCS. Springer, 2007.
[72] G. Winsel. Synchronisation trees. Theoretical Computer Science, 34(1-2):33–82, 1984.
[73] J. Woodcock and A. Cavalcanti. A concurrent language for refinement. In A. Butterfield, G. Strong,
     and C. Pahl, editors, Proc. 5th Irish Workshop on Formal Methods (IWFM), Workshops in Computing.
     BCS, July 2001.
[74] J. Woodcock and J. Davies. Using Z: Specification, Refinement, and Proof. Prentice-Hall, 1996.
[75] L.-Y. Xia, Y. Zakowski, P. He, C.-K. Hur, G. Malecha, B. C. Pierce, and S. Zdancewic. Interaction
     trees: Representing recursive and impure programs in Coq. In Proc. 47th ACM SIGPLAN Symposium
     on Principles of Programming Languages (POPL). ACM, 2020. doi:10.1145/3371119.
[76] Li-yao Xia. Executable Denotational Semantics with Interaction Trees. Ph.D., University of Pennsylvania,
     United States – Pennsylvania, 2022. ISBN: 9798351434490.
[77] F. Yan, S. Foster, and I. Habli. Automated compositional verification for robotic state machines using
     Isabelle/HOL. In Proc. 27th Intl. Conf. on Engineering of Complex Computer Systems (ICECCS).
     IEEE, June 2023. doi:10.1109/ICECCS59891.2023.00029.
[78] K. Ye, S. Foster, and J. Woodcock. Formally verified animation for RoboChart using interaction trees.
     Journal of Logical and Algebraic Methods in Programming, 137, February 2024.
[79] Yannick Zakowski, Paul He, Chung-Kil Hur, and Steve Zdancewic. An equational theory for weak
     bisimulation via generalized parameterized coinduction. In Proc. 9th ACM SIGPLAN International
     Conference on Certified Programs and Proofs (CPP), 2020. doi:10.1145/3372885.3373813.
[80] Vadim Zaliva, Ilia Zaichuk, and Franz Franchetti. Verified translation between purely functional and
     imperative domain specific languages in HELIX. In Proc. 12th International Conference on Verified
     Software: Theories, Tools, Experiments (VSTTE), 2020.
[81] Hengchu Zhang, Wolf Honoré, Nicolas Koh, Yao Li, Yishuai Li, Li-Yao Xia, Lennart Beringer, William
     Mansky, Benjamin C. Pierce, and Steve Zdancewic. Verifying an HTTP key-value server with Interaction
     Trees and VST. In Proc. 12th International Conference on Interactive Theorem Proving (ITP), 2021.
     doi:10.4230/LIPIcs.ITP.2021.32.




            ACM Trans. Softw. Eng. Methodol., Vol. 1, No. 1, Article . Publication date: October 2024.
