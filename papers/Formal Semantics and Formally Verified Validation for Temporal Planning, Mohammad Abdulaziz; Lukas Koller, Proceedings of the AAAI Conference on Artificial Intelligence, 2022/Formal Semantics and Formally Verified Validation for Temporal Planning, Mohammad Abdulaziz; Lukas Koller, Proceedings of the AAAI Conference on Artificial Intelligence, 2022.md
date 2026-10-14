                                               Formal Semantics and Formally Verified Validation for Temporal Planning

                                                                               Mohammad Abdulaziz1,2 and Lukas Koller1
                                                                                        1
                                                                                            Techniche Universität München, Germany
                                                                                         2
                                                                                             King’s College London, United Kingdom
arXiv:2203.13604v1 [cs.AI] 25 Mar 2022




                                                                    Abstract                                      for most planning competitions, VAL (Howey, Long, and
                                                                                                                  Fox 2004), is implemented in C++. Another challenge to
                                           We present a simple and concise semantics for temporal plan-
                                                                                                                  plan validation is that the semantics of planning languages
                                           ning. Our semantics are developed and formalised in the
                                           logic of the interactive theorem prover Isabelle/HOL. We de-           have ambiguities, which lead to different interpretations of
                                           rive from those semantics a validation algorithm for tempo-            what constitutes a correct plan. E.g. there are multiple inter-
                                           ral planning and show, using a formal proof in Isabelle/HOL,           pretations of sub-typing using “Either” in PDDL.
                                           that this validation algorithm implements our semantics. We               In this work we address the aforementioned challenges
                                           experimentally evaluate our verified validation algorithm and          using an interactive theorem prover (ITP). In particular, we
                                           show that it is practical.                                             use the ITP Isabelle/HOL (Nipkow, Paulson, and Wenzel
                                                                                                                  2002), which implements a formal mathematical system
                                                                Introduction                                      combining higher-order logic (HOL) and simple type the-
                                                                                                                  ory. Our first contribution is that we formally specify an
                                         Although, performance-wise, planning algorithms and sys-
                                                                                                                  abstract syntax for the temporal fragment of PDDL 2.1 in
                                         tems are very scalable and efficient, as shown by different
                                                                                                                  Isabelle/HOL and, based on that, formalise its semantics.
                                         planning competitions (Long et al. 2000; Coles et al. 2012;
                                                                                                                  Compared to a pen-and-paper semantics, this has the advan-
                                         Vallati et al. 2015), there is still to be desired when it comes
                                                                                                                  tage that it removes any room for ambiguity. Furthermore,
                                         to their trustworthiness, which is crucial to their wide adop-
                                                                                                                  during formalising this fragment of PDDL, we found that
                                         tion. Consequently, there have been substantial efforts to
                                                                                                                  certain parts of the semantics as specified by Fox and Long
                                         improve the trustworthiness of planning systems (Howey,
                                                                                                                  could be simplified. As our second contribution, we imple-
                                         Long, and Fox 2004; Fox, Howey, and Long 2005; Eriksson,
                                                                                                                  ment an executable plan validator for the temporal part of
                                         Röger, and Helmert 2017; Abdulaziz, Norrish, and Gretton
                                                                                                                  PDDL2.1 and we formally verify, using Isabelle/HOL, that
                                         2018; Abdulaziz and Lammich 2018; Cimatti, Micheli, and
                                                                                                                  it correctly implements the semantics which we formalised.
                                         Roveri 2017; Abdulaziz, Gretton, and Norrish 2019). A ba-
                                                                                                                  Our validator checks (i) if a given problem and the candidate
                                         sic task when it comes to the trustworthiness of planning
                                                                                                                  plan are well-formed, and (ii) if the candidate plan is indeed
                                         systems is that of plan validation. In its most basic form,
                                                                                                                  a solution to the problem. Lastly, we experimentally show
                                         this task is solved by a plan validator, which is a program
                                                                                                                  that this validator is practical and compare it with VAL.
                                         that, given a planning problem and a candidate plan, con-
                                         firms whether the candidate plan indeed solves the problem.                                     Background
                                         This boosts the trustworthiness of a plan chiefly because the
                                         plan validator should be a simple piece of software that can             In this work we build upon previous work by Abdulaziz and
                                         be more easily inspected than the planning system that com-              Lammich. In their work, they formalised the syntax and se-
                                         puted the plan and, accordingly, less likely to have mistakes.           mantics of the STRIPS fragment of PDDL in Isabelle/HOL.
                                            One challenge to plan validation is that the semantics of             The syntax was based on a grammar by Kovacs. Their se-
                                         planning languages and formalisms can be too complicated.                mantics have two parts: (i) a part defining what it means for a
                                         This makes the validator a rather complicated piece of soft-             PDDL domain, instance or plan to be well-formed and (ii) a
                                         ware defeating the trustworthiness appeal of the whole ap-               part defining the execution semantics of PDDL. The most
                                         proach. This is especially the case for advanced planning                interesting aspect of well-formedness has to do with typ-
                                         formalisms, like temporal planning (Fox and Long 2003),                  ing: since the grammar of PDDL allows for Either-supertype
                                         hybrid planning, and planning problems with processes and                specifications of the form ‘obj - Either obj1 obj2· · · ’, this
                                         events (Fox and Long 2002). This problem is further exacer-              leads to ambiguities in interpreting the sub-typing relation
                                         bated by the low-level languages in which plan validators are            when, for instance, instantiating a parameter with an Either-
                                         usually implemented, e.g. the plan validation system used                type by an object of an Either-type. In this situation, they
                                                                                                                  took the interpretation that this is a valid substitution if each
                                         Copyright © 2022, Association for the Advancement of Artificial          of the object types is reachable, in the sub-typing relation,
                                         Intelligence (www.aaai.org). All rights reserved.                        from at least one of the parameter types. For the execution
semantics, they formalised execution semantics of grounded                     and (p-at pk fj ) encode at which floor an elevator or a passen-
STRIPS in Isabelle/HOL and, based on that, specified the                       ger currently is. The proposition (in-el pk ei ) encodes whether
execution semantics of PDDL by instantiating PDDL action                       a passenger is in an elevator or not. The proposition (el-op ei )
schemata into STRIPS ground actions.                                           encodes whether an elevator door is open. The initial state
    Since most of our work here concerns action execution,                     is I ≡ {(el-at e0 f0 ), (el-at e1 f1 ), (p-at p0 f1 ), (p-at p1 f0 ),
which is defined at the level of ground actions, this entire                   (el-op e0 )} and its goal is G ≡ (p-at p0 f0 ) ∧ (p-at p1 f1 ). In
paper discusses ground actions and grounded planning prob-                     the initial state passenger p0 is on floor f 1 and passenger
lems. The main change we made at the lifted action/problem                     p1 is on floor f 0 . Both passengers want to change floors:
level to the formalisation by Abdulaziz and Lammich is that                    passenger p0 want to move to floor f 0 and passenger p1
we add an action duration constraints as a syntactic element                   wants to move to floor f 1 . This is specified in the goal state
to the abstract syntax element modelling action schemata.                      formula. Among many actions, the problem has actions to
We skip here those (modified) definitions and assume that                      open one elevator’s door (op e1 ) ≡ hh¬(el-op e1 ), ∅, ∅i, h>,
the ground problems and plans were obtained from well-                         {(el-op e1 )}, ∅i, >i, to have each of the passengers enter one
formed PDDL problems and plans, e.g. all parameters to                         of the elevators (en p0 e1 f1 ) ≡ hh(p-at p0 f1 ) ∧ (el-at e1 f1 ),
predicates and action schemata are well-typed and action                       ∅, ∅i, h>, {(in-el p0 e1 )}, {(p-at p0 f1 )}i, (el-op e1 )i             and
durations in the plan respect the duration constraints in the                  (en p1 e0 f0 )        ≡        hh(p-at p1 f0 ) ∧ (el-at e0 f0 ), ∅, ∅i, h>,
action schemata. Interested readers should consult the for-                    {(in-el p1 e0 )}, {(p-at p1 f0 )}i, (el-op e0 )i, and to close
malisation scripts.                                                            an elevator’s door (cl e0 ) ≡ hh(el-op e0 ), ∅, ∅i, h>, ∅,
Definition 1 (Propositional Formulae). A propositional for-                    {(el-op e0 )}i, >i. Each one of the actions has the expected
mula φ defined over a set of atoms V is either (i) the verum                   preconditions and effects; e.g. moving the elevator requires
>, (ii) an atom v, s.t. v ∈ V , (iii) a negated propositional                  its door to be closed during the entire move action.
formula ¬φ, (iv) a conjunction of two propositional formu-                     Definition 3 (Plan). A plan is a sequence of tuples
lae φ1 ∧ φ2 , or (v) a disjunction of propositional formulae                   hπ0 , t0 , d0 i, . . . , hπn , tn , dn i, where, for 1 ≤ i ≤ n, πi ∈ δ
φ1 ∨ φ2 . A valuation A is a mapping of V to the set {0, 1}.                   is an action, ti ∈ Q≥0 and di ∈ Q≥0 are rational numbers,
A valuation A is a model for a formula φ, written A |= φ,                      to which we refer as the starting time point and the dura-
iff (i) φ is the verum, (ii) if φ is an atom, then A(v) = 1,                   tion, respectively. For a plan →          π , we call a sorted sequence
(iii) if φ a negated formula ¬φ, then A 6|= φ, (iv) if φ is a                  t0 , . . . , tn of the set of rational numbers {t | ha, t, di ∈
                                                                               →
conjunction φ1 ∧ φ2 , then A |= φ1 and A |= φ2 , and (v) if                    π } ∪ {t + d | ha, t, di ∈ →             π } the happening time points
φ is a disjunction of propositional formulae φ1 ∨ φ2 , then                    of the plan, and we denote it by htps(→          π ).
A |= φ1 or A |= φ2 .                                                               A valid plan for the elevator running exam-
Note: sometimes, for notational economy, we treat a valua-                     ple starts with the following four plan actions:
tion as a set. In such cases, a valuation A : V → {0, 1} is                    h(op e1 ), 0, 1i, h(en p0 e1 f1 ), 1.25, 0.5i, h(en p1 e0 f0 ), 2, 1i,
interpreted as the set {v | A(v ) = 1} and a set of atoms V                    and h(cl e0 ), 3, 1i.
is interpreted as a valuation which maps any v ∈ V to 1, and                       A central question when it comes to the semantics of tem-
everything else to 0. Also, in the rest of this paper a state is               poral planning is that of plan validity. A central notion for
synonymous with a valuation.1                                                  defining plan validity is that of action non-interference.
Definition 2 (Planning Problem). A planning problem Π is a                     Definition 4 (Non-interference). Snap actions π 1 and π 2
tuple hP, δ, I, Gi, where (i) P is a set of atoms, each of which               are non-interfering iff (i) atoms(π 1 pre )∩ (π 2 add ∪π 2 del ) = ∅,
is a state characterising proposition, (ii) δ: set of actions,                 (ii) atoms(π 2 pre )∩(π 1 add ∪π 1 del ) = ∅, (iii) π 1 add ∩π 2 del = ∅,
each of which is a tuple hπstart , πend , πinv i where • πstart , πend         and (iv) π 2 add ∩ π 1 del = ∅.
are start and end snap actions, and • πinv is a formula de-
fined over the propositions P . A snap action π is a tuple                         The first definition of PDDL 2.1 temporal plan validity
hπpre , πadd , πdel i where • πpre is its precondition, a formula              was posed by Fox and Long 2003. Here we outline their
using propositions P , • πadd ⊆ P are its positive effects, and                definitions informally, due to lack of space. In their defi-
• πdel ⊆ P are its negative effects. (iii) I is a valuation over               nitions, a central notion was that of a simple plan, which
P , modelling the initial state, and (iv) G is the goal state                  can be thought of as a temporal plan whose actions all have
condition, which is a propositional formula defined over P .                   zero duration. Execution semantics of simple plans are sim-
                                                                               ilar to the semantics of ∀-step parallel plans (Rintanen, Hel-
    As a running example we use a planning problem,                            janko, and Niemelä 2006): more than one action can execute
which models an elevator control situation. There are                          at the same time, given that the actions are non-interfering.
two passengers (p0 and p1 ), who want to use two el-                           A valid temporal plan is defined one that can be compiled
evators (e0 and e1 ) to change floors (f 0 and f 1 ). The                      into a valid simple plan. In this compilation, each durative
set of state characterising
                          S      propositions for this planning                action π starting at a time point t and which has duration
problem is P ≡              {{(el-at ei fj ), (p-at pk fj ), (in-el pk ei ),   d is compiled to three snap actions with duration zero. The
(el-op ei )} | 0 ≤ i, j, k ≤ 1}. The propositions (el-at ei fj )               first action is πstart and it is scheduled to execute at t in the
    1
      In the formalisation by Abdulaziz and Lammich, on which we               simple plan. The second action is πend and it is scheduled to
base our work, there is support for equalities. This is done by mod-           execute at t + d in the simple plan. The third is an action
elling states as sets of formulae. We omit these details here since            with precondition πinv and no effects, which is scheduled to
they are orthogonoal to the the semantics of durative actions.                 execute in the simple plan multiple times. It executes once
between every two happening time points of the plan iff the         0                                      0.75          1            1.25           1.5

two happening time points are between t and t+d, inclusive.
                                                                                            (op e1 )                                         (en p0 e1 f1 )
Isabelle/HOL
                                                                                                                   (en p1 e0 f0 )                      (cl e0 )
An ITP is a program which implements a formal mathe-
matical system, i.e. a formal language, in which definitions
and theorem statements are written, and a set of axioms
                                                                    I0                                    I0.75         I1           I1.25          I1.5
or derivation rules, using which proofs are constructed. To
prove a fact in an ITP, the user provides high-level steps of a
                                                                    B0                                    B0.75         B1          B1.25           B1.5
proof, and the ITP fills in the details, at the level of axioms,
culminating in a formal proof.                                       I0 = {}                                       B0 = {(op e1 )start }
                                                                     I0.75 = {(op e1 )inv }                        B0.75 = {(en p1 e0 f0 )start }
   We performed the formalisation and the verification using
                                                                     I1 = {(op e1 )inv , (en p1 e0 f0 )inv }       B1 = {(op e1 )end }
the interactive theorem prover Isabelle/HOL (Nipkow, Paul-
                                                                     I1.25 = {(en p1 e0 f0 )inv }                  B1.25 = {(en p1 e0 f0 )end ,
son, and Wenzel 2002), which is a theorem prover for HOL.            I1.5 = {(en p0 e1 f1 )inv }                                    (en p1 e0 f0 )start }
Roughly speaking, HOL can be seen as a combination of                                                              B1.5 = {(cl e0 )start }
functional programming with logic. Isabelle/HOL supports
the extraction of the functional fragment to actual code in         Figure 1: Concepts from Def. 5 for the elevator example.
various languages (Haftmann and Nipkow 2007).
   Isabelle is designed for trustworthiness: following the
Logic for Computable Functions approach (LCF) (Milner              Definition 5 (Valid State Sequence). For t ∈ Q≥0 and
1972), a small kernel implements the inference rules of the        a plan → π , let Bt ≡ {πstart | hπ, t, di ∈ →   π } ∪ {πend |
logic, and, using encapsulation features of ML, it guaran-         hπ, t − d, di ∈ →   π } and It ≡ {πinv | hπ, t0 , di ∈ →    π ∧
tees that all theorems are actually proved by this small ker-      t0 < t < t0 + d}. Also, let t0 , . . . , tn be the happening
nel. Around the kernel there is a large set of tools that im-      time points of → π . For a sequence of states M0 , . . . , Mn+1 ,
plement proof tactics and high-level concepts like algebraic       we say the sequence of states is valid wrt a plan →           π
datatypes and recursive functions. Bugs in these tools can-        iff, for every happening time point ti of →     π , we have:
not lead to inconsistent theorems being proved, but only to        (i) Mi |= πinv , for every πinv ∈ Iti , (ii) Mi |= πpre , for
error messages when the kernel refuses a proof.                    every π ∈ Bti , (iii)SBti is pairwise
   All the definitions, theorems and proofs in this paper have                                           S non-interfering, and
                                                                   (iv) Mi+1 = (Mi − π∈Bt πdel ) ∪ π∈Bt πadd .
been formalised in Isabelle/HOL. The formalisation can be                                                      i                         i

found online2 . Usually, some definitions are best represented     Definition 6 (Valid Plan). Plan →    π is a valid plan for a
formally in a way which is different from how they repre-          problem Π iff there is a state sequence M1 , . . . , Mn+1 s.t.
sented informally. For instance, a for-loop or a function ap-      I, M1 , . . . , Mn+1 is valid wrt →
                                                                                                     π and Mn+1 |= G.
plied to an indexed sequence in the informal definition are           Note: above, simultaneous execution of instantaneous
formalised in Isabelle/HOL as recursions over lists. How-          ground actions is only allowed for non-interfering ground
ever, there is always a clear resemblance between the formal       actions. Otherwise, simultaneous execution might result in a
and the informal definitions and we provide a description          not well-defined state. We also use the same ground action
associated with the formal definitions.                            interference condition defined by Fox and Long.
           Semantics of Temporal Planning                             Figure 1 illustrates the beginning of the instantiation of
                                                                   the elevator running example for Def. 5. At the top of the il-
One issue with Fox and Long’s definition of plan validity          lustration a timeline is depicted. Below the timeline the first
is that it is too close to an operational specification of a       four actions from the valid plan are shown. At the bottom
validation algorithm for temporal plans. A negative conse-         of the illustration the individual sets needed for the state se-
quence of that becomes evident when trying to formalise            quence are shown.
the semantics and pin down all the details: the definitions
then become very complicated and unreadable. Although              Refining the Semantics Towards Executability
the need for simplifying definitions is generally evident, that    A main goal of this paper is to construct a plan valida-
need is exacerbated when the definitions are used as specifi-      tor which is formally verified wrt the semantics. We do
cations against which we formally verify a validator. In that      that by following a step-wise refinement approach (Wirth
scenario, the semantics should also provide a description of       1971), where we start from the abstractly specified seman-
what the validator should do and they should be easily un-         tics and refine that specification towards an executable pro-
derstandable through visual inspection. We resolve that by         gram which fulfils those abstractly specified semantics. The
providing a description of the semantics that abstractly de-       next step to refine our semantics is to obtain a version that is
scribes what a valid plan is, without appealing to algorithmic     closer to the executable program. In this version, we closely
constructions like the one of induced happening sequences.         follow the semantics given by Fox and Long. A central con-
We then show that our new definitions are equivalent to the        cept in defining the semantics of temporal plans is that of
operational definitions of Fox and Long.                           happening sequences. Intuitively, these are the instantaneous
   2                                                               changes that happen over the course of plan execution.
       DOI:10.5281/zenodo.5784579
  0                                     0.75         1          1.25           1.5             to be checked. Therefore, happening h2 contains the invari-
                                                                                               ant snap action for the first plan action (op e1 ). In between
                         (op e1 )                                      (en p0 e1 f1 )
                                                                                               the consecutive happening time points 0.75 and 1 the action
                                                                                               (op e1 ) is running as well as the action (en p1 e0 f0 ), hence
                                               (en p1 e0 f0 )                    (cl e0 )
                                                                                               the happening h4 contains the invariant snap actions for both
                                                                                               (op e1 ) and (en p1 e0 f0 ).
                                                                                                  The illustration in Figure 2 only shows one possible in-
 h1                 h2                  h3     h4    h5    h6   h7      h8     h9
                                                                                               duced happening sequence for the valid plan. Def. 8 allows
  h1 ≡ h{(op e1 )start }, 0.0i                       h6 ≡ h{(en p1 e0 f0 )inv }, 1.125i        invariant snap actions to be placed arbitrarily in between
  h2 ≡ h{(op e1 )inv }, 0.375i                       h7 ≡ h{(en p1 e0 f0 )end ,                consecutive happening time points. This is more general
  h3 ≡ h{(en p1 e0 f0 )start }, 0.75i                           (en p1 e0 f0 )start }, 1.25i
                                                                                               than the definition of Fox and Long, which arbitrarily re-
  h4 ≡ h{(op e1 )inv , (en p1 e0 f0 )inv }, 0.875i   h8 ≡ h{(en p0 e1 f1 )inv }, 1.375i
  h5 ≡ h{(op e1 )end }, 1.0i
                                                                                               stricts the placement of invariant snap actions to be exactly
                                                     h9 ≡ h{(cl e0 )start }, 1.5i
                                                                                               in the middle of happening time points. We use this place-
                                                                                               ment of invariant actions in the next section, where we give
Figure 2: Illustration for the beginning of an induced hap-
                                                                                               an executable definition of plan validity. Based on the notion
pening sequence (Def. 8) for the elevator-running example.
                                                                                               of valid happening we define the following notion of plan
                                                                                               validity, which is closer to the definition of Fox and Long
 Definition 7 (Valid Happening Sequence). A happening h                                        and to executability.
 is a pair hA, ri, where A is a set of snap actions and                                        Definition 9 (Valid Plan II). Plan →   π is valid for a plan-
 r ∈ Q≥0 is the starting time point. For a happening se-                                       ning problem Π iff →    π has an induced happening sequence
 quence hA0 , r0 i, . . . , hAn , rn i and a state M0 , we call a                              h0 . . . , hn s.t. the happening sequence is valid wrt I and
 state sequence M1 , . . . , Mn+1 to be induced by M0 and the                                  Mn+1 |= G, where Mn+1 is the last state in the induced
 happening sequence iff for every 0 ≤ i < m (i) Mi |= πpre ,                                   state sequence.
 for every π ∈ Ai , (ii) ASi is pairwise         S non-interfering,                              At a higher-level, the contrast between Def. 9 and 6 boils
 and (iii) Mi+1 = Mi − π∈Ai πdel ∪ π∈Ai πadd , for                                             down to that the former specifies plan validity in terms of
 0 ≤ i ≤ n. A happening sequence is valid wrt some state iff                                   a happening sequence that should be computed, while the
 they induce a valid state sequence.                                                           latter specifies validity more abstractly. More specifically,
     A happening sequence which models the effects and exe-                                    instead of referring to happening sequences, Def. 6 uses Bt
 cutability of a temporal plan is called an induced happening                                  and It , which denote the snap actions executing at time t
 sequence. The validity of a temporal plan is defined as the                                   and the set of invariants which should hold at time t, respec-
 validity of the induced happening sequence.                                                   tively. Accordingly, for Def. 9 we only assert the existence
 Definition 8 (Induced Happening Sequence). A happen-                                          of a sequence of valid states, which can be formalised, in
 ing sequence hA0 , r0 i, . . . , hAm , rm i is an induced hap-                                Isabelle/HOL, as a simple recursion on the happening time
 pening sequence for a plan →         π with happening time points                             points of a plan, instead of asserting the existence of an in-
tS0 , . . . , tn iff, for all 0 ≤ i ≤ m, we have that Ai ⊆                                     duced happening sequence as in the case of Def. 9. The two
    {{hπinv , ∅, ∅i, πstart , πend } | hπ, t, di ∈ →π } and, for all                           definitions are equivalent as shown below.
hπ, t, di ∈ →     π , (i) there is a happening hAi , ri i with ri = t                          Theorem 1. For a planning problem Π, a plan →        π is valid
and πstart ∈ Ai , (ii) there is a happening hAj , rj i with                                    according to Def. 9 iff it is valid according to Def. 6.
rj = t + d and πend ∈ Aj , (iii) for each 0 ≤ l < n with
t ≤ tl < t + d there is hAk , rk i with tl < rk < tl+1 and                                     Proof sketch. Let t0 , . . . , tn be the happening time points of
                                                                                               →
hπinv , ∅, ∅i ∈ Ak , and (iv) the starting time points r0 , . . . , rm                         π after being sorted in ascending order.
are strictly sorted in an ascending order.                                                     (⇒) From Def. 9, →        π has an induced happening sequence
                                                                                               hA0 , r0 i, . . . , hAm , rm i, and that happening sequence is
     Figure 2 illustrates the beginning of an induced happen-
                                                                                               valid wrt I. Note that m ≥ n. Our goal here is to show
ing sequence for the elevator running example. At the top of
                                                                                               that the induced state sequence of this happening sequence
the illustration, a timeline with the happening time points is
                                                                                               is a valid state sequence, according to Def. 5. Since the in-
shown. Every start- or end-point of a plan action is a hap-
                                                                                               duced happening sequence is strictly sorted according to the
pening time point. In this example, the first five happening
                                                                                               starting time of the happenings, we know that the different
time points are: 0, 0.75, 1, 1.25, and 1.5. Below the timeline
                                                                                               happenings have different starting points. Accordingly, we
the first four actions from the valid plan are shown. For each
                                                                                               have, for each ti , where 0 ≤ i ≤ n, there is a happening
plan action, the snap actions are placed along the timeline
                                                                                               hAj , rj i, s.t. Bti = Aj and ti = rj . Since this induced
and collected in the happenings, which are symbolized as
                                                                                               happening sequence is also a valid happening sequence, the
red squares in the illustration. E.g. for the first plan action
                                                                                               conjuncts (ii), (iii), and (iv) of Def. 5 hold for the induced
h(op e1 ), 0, 1i, the start snap action (op e1 )start is placed at
                                                                                               state sequence. What remains is to show that conjunct (i)
the start of the action, at time point 0 and collected in hap-
                                                                                               holds for the induced state sequence, which states that all
pening h1 , whereas the end snap action (op e1 )end is placed
                                                                                               action invariants hold during action execution. Observe that
at the end of the action, at time point 1 and collected in
                                                                                               conjunct (iii) of Def. 8 asserts that, for each hπ, t, di ∈ → π,
happening h5 . For every two consecutive happening time
                                                                                               there is an action hπinv , ∅, ∅i between each two happenings
points the invariants of all currently running actions need
that happen during the execution of an action π. The precon-              Algorithm 1: The executable specification of plan
ditions of this action ensure that the invariants of the action π         validity, check-plan, as pseudo-code. In this pseudo-
are not violated during its execution. Accordingly, conjunct              code, Π denotes a planning problem, →            π a plan to be
(i) holds for the induced state sequence.                                 checked, H a sequence of happenings, Ai a set of
(⇐) To prove this direction, we need to show that →           π has       snap actions, ri a happening starting time point, and
an induced happening sequence, which is valid wrt I, from                 t a happening time point.
a given valid state sequence I, M1 , . . . , Mn+1 . Consider
the happening sequence hBt0 , t0 i, hIt1 , t0 +t                            function insert-action(hA0 , r0 i, . . . , hAm , rm i, t, π)
                                                   2 i, hBt1 , t1 i,
                                                      1

      t1 +t2                                tn−1 +tn                         for each 0 ≤ i < m
hIt2 , 2 i, . . . , hBtn−1 , tn−1 i, hItn ,    2     i, hBtn , tn i.           if ri = t
We now need to show that this happening sequence                                  ret hA0 , r0 i, . . . , hAi ∪ {π}, ri i, . . . , hAm , rm i
is a valid one, according to Def. 7. It is easy to see                         if ri+1 = t
that conjunct (ii) of Def. 7 holds for this happening se-                         ret hA0 , r0 i, . . . , hAi+1 ∪ {π}, ri+1 i, . . . ,
quence. To show that the other two conjuncts of Def. 7                                    hAm , rm i
hold, we first need to provide a witness state sequence                        if ri < t < ri+1
to which those conjuncts apply. The state sequence                                ret hA0 , r0 i, . . . , hAi , ri i, h{π}, ri,
I, M1 , M1 , . . . , Mn+1 , Mn+1 3 is the witness: • Conjunct (i)                         hAi+1 , ri+1 i, . . . , hAm , rm i
of Def. 7 holds for I, M1 , M1 , . . . , Mn+1 , Mn+1 because
                                                                            function simplify-action(t0 , . . . tn , hπ, t, di, H)
conjunct (i) of Def. 5 holds for I, M1 , . . . , Mn+1 , which
                                                                             H := insert-action(H, t, πstart )
implies that the preconditions in each action in a happening
                                                                             H := insert-action(H, t + d, πend )
hBti , ti i are entailed by the state Mi , and conjunct (ii)
                                                                             for each 0 ≤ i < n
of Def. 5 also holds for I, M1 , . . . , Mn+1 , which implies
                                                                               if t ≤ ti < ti+1 ≤ t + d
that the preconditions of each happening hIti , ti−12+ti i are                                                     r +r
entailed by the state Mi−1 . • Conjunct (iii) of Def. 7 holds                     H := insert-action(H, i 2 j , hπinv , ∅, ∅i)
for I, M1 , M1 , . . . , Mn+1 , Mn+1 because conjunct (iii)                  ret H
of Def. 7 holds for I, M1 , . . . , Mn+1 . The last remaining               function simplify-plan(→        π)
thing is to show that the happening sequence we constructed                  H := ∅
is an induced happening sequence for →            π , according to           for each hπ, t, di ∈ →     π
Def. 8: • The first two conjuncts of Def. 8 hold for this                      simplify-action(htps(→       π ), hπ, t, di, H)
happening sequence because from the definition of B and I.                   ret H
• The third conjunct holds due to the way we construct the                  function valid-hap-seq(hA0 , r0 i, . . . , hAm , rm i, Π)
happening sequence. • The fourth conjunct holds because                      M := I
we have the happening time points already sorted and the                     for each 0 ≤ i ≤ m
way we construct our happening sequence. This finishes our                     if ∃π 1 , π 2 ∈ Ai and they are interfering
proof.                                                                            ret False
                                                                               if ∃π ∈ Ai .M 6|= πpre
          An Executable Verified Validator                                        ret False
The last part of our work is regarding implementing an ex-
                                                                                               S                 S
                                                                               M := M − π∈Ai πdel ∪ π∈Ai πadd
ecutable specification of the semantics, i.e. a plan valida-                 if M |= G
tion algorithm, and formally proving that it is equivalent to                  ret True
the unexecutable specification of the semantics in Def. 6.                   ret False
The formalized semantics are defined with unexecutable ab-
                                                                            function check-plan(Π, →        π)
stract mathematical types and depend on several mathemat-
                                                                             H := simplify-plan(→         π)
ical concepts, e.g. sets and quantifiers. To obtain an ex-
                                                                             if valid-hap-seq(H, Π)
ecutable validator these mathematical types and concepts
                                                                               ret “valid Plan”
need to be replaced with efficient algorithms. We use step-
                                                                             ret “error”
wise refinement to replace the abstract specifications in the
semantics with algorithms. With step-wise refinement effi-
cient implementations of algorithms can be proven correct
by using multiple correctness preserving steps to refine an              on abstract mathematical types like sets. This is shown in
abstract version of the algorithm towards the efficient im-              the pseudo-code of our validation algorithm in Algorithm 1,
plementation. This allows us to formalize concise semantics              where check-plan is the top-level routine. We then prove the
and implement an efficient validator wrt. those semantics.               following theorem about it.
   We do two main refinement steps: first, we replace the ab-            Theorem 2. check-plan(Π, →    π ) = "valid Plan" iff →
                                                                                                                              π is valid
stract specifications of the semantics with algorithms defined           for the planning problem Π according to Def. 6.
   3
     This repetition of states is intended: each state Mi occurs first   Lemma 1. Let →  π be a plan and H and H 0 be induced hap-
as a result of executing the happening hBti , ti i at state Mi−1 and     pening sequences for → π . If a state sequence is an induced
                                                            t  +t
then second as a result of executing the happening hIti , i−12 i i,      state sequence by a state M0 and H, then there is a state
which has no effects, at state Mi .                                      sequence induced by M0 and H 0 , where the last state of the
two sequences is the same.                                                                        1
                                                                                                              VAL
Proof sketch. Firstly, let H (H 0 ) be (A0 , r0 ), (A1 , r1 ), . . . ,                                    our validator




                                                                                   runtime [s]
(Am , rm )            ((A00 , r0 ), (A01 , r10 ), . . . , (Am0 , rm0 )),    let
t0 , t1 , . . . , tn be the happening time points of →              π , and let                  0.5
M1 , M2 , . . . , Mm+1 (M10 , M20 , . . . , Mm0 +1 ) be the induced
state sequences of I and H (H 0 ). Because of the fourth con-
junct of Def. 8, we have a monotonically increasing mapping
f (f 0 ) from {0, 1, . . . , n} to {0, 1, . . . , m} ({0, 1, . . . , m0 }),                       0
such that, for 0 ≤ i ≤ n, ti = rf (i) (ti = rf 0 (i) ) and




                                                                                                       crewplanning

                                                                                                                      elevators

                                                                                                                                  openstacks

                                                                                                                                               pegsol

                                                                                                                                                        sokoban

                                                                                                                                                                  Driverlog

                                                                                                                                                                              MatchCellar

                                                                                                                                                                                            Parking

                                                                                                                                                                                                      Satellite

                                                                                                                                                                                                                  Storage

                                                                                                                                                                                                                            TurnandOpen
f (n) = m (f 0 (n) = m0 ). Also, from the third conjunct of
Def. 8 we have that, for 0 ≤ i ≤ n, Af (i) (Af 0 (i) ) has no
invariant snap actions and, accordingly, Af (i) = Af 0 (i) ,
and for j ∈ {0, 1, . . . , m} \ {f (0), f (1), . . . , f (n)}
(j ∈ {0, 1, . . . , m} \ {f (0), f (1), . . . , f (n)}), Aj has                    Figure 3: Validation running times for IPC 2014 domains.
only invariant snap actions, i.e. Aj ⊆ {hφ, ∅, ∅i | φ is
propositional formula}. From the two previous statements,
we conclude that Mf (i) = Mf 0 (i) , for 0 < i ≤ n, which                         2004) implements this  and thus requires the  as an extra
finishes our proof.                                                               parameter. This leads to rejecting, otherwise valid, plans if a
                                                                                  too large  is given to VAL.
Lemma 2. For any plan → π , simplify-plan(→
                                          π ) is an induced                       Parsing Problems and Code Generation For parsing, we
happening sequence for the plan →
                                π.                                                use an open source parser combinator library written in Stan-
Proof sketch. This follows from Def. 8.                                           dard ML. We note that parsing is a trusted part of our val-
                                                                                  idator, i.e. we have no formal proof that the parser actually
Lemma 3. For any happening sequence H and planning                                recognises the desired grammar and produces the correct
problem Π, valid-hap-seq(H, Π) is true iff H is a valid hap-                      abstract syntax tree. However, the parsing combinator ap-
pening sequence wrt. I.                                                           proach allows to write concise, clean, and legible parsers,
                                                                                  which can be relatively easily checked.
Proof sketch. This follows from Def. 7.
                                                                                  Experimental        Evaluation Our          validator   sup-
Proof of Theorem 2. The theorem follows from Lem-                                 ports the following PDDL requirements: :strips,
mas 2, 3 and 1, and Theorem 1.                                                    :equality, :typing, :negative-preconditions,
   A validator has to be executable and efficient and thus the                    :disjunctive-preconditions, :durative-actions,
implementation of a validator is more complicated than the                        and :duration-inequalities. For the evaluation of our
formalisation of the semantics.                                                   validator, we compare the validation results and running
   In the next step-wise refinement step, the abstract math-                      time of our validator to those of VAL (Howey, Long, and
ematical types, like the set operations in valid-hap-seq, are                     Fox 2004). We use IPC 2014 domains. We used the temporal
replaced with efficient implementation using balanced trees.                      planners ITSAT (Rankooh and Ghassem-Sani 2015) and
Since this step is completely automated with the Contain-                         Temporal Fast Downward (TFD) (Eyerich, Mattmüller, and
ers Framework in Isabelle/HOL (Lochbihler 2013), we do                            Röger 2009) to generate plans for the domains and prob-
not describe the resulting pseudo-code or the proofs of its                       lems. In all test cases, the validation outcome between our
equivalence to the pseudo-code from Algorithm 1.                                  validator and VAL is the same. Our validator is consistently
   Before we close this section we would like to note two                         slower than VAL, as can be seen in Figure 3. However, it
points. First, the formal version of Algorithm 1 includes                         never needs more than one second to validate any plan.
checks related to PDDL-level well-formedness, like the cor-                       This is a practically acceptable performance, escpecially
rectness of typing of action arguments, etc. These details are                    since our validator uses arbitrary precision arithmetic. We
similar to what was done by Abdulaziz and Lammich and                             also note that formally verified code is usually orders of
we ignore them here as we only focus on grounded prob-                            magnitude slower than unverified code due to the difficulty
lems. Readers interested in the PDDL-level reasoning can                          of verifying all code optimisations which are liberally used
consult the associated formalisation. Second, as one of our                       in unverified code.
goals was to simplify the semantics, we do not assert the                                                                              Discussion
presence of a concrete minimum separation, , between plan
actions. In our refinement steps, we are able to derive a vali-                   In this work we presented the first specification of the se-
dation algorithm which uses arbitrary arithmetic on rational                      mantics of the temporal part of PDDL2.1 in a formal mathe-
numbers and it is formally proved to implement Def. 6. This                       matical system, namely, Isabelle/HOL. Specifying language
is an improvement over the approach of Fox and Long, who                          semantics in formal mathematical systems has the advan-
claimed in their paper that it is necessary to accept that nu-                    tages of removing any ambiguities and providing the ba-
meric conditions, including time, will have to be evaluated                       sis to build formally verified tool chains to reason about
to a certain tolerance. Indeed, VAL (Howey, Long, and Fox                         these languages. These advantages of formalising language
semantics have been reported by researchers who use ITPs          mantics are a declarative specification of the semantics of
to formalise programming language semantics, e.g. C (Nor-         PDDL 2.1 as opposed to the state transition-based seman-
rish 1998), SML (Kumar et al. 2014), and Rust (Jung et al.        tics of Fox and Long. This has the advantage that all the
2018). One main purpose of our work was to showcase the           computational and meta-theoretic properties of ES apply to
merits of this methodology to the planning community.             it. On the other hand, it has the disadvantage of being less
   The semantics and validation of the temporal fragment of       understandable than a state transition-based definition, as
PDDL have been studied by multiple authors. We believe            one needs to first understand ES. Seen from that perspec-
our work improves over all the previous approaches in two         tive, our formalisation three properties:(i) It is clearly state
aspects: the succinctness of our semantics specificaiton and      transition-based as our semantics are in terms recursively
the trusworthiness of our executable validator.                   defined action execution and state transitions. This makes
   PDDL2.1 was first introduced during the second inter-          it more readable than the formalisation of Claßen, Hu, and
national planning competition and its semantics were most         Lakemeyer. (ii) It is also declarative in HOL since, although
comprehensively defined by Fox and Long 2003. We base             our top-level definitions are state transition-based, the mech-
our work on the semantics of Fox and Long. One issue              anisms behind the recursive function definitions and the al-
with their semantics noted by earlier authors Claßen, Hu,         gebraic data types in HOL are all declarative in terms of
and Lakemeyer is that it defines plan validity using an ex-       the axioms of HOL (Krauss 2009; Traytel, Popescu, and
ecutable plan validation algorithm, which is more compli-         Blanchette 2012). (iii) Has less clear computational prop-
cated than what a specification of semantics ought to be. We      erties, since general procedures to reason about HOL are all
address that by providing simpler semantics and showing it        heuristic, since the logic is incomplete. This disadvantage is
is equivalent to an executable validator. Our semantics are       not an issue, however, in our context given that our goal is
simpler because they (i) remove the need for a fixed “” sep-     to specify a concise semantics for deriving correct by con-
aration between interfering actions, requiring only an arbi-      struction software. It can, nonetheless, be remedied by for-
trary non-zero separation, (ii) bypass the concept of induced     malising the semantics of ES in HOL and formally show-
happening sequences, and (iii) do not require that snap ac-       ing, within Isabelle/HOL, the correctness of the encoding of
tions representing invariants occur exactly between each two      PDDL in ES from Claßen, Hu, and Lakemeyer.
happenings which occur while the invariant has to hold. An-           A lot of work on trustworthiness in planning has fo-
other difference between our work and that of Fox and Long        cused on plan validation. The state-of-the-art plan validator
is that we specify our semantics in Isabelle/HOL wrt abstract     for temporal plans is VAL (Howey, Long, and Fox 2004).
syntax which is very close to PDDL syntax.4 This gives rise       Since VAL implements temporal planning semantics, which
to a more detailed specification of the semantics and leaves      is rather involved, in C++, it is difficult to inspect VAL to
less room for ambiguities.                                        make sure that it is free of bugs. This, in a sense, defeats one
   Another tangentially related work is that of Gigante           of the main purposes of plan validators: they are supposed
et al. 2020. In their work, they studied the complexity of        to boost trustworthiness by being much simpler than plan-
computing plans for different restrictions of the temporal        ning systems, making it less likely for them to have bugs
planning as described by Fox and Long.                            and making them easier to inspect. One motivation for our
   Another notable planning language which includes tem-          work was to avoid that problem by having a separate con-
poral elements is ANML (Smith, Frank, and Cushing 2008).          cise specification of the semantics which precisely describes
The semantics of a language “inspired” by ANML were               what the validator implements. These semantics are then for-
defined by Cimatti, Micheli, and Roveri 2017. Although            mally connected to an efficient validator. Another approach
Cimatti, Micheli, and Roveri use pen-and-paper definitions,       to temporal plan validation is the one by (Cimatti, Micheli,
the level of detail of their presentation is closer to ours as    and Roveri 2017), who compile a given planning problem
they specified an abstract syntax for their language, based       and a candidate plan into a formula of temporal logic. Plan
on which they defined their semantics. However, our seman-        validation then becomes a satisfiability task for an LTL for-
tics are much more succinct than theirs since we use HOL to       mula. From a trustworthiness perspective, this approach has
specify our semantics, while they specify their semantics in      the disadvantages that one has to trust the code that imple-
terms of linear temporal logic modulo real arithmetic, which      ments the compilation to LTL and, more importantly, either
is significantly less expressive than HOL.                        one has to trust an LTL model-checker or devise a valida-
   Another well-established formalism for studying the se-        tor that validates models of LTL formulae. Our approach, on
mantics of planning and action languages in general is sit-       the other hand, trusts a much smaller code base, thanks to
uation calculus (McCarthy and Hayes 1981; Reiter 2001).           the LCF architecture of Isabelle/HOL.
In that line of work, the work by Claßen, Hu, and Lake-               As future work, we would like to connect our formalisa-
meyer 2007 is the most related to this paper. They showed         tion of temporal planning to the formalisation of timed au-
how to encode a PDDL 2.1 problem as a formula in ES,              tomata by Wimmer and von Mutius 2020. This would enable
which is a dialect of first-order logic with interesting compu-   us to generate formally checkable certificates of unsolvabil-
tational and meta-theoretic properties introduced by Lake-        ity for temporal planning problems. It would also enable for-
meyer and Levesque 2004. The main merit of that approach,         mally verified checking of different properties of a planning
as stated by Claßen, Hu, and Lakemeyer, is that their se-         domain similar to the ones by Cimatti, Micheli, and Roveri,
   4
                                                                  but with formal guarantees.
       Interested readers should consult the formalisation.
Acknowledgements This work was facilitated through the           AAAI Conference on Artificial Intelligence, AAAI 2020, The
DFG Koselleck Grant NI 491/16-1.                                 Thirty-Second Innovative Applications of Artificial Intelli-
                                                                 gence Conference, IAAI 2020, The Tenth AAAI Symposium
                       References                                on Educational Advances in Artificial Intelligence, EAAI
Abdulaziz, M.; Gretton, C.; and Norrish, M. 2019. A Ver-         2020, New York, NY, USA, February 7-12, 2020, 9859–9866.
ified Compositional Algorithm for AI Planning. In 10th           AAAI Press.
International Conference on Interactive Theorem Proving,         Haftmann, F.; and Nipkow, T. 2007. A Code Generator
ITP 2019, September 9-12, 2019, Portland, OR, USA, vol-          Framework for Isabelle/HOL. Technical Report 364/07, De-
ume 141 of LIPIcs, 4:1–4:19. Schloss Dagstuhl - Leibniz-         partment of Computer Science, University of Kaiserslautern.
Zentrum für Informatik.                                          Howey, R.; Long, D.; and Fox, M. 2004. VAL: Automatic
Abdulaziz, M.; and Lammich, P. 2018. A Formally Verified         Plan Validation, Continuous Effects and Mixed Initiative
Validator for Classical Planning Problems and Solutions. In      Planning Using PDDL. In 16th IEEE International Confer-
IEEE 30th International Conference on Tools with Artifi-         ence on Tools with Artificial Intelligence (ICTAI 2004), 15-
cial Intelligence, ICTAI 2018, 5-7 November 2018, Volos,         17 November 2004, Boca Raton, FL, USA, 294–301. IEEE
Greece, 474–479. IEEE.                                           Computer Society.
Abdulaziz, M.; Norrish, M.; and Gretton, C. 2018. Formally       Jung, R.; Jourdan, J.-H.; Krebbers, R.; and Dreyer, D. 2018.
Verified Algorithms for Upper-Bounding State Space Diam-         RustBelt: Securing the Foundations of the Rust Program-
eters. J. Autom. Reason., 61(1-4): 485–520.                      ming Language. Proc. ACM Program. Lang., 2(POPL):
Cimatti, A.; Micheli, A.; and Roveri, M. 2017. Validat-          66:1–66:34.
ing Domains and Plans for Temporal Planning via Encoding         Kovacs, D. L. 2011. BNF Definition of PDDL 3.1. IPC-
into Infinite-State Linear Temporal Logic. In Proceedings of     2011.
the Thirty-First AAAI Conference on Artificial Intelligence,
                                                                 Krauss, A. 2009. Automating Recursive Definitions and Ter-
February 4-9, 2017, San Francisco, California, USA, 3547–
                                                                 mination Proofs in Higher-Order Logic. Ph.D. thesis, Tech-
3554. AAAI Press.
                                                                 nical University Munich.
Claßen, J.; Hu, Y.; and Lakemeyer, G. 2007. A Situation-
                                                                 Kumar, R.; Myreen, M. O.; Norrish, M.; and Owens, S.
Calculus Semantics for an Expressive Fragment of PDDL.
                                                                 2014. CakeML: A Verified Implementation of ML. In The
In Proceedings of the Twenty-Second AAAI Conference on
                                                                 41st Annual ACM SIGPLAN-SIGACT Symposium on Prin-
Artificial Intelligence, July 22-26, 2007, Vancouver, British
                                                                 ciples of Programming Languages, POPL ’14, San Diego,
Columbia, Canada, 956–961. AAAI Press.
                                                                 CA, USA, January 20-21, 2014, 179–192. ACM.
Coles, A. J.; Coles, A.; Olaya, A. G.; Celorrio, S. J.; López,
C. L.; Sanner, S.; and Yoon, S. 2012. A Survey of the Sev-       Lakemeyer, G.; and Levesque, H. J. 2004. Situations, Si!
enth International Planning Competition. AI Mag., 33(1):         Situation Terms, No! In Principles of Knowledge Repre-
83–88.                                                           sentation and Reasoning: Proceedings of the Ninth Interna-
                                                                 tional Conference (KR2004), Whistler, Canada, June 2-5,
Eriksson, S.; Röger, G.; and Helmert, M. 2017. Unsolvabil-       2004, 516–526. AAAI Press.
ity Certificates for Classical Planning. In Proceedings of
the Twenty-Seventh International Conference on Automated         Lochbihler, A. 2013. Light-Weight Containers for Isabelle:
Planning and Scheduling, ICAPS 2017, Pittsburgh, Pennsyl-        Efficient, Extensible, Nestable. In Interactive Theorem
vania, USA, June 18-23, 2017, 88–97. AAAI Press.                 Proving - 4th International Conference, ITP 2013, Rennes,
                                                                 France, July 22-26, 2013. Proceedings, volume 7998 of Lec-
Eyerich, P.; Mattmüller, R.; and Röger, G. 2009. Using the       ture Notes in Computer Science, 116–132. Springer.
Context-Enhanced Additive Heuristic for Temporal and Nu-
meric Planning. ICAPS.                                           Long, D.; Kautz, H. A.; Selman, B.; Bonet, B.; Geffner, H.;
                                                                 Koehler, J.; Brenner, M.; Hoffmann, J.; Rittinger, F.; Ander-
Fox, M.; Howey, R.; and Long, D. 2005. Validating Plans          son, C. R.; Weld, D. S.; Smith, D. E.; and Fox, M. 2000. The
in the Context of Processes and Exogenous Events. In Pro-        AIPS-98 Planning Competition. AI Mag., 21(2): 13–33.
ceedings, The Twentieth National Conference on Artificial
Intelligence and the Seventeenth Innovative Applications of      McCarthy, J.; and Hayes, P. J. 1981. Some Philosophical
Artificial Intelligence Conference, July 9-13, 2005, Pitts-      Problems from the Standpoint of Artificial Intelligence. In
burgh, Pennsylvania, USA, 1151–1156. AAAI Press / The            Readings in Artificial Intelligence.
MIT Press.                                                       Milner, R. 1972. Logic for Computable Functions Descrip-
Fox, M.; and Long, D. 2002. PDDL+: Modeling Contin-              tion of a Machine Implementation. Technical report, Stan-
uous Time Dependent Effects. In Proceedings of the 3rd           ford University.
International NASA Workshop on Planning and Scheduling           Nipkow, T.; Paulson, L. C.; and Wenzel, M. 2002. Is-
for Space.                                                       abelle/HOL - A Proof Assistant for Higher-Order Logic, vol-
Fox, M.; and Long, D. 2003. PDDL2.1: An Extension to             ume 2283 of Lecture Notes in Computer Science. Springer.
PDDL for Expressing Temporal Planning Domains. JAIR.             ISBN 978-3-540-43376-7.
Gigante, N.; Micheli, A.; Montanari, A.; and Scala, E.           Norrish, M. 1998. C Formalised in HOL. Technical report,
2020. Decidability and Complexity of Action-Based Tem-           University of Cambridge, Computer Laboratory.
poral Planning over Dense Time. In The Thirty-Fourth
Rankooh, M. F.; and Ghassem-Sani, G. 2015. ITSAT: An
Efficient SAT-Based Temporal Planner. J. Artif. Intell. Res.,
53: 541–632.
Reiter, R. 2001. Knowledge in Action: Logical Foundations
for Specifying and Implementing Dynamical Systems. MIT
Press.
Rintanen, J.; Heljanko, K.; and Niemelä, I. 2006. Plan-
ning as Satisfiability: Parallel Plans and Algorithms for Plan
Search. Artif. Intell., 170(12-13): 1031–1080.
Smith, D. E.; Frank, J.; and Cushing, W. 2008. The ANML
Language. In KEPS.
Traytel, D.; Popescu, A.; and Blanchette, J. C. 2012. Foun-
dational, Compositional (Co)Datatypes for Higher-Order
Logic: Category Theory Applied to Theorem Proving. In
Proceedings of the 27th Annual IEEE Symposium on Logic
in Computer Science, LICS 2012, Dubrovnik, Croatia, June
25-28, 2012, 596–605. IEEE Computer Society.
Vallati, M.; Chrpa, L.; Grzes, M.; McCluskey, T. L.; Roberts,
M.; and Sanner, S. 2015. The 2014 International Planning
Competition: Progress and Trends. AI Mag., 36(3): 90–98.
Wimmer, S.; and von Mutius, J. 2020. Verified Certification
of Reachability Checking for Timed Automata. In Tools and
Algorithms for the Construction and Analysis of Systems -
26th International Conference, TACAS 2020, Held as Part of
the European Joint Conferences on Theory and Practice of
Software, ETAPS 2020, Dublin, Ireland, April 25-30, 2020,
Proceedings, Part I, volume 12078 of Lecture Notes in Com-
puter Science, 425–443. Springer.
Wirth, N. 1971. Program Development by Stepwise Refine-
ment. Commun. ACM.
                Appendix: Running Example                          door to be open. A PDDL-domain defines action schemas,
The problem is specified in PDDL by the PDDL-domain                which are instantiated with arguments to obtain executable
temp-elevators and PDDL-problem temp-elevators                     ground actions. For the instantiation of an action schema the
-prob1 in Listing 1 and 2.                                         conditions and effects of are partitioned by their annotation
                                                                   (at start, at end, and over all) to produce the snap
Listing 1: PDDL-domain for elevator planning problem
                                                                   actions πstart , πend , and the invariants πinv . The snap action
(define (domain temp-elevators)                                    πstart contains all instantiated conditions and effects anno-
  (:requirements :typing :negative-preconditions
        :durative-actions :duration-inequalities)
                                                                   tated with at start, whereas the snap action πend contains
  (:types floor - object elevator - object passenger - object)     all instantiated conditions and effects annotated with at
  (:predicates
      (el-at ?e - elevator ?f - floor)                             end, and πinv contains all instantiated invariants.
      (p-at ?e - passenger ?f - floor)
      (in-el ?p - passenger ?e - elevator)                          Listing 3: Valid plan for elevator planning problem
      (el-op ?e - elevator)
  )                                                                 0: (op e1)[1]
  (:functions (el-dur ?from - floor ?to - floor) - number)          1.25: (en p0 e1 f1)[0.5]
  (:durative-action mv                                              2: (cl e1)[1]
      :parameters (?e - elevator ?from - floor ?to - floor)         3: (mv e1 f1 f0)[1]
      :duration (= ?duration (el-dur ?from ?to))                    4: (op e1)[1]
      :condition (and (at start (el-at ?e ?from))                   5.25: (ex p0 e1 f0)[0.5]
                       (over all (not (el-op ?e))))                 0.75: (en p1 e0 f0)[0.5]
      :effect (and (at start (not (el-at ?e ?from)))                1.5: (cl e0)[1]
                   (at end (el-at ?e ?to)))                         2.5: (mv e0 f0 f1)[1]
  )                                                                 3.5: (op e0)[1]
  (:durative-action op                                              4.75: (ex p1 e0 f1)[0.5]
      :parameters (?e - elevator)
      :duration (= ?duration 1)
      :condition (at start (not (el-op ?e)))                          Listing 3 shows a valid plan for the running example. A
      :effect (at end (el-op ?e))
  )                                                                plan for a temporal planning problem is a schedule of actions
  (:durative-action cl                                             to execute. The plan specifies the starting time point and a
      :parameters (?e - elevator)
      :duration (= ?duration 1)                                    duration for each action. In PDDL the starting time points
      :condition (at start (el-op ?e))
      :effect (at end (not (el-op ?e)))
                                                                   are denoted in front of a colon (:) at the beginning of each
  )                                                                line. The duration of an action is denoted in brackets ([d],
  (:durative-action en
      :parameters (?p - passenger ?e - elevator ?f - floor)
                                                                   with duration d) at the end of a line.
      :duration (<= ?duration 1)                                      In the elevator example the end snap action for the action
      :condition (and (at start (and (p-at ?p ?f) (el-at ?e ?f))
            )                                                      instantiation of cl e0 and the start snap action for the action
                       (over all (el-op ?e)))                      instantiation of op e0 are interfering ground actions.
      :effect (and (at start (not (p-at ?p ?f)))
                   (at end (in-el ?p ?e)))                           • (cl e0)end = h>, ∅, {(el-op e0)}i
  )
  (:durative-action ex                                               • (op e0)start = h¬(el-op e0), ∅, ∅i
      :parameters (?p - passenger ?e - elevator ?f - floor)
      :duration (<= ?duration 1)                                   The end snap action for cl e0 contains the negative effect el-
      :condition (and (at start (and (in-el ?p ?e) (el-at ?e ?f)   op e0, which is a precondition of the start snap action of op
            ))
                       (over all (el-op ?e)))                      e0. This violates the first condition for non-interference be-
      :effect (and (at start (not (in-el ?p ?e)))
                   (at end (p-at ?p ?f)))
                                                                   tween ground actions (Definition 4). Intuitively this means,
  )                                                                there has to be a non-zero, but arbitrarily small, time inter-
)
                                                                   val where the elevator door is open before it can be closed
                                                                   again.
Listing 2: PDDL-problem for elevator planning problem

(define (problem temp-elevators-prob1)
                                                                                 Appendix: Isabelle/HOL Listings
(:domain elevators)
(:objects f0 f1 - floor p0 p1 - passenger e0 e1 - elevator)
                                                                   Isabelle’s syntax is a variation of Standard ML combined
(:init (el-at e0 f0)                                               with standard mathematical notation. Function application
    (el-at e1 f1)
    (el-op e0)                                                     is written infix, and functions can be Curried, i.e. function f
    (p-at p0 f1)                                                   applied to arguments x1 . . . xn is written as f x1 . . . xn
    (p-at p1 f0)
    (= (el-dur f0 f1) 1)                                           instead of the standard notation f (x1 , . . . , xn ).
    (= (el-dur f1 f0) 1))
(:goal (and (p-at p0 f0) (p-at p1 f1))))                           Formalising the Semantics
                                                                   The following code snippet shows our formalization of the
   In the running example, there are two passengers p0 and         ground action interference according to Definition 4.
p1, who want to use two elevators e0 and e1. Passenger p0
                                                                    Listing 4: Ground Action interference and Happening Sequence validity
wants to move from floor f1 to floor f0, whereas the passen-
                                                                         definition acts_non_intrf :: "ground_action ⇒ ground_action ⇒
ger p1 wants to move from floor f0 to floor f1. The PDDL-                      bool" where
domain (listing 1) specifies actions to move an elevator (mv),      2      "acts_non_intrf a b ←→
                                                                           (let
to enter and exit an elevator (en and ex), and to open and          4        adda = set(adds(effect a));
close and elevator door (op and cl). Each one of the actions        6
                                                                             dela = set(dels(effect a));
                                                                             prea = Atom ` atoms (precondition a);
has the expected preconditions and effects; e.g. mv requires                 addb = set(adds(effect b));
                                                                    8        delb = set(dels(effect b));
the elevator door to be closed during the entire move actions.               preb = Atom ` atoms (precondition b) in
For a passenger to enter an elevator, en requires the elevator     10        prea ∩ (addb ∪ delb ) = {} ∧
           preb ∩ (adda ∪ dela) = {} ∧
12         adda ∩ delb = {} ∧                                         of plan validity according to Definition 6.
           addb ∩ dela = {})"
                                                                       Listing 6: New Semantics

                                                                           lemma "valid_plan πs ≡ wf_plan πs
   The formalization of the ground action interference is              2     ∧ (∃htps M'. htps_seq πs htps
straight forward. The function acts_non_intrf returns a                      ∧ valid_state_seq I htps πs M' ∧ M' c |== (goal P))"
                                                                       4     unfolding valid_plan_def valid_plan_from_def by auto
boolean value indicating whether the given ground actions
are non-interfering according to Definition 4.
   The following code snippet shows our formalization of                 The predicate wf_plan characterizes a well-formed
Definition 5.                                                         plan, and the predicate htps_seq characterizes the se-
 Listing 5: New Semantics
                                                                      quence of happening time points for a plan. The predicate
                                                                      valid_plan characterizes the plan validity of a plan ac-
     definition acts_of_plan_at :: "time ⇒ plan ⇒ ground_action set
            " where                                                   cording to Definition 6.
 2     "acts_of_plan_at t i πs =
         {aπ. ∃π. (t i ,π) ∈ simple_acts πs ∧ Some aπ = res_inst π}   Formalising the Refined Semantics
 4     ∪ {as tar t . ∃π. (t i ,π) ∈ durative_acts πs
       ∧ Some as tar t = res_inst_snap_action π At_Start}             Next we are showing our formalization of our refined se-
 6     ∪ {aend . ∃t' π. (t',π) ∈ durative_acts πs
       ∧ t i = t' + duration π                                        mantics, which are based around the induced happening se-
 8     ∧ Some aend = res_inst_snap_action π At_End}"                  quence (Definition 8 and 7).
10   definition invs_of_plan_at :: "time ⇒ plan ⇒ (object atom)          The following code snippet shows our formalization of
           formula set" where
       "invs_of_plan_at t i πs =
                                                                      the happening execution (apply_happ) and the validity of
12       {inv. ∃tπ π. (tπ,π) ∈ durative_acts πs                       a happening sequence (valid_happ_seq).
       ∧ tπ < t i ∧ t i ≤ tπ + (duration π)
14     ∧ Some inv = res_inst_inv π}"                                   Listing 7: Induced Happening Sequence and Plan validity

16   fun apply_eff :: "ground_action set ⇒ world_model ⇒                   fun apply_happ :: "happening ⇒ world_model ⇒ world_model"
           world_model" where                                                    where
       "apply_eff Ai M =                                               2     "apply_happ (t i , A i ) M =
                (set ` dels ` effect ` A i )) ∪   (set ` adds `
              S                                 S                                 S                                           S
18       (M -                                                                (M -   (set (map (set o dels o effect) A i ))) ∪   (set (map
               effect ` A i )"                                                     (set o adds o effect) A i ))"
                                                                       4
20   fun valid_state_seq :: "world_model ⇒ time list ⇒ plan ⇒              fun valid_happ_seq :: "world_model ⇒ happening list ⇒
           world_model ⇒ bool" where                                             world_model ⇒ bool" where
       "valid_state_seq M [] πs M' ←→ (M = M')"                        6     "valid_happ_seq M [] M' ←→ (M = M')"
22   | "valid_state_seq M (t i #ts) πs M' ←→                               | "valid_happ_seq M ((t i ,A i )#hs) M' ←→
       (let A i = acts_of_plan_at t i πs in                            8     (∀a∈ set A i . M c |== precondition a)
24     (∀i ∈ invs_of_plan_at t i πs. M c |== i)                              ∧ (∀a ∈ set A i . ∀b ∈ set A i . a 6= b −→ acts_non_intrf a b)
       ∧ (∀a ∈ A i . M c |== precondition a)                          10     ∧ valid_happ_seq (apply_happ (t i ,A i ) M) hs M'"
26     ∧ (∀a ∈ A i . ∀b ∈ A i . a 6= b −→ acts_non_intrf a b)
       ∧ valid_state_seq (apply_eff A i M) ts πs M')"
                                                                         The function apply_happ returns the state after applying
   Note that in our formalization we make a distinc-                  the effects of a given happening to a given state. The validity
tion between durative and non-durative (instantaneous) ac-            of a happening sequence (Definition 7) is formalized with
tions. Therefore, the function simple_acts return all non-            the function valid_happ_seq, which is recursive on the
durative plan actions in a given plan, and the function               given happening sequence. The state sequence is only con-
durative_acts return all durative plan actions in a given             structed implicitly through the recursion. In each recursion
plan. The function res_inst_snap_action instantiates                  step it is checked that (i) the actions within the happening are
the snap action of a given durative plan action for a given           pairwise non-interfering and (ii) the preconditions of each
temporal annotation: At_Start or At_End, corresponding                action in the happening are satisfied by the current state.
to πstart and πend . The function res_inst instantiates the              The following code snippet shows our formalization
ground action for a non-durative plan action. The function            of the predicate that characterizes induced happening se-
res_inst_inv instantiates the invariant formula (πinv ) for           quences (Definition 8).
a given durative plan action. Given a time point t and a plan          Listing 8: Induced Happening Sequence
πs, the function call acts_of_plan_at t πs returns the                     definition ind_happ_seq :: "plan ⇒ happening list ⇒ bool"
set Bt from Definition 5. Similarly, given a time point t and                    where
                                                                       2     "ind_happ_seq πs hs ←→
a plan πs, the function call invs_of_plan_at t πs re-                        (strict_sorted (map fst hs)
turns the set It from Definition 5.                                    4     ∧ (∀(tπ,π) ∈ simple_acts πs.
                                                                               let ga = the (res_inst π) in
   The function apply_eff applies the effects of a set of              6       ∃A. (tπ,A) ∈ set hs ∧ ga ∈ set A)
                                                                             ∧ (∀(tπ,π) ∈ durative_acts πs.
ground actions to a given state and returns the resulting state.       8       let πs tar t = the (res_inst_snap_action π At_Start);
The function valid_state_seq recursively formalizes the                          πend = the (res_inst_snap_action π At_End);
                                                                      10         πinv = the (res_inst_snap_action π Over_All) in
validity of a state sequence according to Definition 5. The                    (∃A. (tπ,A) ∈ set hs ∧ πs tar t ∈ set A) ∧
state sequence is never explicitly constructed. In each recur-        12       (∃A. (tπ + (duration π),A) ∈ set hs ∧ πend ∈ set A) ∧
                                                                               (∀t i tj . (consec_htps πs t i tj
sion step it is checked that (i) all invariants for the current       14     ∧ tπ ≤ t i ∧ tj ≤ tπ + (duration π))
time point are satisfied by the current state, (ii) the precon-               −→ (∃(t',A) ∈ set hs.
                                                                      16         t i < t' ∧ t' < tj ∧ πinv ∈ set A)))
dition of each action for the current time point is satisfied                ∧ (∀(t i ,A i ) ∈ set hs. A i 6= [] ∧
by the current state, and (iii) all actions for the current time      18       (∀a ∈ set A i . ∃(tπ,π) ∈ set πs.
                                                                                 inst_of_plan_action πs (tπ,π) (t i ,a))))"
point are pairwise non-interfering.
   The following code snippet then shows our formalization
   An induced happening sequence is characterized by the              happening h is enabled in a given state M then en_exE re-
following constraints: (i) the induced happening sequence is          turn the resulting state after applying the effects of the hap-
strictly sorted by the time points of each happening, (ii) for        pening h. The function apply_happ_exec is an executable
each plan action the induced happening sequence contains              refinement of the function apply_happ.
the correct snap actions (according to Definition 8), and                The following lemma justifies the refinement for the hap-
(iii) every action in the induced happening sequence is a             pening execution.
grounded and instantiated snap action for a plan action. The          Listing 12: Justification Enabled-ness Execution of a Happening
predicate ind_happ_seq formalizes these constraints and
                                                                           lemma (in wf_ast_problem) en_exE_return_iff:
consists of four conjuncts. The first conjunct ensures that an        2      assumes "wm_basic s"
induced happening sequence is strictly sorted by the time                    and "∀a ∈ set A i . wf_ground_action a"
                                                                      4      shows "en_exE (t i ,A i ) s = Inr s' ←→ happ_enabled (t i ,A i ) s
points of happenings. The second and third conjuncts spec-                         ∧ s' = apply_happ (t i ,A i ) s"
                                                                             unfolding en_exE_def
ify the placement of the instantiated ground actions for each         6      using assms holds_for_wf_fmlas[OF <wm_basic s>]
plan action according to Definition 8. The fourth and final                  symmetric_pred_check_pairwise[OF acts_non_intrf_symmetric]
                                                                      8      apply_happ_exec_refine
conjunct uses the function inst_of_plan_action to en-                        by auto
sure that all ground actions in the induced happening se-
quence are a instantiated snap actions for a plan action.                The assumptions for this lemma are that the world model
   The following code snippet then shows our formalization            is basic and all ground actions in the happening are well-
of plan validity according to Definition 9.                           formed. A basic world model only contains predicate atoms.
Listing 9: Plan validity (II)                                         The lemma then states, that the function en_exE only re-
     definition plan_happ_path :: "world_model ⇒ plan ⇒ world_model   turns Inr s' if the given happening (ti ,Ai ) is enabled in
           ⇒ bool" where                                              the state s and the application of the effects yield the world
2      "plan_happ_path M πs M' ←→
       (∃hs. ind_happ_seq πs hs ∧ valid_happ_seq M hs M')"            model s'. Otherwise the function will return Inl msg with
4
     lemma "valid_plan2 πs ≡ wf_plan πs
                                                                      an error message msg.
6      ∧ (∃M'. plan_happ_path I πs M' ∧ M' c |== goal P)"                The validity of a happening sequence (Definition 7) is im-
       unfolding valid_plan2_def valid_plan_from2_def by auto
                                                                      plemented recursively and combined with the enabled-ness
                                                                      execution for happenings. Moreover, the entailment of the
   The formalization of the plan validity valid_plan2 uses            goal state specifications is directly checked in the base case
an existential quantifier for a valid induced happening se-           of the recursion.
quence.                                                               Listing 13: Validity of a Happening Sequence
   The next code snippet shows the Lemma that proves the                   fun valid_happ_seq_fromE :: "nat ⇒ world_model ⇒ happening
equivalence between the two plan validity definitions (Defi-                     list ⇒ _+unit" where
                                                                      2      "valid_happ_seq_fromE si s [] =
nition 6 and 9).                                                             check (holds s (goal P))
Listing 10: Equivalence Proof                                         4        (ERRS ''Postcondition does not hold'')"
                                                                           | "valid_happ_seq_fromE si s (h#hs) = do {
     lemma                                                            6      s ← en_exE h s <+? (λe _. shows ''at step '' o shows si o
2      assumes "wf_problem"                                                        shows '': '' o e ());
       shows "valid_plan πs ←→ valid_plan2 πs"                               valid_happ_seq_fromE (si+1) s hs}"
4      unfolding valid_plan_def valid_plan2_def
       using valid_plan_from2_iff[OF assms] by blast
                                                                         The argument si is the index of the current execution
                                                                      step. The implementation is justified with the following
   Under the assumptions that the given planning problem              lemma.
and plan are well-formed (wf_problem) both formaliza-                 Listing 14: Justification for Validity of a Happening Sequence
tions (valid_plan and valid_plan2) are equivalent.
                                                                           lemma (in wf_ast_problem)
Formalization of Executable Plan Validator                            2      assumes "wm_basic M" and "wf_happ_seq hs"
                                                                             shows "valid_happ_seq_fromE k M hs = Inr () ←→
                                                                             (∃ M'. valid_happ_seq M hs M' ∧ M' c |== (goal P))"
First, executable refinements for the semantics of ground ac-         4
                                                                             using assms valid_happ_seq_from_refine
tions and happenings are implemented.                                              valid_happ_seq_fromE_return_iff by auto

Listing 11: Enabled-ness Execution of a Happening

     definition en_exE :: "happening ⇒ world_model ⇒ _+world_model"
                                                                        The function valid_happ_seq_fromE only returns Inr
            where                                                      () if there exists a state M', such that the given happening
2      "en_exE ≡ λ(t i ,A i ) ⇒ λs. do {
       check_allm (λa. check (holds s (precondition a))
                                                                      sequence hs is valid from the starting state M to the state M'
4        (ERRS ''Precondition not satisfied'')) A i ;                 and M' entails the goal state specifications.
       check_pairwise (λa b.
6        check (a 6= b −→ acts_non_intrf a b)                            Next the executable refinements for the semantics of tem-
           (ERRS ''Actions in happening interfering'')) A i ;         poral plan validity are described.
8      Error_Monad.return (apply_happ_exec (t i ,A i ) s)}"
                                                                         The following code snippet shows the implementation of
                                                                      the function simplify_plan, which is an executable func-
   The function en_exE combines the execution of a hap-               tion that produces an induced happening sequence.
pening with an enabled-ness check. A happening h is en-
                                                                      Listing 15: Executable Construction of an Induced Happening Sequence
abled in a state if (i) the precondition of every ground action
in the happening h is satisfied in the state M , and (ii) no two           fun insort_happ :: "happening ⇒ happening list ⇒ happening
                                                                                 list" where
ground actions in the happening h are interfering. If a given         2      "insort_happ (t i ,A i ) [] = [(t i ,A i )]"
     | "insort_happ (t i ,A i ) ((tj ,Aj )#hs) =
 4     (if t i < tj then (t i ,A i )#(tj ,Aj )#hs                               Listing 17: Efficient Construction of the Induced Happening Sequence with an AVL-tree
       else if t i = tj then (tj ,A i @ Aj )#hs
                                                                                    fun insert_happ_to_tree :: "happening ⇒ happening tree_ht ⇒
 6     else (tj ,Aj )#(insort_happ (t i ,A i ) hs))"
                                                                                          happening tree_ht" where
                                                                                2     "insert_happ_to_tree (t i ,A i ) hi = avl_node hi (t i ,A i ) hi"
 8   fun insort_mult_happs :: "happening list ⇒ happening list ⇒
                                                                                    | "insert_happ_to_tree (t i ,A i ) hl,((tj ,Aj ),h),ri = (
           happening list" where
                                                                                4     if t i < tj then avl_balL (insert_happ_to_tree (t i ,A i ) l) (t
       "insort_mult_happs [] hs2 = hs2 "
10   | "insort_mult_happs (h#hs1 ) hs2 = insort_happ h (                                     j ,Aj ) r
                                                                                      else if t i = tj then avl_node l (tj ,A i @ Aj ) r
           insort_mult_happs hs1 hs2 )"
                                                                                6     else avl_balR l (tj ,Aj ) (insert_happ_to_tree (t i ,A i ) r))"
12   definition consec_htps_in_interval :: "time list ⇒ time ⇒ time
           ⇒ (time × time) list" where                                          8   fun insert_timed_ground_acts_to_tree :: "(time × ground_action
       "consec_htps_in_interval htps t i tj =                                             ) list ⇒ happening tree_ht ⇒ happening tree_ht" where
14     filter (λ(t,t'). t i ≤ t ∧ t' ≤ tj ) (zip (butlast htps) (tl                   "insert_timed_ground_acts_to_tree [] htree = htree"
                                                                               10   | "insert_timed_ground_acts_to_tree ((ta,a)#as) htree =
             htps))"
                                                                                      insert_happ_to_tree (ta,[a]) (
                                                                                            insert_timed_ground_acts_to_tree as htree)"
16   fun simplify_action :: "time list ⇒ (time × plan_action) ⇒ (
                                                                               12
           time × ground_action) list" where
                                                                                    fun simplify_planE_avl' :: "_ ⇒ (object, type) mapping ⇒ (
       "simplify_action htps (t,Simple_Plan_Action n args) = (
                                                                                          object, rat) mapping ⇒ time list ⇒ plan ⇒ _+happening
18     let a = the (resolve_action_schema n) in
                                                                                          tree_ht" where
         [(t, instantiate_action_schema a args)])"
                                                                               14     "simplify_planE_avl' stg mp mp_fe htps [] = do {
20   | "simplify_action htps (t,Durative_Plan_Action n args d) = (
                                                                                            Error_Monad.return hi }"
       let a = the (resolve_action_schema n) in
                                                                                    | "simplify_planE_avl' stg mp mp_fe htps (π#πs) = do {
22     (t,inst_snap_action a args At_Start) #
                                                                               16     as ← simplify_actionE G mp mp_fe htps π;
       (t+d,inst_snap_action a args At_End) #
                                                                                      htree ← simplify_planE_avl' G mp mp_fe htps πs;
24     (map (λ(t i ,tj ).((t i +tj ) / 2,inst_snap_action a args
                                                                               18     Error_Monad.return (insert_timed_ground_acts_to_tree as
             Over_All)) (consec_htps_in_interval htps t (t+d))))"
                                                                                            htree)}"
26   fun simplify_plan :: "time list ⇒ plan ⇒ happening list" where
                                                                               20   fun simplify_planE_avl :: "_ ⇒ (object, type) mapping ⇒ (
       "simplify_plan htps [] = []"
                                                                                          object, rat) mapping ⇒ time list ⇒ plan ⇒ _+happening
28   | "simplify_plan htps (π#πs) =
                                                                                          list" where
       insort_mult_happs (map (λ(ta,a). (ta,[a])) (simplify_action
                                                                                      "simplify_planE_avl stg mp mp_fe htps πs = do {
              htps π)) (simplify_plan htps πs)"
                                                                               22     htree ← simplify_planE_avl' G mp mp_fe htps πs;
                                                                                      Error_Monad.return (avl_inorder htree)}"

   The function simplify_plan takes two arguments: a
sequence of happening time points and a plan. The se-                             The function simplify_planE_avl' constructs
quence of happening time points is needed to place the in-                     an AVL-tree containing all happenings for the con-
variant snap actions. The invariant snap actions are placed                    structed induced happening sequence. The function
at ti +t2i+1 for two consecutive happening time points                         simplify_planE_avl then simply uses an inorder-
ti and ti+1 . The function simplify_plan is recursive                          traversal (avl_inorder) on the AVL-tree to obtain the
on the given plan. In each recursion step alls snap ac-                        induced happening sequence.
tions for the current plan action (according to Defini-                           The argument stg is the instantiated subtype rela-
tion 8) are inserted into the existing happening sequence                      tion for an implicitly fixed domain and the argument
with the function insort_mult_happs. The function                              mp is a map from object names to types. For a given
insort_mult_happs uses the function insort_happ to                             plan action the function simplify_actionE returns all
inserts multiple happenings into a existing happening se-                      snap actions and checks the well-formedness of the given
quence. The function simplify_action return a list of all                      plan action. The implementations for the efficient type
snap actions for a given plan action (according to Defini-                     checking and its verification are reused from (Abdu-
tion 8). The function consec_htps_in_interval returns                          laziz and Lammich 2018) without any modifications. The
all intervals of consecutive happening time points that lie in                 functions insert_timed_ground_acts_to_tree and
between two given time points.                                                 insert_happ_to_tree are used to insert elements to the
   The following lemma proves the correctness of the func-                     AVL tree.
tion simplify_plan.                                                             Listing 18: Correctnes of the Construction of the Induced Happening Sequence

 Listing 16: Correctnes of the Construction of an Induced Happening Sequence        lemma (in wf_ast_problem)
                                                                                2     assumes "wf_domain"
     lemma (in wf_ast_problem)                                                        and "simplify_planE_avl STG mp_objT mp_Fevl (htps_exec πs)
 2     assumes "wf_plan πs"                                                                πs = Inr hs"
       shows "ind_happ_seq πs (simplify_plan (htps_exec πs) πs)"                4     shows "ind_happ_seq πs hs" and "wf_plan πs"
 4     using assms by (rule simplify_plan_correct)                                    using assms simplify_planE_avl_equiv
                                                                                            simplify_planE_return_iff
                                                                                6     htps_exec_sorted htps_exec_distinct simplify_plan_correct
   The lemma proves, that given a well-formed plan                                    by (auto simp: strict_sorted_iff)

(wf_plan πs) the function simplify_plan constructs an
induced happening sequence for the given plan πs. The                            This lemma proves that if simplify_planE_avl returns
function htps_exec constructs the sequence of happening                        Inr hs then the returned happening sequence hs is an in-
time points for a given plan.                                                  duced happening sequence and the plan πs is well-formed.
                                                                                  Finally, the construction of the induced happen-
Efficiency Refinement of Executable Plan Validator                             ing sequence (simplify_planE_avl) and the im-
The following code snippet shows the more efficient refine-                    plementation for the validity a happening sequence
ment of the function simplify_plan, that uses an AVL-                          (valid_happ_seq_fromE) are combined in the function
tree instead of a list.                                                        check_plan, which gives us the desired validator.
Listing 19: Implementation of Validtor function

     definition "check_plan P πs ≡ do {
2      let stg = ast_domain.STG (ast_problem.domain P);
       let conT = ast_domain.mp_constT (ast_problem.domain P);
4      let mp = ast_problem.mp_objT P;
       let mp_fe = ast_problem.mp_Fevl P;
6      check_wf_problem P stg conT mp;
       hs ← ast_problem.simplify_planE_avl stg mp mp_fe (htps_exec
             πs) πs;
8      ast_problem.valid_happ_seq_fromE 1 (ast_problem.I P) hs
     } <+? (λe. String.implode (e () ''''))"


    The following theorem proves our validator correct.
Listing 20: Correctness of our Validator

     theorem "check_plan P πs = Inr () ←→ ast_problem.wf_problem
           P ∧ ast_problem.valid_plan P πs"
2      by (rule check_plan_return_iff)


  Our validator check_plan only returns Inr () if the
problem is well-formed and the plan is valid.
