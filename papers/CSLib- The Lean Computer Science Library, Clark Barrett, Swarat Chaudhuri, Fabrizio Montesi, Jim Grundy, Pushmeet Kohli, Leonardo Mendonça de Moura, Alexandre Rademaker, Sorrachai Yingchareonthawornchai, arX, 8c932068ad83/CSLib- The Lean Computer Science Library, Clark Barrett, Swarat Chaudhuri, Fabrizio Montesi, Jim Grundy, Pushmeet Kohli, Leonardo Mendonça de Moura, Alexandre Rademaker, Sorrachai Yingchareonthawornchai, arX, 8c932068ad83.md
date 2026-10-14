                                                           CSLib: The Lean Computer Science Library
                                            Clark Barrett1,2 , Swarat Chaudhuri3,4 , Fabrizio Montesi5 , Jim Grundy1 , Pushmeet Kohli3 ,
                                            Leonardo de Moura6,1 , Alexandre Rademaker7,8 , and Sorrachai Yingchareonthawornchai9
                                                                                             1
                                                                                              Amazon
                                                                                      2
                                                                                       Stanford University
                                                                                      3
                                                                                        Google DeepMind
arXiv:2602.04846v1 [cs.LO] 4 Feb 2026




                                                                             4
                                                                               The University of Texas at Austin
                                                                         5
                                                                           FORM, University of Southern Denmark
                                                                                           6
                                                                                             Lean FRO
                                                                                       7
                                                                                         Atlas Computing
                                                                                 8
                                                                                   Getulio Vargas Foundation
                                                                      9
                                                                        Institute for Theoretical Studies, ETH Zürich



                                                                                              Abstract
                                                  We introduce CSLib, an open-source framework for proving computer-science-related theorems and
                                              writing formally verified code in the Lean proof assistant. CSLib aims to be for computer science
                                              what Lean’s Mathlib is for mathematics. Mathlib has been tremendously impactful: it is a key reason for
                                              Lean’s popularity within the mathematics research community, and it has also played a critical role in the
                                              training of AI systems for mathematical reasoning. However, the base of computer science knowledge in
                                              Lean is currently quite limited. CSLib will vastly enhance this knowledge base and provide infrastructure
                                              for using this knowledge in real-world verification projects. By doing so, CSLib will (1) enable the broad
                                              use of Lean in computer science education and research, and (2) facilitate the manual and AI-aided
                                              engineering of large-scale formally verified systems.


                                        1    Introduction
                                        On its face, Mathlib [1] is a library of mathematical results and techniques formalized in the Lean [32] proof
                                        assistant. In reality, it is much more than that—it is a community effort by mathematicians all over the
                                        world to collect the world’s mathematical knowledge in a form that can easily be vetted and shared. Mathlib
                                        provides a platform for a new way to do mathematics, where many people can confidently collaborate on
                                        large and challenging projects [38]. Also, by representing a wide range of mathematical definitions and
                                        proofs in a machine-checkable form, it opens up new opportunities for AI systems to aid the process of
                                        mathematical discovery [44, 19]. This new approach to mathematics is being embraced by a new generation
                                        of mathematicians and has gained many prominent champions [41, 24]. Mathlib is at the heart of this
                                        paradigm shift, and as such, it is hard to overstate its impact.
                                            Computer science has always been close to mathematics. Many computer science departments originally
                                        emerged as offshoots of mathematics departments, and even today, the distinction between computer science
                                        theory and mathematics is blurry. Moreover, computer scientists have long recognized formal mathematics


                                                                                                  1
as a power tool that enables the design of reliable and secure systems [4, 9, 18]. However, until now there
has been no effort to build a Mathlib-like universal repository of formalized computer science knowledge.
    In this white paper, we introduce CSLib,1 a library for Lean-based formal verification and computer
science research that seeks to change this state of affairs. CSLib has two “pillars”:

   1. Formalizing all essential computer science concepts in Lean. The formalizations include, but are not
      limited to, models of computation such as the λ-calculus and resource-bounded Turing machines;
      numerous algorithms and data structures accompanied by proofs of correctness and complexity; con-
      currency theory; foundations of programming languages; and mathematical tools relevant to computer
      science that do not currently appear in Mathlib.

   2. Building an infrastructure for Lean-based reasoning about everyday imperative code. This infras-
      tructure consists of an intermediate programming language, called Boole, that allows classical im-
      perative constructs to be interspersed with specifications written in Lean; machinery for generating
      Lean-language verification conditions from Boole code; and verified Boole implementations of the
      algorithms and data structures covered in Pillar 1.

    Collectively, the Lean code and proofs in CSLib enable the use of Lean as a medium for mathematically
grounded computer science research and development. For example, we can imagine a theory researcher us-
ing CSLib’s built-in abstractions to quickly mock up a novel approximation algorithm and theorems captur-
ing its essential properties, a programming languages researcher using the framework to build verified com-
pilers, or a systems researcher using the library to model new network protocols with worst-case guarantees.
The Boole framework offers a crucial bridge from Lean to everyday programming languages. Specifically,
we envision a world in which code in mainstream languages like Rust and C++ is automatically translated
into Boole at scale. CSLib’s built-in infrastructure turns the task of verifying these Boole-language pro-
grams into that of proving Lean-language theorems. This proof task is then solved using Lean-language
proof machinery.

CSLib’s Impact. We see the impact of CSLib taking two forms: addressing an urgent practical need for
reliable software systems, and fulfilling a long-term need for more rigorous and scalable computer science.
    On the first point, progress on software reliability and security is more time-critical than ever because
of new risks that developments in AI pose to the world’s computing infrastructure. Today’s AI systems
have a remarkable ability to analyze code, making it much easier for an AI-powered malicious actor to find
and exploit vulnerabilities. At the same time, AI coding agents are writing more and more of the world’s
code. While this leads to overall productivity gains, AI can also introduce correctness errors and security
vulnerabilities into code [36]. Formal methods can mitigate these risks by mathematically proving code—
whether human-written or AI-generated—to be free of bugs and vulnerabilities.
    However, the impact of formal methods has been historically constrained by the immense human effort
that they require. Consider seL4 [23], the world’s first formally verified operating system kernel. The
system had a profound impact: an seL4-powered drone in the DARPA HACMS program famously resisted
six weeks of sustained attacks by an elite red team, leading the drone to be called the “most secure drone in
the world.” But seL4 also highlights the cost penalties associated with traditional formal verification. The
system required over 20 person-years of proof effort and included about 480,000 lines of formal specification
and proof in the Isabelle [34] framework. Such costs are difficult to justify in most commercial settings.
  1
   The main CSLib website is at https://cslib.io. The current CSLib codebase is at https://github.com/
leanprover/cslib/.


                                                     2
    The CSLib vision addresses this bottleneck in two ways. Once CSLib has been built, a developer would
be able to derive reliable and secure systems compositionally, by putting together pre-verified CSLib com-
ponents. Second, CSLib can simplify the use of AI in formal verification. AI systems have already demon-
strated superhuman formal proof capabilities in the pure mathematics setting [19]. However, to leverage
these capabilities in broad-domain code verification, we need a comprehensive language in which to specify
code properties. Lean and CSLib will provide this language. In addition, CSLib will serve as a repository
of high-quality data on which to train AI systems for formalization and formal proof.
    Beyond this impact on practical formal verification, CSLib will serve as a platform for 21st-century
computer science research. The formal verification that CSLib enables will induce confidence in claims
and allow the large-scale reuse of foundational concepts. We can also imagine AI tools trained on CSLib
discovering novel algorithms and settling open claims, extending to computer science the role that AI agents
are beginning to play in mathematics research.


2     Technical Approach
Now we provide some more details on the two pillars of CSLib’s technical approach.

2.1   Pillar 1: Formalizing Computer Science in Lean
CSLib’s first development pillar uses Lean to formalize a comprehensive body of models of computation,
algorithms, and data structures, along with properties of these artifacts and proofs of these properties. The
formalizations are designed to form a coherent and integrated framework rather than a collection of unrelated
modules. Such unification leads to a whole that is greater than the sum of its parts and has been key to
Mathlib’s impact.
     The pillar has a synergistic relationship with Mathlib. On the one hand, it heavily uses Mathlib modules
for, say, big-O reasoning and probability theory. On the other hand, it formalizes some core mathematics—
for example, certain lemmas from combinatorics needed to analyze approximation algorithms or inequalities
needed to prove the convergence of optimization algorithms—that are useful in computer science but do not
currently appear in Mathlib. Depending on the circumstances, we may either contribute these formalizations
to Mathlib or keep them within the CSLib repository.
     Now we provide some more details on this pillar’s targets.

Models & Logics. Over the years, computer scientists have designed a wide range of models of compu-
tation. These include models for deterministic, nondeterministic, probabilistic, and quantum computation;
models for functional computations, online algorithms, and interactive protocols; models that solve decision
problems; and models that approximately solve optimization problems. Many of these models have never
been formalized; the ones that have tend to exist in isolated repositories. A key goal of CSLib’s Pillar 1 is
to create a unified body of formalizations of these models.
    Another piece is the formalization of specification notations for models and algorithms. For example,
temporal logics are natural for specifying properties of stateful systems; Hoare logic is a standard mech-
anism for specifying procedural code; separation logic simplifies the specification of low-level imperative
computations; linear logic is suitable for reasoning about resource usage and concurrent behaviors. At this
point, there is no unified codebase consisting of such specification notations, and CSLib will address this
problem.



                                                     3
                                                               Deterministic                                                        Lists


                                   Finite words                Nondeterministic                                                     Graphs
                                                                                                       Data Structures
           Automata                Finite trees                ...                                                                  Hash tables


                                   ...                                                                                              ...


                                   Untyped                                                                                         Sorting


                                   Simply typed                                                        List algorithms             Selection
           λ-calculus
                                   Polymorphic                                                                                     ...


                                   ...                                                                                                  Pattern matching
                                               Deterministic
                                                                                                       String algorithms
                                                                                                                                        ...
                                               Nondeterministic

                                                                                                                                         Traversal
           Turing machines                     Probabilistic

                                                                                                                                         Shortest paths
                                               Quantum
                                                                                                       Graph algorithms
                                                                                                                                         Spanning trees
                                               ...

                                                                                                                                         ...
                             Temporal logic

                                                                                                                                         GCD
Models &                     Linear logic
 logics                                                                             Algorithms &
           Logics
                                                                                   data structures                                       Primality
                             Separation logic                                                          Number-theoretic
                                                                                                         algorithms
                                                                                                                                         Modular Arithmetic
                             ...                     P

                                                                                                                                         ...
                                                     NP
           Complexity classes
                                                                                                                            Convex hull
                                                     PSPACE
                                                                                                       Geometric
                                                                                                                            Voronoi diagrams
                                                     ...                                               algorithms

                                                                                                                            ...
                                    Labeled Transition System

                                                                                                                                     Linear
                                    Reduction System                                                                              programming
           Semantics
                                    Bisimulation                                                                                  Semidefinite
                                                                                                       Mathematical               programming
                                    ...                                                                optimization                                        Gradient descent
                                                                                                                                  Numerical
                                         Process calculi                                                                                                   ...
                                                                                                                                  ...
                                         Petri nets                                                                                            Database search
           Concurrency
                                         Choreographic languages                                       Quantum algorithms                      Factoring


                                         ...                                                           ...                                     ...

              (a) Models & logics                                                              (b) Algorithms and data structures

            Figure 1: CSLib’s Pillar 1: A possible organization of covered topics.



                                                                               4
  (a)                                                   (c)
                                                 theorem LTS.IsBisimulation.inv
  structure LTS
                                                     (h : lts.IsBisimulation r) :
      (State : Type u)
                                                     lts.IsBisimulation (flip r) := by
      (Label : Type v) where
                                                   simp only [IsBisimulation] at h
    /-- The transition relation. -/
                                                   simp only [IsBisimulation]
    Tr : State → Label → State → Prop
                                                   intro s1 s2 hrinv µ
                                                   constructor
  (b)                                              case left =>
  def LTS.IsBisimulation                             intro s1’ htr
      (lts : LTS State Label)                        specialize h hrinv µ
      (r : State → State → Prop) : Prop :=           have h’ := h.2 s1’ htr
    ∀ {|s1 s2|}, r s1 s2 → ∀ µ, (                    obtain ⟨s2’, h’⟩ := h’
      (∀ s1’, lts.Tr s1 µ s1’ → ∃ s2’, lts.Tr s2     exists s2’
        µ s2’ ∧ r s1’ s2’)                         case right =>
      ∧                                              intro s2’ htr
      (∀ s2’, lts.Tr s2 µ s2’ → ∃ s1’, lts.Tr s1     specialize h hrinv µ
        µ s1’ ∧ r s1’ s2’)                           have h’ := h.1 s2’ htr
    )                                                obtain ⟨s1’, h’⟩ := h’
                                                     exists s1’




Figure 2: (a) Definition of a Labeled Transition System (“LTS”), which models the observable behavior of
the possible states of a discrete computational system. (b) Definition of a bisimulation between two states.
(c) Theorem establishing that the inverse of a bisimulation is a bisimulation.


    While the specific set of formalizations that we will build in this pillar will necessarily evolve over time,
Figure 1-(a) spells out some of the models and logics we currently plan to cover. Figure 2-(a) and Figure 2-
(b) give concrete examples of formalizations. Specifically, Figure 2-(a) shows (part of) a Lean definition of
labeled transition systems [43], a classic model for stateful systems, and Figure 2-(b) defines bisimulations,
a key notion of equivalence between system states. If two states s1 and s2 are related by a bisimulation,
then s1 can mimic all transitions of s2 by a corresponding transition and vice versa, and the states reached
through these original and mimicking transitions remain related by the bisimulation.
    Transition systems and bisimulations have numerous applications in computer science, in areas from
hardware design [8] to control [13] to machine learning [45]. Formal definitions of these concepts and
associated theorems (such as the theorem in Figure 2-(c)) are therefore valuable both from a theoretical and
a practical perspective. However, such formalizations are not naturally in scope for Mathlib and are thus an
example of the distinct capabilities that CSLib will provide.

Algorithms & Data Structures. Pillar 1 will also use Lean to build a comprehensive repository of for-
mally verified algorithms and data structures. Our long-term ambition is for this library to cover all of
computer science. In the medium term, we aim for this library to cover all algorithms and data structures
that a typical computer science graduate is likely to encounter. Figure 1-(b) names some of the algorithmic
categories that we plan to cover.
    A key objective in this thread is to formalize analysis of algorithms, including, in particular, the com-
plexity of algorithms. We note that there is much prior work on automatic, lightweight complexity analysis
of programs [15, 39], and some work on proof-assistant-based complexity verification of specific algorithms
[7, 6] and formalization in Isabelle [33]. However, we are only aware of one effort [20] on the systematic
formalization of algorithmic complexity in Lean. That formalization [5] was focused on stochastic oracle


                                                       5
  structure TimeM (α : Type*) where
    ret : α
    time : N

  namespace TimeM

  protected def pure {α} (a : α) : TimeM α :=
    ⟨a, 0⟩

  def bind {α β} (m : TimeM α) (f : α → TimeM β) : TimeM β :=
    let r := f m.ret
    ⟨r.ret, m.time + r.time⟩

  instance : Monad TimeM where
    pure := pure
    bind := bind

  /-- Advances the time cost by ‘c‘ (default 1) without changing the value. -/
  def tick (c : N := 1) : TimeM PUnit := ⟨.unit, c⟩

  macro "✓[" c:term "]" body:doElem : doElem => ‘(doElem| do TimeM.tick c; body:doElem)
  /-- ‘✓ x‘ is ‘pure x‘, adding one tick. -/
  macro "✓" body:doElem : doElem => ‘(doElem| ✓[1] body)

  -- Simp lemmas
  @[simp] theorem ret_pure {α} (a : α) : (pure a : TimeM α).ret = a := rfl
  @[simp] theorem ret_bind {α β} (m : TimeM α) (f : α → TimeM β) :
    (m >>= f).ret = (f m.ret).ret := rfl
  @[simp] theorem ret_tick (c : N) : (tick c).ret = () := rfl
  @[simp] theorem time_bind {α β} (m : TimeM α) (f : α → TimeM β) :
    (m >>= f).time = m.time + (f m.ret).time := rfl
  @[simp] theorem time_pure {α} (a : α) : (pure a : TimeM α).time = 0 := rfl
  @[simp] theorem time_tick (c : N) : (tick c).time = c := rfl
  -- additional simp lemmas for <* and *> and <*>
  (...)

  end TimeM




Figure 3: A monadic API for complexity analysis of elementary algorithms. An object of type TimeM α
comprises ret, which is a value of type α, and the time cost incurred by the computation of this value. The
bind operation chains together two computations and defines the time cost of the composition as the sum of
the time costs of the individual operations. The helper function tick assigns the time cost. The notation ✓
is syntactic sugar for the invocation of tick. The final section asserts some basic lemmas that help simplify
expressions involving TimeM.




                                                     6
  import ComplexityAPI
  variable {α : Type} [LinearOrder α]

  def merge : List α → List α → TimeM (List α)
    | [], ys => return ys
    | xs, [] => return xs
    | x::xs’, y::ys’ => do
      ✓ let c := x ≤ y
      if c then
        let rest ← merge xs’ (y::ys’)
        return (x :: rest)
      else
        let rest ← merge (x::xs’) ys’
        return (y :: rest)

  /-- Merge sort algorithm that returns a ‘TimeM (List α)‘ where the time represents the total
      number of comparisons. -/
  def mergeSort (xs : List α) : TimeM (List α) := do
    if xs.length < 2 then return xs
    else
      let half := xs.length / 2
      let L := xs.take half
      let R := xs.drop half
      let L’ ← mergeSort L
      let R’ ← mergeSort R
      let result ← merge L’ R’
      return result

  /-- MergeSort is functionally correct. -/
  theorem mergeSort_correct (xs : List α) :
    IsSorted (mergeSort xs).ret ∧ List.Perm (mergeSort xs).ret xs           := by
    -- Proof omitted

  /-- Time complexity of mergeSort counted as the number of comparisons. -/
  theorem mergeSort_time (xs : List α) :
    let n := xs.length
    (mergeSort xs).time ≤ n * clog2 n := by
    -- Proof omitted




Figure 4: An implementation of Mergesort using the API in Figure 3. Note how each invocation of the
sorting routine returns a sorted list along with a computational cost. With these definitions in place, one can
formally state and prove theorems establishing the correctness of Mergesort and its worst-case number of
comparisons.




                                                      7
computations; by contrast, we aim for a universal framework for complexity analysis.
    The precise definition of the framework that we propose will require more work and evolve over time.
For now, we show in Figure 3 a simple monadic API, akin to Mathlib’s Writer monad and inspired by
prior work on analysis of functional algorithms [10, 12], that will be part of CSLib’s complexity analysis
framework. The API packages return values of procedures with the cost of computing these values; see
Figure 4 for an example of its use. Treating time complexity as a computational effect makes correctness
and complexity analysis orthogonal. Also, by giving users control over tick placement, the framework
enables experimentation with different cost models, enabling a diverse set of complexity analyses.
    At the same time, the API has multiple limitations. For example, it relies on manual tick annotations
that a user could accidentally get wrong rather than automated verification of execution costs. Also, it
cannot directly prove statements of the form “no algorithm can solve problem X faster than f (n).” However,
because it is lightweight and allows proof of many interesting theorems about algorithmic complexity, it is
a good starting point for our efforts. In the longer run, we plan to complement this approach with heavier-
weight methods that formalize complexity via explicit RAM and query models.

2.2    Pillar 2: Infrastructure for Reasoning about Everyday Code
CSLib’s second pillar will develop a powerful new infrastructure for reasoning about everyday imperative
code. Lean has recently added substantial support for the definition [42] and verification2 of imperative
programs, and we intend to leverage these advances in our Pillar-1 efforts. The methods we pursue in the
present pillar are complementary in that they connect Lean-based formal reasoning to the verification of
code in mainstream languages like Rust, Python, and C++.
    Our approach builds on the rich tradition of deductive verification techniques and tools [11, 17], in
particular systems built on top of intermediate verification languages (IVLs). Perhaps best-known is the
Boogie IVL [26, 28], which is used by many systems (e.g., Dafny [27], Viper [21], CIVL [25], and the
Move Prover [46]). CSLib’s Pillar 2 will be based on a new IVL called Boole, partly inspired by Boogie,
but also leveraging the capabilities and advantages of Lean.
    Figure 5 illustrates the long-term vision for CSLib-based code reasoning. We envision a framework
with support for multiple front-end languages. A user can write their code accompanied by specifications in
Lean. These are then transpiled (translated via compilation) to Boole. We plan to build a deductive verifica-
tion platform built around Boole, which can use various algorithms and back-ends to generate verification
conditions in Lean. These can then be discharged using various Lean automation techniques.
    This vision is guided by several forward-looking design principles, which aim to avoid shortcomings
and pitfalls revealed by previous work: (i) Boole should look like pseudocode and be easy for humans to
understand; (ii) Boole and its ecosystem will be embedded in Lean, and both the transpilation step and the
verification condition generation step should be implemented with the goal of minimizing the trusted com-
puting base (TCB); (iii) verification conditions should be generated as Lean goals and should be intuitive
for humans to read and easily connectable to the code they came from; and (iv) code specifications and
verification conditions should be able to leverage the rich formal universe defined in CSLib’s Pillar 1.
    Verification condition generation from Boole will build on infrastructure and ideas from other open
source projects, such as Loom [14] and Strata. Loom3 provides a mechanism for the definition of shallowly-
embedded languages in Lean (including a Dafny-like language called Velvet), with strong guarantees about
correct verification condition generation. Strata4 is an open-source project that aims at facilitating the cre-
   2
     https://lean-lang.org/doc/reference/latest/The--mvcgen--tactic/
   3
     https://github.com/verse-lab/loom
   4
     https://github.com/strata-org/Strata


                                                      8
                             Rust            Python                C/C++              Java         + Specs in Lean

      Trusted
      Computing Base:                                                             Verified Transpilation

      Semantics of PL
      Lean Kernel                                      Boole IVL
                                       Shallow                            Deep
                                      Embedding                         Embedding
                                          Velvet / Loom             Strata



                                             Verification Conditions in Lean




                 Grind     Lean SMT      Lean Hammer          LLM-based Provers      Other AI-based Provers




                                    Figure 5: CSLib Code Reasoning Vision.


ation of domain-specific languages called dialects, which are deeply embedded in Lean.
    Figure 6 shows a simple snippet of Lean code containing a program written in Boole. Boole is imple-
mented as an extension of the Core dialect of Strata, which in turn is largely modeled after the classic Boogie
IVL. After a prelude that imports and opens relevant packages, the program itself can be written in an easily
readable form. Notice the spec keyword, which signals a specification. In this case, there is a requirement
(precondition) that n should be non-negative indicated by the requires keyword. We can also specify a
loop invariant using the invariant keyword as well as more general program invariants that should hold
at specific points in the code using the assert keyword.
    We can verify the assertions by translating the specifications and code into verification conditions. This
can be done by assigning Lean semantics to each construct in the program and then following the standard
deductive verification approach, which involves proving, for certain loop-free paths in the program, that
for all possible executions along that path, the precondition for the path ensures the postcondition of the
path. The #prove_vcs command in our example invokes a prototype verification condition generator that
generates goals in Lean. A set of generated goals is shown in Figure 7. The first goal, for example, represents
a path from the entry to the procedure to the beginning of the loop. The precondition of the program requires
n ≥ 0, and the loop condition must be true, implying i < n. These should imply the loop invariant. Our
verification condition generator performs some basic simplification—in this case, it knows that i = 0 when
entering the loop, so it replaces i with 0 and simplifies. The result is the goal shown. Similarly, the second
goal represents the verification condition stating that the invariant is preserved around one iteration of the
loop, and the other two goals correspond to the two assertions.
    Goals in Lean can be proved by hand or by invoking hammers, which are general-purpose tactics for
automating proofs of Lean goals. A number of potential hammers are shown at the bottom of Figure 5. For

                                                          9
  import Strata.MetaVerifier
  import Smt
  import Smt.Rat

  open Strata

  def loopSimple : Strata.Program :=
  #strata
  program Boole;

  procedure loopSimple (n: int) returns (r: int)
  spec {
    requires (n >= 0);
  }
  {
    var sum : int;
    var i : int;

    sum := 0;
    i := 0;
    while(i < n)
      invariant (i <= n && ((i * (i-1)) div 2 == sum));
    {
      sum := sum + i;
      i := i + 1;
    }
    assert [sum_assert]: ((n * (n-1)) div 2 == sum);
    assert [neg_cond]: (i == n);
    r := sum;
  };
  #end

  #prove_vcs loopSimple by
    all_goals (try smt)




Figure 6: A simple program, written in the Boole dialect of Strata, for computing the sum of the first n
positive integers.


our example, a tactic called smt can solve all of them. This tactic uses the Lean-SMT tool [30] to translate
a goal into an SMT formula, call a solver, get a proof certificate, and then replay the proof step-by-step in
Lean. The number and capabilities of such hammers have been growing rapidly, and the future promises
even stronger hammers, including AI-based ones.
     The long-term roadmap for CSLib will involve extending Boole over time to add more functionality,
including cost semantics (to support reasoning about and proving theorems about computational complex-
ity), support for specifications using definitions from Mathlib and Pillar 1 of CSLib, support for reasoning
about concurrency, and support for reasoning about low-level constructs such as pointers. We will con-
sider modern programming abstractions and verification techniques, for example, as found in research on
choreographic programming [31, 40] and separation logic [22, 35].
     More significantly, we also intend for Boole to be used as a true intermediate language for the verifi-
cation of real systems in standard programming languages. The plan is to formalize the semantics of real
programming languages in Lean, use those semantics to translate code and specifications in those languages
into Boole code and specifications, and then use the verification tools we are building for Boole to verify
the translated code. The Aeneas project [16], which translates a sizeable subset of Rust into several proof


                                                     10
    case entry_invariant_0
    ⊢ ∀ (n : Int), 0 < n → n ≥ 0 → 0 ≤ n ∧ True

    case arbitrary_iter_maintain_invariant_0
    ⊢ ∀ (n i sum : Int),
      0 < n →
        i < n →
          i ≤ n ∧ i * (i - 1) / 2 = sum →
            n ≥ 0 → i + 1 ≤ n ∧ (i + 1) * (i + 1 - 1) / 2 = sum + i

    case sum_assert
    ⊢ ∀ (n i sum i’ sum’ : Int),
      n ≥ 0 →
        (if 0 < n then 0 < n else True) →
          (if 0 < n then i < n else True) →
            (if 0 < n then i ≤ n ∧ i * (i - 1) / 2 = sum else True) →
              (if 0 < n then ¬i’ < n else True) →
                (if 0 < n then i’ ≤ n ∧ i’ * (i’ - 1) / 2 = sum’ else True) →
                  (if if 0 < n then False else True then if 0 < n then False else True
        else True) →
                    n * (n - 1) / 2 = if 0 < n then sum’ else 0

    case neg_cond
    ⊢ ∀ (n i sum i’ sum’ : Int),
      n ≥ 0 →
        (if 0 < n then 0 < n else True) →
          (if 0 < n then i < n else True) →
            (if 0 < n then i ≤ n ∧ i * (i - 1) / 2 = sum else True) →
              (if 0 < n then ¬i’ < n else True) →
                (if 0 < n then i’ ≤ n ∧ i’ * (i’ - 1) / 2 = sum’ else True) →
                  (if if 0 < n then False else True then if 0 < n then False else True
        else True) →
                    (if 0 < n then i’ else 0) = n∀ (n : Int), 0 < n → n ≥ 0 → 0 ≤ n ∧
         True




                Figure 7: Lean verification conditions generated from the program in Figure 6.


assistants (including Lean), offers a model of such a pipeline.
    A final concrete goal of this pillar is to assemble a large library of code that has been certified using
the CSLib verification infrastructure. We plan to make this library freely available and to integrate it with
synergistic efforts such as VeriLib.5


3        The Role of AI
The CSLib community effort is motivated by the ongoing revolution in AI-based code generation in two
ways. On the one hand, we believe CSLib can be a part of our collective response to the risks of AI: the
ability of AI-powered malicious actors to break the world’s software and the possibility that engineers using
AI-based coding tools would unwittingly write vulnerable code. These risks make rigorous software verifi-
cation and formally verified code generation more important than ever, and CSLib will enable this. On the
other hand, AI projects such as AlphaProof [19], Deepseek-Prover [37], and Aristotle [2] showcase the abil-
ity of AI to solve hard formal proof tasks. However, AI-based provers are bottlenecked by the abstractions
    5
        https://verilib.org/



                                                     11
available in the underlying proof assistant. By expanding the universe of CS-relevant abstractions available
in Lean, CSLib will also vastly enhance the capabilities of such provers in formal verification settings.
    The formalizations produced in CSLib will serve as high-quality training data for AI-based formalization
and theorem-proving systems [19, 37, 29]. At the same time, we expect that AI-based tooling for Lean proofs
will vastly accelerate the development of CSLib. The ideal outcome would be a “flywheel” in which both
AI-based proof tools and human experts become progressively more efficient at producing new knowledge.
    One risk with the use of AI in a sophisticated development effort like CSLib is that AI-generated for-
malizations might be buggy. Also, while AI-generated Lean proofs of formal statements may be sound,
they may not be human-comprehensible. We will mitigate these risks by ensuring that AI tools play only
an advisory role in the development of CSLib, and that all formalizations and proofs that are committed to
CSLib are subject to a manual, Github-based code review process.


4       Building a CSLib Community
A library is only as impactful as its user base. While formal verification is a vibrant subarea of computer
science, we aim for CSLib’s impact to transcend that research area. We would like computer science re-
searchers of all sorts, from theorists to system-builders, to use CSLib in their everyday work. We want
CSLib to drastically reduce the cost of formal verification to the extent that engineers in a broad range of
industries choose to embrace formal techniques. We would like CSLib to be used in a broad swathe of
universities to teach the mathematical underpinnings of computer science.
    Fortunately, we can look to Mathlib [3] as a blueprint for achieving our goals. The Mathlib community
has demonstrated that open discussion and community activities are essential to making a large-scale for-
malization project such as ours successful. Following their lead, we have set up a CSLib channel 6 on the
Lean Zulip chat. This channel is already quite active, and we encourage everyone interested in the project to
join it. We also urge you to keep an eye out for the calls for contributions to specific components of CSLib
that we plan to issue in the coming months. We also plan to hold many workshops and tutorials on CSLib
in the coming months and years. If you are interested in joining or leading such an event, please reach out
to us!
    Another dimension is the use of rigorous code review practices and the creation of tooling that lowers the
cost of CSLib development and maintenance. In particular, AI tools for automatic formalization and formal
theorem-proving have progressed at a breakneck pace over the last few years. As mentioned in Section 3, a
goal of the CSLib effort is to both leverage and improve such tools. We expect these tools to substantially
lower the barrier to developing and using CSLib.
    Dependently typed languages have historically existed in a separate universe from mainstream impera-
tive languages, and this is a key reason why their adoption has been limited. CSLib’s Pillar 2 aims to change
this status quo. The engineering of translations from mainstream languages like Rust and C++ to Boole will
be especially important for the success of this vision. We encourage community members to take on the
challenge of building these translations.
    Finally, we will prioritize building high-quality, searchable documentation for CSLib. Such documenta-
tion will include tutorials targeted specifically at researchers working in different areas of computer science,
as well as entry-level textbooks. Please write to us if you would like to lead or contribute to such a textbook.
    6
        https://leanprover.zulipchat.com/#narrow/channel/513188-CSLib




                                                      12
5    Governance Model
CSLib is governed by a dual-body structure designed to balance strategic direction with technical execution.
A steering committee comprising leaders from academia and industry is responsible for securing financial
support and guiding the project’s overall vision. The founding members of this committee are Clark Bar-
rett (Stanford University & Amazon Web Services), Swarat Chaudhuri (Google DeepMind & UT Austin),
Jim Grundy (Amazon Web Services), Pushmeet Kohli (Google DeepMind), Fabrizio Montesi (University of
Southern Denmark), and Leonardo de Moura (Lean FRO & Amazon Web Services). Working alongside this
committee, a maintainer team manages the codebase’s technical direction, quality standards, and day-to-day
development. As of the date of this paper, the team is headed by a lead maintainer (Fabrizio Montesi), who
coordinates overall efforts, and includes technical leads (Alexandre Rademaker and Sorrachai Yingchare-
onthawornchai) for long-term cross-cutting developments, and area maintainers (Chris Henson and Kim
Morrison) taking ownership of specific domains such as λ-calculi, metaprogramming, and CI/CD infras-
tructure.
     Naturally, we expect the maintainer team and the steering committee to change as the community grows.
Specifically, we plan to periodically invite new maintainers based on merit—particularly, contributions and
review activity—and project needs. The goal is to ensure strategic coherence through the steering commit-
tee’s guidance and technical excellence through the maintainer team’s specialized expertise, while fostering
a welcoming environment for a broad set of contributors.


6    Roadmap
Now we present a brief overview of how we see the CSLib project evolving over 2026 and 2027. This
roadmap is tentative given that the project is currently only a few months old and that we plan to refine
its scope with community input. A more detailed (and periodically revised) roadmap can be found on the
CSLib website: https://cslib.io.

2026. The CSLib repository already includes initial Lean formalizations of operational semantics, pro-
gram equivalences, several automata models, a linear logic, and a few elementary sorting and searching
algorithms. We expect that by the end of 2026, CSLib will include formalizations of many algorithms cov-
ered in a typical undergraduate algorithms and data structures course, and most of the models and logics
covered in a typical undergraduate theory of computation course. In addition, community members will be
welcome to contribute formalizations from specialized research areas that they work on. Note that progress
on this Pillar-1 task does not depend on Boole to be ready.
     As for Pillar 2, we have already developed an initial version of Boole on top of the Strata framework.
Over the next year, we expect the framework to mature substantially. By the end of 2026, the Boole frame-
work will have robust capabilities for generating Lean-language verification conditions and interacting with
SMT-based hammers. By that point, the CSLib repository will include Boole-language representations of a
sizeable number of elementary algorithms and data structures, along with Lean specifications and proofs of
all relevant verification conditions.

2027. The project’s second year will focus on scale and unification. In particular, our Pillar-1 efforts will
move on to technically challenging topics such as complexity theory, concurrency, secure compilation, and
randomized and quantum algorithms. We expect that as a result, CSLib will have substantially aided at least
one important foundational discovery in computer science by the end of 2027. In our Pillar-2 efforts, we will

                                                     13
extend Boole to support machinery, such as separation logic, that is needed for the verification of low-level
systems code, and extensively use the Pillar-1 machinery to write more advanced system specifications.
We expect that by the end of 2027, CSLib will have enabled the end-to-end verification of at least one
substantially sized real-world system.

Acknowledgements
We thank all current and future contributors to CSLib7 for their work on the project, and Eric Wieser and
Tom Kalil for their thoughtful feedback on this paper.


References
 [1] The Lean mathematical library. CoRR, abs/1910.09336, 2019.

 [2] T. Achim, A. Best, A. Bietti, K. Der, M. Fédérico, S. Gukov, D. Halpern-Leistner, K. Hennings-
     gard, Y. Kudryashov, A. Meiburg, M. Michelsen, R. Patterson, E. Rodriguez, L. Scharff, V. Shanker,
     V. Sicca, H. Sowrirajan, A. Swope, M. Tamas, V. Tenev, J. Thomm, H. Williams, and L. Wu. Aristotle:
     IMO-level automated theorem proving. arXiv preprint arXiv:2510.01346, 2025.

 [3] A. Baanen, M. R. Ballard, J. Commelin, B. G. ge Chen, M. Rothgang, and D. Testa. Growing mathlib:
     maintenance of a large scale mathematical library, 2025.

 [4] R. S. Boyer and J. S. Moore. Proof-checking, theorem-proving, and program verification. Technical
     report, Institute for Computing Science, The University of Texas at Austin, 1983.

 [5] J. Brown-Cohen, G. Irving, and G. Piliouras. Scalable ai safety via doubly-efficient debate. arXiv
     preprint arXiv:2311.14125, 2023.

 [6] H. Chan and M. Norrish. Mechanisation of the AKS algorithm. Journal of Automated Reasoning,
     65(2):205–256, 2021.

 [7] A. Charguéraud and F. Pottier. Verifying the correctness and amortized complexity of a union-find
     implementation in separation logic with time credits. Journal of Automated Reasoning, 62(3):331–
     365, 2019.

 [8] G. Chehaibar, H. Garavel, L. Mounier, N. Tawbi, and F. Zulian. Specification and verification of the
     powerscaletm bus arbitration protocol: An industrial experiment with lotos. In Formal Description
     Techniques IX: Theory, application and tools, pages 435–450. Springer, 1996.

 [9] E. M. Clarke. Model checking. In International conference on foundations of software technology and
     theoretical computer science, pages 54–56. Springer, 1997.

[10] N. A. Danielsson. Lightweight semiformal time complexity analysis for purely functional data struc-
     tures. In POPL, pages 133–144. ACM, 2008.

[11] R. W. Floyd. Assigning meanings to programs. In Mathematical Aspects of Computer Science, Pro-
     ceedings of Symposia in Applied Mathematics, pages 19–32. American Mathematical Society, 1967.
  7
   A list of current CSLib contributors is available at https://github.com/leanprover/cslib/graphs/
contributors.


                                                     14
[12] J. Gibbons and R. Hinze. Just do it: Simple monadic equational reasoning. In ICFP, pages 2–14.
     ACM, 2011.

[13] A. Girard and G. J. Pappas. Approximate bisimulation: A bridge between computer science and control
     theory. European Journal of Control, 17(5-6):568–578, 2011.

[14] V. Gladshtein, G. Pı̂rlea, Q. Zhao, V. Kurin, and I. Sergey. Foundational multi-modal program verifiers.
     Proc. ACM Program. Lang, 10, 2026.

[15] S. Gulwani, K. K. Mehra, and T. Chilimbi. Speed: precise and efficient static estimation of program
     computational complexity. ACM Sigplan Notices, 44(1):127–139, 2009.

[16] S. Ho and J. Protzenko. Aeneas: Rust verification by functional translation. Proceedings of the ACM
     on Programming Languages, 6(ICFP):711–741, 2022.

[17] C. A. R. Hoare. An axiomatic basis for computer programming. Commun. ACM, 12(10):576–580,
     1969.

[18] T. Hoare. The verifying compiler: A grand challenge for computing research. Journal of the ACM
     (JACM), 50(1):63–69, 2003.

[19] T. Hubert, R. Mehta, L. Sartran, M. Z. Horváth, G. Žužić, E. Wieser, A. Huang, J. Schrittwieser,
     Y. Schroecker, H. Masoom, et al. Olympiad-level formal mathematical reasoning with reinforcement
     learning. Nature, pages 1–3, 2025.

[20] G. Irving. Debate: Lean formalization of debate protocols. https://github.com/girving/
     debate, 2025.

[21] U. Juhasz, I. T. Kassios, P. Müller, M. Novacek, M. Schwerhoff, and A. J. Summers. Viper: A verifi-
     cation infrastructure for permission-based reasoning. Technical report, ETH Zurich, 2014.

[22] R. Jung, R. Krebbers, J. Jourdan, A. Bizjak, L. Birkedal, and D. Dreyer. Iris from the ground up: A
     modular foundation for higher-order concurrent separation logic. J. Funct. Program., 28:e20, 2018.

[23] G. Klein, K. Elphinstone, G. Heiser, J. Andronick, D. Cock, P. Derrin, D. Elkaduwe, K. Engelhardt,
     R. Kolanski, M. Norrish, et al. sel4: Formal verification of an OS kernel. In Proceedings of the ACM
     SIGOPS 22nd symposium on Operating systems principles, pages 207–220, 2009.

[24] A. Kontorovich. The shape of math to come. arXiv preprint arXiv:2510.15924, 2025.

[25] B. Kragl and S. Qadeer. The civl verifier. In Formal Methods in Computer Aided Design, FMCAD
     2021, New Haven, CT, USA, October 19-22, 2021, pages 143–152. IEEE, 2021.

[26] K. R. M. Leino. This is Boogie 2, 2008. Manuscript KRML 178.

[27] K. R. M. Leino. Dafny: An automatic program verifier for functional correctness. In International
     conference on logic for programming artificial intelligence and reasoning, pages 348–370. Springer,
     2010.

[28] K. R. M. Leino and P. Rümmer. A polymorphic intermediate verification language: Design and logical
     encoding. In J. Esparza and R. Majumdar, editors, TACAS, pages 312–327, Berlin, Heidelberg, 2010.
     Springer Berlin Heidelberg.

                                                     15
[29] Y. Lin, S. Tang, B. Lyu, J. Wu, H. Lin, K. Yang, J. Li, M. Xia, D. Chen, S. Arora, et al. Goedel-prover:
     A frontier model for open-source automated theorem proving. arXiv preprint arXiv:2502.07640, 2025.

[30] A. Mohamed, T. Mascarenhas, H. Khan, H. Barbosa, A. Reynolds, Y. Qian, C. Tinelli, and C. Barrett.
     LEAN - SMT: An SMT tactic for discharging proof goals in lean. In R. Piskac and Z. Rakamarić, editors,
     Proceedings of the 37th International Conference on Computer Aided Verification (CAV ’25), volume
     15931 of Lecture Notes in Computer Science, pages 197–212. Springer, July 2025. Zagreb, Croatia.

[31] F. Montesi. Introduction to Choreographies. Cambridge University Press, 2023.

[32] L. d. Moura and S. Ullrich. The Lean 4 theorem prover and programming language. In International
     Conference on Automated Deduction, pages 625–635. Springer, 2021.

[33] T. Nipkow, J. C. Blanchette, M. Eberl, A. Gómez-Londoño, P. Lammich, C. Sternagel, S. Wimmer,
     and B. Zhan, editors. Functional Data Structures and Algorithms: A Proof Assistant Approach. ACM
     Books, 2025.

[34] T. Nipkow, M. Wenzel, and L. C. Paulson. Isabelle/HOL: A proof assistant for higher-order logic.
     Springer, 2002.

[35] P. O’Hearn. Separation logic. Commun. ACM, 62(2):86–95, Jan. 2019.

[36] N. Perry, M. Srivastava, D. Kumar, and D. Boneh. Do users write more insecure code with ai assistants?
     In Proceedings of the 2023 ACM SIGSAC conference on computer and communications security, pages
     2785–2799, 2023.

[37] Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao, L. Zhang, Z. Fu, Q. Zhu, D. Yang, et al.
     Deepseek-prover-v2: Advancing formal mathematical reasoning via reinforcement learning for sub-
     goal decomposition. arXiv preprint arXiv:2504.21801, 2025.

[38] T. Ringer. Proofs and conversations. Notices of the American Mathematical Society, 71(9):1179–1182,
     2024.

[39] M. Rosendahl. Automatic complexity analysis. In Proceedings of the fourth international conference
     on Functional programming languages and computer architecture, pages 144–156, 1989.

[40] R. Rubbens, P. van den Bos, and M. Huisman. Veymont: Choreography-based generation of correct
     concurrent programs with shared memory. In N. Kosmatov and L. Kovács, editors, Integrated For-
     mal Methods - 19th International Conference, IFM 2024, Manchester, UK, November 13-15, 2024,
     Proceedings, volume 15234 of Lecture Notes in Computer Science, pages 217–236. Springer, 2024.

[41] T. Tao. Machine assisted proof. Notices of the American Mathematical Society, to appear, 2024.

[42] S. Ullrich and L. de Moura. ‘do’unchained: embracing local imperativity in a purely functional lan-
     guage (functional pearl). Proceedings of the ACM on Programming Languages, 6(ICFP):512–539,
     2022.

[43] G. Winskel and M. Nielsen. Models for concurrency, volume 4, page 1–148. Oxford University Press,
     Inc., USA, 1995.



                                                     16
[44] K. Yang, G. Poesia, J. He, W. Li, K. E. Lauter, S. Chaudhuri, and D. Song. Position: Formal mathemat-
     ical reasoning—a new frontier in ai. In Forty-second International Conference on Machine Learning
     Position Paper Track, 2025.

[45] A. Zhang, R. McAllister, R. Calandra, Y. Gal, and S. Levine. Learning invariant representations for
     reinforcement learning without reconstruction. ICLR, 2021.

[46] J. E. Zhong, K. Cheang, S. Qadeer, W. Grieskamp, S. Blackshear, J. Park, Y. Zohar, C. Barrett, and
     D. L. Dill. The move prover. In S. K. Lahiri and C. Wang, editors, Proceedings of the 32nd Inter-
     national Conference on Computer Aided Verification (CAV ’20), volume 12224 of Lecture Notes in
     Computer Science, pages 137–150. Springer International Publishing, July 2020.




                                                   17
