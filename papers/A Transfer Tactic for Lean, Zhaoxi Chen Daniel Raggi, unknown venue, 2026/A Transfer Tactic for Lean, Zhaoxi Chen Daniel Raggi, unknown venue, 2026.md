                                                                             A Transfer Tactic for Lean
                                                                   Zhaoxi Chen                                                       Daniel Raggi
                                                            fourfours1234@gmail.com                                               dr495@cam.ac.uk
                                                             Independent Researcher                                            University of Cambridge
                                                             Great Neck, United States                                        Cambridge, United Kingdom

                                         Abstract                                                               from Huet’s semi-decision algorithm [8]. The rule compo-
                                         Rewriting in proof assistants spans a strict hierarchy. Equa-          sition machinery of Section 2 uses restricted higher order
                                         tional rewriting substitutes based on extensional equality;            unification.
                                         subequational rewriting substitutes based on homogeneous
                                                                                                                1.2   Rewriting beyond equality
                                         relations such as ≤ or ⊆, justified by monotonicity lemmas;
                                         and generalized rewriting relates different operations across          Sometimes we want to substitute under a relation weaker
arXiv:2609.32115v1 [cs.LO] 26 Sep 2026




                                         different types, justified by transfer rules. All three are spe-       than equality. Knowing 𝑃 → 𝑄, we would like to pass from
                                         cializations of one schema, the function relator (𝑅 ⇒ 𝑆) 𝑓 𝑔.          𝑃 ∧ 𝑅 to 𝑄 ∧ 𝑅, or knowing 𝐴 ⊆ 𝐵, we would like to conclude
                                         Lean 4’s rw and Mathlib’s grw/gcongr implement the first               𝐴 ∪ 𝐶 ⊆ 𝐵 ∪ 𝐶. In each case we “rewrote” using relations →
                                         two levels, but the third has had no Lean implementation. We           or ⊆ instead of the stronger =. For such an operation to be
                                         present one: a transfer tactic family over a tagged rule data-         valid, the surrounding context must respect the relation. We
                                         base, benchmarked using Mathlib’s own test suites, of which            say that a function 𝑓 respects the relation 𝑆 provided 𝑆 (𝑥, 𝑦)
                                         112 of 178 ported tests close through the transfer engine. An          implies 𝑆 (𝑓 (𝑥), 𝑓 (𝑦)). In our example, the function (_ ∧ 𝑅)
                                         evaluation of the design’s three motivating hypotheses re-             respects → since 𝑃 → 𝑄 implies (𝑃 ∧ 𝑅) → (𝑄 ∧ 𝑅). This
                                         turns a mixed result: generality holds, authoring effort wins          can easily be generalized to a pair of relations, saying that
                                         in its amortized form (averaged per use), but on dependency            𝑓 respects the pair 𝑅, 𝑆 if 𝑅(𝑥, 𝑦) implies 𝑆 (𝑓 (𝑥), 𝑓 (𝑦)). The
                                         footprint, transfer only ties a mature library and loses on            type theoretic account of rewriting modulo such respectful-
                                         coercions. This shows that transfer’s value is concentrated            ness is due to Sozeau [16], whose implementation underlies
                                         on transferring into domains where few theorems exist.                 Coq’s setoid_rewrite. Moving forward we will use the
                                                                                                                convention of writing 𝑓 𝑥 instead of 𝑓 (𝑥) and 𝑅 𝑥 𝑦 instead
                                         Keywords: interactive theorem proving, Lean, generalized               of 𝑅(𝑥, 𝑦), in line with type-theoretic conventions.
                                         rewriting
                                                                                                                1.3   The function relator and hierarchy
                                                                                                                All of the above are instances of one schema. Given relations
                                         1     Introduction: three levels of rewriting                          𝑅 : 𝛼 → 𝛽 → Prop and 𝑆 : 𝛾 → 𝛿 → Prop, the function
                                         1.1   Rewriting with equations                                         relator ⇒ is defined by
                                         Rewriting plays a large role in formal proof. If we know                      (𝑅 ⇒ 𝑆) 𝑓 𝑔 := ∀𝑥 𝑦, 𝑅 𝑥 𝑦 → 𝑆 (𝑓 𝑥) (𝑔 𝑦),
                                         𝑡 1 = 𝑡 2 and we know some formula 𝜙 (𝑡 1 ), we should be able
                                                                                                                meaning 𝑓 and 𝑔 map 𝑅-related arguments to 𝑆-related
                                         to conclude 𝜙 (𝑡 2 ). Captured as an inference rule,
                                                                                                                values. (In Mathlib this is Relator.LiftFun, and multi-
                                                          𝑡1 = 𝑡2        𝜙 (𝑡 1 )                               argument functions chain the relator as in (𝑅 ⇒ 𝑆 ⇒ 𝑇 ) 𝑓 𝑔.)
                                                                                  (rewrite)                     The associated elimination rule provides the ability to
                                                                𝜙 (𝑡 2 )
                                                                                                                conclude 𝑆 (𝑓 𝑥) (𝑔 𝑦) from (𝑅 ⇒ 𝑆) 𝑓 𝑔 and 𝑅 𝑥 𝑦:
                                         is the substitution of equals for equals, sometimes called                             (𝑅 ⇒ 𝑆) 𝑓 𝑔      𝑅𝑥𝑦
                                         Leibniz’s law. In practice, the equalities are universally quan-                                            (⇒ e)
                                                                                                                                    𝑆 (𝑓 𝑥) (𝑔 𝑦)
                                         tified rules such as ∀𝑥 (𝑥 + 0 = 𝑥), and applying one means
                                                                                                                   Three specializations of this schema, ordered by the num-
                                         finding a substitution z𝜎 that maps the rule’s left-hand side
                                                                                                                ber of parameters that are allowed to vary, give rise to three
                                         onto a subterm of the goal. This process is called pattern
                                                                                                                levels of rewriting.
                                         matching when only the rule contains variables, but it is
                                         called unification in general.                                            The equational level. The expression (= ⇒ · · · ⇒
                                            First order unification is well behaved: when a unifier ex-         =) 𝑓 𝑓 characterizes extensional equality for 𝑓 . It holds
                                         ists there is a most general one, unique up to renaming, and           for any 𝑛-ary function 𝑓 , as it simply states that replacing
                                         it can be computed in near linear time [12, 15]. Higher order          the arguments of 𝑓 for equals yields equal values. Thus,
                                         unification, where variables may stand for functions, is not:          equational rewriting is a special case of the use of ⇒. For
                                         second order unification [5, 7] and even third order pattern           instance, the theorem (= ⇒ =) 𝑓 𝑓 and the premise 𝑥 = 𝑦
                                         matching [11] are undecidable. Proof assistants therefore              can be used to derive 𝑓 (𝑥) = 𝑓 (𝑦). If 𝑓 (𝑥) is a proposition,
                                         use heuristic procedures that may not terminate, descending            𝑓 (𝑥) = 𝑓 (𝑦) states equivalence, so 𝑓 (𝑥) and 𝑥 = 𝑦 can be
                                                                                                            1
                                                                                                             Zhaoxi Chen and Daniel Raggi


Level           Schema instance       Type of fact                                  Authoring cost                             Tactic
Equational      (= ⇒ · · · ⇒ =) 𝑓 𝑓   theorem, for every 𝑓                          zero                                       rw
Subequational   (𝑅 ⇒ 𝑅 ′ ) 𝑓 𝑓        monotonicity, proved and tagged               one lemma per function                     grw
Generalized     (𝑅 ⇒ 𝑆) 𝑓 𝑔           transfer rule                                 one rule per pair                          transfer
Table 1. Three levels of rewriting as three specializations of the function relator. gcongr is the congruence engine behind grw,
and the transfer family comprises transfer, transfer_rw, transfer_back and btransfer.



used to conclude 𝑓 (𝑦). In Lean, equational rewriting is                gcongr/grw implements (𝑅 ⇒ 𝑅 ′ ) 𝑓 𝑓 for homogeneous re-
implemented in the tactic rw.                                           lations, and quotients implement (𝑄 ⇒ 𝑄) for quotient
                                                                        surjections 𝑄, but there is currently no implementation of
   The subequational level. The expression (𝑅 ⇒ 𝑆) 𝑓 𝑓
                                                                        the general (𝑅 ⇒ 𝑆) 𝑓 𝑔 framework.
(often 𝑅 = 𝑆) states a monotonicity fact about 𝑓 that holds
for some relations 𝑅, 𝑆. As shown above, this is a theorem              1.6     Contributions
when 𝑅 and 𝑆 are the equality relation, but otherwise they
are not necessarily true. We call this level subequational as           This paper makes three contributions.
it may hold for relations that are weaker than equality such                  1. An account of the hierarchy: equational, subequa-
as preorders. In practice, reflexivity closes the untouched                      tional, and generalized rewriting as three specializa-
argument positions during congruence descent, while tran-                        tions of one schema.
sitivity allows consecutive rewrite steps to chain. This is the               2. An implementation of the generalized level
level at which we can use 𝑃 → 𝑄 and 𝑃 ∧ 𝑅 to conclude                            for Lean 4 (Section 2): the transfer tactic fam-
𝑄 ∧ 𝑅. In Lean, subequational rewriting is implemented in                        ily (transfer, transfer_rw, transfer_back, and
the tactics grw and gcong.                                                       btransfer) over a tagged rule database. It consumes
                                                                                 the @[gcongr] lemma database directly, reuses grw’s
   The generalized level. Expressions of the form (𝑅 ⇒                           occurrence abstraction, and is benchmarked using
𝑆) 𝑓 𝑔, called transfer rules, represent the most general level                  Mathlib’s own test suites.
of rewriting. Because the domains of 𝑓 and 𝑔 can be different,                3. An evaluation (Section 3) of proof size, authoring
the relations at this level can relate different types, enabling                 effort, and generality.
change of representation transformations. In this paper we
present our implementation of a family of tactics that do               Efforts to automate change of representation transformations
this.                                                                   have already been completed in Isabelle [13, 14] using its
                                                                        Transfer package [9].
1.4     A note on names
Mathlib’s grw tactic is documented as “generalized rewriting”           2     The transfer tactic family
because it generalizes rw from = to other relations. In this            Our implementation of the generalized level consists of a
paper, however, grw occupies the subequational level because            tagged rule database and a family of tactics that consume
it cannot transfer between domains. For the rest of the paper,          it. The precursor of our tactic design is Isabelle’s Transfer
we will leave Mathlib’s tactic names as they are and use the            package [9]. Later we will describe how the system relates
paper’s taxonomy when explaining concepts.                              to Mathlib’s gcongr/grw.

1.5     The Lean 4 landscape                                            2.1     Transfer rules and attributes
Lean 4 [4] and its mathematical library Mathlib [19] have               A transfer rule is a theorem whose statement is a function-
powerful rewriting tools, but they don’t cover all levels of            relator fact, registered with the tactic by an attribute. Math-
the hierarchy.                                                          lib’s Relator.LiftFun acts as a foundation for this. The
   What exists. rw rewrites from equality. gcongr (“general-            elimination principle is function application: given the terms
ized congruence”) [1] applies tagged monotonicity lemmas                h : (R ⇒ S) f g and r : R x y, the application h r proves
to reduce a relational goal to subgoals between the inputs,             S (f x) (g y).
while side conditions are handled by an extensible discharger.             Relations that act as bridges between domains, or rep-
grw [20] is the rewriting tool built on gcongr. Finally, Lean           resentations of mathematical objects, are registered with
defines quotient types for equivalence relations.                       @[transfer_relation]. Standard rules are tagged with ei-
   What does not exist. Lean has no user-defined morphisms              ther @[transfer_rule] or @[transfer_back_rule], and the
of the kind Coq provides via setoid_rewrite [16] and no                 remaining auxiliary pools are @[transfer_respects], its fall-
translation across domains of the kind Isabelle provides                back variant for decomposing structured predicates, and
via its Transfer package [9]. rw implements (= ⇒ =) 𝑓 𝑓 ,               @[btransfer_rule] for the backtracking engine below. All
                                                                   2
A Transfer Tactic for Lean


categories live in a single environment extension, and the                                 ((· + ·) : Z → Z → Z) := by
rules have numerical priorities. For example, the cardinality            intro n1 z1 h1 n2 z2 h2
bridge puts its bijection-reduction rule at priority 2100 so             change ((n1 + n2 : N) : Z) = z1 + z2
that, to prove equality of cardinalities, exhibiting a bijection         unfold NZ at h1 h2 ; subst h1 ; subst h2
outranks an attempt at direct equality transfer:                         exact @Nat.cast_add Z _ n1 n2
@[transfer_back_rule 2100, btransfer_rule]                             Not every operation transfers unconditionally. Natural-
theorem rel_card_bij (hA : Card A n) (hB : Card B m)                   number subtraction is truncated (𝑎 − 𝑏 = 0 when 𝑎 < 𝑏),
    (h : Nonempty (A ≃ B)) : n = m                                     so the tagged rule carries a precondition that becomes a
The premise is to reduce an equality of numbers to a bijection         subgoal at application time and closes from a matching
between the witnessing finite sets. The transfer_back_rule             hypothesis in context:
tag serves both the regular and the backtracking engine, but           @[transfer_rule]
the set priority only matters to the regular engine, as the            theorem rel_nat_sub :
backtracking one recovers from the wrong choice and thus                   ∀ {{n1 z1 }}, NZ n1 z1 → ∀ {{n2 z2 }}, NZ n2 z2 →
does not need to be steered away from it.                                  n2 ≤ n1 → NZ (n1 - n2 ) (z1 - z2 )
   Within a bridge, rules cluster into recurring shapes: ground
facts relating closed forms (BP 1 0: the number 1 corresponds          Order transfers through rel_le : (NZ ⇒ NZ ⇒ Iff) (· ≤
to the empty bag); structural rules relating operations argu-            ·) (· ≤ ·). The Iff-conclusion rule cannot be directly ap-
ment by argument; uniqueness and totality facts (left/right-           plied to the goal z1 ≤ z2 (the conclusion _ ↔ _ does not
unique, left/right-total and their combinations), which enable         unify with _ ≤ _), so the database also includes the arrow
equality and existential transfer; and one-way equality lem-           variant rel_le_mp, derived by .mp, which is what backward
mas (rel_eq_mp needs only RightUnique R for the forward                chaining actually uses. Finally, four facts fix what we call
direction, and rel_eq_mpr only LeftUnique R for the back-              the bridge’s grade. Left-totality, left-uniqueness and right-
ward direction, refining Mathlib’s Relator.rel_eq).                    uniqueness all hold and characterize the bridge as a partial
   Crucially, nothing constrains the two function slots to             bijection. Right-totality fails because NZ cannot apply to neg-
look alike. The bags-of-primes bridge relates a number to              ative integers, which have no preimage. Which of these theo-
the multiset of its prime factors:                                     rems are tagged is decided not necessarily by their truth, but
                                                                       also by their consequences. RightUnique NZ unfolds to b = c
BP : N → Multiset N → Prop                                             with metavariables on both sides, and since NZ n z is defini-
(BP ⇒ BP ⇒ BP) (· * ·) (· + ·) -- mult. ↦→ bag union                   tionally (n : Z) = z, the rule matches the very subgoals it
(BP ⇒ BP ⇒ Iff) (· | ·) (· ≤ ·) -- dvd ↦→ multiset                     generates; tagging it would send the search into a regress.
    order                                                              Both uniqueness directions are therefore kept as proof terms
This exemplifies the heterogeneity that Section 1.3 identified         only, and their conjunction nz_bi_unique : BiUnique NZ is
as the defining feature of the generalized level.                      tagged in their place, carrying the same content behind a
   One family of facts is never tagged: the equational congru-         head symbol the index can discriminate on. In the same
ences (= ⇒ · · · ⇒ =) 𝑓 𝑓 , which hold for every 𝑓 at every            way as rel_le_mp’s constraint, what the database can hold
arity. Tagging them per function would fill the database with          is shaped by what the search can handle.
facts that carry no information.                                           In use, the rules compose without being named. Nested
                                                                       arithmetic decomposes through rel_mul and rel_add down
2.2    A complete bridge                                               to the context hypotheses:
One bridge in the repository relates a natural number to               example (a b c : N) (a' b' c' : Z)
its integer coercion, and is small enough to show almost                   (ha : NZ a a') (hb : NZ b b') (hc : NZ c c') :
entirely. The relation and its ground facts form three lines:              NZ (a * b + c) (a' * b' + c') := by transfer
@[transfer_relation]                                                   The derivation tree and the tactic call coincide. Below is
def NZ (n : N) (z : Z) : Prop := (n : Z) = z                           the same order-transfer fact, written first as two explicit
                                                                       elimination steps and then as the tactic that finds them:
@[transfer_rule] theorem rel_zero : NZ 0 0 := rfl
@[transfer_rule] theorem rel_one : NZ 1 1 := rfl                       example (n1 n2 : N) (z1 z2 : Z) (h1 : NZ n1 z1 )
                                                                           (h2 : NZ n2 z2 ) (hle : n1 ≤ n2 ) : z1 ≤ z2 :=
A structural rule states that an operation respects the bridge,          (rel_le h1 h2 ).mp hle   -- two (⇒E) steps, then mp
and its proof is the authoring cost of covering that operation:
@[transfer_rule]                                                       example (n1 n2 : N) (z1 z2 : Z) (h1 : NZ n1 z1 )
theorem rel_add :                                                          (h2 : NZ n2 z2 ) (hle : n1 ≤ n2 ) : z1 ≤ z2 := by
    (NZ ⇒ NZ ⇒ NZ) ((· + ·) : N → N → N)                                 transfer
                                                                   3
                                                                                                             Zhaoxi Chen and Daniel Raggi


transfer_back performs the zify-style translation in                     a wrong rule choice fails downstream instead of succeeding
reverse: on a N-side goal it leaves the Z-side goal, pushing             with a residual. Back-rules come from @[btransfer_rule]
casts through compound expressions because the structural                alongside the shared decomposition pools.
rules decompose the witness subgoal NZ (n + m) ?z into
per-argument witnesses before reflexivity fires. Therefore,              2.4   A worked derivation
?z unifies to ↑n + ↑m rather than ↑(n + m):                              The tactics automate the mechanical composition of elimi-
example (n m k : N)                                                      nation steps. Consider the bags-of-primes bridge with two
    (hz : (↑n : Z) + ↑m ≤ ↑k) : n + m ≤ k := by                          ground facts and one structural rule:
  transfer_back                                                                      BP 6 {2, 3},     BP 120 {2, 2, 2, 3, 5},
  exact hz
                                                                                          (BP ⇒ BP ⇒ ←) (|) (≤),

2.3   The tactics                                                        where ← stands for backward implication and ≤ for mul-
                                                                         tiset order/inclusion. Applying the elimination rule to the
Four tactics (with variants) consume the database.                       structural rule and the first ground fact specializes the first
   transfer: Engine-driven backward chaining over the                    argument slot, and applying it again with the second ground
tagged rules and Mathlib’s @[gcongr] database (Section 2.7).             fact specializes the second, leaving
The engine uses discrimination trees, performing indexed                               {2, 3} ≤ {2, 2, 2, 3, 5} → 6 | 120.
candidate lookup with backtracking on failed rule applica-
tions. It tries to close the goal up to content residuals, or sub-       The same composition works for any combination of rules.
goals (such as Nonempty (A ≃ B)) that are left open. Direct              The transfer tactics build such derivation trees automati-
congruence descent with equality is possible, so ordinary                cally. An example on a live goal is that from Nat.gcd m n | m,
rewriting is subsumed as the 𝑅 = = instance of transfer.                 transfer produces PF m ∩ PF n ≤ PF m, where the gcd-to-
The variant called transfer to T skews the search toward a               intersection and divisibility-to-order steps each come from
named target type so that within each priority level, rules              a tagged rule.
whose statement mentions T more often are tried first.
                                                                         2.5   Transfer in a live proof
   transfer_back: Goal translation in the opposite direc-                Quotient bridges are easy to use transfer with. The relation
tion. A goal stated in the target representation is reduced,             ZM n : Z → ZMod n → Prop relates an integer to its residue
via the @[transfer_back_rule] category, to the correspond-               modulo 𝑛 and is right-total and right-unique but not left-
ing goal in the source representation, which remains as the              unique, meaning equality transfers forward only. With its
residual (together with any side conditions that the rules               structural rules tagged, the classic impossibility argument
could not discharge). transfer_back to T is the correspond-              that no integer squares to 3 runs as a one-call reduction
ing search filter, and transfer_at h applies the translation             modulo 5 followed by a finite check:
to a hypothesis instead of the goal.
                                                                         example : ¬ ∃ z : Z, z * z = 3 := by
   transfer_rw: Generalized rewriting via the transfer en-                 rintro ⟨z, hz⟩
gine, with the same idea as Mathlib’s grw. transfer_rw [h1 ,               have h5 : ((z * z : Z) : ZMod 5)
← h2 ] (at h)? rewrites with relational hypotheses h𝑖 : R𝑖                         = ((3 : Z) : ZMod 5) := by transfer
a𝑖 b𝑖 for any binary relation, replacing occurrences of 𝑎𝑖 with            push_cast at h5
𝑏𝑖 in the goal or a hypothesis and trying to close by reflexiv-            have : ∀ x : ZMod 5, x * x ≠ 3 := by decide
ity. The front end copies the occurrence abstraction design                exact this _ h5
of Lean.MVarId.grewrite, but the implication is proved by
                                                                         The transfer call discharges the casting step, and the ZM-
the transfer engine (native rules, the gcongr adapter, and
                                                                         multiplication and forward equality rules compose to carry
a transitivity fallback) rather than by gcongr itself. Exactly
                                                                         hz across the bridge. What would otherwise be a hand-picked
as in the case of grw, Lean’s own rewriter is used for =/↔
                                                                         chain of Int.cast lemmas is one uniform call, and the re-
rules. For heterogeneous rules h : T a b with a : 𝛼 and
                                                                         maining goal is decidable.
b : 𝛽 of different types, where occurrence substitution is
poorly defined, the tactic falls back to goal transfer with h            2.6   Backward transfer and content residuals
seeded as a leaf. Mathlib’s grw is left available for side-by-side
                                                                         In transfer_back, the engine performs the bookkeeping
comparison.
                                                                         while the mathematical content remains open. The car-
  btransfer: Goal translation with backtracking. Where                   dinality bridge’s comparison back-rules are an example.
transfer and transfer_back accept residuals, btransfer re-               rel_card_bij (Section 2.1) reduces a numeric equality to a
quires every subgoal to close except Nonempty-headed con-                bijection between the witnessing finite sets, and its siblings
tent residuals. This is what makes its backtracking effective:           reduce the inequalities to an injection or surjection:
                                                                     4
A Transfer Tactic for Lean


@[transfer_back_rule, btransfer_rule]                                          queries the gcongr environment extension with its
theorem rel_card_inj (hA : Card A n) (hB : Card B m)                           own key, making roughly 700 monotonicity lemmas
    (h : Nonempty (A ↩→ B)) : n ≤ m                                            usable without re-tagging. The gcongr tactic itself is
                                              
On the symmetry of binomial coefficients, 𝑛𝑘 = 𝑛−𝑘    𝑛                       never called on goals, but its discharger is used for
for 𝑘 ≤ 𝑛, the division works as intended. transfer_back                       side conditions such as positivity.
fires rel_card_bij on the equality, decomposes both sides                   2. Skeleton: transfer_rw reuses grw’s occurrence ab-
through the 𝑘-subset structural rule down to a shared                          straction, with the transfer engine proving the result-
canonical witness set 𝑆 of size 𝑛, and leaves as the sole                      ing implication. The earlier rewriting front end was
residual                                                                       retired in its favor.
                                                                            3. Benchmark: The system is passed through Mathlib’s
⊢ Nonempty (powersetCard k S ≃                                                 own test suites for gcongr and grw, ported to a parity
            powersetCard (n - k) S)                                            suite (Section 3.3). In the deferred cases, parity files
which is discharged by the actual complement bijection, with                   still run the original tactics, so both systems remain
no cardinality arithmetic anywhere in the user’s proof.                        live.
def complEquiv [DecidableEq 𝛼] (S : Finset 𝛼)                           A summary is that the transfer engine subsumes
    {k m : N} (hS : S.card = m) (hk : k ≤ m) :                        grw/gcongr by consuming its rule database and reproducing
    ↑(S.powersetCard k) ≃ ↑(S.powersetCard (m - k))                   its test suites. It is neither a parallel system nor a wrapper
                                𝑛                                    around Mathlib’s tactics. This framing clears up the
The same mechanism unlocks      𝑘 ≤ 2 , as the injection rule
                                     𝑛

reduces it to the inclusion embedding of 𝑘-subsets into the           generality comparison of Section 3, which uses the same
powerset, an inequality the forward-only monotonicity route           lemma database and the same tests.
rejects.
                                                                      2.8     Outlook: refinement is a bridge
                                 𝑛     𝑛 
   Pascal’s recurrence, 𝑛+1
                          𝑘+1 = 𝑘 + 𝑘+1 , marks the bound-
ary of transfer_back. The combinatorial proof is a hybrid             A data refinement relation is a bridge. Where the transfor-
in that the (𝑘+1)-subsets of insert x s split into those              mations of this paper relate two representations of a math-
not containing 𝑥 (counted directly) and those containing              ematical object, a refinement relation R : Impl → Spec →
𝑥 (counted through the insert x bijection), so the identity            Prop relates a program state to the abstract value it imple-
needs the disjoint-union rule and rel_card_bij together.              ments; operations preserved by the refinement are exactly
What transfer_back actually does is fire rel_card_bij first,          relator facts (𝑅 ⇒ 𝑅) opimpl opspec , observations are (𝑅 ⇒ =)
after which the low-priority canonical-witness rule closes            facts, and invariant-guarded operations take the precondi-
the right-hand Card witness before the sum can decompose,             tion shape of rel_nat_sub (Section 2.2). The classic batched
and no backtracking revisits this. The residual becomes a             queue is a pair of lists refining a single list, with amortized-
bijection into an arbitrary canonical set of the right size,          constant enqueue. We sketch the bridge in the framework’s
dischargeable only by equating cardinalities. The proof state         notation, with each rule being a two-line list lemma:
falsely progresses since transfer essentially reduces Pascal
to itself. Lifting the partition lemma to a tagged rule does          @[transfer_relation]
not change the route; the shortcut fires before structural            def RQ (p : List 𝛼 × List 𝛼) (q : List 𝛼) : Prop :=
decomposition is attempted. In this case, the tactic’s search           p.1 ++ p.2.reverse = q
success criterion is the obstruction. transfer_back treats a
rule as successful once it applies and the recursion continues.       @[transfer_rule] theorem rel_empty : RQ ([], []) []
A choice that leaves a residual does not fail, so it never
triggers a backtrack. On the other hand, btransfer requires           @[transfer_rule] -- enqueue: cons on the back list
every subgoal to close except Nonempty-headed content                 theorem rel_enq (x : 𝛼) :
residuals, so the wrong choice fails downstream and the                   (RQ ⇒ RQ) (fun p => (p.1, x :: p.2))
search backtracks. In Pascal’s case, it backtracks to the                           (fun q => q ++ [x])
partition rule and closes it over the same database.
                                                                      @[transfer_rule] -- dequeue, guarded by nonemptiness
2.7    Relationship to gcongr and grw                                 theorem rel_deq :
The system began fully independent of Mathlib’s subequa-                  ∀ {{p q}}, RQ p q → p.1 ≠ [] →
tional level machinery, containing its own search, rule cat-              RQ (p.1.tail, p.2) q.tail
egories, and rewriting front end. It is now integrated with
Mathlib in three different ways:                                      theorem rebalance : -- two states, one queue
    1. Database: The engine consumes Mathlib’s @[gcongr]                  ∀ {{b q}}, RQ ([], b) q → RQ (b.reverse, []) q
       lemma database in the following way: an adapter
                                                                  5
                                                                                                              Zhaoxi Chen and Daniel Raggi


The relation’s grade is interesting. RQ is left-total (every pair       can conceal a detour through the typeclass instance tower.
abstracts to something), right-total (every queue is imple-             The first two metrics remain informative about authoring
mented, by (q, [])), and right-unique (each state imple-                effort (H2), where the use site cost is at issue, with the caveat
ments one queue), but not left-unique, as rebalance exhibits            just stated for the first. For footprint we separate fixed cost
two states implementing the same queue. That is the grade               (the bridge) from marginal cost (each new theorem), and the
of the quotient row of Table 1, and the consequences are                headline metric is amortized—a bridge of 𝑅 rules closing 𝑇
that equality transfers from implementation to specification            theorems costs 𝑅/𝑇 rules per theorem, and we track whether
only, and two states with equal abstractions are observation-           that investment pays off as cumulative union proof-graph
ally equal without actually being equal. Refinement is the              size |𝐺 | against corpus size 𝑘.
quotient pattern read operationally. Proofs then flow in the
refinement direction. transfer_back, on an implementation-              3.1   H1: proof size and dependency footprint
side goal, leaves the specification-side goal, so correctness is          Evidence for. Three cardinality theorems proved by
proved against the abstract queue once and then transported             transfer have individual proof graphs of 4483, 2565,
to the batched one.                                                     and 3431 declarations, but due to reuse, the size of their
   The bridge above is a sketch and is not part of the corpus           combined graph is only 4739. Theorems using the same
evaluated in Section 3. The identification itself is established        bridge share a big part of their whole graph, so the marginal
practice elsewhere—Isabelle’s data refinement is built on               cost of an additional theorem collapses.
the same Lifting/Transfer machinery [6, 9], and CoqEAL’s
“refinements for free” brings refinement-by-relations to Coq               Evidence against. The break-even experiments return
with the same relator discipline [3]. The point of the sketch           negatives. Six distinct cardinality identities, each proved on
is that the framework of this paper expresses it with no new            the same goal by both transfer and a hand proof using Math-
machinery, and a refinement is one more entry in the bridge             lib’s card_* lemmas, give cumulative union proof-graphs
catalogue.                                                              that are nearly identical. The six identities count powersets,
                                                                        products, and their compositions: |P (𝑠)| = 2𝑛 , |𝑠 × 𝑡 | = 𝑛𝑚,
3    Evaluation                                                         |P (𝑠 × 𝑡)| = 2𝑛𝑚 , |P (𝑠) × P (𝑡)| = 2𝑛 · 2𝑚 , |P (P (𝑠))| = 22 ,
                                                                                                                                        𝑛


The design was motivated by three hypotheses:                           and |P (𝑠) × 𝑡 | = 2𝑛 · 𝑚.
    H1 (proof size). Transfer shortens proofs that cross do-               The same experiment on the structurally different bags-
       mains.                                                           of-primes bridge (non-injective, predicated totality, multiset-
    H2 (authoring effort). Transfer reduces the invest-                 valued) reproduces the result. A bridge’s rules are proved
       ment needed to build proofs.                                     from the same library lemmas an incumbent hand proof uses,
    H3 (generality). Transfer subsumes rw/grw/gcongr.                   so the two dependency graphs share their core. A footprint
                                                                        win therefore requires a domain where the incumbent rein-
We evaluate each against the repository’s corpora: a baseline
                                                                        vents the machinery of each theorem—which does not arise
of nine bridge modules with 118 in-file examples, single-
                                                                        when the incumbent has reusable lemmas, as is the common
theorem case studies, two break-even families measuring
                                                                        case in Mathlib.
dependency footprint as a corpus grows, a pre-registered grid
                                                                           The coercion class is another negative. On a pre-registered
on the coercion class, and a 178-test parity suite ported from
                                                                        10-row grid over relations {≤, =} and expression shapes
Mathlib’s own gcongr and grw tests. For each hypothesis we
                                                                        (atom, sums, products, nesting), transfer_back closes all ten
draw a verdict after presenting the evidence for and against.
                                                                        rows, but so do exact_mod_cast and omega, identically. Mean-
   Methodology. We report three metrics that have different             while, transfer requires the N → Z bridge (531 lines, 16
purposes. Raw proof length, which counts the lines of tactic            rules) as a fixed cost that the built-ins do not. On bi-unique
script or proof-term nodes, is the visible cost at the use site.        coercions, where norm_cast is complete, the bridge is purely
Distinct-constant count is the number of distinct constants             overhead. Finally, a decision procedure dominates on decid-
a proof term references. Proof-graph size, written |𝐺 |, is the         able arithmetic fragments, as omega proves a representative
transitive closure of constants used by a proof, terminating at         cast goal with a 133-node term against transfer’s 33497.
axioms. The third metric measures true dependency footprint                Two audits qualify the single-theorem comparisons in
and is the only one on which we judge H1, but even there,               both directions. The binomial gap decomposes into a shared
the granularity matters. A single theorem’s proof-graph size            core of 3245 declarations plus 1238 unique to transfer (but
is dominated by the route its proof takes rather than by                only about 9 from the transfer framework itself) and 396
the tactic that found it, so only cumulative comparisons                unique to the incumbent. However, the incumbent uses an
that use the same route carry evidential weight. However,               algebraic shortcut through the ring hierarchy, an example of
raw length is completely dominated by strategy and can                  how the tactic can be conflated with the mathematical strat-
hide true cost in both directions, as a one-line by transfer            egy. Additionally, proof graph footprint is highly sensitive to
conceals the bridge’s fixed rule set while a short hand proof           proof style, as a single typeclass lemma (add_zero resolving
                                                                    6
A Transfer Tactic for Lean


                                               Card family                         BP family
                              𝑘   transfer |𝐺 | incumbent |𝐺 |        𝑘    transfer |𝐺 | incumbent |𝐺 |
                              1         2565             2564         1           418              417
                              2         2905             2902         2           419              418
                              3         2906             2903         3           420              419
                              4         2907             2904         4           431              429
                              5         2908             2905         5           432              430
                              6         2909             2906         6           433              431
Table 2. Break-even experiments: cumulative union proof-graph size as the corpus grows, transfer vs. hand proofs from library
lemmas (“incumbent”—the established route the library already provides). No crossover on either family.



through an instance tower) added over 1400 declarations into         gcongr adapter, about 700 of Mathlib’s existing monotonic-
a hand proof before being swapped for the targeted multiset          ity lemmas become usable without re-tagging. Authoring
lemma. Fair comparisons must hold the style fixed, which is          style also entails the advantage that bridges supply targeted
something only satisfied by Table 2.                                 ground facts (rel_one : BP 1 0), which structurally avoids
                                                                     the instance-tower detours that inflated the previous hand
   Why single-theorem footprint comparisons do                      proof by 1400 declarations. Finally, the use site is often one
not settle H1. The proof-graph size of 2𝑛 = 𝑘 𝑛𝑘 via
                                                  Í
                                                                     uniform line with no need to know which lemma chain ap-
transfer_back is 4483 compared to 3641 for Mathlib’s                 plies.
incumbent. However, in raw proof length, transfer_back
wins by a factor of five. It uses 751 proof-term nodes refer-           Evidence against. Writing correct rules requires under-
encing 36 distinct constants, compared to 3718 nodes and             standing the relator shapes, and even then it often needs
58 constants for Mathlib’s algebraic Nat.sum_range_choose.           iteration. Priorities are also difficult to set. For example, the
Neither the proof-graph footprint nor the size at the use            cardinality bridge’s bijection rule must be tagged at a pri-
site is evidential for the tactic. The two graphs share a            ority that outranks the generic equality route, but this can
core of 3245 declarations, with 1238 unique to transfer              only be known by seeing the search fail. This can be done
and 396 unique to the incumbent. The remainder is the                only by understanding the computational tools used, not the
List/Multiset substrate that Transfer’s combinatorial route          mathematical semantics. This perhaps suggests the need to
requires, set against the ring hierarchy required by the             weight rules in some systematic, automatic way, but at the
incumbent’s algebraic proof through add_pow. One generic             moment this is infeasible.
monoid lemma (add_zero, resolving through Multiset’s
instance tower) adds 1437 declarations, showing that                   Verdict. H2 holds in its amortized form, with an expertise
footprint is just as sensitive to style. Only same-style             barrier in rule authoring. Similar to H1, the benefit is greatest
cumulative comparisons are meaningful in this respect,               where no reusable incumbent library exists.
which is what Table 2 measures and what we judge H1 on.
   Verdict. H1 fails as stated on well-developed targets:            3.3   H3: generality
transfer ties the incumbent on footprint and loses on                   Evidence for. In principle, the hierarchy of Section 1.3
bi-unique coercions. Where the target theorem already                settles the containment: the 𝑓 = 𝑔 constraint confines
exists, transfer’s advantage is authoring, not footprint             grw/gcongr to homogeneous relations, and every hetero-
(H2), and where it does not exist, there is no incumbent             geneous bridge in the repository is outside their reach by
to amortize against at all. Transfer is better judged as a           construction. For a hypothesis h : T a b across different
transport tool than as a refactoring tool.                           types, occurrence substitution is poorly defined and grw
                                                                     cannot be applied, while transfer_rw falls back to goal
3.2    H2: authoring effort                                          transfer. On the equational side, ordinary rw’s proof term is
   Evidence for. Across nine bridges, the tagged rule cate-          exactly the congruence (= ⇒ · · · ⇒ =) 𝑓 𝑓 applied to the
gories total 114 forward rules (plus 6 low-priority rules and        rewrite equation, so rewriting is the 𝑅 = = instance.
26 backward rules). The bridges themselves total 1527 lines             In practice, the claim is tested by porting Mathlib’s own
of code (3223 raw, including documentation and in-file tests)        test suites for gcongr and grw, with gcongr replaced with
for 117 tagged transfer lemmas. This investment serves the           transfer and grw with transfer_rw.
118-example baseline and the entire parity suite, and the               Of 178 ported tests, 112 close through the production en-
amortization results show 𝑇 grows at near-zero marginal              gine and none fail outright, meaning each deferral is a gap in
footprint, so 𝑅/𝑇 → 0 for a well-exercised bridge. With the          the interface rather than in the engine. The full passes include
                                                                 7
                                                                                                                 Zhaoxi Chen and Daniel Raggi


                             File                  Tests   Via transfer      Def. (UX)   Def. (partial)   Fail
                             GCongrBasic              10                 7          3                0      0
                             GCongrCore               12                 5          7                0      0
                             GCongrImplications       12                 5          7                0      0
                             GCongrInequalities       74                42         20               12      0
                             GCongrMod                17                11          6                0      0
                             GRewrite                 53                42         11                0      0
                             Total                   178               112         54               12      0
Table 3. Parity suite: Mathlib’s gcongr and grw test suites replayed through the transfer engine. Each test either passes via
transfer or carries an explicit deferral tag with the original tactic retained; there are no engine failures.



mixed strict/non-strict rewrite chains, Q → R casts, divis-              value concentrates on transferring into domains where few
ibility rewrites, the at * wildcard with correct self-rewrite            or no target theorems already exist, not on re-deriving what
skipping, and rewriting through a sum-subset chain. In five              a mature library already proves well.
sibling tests the port improved on the original. Side goals that
gcongr left to simp closed under the engine’s own discharger,
collapsing the proofs to a bare transfer.                                4    Related work
   The following is a representative ported test from the                   Transfer in Isabelle/HOL.. The design of the tactics pre-
transparency section of Mathlib’s gcongr suite. The test’s               sented in this paper was inspired by Isabelle’s Transfer pack-
own @[gcongr]-tagged lemma is consumed through the                       age [9], which introduced the tagged-relator paradigm im-
adapter, and the finishing call—originally by gcongr—                    plemented in this paper for Lean, and also from its use for
becomes by transfer with no other change.                                data refinement [6]. The distinction comes from the deep
@[gcongr] lemma mono_measure (h : 𝜈 ≤ 𝜈') :                              differences between Isabelle and Lean. Isabelle’s package
    𝜈 a ≤ 𝜈' a := h a                                                    serves as a foundation for quotient types in HOL, whereas
                                                                         Lean has native Quot for quotient types. The question is how
example (h : 𝜈 ≤ 𝜈') : 𝜈 a ≤ 𝜈' a := by                                  an implementation of transfer in Lean earns back its cost
  transfer   -- original: by gcongr                                      given the preexisting Quot machinery.

  Evidence against. The 54 UX deferrals mark where                          Parametricity-based transfer in Coq. A different ap-
gcongr’s interface is still ahead: template patterns with ?_             proach computes the transfer from the statement’s type struc-
holes for depth control (22 tests), asserted error message               ture rather than from tagged facts. Univalent parametricity
text (10), the rel finishing variant (7), and smaller families           transforms based on type equivalences [17, 18], and Trocq [2]
for implication-hypothesis, binder-naming intro patterns,                generalizes it to a hierarchy of relation classes, so a transfer
explicit recursion depth, occurrence configuration, and                  requires only as much structure as the statement demands
𝑛th-occurrence rewriting. The 12 partial progress deferrals              and univalence is avoided where it is not needed. CoqEAL
expose the consequences of the transfer tactics having an                applies the same relator discipline to program refinement [3].
all-or-nothing principle. Finally, a search based tactic has             A translation is automatic and complete over the fragment it
unpredictable failure modes, requiring understanding of the              covers, but constrains which relations may enter it. A search
rule database for diagnosis.                                             over tagged facts accepts any heterogeneous relation, in-
  Verdict. H3 holds at the engine level. Subsumption is                  cluding bridges whose grade is neither an equivalence nor a
demonstrated on Mathlib’s own tests over the same lemma                  function, but finds only what has been tagged. Trocq’s clas-
database, with no engine failures, and heterogeneity goes                sification of relations by how much equivalence structure
further beyond the subequational tactics.                                they carry is, in spirit, close to the totality and uniqueness
                                                                         grade used in this paper.
3.4   Summary
Generality (H3) is a win because the engine reproduces the                  Cast handling in Lean. norm_cast and its family normal-
subequational test suites and expresses the heterogeneity                ize coercions through a dedicated simp-set discipline [10].
that other tactics lack. Authoring effort (H2) wins in its amor-         On bi-unique coercions, this is the incumbent that transfer
tized form, bounded by an expertise cost in rule authoring.              does not beat (the coercion grid closes under exact_mod_cast
Proof size (H1) is a tie on well-developed targets and a loss            as completely as under transfer_back, and the bridge is pure
on bi-unique coercions, and its failure shows that transfer’s            overhead).
                                                                   8
A Transfer Tactic for Lean


   Syntactic transport in Mathlib. to_additive [19] is one            the target theorem does not yet exist—transport into under-
of Mathlib’s own transfer mechanisms that is its most heav-           developed or better-behaved domains—since there the break-
ily used. It is complementary rather than competing: the              even question against an incumbent does not arise. The
correspondence is fixed and built in, the translation is syn-         boundary drawn by the footprint studies is also a map of
tactic and runs once at declaration time, and it produces new         where to look.
declarations rather than closing goals. The mechanism here               Further developments. Subsequent work on the same en-
is semantic, user-extensible, and applied to a goal mid-proof.        gine, outside the scope of this report, explores treating a
                                                                      transfer relation together with its tagged rules as an exe-
                                                                      cutable analogy between domains: inspecting the correspon-
5     Conclusion                                                      dence a bridge induces, synthesizing the analogue of a given
                                                                      theorem rather than proving a stated one, sweeping a names-
5.1    Summary
                                                                      pace for its transferable fragment, and composing bridges.
This paper set out a strict hierarchy of rewriting—equational,
subequational, generalized—as three specializations of one            5.3    Big picture
schema, the function relator (𝑅 ⇒ 𝑆) 𝑓 𝑔, ordered by the              The ingredients for the generalized level were already
number of parameters that are allowed to vary and, in conse-          present in Lean. There was a typeclass-style attribute
quence, by what each level entails in authoring cost: nothing,        system to play the role of the rule database, an existing
one lemma per function, one rule per pair of operations; in           corpus of some 700 tagged monotonicity lemmas, and a
that order. Lean’s rw and Mathlib’s grw/gcongr occupy the             metaprogramming interface expressive enough to build
first two levels, and the transfer family presented here im-          derivation trees. What was missing was the unifying
plements the third, the first such implementation for Lean 4.         schema. Seen through it, ordinary rewriting, congruence
It is not a parallel system, as the engine consumes Mathlib’s         of inequalities, quotient lifting, and cross-domain transfer
@[gcongr] database directly, reuses grw’s occurrence abstrac-
                                                                      are not four mechanisms but one, at different settings of the
tion, and takes Mathlib’s own test suites as its acceptance           same three parameters—and now a library that has already
bar.                                                                  established its subequational level rule database gets the
    The evaluation returned one clean win, one qualified win,         generalized level’s engine over the same rules.
and one instructive failure. Generality (H3) holds at the en-
gine level: 112 of 178 ported Mathlib tests close through
                                                                      Acknowledgments
the transfer engine, and heterogeneity (different operations
across different types) is beyond the subequational tactics           The implementation, the evaluation corpora, and drafts of
in principle, not merely in practice. Having many (a hun-             this paper were developed with substantial assistance from
dred) tagged rules could in turn serve hundreds of goals, so          Claude (Anthropic), used as a pair-programming and drafting
authoring effort (H2) holds in its amortized form but with            tool under the authors’ direction, and the authors take full
an expertise barrier at rule-writing time. Proof size (H1),           responsibility for the content.
measured by dependency footprint, is a tie against a mature
library and a loss on bi-unique coercions, where norm_cast is         References
already complete. A bridge’s rules are proved from the same            [1] Mario Carneiro, Heather Macbeth, and Jovan Gerbscheid. 2023. The
                                                                           generalized congruence tactic gcongr (Mathlib.Tactic.GCongr).
lemmas a hand proof uses, so footprint parity is structural,
                                                                           Part of the Lean mathematical library (mathlib4). https://leanprover-
and transfer’s value concentrates where the incumbent must                 community.github.io/mathlib4_docs/Mathlib/Tactic/GCongr/Core.
reinvent each theorem.                                                     html.
                                                                       [2] Cyril Cohen, Enzo Crance, and Assia Mahboubi. 2024. Trocq: Proof
                                                                           Transfer for Free, With or Without Univalence. In Programming Lan-
                                                                           guages and Systems — 33rd European Symposium on Programming,
5.2    Future work                                                         ESOP 2024 (Lecture Notes in Computer Science). Springer. doi:10.1007/
Three directions follow directly from the evaluation.                      978-3-031-57262-3_10
   Interface parity. Each parity deferral is an interface gap          [3] Cyril Cohen, Maxime Dénès, and Anders Mörtberg. 2013. Refine-
with an identified path: template patterns for depth control,              ments for Free!. In Certified Programs and Proofs — Third Interna-
                                                                           tional Conference, CPP 2013, Melbourne, VIC, Australia, December 11–
the rel finishing variant, occurrence configuration, and—                  13, 2013, Proceedings (Lecture Notes in Computer Science, Vol. 8307),
most substantively—a progress-tactic mode. The engine al-                  Georges Gonthier and Michael Norrish (Eds.). Springer, 147–162.
ready carries the required contract internally (main versus                doi:10.1007/978-3-319-03545-1_10
side subgoals, loose side-constraints) for transfer_rw; expos-         [4] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem
ing it as a transfer-variant syntax would convert the twelve               Prover and Programming Language. In Automated Deduction — CADE
                                                                           28, 28th International Conference on Automated Deduction, Virtual
partial-progress deferrals.                                                Event, July 12–15, 2021, Proceedings (Lecture Notes in Computer Science,
   Transport targets. The reframing that closed Section 3.1                Vol. 12699), André Platzer and Geoff Sutcliffe (Eds.). Springer, 625–635.
implies that the next thing to do is to evaluate transfer where            doi:10.1007/978-3-030-79876-5_37
                                                                  9
                                                                                                                                Zhaoxi Chen and Daniel Raggi


 [5] Warren D. Goldfarb. 1981. The Undecidability of the Second-Order                [13] Daniel Raggi, Alan Bundy, Gudmund Grov, and Alison Pease. 2015.
     Unification Problem. Theoretical Computer Science 13, 2 (1981), 225–                 Automating Change of Representation for Proofs in Discrete Math-
     230.                                                                                 ematics. In Intelligent Computer Mathematics — International Con-
 [6] Florian Haftmann, Alexander Krauss, Ondřej Kunčar, and Tobias Nip-                   ference, CICM 2015, Washington, DC, USA, July 13–17, 2015, Proceed-
     kow. 2013. Data Refinement in Isabelle/HOL. In Interactive Theorem                   ings (Lecture Notes in Computer Science, Vol. 9150). Springer, 227–242.
     Proving — 4th International Conference, ITP 2013, Rennes, France, July               doi:10.1007/978-3-319-20615-8_15
     22–26, 2013, Proceedings (Lecture Notes in Computer Science, Vol. 7998),        [14] Daniel Raggi, Alan Bundy, Gudmund Grov, and Alison Pease. 2016.
     Sandrine Blazy, Christine Paulin-Mohring, and David Pichardie (Eds.).                Automating Change of Representation for Proofs in Discrete Math-
     Springer, 100–115. doi:10.1007/978-3-642-39634-2_10                                  ematics (Extended Version). Mathematics in Computer Science 10, 4
 [7] Gérard Huet. 1973. The Undecidability of Unification in Third Order                  (2016), 429–457. doi:10.1007/s11786-016-0275-z
     Logic. Information and Control 22, 3 (1973), 257–267.                           [15] John Alan Robinson. 1965. A Machine-Oriented Logic Based on the
 [8] Gérard Huet. 1975. A Unification Algorithm for Typed 𝜆-Calculus.                     Resolution Principle. Journal of the ACM 12, 1 (1965), 23–41. doi:10.
     Theoretical Computer Science 1, 1 (1975), 27–57.                                     1145/321250.321253
 [9] Brian Huffman and Ondřej Kunčar. 2013. Lifting and Transfer: A                  [16] Matthieu Sozeau. 2009. A New Look at Generalized Rewriting in
     Modular Design for Quotients in Isabelle/HOL. In Certified Programs                  Type Theory. Journal of Formalized Reasoning 2, 1 (2009), 41–62.
     and Proofs — Third International Conference, CPP 2013, Melbourne,                    doi:10.6092/issn.1972-5787/1574
     VIC, Australia, December 11–13, 2013, Proceedings (Lecture Notes in             [17] Nicolas Tabareau, Éric Tanter, and Matthieu Sozeau. 2018. Equiv-
     Computer Science, Vol. 8307), Georges Gonthier and Michael Norrish                   alences for Free: Univalent Parametricity for Effective Transport.
     (Eds.). Springer, 131–146. doi:10.1007/978-3-319-03545-1_9                           Proceedings of the ACM on Programming Languages 2, ICFP (2018).
[10] Robert Y. Lewis and Paul-Nicolas Madelaine. 2020. Simplifying Casts                  doi:10.1145/3236787
     and Coercions. In Joint Proceedings of the 7th Workshop on Practical            [18] Nicolas Tabareau, Éric Tanter, and Matthieu Sozeau. 2021. The Mar-
     Aspects of Automated Reasoning (PAAR) and the 5th Satisfiability Check-              riage of Univalence and Parametricity. Journal of the ACM 68, 1
     ing and Symbolic Computation Workshop (SC-Square) (CEUR Workshop                     (2021).
     Proceedings, Vol. 2752).                                                        [19] The mathlib Community. 2020. The Lean Mathematical Library. In
[11] Ralph Loader. 2003. Higher Order 𝛽 Matching is Undecidable. Logic                    Proceedings of the 9th ACM SIGPLAN International Conference on Cer-
     Journal of the IGPL 11, 1 (2003), 51–68.                                             tified Programs and Proofs, CPP 2020, New Orleans, LA, USA, January
[12] Alberto Martelli and Ugo Montanari. 1982. An Efficient Unification                   20–21, 2020. Association for Computing Machinery, New York, NY,
     Algorithm. ACM Transactions on Programming Languages and Systems                     USA, 367–381. doi:10.1145/3372885.3373824
     4, 2 (1982), 258–282. doi:10.1145/357162.357169                                 [20] Sebastian Zimmer, Mario Carneiro, Heather Macbeth, and Jo-
                                                                                          van Gerbscheid. 2023.        The generalized rewriting tactic grw
                                                                                          (Mathlib.Tactic.GRewrite). Part of the Lean mathematical library
                                                                                          (mathlib4); pull request #8167. https://leanprover-community.github.
                                                                                          io/mathlib4_docs/Mathlib/Tactic/GRewrite/Elab.html.




                                                                                10
