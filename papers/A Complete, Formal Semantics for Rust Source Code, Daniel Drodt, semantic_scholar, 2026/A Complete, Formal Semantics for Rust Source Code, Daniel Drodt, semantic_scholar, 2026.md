                                        A Complete, Formal Semantics for Rust Source Code
                                        DANIEL DRODT, Technical University of Darmstadt, Germany
                                        Formally reasoning about Rust programs requires a rigorous formal semantics, especially in the context of
                                        deductive verification and concurrent programming. We present a modular, flexible semantics for a significant
                                        subset of (close to) source code level Rust, based on the recent locally abstract, globally concrete semantics
                                        framework, separating local evaluation of expressions from their composition into concrete traces. The
                                        semantics is extended to model Rust’s asynchronous programming features and Rust’s most popular async
                                        runtime, Tokio. Based on our more abstract formalization, we establish the fairness of Tokio’s scheduler.
arXiv:2610.06003v1 [cs.PL] 5 Oct 2026




                                        Further, we show the applicability of our semantics to deductive verification of Rust by providing soundness
                                        proofs for a Rust program logic.
                                        CCS Concepts: • Theory of computation → Program semantics; Programming logic; • Computing
                                        methodologies → Concurrent programming languages.
                                        Additional Key Words and Phrases: Rust, denotational semantics, trace semantics, dynamic logic, concurrency,
                                        fairness
                                        ACM Reference Format:
                                        Daniel Drodt. 2026. A Complete, Formal Semantics for Rust Source Code. ACM Trans. Program. Lang. Syst.
                                        XXX, YYY, Article ZZZ (September 2026), 67 pages. https://doi.org/XXXXXXX.XXXXXXX

                                        1    Introduction
                                        Rust is a modern, flexible, systems-level programming language of growing importance. It is used
                                        in many crucial application domains, most notably the Linux kernel [44]. This importance and
                                        usage increases the need for formal analysis and formal verification of Rust programs, both of
                                        which are well supported by Rust’s language design. Accordingly, several verification tools for Rust
                                        are being developed [3, 6, 12, 21, 30, 43]. With its complex ownership model and reference system,
                                        Rust provides a powerful yet unusually restrictive type system that ensures memory safety and the
                                        absence of data races [42].
                                           The lack of an official, formal, source code level Rust semantics makes validation of these tools
                                        problematic. Without such a semantics, interoperability of verification tools is difficult, as tools
                                        may not be based on the same, or even compatible, formalisms. Similarly, verification of the Rust
                                        compiler needs a formal semantics for each of Rust’s intermediate representations.
                                           The semantics problem is partially addressed by formal models of parts of Rust’s type system
                                        or intermediate representations, typically the mid-level intermediate representation (MIR) [13, 28,
                                        36, 39]. These semantics provide usable and rigorous formalizations of Rust’s borrow checker and
                                        operational semantics of subsets of the language, each offering different trade-offs and specializa-
                                        tions. Nevertheless, they are limited in at least two respects. First, being low-level and focused on
                                        the MIR, they offer little for reasoning about Rust programs at a level closer to the source code. A
                                        high-level representation crucially allows, e.g., comprehension of the complex proof state [21].
                                        Author’s Contact Information: Daniel Drodt, daniel.drodt@tu-darmstadt.de, Technical University of Darmstadt, Darmstadt,
                                        Hessen, Germany.

                                        Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                        provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the
                                        full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored.
                                        Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
                                        prior specific permission and/or a fee. Request permissions from permissions@acm.org.
                                        © 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                        ACM 1558-4593/2026/9-ARTZZZ
                                        https://doi.org/XXXXXXX.XXXXXXX


                                                            ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:2                                                                                                Daniel Drodt


   Second, no formal semantics for Rust’s concurrent features (“async Rust”) has been developed.
As “fearless concurrency” is a major feature and promise of Rust [42], this is an unfortunate
limitation. Without formal semantics, it remains difficult to reason about concurrent and parallel
Rust programs or to prove them correct, free of deadlocks, and similar properties. Furthermore, it
remains elusive to model concrete schedulers or runtimes, which is especially relevant as Rust allows
different asynchronous runtimes to be used. Here too, a high-level view seems more promising
than semantics of lower-level representations.
   As Rust has matured and its type system, borrow checking, and memory model have been
examined, refined, and formalized, we argue that a sensible next step is to examine the high-level
features, building on these closely-studied foundations.
   Hence, we see a crucial gap left open: a formal semantics of Rust suitable for formalizing high-
level properties of Rust programs. Ideally, such a semantics should (1) be highly flexible and
compositional to accommodate future language extensions; (2) formalize Rust at the source code
level (or close to it); (3) allow the formalization of asynchronous Rust code; (4) permit modeling of
and reasoning about asynchronous runtimes; and (5) ease deductive verification of Rust programs.
   To meet these goals, modularity of the semantics is paramount: Extendability is only feasible
if adding a new language feature does not require to significantly rewrite the existing semantics
rules. Additionally, a modular semantics eases verification effort, as calculus proof rules are also
made modular in the sense that it is possible to extend the calculus with new rules and constructs
without revising the rest of the calculus.
   However, semantics in the style of structural operational semantics (SOS) struggle with modularity.
As Peter Mosses put it, “conventional SOS descriptions of programming languages have quite poor
modularity,” which leads to complex semantics, as “[w]hen extending a pure functional language
with concurrency primitives and/or references, for instance, the SOS rules for all the functional
constructs had to be completely reformulated” [50]. While Mosses [50] provides a modification of
SOS that improves modularity, recent developments in trace-based semantics offer an even more
flexible, complete, and modular path [7, 8, 32, 41].
   The present paper remedies this situation by providing a comprehensive, formal semantics for
most parts of safe Rust’s high-level intermediate representation (HIR) based on the locally abstract,
globally concrete (LAGC) semantics framework [17], which was developed with concurrent and
parallel programs and deductive verification in mind. LAGC achieves a modular and flexible
semantics by separating the local evaluations of expressions from the global state and concerns
such as scheduling. This approach is modular in the sense that each syntactic structure—expressions
or statements—have one local rule that is independent of the global context. Adding new language
features consists largely of formulating new local rules. Furthermore, the approach is well-suited for
concurrency by delegating all scheduling concerns to the global layer and building hybrid traces over
states and events for each program execution. These traces contain all relevant information of state
changes and scheduling relevant events. Combining these elements, LAGC defines the semantics
of a specific program as the set of all well-formed traces generated by the global composition rules.
   LAGC has been successfully applied to a number of programming languages and settings, such
as ProMeLa and active object languages [10] like ABS [17, 18], demonstrating its flexibility. Further
examples include Real-Time ABS [62] and Timed Rebeca [25]. The LAGC approach has also been
used, in a slightly different form, in the context of deductive verification [8]. These examples
demonstrate that LAGC, with its modular approach, separation of local and global context, and
hybrid traces, is more suitable than the traditional SOS semantics for purposes of verification and
the modeling of concurrent programming languages.



ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                            ZZZ:3


  For these reasons, LAGC is a viable semantics framework to achieve the goals outlined above
and it allows a semantics of higher-level Rust. Hence, the presented semantics is based on LAGC.
Our detailed contributions are:
    (1) We provide a semantics for most parts of safe Rust’s HIR in the LAGC framework and demon-
        strate the semantics’ usability with a number of examples. To demonstrate the applicability
        of the semantics, we support complex language features and control flows, such as loops
        with breaks and continues.
    (2) We extend this semantics to async Rust, modeling any possible scheduling of async functions.
        Notably, to our knowledge, this is the first formal semantics of async Rust in the literature.
    (3) Based on the asynchronous semantics, we formalize Rust’s most widely-used runtime, the
        “current thread runtime” of Tokio [64], and prove its fairness. We stress that our approach is
        straightforwardly adaptable to other runtimes, with the async Rust semantics carrying over.
    (4) Finally, we show how our semantics can be used to prove soundness of the calculus for
        RustyDL, a program logic for Rust [21] based on dynamic logic (DL) [53], demonstrating how
        the modular rules of LAGC ease such proofs. Thereby, we also highlight the interaction of
        DL and LAGC.
   Section 2 introduces the necessary background and definitions on which our semantics is built,
as well as the general LAGC approach. We present the semantics for synchronous Rust in Section 3
and extend it to async Rust in Section 4. Section 5 then builds upon the async semantics to represent
one of Tokio’s runtimes in LAGC and proves its fairness guarantees. The calculus of the program
logic RustyDL [21] is proven sound in Section 6. We present related work in Section 7 and conclude
the paper in Section 8.

2     Prerequisites
The goal of the LAGC approach [17] is to represent a program run as a trace consisting of states
and events and to represent a program’s entire behavior as the set of all possible traces starting
from a concrete state. As a principle idea to tackle the complexity of all possible executions, LAGC
consists of many local rules for each syntactic structure, which consider abstract states and traces,
and global rules, which consider concrete states and traces and are concerned with the correct
composition of such traces. Events in traces aid this effort by providing more structural information,
e.g., that a function was invoked or a panic occurred.
   Building an LAGC semantics consists of four steps: (1) the local evaluation, mapping expressions
to (abstract) continuation traces, without knowledge of the surrounding context; (2) a well-formed-
ness predicate, restricting the set of allowed traces and enforcing, e.g., proper ordering of events;
(3) trace composition rules, defining how the local traces are stitched together to concrete traces;
and (4) global program semantics, defining the initial state and allowed end states. This framework
yields a set of concrete traces describing all possible executions for a given program from an
initial state and achieves a modular semantics: Each kind of expression has exactly one local rule
irrespective of context.
   This section gives the necessary background for states, events, and traces, mainly following the
definitions in [17], modified to adapt to Rust’s more functional, expression-based structure. This
modification in fact simplifies some parts of the LAGC approach.

2.1    Values and States
Due to the high-level concerns of our semantics, we do not map Rust constructs to low-level or even
machine-level domains; rather, we map to mathematical domains: Rust’s concrete, machine word
integer types, such as i32 and u8, are mapped to mathematical integers Z, while bool is mapped to

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:4                                                                                                    Daniel Drodt


boolean values tt and ff. We proceed similarly with compound types like arrays and structs. This
abstraction is not a limitation of the semantics. We ensure the correct behavior of Rust types as
part of the evaluation of the relevant expressions.
  Definition 2.1 ((Starred) Semantic Values). We write Var for the set of program variables with
typical elements x, y, z, etc. Further, we define a place 𝑝 ∈ Place as an abstract representation of
memory locations. Such a place is either a program variable x, an array field 𝑝 [𝑛] of another place 𝑝
where 𝑛 is a natural number, or a field access 𝑝.identifier.
                                         x ∈ Var ::= identifier
                                       𝑝 ∈ Place ::= x | 𝑝 [𝑛] | 𝑝.identifier
                                           𝑛 ∈ N ::= 0 | 1 | . . .
   The set of semantic values Val, with typical elements 𝑣, 𝑣 1, 𝑣 2, . . ., includes boolean, integer,
reference, function, tuple, array, struct, and enum variant values. The latter compound types are
defined as their Rust counterparts, where all fields are values. Reference values are either shared
(denoted by 𝑠) or mutable (denoted by 𝑚) and contain a place 𝑝 ∈ Place and a borrow identifier
𝑏 ∈ BId; e.g., Ref 𝑚
                   x[1] (𝑏 0 ) is a mutable reference of place x[1] with borrow identifier 𝑏 0 . Function
values are represented as function names.
            𝑣 ∈ Val ::= tt | ff | 𝑧 | Ref 𝑠𝑝 (𝑏) | Ref 𝑚
                                                       𝑝 (𝑏) | (𝑣) | [𝑣] | structs | enums | functions
              𝑧 ∈ Z ::= 𝑛 | −1 | −2 | . . .
  The set of starred values SVal ⊃ Val, with typical element sv, extends values with the starred
value ∗, representing unknown, symbolic values.
                                                 sv ∈ SVal ::= 𝑣 | ∗
   Example 2.2. The semantic value to which the Rust expression (true, 4 ∗ 2, &mut n), where n is
a program variable of type i32, evaluates is (tt, 8, Ref 𝑚
                                                         n (𝑏 0 )), where 𝑏 0 ∈ BId is unique.

   To associate variables with values, we use a symbolic state 𝜎, modelled as a partial mapping
𝜎 : Var ⇀ SVal from variables to starred values. We express a modification of a variable x with the
(starred) value sv as the state update of 𝜎:
                                                    (
                                                      sv   x=y
                                  𝜎 [x ↦→ sv] (y) =
                                                     𝜎 (y) x ≠ y .
  As values can be nested in arrays, tuples, structs, and enums, we define syntactic sugar for
updating not just variables but places 𝑝 ∈ Place. The base case of 𝑝 = x for some variable x is
handled by state updates. Updates to an array place 𝑝 [𝑛] is resolved by updating place 𝑝 with a
changed array value.
𝜎 [𝑝 [𝑛] ↦→ sv] = 𝜎 [𝑝 ↦→ [sv 0, . . . , sv𝑛−1, sv, sv𝑛+1, . . . , sv𝑚 ]]   where 𝑛 ≤ 𝑚 ∧𝜎 (𝑝) = [sv 0, . . . , sv𝑚 ]
The case for updating field places 𝑝.identifier is analogous: 𝜎 [𝑝.identifier ↦→ sv].
  The symbolic variables of state 𝜎 are defined as symb(𝜎) = {X ∈ Var | 𝜎 (X) = ∗} and are used to
abstract from concrete evaluations, e.g., for function parameters. We typically denote them with
capital letters. If symb(𝜎) = ∅, we call 𝜎 concrete.
  As our semantics may introduce new variables, we require a notion of state extension.
    Definition 2.3 (State Extension). Let 𝜎1, 𝜎2 be two states. We say 𝜎2 extends 𝜎1 —written as 𝜎1 ⊆ 𝜎2 —
iff dom(𝜎1 ) ⊆ dom(𝜎2 ) and ∀x ∈ dom(𝜎1 ). 𝜎1 (x) = 𝜎2 (x).

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                             ZZZ:5


2.2   Traces and Events
Traces are sequences of states and events, the latter of which give a structure and additional
information to traces. Events cannot change the state; we add the relevant events for Rust as we go
along. Like states, traces can be symbolic.
  Definition 2.4 (Symbolic Trace). We define symbolic traces inductively by the following rules,
where 𝜀 is the empty trace:

                             𝜏 ::= 𝜀 | 𝜏 ↷ 𝑡      (trace)
                              𝑡 ::= 𝜎 | ev(ep)    (trace element)
                            ep ::= x | 𝑣          (event parameter)
where ev(ep) is an event marker and ep are the event parameters, i.e., variables or values.
   Example 2.5. Let 𝜎0 := [X ↦→ ∗, y ↦→ ff] be a symbolic state and ev 0 an event marker with one
parameter. Then, 𝜏0 := 𝜀 ↷ 𝜎0 ↷ ev 0 (X) ↷ 𝜎0 [y ↦→ tt] is a symbolic trace, representing an
execution starting in (symbolic) state 𝜎0 , then event ev 0 (X), and ending in the updated state where
y’s value is changed to false.
   We take care that each event in a trace is surrounded on either side by a state. This ensures that
that functions over traces like last(𝜏) and lastEv(𝜏), which evaluate to the last state and event of
trace 𝜏, respectively, are always defined for non-empty traces.
   Often, it is necessary to construct a trace 𝜏 from two given traces 𝜏1, 𝜏2 . We call this process trace
composition. We write ⟨𝜎⟩ for the singleton trace 𝜀 ↷ 𝜎 and 𝜏1 · 𝜏2 for the concatenation of two
symbolic traces 𝜏1, 𝜏2 . For example, we write the trace from Example 2.5 as
                                      𝜏0 = ⟨𝜎0 ⟩ ↷ ev 0 (X) ↷ 𝜎0 [y ↦→ tt] .
  Traces 𝜏1 and 𝜏2 , where 𝜏1 ends in the state with which 𝜏2 begins, can be “stitched together” with
the semantic chop operation1 :
                            𝜏1 ∗∗ 𝜏2 = 𝜏 · 𝜏2 where 𝜏1 = 𝜏 ↷ 𝜎 and 𝜏2 = ⟨𝜎⟩ · 𝜏 ′ .
Note that the chop is a partial operation: If 𝜏1 is empty or if the last state of 𝜏1 and first state of 𝜏2
are incompatible, the chop is undefined.
  We also require a way to concretize symbolic traces into concrete traces. To this end, we work
with concretization mappings 𝜌.
 Definition 2.6 (Concretization Mapping). A concretization mapping 𝜌 : Var ⇀ Val is a partial
mapping for state 𝜎 if dom(𝜌) ∩ dom(𝜎) = symb(𝜎). We denote the concretization of 𝜎 with 𝜌 as
                             𝜌 • 𝜎 = 𝜌 ∪ {x ↦→ 𝜎 (x) | x ∈ dom(𝜎) \ dom(𝜌)} .
   Proposition 2.7. Let 𝜎 be a state and 𝜌 a 𝜎 concretization mapping. Then 𝜌 • 𝜎 is a concrete state.
   Definition 2.8 (Trace Concretization). We extend the notion of concretization mapping to traces
in the natural way: A partial mapping 𝜌 is a concretization mapping for 𝜏 if it is a concretization
mapping for all states in 𝜏. The concretization 𝜌 (𝜏) of 𝜏 is defined as:
                                                   𝜌 (𝜀) = 𝜀
                                            𝜌 (𝜏 ↷ 𝑡) = 𝜌 (𝜏) ↷ 𝜌 (𝑡)
                                                  𝜌 (𝜎) = 𝜌 • 𝜎
                                            𝜌 (ev(ep)) = ev(𝜌 (ep))
                                                   𝜌 (𝑣) = 𝑣
1 The name “chop” stems from temporal interval logic [27].



                   ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:6                                                                                                Daniel Drodt


   Example 2.9. The trace 𝜏0 = ⟨𝜎0 ⟩ ↷ ev 0 (X) ↷ 𝜎0 [y ↦→ tt] in Example 2.5 is symbolic. With
𝜌 0 := [X ↦→ 3] we concretize it to 𝜌 0 • 𝜎0 = [X ↦→ 3, y ↦→ ff], 𝜌 0 • 𝜎0 [y ↦→ tt] = [X ↦→ 3, y ↦→ tt] =
𝜌 (𝜎0 ) [y ↦→ tt], and 𝜌 (𝜏0 ) := ⟨𝜌 (𝜎0 )⟩ ↷ ev0 (3) ↷ 𝜌 (𝜎0 ) [y ↦→ tt].
  Finally, we require continuation markers, as placeholders marking the unevaluated remainder of
an expression.
   Definition 2.10 (Continuation Marker). Let 𝑒 be a Rust expression. The continuation marker K(𝑒)
states that a trace is extended by the traces resulting from evaluating 𝑒.
   The set of symbolic traces with continuation markers, i.e., all 𝜏 · K(𝑒), is denoted as CTr. We call
the elements of CTr “continuation traces.”
   Finally, to ease reasoning over traces, they must adhere to a certain structure, e.g., agree on the
set of symbolic variables. Additionally, our semantics should not generate any symbolic traces, only
concrete ones. Definition 2.11 introduces well-formed and concrete (or “shining”) traces, which our
semantics generates.
                                                                                        Ð
   Definition 2.11 (Well-Formed and Shining Trace). Let 𝜏 be a symbolic trace and 𝑆 = 𝜎 ∈𝜏 symb(𝜎).
Trace 𝜏 is well-formed if conditions (1) to (3) hold.
                                                      ∀𝜎 ∈ 𝜏 . (dom(𝜎) \ symb(𝜎)) ∩ 𝑆 = ∅                     (1)
                                                                   ∀ev(ep) ∈ 𝜏 . vars(ep) ⊆ 𝑆                 (2)
                  ∀ev(ep), 𝜏1, 𝜏2, 𝜎1, 𝜎2 . (𝜏 = 𝜏1 ↷ 𝜎1 ↷ ev(ep) ↷ 𝜎2 · 𝜏2 → 𝜎1 ⊆ 𝜎2 )                       (3)
Condition (1) ensures that each variable is either symbolic in all states or in no state. Condition (2)
holds if all variables in events are symbolic. Finally, condition (3) states that the state succeeding an
event is an extension of the state preceding the event. 𝜎1 ⊆ 𝜎2 expresses that 𝜎2 is an extension of
𝜎1 (see Definition 2.3); hence, events may not alter the state but only introduce new variables to it.
  If a well-formed trace contains only concrete states (i.e., 𝑆 = ∅), we call it concrete or shining.
Shining traces are denoted by sh.
    Proposition 2.12. The concretization of a well-formed trace is a well-formed shining trace.

3    LAGC Semantics for Rust
This section presents an LAGC semantics for synchronous, safe Rust. Concretely, we cover the
expressions and statements in Fig. 1. Type, trait, and module definitions are left out, as they have
no evaluation and, therefore, require no LAGC treatment. Note that, due to our focus on the HIR,
macros are already expanded (though we still denote panic expressions, i.e., forceful errors that
stop the program’s execution, as panic!() for readability) and all loops are transformed into the
singular loop expression. For clarity, we assume a number of straightforward normalizations of the
HIR expressions: (i) all loops, break, and continue expressions have unique labels; (ii) all blocks,
and break expressions contain expressions, e.g., break 'l 2 ∗ 3 where 'l is the label and 2 ∗ 3 is the
break’s expression (this is achieved by inserting the unit expression “()” where necessary); (iii) all if
expressions have an else branch, and (iv) all functions have at least one explicit return expression.
   Observe that most syntactic structures that would be statements in other languages are expres-
sions in Rust, e.g., if and loop expressions. The intuitive semantics of such expressions is explained
alongside the formal semantics but we refer to the Rust book [42], the Rust reference [57], and the
ferrocene language specification (FLS) [63] for details.
   The syntax of expressions also contains an additional construct needed to model function calls
ergonomically: ?𝑖, where 𝑖 ∈ CId is a call identifier, serves as a stand-in for the value that is to be
returned by the function call with identifier 𝑖. The precise, formal semantics are outlined below.

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                            ZZZ:7


         𝑒 ∈ Exp ::= 𝑣 | x | !𝑒 | -𝑒 | *𝑒 | 𝑒 op 𝑒 | ae = 𝑒 | [𝑒] | (𝑒) | 𝑒(𝑒) | 𝑒.identifier(𝑒)
                         | match 𝑒 {𝑎𝑟𝑚} | 𝑒.identifier | 𝑒[𝑒] | &𝑒 | &mut 𝑒
                         | break ’𝑙 𝑒 | continue’𝑙 | return 𝑒 | x {identifier: 𝑒} | [𝑒; 𝑛] | {𝑠 𝑒}
                         | if 𝑒 𝑒 else 𝑒 | ’𝑙: loop 𝑒 | panic! () | ?𝑖
        𝑠 ∈ Stmt ::= 𝑒 | let pat = 𝑒;
       𝑙 ∈ Label ::= identifier
          𝑖 ∈ CId ::= callidentifier
         op ∈ Op ::= + | - | * | . . . | += | -= | *= | . . .
     arm ∈ Arm ::= pat => 𝑒
       pat ∈ Pat ::= _ | 𝑣 | x | x {identifier : pat} | x(pat) | (pat) | (pat | pat)
                         | 𝑒..𝑒 | 𝑒..=𝑒 | 𝑒.. | 𝑒..= | ..𝑒 | ..=𝑒
 ae ∈ AssignExp ::= pe | _ | [𝑎𝑒] | x {identifier: ae} | (𝑎𝑒) | x(𝑎𝑒)
  pe ∈ PlaceExp ::= x | pe[𝑒] | pe.identifier | *pe
        foo ∈ Fn ::= fn identifier(𝑥) 𝑒
    𝑟 ∈ Program ::= foo fn main() 𝑒

                            Fig. 1. The syntax of Rust’s HIR covered in this section.


   Some rules below, especially regarding assignments, also consider important subsets of Exp,
which we enumerate above: Place expressions (PlaceExp ⊂ Exp) are expressions that represent a
memory location, such as local variables, index expressions, dereferences, and field expressions.
Assignee expressions (AssignExp ⊂ Exp) are expressions that can appear on the left-hand side of
assignments. Aside from place expressions and the underscore expression (i.e., an assignment to
nowhere), these are used for destructuring. If a place expression pe contains only values in the index
and no dereferences, then pe ∈ Place. Further, if every place expression in an assignee expression
ae is in Place, it is an element of the assignee value set AssignVal ⊂ Exp.
   The considered subset covers almost all of safe Rust, the only limitation being closures, which
can be translated to normal functions. Async Rust’s features are discussed in Section 4. We are
interested in an operational semantics of Rust, hence we abstract away from memory layout and
typing. All expressions and functions in programs must be well-typed and all types must be known.
   Example 3.1 (Running Example). We consider a running example in this section which highlights
many important Rust features considered here, see Listing 1. It contains three functions: fac,
computing the factorial recursively, set_all setting all fields of an array passed via a mutable
reference to a given value. The main function calls the other two with example arguments.

Listing 1. A simple Rust program adhering to the           10      ∗a[i] = v; i += 1 }
simplifications above.                                     11     return (); ()
 1   fn fac(n: u64) −> u64 {                               12   }
 2     return if n <= 1 { 1 }                              13   fn main() {
 3     else {                                              14     let b = false;
 4       let left = n; let right = fac(n − 1);             15     let c = !b;
 5       left ∗ right }; ()                                16     let f = fac(4);
 6   }                                                     17     let arr = [8; 3];
 7   fn set_all(arr: &mut [u64; 3], v: u64) {              18     set_all(&mut arr, f);
 8     let mut i = 0;                                      19     return (); ()
 9     'l1: loop { if i == 3 { break 'l1 () } else {()}    20   }

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:8                                                                                                Daniel Drodt


3.1     Local Evaluation
We define a local evaluation function val𝜎 : Exp → 2CTr , mapping Rust expressions to a set of
symbolic continuation traces relative to state 𝜎. Each such trace contains state changes, emitted
events, and the continuation marker, denoting the expression or value with which we continue. We
define one local rule per kind of expression (syntax in Fig. 1). Due to the rich syntax, the number of
rules is quite large. Since Rust lacks a full, official specification [34], our local rules follow the Rust
reference [57] and the unofficial yet “adopted” FLS [63]. Observe that for the subset we consider,
every program has a deterministic execution.
   Values are already fully evaluated. Hence, we define a value’s local evaluation as the empty set.
                                                   val𝜎 (𝑣) = ∅                                               (4)
  Reading a local variable produces a set with a single continuation trace, starting with the state 𝜎
and a continuation with x’s value in 𝜎.
                                           val𝜎 (x) = {⟨𝜎⟩ · K(𝜎 (x))}                                        (5)
3.1.1 Evaluation of Sub-Expressions. A common pattern in the following rules and expressions
is that an expression 𝑒 contains sub-expressions, which need to be evaluated before 𝑒’s top-level
operator can be evaluated. For instance, for the expression (5 + 1) / 3, the division cannot be
evaluated until the sub-expression 5 + 1 is fully evaluated. Therefore, we require a way to obtain
for a given expression 𝑒 the next sub-expression 𝑒 ′ to be evaluated. However, in Rust, what this
sub-expression is, depends on the context: If we evaluate a[1 + 1] to a value, then “a” is the next
sub-expression. However, evaluating it in an assignment context, e.g., a[1 + 1] = 4 / 2, the behavior
is different: Because the left-hand side of an assignment is evaluated not to values but to assignee
values (AssignVal), the next sub-expression is 1 + 1.
   For that reason, we also require the context of the expression in addition to the next sub-
expression to be evaluated. This allows us to evaluate the next sub-expression and then replace
the old sub-expression with the result, leaving the rest of the expression unaltered. For this, we
introduce hole expressions. Let HoleExp with typical element he be defined analogous Exp but with a
new base case, a hole •, similar to holes in types and terms in functional programming [49, 67]. We
further require that • occurs exactly once per he ∈ HoleExp. For example, • / 3 is a hole expression.
This allows us to extract a sub-expression from an expression and substitute it without altering
the rest. We denote filling the hole in he ∈ HoleExp with expression 𝑒 as he⟨⟨𝑒⟩⟩. The result is an
element of Exp.
   We now obtain the next sub-expression with the function next : Exp × 2Exp → Exp × HoleExp,
which accurately models Rust’s evaluation order using the sub-expression’s context as second
argument. For example, next ((5 + 1) / 3, Val) is expected to yield (5 + 1, • / 3), which allows us to
evaluate the next sub-expression 5 + 1 to the value 6 which can then be inserted into the hole. We
get (• / 3)⟨⟨6⟩⟩ = 6 / 3. The next function must be defined such that for all 𝑒, 𝑒 ′, he, and 𝑀 such that
next (𝑒, 𝑀) = (𝑒 ′, he), we have he⟨⟨𝑒 ′ ⟩⟩ = 𝑒.
   The function next is defined recursively and, as mentioned before, it carries the context as its
second argument. The recursion stops when reaching an element of this set. Typically it is the
set Val or AssignVal. By default we are the context Val. For example, to evaluate the expression
a[1 + 1] = 4 / 2, we determine the next sub-expression by next (a[1 + 1] = 4 / 2, Val). In this case,
first 4 / 2 is evaluated, then a[1 + 1]. However, when we have a[1 + 1] = 2, we must consider the
left-hand side by calling next (a[1 + 1], AssignVal), because do not want to evaluate a[1 + 1] to a
value but to get the assignee value (in this case, it is a place) a[2]. The latter call yields (1 + 1, a[•]).
   We need to define next for all Rust expressions. For instance, the next sub-expression of the
negation expression !𝑒 is defined as follows: If 𝑒 also has a further sub-expression that is to be

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                             ZZZ:9


evaluated, we return it. Otherwise, if 𝑒 is not in Val, it is the next sub-expression and should be
evaluated to a value. We always pass Val to the recursive call, because negations cannot be part of
an assignee expression.
                                  (
                                    (!𝑒, •)   if 𝑒 ∈ Val
                   next (!𝑒, 𝑀) =
                                    (𝑒 , !he) if 𝑒 ∉ Val ∧ (𝑒 ′, he) = next (𝑒, Val)
                                       ′


  The expression if 𝑒 1 𝑒 2 else 𝑒 3 behaves similarly. Because the branches are only conditionally
evaluated depending on 𝑒 1 ’s value, they should not be considered as sub-expressions to be evaluated.
Hence, we only consider the condition and obtain the same cases and results as for negation.
                                       (
                                         (if 𝑒 1 𝑒 2 else 𝑒 3, •) if 𝑒 1 ∈ Val
       next (if 𝑒 1 𝑒 2 else 𝑒 3, 𝑀) =
                                         (𝑒 1′ , if he 𝑒 2 else 𝑒 3 ) if 𝑒 1 ∉ Val ∧ (𝑒 1′ , he) = next (𝑒 1, Val)
   An assignment ae = 𝑒 is evaluated by first evaluating the right-hand side 𝑒 to a value and then
the left-hand side ae to an assignee value. Hence, the second case, where 𝑒 is not a value and may
have further sub-expressions, behaves as above. If 𝑒 is a value, we treat ae similarly, but denote
that ae is to be evaluated to an assignee value. Observe that ae may contain sub-expression that
must be evaluated to values, e.g., 1 + 1 in a[1 + 1] = 4 / 2. Because assignments occur only on the
right-hand side, we do not consider 𝑀.
                          
                          
                           (ae = 𝑒, •)   if 𝑒 ∈ Val ∧ ae ∈ AssignVal
                          
                          
  next (ae = 𝑒, 𝑀) = (𝑒 ′, ae = ℎ𝑒) if 𝑒 ∉ Val ∧ (𝑒 ′, he) = next (𝑒, Val)
                          
                           ′                                               ′
                           (ae , he = 𝑒) if 𝑒 ∈ Val ∧ ae ∉ AssignVal ∧ (ae , he) = next (ae, AssignVal)
                          

   The second parameter matters when the expression can be an assignee expression, as in that
case sub-expressions should not be considered if they are places rather than values. For the index
expression 𝑒 1 [𝑒 2 ], if we are in an assignment context, 𝑒 1 is not a sub-expression if it is a place, e.g.,
x or x[1]. However, the indexing expression 𝑒 2 must be evaluated to a value.
                                  (𝑒 [𝑒 ], •) if 𝑒 1 ∈ 𝑀 ∧ 𝑒 2 ∈ Val
                                  1 2
                                 
                                 
                                 
           next (𝑒 1 [𝑒 2 ], 𝑀) = (𝑒 1′ , he[𝑒 2 ]) if 𝑒 1 ∉ 𝑀 ∧ (𝑒 1′ , he) = next (𝑒 1, 𝑀)
                                 
                                  (𝑒 ′ , 𝑒 1 [he]) if 𝑒 1 ∈ 𝑀 ∧ 𝑒 2 ∉ Val ∧ (𝑒 ′ , he) = next (𝑒 2, Val)
                                 
                                  2                                             2
   We do not enumerate all the other definitions for the remaining expressions here. See Appendix A
for the full definitions.
   This helper function allows us to express the pattern of evaluating sub-expressions concisely as
a local evaluation rule. We evaluate the first sub-expression one step, attach the trace generated by
the sub-expression, and rebuild the expression with the sub-expression replaced by its continuation.
Rule (6) considers only the cases where next (𝑒, Val) = (𝑒 ′, he) and he ≠ •; for all other expressions,
the rule is not applicable.
    val𝜎 (𝑒) = {𝜏 · K(he⟨⟨𝑒 ′′ ⟩⟩) | 𝜏 · K(𝑒 ′′ ) ∈ val𝜎 (𝑒 ′ )}   where next (𝑒, Val) = (𝑒 ′, he) ∧ he ≠ •       (6)
  With this rule in place, the remaining rules can assume that all sub-expressions are (assignment)
values, simplifying the presentation.
3.1.2 Arithmetic and Logic Operators. For clarity, we split the rules for operators, which are typically
overloaded via traits, into multiple definitions for different types. For bool, negation is defined as:
                                             (
                                               {⟨𝜎⟩ · K(ff)} if 𝑣 = tt
                                 val𝜎 (!𝑣) =                                                         (7)
                                               {⟨𝜎⟩ · K(tt)} if 𝑣 = ff

                   ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:10                                                                                               Daniel Drodt


   We present bitwise negation only for the case where 𝑒 is of type u8; all signed and unsigned
                                   − represents the mathematical subtraction operation over Z
integer types are analogous. Here, b
rather than the Rust operator.
                                       val𝜎 (!𝑣) = {⟨𝜎⟩ · K(28 b
                                                               −𝑣 b
                                                                  − 1)}                                       (8)
  Finally, for all other types, negation is resolved by calling the not function of the Not trait, as in
rule (9). The trait is in module core::ops, hence, we add the module to the call. We stress that the
rules are modular, as which rule is applied depends strictly on the local expression and its type, not
the wider context.
                                 val𝜎 (!𝑣) = val𝜎 (core::ops::Not::not(𝑣))                           (9)
   Example 3.2. Assume the program in Listing 1. Let 𝜎1 be the state [b ↦→ ff]. The local evaluation
of b in 𝜎1 yields val𝜎1 (b) = {⟨𝜎1 ⟩ · K(ff)}. Locally evaluating !ff in 𝜎1 gives {⟨𝜎1 ⟩ · K(tt)}. The
evaluation of !b in line 15 in 𝜎1 is val𝜎1 (!b) = {𝜏 · K(!𝑒) | 𝜏 · K(𝑒) ∈ val𝜎1 (b)}, which we simplify to
{⟨𝜎1 ⟩ · K(!ff)}.
   Sign negation is similar to bitwise negation, in that it is overloaded. We present the version for
i8 in rule (10); other integer types are similar. If the result of the negation would be outside the
type’s range (in i8’s case, [−128, 127]), a panic occurs.
                                     (
                                       {⟨𝜎⟩ · K(b
                                                −𝑣)}        if −128 < 𝑣 < 128
                         val𝜎 (-𝑣) =                                                             (10)
                                       {⟨𝜎⟩ · K(panic! ())} if 𝑣 = −128
   For all other types, the Neg trait’s function is invoked.
                                   val𝜎 (-𝑣) = val𝜎 (core::ops::Neg::neg(𝑣))                                (11)
  Addition is handled similarly to negation above: If the sub-values 𝑣 1, 𝑣 2 can be added without
exceeding the bounds of the type, we continue with this value; otherwise we emit a panic. For
non-integer types, the Add trait is used. Rule (12) shows the case for u8, where b   + again stands for
the mathematical addition over Z.
                                          (
                                            {⟨𝜎⟩ · K(𝑣 1 b
                                                         + 𝑣 2 )}        + 𝑣 2 ≤ 255
                                                                  if 𝑣 1 b
                      val𝜎 (𝑣 1 + 𝑣 2 ) =                                                          (12)
                                            {⟨𝜎⟩ · K(panic! ())} if 𝑣 1 b+ 𝑣 2 > 255
  Compound assignment proceeds by invoking the appropriate function of the AddAssign trait.
Observe that the left-hand side is a place and the right-hand side a value.
                      val𝜎 (𝑝 += 𝑣) = {⟨𝜎⟩ · K(AddAssign::add_assign(&mut 𝑝, 𝑣))}                           (13)
3.1.3 References. References are either shared (also called “immutable”) or mutable. As discussed
in Section 2, we represent shared references as Ref 𝑠𝑝 (𝑏) and mutable references as Ref 𝑚
                                                                                         𝑝 (𝑏), where
𝑝 is the borrowed place and 𝑏 is a borrow identifier.
   Rules (14) and (15) describe the evaluation of borrowing from a place 𝑝 to create a shared and
mutable reference, respectively. Note that rules (14) and (15) create fresh borrow identifiers, so that
two references created by different expressions are distinct.
                             val𝜎 (&𝑝) = {⟨𝜎⟩ · K(Ref 𝑠𝑝 (𝑏)) | 𝑏 ∈ BId, 𝑏 fresh}                           (14)
                          val𝜎 (&mut 𝑝) = {⟨𝜎⟩ · K(Ref 𝑚
                                                       𝑝 (𝑏)) | 𝑏 ∈ BId, 𝑏 fresh}                           (15)
   Example 3.3. Continuing the running example, evaluating the mutable reference expression in
line 18 in a state 𝜎2 = [arr ↦→ [8, 8, 8]] yields val𝜎 (&mut arr) = {⟨𝜎2 ⟩ · K(Ref 𝑚
                                                                                   arr (𝑏)) | 𝑏 ∈ BId}.
Observe, that we do not evaluate arr to create the mutable reference: a variable is a fully evaluated

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:11


place and the reference need not know the borrowed variable’s value. The generated set is infinite
if we assume BId to be infinite.
  Dereferencing an expression (*𝑣) has multiple possible evaluations. If 𝑣 is of a pointer type
(&T or &mut T), dereferencing evaluates to the referenced value. However, this is only legal if T
implements the Copy trait. Rule (16) handles this case.
                       val𝜎 (*𝑣) = {⟨𝜎⟩ · K(𝜎 (𝑝))}          if 𝑣 = Ref 𝑠𝑝 (𝑏) ∨ 𝑣 = Ref 𝑚
                                                                                         𝑝 (𝑏)                 (16)
  If 𝑣’s type is not a pointer type, dereferencing is evaluated via the Deref trait. As the trait’s
function takes a shared reference, we also add a borrow expression.
                            val𝜎 (*𝑣) = {⟨𝜎⟩ · K(*core::ops::Deref::deref(&𝑣))}                                (17)
3.1.4 Assignments. Assignments encompass a range of possible evaluations depending on the
left-hand side (the “assignee expression”). We split them into different rules for clarity. Rule (18)
handles the case where we assign to _, i.e., to nowhere. This assignment does not affect the state
and evaluates to the unit value.
                                            val𝜎 (_ = 𝑣) = {⟨𝜎⟩ · K(())}                                       (18)
Assigning to a program variable simply updates the state at this variable.
                                   val𝜎 (x = 𝑣) = {⟨𝜎⟩ ↷ 𝜎 [x ↦→ 𝑣] · K(())}                                   (19)
   An assignment to the field on an array of type [T; N], where T is the array’s element type and
N the array’s size, has two cases: If the index is less than the array’s length, the state is updated
at that location; otherwise, a panic occurs. The index must be of type usize, hence it cannot be
negative (see rule (20)). Index assignments to other types typically go through the IndexMut trait.
In rule (20), 𝑣 1, 𝑣 2 ∈ Val and 𝑝 ∈ Place is a place of type [T; N], i.e., a variable of the correct type,
a field access like x.f, or an inner array x.f[2]. Rule (21) work similarly for struct and tuple fields,
except no panic can occur.
                                               (
                                                 {⟨𝜎⟩ ↷ 𝜎 [𝑝 [𝑛] ↦→ 𝑣] · K(())} if 𝑛 < N
                       val𝜎 (𝑝[𝑣 1 ] = 𝑣 2 ) =                                                         (20)
                                                 {⟨𝜎⟩ · K(panic! ())}           otherwise
                        val𝜎 (𝑝.ident = 𝑣) = {⟨𝜎⟩ ↷ 𝜎 [𝑝.ident ↦→ 𝑣] · K(())}                       (21)
   The dereferencing expression evaluates a reference to a place 𝑝 which can then be assigned a
value by the expression *𝑟 = 𝑣, where 𝑟 is a reference. Because assigning to a dereferenced expression
is only permitted when the reference is a mutable reference, we know that 𝑟 = Ref 𝑚     𝑝 (𝑏) for some
𝑝 ∈ Place, 𝑏 ∈ BId. Rule (22) simply updates the corresponding place.
                             val𝜎 (*Ref 𝑚
                                        𝑝 (𝑏) = 𝑣) = {⟨𝜎⟩ ↷ 𝜎 [𝑝 ↦→ 𝑣] · K(())}                                (22)
   Next, we deal with the destructuring assignments, where parts of complex values can be assigned
to multiple locations at once. Since the assignment is correctly typed, we know that the value
on the right fits the assignee value on the left. Rules (23) to (26) deal with arrays, tuples, structs,
and tuple structs, respectively. All are evaluated by introducing a block with assignments to the
individual assignee values. Let 𝑇assign := {⟨𝜎⟩ · K({av 1 =𝑣 1 ; . . .; av𝑛 =𝑣𝑛 })} in the following, as all
these assignments lead to the same set of traces.
                                              val𝜎 ([av 1 , . . ., av𝑛 ] = [𝑣 1, . . . , 𝑣𝑛 ]) = 𝑇assign       (23)
                                               val𝜎 ((av 1 , . . ., av𝑛 ) = (𝑣 1, . . . , 𝑣𝑛 )) = 𝑇assign      (24)
                    val𝜎 (x {id 1 :av 1 , . . ., id𝑛 :av𝑛 } = x {id 1 :v1 , . . ., id𝑛 :v𝑛 }) = 𝑇assign        (25)
                                            val𝜎 (x(av 1 , . . ., av𝑛 ) = x(𝑣 1, . . . , 𝑣𝑛 )) = 𝑇assign       (26)

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:12                                                                                               Daniel Drodt


  Example 3.4. We demonstrate the state changes incurred by an assignment by continuing Ex-
ample 3.2: The assignment c = !b (line 15) in state 𝜎1 gives us the traces {𝜏 · K(c = 𝑒) | 𝜏 · K(𝑒) ∈
val𝜎 (!b)} = {⟨𝜎1 ⟩ · K(c = !ff)}. The assignment c = true, the result of multiple local evaluations,
yields: {⟨𝜎1 ⟩ ↷ 𝜎1 [c ↦→ tt] · K(())}.

3.1.5 Compound Types. Array expressions are evaluated by evaluating their elements left-to-right.
This is entirely handled by the rules in Section 3.1.1. The same approach works for tuples, struct,
and enum expressions.
   An array repeat expression creates an array value with the inner value repeated 𝑛 times.
                                                                   𝑛 times
                                                                z }| {                                      (27)
                                      val𝜎 ([𝑣; 𝑛]) = {⟨𝜎⟩ · K([𝑣, . . . , 𝑣])}

   To access a struct field or tuple field, we simply take the field’s value from the state.

                       val𝜎 (𝑣.ident) = {⟨𝜎⟩ · K(𝑣 ′ )}     where 𝑣 = x {ident : 𝑣 ′, . . .}                (28)

   Accessing the index of an array is similar to a struct field, besides the necessary bounds check: if
the index is at least the array’s length, a panic occurs. Since we know that 𝑣 ′ is of type usize, we
need not check for negative values. We only show the case for arrays; all other types are translated
to a trait function call.
                                     (
                                       {⟨𝜎⟩ · K(𝑣 𝑣 ′ )}    if 𝑣 = [𝑣 0, . . . , 𝑣𝑛 ], 𝑣 ′ ≤ 𝑛
                    val𝜎 (𝑣[𝑣 ′ ]) =                                                              (29)
                                       {⟨𝜎⟩ · K(panic! ())} otherwise

3.1.6 Basic Control Flow. Evaluating a conditional expression such as if 𝑣 𝑒 1 else 𝑒 2 is straightfor-
ward: If condition 𝑣 is the true value, we continue with the then expression 𝑒 1 ; if 𝑣 is false, we
continue with 𝑒 2 .
                                                      (
                                                        {⟨𝜎⟩ · K(𝑒 1 )} if 𝑣 = tt
                          val𝜎 (if 𝑣 𝑒 1 else 𝑒 2 ) =                                              (30)
                                                        {⟨𝜎⟩ · K(𝑒 2 )} if 𝑣 = ff

  Example 3.5. When evaluating the if in line 2 in a state 𝜎3 = [n ↦→ 4], we evaluate the
condition. Once the condition is simplified to ff, we have val𝜎 (if ff {1} else {let left = . . . }) =
{⟨𝜎3 ⟩ · K({let left = . . . })}.

   A match expression is evaluated step-wise. First, we consider the first arm. This arm contains a
pattern pat and a body 𝑒. If the pattern’s structure fits the matched value (the scrutinee), we want to
continue with this arm. However, pattern matching may introduce new variable bindings: A match
arm like x => {x + 2}, where x is some integer variable, does not compare the scrutinee’s value with
the value of an existing variable x. Instead, a new variable x is added to the scope and it is bound to
the scrutinee’s value.
   To accommodate this binding pattern, we use the partial function patMatch𝜎 : Pat × Val ⇀ State,
which takes a pattern and a value and returns an extension of state 𝜎, that is, new values may be
introduced but no existing values changed.
   We cover a few important cases of the function patMatch𝜎 below. The wildcard pattern “_”
always matches, values (i.e., literal patterns) match if they are exactly the scrutinee’s value, binding
patterns (x) introduce new variables, and the alternative pattern considers both sub-patterns and
returns the first successful match. The other patterns follow the same approach. Note that we use

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:13


the symbol “↑” to denote undefinedness.
               patMatch𝜎 (_, 𝑣) = 𝜎(
                                         𝜎 if 𝑣 1 = 𝑣 2
             patMatch𝜎 (𝑣 1, 𝑣 2 ) =
                                         ↑ otherwise
               patMatch𝜎 (x, 𝑣) = 𝜎 [x ↦→ 𝑣]
                                        𝜎 if patMatch𝜎 (pat 1, 𝑣) = 𝜎1
                                        1
                                       
                                       
                                       
       patMatch𝜎 (pat 1 | pat 2, 𝑣) = 𝜎2 if patMatch𝜎 (pat 1, 𝑣)↑ ∧ patMatch𝜎 (pat 2, 𝑣) = 𝜎2
                                       
                                       ↑ otherwise
                                       
                                       
                                   ...
  If the first pattern does not match, we remove its arm from the match expression and continue
with the rest. The Rust compiler ensures that the match arms are exhaustive, hence we need not
cover the case of all arms being removed.
                                     (
                                       {⟨𝜎⟩ ↷ 𝜎 ′ · K(𝑒)}         if patMatch𝜎 (pat, 𝑣) = 𝜎 ′
  val𝜎 (match 𝑣 {pat => 𝑒, arm}) =                                                            (31)
                                       {⟨𝜎⟩ · K(match 𝑣 {arm})} if patMatch𝜎 (pat, 𝑣)↑
3.1.7 Function and Method Calls. Evaluating functions and methods introduces additionally com-
plexity that must be managed by the semantics. To model the lifecycle of a call—invocation,
execution, computation, and reaction to the computation—it is helpful to directly express these
points in the semantics and the generated traces. Hence the events we allow in our traces. We
make use of four call events in this section, one for each point of the lifecycle of a call. These four
events follow the four event semantics of Din et al. [16]. Including these events directly in the trace
permits easy, declarative restrictions on the order of events to ensure correct evaluation order.
   To evaluate calls, we emit an invocation event with the function identifier, a unique but arbitrary
call identifier 𝑖 ∈ CId, where CId is the set of call identifiers, and the call arguments. We discuss
below, how we ensure uniqueness of the call identifiers. Because the trace composition rules take
care of actually executing the called function, the local evaluation rule needs to put a placeholder
in the continuation marker that denotes that this expression will evaluate to the value returned by
the call with identifier 𝑖. For that, we introduce the get expression ?𝑖 with 𝑖 ∈ CId. This is necessary
to mark that this expression cannot be resolved until the called function is completely executed
and to access the called function’s return value.
                        val𝜎 (𝑣(𝑣)) = {⟨𝜎⟩ ↷ invEv(𝑣, 𝑖, 𝑣) ↷ 𝜎 · K(?𝑖) | 𝑖 ∈ CId}                             (32)
  Method calls, e.g., x.m(1 + 1) behave similarly to regular function calls but we make use of the
method lookup function method2Fn(𝑣, 𝑚), which yields the function name for the method 𝑚 on
callee 𝑣. Assume in rule (33) for brevity that foo = method2Fn(𝑣, 𝑚). Observe that the callee is
added as the first argument of the call identifier. This matches Rust’s treatment of methods [57].
                    val𝜎 (𝑣.𝑚(𝑣)) = {⟨𝜎⟩ ↷ invEv(foo, 𝑖, 𝑣, 𝑣) ↷ 𝜎 · K(?𝑖) | 𝑖 ∈ CId}                          (33)
  To evaluate a function’s body, we extend val𝜎 to a function declaration, emitting an invocation
reaction event, introducing symbolic variables X for the parameter’s values, and continuing with
the body where the parameters x have been substituted with X. We use the notation 𝑒 [x ← X] for
syntactically substituting all x ∈ x with the corresponding X ∈ X in 𝑒.
  val𝜎 (fn foo(x) 𝑒) = {⟨𝜎⟩ ↷ invREv(foo, 𝑖, X) ↷ 𝜎 [X ↦→ ∗] · K(𝑒 [x ← X]) | 𝑖 ∈ CId, X fresh} (34)
  Example 3.6. Consider the call in line 16 and assume that the callee is already evaluated to the
function identifier fac. Both callee and argument are already values, hence, we have val𝜎1 (fac(4)) =

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:14                                                                                               Daniel Drodt


{⟨𝜎1 ⟩ ↷ invEv(fac, 𝑖, 1) ↷ 𝜎1 · K(?𝑖) | 𝑖 ∈ CId}. The get expression ?𝑖 creates a computation
reaction event and we must ensure, as we do below, that this is only evaluated directly after the
function call with id 𝑖 is completed. Evaluation of the body gives us
   val𝜎1 (fn fac(n) 𝑒) = {⟨𝜎⟩ ↷ invREv(fac, 𝑖, X) ↷ 𝜎1 [X ↦→ ∗] · K(𝑒 [n ← X]) | 𝑖 ∈ CId, X fresh}
where 𝑒 is the body of fac in Listing 1.
  An expression return 𝑣 emits a return event with the returned value. The return expression
evaluates to the unit value, because the returned value is not to be considered for the surrounding
context. Instead, the event is used to transmit the return value to the caller.
                              val𝜎 (return 𝑣) = {⟨𝜎⟩ ↷ retEv(𝑣) ↷ 𝜎 · K(())}                                (35)
  The get expression emits a computation reaction event and introduces a fresh symbolic variable X
which represents the value returned by call 𝑖.
                   val𝜎 (?𝑖) = {⟨𝜎⟩ ↷ compREv(𝑖, X) ↷ 𝜎 [X ↦→ ∗] · K(X) | X fresh}                          (36)
   Example 3.7. Combining the results of Examples 3.1 to 3.4 and 3.6, we obtain the following traces:
                        val𝜎0 (b = false) = {⟨𝜎0 ⟩ ↷ 𝜎1 · K(())}
                           val𝜎1 (c = !b) = {⟨𝜎1 ⟩ · K(c = !ff)}
                           val𝜎1 (c = !ff) = {⟨𝜎1 ⟩ · K(c = tt)}
                            val𝜎1 (c = tt) = {⟨𝜎1 ⟩ ↷ 𝜎2 · K(())}
                       val𝜎2 (f = fac(4)) = {⟨𝜎1 ⟩ ↷ invEv(fac, 𝑖, 4) ↷ 𝜎2 · K(f = ?𝑖) | 𝑖 ∈ CId}
                     val𝜎3 (arr = [8; 3]) = {⟨𝜎3 ⟩ · K(arr = [8, 8, 8])}
                  val𝜎3 (arr = [8, 8, 8]) = {⟨𝜎3 ⟩ ↷ 𝜎4 · K(())}
           val𝜎4 (set_all(&mut arr, f)) = {⟨𝜎4 ⟩ · K(set_all(Ref 𝑚
                                                                 arr (𝑏), f)) | 𝑏 ∈ BId}
with dom(𝜎0 ) = ∅, 𝜎1 = 𝜎0 [b ↦→ ff], 𝜎2 = 𝜎1 [c ↦→ tt], 𝜎3 = 𝜎2 [f ↦→ 24], 𝜎4 = 𝜎3 [arr ↦→ [8, 8, 8]].
Clearly, the resulting trace of this series of computations must be of the form
                         ⟨𝜎0 ⟩ ↷ 𝜎1 ↷ 𝜎2 ↷ invEv(fac, 𝑖, 4) ↷ · · · ↷ 𝜎3 ↷ 𝜎4 .
What is missing so far is (1) local rules dealing with variable declarations as in Listing 1, not just
assignments, (2) local rules dealing with blocks, and (3) a way to compose these individual local
rules into one single trace. We deal with the first two items immediately and return to the third
one in Section 3.3.
3.1.8 Block Expressions. When a block is fully evaluated and, hence, removed from the continuation,
we want to drop all local variables this block introduced, i.e., remove them from the state. This
requires bookkeeping of which variables are introduced by a block. Thus, we add a syntactic
extension called scoped block expressions: {x ≬ 𝑠 𝑒} stands for the block expression {𝑠 𝑒}, which
has so far introduced the local variables x. For brevity, we also write {𝑠 𝑒} for the scoped block
expression {∅ ≬ 𝑠 𝑒}.
   Expressions and statements in blocks are also evaluated piecemeal. Declarations with initial
value are split into the declaration and the assignment. For simplicity, we only show rules for
declaring variables.
                        val𝜎 ({x ≬ let y = 𝑒 1 ; 𝑠 𝑒 2 }) = val𝜎 ({x ≬ let y; y = 𝑒 1 ; 𝑠 𝑒 2 })            (37)
  A declaration of program variable y is evaluated by adding y to the declared variables in the
block. Additionally, to avoid name clashes in our state caused by, e.g., evaluating two function

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
     A Complete, Formal Semantics for Rust Source Code                                                             ZZZ:15


     bodies in parallel, we rename y to a fresh program variable y′ . As there are potentially infinitely
     many fresh y′ , rule (38) may introduce infinitely many traces; which of these is chosen is covered
     in Section 3.3.
                          val𝜎 ({x ≬ let y; 𝑠 𝑒}) = {⟨𝜎⟩ · K({x, y ≬ 𝑠 𝑒}[y ← y′ ]) | y′ fresh}                       (38)
       The first expression in a block is either a value or a complex expression. The latter case is handled
     by Section 3.1.1. In the former case, we can remove it as in rule (39).
                                         val𝜎 ({x ≬ 𝑣; 𝑠 𝑒}) = {⟨𝜎⟩ · K({x ≬ 𝑠 𝑒})}                                   (39)
       A block containing only the final value 𝑣 is removed, all variables introduced by the block are
     dropped, i.e., removed from the state, and we continue with 𝑣 only.
                                         val𝜎 ({x ≬ 𝑣}) = {⟨𝜎⟩ ↷ (𝜎 \ x) · K(𝑣)}                                      (40)
        Panics, in turn, are handled by emitting a panic event and leaving the unit value behind. Abrupt
     termination is modeled during composition.
                                   val𝜎 (panic! ()) = {⟨𝜎⟩ ↷ panicEv() ↷ 𝜎 · K(())}                                   (41)
     3.1.9 Loops. The more complex control flow options of a loop, including break and continue prove
     to be a challenge, as they require the context of the surrounding loops, which complicates control
     flow, especially when labeled jumps are involved. We model loops by extending the syntax with
     loop frames, taking inspiration from loop scopes in deductive program verification [61]. These frames
     permit tracking of the surrounding loop context while leaving the original loop—to which the
     program might jump again—unaltered. A loop frame lframe(‘𝑙, 𝑒) states that we are evaluating the
     loop with label 𝑙 and that the current expression to be evaluated of the loop’s body is 𝑒. Once the
     loop body is fully evaluated, the loop is evaluated from the beginning again. Figure 2 demonstrates
     the possible relevant control flow options in a loop. Breaks jump out of the loop addressed by its
     label; continues jump to the next iteration of its corresponding loops. Note that the loop with label
     'l1 has an integer value (i, once the corresponding break in line 8 is executed) and the loop 'l2 has
     the unit value ().

 1   'l1: loop {
 2     'l2: loop {
 3       if i < −3 {
 4         continue 'l2
 5       } else if i < 0 {
 6         continue 'l1
 7       } else if i == 3 {
 8         break 'l1 i
 9       } else if i == 4 {
10         break 'l2 ()
11       } else { i += 2 }
12     }
13   }


                              Fig. 2. Possible control-flow paths of a loop expression in Rust.


                         ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:16                                                                                                Daniel Drodt


   To start a loop’s evaluation, it is translated to a loop frame.
                                     val𝜎 (’𝑙: loop 𝑒) = val𝜎 (lframe(‘𝑙, 𝑒))                                (42)
   In Rust, break expressions contain an (optional) expression. These expressions mark the value of
the loop or block to which the break’s label refers. A loop expression’s value thus depends on the
break expression contained therein.
   A break with value 𝑣 in a loop is resolved in one of two ways: If the label matches the active loop
frame’s label, we continue with the expression. Otherwise, we replace the entire frame with the
break expression. The following rules consider a break expression in the context of a loop frame
and a block. The latter may contain additional statements and an expression after the break. These
are discarded once the break is evaluated.
                                                          (
                                                            {⟨𝜎⟩ · K({x ≬ 𝑣})}            𝑙1 = 𝑙2
          val𝜎 (lframe(‘𝑙 1, {x ≬ break ’𝑙 2 𝑣; 𝑠; 𝑒})) =                                           (43)
                                                            {⟨𝜎⟩ · K({x ≬ break ’𝑙 2 𝑣})} 𝑙 1 ≠ 𝑙 2
   When we encounter a continue expression with label 𝑙 2 in a loop frame, we evaluate the loop with
label 𝑙 2 , using the function “getLoop,” which maps labels to loops. We maintain the surrounding
block to maintain the scope, which preserves proper dropping of the declared variables.
            val𝜎 (lframe(‘𝑙 1, {x ≬ continue’𝑙 2 ; 𝑠; 𝑒})) = {⟨𝜎⟩ · K({{x ≬ ()}; getLoop( ′𝑙 2 )})}          (44)
  If the loop frame’s expression is not a continue or break, we re-insert the loop of the active label,
repeating execution. The value of the loop’s body is ignored, as only break expressions affect the
loop’s value.
                            val𝜎 (lframe(‘𝑙, 𝑣)) = {⟨𝜎⟩ · K(getLoop( ′𝑙))}                         (45)
   Example 3.8. Evaluating a loop expression 'l loop { if n == 0 { break 'l true; } else {()} n −= 1; } in
state 𝜎2 = [n ↦→ 1] leads to val𝜎2 (’l loop . . .) = val𝜎2 (lframe(‘l, {if . . .})), which we further evaluate
to {⟨𝜎2 ⟩ · K(lframe(‘l, {if 1 == 0 . . .}))}. Evaluating val𝜎3 (lframe(‘l, {break ’l true;})), where 𝜎3 =
𝜎2 [n ↦→ 0], yields {⟨𝜎3 ⟩ · K({true})}.

3.2   Well-Formedness of Traces
Without any restrictions, the traces generated by our semantics do not necessarily describe pos-
sible program behavior, as they encompass traces with undesired behavior, e.g., a function body
evaluation where the parameters do not match the call arguments. The well-formedness predicate
wf restricts the set of generated traces to ensure a certain ordering and matching between events.
This predicate is defined over shining traces and hence defines additional restrictions on top of
Definition 2.11. We define the well-formedness predicate recursively: An empty trace is always
well-formed, as is the trace ⟨𝜎⟩. States do not influence the well-formedness, and a panic event can
only occur as the final event and it is followed by exactly one state.
                                         wf (𝜀) = true
                                   wf (𝜀 ↷ 𝜎) = true
                             wf (sh ↷ 𝑡 ↷ 𝜎) = wf (sh ↷ 𝑡) ∧ panicEv() ∉ sh
                          wf (sh ↷ panicEv()) = wf (sh)
  Every invocation event must have a unique call identifier. For the invocation reaction, we require
that the last event prior is an invocation event with matching function name, call id, and arguments.
This requirement also implies that each invocation is reacted to at most once.
                 wf (sh ↷ invEv(foo, 𝑖, 𝑣)) = wf (sh) ∧ foo′, 𝑣 ′ . invEv(foo′, 𝑖, 𝑣 ′ ) ∈ sh               (46)
                                                                                             
                wf (sh ↷ invREv(foo, 𝑖, 𝑣)) = wf (sh) ∧ invEv(foo, 𝑖, 𝑣) = lastEv(sh)                        (47)

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:17


   No restrictions are placed on the return event, while the computation reaction event—similarly
to the invocation’s case—must follow immediately its corresponding return event.

                         wf (sh ↷ retEv(𝑣)) = wf (sh)                                                          (48)
                                                                                                  
                wf (sh ↷ compREv(foo, 𝑣)) = wf (sh) ∧ compEv(foo, 𝑣) = lastEv(sh)                              (49)

  Example 3.9. The trace ⟨𝜎0 ⟩ ↷ panicEv() ↷ 𝜎0 ↷ invEv(foo, cid 0, 3) ↷ 𝜎0 is not well-
formed, as the panic event is succeeded by an invocation event. However, the trace ⟨𝜎0 ⟩ ↷
invEv(foo, cid 0, 3) ↷ 𝜎0 ↷ invREv(foo, cid 0, 3) ↷ 𝜎0 [x ↦→ 3] is well-formed as the invocation
reaction event matches the invocation event and follows it immediately.

3.3   Trace Composition Rules
So far, our semantics provides the local, symbolic traces for each expression and a definition of
“correct” (well-formed) traces. The next step in an LAGC semantics is to compose together the local
traces generated in Section 3.1 into well-formed, shining traces (see Definition 2.11). We define
trace composition rules, which govern how traces are combined.
   Trace composition rules are transition rules and define the relation → between two configurations.
In general, a configuration consists of a shining trace and some data structures over continuation
markers. The former is the trace generated so far, the latter represents in some form the remaining
program to evaluate. Thus, the configuration expresses the global state of the program evaluation
as well as its history in the form of the trace.
   In the synchronous Rust case, we aim to model the call stack created by function and method
calls. Hence, we choose as configuration
                                                        h i
                                                     sh, 𝑘


where 𝑘 are continuations and the left-most continuation is the top element.
  All composed traces must be well-formed according to wf . This restricts both the local traces
that may be chosen and the applicability of rules.
  Assume an expression 𝑒 and a shining trace sh. The trace composition rule (50) defines the
derivation from the configuration sh, [K(𝑒), 𝑘] to sh ∗∗ 𝜌 (𝜏), [K(𝑒 ′ ), 𝑘], where 𝑒 is the expression in
the top continuation marker of the continuation stack. We take the last state of sh to evaluate 𝑒
one step further. This yields a set of continuation traces, from which we pick one trace, 𝜏 · K(𝑒 ′ ),
arbitrarily. The trace 𝜏 may be symbolic and we use concretization mapping 𝜌 to concretize it. Then,
we use chop to stitch the concretized trace 𝜌 (𝜏) to sh and continue with 𝑒 ′ in the top continuation
marker. The lower levels of the stack are unchanged.


                 𝜎 = last(sh)     𝜏 · K(𝑒 ′ ) ∈ val𝜎 (𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                       h         i              h        i                                     (50)
                                   sh, K(𝑒), 𝑘 → sh ∗∗ 𝜌 (𝜏), K(𝑒 ′ ), 𝑘

    Example 3.10. We continue the running example. Assume a state 𝜎0 with dom(𝜎0 ) = ∅ and let
𝑒 0 be the main function’s block in Listing 1. Let further 𝜎1 := 𝜎0 [x ↦→ ff] and 𝜎2 := 𝜎1 [y ↦→ tt].
We start in configuration ⟨𝜎0 ⟩, [K(𝑒 0 )]. As the states are concrete, we can use the concretization
mapping 𝜌 0 with dom(𝜌 0 ) = ∅ throughout. By repeated applications of rule (50) we obtain the

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:18                                                                                               Daniel Drodt


following derivation
                ⟨𝜎0 ⟩, [K(𝑒 0 )] → ⟨𝜎0 ⟩, [K({x ≬ x = false; . . .})]
             →⟨𝜎0 ⟩ ↷ 𝜎1, [K({x ≬ let c = !x; . . .})] → ⟨𝜎0 ⟩ ↷ 𝜎1, [K({x,y ≬ y = !x; . . .})]
             →⟨𝜎0 ⟩ ↷ 𝜎1, [K({x,y ≬ y = !ff; . . .})] → ⟨𝜎0 ⟩ ↷ 𝜎1, [K({x,y ≬ y = tt; . . .})]
             →⟨𝜎0 ⟩ ↷ 𝜎1 ↷ 𝜎2, [K({x,y ≬ let f = fac(4);. . .})]
             →⟨𝜎0 ⟩ ↷ 𝜎1 ↷ 𝜎2, [K({x,y ≬ let f; f = fac(4);. . .})]
             →⟨𝜎0 ⟩ ↷ 𝜎1 ↷ 𝜎2, [K({x,y,z ≬ z = fac(4);. . .})]
             →⟨𝜎0 ⟩ ↷ 𝜎1 ↷ 𝜎2 ↷ invEv(fac, 𝑖 0, 4) ↷ 𝜎2, [K({x,y,z ≬ z = ?𝑖 0 ;. . .})]
It is not possible to apply rule (50) further, as the well-formedness predicate prohibits adding the
computation reaction event that evaluation of ?𝑖 0 would yield. Observe that we could have many
other derivations similar to the one above, the only difference being that different concrete variable
namings and call identifiers are chosen.
   Rule (50) ensures that all constructed traces are well-formed and concrete. The composition is
also stuck if the last event of sh is a panicEv event, as we cannot continue past such a fatal error.
Similarly, it is not applicable if 𝑒 is a value, because values generate no traces.
   Rule (51) executes a function body and pushes the resulting continuation onto the continuation
stack. The rule may pick any function from the program at any point, leading to possible spurious
function execution. However, the predicate wf ensures with equation (47) that rule (51) is only
applicable when appropriate, i.e., immediately after its corresponding invocation event, and with
the correct function. This restriction ensures correct applications of the rule and prohibits spurious
function executions.
                                       𝜎 = last(sh) fn foo(x) 𝑒 ∈ Fn
                   𝜏 · K(𝑒 ′ ) ∈ val𝜎 (fn foo(𝑥) 𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                          h i               h       i                              (51)
                                                                ′
                                      sh, 𝑘 → sh ∗∗ 𝜌 (𝜏), K(𝑒 ), 𝑘

   Example 3.11. Continuing Example 3.10 we start from configuration ⟨𝜎0 ⟩ ↷ 𝜎1 ↷ 𝜎2 ↷
invEv(fac, 𝑖 0, 4) ↷ 𝜎2, [K({x,y,z ≬ z=?𝑖 0 ;. . .})] by executing function fac and putting the result to
the top of the continuation stack. By rule (51) we derive ⟨𝜎0 ⟩ ↷ 𝜎1 ↷ 𝜎2 ↷ invEv(fac, 𝑖 0, 4) ↷
𝜎2 ↷ invREv(fac, 𝑖 0, 4) ↷ 𝜎3, [K({p ≬ return if p <= 1 . . .}), K({x,y,z ≬ z=?𝑖 0 ;. . .})] where we have
𝜎3 := 𝜎2 [p ↦→ 4]. Note how the trace composition applies the concretization: The symbolic variables
introduced by rule (34) are immediately concretized and the well-formedness predicate ensures
that it is concretized to the actual call arguments. With rules (50) and (51) we can also evaluate the
next call of fac with argument 3 in line 4 but we cannot, as yet, continue after a function returns.
   Once a function call completes, we require a rule to pop the top continuation off the continuation
stack, effectively returning control to the calling function. Crucially, we cannot do this step once
the top continuation marker contains a value, i.e., is fully evaluated, because a return-expression
may not be the last or only expression in a function body; it can occur at any point. Because this
return emits a return event and immediately stops the function’s evaluation, we want to pop the
top continuation marker off the stack at this point.
   Observe that, by rules (32) and (51) and equations (46) and (47), any continuation marker but
the top one must contain as the next sub-expression to be evaluated a get expression ?𝑖—i.e., any
continuation marker except the top one is waiting on the function call above it to finish. By rule (36)
and equation (49), such a get expression ?𝑖 can be evaluated iff the call 𝑖 has just returned. This
condition precisely models when we can clean up the continuation marker for the call 𝑖.

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:19


  Hence, the structure of rule (52): We remove the top continuation marker K(𝑒) if we can evaluate
the continuation marker K(𝑒 ′ ) below it and the result is well-formed according to equation (49). We
know that 𝑒 ′ ’s next sub-expression to be evaluated is a get expression waiting on K(𝑒) to finish. If
the result is well-formed, the top continuation marker must have just returned and must therefore
be removed from the stack.
                𝜎 = last(sh) 𝜏 · K(𝑒 ′′ ) ∈ val𝜎 (𝑒 ′ ) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                h               i                h          i                     (52)
                            sh, K(𝑒), K(𝑒 ′ ), 𝑘 → sh ∗∗ 𝜌 (𝜏), K(𝑒 ′′ ), 𝑘

    Example 3.12. We continue Example 3.11. After the call with identifier 𝑖 0 , we have a configu-
ration of the form · · · ↷ invEv(fac, 𝑖 0, 4) ↷ · · · ↷ retEv(24) ↷ 𝜎3, [K(()), K({x,y,z ≬ z=?𝑖 0 ;. . .})].
Observe that the called function’s continuation marker does not contain the return value; this value
is transmitted only via events and is not passed to the surrounding context of the return. Rule (52)
allows to remove the stack’s top and continue local evaluation of the main block with rule (36):
· · · ↷ retEv(24) ↷ 𝜎3 ↷ compREv(𝑖 0, 24) ↷ 𝜎3, [K({x,y,z ≬ z=24;. . .})].

3.4   Global Program Semantics
It remains to define the starting point of trace composition and the semantics of a Rust program as a
whole. Definition 3.13 further defines a partial semantics, which gives meaning to a Rust expression
relative to a state 𝜎. Partial semantics are crucial to the soundness proofs of Section 6.
  Definition 3.13 ((Partial) Program Semantics). Let 𝑒 be a Rust expression and 𝜎 a concrete state.
Assume a maximal sequence of applications of rules (50) to (52)
                                        sh0, [K(𝑒)] → sh1, [𝑘] → · · ·
with sh0 = ⟨𝜎⟩. If the sequence is finite, it has the form
                                                                     ′
                                            ⟨𝜎⟩, [K(𝑒)] →∗ sh, [𝑘 ]
with →∗ being the transitive closure of →. If the sequence is infinite, we define sh = lim𝑖→∞ sh𝑖 .
We denote the set of all such traces, whether finite or infinite, as Tr(𝑒, 𝜎).
  For a Rust program 𝑟 with the main function fn main() 𝑒, we define the set of traces for 𝑟 as
Tr(𝑟 ) := Tr(main(), 𝜎), where 𝜎 is the state with dom(𝜎) = ∅.
  Example 3.14. Continuing Example 3.2, we start in configuration ⟨𝜎1 ⟩, K(!b). With the local
evaluation, we derive ⟨𝜎1 ⟩, K(!ff), which is the only possible derivation. We then compose this with
the local evaluation of !ff to get ⟨𝜎1 ⟩, K(tt). This trace is the only element of Tr(!b, 𝜎1 ).
  Example 3.15. Let x, y be program variables of type u32, b a variable of type bool, 𝜎0 the state
that assigns x, y the value 0 and b ff. For the Rust program x = if b {y = 3; y − 2} else {y = 4; y + 1},
we have the following derivation:
                ⟨𝜎0 ⟩, K(x = if b {y = 3; y - 2} else {y = 4; y + 1})
            → ⟨𝜎0 ⟩, K(x = if ff {y = 3; y - 2} else {y = 4; y + 1})
            → ⟨𝜎0 ⟩, K(x = {y = 4; y + 1}) → ⟨𝜎0 ⟩ ↷ 𝜎0 [y ↦→ 4], K(x = {(); y + 1})
            → ⟨𝜎0 ⟩ ↷ 𝜎0 [y ↦→ 4], K(x = {y + 1}) → ⟨𝜎0 ⟩ ↷ 𝜎0 [y ↦→ 4], K(x = {4 + 1})
            → ⟨𝜎0 ⟩ ↷ 𝜎0 [y ↦→ 4], K(x = {5}) → ⟨𝜎0 ⟩ ↷ 𝜎0 [y ↦→ 4], K(x = 5)
            → ⟨𝜎0 ⟩ ↷ 𝜎1 [y ↦→ 4] [x ↦→ 5], K(())
  Example 3.16. Consider the expression 𝑒 = {let x; x = 1; x}. Assume a concrete state 𝜎2 ; we start
with ⟨𝜎2 ⟩, K({let x; . . .}). Per rule (38), the local evaluation yields the set {⟨𝜎2 ⟩ · K({y ≬ y = 1; y}) |

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:20                                                                                               Daniel Drodt


y fresh}. Hence, rule (50) can pick any of these infinite traces to compose. We choose variable z as
an example, yielding ⟨𝜎2 ⟩, K({z ≬ z = 1; z}). Evaluating twice with both cases of rule (39), we have
⟨𝜎2 ⟩ ↷ 𝜎2 [z ↦→ 1], K({z ≬ z}). Using rules (5) and (40), we have ⟨𝜎2 ⟩ ↷ 𝜎2 [z ↦→ 1], K({z ≬ 1}),
which we finally evaluate with rule (40) to ⟨𝜎2 ⟩ ↷ 𝜎2 [z ↦→ 1] ↷ 𝜎2, K(1). The set Tr(𝑒, 𝜎2 ) is the
set containing all traces of this form with different instantiations for y. The first and final states are
the same for all these traces.
  Example 3.17. Consider a very simple program like fn main() { panic!(); let x = 1; () }. Evaluating
this program in state 𝜎0 with dom(𝜎0 ) = ∅, we first evaluate the panic expression and obtain
the configuration ⟨𝜎0 ⟩ ↷ panicEv() ↷ 𝜎0, [{(); let x = 1; ()}]. We cannot continue from this
configuration, as the well-formedness predicate allows exactly one state after a panic event and
nothing else. Hence, this is the maximal application.
  Example 3.18. Assume the program fn main() { 'l: loop { () } }, which is obviously non-terminating.
Due to our use of chop, where ⟨𝜎0 ⟩ ∗∗ ⟨𝜎0 ⟩ = ⟨𝜎0 ⟩, we obtain the following infinite derivation:
                                           𝜎0, [K({’l: loop {()}})]
                                       → ⟨𝜎0 ⟩, [K({lframe(‘l, {()})})]
                                       → ⟨𝜎0 ⟩, [K({lframe(‘l, ())})]
                                       → ⟨𝜎0 ⟩, [K({getLoop(l}))]
                                       → ⟨𝜎0 ⟩, [K({’l: loop {()}})]
                                       → ...
Hence, the traces for the program consist just of a singleton trace: {⟨𝜎0 ⟩}. If the loop has an effect
on the state, e.g., 'l: loop { x += 1 }, where x is originally set to 0, the resulting trace would be an
infinite trace of the form ⟨𝜎0 ⟩ ↷ [x ↦→ 1] ↷ [x ↦→ 2] ↷ . . . . See [17] for a discussion of this
modeling of infinite computations.
   We want to state some general properties over the set of generated concrete traces for a state
and expression Tr(𝑒, 𝜎). In particular, we notice that for the synchronous subset of Rust presented
in Fig. 1 the generated traces differ only in the names chosen for local variables, e.g., in rule (38),
and chosen borrow identifiers. Hence, Definitions 3.20 and 3.22 introduce the notion of relative
equality. Intuitively, two states may have different names for some variables but they must agree
on a fixed set of variables.
  Definition 3.19 (Renaming). Let 𝜅 : Var → Var and 𝜄 : BId → BId be two bijective functions.
Then we call 𝜅 a variable renaming, 𝜄 a borrow renaming, and (𝜅, 𝜄) a renaming. Variable renamings
𝜅 are lifted to places in the natural manner:
                                      
                                      
                                      𝜅 (x)                     if 𝑝 = x
                                      
                                      
                               𝜅 (𝑝) = 𝜅 (𝑝 ′ ) [𝑛]              if 𝑝 = 𝑝 ′ [𝑛]
                                      
                                      𝜅 (𝑝 ′ ).identifier
                                      
                                                                 if 𝑝 = 𝑝 ′ .identifier
                                      
A renaming (𝜅, 𝜄) can be applied on a reference value with the function “rnm” as follows:
                                       rnm(𝜅, 𝜄, Ref 𝑠𝑝 (𝑏)) = Ref 𝜅𝑠 (𝑝 ) (𝜄 (𝑏))
                                      rnm(𝜅, 𝜄, Ref 𝑚              𝑚
                                                    𝑝 (𝑏)) = Ref 𝜅 (𝑝 ) (𝜄 (𝑏))

The “rnm” function is extended to values in the usual manner; every reference contained in a value
is renamed as above.

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:21


   Definition 3.20 (State Equality Modulo Renaming). We define a relation ≃𝑉 over LAGC states
and a set of variables 𝑉 ⊆ Var. Two states 𝜎1, 𝜎2 are equal modulo renaming relative to 𝑉 —written
as 𝜎1 ≃𝑉 𝜎2 —iff dom(𝜎1 ) ∩ 𝑉 = dom(𝜎2 ) ∩ 𝑉 , 𝜎1 (x) = 𝜎2 (x) for all x ∈ dom(𝜎1 ) ∩ 𝑉 , and there
exists a renaming (𝜅, 𝜄) such that 𝜎1 (x) = rnm(𝜅 −1, 𝜄 −1, 𝜎2 (𝜅 (x))) for all x ∈ dom(𝜎1 ) \ 𝑉 and
𝜎2 (x) = rnm(𝜅, 𝜄, 𝜎1 (𝜅 −1 (x))) for all x ∈ dom(𝜎2 ) \ 𝑉 .
   Proposition 3.21. For every set 𝑉 ⊆ Var, the relation ≃𝑉 over LAGC states is an equivalence
relation.
    Definition 3.22 extends this notion to traces in the natural way.
   Definition 3.22 (Trace Equality Modulo Renaming). We extend the relation ≃𝑉 over concrete traces
for the set 𝑉 ⊆ Var with the following inductive definition:
    • 𝜀 ≃𝑉 𝜀,
    • sh1 ↷ 𝜎1 ≃𝑉 sh2 ↷ 𝜎2 iff sh1 ≃𝑉 sh2 and 𝜎1 ≃𝑉 𝜎2 ,
    • sh1 ↷ ev1 (𝑣 1 ) ≃𝑉 sh2 ↷ ev2 (𝑣 2 ) iff sh1 ≃𝑉 sh2 and ev1 (𝑣 1 ) = ev2 (𝑣 2 ).
We again pronounce it as equality modulo renaming relative to 𝑉 .
    Lemma 3.23 can now define the determinism of our Rust fragment in terms of generates traces.
    Lemma 3.23. For each LAGC state 𝜎 and each expression 𝑒, the following propositions hold:
                                                                   Tr(𝑒, 𝜎)/≃dom(𝜎 ) = 1                       (53)
                      (∀sh ∈ Tr(𝑒, 𝜎). sh is finite) ∨ (∀sh ∈ Tr(𝑒, 𝜎). sh is infinite)                        (54)
                            ∀sh ∈ Tr(𝑒, 𝜎). sh is finite → dom(𝜎) = dom(last(sh))                              (55)
Equation (53) states that all traces generated for 𝑒 starting in 𝜎 are equal modulo renaming relative to
the variables defined in 𝜎. As a direct consequence, equation (54) states that either all generated traces
are finite or all are infinite. Similarly, equation (55) states that for all generated traces, the first and
final state (if one exists) share their domain. Together, equations (53) to (55) give us the fact that either
all generated traces are infinite or they share the final state.

4     Asynchronous Rust Semantics
LAGC is suitable for asynchronous and parallel code. Here, we present a semantics for asynchronous
constructs in Rust and their use in a concurrent, but not parallel, setting with the most permissive
scheduler possible. Section 5 shows how these definitions can be used to model a realistic async
runtime: Tokio, Rust’s most widely-used async runtime.

4.1    Background: Async Rust
Rust’s use of async, await, and futures seems to be similar to other programming languages such
as JavaScript and active object languages like ABS [35] but it differs in crucial respects.
   Asynchronous Rust revolves around the declaration and use of futures, i.e., representations of
computations that have yet to be completed. Unlike other languages, Rust does not provide a single
type for futures, but instead defines a trait, Future, which can be implemented for many types.
   A simplified definition of the Future trait can be seen in Listing 2. It requires an implementor
to define the output type which the future is to compute and a poll method, which returns the
Poll enum. This type is either Pending or Ready(Output), the latter containing the computed value.
Calling poll on a future runs the future until its next suspension point. Such a point may either
be the end of the function body or another await expression. In the former case, the function
returns Ready with the return value and is finished. In the latter case, we say the future yields (or
“suspends”) and returns Pending.

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:22                                                                                                            Daniel Drodt


                               Listing 2. A simplified definition of Rust’s Future trait.
trait Future {
  type Output;
  fn poll(self) −> Poll<Self::Output>;
}
    Hence, a Rust future is a state machine that advances from the initial state to its next yield and
after a number of calls may reach its final state and return a value. How the future exactly progresses
and when and how it computes its final value is left up to the implementation. Rust merely defines
the basic operations and defines suitable abstractions on top of them. Rust futures are passive, that
is, they are not automatically scheduled and need to be actively polled to be (partially) executed. On
top of these asynchronous primitives, libraries can provide async runtimes, which allow scheduling
of futures and can make these scheduled futures behave like “active” futures, as we discuss below.
    With an expression f.await, where f is a future, a future is repeatedly polled until it is completed.
If the awaited future is still pending, the await expression also suspends. Hence, await provides
a suitable abstraction over polling of futures. However, the await expression is only allowed in
functions declared with the async keyword, as in Listing 3. Assume that the async function “get”
returns the HTML of a URL as a String. Calling “get(url),” hence, returns a future with output type
String. In other languages, the created future would automatically be scheduled. In Rust, however,
this is not the case; the future remains passive.

                                     Listing 3. An example async function in Rust.
async fn check(url: &str) −> bool {
  let f1 = get(url); let f2 = get(url);
  let x = f1.await; let y = f2.await;
  return x.len() == y.len();
}
   Functions marked with async are only syntactic sugar. An asynchronous function like check is
actually transformed into a regular function that returns something that implements Rust’s Future
trait. The signature of the function then looks as follows
                            fn check(url: &str) −> impl Future<Output=bool> { ... }
   Hence, when the future of function “check” polls “get” and the latter’s future is still pending,
“check”’s future also returns Pending. Awaiting futures is the only way to suspend a future.2
   With futures as the basic building blocks in place, a number of different schedulers and ab-
stractions can be built. Rather than provide a single runtime for asynchronous programs, Rust
leaves runtimes up to libraries and developers. A variety of runtimes have been developed with
different features and specializations: Glommio [23] is specialized for I/O operations and is based
on Linux’s io_uring; smol [60] is a small, simple runtime with little overhead. By far the most
prevalent runtime library is Tokio [64].
   With a runtime set up, futures can be handed to the runtime to be scheduled; typically, this
happens by calling the runtime’s “spawn” function. It is the runtime’s responsibility to keep track of
these futures and calling poll on scheduled futures to advance them. These “spawned” or “scheduled”
futures then are active futures and behave differently. They may be executed whenever the runtime
deems fit, even in parallel to other futures. Hence, scheduled futures behave more analogously to

2 Technically, there are other possibilities for suspension, e.g., locks, but we leave these aside for brevity.



ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
    A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:23


    futures in active object languages [10]. Such spawned futures are often called “handles” (JoinHandle
    in Tokio’s lingo).
       Any non-scheduled future, even when created by a scheduled future, behaves passively, as
    described above: They only progress when polled and this polling may suspend the scheduled
    future. We call these non-scheduled futures “local.”
       A Rust developer is unlikely to use the Future trait directly and is typically guided by Rust’s
    design and the existing libraries to use async functions and await expressions as the principal
    elements. Therefore, our semantics abstracts away from poll calls and instead focuses on awaiting
    local (or unscheduled) and scheduled futures. This is not due to a fundamental restriction of the
    approach. Modeling such lower-level steps leads to a somewhat more verbose semantics and may
    be justified in other contexts. Focusing on await is an important design decision and potential
    limitation but we believe it to be a sensible abstraction for a high-level semantics, which allows us
    to achieve the results laid out in the following sections.
      Example 4.1 (Running Example). In this section, we demonstrate our semantics with running
    examples based on Listing 4. It consists of two asynchronous functions, two_power and bar, both
    taking one parameter of type u32 and returning a value of the same type. The former function
    recursively computes 𝑛 ↦→ 2𝑛 for 𝑛 ∈ N, the latter computes 𝑚 ↦→ 2𝑚+1 for 𝑚 ∈ N, using two_power.
    The main function schedules futures of both functions and awaits them later on, while the functions
    two_power and bar create and await only local futures.

           Listing 4. An asynchronous program.            8    async fn bar(m: u32) −> u32 {
1   async fn two_power(n: u32) −> u32 {                   9      return two_power(m).await ∗ 2; ()
2     return if n == 0 {                                 10    }
3       1                                                11    fn main() {
4     } else {                                           12      let f1 = spawn(two_power(1));
5       2 ∗ two_power(n − 1).await                       13      let f2 = spawn(bar(2));
6     }; ()                                              14      let x = f1.await + f2.await;
7   }                                                    15      return (); ()
                                                         16    }

       Observe that the main function here is only used for ease of presentation: In truth, it must set
    up the runtime and does not have access to await, as it is not declared as async. But the pattern is
    not uncommon. See how Tokio, for instance, sets up the tokio::main macro to achieve the same
    effect [65].

    4.2   Local Evaluation
    We extend the values as defined in Definition 2.1 with future identifiers FId ⊂ Val, standing
    for created futures. The syntax of Fig. 1 is extended with additional syntactic structures: await
    expressions like 𝑒.await and asynchronous functions declared as async fn foo(x1, . . . , x𝑛 ) 𝑒, where
    x1, . . . , x𝑛 are the parameters and 𝑒 the function body. From this point on, the evaluation function
    is tagged with a future identifier 𝐹 ∈ FId: val𝜎𝐹 , which denotes the currently active future.
       Evaluating a call to async function foo adds a future creation event createEv(foo, F′, 𝑣), denoting
    that a future of foo is called with parameters 𝑣. F′ is a fresh, symbolic variable standing for the created
    future. The symbolic variable will be concretized with a concrete future ID during composition.
                 val𝜎𝐹 (foo(𝑣)) = {⟨𝜎⟩ ↷ createEv(foo, F′, 𝑣) ↷ 𝜎 [F′ ↦→ ∗] · K(F′ ) | F′ fresh}                   (56)


                      ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:24                                                                                               Daniel Drodt


  Example 4.2. Calling two_power in line 12 of Listing 4, creates a future. The evaluation is
   𝑓
val𝜎00 (two_power(1)){⟨𝜎0 ⟩ ↷ createEv(two_power, F, 1) ↷ 𝜎0 [F ↦→ ∗] · K(F) | F fresh}, assuming
we are in some state 𝜎0 and the current future is 𝑓0 .
   A future is scheduled, or spawned, with the spawn function. We mark this with a spawn event
containing the future’s identifier and the symbolic variable H, standing for a handle identifier. The
latter is needed, as we formally differentiate between local futures and handles, i.e., wrappers
around futures which represent the tasks. The set of all handle identifiers is called HId ⊂ FId.
               val𝜎𝐹 (spawn(𝑣)) = {⟨𝜎⟩ ↷ spawnEv(𝑣, H) ↷ 𝜎 [H ↦→ ∗] · K(H) | H fresh}                       (57)
  Example 4.3. The futures created in the main function in Listing 4 are spawned. If we assume
that the future created in Example 4.2 is concretized to future 𝑓𝑡 and the future of bar is 𝑓𝑏 , we have
the spawn events spawnEv(𝑓𝑡 , ℎ𝑡 ) and spawnEv(𝑓𝑏 , ℎ𝑏 ) for some fresh handle identifiers ℎ𝑡 and ℎ𝑏 .
   Evaluating an async function emits an evaluation event with the function’s name, the currently
executing future and fresh symbolic variables X for the call arguments. Then, the function’s body
is evaluated with parameters x substituted with X, just as in rule (34).
  val𝜎𝐹 (async fn foo(x) 𝑒) = {⟨𝜎⟩ ↷ evalEv(foo, 𝐹, X) ↷ 𝜎 [X ↦→ ∗] · K(𝑒 [x ← X]) | X fresh} (58)
  Example 4.4. If we evaluate function bar of Listing 4 in state 𝜎2 and future ℎ𝑏 , we have the traces
{⟨𝜎2 ⟩ ↷ evalEv(bar, ℎ𝑏 , X) ↷ 𝜎2 [X ↦→ ∗] · K({return two_power(X).await * 2;}) | X fresh}.
  A return expression now emits a computation event with the active future and the returned
value. We replace rule (35) with the following:
                           val𝜎𝐹 (return 𝑣) = {⟨𝜎⟩ ↷ compEv(𝐹, 𝑣) ↷ 𝜎 · K(())}                              (59)
   Awaiting a local future emits a local await event localAwEv(𝑣), where 𝑣 ∈ FId is the awaited
future. Since this event starts computation of the function represented by 𝑣, we model it similarly
to a local synchronous call (rule (32)) and leave a “get expression” for the awaited future. This
expression can now be applied to call identifiers or local futures. However, if 𝑣 is a handle identifier,
i.e., refers to a spawned future, we directly emit a computation reaction event with a symbolic result
value. The well-formedness predicate ensures that an await on a spawned future is only executed
once this future is completed.
                     (
        𝐹              {⟨𝜎⟩ ↷ localAwEv(𝑣) ↷ 𝜎 · K(?𝑣)}                          if 𝑣 ∈ FId \ HId
   val𝜎 (𝑣.await) =                                                                                 (60)
                       {⟨𝜎⟩ ↷ compREv(𝑣, V) ↷ 𝜎 [V ↦→ ∗] · K(V) | V fresh} if 𝑣 ∈ HId
   Example 4.5. The futures created by the calls in Listing 4, lines 5 and 9 are local futures, which
are not spawned; hence, their await expressions in those same lines “end up” in the first case of
rule (60). On the other hand, the awaits in line 14 are handled by rule (60)’s second case, as the
futures were spawned and are thus handle identifiers.

4.3    Well-Formedness
We adjust the well-formedness predicate as follows: A trace ending in a creation event is well-
formed if the preceding trace is well-formed and does not contain a creation event with the same
future identifier. The create event cannot create a handle, as those must be created via spawning.
      wf (sh ↷ createEv(foo, 𝑓 , 𝑣)) = wf (sh) ∧ 𝑓 ∉ HId ∧ foo′, 𝑣 ′ . createEv(foo′, 𝑓 , 𝑣 ′ ) ∈ sh       (61)
  Spawn events must follow a creation event of the spawned future and this future must not have
been spawned or locally awaited already. The created handle identifier must also be unique. A

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:25


future can either be local or spawned, never both. Hence, no future can have both a local await and
a spawn event in the same trace.
  wf (sh ↷ spawnEv(𝑓 , ℎ)) = wf (sh) ∧ ∃foo, 𝑣 . createEv(foo, 𝑓 , 𝑣) ∈ sh ∧ localAwEv(𝑓 ) ∉ sh
                                                                                                               (62)
                                   ∧ ℎ ′ . spawnEv(𝑓 , ℎ ′ ) ∈ sh ∧ 𝑓 ′ . spawnEv(𝑓 ′, ℎ) ∈ sh
  Local await events are only valid if the future has already been created but not awaited or
spawned before:
           wf (sh ↷ localAwEv(𝑓 )) = wf (sh) ∧ 𝑓 ∉ HId ∧ ∃foo, 𝑣. createEv(foo, 𝑓 , 𝑣) ∈ sh
                                            ∧ localAwEv(𝑓 ) ∉ sh ∧ ℎ. spawnEv(𝑓 , ℎ) ∈ sh
    An evaluation event can only occur once per future. Additionally, it must follow a local await
event or a spawn event. If the future 𝑓 is local, it must have been created before being evaluated
and the function name and parameter must match, ensuring a pairing between call and execution.
If the future is a spawned future, it must have been spawned from a future 𝑓 ′ that was created with
the correct function name and arguments.
wf (sh ↷ evalEv(foo, 𝑓 , 𝑣)) = wf (sh) ∧ foo′, 𝑣 ′ . evalEv(foo′, 𝑓 , 𝑣 ′ ) ∈ sh
                                   ∧ (localAwEv(𝑓 ) ∈ sh ∧ createEv(foo, 𝑓 , 𝑣) ∈ sh
                                   ∨ 𝑓 ∈ HId ∧ ∃𝑓 ′ . spawnEv(𝑓 ′, 𝑓 ) ∈ sh ∧ createEv(foo, 𝑓 ′, 𝑣) ∈ sh)
                                                                                                     (63)
   We place no restrictions on computation events, as we can only reach a return after evaluating
a function, which would already have taken care of the necessary events. Computation reaction
events must follow a corresponding computation event, which leads to a case distinction: If the
event is over a future, it must follow a computation event of that future. If, however, the event is
over a call identifier, it was a synchronous call and, hence, the future in the computation event
is the future in which the function was called; the computation reaction event must also directly
succeed the computation event. There can be at most one computation reaction event per identifier.
In the following, we use fi ∈ CId ⊎ FId for a future or call identifier.
                 wf (sh ↷ compEv(𝑓 , 𝑣)) = wf (sh)
                wf (sh ↷ compREv(fi, 𝑣)) = wf (sh) ∧ 𝑣 ′ . compREv(fi, 𝑣 ′ ) ∈ sh
                                           ∧ (fi ∈ FId → compEv(fi, 𝑣) ∈ sh)
                                           ∧ (fi ∈ CId → lastEv(sh) = compEv(fi, 𝑣))

4.4   Trace Composition Rules
We define trace composition rules for async Rust that generate all possible schedules of futures or
“tasks.” They are defined over configurations consisting of a bag of tasks 𝑄. A task, thus, consists of
a stack of continuation markers as in Section 3.3 with two differences: (a) the continuation markers
are tagged with future identifiers, e.g., K 𝑓0 (x + y), and (b) the elements of the stack represent
both called functions and locally evaluated, unscheduled futures. A configuration is written as
sh, (active, 𝑄), where sh is the current shining trace, active is the active task, i.e., the task currently
being executed, or Idle if there is none, and 𝑄 is the current bag of tasks. This representation ensures
that an active task is not prematurely preempted.
   The first rule executes the top continuation marker of the active task if possible. It pops the
first continuation of the stack, takes one step of the local evaluation, extends the trace by the
concretization of the result if it is well-formed, and pushes the new continuation onto the stack.
This rule corresponds to rule (50) extended with a bag of stacks. We highlight which parts of the

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:26                                                                                               Daniel Drodt


rules are changed.

                                  𝜏 · K(𝑒 ′ ) ∈ val𝜎 (𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                                    𝑓
                 𝜎 = last(sh)
                                h           i                 h          i                              (64)
                             sh, K 𝑓 (𝑒), 𝑘 , 𝑄 → sh ∗∗ 𝜌 (𝜏), K 𝑓 (𝑒 ′ ), 𝑘 , 𝑄

   Example 4.6. We continue our running       Example 4.1. Assume we are in a configuration sh0 ↷
𝜎0, [Kℎ𝑡 ({return if n == 0 . . .})], 𝑄 0 with 𝜎0 (n) = 1. Then, we are executing function two_power
in the active task, 𝑄 0 must contain the task for main and, possibly, the task for bar on handle ℎ𝑏
(the latter may already be finished). With rule (64), we execute the body one step further to
sh0 ↷ 𝜎0, [Kℎ𝑡 ({return if 1 == 0 . . .})], 𝑄 0 . Clearly, this is the semantics we expect, behaving
similar to Section 3.3.
  Rule (65) extends the active task with a new call context, executing a locally called, synchronous
function, just as rule (51) does in the synchronous case. The rules are identical except for the
addition of 𝑄 and the tag 𝑓 .
                                  𝜎 = last(sh) 𝑓 ∈ FId fn foo(x) 𝑒 ∈ Fn
                    𝜏 · K(𝑒 ′ ) ∈ val𝜎 (fn foo(𝑥) 𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                     𝑓
                                                                                                            (65)
                                    h i                  h          i 
                                 sh, 𝑘 , 𝑄 → sh ∗∗ 𝜌 (𝜏), K 𝑓 (𝑒 ′ ), 𝑘 , 𝑄

   A locally awaited future is handled exactly the same as a synchronous in call rule (65), except
in this case, an active task exists and the new continuation is pushed on top. Rule (66) has no
corresponding rule in Section 3.3.
                           𝜎 = last(sh) 𝑓 ∈ FId \ HId async fn foo(𝑥) 𝑒 ∈ Fn
                𝜏 · K(𝑒 ′ ) ∈ val𝜎 (async fn foo(𝑥) 𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                 𝑓
                                                                                                            (66)
                                    h i                 h          i 
                                sh, 𝑘 , 𝑄 → sh ∗∗ 𝜌 (𝜏), K 𝑓 (𝑒 ′ ), 𝑘 , 𝑄

   Example 4.7. Rule (66) is used, for instance, for the recursive future in two_power: After the local
future is awaited, the rule becomes applicable, according to wf . Like a synchronous function call, the
stack is extended with the new future as top and takes the form [K 𝑓3 ({return if k == 0 . . .}), Kℎ𝑡 (?𝑓3 )].
   Similar to rule (52), we pop the top continuation of a stack, returning control to the calling
function. As before, we do not require 𝑒 to be a value. Rather, the structure of the continuation
stack and the well-formedness predicate ensures that 𝑒 ′ is a get expression, which can only be
executed once the called function, represented by K 𝑓 (𝑒), returns by the argument for rule (52).
                                                   𝑓′
                𝜎 = last(sh)    𝜏 · K(𝑒 ′′ ) ∈ val𝜎 (𝑒 ′ ) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                               h            ′
                                                      i        h ′           i                           (67)
                            sh, K 𝑓 (𝑒), K 𝑓 (𝑒 ′ ), 𝑘 , 𝑄 → sh, K 𝑓 (𝑒 ′′ ), 𝑘 , 𝑄

  Example 4.8. After the recursive future in Example 4.7 was pushed onto the stack and it was fully
evaluated as in Example 4.6, the return emitted a computation event. According to the wf predicate
the this event must follow, which can only be done by the ?𝑓3 expression in the continuation marker
below the top. Thus, only rule (67) is applicable and the stack is simplified to [Kℎ𝑡 (1)].
   If the stack is empty, we have no more active task and mark the configuration as idle.
                                           sh, ( [], 𝑄) → sh, (Idle, 𝑄)                                     (68)

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:27


  When the next sub-expression of an expression 𝑒 is an await on a scheduled future that has no
corresponding computation event in trace sh, we call 𝑒 suspended in sh, written suspended(𝑒, sh).
We define this predicate as
      suspended(𝑒, sh) := ∃ℎ ∈ HId. next (𝑒, Val) = (ℎ.await, . . .) ∧ 𝑣 ∈ Val. compEv(ℎ, 𝑣) ∈ sh .
   If the top continuation marker of the active task contains a suspended expression, we no longer
have an active task and the suspended task is added to the bag of tasks. This models Rust’s behavior
of an await only yielding if the awaited future is not yet ready.
                                                    suspended(𝑒, sh)
                                  h           i                   nh          i o                          (69)
                            sh,        K 𝑓 (𝑒), 𝑘 , 𝑄 → sh, Idle, 𝑄 ⊎ K 𝑓 (𝑒), 𝑘
  A scheduled future can be executed if there is no active task. Then an arbitrary function is
taken, evaluated, and, if well-formed, appended to the trace. The well-formedness ensures that
only scheduled functions are executed. The configuration now has an active task with the new
continuation marker as its only element.
                              𝜎 = last(sh) 𝑓 ∈ HId async fn foo(𝑥) 𝑒 ∈ Fn
                𝜏 · K(𝑒 ′ ) ∈ val𝜎 (async fn foo(𝑥) 𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                 𝑓
                                                                                                               (70)
                                  sh, (Idle, 𝑄) → sh ∗∗ 𝜌 (𝜏), K 𝑓 (𝑒 ′ ) , 𝑄
                                                                         

  Example 4.9. Rule (70) may be applied to functions two_power and bar after futures of them are
spawned in lines 12 and 13, as soon as there is no active task. Observe how the well-formedness
predicate ensures that their identifiers are unique and that parameters match.
  Alternatively, if we are idle, we can pick a task from the bag 𝑄 and add it as the active task. The
chosen task is also removed from 𝑄.
                                           h           i
                                             K 𝑓 (𝑒), 𝑘 ∈ 𝑄
                                             h          i    nh         i o                     (71)
                         sh, (Idle, 𝑄) → sh, K 𝑓 (𝑒), 𝑘 , 𝑄 \ K 𝑓 (𝑒), 𝑘

4.5    Global Program Semantics
Let 𝑟 be a Rust program with main function fn main() 𝑒. We extend the global semantics of Section 3.4
to our present case:
  Definition 4.10 (Asynchronous Program Semantics). Let 𝑟 be a an asynchronous Rust program
with the main function fn main() 𝑒. Assume a maximal sequence of applications of rules (64) to (71)
                               h init i 
                          sh0, K 𝑓 (𝑒) , ∅ → sh1, (active1, 𝑄 1 ) → · · ·

with sh0 = ⟨𝜎0 ⟩, dom(𝜎0 ) = ∅ and 𝑓 init is the initial future identifier. If the sequence is finite, it has
the form                             h init i                 h i 
                                ⟨𝜎⟩, K 𝑓 (𝑒) , ∅ →∗ sh, 𝑘 , 𝑄
If the sequence is infinite, we define sh = lim𝑖→∞ sh𝑖 . We denote the set of all such possibly infinite
traces as Tr(𝑟 ).
   This semantics for asynchronous programs now gives meaning to programs with Rust’s async
features. It provides a highly non-deterministic scheduler that is maximally permissive: Any possible
scheduling of futures in a program 𝑟 is covered by the semantics and included in the set Tr(𝑟 ). The

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:28                                                                                               Daniel Drodt


well-formedness restrictions ensure that any trace in Tr(𝑟 ) is valid, i.e., it follows the existing Rust
semantics. While typically not desired from an actual runtime, it gives us a base to which we can
compare any real-world runtime, as they must produce a subset of the traces in Tr(𝑟 ).
  It remains to model the Tokio runtime and show that they produce fair schedules.

5     Showing the Fairness of Tokio’s Schedulers
A central property of any runtime (or scheduler) is its fairness: If a future is scheduled, a developer
wants guarantees that, under certain conditions, this future is eventually executed. In the case of
Rust’s Tokio runtime, its documentation gives informal fairness guarantees [65].
   We cover both the formalization of Tokio’s scheduling behavior in terms of composition rules
and a formalization of fairness guarantees, including those of the documentation. We also provide
a formal proof that these guarantees hold for one of Tokio’s runtimes.

5.1    Background: Tokio
The Tokio library provides two runtimes: the current thread runtime, which works on a single
thread; and the multi-threaded runtime, which provides concurrency and parallelism. Although
the implementations differ slightly, both runtimes are intended to work similarly, except for the
number of threads.
   The following description is derived partly from Tokio’s documentation [65] and partly from
analysis of Tokio’s code base [64].
   In both runtimes, each thread is associated with a worker, each of which has a local queue of
tasks and, potentially, an active task (similar to the notion of active task in Section 4.4). A task is a
future scheduled on the runtime. Each worker also has a tick, a counter that is increased whenever
a future is polled. Further, each runtime has a global queue of tasks. Additionally, the runtimes have
a parameter for the global queue interval, call it 𝐼𝐺 ∈ N, controlling the interval in which the global
queue is considered. This parameter cannot be changed while the runtime is active. To which queue
a scheduled task is appended depends on where it is scheduled and the queues’ current state. Tasks
can be scheduled either from a task executed by a worker or from outside the runtime, i.e., from
parts of the Rust program not controlled by the runtime. If the task is scheduled from outside the
runtime or the local queue is full, the task is pushed to the global queue. Otherwise, it is pushed
onto the corresponding local queue.
   Additionally, the runtimes track I/O timers and events. However, as I/O is more difficult to model,
we ignore this feature for now and only model futures.
5.1.1 The Current Thread Runtime. The current thread runtime must decide which task to execute
next if the worker is idle, i.e., if it has no active task: If the tick is divisible by 𝐼𝐺 or the local queue
is empty, remove the first task of the global queue and execute it. Otherwise, remove and execute
the first task of the local queue. Thus, tasks in the local queue are prioritized while the global queue
is only queried in periodic intervals.
5.1.2 The Multi-Threaded Runtime. The multi-threaded runtime not only has more workers but
also some optimizations and more complex scheduling. Each worker has a last in, first out (LIFO)
slot in addition to its queue. This slot contains the last locally scheduled task. The assumption is that
the most recently scheduled task is often more pressing. An idle worker considers the following
cases to choose its next task: (a) If the tick is divisible by 𝐼𝐺 and the global queue is not empty,
execute the first global task; (b) otherwise, if there is a task in the LIFO slot, execute it; (c) otherwise,
if the local queue is not empty, execute its first task; (d) otherwise, if the global queue is not empty,
take a fixed number of tasks from the global queue, execute the first task, and push the rest to the
back of the local queue; (e) otherwise, try to “steal,” i.e., take, another worker’s local tasks.

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                             ZZZ:29


  Case (a) ensures that tasks in the global queue are not ignored and checked in a fixed interval. If
a worker is idle, case (d) restores some balance by moving global tasks to the idle worker. Similarly,
case (e) balances the load between workers.
  Figure 3 shows the structure of both Tokio runtimes. We now model Tokio by extending our
LAGC semantics. The local evaluation rules defined in Section 4.4 are applicable to both runtimes;
only the trace composition and program semantics differ between the two runtimes.


                                                𝑞𝐺        ···

                         𝑤1                                         𝑤𝑛

                        𝑡1    act 1     lifo1                      𝑡𝑛    act𝑛     lifo𝑛
                                                           ···
                        𝑞1                      ···               𝑞𝑛                ···


Fig. 3. The general setup of Tokio’s runtimes. 𝑞𝐺 is the global queue of tasks. There are 𝑛 workers 𝑤𝑖 , each
with a tick 𝑡𝑖 , a local queue 𝑞𝑖 , a (potentially empty) active task act𝑖 , and a LIFO slot lifo𝑖 . Note that 𝑤 1 has
an active task but no task in its LIFO slot (denoted by the dotted border), whereas 𝑤𝑛 has a task in its LIFO
slot but no active task (dotted border). The current thread runtime has only one worker and no LIFO slot.



5.2   Local Evaluation
As we already defined spawning of tasks with the spawn function in Section 4, we reuse those
definitions to define Tokio’s scheduler. No additional local rules are required.

5.3   Well-Formedness
We adjust and extend the definition of the wf -predicate by adding a case for the new schedule event
schedEv(foo, 𝑓 ), where foo is an asynchronous function and 𝑓 ∈ FId is a future identifier. It denotes
that a task for function foo with future 𝑓 has been scheduled. This event must follow corresponding
spawn and create events. This ensures a coupling of creation, spawning, and scheduling. The above
requirements also ensure that evaluation is similarly associated.
 wf (sh ↷ schedEv(foo, 𝑓 )) = wf (sh) ∧ ∃ℎ ∈ HId. spawnEv(𝑓 , ℎ) ∈ sh
                                                                                                                 (72)
                                        ∧ ∃𝑣 . createEv(foo, 𝑓 , 𝑣) ∈ sh ∧ foo′ . schedEv(foo′, 𝑓 ) ∈ sh
   All other cases are unchanged from Section 4.3.

5.4   Modeling the Current Thread Runtime
We model Tokio’s current thread runtime via the trace composition rules below. The general
approach follows [24].
   We modify the configuration to be of the form sh, ⟨active, 𝑡, 𝑞𝐺 , 𝑞⟩, where sh is the current trace,
active is the currently active continuation stack or Idle if the scheduler is idle, 𝑡 is the tick, 𝑞𝐺 is the
global queue, and 𝑞 is the local queue. See Appendix B for an axiomatization of queues. The rules
below model the relation →ct to differentiate it from other possible schedules.
   To ensure a deterministic scheduling, which allows us to show fairness, and to accurately model
the current thread runtime, we require many composition rules. Figure 4 shows the decision tree
of the current thread runtime.

                   ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:30                                                                                                         Daniel Drodt


                                                      eval (74)
                                                        call (75)
                                                         local await (76)
                                  𝐶 ≠ ⟨Idle, . . .⟩
                                                         pop (77)
                                                        empty (78)
                                                  suspend (79)                        h i
                 lastEv(sh) ≠ spawnEv                                 pop (𝑞𝐺 ) = 𝑞𝐺′ , 𝑘 (80)
                                                 𝑡 ≡ 0 mod 𝐼𝐺
                                                                     pop (𝑞𝐺 ) = (𝑞𝐺′ , (foo, 𝑓 )) (81)
         sh, 𝐶                                                                                      h i
                                  𝐶 = ⟨Idle, . . .⟩                             pop (𝑞𝐺 ) = 𝑞𝐺′ , 𝑘 (82)
           lastEv(sh) = spawnEv (73)                              empty (𝑞)
                                                                                pop (𝑞𝐺 ) = (𝑞𝐺′ , (foo, 𝑓 )) (89)
                                                 𝑡 . 0 mod 𝐼𝐺                                h i
                                                                                   pop (𝑞) = 𝑞 ′, 𝑘 (83)
                                                                  ¬empty (𝑞)
                                                                                   pop (𝑞) = (𝑞 ′, (foo, 𝑓 )) (90)

                    Fig. 4. The current thread scheduler’s rule structure. Read left to right.


   If the last event was a spawn event, rule (73) appends a schedule event to the trace and, if the
result is well-formed, adds a task marker (foo, 𝑓 ) to the end of the local queue.3 The well-formedness
requirements above ensure that the schedule event contains the correct function name. We only
add this event to ensure that afterwards no spawn event is the last event, guaranteeing that rule (73)
is applied at most once per scheduled future. Observe that the function foo is coupled with the
future 𝑓 via the create event in equation (72). We write 𝑞 ⊕ 𝑘 for the result of enqueuing 𝑘 to 𝑞.
                            lastEv(sh) = spawnEv(𝑓 , ℎ) async fn foo(𝑥) 𝑒 ∈ Fn
                              sh′ = sh ↷ schedEv(foo, 𝑓 ) ↷ last(sh) wf (sh′ )                                        (73)
                           sh, ⟨active, 𝑡, 𝑞𝐺 , 𝑞⟩ →ct sh′, ⟨active, 𝑡, 𝑞𝐺 , 𝑞 ⊕ (foo, 𝑓 )⟩
   Example 5.1. We demonstrate
                                     the
                                       scheduling rules using Listing 4 (p. 23). The scheduler starts in
configuration ⟨𝜎0 ⟩, K 𝑓init (𝑒 main ) , 0, queue(), queue() , where dom(𝜎0 ) = ∅ and 𝑒 main is the main
function’s body.
   Assume the body has been executed so that the spawn call in line 12 was just evaluated, emitting
a spawn event. Then, rule (73) is the next rule to be applied and we arrive at the configuration
                   ⟨𝜎0 ⟩ ↷ · · · ↷ 𝜎1 ↷ schedEv(two_power, 𝑓0 ) ↷ 𝜎1,
                      𝑓                          
                      K init ({let f1 = H; . . .}) , 0, queue(), queue() ⊕ (two_power, 𝑓0 )
   We continue by presenting the rules that are analogous to the rules in Section 4.4, namely
the rules where there is an active task which is to be executed, possibly causing function calls
or awaiting local futures. Since an active task exists, active is a stack of continuation markers.
Because the rules are so similar, we highlight which elements of the rule have changed compared
to Section 4.4.
   If the top continuation marker in the stack contains a non-value expression—which is equivalent
to its local evaluation yielding a non-empty set—we evaluate the expression one step, add the
3 For brevity, we only model scheduling tasks from an active worker.



ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:31


resulting trace to the configuration, and replace the stack’s top element with the new continuation
marker. Rule (74) adapts rule (64).
                 𝑓 , ℎ. lastEv(sh) = spawnEv(𝑓 , ℎ) 𝑓 . lastEv(sh) = localAwEv(𝑓 )
                 𝜎 = last(sh) 𝜏 · K(𝑒 ′ ) ∈ val𝜎 (𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                                 𝑓
                                                                                                               (74)
                         Dh        i           E                Dh            i            E
                     sh, K 𝑓 (𝑒), 𝑘 , 𝑡, 𝑞𝐺 , 𝑞 →ct sh ∗∗ 𝜌 (𝜏), K 𝑓 (𝑒 ′ ), 𝑘 , 𝑡, 𝑞𝐺 , 𝑞
  If the last event was an invocation event, we evaluate the called function and push it onto the
active task as in Sections 3.3 and 4.4. We adapt rule (65) to obtain rule (75). Because the last event is
an invocation event, it cannot be a spawn event; hence, we need no explicit condition as in the
previous rules.
                     lastEv(sh) = invEv(foo, . . .) 𝜎 = last(sh) fn foo(𝑥 𝑒) ∈ Fn
                         𝜏 · K(𝑒 ′ ) ∈ val𝜎 (𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                          𝑓
                                                                                                               (75)
                             Dh i           E               Dh           i            E
                         sh, 𝑘 , 𝑡, 𝑞𝐺 , 𝑞 →ct sh ∗∗ 𝜌 (𝜏), K 𝑓 (𝑒 ′ ), 𝑘 , 𝑡, 𝑞𝐺 , 𝑞
  If the last event was a local await event, we evaluate the corresponding function and push it
onto the active task. Hence, we model awaiting on local futures within the same task similar to
function calls in the synchronous case. Rule (76) is an adaptation of rule (66).
                  lastEv(sh) = localAwEv(𝑓 ) 𝜎 = last(sh) async fn foo(𝑥 𝑒) ∈ Fn
                        𝜏 · K(𝑒 ′ ) ∈ val𝜎 (𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                         𝑓
                                                                                                               (76)
                            Dh i           E               Dh           i            E
                        sh, 𝑘 , 𝑡, 𝑞𝐺 , 𝑞 →ct sh ∗∗ 𝜌 (𝜏), K 𝑓 (𝑒 ′ ), 𝑘 , 𝑡, 𝑞𝐺 , 𝑞

  Example 5.2. We continue with the running example. The local await in line 9 pushes a new
continuation marker for function two_power on the active stack:
                  D                                                            h init    iE
              sh1, K 𝑓1 (. . . 𝑓2 .await * 2. . .) , 𝑡 1, queue(), queue() ⊕ K 𝑓 (. . .)
                  D                                                               h init       iE
           → sh2, K 𝑓2 (. . .), K 𝑓1 (. . . ?𝑓2 * 2 . . .) , 𝑡 1, queue(), queue() ⊕ K 𝑓 (. . .)
Note that the timer is not increased.
  Rule (77), an adaptation of rule (67), removes the top continuation marker of the active task if
possible, as this implies that we awaited a local future, which is now fully evaluated, or we fully
evaluated a synchronous call.
                           𝑓 , ℎ. lastEv(sh) = spawnEv(𝑓 , ℎ) 𝜎 = last(sh)
                                         𝑓′
                       𝜏 · K(𝑒 ′′ ) ∈ val𝜎 (𝑒 ′ ) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                                                                                               (77)
                       Dh             ′
                                              i           E       Dh ′           i            E
                    sh, K 𝑓 (𝑒), K 𝑓 (𝑒 ′ ), 𝑘 , 𝑡, 𝑞𝐺 , 𝑞 →ct sh, K 𝑓 (𝑒 ′′ ), 𝑘 , 𝑡, 𝑞𝐺 , 𝑞

   Example 5.3. Continuing Example 5.2, we find that rule (77) can be applied in the execution of
Listing 4 when the call to two_power from bar (line 9) is fully computed. Then, the top continuation
marker is popped off the stack.
  If the active continuation stack is empty, we remove it and make the scheduler idle. Rule (78)
adapts rule (68).
                                𝑓 , ℎ. lastEv(sh) = spawnEv(𝑓 , ℎ)
                                                                                            (78)
                               sh, ⟨[], 𝑡, 𝑞𝐺 , 𝑞⟩ →ct sh, ⟨Idle, 𝑡, 𝑞𝐺 , 𝑞⟩

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:32                                                                                               Daniel Drodt


   When the expression of the active task is suspended in sh, the the worker is made idle and the
stack is pushed to the end of the queue. Rule (79) follows rule (69).
                          𝑓 , ℎ. lastEv(sh) = spawnEv(𝑓 , ℎ) suspended(𝑒, sh)
                          Dh           i         E       D                 h           iE                   (79)
                       sh, K 𝑓 (𝑒), 𝑘 , 𝑡, 𝑞𝐺 , 𝑞 →ct sh, Idle, 𝑡, 𝑞𝐺 , 𝑞 ⊕ K 𝑓 (𝑒), 𝑘

Observe that if rule (79) is applicable, rule (74) cannot be applicable, as the resulting trace cannot
be well-formed if the computation event is missing.
   Example 5.4. We continue the running example by demonstrating suspension. After the initial
task has spawned its sub-tasks (lines 12 and 13) and reached the first await in line 14, it cannot
continue until the first task is resolved. Hence, the initial task is suspended and rule (79) is applicable:
                 D h init       i                                                        E
            sh3, K 𝑓 (. . .) , 𝑡 2, queue(), queue() ⊕ (two_power, 𝑓0 ) ⊕ (bar, 𝑓1 )
                 D                                                                h init      iE
          →sh4, Idle, 𝑡 2, queue(), queue() ⊕ (two_power, 𝑓0 ) ⊕ (bar, 𝑓1 ) ⊕ K 𝑓 (. . .)

   Now we model the case of the idle worker, following the descriptions in Section 5.1. If rule (73)
is not applicable, the tick is divisible by the global interval, the global queue is not empty (pop is
defined), and the configuration is idle, then rule (80) takes the first task of 𝑞𝐺 , advances the tick,
and changes the active task to the popped one.
                                                                                      h i
             𝑓 , ℎ. lastEv(sh) = spawnEv(𝑓 , ℎ) 𝑡 ≡ 0 mod 𝐼𝐺 pop (𝑞𝐺 ) = (𝑞𝐺′ , 𝑘 )
                                                           Dh i                E                   (80)
                              sh, ⟨Idle, 𝑡, 𝑞𝐺 , 𝑞⟩ →ct sh, 𝑘 , 𝑡 + 1, 𝑞𝐺′ , 𝑞
  An analogous rule is required for the case that the first task in 𝑞𝐺 is not a continuation marker
but a task marker: Rule (81) evaluates the function of the task marker one step, concretizes it, and
makes it the active task.
                             𝑓 , ℎ. lastEv(sh) = spawnEv(𝑓 , ℎ) 𝑡 ≡ 0 mod 𝐼𝐺
              pop (𝑞𝐺 ) = (𝑞𝐺′ , (foo, 𝑓 )) 𝜎 = last(sh) lookup(foo) = async fn foo(𝑥) e
                𝜏 · K(𝑒 ′ ) ∈ val𝜎 (async fn foo(𝑥) e) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                  𝑓                                                                         (81)

                         sh, ⟨Idle, 𝑡, 𝑞𝐺 , 𝑞⟩ →ct sh ∗∗ 𝜌 (𝜏), K 𝑓 (𝑒 ′ ) , 𝑡 + 1, 𝑞𝐺′ , 𝑞
                                                                         

  Rule (82) proceeds similarly in the case where the local queue is empty: The first global task is
taken and executed.
     𝑓 , ℎ. lastEv(sh) = spawnEv(𝑓 , ℎ)           𝑡 . 0 mod 𝐼𝐺 empty (𝑞) pop (𝑞𝐺 ) = (𝑞𝐺′ , [𝑘])
                                                            Dh i                E                           (82)
                               sh, ⟨Idle, 𝑡, 𝑞𝐺 , 𝑞⟩ →ct sh, 𝑘 , 𝑡 + 1, 𝑞𝐺′ , 𝑞

   Otherwise, the first local task is executed per rule (83).
                𝑓 , ℎ. lastEv(sh) = spawnEv(𝑓 , ℎ)        𝑡 . 0 mod 𝐼𝐺 pop (𝑞) = (𝑞 ′, [𝑘])
                                                             Dh i                 E                         (83)
                                sh, ⟨Idle, 𝑡, 𝑞𝐺 , 𝑞⟩ →ct sh, 𝑘 , 𝑡 + 1, 𝑞𝐺 , 𝑞 ′

 Analogous rules to rules (82) and (83), where the task from the queue is not a continuation
marker but a task marker, are defined as rules (89) and (90) in Appendix C.
  Example 5.5. We continue from Example 5.4: Assume the two tasks in Listing 4 have been
spawned (lines 12 and 13) but not yet started and the initial task is suspended while it waits for the

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                             ZZZ:33


spawned tasks. Then, the program is in an idle configuration and we can apply rule (90), yielding
the following transition:
                 D                                                              h init     iE
            sh5, Idle, 𝑡 3, queue(), queue() ⊕ (two_power, 𝑓0 ) ⊕ (bar, 𝑓1 ) ⊕ K 𝑓 (. . .)
                 D                                                  h init       iE
          →sh6, K 𝑓0 (𝑒 2 ) , 𝑡 3 + 1, queue(), queue() ⊕ (bar, 𝑓1 ) ⊕ K 𝑓 (. . .)
where 𝑒 2 is the expression left after evaluating the function body of two_power one step and sh2 is
the extension of sh1 with the resulting trace. Note that the time is incremented and the local queue
is shortened by one element. The cases for starting function bar and continuing the initial task are
similar, though the latter uses rule (83).
   The definition of the rules with their restrictive conditions ensures a deterministic scheduler.
  Proposition 5.6. Rules (73) to (83), (89) and (90) are mutually exclusive and model a deterministic,
well-defined scheduler.

5.5    Fairness
When we consider the fairness of the runtime defined above, the question arises, which definition
of fairness to examine. Strong fairness, i.e., every expression which is schedulable infinitely often
is executed as some point, is too strong for our case. As demonstrated by Hähnle and Henrio [24],
weak fairness, i.e., every expression which is always schedulable from some point onwards is
eventually executed, is inadequate for cooperative scheduling (e.g., Tokio) and is even inadequate
for the more straightforward case of ProMeLa [33]. This limitation is easy to see in the runtime
above: So long as we have an active task, the composition rules permit no other task to be scheduled,
even when it is “ready.” However, weak fairness guarantees only hold for a task that is continuously
schedulable. Thus, weak fairness offers no guarantees for the Tokio runtime at all.
   To remedy this limitation, quiescent fairness is introduced [24], which is more suitable to cooper-
ative settings. Intuitively, it states that if a task is continuously schedulable when there is no active
task, it will be scheduled at some future point. Hence, it is an adaption of weak fairness, as a task
need not be schedulable in every state but only on quiescent states, i.e., states with no active task.
   If we consider programs with no locally infinite computations, i.e., programs where at any point
in time, there will be a quiescent state in the future, we can formally state quiescent fairness
of the current thread scheduler. Theorem 5.7 assumes a function “trans,” translating a current
thread runtime configuration sh, ⟨act, 𝑡, 𝑞𝐺 , 𝑞⟩ into a configuration sh′, (act, 𝑄) as in Section 4.4.
See Appendix D for a formal treatment.
  Theorem 5.7 (Quiescent Fairness). Assume a program with no locally infinite computations.
Starting from an initial configuration, the current thread scheduler is quiescent fair: If
                                                    𝐶 0 →ct 𝐶 1 →ct 𝐶 2 →ct · · ·
then there is a quiescent fair execution
                                            init
                              ⟨𝜎0 ⟩, {K 𝑓          (𝑒)} →∗ trans(𝐶 1 ) →∗ trans(𝐶 2 ) → · · ·
producing the same trace (excluding schedEv events).
   With the LAGC approach presented in [24], Theorem 5.7 is straightforward (albeit tedious) to
prove; see Appendix D. However, the Tokio documentation, informally, claims a different notion of
fairness for both runtimes [64]: If, for a given Rust program 𝑟 ,4 there is some 𝑇max ∈ N such that at
any point the number of tasks in the runtime is less or equal 𝑇max and there is some 𝑃max ∈ N that
4 This addition is not explicit in the documentation but it is crucial to make the fairness usable.



                    ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:34                                                                                               Daniel Drodt


the evaluation of a poll call on a task in the scheduler finishes within 𝑃max time units, then there is
some 𝐷 max ∈ N such that a task is scheduled in 𝐷 max time units.
  Definition 5.8 makes us of the predicate quiescent(𝐶) over a configuration 𝐶, which holds iff 𝐶 has
no active task. The function newConts(𝐶, 𝐶 ′ ) returns a set of exactly those continuation markers
that are newly reachable after a step 𝐶 → 𝐶 ′ [24]. With function enabled(𝐶) we get all continuation
markers which are reachable from one step of 𝐶: enabled(𝐶) := {newConts(𝐶, 𝐶 ′ ) | 𝐶 → 𝐶 ′ }.
  Definition 5.8 (Tokio Fairness). Let 𝑟 be an asynchronous Rust program. Assume there are
𝑇max, 𝑃max ∈ N such that for all infinite sequences of LAGC rule applications 𝐶 0 → 𝐶 1 → · · ·
the following holds
                                           ∀𝑖. numTasks(𝑄𝑖 ) ≤ 𝑇max
                                                                                 nh i      h i   o
where 𝑄𝑖 is the set of task stacks in the configuration 𝐶𝑖 and numTasks(𝑄) = 𝑘 ∈ 𝑄 | 𝑘 ≠ [] .
Assume further that all local computations finish in 𝑃max time units. Then the infinite sequence of
rule applications 𝐶 0 → 𝐶 1 → · · · is Tokio fair if there is a 𝐷 max ∈ N such that
                                                                                      
         ∀𝑚, 𝑒, 𝑓 . ∀𝑛 ≥ 𝑚. quiescent(trans(𝐶𝑛 )) ⇒ K 𝑓 (𝑒) ∈ enabled(trans(𝐶𝑛 ))
             ⇒ ∃𝑛 ′ . 𝑚 < 𝑛 ′ ≤ 𝑚 + 𝐷 max ∧ K 𝑓 (𝑒) ∈ newConts(trans(𝐶𝑛′ ), trans(𝐶𝑛′ +1 ))
                                                                                            

  We can show that the current thread runtime is Tokio fair as a result of it being quiescent fair
(Theorem 5.9). In fact, we show that each quiescent fair scheduler where a scheduling distance
with a well-founded order can be defined (as we do in the fairness proof in Appendix D) is also
Tokio fair.
   Theorem 5.9. Assume an infinite sequences of LAGC rule applications 𝐶 0 →ct 𝐶 1 →ct · · · ,
                                                init
then there is a Tokio fair execution ⟨𝜎0 ⟩, {K 𝑓 (𝑒)} →∗ trans(𝐶 1 ) → · · · producing the same trace
(excluding schedEv events).
  Proof Sketch. Tokio fairness follows from quiescent fairness and the fact that we can construct
a 𝐷 max ∈ N from the distance function we used to proof quiescent fairness in Appendix D in
combination with 𝑇max and 𝑃 max . See Appendix E for a full proof.                             □

5.6   A Comment on the Multi-Thread Runtime
The present paper is focussed on the current thread runtime and we omit a formalization and
fairness proof of the multi-tread runtime. While the multi-thread runtime is more widely used, we
leave it for future work.
   Creating a formalization of the multi-thread runtime consists mainly in creation of new trace
composition rules; local evaluation and well-formedness can be left unaltered. Developing these
composition rules from the existing rules is a relatively straightforward process. The configuration
needs to be extended to support a fixed number of workers, each containing a local queue; the
global queue is left as is.
   We do not present these composition rules for two reasons. First, for space limitations. Second,
because in the multi-threaded runtime, idle workers may steal tasks from other workers to spread
the workload more evenly. This stealing procedure is only described conceptually, the concrete
algorithm for it is left oblique. Study of the complex code is a time consuming task.
   More adaption would be necessary to prove fairness of the multi-threaded runtime. Because
multiple workers execute in parallel, an additional counter atop the “local” counter in Appendix D
is required to ensure that the composition rules do not “starve” a worker. Additionally, parallelism
causes the scheduler to be non-deterministic, which complicates the fairness reasoning. It is possible
to overcome these hurdles, but space reasons do not permit an attempt in the present work.

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                                        ZZZ:35


6     Application: Soundness of a Dynamic Logic Calculus
One promising area of application for our semantics is the soundness of program logic calculi.
The development of program logics to provide semantics for a language and proof correctness of
programs go back to Hoare [31]. Since then, Pratt [53] introduced dynamic logic (DL), an extension
of first-order logic, where programs can appear in formulas, e.g., [x = x + 1;] (x > 0). DL is closed
under all logical operators. Hence, any Hoare triple {𝜙 }𝑃 {𝜓 }, where 𝑃 is a program and 𝜙,𝜓 are
formulas can be expressed in DL as 𝜙 → [𝑃]𝜓 . DL is also strictly more expressive than Hoare
logic [2]. DLs have proven especially helpful for program verification close to the source code level,
as there is a reduced mental and semantical gap between the program under verification and the
formulas. The DL developed for Java as part of the KeY verification system [1], JavaDL, has been
especially successful [5].
   As such program logic calculi are designed to be highly modular, i.e., typically have one rule
per language construct, a modular semantics is needed to show soundness. So far, the discrepancy
between calculus design and semantics design hindered or outright prevented soundness proofs
for program logic calculi.
   As no suitable semantics was defined, soundness of JavaDL’s calculus rules dealing with programs—
mainly its symbolic execution rules—could not be shown, even though it is “[t]he most important
property of the JavaDL calculus” [1]. Since real-world programming languages rarely have (official)
formal semantics and program semantics are typically difficult to relate to the semantics of a
logic, resolving this issue has been difficult. In this section, we show how the modular semantics
developed in Section 3 can be used for soundness proofs of a DL for Rust.
   In previous work [21, 22] we presented a DL called “RustyDL” and a calculus to verify Rust
programs. This calculus has been implemented in the KeY system. While RustyDL’s calculus rules
have been validated by using examples, any formal verification system needs a formal proof of
soundness. As most Rust verification tools rely on translations to other languages—e.g., Prusti [3]
translating to Viper [51]—correctness proofs of the tools rely on a semantics of both Rust and
the target language and the correct relation between the two. RustyDL on the other hand, can be
proven correct merely by showing that all its rules are sound.
   In this section we only consider the sequential subset of Rust discussed in Section 3. While DLs for
concurrent languages have been proposed [15, 17, 19], the non-determinicity of concurrent language
features significantly alters the semantics and calculus. Sections 6.1 and 6.2 largely recapitulate the
results of [21], with minor modifications for brevity and presentation, while Section 6.3 contains
our new contributions.
   RustyDL extends first-order logic with modalities containing Rust program fragments. Hence,
formula 𝜙 := x ≥ 0 → ⟨x += 1;⟩(x > 0) expresses that if x is greater than or equal to 0 in a state 𝑠
and the program “x += 1;” is executed in 𝑠, then it terminates in state 𝑠 ′ , in which x > 0 holds. We
prove such a formula valid, i.e., |= 𝜙, by deriving the sequent =⇒ 𝜙 in our sequent calculus.

6.1    Syntax and Semantics of RustyDL
The set of dynamic logic terms of sort 𝐴, called DLTrm𝐴 , is defined as for sorted FOL with an
additional base case: x ∈ DLTrm𝐴 for all x ∈ Var where x’s type maps to the sort 𝐴.5 Similarly, the
set of dynamic logic formulas DLFml is similar to FOL extended with ⟨𝑝⟩𝜙 (“diamond”) and [𝑝]𝜙
(“box”) where 𝑝 is a program fragment and 𝜙 ∈ DLFml. Note that DLFml is closed under all logical
operatives and nesting of modalities, e.g., ⟨𝑝 1 ⟩(𝜙 ∧ ⟨𝑝 2 ⟩𝜓 ) is a syntactically correct formula.

5 Note that the set Var is the set of program variables—called “ProgVSym” in [21]. It is distinct from the logical variables used

in quantifiers; quantifying over program variables is not permitted and neither is a logical variable occurring in a program.


                    ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:36                                                                                               Daniel Drodt


  To manage fine-grained state changes, we add the notion of updates (Definition 6.1) to express
uniform, total state changes in our logic. These updates may modify program variables or modify
memory locations borrowed by a mutable reference.
  Definition 6.1 (Update, Update Application). We define the set Upd inductively by:
  (1) (a := 𝑡) ∈ Upd for each program variable 𝑎 : 𝐴 and each term 𝑡 of sort 𝐴,
  (2) (𝑡 1 ∗→ 𝑡 2 ) ∈ Upd for each term 𝑡 1 of sort Ref 𝑚𝐴 and 𝑡 2 of sort 𝐴,
  (3) skip ∈ Upd,
  (4) (𝑢 1 ∥ 𝑢 2 ) ∈ Upd for all updates 𝑢 1, 𝑢 2 ∈ Upd,
  (5) ({𝑢 1 }𝑢 2 ) ∈ Upd for all updates 𝑢 1, 𝑢 2 ∈ Upd.
  We extend the inductive definition of terms with term {𝑢}𝑡 ∈ DLTrm𝐴 for all updates 𝑢 ∈ Upd
and terms 𝑡 ∈ DLTrm𝐴 . The inductive definition of formulas is extended with formula {𝑢}𝜙 for all
updates 𝑢 ∈ Upd and formulas 𝜙 ∈ DLFml. Update applications represent state changes to terms
and formulas syntactically and change the state in which a formula or term is evaluated.
   Example 6.2. Let a, b be program variables of type u64 and c of type &mut u64. Consider the
following examples of updates:
    • skip represents the effectless update.
    • An elementary update a := 2 · a expresses a state change where a’s value is doubled. Hence,
      {a := 2 · a}a is semantically equivalent to 2 · a.
    • A parallel update (a := b ∥ b := a) represents a state change where the values a and b are
      swapped. There is no interference between the updates in a parallel update. If there are
      multiple updates to the same program variable in one parallel update, only the last one affects
      the state.
    • The mutable update c ∗→ a + b stands for the state change where the variable borrowed by c
      is set to a + b. The value of c itself is unchanged.
   Example 6.3. Let x : int, y : int, z : Ref 𝑚
                                              int be program variables. Then the formula
                          {x := y ∥ y := x ∥ z ∗→ x + 1}⟨x = y + *z;⟩(x  2 · x + 1)
expresses that, in a state where the values of x and y are swapped and the value referenced by z is
updated to x plus one, the program fragment “x = y + *z;” terminates and afterwards the formula
x  2 · x + 1 holds. The formula is valid if the addition in the program does not overflow.
   Mutating updates allow our logic to represent mutable references. Just as in the semantics,
mutable references need to contain the borrowed memory location, i.e., the borrowed place. We
introduce the sort Place for places. For each program variable x, its place is represented with
the unique constant TxW : Place. With the function mref , mutable references of a place 𝑝 can be
represented as a term mref (𝑝). If 𝑝 is a place of a lender of sort 𝐴, then mref (𝑝) is of sort Ref 𝑚
                                                                                                    𝐴.
   Formally, we define the semantics of RustyDL using a Kripke structure consisting of states, i.e.,
first-order models, and a program transition function 𝜌.
   Definition 6.4 (RustyDL Kripke structure). Let 𝑟 be a valid Rust program. A RustyDL Kripke
structure for a signature derived from 𝑟 is a tuple
                                                K = (D, 𝐼, S, 𝜌)
where
   • D is the logic’s domain, i.e., a non-empty set. This domain can be split into different sub-
     domains per sort, e.g., D int for integers.
   • 𝐼 is the interpretation of functions and predicates.

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                              ZZZ:37


    • S is an infinite set of states 𝑠 : Var → D.
    • 𝜌 is a function mapping a program fragment 𝑝 to a partial function S ⇀ S with 𝜌 (𝑝) (𝑠 1 ) = 𝑠 2
      iff evaluating 𝑝 in state 𝑠 1 terminates normally in 𝑠 2 . If 𝑝 does not terminate normally starting
      in 𝑠 1 , then 𝜌 (𝑝) (𝑠 1 )↑. We assume Rust programs to be deterministic, which is true of the
      subset considered in Section 3.
   Whereas [21] left 𝜌 unspecified due to a lack of a formal semantics, we can now use the LAGC
semantics to close this gap. For this, we must clarify the relation between LAGC states 𝜎 and RustyDL
states 𝑠. We assume a relation ∼ between RustyDL states and LAGC states (see Definition F.3 for
a formal definition), pronounced “corresponds to,” in the expected manner: integer, boolean, and
compound values map to each other in the expected way; references, however, have no borrow
identifier on the RustyDL side, hence we obtain a many-to-one mapping.
  Proposition 6.5. Let K = (D, 𝐼, S, 𝜌) be RustyDL Kripke structure and 𝑠 ∈ S a RustyDL state.
There exist an infinite number of LAGC states 𝜎 such that 𝑠 ∼ 𝜎. All states in the set {𝜎 | 𝑠 ∼ 𝜎 } differ
only in the borrow identifiers in shared and mutable references.
   With this relation, we proceed to define 𝜌 in terms of the generated traces. A panic does not count
as normal termination and is therefore excluded from the program transition in Definition 6.6.
  Definition 6.6 (Program Transition Function). Let 𝑟 be a valid Rust program, K = (D, 𝐼, S, 𝜌) a
Kripke structure for 𝑟 , 𝑝 a program fragment for 𝑟 , 𝑠 ∈ S a RustyDL state, and 𝜎 an LAGC state
such that 𝑠 ∼ 𝜎. Then the program transition function 𝜌 is defined as
                  (
                   𝑠 ′ if ∃𝜎 ′ . 𝑠 ′ ∼ 𝜎 ′ ∧ ∃sh. (sh ↷ 𝜎 ′ ) ∈ Tr(𝑒, 𝜎) ∧ lastEv(sh) ≠ panicEv()
      𝜌 (𝑝) (𝑠) =
                    ↑ otherwise

where 𝑒 := {let x; 𝑝} and x := fpv(𝑝) are the free program variables in 𝑝. In the following, we write
K(𝑝) and Tr(𝑝, 𝜎) for K(𝑒) and Tr(𝑒, 𝜎), respectively.
  By Lemma 3.23, 𝜎 ′ is uniquely identified. Our definition for 𝑠 ∼ 𝜎 ensures that 𝑠 is uniquely
identified as well.
   We must also fix the semantics of updates, as they are a crucial part of the calculus rules.
   Definition 6.7 (Semantics of RustyDL updates). Let Crt be a crate, K = (D, 𝐼, S, 𝜌) a Kripke
structure for Crt, 𝑠, 𝑠 ′ ∈ S a state, a : 𝐴, b : 𝐵 ∈ Var program variables, 𝛽 : VSym → D a
variable assignment, 𝑢 1, 𝑢 2 ∈ Upd, 𝑡, 𝑡 2 ∈ DLTrm𝐴 , and 𝑡 1 ∈ DLTrmRef𝑚                   𝐵
                                                                                               . The valuation function
val K,𝑠,𝛽 : Upd → (S → S) is defined as:
                                                (
                                       ′          val K,𝑠,𝛽 (𝑡) if b = a
              val K,𝑠,𝛽 (a := 𝑡) (𝑠 ) (b) = ′
                                                 𝑠 (b)             otherwise
                                                (
                                                  val K,𝑠,𝛽 (𝑡 2 ) if val K,𝑠,𝛽 (𝑡 1 ) = val K,𝑠,𝛽 (mref (TbW))
            val K,𝑠,𝛽 (𝑡 1 ∗→ 𝑡 2 ) (𝑠 ′ ) (b) = ′
                                                 𝑠 (b)              otherwise
                  val K,𝑠,𝛽 (skip) (𝑠 ′ ) =𝑠 ′
                val K,𝑠,𝛽 (𝑢 1 ∥ 𝑢 2 ) (𝑠 ′ ) = val K,𝑠,𝛽 (𝑢 2 ) (val K,𝑠,𝛽 (𝑢 1 ) (𝑠 ′ ))
                     val K,𝑠,𝛽 ({𝑢 1 }𝑢 2 ) = val K,𝑠 ′ ,𝛽 (𝑢 2 ) where 𝑠 ′ = val K,𝑠,𝛽 (𝑢 1 ) (𝑠)
  With updates and program transition defined, the semantics of RustyDL terms and formulas is
now definable.

                   ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:38                                                                                                           Daniel Drodt


   Definition 6.8 (Semantics of RustyDL Terms and Formulas). Let Crt be a valid Rust crate, VSym the
set of logic variable symbols, K = (D, 𝐼, S, 𝜌) a Kripke structure modeling Rust programs, 𝑠 ∈ S a
state, and 𝛽 : VSym → D a variable assignment.
   For every RustyDL term 𝑡 we define its evaluation inductively by the evaluation function val K,𝑠,𝛽
exactly as in first-order logic, with evaluation of program variables defined as val K,𝑠,𝛽 (a) = 𝑠 (a)
for each program variable a and val K,𝑠,𝛽 ({𝑢}𝑡) = val K,𝑠 ′ ,𝛽 (𝑡) where 𝑠 ′ = val K,𝑠,𝛽 (𝑢) (𝑠).
   For every RustyDL formula 𝜙 we define satisfaction, denoted (K, 𝑠, 𝛽) |= 𝜙, exactly as in first-
order logic with three new cases:
      • (K, 𝑠, 𝛽) |= [𝑝]𝜙 iff 𝜌 (𝑝) (𝑠)↑ or 𝜌 (𝑝) (𝑠) = 𝑠 ′ and (K, 𝑠 ′, 𝛽) |= 𝜙,
      • (K, 𝑠, 𝛽) |= ⟨𝑝⟩𝜙 iff 𝜌 (𝑝) (𝑠) = 𝑠 ′ exists and (K, 𝑠 ′, 𝛽) |= 𝜙.
      • (K, 𝑠, 𝛽) |= {𝑢}𝜙 iff (K, 𝑠 ′, 𝛽) |= 𝜙 where 𝑠 ′ = val K,𝑠,𝛽 (𝑢) (𝑠).

6.2     Calculus Rules
To show the validity of RustyDL formulas, we rely on a sequent calculus over our logic, a standard
approach for verification and theorem proving.
   Beyond the familiar rules for propositional and first-order logic, as well as rules for reasoning
about, e.g., integer and boolean values, the calculus also contains a large number of symbolic
execution rules. These allow the unfolding and decomposition of complex expressions and statements
into simpler ones until the entire program has been executed and only first-order formulas remain.
   To represent the symbolic execution calculus in a compact and understandable manner, a further
extension of the Rust syntax is required. In program fragments in rules—and only there—we can
use 𝜋 and 𝜔 to represent the inactive prefix and the rest of the program, respectively. The inactive
prefix contains any opening braces and similar structures that represent the context; 𝜔 stands for
the rest of the program, including closing braces. Hence, the schematic program fragment 𝜋 x = 1 𝜔
matches any program fragment where x = 1 is the first active expression, e.g., {{x = 1; ()} x = 2}.6
   We present these rules in a schematic form with schema variables for different parts of the
sequent. In the rule ifElseSplit below, Γ, Δ stand for sets of DL formulas, 𝜙 for a DL formula, {U}
stands for any potential update application (it may also be empty; no update is necessary for the rule
to be applicable), se stands for a “simple expression,” i.e., a program variable or literal, {be0 }, {be1 }
stand for block expressions, and 𝜋 and 𝜔 stand for the inactive program prefix and the program
rest, respectively.

                                        Γ, {U}(se  TRUE) =⇒ {U}⟨𝜋 {be0 } 𝜔⟩𝜙, Δ
                                        Γ, {U}(se  FALSE) =⇒ {U}⟨𝜋 {be1 } 𝜔⟩𝜙, Δ
                         ifElseSplit
                                          Γ =⇒ {U}⟨𝜋 if se {be0 } else {be1 } 𝜔⟩𝜙, Δ
   The rule above splits the sequent when an if expression with a side-effect-free condition is
encountered into two branches: one where the condition is true and one where it is false.
   Crucial rules of our calculus simplify the program in modalities and extract singular effects into
updates. For instance, the following rule copy transforms an assignment, where the right-hand
side is a simple expression, into an update and leaves behind a unit expression.
                      Γ =⇒ {U}{x := se}⟨𝜋 () 𝜔⟩𝜙, Δ
              copy                                                   se is a literal or implements Copy
                         Γ =⇒ {U}⟨𝜋 x = se 𝜔⟩𝜙, Δ
   For details on RustyDL and more calculus rules, we refer to [21, 22].

6 The notion an active expression is related to the next sub-expression discussed in Section 3.1.1, but it is not identical.



ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:39


6.3   Showing Soundness
Following the standard definitions of the sequent calculus, we define the soundness of RustyDL
rules as follows:
  Definition 6.9 (Soundness of Rules). A RustyDL rule with 𝑛 premisses of form Γ𝑖 =⇒ Δ𝑖 (1 ≤ 𝑖 ≤ 𝑛)
and conclusion Γ =⇒ Δ is sound iff |= Γ =⇒ Δ under the assumption that |= Γ𝑖 =⇒ Δ𝑖 for all
1 ≤ 𝑖 ≤ 𝑛.
  From Definition 6.8, we conclude that only the final state of a trace is relevant for the RustyDL
semantics. Hence, when proving soundness of a rule with a modality, it suffices to show that two
sets of traces generated by two modalities agree on some suffix. For this purpose, Definition 6.10
defines the suffix relations of trace sets and Lemma 6.11 relates this to validity in RustyDL.
   Definition 6.10 (Trace Suffix). Let 𝑇1,𝑇2 be sets of traces. We call 𝑇1 the suffix set of 𝑇2 , denoted
as 𝑇1 ⋟ 𝑇2 , iff there is a finite shining trace sh such that 𝑇2 = {sh ∗∗ sh′ | sh′ ∈ 𝑇1 }. We call sh the
prefix.
  Lemma 6.11. Let K be a Rust Kripke structure, 𝛽 a variable assignment, 𝑠 1, 𝑠 2 RustyDL states, 𝜎1, 𝜎2
LAGC states with 𝑠 1 ∼ 𝜎1 and 𝑠 2 ∼ 𝜎2 , 𝜙 a RustyDL formula, and 𝑝 1 = 𝜋 𝑒 1 𝜔, 𝑝 2 = 𝜋 𝑒 2 𝜔 two
program fragments. If (K, 𝑠 2, 𝛽) |= ⟨𝑝 2 ⟩𝜙 and Tr(𝑝 2, 𝜎2 ) ⋟ Tr(𝑝 1, 𝜎1 ), then (K, 𝑠 1, 𝛽) |= ⟨𝑝 1 ⟩𝜙.
  Proof. We assume (K, 𝑠 2, 𝛽) |= ⟨𝑝 2 ⟩𝜙. By Definitions 6.6 and 6.8, we know that there is an
LAGC state 𝜎 and a state 𝑠 such that at least one trace in Tr(𝑝 2, 𝜎2 ) ends in 𝜎 and 𝑠 ∼ 𝜎 such that
(K, 𝑠, 𝛽) |= 𝜙. By Lemma 3.23, all traces in Tr(𝑝 2, 𝜎2 ) end in 𝜎.
  Since Tr(𝑝 2, 𝜎2 ) ⋟ Tr(𝑝 1, 𝜎1 ), we know that all traces in Tr(𝑝 1, 𝜎1 ) end in 𝜎. Thus, Definition 6.8
gives us (K, 𝑠 1, 𝛽) |= ⟨𝑝 1 ⟩𝜙.                                                                         □
  We can now begin proving our calculus rules sound.
  Theorem 6.12 (Soundness of rule copy). Let Γ, Δ ∈ 2DLFml be sets of formulas, U ∈ Upd be an
update, x be a program variable whose type is Copy, se be a variable or a literal expression, 𝜋 x = se 𝜔
be a program fragment, and 𝜙 ∈ DLFml be a formula. If
                                     |= Γ =⇒ {U}{x := se}⟨𝜋 () 𝜔⟩𝜙, Δ
then the following holds:
                                       |= Γ =⇒ {U}⟨𝜋 x = se 𝜔⟩𝜙, Δ.
  Proof. We assume |= Γ =⇒ {U}{x := se}⟨𝜋 () 𝜔⟩𝜙, Δ. It is sufficient to show
                                          (K, 𝑠 1, 𝛽) |= ⟨𝜋 x = se 𝜔⟩𝜙
for all K, 𝑠, 𝛽 with 𝑠 1 = val K,𝑠,𝛽 (U) (𝑠). We infer from the assumption that
                                            (K, 𝑠 2, 𝛽) |= ⟨𝜋 () 𝜔⟩𝜙                                           (84)
with 𝑠 2 = val K,𝑠1,𝛽 (x := se) (𝑠 1 ).
  Let 𝜎1, 𝜎2 be LAGC states such that 𝑠 1 ∼ 𝜎1 and 𝑠 2 ∼ 𝜎2 .
  We know that x = se is the active expression. By the construction of the local evaluation rules,
we know that it is also the next (sub-)expression to be evaluated and added to the trace sh using
rule (50). Thus we can use the local evaluation. We split over the construction of se. Since it is a
simple expression, it is either a value or a variable.
  Case 6.1 (se ∈ Val). Then val𝜎1 (x = se) = {⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ se] · K(())}. Hence the only possible
composition is, ⟨𝜎1 ⟩, K(𝜋 x = se 𝜔) → ⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ se], K(𝜋 () 𝜔). As 𝑠 2 = val K,𝑠1,𝛽 (x := se) (𝑠 1 ),
we know 𝜎2 = 𝜎1 [x ↦→ se].

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:40                                                                                               Daniel Drodt


  Thus, Tr(𝜋 x = se 𝜔, 𝜎1 ) = {⟨𝜎1 ⟩ · sh | sh ∈ Tr(𝜋 () 𝜔, 𝜎2 )}. Clearly, then, Tr(𝜋 () 𝜔, 𝜎2 ) ⋟
Tr(𝜋 x = se 𝜔, 𝜎1 ). By Lemma 6.11 and assumption (84), we have (K, 𝑠 1, 𝛽) |= ⟨𝜋 x = se 𝜔⟩𝜙.
   Case 6.2 (se ∈ Var). Let 𝑣 = 𝑠 1 (se). Since se is not symbolic (our semantics only generates
concrete traces with concrete states), 𝑣 ∈ Val. Then val𝜎1 (se) = {⟨𝜎1 ⟩ · K(𝑣)} and val𝜎1 (x = se) =
{𝜏 · K(x = 𝑒) | 𝜏 · K(𝑒) ∈ val𝜎1 (se)} = {⟨𝜎1 ⟩ · K(x = 𝑣)}.
   Further, we have val𝜎1 (x = 𝑣) = {⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ 𝑣] · K(())}.
   Hence, the only possible composition is
              ⟨𝜎1 ⟩, K(𝜋 x = se 𝜔) → ⟨𝜎1 ⟩, K(𝜋 x = 𝑣 𝜔) → ⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ 𝑣], K(𝜋 () 𝜔)
Since 𝑠 2 = val K,𝑠1,𝛽 (x := se) (𝑠 1 ), we know that 𝜎2 = 𝜎1 [x ↦→ 𝑣].
   Thus, we have Tr(𝜋 x = se 𝜔, 𝜎1 ) = {⟨𝜎1 ⟩ ↷ 𝜎2 · sh | sh ∈ Tr(𝜋 () 𝜔, 𝜎2 )} which, with Defini-
tion 6.6, assumption (84), and the argument in case 6.1, gives us (K, 𝑠 1, 𝛽) |= ⟨𝜋 x = se 𝜔⟩𝜙.  □
   The modularity of LAGC thus permits relatively concise and schematic soundness proofs. This
ease carries over even to more complex rules, as both the semantics and calculus are on a similar
level of modularity and there is, thus, a suitable correlation. We present proofs for additional rules
encountered in [21] in Appendix G. The rules presented and proven here and in Appendix G present
some of the core and most important rules of our calculus. Already, the rules support references
and loops. Given the schematic nature of the proofs, proving the remaining calculus rules presents
time consuming but straightforward work. These results lead us to postulate Theorem 6.13 with
considerable confidence.
    Theorem 6.13 (Soundness of RustyDL calculus). The calculus of RustyDL is sound.
  Thus, RustyDL is, to our knowledge, the first DL calculus for a real-world programming language,
where “[t]he most important property of the [. . .] calculus” [1] has been proven.

7     Related Work
For related work, we first consider other semantics and formalizations of parts of Rust and com-
pare them to LAGC in approach and scope. Then, we consider other applications of the LAGC
approach and how they differ from our Rust semantics. Finally, we comment on different LAGC-like
applications to deductive verification.

7.1    Rust Semantics
Multiple semantics for substantial parts of Rust have been defined in recent years, all with different
scopes, focal points, and drawbacks. We present a broad selection here.
   In contrast to the approaches discussed below, our semantics targets the high-level HIR represen-
tation and abstracts away from memory representations of the data and other low-level concerns
indistinguishable for a Rust programmer. Most existing work targets the lower-level MIR; the
differences between these two layers are substantial [56], resulting in a significant semantic gap
between many existing formalizations and source code level Rust. As a consequence, we also leave
other concerns such as type checking and borrow checking aside. Rather than formalizing the
borrow checker properties in our semantics—which would be possible—we take Rust’s guarantees
for granted and model the operational behavior only. For similar reasons, we only consider safe
Rust with its stronger guarantees, whereas other approaches also cover unsafe Rust. Lastly, our
semantics is the only one to date with support for async Rust. Hence, a model of a runtime as in
Section 5 and fairness proofs are not possible in other semantics. Table 1 offers a comprehensive
overview of the existing semantics.

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:41


   Jung et al. [38, 39] introduced RustBelt and set out to prove soundness of Rust’s safety guarantees
and to formalize the conditions under which a Rust library is a “safe extension” of the language. To
accomplish this, the authors define a semantic model of a subset of Rust called 𝜆Rust and implement
this model using Iris [40]. This approach has been extended to also consider properties other than
safety [48]. Given their scope, 𝜆Rust is more closely aligned with Rust’s MIR. Furthermore, Jung
et al. are concerned with the type system’s semantics, i.e., how types are modeled and inhabited,
while we take a more abstract view, focused on the operational semantics of expressions. RustBelt
supports unsafe Rust and all relevant data types. As 𝜆Rust is a version of the 𝜆-calculus, the semantics
is based on translation. Enums, e.g., are modeled via sum types.
   The MiniRust project [36] provides a specification for a MIR-like language with the goal of
modeling the core of Rust. Though unofficial, it covers a crucial subset of the MIR and serves as a
more formal FLS, i.e., a formal specification of Rust at a lower level. Its formalization of references
and data types is more explicit than ours in that MiniRust, covering also unsafe Rust, tracks aliases.
MiniRust’s big-step operational semantics (BOS) is not presented in a mathematical style like an
LAGC semantics but a programmatic style. It supports all data types and expressions, though loops
are not explicitly modeled at this level, as they have been translated to basic blocks.
   Similar to MiniRust but more comprehensive is the a-mir-formality project [13], which is part of
the Rust foundation’s efforts. It also aims to cover the type and borrow checker and the trait system.
As it is currently under development, we cannot offer a more detailed comparison at this point.
   Ho et al. [28, 29] present a semantics for a Rust subset called low-level borrow calculus (LLBC) in
the context of the verification tool Aeneas [30]. Their semantics is based on translation to multiple,
successively lower-level languages and can serve as model of Rust’s borrow checker. It supports all
relevant types and expressions, though as translations to other languages.
   Pearce [52] offers an SOS-style semantics for a Rust subset, featherweight Rust (FR). This semantics
also covers references, ownership, and a version of borrow checking. Of the compound types, only
tuples are explicitly covered; others can be translated to suitable representations. Loops are discussed
and an approach outlined, but no rules are provided.

 Semantics          Level    Style      Tuple    Array     Struct     Enum      Loop     Async     Unsafe     BC
 RustBelt [38]      MIR      SOS          ◦         ◦         ◦         ◦         ◦         −         •        •
 MiniRust [36]      MIR      BOS          •         •         •         •         ◦         −         •        •
 LLBC# [28]         MIR      BOS          ◦         ◦         ◦         ◦         ◦         −         −        •
 FR [52]            Src      SOS          •         ◦         ◦         ◦         ◦         −         −        •
 Rust LAGC          HIR      LAGC         •         •         •         •         •         •         −        −
Table 1. Comparison of Rust semantics. We denote a feature being supported by •, unsupported by −, and
partially supported (e.g., by translation to sum types or lambda functions) by ◦. “BC” stands for the borrow
checker being modeled; “Src” stands for source code level.



   There are formal models of Rust ownership and reference system designed for particular per-
spectives. Jung et al. [37] present stacked borrows, a memory model of borrowing in terms of
stacks, which has been extended to more permissive tree borrows by Villani et al. [66]. Even more
encompassing are the formalizations of Rust’s upcoming borrow checker Polonius [14, 45, 46,
47, 54]. As we, at present, offer no model of borrowing, these works can be seen as orthogonal:
their semantics can be incorporated into our semantics by using events and the wf predicate. The
work of Crichton et al. [9] is also relevant, as they provide a conceptual model of ownership and
borrowing along with a concise formalization of Polonius.

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:42                                                                                               Daniel Drodt


7.2    LAGC Semantics
The LAGC approach has been applied to a number of programming languages. In the original
LAGC paper, Din et al. [17] defined semantics for a simple While language, for a ProMeLa-like
language [33], and for a subset of the asynchronous modeling languages ABS [35] and similar
active object languages [10]. The latter has been expanded by Tarifa to a semantics for Real-Time
ABS [62]. Other examples include Timed Rebeca by Hähnle et al. [25] and the smart contract
modeling language SmartML by Reinhold [55]. The breadth of these languages demonstrate the
flexibility of LAGC and especially its usability for concurrency.
   Nevertheless, all prior applications of the LAGC approach were chiefly to small subsets of
languages or modeling languages; real-world programming languages were not approached. One
result of this limited scope is that expressions had so far been assumed to be side-effect free and
pure. We provide the first LAGC semantics that evaluates expressions, not just statements. In fact,
this leads to a slight simplification of the approach: path conditions, a central element of symbolic
traces in prior semantics, can be dropped entirely.
   Another avenue for LAGC research is the fairness of schedulers for programs with cooperative
scheduling. Hähnle and Henrio [24] formalized a deterministic and quiescent fair scheduler for a
language inspired by ABS [35] in LAGC and proved its fairness. Our work builds on their approach
and adapts it to the Tokio scheduler.

7.3    Deductive Verification based on LAGC
Applying LAGC to devise a sound program logic was a core design goal of Din et al. [17] and
part of their work. However, their logic was limited first by their target languages being modeling
languages, as discussed above, and second by the fact that their logics lack implementation. Bubel
et al. [8] extend this trace-based deductive verification approach by devising a logic and calculus for
a more sophisticated setting. It has since been further refined by Hähnle et al. [26] and Scaletta [59].
An implementation of this calculus has since been developed, though only the sequential parts are
supported as yet [58].
   Our work is set apart from the existing LAGC verification approaches, since we did not design
a program logic and calculus based on a semantics or based on traces, but used a trace-based
semantics to validate the soundness of an existing calculus [21]. We demonstrate that even when
a calculus is independent of an LAGC semantics, soundness proofs follow quite readily from the
semantics due to its modular nature. We find that LAGC with its local evaluation rules fits naturally
onto a DL calculus, even for complex languages such as Rust.
   Somewhat related is the work of Beckert and Bruns [4], where they develop a DL, called dynamic
trace logic, over traces and provide a sequent formulas. The approach differs in that Beckert and
Bruns are confined to sequential programs and consider only traces over states without events.
Their goal was a connection between DL and linear temporal logic (LTL).

8     Future Work and Conclusion
8.1    Future Work
The original goal of applying LAGC to Rust in order to obtain a semantics with which our dynamic
logic calculus can be proven sound has been achieved in Section 6. An avenue for future work is to
extend these soundness proofs for the remaining calculus rules, as we present and discuss only
the core rules here—though the remaining rules can be proven straightforwardly following the
schematic approach demonstrated here. Similarly, we plan to consider completeness of the calculus
and demonstrate where incompleteness is still encountered.

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                          ZZZ:43


   As future work, we would like to obtain a mechanization of our complete semantics, the Tokio
formalization, and the DL proofs in a proof assistant. Section 2 has largely been mechanized in
Lean [11], see Drodt [20]. Mechanization of Section 3 is in progress. We intend to extend this to
our other contributions.
   Another direction for future work is to provide an LAGC semantics for other parts of Rust not
adequately modeled in the present article. For instance, a semantics of MIR might be developed,
which more directly expresses Rust’s ownership and reference semantics. Having a semantics both
for the HIR and MIR level would permit defining a notion of correct translation from HIR to MIR,
against which concrete implementations can be checked. Though we believe it possible even on our
chosen level of abstraction, references and borrow checking are more easily modeled on the MIR
level. We may also explore integrating the Polonius borrow-checking formalization into LAGC. A
formalization of Rust’s reference and ownership properties in terms of well-formedness of traces is
not part of our work due to constraints of time and space.
   A final avenue for research is to extend the model of Tokio’s current thread runtime to its multi-
threaded counterpart and prove its fairness. While modeling the runtime is a manageable task, the
fairness proof requires additional proof methods or a more complex proof. Further, extending the
formalization to include I/O events presents an interesting challenge. While Din et al. [17] consider
rudimentary user input, modeling I/O in LAGC has not been attempted at a larger scale.

8.2   Conclusion
Any formal semantics of a real-world programming language is necessarily complex and technically
challenging, which is exacerbated by considering concurrency and scheduling choices. Rust intro-
duces the additional challenge of multiple language layers (HIR and MIR) and sub-languages (unsafe
Rust). Hence, any formalization and semantics of Rust contains abstraction and differing focal
points. We choose to present a relatively abstract, high-level semantics both in terms of language
layer and representation of states. While properties such as memory layout or type safety are not
expressible on this level, we can reason effectively about HIR Rust and asynchronous programs.
   We demonstrate the expressive power of the LAGC approach by formalizing the Tokio runtime
and proving two notions of fairness for our model. Additionally, we show how soundness of a
program logic calculus can be derived from our semantics. Both of these endeavors would be much
more complex, if not unfeasible, in a SOS-style semantics or a semantics for Rust’s lower layers.
Thereby, we show that the seemingly high upfront complexity of the LAGC approach is offset by
the gain in its modular approach.
   Our semantics also demonstrate the LAGC approach’s applicability to real-world programming
languages, bridging the gap from the academic languages to which it had been confined. The
approach is sufficiently flexible and powerful to accurately model a language like Rust which, with
its more functional syntax, lays outside the purview of LAGC’s original scope. In fact, we were able
to simplify the approach, dropping path conditions entirely, and complete the model with relative
ease. It proved to be a natural match for modeling Rust’s async features and runtimes.
   Thus, we offer a formal semantics for Rust with many different applications and use cases, as
demonstrated above.

Acknowledgments
This work is supported by the German Research Foundation under Grants No. BU 2924/3-1 and
HA 2617/9-1.
  We would like to thank the following people for their careful and incisive feedback: Reiner
Hähnle, Richard Bubel, Marco Scaletta, Lukas Grätz, and Niklas Heidler. We also thank Thanh Long
Nguyen for his work on the Lean mechanization.

                 ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:44                                                                                                         Daniel Drodt


References
 [1]   Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, Reiner Hähnle, Peter H. Schmitt, and Mattias Ulbrich, (Eds.)
       2016. Deductive Software Verification – the KeY Book: From Theory to Practice. Number 10001 in LNCS. Springer.
       doi:10.1007/978-3-319-49812-6.
 [2]   Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, Reiner Hähnle, and Mattias Ulbrich. 2025. The many uses of
       dynamic logic. In Go Where the Bugs Are – Essays Dedicated to Wolfgang Reif on the Occasion of His 65th Birthday
       (LNCS) number 15765. Gidon Ernst, Matthias Güdemann, Alexander Knapp, Florian Nafz, Frank Ortmeier, Hella
       Ponsar, Gerhard Schellhorn, and Alexander Schiendorfer, (Eds.) Springer, Cham, (June 2025), 56–82. doi:10.1007/978-
       3-031-92196-4_4.
 [3]   Vytautas Astrauskas, Aurel Bílý, Jonás Fiala, Zachary Grannan, Christoph Matheja, Peter Müller, Federico Poli,
       and Alexander J. Summers. 2022. The Prusti project: Formal verification for Rust. In NFM 2022 Proceedings (LNCS)
       number 13260. Jyotirmoy V. Deshmukh, Klaus Havelund, and Ivan Perez, (Eds.) Springer, 88–108. doi:10.1007/978-3-
       031-06773-0_5.
 [4]   Bernhard Beckert and Daniel Bruns. 2013. Dynamic logic with trace semantics. In Automated Deduction – CADE-24
       (LNAI) number 7898. Maria Paola Bonacina, (Ed.) Springer, Berlin, Heidelberg, 315–329. doi:10.1007/978-3-642-38574
       -2_22.
 [5]   Bernhard Beckert, Richard Bubel, Daniel Drodt, Reiner Hähnle, Florian Lanzinger, Wolfram Pfeifer, Mattias Ulbrich,
       and Alexander Weigl. 2025. The Java verification tool KeY: A tutorial. In Formal Methods (LNCS) number 14934.
       Andre Platzer, Kristin Yvonne Rozier, Matteo Pradella, and Matteo Rossi, (Eds.) Springer Nature Switzerland, Cham,
       597–623. isbn: 978-3-031-71177-0. doi:10.1007/978-3-031-71177-0_32.
 [6]   Karthikeyan Bhargavan, Maxime Buyse, Lucas Franceschino, Lasse Letager Hansen, Franziskus Kiefer, Jonas
       Schneider-Bensch, and Bas Spitters. 2025. Hax: Verifying security-critical Rust software using multiple provers. In
       Verified Software. Theories, Tools and Experiments 2024 Proceedings (LNCS) number 15525. Jonathan Protzenko and
       Azalea Raad, (Eds.) Springer, 96–119. doi:10.1007/978-3-031-86695-1_7.
 [7]   Stephen Brookes. 2007. A semantics for concurrent separation logic. Theor. Comput. Sci., 375, 1–3, 227–270. doi:10.10
       16/j.tcs.2006.12.034.
 [8]   Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta. 2023. Trace-based deductive verification. In LPAR
       2023: Proceedings of 24th International Conference on Logic for Programming, Artificial Intelligence and Reasoning,
       Manizales, Colombia, 4–9th June 2023 (EPiC Series in Computing). Ruzica Piskac and Andrei Voronkov, (Eds.) Vol. 94.
       EasyChair, 73–95. doi:10.29007/VDFD.
 [9]   Will Crichton, Gavin Gray, and Shriram Krishnamurthi. 2023. A grounded conceptual model for ownership types in
       Rust. Proc. ACM Program. Lang., 7, (Oct. 2023), 265:1–265:29, OOPSLA2, (Oct. 2023). Michael Hicks, (Ed.) doi:10.1145
       /3622841.
[10]   Frank de Boer et al. 2017. A survey of active object languages. ACM Computing Surveys, 50, 5, (Oct. 2017), 76:1–76:39.
       doi:10.1145/3122848.
[11]   Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 theorem prover and programming language. In CADE
       (LNCS) number 12699. Springer, 625–635. doi:10.1007/978-3-030-79876-5_37.
[12]   Xavier Denis, Jacques-Henri Jourdan, and Claude Marché. 2022. Creusot: A foundry for the deductive verification of
       Rust programs. In ICFEM 2022, Proceedings (LNCS) number 13478. Adrián Riesco and Min Zhang, (Eds.) Springer,
       90–105. doi:10.1007/978-3-031-17244-1_6.
[13]   [SW] The Rust developers, A-Mir-Formality 2026. url: https://github.com/rust-lang/a-mir-formality.
[14]   [SW] The Rust developers, Polonius 2025. url: https://github.com/rust-lang/polonius.
[15]   Crystal Chang Din, Richard Bubel, and Reiner Hähnle. 2015. KeY-ABS: A deductive verification tool for the con-
       current modelling language ABS. In Proc. 25th Intl. Conf. on Automated Deduction (CADE), Berlin, Germany (LNCS)
       number 9195. Amy Felty and Aart Middeldorp, (Eds.) Springer, 517–526. doi:10.1007/978-3-319-21401-6_35.
[16]   Crystal Chang Din, Johan Dovland, Einar Broch Johnsen, and Olaf Owe. 2012. Observable behavior of distributed
       systems: Component reasoning for concurrent objects. Journal of Logic and Algebraic Programming, 81, 3, 227–256.
       doi:10.1016/j.jlap.2012.01.003.
[17]   Crystal Chang Din, Reiner Hähnle, Ludovic Henrio, Einar Broch Johnsen, Violet Ka I Pun, and Silvia Lizeth Tapia
       Tarifa. 2024. Locally abstract, globally concrete semantics of concurrent programming languages. Transactions on
       Programming Languages and Systems, 46, 1, (Mar. 2024), 3:1–3:58. doi:10.1145/3648439.
[18]   Crystal Chang Din, Reiner Hähnle, Einar Broch Johnsen, Violet Ka I Pun, and Silvia Lizeth Tapia Tarifa. 2017. Locally
       abstract, globally concrete semantics of concurrent programming languages. In TABLEAUX 2017 (LNCS). Cláudia
       Nalon and Renate Schmidt, (Eds.) Vol. 10501. Springer, (Sept. 2017), 22–43. doi:10.1007/978-3-319-66902-1_2.
[19]   Crystal Chang Din and Olaf Owe. 2015. Compositional reasoning about active objects with shared futures. Formal
       Asp. Comput., 27, 3, 551–572. doi:10.1007/s00165-014-0322-y.
[20]   [SW] Daniel Drodt, Rust-LAGC Sept. 21, 2026. url: https://github.com/Drodt/Rust-LAGC.


ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                                    ZZZ:45


[21]   Daniel Drodt and Reiner Hähnle. 2026. RustyDL: A program logic for Rust. In Proc. 27th Intl. Symp. on Formal
       Methods, Tokyo, Japan, Part I (LNCS) number 16556. Augusto Sampaio, Marielle Stoelinga, Achim D. Brucker, and
       Marie-Christine Jakobs, (Eds.) Springer, Cham, (May 2026), 357–377. doi:10.1007/978-3-032-26204-2_19.
[22]   Daniel Drodt and Reiner Hähnle. 2026. RustyDL: A Program Logic for Rust. Technical report. arXiv: 2602.22075
       [cs.PL]. doi:10.48550/arXiv.2602.22075.
[23]   [SW] Glommio Developers, Glommio version 0.9.0, Mar. 25, 2024. url: https://docs.rs/glommio/0.9.0/glommio
       /Retrieved Aug. 22, 2026 from.
[24]   Reiner Hähnle and Ludovic Henrio. 2024. Provably fair cooperative scheduling. Art Sci. Eng. Program., 8, 2. doi:10.221
       52/PROGRAMMING-JOURNAL.ORG/2024/8/6.
[25]   Reiner Hähnle, Einar Broch Johnsen, and Silvia Lizeth Tapia Tarifa. 2025. An LAGC semantics for Timed Rebeca.
       In Rebeca for Actor Analysis in Action – Essays Dedicated to Marjan Sirjani on the Occasion of Her 60th Birthday
       (LNCS) number 15560. Edward A. Lee, Mohammad Reza Mousavi, and Carolyn L. Talcott, (Eds.) Springer, 326–348.
       doi:10.1007/978-3-031-85134-6_14.
[26]   Reiner Hähnle, Eduard Kamburjan, and Marco Scaletta. 2024. Context-aware trace contracts. In Active Object
       Languages: Current Research Trends (LNCS) number 14360. Frank De Boer, Ferruccio Damiani, Reiner Hähnle, Einar
       Broch Johnsen, and Eduard Kamburjan, (Eds.) Springer, Cham, 292–325. doi:10.1007/978-3-031-51060-1_11.
[27]   Joseph Halpern, Zohar Manna, and Ben Moszkowski. 1983. A hardware semantics based on temporal intervals. In
       Automata, Languages and Programming. Josep Diaz, (Ed.) Springer, Berlin, Heidelberg, 278–291. doi:10.1007/BFb0036
       915.
[28]   Son Ho, Aymeric Fromherz, and Jonathan Protzenko. 2024. Sound borrow-checking for Rust via symbolic semantics.
       Proc. ACM Program. Lang., 8, 426–454, ICFP. doi:10.1145/3674640.
[29]   Son Ho, Aymeric Fromherz, and Jonathan Protzenko. 2024. Sound borrow-checking for Rust via symbolic semantics
       (long version). (July 1, 2024). arXiv: 2404.02680 [cs]. Pre-published.
[30]   Son Ho and Jonathan Protzenko. 2022. Aeneas: Rust verification by functional translation. Proc. ACM Program. Lang.,
       6, 711–741, ICFP. doi:10.1145/3547647.
[31]   C. A. R. Hoare. 1969. An axiomatic basis for computer programming. Commun. ACM, 12, 10, (Oct. 1, 1969), 576–580.
       doi:10.1145/363235.363259.
[32]   Kevin J. Hoffman, Patrick Eugster, and Suresh Jagannathan. 2009. Semantics-aware trace analysis. SIGPLAN Not., 44,
       6, (June 2009), 453–464. doi:10.1145/1543135.1542527.
[33]   Gerard J. Holzmann. 2004. The SPIN Model Checker – Primer and Reference Manual. Addison-Wesley.
[34]   Eric Huss, Felix Klock, Joel Marcey, and Mara Bos. 2023. Our vision for the Rust specification. Inside Rust Blog.
       (Nov. 15, 2023). Retrieved July 23, 2026 from https://blog.rust-lang.org/inside-rust/2023/11/15/spec-vision/.
[35]   Einar Broch Johnsen, Reiner Hähnle, Jan Schäfer, Rudolf Schlatte, and Martin Steffen. 2011. ABS: A core language
       for abstract behavioral specification. In FMCO 2010 Proceedings (LNCS) number 6957. Bernhard K. Aichernig, Frank
       de Boer, and Marcello M. Bonsangue, (Eds.) Springer, 142–164. doi:10.1007/978-3-642-25271-6_8.
[36]   [SW] Ralf Jung, MiniRust Mar. 25, 2026. minirust. url: https://github.com/minirust/minirust.
[37]   Ralf Jung, Hoang-Hai Dang, Jeehoon Kang, and Derek Dreyer. 2019. Stacked borrows: an aliasing model for Rust.
       Proc. ACM Program. Lang., 4, (Dec. 20, 2019), 41:1–41:32, POPL, (Dec. 20, 2019). doi:10.1145/3371109.
[38]   Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. RustBelt: Securing the Foundations of
       the Rust Programming Language. Technical appendix. Retrieved July 23, 2026 from https://plv.mpi-sws.org/rustbelt
       /popl18/.
[39]   Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2018. RustBelt: Securing the foundations of
       the Rust programming language. Proc. ACM Program. Lang., 2, 66:1–66:34, POPL. doi:10.1145/3158154.
[40]   Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. 2015.
       Iris: Monoids and invariants as an orthogonal basis for concurrent reasoning. In Proceedings of the 42nd Annual ACM
       SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2015, Mumbai, India, January 15–17,
       2015. Sriram K. Rajamani and David Walker, (Eds.) ACM, 637–650. doi:10.1145/2676726.2676980.
[41]   Eduard Kamburjan. 2019. Behavioral program logic. In TABLEAUX 2019 (LNCS). Serenella Cerrito and Andrei Popescu,
       (Eds.) Vol. 11714. Springer, 391–408. doi:10.1007/978-3-030-29026-9_22.
[42]   Steve Klabnik, Carol Nichols, and Chris Krycho. 2026. The Rust Programming Language. (3rd ed.). No Starch Press,
       San Francisco, CA, (Mar. 2026). Retrieved July 23, 2026 from https://doc.rust-lang.org/stable/book/.
[43]   Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno,
       and Chris Hawblitzel. 2023. Verus: Verifying Rust programs using linear ghost types. Proc. ACM Program. Lang., 7,
       286–315, OOPSLA1. doi:10.1145/3586037.
[44]   Hongyu Li, Liwei Guo, Yexuan Yang, Shangguang Wang, and Mengwei Xu. 2024. An empirical study of Rust-for-Linux:
       The success, dissatisfaction, and compromise. In USENIX ATC 2024 Proceedings. Saurabh Bagchi and Yiying Zhang,
       (Eds.) USENIX Association, 425–443. https://www.usenix.org/conference/atc24/presentation/li-hongyu.


                   ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:46                                                                                                           Daniel Drodt


[45]   Niko Matsakis. 2018. An alias-based formulation of the borrow checker. baby steps. (Apr. 27, 2018). Retrieved July 23,
       2026 from https://smallcultfollowing.com/babysteps/blog/2018/04/27/an-alias-based-formulation-of-the-borrow-ch
       ecker/.
[46]   Niko Matsakis. 2023. Polonius revisited, part 2. baby steps. (Sept. 29, 2023). Retrieved July 23, 2026 from https://small
       cultfollowing.com/babysteps/blog/2023/09/29/polonius-part-2/.
[47]   Niko Matsakis. 2023. Polonius revisted, part 1. baby steps. (Sept. 22, 2023). Retrieved July 23, 2026 from https://smallc
       ultfollowing.com/babysteps/blog/2023/09/22/polonius-part-1/.
[48]   Yusuke Matsushita, Xavier Denis, Jacques-Henri Jourdan, and Derek Dreyer. 2022. RustHornBelt: A semantic
       foundation for functional verification of Rust programs with unsafe code. In PLDI ’22: 43rd ACM SIGPLAN International
       Conference on Programming Language Design and Implementation, San Diego, CA, USA, June 13 - 17, 2022. Ranjit Jhala
       and Isil Dillig, (Eds.) ACM, 841–856. doi:10.1145/3519939.3523704.
[49]   Yasuhiko Minamide. 1998. A functional representation of data structures with a hole. In Proc. of the 25th ACM
       SIGPLAN-SIGACT Symposium on Principles of Programming Languages (Popl ’98). ACM, San Diego, California, USA,
       75–84. doi:10.1145/268946.268953.
[50]   Peter D Mosses. 2004. Modular structural operational semantics. The Journal of Logic and Algebraic Programming.
       Structural Operational Semantics 60–61, (July 1, 2004), 195–228. doi:10.1016/j.jlap.2004.03.008.
[51]   Peter Müller, Malte Schwerhoff, and Alexander J. Summers. 2016. Viper: A verification infrastructure for permission-
       based reasoning. In Verification, Model Checking, and Abstract Interpretation. Barbara Jobstmann and K. Rustan M.
       Leino, (Eds.) Springer Berlin Heidelberg, Berlin, Heidelberg, 41–62. isbn: 978-3-662-49122-5. doi:10.1007/978-3-662-4
       9122-5_2.
[52]   David J. Pearce. 2021. A lightweight formalism for reference lifetimes and borrowing in Rust. ACM Trans. Program.
       Lang. Syst., 43, 1, (Apr. 17, 2021), 3:1–3:73. doi:10.1145/3443420.
[53]   Vaughan R Pratt. 1976. Semantical considerations on Floyd-Hoare logic. In 17th Annual Symposium on Foundations of
       Computer Science, Houston, TX, USA. IEEE, Los Alamitos, CA, 109–121. doi:10.1109/SFCS.1976.27.
[54]   Rémy Rakic and Niko Matsakis. 2023. Polonius update. Inside Rust Blog. (Oct. 6, 2023). Retrieved July 23, 2026 from
       https://blog.rust-lang.org/inside-rust/2023/10/06/polonius-update/.
[55]   Tobias Reinhold. 2024. Formal Semantics for Smart Contracts. BA thesis. Technical University of Darmstadt, Depart-
       ment of Computer Science, Darmstadt, Germany, (Dec. 11, 2024). 68 pp.
[56]   Rust Community. 2026. Rust Compiler Development Guide. Retrieved July 23, 2026 from https://rustc-dev-guide.rust-l
       ang.org/.
[57]   Rust Community. 2026. The Rust Reference. Reference. Rust Foundation. Retrieved July 23, 2026 from https://doc.rus
       t-lang.org/stable/reference/introduction.html.
[58]   [SW] Marco Scaletta, KeY4CATs: A Deductive Verification Tool for Context-Aware Trace Contracts June 2026.
       Zenodo. doi:10.5281/zenodo.20762522.
[59]   Marco Scaletta. 2026. Modular Specification and Verification of Concurrent Programs with Context-Aware Trace Contracts.
       Ph.D. Dissertation. Technical University of Darmstadt, Department of Computer Science. doi:10.26083/tuda-8276.
[60]   [SW] smol Developers, smol version 2.0.2, Sept. 7, 2024. url: https://docs.rs/smol/2.0.2/smol/Retrieved Aug. 22, 2026
       from.
[61]   Dominic Steinhöfel and Nathan Wasser. 2017. A new invariant rule for the analysis of loops with non-standard
       control flows. In iFM 2017 Proceedings (LNCS) number 10510. Nadia Polikarpova and Steve A. Schneider, (Eds.)
       Springer, 279–294. doi:10.1007/978-3-319-66845-1_18.
[62]   Silvia Lizeth Tapia Tarifa. 2022. Locally abstract globally concrete semantics of time and resource aware active objects.
       In The Logic of Software. A Tasting Menu of Formal Methods – Essays Dedicated to Reiner Hähnle on the Occasion of His
       60th Birthday (LNCS) number 13360. Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, and Einar Broch Johnsen,
       (Eds.) Springer, 481–499. doi:10.1007/978-3-031-08166-8_23.
[63]   The Ferrocene developers and The Rust project contributors. 2026. Ferrocene Language Specification. Reference.
       Rust Foundation. Retrieved July 23, 2026 from https://rust-lang.github.io/fls.
[64]   [SW] Tokio Developers, Tokio version 1.53.1, July 20, 2026. url: https://crates.io/crates/tokio.
[65]   Tokio Developers. 2026. tokio::runtime – Documentation. (July 20, 2026). Retrieved July 23, 2026 from https://docs.rs
       /tokio/1.53.1/tokio/runtime/index.html#detailed-runtime-behavior.
[66]   Neven Villani, Johannes Hostert, Derek Dreyer, and Ralf Jung. 2025. Tree borrows. Proc. ACM Program. Lang., 9,
       (June 13, 2025), 188:1019–188:1042, PLDI, (June 13, 2025). doi:10.1145/3735592.
[67]   Philip Wadler. 2018. Programming language foundations in Agda. In Formal Methods: Foundations and Applications
       (LNCS) number 11254. Tiago Massoni and Mohammad Reza Mousavi, (Eds.) Springer, Cham, 56–73. doi:10.1007/978-
       3-030-03044-5_5.




ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                                            ZZZ:47


A   Additional Definitions of the next Function
First, we show the expressions which have no sub-expression under any circumstances. Those are
values, program variables, continue, loop, and panic expressions. For them, the entire expression is
considered the sub-expression and the hole expression is the hole •.
                                                                      next (𝑣, 𝑀) = (𝑣, •)
                                                                      next (x, 𝑀) = (x, •)
                                          next (continue ’𝑙, 𝑀) = (continue ’𝑙, •)
                                                  next (’𝑙 loop 𝑒, 𝑀) = (’𝑙 loop 𝑒, •)
                                                        next (panic!, 𝑀) = (panic!, •)
Dereferencing expressions have, potentially, one sub-expression, which is always evaluated to a
value. Similar definitions holds for match, break, return, and array repeat expressions.
                                                       (
                                                         (*𝑒, •)   if 𝑒 ∈ Val
                                  next (*𝑒, 𝑀) =
                                                         (𝑒 , *he) if 𝑒 ∉ Val ∧ (𝑒 ′, he) = next (𝑒, Val)
                                                           ′
                                    (
                                      (match 𝑒 {arm}, •)           if 𝑒 ∈ Val
      next (match 𝑒 {arm}, 𝑀) =
                                      (𝑒 ′, match he {arm}) if 𝑒 ∉ Val ∧ (𝑒 ′, he) = next (𝑒, Val)
                                            (
                                              (break ’𝑙 𝑒, •)      if 𝑒 ∈ Val
                  next (break ’𝑙 𝑒, 𝑀) =
                                              (𝑒 , break ’𝑙 he) if 𝑒 ∉ Val ∧ (𝑒 ′, he) = next (𝑒, Val)
                                                 ′
                                             (
                                                (return 𝑒, •)      if 𝑒 ∈ Val
                     next (return 𝑒, 𝑀) =
                                                (𝑒 ′, return he) if 𝑒 ∉ Val ∧ (𝑒 ′, he) = next (𝑒, Val)
                                                  (
                                                    ([𝑒; 𝑛], •)    if 𝑒 ∈ Val
                           next ([𝑒; 𝑛], 𝑀) =
                                                    (𝑒 , [he; 𝑛]) if 𝑒 ∉ Val ∧ (𝑒 ′, he) = next (𝑒, Val)
                                                       ′


  Block expressions must be considered depending on their first statement. If it is a let statement,
there is no next sub-expression. If it is an expression, but not a break expression with a value or
continue expression, it behaves as above. We exclude break and continues here to fit the expected
rule shape expected in Section 3.1.9. If there are no statements, it is exactly as in the cases above, as
there is only one possible sub-expression.
                                                          next ({let pat = 𝑒 1 ; 𝑠 𝑒 2 }, =) ({let pat = 𝑒 1 ; 𝑠 𝑒 2 }, •)
                                   (
                                       ({𝑒 1 ; 𝑠 𝑒 2 }, •)
                                                    if 𝑒 1 ∈ Val ∨ 𝑒 1 = break ’𝑙 𝑣 ∨ 𝑒 1 = continue ’𝑙
        next ({𝑒 1 ; 𝑠 𝑒 2 }, =)
                                       (𝑒 1′ , {he; 𝑠 𝑒 2 })
                                                    otherwise, where (𝑒 1′ , he) = next (𝑒 1, Val)
                                                   (
                                                     ({𝑒}, •)     if 𝑒 ∈ Val
                                   next ({𝑒}, 𝑀) =
                                                     (𝑒 , {he}) if 𝑒 ∉ Val ∧ (𝑒 ′, he) = next (𝑒, Val)
                                                       ′


  Operator expressions have two potential sub-expressions, which are all evaluated to values. We
only show the case for addition; other operators are analogous.
                               (𝑒 + 𝑒 , •)                    if 𝑒 1, 𝑒 2 ∈ Val
                               1 2
                              
                              
                              
         next (𝑒 1 + 𝑒 2, 𝑀) = (𝑒 1′ , he + 𝑒 2 )              if 𝑒 1 ∉ Val ∧ (𝑒 1′ , he) = next (𝑒 1, Val)
                              
                               (𝑒 ′ , 𝑒 1 + he)
                              
                                                               if 𝑒 1 ∈ Val ∧ 𝑒 2 ∉ Val ∧ (𝑒 2′ , he) = next (𝑒 2, Val)
                               2

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:48                                                                                                                   Daniel Drodt


Assignment operators behave differently. When 𝑒 1, 𝑒 2 are of integer types, the sub-expressions are
evaluated right-to-left; otherwise left-to-right. We always evaluate 𝑒 2 to a value, but 𝑒 1 to a place.
Here, we show the integer version.

                              (𝑒 += 𝑒 2, •)                    if 𝑒 1 ∈ Place ∧ 𝑒 2 ∈ Val
                              1
                             
                             
                             
       next (𝑒 1 += 𝑒 2, 𝑀) = (𝑒 2′ , 𝑒 1 += he)                if 𝑒 2 ∉ Val ∧ (𝑒 2′ , he) = next (𝑒 2, Val)
                             
                              (𝑒 ′ , he += 𝑒 2 )
                             
                                                                if 𝑒 2 ∈ Val ∧ 𝑒 1 ∉ Place ∧ (𝑒 1′ , he) = next (𝑒 1, Place)
                              1

Arrays and tuples behave identically: Evaluation is left-to-right and we might be in an assignee or
value context. Struct expressions x{ident 1 : 𝑒 1, . . . , ident𝑛 : 𝑒𝑛 } are analogous to arrays and tuples.

                                     ([𝑒 , . . . , 𝑒𝑛 ], •)                                  if 𝑒 1, . . . , 𝑒𝑛 ∈ 𝑀
                                     1
                                    
                                    
                                    
      next ([𝑒 1, . . . , 𝑒𝑛 ], 𝑀) = (𝑒𝑘′ , [𝑒 1, . . . , 𝑒𝑘 −1, he, 𝑒𝑘+1, . . . , 𝑒𝑛 ])      if 𝑒 1, . . . , 𝑒𝑘 −1 ∈ 𝑀 ∧ 𝑒𝑘 ∉ 𝑀
                                    
                                                                                                  ∧(𝑒𝑘′ , he) = next (𝑒𝑘 , 𝑀)
                                    
                                    
                                    

                                     ((𝑒 , . . . , 𝑒𝑛 ), •)                                  if 𝑒 1, . . . , 𝑒𝑛 ∈ 𝑀
                                     1
                                    
                                    
                                    
      next ((𝑒 1, . . . , 𝑒𝑛 ), 𝑀) = (𝑒𝑘′ , (𝑒 1, . . . , 𝑒𝑘 −1, he, 𝑒𝑘+1, . . . , 𝑒𝑛 ))      if 𝑒 1, . . . , 𝑒𝑘 −1 ∈ 𝑀 ∧ 𝑒𝑘 ∉ 𝑀
                                    
                                                                                                  ∧(𝑒𝑘′ , he) = next (𝑒𝑘 , 𝑀)
                                    
                                    
                                    
Function calls behave like tuples and array but with an additional expression, the callee, which is
evaluated first. Method calls 𝑒.ident(𝑒 1, . . . , 𝑒𝑛 ) analogous to function calls and are omitted.

                                   
                                   
                                    (𝑒(𝑒 1, . . . , 𝑒𝑛 ), •)                               if 𝑒, 𝑒 1, . . . , 𝑒𝑛 ∈ Val
                                    (𝑒 ′, he(𝑒 , . . . , 𝑒 ))                              if 𝑒 ∉ Val ∧ (𝑒 ′, he) = next (𝑒, Val)
                                   
                                   
                                                1          𝑛
 next (𝑒(𝑒 1, . . . , 𝑒𝑛 ), 𝑀) =
                                   
                                   
                                    (𝑒𝑘′ , 𝑒(𝑒 1, . . . , 𝑒𝑘 −1, he, 𝑒𝑘+1, . . . , 𝑒𝑛 ))   if 𝑒, 𝑒 1, . . . , 𝑒𝑘 −1 ∈ Val ∧ 𝑒𝑘 ∉ Val
                                                                                                ∧(𝑒𝑘′ , he) = next (𝑒𝑘 , Val)
                                   
                                   
                                   

   Field access expressions depend on the context, as they may evaluate their single sub-expression
to an assignee value or a value.
                                                 (
                                                     (𝑒.ident, •)         if 𝑒 ∈ 𝑀
                     next (𝑒.ident, 𝑀) =
                                                     (𝑒 ′, he.ident)      if 𝑒 ∉ 𝑀 ∧ (𝑒 ′, he) = next (𝑒, 𝑀)

    Reference expressions always evaluate their sub-expression to a place.
                                                     (
                                                         (&𝑒, •)       if 𝑒 ∈ Place
                             next (&𝑒, 𝑀) =
                                                         (𝑒 ′, &he)    if 𝑒 ∉ Place ∧ (𝑒 ′, he) = next (𝑒, Place)
                                            (
                                                (&mut 𝑒, •)            if 𝑒 ∈ Place
               next (&mut 𝑒, 𝑀) =
                                                (𝑒 ′, &mut he)         if 𝑒 ∉ Place ∧ (𝑒 ′, he) = next (𝑒, Place)

B    Axiomatization of Queue
We repeat and adapt the axiomatization for queues found in [24].


ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:49


  Definition B.1 (Queue). We define a queue of type 𝑇 𝑞 as queues over elements of type 𝑇 . The
operations are:
           queue()       — creates an empty queue
          empty (𝑞)      — is true iff 𝑞 is the empty queue
              𝑞 ⊕𝑘       — returns a queue 𝑞 ′ that is 𝑞 extended with 𝑘 as its last element
            pop (𝑞)      — returns a pair (𝑞 ′, 𝑘), where 𝑘 is the first element in 𝑞 and 𝑞 ′
                           the remaining queue after 𝑘 is removed; the operation is
                           undefined iff 𝑞 is empty
The operations are defined by the following axioms:
                                                                                    empty (queue())            (85)
                                                                                     pop (queue()) ↑           (86)
                                                                              ∀𝑞, 𝑘. ¬empty (𝑞 ⊕ 𝑘)            (87)
                                             (
                                                 (queue(), 𝑘)   if empty (𝑞)
           ∀𝑞, 𝑘, 𝑞 ′, 𝑘 ′ . pop (𝑞 ⊕ 𝑘) =                                                                     (88)
                                                 (𝑞 ′ ⊕ 𝑘)      otherwise, where (𝑞 ′, 𝑘 ′ ) = pop (𝑞)

If 𝑞 is a queue of stacks of continuation markers, we also define the set of continuation markers in
𝑞, Ks (𝑞), as:
                                    (
                                      ∅            if empty (𝑞)
                           Ks (𝑞) =
                                      𝑘 ⊎ Ks (𝑞 ) where pop (𝑞) = (𝑞 ′, 𝑘)
                                               ′


C   Additional Current Thread Composition Rules
                         𝑓 , ℎ. lastEv(sh) = spawnEv(𝑓 , ℎ) 𝑡 . 0 mod 𝐼𝐺
               empty (𝑞) pop (𝑞𝐺 ) = (𝑞𝐺′ , (foo, 𝑓 )) 𝜎 = last(sh) fn foo(𝑥) 𝑒 ∈ Fn
                 𝜏 · K(𝑒 ′ ) ∈ val𝜎 (fn foo(𝑥) 𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                   𝑓                                                                           (89)

                           sh, ⟨Idle, 𝑡, 𝑞𝐺 , 𝑞⟩ →ct sh, K 𝑓 (𝑒 ′ ) , 𝑡 + 1, 𝑞𝐺′ , 𝑞
                                                                  


                            𝑓 , ℎ. lastEv(sh) = spawnEv(𝑓 , ℎ) 𝑡 . 0 mod 𝐼𝐺
                         pop (𝑞) = (𝑞 ′, (foo, 𝑓 )) 𝜎 = last(sh) fn foo(𝑥) 𝑒 ∈ Fn
                    𝜏 · K(𝑒 ′ ) ∈ val𝜎 (fn foo(𝑥) 𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))
                                      𝑓                                                                        (90)

                              sh, ⟨Idle, 𝑡, 𝑞𝐺 , 𝑞⟩ →ct sh, K 𝑓 (𝑒 ′ ) , 𝑡 + 1, 𝑞𝐺 , 𝑞 ′
                                                                     


D    Quiescent Fairness of the Current Thread Scheduler
We first define a translation function “trans” mapping current thread configurations to configura-
tions in the semantics of Section 4. Traces and the scheduler’s state can be mapped independently
to traces and sets of tasks, respectively. For this, we lift trans to both:
                     trans(sh, ⟨active, 𝑡, 𝑞𝐺 , 𝑞⟩) = trans(sh), trans(⟨active, 𝑡, 𝑞𝐺 , 𝑞⟩)
   Traces are “translated” via a projection, by removing the schedule events and the preceding state
(as rule (73) repeats this state).
                                 trans(𝜀) = 𝜀
          trans(sh ↷ 𝜎 ↷ schedEv(foo, 𝑓 )) = trans(sh)
                           trans(sh ↷ 𝑡) = trans(sh) ↷ 𝑡                   when 𝑡 ≠ schedEv(foo, 𝑓 )

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:50                                                                                                         Daniel Drodt


   Next, we define how queues of continuation stacks and task markers are mapped to sets of these
stacks. The inductive definition is obvious; note that the third case drops task markers.
                             
                             
                             
                              ∅                            if empty (𝑞) 
                             nh io
                                                                            h i
                      0
                 trans (𝑞) =     𝑘 ⊎ trans0 (𝑞 ′ )          if pop (𝑞) = 𝑞 ′, 𝑘
                             
                              trans0 (𝑞 ′ )                otherwise, with pop (𝑞) = (𝑞 ′, 𝑘)
                             
                             
                             
   Finally, we translate the scheduler state by combining the global and local queue with the active
task:
                                                                                  
                         trans(⟨act, 𝑡, 𝑞𝐺 , 𝑞⟩) = act, trans0 (𝑞𝐺 ) ⊎ trans0 (𝑞)
   Next, we define a measure of the scheduling distance. We use this in our fairness proof, showing
that at every step, an enabled expression is either executed or its distance decreases. Similar to
a termination witness in formal verification [1], this distance does not need to be an accurate
representation of how many “steps” it takes until an expression is executed. It suffices to be a
finitely descending chain of values.

  Definition D.1 (Scheduling Distance: Current Thread). Let the configuration 𝐶 = sh, ⟨act, 𝑡, 𝑞𝐺 , 𝑞⟩
and 𝑐 ∈ Z. We define the scheduling distance 𝑑 of a continuation marker K 𝑓 (𝑒) in 𝐶 as follows:

                         𝑑 (K 𝑓 (𝑒), 𝐶, 𝑐) = (pos(K 𝑓 (𝑒), 𝐶), idle(𝐶), unsched(sh), 𝑐)

where pos defines the position of the continuation in the scheduler as:

             pos(K 𝑓 (𝑒), sh, ⟨act, 𝑡, 𝑞𝐺 , 𝑞⟩) =
           
           
           
            1                                       if act = [𝑘 1, . . . , 𝑘𝑛 ] ∧ K 𝑓 (𝑒) = 𝑘 1
           
           
           
                                                       ∧ ¬suspended(𝑒, sh)
           
             |Ks (𝑞)| + |Ks (𝑞𝐺 )| + 2               if act = [𝑘 1, . . . , 𝑘𝑛 ] ∧ K 𝑓 (𝑒) = 𝑘 1
           
           
           
           
           
                                                        ∧ suspended(𝑒, sh)
           
           
           
           
           
           𝑖 + |Ks (𝑞)| + |Ks (𝑞 )| + 2
           
                                   𝐺                if act = [𝑘 1, . . . , 𝑘𝑛 ] ∧ K 𝑓 (𝑒) = 𝑘𝑖 ∧ 1 < 𝑖 ≤ 𝑛
           
           
            1 + qPos(K 𝑓 (𝑒), 𝑞) + |Ks (𝑞𝐺 )|       if act ≠ Idle ∧ K 𝑓 (𝑒) ∈ Ks (𝑞)
           
           
           
            1 + |Ks (𝑞)| + qPos(K 𝑓 (𝑒), 𝑞𝐺 )       if act ≠ Idle ∧ K 𝑓 (𝑒) ∈ Ks (𝑞𝐺 )
           
             qPos(K 𝑓 (𝑒), 𝑞) + |Ks (𝑞𝐺 )|           if act = Idle ∧ K 𝑓 (𝑒) ∈ Ks (𝑞)
           
           
           
           
           
             |Ks (𝑞)| + qPos(K 𝑓 (𝑒), 𝑞𝐺 )           if act = Idle ∧ K 𝑓 (𝑒) ∈ Ks (𝑞𝐺 )
           
           
           
           
           
            undef                                   if K 𝑓 (𝑒) ∉ Ks (trans(⟨[𝑘 1, . . . , 𝑘𝑛 ], 𝑡, 𝑞𝐺 , 𝑞⟩))
           
           
Note that this position definition is pessimistic: If a continuation marker is in one queue, it assumes
that the entire other queue may be scheduled before it. While unrealistic, our scheduling distance
need only be an over approximation of the “real distance.” Further, the distance is only used in our
proof for enabled continuation markers, i.e., continuation markers executable in the next step.
  A continuation marker’s position in a queue is defined as follows:
                         
                         
                         𝑖                           if pop (𝑞) = (𝑞 ′, [𝑘 1, . . . , 𝑘𝑛 ]) ∧ K 𝑓 (𝑒) = 𝑘𝑖
                         𝑛 + qPos(K 𝑓 (𝑒), 𝑞 ′ )     if pop (𝑞) = (𝑞 ′, [𝑘 1, . . . , 𝑘𝑛 ]) ∧ K 𝑓 (𝑒) ∉ 𝑘 1, . . . , 𝑘𝑛
                         
                         
                         
    qPos(K 𝑓 (𝑒), 𝑞) =
                         
                         
                          1 + qPos(K 𝑓 (𝑒), 𝑞 ′ )    if pop (𝑞) = (𝑞 ′, (foo, 𝑓 ))
                         
                          undef
                                                     if K 𝑓 (𝑒) ∉ Ks (𝑞)

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:51


The function “idle” is 1 if the scheduler is idle and 0 otherwise.
                                                           (
                                                             1 if act = Idle
                              idle(sh, ⟨act, 𝑡, 𝑞𝐺 , 𝑞⟩) =
                                                             0 otherwise
With “unsched,” we check whether there is an unscheduled spawn events in the trace. It is always
either 0 or 1, as there may be at most one unscheduled spawn event in the trace.
                                     (
                                       1 if ∃𝑓 , ℎ. lastEv(sh) = spawnEv(𝑓 , ℎ)
                      unsched(sh) =
                                       0 otherwise
We extend the definition to task markers as follows:
                     
                     
                      1                         if pop (𝑞) = (𝑞 ′, (foo, 𝑓 ))
                     
                      𝑘 + qPos((foo, 𝑓 ), 𝑞 ′ ) if pop (𝑞) = (𝑞 ′, [𝑘])
                     
                     
                     
qPos((foo, 𝑓 ), 𝑞) =
                                            ′
                      1 + qPos((foo, 𝑓 ), 𝑞 )
                     
                                                if pop (𝑞) = (𝑞 ′, (foo′, 𝑓 ′ )) ∧ (foo ≠ foo′ ∨ 𝑓 ≠ 𝑓 ′ )
                     
                      undef                     if (foo, 𝑓 ) ∉ 𝑞
                     
                     
                    pos((foo, 𝑓 ), sh, ⟨act, 𝑡, 𝑞𝐺 , 𝑞⟩)
                      
                      
                       1 + qPos((foo, 𝑓 ), 𝑞) + |Ks (𝑞𝐺 )|    if act ≠ Idle ∧ (foo, 𝑓 ) ∈ 𝑞
                      
                       1 + |Ks (𝑞)| + qPos((foo, 𝑓 ), 𝑞 )
                      
                                                          𝐺   if act ≠ Idle ∧ (foo, 𝑓 ) ∈ 𝑞𝐺
                  =
                 
                 
                  qPos((foo, 𝑓 ), 𝑞) + |Ks (𝑞𝐺 )|             if act = Idle ∧ (foo, 𝑓 ) ∈ 𝑞
                 
                  |Ks (𝑞)| + qPos((foo, 𝑓 ), 𝑞 )
                                              𝐺               if act = Idle ∧ (foo, 𝑓 ) ∈ 𝑞𝐺
We define the order relation > over scheduling distances as the canonical ordering of tuples.
    As can be seen by the distance definition, 𝑑 (K 𝑓 (𝑒), 𝐶, 𝑐) ≥ (1, 0, 0, 𝑐) if K 𝑓 (𝑒) ∈ Ks (trans(𝐶));
otherwise, the distance is undefined. If 𝑑 (K 𝑓 (𝑒), 𝐶, 𝑐) = (1, 0, 0, 𝑐) and 𝑒 ∉ Val, then rule (76) or
rule (74) are the next applicable rules. Likewise, if 𝑑 (K 𝑓 (𝑒), 𝐶, 𝑐) = (1, 1, 0, 𝑐), then the next rule is
one of rule (80), rule (82), or rule (83).
    The distance of a continuation marker being undefined is not a problem in the following discus-
sion. As we will consider the production of new expressions, we need only consider continuation
or task markers that may lead to new expressions via composition rules. These are precisely those
markers that have a defined scheduling distance. We never consider the ordering where either
component is undefined.
    The component 𝑐 in the distance tracks the local computation. Its value is changed depending
on the composition rules. We extend →ct with a new local task counter 𝑐: 𝐶, 𝑐 →ct 𝐶 ′, 𝑐 ′ . Initially,
𝑐 init = 0. The scheduler rules are updated to modify 𝑐 in the following ways: Rule (73) does not
change 𝑐, hence, 𝑐 ′ = 𝑐. Rules (80) to (83), (89) and (90) set 𝑐 = 0, as a task is (re-)started. In rules (78)
and (79), we leave 𝑐 as is: 𝑐 ′ = 𝑐. Finally, rules (74) to (77) decrease 𝑐 by one: 𝑐 ′ = 𝑐 − 1.
   Lemma D.2. Assume an execution sh0, act 0, 𝑡 0, 𝑞𝐺,0, 𝑞 0 →+ct sh1, act 1, 𝑡 1, 𝑞𝐺,1, 𝑞 1 . Further assume
that spawnEv(𝑓 , ℎ) ∈ sh1 , lastEv(sh1 ) ≠ spawnEv(𝑓 , ℎ) and createEv(foo, 𝑓 , 𝑣) ∈ sh1 . Then either
(foo, ℎ) ∈ 𝑞𝐺,1 , (foo, ℎ) ∈ 𝑞 1 , or evalEv(foo, ℎ, 𝑣) ∈ sh1 .
  Proof Sketch. This lemma is proven by a straightforward induction over the scheduling rules.
Once a future is spawned its corresponding task marker is in a queue until its execution begins, in
which case an evaluation event is emitted.                                                        □
  Naturally, the absence of locally infinite computations preclude infinitely decreasing chains of
scheduling distances:

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:52                                                                                               Daniel Drodt


   Lemma D.3. If there are no infinite local computations, then there is no infinitely decreasing chain
of scheduling distances.

   Theorem D.4 (Quiescent Fairness With Counter). Starting from an initial judgement, the
current thread scheduler (adjusted with a counter) is quiescent fair if there are noinfinite localcom-
                                                                                              init
putations: If 𝐶 0 →ct 𝐶 1 →ct 𝐶 2 · · · , then there is a quiescent fair execution ⟨𝜎0 ⟩, [K 𝑓 (𝑒)], ∅ →∗
trans(𝐶 1 ) →∗ trans(𝐶 2 ) →∗ · · · producing the same trace (modulo schedEv events).

   Proof. We must prove two parts: First, for any execution derived by →ct , there exists an execu-
tion using →. Then, we prove the quiescent fairness.
   Existence: We proceed by induction over 𝑛 derivation steps with →ct . As both the semantics
using → and →ct have the same starting point, the base case is free. Assume a derivation in 𝑛 steps
for 𝐶, 𝑐. We apply →ct once more to get 𝐶 ′, 𝑐 ′ . By the induction hypothesis, we have a →-execution
for trans(𝐶). We show via a case distinction over the rule applied to get 𝐶 ′, 𝑐 ′ that a derivation for
trans(𝐶 ′ ) exists. Let in the following 𝐶 = sh, ⟨act, 𝑡, 𝑞𝐺 , 𝑞⟩.
Rule (73) The task marker (foo, 𝑓 ) is pushed to the end of the local queue 𝑞 and appends a schedule
     event and a repetition of sh’s last state to sh. By the definition of trans, this has no effect on
     trans(𝐶). Thus, trans(𝐶) is already the required →-configuration.
Rule (74): Then rule (64) is applicable.
                                       D The resulting traces  E are equivalent according
                                                                                     D          to “trans.” Ad- E
     ditionally, per definition, trans( [K 𝑓 (𝑒), 𝑘], 𝑡, 𝑞𝐺 , 𝑞 ) differs from trans( [K 𝑓 (𝑒 ′ ), 𝑘], 𝑡, 𝑞𝐺 , 𝑞 )
     only by K 𝑓 (𝑒) being replaced by K 𝑓 (𝑒 ′ ). This is the same change done by rule (64). Thus, we
     have a →-derivation.
Rule (75): Then rule (65) is applicable, since its preconditions  D      follow
                                                                            E from    those
                                                                                          of rule (75).
     The old configuration must be of the form trans( [𝑘], 𝑡, 𝑞𝐺 , 𝑞 ) = [𝑘], 𝑄 . The resulting
     configuration is:
                                                               
                                             [K 𝑓 (𝑒 ′ ), 𝑘], 𝑄
                                 D                         E
     This is the same as trans( [K 𝑓 (𝑒 ′ ), 𝑘], 𝑡, 𝑞𝐺 , 𝑞 ), as only the active task’s stack is removed
     and then the same stack with new top element K 𝑓 (𝑒 ′ ) is added; this is equivalent to the active
     task [K 𝑓 (𝑒 ′ ), 𝑘]. Similarly, the traces in the resulting configuration match according to trans.
Rule (76): Then rule (66) is applicable. For the same reasons as in rule (75), the resulting configu-
     rations match.
Rule (77): Then rule (67) is applicable. Clearly, trans(𝐶 ′ ) matches the result of rule (67).
Rule (78): Then rule (68) is applicable. The resulting configurations match per the definition of
     “trans.”
Rule (79): Then rule (69) is applicable. The resulting configurations clearly agree.
Rule (80) moves the first stack from 𝑞𝐺 to the active           slot. Then, rule (71) is applicable. Since
     sh in unchanged, the result trans(𝐶) = sh, [K (𝑒), 𝑘], 𝑄 \ {[K (𝑒), 𝑘]} is the desired →-
                                                              𝑓                𝑓

     derivation.
Rule (81): Since the preconditions of rule (81) imply those of rule (70), the latter is applicable
     on configuration trans(sh), trans(⟨Idle,       𝑡, 𝑞𝐺 , 𝑞⟩) = trans(sh), (Idle, 𝑄), resulting in configu-
     ration trans(sh), [K 𝑓 (𝑒 ′ )], 𝑄 . Since trans0 (𝑞𝐺 ) = trans0 (𝑞𝐺′ ), this is exactly the translation
                                        
     trans(𝐶 ′ ).
Rule (82): Same argument as for rule (80).
Rule (89): Same argument as for rule (81).

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:53


Rule (83): Similar to the cases for rules (80) and (82) but with 𝑞 and 𝑞 ′ substituted for 𝑞𝐺 and 𝑞𝐺′ ,
      respectively.
Rule (90): Analogous to the cases for rules (81) and (89), except with the observation that trans0 (𝑞) =
      trans0 (𝑞 ′ ).
Mapping: As in [24], we define a mapping between configurations in → and →ct for a fixed
→ct -execution. Assume such a →ct -execution
                                        𝐶 0ct →ct 𝐶 1ct →+ct 𝐶𝑛ct →ct · · ·                                    (91)
For most →ct -applications, there is a direct one-to-one correspondence to a →-step. However,
rule (73), which schedules a future, has no equivalent. For this rule, we have no step (i.e., a no-op)
on the →-side. Hence the change from at least one step (→+ct ) to the reflexive-transitive closure
(→∗ ). Then, for the execution (91) there is a →-execution
                                           𝐶 0′ → 𝐶 1′ →∗ 𝐶𝑚
                                                           ′
                                                             → ···                                             (92)
  Then we can define a mapping 𝜋 : N → N such that the execution (92) can be written as
                         trans(𝐶𝜋ct(0) ) → trans(𝐶𝜋ct(1) ) →+ trans(𝐶𝜋ct(𝑚) ) → · · ·                          (93)
namely: 𝜋 (𝑖) = 𝑖 + #(applications of rule (73)).
   Fairness: Assume a →ct -execution like (91) and the corresponding →-execution (93). We need
to show that the letter is quiescent fair, i.e.:
            
  ∀𝑚, 𝑒, 𝑓 . ∀𝑛 > 𝑚.
                                                                                                             
                ∃𝑄. trans( act 𝜋 (𝑛) , 𝑡𝜋 (𝑛) , 𝑞𝐺,𝜋 (𝑛) , 𝑞𝜋 (𝑛) ) = (Idle, 𝑄) ⇒ K 𝑓 (𝑒) ∈ enabled(𝐶𝜋 (𝑛) )
                                                                                                    
                  ⇒ ∃𝑛 ′ > 𝑚. K 𝑓 (𝑒) ∈ Ks trans( act 𝜋 (𝑛′ ) , 𝑡𝜋 (𝑛′ ) , 𝑞𝐺,𝜋 (𝑛′ ) , 𝑞𝜋 (𝑛′ ) )

   Let 𝑚, 𝑒, 𝑓 be arbitrary but fixed and assume that K 𝑓 (𝑒) is enabled in 𝐶𝜋 (𝑛) whenever there is
no active task in 𝐶𝜋 (𝑛) ’s translation. We need to show that eventually, a scheduler rule occurs
that produces 𝑒. We consider each possible rule to yield K 𝑓 (𝑒) ∈ enabled(𝐶𝜋 (𝑛) ). There are three
possibilities for add K 𝑓 (𝑒): (i) it is the consequence of evaluating an expression 𝑒 ′ in rule (64) or
rule (67); (ii) it is the result of evaluating the first step of a scheduled task (rule (70)); or (iii) it is the
result of evaluating a synchronous call (rule (65)) or a local future (rule (66)). We show fairness
by proving that either 𝑒 is produced, the quiescent fairness precondition does not hold, or the
scheduling distance for expression 𝑒 ′ or (foo, 𝑓 ) decreases. By Lemma D.3, there is no infinitely
decreasing chain of distances, thus 𝑒 ′ or (foo, 𝑓 ) are eventually scheduled, leading to 𝑒 being
produced.
   We assume the quiescent fairness precondition; hence, K 𝑓 (𝑒) is reachable. Now there are two
possible cases: (case Produce) expression 𝑒 is produced or (case Decrease) the scheduling distance
of 𝑒 ′ or (foo, 𝑓 ) decreases.
Rule (64): We restate rule (64) with the translated configuration
                 trans(𝐶𝜋 (𝑛) ) = trans(sh𝜋 (𝑛) ), trans( act 𝜋 (𝑛) , 𝑡𝜋 (𝑛) , 𝑞𝐺,𝜋 (𝑛) , 𝑞𝜋 (𝑛) ) :
                                                                        h            i 
                       trans( act 𝜋 (𝑛) , 𝑡𝜋 (𝑛) , 𝑞𝐺,𝜋 (𝑛) , 𝑞𝜋 (𝑛) ) = K 𝑓 (𝑒 ′ ), 𝑘 , 𝑄
                             𝜎 = last(trans(sh𝜋 (𝑛) )) 𝜏 · K 𝑓 (𝑒) ∈ val𝜎 (𝑒 ′ )
                                                                                𝑓

                              𝜌 concretizes 𝜏 wf (trans(sh𝜋 (𝑛) ) ∗∗ 𝜌 (𝜏))                                    (94)
                                                                   h          i 
                         trans(𝐶𝜋 (𝑛) ) → trans(sh𝜋 (𝑛) ) ∗∗ 𝜌 (𝜏), K 𝑓 (𝑒), 𝑘 , 𝑄

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:54                                                                                                Daniel Drodt


     In this case, because the translated configuration has an active task, so does the configuration
     𝐶𝜋 (𝑛) and the top of this task, K 𝑓 (𝑒 ′ ) can be evaluated yielding a well-formed trace. Hence,
     only the rules (73) and (74) can be applied; all others have either an idle worker or they
     cannot evaluate the top of the active task.
     If we can apply rule (73), then there must be a spawn event that has not yet been responded
     too and the distance is of the form (𝑘, 0, 1, 𝑐), which is reduced by rule (73) to (𝑘, 0, 0, 𝑐). So
     we have the case Decrease.
     Otherwise, we have 𝑑 (K 𝑓 (𝑒 ′ ), 𝐶𝜋 (𝑛) , 𝑐 𝜋 (𝑛) ) = (𝑘, 0, 0, 𝑐 𝜋 (𝑛) ) for some 𝑘 ≥ 1. Either 𝑘 = 1,
     which implies that 𝑒 ′ is the next expression to be executed and is not suspended. Then, clearly,
     rule (64) is applicable, yielding 𝑒 (Produce).
     If 𝑘 > 1, 𝑒 ′ is not evaluated by this application of rule (74). But we obtain case Decrease by
     the observation that 𝑑 (K 𝑓 (𝑒 ′ ), 𝐶𝜋 (𝑛)+1, 𝑐 𝜋 (𝑛)+1 ) = (𝑘, 0, 0, 𝑐 𝜋 (𝑛) − 1).
Rule (65) executes a synchronous call. We restate it in the translated setting:
                                                                   
           trans( act 𝜋 (𝑛) , 𝑡𝜋 (𝑛) , 𝑞𝐺,𝜋 (𝑛) , 𝑞𝜋 (𝑛) ) = [𝑘], 𝑄    𝜎 = last(sh𝜋 (𝑛) ) 𝑓 ∈ FId
                        lookup(foo) = fn foo(𝑥) 𝑒 𝜏 · K 𝑓 (𝑒) ∈ val𝜎 (fn foo(𝑥) 𝑒 ′ )
                                                                           𝑓

                               𝜌 concretizes 𝜏 wf (trans(sh𝜋 (𝑛) ) ∗∗ 𝜌 (𝜏))                                 (95)
                                                                                    
                          trans(𝐶𝜋 (𝑛) ) → trans(sh𝜋 (𝑛) ) ∗∗ 𝜌 (𝜏), [K 𝑓 (𝑒), 𝑘], 𝑄

     By the same argument as for rule (64), only the rules rules (73) and (75) are applicable. The
     exact same argument further gives us that we either Produce 𝑒 or Decrease the distance.
Rule (66) executes a local future. We restate rule (66) in our translated setting:
                                                                  
          trans( act 𝜋 (𝑛) , 𝑡𝜋 (𝑛) , 𝑞𝐺,𝜋 (𝑛) , 𝑞𝜋 (𝑛) ) = [𝑘], 𝑄   𝜎 = last(sh𝜋 (𝑛) ) 𝑓 ∈ FId
                lookup(foo) = async fn foo(𝑥) 𝑒 𝜏 · K 𝑓 (𝑒) ∈ val𝜎 (async fn foo(𝑥) 𝑒 ′ )
                                                                           𝑓

                            𝜌 concretizes 𝜏 wf (trans(sh𝜋 (𝑛) ) ∗∗ 𝜌 (𝜏))                                    (96)
                                                                                 
                       trans(𝐶𝜋 (𝑛) ) → trans(sh𝜋 (𝑛) ) ∗∗ 𝜌 (𝜏), [K 𝑓 (𝑒), 𝑘], 𝑄

     We repeat the argument for rule (65) but with rules (73) and (76) applicable.
Rule (67) removes the top continuation of the active task’s stack if its computation is completed.
     Restated in our terms, the rule goes:
                                                                                      
     trans( act 𝜋 (𝑛) , 𝑡𝜋 (𝑛) , 𝑞𝐺,𝜋 (𝑛) , 𝑞𝜋 (𝑛) ) = [K 𝑓 (𝑒 ′′ ), K 𝑓 (𝑒 ′ ), 𝑘], 𝑄   𝜎 = last(sh𝜋 (𝑛) )
                 𝜏 · K(𝑒) ∈ val𝜎 (𝑒 ′ )
                                 𝑓
                                          𝜌 concretizes 𝜏   wf (trans(sh𝜋 (𝑛) ) ∗∗ 𝜌 (𝜏))                    (97)
                                                                              
                             trans(𝐶𝜋 (𝑛) ) → trans(sh𝜋 (𝑛) ), [K 𝑓 (𝑒), 𝑘], 𝑄

     Again, the same argument as for rules (64) to (66) but now rules (73) and (77) can be applied.
Rule (68): Has no effect on the set of enabled continuations. Thus, it cannot have produced 𝑒 ′ .
Rule (69): Has no effect on the set of enabled continuations. Thus, it cannot have produced 𝑒 ′ .
Rule (70) executes a spawned future. We restate rule (70) in our translated setting:
             trans( act 𝜋 (𝑛) , 𝑡𝜋 (𝑛) , 𝑞𝐺,𝜋 (𝑛) , 𝑞𝜋 (𝑛) ) = (Idle, 𝑄) 𝜎 = last(sh𝜋 (𝑛) ) 𝑓 ∈ FId
                lookup(foo) = async fn foo(𝑥) 𝑒 𝜏 · K 𝑓 (𝑒) ∈ val𝜎 (async fn foo(𝑥) 𝑒 ′ )
                                                                           𝑓

                                 𝜌 concretizes 𝜏 wf (trans(sh𝜋 (𝑛) ) ∗∗ 𝜌 (𝜏))                               (98)
                                                                                  
                           trans(𝐶𝜋 (𝑛) ) → trans(sh𝜋 (𝑛) ) ∗∗ 𝜌 (𝜏), K 𝑓 (𝑒) , 𝑄

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                            ZZZ:55


     Since the evaluation of async fn foo(𝑥) 𝑒 starts with an evaluation event, well-formedness
     gives us that a spawn event for 𝑓 and foo exists in trans(sh𝜋 (𝑛) ) but no evaluation event for 𝑓
     and foo. If lastEv trans(sh𝜋 (𝑛) ) is a spawn event, we apply rule (73) and start our argument
     on its result.
     Lemma D.2 gives us that (foo, 𝑓 ) is in one of the scheduler’s queues and its distance is greater
     or equal to (1, 1, 0, 𝑐 𝜋 (𝑛) ). We consider each case of the application 𝐶𝜋 (𝑛) →ct 𝐶𝜋 (𝑛)+1 .
     Rule (73) can only be applied to schedule a task with a different future identifier. The distance
       is, hence, 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛) , 𝑐 𝜋 (𝑛) ) = (𝑘, 𝑖, 1, 𝑐 𝜋 (𝑛) ) for some 𝑘 ≥ 1 and 𝑖 ∈ {0, 1} before
       the step and 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛)+1, 𝑐 𝜋 (𝑛) ) = (𝑘, 𝑖, 0, 𝑐 𝜋 (𝑛) ) afterwards. Thus, the scheduling
       distance decreases (Decrease).
     Rule (74): Again we have case Decrease, as the distance goes from 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛) , 𝑐 𝜋 (𝑛) ) =
       (𝑘, 0, 0, 𝑐 𝜋 (𝑛) ), with 𝑘 > 1, to 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛)+1 ) = (𝑘, 0, 0, 𝑐 𝜋 (𝑛) − 1).
     Rule (75) evaluates a synchronous call. Then, case Decrease holds, as the distance goes from
       𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛) , 𝑐 𝜋 (𝑛) ) = (𝑘, 0, 0, 𝑐 𝜋 (𝑛) ), for some 𝑘 > 1, to 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛)+1, 𝑐 𝜋 (𝑛) ) =
       (𝑘, 0, 0, 𝑐 𝜋 (𝑛) − 1).
     Rule (76): Same argument as for rule (75).
     Rule (77): Before the application, we have 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛) , 𝑐 𝜋 (𝑛) ) = (𝑘, 0, 0, 𝑐 𝜋 (𝑛) ) for some
       𝑘 > 1. Afterwards, 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛)+1, 𝑐 𝜋 (𝑛)+1 ) = (𝑘, 0, 0, 𝑐 𝜋 (𝑛) − 1), which is a decrease of
       the scheduling distance (Decrease).
     Rule (78): Then the scheduling distance decreases from 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛) ) = (𝑘, 0, 0, 𝑐 𝜋 (𝑛) ),
       for some 𝑘 > 1, to 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛)+1 ) = (𝑘 − 1, 1, 0, 𝑐 𝜋 (𝑛) − 1). We have Decrease.
     Rule (79): Same argument as for rule (78).
     Rule (80): Before the application, we have 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛) , 𝑐 𝜋 (𝑛) ) = (𝑘, 1, 0, 𝑐 𝜋 (𝑛) ) for some
       𝑘 > 1. Afterwards, we have 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛)+1, 𝑐 𝜋 (𝑛) ) = (𝑘, 0, 0, 0), i.e., a decrease of the
       scheduling distance (Decrease).
     Rule (81): Either 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛) , 𝑐 𝜋 (𝑛) ) = (1, 1, 0, 𝑐 𝜋 (𝑛) ), in which case the correct continu-
       ation is produced (Produce), or the distance is (𝑘, 1, 0, 𝑐 𝜋 (𝑛) ) with 𝑘 > 1 and the application
       reduces the scheduling distance (Decrease) to 𝑑 ((foo, 𝑓 ), 𝐶𝜋 (𝑛)+1, 𝑐 𝜋 (𝑛)+1 ) = (𝑘, 0, 0, 0).
     Rule (82): Same argument as for rule (80).
     Rule (89): Same argument as for rule (81).
     Rule (83): Same as for rules (80) and (82).
     Rule (90): Same argument as for rules (81) and (89).
Rule (71): We follow the same argument as for rule (70) but now with a task [𝑘] rather than a task
     marker.                                                                                                        □

E   Relation of Quiescent and Tokio Fairness
   Proof of Theorem 5.9. As established in Appendix D, we know that the current thread runtime
is quiescent fair. We show that the premisses of Tokio fairness are stronger than those of quiescent
fairness and the conclusion follows from that of quiescent fairness. Since the first assumption of
Definition 5.8 is absent from the definition of quiescent fairness, we can add it without altering the
conclusion.
   The second premiss is stronger than the assumption of locally finite computations: For quiescent
fairness we only assume that each task completes or suspends in a final amount of steps; we do not
require a fixed upper bound for all tasks.
   Finally, note that the conclusions of both definitions are similar except that ∃𝑛 ′ > 𝑚. 𝑒 ∈
newConts(𝐶𝑛′ , 𝐶𝑛′ +1 ) in quiescent fairness is strengthened to ∃𝑛 ′ . 𝑚 < 𝑛 ′ ≤ 𝑚 + 𝐷 max ∧ 𝑒 ∈
newConts(𝐶𝑛′ , 𝐶𝑛′ +1 ) in Tokio fairness. Hence, we need to show that the 𝑛 ′ we find for quiescent

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:56                                                                                               Daniel Drodt


fairness is always less than 𝑚 + 𝐷 max . The distance function defined in Appendix D can be used to
find 𝐷 max .
   We note that, because the local computations must complete within 𝑃max steps, we can make all
components of the scheduling distance non-negative by adding 𝑃 max to the final component. Then,
for a scheduling distance (𝑎, 𝑏, 𝑐, 𝑑) we construct 𝐷 ∈ N by
                                               𝐷 := 𝑎 ◦ 𝑏 ◦ 𝑐 ◦ 𝑑 ′
where ◦ denotes concatenation of digits and 𝑑 ′ is 𝑑 + 𝑃max extended with leading zeroes to the
number of digits of 𝑃max . For example, if 𝑃max = 100, the scheduling distance (32, 1, 0, −64) is
mapped to 𝐷 0 = 3210036. As can be easily seen, this mapping preserves the order over distances.
   By definition of the scheduling distance (Definition D.1), the first component is bounded by the
sizes of both queues plus one: 0 ≤ 𝑎 ≤ |Ks (𝑞) | + |Ks (𝑞𝐺 ) | + 1; because the number of tasks is
less than 𝑇max , we have 𝑎 ≤ 𝑇max + 1. The second and third components are either 0 or 1; the last
component is 0 ≤ 𝑑 ≤ 𝑃max . Thus, all distance numbers 𝐷 for all expressions at all points are less
than or equal to
                                 𝐷 max := (𝑇max + 1) ◦ 1 ◦ 1 ◦ 𝑃max .                             □
  As the proof above uses no properties of the current thread runtime besides its quiescent fairness
and the existence of a scheduling distance, the following corollary follows immediately:
  Corollary E.1. A quiescent fair scheduler, where there is a scheduling distance 𝑑 (K 𝑓 (𝑒), 𝐶, 𝑐) such
that, for each continuation marker K 𝑓 (𝑒) that is in enabled(𝐶𝑖 ) for some configuration in an execution,
the distance for K 𝑓 (𝑒) is either decreased by each step or 𝑒 is produced and the distance is bounded by
a maximum, is also Tokio fair.
    It is unknown whether there exist any quiescent fair schedulers that are not Tokio fair.

F    Auxiliary Definitions and Theorems for DL
    Definition F.1 (Domain). We fix the domain D 𝐴 of each sort 𝐴 as follows:
     • D bool = {tt, ff },
     • D int = Z,
     • D Field an infinite set of field identifiers,
     • D Place𝐴 = lim𝑛→∞ D𝑛Place𝐴 where
       – D0Place𝐴 = {Place(x) | x : 𝐴 ∈ ProgVSym} and
             Place𝐴
       – D𝑖+1        = D𝑖Place𝐴 ∪ {ArrPlace(𝑝, 𝑛) | 𝑝 ∈ D𝑖Place𝐴 , 𝑛 ∈ N} ∪ {FldPlace(𝑝, 𝑓 ) | 𝑝 ∈
          D𝑖Place𝐴 , 𝑓 ∈ D Field }
              𝑠
     • D Ref 𝐴 = {SharedRef (𝑎) | 𝑎 ∈ D 𝐴 } for all sorts 𝐴,
              𝑚
     • D 𝐴 = {MutRef (𝑝) | 𝑝 ∈ D Place𝐴 } for all sorts 𝐴,
          Ref

     • D (𝐴1,...,𝐴𝑛 ) = D 𝐴1 × · · · D 𝐴𝑛 ,
     • D [𝐴;𝑛] = {Array(𝑑𝑛 , . . . , 𝑑𝑛 ) | 𝑑 1, . . . , 𝑑𝑛 ∈ D 𝐴 },
     • and domains for each datatype declared in the program.
  Definition F.2 (Correspondence of RustyDL Domain and LAGC Values). Let D be a RustyDL Domain
and 𝜎 an LAGC state. We define the binary relation ∼𝜎 ⊆ D × Val (pronounced “𝑑 corresponds to 𝑣
w.r.t. 𝜎”) inductively as follows:
  (1) 𝑛 ∼𝜎 𝑛 for each 𝑛 ∈ Z,
  (2) tt ∼𝜎 tt and ff ∼𝜎 ff,
  (3) SharedRef (𝑎) ∼𝜎 Ref 𝑠x (𝑏) for each x ∈ Var and for all 𝑏 ∈ BId, where 𝑎 ∼𝜎 𝜎 (x),
  (4) MutRef (𝑝) ∼𝜎 Ref 𝑚                         Place𝐴 , 𝑏 ∈ BId, 𝑝 ′ ∈ Place iff 𝑝 and 𝑝 ′ correspond,
                           𝑝 ′ (𝑏) for each 𝑝 ∈ D

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                              ZZZ:57


    (5) (𝑑 1, . . . , 𝑑𝑛 ) ∼𝜎 (𝑣 1, . . . , 𝑣𝑛 ) iff 𝑑 1 ∼𝜎 𝑣 1, . . . , 𝑑𝑛 ∼𝜎 𝑣𝑛 ,
    (6) Array(𝑑 1, . . . , 𝑑𝑛 ) ∼𝜎 [𝑣 1, . . . , 𝑣𝑛 ] iff 𝑑 1 ∼𝜎 𝑣 1, . . . , 𝑑𝑛 ∼𝜎 𝑣𝑛 .
   Definition F.3 (Correspondence of RustyDL States and LAGC States). Let K = (D, 𝐼, S, 𝜌) be
RustyDL Kripke structure, 𝑠 ∈ S a RustyDL state, and 𝜎 an LAGC state. We define the binary
relation ∼ (pronounced “corresponds”) as follows: 𝑠 ∼ 𝜎 iff for all x : 𝐴 ∈ ProgVSym such that
x ∈ dom(𝜎), we have 𝑠 (x) ∼𝜎 𝜎 (x).
    We fix some interpretations of functions and relations:
     • 𝐼 (+) (𝑛, 𝑚) = 𝑛 + 𝑚 with 𝑛, 𝑚 ∈ D int (similar for all integer functions),
     • 𝐼 (sref ) (𝑑) = SharedRef (𝑑) with 𝑑 ∈ D,
     • 𝐼 (mref ) (𝑝) = MutRef (𝑝),
     • 𝐼 (∗𝑠 ) (SharedRef (𝑑)) = 𝑑,
     • 𝐼 (inU32) = {𝑛 ∈ N | 0 ≤ 𝑛 < 232 }.

G     Additional Soundness Proofs of Dynamic Logic Calculus Rules
   Theorem G.1 (Soundness of rule ifElseSplit). Let Γ, Δ ∈ 2DLFml be sets of formulas, U ∈ Upd
be an update, se a literal or a program variable of type bool, {be0 } and {be1 } be block expressions,
𝜋 if se {be0 } else {be1 } 𝜔 be a program fragment, and 𝜙 ∈ DLFml be a formula. If
                                  |= Γ, {U}(se  TRUE) =⇒ {U}⟨𝜋 {be0 } 𝜔⟩𝜙, Δ
                                  |= Γ, {U}(se  FALSE) =⇒ {U}⟨𝜋 {be1 } 𝜔⟩𝜙, Δ
then the following holds:
                                    |= Γ =⇒ {U}⟨𝜋 if se {be0 } else {be1 } 𝜔⟩𝜙, Δ.
    Proof. We assume
                                  |= Γ, {U}(se  TRUE) =⇒ {U}⟨𝜋 {be0 } 𝜔⟩𝜙, Δ                                     (99)
                                  |= Γ, {U}(se  FALSE) =⇒ {U}⟨𝜋 {be1 } 𝜔⟩𝜙, Δ                                   (100)
It is sufficient to show
                                      (K, 𝑠 1, 𝛽) |= ⟨𝜋 if se {be0 } else {be1 } 𝜔⟩𝜙 .                           (101)
We infer from the assumptions that
                                       (K, 𝑠 1, 𝛽) |= se  TRUE → ⟨𝜋 {be0 } 𝜔⟩𝜙                                  (102)
                                       (K, 𝑠 1, 𝛽) |= se  FALSE → ⟨𝜋 {be1 } 𝜔⟩𝜙                                 (103)
   We know that if se {be0 } else {be1 } is the active expression. By the construction of the local
evaluation rules, we know that it is also the next (sub-)expression to be evaluated and added to the
trace sh. Thus, we can use the local evaluation. We split over the structure of se.
   Case G.1 (se ∈ Val). Then se is either true or false. We cover the former case as both are analogous.
se = true: Then, val𝜎1 (true) = {⟨𝜎1 ⟩ · K(tt)}. From that we infer
                           val𝜎1 (if true{be0 } else {be1 })
                                = {𝜏 · K(if 𝑒 {be0 } else {be1 }) | 𝜏 · K(𝑒) ∈ val𝜎1 (true)}
                                = {⟨𝜎1 ⟩ · K(if tt {be0 } else {be1 })}
Further, val𝜎1 (if tt {be0 } else {be1 }) = {⟨𝜎1 ⟩ · K({be0 })}. Hence, the only possible composition is
           ⟨𝜎1 ⟩, K(if true{be0 } else {be1 }) → ⟨𝜎1 ⟩, K(if tt {be0 } else {be1 }) → ⟨𝜎1 ⟩, K({be0 })

                     ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:58                                                                                               Daniel Drodt


which ends in the start configuration of Tr(𝜋 {be0 } 𝜔, 𝜎1 ), i.e., we have the relation Tr({be0 }, 𝜎1 ) ⋟
Tr(if se {be0 } else {be1 }, 𝜎1 ). Thus, we simplify (101) to
                                           (K, 𝑠 1, 𝛽) |= ⟨𝜋 {be0 } 𝜔⟩𝜙 .                                  (104)
   Assumption (102) can be simplified, by the definition of the implication, to
                         (K, 𝑠 1, 𝛽) ⊭ se  TRUE       or   (K, 𝑠 1, 𝛽) |= ⟨𝜋 {be0 } 𝜔⟩𝜙                   (105)
Since se = true, we know that (K, 𝑠 1, 𝛽) |= se  TRUE, which means with (105) and Lemma 6.11
that the goal (104) holds.
  Case G.2 (se ∈ Var). Let 𝑣 = 𝜎1 (se). Since se is not symbolic, 𝑣 ∈ Val. Then val𝜎1 (se) = {⟨𝜎1 ⟩ ·
K(𝑣)}, because se is of type bool, which implements Copy. We present the case for 𝑣 = tt, as the
case 𝑣 = ff is similar. Then the local evaluation yields
                         val𝜎1 (if se {be0 } else {be1 })
                             = {𝜏 · K(if 𝑒 {be0 } else {be1 }) | 𝜏 · K(𝑒) ∈ val𝜎1 (se)}
                             = {⟨𝜎1 ⟩ · K(if tt {be0 } else {be1 })}
As in case G.1, we know that the only possible composition is
         ⟨𝜎1 ⟩, K(if se {be0 } else {be1 }) → ⟨𝜎1 ⟩, K(if tt {be0 } else {be1 }) → ⟨𝜎1 ⟩, K({be0 }) .
By the same argument as in case G.1, goal (101) holds.                                                         □

                                       Γ =⇒ {U}{x := y ∥ y := 𝑐}⟨𝜋 () 𝜔⟩𝜙, Δ
                              move
                                            Γ =⇒ {U}⟨𝜋 x = y 𝜔⟩𝜙, Δ
                              y : 𝐴, 𝐴 is not Copy, and 𝑐 : 𝐴 a fresh constant
  Theorem G.2 (Soundness of Rule move). Let Γ, Δ ∈ 2DLFml be sets of formulas, U ∈ Upd be an
update, x be a program variable whose type is not Copy and not a mutable reference, y be a program
variable of the same type as x, 𝑐 a constant of y’s type that does not occur in Γ, Δ, 𝜙, or U, 𝜋 x = y 𝜔
be a program fragment, and 𝜙 ∈ DLFml be a formula. If
                                 |= Γ =⇒ {U}{x := y ∥ y := 𝑐}⟨𝜋 () 𝜔⟩𝜙, Δ
then the following holds:
                                         |= Γ =⇒ {U}⟨𝜋 x = y 𝜔⟩𝜙, Δ.
   Proof. We assume
                                 |= Γ =⇒ {U}{x := y ∥ y := 𝑐}⟨𝜋 () 𝜔⟩𝜙, Δ
   It is sufficient to show
                                           (K, 𝑠 1, 𝛽) |= ⟨𝜋 x = y 𝜔⟩𝜙 .                                   (106)
We infer from the assumptions that
                                     (K, 𝑠 1, 𝛽) |= {x := y ∥ y := 𝑐}⟨𝜋 () 𝜔⟩𝜙                             (107)
Let 𝑠 2 = val K,𝑠,𝛽 (x := y ∥ y := 𝑐) (𝑠 1 ). Then we simplify equation (107) to
                                             (K, 𝑠 2, 𝛽) |= ⟨𝜋 () 𝜔⟩𝜙                                      (108)
Let 𝑣 = 𝜎1 (y). Following Section 3.1.1 and then rule (5) we have the local evaluation
                 val𝜎1 (x = y) = {𝜏 · K(x = 𝑒) | 𝜏 · K(𝑒) ∈ val𝜎1 (y)} = {⟨𝜎1 ⟩ · K(x = 𝑣)}                (109)

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:59


The local evaluation rule (19) further yields val𝜎1 (x = 𝑣) = {⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ 𝑣] · K(())}. Therefore,
the only possible composition is
              ⟨𝜎1 ⟩, K(𝜋 x = y 𝜔) → ⟨𝜎1 ⟩, K(𝜋 x = 𝑣 𝜔) → ⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ 𝑣], K(𝜋 () 𝜔)
Which implies that Tr(𝜋 () 𝜔, 𝜎1 [x ↦→ 𝑣]) ⋟ Tr(𝜋 x = y 𝜔, 𝜎1 ). By Lemma 6.11, we know that goal
(106) holds if (K, 𝑠 3, 𝛽) |= ⟨𝜋 () 𝜔⟩𝜙 holds, with 𝑠 3 = val K,𝑠2,𝛽 (x := 𝑣) (𝑠 1 ). Assumption (108) gives
us a stronger formula than this: It gives us validity of ⟨𝜋 () 𝜔⟩𝜙 with no information about y′𝑠
value. Thus, by (108), we are done.                                                                       □

                              Γ, {U}inU32(se1 + se2 ) =⇒ {U}{x := se1 + se2 }⟨𝜋 () 𝜔⟩𝜙, Δ
                              Γ, {U}¬inU32(se1 + se2 ) =⇒ {U⟨𝜋 panic! () 𝜔⟩𝜙 }, Δ
            assignAddU32
                                             Γ =⇒ {U}⟨𝜋 x = se1 + se2 𝜔⟩𝜙, Δ
  Theorem G.3 (Soundness of Rule assignAddU32). Let Γ, Δ ∈ 2DLFml be sets of formulas, U ∈
Upd be an update, x be a program variable of type u32, se1, se2 either literals or program variables of
type u32, 𝜋 x = se1 + se2 𝜔 be a program fragment, and 𝜙 ∈ DLFml be a formula. If
                    |= Γ, {U}inU32(se1 + se2 ) =⇒ {U}{x := se1 + se2 }⟨𝜋 () 𝜔⟩𝜙, Δ
                    |= Γ, {U}¬inU32(se1 + se2 ) =⇒ {U⟨𝜋 panic! () 𝜔⟩𝜙 }, Δ
then the following holds:
                                   |= Γ =⇒ {U}⟨𝜋 x = se1 + se2 𝜔⟩𝜙, Δ.
  Proof. We only present the case where se1, se2 ∈ Val. The other two cases are handled as in the
above proofs.
  We need to show
                                      (K, 𝑠 1, 𝛽) |= ⟨𝜋 x = se1 + se2 𝜔⟩𝜙 .                                   (110)
We infer from the assumptions that
                       (K, 𝑠 1, 𝛽) |= inU32(se1 + se2 ) → {x := se1 + se2 }⟨𝜋 () 𝜔⟩𝜙                          (111)
                       (K, 𝑠 1, 𝛽) |= ¬inU32(se1 + se2 ) → ⟨𝜋 panic! () 𝜔⟩𝜙                                   (112)
Let 𝜎1 be an LAGC state such that 𝑠 1 ∼ 𝜎1 . Further, let 𝑛 = val K,𝑠1,𝛽 (se1 ) + val K,𝑠1,𝛽 (se2 ). By the
semantics if inU32, we know that (K, 𝑠 1, 𝛽) |= inU32(se1 + se2 ) iff 0 ≤ 𝑛 < 232 .
  Case G.3 (inU32(𝑛) holds). Then the first case of rule (12) holds and the evaluation yields
                                       val𝜎1 (se1 + se2 ) = {⟨𝜎1 ⟩ · K(𝑛)}
which makes the local evaluation of the assignment
                            val𝜎1 (x = se1 + se2 ) = {⟨𝜎1 ⟩ · K(x = 𝑛)}                                       (113)
                                    val𝜎1 (x = 𝑛) = {⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ 𝑛] · K(())}                             (114)
Hence, the only possible composition is
                 ⟨𝜎1 ⟩, K(x = se1 + se2 ) → ⟨𝜎1 ⟩, K(x = 𝑛) → ⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ 𝑛], K(())
Since 𝑠 2 ∼ 𝜎2 , Tr(𝜋 () 𝜔, 𝜎2 ) ⋟ Tr(𝜋 x = se1 + se2 𝜔, 𝜎1 ). Hence, with Lemma 6.11, we simplify the
goal to
                                          (K, 𝑠 2, 𝛽) |= ⟨𝜋 () 𝜔⟩𝜙                               (115)
As (K, 𝑠 1, 𝛽) |= inU32(se1 + se2 ), we can simplify assumption (111) to (115)

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:60                                                                                               Daniel Drodt


   Case G.4 (inU32(𝑛) does not hold). Then the second case of rule (12) holds and the evaluation
yields
                               val𝜎1 (se1 + se2 ) = {⟨𝜎1 ⟩ · K(panic! ())}
And val𝜎1 (panic! ()) = {⟨𝜎1 ⟩ ↷ panicEv() ↷ 𝜎1 · K(())}, which means that we have the suf-
fix relation Tr(𝜋 panic! () 𝜔, 𝜎1 ) ⋟ Tr(𝜋 se1 + se2 𝜔). With (K, 𝑠 1, 𝛽) |= ¬inU32(𝑛), we simplify
assumption (112) to
                                     (K, 𝑠 1, 𝛽) |= ⟨𝜋 panic! () 𝜔⟩𝜙                          (116)
which, by Lemma 6.11, gives us (110).
                                                                                                               □

                                            Γ =⇒ {U}{x := sref (y)}⟨𝜋 () 𝜔⟩𝜙, Δ
                          borrowShared
                                                 Γ =⇒ {U}⟨𝜋 x = &y 𝜔⟩𝜙, Δ
  Theorem G.4 (Soundness of Rule borrowShared). Let Γ, Δ ∈ 2DLFml be sets of formulas, U ∈
Upd be an update, x be a program variable of some immutable reference type, y a program variable,
𝜋 x = &y 𝜔 be a program fragment, and 𝜙 ∈ DLFml be a formula. If
                                   |= Γ =⇒ {U}{x := sref (y)}⟨𝜋 () 𝜔⟩𝜙, Δ
then the following holds:
                                       |= Γ =⇒ {U}⟨𝜋 x = &y 𝜔⟩𝜙, Δ.
   Proof. We assume
                                   |= Γ =⇒ {U}{x := sref (y)}⟨𝜋 () 𝜔⟩𝜙, Δ                                  (117)
We only need to show
                                          (K, 𝑠 1, 𝛽) |= ⟨𝜋 x = &y 𝜔⟩𝜙 .                                   (118)
We infer from the assumptions that
                                     (K, 𝑠 1, 𝛽) |= {x := sref (y)}⟨𝜋 () 𝜔⟩𝜙                               (119)
Let 𝑠 2 = val K,𝑠1,𝛽 (x := sref (y)) (𝑠 1 ). Then we can transform (119) to
                                             (K, 𝑠 2, 𝛽) |= ⟨𝜋 () 𝜔⟩𝜙                                      (120)
  We know that x = &y is the active expression. By the construction of the local evaluation rules,
we know that it is also a (sub-)expression to be evaluated and added to the trace sh. Thus we can
use the local evaluation.
  Let 𝑣 = 𝜎1 (y). We know val𝜎1 (y) = {⟨𝜎1 ⟩ · K(𝑣)}. Further,
                             val𝜎1 (&y) = {⟨𝜎1 ⟩ · K(Ref 𝑠y (𝑏)) | 𝑏 ∈ BId}
                         val𝜎1 (x = &y) = {𝜏 · K(x = 𝑒) | 𝜏 · K(𝑒) ∈ val𝜎1 (&y)}
                                          = {⟨𝜎1 ⟩ · K(x = Ref 𝑠y (𝑏)) | 𝑏 ∈ BId}
                   val𝜎1 (x = Ref 𝑠y (𝑏)) = {⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ Ref 𝑠y (𝑏)] · K(()) | 𝑏 ∈ BId}
Hence, we know that the only possible compositions starting in state 𝜎1 have the shape
          ⟨𝜎1 ⟩, K(𝜋 x = &y 𝜔) → ⟨𝜎1 ⟩, K(x = Ref 𝑠y (𝑏 1 )) → ⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ Ref 𝑠y (𝑏 1 )], K(())
for 𝑏 1 ∈ BId concrete, fresh borrow identifiers.
  We know that 𝜎1 [x ↦→ Ref 𝑠y (𝑏)] = 𝜎2 , so we know that the suffix relation Tr(𝜋 () 𝜔, 𝜎2 ) ⋟
Tr(𝜋 x = &y 𝜔, 𝜎1 ). Therefore, by Lemma 6.11 and assumption (120), we have (118).             □

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:61



                                            Γ =⇒ {U}{x := ∗𝑠 (y)}⟨𝜋 () 𝜔⟩𝜙, Δ
                            derefShared
                                                Γ =⇒ {U}⟨𝜋 x = *y 𝜔⟩𝜙, Δ
                                           x : 𝐴, y : Ref 𝑠𝐴 , 𝐴 is Copy
  Theorem G.5 (Soundness of Rule derefShared). Let Γ, Δ ∈ 2DLFml be sets of formulas, U ∈ Upd
be an update, x be a program variable of type T, y a program variable of type &T, 𝜋 x = *y 𝜔 be a
program fragment, and 𝜙 ∈ DLFml be a formula. If
                                   |= Γ =⇒ {U}{x := ∗𝑠 (y)}⟨𝜋 () 𝜔⟩𝜙, Δ
then the following holds:
                                       |= Γ =⇒ {U}⟨𝜋 x = *y 𝜔⟩𝜙, Δ.
  Proof. We assume
                                   |= Γ =⇒ {U}{x := ∗𝑠 (y)}⟨𝜋 () 𝜔⟩𝜙, Δ                                       (121)
It is sufficient to show
                                          (K, 𝑠 1, 𝛽) |= ⟨𝜋 x = &y 𝜔⟩𝜙 .                                      (122)
We infer from the assumptions that
                                     (K, 𝑠 1, 𝛽) |= {x := ∗𝑠 (y)}⟨𝜋 () 𝜔⟩𝜙                                    (123)
Let 𝑠 2 = val K,𝑠1,𝛽 (x := ∗𝑠 (y)) (𝑠 1 ). Then we can transform (123) to
                                             (K, 𝑠 2, 𝛽) |= ⟨𝜋 () 𝜔⟩𝜙                                         (124)
  We know that x = *y is the active expression. By the construction of the local evaluation rules,
we know that it is also a (sub-)expression to be evaluated and added to the trace sh. Thus we can
use the local evaluation.
  Let 𝜎1 be an LAGC state such that 𝑠 1 ∼ 𝜎1 , let Ref 𝑠z (𝑏) = 𝜎1 (y) with some program variable z and
some borrow Id 𝑏, and let 𝑣 := 𝜎1 (z). We know that val𝜎1 (y) = {⟨𝜎1 ⟩ · K(Ref 𝑠z (𝑏))}. Further,
                               val𝜎1 (*y) = {𝜏 · K(*𝑒) | 𝜏 · K(𝑒) ∈ val𝜎1 (y)}
                                           = {⟨𝜎1 ⟩ · K(*Ref 𝑠z (𝑏))}
                        val𝜎1 (*Ref 𝑠z (𝑏)) = {⟨𝜎1 ⟩ · K(𝑣)}
                           val𝜎1 (x = *y) = {𝜏 · K(x = 𝑒) | 𝜏 · K(𝑒) ∈ val𝜎1 (*y)}
                                           = {⟨𝜎1 ⟩ · K(x = *Ref 𝑠z (𝑏))}
                   val𝜎1 (x = *Ref 𝑠z (𝑏)) = {𝜏 · K(x = 𝑒) | 𝜏 · K(𝑒) ∈ val𝜎1 (*Ref 𝑠z (𝑏))}
                                           = {⟨𝜎1 ⟩ · K(x = 𝑣)}
                            val𝜎1 (x = 𝑣) = {⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ 𝑣] · K(())}
  Hence, we know that the only possible composition starting in state 𝜎1 is
                            ⟨𝜎1 ⟩, K(𝜋 x = *y 𝜔) → ⟨𝜎1 ⟩, K(𝜋 x = *Ref 𝑠z (𝑏) 𝜔)
                         →⟨𝜎1 ⟩, K(𝜋 x = 𝑣 𝜔) → ⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ 𝑣], K(𝜋 () 𝜔) .
Let SharedRef (𝑤) = 𝑠 1 (y). We know that val K,𝑠1,𝛽 (∗𝑠 (y)) = 𝑤, which implies 𝑠 2 (x) = 𝑤. Since
𝑠 1 ∼ 𝜎1 , SharedRef (𝑤) must correspond to Ref 𝑠z (𝑏), which implies 𝑤 ∼𝜎1 𝑣. Let 𝜎2 := 𝜎1 [x ↦→ 𝑣].
Then, 𝑠 2 ∼ 𝜎2 .
    We know that Tr(𝜋 () 𝜔, 𝜎2 ) ⋟ Tr(𝜋 x = *y 𝜔, 𝜎1 ). Therefore, by Lemma 6.11 and assumption (124),
we have (122).                                                                                      □

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:62                                                                                               Daniel Drodt



                                                derefOfSharedRef
                                                  ∗𝑠 (sref (𝑡)) { 𝑡
  Theorem G.6 (Soundness and Completeness of Rule derefOfSharedRef). Let K = (D, 𝐼, S, 𝜌)
be a Kripke structure, 𝑠 ∈ S a state, and 𝛽 a variable assignment. Then
                                      val K,𝑠,𝛽 (∗𝑠 (sref (𝑡))) = val K,𝑠,𝛽 (𝑡)
   Proof.
                                         val K,𝑠,𝛽 (∗𝑠 (sref (𝑡)))
                                       =𝐼 (∗𝑠 ) (val K,𝑠,𝛽 (sref (𝑡)))
                                       =𝐼 (∗𝑠 ) (𝐼 (sref ) (val K,𝑠,𝛽 (𝑡)))
                                       =𝐼 (∗𝑠 ) (SharedRef (val K,𝑠,𝛽 (𝑡)))
                                       =val K,𝑠,𝛽 (𝑡)
                                                                                                               □


                                        Γ =⇒ {U}{x := mref (TyW)}⟨𝜋 () 𝜔⟩𝜙, Δ
                         borrowMut
                                             Γ =⇒ {U}⟨𝜋 x = &mut y 𝜔⟩𝜙, Δ

  Theorem G.7 (Soundness of Rule borrowMut). Let Γ, Δ ∈ 2DLFml be sets of formulas, U ∈
Upd be an update, x be a program variable of some mutable reference type, y a program variable,
𝜋 x = &mut y 𝜔 be a program fragment, and 𝜙 ∈ DLFml be a formula. If
                                |= Γ =⇒ {U}{x := mref (TyW)}⟨𝜋 () 𝜔⟩𝜙, Δ
then the following holds:
                                     |= Γ =⇒ {U}⟨𝜋 x = &mut y 𝜔⟩𝜙, Δ.
   Proof. It suffices to show
                                       (K, 𝑠 1, 𝛽) |= ⟨𝜋 x = &mut y 𝜔⟩𝜙 .                                  (125)
We infer from the assumptions that
                                  (K, 𝑠 1, 𝛽) |= {x := mref (TyW)}⟨𝜋 () 𝜔⟩𝜙                                (126)
Let 𝑠 2 = val K,𝑠1,𝛽 (x := mref (TyW)) (𝑠 1 ). Then we can transform (126) to
                                             (K, 𝑠 2, 𝛽) |= ⟨𝜋 () 𝜔⟩𝜙                                      (127)
  We know that x = &mut y is the active expression. By the construction of the local evaluation
rules, we know that it is also a (sub-)expression to be evaluated and added to the trace sh. Thus we
can use the local evaluation.
  Let 𝜎1 be an LAGC state such that 𝑠 1 ∼ 𝜎1 . Let 𝑣 = 𝜎1 (y). We know val𝜎1 (y) = {⟨𝜎1 ⟩ · K(𝑣)}.
Further,
                          val𝜎1 (&mut y) = {⟨𝜎1 ⟩ · K(Ref 𝑚
                                                          y (𝑏)) | 𝑏 ∈ BId}
                     val𝜎1 (x = &mut y) = {𝜏 · K(x = 𝑒) | 𝜏 · K(𝑒) ∈ val𝜎1 (&mut y)}
                                           = {⟨𝜎1 ⟩ · K(x = Ref 𝑚
                                                                y (𝑏)) | 𝑏 ∈ BId}
                     val𝜎1 (x = Ref y (𝑏)) = {⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ Ref 𝑚
                                   𝑚
                                                                    y (𝑏)] · K(())}


ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:63


Hence, we know that the only possible composition starting in state 𝜎1 is

      ⟨𝜎1 ⟩, K(𝜋 x = &mut y 𝜔) → ⟨𝜎1 ⟩, K(x = Ref 𝑚                            𝑚
                                                  y (𝑏)) → ⟨𝜎1 ⟩ ↷ 𝜎1 [x ↦→ Ref y (𝑏)], K(()) .

Let 𝜎2 := 𝜎1 [x ↦→ Ref 𝑠y (𝑏)]. Then, Tr(𝜋 () 𝜔, 𝜎2 ) ⋟ Tr(𝜋 x = &y 𝜔), 𝜎1 . We know 𝑠 2 ∼ 𝜎2 . Therefore,
by Lemma 6.11 and assumption (127), we have (125).                                                      □


                                          Γ =⇒ {U}{x ∗→ se}⟨𝜋 () 𝜔⟩𝜙, Δ
                                mutate
                                             Γ =⇒ {U}⟨𝜋 *x = se 𝜔⟩𝜙, Δ

  Theorem G.8 (Soundness of Rule mutate). Let Γ, Δ ∈ 2DLFml be sets of formulas, U ∈ Upd
be an update, x be a program variable of type &mut T, se a literal or a program variable of type T,
𝜋 *x = se 𝜔 be a program fragment, and 𝜙 ∈ DLFml be a formula. If

                                    |= Γ =⇒ {U}{x ∗→ se}⟨𝜋 () 𝜔⟩𝜙, Δ

then the following holds:
                                       |= Γ =⇒ {U}⟨𝜋 *x = se 𝜔⟩𝜙, Δ.

  Proof. It suffices to show

                                         (K, 𝑠 1, 𝛽) |= ⟨𝜋 *x = se 𝜔⟩𝜙 .                                      (128)

We infer from the assumptions that

                                       (K, 𝑠 1, 𝛽) |= {x ∗→ se}⟨𝜋 () 𝜔⟩𝜙                                      (129)

Let 𝑠 2 = val K,𝑠1,𝛽 (x ∗→ se) (𝑠 1 ). Then we can transform (129) to

                                            (K, 𝑠 2, 𝛽) |= ⟨𝜋 () 𝜔⟩𝜙                                          (130)

  We know that *x = se is the active expression. By the construction of the local evaluation rules,
we know that it is also a (sub-)expression to be evaluated and added to the trace sh. Thus we can
use the local evaluation.
  We only show the case where se is a value. The case where it is a variable is analogous.
  Let 𝜎1 be an LAGC state such that 𝑠 1 ∼ 𝜎1 . Let 𝑏 and y be such that 𝜎1 (x) = Ref 𝑚
                                                                                     y (𝑏). We know

                  val𝜎1 (*x) = {⟨𝜎1 ⟩ · K(y)}
             val𝜎1 (*x = se) = {𝜏 · K(pe = se) | 𝜏 · K(pe) ∈ val𝜎1 (*x)} = {⟨𝜎1 ⟩ · K(y = se)}
              val𝜎1 (y = se) = {⟨𝜎1 ⟩ ↷ 𝜎1 [y ↦→ se] · K(())}

Therefore, the only possible composition is

                    ⟨𝜎1 ⟩, K(*x = se) → ⟨𝜎1 ⟩, K(y = se) → ⟨𝜎1 ⟩ ↷ 𝜎1 [y ↦→ se], K(())

Let 𝜎2 := 𝜎1 [y ↦→ se]. Since val K,𝑠1,𝛽 (x ∗→ se) (𝑠 1 ) (y) = se and is 𝑠 1 (z) for all program variables
other than y, we have 𝑠 2 ∼ 𝜎2 .
  Then, Tr(𝜋 () 𝜔, 𝜎2 ) ⋟ Tr(𝜋 *x = se 𝜔, 𝜎1 ), which with Lemma 6.11 and assumption (130), gives
us goal (128).                                                                                           □

                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:64                                                                                               Daniel Drodt


G.1      Loop Rules
The remaining rules deal with loops using loop scopes. [61]. The intuitive semantics of a loop scope
⟳x 𝑒 ⟲ with index variable x and body 𝑒, is that 𝑒 is evaluated. If the evaluation encounters an
expression that exits the loop, such as a break or return, x is set to true; the break’s value becomes
the loop scope’s value. Otherwise, x is set to false. Thereby, it models exactly one iteration of the
loop and x models whether we exit the loop.
  In terms of LAGC semantics, we define local rules that evaluate the body 𝑒 as for normal blocks,
except when the next sub-expression is a relevant expression, i.e., break, continue, or return.
  When encountering an expression like break 𝑒 in a loop scope, we have:
                           val𝜎 (⟳x {break 𝑣; 𝑠 𝑒} ⟲) = {⟨𝜎⟩ · K({x = true; 𝑒})}                           (131)
   The local evaluation for continue sets the value of x to false and emits a continue event.
              val𝜎 (⟳x {continue; 𝑠 𝑒 2 } ⟲) = {⟨𝜎⟩ ↷ continueEv() ↷ 𝜎 [x ↦→ ff] · K(())}                  (132)
  We must also adapt the global composition rules to stop execution after a continue event, as
the evaluation should not proceed with the rest of the program after a continue in a loop scope.
Rule (133) is the changed version of rule (50). All others are analogous.

                  𝜎 = last(sh) lastEv(sh) ≠ panicEv() lastEv(sh) ≠ continueEv()
                        𝜏 · K(𝑒 ′ ) ∈ val𝜎 (𝑒) 𝜌 concretizes 𝜏 wf (sh ∗∗ 𝜌 (𝜏))                            (133)
                                         sh, K(𝑒) → sh ∗∗ 𝜌 (𝜏), K(𝑒 ′ )
  With these adapted rules, we can proceed with proving the relevant RustyDL calculus rules
sound.

loopScopeInvBox
      Γ =⇒ {U}inv, Δ
                                                                                 
      Γ =⇒ {U}{V} inv → [𝜋 ⟳x 𝑒; continue ⟲ 𝜔] (x  TRUE → 𝜙) ∧ (x  FALSE → inv) , Δ
                                            Γ =⇒ {U}[𝜋 loop 𝑒 𝜔]𝜙, Δ
where V is an anonymizing update that overwrites every variable written to or mutated in 𝑒, see [1,
22] for details.
   Theorem G.9 (Soundness of Rule loopScopeInvBox). Let Γ, Δ ∈ 2DLFml be sets of formulas,
U ∈ Upd be an update, x : bool be a fresh program variable, 𝜋 loop 𝑒 𝜔 be a program fragment, and
𝜙, inv ∈ DLFml be formulas, and
                        V = b1 := 𝑏 1 ∥ · · · ∥ b𝑛 := 𝑏𝑛 ∥ d1 ∗→ 𝑑 1 ∥ · · · ∥ d𝑚 ∗→ 𝑑𝑚
the anonymizing update, where b1, . . . , b𝑛 are all variables written to in 𝑒, d1, . . . , d𝑚 are all mutable
references mutated in 𝑒, and 𝑏 1, . . . , 𝑏𝑛 , 𝑑 1, . . . , 𝑑𝑚 are fresh constants of appropriate sorts. If
                           |= Γ =⇒ {U}inv, Δ
                                           
                              Γ =⇒ {U}{V} inv → [𝜋 ⟳x 𝑒; continue ⟲ 𝜔]
                           |=                                     
                                (x  TRUE → 𝜙) ∧ (x  FALSE → inv) , Δ

then the following holds:
                                        |= Γ =⇒ {U}[𝜋 loop 𝑒 𝜔]𝜙, Δ.

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:65


  Proof. We assume
                           |= Γ =⇒ {U}inv, Δ                                                                  (134)
                                           
                              Γ =⇒ {U}{V} inv → [𝜋 ⟳x 𝑒; continue ⟲ 𝜔]
                           |=                                                                               (135)
                                (x  TRUE → 𝜙) ∧ (x  FALSE → inv)

  Let K = (D, 𝐼, S, 𝜌) be a random but arbitrary Kripke structure, 𝑠 ∈ S a state, and 𝛽 a variable
assignment. We want to show that
                                  (K, 𝑠, 𝛽) |= Γ =⇒ {U}[𝜋 loop 𝑒 𝜔]𝜙, Δ.
Let 𝑠 1 = val K,𝑠,𝛽 (U)(𝑠). Then we need to show
                                          (K, 𝑠 1, 𝛽) |= [𝜋 loop 𝑒 𝜔]𝜙 .                                      (136)
We infer from the assumptions that
                       (K, 𝑠 1, 𝛽) |= inv                                                                     (137)
                                            
                                        {V} inv → [𝜋 ⟳x 𝑒; continue ⟲ 𝜔]
                       (K, 𝑠 1, 𝛽) |=                                                                       (138)
                                          (x  TRUE → 𝜙) ∧ (x  FALSE → inv)

Let 𝑠 2 = val K,𝑠1,𝛽 (V) (𝑠 1 ). Then we can transform (138) to
            (K, 𝑠 2, 𝛽) |=
                                                                                                           (139)
              inv → [𝜋 ⟳x 𝑒; continue ⟲ 𝜔] (x  TRUE → 𝜙) ∧ (x  FALSE → inv)
If the loop does not terminate when started in 𝑠 1 , then the above holds trivially. Hence, we assume
that the loop is exited after 𝑘 iterations. We proceed with an inductive proof to show that the
formula inv holds before all iterations. Let 𝑠 (𝑖 ) denote the state before the 𝑖-th iteration.
  Case G.5 (Before first iteration (𝑖 = 1)). Then, 𝑠 (𝑖 ) = 𝑠 (1) = 𝑠 1 . By assumption (137), we have
(K, 𝑠 1, 𝛽) |= inv, hence, the hypothesis holds.
   Case G.6 (Induction step: Before iteration 𝑖 + 1). We assume (K, 𝑠 (𝑖 ) , 𝛽) |= inv. We execute the loop
body 𝑒 once in state 𝑠 (𝑖 ) . Either iteration 𝑖 exits the loop or we continue with the loop’s execution.
In the former case, there is no iteration 𝑖 + 1 and we are done. In the latter case, the semantics of
the loop scope and the continue expression (rule (132)) mean that (K, 𝑠 (𝑖+1) , 𝛽) |= inv holds iff the
following holds:
                                                                                                   
     (K, 𝑠 (𝑖 ) , 𝛽) |= inv → [𝜋⟳x 𝑒; continue ⟲𝜔] (x  TRUE → 𝜙) ∧ (x  FALSE → inv)
Any changes the body 𝑒 can affect are to b1, . . . , b𝑛 and the places borrowed by d1, . . . , d𝑚 . Because
these are overwritten by the anonymizing update V, and for all other program variables we have
𝑠 2 (y) = 𝑠 (𝑖+1) (y), the above follows from assumption (139). Hence, (K, 𝑠 (𝑖+1) , 𝛽) |= inv.
  Now we know that iteration 𝑘 exits the loop and that (K, 𝑠 (𝑘 ) , 𝛽) |= inv. From this, it follows that
                                                                                                  
   (K, 𝑠 (𝑘 ) , 𝛽) |= inv → [𝜋 ⟳x 𝑒; continue ⟲ 𝜔] (x  TRUE → 𝜙) ∧ (x  FALSE → inv)

Because we exit the loop in iteration 𝑘, we simplify this to
                              (K, 𝑠 (𝑘 ) , 𝛽) |= inv → [𝜋𝜔] (x  TRUE → 𝜙)
                                                                                   


                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
ZZZ:66                                                                                               Daniel Drodt


which we further simplify to
                                              (K, 𝑠 (𝑘 ) , 𝛽) |= [𝜋𝜔]𝜙                                     (140)
Because we assume the loop’s termination, we have
                                      Tr(𝜋𝜔, 𝜎 (𝑘 ) ) ⋟ Tr(𝜋 loop 𝑒 𝜔, 𝜎1 ).
By equation (140) and Lemma 6.11 we have goal (136).                                                           □


                                            Γ =⇒ {U}⟨𝜋 {x = true; se} 𝜔⟩𝜙, Δ
                         breakValue
                                       Γ =⇒ {U}⟨𝜋 ⟳x {break se; 𝑠 𝑒} ⟲ 𝜔⟩𝜙, Δ

   Theorem G.10 (Soundness of Rule breakValue). Let Γ, Δ ∈ 2DLFml be sets of formulas, U ∈ Upd
be an update, x : bool be a program variable, 𝜋 ⟳x break se 𝑠 𝑒 ⟲ 𝜔 be a program fragment, 𝑠 a series
of statements, 𝑒 an expression, and 𝜙 ∈ DLFml a formula. If
                                     |= Γ =⇒ {U}⟨𝜋 {x = true; se} 𝜔⟩𝜙, Δ
then the following holds:
                               |= Γ =⇒ {U}⟨𝜋 ⟳x {break se; 𝑠 𝑒} ⟲ 𝜔⟩𝜙, Δ.
   Proof. We assume
                                     |= Γ =⇒ {U}⟨𝜋 {x = true; se} 𝜔⟩𝜙, Δ                                   (141)
   It suffices to show
                                 (K, 𝑠 1, 𝛽) |= ⟨𝜋 ⟳x {break se; 𝑠 𝑒} ⟲ 𝜔⟩𝜙 .                              (142)
We infer from the assumption (141) that
                                      (K, 𝑠 1, 𝛽) |= ⟨𝜋 {x = true; se} 𝜔⟩𝜙                                 (143)
  We only consider the case where se ∈ Val. The case where se ∈ Var is analogous.
  Let 𝜎1 be an LAGC state with 𝑠 1 ∼ 𝜎1 By rule (131), we have
                         val𝜎1 (⟳x {break se; 𝑠 𝑒} ⟲) = {⟨𝜎1 ⟩ · K({x = true; se})}                        (144)
Clearly, then, Tr({x = true; se}, 𝜎1 ) ⋟ Tr(⟳x {break se; 𝑠 𝑒} ⟲, 𝜎1 ). By Lemma 6.11, this implies
that the goal (142) holds.                                                                       □


                                                Γ =⇒ {U}⟨x = false⟩𝜙, Δ
                          continue
                                      Γ =⇒ {U}⟨𝜋 ⟳x {continue 𝑠 𝑒} ⟲ 𝜔⟩𝜙, Δ

   Theorem G.11 (Soundness of Rule continue). Let Γ, Δ ∈ 2DLFml be sets of formulas, U ∈ Upd
be an update, x : bool be a program variable, 𝜋 ⟳x continue; 𝑠 𝑒 ⟲ 𝜔 be a program fragment, 𝑠 a
series of statements, 𝑒 an expression, and 𝜙 ∈ DLFml a formula. If
                                         |= Γ =⇒ {U}⟨x = false⟩𝜙, Δ
then the following holds:
                               |= Γ =⇒ {U}⟨𝜋 ⟳x {continue 𝑠 𝑒} ⟲ 𝜔⟩𝜙, Δ.

ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
A Complete, Formal Semantics for Rust Source Code                                                           ZZZ:67


  Proof. We assume
                                         |= Γ =⇒ {U}⟨x = false⟩𝜙, Δ                                           (145)
  It suffices to show
                          (K, 𝑠 1, 𝛽) |= ⟨𝜋 ⟳x {continue 𝑠 𝑒} ⟲ 𝜔⟩𝜙 .                                         (146)
We infer from the assumption (141) that
                                           (K, 𝑠 1, 𝛽) |= ⟨x = false⟩𝜙                                        (147)
  Let 𝜎1 be an LAGC state with 𝑠 1 ∼ 𝜎1 By rule (132), we have
            val𝜎1 (⟳x {continue 𝑠 𝑒} ⟲) = {⟨𝜎1 ⟩ ↷ continueEv() ↷ 𝜎1 [x ↦→ ff] · K(())}                       (148)
   By rule (133), we know that after the continue event, the composition cannot continue. Hence,
we infer that all traces in Tr(⟳x {continue 𝑠 𝑒} ⟲, 𝜎1 ) are of the form sh · ⟨𝜎1 ⟩ ↷ continueEv() ↷
𝜎1 [x ↦→ ff] for some shining trace sh. Let 𝜎2 := 𝜎1 [x ↦→ ff]. It is trivial to derive that Tr(x=false, 𝜎1 ) =
{⟨𝜎1 ⟩ ↷ 𝜎2 }. Since all traces in both sets end in state 𝜎2 , Definition 6.6 implies the goal (146)
holds.                                                                                                        □




                  ACM Trans. Program. Lang. Syst., Vol. XXX, No. YYY, Article ZZZ. Publication date: September 2026.
