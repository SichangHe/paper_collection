                                         Noname manuscript No.
                                         (will be inserted by the editor)




                                         Specification Decomposition for Reactive Synthesis
                                         Bernd Finkbeiner · Gideon Geier · Noemi Passing
arXiv:2103.08459v3 [cs.LO] 16 Dec 2021




                                         Received: date / Accepted: date


                                         Abstract Reactive synthesis is the task of automati-          Keywords Reactive Synthesis · Specification De-
                                         cally deriving a correct implementation from a specifi-       composition · Modular Synthesis · Compositional
                                         cation. It is a promising technique for the development       Synthesis · Preprocessing for Synthesis
                                         of verified programs and hardware. Despite recent ad-
                                         vances in terms of algorithms and tools, however, re-
                                         active synthesis is still not practical when the specified    1 Introduction
                                         systems reach a certain bound in size and complexity.
                                         In this paper, we present a sound and complete modular        Reactive synthesis automatically derives an implemen-
                                         synthesis algorithm that automatically decomposes the         tation that satisfies a given specification. It is a push-
                                         specification into smaller subspecifications. For them,       button method producing implementations which are
                                         independent synthesis tasks are performed, significantly      correct by construction. Therefore, reactive synthesis is
                                         reducing the complexity of the individual tasks. Our          a promising technique for the development of probably
                                         decomposition algorithm guarantees that the subspec-          correct systems since it allows for concentrating on what
                                         ifications are independent in the sense that completely       a system should do instead of how it should be done.
                                         separate synthesis tasks can be performed for them.                Despite recent advances in terms of efficient algo-
                                         Moreover, the composition of the resulting implementa-        rithms and tools, however, reactive synthesis is still not
                                         tions is guaranteed to satisfy the original specification.    practical when the specified systems reach a certain
                                         Our algorithm is a preprocessing technique that can be        bound in size and complexity. It is long known that
                                         applied to a wide range of synthesis tools. We evaluate       the scalability of model checking algorithms can be im-
                                         our approach with state-of-the-art synthesis tools on         proved significantly by using compositional approaches,
                                         established benchmarks: The runtime decreases signifi-        i.e., by breaking down the analysis of a system into
                                         cantly when synthesizing implementations modularly.           several smaller subtasks. [4, 31]. In this paper, we ap-
                                                                                                       ply compositional concepts to reactive synthesis: We
                                         This work was partially supported by the German Research      present and extend a modular synthesis algorithm [12]
                                         Foundation (DFG) as part of the Collaborative Research Cen-
                                         ter “Foundations of Perspicuous Software Systems” (TRR        that decomposes a specification into several subspec-
                                         248 – CPEC, 389792660), and by the European Research          ifications. Then, independent synthesis tasks are per-
                                         Council (ERC) Grant OSARES (No. 683300). The authors          formed for them. The implementations obtained from
                                         thank Alexandre Duret-Lutz for providing valuable feedback    the subtasks are combined into an implementation for
                                         on the algorithm and for bringing up the idea of extending
                                         assumption dropping to non-strict formulas. Moreover, they    the initial specification. The algorithm uses synthesis
                                         thank Marvin Stenger for help with the implementation.        as a black box and can thus be applied to a wide range
                                         B. Finkbeiner and N. Passing
                                                                                                       of synthesis algorithms. In particular, it can be seen as
                                         CISPA Helmholtz Center for Information Security, Germany      a preprocessing step for reactive synthesis that enables
                                         E-mail: finkbeiner@cispa.de, noemi.passing@cispa.de           compositionality for existing algorithms and tools.
                                         G. Geier                                                           Soundness and completeness of modular synthesis
                                         Saarland University, Germany                                  strongly depends on the decomposition of the specifi-
                                         E-mail: geier@react.uni-saarland.de                           cation into subspecifications. We introduce a criterion,
2                                                                                              Bernd Finkbeiner et al.

non-contradictory independent sublanguages, for sub-        tively. For instance, on the generalized buffer bench-
specifications that ensures soundness and completeness:     mark [17, 20] with three receivers, BoSy is able to syn-
The original specification is equirealizable to the sub-    thesize a solution within 28 seconds using modular syn-
specifications and the parallel composition of the im-      thesis while neither the non-compositional version of
plementations for the subspecifications is guaranteed       BoSy, nor the non-compositional version of Strix ter-
to satisfy the original specification. The key question     minates within one hour. For twelve and nine further
is now how to decompose a specification such that the       benchmarks, respectively, BoSy and Strix reduce their
resulting subspecifications satisfy the criterion.          synthesis times significantly, often by an order of magni-
    Lifting the language-based criterion to the automa-     tude or more, when using modular synthesis instead of
ton level, we present a decomposition algorithm for non-    their classical algorithms. The remaining benchmarks
deterministic Büchi automata that directly implements      are too small and too simple for compositional meth-
the independent sublanguages paradigm. Thus, using          ods to pay off. Thus, decomposing the specification into
subspecifications obtained with this decomposition al-      smaller subspecifications indeed increases the scalabil-
gorithm ensures soundness and completeness of mod-          ity of synthesis on larger systems.
ular synthesis. A specification given in the standard            Related Work: Compositional approaches are long
temporal logic LTL can be translated into an equiv-         known to improve the scalability of model checking al-
alent nondeterministic Büchi automaton and hence the       gorithms significantly [4,31]. The approach that is most
decomposition algorithm can be applied as well.             related to our contribution is a preprocessing algorithm
    However, while the decomposition algorithm is se-       for compositional model checking [6]. It analyzes depen-
mantically precise, it utilizes several expensive automa-   dencies between the properties that need to be checked
ton operations. For large specifications, the decomposi-    in order to reduce the number of model checking tasks.
tion thus becomes infeasible. Therefore, we present an      We lift this idea from model checking to reactive synthe-
approximate decomposition algorithm for LTL specifi-        sis. The dependency analysis in our algorithm, however,
cation that still ensures soundness and completeness of     differs inherently from the one for model checking.
modular synthesis but is more scalable. It is approxi-           There exist several compositional approaches for re-
mate in the sense that, in contrast to the automaton        active synthesis. The algorithm by Filiot et al. depends,
decomposition algorithm, it does not necessarily find       like our LTL decomposition approach, heavily on drop-
all possible decompositions. Moreover, we present an        ping assumptions [10]. They use an heuristic that, in
optimization of the LTL decomposition algorithm for         contrast to our criterion, is incomplete. While their ap-
formulas in a common assumption-guarantee format. It        proach is more scalable than a non-compositional one,
analyzes the assumptions and drops those that do not        one does not see as significant differences as for our al-
influence the realizability of the rest of the formula,     gorithm. The algorithm by Kupferman et al. is designed
yielding more fine-grained decompositions. We extend        for incrementally adding requirements to a specification
the optimization from specifications in a strict assume-    during system design [21]. Thus, it does not perform in-
guarantee format to specifications consisting of several    dependent synthesis tasks but only reuses parts of the
conjuncts in assume-guarantee format. This allows for       already existing solutions. In contrast to our algorithm,
applying the optimization to even more of the common        both [21] and [10] do not consider dependencies between
LTL synthesis benchmarks.                                   the components to obtain prior knowledge about the
    We have implemented both decomposition proce-           presence or absence of conflicts in the implementations.
dures as well as the modular synthesis algorithm and             Assume-guarantee synthesis algorithms [2, 3, 14, 23]
used it with the two state-of-the-art synthesis tools       take dependencies between components into account.
BoSy [9] and Strix [25]. We evaluate our algorithms on      In this setting, specifications are not always satisfiable
the established benchmarks from the synthesis compe-        by one component alone. Thus, a negotiation between
tition SYNTCOMP [18]. As expected, the decomposi-           the components is needed. While this yields more fine-
tion algorithm for nondeterministic Büchi automata be-     grained decompositions, it produces a significant over-
comes infeasible when the specifications grow. For the      head that, as our experiments show, is often not nec-
LTL decomposition algorithm, however, the experimen-        essary for common benchmarks. Avoiding negotiation,
tal results are excellent: Decomposition terminates in      dependency-based compositional synthesis [13] decom-
less than 26 milliseconds on all benchmarks. Hence, the     poses the system based on a dependency analysis of the
overhead of LTL decomposition is negligible, even for       specification. The analysis is more fine-grained than the
non-decomposable specifications. Out of 39 decompos-        one presented in this paper. Moreover, a weaker winning
able specifications, BoSy and Strix increase their num-     condition for synthesis, remorsefree dominance [5], is
ber of synthesized benchmarks by nine and five, respec-     used. While this allows for smaller synthesis tasks since
Specification Decomposition for Reactive Synthesis                                                                                3

the specification can be decomposed further, both the              Implementations and Counterstrategies. An implemen-
dependency analysis and using a different winning con-             tation of a system with inputs I, outputs O, and vari-
dition produce a larger overhead than our approach.                ables V = I ∪ O is a function f : (2V )∗ × 2I → 2O
    The reactive synthesis tools Strix [25], Unbeast [8],          mapping a history of variables and the current input
and Safety-First [32] decompose the given specification.           to outputs. An infinite word σ = σ1 σ2 · · · ∈ (2V )ω is
Strix uses decomposition to find suitable automaton                compatible with an implementation f if for all n ∈ N,
types for internal representation and to identify iso-             f (σ1 . . . σn−1 , σn ∩I) = σn ∩O holds. The set of all com-
morphic parts of the specification. Unbeast and Safety-            patible words of f is denoted by C(f ). An implementa-
First in contrast, decompose the specification to iden-            tion f realizes a specification s if σ ∈ L(s) holds for all
tify safety parts. All three tools do not perform indepen-         σ ∈ C(f ). A specification is called realizable if there ex-
dent synthesis tasks for the subspecifications. In fact,           ists an implementation realizing it. If a specification is
our experiments show that the scalability of Strix still           unrealizable, there is a counterstrategy f c : (2V )∗ → 2I
improves notably with our algorithm.                               mapping a history of variables to inputs. An infinite
    Independent of [12], Mavridou et al. introduce a               word σ = σ1 σ2 · · · ∈ (2V )ω is compatible with f c if
compositional realizability analysis of formulas given in          f c (σ1 . . . σn−1 ) = σn ∩ I holds for all n ∈ N. All com-
FRET [16] that is based on similar ideas as our LTL                patible words of f c violate s, i.e., C(f c ) ⊆ L(s).
decomposition algorithm [24]. They only study the re-
alizability of formulas but do not synthesize solutions.           Reactive Synthesis. Given a specification, reactive syn-
Optimized assumption handling cannot easily be in-                 thesis derives an implementation realizing it. For LTL
tegrated into their approach. For a detailed compari-              specifications, synthesis is 2EXPTIME-complete [29].
son of both approaches, we refer to [24]. The first ver-           In this paper, we use reactive synthesis as a black box
sion [12] of our modular synthesis approach is already             procedure and thus we do not go into detail here. In-
well-accepted in the synthesis community: Our LTL de-              stead, we refer the interested reader to [11].
composition algorithm has been integrated into the new
version [30] of the synthesis tool ltlsynt [26].                   Notation. Overloading notation, we use union and in-
                                                                   tersection on infinite words: For σ = σ1 σ2 · · · ∈ (2Σ1 )ω ,
                                                                   σ ′ = σ1′ σ2′ · · · ∈ (2Σ2 )ω with Σ = Σ1 ∪ Σ2 , we define
2 Preliminaries                                                    σ ∪ σ ′ := (σ1 ∪ σ1′ )(σ2 ∪ σ2′ ) · · · ∈ (2Σ )ω . For σ as above
                                                                   and a set X, let σ ∩ X := (σ1 ∩ X)(σ2 ∩ X) · · · ∈ (2X )ω .
LTL. Linear-time temporal logic (LTL) [28] is a speci-
fication language for linear-time properties. For a finite
set Σ of atomic propositions, the syntax of LTL is given           3 Modular Synthesis
by ϕ, ψ ::= a | true | ¬ϕ | ϕ ∨ ψ | ϕ ∧ ψ | ϕ | ϕ U ψ,
where a ∈ Σ. We define the operators ϕ := true U ϕ                 In this section, we introduce a modular synthesis algo-
and ϕ := ¬ ¬ϕ and use standard semantics. The                      rithm that divides the synthesis task into independent
atomic propositions in ϕ are denoted by prop(ϕ), where             subtasks by splitting the specification into several sub-
every occurrence of true or false in ϕ does not add any            specifications. The decomposition algorithm has to en-
atomic propositions to prop(ϕ). The language L(ϕ) of ϕ             sure that the synthesis tasks for the subspecifications
is the set of infinite words that satisfy ϕ.                       can be solved independently and that their results are
                                                                   non-contradictory, i.e., that they can be combined into
Automata. For a finite alphabet Σ, a nondeterministic              an implementation satisfying the initial specification.
Büchi automaton (NBA) is a tuple A = (Q, Q0 , δ, F ),             Note that when splitting the specification, we assign a
where Q is a finite set of states, Q0 ⊆ Q is a set of              set of relevant in- and output variables to every sub-
initial states, δ : Q × Σ × Q is a transition relation, and        specification. The corresponding synthesis subtask is
F ⊆ Q is a set of accepting states. Given an infinite              then performed on these variables.
word σ = σ1 σ2 · · · ∈ Σ ω , a run of σ on A is an infinite            Algorithm 1 describes this modular synthesis ap-
sequence q1 q2 q3 · · · ∈ Qω of states where q1 ∈ Q0 and           proach. First, the specification is decomposed into a list
(qi , σi , qi+1 ) ∈ δ holds for all i ≥ 1. A run is accepting if   of subspecifications using an adequate decomposition
it contains infinitely many accepting states. A accepts            algorithm. Then, the synthesis tasks for all subspecifi-
a word σ if there is an accepting run of σ on A. The               cations are solved. If a subspecification is unrealizable,
language L(A) of A is the set of all accepted words.               its counterstrategy is extended to a counterstrategy for
Two NBAs are equivalent if their languages are. An                 the whole specification. This construction is given in
LTL specification ϕ can be translated into an equivalent           Definition 3.1. Otherwise, the implementations of the
NBA Aϕ with a single exponential blow up [22].                     subspecifications are composed.
4                                                                                                     Bernd Finkbeiner et al.


    Algorithm 1: Modular Synthesis                                    Soundness and completeness of modular synthesis
        Input: s: Specification, inp: List Variable, out: List   depend on three requirements: Equirealizability of the
               Variable                                          initial specification and the subspecifications, non-con-
      Output: realizable: Bool, implementation: T                tradictory composability of the subresults, and satisfac-
    1 subspecifications ← decompose(s, inp, out)
                                                                 tion of the initial specification by the parallel compo-
    2 sub results ← map synthesize subspecifications
    3 foreach (real,strat) ∈ sub results do
                                                                 sition of the subresults. Intuitively, these requirements
    4     if ! real then                                         are met if the decomposition algorithm neither intro-
    5          impl ← extendCounterStrategy(strat, s)            duces nor drops parts of the system specification and
    6          return (⊥, impl)
                                                                 if it does not produce subspecifications that allow for
    7   impls ← map second sub results                           contradictory implementations. To obtain composabil-
    8   return (⊤, compose impls)                                ity of the subresults, the implementations need to agree
                                                                 on shared variables. We ensure this by assigning dis-
                                                                 joint sets of output variables to the synthesis subtasks:
    Intuitively, the behavior of the counterstrategy of an       Since every subresult only defines the behavior of the
unrealizable subspecification si violates the full speci-        assigned output variables, the implementations are non-
fication s as well. A counterstrategy for the full spec-         contradictory. Since the language alphabets of the sub-
ification, however, needs to be defined on all variables         specifications thus differ, the composition of their lan-
of s, i.e., also on the variables that do not occur in si .      guages is non-contradictory:
Thus, we extend the counterstrategy for ϕi such that it
ignores outputs outside of si and produces an arbitrary          Definition 3.2 (Language Composition) Let L1 ,
valuation of the input variables outside of si :                 L2 be languages over 2Σ1 and 2Σ2 , respectively. The
                                                                 non-contradictory composition of L1 and L2 is given by
Definition 3.1 (Counterstrategy Extension) Let                   L1 || L2 = {σ1 ∪σ2 | σ1 ∈ L1 ∧σ2 ∈ L2 ∧σ1 ∩Σ2 = σ2 ∩Σ1 }.
s be a specification with L(s) ⊆ (2V )ω . Let V1 , V2 ⊂ V
with V1 ∪V2 = V and V1 ∩V2 ⊆ I. Let s1 , s2 be subspec-             The satisfaction of the initial specification by the
ifications of s with L(s1 ) ⊆ (2V1 )ω , L(s2 ) ⊆ (2V2 )ω such    composed subresults can be guaranteed by requiring
that L(s1 ) || L(s1 ) = L(s). Let s1 be unrealizable and         the subspecifications to be independent sublanguages:
let f1c : (2V1 )∗ → 2I∩V1 be a counterstrategy for s1 . We
construct a counterstrategy f c : (2V )∗ → 2I from f1c           Definition 3.3 (Independent Sublanguages) Let
for s: f c (σ) = f1c (σ ∩ V1 ) ∪ µ, where µ ∈ 2I\V1 is an        L ⊆ (2Σ )ω , L1 ⊆ (2Σ1 )ω , and L2 ⊆ (2Σ2 )ω be languages
arbitrary valuation of the input variables outside of V1 .       with Σ1 , Σ2 ⊆ Σ and Σ1 ∪ Σ2 = Σ. Then, L1 and L2
                                                                 are independent sublanguages of L if L1 || L2 = L holds.
    The counterstrategy for the full specification con-
structed as in Definition 3.1 then indeed fulfills the con-          From these two requirements, i.e., the subspecifica-
dition of a counterstrategy for the full specification, i.e.,    tions form non-contradictory and independent sublan-
all of its compatible words violate the full specification:      guages, equirealizability of the initial specification and
                                                                 the subspecifications follows:
Lemma 3.1 Let s be a specification with L(s) ⊆ (2V )ω.
Let V1 , V2 ⊂ V with V1 ∪ V2 = V , V1 ∩ V2 ⊆ I. Let s1 , s2      Theorem 3.1 Let s, s1 , and s2 be specifications with
be specifications with L(s1 ) ⊆ (2V1 )ω , L(s2 ) ⊆ (2V2 )ω       L(s) ⊆ (2V )ω , L(s1 ) ⊆ (2V1 )ω , L(s2 ) ⊆ (2V2 )ω . Recall
and L(s1 ) || L(s1 ) = L(s). Let f1c : (2V1 )∗ → 2I∩V1 be a      that I ⊆ V is the set of input variables. If V1 ∩ V2 ⊆ I
counterstrategy for s1 . The function f c constructed as         and V1 ∪V2 = V hold, and L(s1 ) and L(s2 ) are indepen-
in Definition 3.1 from fic is a counterstrategy for s.           dent sublanguages of L(s), then s is realizable if, and
                                                                 only if, both s1 and s2 are realizable.
Proof Let σ ∈ C(f c ). Then f c (σ1 . . . σn−1 ) = σn ∩ I
for all n ∈ N and hence, by construction of f c , we have        Proof First, suppose that s1 and s2 are realizable. Let
f1c (σ1 . . . σn−1 ∩V1 ) = σn ∩(I ∩V1 ). Thus, σ∩V1 ∈ C(f1c )    f1 : (2V1 )∗ ×2I∩V1 → 2O∩V1 , f2 : (2V2 )∗ ×2I∩V2 → 2O∩V2
follows. Since f1c is a counterstrategy for s1 , we have         be implementations realizing s1 and s2 , respectively. We
C(f1c ) ⊆ L(s1 ). Hence, σ ∩ V1 ∈ L(s1 ). By assumption,         construct an implementation f : (2V )∗ × 2I → 2O from
L(s1 ) || L(s2 ) = L(s) and thus (σ ∩ V1 ) ∪ σ ′ 6∈ L(s)         f1 and f2 : f (σ, i) := f1 (σ ∩V1 , i∩V1 )∪f2 (σ ∩V2 , i∩V2 ).
for any infinite word σ ′ ∈ (2V2 )ω . Thus, in particular,       Let σ ∈ C(f ). Hence, f ((σ1 . . . σn−1 ), σn ∩ I) = σn ∩ O
(σ ∩ V1 ) ∪ (σ ∩ V2 ) 6∈ L(s) holds. Since V1 ∪ V2 = V ,         for all n ∈ N. Let σ ′ ∈ (2V1 )ω , σ ′′ ∈ (2V2 )ω be sequences
(σ ∩ V1 ) ∪ (σ ∩ V2 ) = σ follows. Thus, σ ∈  / L(s). Hence,     with σn′ ∩ O = f1 ((σ1 . . . σn−1 ∩ V1 ), σn ∩ (I ∩ V1 )) and
for all σ ∈ C(f ), σ 6∈ L(s) and thus C(f c ) ⊆ L(s).
                    c
                                                                 σn′′ ∩ O = f2 ((σ1 . . . σn−1 ∩ V2 ), σn ∩ (I ∩ V2 )), respec-
Thereforde, f c is a counterstrategy for s.               ⊓
                                                          ⊔      tively, for all n ∈ N. Then, σn′ ∪ σn′′ = σn ∩ O for all
Specification Decomposition for Reactive Synthesis                                                                                   5

n ∈ N follows by construction of f and thus σ = σ ′ ∪ σ ′′       we consider their composition instead of the composi-
holds. Further, σ ′ ∈ C(f1 ) and σ ′′ ∈ C(f2 ) and thus,         tion of their languages: Let A1 = (Q1 , Q10 , δ1 , F1 ) and
since s1 and s2 are realizable by assumption, σ ′ ∈ L(s1 )       A2 = (Q2 , Q20 , δ2 , F2 ) be NBAs over 2V1 , 2V2 , respec-
and σ ′′ ∈ L(s2 ). Since L(s1 ) and L(s2 ) are indepen-          tively. The parallel composition of A1 and A2 is defined
dent sublanguages by assumption, L(s1 ) || L(s2 ) = L(s)         by the NBA A1 || A2 = (Q, Q0 , δ, F ) over 2V1 ∪V2 with
holds. Hence, by definition of language composition,             Q = Q1 × Q2 , Q0 = Q10 × Q20 , ((q1 , q2 ), i, (q1′ , q2′ )) ∈ δ if,
σ1 ∪ σ2 ∈ L(s) follows and thus, σ ∈ L(s) holds. Hence,          and only if, (q1 , i ∩ V1 , q1′ ) ∈ δ1 and (q2 , i ∩ V2 , q2′ ) ∈ δ2 ,
for all σ ∈ C(f ), σ ∈ L(s) and therefore f realizes s.          and F = F1 × F2 . The parallel composition of NBAs
    Second, let si is unrealizable for some i ∈ {1, 2} and       reflects the composition of their languages:
let fic : (2V )∗ → 2I∩V1 be a counterstrategy for si . We
                                                                 Lemma 4.1 Let A1 and A2 be NBAs over alphabets
construct a counterstrategy f c : (2V )∗ → 2I from fic
                                                                 2V1 and 2V2. Then, L(A1 || A2 ) = L(A1 ) || L(A2 ) holds.
as described in Definition 3.1. By Lemma 3.1, f c is a
counterstrategy for s. Thus, s is unrealizable.          ⊓
                                                         ⊔       Proof First, let σ ∈ L(A1 || A2 ). Then, σ is accepted
                                                                 by A1 || A2 . Hence, by definition of automaton compo-
    The soundness and completeness of Algorithm 1                sition, for i ∈ {1, 2}, σ ∩ Vi is accepted by Ai . Thus,
for adequate decomposition algorithms now follows di-            σ ∩ Vi ∈ L(Ai ). Since (σ ∩ V1 ) ∩ V2 = (σ ∩ V2 ) ∩ V1 ,
rectly with Theorem 3.1 and the properties of such algo-         we have (σ ∩ V1 ) ∪ (σ ∩ V2 ) ∈ L(A1 ) || L(A2 ). By defini-
rithms described above: They produce subspecifications           tion of automaton composition, σ ∈ (2V1 ∪V2 )ω and thus
that (1) do not share output variables and that (2) form         σ = (σ ∩ V1 ) ∪ (σ ∩ V2 ). Hence, σ ∈ L(A1 ) || L(A2 ).
independent sublanguages of the initial specification.               Next, let σ ∈ L(A1 ) || L(A2 ). Then, for σ1 ∈ (2V1 )ω ,
Theorem 3.2 Let s be a specification. Moreover, let              σ2 ∈ (2V2 )ω with σ = σ1 ∪ σ2 , we have σi ∈ L(Ai ) for
S = {s1 , . . . , sk } be a setSof subspecifications of s with   i ∈ {1, 2} and σ1 ∩ V2 = σ2 ∩ V1 . Hence, σi is accepted
L(si ) ⊆ (2Vi )ω such that 1≤i≤k Vi = V , Vi ∩Vj ⊆ I for         by Ai . Thus, by definition of automaton composition
1 ≤ i, j ≤ k with i 6= j, and such that L(s1 ), . . . , L(sk )   and since σ1 and σ2 agree on shared variables, σ1 ∪ σ2
are independent sublanguages of L(s). If s is realizable,        is accepted by A1 || A2 . Thus, σ1 ∪ σ2 ∈ L(A1 || A2 ) and
Algorithm 1 yields an implementation realizing s. Oth-           hence σ ∈ L(A1 || A2 ) holds.                             ⊓
                                                                                                                           ⊔
erwise, Algorithm 1 yields a counterstrategy for s.                  Using the above lemma, we can formalize the inde-
Proof First, let s be realizable. Then, by applying The-         pendent sublanguage criterion on NBAs directly: Two
orem 3.1 recursively, it follows that si is realizable for       automata A1 , A2 are independent subautomata of A if
all si ∈ S. Since Vi ∩Vj ⊆ I holds for any si , sj ∈ S with      A = A1 || A2 . To apply Theorem 3.1, the alphabets of
i 6= j, the implementations realizing s1 , . . . , sk are non-   the subautomata may not share output variables. Our
contradictory. Hence, Algorithm 1 returns their compo-           decomposition algorithm achieves this by constructing
sition: Implementation f . Since V1 ∪ · · · ∪ Vk = V , f de-     the subautomata from the initial automaton by pro-
fines the behavior of all outputs. By construction, f re-        jecting to disjoint sets of outputs. Intuitively, the pro-
alizes all si ∈ S. Since the L(si ) are non-contradictory,       jection to a set X abstracts from the variables out-
independent sublanguages of L(s), f thus realizes s.             side of X. Hence, it only captures the parts of the ini-
    Next, let s be unrealizable. Then, by applying The-          tial specification concerning the variables in X. For-
orem 3.1 recursively, si is unrealizable for some si ∈ S.        mally: Let A = (Q, Q0 , δ, F ) be an NBA over alpha-
Thus, Algorithm 1 returns the extension of si ’s counter-        bet 2V and let X ⊂ V . The projection of A to X
strategy to a counterstrategy for the full specification.        is the NBA Aπ(X) = (Q, Q0 , πX (δ), F ) over 2X with
Its correctness follows with Lemma 3.1.                     ⊓
                                                            ⊔    πX (δ) = {(q, a, q ′ ) | ∃ b ∈ 2V \X . (q, a ∪ b, q ′ ) ∈ δ}.
                                                                     The decomposition algorithm for NBAs is described
                                                                 in Algorithm 2. It is a recursive algorithm that, starting
4 Decomposition of Büchi Automata                               with the initial automaton A, guesses a subset X of the
                                                                 output variables out. It abstracts from the output vari-
To ensure soundness and completeness of modular syn-             ables outside of X by building the projection AX of A to
thesis, a specification decomposition algorithm needs to         X∪inp, where inp is the set of input variables. Similarly,
meet the language-based adequacy conditions of The-              it builds the projection AY of A to Y := (out \ X) ∪ inp.
orem 3.1. In this section, we lift these conditions from         By construction of AX and AY and since both X ∩ Y = ∅
the language level to nondeterministic Büchi automata           and X ∪ Y = out hold, we have L(A) ⊆ L(AX || AY ).
and present a decomposition algorithm for specifica-             Hence, if L(AX || AY ) ⊆ L(A) holds, then AX || AY is
tions given as NBAs on this basis. Since the algorithm           equivalent to A and therefore L(AX ) and L(AY ) are in-
works directly on NBAs and not on their languages,               dependent sublanguages of L(A). Thus, since X and Y
6                                                                                                                            Bernd Finkbeiner et al.


    Algorithm 2: Automaton Decomposition                                                                         q0    (¬
                                                                                                                            i∧
        Input: A: NBA, inp: List Variable, out: List Variable                                                                    ¬o
        Output: subautomata: List (NBA, List Variable, List
                                                                                                                                   1   )∨
                                                                                       ¬o1      ¬o1                                         (¬         ¬i ∨ o2
                                                                                                                                             o1




                                                                                                                       i∧
                  Variable)                                                                                                                       ∧o




                                                                                                                        ¬o 1
    1   if isNull checkedSubsets then                                                                                                              2)
    2        checkedSubsets ← ∅                                                                             o1




                                                                                                                             ∧¬
                                                                                        q1                                                                q3
   subautomata ← [(A, inp, out)]




                                                                                                                               o2
    3
                                                                                                o1                                           o2
 4 foreach X ⊂ out do
       Y ← out\X                                                                                                                                          2
                                                                                                                                                       ¬o
 5
 6     if X 6∈ checkedSubsets ∧ Y 6∈ checkedSubsets then                                              q2    ⊤         ¬o2              q4         i∧
 7         AX ← Aπ(X∪inp)
 8         AY ← Aπ(Y∪inp)
 9         if L(AX || AY ) ⊆ L(A) then                                               Fig. 4.3: NBA A′ for ϕ′ = o1 ∨ (i → o2 ). Accept-
10              subautomata ← decompose(AX , inp, X)                                 ing states are marked with double circles.
                 ++ decompose(AY , inp, Y)
11                     break

12         checkedSubsets ← checkedSubsets ∪ {X, Y}                                  ϕ = o1 ∧ (i → o2 ) for inputs I = {i} and out-
13      return subautomata                                                           puts O = {o1 , o2 }. The NBA A that accepts L(ϕ) is
                                                                                     depicted in Figure 4.1. The (minimized) subautomata
                                                                                     obtained with Algorithm 2 are shown in Figures 4.2a
                                                        (¬i ∧ ¬o1 )
                                               q0                                    and 4.2b. Clearly, V1 ∩ V2 ⊆ I holds. Moreover, their
                                                        ∨ (¬o1 ∧ o2 )
                                  o2                                                 parallel composition is exactly A depicted in Figure 4.1
                                 ¬
                             ∧                                                       and therefore their parallel composition accepts exactly
                                                                 i∧




                        o1                      (¬i ∧ o1 )
                       ¬                                                             those words that satisfy ϕ. For a slightly modified spec-
                                                                   o1




                  i∧                            ∨ (o1 ∧ o2 )
                                       o2




                                                                      ∧




                                                                                     ification ϕ′ = o1 ∨ (i → o2 ), however, Algorithm 2
                                  ∧




                                                                        ¬o
                              o1




                                                          i∧¬
                                                                                     does not decompose the NBA A′ with L(A′ ) = L(ϕ′ )
                                                                           2




                                                             o2
                             ¬




                                               q2
                                                                                     depicted in Figure 4.3: The only possible decomposition
                                       o2
             q1              o1 ∧                                              q3    is X = {o1 }, Y = {o2 } (or vice-versa), yielding NBAs
                                                          o2
                                            ¬i ∨ o2                                  A′X and A′Y that accept every infinite word. Clearly,
         ¬o1 ∧ ¬o2                          o1 ∧ ¬o2                       ¬o2       L(A′X || A′Y ) 6⊆ L(A′ ) since L(A′X || A′Y ) = (2I∪O )ω and
                                                                                     hence A′X and A′Y are no valid decomposition.
Fig. 4.1: NBA A for ϕ = o1 ∧ (i →                                o2 ). Accepting         Algorithm 2 ensures soundness and completeness of
states are marked with double circles.                                               modular synthesis: The subspecifications do not share
                                                                                     output variables and they are equirealizable to the ini-
           ¬o1                         ⊤               ¬i ∨ o2                 ¬o2   tial specification. This follows from the construction of
                                                                 i ∧ ¬o2
                                                                                     the subautomata, Lemma 4.1, and Theorem 3.1:
                     o1
           q0                       q1                   q0                     q1
                                                                                     Theorem 4.1 Let A be an NBA over alphabet 2V . Al-
                                                                   o2
                                                                                     gorithm 2 terminates on A with a set S = {A1 , . . . , Ak }
(a) Minimization of Aπ(V1 ) .                   (b) Minimization of Aπ(V2 ) .
                                                                                     of NBAs with L(Ai ) ⊆ (2Vi )ω , whereS Vi ∩ Vj ⊆ I for
Fig. 4.2: Minimized NBAs for the projections Aπ(V1 )                                 1 ≤ i, j ≤ k with i 6= j, V = 1≤i≤k Vi , and A is
and Aπ(V2 ) of the NBA A from Figure 4.1 to the sets                                 realizable if, and only if, Ai is realizable for all Ai ∈ S.
of variables V1 = {i, o1 } and V2 = {i, o2 }, respectively.
Accepting states are marked with double circles.                                     Proof Clearly, there are NBAs that cannot be decom-
                                                                                     posed further, e.g., automata whose alphabet contains
                                                                                     only one output variable. Thus, since there are only
are disjoint and therefore AX and AY do not share out-                               finitely many subsets of O, Algorithm 2 terminates.
put variables, AX and AY are a valid decomposition                                       We show that the algorithm returns subspecifica-
of A. The subautomata are then decomposed recur-                                     tions that only share input variables, define all output
sively. If no further decomposition is possible, the al-                             variables of the system, and that are independent sub-
gorithm returns the subautomata. By only considering                                 languages of the initial specification by structural in-
unexplored subsets of output variables, no subset com-                               duction on the initial automaton:
bination X, Y is checked twice.                                                          For any automaton A′ that is not further decompos-
    As an example for the specification decomposition                                able, Algorithm 2 returns a list S ′ solely containing A′ .
algorithm based on NBAs, consider the specification                                  Clearly, the parallel composition of all automata in S ′
Specification Decomposition for Reactive Synthesis                                                                       7

is equivalent to A′ and the alphabets of the languages          5 Decomposition of LTL Formulas
of the subautomata do not share output variables.
    Next, let A′ be an NBA such that there exists a set         An LTL specification can be decomposed by translat-
X ⊂ out with L(A′π(X∪inp) || A′π(Y∪inp) ) ⊆ L(A′ ), where       ing it into an equivalent NBA and by then applying
Y = out \ X. By construction of A′π(X∪inp) and A′π(Y∪inp) ,     Algorithm 2. To circumvent expensive automaton oper-
we have (A′ ∩ (Z ∪ inp)) ⊆ A′π(Z∪inp) for Z ∈ {X, Y}.           ations, though, we introduce an approximate decompo-
Since both X ∩ Y = ∅ and X ∪ Y = out hold by construc-          sition algorithm that, in contrast to Algorithm 2, does
tion of X and Y, (X ∪ inp) ∩ (Y ∪ inp) ⊆ inp as well            not necessarily find all possible decompositions. In the
as (X ∪ inp) ∪ (Y ∪ inp) = inp ∪ out follows. There-            following, we assume that V = prop(ϕ) holds for the
fore, L(A) ⊆ L(A′π(X∪inp) || A′π(Y∪inp) ) holds and thus,       initial specification ϕ. Note that any implementation
A′π(X∪inp) || A′π(Y∪inp) ≡ A′ follows. By induction hy-         for the variables in prop(ϕ) can easily be extended to
pothesis, the calls to the algorithm with A′π(X∪inp) and        one for the variables in V if prop(ϕ) ⊂ V holds by ignor-
A′π(Y∪inp) return lists SX′ and SY′ , respectively, where the   ing the inputs in I \ prop(ϕ) and by choosing arbitrary
parallel composition of all automata in SZ′ is equivalent       valuations for the outputs in O \ prop(ϕ).
to A′π(Z∪inp) for Z ∈ {X, Y}. Thus, the parallel composi-           The main idea of the decomposition algorithm is
tion of all automata in the concatenation of SX′ and SY′        to rewrite the initial LTL formula ϕ into a conjunctive
is equivalent to A′π(X∪inp) || A′π(Y∪inp) and thus, by con-     form ϕ = ϕ1 ∧· · · ∧ϕk with as many top-level conjuncts
struction of X, to A′ . Hence, their languages are inde-        as possible by applying distributivity and pushing tem-
pendent sublanguages of A′ . Furthermore, by induction          poral operators inwards whenever possible. Then, we
hypothesis, the alphabets of the automata in SZ′ do not         build subspecifications ϕi consisting of subsets of the
share output variables for Z ∈ {X, Y} and, by construc-         conjuncts. Each conjunct occurs in exactly one sub-
tion, they are subsets of the alphabet of A′π(Z) . Hence,       specification. We say that conjuncts are independent
since clearly (X ∪ inp) ∩ ((out \ X) ∪ inp) ⊆ inp holds,        if they do not share output variables. Given an LTL
the alphabets of the automata in the concatenation of           formula with two independent conjuncts, the languages
SX′ and SY′ do not share output variables. Moreover, the        of the conjuncts are independent sublanguages of the
union of the alphabets of the automata in SZ′ equals            language of the whole formula:
the alphabet of Aπ(Z∪inp) for Z ∈ {X, Y} by induction           Lemma 5.1 Let ϕ = ϕ1 ∧ ϕ2 be an LTL formula over
hypothesis. Since clearly X ∪ Y = out, it follows that          atomic propositions V with conjuncts ϕ1 and ϕ2 over
the union of the alphabets of the automata in the con-          V1 and V2 , respectively, with V1 ∪ V2 ⊆ V . Then, L(ϕ1 )
catenationSof SX′ and SY′ equals inp ∪ out.                     and L(ϕ2 ) are independent sublanguages of L(ϕ).
    Thus, 1≤i≤k Vi = V and Vi ∩Vj ⊆ I for 1 ≤ i, j ≤ k
with i 6= j. Moreover, L(A1 ), . . . , L(Ak ) are indepen-      Proof First, let σ ∈ L(ϕ). Then, σ ∈ L(ϕi ) holds for
dent sublanguages of L(A). Thus, by Theorem 3.1, A              all i ∈ {1, 2}. Since prop(ϕi ) ⊆ Vi holds and since the
is realizable if, and only if, all Ai ∈ S are realizable. ⊓ ⊔   satisfaction of ϕi only depends on the valuations of the
                                                                variables in prop(ϕi ), we have σ ∩ Vi ∈ L(ϕi ). Since
   Since Algorithm 2 is called recursively on every sub-        clearly (σ ∩ V1 ) ∩ V2 = (σ ∩ V2 ) ∩ V1 holds, we have
automaton obtained by projection, it directly follows           (σ ∩ V1 ) ∪ (σ ∩ V2 ) ∈ L(ϕ1 ) || L(ϕ2 ). Since V1 ∪ V2 = V
that the nondeterministic Büchi automata contained in          holds by assumption, we have σ = (σ ∩ V1 ) ∪ (σ ∩ V2 )
the returned list are not further decomposable:                 and hence σ ∈ L(ϕ1 ) || L(ϕ2 ) follows.
Theorem 4.2 Let A be an NBA and let S be the set                    Next, let σ ∈ L(ϕ1 ) || L(ϕ2 ). Then, there are words
of NBAs that Algorithm 2 returns on input A. Then,              σ1 ∈ L(ϕ1 ), σ2 ∈ L(ϕ2 ) with σ1 ∩ V2 = σ2 ∩ V1 and
for each Ai ∈ S over alphabet 2Vi , there are no NBAs           σ = σ1 ∪ σ2 . Since σ1 and σ2 agree on shared variables,
                          ′       ′′
A′ , A′′ over alphabets 2V and 2V with Vi = V ′ ∪ V ′′          σ ∈ L(ϕ1 ) and σ ∈ L(ϕ2 ). Hence, σ ∈ L(ϕ1 ∧ ϕ2 ). ⊓      ⊔
such that Ai = A′ || A′′ holds.                                     Our decomposition algorithm then ensures that dif-
                                                                ferent subspecifications share only input variables by
    Hence, Algorithm 2 yields perfect decompositions
                                                                merging conjuncts that share output variables into the
and is semantically precise. Yet, it performs several ex-
                                                                same subspecification. Then, equirealizability of the ini-
pensive automaton operations such as projection, com-
                                                                tial formula and the subformulas follows directly from
position, and language containment checks. For large
                                                                Theorem 3.1 and Lemma 5.1:
automata, this is infeasible. For specifications given as
LTL formulas, we thus present an approximate decom-             Corollary 5.1 Let ϕ = ϕ1 ∧ ϕ2 be an LTL formula
position algorithm in the next section that does not            over V with conjuncts ϕ1 , ϕ2 over V1 , V2 , respectively,
yield non-decomposable subspecifications, but that is           with V1 ∪ V2 = V and V1 ∩ V2 ⊆ I. Then, ϕ is realizable
free of the expensive automaton operations.                     if, and only if, both ϕ1 and ϕ2 are realizable.
8                                                                                                   Bernd Finkbeiner et al.


    Algorithm 3: LTL Decomposition                              occurring in ϕi to the subspecification ϕi . While re-
        Input: ϕ: LTL, inp: List Variable, out: List Variable   stricting the inputs is not necessary for correctness, it
        Output: specs: List (LTL, List Variable, List           may improve the runtime of the synthesis task.
                 Variable)                                          As an example for the decomposition of LTL for-
   ϕ ← rewrite(ϕ)
    1
                                                                mulas, consider the specification ϕ = o1 ∧ (i → o2 )
 2 formulas ← removeTopLevelConjunction(ϕ)
 3 graph ← buildDependencyGraph(ϕ, out)
                                                                with I = {i} and O = {o1 , o2 } again. Since ϕ is already
 4 components ← graph.connectedComponents()                     in conjunctive form, no rewriting has to be performed.
 5 specs ← new LTL[|components|+1] // initialized               The two conjuncts of ϕ do not share any variables and
      with true
                                                                therefore the dependency graph Dϕ does not contain
 6 foreach ψ ∈ formulas do
 7     propositions ← getProps(ψ)                               any edges. Therefore, we obtain two subspecifications
 8     foreach (spec,set) ∈ zip specs (components ++            ϕ1 = o1 and ϕ2 = (i → o2 ).
        [inp]) do                                                   Soundness and completeness of modular synthesis
 9         if propositions ∩ set =
                                 6 ∅ then
                                                                with Algorithm 3 as a decomposition algorithm for LTL
10             spec.And(ψ)
11                 break                                        formulas follows directly from Corollary 5.1 if the sub-
                                                                specifications do not share any output variables:
12      return map (λϕ → (ϕ, inputs(ϕ), outputs(ϕ))) specs
                                                                Theorem 5.1 Let ϕ be an LTL formula over V . Then,
                                                                Algorithm 3 terminates with a set S = {ϕ1 , . . . , ϕk }
                                                                of LTL formulas on ϕ with L(ϕi ) ∈ (2Vi )ω such that
                                                                                                          S
     To determine which conjuncts of an LTL formula             Vi ∩ Vj ⊆ I for 1 ≤ i, j ≤ k with i 6= j, 1≤i≤k Vi = V ,
ϕ = ϕ1 ∧ · · · ∧ ϕn share variables, we build the depen-        and such that ϕ is realizable, if, and only if, for all
dency graph Dϕ = (V, E) of the output variables, where          subspecifications ϕi ∈ S, ϕi is realizable.
V = O and (a, b) ∈ E if, and only if, a ∈ prop(ϕi ) and
b ∈ prop(ϕi ) for some 1 ≤ i ≤ n. Intuitively, outputs a        Proof Since an output variable is part of exactly one
and b that are contained in the same connected com-             connected component and since all conjuncts contain-
ponent of Dϕ depend on each other in the sense that             ing an output are contained in the same subspecifica-
they either occur in the same conjunct or that they oc-         tion, every output is part of exactly one subspecifica-
cur in conjuncts that are connected by other output             tion. Therefore, Vi ∩ Vj ⊆ I holds for 1 ≤ i, j ≤ k with
variables. Hence, to ensure that subspecifications do           i 6= j. Moreover, the last component added in Line 8
not share output variables, conjuncts containing a or b         contains all inputs. Hence, all variables that occur in a
                                                                conjunct of ϕ are featured in at least one subspecifica-
need to be assigned to the same subspecification. Out-                       S
                                                                tion. Thus, 1≤i≤k Vi = prop(ϕ) holds and hence, since
put variables that are contained in different connected                                         S
components, however, are not linked and therefore im-           V = prop(ϕ) by assumption, 1≤i≤k Vi = V follows.
plementations for their requirements can be synthesized         Therefore, equirealizability of ϕ and the formulas in S
independently, i.e., with independent subspecifications.        directly follows with Corollary 5.1.                   ⊓
                                                                                                                       ⊔
     Algorithm 3 describes how an LTL formula is de-                While Algorithm 3 is simple and ensures soundness
composed into subspecifications. First, the formula is          and completeness of modular synthesis, it strongly de-
rewritten into conjunctive form. Then, the dependency           pends on the structure of the formula: When rewrit-
graph is built and the connected components are com-            ing formulas in assume-guarantee format, i.e., formulas
                                                                                    Vm           Vn
puted. For each connected component as well as for              of the form ϕ = i=1 ϕi → j=1 ψj , to a conjunc-
all input variables, a subspecification is built by adding      tive form, the conjuncts contain both assumptions ϕi
the conjuncts containing variables of the respective con-       and guarantees ψj . Hence, if a, b ∈ O occur in assump-
nected component or an input variable, respectively.            tion ϕi and guarantee ψj , respectively, they are depen-
To also consider the input variables is necessary to as-        dent. Thus, all conjuncts featuring a or b are contained
sign every conjunct, including input-only ones, to at           in the same subspecification according to Algorithm 3.
least one subspecification. By construction, no conjunct        Yet, ψj might be realizable even without ϕi . An algo-
is added to the subspecifications of two different con-         rithm accounting for this might yield further decompo-
nected components. Yet, a conjunct could be added to            sitions and thus smaller synthesis subtasks.
both a subspecification of a connected component and                In the following, we present a criterion for dropping
the subspecification for the input-only conjuncts. This         assumptions while maintaining equirealizability. Intu-
is circumvented by the break in Line 11. Hence, every           itively, we can drop an assumption ϕ for a guarantee ψ if
conjunct is added to exactly one subspecification. To           they do not share any variable. However, if ϕ can be vi-
define the input and output variables for the synthesis         olated by the system, i.e., if ¬ϕ is realizable, equirealiz-
subtasks, the algorithm assigns the inputs and outputs          ability is not guaranteed when dropping ϕ. For instance,
Specification Decomposition for Reactive Synthesis                                                                                9

consider the formula ϕ = (i1 ∧ o1 ) → (i2 ∧ o2 ),                  with c = f2c (τ ∩prop(ϕ2 )). We construct an implementa-
where I = {i1 , i2 } and O = {o1 , o2 }. Although as-              tion g : (2V1 )∗ × 2I1 → 2O1 based on f and η̂ as follows:
sumption and guarantee do not share any variables,                 g(η, i) := f (η̂, i ∪ (f2c (η̂) ∩ I)) ∩ O1 . Let σ ∈ C(g). Let σf
the assumption cannot be dropped: An implementation                be the corresponding infinite sequence obtained from
that never sets o1 to true satisfies ϕ but (i2 ∧ o2 ) is           g when not restricting the output of f to O1 . Hence,
not realizable. Furthermore, dependencies between in-              σf ∩ V1 = σ. Clearly, by construction of g, we have
put variables may yield unrealizability if an assumption           σf ∈ C(f ) and hence, since f realizes ϕ by assumption,
is dropped as information about the remaining inputs               σf ∈ L(ϕ). Furthermore, we have σf ∈ L(ϕ2 ) by con-
might get lost. For instance, in the formula ϕ → ψ with            struction of g since η̂ forces f to satisfy ϕ2 . Hence,
ϕ = ( i1 → i2 )∧(¬ i1 → i3 )∧(i2 ↔ i4 )∧(i3 ↔ ¬i4 ) and            σf ∈ L(ϕ1 → ψ). Since ϕ2 neither shares variables
ψ = i1 ↔ o, where I = {i1 , i2 , i3 , i4 } and O = {o},            with ϕ1 nor with ψ by assumption, the satisfaction of
no assumption can be dropped: Otherwise the informa-               ϕ1 → ψ is not influenced by the variables outside of
tion about the global behavior of i1 , which is crucial            V1 . Thus, since we have σf ∩ V1 = σ by construction,
for the existence of an implementation, is incomplete.             σ ∈ L(ϕ1 → ψ) follows. Hence, g realizes ϕ1 → ψ. ⊓              ⊔
These observations lead to the following criterion for
safely dropping assumptions.                                           By dropping assumptions, we are able to decompose
                                                                                                      Vm          Vn
                                                                   LTL formulas of the form ϕ = i=1 ϕi → j=1 ψj in
                                                                                                      Vn Vm
Lemma 5.2 Let ϕ = (ϕ1 ∧ϕ2 ) → ψ be an LTL formula                  further cases: We rewrite ϕ to j=1 ( i=1 ϕi → ψj )
with prop(ϕ1 ) ∩ prop(ϕ2 ) = ∅, prop(ϕ2 ) ∩ prop(ψ) = ∅.           and then drop assumptions for the individual guaran-
Let ¬ϕ2 be unrealizable. Then, ϕ1 → ψ is realizable if,            tees. If the resulting subspecifications only share input
and only if, ϕ is realizable.                                      variables, they are equirealizable to ϕ.

Proof Let V1 := prop(ϕ1 ) ∪ prop(ψ), I1 := I ∩ V1 , and            Theorem 5.2 Let ϕ = (ϕ1 ∧ ϕ2 ∧ ϕ3 ) → (ψ1 ∧ ψ2 )
O1 := O ∩ V1 . First, let ϕ1 → ψ be realizable. Then               be an LTL formula over V , where prop(ϕ3 ) ⊆ I and
there is an implementation f1 : (2V1 )∗ × 2I1 → 2O1                prop(ψ1 )∩prop(ψ2 ) ⊆ I. Let prop(ϕi )∩prop(ϕj ) = ∅ for
that realizes ϕ1 → ψ. From f1 , we construct a strategy            i, j ∈ {1, 2, 3} with i 6= j, and prop(ϕi )∩prop(ψ3−i ) = ∅
f : (2V )∗ × 2I → 2O as follows: Let µ ∈ 2O\O1 is an               for i ∈ {1, 2}. Let ¬(ϕ1 ∧ϕ2 ∧ϕ3 ) be unrealizable. Then,
arbitrary valuation of the outputs outside of O1 . Then,           ϕ is realizable if, and only if, both ϕ′ = (ϕ1 ∧ ϕ3 ) → ψ1
let (σ, i) := f1 (σ ∩ V1 , i ∩ I1 ) ∪ µ. Let σ ∈ C(f ). Then       and ϕ′′ = (ϕ2 ∧ ϕ3 ) → ψ2 are realizable.
we have f (σ1 . . . σn−1 , σn ∩ I) = σn ∩ I for all n ∈ N
and thus f1 ((σ1 . . . σn−1 ) ∩ V1 , σ ∩ I1 ) = σn ∩ (I ∩ V1 )     Proof Define Vi = prop(ϕi ) ∪ prop(ϕ3 ) ∪ prop(ψ3 ) for
follows by construction of f . Hence, σ ∩ V1 ∈ C(f1 )              i ∈ {1, 2}. Since we have V = prop(ϕ) by assumption,
holds and thus, since f1 realizes ϕ1 → ψ by assumption,            V1 ∪ V2 = V holds. With the assumptions made on ϕ1 ,
σ ∩ V1 ∈ L(ϕ1 → ψ). Since prop(ϕ1 ) ∩ prop(ϕ2 ) = ∅ and            ϕ2 , ϕ3 , ψ1 , and ψ2 , we obtain V1 ∩ V2 ⊆ I.
prop(ϕ2 ) ∩ prop(ψ) = ∅, we have prop(ϕ2 ) ∩ V1 = ∅.                   First, let ϕ be realizable and let f : (2V )∗ ×2I → 2O
Hence, the valuations of the variables in prop(ϕ2 ) do             be an implementation that realizes ϕ. Let σ ∈ C(f ).
not affect the satisfaction of ϕ1 → ψ. Thus, we have               Then, σ ∈ L(ϕ) and thus by the semantics of implica-
(σ ∩ V1 ) ∪ σ ′ ∈ L(ϕ1 → ψ) for any σ ′ ∈ (2prop (ϕ2 ))ω .         tion, σ ∩ (V \ prop(ψ3−i )) ∈ L((ϕ1 ∧ ϕ2 ∧ ϕ3 ) → ψi )
In particular, (σ ∩ V1 ) ∪ (σ ∩ prop(ϕ2 )) ∈ L(ϕ1 → ψ).            follows for i ∈ {1, 2}. Hence, an implementation fi
Since prop(ϕ) = V by assumption, V = V1 ∪ prop(ϕ2 )                that behaves as f restricted to O \ prop(ψ3−i ) realizes
holds and thus (σ ∩ V1 ) ∪ (σ ∩ prop(ϕ2 )) = σ. Hence,             (ϕ1 ∧ϕ2 ∧ϕ3 ) → ψi . By Lemma 5.2, (ϕ1 ∧ϕ2 ∧ϕ3 ) → ψi
σ ∈ L(ϕ1 → ψ) holds and thus, since ϕ1 → ψ implies                 and (ϕi ∧ ϕ3 ) → ψi are equirealizable since ϕ1 , ϕ2 ,
(ϕ1 ∧ ϕ2 ) → ψ, σ ∈ L(ϕ) follows. Hence, f realizes ϕ.             and ϕ3 as well as ϕ3−i and ψi do not share any vari-
    Next, let (ϕ1 ∧ ϕ2 ) → ψ be realizable. Then, there            ables. Thus, there exist implementations f1 and f2 real-
is an implementation f : (2V )∗ × 2I → 2O that realizes            izing (ϕ1 ∧ ϕ3 ) → ψ1 and (ϕ2 ∧ ϕ3 ) → ψ2 , respectively.
(ϕ1 ∧ ϕ2 ) → ψ. Since ¬ϕ2 is unrealizable, there is a                  Next, let both (ϕ1 ∧ ϕ3 ) → ψ1 and (ϕ2 ∧ ϕ3 ) → ψ2
counterstrategy f2c : (2prop(ϕ2 ) )∗ → 2I∩prop(ϕ2 ) for ¬ϕ2        be realizable and let fi : (2Vi )∗ × 2I∩Vi → 2O∩Vi be an
and all words compatible with f2c satisfy ϕ2 . Given a fi-         implementation realizing (ϕi ∧ ϕ3 ) → ψi . We construct
nite sequence η ∈ (2V1 )∗ , let η̂ ∈ (2V )∗ be the sequence        an implementation f : (2V )∗ × 2I → 2O from f1 and f2
obtained by lifting η to V using the output of f2c . For-          as follows: f (σ, i) := f1 (σ ∩V1 , i∩V1 )∪f2 (σ ∩V2 , i∩V2 ).
mally, let η̂ = h(ε, η), where h : (2V )∗ × (2V1 )∗ → (2V )∗       Let σ ∈ C(f ). Since V1 and V2 do not share any output
is a function defined by h(τ, ε) = τ for the empty word ε          variables, σ ∩ Vi ∈ L((ϕi ∧ ϕ3 ) → ψi ) follows from the
and, when · : V × V ∗ → V ∗ denotes concatenation,                 construction of f . Moreover, σ ∩ V1 and σ ∩ V2 agree on
h(τ, s · η) = h(τ · ((s ∩ I) ∪ c ∪ f (τ, ((s ∩ I) ∪ c) ∩ I)), η)   shared variables and thus (σ∩V1 )∪(σ∩V2 ) ∈ L(ϕ′ ∧ϕ′′ )
10                                                                                                 Bernd Finkbeiner et al.

holds. Therefore, we have (σ ∩ V1 ) ∪ (σ ∩ V2 ) ∈ L(ϕ) as     Algorithm 4: Optimized LTL Decomposition
well by the semantics of conjunction and implication.         Algorithm
Since V1 ∪ V2 = V , we have (σ ∩ V1 ) ∪ (σ ∩ V2 ) = σ and         Input: ϕ: LTL, inp: List Variable, out: List Variable
thus σ ∈ L(σ). Hence, f realizes ϕ.                     ⊓
                                                        ⊔         Result: specs: List (LTL, List Variable, List
                                                                          Variable)
    Analyzing assumptions thus allows for decomposing         1 assumptions ← getAssumptions(ϕ)
LTL formulas in further cases and still ensures sound-        2 guarantees ← getGuarantees(ϕ)
                                                              3 decCritProps ← getDecCritProps(ϕ)
ness and completeness of modular synthesis. In the fol-
                                                              4 graph ← buildDependencyGraph(ϕ,decCritProps)
lowing, we present an optimized LTL decomposition             5 components ← graph.connectedComponents()
algorithm that incorporates assumption dropping into          6 specs ← new LTL[|components| + 1]

the search for independent conjuncts. Intuitively, the        7 freeAssumptions ←[ ]
                                                              8 foreach ψ ∈ assumptions do
algorithm needs to identify variables that cannot be
                                                              9     propositions ← decCritProps ∩ getProps(ψ)
shared safely among subspecifications. If an assumption      10     if |propositions| = 0 then
contains such non-sharable variables, we say that it is      11          freeAssumptions.append(ψ)
bound to guarantees since it can influence the possible      12     else
decompositions. Otherwise, it is called free.                13          foreach (spec, set) ∈ zip specs (components
                                                                          ++ [inp]) do
    To determine which assumptions are relevant for de-      14              if propositions ∩ set =
                                                                                                   6 ∅ then
composition, i.e., which assumptions are bounded as-         15                  spec.addAssumption(ψ)
sumptions, we build a slightly modified version of the       16                  break
dependency graph that is only based on assumptions
and not on all conjuncts of the formula. Moreover, all       17 foreach ψ ∈ guarantees do
variables serve as the nodes of the graph, not only the      18     propositions ← decCritProps ∩ getProps(ψ)
                                                             19     foreach (spec, set) ∈ zip specs (components ++
output variables. An undirected edge between two vari-               [inp]) do
ables in the modified dependency graph denotes that          20         if propositions ∩ set =
                                                                                              6 ∅ then
the variables occur in the same assumption. Variables        21             spec.addGuarantee(ψ)
that are contained in the same connected component           22              break
as an output variable o ∈ O are thus connected to o
                                                             23   return addFreeAssumptions specs freeAssumptions
over a path of one or more assumptions. Therefore,
they may not be shared among subspecifications as
they might influence o and thus may influence the de-
composability of the specification. These variables are           The decomposition algorithm does not check for as-
then called decomposition-critical. Given the modified       sumption violations. The unrealizability of the nega-
dependency graph, we can compute the decomposition-          tion of the dropped assumption, however, is an essen-
critical propositions with a simple depth-first search.      tial part of the criterion for assumption dropping (c.f.
    After computing the decomposition-critical proposi-      Theorem 5.2). Therefore, we incorporate the check for
tions, we create the dependency graph and extract con-       assumption violations into the modular synthesis algo-
nected components in the same way as in Algorithm 3          rithm: Before decomposing the specification, we per-
to decompose the LTL specification. Instead of using         form synthesis on the negated assumptions. If synthe-
only output variables as nodes of the graph, though,         sis returns that the negated assumptions are realizable,
we use all decomposition-critical variables. We then ex-     the system is able to violate an assumption. The imple-
clude free assumptions and add all other assumptions to      mentation satisfying the negated assumptions is then
their respective subspecification similar to Algorithm 3.    extended to an implementation for the whole specifi-
We assign the guarantees to their subspecification in        cation that violates the assumptions and thus realizes
the same manner. Lastly, we add the remaining assump-        the specification. Otherwise, if the negated assumptions
tions. Since all of these assumptions are free, they could   are unrealizable, the conditions of Theorem 5.2 are sat-
be safely added to all subspecifications. Yet, to obtain     isfied. Hence, we can use the decomposition algorithm
small subspecifications, we only add them to subspeci-       and proceed as in Algorithm 1. The modified modu-
fications for which they are needed. Note that we have       lar synthesis algorithm that incorporates the check for
to add all assumptions featuring an input variable that      assumption violations is shown in Algorithm 5.
occurs in the subspecification. Therefore, we analyze             Note that Algorithm 4 is only applicable to specifi-
the assumptions and add them in one step, as a naive         cations in a strict assume-guarantee format since Theo-
approach could have an unfavorable running time. The         rem 5.2 assumes a top-level implication in the formula.
whole LTL decomposition algorithm with optimized as-         In the next section, we thus present an extension of
sumption handling is shown in Algorithm 4.                   the LTL decomposition algorithm with optimized as-
Specification Decomposition for Reactive Synthesis                                                                   11


 Algorithm 5: Modular Synthesis Algorithm                     applicable and thus Algorithm 3 does not decompose ϕ.
 with Optimized LTL Decomposition                             The naive approach for incorporating assumption drop-
     Input: s: Specification, inp: List Variable, out: List   ping described above considers the third conjunct of ϕ
            Variable                                          separately and checks whether whether the assumption
   Result: realizable: Bool, implementation: T                   i can be dropped. Since the assumptions and guar-
 1 (real, strat) ← synthesize(getNegAss(ϕ), inp, out)
                                                              antees do not share any variables, Lemma 5.2 is ap-
 2 if real then
 3     return (⊤, strat)                                      plicable and thus the naive algorithm drops i, yield-
 4 subspecifications ← decompose(s, inp, out)
                                                              ing ϕ′ = ¬(o1 ∧ o2 ) ∧ ¬(i ↔ o1 ) ∧ o2 . Yet, ϕ′ is
 5 sub results ← map synthesize subspecifications             not realizable: If i is constantly set to false, the sec-
 6 foreach (real, strat) ∈ sub results do                     ond conjunct of ϕ′ enforces o1 to be always set to true.
 7     if ! real then                                         The third conjunct enforces that o2 is constantly set
 8          implementation ←
             extendCounterStrategy(strat, s)                  to true irrespective of the input i. The first conjunct,
 9          return (⊥, implementation)                        however, requires in every time step one of the output
                                                              variables to be false. Thus, although Lemma 5.2 is ap-
10 impls ← map second sub results
11 implementation ← compose impls
                                                              plicable to i → o1 , dropping the assumption safely
12 return (⊤, implementation)                                 is not possible in the context of the other two conjuncts.
                                                              In particular, the first conjunct of ϕ introduces a de-
                                                              pendency between o1 and o2 while the second conjunct
sumption handling to specifications consisting of sev-        introduces one between i and o1 . Hence, there is a tran-
eral assume-guarantee conjuncts, i.e., specifications of      sitive dependency between i and o1 due to which the
the form ϕ = (ϕ1 → ψ1 ) ∧ · · · ∧ (ϕk → ψk ).                 assumption i cannot be dropped. This dependency is
                                                              not detected when considering the conjuncts separately
                                                              during the assumption dropping phase.
                                                                   In this section, we introduce an optimization of the
6 Optimized LTL Decomposition for Formulas
                                                              LTL decomposition algorithm which is able to decom-
with Several Assume-Guarantee Conjuncts
                                                              pose specifications with several conjuncts (possibly) in
                                                              assume-guarantee format and which is, in contrast to
Since Corollary 5.1 can be applied recursively, classical
                                                              the naive approach described before, sound. Similar to
LTL decomposition, i.e., as described in Algorithm 3, is
                                                              the naive approach, the main idea is to first check for
applicable to specifications with several conjuncts. That
                                                              assumptions that can be dropped in the different con-
is, in particular, it is applicable to specifications with
                                                              juncts and to then perform the classical LTL decompo-
several assume-guarantee conjuncts, i.e., specifications
                                                              sition algorithm. Yet, the assumption dropping phase is
of the form ϕ = (ϕ1 → ψ1 ) ∧ · · · ∧ (ϕk → ψk ). Algo-
                                                              not performed completely separately for the individual
rithm 4, in contrast, is restricted to LTL specifications
                                                              conjuncts but takes the other conjuncts and thus pos-
consisting of a single assume-guarantee pair since The-
                                                              sible transitive dependencies between the assumptions
orem 5.2, on which Algorithm 4 relies, assumes a top-
                                                              and guarantees into account.
level implication in the specification. Hence, we cannot
                                                                   If the other conjuncts do not share any variable with
apply the optimized assumption handling to specifica-
                                                              the assumption to be dropped, then there are no tran-
tions with several assume-guarantee conjuncts directly.
                                                              sitive dependencies between the assumption and the
     A naive approach to extend assumption dropping to
                                                              guarantee due to the other conjuncts. Thus, the as-
formulas with several assume-guarantee conjuncts is to
                                                              sumption can be dropped safely if the other conditions
first drop assumptions for all conjuncts separately and
                                                              of Lemma 5.2 are satisfied:
then to decompose the resulting specification using Al-
gorithm 3. In general, however, this is not sound: The        Lemma 6.1 Let ϕ = ψ1 ∧ ((ϕ1 ∧ ϕ2 ) → ψ2 ) be an
other conjuncts may introduce dependencies between            LTL formula, where we have prop(ϕ1 ) ∩ prop(ϕ2 ) = ∅,
assumptions and guarantees that prevent the dropping          prop(ϕ2 ) ∩ prop(ψ1 ) = ∅ and prop(ϕ2 ) ∩ prop(ψ2 ) = ∅.
of the assumption. When considering the conjuncts dur-        Let ¬ϕ2 be unrealizable. Then, ϕ′ = ψ1 ∧ (ϕ1 → ψ2 ) is
ing the assumption dropping phase separately, however,        realizable if, and only if, ϕ is realizable.
such dependencies are not detected. For instance, con-
sider a system with I = {i}, O = {o1 , o2 }, and the spec-    Proof Let V1 := prop(ψ1 ∧(ϕ1 → ψ2 )), I1 := I ∩V1 , and
ification ϕ = ¬(o1 ∧ o2 ) ∧ ¬(i ↔ o1 ) ∧ ( i → o2 ).          O1 := O ∩ V1 . If ϕ′ is realizable, then we can construct
Clearly, ϕ is realizable by an implementation that sets       an implementation f : (2V )∗ × 2I → 2O that realizes ϕ
o1 to ¬i and o2 to i in every time step. Since the first      from the implementation f1 : (2V1 )∗ × 2I1 → 2O1 that
conjunct contains both o1 and o2 , Corollary 5.1 is not       realizes ϕ′ analogous to the proof of Lemma 5.2.
12                                                                                                     Bernd Finkbeiner et al.

    If ϕ is realizable, then there is an implementation           Algorithm 6: Optimized LTL Decomposition
f : (2V )∗ × 2I → 2O that realizes ϕ. Since ¬ϕ2 is                Algorithm for Specifications with Conjuncts
unrealizable by assumption, there is a counterstrategy                Input: ϕ: LTL, inp: List Variable, out: List Variable
f2c : (2prop(ϕ2 ) )∗ → 2I∩prop(ϕ2 ) for ¬ϕ2 and all words             Result: specs: List (LTL, List Variable, List
compatible with f2c satisfy ϕ2 . Let g : (2V1 )∗ ×2I1 → 2O1                   Variable)
                                                                    implication ← chooseImplication(ϕ)
be the implementation constructed from f and f2c in               1
                                                                  2 assumptions ← getAssumptions(implication)
the proof of Lemma 5.2. We show that g realizes ϕ′ .              3 guarantees ← getGuarantees(implication)
Let σ ∈ C(g) and let σf be the corresponding infi-                4 decCritProps ← getDecCritProps(implication)

nite sequence obtained from g when not restricting the            5 graph ← buildDependencyGraph(ϕ,decCritProps)
                                                                  6 components ← graph.connectedComponents()
output of f to the variables in O1 . As shown in the
                                                                  7 specs ← new LTL[|components| + 1]
proof of Lemma 5.2, σf ∈ L(ϕ) and σf ∈ L(ϕ2 ). Thus,              8 freeAssumptions ←[ ]
σf ∈ L(ψ1 ∧ (ϕ1 → ψ2 )). Since ϕ2 neither shares vari-            9 foreach ψ ∈ assumptions do

ables with ϕ1 nor with ψ1 or ψ2 , the satisfaction of            10     propositions ← decCritProps ∩ getProps(ψ)
                                                                 11     if |propositions| = 0 then
ψ1 ∧ (ϕ1 → ψ2 ) is not influenced by the variables out-
                                                                 12          freeAssumptions.append(ψ)
side of V1 . Hence, since σf ∩ V1 = σ by construction,           13     else
σ ∈ L(ϕ′ ) follows and thus g realizes ϕ′ .               ⊓
                                                          ⊔      14          foreach (spec, set) ∈ zip specs (components
                                                                              ++ [inp]) do
    Similar to the optimized assumption handling for             15              if propositions ∩ set =
                                                                                                       6 ∅ then
                                                                 16                  spec.addAssumption(ψ)
specifications in strict assume-guarantee form described
                                                                 17                  break
in the previous section, we utilize Lemma 6.1 for an
optimized decomposition for specifications containing
                                                                 18 foreach ψ ∈ guarantees do
several assume-guarantee conjuncts:V      We rewrite
                                                Vn    LTL        19     propositions ← decCritProps ∩ getProps(ψ)
formulas of the form ϕ = ψ ′ ∧ m         ϕ   →   j=1 j to
                                                     ψ                  foreach (spec, set) ∈ zip specs (components ++
     V      V                        i=1 i                       20

ψ ′ ∧ nj=1 ( m    ϕ
              i=1 i   →   ψj ) and then drop  assumptions                [inp]) do
                                                                 21         if propositions ∩ set =
                                                                                                  6 ∅ then
for the individual guarantees ψ1 , . . . , ψj according to
                                                                 22             spec.addGuarantee(ψ)
Lemma 6.1. If the resulting subspecifications only share         23              break
input variables, they are equirealizable to ϕ.
                                                                 24 foreach ψ ∈ getConjuncts(ϕ)\implication do
Theorem 6.1 Let ϕ = ψ1′ ∧ψ2′ ∧((ϕ1 ∧ϕ2 ∧ϕ3 ) → ψ1 ∧ψ2 )          25     propositions ← decCritProps ∩ getProps(ψ)
be an LTL formula over V , where prop(ϕ3 ) ⊆ I and               26     foreach (spec, set) ∈ zip specs (components ++
                                                                         [inp]) do
(prop(ψ1 ) ∪ prop(ψ1′ )) ∩ (prop(ψ2 ) ∪ prop(ψ2′ )) ⊆ I. Let     27         if propositions ∩ set =
                                                                                                  6 ∅ then
prop(ϕi ) ∩ prop(ϕj ) = ∅ for i, j ∈ {1, 2, 3} with i 6= j,      28             spec.addConjunct(ψ)
and let prop(ϕi ) ∩ prop(ψ3−i ) = ∅ for i ∈ {1, 2}. Let          29              break
prop(ψi′ ) ∩ prop(ϕ3−i ) = ∅ for i ∈ {1, 2}. Moreover, let
                                                                      return addFreeAssumptions specs freeAssumptions
¬(ϕ1 ∧ ϕ2 ∧ ϕ3 ) be unrealizable. Then, ϕ is realizable          30


if, and only if, both ϕ′ = ψ ′ ∧ ((ϕ1 ∧ ϕ3 ) → ψ1 ) and
ϕ′′ = ψ ′′ ∧ ((ϕ2 ∧ ϕ3 ) → ψ2 ) are realizable.
                                                                                                       ′
                                                                 variables with ϕ3 , ϕ3−1 , ψ3−1 and ψ3−1 . Therefore, by
                   ′       ′′
Proof First, let ϕ and ϕ be realizable. Then, there are          Lemma 6.1, ψ1 ∧ ((ϕ1 ∧ ϕ2 ∧ ϕ3 ) → ψ1 ) and ϕ′ are
                                                                                ′

implementations f1 and f2 realizing ϕ′ and ϕ′′ , respec-         equirealizable. Moreover, ψ2′ ∧ ((ϕ1 ∧ ϕ2 ∧ ϕ3 ) → ψ2 )
tively. Since ϕ′ and ϕ′′ do not share output variables by        and ϕ′′ are equirealizable. Thus, since f1 and f2 realize
assumption, we can construct an implementation real-             the former formulas, ϕ′ and ϕ′′ are both realizable. ⊓ ⊔
izing ϕ from f1 and f2 as in the proof of Theorem 5.2.
     Next, let ϕ be realizable and let f : (2V )∗ ×2I → 2O           Utilizing Theorem 6.1, we extend Algorithm 4 to
be an implementation realizing ϕ. Let σ ∈ C(f ). Then,           LTL specifications that do not follow a strict assume-
σ ∈ L(ϕ) holds. Let V ′ = prop(ϕ′ ) ∪ prop(ϕ2 ) and let          guarantee form but consist of multiple conjuncts. The
V ′′ = prop(ϕ′′ ) ∪ prop(ϕ1 ). Then, since σ ∈ L(ϕ) holds,       extended algorithm is depicted in Algorithm 6. We as-
σ ∩ V ′ ∈ L(ψ ′ ∧ ((ϕ1 ∧ ϕ2 ∧ ϕ3 ) → ψ1 )) as well as            sume that the specification is not decomposable by Al-
σ ∩ V ′′ ∈ L(ψ ′′ ∧ ((ϕ1 ∧ ϕ2 ∧ ϕ3 ) → ψ2 )) follow. Thus,       gorithm 3, i.e., we assume that no plain decompositions
an implementation f1 that behaves as f restricted to             are possible. In practice, we thus first rewrite the spec-
the variables in V ′ realizes ψ ′ ∧ ((ϕ1 ∧ ϕ2 ∧ ϕ3 ) → ψ1 ).     ification and apply Algorithm 3 afterwards before then
An implementation f2 that behaves as f restricted to             applying Algorithm 6 to the resulting subspecifications.
the variables in V ′′ realizes ψ ′′ ∧ ((ϕ1 ∧ ϕ2 ∧ ϕ3 ) → ψ2 ).       Hence, we assume that the dependency graph built
By assumption, for i ∈ {1, 2}, ϕi does not share any             from the output propositions of all given conjuncts con-
Specification Decomposition for Reactive Synthesis                                                                                            13

sists of a single connected component. Theorem 6.1
hands us the tools to “break a link” in that chain of                          1,000                   BoSy (original)
dependencies. This link has to be induced by a suitable                                                BoSy (modular)
implication. Algorithm 6 assumes that at least one of




                                                              synthesis time (seconds)
                                                                                                       Strix (original)
the conjuncts is an implication. In case of more than                                                  Strix (modular)
                                                                                         100
one implication, the choice of the implication conse-
quently determines whether or not a decomposition os
found. Therefore, it is crucial to reapply the algorithm
on the subspecifications after a decomposition has been                                   10
found and to try all implications if no decomposition is
found. Since iterating through all conjuncts does not
pose a large overhead in computing time, the choice of
                                                                                           1
the implication is not further specified in the algorithm.
    The extended algorithm is similar to Algorithm 4.
Note that the dependency graph used for finding the                                            0   5       10     15      20   25   30   35   40
decomposition-critical propositions is built only from                                                           solved instances
the assumptions of the chosen implication as we are
only seeking for droppable assumptions of this implica-      Fig. 7.1: Comparison of the performance of modular
tion. In contrast to Algorithm 4, the dependency graph       and non-compositional synthesis with BoSy and Strix
in line 5 of Algorithm 6 also includes the dependencies      on the decomposable SYNTCOMP benchmarks. For
induced by the other conjuncts, similarly to the de-         the modular approach, the accumulated time for all
pendency graph in Algorithm 3. Here, we consider all         synthesis tasks is depicted.
decomposition-critical variables in the conjuncts, not
only output variables, as an assumption can only be          them on the 346 publicly available SYNTCOMP [18]
dropped if there are no shared variables with the re-        2020 benchmarks. Note that only 207 of the bench-
maining conjuncts. Therefore, the additional conjuncts       marks have more than one output variable and are
are treated in the same way as the guarantees. This car-     therefore realistic candidates for decomposition. The
ries over to when the conjuncts are added to the sub-        automaton decomposition algorithm utilizes Spot’s [7]
specifications. Lastly, Algorithm 6 slightly differs from    automaton library (Version 2.9.6). The LTL decompo-
Algorithm 4 when the free assumptions are added to the       sition relies on SyFCo [19] for formula transformations
subspecifications. Here, the remaining conjuncts have        (Version 1.2.1.1). We first decompose the specification
to be considered, too, since we may not drop assump-         with our algorithms and then run synthesis on the re-
tions that share variables with the outside conjunct.        sulting subspecifications. We compare the CPU time of
Consequently, all free assumptions that share an input       the synthesis task as well as the number of gates, and
with one of the remaining conjuncts, needs to be added.      latches of the synthesized AIGER circuit for the original
    One detail that has to be taken into account when        specification to the sum of the corresponding attributes
integrating this LTL decomposition algorithm with ex-        of all subspecifications. Thus, we calculate the runtime
tended optimized assumption handling into a synthesis        for sequential modular synthesis. Parallelization of the
tool, is that, like Algorithm 4, Algorithm 6 assumes that    synthesis tasks may further reduce the runtime.
all negated assumptions are unrealizable. For formulas
in a strict assume-guarantee format, the consequences
of realizable assumptions is that we have found a strat-
                                                             7.1 LTL Decomposition
egy for the implementation. This changes when con-
sidering formulas with additional conjuncts since they
                                                             LTL decomposition with optimized assumption han-
might forbid this strategy. To detect such strategies, we
                                                             dling (c.f. Section 6) terminates on all benchmarks in
can verify the synthesized strategy against the remain-
                                                             less than 26ms. Thus, even for non-decomposable spec-
ing conjunct and only extend it to a counterstrategy for
                                                             ifications, the overhead of trying to perform decomposi-
the whole specification in the positive case.
                                                             tions is negligible. The algorithm decomposes 39 formu-
                                                             las into several subspecifications, most of them yielding
7 Experimental Evaluation                                    two or three subspecifications. Only a handful of for-
                                                             mulas are decomposed into more than six subspecifica-
We implemented the modular synthesis algorithm as            tions. The full distribution of the number of subspeci-
well as the decomposition approaches and evaluated           fications for all specifications is shown in Table 7.1
14                                                                                                              Bernd Finkbeiner et al.

       Table 7.1: Distribution of the number of subspecifications over all specifications for LTL decomposition.

              # subspecifications        1       2     3      4        5      6        7    8        9     10     11      12
              # specifications          308     19     8      2        3      2        0    2        0      1      1       1

Table 7.2: Synthesis time in seconds of BoSy and Strix for non-compositional and modular synthesis on exemplary
SYNTCOMP benchmarks with a timeout of 60 minutes.

                                                     original                          modular
                 Benchmark                     BoSy           Strix            BoSy              Strix       # subspec.
                 Cockpitboard                 1526.32         11.06            2.108             8.168            8
                 Gamelogic                      TO           1062.27              TO         25.292               4
                 LedMatrix                      TO             TO                 TO         1156.68              3
                 Radarboard                     TO           126.808          3.008           11.04              11
                 Zoo10                         1.316           1.54           0.884           2.744               2
                 generalized buffer 2          70.71         534.732          4.188           7.892               2
                 generalized buffer 3           TO             TO             27.136         319.988              3
                 shift 8                       0.404          1.336            2.168           3.6                8
                 shift 10                      1.172          1.896            2.692          4.464              10
                 shift 12                      4.336          6.232            3.244          5.428              12


Table 7.3: Gates of the synthesized solutions of BoSy                  Table 7.4: Latches of the synthesixed solutions of BoSy
and Strix for non-compositional and modular synthesis                  and Strix for non-compositional and modular synthesis
on exemplary SYNTCOMP benchmarks. Entry – de-                          on exemplary SYNTCOMP benchmarks. Entry – de-
notes that no solution was found within 60 minutes.                    notes that no solution was found within 60 minutes.

                               original            modular                                               original         modular
     Benchmark              BoSy     Strix      BoSy    Strix              Benchmark                 BoSy      Strix   BoSy    Strix
     Cockpitboard            11         7        25      10                Cockpitboard                1          0      8       0
     Gamelogic               –        26          –      21                Gamelogic                   –          2      –       2
     LedMatrix               –          –         –      97                LedMatrix                   –          –      –       5
     Radarboard              –          6        19       6                Radarboard                  –          0     11       0
     Zoo10                   14       15         15      13                Zoo10                      1           2      2        2
     generalized buffer 2    3        12          3      11                generalized buffer 2       69       47134    14      557
     generalized buffer 3    –          –        20     3772               generalized buffer 3        –          –     3        14
     shift 8                 8          0         8       7                shift 8                     1          0      8       0
     shift 10                10         0        10       9                shift 10                    1          0     10       0
     shift 12                12         0        12      11                shift 12                    1          0     12       0



    We evaluate our modular synthesis approach with                    plary benchmarks. For modular synthesis, the accumu-
two state-of-the-art synthesis tools: BoSy [9], a bounded              lated running time of all synthesis tasks is depicted. On
synthesis tool, and Strix [25], a game-based synthesis                 almost all of them, both tools decrease their synthe-
tool, both in their 2019 release. We used a machine with               sis times with modular synthesis notably compared to
a 3.6GHz quad-core Intel Xeon processor and 32GB                       the original non-compositional approaches. Particularly
RAM as well as a timeout of 60 minutes.                                noteworthy is the benchmark generalized buffer 3. In
    In Figure 7.1, the comparison of the accumulated                   the last synthesis competition, SYNTCOMP 2021, no
runtimes of the synthesis tasks of the subspecifications               tool was able to synthesize a solution for it within one
and of the original formula is shown for the decom-                    hour. With modular synthesis, however, BoSy yields a
posable SYNTCOMP benchmarks. For both BoSy and                         result in less than 28 seconds.
Strix, decomposition generates a slight overhead for                       In Tables 7.3 and 7.4, the number of gates and
small specifications. For larger and more complex spec-                latches, respectively, of the AIGER circuits [1] corre-
ifications, however, modular synthesis decreases the ex-               sponding to the implementations computed by BoSy
ecution time significantly, often by an order of magni-                and Strix for modular and non-compositional synthesis
tude or more. Note that due to the negligible runtime                  are depicted for exemplary benchmarks. For most spec-
of specification decomposition, the plot looks similar                 ifications, the solutions of modular synthesis are of the
when considering all SYNTCOMP benchmarks.                              same size or smaller in terms of gates than the solutions
    Table 7.2 shows the running times of BoSy and Strix                for the original specification. The size of the solutions
for modular and non-compositional synthesis on exem-                   in terms of latches, however, varies. Note that BoSy
Specification Decomposition for Reactive Synthesis                                                                   15

Table 7.5: Distribution of the number of subspecifications over all specifications for NBA decomposition. For 79
specifications, the timeout (60min) was reached. For 39 specification, the memory limit (16GB) was reached.

   # subspec.    1      2      3     4      5        6   7   8      9     10    12     14    19     20    24    36
   # spec.      192     9      8     6      2        3   1   2      1      1    4      1     1      2     1      1


does not generate solutions with less than one latch in      8 Conclusion
general. Hence, the modular solution will always have
at least as many latches as subspecifications.               We have presented a modular synthesis algorithm that
                                                             applies compositional techniques to reactive synthesis.
7.2 Automaton Decomposition                                  It reduces the complexity of synthesis by decomposing
                                                             the specification in a preprocessing step and then per-
Besides LTL specifications, Strix also accepts specifica-    forming independent synthesis tasks for the subspecifi-
tions given as deterministic parity automata (DPAs) in       cations. We have introduced a criterion for decomposi-
extended HOA format [27], an automaton format well-          tion algorithms that ensures soundness and complete-
suited for synthesis. Thus, our implementation for de-       ness of modular synthesis as well as two algorithms for
composing specifications given as NBAs performs Algo-        specification decomposition satisfying the criterion: A
rithm 2, converts the resulting automata to DPAs and         semantically precise one for specifications given as non-
then synthesizes solutions with Strix.                       deterministic Büchi automata, and an approximate al-
    For 235 out of the 346 benchmarks, NBA decompo-          gorithm for LTL specifications. We presented optimiza-
sition terminates within ten minutes, yielding several       tions of the LTL decomposition algorithm for formulas
subspecifications or proving that the specification is not   in a strict assume-guarantee format and for formulas
decomposable. In 79 of the other cases, the tool timed       consisting of several assume-guarantee conjuncts. Both
out after 60 minutes and in the remaining 32 cases it        optimizations are based on dropping assumptions that
reached the memory limit of 16GB or the internal lim-        do not influence the realizability of the rest of the for-
its of Spot. Note, however, that for 81 specifications       mula. We have implemented the modular synthesis al-
even plain DPA generation failed. The distribution of        gorithm as well as both decomposition algorithms and
the number of subspecifications for all specifications is    we compared our approach for the state-of-the-art syn-
shown in Table 7.5. Thus, while automaton decomposi-         thesis tools BoSy and Strix to their non-compositional
tion yields more fine-grained decompositions than the        forms. Our experiments clearly demonstrate the signif-
approximate LTL approach, it becomes infeasible when         icant advantage of modular synthesis with LTL decom-
the specifications grow. Hence, the advantage of smaller     position over traditional synthesis algorithms. While
synthesis subtasks cannot pay off. However, the coarser      the overhead is negligible, both BoSy and Strix are able
LTL decomposition suffices to reduce the synthesis time      to synthesize solutions for more benchmarks with mod-
on common benchmarks significantly. Thus, LTL de-            ular synthesis than in their non-compositional form.
composition is in the right balance between small sub-       Moreover, on large and complex specifications, BoSy
tasks and a scalable decomposition.                          and Strix improve their synthesis times notably, demon-
    For 43 specifications, the automaton approach yields     strating that specification decomposition is a game-
decompositions and many of them consist of four or           changer for practical LTL synthesis.
more subspecifications. For 22 of these specifications,          Building up on the presented approach, we can addi-
the LTL approach yields a decomposition as well. Yet,        tionally analyze whether the subspecifications fall into
they differ in most cases, as the automaton approach         fragments for which efficient synthesis algorithms exist,
yields more fine-grained decompositions.                     for instance safety specifications. Since modular syn-
    Recall that only 207 SYNTCOMP benchmarks are             thesis performs independent synthesis tasks for the sub-
realistic candidates for decomposition. The automaton        specifications, we can choose, for each synthesis task, an
approach proves that 90 of those specifications (43.6%)      algorithm that is tailored to the fragment the respective
are not decomposable. Thus, our implementations yield        subspecification lies in. Moreover, parallelizing the in-
decompositions for 33.33% (LTL) and 36.75% (NBA)             dividual synthesis tasks may increase the advantage of
of the potentially decomposable specifications. We ob-       modular synthesis over classical algorithms. Since the
served that decomposition works exceptionally well for       number of subspecifications computed by the LTL de-
specifications that stem from real system designs, for       composition algorithm highly depends on the rewriting
instance the Syntroids [15] case study, indicating that      of the initial formula, a further promising next step is
modular synthesis is particularly beneficial in practice.    to develop more sophisticated rewriting algorithms.
16                                                                                                   Bernd Finkbeiner et al.

References                                                          cation - 29th International Conference, CAV 2017. Pro-
                                                                    ceedings, Part II, Lecture Notes in Computer Science, vol.
1. Biere, A., Heljanko, K., Wieringa, S.: AIGER 1.9 And             10427, pp. 325–332. Springer (2017). URL https://doi.
   Beyond. Tech. Rep. 11/2, Institute for Formal Models             org/10.1007/978-3-319-63390-9 17
   and Verification, Johannes Kepler University, Altenberg-     10. Filiot, E., Jin, N., Raskin, J.: Compositional Algorithms
   erstr. 69, 4040 Linz, Austria (2011)                             for LTL Synthesis. In: A. Bouajjani, W. Chin (eds.)
2. Bloem, R., Chatterjee, K., Jacobs, S., Könighofer, R.:          Automated Technology for Verification and Analysis -
   Assume-Guarantee Synthesis for Concurrent Reactive               8th International Symposium, ATVA 2010. Proceedings,
   Programs with Partial Information.        In: C. Baier,          Lecture Notes in Computer Science, vol. 6252, pp. 112–
   C. Tinelli (eds.) Tools and Algorithms for the Construc-         127. Springer (2010). URL https://doi.org/10.1007/
   tion and Analysis of Systems - 21st International Con-           978-3-642-15643-4 10
   ference, TACAS 2015, Held as Part of the European            11. Finkbeiner, B.: Synthesis of Reactive Systems. In: J. Es-
   Joint Conferences on Theory and Practice of Software,            parza, O. Grumberg, S. Sickert (eds.) Dependable Soft-
   ETAPS 2015. Proceedings, Lecture Notes in Computer               ware Systems Engineering, NATO Science for Peace and
   Science, vol. 9035, pp. 517–532. Springer (2015). URL            Security Series - D: Information and Communication Secu-
   https://doi.org/10.1007/978-3-662-46681-0 50                     rity, vol. 45, pp. 72–98. IOS Press (2016). URL https:
3. Chatterjee, K., Henzinger, T.A.: Assume-Guarantee Syn-           //doi.org/10.3233/978-1-61499-627-9-72
   thesis. In: O. Grumberg, M. Huth (eds.) Tools and            12. Finkbeiner, B., Geier, G., Passing, N.: Specification De-
   Algorithms for the Construction and Analysis of Sys-             composition for Reactive Synthesis. In: NASA Formal
   tems, 13th International Conference, TACAS 2007, Held            Methods, NFM 2021. Proceedings (2021)
   as Part of the Joint European Conferences on The-            13. Finkbeiner, B., Passing, N.: Dependency-Based Compo-
   ory and Practice of Software, ETAPS 2007. Proceed-               sitional Synthesis. In: D.V. Hung, O. Sokolsky (eds.)
   ings, Lecture Notes in Computer Science, vol. 4424, pp.          Automated Technology for Verification and Analysis -
   261–275. Springer (2007). URL https://doi.org/10.1007/           18th International Symposium, ATVA 2020. Proceed-
   978-3-540-71209-1 21                                             ings, Lecture Notes in Computer Science, vol. 12302, pp.
4. Clarke, E.M., Long, D.E., McMillan, K.L.: Compositional          447–463. Springer (2020). URL https://doi.org/10.1007/
   Model Checking. In: Proceedings of the Fourth Annual             978-3-030-59152-6 25
   Symposium on Logic in Computer Science, LICS 1989,           14. Finkbeiner, B., Passing, N.: Compositional synthesis
   pp. 353–362. IEEE Computer Society (1989). URL https:            of modular systems. In: Z. Hou, V. Ganesh (eds.)
   //doi.org/10.1109/LICS.1989.39190                                Automated Technology for Verification and Analysis -
5. Damm, W., Finkbeiner, B.: Does It Pay to Extend                  19th International Symposium, ATVA 2021, Gold Coast,
   the Perimeter of a World Model? In: M.J. Butler,                 QLD, Australia, October 18-22, 2021, Proceedings, Lec-
   W. Schulte (eds.) Formal Methods - 17th International            ture Notes in Computer Science, vol. 12971, pp. 303–
   Symposium on Formal Methods, FM 2011. Proceed-                   319. Springer (2021). URL https://doi.org/10.1007/
   ings, Lecture Notes in Computer Science, vol. 6664, pp.          978-3-030-88885-5 20
   12–26. Springer (2011). URL https://doi.org/10.1007/         15. Geier, G., Heim, P., Klein, F., Finkbeiner, B.: Syntroids:
   978-3-642-21437-0 4                                              Synthesizing a game for fpgas using temporal logic spec-
6. Dureja, R., Rozier, K.Y.: More Scalable LTL Model                ifications. In: C.W. Barrett, J. Yang (eds.) 2019 For-
   Checking via Discovering Design-Space Dependencies               mal Methods in Computer Aided Design, FMCAD 2019.
   (D 3 ). In: D. Beyer, M. Huisman (eds.) Tools and Al-            Proceedings, pp. 138–146. IEEE (2019). URL https:
   gorithms for the Construction and Analysis of Systems            //doi.org/10.23919/FMCAD.2019.8894261
   - 24th International Conference, TACAS 2018, Held as         16. Giannakopoulou, D., Pressburger, T., Mavridou, A.,
   Part of the European Joint Conferences on Theory and             Rhein, J., Schumann, J., Shi, N.: Formal requirements
   Practice of Software, ETAPS 2018. Proceedings, Part              elicitation with FRET. In: M. Sabetzadeh, A. Vogel-
   I, Lecture Notes in Computer Science, vol. 10805, pp.            sang, S. Abualhaija, M. Borg, F. Dalpiaz, M. Daneva,
   309–327. Springer (2018). URL https://doi.org/10.1007/           N. Condori-Fernández, X. Franch, D. Fucci, V. Gervasi,
   978-3-319-89960-2 17                                             E.C. Groen, R.S.S. Guizzardi, A. Herrmann, J. Horkoff,
7. Duret-Lutz, A., Lewkowicz, A., Fauchille, A., Michaud,           L. Mich, A. Perini, A. Susi (eds.) Joint Proceedings
   T., Renault, E., Xu, L.: Spot 2.0 - A Framework for LTL          of REFSQ-2020 Workshops, Doctoral Symposium, Live
   and ω -automata Manipulation. In: C. Artho, A. Legay,            Studies Track, and Poster Track co-located with the 26th
   D. Peled (eds.) Automated Technology for Verification            International Conference on Requirements Engineering:
   and Analysis - 14th International Symposium, ATVA                Foundation for Software Quality (REFSQ 2020), Pisa,
   2016. Proceedings, Lecture Notes in Computer Science, vol.       Italy, March 24, 2020, CEUR Workshop Proceedings, vol.
   9938, pp. 122–129 (2016). URL https://doi.org/10.1007/           2584. CEUR-WS.org (2020). URL http://ceur-ws.org/
   978-3-319-46520-3 8                                              Vol-2584/PT-paper4.pdf
8. Ehlers, R.: Unbeast: Symbolic bounded synthesis. In:         17. Jacobs, S., Bloem, R.: The Reactive Synthesis Compe-
   Tools and Algorithms for the Construction and Analy-             tition: SYNTCOMP 2016 and Beyond. In: R. Piskac,
   sis of Systems - 17th International Conference, TACAS            R. Dimitrova (eds.) Fifth Workshop on Synthesis,
   2011, Held as Part of the Joint European Conferences on          SYNT@CAV 2016. Proceedings, EPTCS, vol. 229, pp.
   Theory and Practice of Software, ETAPS 2011. Proceed-            133–148 (2016). URL https://doi.org/10.4204/EPTCS.
   ings, Lecture Notes in Computer Science, vol. 6605, pp.          229.11
   272–275. Springer (2011). URL https://doi.org/10.1007/       18. Jacobs, S., Bloem, R., Colange, M., Faymonville, P.,
   978-3-642-19835-9 25                                             Finkbeiner, B., Khalimov, A., Klein, F., Luttenberger,
9. Faymonville, P., Finkbeiner, B., Tentrup, L.: BoSy: An           M., Meyer, P.J., Michaud, T., Sakr, M., Sickert, S., Ten-
   Experimentation Framework for Bounded Synthesis. In:             trup, L., Walker, A.: The 5th Reactive Synthesis Com-
   R. Majumdar, V. Kuncak (eds.) Computer Aided Verifi-             petition (SYNTCOMP 2018): Benchmarks, Participants
Specification Decomposition for Reactive Synthesis                                                                   17

    & Results. CoRR abs/1904.07736 (2019). URL http:              Tools Technol. Transf. 15(5-6), 433–454 (2013).   URL
    //arxiv.org/abs/1904.07736                                    https://doi.org/10.1007/s10009-012-0224-3
19. Jacobs, S., Klein, F., Schirmer, S.: A High-level LTL Syn-
    thesis Format: TLSF v1.1. In: R. Piskac, R. Dimitrova
    (eds.) Fifth Workshop on Synthesis, SYNT@CAV 2016.
    Proceedings, EPTCS, vol. 229, pp. 112–132 (2016). URL
    https://doi.org/10.4204/EPTCS.229.10
20. Jobstmann, B.: Applications and Optimizations for LTL
    Synthesis. Ph.D. thesis, Graz University of Technology
    (2007)
21. Kupferman, O., Piterman, N., Vardi, M.Y.: Safraless
    Compositional Synthesis. In: T. Ball, R.B. Jones (eds.)
    Computer Aided Verification, 18th International Con-
    ference, CAV 2006. Proceedings, Lecture Notes in Com-
    puter Science, vol. 4144, pp. 31–44. Springer (2006). URL
    https://doi.org/10.1007/11817963 6
22. Kupferman, O., Vardi, M.Y.: Safraless Decision Proce-
    dures. In: 46th Annual IEEE Symposium on Founda-
    tions of Computer Science (FOCS) 2005. Proceedings,
    pp. 531–542. IEEE Computer Society (2005)
23. Majumdar, R., Mallik, K., Schmuck, A., Zufferey, D.:
    Assume-Guarantee Distributed Synthesis. IEEE Trans.
    Comput. Aided Des. Integr. Circuits Syst. 39(11), 3215–
    3226 (2020). URL https://doi.org/10.1109/TCAD.2020.
    3012641
24. Mavridou, A., Katis, A., Giannakopoulou, D., Kooi, D.,
    Pressburger, T., Whalen, M.W.: From partial to global
    assume-guarantee contracts: Compositional realizability
    analysis in FRET. In: M. Huisman, C.S. Pasareanu,
    N. Zhan (eds.) Formal Methods - 24th International
    Symposium, FM 2021, Virtual Event, November 20-26,
    2021, Proceedings, Lecture Notes in Computer Science,
    vol. 13047, pp. 503–523. Springer (2021). URL https:
    //doi.org/10.1007/978-3-030-90870-6 27
25. Meyer, P.J., Sickert, S., Luttenberger, M.: Strix: Ex-
    plicit Reactive Synthesis Strikes Back! In: H. Chock-
    ler, G. Weissenbacher (eds.) Computer Aided Verifica-
    tion - 30th International Conference, CAV 2018, Held
    as Part of the Federated Logic Conference, FloC 2018.
    Proceedings, Part I, Lecture Notes in Computer Science,
    vol. 10981, pp. 578–586. Springer (2018). URL https:
    //doi.org/10.1007/978-3-319-96145-3 31
26. Michaud, T., Colange, M.: Reactive synthesis from LTL
    specification with Spot. In: 7th Workshop on Synthe-
    sis, SYNT@CAV (2018). URL https://www.lrde.epita.
    fr/dload/papers/michaud.18.synt.pdf
27. Pérez, G.A.: The Extended HOA Format for Synthesis.
    CoRR abs/1912.05793 (2019). URL http://arxiv.org/
    abs/1912.05793
28. Pnueli, A.: The Temporal Logic of Programs. In: Annual
    Symposium on Foundations of Computer Science, 1977,
    pp. 46–57. IEEE Computer Society (1977)
29. Pnueli, A., Rosner, R.: On the Synthesis of a Reactive
    Module. In: Conference Record of the Sixteenth An-
    nual ACM Symposium on Principles of Programming
    Languages 1989, pp. 179–190. ACM Press (1989). URL
    https://doi.org/10.1145/75277.75293
30. Renkin, F., Duret-Lutz, A., Schlehuber, P., Pommellet,
    A.: Improvements to ltlsynt. In: 10th Workshop on
    Synthesis, SYNT@CAV (2021). URL https://www.lrde.
    epita.fr/∼frenkin/publications/syntcomp21.pdf
31. de Roever, W.P., Langmaack, H., Pnueli, A. (eds.): Com-
    positionality: The Significant Difference, COMPOS 1997,
    Lecture Notes in Computer Science, vol. 1536. Springer
    (1998). URL https://doi.org/10.1007/3-540-49213-5
32. Sohail, S., Somenzi, F.: Safety First: A two-stage Algo-
    rithm for the Synthesis of Reactive Systems. Int. J. Softw.
