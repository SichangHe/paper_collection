                                                           HITrees: Higher-Order Interaction Trees
                                                       Amir Mohammad Fadaei Ayyam                                                      Michael Sammler
                                                     Institute of Science and Technology (ISTA)                            Institute of Science and Technology (ISTA)
                                                               Klosterneuburg, Austria                                               Klosterneuburg, Austria
                                                           Sharif University of Technology                                         michael.sammler@ista.ac.at
                                                         Computer Engineering Department
                                                                      Tehran, Iran
                                                               am.fadaei@ce.sharif.edu
                                         Abstract                                                                    in complexity. This has led to a rise of research on how to for-
                                         Recent years have witnessed the rise of compositional se-                   mally embed complex semantics into theorem provers [Char-
                                         mantics as a foundation for formal verification of complex                  guéraud et al. 2023; Frumin et al. 2024; Letan and Régis-
arXiv:2510.14558v1 [cs.PL] 16 Oct 2025




                                         systems. In particular, interaction trees have emerged as a                 Gianas 2020; Stepanenko et al. 2025; Xia et al. 2020].
                                         popular denotational semantics. Interaction trees achieve                      A common method of embedding semantics into a theo-
                                         compositionality by providing a reusable library of effects.                rem prover is to use operational semantics (either big-step
                                         However, their notion of effects does not support higher-                   or small-step). Operational semantics are very well under-
                                         order effects, i.e., effects that take or return monadic compu-             stood (though there are still new, easier to use variants being
                                         tations. Such effects are essential to model complex semantic               discovered [Charguéraud et al. 2023]) and widely used by
                                         features like parallel composition and call/cc.                             verification projects [Jung et al. 2018; Leroy 2006]. How-
                                            We introduce Higher-Order Interaction Trees (HITrees), the               ever, operational semantics have one important limitation:
                                         first variant of interaction trees to support higher-order ef-              They can be challenging to compose modularly. Operational
                                         fects in a non-guarded type theory. HITrees accomplish this                 semantics are usually defined as a monolithic inductive defi-
                                         through two key techniques: first, by designing the notion                  nition giving the transition system for the language in ques-
                                         of effects such that the fixpoints of effects with higher-order             tion, which can make it difficult to reuse components and
                                         input can be expressed as inductive types inside the type the-              constructs between different languages.
                                         ory; and second, using defunctionalization to encode higher-                   This lack of compositionality has led to a rise of research
                                         order outputs into a first-order representation. We imple-                  into more compositional methods of defining semantics via
                                         ment HITrees in the Lean proof assistant, accompanied by                    denotational semantics. A particularly active area of research
                                         a comprehensive library of effects including concurrency,                   on denotational semantics is based on variants of the free
                                         recursion, and call/cc. Furthermore, we provide two inter-                  monad [Swierstra 2008]. While free monads have a long tra-
                                         pretations of HITrees, as state transition systems and as                   dition as denotational semantics [Kiselyov and Ishii 2015;
                                         monadic programs. To demonstrate the expressiveness of                      Letan and Régis-Gianas 2020; McBride 2015], they started
                                         HITrees, we apply them to define the semantics of a language                receiving significantly more attention for defining the seman-
                                         with parallel composition and call/cc.                                      tics of programming languages with the arrival of interaction
                                                                                                                     trees (ITrees) [Xia et al. 2020]. ITrees arose from the desire to
                                         CCS Concepts: • Theory of computation → Denota-                             encode the complex semantics of LLVM in a compositional
                                         tional semantics.                                                           way as part of the VellVM project [Beck et al. 2025]. Since
                                         Keywords: denotational semantics, interaction trees, Lean                   then, they have been picked up by a wide range of verifica-
                                                                                                                     tion projects [Beck et al. 2025; Chappe et al. 2025; Sammler
                                                                                                                     et al. 2023; Song et al. 2023; Vistrup et al. 2025]
                                         1    Introduction                                                              The key insight of a denotational semantics based on
                                         Formal verification using machine-checked proofs has seen                   ITrees (or a free monad in general) is to build a compo-
                                         important advances in recent years, leading researchers to                  sitional semantics around a set of uninterpreted effects. Such
                                         tackle more and more complex languages and systems [Beck                    effects can include state, concurrency, non-determinism, and
                                         et al. 2025; Gu et al. 2019; Klein et al. 2009; Li et al. 2021].            many more. Using ITrees, one can build a complex denota-
                                         At the core of these verification projects are the formal se-               tional semantics using many different effects by composing
                                         mantics of the system that should be verified. As these sys-                reusable building blocks for individual effects. This compo-
                                         tems become more complex, their semantics also increases                    sitionality significantly simplifies the definition of complex
                                                                                                                     semantics [Beck et al. 2025; Vistrup et al. 2025].
                                         Authors’ Contact Information: Amir Mohammad Fadaei Ayyam, Institute
                                         of Science and Technology (ISTA), Klosterneuburg, Austria and Sharif Uni-      While the notion of effects supported by ITrees and most
                                         versity of Technology, Computer Engineering Department, Tehran, Iran,       variants of the free monad is quite general, there is one im-
                                         am.fadaei@ce.sharif.edu; Michael Sammler, Institute of Science and Tech-    portant class of effects that is not supported: Higher-order
                                         nology (ISTA), Klosterneuburg, Austria, michael.sammler@ista.ac.at.
                                                                                                               Amir Mohammad Fadaei Ayyam and M. Sammler


effects that take a monadic computation as an input or re-                            define HITrees as an inductive2 data type inside the Lean
turn a monadic computation. Such higher-order effects are                             proof assistant and show that HITrees support a large variety
useful to model complex higher-order languages. As a con-                             of higher-order effects.
crete example, consider the recent formalization of OCaml                                To support higher-order effects, HITrees leverage two
by Seassau et al. [2025]. Its monad micro 𝐴 exposes three                             techniques, one for handling higher-order inputs,3 one for
different higher-order effects:1                                                      higher-order outputs.4 Let us give a glimpse of the high-level
                                                                                      ideas of these techniques here. (A detailed description can
         par (𝑚 1 : micro 𝐴) (𝑚 2 : micro 𝐵) : micro (𝐴 × 𝐵)                          be found in §2.1.)
         try (𝑚 : micro 𝐴) : micro (𝐴 + Exn)                                             To support higher-order inputs, HITrees adapt the notion
    handle (𝑚 : micro 𝐴) (𝑚 ′ : Eff → micro 𝐴) : micro 𝐴                              of effects to avoid any dependency between the input and
                                                                                      output types of the effect. This enables computing the fix-
The effect par 𝑚 1 𝑚 2 denotes the parallel composition of the                        point of effects with higher-order inputs as an inductive type
monadic computations 𝑚 1 and 𝑚 2 . The effect try 𝑚 catches                           inside the ambient type theory of the proof assistant. While
exceptions Exn raised by 𝑚. Finally, the effect handle 𝑚 𝑚 ′                          the restriction that output types cannot depend on inputs
uses 𝑚 ′ to interpret the algebraic effect Eff during the ex-                         may appear limiting, we demonstrate in §2.1 how dependent
ecution of 𝑚. While this example shows the usefulness of                              effects can be recovered for HITrees.
higher-order effects, it has one important caveat: The micro 𝐴                           To support higher-order outputs, we use a variant of de-
monad is defined in a monolithic way—hard-coding the spe-                             functionalization [Reynolds 1972]. Concretely, we observe
cific effects necessary for modeling OCaml. While this works                          that when an effect returns a HITree, it represents some ab-
for Seassau et al. [2025], this solution is not very satisfying.                      stract computation whose purpose is to be run at some point.
By hard-coding the effects, one loses many of the benefits                            This means that we can transform an effect with higher-
of the free monad—in particular, the ability to have a com-                           order outputs to return an abstract identifier instead of a
posable library of effects that can be reused across different                        HITree, together with exposing a separate effect to run the
languages.                                                                            computation associated with the identifier.
   This leads us to the core question of this paper: How can                             Together, these techniques enable HITrees to support a
one define a compositional, free-monad-based denotational                             large variety of higher-order effects including the par effect
semantics that supports higher-order effects?                                         from above, a call/cc effect that allows capturing the current
   Answering this question is surprisingly challenging: None                          continuation, and a fixpoint combinator rec.
of the popular variants of the free monad, including ITrees [Xia                         We implement HITrees in the Lean proof assistant [Moura
et al. 2020] and FreeSpec [Letan and Régis-Gianas 2020] sup-                          and Ullrich 2021]. Our implementation comes with a rich
port higher-order effects. To our knowledge, the only variant                         library of effects including state, non-determinism, concur-
of free monads supporting higher-order effects generically in                         rency, recursion, and call/cc. Thanks to Lean’s rich meta-
a theorem prover is the GITree library by Frumin et al. [2024].                       programming features, our implementation of HITrees pro-
GITrees support arbitrary higher-order effects with compu-                            vides custom commands for declaring new effects and taking
tations both as inputs and outputs of effects. Frumin et al.                          the fixpoint of a higher-order effect. To reason about and
[2024] show how GITrees can model complex effects like                                execute HITrees, we develop two interpretations: One as
a higher-order store containing GITrees, or control effects                           state transition systems (inspired by Vistrup et al. [2025])
like call/cc [Stepanenko et al. 2025]. However, to achieve this                       and one as an executable function into a suitably chosen
expressiveness, GITrees have to pay a steep price: Instead                            monad. Additionally, we show how to embed a language
of defining the free monad as a normal (co-)inductive type                            with parallel composition and call/cc into HITrees. Overall,
in the ambient type theory of the proof assistant, GITrees                            we make the following contributions:
are defined as the solution of a complex recursive domain
equation inside a guarded type theory. This means that work-                             Contributions.
ing with GITrees requires working inside this guarded type                                 • HITrees: a version of interaction trees supporting
theory, not the ambient type theory of the proof assistant.                                  higher-order effects (§3)
In particular, one cannot use datatypes like pairs from the                                • An implementation of HITrees and their effects in
ambient type theory but has to define them in the guarded                                    Lean including meta-theory and commands for defin-
type theory (e.g., via the church encoding) and then reason                                  ing new effects and taking the fixpoint of effects
about them in the guarded type theory using step-indexing.                                 • Two interpretations of HITrees (§4), one as state tran-
   In this paper, we propose higher-order interaction trees                                  sition systems and one as executable monads.
(HITrees), the first version of interaction trees supporting higher-
order effects in a non-guarded type theory. In particular, we                         2 §7 discusses why HITrees are inductive instead of co-inductive.
                                                                                      3 Technically, strictly positive occurrences of HITrees in effects.
1 This presentation is simplified. For the full version, see Seassau et al. [2025].   4 Technically, for negative occurrences of HITrees in effects.
    HITrees: Higher-Order Interaction Trees


                                                                          1 -- automatically generated by effect FailE
          𝑣 ∈ Val F 𝑧 | ℓ | (𝑣 1, 𝑣 2 ) | 𝜆𝑥 . 𝑒      (𝑧 ∈ Z, ℓ ∈ N)      2 inductive FailE.I where | fail
                                                                          3 inductive FailE.O where | fail (_ : Empty)
          𝑒 ∈ Exp F 𝑣 | 𝑥 | 𝑒 1 b
                                + 𝑒 2 | 𝑒.1 | 𝑒.2 | ! 𝑒 | 𝑒 1 ← 𝑒 2 |
                                                                          4 def FailE : Effect := 〈FailE.I, FailE.O〉
                   ref(𝑒) | 𝑒 1 || 𝑒 2 | 𝑒 1 (𝑒 2 )
                                                                              HITrees, shown in Figure 2,6 are a variant of interaction
                                                                              trees over Effect. HITrees have three constructors:7 pure r
                          Figure 1. ExampleLang                               to denote a pure computation resulting in a value r of type
                                                                              𝜌 ; impure i k for an (impure) invocation of the effect with
1 structure Effect where                                                      input i and continuation k that takes the result (of output
2   I : Type
3   O : Type
                                                                              type E.O) as the argument; and unreachable as a denotation
4                                                                             for impossible branches that cannot be ruled out statically.
5 inductive HITree (E : Effect) (𝜌 : Type) where                                  The effect FailE command automatically lifts the fail op-
6   | pure (r : 𝜌)                                                            eration to a function on HITree by generating a fail function:8
7   | impure (i : E.I) (k : E.O → HITree E 𝜌)
8   | unreachable                                                         1 -- automatically generated by effect FailE
                                                                          2 def fail : HITree FailE 𝜌 :=
                                                                          3   .impure FailE.I.fail (𝜆 x => x.1.elim)
     Figure 2. (Preliminary) definition of effects and HITrees
                                                                                  Now, finally everything is in place to define the denotation
                                                                                   + 𝑒 2 K. First, we define the effect ExE of ExampleLang. For
                                                                              J𝑒 1 b
         • A library of effects including state, non-determinism,             now, it contains only FailE, but we will extend it later.
            concurrency, recursion, and call/cc. (§5)                     1   def ExE := FailE
         • A formalization of a language with concurrency and
            call/cc as a case study of HITrees (§6)                           Then, we define a function intOrFail to checks if a value is
                                                                              an integer and fail otherwise.
    §2 provides an introduction to HITrees, and §7 compares to
                                                                          1 def Val.intOrFail : Val → HITree ExE Int :=
    related work. Our Lean development is provided at https:              2   | .int z => return z
    //git.ista.ac.at/plv/hitrees.                                         3   | _ => fail

    2     HITrees by Example                                                                           + 𝑒 2 K (in Lean: (.plus e1 e2 ).denote):
                                                                              Then, we can define J𝑒 1 b
                                                                          1 def Exp.denote : Exp → HITree ExE Val := -- e.denote is J𝑒K
    We introduce HITrees via ExampleLang (Figure 1), an un-               2   | .plus e1 e2 => do -- .plus e1 e2 is 𝑒 1 b+ 𝑒2
    typed lambda calculus with integers 𝑧, pairs, a heap with             3     let v1 ← e1 .denote; let v2 ← e2 .denote
    locations ℓ, and concurrency via parallel composition.                4     return .int ((← v1 .intOrFail) + (← v2 .intOrFail)) ...
                                                                              HITrees form a monad (see §3.1) and thus we can use Lean’s
    2.1    Semantics of ExampleLang
                                                                              do notation [Ullrich and de Moura 2022] for monads. This
    This section constructs a denotational semantics J𝑒K for Ex-              notation elaborates into a sequence of HITree binds where
    ampleLang using HITrees by gradually introducing the dif-                 each left arrow ← corresponds to one bind.
    ferent effects of ExampleLang.
                                                                                 #2 State: Unreachable. Let us now continue with the
       #1 Failure: Introducing HITrees. We start with the se-                 denotations of the next expressions of ExampleLang: loading
    mantics of addition J𝑒 1 b+ 𝑒 2 K. For this, we introduce our first       from the heap (! 𝑒) and storing to the heap (𝑒 1 ← 𝑒 2 ). To
    effect: failure (also called getting stuck, crashing, or unde-            model the heap, we introduce the StateE effect.
    fined behavior). Addition is only defined on integers, but not
                                                                          1   effect StateE (𝛼 : Type) where
    on lambda terms. Thus, the semantics of addition first checks         2     | get : Unit → 𝛼 | set : 𝛼 → Unit
    that the summands are integers and fail otherwise. This fail
    operation is provided by the failure effect FailE, which we               This effect is parametrized by the type 𝛼 of the state. It pro-
    define using the effect command provided by our library:                  vides two operations, get and set, for retrieving resp. updat-
                                                                              ing the state. As before, the effect command automatically
1   effect FailE where
2     | fail : Unit → Empty                                                   generates the input and output types from this description:
    This command declares the effect FailE with a single opera-           1 -- automatically generated by effect StateE
                                                                          2 inductive StateE.I (𝛼 : Type) where
    tion fail. Concretely, effects are a pair of an input type I and      3   | get         | set (_ : 𝛼)
    an output type O, represented by the Effect type in Figure 2.5        4 inductive StateE.O (𝛼 : Type) where
    The effect command creates an Effect by generating an in-             5   | get (_ : 𝛼) | set
    put type and an output type, each with one constructor per            6 def StateE (𝛼 : Type) : Effect := 〈StateE.I 𝛼, StateE.O 𝛼〉

    operation. Concretely, using Lean’s meta-programming, the
                                                                              6 This figure omits an intermediate definition, see §3 for details.
    effect command from above generates the following types:
                                                                              7 The names “pure” and “impure” are inspired by Kiselyov and Ishii [2015].
    5We omit universe parameters to not clutter the presentation.             8 This definition is simplified. We will come back to it later.
                                                                                                         Amir Mohammad Fadaei Ayyam and M. Sammler


1 def SumE (E1 : Effect) (E2 : Effect) : Effect                                  FailE and StateE (using a treemap with extensional equality
2   := 〈E1 .I ⊕ E2 .I, E1 .O ⊕ E2 .O〉
3 infixr:50 " ⊕𝑒 " => SumE
                                                                                 to denote the heap as a map from location to values).
4                                                                            1   def ExE := FailE ⊕𝑒 StateE (ExtTreeMap Loc Val)
5 class Subeffect (E1 : Effect) (E2 : Effect) where
                                                                                 When trying to use get from above with ExE, we run into an
6   mapI : E1 .I → E2 .I
7   mapO? : E2 .O → Option E1 .O                                                 issue: get is specific to the effect StateE 𝛼 and thus does not
8 infix:20 " -< " => Subeffect                                                   work for ExE. To address this issue, we introduce the notion of
9                                                                                subeffects [Kiselyov and Ishii 2015; Xia et al. 2020], captured
10 instance {E} : E -< E where                                                   by the Subeffect typeclass in Figure 3. E1 is a subeffect of E2
11   mapI i := i
12   mapO? o := some o                                                           (written E1 -< E2 ) if there is a map mapI from the inputs of
13                                                                               E1 to the inputs of E2 and a map mapO? from the outputs of
14 instance {E1 E2 E'} [sub : E1 -< E2 ] : E1 -< (E2 ⊕𝑒 E') where                E2 to the outputs of E1 . Since E2 represents a “bigger” effect
15   mapI i := .inl (sub.mapI i)                                                 than E1 , mapO? can fail (by returning none) for outputs of E2
16   mapO? := 𝜆
17   | .inl o => sub.mapO? o
                                                                                 that do not correspond to outputs of E1 . E1 -< E2 is reflexive
18   | .inr _ => none                                                            and (subeffects of) E1 and E2 are subeffects of E1 ⊕𝑒 E2 :
19                                                                                  The trigger function (Figure 3) invokes a subeffect E1 in a
20   instance {E1 E2 E'} [sub : E1 -< E2 ] : E1 -< (E' ⊕𝑒 E2 ) where             larger effect E2 . trigger uses mapI to inject i into E2 and mapO?
21     ... -- analogous to the previous instance
                                                                                 to project out the result. The none case of mapO? is unreachable
22
23 def trigger {E1 E2 } [sub : E1 -< E2 ] (i : E1 .I) : HITree E2 E1 .O          since the input of the .impure was an operation of E1 .
24   := .impure (sub.mapI i) 𝜆 x => match sub.mapO? x with                          Using trigger, we can define get in a way that automati-
25        | some x => .pure x                                                    cally works for arbitrary supereffects.
26        | none => .unreachable
                                                                             1 -- automatically generated by effect StateE
                                                                             2 def get {𝛼 : Type} {E} [StateE 𝛼 -< E] : HITree E 𝛼 :=
                         Figure 3. Effect composition                        3   trigger (StateE.I.get).bind 𝜆
                                                                             4     | StateE.O.get o => .pure o
                                                                             5     | _ => .unreachable
     However, when we try to use this effect with .impure, we
                                                                                    This allows us to define J! 𝑒K (J𝑒 1 ← 𝑒 2 K is analogous):
     run into an issue. Intuitively, an input StateE.I.get should
     always result in an output StateE.O.get, but nothing in the             1 def Exp.denote : Exp → HITree ExE Val :=
                                                                             2   | .deref e => do -- .deref e is ! 𝑒
     type system enforces this. ITrees address this issue by us-             3     let v ← e.denote;
     ing a more dependent notion of effects where each input                 4     let h ← get; let l ← v1 .locOrFail;
     comes with the type of its output. However, this dependency             5     let some r := h[l]? | fail
     prevents higher-order effects (due to a negative occurrence             6     return r ...
     of the effect type, as we will see later in this section). To                  #3 Demonic choice: Dependent effects. Let us now turn
     enable higher-order effects, HITrees avoid a dependency of                  to the last remaining heap operation: allocation ref(𝑒 1 ). Allo-
     the output type on the input. Instead, we implement this                    cation is usually modeled using demonic non-determinism, i.e.,
     dependency using a dynamic check. Concretely, the effect                    the allocator picks an arbitrary location that is not allocated
     command generates the following function for get.9                          yet. To represent demonic non-determinism, we introduce a
1 -- automatically generated by effect StateE                                    new effect DemonicE. How should we define DemonicE? Vistrup
2 def get {𝛼 : Type} : HITree (StateE 𝛼) 𝛼 :=
3   .impure (StateE.I.get) 𝜆                                                     et al. [2025] define demonic choice by taking a type 𝛼 as an
4     | StateE.O.get o => .pure o                                                input and returning an element of type 𝛼:
5     | _ => .unreachable                                                    1   effect DemonicE where -- try 1
     This function uses a dynamic check to inspect the output of             2     | choose : (𝛼 : Type) → 𝛼
     the get operation. If it is StateE.O.get o, get returns o. Other-           However, this definition is rejected since our Effect type does
     wise, it discards the execution using .unreachable. Thanks to               not support the output type to depend on the input.10 We can
     this automatically generated dynamic check, the user can                    mitigate this problem by making 𝛼 a parameter of DemonicE:
     use get with expected type HITree (StateE 𝛼) 𝛼 .                        1   effect DemonicE (𝛼 : Type) where -- try 2
                                                                             2     | choose : Unit → 𝛼
        Effect composition. So far, we have only seen HITrees
     using single effects, but our denotation J𝑒K requires both the              This definition works, but it is quite restrictive as one needs
     FailE and the StateE effect. To combine effects, HITrees pro-               to fix the types of demonic choice statically. This is an issue
     vide the infrastructure shown in Figure 3. The sum E1 ⊕𝑒 E2                 for ref(𝑒): It should pick an arbitrary location that is not
     of E1 and E2 is defined as the sum of the input type and of
                                                                                 10 An additional problem is that this DemonicE must live in a higher universe
     the output type. With this, we can define ExE as the sum of
                                                                                 than 𝛼. Combining this DemonicE with effects in lower universes requires
     9 The version here is preliminary, it will be slightly adapted later.       manual universe lifting since Lean lacks universe cumulativity.
    HITrees: Higher-Order Interaction Trees


    allocated on the current heap. Since the current heap is not               To find the fixpoint of higher-order effects like ExE, HITrees
    available statically, we cannot refer to it in 𝛼.                        provide the fix_effect command.
       Thus, we arrive at our final definition of DemonicE:              1   fix_effect ExE := ConcE Val ExE ⊕𝑒 FailE ⊕𝑒 ...
1 effect DemonicE (𝛼 : Type) where -- final                                  This command defines ExE as a recursive effect that is iso-
2   | choose : (p : 𝛼 → Prop) → [DecidablePred p] → 𝛼                        morphic to the rejected version of ExE above.
    The idea is to fix 𝛼 statically, but allow dynamically picking a           Using this ExE, we can define J𝑒 1 || 𝑒 2 K as follows:
    decidable predicate 𝑝 that restricts the possible values of the      1 def Exp.denote : Exp → HITree ExE Val :=
    demonic choice. This allows us to define a choose function           2  | .par e1 e2 => do -- .par e1 e2 is 𝑒 1 | | 𝑒 2
    that guarantees that the resulting value satisfies 𝑝.                3   let (v1 , v2 ) ← par (e1 .denote >>= kill) (e2 .denote >>= kill)
                                                                         4   return .pair v1 v2 ...
1 def choose {𝛼 : Type} (p : 𝛼 → Prop) [DecidablePred p]
2   {E} [DemonicE 𝛼 -< E] : HITree E (x : 𝛼 // p x) :=                       Note that it is crucial that par takes HITree ExE Empty as the ar-
3   trigger (Demonic.I.choose p).bind 𝜆 o =>                                 gument to support nested parallel composition J𝑒 1 || 𝑒 2 || 𝑒 3 K.
4     if h : p o.1 then return 〈o.1, h〉 else .unreachable                       Let us now have a look under the hood of fix_effect. Our
    With this, we can define Jref(𝑒)K as follows:                            key observation is that Lean (and CIC in general) provides a
1 def Exp.denote : Exp → HITree ExE Val :=                                   native way to take the fixpoint of a type: the inductive com-
2   | .ref e => do                                                           mand. Inductive types can contain recursive occurrences
3     let v ← e.denote; let h ← get;                                         of themselves, as long as all occurrences are strictly posi-
4     let l ← choose (𝜆 l => l ∉ h); set (h.insert l.1 v)
5     return r ...
                                                                             tive [Coquand and Paulin 1988]. This means the recursive
                                                                             occurrences cannot be on the left-hand side of an arrow and
       This example of DemonicE shows how HITrees deal with                  (in Lean) are only allowed to appear either directly or in
    dependencies between inputs and outputs of effects. The                  arguments to other inductive types.11
    strict separation of input and output in Effect rules out direct            The following shows the code that fix_effect ExE gener-
    dependencies of the output type on the input. This prevents              ates to find the fixpoint of ExE using the inductive command.12
    some effects like try 1 of DemonicE that are possible in more        1 -- automatically generated from fix_effect ExE
    dependent encodings like interaction trees. However, one can         2 def ExE.O := ConcE.O Val ⊕ FailE.O ⊕ ...
    still have an operation where the type of the output depends         3 inductive ExE.I where
    on the input, as long as one can provide a non-dependent             4   | closed (_ : ConcE.I Val 〈ExE.I, ExE.O〉 ⊕ FailE.I ⊕ ...)
                                                                         5 def ExE : Effect := 〈ExE.I, ExE.O〉
    output type (𝛼 in DemonicE) that can be decidably cast into
    the dependent output type (x : 𝛼 // p x in DemonicE).                    It splits ExE into the output type ExE.O and input type ExE.I.
                                                                             Only the input type occurs in a strictly positive position in
       #4 Parallel: Higher-order effects. While the previous                 the HITree type and thus the output type must not contain a
    section showed the cost of using a non-dependent notion of               recursive occurrence of ExE. The input type ExE.I is defined as
    effects, we will now discuss the payoff: higher-order effects.           an inductive type that recursively appears as an argument to
    For this, consider parallel composition 𝑒 1 || 𝑒 2 . To model this       ConcE.I. This works since the Effect type is designed such that
    construct, we introduce a new effect ConcE for concurrency.              the output type does not depend on the input—if the output
1 effect ConcE (𝛼 : Type) (E : Effect) where                                 type would depend on the input, the input type would need
2   | par : (t1 t2 : HITree E Empty) → (𝛼 × 𝛼)
                                                                             to appear as part of the output type in a not strictly-positive
3   | kill : 𝛼 → Empty
4   | yield : Unit → Unit                                                    position and Lean would reject the inductive type.
    The main operation of this effect is the parallel composition               #5 Recursion: Negative occurrences via defunctional-
    par that takes two HITrees, runs them in parallel, and returns           ization. Let us now see how HITrees can support higher-
    a pair of the results. The result of a thread is given to the            order operations where the recursive occurrence is in a nega-
    kill operation that terminates the current thread. Addition-             tive position. For this, we consider the semantics of function
    ally, the effect exposes a yield operation for switching to              application J𝑒 1 (𝑒 2 )K. Here the challenge is that function calls
    another thread. We adapt J𝑒K such that it inserts yield at the           can introduce non-termination and we need a way to repre-
    appropriate points, following Vistrup et al. [2025].                     sent this non-termination in our semantic domain of HITrees.
       The challenge of ConcE is that par takes HITrees as ar-               One option is to use a co-inductive definition based on the De-
    guments and these HITrees should be able to use parallel                 lay monad [Capretta 2005] as used by ITrees. However, since
    composition themselves. In particular, the effect parameter              Lean does not have native support for co-inductive types, we
    E of ConcE should contain ConcE, creating a recursive loop.              cannot use this option. Instead, we use a higher-order effect
    Concretely, we would like to define ExE as follows:                      for recursion to represent non-termination. Concretely, our
1   -- error: fail to show termination                                       goal is to have a recursion combinator rec on HITrees:
2   def ExE := ConcE Val ExE ⊕𝑒 FailE ⊕𝑒 ...
                                                                             11 See      https://lean-lang.org/doc/reference/4.22.0/The-Type-System/
    However, Lean rejects this recursive usage of ExE since it               Inductive-Types/#--tech-term-Nested-inductive-types for details.
    cannot show termination of this recursive definition.                    12 The inductive type here is simplified (see §3.3 for details).
                                                                                                   Amir Mohammad Fadaei Ayyam and M. Sammler


1   rec : ((𝛼→HITree E 𝛽) → (𝛼→HITree E 𝛽)) → 𝛼→HITree E 𝛽               1 inductive HITree.Raw (I O 𝜌) where
                                                                         2   | pure (r : 𝜌)
    A naive idea would be to define rec directly as an effect:           3   | impure (i : I) (k : O → HITree.Raw I O 𝜌)
1 -- error: not strictly positive occurrence of E                        4   | unreachable
2 effect RecE (𝛼 𝛽 : Type) (E : Effect) where                            5
3 | fix : (_ : (𝛼→HITree E 𝛽) → 𝛼→HITree E 𝛽) (_ : 𝛼) → 𝛽                6    def HITree (E : Effect) := HITree.Raw E.I E.O
                                                                         7    -- ... lift pure, impure, unreachable to HITree ...
    However, this approach does not work since the first occur-          8
    rence of E is in a not in a strictly positive position. To resolve   9  def HITree.bind (t : HITree E 𝜌) (f : 𝜌 → HITree E 𝜌')
    this issue, we use defunctionalization [Reynolds 1972]. Con-         10   := match t with
    cretely, we introduce a set of abstract identifiers FId that rep-    11     | .unreachable => unreachable
                                                                         12     | .pure r => f r
    resent fixpoints with an operation call : FId→𝛼→HITree E 𝛽
                                                                         13     | .impure i k => impure i (𝜆 x => bind (k x) f)
    that invokes the fixpoint represented by the FId:                    14
1 effect RecE (𝛼 𝛽 : Type) (E : Effect) where                            15 instance : Monad (HITree E) where
2   | fix : (_ : FId → 𝛼 → HITree E 𝛽) (_ : 𝛼) → 𝛽                       16   pure := HITree.pure
3   | call : (_ : FId) (_ : 𝛼) → 𝛽                                       17   bind := HITree.bind
                                                                         18 instance : LawfulMonad (HITree E) where ...
    This definition avoids the not strictly positive occurrence of
    E by using FId. We can obtain rec by combining fix and call.
                                                                                           Figure 4. Full definition of HITrees
1 def rec [RecE 𝛼 𝛽 E -< E]
2    (f : (𝛼 → HITree E 𝛽) → 𝛼 → HITree E 𝛽) :
3 𝛼 → HITree E 𝛽 := fix 𝜆 fid => f (call fid)
                                                                              big-step semantics allows us to prove that certain (problem-
      The recursion combinator rec lets us define J𝑒 1 (𝑒 2 )K:               atic) executions exist. For example, we can show that a race
1 def Exp.denoteRaw (denote : Exp → HITree ExE Val)                           condition can cause the following program to return 1:
2   : Exp → HITree ExE Val :=
3   | .app e1 e2 => do -- .app e1 e2 is 𝑒 1 (𝑒 2 )                                Jlet 𝑥 = ref(0) in (𝑥 ← ! 𝑥 + 1 || 𝑥 ← ! 𝑥 + 1); ! 𝑥K ⇓ 1
4     let v1 ← e1 .denoteRaw; let v2 ← e2 .denoteRaw;
5     let 〈x, e〉 ← v1 .toRec! -- turn v1 into 𝜆 x. e
                                                                              §4.2 discusses the state machine semantics in more detail
6     denote (e.subst x v2 ) -- Je[v2 /x]K                                    and §6 shows more examples. In the future, it would be inter-
7 ...                                                                         esting to implement more powerful reasoning mechanisms
8 def Exp.denote : Exp → HITree ExE Val := rec Exp.denoteRaw                  for HITrees, like the program logic of Vistrup et al. [2025].
    This definition uses the fixpoint denote provided by rec to re-
    cursively call denoteRaw on 𝑒 [𝑣 2 /𝑥]. Directly calling denoteRaw        3     HITrees in Detail
    would be rejected by Lean since the call is not structurally              This section presents the definition of HITrees (§3.1) and the
    recursive. Overall, this shows how defunctionalization can                effect (§3.2) and fix_effect (§3.3) commands in detail.
    encode higher-order effects with not strictly positive occur-
    rences.                                                                   3.1    Definition of HITrees
                                                                                 Figure 4 shows the full definition of HITrees. This defini-
    2.2   Interpreting HITrees                                                tion differs from Figure 2 by introducing the intermediate
    We have seen how HITrees can give a denotational semantics                type HITree.Raw. This type is necessary due to a problem we
    to ExampleLang. Let us now see what we can do with such a                 glanced over in §2: The definition of HITree E 𝜌 from Figure 2
    semantics. We focus on two aspects: execution and reasoning.              actually contains the type of inputs E.I in a negative posi-
                                                                              tion: E.I it is contained in E, which appears in E.O that occurs
       Executing HITrees. To test a formal semantics, it is useful
                                                                              in a negative position in impure. This negative occurrence
    to be able to execute it. HITrees can be executed by inter-
                                                                              prevents taking the fixpoint of higher-order effects.
    preting them into a suitable Lean Monad, which can then be
                                                                                 To resolve this issue, we introduce HITree.Raw. It ensures
    compiled and executed like normal Lean code. Concretely,
                                                                              that the input type occurs only in strictly positive positions
    each effect can provide a monad handler that describes how
                                                                              by separating the input type I from the output type O. We ob-
    to interpret the effect into a monad. For example, the monad
                                                                              tain HITree as a straightforward definition on top of HITree.Raw
    handler for the ConcE effect interprets the effect into a state
                                                                              and we lift pure, impure, and unreachable to HITree. Users only
    monad that keeps track of all running threads and imple-
                                                                              interact with HITree. The only place where HITree.Raw appears
    ments a scheduler that picks the next thread on yield. §4.1
                                                                              is in the definition of higher-order effects. This is necessary
    explains this in more detail.
                                                                              since higher-order effects are part of the fixpoint and thus
       Reasoning about HITrees. To reason about HITrees, we                   must only contain the recursive occurrence in strictly posi-
    implement the technique of Vistrup et al. [2025] to turn in-              tive positions. The effect command automatically handles
    teraction trees into state machines. In a nutshell, this means            this by desugaring effects using HITree to use HITree.Raw.
    that each effect defines a small-step semantics, which can                   HITrees provide a bind function (Figure 4) and inhabit the
    then be lifted to a big-step semantics 𝑡 ⇓ 𝑣 on HITrees. This             Monad and LawfulMonad interfaces. The first instance enables us
     HITrees: Higher-Order Interaction Trees

 1 effect Eff p1 ... p𝑖 where
 2   | op1 : (x1 : 𝜄 1,1 ) → ... → (x𝑚1 : 𝜄 1,𝑚1 ) → o1
                                                                           Next, the effect command generates two unification hints
 3   ...                                                                via the unif_hint command. These hints guide Lean’s uni-
 4   | op𝑛 : (x1 : 𝜄𝑛,1 ) → ... → (x𝑚𝑛 : 𝜄𝑛,𝑚𝑛 ) → o𝑛                   fication when solving constraints of the form ?E.I =? Eff.I
                             (a) Syntax of effect.
                                                                        and ?E.O =? Eff.O by telling it to instantiate the unification
                                                                        variable ?E with Eff. For example, these hints allow Lean to
 1 inductive Eff.I p1 ... p𝑘 where                                      infer that HITree.impure (Eff.I.op𝑖 ...) 𝜆 _ => return 0 has
 2   | op1 (x1 : 𝜄 1,1 ) ... (x𝑚1 : 𝜄 1,𝑚1 )
 3   ...                                                                type HITree (Eff ...) Nat without specifying (E:=Eff ...).
 4   | op𝑛 (x𝑛 : 𝜄𝑛,1 ) ... (x𝑚𝑛 : 𝜄𝑛,𝑚𝑛 )                                 Finally, for each operation op𝑖 the effect command gener-
 5 inductive Eff.O p1 ... p𝑘 where                                      ates a specialized trigger function Eff.op𝑖 . This function casts
 6   | op1 (_ : o1 ) | ... | op𝑛 (_ : o𝑛 )                              the output to the right type by checking if the output cor-
 7 def Eff p1 ... p𝑘 : Effect :=
 8   〈Eff.I p1 ... p𝑘 , Eff.O p1 ... p𝑘 〉
                                                                        responds to the same operation as the input and otherwise
 9                                                                      discarding the execution as unreachable (see also §2.1).
10 unif_hint (E : Effect) p1 ... p𝑘
             ?           ?
11   where E = Eff ⊢ E.I = Eff.I p1 ... p𝑘                                 Special cases. There are three special cases: First, if the
12 unif_hint (E : Effect) p1 ... p𝑘
             ?           ?                                              type of a parameter is Unit, the parameter is omitted (see
13   where E = Eff ⊢ E.O = Eff.O p1 ... p𝑘
                                                                        get in §2.1). Second, if the output type o𝑖 is Empty, the trig-
14
15 -- per operation op𝑖                                                 ger function Eff.op𝑖 will be automatically generalized from
16 def Eff.op𝑖 {E} p1 ... p𝑘 [Eff p1 ... p𝑘 -< E]                       HITree E Empty to HITree E 𝜌 (for arbitrary 𝜌 ) by eliminating
17             (x1 : 𝜄𝑖,1 ) ... (x𝑚𝑖 : 𝜄𝑖,𝑚𝑖 ) : HITree E o𝑖 :=         the Empty (see fail in §2.1). Third, if a type of an input pa-
18   (trigger (.I.op𝑖 p1 ... p𝑘 x1 ... x𝑚𝑖 )).bind 𝜆 o =>
19     if let .O.op𝑖 o' := o then .pure o' else .unreachable
                                                                        rameter 𝜄𝑖,𝑗 contains HITree p𝑙 _, HITree p𝑙 _ is converted to
                                                                        HITree.Raw p𝑙 I p𝑙 O _ in 𝜄𝑖,𝑗 and the effect parameter p𝑙 is re-
                          (b) Desugaring of effect.                     placed with two parameters p𝑖 I and p𝑖 O (updating the other
                                                                        definitions as necessary). This desugaring of HITree to HITree.Raw
                     Figure 5. The effect command.                      is necessary to avoid not strictly positive occurrences as dis-
                                                                        cussed in §3.1.

                                                                        3.3   Fixpoints of Effects
     to use Lean’s do notation to define HITrees and the second
                                                                           Figure 6a shows the syntax of the fix_effect command
     instance automatically registers the monad laws with Lean’s
                                                                        along with the definitions it generates. fix_effect takes the
     simplifier tactic simp. We reuse the trigger function from
                                                                        name Eff of the recursively defined effect and the body of the
     Figure 3 for HITree with the definition of HITree in Figure 4.
                                                                        fixpoint. The body is a list of effects E1 ... E𝑛 combined using
                                                                        ⊕𝑒 . These effects can mention Eff as the recursive occurrence.
     3.2   Defining Effects                                                The fix_effect command generates several definitions
     This section discusses the effect command for defining new         shown in Figure 6b: First, it defines Eff.Pre as the version of
     effects and how it works under the hood.                           Eff that takes the recursive occurrence as an argument.
        The syntax for declaring new effects is shown in Figure 5a.        Second, the output type Eff.O is defined as the output
     The effect command first expects the name of the effect Eff        type of the effect E1 ⊕𝑒 ... ⊕𝑒 E𝑛 . To avoid a spurious de-
     and its 𝑘 parameters p1 , ..., p𝑘 . These parameters follow        pendency on the recursive occurrence Eff, we first reduce
     the same syntax as regular binders in Lean, supporting ex-         (E1 ⊕𝑒 ... ⊕𝑒 E𝑛 ).O to E1 O ⊕ ... ⊕ E𝑛 O where E𝑖 O is the out-
     plicit, implicit and typeclass parameters. Then follow the         put type of E𝑖 . (Recall that the output type cannot contain
     𝑛 operations op1 , ..., op𝑛 , where each operation op𝑖 has 𝑚𝑖      a recursive occurrence since it appears in a negative posi-
     inputs of types 𝜄𝑖,1 , ..., 𝜄𝑖,𝑚𝑖 respectively, and an output of   tion in HITree.Raw.) In case the fix_effect command detects
     type o𝑖 . The syntax of these operations follows the syntax        a recursive occurrence in Eff.O or if it cannot perform the
     of constructors of an inductive type, except that the output       reduction, it emits an error.
     type o1 cannot depend on any of the input binders x 𝑗 .               Finally, we reach the heart of the fix_effect command: The
        Let us now see how the effect command automatically             definition of Eff.I as an inductive type. Intuitively, this induc-
     generates the corresponding Effect. Concretely, the effect         tive type should contain a single field (E1 ⊕𝑒 ... ⊕𝑒 E𝑛 ).I
     command desugars to the Lean code shown in Figure 5b.              with the recursive occurrence replaced by 〈Eff.I, Eff.O〉.
        First, the effect command defines the input and output          However, we need to be careful to satisfy all the condi-
     types of the effect as the inductive types Eff.I and Eff.O         tions that Lean places on inductive types. First, we must
     and defines Eff by combining them. The input and output            ensure that all occurrences of Eff.I are strictly positive. As
     types each contain one constructor per operation with the          described in §3.1, the HITree.Raw type is carefully set up to
     corresponding inputs resp. outputs as parameters.                  avoid not strictly positive occurrences. Second, we need to
                                                                                                Amir Mohammad Fadaei Ayyam and M. Sammler

1    fix_effect Eff := E1 ⊕𝑒 ... ⊕𝑒 E𝑛                                 1    class MHandler (E E' : Effect) (𝜌 m) [Monad m] where
                                                                       2      handle : E.I → (k : E.O → HITree E' 𝜌) → m (HITree E' 𝜌)
                         (a) Syntax of fix_effect.
                                                                       3
1    def Eff.Pre (Eff : Effect) := E1 ⊕𝑒 ... ⊕𝑒 E𝑛                     4 instance sumMH {E1 E2 E' 𝜌 m} [Monad m]
2                                                                      5       [mh1 : MHandler E1 E' 𝜌 m] [mh2 : MHandler E2 E' 𝜌 m]
3    -- E𝑖 O is the reduced form of E𝑖 .O                              6     : MHandler (E1 ⊕𝑒 E2 ) E' 𝜌 m where
4    def Eff.O := E1 O ⊕ ... ⊕ E𝑛 O                                    7   handle i k := match i with
5                                                                      8     | .inl i => MHandler.handle i (k ◦ Sum.inl)
6 -- E𝑖′ is E𝑖 [〈Eff.I, Eff.O〉/Eff] and E𝑖′ I                          9     | .inr i => MHandler.handle i (k ◦ Sum.inr)
7 -- is the reduced form of E𝑖′ .I                                     10
8 inductive Eff.I where                                                11 instance unfoldMH {𝜌 m E EPre E'} [Monad m]
9   | closed (_ : E1′ I ⊕ ... ⊕ E𝑛′ I)                                 12       [UnfoldEffect E EPre] [MHandler EPre E' 𝜌 m]
10                                                                     13       : MHandler E E' 𝜌 m where
11   def Eff : Effect := 〈Eff.I, Eff.O〉                                14   handle i k := mh.handle (UnfoldEffect.invI i)
12                                                                     15     (𝜆 x => k (Eq.mp UnfoldEffect.out_eq x))
13   instance : UnfoldEffect Eff (Eff.Pre Eff) where                   16
14     -- body omitted                                              partial def eval {E 𝜌 m} [Monad m] [MHandler E E 𝜌 m]
                                                                       17
                                                                        [Inhabited 𝜌] : HITree E 𝜌 → m 𝜌
                                                                       18
                  (b) Desugaring of fix_effect.                  19   | .pure r => return r
                                                                 20   | .impure i k => do let r ← MHandler.handle i k; eval r
1 class UnfoldEffect (E : Effect) (EPre : outParam Effect) where
                                                                 21   | .unreachable => panic! "Unreachable computation"
2   injI : E.I → EPre.I
3   invI : EPre.I → E.I
4   injI_invI : ∀ i, injI (invI i) = i                                           Figure 7. The eval interpretation
5   invI_injI : ∀ i, invI (injI i) = i
6   out_eq : EPre.O = E.O
7
                                                                                Eff is defined by combining Eff.I and Eff.O.
8  instance {E EPre E1 } [UnfoldEffect E EPre] [sub : E1 -< EPre]
 9     : E1 -< E where                                                         Unfolding recursive effects. How can we work with the
10   mapI i := UnfoldEffect.injI (sub.mapI i)
11   mapO? o := sub.mapO? (Eq.mpr UnfoldEffect.out_eq o)
                                                                            recursive effects defined via fix_effect? This is where the
                                                                            UnfoldEffect typeclass comes into play, shown in Figure 6c.
                           (c) Unfolding effects.                           Intuitively, UnfoldEffect E EPre states that the recursive effect
                                                                            E is isomorphic to its unfolding EPre. The fix_effect command
                 Figure 6. The fix_effect command.                          generates an instance UnfoldEffect Eff (Eff.Pre Eff).
                                                                               UnfoldEffect is used to automatically lift properties of EPre
                                                                            to E. For example, Figure 6c shows that if E1 is a subeffect of
     ensure that Eff.I only appears as arguments to type con-               EPre, it is also a subeffect of E. We already used this implicitly
     structors of inductive types. In particular, we cannot use             in §2.1 when using operations of ConcE in HITree ExE Val. Note
     (E1 ⊕𝑒 ... ⊕𝑒 E𝑛 ).I directly (since the projection .I is not a        that EPre is an outParam of UnfoldEffect. This allows typeclass
     type constructor of an inductive type) but need to reduce it to        synthesis to determine EPre from E.
     expose input types of the effects E1 I ⊕ ... ⊕ E𝑛 I. Since the
     effect command generates the input types as inductive types,           4     Interpretations
     we know that E𝑖 I will be an inductive type. (The reduction
                                                                            This section presents two interpretations for HITrees: first,
     is also important to avoid spurious negative occurrences.)
                                                                            for execution (§4.1) and second, for reasoning (§4.2).
     Additionally, recall that the effect command (§3.2) expanded
     HITree E 𝜌 to HITree.Raw EI EO 𝜌 , avoiding the use of the pro-
                                                                            4.1    Execution using Monads
     jection .I. All of this together ensures that the generated
     inductive type is accepted by Lean.                                    The first interpretation enables the execution of HITrees
        As a concrete example, the input of the ExE effect from             by interpreting them into (executable) monads, provided by
     §2.1 is defined as follows:                                            Lean’s Monad typeclass. Central to this interpretation is the
                                                                            MHandler typeclass (Figure 7), which enables modular interpre-
1 fix_effect ExE := ConcE Val ExE ⊕𝑒 Fail
2 -- generates the following:
                                                                            tation of different effects. An instance of MHandler E E' 𝜌 m
3 inductive ExE.I where                                                     shows how to interpret any impure computation with input
4   | closed (_ : ConcE.I Val ExE.I ExE.O ⊕ FailE.I)                        i : E.I and continuation k of type E.O → HITree E' 𝜌 into
     Note ConcE takes ExE.I and ExE.O as separate arguments (as             the monad m. As a concrete example, consider the MHandler
     described in §3.2). This makes Lean accept this definition—in          instance for StateE from §2.1:
     contrast to the simplified version shown in §2.1 which would      1 instance {𝛼 E' 𝜌 m} [Monad m] [MonadState 𝛼 m]
                                                                       2   : MHandler (StateE 𝛼) E' 𝜌 m where
     be rejected since the recursive occurrence of ExE.I appears       3   handle i k := match i with
     under the constructor 〈Eff.I, Eff.O〉, which is not a type         4     | .get => do return k (StateE.O.get (← MonadState.get))
     constructor of an inductive type.                                 5     | .set v => do MonadState.set v; return k (StateE.O.set)
     HITrees: Higher-Order Interaction Trees


1 class EHandler (E E' : Effect) (𝜎 𝜌) where                                     This section describes how we adapt the technique from
2   handle : (i : E.I) → (s : 𝜎) → (k : E.O→HITree E' 𝜌) →
3            (p : HITree E' 𝜌 → 𝜎 → Prop) → Prop
                                                                              Vistrup et al. [2025] to interpret HITrees as state machines.13
4   handle_mono : ∀ {i s k p q},                                              These state machines can be seen as a big-step semantics
5     (∀ o s', p o s' → q o s') →                                             for HITrees and can be used to reason about all possible
6     handle i s k p → handle i s k q                                         executions of a HITree.
7
                                                                                 We follow the same recipe as §4.1: We first define a no-
8  inductive execPre exec : HITree E 𝜌 → 𝜎 →
9        (HITree E 𝜌 → 𝜎 → Prop) → Prop where                                 tion of handlers EHandler that describes how to interpret an
10   | halt t s p : p t s → execPre exec t s p                                individual effect into a small-step relation. Then, we define
11   | step i k s :                                                           a function exec that lifts these handlers to a big-step relation
12       EHandler.handle i s k (𝜆 t' s' => exec t' s' p) →                    on HITrees. (We also write (𝑡, 𝑠) ⇓ 𝑇 for exec t s T.) The
13       execPre exec (HITree.impure i k) s p
14
                                                                              definitions are shown in Figure 8.
15 def exec (t : HITree E 𝜌) (s : 𝜎)                                             The definition of EHandler follows the structure of MHandler:
16     (p : HITree E 𝜌 → 𝜎 → Prop) : Prop :=                                  EHandler is parameterized by (1) the effect E whose semantics
17   execPre exec t s p                                                       is being defined, (2) the effect E’ and return type 𝜌 of the
18 coinductive_fixpoint monotonicity fun f f' himp => by ...
                                                                              continuation, and (3) the state 𝜎 of the EHandler. The handle
                                                                              predicate gives the small-step relation for the input i : E.I,
                    Figure 8. The exec interpretation
                                                                              state s : 𝜎 , and continuation k. The final states of the step are
                                                                              given by the set p, following Omnisemantics [Charguéraud
                                                                              et al. 2023]). handle_mono states that handle is monotonic in p.
                                                                                 Consider the EHandler for DemonicE from §2 as an example:
     This handler interprets StateE 𝛼 into an arbitrary monad m           1 instance {𝛼 E 𝜌} : EHandler (DemonicE 𝛼) E Unit 𝜌 where
     that provides a state of type 𝛼 . (This requirement is encoded       2   handle i s k p := ∃ x : 𝛼, i.1 x ∧
     using [MonadState 𝛼 m].) The handler checks whether the in-          3                        p (k (DemonicE.O.choose x)) ()
     put i is a get or set and forwards it to the get resp. set of the    4   handle_mono := by grind
     underlying monad.                                                        To construct an execution of a demonic choice we must show
        Such individual handlers can be lifted to a composite ef-             that there exists a choice x satisfying the predicate i.1 passed
     fect like ExE using the sum handler sumMH (Figure 7). This               as the input to the choice (see §2.1). The final state is the
     handler lifts MHandlers for E1 and E2 to an MHandler for E1 ⊕𝑒 E2        continuation k applied to x (with unit for the state).
     by matching on the sum in the input and then invoking                       To define exec, we first introduce the predicate execPre that
     the respective handler. For effect fixpoints, the unfoldMH han-          models one step of the execution. There are two cases: Either
     dler lifts the MHandler for EPre to the MHandler for E given             the execution halts using execPre.halt by showing that p con-
     UnfoldEffect E EPre.                                                     tains the current HITree t and state s. Or if t is .impure i k,
        These MHandlers are used by the eval function to interpret            execPre.step executes a small step using EHandler.handle and
     a HITree into a monad m. eval recursively pattern matches on             then continues the execution for the resulting HITree and
     the HITree: for .pure r, eval returns r; for .impure i k, eval           state. exec is then defined as the co-inductive fixpoint of
     invokes the MHandler to interpret the effect and continues               execPre. The use of co-induction means that exec can repre-
     with the resulting HITree; for .unreachable, eval terminates             sent infinite executions. Using the coinductive_fixpoint com-
     the interpretation by panicking.                                         mand requires proving that exec is monotonic, which follows
                                                                              from handle_mono.
        Simple MHandler. The handle function of MHandler is very                 Following Vistrup et al. [2025], we obtain rules for rea-
     powerful: It takes as argument the full continuation k and               soning about exec, in particular for co-induction, bind, and
     can return an arbitrary HITree, not just a version of k. We              lifting EHandler through effect composition.
     will see in §5 how this allows interpreting effects that alter
     the control flow like concurrency. However, for many effects             5    Effects
     a simpler variant suffices:                                                 §2 showed the basics of defining and using effects. This
1 class SMHandler (E m) [Monad m] where                                       section comes back to the most interesting higher-order
2   handle : E.I → m E.O                                                      effects and their interpretations. In particular, we discuss
3 instance [Monad m] [SMHandler E m] : MHandler E E' 𝜌 m where                RecE and ConcE from §2.1 and introduce a call/cc effect.
4   handle i k := do return k (← SMHandler.handle i)
                                                                                 Recursion. Figure 9a shows the recursion effect RecE. Re-
     SMHandler.handle interprets E.I directly to E.O using m. SMHandler       call from §2.1 that RecE provides two operations: fix to create
     makes it simpler to define MHandler for effects like StateE.
                                                                              13 Vistrup et al. [2025] only describe a version of the technique that does not

                                                                              provide access to the continuation in the paper, but provide the full version
     4.2   Reasoning using State Machine Semantics
                                                                              in their Rocq development. We follow their Rocq development.
                                                                                               Amir Mohammad Fadaei Ayyam and M. Sammler

1 private structure FId where id : Nat                                 1 abbrev TId := Nat
2 effect RecE (𝛼 𝛽 : Type) (E : Effect) where                          2 private inductive Thread 𝛼 E 𝜌 where
3   | fix : (_ : FId → 𝛼 → HITree E 𝛽) (_ : 𝛼) → 𝛽                     3   | yielded (t : HITree E 𝜌) | completed (val : 𝛼)
4   | call : (_ : FId) (_ : 𝛼) → 𝛽                                     4   | blocked (b1 : TId) (b2 : TId) (k : ConcE.O 𝛼 → HITree E 𝜌)
5                                                                      5 abbrev ThreadPool 𝛼 E 𝜌 := List (Thread 𝛼 E 𝜌)
6  instance {𝜌 E 𝛼 𝛽} : EHandler (RecE 𝛼 𝛽 E) E                        6
7      (List (𝛼 → HITree E 𝛽)) 𝜌 where                                 7 private def Thread.continue? (th : Thread 𝛼 E 𝜌)
 8   handle i s k p := match i with                                    8     (tp : ThreadPool 𝛼 E 𝜌) : Option (HITree E 𝜌) :=
 9     | RecE.I.fix f a => let f' := f 〈s.length〉;                     9 /- check if th is yielded or its blocking threads completed -/
10        p (do let r ← f' a; k (RecE.O.fix r)) (s ++ [f'])            10
11     | RecE.I.call fid a => match s[fid.id]? with                    11 structure HandlerState 𝛼 E 𝜌 where
12        | some f => p (do let r ← f a; k (RecE.O.call r)) s          12   curr : TId
13        | none   => True                                             13   tp : ThreadPool 𝛼 E 𝜌
14   handle_mono := by grind                                           14
15                                                                     15 /- EHandler -/
16 instance {m 𝜌 E 𝛼 𝛽} [RecE 𝛼 𝛽 E -< E] [Monad m]                    16 def choose_thread (tp : ThreadPool 𝛼 E 𝜌) p :=
17    [MonadStateOf (List (𝛼 → HITree E 𝛽)) m] :                       17   ∃ nextId nextThread t, tp[nextId]? = some nextThread ∧
18    MHandler (RecE 𝛼 𝛽 E) E 𝜌 m where                                18     nextThread.continue? tp = some t ∧ p t 〈curr, tp〉
19   handle i k := do                                                  19
20     let s ← get; match i with                                       20 instance : EHandler (ConcE 𝛼 E) E (HandlerState 𝛼 E 𝜌) 𝜌 where
21     | RecE.I.fix f a =>                                             21   handle i s k p :=
22       let f' := f 〈s.length〉; set (s ++ [f'])                       22     match i with
23       return (do let r ← f' a; k (RecE.O.fix r))                    23     | .par t1 t2 => let 〈curr, tp〉 := s
24     | RecE.I.call fid a => match s[fid.id]? with                    24       let t' := Thread.blocked tp.length tp.length.succ k
25       | some f => return (do let r ← f a; k (RecE.O.call r))        25       let tp' := (tp.set curr t') ++ [.yielded t1 , .yielded t2 ]
26       | none => panic! "Invalid FId"                                26       choose_thread tp' p
                                                                       27     | .yield => let 〈curr, tp〉 := s
                        (a) The recursion effect.                      28       let tp' := tp.set curr (.yielded (k .yield))
1 private structure KId where id : Nat                                 29       choose_thread tp' p
2 effect CallccE (𝛼 : Type) (E : Effect) where                         30     | .kill v => let 〈curr, tp〉 := s
3   | callcc (f : KId → HITree E Empty) : 𝛼                            31       let tp' := tp.set curr (.completed v)
4   | throw (v : 𝛼) (k : KId) : Empty                                  32       choose_thread tp' p
5                                                                      33   handle_mono := by ...
6  instance {𝛼 E 𝜌} : EHandler (CallccE 𝛼 E) E                         34
7      (List (𝛼 → HITree E 𝜌)) 𝜌 where                                 35 /- MHandler -/
 8   handle i s k p := match i with                                    36 def schedule (s : HandlerState 𝛼 E 𝜌) :
 9     | .callcc f => let id := 〈s.length〉                             37   HandlerState 𝛼 E 𝜌 × HITree E 𝜌 :=
10       p ((f id).bind Empty.elim) (s ++ [𝜆 v => k (.callcc v)])      38 /- schedule next unblocked thread in round-robin -/
11     | .throw v k => match s[k.id]? with                             39
12       | some k => p (k v) s                                         40 instance [Monad m] [MonadStateOf (HandlerState 𝛼 E 𝜌) m]
13       | none => True                                                41     [Inhabited 𝛼] : MHandler (ConcE 𝛼 E) E 𝜌 m where
14 -- MHandler is analogous                                            42   handle i k := match i with
                                                                       43     | .par t1 t2 => do
                          (b) The call/cc effect.                      44       let 〈curr, tp〉 ← get
                                                                       45       let t' := Thread.blocked tp.length tp.length.succ k
             Figure 9. Effects and their interpretations.              46       let tp := (tp.set curr t') ++ [.yielded t1 , .yielded t2 ]
                                                                       47       let 〈s', t'〉 := schedule {curr, tp}; set s'; return t'
                                                                       48     | .yield => do
     a fixpoint and call to invoke a fixpoint. Fixpoints are repre-    49       let 〈curr, tp〉 ← get
                                                                       50       let tp := tp.set curr (.yielded (k .yield))
     sented using the FId type, which serve as abstract identifiers    51       let 〈s', t'〉 := schedule {curr, tp}; set s'; return t'
     (implemented by natural numbers).                                 52     | .kill v => do
        Both the EHandler and MHandler for RecE follow the same        53       let 〈curr, tp〉 ← get
     strategy to implement the effect: They store a list of HITree     54       let tp := tp.set curr (.completed v)
                                                                       55       let 〈s', t'〉 := schedule {curr, tp}; set s'; return t'
     functions representing the fixpoints, with the index in the
     list representing the id of the fixpoint. Invoking fix with a
     function f first provides the id of the new fixpoint to f. Then           Figure 10. Interpretation of the concurrency effect.
     it appends the resulting function f' to the list of fixpoints
     and continues with the HITree executing f' and the k. The
     handler for call looks up the corresponding fixpoint for an               Call/CC. Control effects like call/cc are a notoriously sub-
     identifier (terminating the execution if it does not exist) and        tle feature in higher-order languages [Dreyer et al. 2012]. To
     executes the fixpoint. Together, these encode the desired              show that HITrees can support control effects, we implement
     behavior for recursion where one can create new recursive              the CallccE effect in Figure 9b. CallccE provides two opera-
     functions via fix that can invoke themselves using call.               tions: callcc captures the current continuation and passes it
HITrees: Higher-Order Interaction Trees


                                                                            1  def awk := [𝜆|
𝑣 ∈ Val F 𝑧 | ℓ | (𝑣 1, 𝑣 2 ) | 𝑘 | 𝜆𝑥 . 𝑒     (𝑧 ∈ Z, ℓ,𝑘 ∈ N)             2    let x := ref #0 in
                                                                             3   𝜆 f, (x ← #0; f #(); x ← #1; f #(); assert (!x = #1))
𝑒 ∈ Exp F 𝑣 | 𝑥 | 𝑒 1 b
                      + 𝑒2 | 𝑒1 b
                                = 𝑒 2 | 𝑒.1 | 𝑒.2 | ! 𝑒 | 𝑒 1 ← 𝑒 2 |        4 ]
         ref(𝑒) | 𝑒 1 || 𝑒 2 | 𝑒 1 (𝑒 2 ) | call/cc(𝑒) | throw(𝑒) |          5 def C_callcc := [𝜆|
                                                                             6   let g := $awk in let b := ref #0 in
         assert(𝑒) | faa(𝑒) | if 𝑒 1 then 𝑒 2 else 𝑒 3                       7   let f := (𝜆 _, if !b then -- ! is a load, not negation
 let 𝑥 = 𝑒 1 in 𝑒 2 ≜ (𝜆𝑥 . 𝑒 2 ) (𝑒 1 )   𝑒 1 ; 𝑒 2 ≜ let _ = 𝑒 1 in 𝑒 2    8     call/cc (𝜆 k, g (𝜆 _, throw #() to k)) else b ← #1) in
                                                                             9   g f
                                                                            10 ]
Figure 11. 𝜆par,callcc , parts shared with ExampleLang in gray.             11 #eval eval C_callcc -- fails with assertion failure
                                                                            12 theorem callcc p : exec C_callcc.denote default p := by ...
                                                                            13
                                                                            14 def C_conc := [𝜆|
                                                                            15   let g := $awk in let f := 𝜆 _, #() in g f || g f
                                                                            16 ]
                                                                            17 #eval eval C_conc -- succeeds
as an abstract identifier KId to the function f. throw invokes              18 theorem conc p : exec C_conc.denote default p := by ...

the continuation k with value v. (Note that we use defunc-
tionalization via KId to deal with higher-order HITrees, here                                  Figure 12. Very awkward example.
the continuation, in a negative position.) The interpretation
of CallccE is straightforward since both EHandler and MHandler
provide the handle function with the current continuation.                       6    Case study: 𝜆par,callcc
The handlers store the continuations in a list in the state and                  To evaluate HITrees and their interpretations, we use them
invoke them on throw.                                                            to define the semantics of the lambda calculus 𝜆par,callcc com-
                                                                                 bining concurrency and call/cc.14 The syntax of 𝜆par,callcc is
   Concurrency. The interpretations of the ConcE effect from                     shown in Figure 11. 𝜆par,callcc extends ExampleLang from §2
§2.1 are shown in Figure 10. First, we define the ThreadPool                     with call/cc by adding the call/cc(𝑒) and throw(𝑒) expres-
data structure used by both interpretations. A ThreadPool is a                   sions. Captured continuations are represented as the values
list of Threads where each thread can either be yielded with                                                                   = 𝑒 2 , an assert(𝑒)
                                                                                 𝑘. 𝜆par,callcc adds an equality operation 𝑒 1 b
body t, completed with resulting value val, or blocked on a                      expression that checks that 𝑒 evaluates to a non-zero in-
parallel composition. A blocked thread tracks the thread                         tegers, an atomic fetch-and-add faa(𝑒), and if-expressions.
identifiers b1 and b2 of the two threads of the parallel compo-                  Let-bindings and sequencing are defined as standard.
sition and the continuation k with the computation after the                      Denotational semantics. We define the denotational se-
parallel composition. The Thread.continue? function checks                       mantics of 𝜆par,callcc based on the following effect:
if the thread th can continue by checking that it is either                 1    fix_effect E := StateE (ExtTreeMap Loc Val) ⊕𝑒 CallccE Val E
yielded or it is blocked and the two blocking threads have                  2       ⊕𝑒 RecE Exp Val E ⊕𝑒 ConcE Val E ⊕𝑒 FailE ⊕𝑒 DemonicE Loc
completed. The state HandlerState combines a ThreadPool with
                                                                                 The effect E provides the effects necessary to model 𝜆par,callcc :
the id of the currently executing thread.
                                                                                 StateE to model the heap, CallccE for call/cc(𝑒), RecE to
   The EHandler picks the next thread using the choose_thread
                                                                                 represent recursive functions, ConCE for concurrency, FailE to
function. This function uses an existential quantifier to model
                                                                                 model failing executions, and DemonicE for non-deterministic
the non-deterministic scheduling usually used by operational
                                                                                 allocation. Using this effect, we define a recursive denote
semantics. The EHandler handles the three operations of ConcE:
                                                                                 function similar to the denote function from §2. call/cc(𝑒)
par t1 t2 marks the current thread as blocked and adds t1 and
                                                                                 and throw(𝑒) dispatch to the corresponding operations of
t2 as new threads that can be executed, before choosing the
                                                                                 the CallccE effect. The placement of yields follows Vistrup
next thread. yield updates the current thread in the thread
                                                                                 et al. [2025].
pool to k and then chooses a new thread. kill sets the current
thread to completed. The choose_thread will not pick this thread                    Very awkward example. From this denotational seman-
again since it cannot continue. Overall, this handler allows                     tics we automatically obtain the evaluation and state ma-
us to reason about all possible concurrent executions using                      chine interpretations described in §4 by composing the han-
a non-deterministic thread pool semantics.                                       dlers for the individual effects. Our Lean development uses
   For the MHandler, the schedule function implements a round-                   a few small examples to test these interpretations. Here we
robin scheduler. The MHandler follows EHandler, except that it                   focus on the most interesting of these examples: the very
uses schedule as a concrete implementation of a scheduler.                       awkward example [Dreyer et al. 2012] shown in Figure 12.
This allows us to evaluate and test concurrent HITrees. In the                   (We use Lean’s extensible syntax mechanisms [Ullrich and
future, it would be interesting to explore different scheduling
strategies.                                                                      14 Our implementation of 𝜆
                                                                                                              par,callcc is inspired by SimpLang [Chajed 2025].
                                                                                                Amir Mohammad Fadaei Ayyam and M. Sammler


de Moura 2020] to embed 𝜆par,callcc programs inside [𝜆| ...].               but there might be other problematic dependent effects that
$awk embeds the definition of awk inside C_callcc and C_conc.)              we have not considered.
   The very awkward example tests whether a language                           Another difference of HITrees compared to ITrees is that
enforces well-bracketed control-flow. Concretely, for a lan-                HITrees are defined as an inductive type instead of a co-
guage with well-bracketed control flow, there is no context                 inductive type. This is mostly due to the fact that Lean does
that makes the assertion in awk fail [Dreyer et al. 2012]. How-             not have native support for co-inductive types. (We do not
ever, 𝜆par,callcc provides two mechanisms that break well-                  foresee a technical problem with building a co-inductive
bracketed control flow: call/cc and concurrency. We provide                 version of HITrees in Rocq.) Using an inductive type makes
two contexts, C_callcc and C_conc, that use these features                  the meta-theory of HITrees simpler since it avoids the need
respectively to violate the assertion in awk.                               for the Tau constructor of ITrees. This means that HITrees
   C_callcc uses call/cc to capture the assert in the continua-             can use the standard notion of equality instead of the equality
tion the second time f is invoked, and then jump to it after                up to (finitely many) Tau used by ITrees. On the flip side,
x has been set to 0 in a second invocation of g. Luckily, we                HITrees cannot natively represent infinite computations.
do not need to understand these details to see that C_callcc                Instead, HITrees rely on effects like rec from §2.1 to encode
violates the assertion—we can just use the eval interpretation              loops.
to execute the HITree. This evaluation indeed triggers the                     An important difference between ITrees and HITrees is
assertion failure. We also use exec to prove that there is an               how one reasons about them. Xia et al. [2020] provide a rich
execution of C_callcc where the assertion fails. Concretely,                theory of equational reasoning principles for ITrees and use
we show that we can prove exec C_callcc.denote default p                    them to reason about the step-wise interpretation of effects
where default is the initial state of 𝜆par,callcc and p is an ar-           into other ITrees. In contrast, such step-wise interpretation
bitrary postcondition. The fact that we can prove this for                  is more challenging for HITrees since they cannot natively
an arbitrary p means that the behavior is unconstrained, i.e.,              represent infinite computations (see above) and thus HITrees
that the program exhibits the undefined behavior caused by                  cannot represent the interpretation of effects like RecE. As
a failed assertion.                                                         a consequence, the equational theory of HITrees cannot be
   For C_conc, the evaluation using eval does not trigger the               used to reason about the interpretation of effects. In partic-
failed assertion since the round-robin scheduler does not                   ular, we do not have rec 𝑓 = 𝑓 (rec 𝑓 ). (rec only becomes
pick the right interleaving for this. We show using exec that               meaningful when paired with an interpretation (§4, §5).)
there in fact exists a schedule that violates the assertion (the            Instead of relying on equational reasoning and step-wise in-
schedule where the x ← 0 of the one thread is executed right                terpretation, we follow Vistrup et al. [2025] and Seassau et al.
before the assert (!x = 1) of the other thread).                            [2025] and directly interpret HITrees into a rich domain—
                                                                            Lean’s monads or a state machine semantics. §4 and §5 show
7    Related Work                                                           how this allows us to model even complex effects like de-
This section first compares the design and trade-offs of HITrees            monic non-determinism, call/cc, or concurrency.
to ITrees [Xia et al. 2020] before discussing related work
more broadly.                                                                  Related work. Defining denotational semantics using free
                                                                            monads goes back to the Datatypes à la carte paper [Swier-
   HITrees vs. ITrees. We compare HITrees and ITrees on                     stra 2008] that popularized free monads in Haskell. Subse-
three different axes: the notion of effects, the use of induction           quent work on the free-er monad [Apfelmus 2010; Kiselyov
vs. co-induction, and the reasoning styles.                                 and Ishii 2015; Kiselyov et al. 2013] refined the definition
   The key feature of HITrees is their support for higher-                  of free monads by exposing the continuation in the impure
order effects like ConcE (§2) that cannot be directly repre-                constructor. This definition was adapted by Letan and Régis-
sented in ITrees. However, HITrees have to pay a price: For                 Gianas [2020] and Xia et al. [2020] into the FreeSpec resp.
HITree effects (unlike ITree effects) the type of outputs can-              interaction trees libraries inside the Rocq proof assistant,
not depend on the input (statically). §2 demonstrated how to                with FreeSpec using an inductive definition focusing on mod-
encode such dependencies dynamically using .unreachable.                    eling first-order, low-level devices, while interaction trees
But this requires a decidable dynamic cast and there are ef-                use a co-inductive definition with a rich equational theory.
fects, like try 1 of DemonicE in §2.1 that cannot be encoded                Subsequent work extended interaction trees to represent
with a dynamic cast (in this case, since equality on types                  non-deterministic programs [Chappe et al. 2023]. Foster et al.
is not decidable).15 §2.1 shows how to obtain a version of                  [2025] show how to implement a version of interaction trees
DemonicE suitable for defining the semantics of allocation.                 in Isabelle/HOL. To our knowledge, none of this work on free
DemonicE (and its dual AngelicE) are the only effects where we              monads in proof assistants considered higher-order effects. It
encountered issues with providing decidable dynamic casts,                  is unclear how interaction trees could support higher-order
15 One can use excluded middle to avoid the decidability requirement, but   effects due to the negative occurrence of the input type in
this makes the HITree noncomputable.                                        the definition of ITrees.
HITrees: Higher-Order Interaction Trees


   We are only aware of one version of interaction trees that                 Dan Frumin, Amin Timany, and Lars Birkedal. 2024. Modular Denotational
support higher-order effects: guarded interaction trees [Fru-                    Semantics for Effects with Guarded Interaction Trees. Proc. ACM Program.
min et al. 2024; Stepanenko et al. 2025]. Guarded interaction                    Lang. 8, POPL (2024), 332–361. doi:10.1145/3632854
                                                                              Ronghui Gu, Zhong Shao, Hao Chen, Jieung Kim, Jérémie Koenig, Xiong-
trees leverage a guarded type theory to support higher-order                     nan (Newman) Wu, Vilhelm Sjöberg, and David Costanzo. 2019. Building
inputs and outputs. They show that this makes GITrees                            Certified Concurrent OS Kernels. Commun. ACM 62, 10 (2019), 89–99.
a powerful denotational semantic that allows interopera-                         doi:10.1145/3356903
tion between different higher-order languages. However,                       Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars
working inside the guarded type theory instead of the ambi-                      Birkedal, and Derek Dreyer. 2018. Iris from the ground up: A mod-
                                                                                 ular foundation for higher-order concurrent separation logic. J. Funct.
ent type theory of the proof assistant makes GITrees more                        Program. 28 (2018), e20. https://doi.org/10.1017/S0956796818000151
cumbersome to use (e.g., by requiring reasoning about step-                   Oleg Kiselyov and Hiromi Ishii. 2015. Freer monads, more extensible effects.
indexing). Instead, we show how one can encode a higher-                         In Haskell. ACM, 94–105. doi:10.1145/2804302.2804319
order version of interaction trees inside the ambient type                    Oleg Kiselyov, Amr Sabry, and Cameron Swords. 2013. Extensible effects:
theory of a proof assistant. In the future, it would be interest-                an alternative to monad transformers. In Haskell. ACM, 59–70. doi:10.
                                                                                 1145/2503778.2503791
ing to investigate whether HITrees can be used as a suitable                  Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David
denotational semantics that allows interoperation between                        Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt, Rafal Kolan-
different languages.                                                             ski, Michael Norrish, Thomas Sewell, Harvey Tuch, and Simon Winwood.
   Vistrup et al. [2025] show how one can build a modular                        2009. seL4: Formal Verification of an OS Kernel. In SOSP. ACM, 207–220.
                                                                                 doi:10.1145/1629575.1629596
program logic based on ITrees. Their state machine inter-
                                                                              Xavier Leroy. 2006. Formal Certification of a Compiler Back-end or: Pro-
pretation of ITree is the bases the interpretation of HITrees                    gramming a Compiler with a Proof Assistant. In POPL. ACM, 42–54.
described in §4.2. In the future, we are interested in investi-                  doi:10.1145/1111037.1111042
gating whether one can adapt their separation-logic-based                     Thomas Letan and Yann Régis-Gianas. 2020. FreeSpec: specifying, verifying,
program logic to HITrees.                                                        and executing impure computations in Coq. In CPP. ACM, 32–46. doi:10.
                                                                                 1145/3372885.3373812
                                                                              Shih-Wei Li, Xupeng Li, Ronghui Gu, Jason Nieh, and John Zhuang Hui. 2021.
Acknowledgments                                                                  A Secure and Formally Verified Linux KVM Hypervisor. In IEEE Sym-
                                                                                 posium on Security and Privacy. IEEE, 1782–1799. doi:10.1109/SP40001.
We thank Thibaut Perami, Amin Timany, and Lars Birkedal                          2021.00049
for the insightful discussions about this work.                               Conor McBride. 2015. Turing-Completeness Totally Free. In MPC (LNCS,
                                                                                 Vol. 9129). Springer, 257–275. doi:10.1007/978-3-319-19797-5_13
                                                                              Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem Prover
References                                                                       and Programming Language. In Automated Deduction – CADE 28: 28th
                                                                                 International Conference on Automated Deduction, Virtual Event, July
Heinrich Apfelmus. 2010. The Operational Monad Tutorial. The                     12–15, 2021, Proceedings. Springer-Verlag, Berlin, Heidelberg, 625–635.
   Monad.Reader 15 (2010).                                                       doi:10.1007/978-3-030-79876-5_37
Calvin Beck, Hanxi Chen, and Steve Zdancewic. 2025. Vellvm: Formalizing       John C. Reynolds. 1972. Definitional interpreters for higher-order pro-
   the Informal LLVM - (Experience Report). In NFM (LNCS, Vol. 15682).           gramming languages. In ACM Annual Conference (2). ACM, 717–740.
   Springer, 91–99. doi:10.1007/978-3-031-93706-4_6                              doi:10.1145/800194.805852
Venanzio Capretta. 2005. General recursion via coinductive types. Log.        Michael Sammler, Simon Spies, Youngju Song, Emanuele D’Osualdo, Robbert
   Methods Comput. Sci. 1, 2 (2005). doi:10.2168/LMCS-1(2:1)2005
                                                                                 Krebbers, Deepak Garg, and Derek Dreyer. 2023. DimSum: A Decentral-
Tej Chajed. 2025. SimpLang. https://github.com/tchajed/iris-simp-lang/.          ized Approach to Multi-language Semantics and Verification. Proc. ACM
Nicolas Chappe, Paul He, Ludovic Henrio, Yannick Zakowski, and Steve             Program. Lang. 7, POPL (2023), 775–805. doi:10.1145/3571220
   Zdancewic. 2023. Choice Trees: Representing Nondeterministic, Recur-       Remy Seassau, Irene Yoon, Jean-Marie Madiot, and François Pottier. 2025.
   sive, and Impure Programs in Coq. Proc. ACM Program. Lang. 7, POPL            Formal Semantics and Program Logics for a Fragment of OCaml. Proc.
   (2023), 1770–1800. doi:10.1145/3571254                                        ACM Program. Lang. 9, ICFP (Aug. 2025). doi:10.1145/3747509
Nicolas Chappe, Ludovic Henrio, and Yannick Zakowski. 2025. Monadic           Youngju Song, Minki Cho, Dongjae Lee, Chung-Kil Hur, Michael Sammler,
   Interpreters for Concurrent Memory Models: Executable Semantics of            and Derek Dreyer. 2023. Conditional Contextual Refinement. In POPL.
   a Concurrent Subset of LLVM IR. In CPP. ACM, 283–298. doi:10.1145/            ACM. doi:10.1145/3571232
   3703595.3705890                                                            Sergei Stepanenko, Emma Nardino, Dan Frumin, Amin Timany, and Lars
Arthur Charguéraud, Adam Chlipala, Andres Erbsen, and Samuel Gruetter.           Birkedal. 2025. Context-Dependent Effects in Guarded Interaction Trees.
   2023. Omnisemantics: Smooth Handling of Nondeterminism. ACM Trans.            In ESOP (2) (LNCS, Vol. 15695). Springer, 286–313. doi:10.1007/978-3-031-
   Program. Lang. Syst. 45, 1 (2023), 5:1–5:43. doi:10.1145/3579834              91121-7_12
Thierry Coquand and Christine Paulin. 1988. Inductively defined types. In     Wouter Swierstra. 2008. Data types à la carte. J. Funct. Program. 18, 4 (2008),
   Conference on Computer Logic (LNCS, Vol. 417). Springer, 50–66. doi:10.       423–436. doi:10.1017/S0956796808006758
   1007/3-540-52335-9_47                                                      Sebastian Ullrich and Leonardo de Moura. 2020. Beyond Notations: Hygienic
Derek Dreyer, Georg Neis, and Lars Birkedal. 2012. The impact of higher-         Macro Expansion for Theorem Proving Languages. In IJCAR (2) (LNCS,
   order state and control effects on local relational reasoning. J. Funct.      Vol. 12167). Springer, 167–182. doi:10.1007/978-3-030-51054-1_10
   Program. 22, 4-5 (2012), 477–528. doi:10.1017/S095679681200024X            Sebastian Ullrich and Leonardo de Moura. 2022. ’do’ unchained: embracing
Simon Foster, Chung-Kil Hur, and Jim Woodcock. 2025. Unifying Model              local imperativity in a purely functional language (functional pearl). Proc.
   Execution and Deductive Verification with Interaction Trees in Is-            ACM Program. Lang. 6, ICFP (2022), 512–539. doi:10.1145/3547640
   abelle/HOL. ACM Trans. Softw. Eng. Methodol. 34, 4 (2025), 108:1–108:40.
   doi:10.1145/3702981
                                                                            Amir Mohammad Fadaei Ayyam and M. Sammler


Max Vistrup, Michael Sammler, and Ralf Jung. 2025. Program Logics à la
   Carte. Proc. ACM Program. Lang. 9, POPL (2025), 300–331. doi:10.1145/
   3704847
Li-yao Xia, Yannick Zakowski, Paul He, Chung-Kil Hur, Gregory Malecha,
   Benjamin C. Pierce, and Steve Zdancewic. 2020. Interaction Trees: Rep-
   resenting Recursive and Impure Programs in Coq. Proc. ACM Program.
   Lang. 4, POPL (2020), 51:1–51:32. doi:10.1145/3371119
