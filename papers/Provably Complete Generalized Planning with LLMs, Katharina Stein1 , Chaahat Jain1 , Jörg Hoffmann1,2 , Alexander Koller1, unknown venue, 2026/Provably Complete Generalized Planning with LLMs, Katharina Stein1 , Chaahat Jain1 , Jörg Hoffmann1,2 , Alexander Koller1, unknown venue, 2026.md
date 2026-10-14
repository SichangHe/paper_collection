                                                                    Provably Complete Generalized Planning with LLMs
                                                             Katharina Stein1 , Chaahat Jain1 , Jörg Hoffmann1,2 , Alexander Koller1
                                                                       1
                                                                       Saarland Informatics Campus, Saarland University, Saarbrücken, Germany
                                                                2
                                                                    German Research Center for Artificial Intelligence (DFKI), Saarbrücken, Germany
                                                                                     Correspondence: kstein@lst.uni-saarland.de




                                                                      Abstract
arXiv:2609.27105v1 [cs.AI] 22 Sep 2026




                                           Generalized planning aims to compute a plan that solves all
                                           instances of a planning domain. Recent work has used LLMs
                                           to automatically generate and debug such generalized plans
                                           in the form of Python programs and achieved perfect test data         Move from the shed to the gate. At each intermediate
                                           coverage for several domains. However, whether these gener-           location, pick-up all spanners. When reaching the gate,
                                           alized plans are actually complete, i.e. solve all instances of       tighten each loose nut using a different spanner.
                                           the domain, could only be determined by manual evaluation.
                                           Here, we present an approach for automatically generating
                                           generalized plans in Lean together with proofs of their com-       Figure 1: Illustration of an example planning task from the
                                           pleteness relative to a specification of the domain constraints    Spanner domain and a strategy for solving all Spanner tasks.
                                           provided as input. We introduce a semantic-preserving PDDL-
                                           to-Lean conversion, and use an LLM to generate both the
                                           generalized plan and the formal proof that it solves every in-
                                           stance satisfying the domain constraints. The correctness of       Language Models (LLMs) to generate, and debug, gener-
                                           the completeness proof is determined by Lean’s kernel. We          alized plans in the form of Python programs (Silver et al.
                                           evaluate our approach on 13 commonly used benchmark do-            2024; Stein et al. 2026), with Stein et al. (2026) achieving
                                           mains, using GPT-5.6-Sol as the LLM. For 12 of the domains         perfect (100%) coverage on the test datasets for 14 bench-
                                           we obtain generalized plans together with valid completeness       mark domains. Yet such empirical evidence is limited to a set
                                           proofs. This is a major advancement of the state of the art in     of example tasks (the test dataset). Do the generalized plans
                                           automatic generalized-plan completeness proofs.                    actually solve all tasks in the domains?
                                                                                                                 Stein et al. (2026) showed through a manual analysis that
                                                                                                              this is indeed the case (similar manual analyses were done
                                                                 Introduction                                 by Drexler, Seipp, and Geffner (2022) and Francès, Bonet,
                                         Generalized planning aims to compute a plan that solve not           and Geffner (2021)). But how to lead this kind of proof
                                         only a single planning task, but all tasks from a given PDDL         automatically? Given the PDDL description of a domain,
                                         domain. Such a strategy will typically contain loops and             as well as some specification of the set of domain instances
                                         conditionals to deal with different cases and sizes of tasks.        (tasks in the domain) that a generalized plan should solve,
                                         For example, in the Spanner domain from the IPC Learning             how to automatically obtain a generalized plan that provably
                                         track 2023 a man can walk between linked locations, pick             solves all these instances? We refer to this challenge as the
                                         up spanners and use a spanner to tighten a loose nut which           problem of computing complete generalized plans.
                                         makes the spanner unusable (Taitler et al. 2024). As per the            Earlier work on this challenge identified a restricted class
                                         IPC problem generator, the links between locations form a            of (so-called one-dimensional) planning problems where
                                         one-way path from the initial location (a shed) to the location      complete generalized plans can be found automatically us-
                                         of all loose nuts (a gate), and all usable spanners are located      ing logical reasoning techniques (Hu and Levesque 2010).
                                         between the shed and the gate. The goal is to tighten all loose      Another strand of work has addressed the complementary
                                         nuts. Figure 1 shows an example planning task and a strategy         challenge of, given a generalized plan, or as part of the
                                         that generalizes to all tasks of the domain.                         computation of the generalized plan, determining a set of
                                            A variety of approaches for formalizing and obtaining             instances which the plan is guaranteed to solve (e.g. Srivas-
                                         generalized plans have been proposed, including represent-           tava, Immerman, and Zilberstein 2011; Bonet et al. 2019).
                                         ing generalized plans as synthesized programs with loops             The key concept in the most recent work on this are so-called
                                         and conditionals (e.g. Srivastava, Immerman, and Zilberstein         sound abstractions, which underlie the generalized plan and
                                         2011; Jiménez, Segovia-Aguas, and Jonsson 2019) or general           guarantee faithfulness to a concrete set of instances. Recent
                                         policies (e.g. Bonet, Francès, and Geffner 2019; Bonet and           work has shown how to automatically prove such abstrac-
                                         Geffner 2018). Recently, there has been work on using Large          tions sound, and therewith solve the challenge of proving a
          1) Lean encoding                                       that the generalized plan GP is complete.1 Apart from the
         structure State where                                   PDDL itself, our approach requires as input only a specifi-
            statics : StaticState                                cation of the domain constraints, as well as a specification
            dynamic : DynamicState                               of state invariants. Everything else is completely automated,
                                                                 including the generation and debugging of GP as per Stein
         def ActionPre ... (s : State) : Prop :=                 et al. (2026), and the proof that GP is complete. Figure 2
            ...
                                                                 illustrates our approach.
          2) Generalized Plan                                       We empirically evaluate our approach on 13 commonly
                                                                 used benchmark domains (a subset of the domains addressed
        def solve(s : State)(g : Goal) :
            List PlanAction :=
                                                                 by Stein et al. (2026)). Using GPT-5.6-Sol as the LLM, for
                                                                 12 of these domains we obtain a generalized plan and a valid
          [Generalized Plan as Lean program]                     proof, showing automatically that the generalized plan is
                                                                 complete. This is a major advancement of the state of the art
          3) Completeness Proof                                  in automatic generalized-plan completeness proofs.
         theorem solveComplete
           (s : State)
           (g : Goal)
                                                                                          Background
           (hvalid : ValidInstance s g):                         PDDL planning. In our work we focus on planning do-
           ValidPlan (solve s g) s ∧                             mains and problems defined in the Planning Domain Defi-
           SatGoal (runPlan (solve s g) s) g := by               nition Language (PDDL) (McDermott 2000; Haslum et al.
                                                                 2019). In PDDL, a planning task is specified by domain D
           [Completeness Proof in Lean]
                                                                 and a problem instance I of the domain. A domain is a pair
          4) Kernel-check                                        D = ⟨PD , AD ⟩ where PD defines the set of predicates for
                                                                 describing states and AD defines the set of action schemas.
         #check (solveComplete :
          ∀ (s : State) (g : Goal),
                                                                 Each predicate P ∈ PD takes a finite number of arguments,
            ValidInstance s g →                                  i.e. has an arity of k ≥ 0. Each action schema A ∈ AD is
            ValidPlan (solve s g) s ∧                            a triplet ⟨Arg(A), Pre(A), Eff(A)⟩ where Arg(A) are the ar-
            SatisfiesGoal (runPlan (solve s g) s) g)             guments of the action, Pre(A) defines its preconditions and
                                                                 Eff(A) its effects.
Figure 2: Illustrations of the main steps of our approach           We focus on domains that can be expressed by a subset of
for obtaining generalized plans in Lean and proving their        PDDL that is restricted to conjunctive conditions with nega-
completeness.                                                    tion. Hence, all preconditions and effects are conjunctions of
                                                                 literals from P where all predicate arguments are also argu-
                                                                 ments of the action. We refer to the positive preconditions
                                                                 and effects as Pre+ and Eff+ , and to the negative precondi-
given generalized plan complete (Cui, Kuang, and Liu 2023).      tions and effects as Pre− and Eff− respectively. We require
The empirical success with this method is, however, limited      Eff+ (A) ∩ Eff− (A) = ∅.
to simple domains and/or instance sets, such as clearing a          A problem instance I is a triplet ⟨O, S0 , G⟩ where O
single block in Blocksworld, the IPC Gripper domain, and         is a finite set of objects, potentially with types, S0 defines
Logistics with a single vehicle.                                 the initial state and G the goal conditions. Both S0 and G
   In the present work, we leverage the power of LLMs to         are defined in terms of ground atoms, i.e. predicates of the
not only generate the generalized plans, but also the com-       domain where the arguments are replaced by objects o ∈ O,
pleteness proofs in a suitable formalization. Specifically, we   p(o1 , ..., ok ). The initial state forms a set of atoms and is
prove completeness of LLM-generated generalized plans us-        interpreted under the closed-world assumption, which means
ing Lean (de Moura et al. 2015), a functional programming        that all atoms that are not listed as part of the initial state are
language and theorem prover. We generate the generalized         false. The goal is a conjunction of literals, G = G+ ∪ G− ,
plans directly in Lean, and automatically prove their com-       that needs to be true at the end of the plan. A state s satisfies
pleteness relative to domain constraints formalizing the set     a goal G iff G+ ⊆ s ∧ G− ∩ s = ∅. We write s |= G if s
of instances.                                                    satisfies G.
                                                                    Figure 3a shows an excerpt from the PDDL Spanner do-
   We automatically generate Lean code from the PDDL en-         main (3a) and Figure 3b shows an example of a problem
forcing the domain semantics. Following Silver et al. (2024)     instance.
and Stein et al. (2026), we let the LLM generate the general-       An action a(o1 , ..., ok ) is an instance of an action schema
ized plan as a program that takes a problem instance as input    A grounded by objects from O. An action a is applicable
and outputs a complete plan. We then prompt the LLM to           in a state s iff all its preconditions are satisfied in s, i.e.
write a proof for the following theorem: Let GP be the gen-      Pre+ (a) ⊆ s ∧ Pre− (a) ∩ s = ∅. Applying an action a
erated generalized plan. If I is a problem instance satisfying
the domain constraints, then GP(I) returns a plan where 1)          1
                                                                      In our benchmarks, we only consider solvable problem in-
all actions are sequentially applicable and 2) the resulting     stances. If the domain constraints do not guarantee solvability, then
state satisfies the goal. A valid proof for this theorem shows   there exists no proof of the theorem.
    (:types                                                          problem generator associated with the domain. For example,
       location locatable - object                                   the problem generator for the Spanner domain generates only
       man nut spanner - locatable)                                  instances where all nuts are loose in the initial state and need
                                                                     to be tightened in the end. Such an implicit representation
    (:predicates                                                     does not permit to reason about whether a generalized plan is
       (at ?m - locatable ?l - location)                             complete w.r.t. a (possible infinite) set of problem instances.
       (carrying ?m - man ?s - spanner)                              In our work here, we specify the instance set in terms of
       (useable ?s - spanner)                                        instance-validity constraints C in Lean.
       (link ?l1 - location ?l2 - location)
                                                                     Generalized planning. Research on generalized planning
       (tightened ?n - nut)
                                                                     comprises a variety of different representations for general-
       (loose ?n - nut))
                                                                     ized plans and different approaches to obtain them. These
                                                                     include policies based on features and abstractions that are
    (:action walk
                                                                     hand-crafted (Bonet and Geffner 2018) or learned (Bonet,
       :parameters (?s - location ?e - location ?m - man)
                                                                     Francès, and Geffner 2019), policies for qualitative numeri-
        :precondition (and (at ?m ?s)
                                                                     cal problems (Srivastava et al. 2011), finite-state controllers
                             (link ?s ?e))
                                                                     that augment a policy with an internal memory (Bonet, Pala-
        :effect (and (not (at ?m ?s)) (at ?m ?e)))
                                                                     cios, and Geffner 2009) and directly synthesized programs
             (a) Excerpt from the domain definition.
                                                                     with control flow structures such as loops and conditionals
                                                                     (e.g. Jiménez, Segovia-Aguas, and Jonsson 2019; Srivastava,
    (:objects bob - man                                              Immerman, and Zilberstein 2011)
                spanner1 spanner2 - spanner                             More recently, approaches involving neural models have
                nut1 nut2 - nut
                                                                     been proposed, including learning general policies with
                location1 location2 shed gate - location)
    (:init
                                                                     graph neural networks (Ståhlberg, Bonet, and Geffner 2022,
       (at spanner1 location2) (useable spanner1)                    2025) and generating programmatic generalized plans using
       (at spanner2 location1) (useable spanner2)                    pretrained LLMs. Silver et al. (2024) and Stein et al. (2026)
       (loose nut1) (at nut1 gate)                                   use LLMs to come up with strategies for solving all plan-
       (loose nut2) (at nut2 gate)                                   ning tasks from a specific domain and to implement these
       (at bob shed) (link shed location1)                           strategies in the form of Python functions that take a Python
       (link location1 location2) (link location2 gate))             representation of a planning problem as input and return
    (:goal                                                           a sequence of actions. Their approaches include an auto-
       (and (tightened nut1) (tightened nut2)))                      mated debugging loop for the Python programs and Stein
                                                                     et al. (2026) also include an automated debugging step of the
                 (b) Example problem instance.                       strategies. Here, we consider generalized plans in the form
                                                                     of executable programs that take a problem instance as input
   Figure 3: PDDL examples from the Spanner domain.
                                                                     and return a plan.
                                                                     Completeness of generalized plans. Completeness guar-
in a state s yields a successor state s′ where s′ = (s \             antees for generalized plans have been approached in dif-
Eff− (a)) ∪ Eff+ (a). We define the successor state function         ferent ways. One line of work restricts the representation of
γ : S×A → S where S denotes the set of all states as follows:        generalized plans itself. For this restricted class of so-called
If an action a is applicable in a state s then γ(s, a) = s′ =        one-dimensional planning problems, complete generalized
                                                                     plans can be found automatically using logical reasoning con-
(s \ Eff− (a)) ∪ Eff+ (a). If a is not applicable then γ(s, a) is
                                                                     straints (Hu and Levesque 2010). A complementary line of
undefined. We extend γ to sequences of actions [a1 , ..., an ]
                                                                     work starts from a generalized plan and determines the char-
by iterated application: γ(s, []) = s and γ(s, [a1 , ..., an ]) =
                                                                     acterization of the set of instances that the generalized plan
γ(γ(s, a1 ), [a2 , ..., an ]), which is defined only if each ai is
                                                                     solves (Bonet et al. 2019), or computes the characterization
applicable in the state resulting from applying [a1 , ..., ai−1 ]
                                                                     of the set of covered instances jointly with the generalized
to s. We say a plan π is applicable from a state s if γ(s, π) is
                                                                     plan (Srivastava, Immerman, and Zilberstein 2011). The key
defined.
                                                                     concept underlying the most recent work in this direction is
   A plan π = [a1 , ..., an ] is a solution for a planning task      that of a sound abstraction: whenever the abstract generalized
⟨D, I⟩ with I = ⟨O, S0 , G⟩ if and only if γ(S0 , π) is defined      plan reaches the abstract goal, the resulting concrete plan is
and γ(S0 , π) satisfies G.                                           guaranteed to solve every concrete instance that is covered
   Domains can be typed, i.e. define a hierarchy of object           by the abstraction. Cui, Kuang, and Liu (2023) show how to
types. A typed domain can be converted into an equivalent            automatically prove the soundness of such abstractions, and
untyped domain by converting types into unary predicates.            hence automatically prove that the generalized plan is com-
   PDDL does not provide a specification language for the            plete. However, this has only been shown for very simple
set of problem instances considered. Instead, in most of the         domains (e.g. IPC Gripper) and restricted set-ups (Logistics
planning literature, this is encoded implicitly through a fixed      with one vehicle) so far. Another approach for establishing
set of instances considered, or as part of the program code of a     completeness is manual analysis, which can be applied to
a larger variety of domains but at the cost of manual work           We represent objects as natural numbers i ∈ N, i.e. our
by experts. Stein et al. (2026), Drexler, Seipp, and Geffner      conversion maps each PDDL object o ∈ O to a unique i ∈ N
(2022) and Francès, Bonet, and Geffner (2021) manually ver-       by enumeration, hence J·K is bijective on O. Each PDDL
ified that their generated or hand-crafted generalized plans      predicate P ∈ PD of arity k is represented as a boolean
solve all instances of a domain.                                  curried function PL : Nk → Bool that takes k objects as
                                                                  input and returns a truth value. Since the predicate functions
Lean. Lean (de Moura and Ullrich 2021) is a dependently           are total functions relative to the set of objects, this matches
typed functional programming language which enables the           the closed-world interpretation of PDDL states. All predicate
implementation of a generalized plan as an executable, type-      functions for which the truth assignments cannot be changed
checked function directly in Lean. Furthermore, Lean is also      by any action are part of the static state part together with the
an interactive theorem prover. So, it is used to write programs   set of objects. For example, the predicate (link ?l1 -
as well as to state and prove mathematical and program-           location ?l2 - location) becomes the function
correctness theorems about them. It is based on a dependent       link_p : N→ N→ Bool, and is part of the static state
type theory where types may depend on values. Lean is built       part because none of the action effects affect the connections
on the Curry-Howard correspondence, thus propositions are         between locations. All other predicate functions are part of
represented as types and a proof of a proposition is a term       the dynamic part. We compile away PDDL types by turning
of that type. Stating a theorem therefore amounts to writing      each type into a unary predicate.
down a type, while proving it amounts to constructing a term         Given the object mappings, a PDDL state s is converted
of that type. A Lean representation is thus a sequence of         into a Lean state sL by defining the truth assignments of the
definitions introducing functions and datatypes, statements       predicate functions such that the following state correspon-
expressing propositions and proofs constructing terms that        dence relation holds uniquely:
inhabit the types of their propositions. Type-checking is what
constitutes verification in Lean: if the term type-checks, the    Definition 1 (State Correspondence). Let s be a PDDL
statement counts as proven since a proof of a proposition is by   state, sL a Lean state. s and sL correspond to each other,
constructing a term of the corresponding type. Constructing       written s ∼ sL , if for every predicate P and tuple of
such terms explicitly is impractical, so Lean offers a tactic     objects (o1 , ..., ok ), p(o1 , ..., ok ) ∈ s iff Jp(o1 , ..., ok )K
mode to provide such proofs as a sequence of transformation       = PL (i1 , ..., ik ) returns true, where ij =Joj K.
steps, such as rewriting with an equation or performing in-       Instances. Encoding a PDDL goal condition follows a sim-
duction. Lean executes this sequence to construct the explicit    ilar principle, but differs in two key aspects. First, predicates
proof term. This term, along with definitions and previously      in the goal are defined as partial functions, as shown in List-
proven lemmas it depends on, is provided to Lean’s kernel,        ing 1, where Option Bool :none means that the atom is
a small trusted program that type-checks it.                      unconstrained, while some b requires the state to assign it
                                                                  the truth value b. Second, the goal is defined only in terms
     Lean Representations and Correctness                         of the predicate functions for which truth assignments can
Our objective is to obtain domain-specific generalized plans      change, i.e. the dynamic part of the state. We refer to the goal
for PDDL planning domains and prove their completeness            function for a predicate P ∈ PD as P GL .
in Lean. This requires a conversion from PDDL to Lean that           A PDDL goal is converted into a Lean goal analogously
faithfully preserves the semantics of the planning task. In       to a state: JGK is created such that for every predicate P
this section, we describe our Lean representation and the         of arity k and tuple of objects, P GL (i1 , ..., ik ) = true
conversion.                                                       iff p(o1 , ..., ok ) ∈ G+ and P GL (i1 , ..., ik ) = false iff
                                                                  p(o1 , ..., ok ) ∈ G− and is undefined otherwise. For example,
   We use the subscript “L” to indicate that a concept is rep-
                                                                  if the goal specifies that nut nut1 needs to be tightened but
resented in Lean and no subscript for PDDL, e.g. I refers
                                                                  does not specify the location of the man bob, and Jnut1K
to PDDL problem instance and IL to a Lean problem in-
                                                                  = 3 and JbobK= 4 then tightened_pG (3) returns true
stance. We write J·K for the conversion operator that maps
                                                                  and at_pG (4, o) returns none for any o ∈ O (see Figure
PDDL concepts to their Lean counterparts as defined in this
                                                                  5 in Appendix for a full example of a converted problem
section. JIK therefore refers to the specific problem instance
                                                                  instance).
obtained by applying the conversion to the PDDL instance
I. We use the inversion of the operator, i.e., J·K−1 , to refer      The goal satisfaction relation, |=L , is defined in Lean as a
to the conversion from Lean concepts back to their original       function SatisfiesGoal : State → Goal → Prop.
PDDL counterpart.                                                 SatisfiesGoal s g holds iff for every goal predicate
                                                                  and every argument, the corresponding predicate of the Lean
                                                                  state s agrees with the value that g requires wherever g
Representing States and Instances                                 requires one. We define the result as a Prop rather than
States. Our Lean representation of a PDDL state is split          a Bool because goal satisfaction appears in our complete-
into two parts: a static state and a dynamic state as shown       ness theorem (Theorem 2), and a theorem statement must
in Listing 1. The static and dynamic parts together comprise      be a proposition. Listing 2 shows an excerpt for the Spanner
everything that is required for capturing all parts of a PDDL     domain.
state: the set of objects, and a boolean-valued function for         A complete PDDL and Lean problem instance then corre-
every predicate of the domain.                                    spond to each other if the following holds:
structure State where                                              def SatisfiesGoal (s : State) (g : Goal) :
     statics : StaticState                                             Prop :=
     dynamic : DynamicState                                          (∀ var_m var_l,
                                                                       match g.dynamic.at_p var_m var_l with
structure StaticState where                                            | none => True
     objects : List N                                                  | some b => s.dynamic.at_p var_m var_l
     link_p : N → N → Bool                                                 = b) ∧
     location_t : N → Bool                                           (∀ var_n,
     locatable_t : N → Bool                                            match g.dynamic.tightened_p var_n with
     ...                                                               | none => True
                                                                       | some b => s.dynamic.tightened_p var_n
structure DynamicState where                                                = b) ∧
     at_p : N → N → Bool                                              ...
     carrying_p : N → N → Bool
     useable_p : N → Bool
     ...                                                           Listing 2: Example of the Lean function checking for goal
                                                                   satisfaction.
structure Goal where
  dynamic : GoalDynamic
                                                                   inductive PlanAction where
structure GoalDynamic where                                          | walk (var_s : N) (var_e : N) (var_m :
     at_p : N → N → Option Bool                                          N)
     carrying_p : N → N → Option Bool                                | pickup_spanner (var_l : N) (var_s : N)
     useable_p : N → Option Bool                                         (var_m : N)
     ...                                                             | tighten_nut (var_l : N) (var_s : N) (
                                                                         var_m : N) (var_n : N)
Listing 1: Excerpt of the Lean state and goal representations
of the PDDL Spanner domain (Figure 3a).                            Listing 3: Example of the action constructors for the action
                                                                   schemas from the Spanner domain.
Definition 2 (Instance correspondence). A PDDL instance
I = ⟨O, S0 , G⟩ and a Lean instance IL =JIK = ⟨JOK, JS0 K,         to return true for a positive literal, or false for a negative
JGK⟩ correspond to each other, written I ∼ IL , if S0 ∼ JS0 K      literal. Listing 4 shows an example for the preconditions of
and for any state s: s |= G iff JsK |=L JGK                        the “walk” action schema from the Spanner domain.
  By construction, our conversion ensures that for each               The effect function for an action schema A takes the same
PDDL instance I, I ∼JIK.                                           input as the precondition function and returns the updated
                                                                   state s′L , in which the predicate function of each add ef-
Representing Actions and Transitions                               fect in Eff(A) returns true at the affected arguments, each
Actions. Actions are encoded as an inductive type                  delete effect returns false, and all other truth assignments
PlanAction with one constructor per PDDL action                    are unchanged. Listing 4 shows this for the “walk” schema,
schema (Listing 3). We use an inductive type here rather           where only at_p is affected. The Lean syntax {s with
than a structure as we did for states, because a structure in      dynamic := ...} builds a copy of s in which only
Lean has a single constructor, whereas actions form a choice       the named field differs, and the nested s.dynamic with
among several schemas. Lean requires that any function over        ... analogously replaces only at_p; every other predicate
PlanAction, such as the transition function, handles every         function is carried over unchanged. The new at_p returns
constructor. Each constructor fixes the arity of its schema,       true for the man’s new location var_e, false for the
so that ill-formed ground actions are rejected by Lean’s type      previous location var_s, and the previous truth value for
checker. A Lean ground action is simply a constructor ap-          all other argument pairs.
plied to all its arguments, e.g. walk(1, 2, 3). Since all ground
actions thus share the type PlanAction, a Lean plan πL             Transitions. By construction, for any ground action a of
is of type List PlanAction.                                        an action schema A and any state s the following holds: the
   Preconditions and effects for each action schema are repre-     Lean precondition function returns true on JaK and JsK iff a
sented as a pair of Lean functions. Like SatisfiesGoal,            is applicable in s and if so, then the effect function applied to
the precondition function for an action schema A takes the         JaK and JsK returns a state s′L that corresponds to the PDDL
arguments of the encoded action and Lean state sL to return        successor state s′ = γ(s, a).
a proposition that the grounded action is applicable in sL .          The functions defined so far are specific to a single action
This function is defined as a conjunction where the conjuncts      schema, whereas the transitions of a planning task are de-
correspond to the Lean conversions of the literals in Pre(A).      fined for arbitrary ground actions. We therefore combine
Since state predicates are Boolean-valued, each conjunct is        them into actionPre and actionApply (Listing 5),
an equation requiring the corresponding predicate function         which take an arbitrary PlanAction and a state as in-
def walkPre (var_s : N) (var_e : N) (var_m                         def actionPre : PlanAction → State → Prop
    : N) (s : State) : Prop :=                                       | .walk var_s var_e var_m, s => walkPre
  s.dynamic.at_p var_m var_s = true ∧                                    var_s var_e var_m s
  s.statics.link_p var_s var_e = true ∧                              | .pickup_spanner var_l var_s var_m
  s.statics.location_t var_s = true ∧                                    , s => pickup_spannerPre var_l var_s
  s.statics.location_t var_e = true ∧                                    var_m s
  s.statics.man_t var_m = true                                       | .tighten_nut var_l var_s var_m var_n, s
                                                                          => tighten_nutPre var_l var_s var_m
def walkEff (var_s : N) (var_e : N) (var_m                               var_n s
    : N) (s : State) : State :=
 {s with dynamic := {                                              def actionApply : PlanAction → State →
  s.dynamic with                                                       State
  at_p :=                                                            | .walk var_s var_e var_m, s => walk
    fun var_m’ var_e’ =>                                                 var_s var_e var_m s
      if var_m’ = var_m ∧ var_e’ = var_e                             | .pickup_spanner var_l var_s var_m
          then                                                           , s => pickup_spanner var_l var_s
        true                                                             var_m s
      else if var_m’ = var_m ∧ var_e’ =                              | .tighten_nut var_l var_s var_m var_n, s
          var_s then                                                      => tighten_nut var_l var_s var_m
        false                                                            var_n s
      else
        s.dynamic.at_p var_m’ var_e’}}
                                                                   Listing 5: Example of the Lean applicability and state update
                                                                   functions for the Spanner domain.
Listing 4: Example of the Lean representation of the precon-
ditions and effects of the action schema ‘walk’.                             J·K                              J·K
                                                                     s              JsK              S0               JS0 K

                                                                         γ(s,a)       γL (JsK,JaK)                       γL (JS0 K,JπK)
put. Lean accepts these definitions only if they match ex-                                             γ(S0 ,π)
haustively over every constructor of PlanAction, so all
                                                                     s′            Js′ K
                                                                             J·K                              J·K
action schemas of the domain are covered, each branch call-                                          sn               Jsn K
ing the precondition or effect function of its correspond-
ing schema. Together, actionPre and actionApply                      (a) Single-action transition.        (b) Full-plan transition.
form the Lean counterpart γL to the PDDL successor state
function γ, with γL (sL , aL ) := actionApply(aL , sL ) if         Figure 4: Conversion J·K commutes with each applicable
actionPre(aL , sL ) is true and undefined otherwise. Un-           ground action when applying this single action (left). Iterat-
like γ, actionApply is a total function by itself, and             ing the square over a full plan shows that J·K also commutes
reproduces the partial definition of γ in combination with         with applying a sequence of actions (right).
actionPre. Figure 4 (left) illustrates the following lemma:
Lemma 1 (Action Transitions Commute). For any state s              ValidPlan(πL , S0L ) is true and runPlan(πL , S0L ) sat-
and ground action a, γ(s, a) is defined iff γL (JsK, JaK) is de-   isfies GL (see correctSolution, Listing 6).
fined. If γ(s, a) = s′ and γL (JsK, JaK) = s′L then s′L =Js′ K.       Since initial states are states and since a single action
                                                                   corresponds to a plan of length 1, Lemma 1 applies to the
                                                                   initial state of a problem instance and extends to plans by
From Single Steps to Plan Correctness                              induction over plan length, as illustrated in Figure 4 (right).
We lift applicability and state updates from single actions to        By construction, our PDDL to Lean conversion ensures
sequences by defining two recursive functions, ValidPlan           that a PDDL problem instance I and its converted Lean
and runPlan (Listing 6), the former stating the proposition        counterpart JIK correspond. Therefore, a PDDL plan and its
under which a plan is applicable and the second comput-            Lean counterpart agree on applicability and goal satisfaction:
ing the state it produces. The empty plan is always appli-         Lemma 2 (Plan Correctness Transfers to Conversion). Let
cable and leaves the state unchanged. For a non-empty list,        I = ⟨O, S0 , G⟩ be an instance of D, and let π = [a1 , ..., an ]
ValidPlan requires the first action to be applicable in the        be a sequence of actions. Then π is a correct plan solving
current state and the remaining actions to form a valid plan       I iff JπK is a correct plan solving the corresponding Lean
from the state that results from applying it, while runPlan        planning problem JIK.
applies the first action and continues on the remaining list.
Notice that runPlan applies an action regardless of whether           Since J·K is bijective on objects and each PDDL action
its preconditions hold and applicability is captured sepa-         schema corresponds to exactly one PlanAction construc-
rately by ValidPlan. Checking for the correctness of a             tor, J·K is bijective on ground action sequences and hence
plan hence requires both: a plan πL is a solution for a prob-      every Lean plan πL has a unique PDDL counterpart JπL K−1 .
lem instance with the initial state S0L and the goal GL iff        Theorem 1 (Soundness of Lean Plan Verification). Let
def ValidPlan : List PlanAction → State →                       solveComplete : ∀ (s : State) (g : Goal),
    Prop                                                          ValidInit s → ValidGoal s g →
  | [], _ => True                                                 ValidPlan (solve s g) s ∧
  | a :: as, s => actionPre a s ∧ ValidPlan                       SatisfiesGoal (runPlan (solve s g) s) g
       as (actionApply a s)

def runPlan : List PlanAction → State →                         Listing 8: Type of the completeness theorem statement for
    State                                                       the generalized plan solve: for any valid initial state and
  | [], s => s                                                  goal, solve returns an applicable plan that reaches the goal.
  | a :: as, s => runPlan as (actionApply a
       s)
                                                                theorem solveComplete
def correctSolution (s : State) (g : Goal)                         (s : State)
    (plan : List PlanAction) : Prop                                (g : Goal)
  ValidPlan plan s ∧                                               (hinit : ValidInit s)
  SatisfiesGoal (runPlan plan s) g                                 (hgoal : ValidGoal s g) :
                                                                   ValidPlan (solve s g) s ∧
                                                                   SatisfiesGoal (runPlan (solve s g) s) g
Listing 6: Lean functions for checking plan applicability and          := by
correctnes and for executing a plan.                              -- Proof term of the theorem


def solve (s : State) (g : Goal) : List                         Listing 9: Lean declaration of the completeness theorem
    PlanAction :=                                               statement in Listing 8.
  -- Implementation of the generalized plan
       GP
                                                                Definition 3 (Generalized Plan Completeness). Let D be a
                                                                domain. A Lean function solve with the signature of List-
Listing 7: Signature of the generalized plan solve, which       ing 7 is a complete generalized plan for D if, for every initial
takes a state and a goal and returns a plan.                    state sL and every goal GL that satisfy ValidInit(sL ) and
                                                                ValidGoal(sL , GL ), the plan returned by solve sL gL is
                                                                applicable from sL and the resulting state satisfies GL .
I = ⟨O, S0 , G⟩ be an instance of D. If we obtain a se-
quence of actions, πL : List PlanAction, and applying              Definition 3 guarantees the correctness of the generated
correctSolution to JS0 K, JGK and πL returns true then          plans for an infinite number of problem instances because
converting πL from Lean to PDDL gives a plan π = JπL K−1        there are infinitely many pairs of valid initial states and
such that π is guaranteed to be a solution of the original      goals. It is expressed as a Lean theorem of the type shown
PDDL problem instance I.                                        in Listing 8 which expresses exactly the universal implica-
                                                                tion statement. Listing 9 shows the actual Lean declaration
   Theorem 1 follows directly from Lemma 2:                     of the theorem which can be completed by a proof candidate
correctSolution(JS0 K, JGK, πL ) is by defini-                  that can then be checked by Lean’s kernel. A Lean proof
tion the Lean statement that πL is a correct plan solving JIK   of solveComplete (Listing 9) for a specific candidate
and the bidirectionality of Lemma 2 gives that JπL K−1 is a     solve function establishes exactly the completeness defini-
correct plan solving I.                                         tion (Def. 3) for that candidate if accepted by Lean’s kernel:
Completeness of Generalized Plans
                                                                Theorem 2 (Completeness GP Lean). Let D be a domain
We now lift the correctness from individual plans to the        and let GPL be a candidate generalized plan for D, i.e.
completeness of generalized plans. We define a generalized      a Lean function with the signature shown in Listing 7. If
plan as a (domain-specific) Lean function solve that takes      there exists a proof for solveComplete (Def. 3) with
a Lean problem instance, separated into the initial state and   solve:= GPL , that is accepted by Lean’s kernel, then GPL
the goal, as input and returns a plan in the form of a list     is a complete generalized plan for D: for every problem
of PlanAction for the input problem instance. Listing 7         instance IL satisfying the domain constraints, applying GPL
shows the signature of a generalized plan.                      to IL returns a plan that is applicable from the initial state
   Not every problem instance expressible in Lean needs to      and reaches the goal.
be handled by the solve function. As described in the Back-        Theorem 2 itself requires no separate proof beyond Lean’s
ground, we define the set of problem instances by validity      own soundness guarantee that whenever the kernel accepts
constraints C on valid initial states and goals. We represent   a proof term of a proposition then the proposition holds.
these constraints in Lean as two predicates ValidInit           Theorem 2 is, however, about the correctness of a generalized
: State → P rop and ValidGoal : State → Goal →                  plan GPL with respect to Lean problem instances and not the
P rop. Completeness of a generalized plan solve is then         original PDDL. We extend the correctness theorem in order
defined as follows:                                             to carry over to PDDL based on Lemma 2 and Theorem
1. From Lemma 2 and Theorem 1 we get that, given our                 def AtLeastAsManySpannersAsNuts (s :
conversion J·K, every PDDL instance I of a domain has a                  StaticState) : Prop :=
corresponding Lean instance, and every Lean plan that solves           (s.objects.filter (fun x => s.nut_t x)).
the converted problem instance has a PDDL counterpart that                 length ≤ (s.objects.filter (fun x =>
solves the original PDDL instance. Therefore, correctness of               s.spanner_t x)).length
solve in Lean transfers to a correctness guarantee for the
original PDDL.                                                       def ValidLinkParam (s : StaticState) : Prop
                                                                          :=
Corollary 1 (Completeness of GP for PDDL Domain). Let                  ∀ var_l1 var_l2, s.link_p var_l1 var_l2 =
GPL be a complete generalized plan in Lean for a domain                     true → s.location_t var_l1 = true ∧
D (Theorem 2), and let J·K be our PDDL to Lean conversion.                 s.location_t var_l2 = true
Then for every I = ⟨O, S0 , G⟩ ∈ ID , GPL (JIK) returns a
plan πL such that πL = JπK for some plan π that solves I.            def LinkAcyclic (s : StaticState) : Prop :=
                                                                       ∀ l, ¬ Relation.TransGen (fun a b => s.
Validity Constraints                                                       link_p a b = true) l l
The completeness theorem in Listing 9 is proven relative to          def InitNutsLoose (s : State) : Prop :=
ValidInit and ValidGoal: these two Lean predicates                     ∀ n, s.statics.nut_t n = true → s.dynamic
specify which problem instances a generalized plan is re-                  .loose_p n = true
quired to solve by defining the constraints on valid problem
instances, which we call validity constraints. Our assump-           def GoalAllNutsTightened (initial : State)
tion here is that the user provides this specification along             (g : Goal) : Prop :=
with the PDDL. This makes sense as the user wants a gener-             ∀ n, initial.statics.nut_t n = true → g.
alized plan, and the set of instances which that plan should               dynamic.tightened_p n = some true
solve is naturally part of the problem specification. In other
words, we view generalized planning as the problem of plan          Listing 10: Examples of constraints on valid instances of the
generation replacing a single PDDL problem instance with            Spanner domain.
a set of PDDL problem instances as captured by the validity
constraints. (A trivial specification would admit all initial
states and goals, but this rarely makes sense; consider e.g.        representation, 2) lets an LLM generate a candidate gener-
Blocksworld initial states with cyclic towers.)                     alized plan solve, and 3) uses again an LLM to generate
   Listing 10 shows examples of validity constraints for the        the proof that solve satisfies the correctness theorem from
Spanner domain. The goal constraints take the goal and the          Listing 9. All these steps, including potential debugging of
initial state as parameters, hence allowing dependencies be-        the LLM-generated Lean code, are fully automated.
tween initial state and goal.
   Lean’s logic is the calculus of inductive construc-              Generating the Lean domain representation. In order to
tions (Pfenning and Paulin-Mohring 1990), used for defining         obtain the Lean formalizations, we implemented a domain-
relations by induction and quantifying over predicates. This        independent Python converter that takes as input the PDDL
allows directly expressing properties such as reachability and      domain, and optionally a PDDL problem, and outputs the
hence the absence of cycles of any length. Thus constraints         converted Lean representation, i.e. the state, action and in-
such as the location graph in Spanner forming a linear se-          stance representations described above (see Listings 1, 3-5).
quence are straightforward as we can define the transitive          Our implementation for processing the PDDL covers a sub-
closure of link_p and state that no location is reachable           set of PDDL that is restricted to conjunctive conditions with
from itself (LinkAcyclic).                                          negation, no action costs, and can be applied to typed and
   The validity of an initial state (ValidInit) is then de-         untyped domains2 . The converter is purely symbolic and
fined as a conjunction of the initial state constraints and         deterministic3 , and applies the conversion described in the
validity of a state in general, which itself is again a con-        previous section in the same structured way to any domain
junction of the constraints on the dynamic state part and the       of the covered PDDL fragment. Therefore, all claims and
constraints on the static state part. Similarly, goal validity of   guarantees that depend on the specific conversion mecha-
a state (ValidGoal) is defined as a conjunction of the goal         nism described before hold for the Lean representation of
constraints.                                                        any domain obtained from our converter.
                                                                    Generating the generalized plan in Lean To generate
   Generalized Planning in Lean with LLMs                           generalized plans with LLMs, we follow the process intro-
The previous section described the theoretical foundation of        duced by Stein et al. (2026), which consists of two main steps:
our approach and the prerequisites for representing gener-             2
                                                                          In order to extend the approach to a larger PDDL fragment only
alized plans for PDDL planning tasks in Lean and proving            the PDDL processing part needs to be adapted.
their completeness. In this section, we now describe how                3
                                                                          The only exception with respect to the determinism concerns
we obtain the generalized plans and completeness proofs.            the order of iterations, e.g. in which the actions are converted and
Given a PDDL domain and the specifications of the validity          objects are enumerated. None of the iteration orderings, however,
constraints, our pipeline 1) automatically generates its Lean       has any effect on the validity of our results.
1) deriving the pseudocode strategy for solving a planning           ration is rejected, the LLM revises the declaration based on
domain, and 2) implementing that strategy in a programming           the code accepted so far and the error message. Thus, errors
language. As our focus here is on completeness proofs rather         are repaired locally without discarding the parts Lean has
than on finding strategies, we start from the pseudocode             already accepted in contrast to the basic approach where the
strategies of Stein et al. (2026), check them and revise them        complete proof needs to be regenerated. The process ends
if necessary. We provide an LLM with the revised strategies          when all declarations are accepted or the maximum number
as well as the complete Lean representation of the target do-        of iterations is reached. During the debugging, to account for
main and have it implement the solve function (Listing 7)            declarations missing in the initial sketch, the LLM is explic-
such that correctSolution (Listing 6) holds. This code               itly allowed to generate more declarations than the one that
is debugged in two steps. Statically, Lean’s kernel must ac-         failed. They are then inserted into the proof sketch at the same
cept the code. Dynamically, the candidate generalized plan           place as the declaration that is currently being debugged.
is run on a set of debugging tasks and the plans it returns
are converted to PDDL and validated with VAL (Howey,                 Preventing LLM cheating. LLMs generating Lean code
Long, and Fox 2004). If either step fails, the LLM receives          are known to find workarounds that make the code compile
feedback about the specific error and is prompted to revise          without establishing the intended result (Wang et al. 2026;
its generated code. If the generated candidate generalized           Paglieri et al. 2026), and recent work analyzing Lean bench-
plan returns correct solutions for all debugging tasks within        marks has found related evaluation-time loopholes that can
a defined number of iterations, the process moves on to the          affect the reliability of evaluation results (Ammanamanchi,
proof step. An example of a generalized plan generated for           Bhat, and Biderman 2026). There are three ways in which
the Spanner domain can be found in Listing 14.                       this can happen in our setting. First, the LLM may change
                                                                     correctSolution either by directly editing the state-
Generating the completeness proof. Once a generalized                ment itself, e.g. adding hypotheses that make the statement
plan has been generated, we ask the LLM to prove that it is          easier to prove, or by altering the semantics, e.g. by redefin-
correct, i.e., to state and prove the correctness theorem shown      ing notation or introducing new definitions (Paglieri et al.
in Listing 9. As input, the LLM receives (i) the complete Lean       2026). Second, the proof may silently rely on unjustified ax-
code from the previous step, consisting of the Lean represen-        ioms which do not appear in the theorem’s type. Third, a
tation and the LLM-generated generalized plan, (ii) lemmas           proof may be accepted while bypassing Lean’s kernel checks
stating that actions preserve state validity, described in the       due to metaprogramming or bugs in incremental compilation
next section, and (iii) helper lemmas describing which parts         within Lean.
of a state an action changes and which it leaves unchanged.             We address these with four checks. We reject code that
These helper lemmas are generated automatically from the             alters how subsequent code is parsed or elaborated, such as
PDDL by a symbolic, domain-independent generator (see                custom notation or macros. We further verify that the final
Listing 12 and 13 in Appendix).                                      code contains a theorem exactly as written in Listing 8. To-
   We again use an automatic debugging procedure to let the          gether, these rule out the first form of cheating. For the second
LLM revise its generated proof in case the generated proof is        form of cheating, we check that the proof does not depend
rejected. If Lean reports any error, or the proof fails one of the   on axioms beyond the standard ones.4 Finally, for efficiency,
checks against cheating described below, the error message           our iterative debugging loop is performed incrementally in
is passed back to the LLM, together with a prompt asking it          REPL.5 As a sanity check, the complete code is rebuilt from
to regenerate the complete proof.                                    scratch as a self-contained module and rechecked by Lean’s
   Depending on the specific planning domain and the con-            standalone checker, thus ruling out the third form of cheating
crete implementation of the generalized plan, completeness           as well.
can be hard to prove and the simple, basic approach described        Invariants. In addition to the types of constraints described
may not work. In particular, we observe that in these cases          above, we specify a set of state invariants: properties that hold
the LLM explicitly replies that proving completeness is too          in the initial state and remain true in any state reachable from
complex. To address this we propose a second, iterative ap-          it, such as NutTightenedLooseExhaustive shown in
proach inspired by Ospanov, Farnia, and Yousefzadeh (2025),          Listing 11 which specifies that each nut is always either tight-
which, as our experiments show, works better for those com-          ened or loose. Every invariant of this kind is a consequence of
plex cases. The LLM is given the same information as in the          the initial state constraints together with the action schemas.
basic approach but is instructed to provide a proof sketch that      In practice, however, we provide these invariants explicitly as
states all lemmas it requires. Notably, this approach allows         part of the valid state specification because doing so removes
the LLM to decide which lemmas it proves immediately in its          the burden of re-deriving them from scratch from the LLM.
first response and which are marked unproven for now. The            At the same time, adding them to the constraints does not
remaining lemmas are then proven in subsequent iterations.           add a substantial additional amount of work. For example,
The completeness proof is only accepted once it depends on           without invariants, the initial state constraints need to include
no unproven lemmas.                                                  both a constraint that all nuts are loose (InitNutsLoose)
   To debug the proof sketch, we split it into its individual
declarations, i.e. definitions, lemmas and theorems. These              4
                                                                          https://lean-lang.org/doc/reference/latest/Axioms/#standard-
declarations are added to the Lean representation one at a           axioms
                                                                        5
time, checking the code after each addition. When a decla-                https://github.com/leanprover-community/repl
 def NutTightenedLooseExhaustive (s : State)
                                                                           as the debugging iterations. For 10 of the domains, the first
      : Prop :=                                                            generated version of the generalized plan already solved the
   ∀ n, s.statics.nut_t n = true                                           debugging tasks, and for the other three domains a single
     → s.dynamic.tightened_p n = true ∨                                    debugging iteration was enough. Given that we made sure to
        s.dynamic.loose_p n = true                                         already provide the LLM a correct strategy for solving the
                                                                           domain, a low number of debugging iterations is expected
                                                                           here.
Listing 11: Examples of a state invariant constraint of the
Spanner domain.                                                            Results proofs. As described above, we consider two dif-
                                                                           ferent approaches for generating the completeness proofs: a
                                                                           basic approach where the complete proof is generated and
and one specifying that no nut is tightened. When adding                   debugged as a whole and an iterative approach where the
NutTightenedLooseExhaustive as an invariant con-                           LLM first generates a sketch of the proof and then debugs
straint, the constraint about all nuts being not tightened be-             the individual declarations (e.g., lemmas, definitions, theo-
comes redundant.                                                           rems, etc.).
   We define a ValidState as a conjunction over all con-                      We first tested the basic approach for all domains with the
straints that apply to arbitrary states (i.e. not only initial             maximum iterations for debugging set to six. For 7 of the 13
states). We then automatically generate one lemma per ac-                  domains, the LLM successfully completed the completeness
tion schema for proving that applying the specific action in               statement from Listing 9 with a proof that was accepted
a valid state yields again a valid state. Then, an LLM is                  by Lean’s kernel. The number of generated proof versions
prompted to generate the proof. We include an automatic                    (i.e. initial + debugging iterations) and the time required
debugging loop where the LLM has up to five tries for gen-                 for obtaining the generalized plans and proofs for these 7
erating these proofs. Here, the LLM is prompted to generate,               domains are shown in the upper part of Table 1.
and debug, the proofs for all actions together instead of for                 For the other six domains, the LLM was not able to gener-
each action individually.                                                  ate the completeness proof using the basic set-up. In partic-
                                                                           ular, for all of these domains the LLM explicitly stated in the
                          Experiments                                      first response that providing a complete proof at once is not
                                                                           possible due to its complexity and the number of required
Pipeline and Set-up                                                        additional lemmas. We therefore ran the iterative approach
We test our approach using GPT-5.6-Sol with temperature set                for those six domains. As the debugging is applied at the level
to 1 and reasoning set to high. We select 13 of the 17 domains             of individual declarations here, we set the debugging limit
on which also Stein et al. (2026) ran their experiments. We                such that the debugging terminates if the same declaration
exclude Gripper because of its similarity to Grippers, Beluga              (as identified by the name of e.g. the lemma) is debugged
because LLMs struggle to find generalized plans there (Stein               six times in a row without success. Using the iterative ap-
et al. 2026) and Minigrid and Visitall as the specification of             proach, we successfully obtain proofs accepted by Lean’s
solvability is not straightforward6 . For all the domains that             kernel for all domains except Transport. The lower part of
we test our approach on except Rovers, Stein et al. (2026)                 Table 1 shows the maximum number of iterations required
manually proved that their generalized plans were complete.                for the same declaration (Decl.) as well as the total number of
We define the domain constraints on valid instances based                  interactions (Prf.) for obtaining the complete correct proof.
on the problem generators, example problems from datasets,                    Note, however, that the lack of a proof for Transport does
potential domain descriptions, and the PDDL domain defini-                 not mean that the generalized plan does not solve all in-
tion. For each domain, we select six small problem instances               stances of the domain, but that the LLM was not capable
from existing datasets as debugging tasks (see Table 3 in                  of generating one. In order to still get an idea of how well
Appendix for sources of datasets).                                         the generalized plan performs, we tested it on the easy and
                                                                           medium test splits of the IPC Learning track 2023 (Taitler
Generalized Plans and Proofs                                               et al. 2024) on which it achieved perfect coverage.
Results generalized plans. The approach for generating
the generalized plan (GP) described above is applied for ob-               Generation times. Table 1 also shows how long it takes
taining the GPs for all 13 domains. We set the maximum                     to obtain the generalized plans and the completeness proofs.
number of debugging iterations to four. Table 1 presents the               The required time varies a lot between the different domains,
results. For all 13 domains, the LLM successfully generated                ranging from 9 minutes for Heavy to almost one hour (54
generalized plans that were accepted by Lean and returned                  minutes) for Rovers. Generating the generalized plans takes
plans that were accepted by VAL for all six debugging tasks.               significantly less time even if the number of iterations is only
The number of interactions (N interactions) refers to the                  slightly higher. As shown in Table 2, the Lean code for the
number of input-output pairs of the LLM generation process                 proofs consists also of significantly more individual decla-
for the generalized plan (GP) and the proof (Prf.), and in-                rations, both with respect to the number of declarations the
cludes both the initial versions generated by the LLM as well              LLM generates and the number of declarations already pro-
                                                                           vided to the LLM in the prompt. The number of declarations
    6                                                                      provided to the LLM is necessarily larger for the proof gener-
      Stein et al. (2026) used a version of Visitall that allows missing
cells in the grid                                                          ation because it includes the complete Lean code (provided
                   N interactions               Time                                       N decl. GP       N decl. Prf.
  Domain                                                                   Domain
                 GP Prf. Decl.           GP      Prf.    total                            given LLM        given LLM
  Basic proof generation                                                   Basic proof generation
  Delivery         1      3       –     121      671      792              Delivery          56       3      92       15
  Ferry            2      3       –     104      586      690              Ferry             45       7      83        7
  Grippers         2      3       –     119      661      780              Grippers          51       9     102       23
  Heavy            1      3       –      36      495      531              Heavy             47       5      76        9
  Hiking           1      2       –     113      582      694              Hiking            45       5      65       16
  Logistics        1      3       –     157     1025     1182              Logistics         61      16     133       46
  Satellite        1      4       –     224     1383     1607              Satellite         56      10     116       17
  Iterative proof generation                                               Iterative proof generation
  Blocks.          2    24        3     315     1505     1819              Blocks.           52      10     122       42
  Goldminer        1    36        2     290     2524     2814              Goldminer         78      16     194       71
  Miconic          1    11        2     204     1302     1506              Miconic           55       7     103       27
  Rovers           1    45        3     307     2914     3221              Rovers           120      17     293       66
  Spanner          1    36        4     214     2735     2950              Spanner           60       9     104       46
  Transport        1      –       –     239        –        –
                                                                    Table 2: Number of Lean code declarations (i.e., lemmas,
Table 1: Number of LLM interactions and run time of the             theorems, and definitions) involved in generating the gener-
pipeline (in seconds) for generating the generalized plan (GP)      alized plan (GP) and its completeness proof (Prf.). “Given”
and its completeness proof (Prf.). “N interactions” counts the      reports the number of declarations provided to the LLM as
number of interactions, i.e. input-output pairs, with the LLM,      part of the prompt (e.g., the domain formalization and, for
including the initial generation and all debugging iterations.      proof generation, the complete GP code); “LLM” reports the
The upper part shows the domains for which the basic ap-            number of individual declarations generated by the LLM it-
proach succeeded, the lower part shows the results using the        self.
iterative approach on the other domains. For the iterative ap-
proach, “Decl.” reports the maximum number of debugging
iterations required for a single declaration.                       here, but for programs that must remain correct across every
                                                                    valid instance of a planning domain, not a single specific
                                                                    input-output specification.
and LLM-generated) for the generalized plan.
                                                                    LLMs for theorem proving. First et al. (2023) introduce
                      Related Work                                  an approach to automatically generate and repair complete
                                                                    proofs using LLMs based on feedback from the Isabelle proof
Software verification. Verifying the correctness of syn-            assistant to iteratively debug incorrect generated proofs.
thesized programs has long been studied in software veri-           They fine-tune models and evaluate them on a benchmark
fication and program synthesis. Classical work established          of general mathematical theorems rather than software or
that a verifier can be used not only to check a synthesized         planning related theorems. Song, Yang, and Anandkumar
program in the end, but to guide synthesis itself, iteratively      (2024) integrate LLM-based tactic suggestions, proof search
refining candidate programs against counterexamples until a         and premise selection directly into the Lean workflow, fo-
verified implementation is found (Solar-Lezama et al. 2006).        cusing on interactively developing proofs for math. Most
More recently, this combination of synthesis and verification       closely related to our proof-debugging approach is the work
has been extended to use LLMs as the source of the candi-           by Ospanov, Farnia, and Yousefzadeh (2025): they isolate
date programs. Bhatia et al. (2024) use an LLM to jointly           failing sub-lemmas in an LLM-generated proof sketch and
generate a program and a proof of its functional equiva-            repair them individually, using a hybrid approach that com-
lence to a source program, translating both into an auto-           bines automated solvers and LLM calls, instead of debugging
mated theorem prover to verify correctness for all program          the whole proof at once. Their focus is on competition-style
states rather than testing on a finite test set. Aggarwal, Parno,   mathematical benchmarks.
and Welleck (2025) similarly address formally verified code
generation by iteratively translating and refining candidate        Formally verified planning components. In ensuring the
programs against feedback from a formal verifier, and Chen          correct PDDL semantics in Lean, our work loosely relates
et al. (2025) fine-tune models on synthesized proof data for        to works on formal verification of components or aspects of
proof generation and debugging in Rust.                             planning. Previous work has worked on formalizing classical
   In all these approaches, an external, trusted verifier pro-      planning domains for the purpose of verification. One line of
vides the correctness guarantee for an LLM-generated pro-           work formalizes the semantics of a PDDL fragment directly
gram, e.g. a transpiled function (Bhatia et al. 2024) or            inside an interactive theorem prover: Abdulaziz and Lam-
a Verus-annotated Rust function (Aggarwal, Parno, and               mich (2018) formalize STRIPS-like PDDL in Isabelle/HOL
Welleck 2025), but the guarantees are only checked once             and derive a formally verified plan validator, and follow-up
against one specification. We adopt the same overall pattern        work extends this to a verified compositional planning algo-
rithm (Abdulaziz, Gretton, and Norrish 2019) and a formally        Ammanamanchi, P. S.; Bhat, S.; and Biderman, S.
verified SAT-based planner (Abdulaziz and Kurz 2023). An-          2026. Faults in Our Formal Benchmarking: Dataset De-
other line of work lets planners emit independently checkable      fects and Evaluation Failures in Lean Theorem Proving.
certificates alongside their output, without formalizing the       arXiv:2606.29493.
planner itself: Eriksson, Röger, and Helmert (2017) intro-         Bhatia, S.; Qiu, J.; Hasabnis, N.; Seshia, S.; and Cheung, A.
duce certificates of unsolvability that a planner-independent      2024. Verified Code Transpilation with LLMs. In Glober-
validator can verify, and Mugdan, Christen, and Eriksson           son, A.; Mackey, L.; Belgrave, D.; Fan, A.; Paquet, U.; Tom-
(2023) extend this approach of certifying algorithms to cer-       czak, J.; and Zhang, C., eds., Advances in Neural Information
tificates of plan optimality. Like our work, both lines of work    Processing Systems, volume 37, 41394–41424. Curran As-
target machine-checked guarantees in the context of classi-        sociates, Inc.
cal planning but verify a fixed planning algorithm’s output,       Bonet, B.; Francès, G.; and Geffner, H. 2019. Learning
e.g. single plans, (un)solvability claims, rather than verifying   Features and Abstract Actions for Computing Generalized
correctness across the entire set of domain instances.             Plans. In Proceedings of the Thirty-Third AAAI Conference
                                                                   on Artificial Intelligence (AAAI 2019), 2703–2710. AAAI
                        Conclusion                                 Press.
We introduce an approach for automatically obtaining gen-          Bonet, B.; Fuentetaja, R.; E-Martín, Y.; and Borrajo, D. 2019.
eralized plans together with machine-checked completeness          Guarantees for Sound Abstractions for Generalized Planning.
proofs, using LLMs to generate both of them directly in Lean.      In Proceedings of the 28th International Joint Conference on
Out of 13 commonly used benchmark domains, our approach            Artificial Intelligence (IJCAI 2019), 1566–1573. IJCAI.
produced provably complete generalized plans in 12. To our
knowledge, this is the first time that generalized plans were      Bonet, B.; and Geffner, H. 2018. Features, Projections, and
automatically proved complete at such a scale, with prior          Representation Change for Generalized Planning. In Pro-
work limited to simple domains and/or instance sets. This          ceedings of the 27th International Joint Conference on Arti-
is a major advancement of the state of the art in automatic        ficial Intelligence (IJCAI 2018), 4667–4673. IJCAI.
generalized-plan completeness proofs.                              Bonet, B.; Palacios, H.; and Geffner, H. 2009. Automatic
                                                                   Derivation of Memoryless Policies and Finite-state Con-
                   Acknowledgments                                 trollers Using Classical Planners. In Proceedings of the
                                                                   Nineteenth International Conference on Automated Planning
The work was partially funded by the Deutsche Forschungs-
                                                                   and Scheduling (ICAPS 2009), 34–41.
gemeinschaft (DFG, German Research Foundation) under
the project number 232722074 – SFB 1102. It was also               Chen, T.; Lu, S.; Lu, S.; Gong, Y.; Yang, C.; Li, X.; Misu,
funded in part by the Deutsche Forschungsgemeinschaft –            M. R. H.; Yu, H.; Duan, N.; CHENG, P.; Yang, F.; Lahiri, S.;
GRK 2853/1 “Neuroexplicit Models of Language, Vision,              Xie, T.; and Zhou, L. 2025. Automated Proof Generation for
and Action” - project number 471607914. We thank Jan               Rust Code via Self-Evolution. In Yue, Y.; Garg, A.; Peng,
Reineke, Dan Fišer and Nicola Müller for insightful discus-        N.; Sha, F.; and Yu, R., eds., International Conference on
sions.                                                             Learning Representations, volume 2025, 71891–71918.
                                                                   Cui, Z.; Kuang, W.; and Liu, Y. 2023. Automatic Verification
                        References                                 for Soundness of Bounded QNP Abstractions for Generalized
Abdulaziz, M.; Gretton, C.; and Norrish, M. 2019. A Veri-          Planning. In Proceedings of the 32nd International Joint
fied Compositional Algorithm for AI Planning. In Harrison,         Conference on Artificial Intelligence (IJCAI 2023), 3149–
J.; O’Leary, J.; and Tolmach, A., eds., 10th International         3157. IJCAI.
Conference on Interactive Theorem Proving (ITP 2019), vol-         de Moura, L.; Kong, S.; Avigad, J.; van Doorn, F.; and von
ume 141 of Leibniz International Proceedings in Informatics        Raumer, J. 2015. The Lean Theorem Prover (System De-
(LIPIcs), 4:1–4:19. Dagstuhl, Germany: Schloss Dagstuhl–           scription). In Felty, A. P.; and Middeldorp, A., eds., Au-
Leibniz-Zentrum fuer Informatik. ISBN 978-3-95977-122-             tomated Deduction - CADE-25, 378–388. Cham: Springer
1.                                                                 International Publishing.
Abdulaziz, M.; and Kurz, F. 2023. Formally Verified SAT-           de Moura, L.; and Ullrich, S. 2021. The Lean 4 Theorem
Based AI Planning. In Proceedings of the Thirty-Seventh            Prover and Programming Language. In Automated Deduc-
AAAI Conference on Artificial Intelligence (AAAI 2023),            tion – CADE 28: 28th International Conference on Auto-
14665–14673. AAAI Press.                                           mated Deduction, Virtual Event, July 12–15, 2021, Proceed-
Abdulaziz, M.; and Lammich, P. 2018. A Formally Verified           ings, 625–635. Berlin, Heidelberg: Springer-Verlag. ISBN
Validator for Classical Planning Problems and Solutions. In        978-3-030-79875-8.
2018 IEEE 30th International Conference on Tools with Ar-          Drexler, D.; Seipp, J.; and Geffner, H. 2022. Learning
tificial Intelligence (ICTAI), 474–479.                            Sketches for Decomposing Planning Problems into Subprob-
Aggarwal, P.; Parno, B.; and Welleck, S. 2025. AlphaVerus:         lems of Bounded Width. In Proceedings of the Thirty-
bootstrapping formally verified code generation through self-      Second International Conference on Automated Planning
improving translation and treefinement. In Proceedings of          and Scheduling (ICAPS 2022), 62–70. AAAI Press.
the 42nd International Conference on Machine Learning,             Eriksson, S.; Röger, G.; and Helmert, M. 2017. Unsolvabil-
ICML’25. JMLR.org.                                                 ity Certificates for Classical Planning. In Proceedings of
the Twenty-Seventh International Conference on Automated         and Natarajan, S., eds., Proceedings of the Thirty-Eighth
Planning and Scheduling (ICAPS 2017), 88–97. AAAI Press.         AAAI Conference on Artificial Intelligence (AAAI 2024),
First, E.; Rabe, M. N.; Ringer, T.; and Brun, Y. 2023. Bal-      20256–20264. AAAI Press.
dur: Whole-Proof Generation and Repair with Large Lan-           Solar-Lezama, A.; Tancau, L.; Bodik, R.; Seshia, S.; and
guage Models. In Proceedings of the 31st ACM Joint Euro-         Saraswat, V. 2006. Combinatorial sketching for finite pro-
pean Software Engineering Conference and Symposium on            grams. In Proceedings of the 12th International Confer-
the Foundations of Software Engineering, ESEC/FSE 2023,          ence on Architectural Support for Programming Languages
1229–1241. Association for Computing Machinery. ISBN             and Operating Systems, ASPLOS XII, 404–415. New York,
9798400703270.                                                   NY, USA: Association for Computing Machinery. ISBN
Francès, G.; Bonet, B.; and Geffner, H. 2021. Learning Gen-      1595934510.
eral Planning Policies from Small Examples Without Super-        Song, P.; Yang, K.; and Anandkumar, A. 2024. Towards
vision. In Proceedings of the Thirty-Fifth AAAI Conference       Large Language Models as Copilots for Theorem Proving in
on Artificial Intelligence (AAAI 2021), 11801–11808. AAAI        Lean. CoRR, abs/2404.12534.
Press.                                                           Srivastava, S.; Immerman, N.; and Zilberstein, S. 2011. A
Haslum, P.; Lipovetzky, N.; Magazzeni, D.; and Muise, C.         new representation and associated algorithms for generalized
2019. An Introduction to the Planning Domain Definition          planning. Artificial Intelligence, 175(2): 615–647.
Language, volume 13 of Synthesis Lectures on Artificial In-      Srivastava, S.; Zilberstein, S.; Immerman, N.; and Geffner,
telligence and Machine Learning. Morgan & Claypool Pub-          H. 2011. Qualitative Numeric Planning. In Proceedings of
lishers.                                                         the Twenty-Fifth AAAI Conference on Artificial Intelligence
Howey, R.; Long, D.; and Fox, M. 2004. VAL: Automatic            (AAAI 2011), 1010–1016. AAAI Press.
Plan Validation, Continuous Effects and Mixed Initiative         Ståhlberg, S.; Bonet, B.; and Geffner, H. 2022. Learning
Planning Using PDDL. In Proceedings of the 16th Interna-         general optimal policies with graph neural networks: Ex-
tional Conference on Tools with Artificial Intelligence (ICTAI   pressive power, transparency, and limits. In Proceedings of
2004), 294–301. IEEE.                                            the International Conference on Automated Planning and
Hu, Y.; and Levesque, H. J. 2010. A Correctness Result           Scheduling, volume 32, 629–637.
for Reasoning about One-Dimensional Planning Problems.           Ståhlberg, S.; Bonet, B.; and Geffner, H. 2025. Learning
In Proceedings of the Twelfth International Conference on        More Expressive General Policies for Classical Planning Do-
Principles of Knowledge Representation and Reasoning (KR         mains. In Proceedings of the Thirty-Ninth AAAI Conference
2010), 362–371. AAAI Press.                                      on Artificial Intelligence (AAAI 2025), 26697–26706. AAAI
Jiménez, S.; Segovia-Aguas, J.; and Jonsson, A. 2019. A          Press.
review of generalized planning. The Knowledge Engineering        Stein, K.; Hodel, N.; Fišer, D.; Hoffmann, J.; Katz, M.; and
Review, 34: e5.                                                  Koller, A. 2026. Improved generalized planning with LLMs
McDermott, D. M. 2000. The 1998 AI planning systems              through strategy refinement and reflection. In Proceedings
competition. AI magazine, 21(2): 35–55.                          of the International Conference on Automated Planning and
Mugdan, E.; Christen, R.; and Eriksson, S. 2023. Optimality      Scheduling, volume 36, 677–686.
Certificates for Classical Planning. In Proceedings of the       Taitler, A.; Alford, R.; Espasa, J.; Behnke, G.; Fišer, D.;
Thirty-Third International Conference on Automated Plan-         Gimelfarb, M.; Pommerening, F.; Sanner, S.; Scala, E.;
ning and Scheduling (ICAPS 2023), 286–294. AAAI Press.           Schreiber, D.; Segovia-Aguas, J.; and Seipp, J. 2024. The
Ospanov, A.; Farnia, F.; and Yousefzadeh, R. 2025.               2023 International Planning Competition. AI Magazine,
APOLLO: Automated LLM and Lean Collaboration for Ad-             45(2): 280–296.
vanced Formal Reasoning. In The Thirty-ninth Annual Con-         Wang, J.; Zhang, J.; Guo, Q.; Guo, L.; Li, R.; Zhang, C.;
ference on Neural Information Processing Systems.                Peng, C.; Wang, C.; Zhao, D.; Shi, J.; Wang, J.; Feng, L.;
Paglieri, D.; Cross, L.; Genewein, T.; Leibo, J. Z.; Tomasev,    Shen, M.; Li, Q.; An, S.; Wang, S.; Shi, W.; Xi, X.; Li, X.;
N.; and Vezhnevets, A. S. 2026. A Case Study on Emer-            Cao, X.; Lu, Y.; Zhao, Y.; Chen, Z.; Lin, Z.; Wang, W.;
gent Cheating and Whistleblowing in Autonomous Research          Pei, P.; and Cai, X. 2026. LongCat-Flash-Prover: Advanc-
Swarms. arXiv:2609.04170.                                        ing Native Formal Reasoning via Agentic Tool-Integrated
                                                                 Reinforcement Learning. arXiv:2603.21065.
Pfenning, F.; and Paulin-Mohring, C. 1990. Inductively de-
fined types in the Calculus of Constructions. In Main, M.;
Melton, A.; Mislove, M.; and Schmidt, D., eds., Mathemati-                               Datasets
cal Foundations of Programming Semantics, 209–228. New           Table 3 lists the datasets from which the debugging problem
York, NY: Springer-Verlag. ISBN 978-0-387-34808-7.               instances, as well as the instance generators based on which
Seipp, J.; Torralba, Á.; and Hoffmann, J. 2022. PDDL Gen-        the validity constraint specifications were created.
erators. https://doi.org/10.5281/zenodo.6382173.
Silver, T.; Dan, S.; Srinivas, K.; Tenenbaum, J.; Pack Kael-           Additional Representation Examples
bling, L.; and Katz, M. 2024. Generalized Planning in PDDL       Figure 5 shows a side-by-side example of a PDDL problem
Domains with Pretrained Large Language Models. In Dy, J.;        instance with two spanners, two nuts and four locations (in-
                   Domain         Source of debugging problems Instance Generator
                   delivery                                   Silver et al. (2024)
                   ferry                          IPC Learning track 2023 (Taitler et al. 2024)
                   heavy                                      Silver et al. (2024)
                   hiking                                     Silver et al. (2024)
                   miconic                                    Silver et al. (2024)
                   spanner                        IPC Learning track 2023 (Taitler et al. 2024)
                   blocksworld                    IPC Learning track 2023 (Taitler et al. 2024)
                   goldminer      Stein et al. (2026)                 Seipp, Torralba, and Hoffmann (2022)
                   grippers       Stein et al. (2026)                 Seipp, Torralba, and Hoffmann (2022)
                   logistics      Stein et al. (2026)                 Seipp, Torralba, and Hoffmann (2022)
                   rovers                         IPC Learning track 2023 (Taitler et al. 2024)
                   satellite                      IPC Learning track 2023 (Taitler et al. 2024)
                   transport      Stein et al. (2026)                 Seipp, Torralba, and Hoffmann (2022)

Table 3: The origin of the debugging tasks that we used for our experiments and the instance generators based on which we
created the validity constraints.


cluding shed and gate) (left part) and the corresponding Lean
problem instance (right part).
   Listing 12 shows examples of the additional, domain-
specific lemmas about how states change (and do not change)
that are generated symbolically based on the PDDL and
provided as helper lemmas to the LLM. Listing 13 shows
additional symbolically generated lemmas that the LLM is
provided for an domain.
(define (problem prob0)            def problemStatics : StaticState :=
 (:domain spanner)                 {
 (:objects                           objects := [0, 1, 2, 3, 4, 5, 6, 7, 8]
     bob - man                       link_p := fun x0 x1 => (x0 == 5 && x1 == 6) || (x0 == 6 && x1 ==
     spanner1 - spanner                   8) || (x0 == 7 && x1 == 5),
     spanner2 - spanner              location_t := fun x0 => (x0 == 5) || (x0 == 6) || (x0 == 7) || (
     nut1 - nut                          x0 == 8),
     nut2 - nut                      locatable_t := fun x0 => (x0 == 0) || (x0 == 1) || (x0 == 2) ||
     loc1 - location                     (x0 == 3) || (x0 == 4),
     loc2 - location                 man_t := fun x0 => (x0 == 0),
     shed - location                 nut_t := fun x0 => (x0 == 3) || (x0 == 4),
     gate - location                 spanner_t := fun x0 => (x0 == 1) || (x0 == 2)
 )                                 }
 (:init
     (at bob shed)                 def problemDynamic : DynamicState :=
     (at spanner1 loc2)            {
     (useable spanner1)              at_p := fun x0 x1 => (x0 == 0 && x1 == 7) || (x0 == 1 && x1 ==
     (at spanner2 loc1)                  6) || (x0 == 2 && x1 == 5) || (x0 == 3 && x1 == 8) || (x0 ==
     (useable spanner2)                  4 && x1 == 8),
     (loose nut1)                    carrying_p := fun x0 x1 => false,
     (at nut1 gate)                  useable_p := fun x0 => (x0 == 1) || (x0 == 2),
     (loose nut2)                    tightened_p := fun x0 => false,
     (at nut2 gate)                  loose_p := fun x0 => (x0 == 3) || (x0 == 4)
     (link shed loc1)              }
     (link loc1 loc2)
     (link loc2 gate)              def goalDynamic : GoalDynamic :=
 )                                 {
 (:goal                               at_p := fun x0 x1 => none,
   (and                               carrying_p := fun x0 x1 => none,
     (tightened nut1)                 useable_p := fun x0 => none,
     (tightened nut2)                 tightened_p := fun x0 => if x0 == 3 then some true else if x0 ==
   )                                       4 then some true else none,
 )                                    loose_p := fun x0 => none
)                                  }}


Figure 5: Example of a PDDL definition of a problem instance from the Spanner domain (left) and the corresponding, converted
Lean problem instance (right).
-- walk does not change any predicate function from the static state part
lemma walk_statics (var_start var_end var_m : Obj) (s : State) :
    (walk var_start var_end var_m s).statics = s.statics := rfl

-- walk changes at_p for the man walking and the end location to true
lemma walk_at_p_eq1 (var_start var_end var_m : Obj) (s : State) :
    (walk var_start var_end var_m s).dynamic.at_p var_m var_end = true := by
  unfold walk
  simp

-- walk never changes at_p for locations other than the start and end location parameters
lemma walk_at_p_ne_var_l (var_start var_end var_m : Obj) (s : State) {var_end’ : Obj} (h1 :
    var_end’ ̸= var_end) (h2 : var_end’ ̸= var_start) :
    (walk var_start var_end var_m s).dynamic.at_p var_m var_end’ = s.dynamic.at_p var_m
        var_end’ := by
  unfold walk
  simp [h1, h2]

-- walk never changes carrying_p
lemma walk_carrying_p (var_start var_end var_m : Obj) (s : State) :
    (walk var_start var_end var_m s).dynamic.carrying_p = s.dynamic.carrying_p := rfl

-- Applying any plan does not change any predicate functions from the static state part
lemma runPlan_statics (plan : List PlanAction) (s : State) :
    (runPlan plan s).statics = s.statics := by
  induction plan generalizing s with
  | nil => simp [runPlan]
  | cons a as ih =>
      simp only [runPlan]
      rw [ih]
      cases a with
      | walk var_s var_e var_m => exact walk_statics var_s var_end var_m s
      | pickup_spanner var_l var_s var_m => exact pickup_spanner_statics var_l var_s var_m s
      | tighten_nut var_l var_s var_m var_n => exact tighten_nut_statics var_l var_s var_m
          var_n s

-- Applying an action in a valid state yields a valid successor state
lemma action_preserves_wf
    {a : PlanAction}
    {s : State}
    (hwf : WellFormed s)
    (hpre : actionPre a s) :
    WellFormed (actionApply a s) := by
  cases a with
  | walk var_start var_end var_m =>
      exact walk_preserves_wf var_start var_end var_m s hwf hpre
  | pickup_spanner var_l var_s var_m =>
      exact pickup_spanner_preserves_wf var_l var_s var_m s hwf hpre
  | tighten_nut var_l var_s var_m var_n =>
      exact tighten_nut_preserves_wf var_l var_s var_m var_n s hwf hpre


Listing 12: Examples of the additional, symbolically generated, lemmas provided the LLM for generating the completeness
proof for the Spanner domain.
-- Applying a valid plan in a valid state yields a valid state
lemma validPlan_preserves_wf
    {plan : List PlanAction}
    {s : State}
    (hplan : ValidPlan plan s)
    (hwf : WellFormed s) :
    WellFormed (runPlan plan s) := by
  induction plan generalizing s with
  | nil =>
      simpa [runPlan]
  | cons a as ih =>
      simp only [ValidPlan] at hplan
      rcases hplan with ⟨ha, has⟩
      have hwf’ :=
        action_preserves_wf (s := s) hwf ha
      exact ih has hwf’

-- Additional lemmas for combining sub plans
lemma runPlan_append (as bs : List PlanAction) (s : State) :
    runPlan (as ++ bs) s = runPlan bs (runPlan as s) := by
  induction as generalizing s with
  | nil => simp [runPlan]
  | cons a as ih => simp [runPlan, ih]

lemma validPlan_append (as bs : List PlanAction) (s : State) :
    ValidPlan (as ++ bs) s ↔ ValidPlan as s ∧ ValidPlan bs (runPlan as s) := by
  induction as generalizing s with
  | nil => simp [ValidPlan, runPlan]
  | cons a as ih => simp [ValidPlan, runPlan, ih, and_assoc]


Listing 13: The additional, symbolically generated, lemmas provided the LLM for generating the completeness proof for any
domain.
 1   structure GPBuild where
 2     actions : List PlanAction
 3     state    : State
 4     location : Obj
 5
 6   def gpFindMan (s : State) : Obj :=
 7     match s.statics.objects.find? (fun o => s.statics.man_t o) with
 8     | some m => m
 9     | none   => 0
10
11   def gpFindManLocation (s : State) (m : Obj) : Obj :=
12     match s.statics.objects.find? (fun l =>
13       s.statics.location_t l && s.dynamic.at_p m l) with
14     | some l => l
15     | none   => 0
16
17   def gpFindNextLocation (s : State) (l : Obj) : Option Obj :=
18     s.statics.objects.find? (fun next =>
19       s.statics.link_p l next)
20
21   def gpFindCarriedUseableSpanner (s : State) (m : Obj) : Option Obj :=
22     s.statics.objects.find? (fun sp =>
23       s.statics.spanner_t sp &&
24       s.dynamic.carrying_p m sp &&
25       s.dynamic.useable_p sp)
26
27   def gpCollectAt : List Obj → Obj → Obj → State → GPBuild
28     | [], l, _, s =>
29         {
30           actions := []
31           state := s
32           location := l
33         }
34     | sp :: rest, l, m, s =>
35         if s.statics.spanner_t sp = true ∧
36             s.dynamic.at_p sp l = true ∧
37             s.dynamic.useable_p sp = true then
38           let a := PlanAction.pickup_spanner l sp m
39           let s’ := actionApply a s
40           let result := gpCollectAt rest l m s’
41           {
42              actions := a :: result.actions
43              state := result.state
44              location := l
45           }
46         else
47           gpCollectAt rest l m s
48
49   def gpTraverse : Nat → Obj → Obj → State → GPBuild
50     | 0, l, m, s =>
51         gpCollectAt s.statics.objects l m s
52     | Nat.succ fuel, l, m, s =>
53         let collected := gpCollectAt s.statics.objects l m s
54         match gpFindNextLocation collected.state l with
55         | none =>
56             collected
57         | some next =>
58             let a := PlanAction.walk l next m
59             let s’ := actionApply a collected.state
60             let result := gpTraverse fuel next m s’
61             {
62               actions := collected.actions ++ (a :: result.actions)
63               state := result.state
64               location := result.location
65                }
66
67   def gpTightenAll : List Obj → Obj → Obj → State → GPBuild
68     | [], l, _, s =>
69         {
70           actions := []
71           state := s
72           location := l
73         }
74     | n :: rest, l, m, s =>
75         if s.statics.nut_t n = true ∧
76            s.dynamic.loose_p n = true then
77           match gpFindCarriedUseableSpanner s m with
78           | none =>
79               gpTightenAll rest l m s
80           | some sp =>
81               let a := PlanAction.tighten_nut l sp m n
82               let s’ := actionApply a s
83               let result := gpTightenAll rest l m s’
84               {
85                 actions := a :: result.actions
86                 state := result.state
87                 location := l
88               }
89         else
90           gpTightenAll rest l m s
91
92   def solve (s : State) (g : Goal) : List PlanAction :=
93     let m := gpFindMan s
94     let start := gpFindManLocation s m
95     let traversed :=
96       gpTraverse s.statics.objects.length start m s
97     let tightened :=
98       gpTightenAll s.statics.objects traversed.location m traversed.state
99     traversed.actions ++ tightened.actions

     Listing 14: Example of an LLM-generated generalized plan for the Spanner domain, consisting of the main solve function
     and helper declarations.
