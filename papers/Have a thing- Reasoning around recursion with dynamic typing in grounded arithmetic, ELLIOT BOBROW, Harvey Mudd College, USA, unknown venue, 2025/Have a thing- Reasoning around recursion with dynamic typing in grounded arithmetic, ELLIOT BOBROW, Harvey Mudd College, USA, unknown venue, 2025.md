                                         Have a thing? Reasoning around recursion with dynamic
                                         typing in grounded arithmetic
                                         DIMITRIOS ALEXOPOULOS, National Technical University of Athens, Greece
                                         ELLIOT BOBROW, Harvey Mudd College, USA
                                         YUSUF DEMIR, Boğaziçi University, Turkey
                                         BRYAN FORD, EPFL, Switzerland
                                         STEFAN MILENKOVIĆ, University of Belgrade, Serbia
                                         OMAR MUHAMMAD, Indian Institute of Science, India
                                         ANANTHAJIT SRIKANTH, EPFL, Switzerland
                                         Neither the classical nor intuitionistic logic traditions are perfectly aligned with the purpose of reasoning
                                         about computation, as neither can permit unconstrained recursive definitions without inconsistency: recursive
                                         definitions must normally be proven terminating before admission and use. Grounded arithmetic or GA is a
                                         formal-reasoning foundation allowing direct expression of arbitrary recursive definitions. GA adjusts traditional
arXiv:2510.25369v3 [cs.PL] 17 Jul 2026




                                         inference rules so that terms that express nonterminating computations harmlessly denote no semantic value (⊥)
                                         instead of yielding inconsistency. Recursive functions are proven terminating in GA essentially by “dynamically
                                         typing” terms, or equivalently, symbolically reverse-executing the computations they denote via inference
                                         rules. Once recursive functions have been proven terminating, logical reasoning about them reduces to familiar
                                         classical rules. We summarize the development and lessons learned from two mechanically-checked formulations
                                         of GA, finding both syntactically consistent and semantically sound with respect to an underlying computable
                                         model. Propositional grounded arithmetic or PGA is a quantifier-free system for inductive grounded reasoning
                                         about open formulas. PGA has logical expressiveness comparable to Skolem’s PRA, but has general-recursive
                                         (Turing-complete) functional expressiveness. PGA builds upon a simpler system of basic grounded arithmetic
                                         or BGA, which omits logical operators entirely. Even BGA can directly express any general-recursive function,
                                         however, and can prove its correct result for arbitrary but fixed arguments on which it terminates. PGA’s primitive
                                         grounded logical operators reduce to Gödel-style reflective computations in BGA. BGA and PGA are not only
                                         sound but semantically complete, a combination impossible for powerful classical systems with arithmetic, due
                                         to Gödel’s incompleteness theorems. These results suggest that contrary to conventional wisdom, powerful
                                         and consistent formal reasoning with unconstrained recursive definitions is possible, potentially enabling new
                                         computation-centric formal languages, proof assistants, and type systems in the future.

                                         1   Introduction
                                         Today’s standard practices for reasoning about computations, both in traditional “pencil-and-paper”
                                         proofs and for automated reasoning and mechanical verification purposes, derive from the classical
                                         or intuitionistic logic traditions. Classical logic offers the strongest and most familiar deduction rules,
                                         including the law of excluded middle (LEM) and proof by contradiction. The intuitionistic tradition
                                         rejects LEM and proof by contradiction, but is nevertheless appealing for computational reasoning
                                         because an intuitionistic proof that an object with certain properties exists yields in principle a
                                         concrete algorithm to construct such an object.
                                            In both logic traditions, one must justify all recursive logical definitions intended to represent
                                         computations, by proving their termination, before using a recursive definition. A fundamental part of
                                         the expressive power of Turing-complete computation, however, is that computations need not always
                                         terminate, and sometimes intentionally do not, as in streaming processes. Allowing direct expression
                                         of non-terminating recursive definitions in classical or intuitionistic formal systems, however, leads to
                                         Authors’ Contact Information: Dimitrios Alexopoulos, National Technical University of Athens, Athens, Greece; Elliot
                                         Bobrow, Harvey Mudd College, Claremont, CA, USA; Yusuf Demir, Boğaziçi University, Istanbul, Turkey; Bryan Ford,
                                         EPFL, Lausanne, Switzerland; Stefan Milenković, University of Belgrade, Belgrade, Serbia; Omar Muhammad, Indian
                                         Institute of Science, Bangalore, India; Ananthajit Srikanth, EPFL, Lausanne, Switzerland.
          Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
2                                                                                     and Ananthajit Srikanth

inconsistency via logical paradoxes such as the Liar or Curry’s paradox. Despite being common and
natural in modern casual programming practice, therefore, unrestricted (potentially non-terminating)
recursion remains a problematic and “foreign” challenge in formal reasoning.
   Can we bring the “freedom of expression” we enjoy in casual programming – to define directly
and employ arbitrary recursive functions without restriction – into the world of consistent formal
reasoning? Church and Curry both pursued this goal [16, 22], only for their systems to be found
inconsistent [42,68]. Scott continued this pursuit of a “Fregean paradise of ‘type-free’ functions” [65]
– but to this date, no conceivably-usable formal system allowing direct expression of arbitrary
unconstrained recursive definitions has to our knowledge survived the consistency test.
   Grounded deduction [27] or GD is a recent proposal in this tradition, which shows promise but
still faces the crucial consistency question. GD is inspired by Kripke’s theory of truth [45] and other
experimental paracomplete logics [26]. Apart from intuitionistic logic, no paracomplete system
we know of has achieved acceptance as being powerful enough to be usable for practical formal
reasoning. GD is powerful enough to express arbitrary recursive functions and reason about them in
arguably-natural ways – but does it escape the inconsistency trap that ensnared Church and Curry?
   This paper focuses more narrowly on systems of grounded arithmetic or GA, or GD constrained to
the natural numbers as the domain of discourse. Our primary contribution is a rigorous metalogical
development of two such formulations – basic grounded arithmetic or BGA and propositional
grounded arithmetic or PGA – aimed primarily at studying this crucial question of consistency.
   GA unsurprisingly parallels classical formal systems of arithmetic such as Peano arithmetic
(PA) and Skolem’s primitive-recursive arithmetic (PRA) [51, 70], while adjusting certain logical
deduction rules to tolerate unrestricted recursive definitions. Following in the tradition of PA and
PRA, intuitionistic Heyting Arithmetic (HA) [33], and minimalist programming formalisms like
LCF and PCF [59], we focus here on natural-number arithmetic and propositional logic to keep the
challenge tractable, while retaining the key interesting property of GD, namely its power to express
and use unconstrained (Turing-complete) recursive definitions directly in formal reasoning. Unlike
a “pure” paracomplete logic studied independently of any particular domain of discourse, GA is
plausibly powerful enough for practical reasoning about arbitrary computations, and hence could be
a promising foundation for computational reasoning – provided it is sound, or at least, consistent.
   GA modifies the classical and intuitionistic inference rules in attempt to tolerate unconstrained
recursion by enforcing a habeas quid principle: informally, one must first “have a thing” in order to
use it in subsequent reasoning. This principle leads to the addition of dynamic typing preconditions
to certain inference rules: not “dynamic” in a time-varying sense, as formal arithmetic has no
notion of time, but rather in the sense that typing depends on what a term actually computes from
given inputs rather than on static syntactic structure alone. GA’s habeas quid or dynamic-typing
preconditions appear to convert logical paradoxes into harmless circular proof obligations. To prove
that the Liar paradox ‘𝐿 ≡ ¬𝐿’ denotes “a thing”, for example (i.e., habeas quid, or “is dynamically
well-typed”), one would first have to prove that 𝐿 already denotes a thing. In a sense, GA takes
dependent typing [48, 56] to a logical extreme by deferring termination-proof obligations until as
“late” as apparently possible. Proving a term dynamically well-typed in GA, i.e., that it terminates
with a value, also amounts in essence to executing it symbolically in reverse, as we will see.
   This paper’s primary contribution is a rigorous confirmation, mechanically verified using Is-
abelle/HOL, that two concrete formulations of GA – BGA and PGA – are indeed consistent. The
consistency proof builds and employs a computational, operational-semantic model to prove the
inference rules truth-preserving, and hence not just syntactically consistent but semantically sound.
Appendix A provides a high-level roadmap and index of the key theorems in the mechanized proofs.
   We first present basic grounded arithmetic or BGA, a foundation that omits logical connectives
entirely and constrains functions to be defined via a single “background” list of 2-argument recursive
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                     3


definitions. Despite these structural constraints, BGA remains Turing complete, all primitive-recursive
and general-recursive functions being directly expressible via such definitions.
   BGA is not only sound but semantically complete: every well-formed BGA formula that is true
under all assignments is also provable in BGA. This combination of properties is impossible in
comparable classical or intuitionistic formal systems with arithmetic – even with only primitive-
recursive arithmetic – due to Gödel’s incompleteness theorems [57, 74]. As in Kripke’s theory of
truth [45], BGA contains its own truth predicate: a predicate 𝑇 ⟨𝑥⟩ such that for any grounded BGA
sentence 𝑝 satisfying the habeas quid condition of being boolean (‘𝑝 B’), BGA proves ‘𝑇 (⌜𝑝⌝) ↔ 𝑝’.
Sentence 𝑝 must be grounded because BGA’s paracomplete biconditional is provable only for
grounded formulas, a property that in turn circumvents Tarski’s undefinability theorem [72].
   Propositional grounded arithmetic or PGA, in turn, leverages BGA’s general-recursive functional
expressiveness and Gödel-style reflection techniques to construct propositional operators as com-
putations atop BGA. To build logical disjunction with Kleene’s strong 3-valued semantics [43],
for example, PGA reflectively searches in parallel for BGA proofs either supporting or refuting
the disjunction. Building on this reduction to BGA, we likewise show that PGA is syntactically
consistent, semantically sound and complete, and contains its own truth predicate.
   As the mechanically-checked formal development of GA consists of over 60K lines of Is-
abelle/HOL proofs, this paper can realistically cover only the development’s overall structure and key
milestones. This work also leaves important metalogical questions unanswered. For example, while
GA can prove the correct evaluation of any closed general-recursive function for particular arguments
on which it terminates, and GA can prove in general (for all argument values) the termination of all
primitive-recursive functions, GA’s precise termination-proving power (its proof-theoretic ordinal)
presently remains unknown.
   As this paper’s focus is on metalogical study, we leave to future work many broader questions, such
as how a truly-practical grounded reasoning system would be formulated and how its expressiveness
and usability would compare to the classical and intuitionistic logics underlying current proof
assistants. Preliminary efforts in this direction, orthogonal to this paper, show promise [40]. In a
practical “grounded proof assistant” we would want features such as quantifiers, richer data types
beyond natural numbers, higher-order functions expressed in familiar lambda-style notation, and
automated habeas quid termination proofs for easy common cases. Our experience suggests that all
of these features should be readily constructible atop PGA, but doing so remains future work.
   Even given a mature grounded reasoning system, how would its practical usability compare to
current systems? Any computation expressible directly in GA can already be expressed indirectly atop
an operational- or denotational-semantic model in current systems, so what are the tradeoffs between
these direct and indirect approaches to reasoning about computation? One clear cost is learning
unfamiliar inference rules with habeas quid preconditions. This cost appears mostly historical
rather than fundamental, however: we can readily imagine an alternate history where Church or
Curry discovered grounded reasoning and adopted it rather than “retreating” to strongly-normalizing
classical systems [17]. Beyond the mere appeal of directly expressing arbitrary computations, other
potential benefits in future reasoning systems could be support for non-local mutual recursion, or
mutually-recursive definitions spread throughout or even across modules, and simpler approaches to
higher-order abstract syntax (HOAS) without termination-proving or parametricity requirements [14,
58]. Exploring these practical tradeoffs remains future work, however. The motivation for our goals
rests, for now, on their record of being historically challenging and of intellectual interest to at least
three central figures of programming language theory – namely Church, Curry, and Scott.
   In summary, this paper’s primary contributions are: (a) a metalogical development of BGA and
PGA, two concrete systems of grounded arithmetic; (b) a reduction of PGA’s grounded propositional
operators to reflective general-recursive computations in BGA; (c) mechanically-checked proofs that
          Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
4                                                                                     and Ananthajit Srikanth

BGA and PGA are syntactically consistent, semantically sound and complete, and contain their own
truth predicates.
   The rest of this paper is organized as follows. Section 2 expands on background and motivation
for GA, and Section 3 introduces GA at a high level. Section 4 then summarizes the metatheory of
BGA, and Section 5 details PGA. Section 6 outlines related work, and Section 7 concludes.

2   Background and Motivation
Reasoning formally about computation has always been challenging, due in part to a fundamental
“impedance mismatch” between classical mathematical tradition and Turing-complete computation.
In classical mathematics, predicates are in principle always either true or false, sets always decide
their membership, and functions always decide their result for given arguments. Computations
in contrast may never terminate, and sometimes are not supposed to. Even after Church and Tur-
ing formulated clear mathematical models of computation, which evolved into operational- and
denotational-semantic models for reasoning about modern programming languages [66, 76], these
useful models still require us to reason “at arm’s length” from the computations of interest: i.e., about
program code in a computational semantic model built out of classical mathematical primitives,
not about programs expressed directly via “raw” mathematical or logical primitives themselves.
Domain-specific tools like Hoare logic [36], process calculi [54], and separation logic [63] can help
bridge this conceptual gap, but these tools bring constraints and limitations of their own.
   As proof assistants like Isabelle [55] and Coq/Rocq [15] have matured to support the machine-
checked verification of significant systems [44, 47], substantial challenges remain. Few deployed
systems, even mission-critical ones, are formally verified. Dependent type theories in proof assistants
like Rocq [15], Lean [25], and Agda [7] allow functional program code to be used both as a target for
reasoning and within the reasoning process itself, via the Curry-Howard correspondence [37] – but
this code must still be provably terminating or strongly normalizing via the type system, constraining
the power and expressiveness of such computations.
   A fundamental challenge facing formal reasoning is ensuring logical consistency. To be trustworthy,
a useful formal system should not allow us to prove absolutely anything, which the classical principle
of explosion allows us to do as soon as any proposition ‘𝑝’ and its negation ‘¬𝑝’ are both provable [51].
From Russell’s discovery that Frege and Cantor’s set theory was inconsistent [75], to the same
discovery by Kleene and Rosser [42] about Curry’s and Church’s proposed systems for computational
reasoning [16, 22], to Girard’s similar observation about early type theories in the Martin-Löf
tradition [28], it remains difficult to ensure that our formal systems are consistent. Most of the
powerful dependent type theories lack any consistency proof, and even more-conservative type
systems like that of Isabelle’s HOL, which in principle reduces to ZFC set theory, still sometimes
encounter subtle consistency issues due to convenient language extensions like overloading [46].
   The conventional wisdom, and the weight of experiential evidence so far, is that formal systems
cannot permit the expression of arbitrary computations – especially non-terminating ones – directly
as unconstrained recursive logical definitions, without inconsistency. This is why Skolem’s primitive-
recursive arithmetic (PRA) structurally constrains its recursion [51,70]. This issue similarly motivates
the typing and normalization constraints Church imposed on his simply-typed lambda calculus [17]
after his untyped formal system was found inconsistent [42]. But is ensuring termination and
constraining computational expressiveness truly the only way we can admit computation directly
into the recursive definitions we use in formal reasoning?
   Mathematical philosophers have long explored theories of truth [45,50,72] as well as the Liar [5,69]
and related paradoxes [26]. Much effort focuses on circumventing Tarski’s undefinability theo-
rem [72], which builds on Gödel’s incompleteness theorems [51, 74] to show that a consistent,
sufficiently-powerful classical formal system cannot precisely model its own semantics or prove
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                   5


itself consistent. This exploration has yielded two significant alternative directions [26]: Kripke-
inspired paracomplete systems [45], which drop the classical expectation that every well-formed
proposition is either true or false, and paraconsistent systems [61], which relax the classical ex-
pectation that a formal system should be entirely consistent. Paraconsistent systems attempt to be
more robust when inconsistency does occur, e.g., by limiting the explosion principle. We focus
here on paracompleteness over paraconsistency, simply because we are not yet ready to give up on
consistency as a seemingly-minimal baseline test for a formal system’s trustworthiness.
   The paracomplete systems proposed so far in Kripke’s tradition, however, have not proven usable
or gained acceptance for everyday formal reasoning, even by their proponents [26, 45, 50]. To our
knowledge no such formal system has been shown powerful enough for reasoning about Turing-
complete computation in particular, even just on natural numbers as in LCF [52,67]. We thus raise the
interdisciplinary question: can paracomplete reasoning in Kripke’s tradition be powerful and usable
enough for practical formal reasoning about realistic programs and Turing-complete computation?
   While this paper focuses on the foundations and metatheory of grounded reasoning, one potentially-
useful capability it could lead to is support for freeform non-local mutual recursion. While casual
programming languages generally allow mutually-recursive functions to invoke each other from
essentially anywhere, including across modules, today’s proof assistants require mutually-recursive
definitions to be tightly bound together using special language constructs to express all components
of a mutually-dependent cycle at once. Grounded reasoning could permit natural expression of
mutual recursion in formal reasoning as in casual languages, without requiring special language
constructs, and could allow mutual recursion even across modules. One concrete use-case might be
modeling a mission-critical embedded system consisting of multiple hardware/software components
that coordinate in continuation-passing style (CPS), such that all components – perhaps residing in
separate modules – invoke and are hence mutually recursive with all others [10].

3     Overview of grounded deduction (GD) and grounded arithmetic (GA)
This section introduces the general principles of Grounded Arithmetic (GA) informally at a high
level, focusing primarily on GA’s relationship to traditional, classical or intuitionistic formulations
of arithmetic such as Peano arithmetic (PA) or Heyting arithmetic (HA), respectively. This section’s
purpose is to provide the “big picture” needed to understand grounded reasoning.
   We use the term grounded arithmetic (GA) broadly to refer not to a particular concrete formal
system, but rather to any reasoning approach that generally applies the principles of grounded
deduction [27] to the purpose of reasoning about the natural numbers. Many concrete GA systems
could be devised with contrasting properties, and we make no pretense of prescribing here the “one
true” formulation of GA. In subsequent sections, however, we will study two particular, concrete and
precisely-defined formulations of grounded arithmetic, which we will call basic grounded arithmetic
or BGA (Section 4), and propositional grounded arithmetic or PGA (Section 5), respectively. While
the broad principles we introduce here are aligned with both BGA and PGA, we emphasize that
many reasonable changes could be made to the specific details of either system while remaining
under the broader umbrella of what we would informally consider a system of grounded arithmetic.

3.1    Grounded versus classical logical inference
The central principle of grounded deduction or GD [27] is the so-called habeas quid principle: we
must “have a thing” in order to use it in subsequent reasoning. Both classical and intuitionistic logics
violate this principle in details of their inference rules, while GD enforces it strictly. This habeas
quid enforcement is what appears to make grounded reasoning resistant to inconsistencies caused
by unconstrained recursion in classical or intuitionistic systems. A few key classical inference rules
appear in Table 1a with corresponding grounded rules in Table 1b for comparison.
           Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
6                                                                                      and Ananthajit Srikanth


           𝑝 ⊢𝑞          𝑝 ⊢ ¬𝑞              ¬¬𝑝                                   𝑝                  𝑝        ¬𝑝
                                    ¬I                ¬¬E                                ¬¬IE                       ¬E
                    ¬𝑝                        𝑝                                   ¬¬𝑝                      𝑞

            𝑝 ⊢𝑞                    𝑝 →𝑞          𝑝                      𝑝B            𝑝 ⊢𝑞               𝑝 →𝑞          𝑝
                        →I                            →E                                      →I                            →E
           𝑝 →𝑞                          𝑞                                   𝑝 →𝑞                               𝑞

                        𝑎 =𝑏             𝑎 =𝑏           𝑏 =𝑐         𝑎N                  𝑎 =𝑏              𝑎 =𝑏          𝑏 =𝑐
           =R                  =S                              =T           =R                  =S                               =T
    𝑎 =𝑎                𝑏 =𝑎                  𝑎 =𝑐                  𝑎 =𝑎                 𝑏 =𝑎                    𝑎 =𝑐

                                                                                          𝑎N                        𝑎N
                                      S≠0I                                  0TI                    STIE                     S≠0I
                         S(𝑎) ≠ 0                                    0N                  S(𝑎) N                 S(𝑎) ≠ 0

                𝑝 ⟨0⟩        𝑝 ⟨𝑥⟩ ⊢ 𝑝 ⟨S(𝑥)⟩                            𝑝 ⟨0⟩         𝑥 N, 𝑝 ⟨𝑥⟩ ⊢ 𝑝 ⟨S(𝑥)⟩         𝑎N
                                                  Ind                                                                       Ind
                             𝑝 ⟨𝑎⟩                                                            𝑝 ⟨𝑎⟩

            (a) Classical inference rules                                        (b) Grounded inference rules

       Table 1. Classical versus grounded reasoning: comparison of a few key inference rules



3.1.1 Logical negation. Like intuitionism, grounded deduction diverges most prominently from
classical logic in its handling of negation. Modern formulations of classical logic typically use two
inference rules to define logical negation: negation introduction (¬I ) and double-negation elimination
(¬¬E) in Table 1a. In brief, GA rejects classical negation introduction, but offers a bidirectional rule
¬¬IE in Table 1b for both introduction and elimination of double negation. GA additionally includes
a negation-elimination rule ¬E, directly embodying the principle of explosion: arbitrary conclusions
follow from contradictory premises, reflecting the incompatibility of 𝑝 and ¬𝑝, also known as the
classical law of non-contradiction.
   Classical negation introduction embodies the principle of reductio ad absurdum or reduction to
absurdity: if we hypothetically assume any proposition 𝑝, and from that assumption can derive a
contradiction – i.e., both 𝑞 and ¬𝑞 for any proposition 𝑞 – then we may conclude ¬𝑝: i.e., that 𝑝 must
be false. This principle directly leads to the classical practices of proof and refutation by contradiction,
and to the classical law of excluded middle (LEM): for any proposition 𝑝, either 𝑝 or ¬𝑝 must be
true. Like intuitionism, GA rejects classical reductio ad absurdum, proof by contradiction, and LEM
– not on the philosophical or constructivist grounds that motivated intuitionism [6, 9, 34], but instead
for the pragmatic reason that strong reductio ad absurdum is inconsistent with the unconstrained
recursive definitions we wish to permit in GA. The ¬¬IE rule distinguishes GA from intuitionism,
however, which rejects the logical equivalence of a formula with its double negation.
   The clearest illustration for why GA rejects LEM is the venerable Liar paradox [5]: if I claim “I
am lying”, am I lying or telling the truth? Unconstrained recursive definitions enable us to express
the Liar paradox simply and directly in GA, via the valid definition ‘𝐿 ≡ ¬𝐿’. If we were to admit
such a definition in a classical system, we could hypothetically assume 𝐿, use 𝐿’s definition to get ¬𝐿,
then use reductio ad absurdum with that contradiction to conclude ¬𝐿 unconditionally (no longer
hypothetically). In the same vein, we assume ¬𝐿 to get 𝐿 unconditionally, a logical inconsistency.
   GA still has proof and refutation by contradiction, but only via the following weakened rules:
                𝑝B             𝑝 ⊢𝑞          𝑝 ⊢ ¬𝑞                 𝑝B           ¬𝑝 ⊢ 𝑞         ¬𝑝 ⊢ ¬𝑞
                                                        boolE1                                                 boolE2
                                 ¬𝑝                                                  𝑝
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                       7


The first rule corresponds to classical negation introduction, except for the newly-added precondition
‘𝑝 B’: informally, a prerequisite that “𝑝 is boolean.” With this precondition, GA demands first that 𝑝
 be proven to be “a thing” (the habeas quid principle) of the appropriate type (in this case boolean),
 before term 𝑝 may be used in refutation or proof by contradiction via these derived rules.
    In GA, ‘𝑝 B’ is a shorthand for ‘𝑝 ∨ ¬𝑝’. Classically this is just the law of excluded middle (LEM),
 a tautology. These habeas quid preconditions could thus be added to classical rules, but would always
 be trivially satisfied and hence pointless. GA, however, rejects the classical blanket assumption
 that any well-formed proposition 𝑝 is either true or false, but instead demands a prior proof that 𝑝
 actually denotes a boolean value – dynamically by virtue of however the term 𝑝 actually evaluates to
 a value, rather than statically based on 𝑝’s syntactic structure alone. The shorthand ‘𝑝 B’ constitutes
 a dynamic type check that 𝑝 denotes a terminating computation yielding a defined boolean value.
    Although the Liar paradox is directly expressible in GA, the habeas quid preconditions on
 contradiction proofs appear to block the paradox from leading to inconsistency. To apply proof or
 refutation by contradiction on ‘𝐿 ≡ ¬𝐿’, in particular, we find we would first have to prove that 𝐿
 denotes a dynamically well-typed boolean value, i.e., that ‘𝐿 B’ or ‘𝐿 ∨ ¬𝐿’ – but the only apparent
way to do that would be to have already completed our proof by contradiction, via the rule we are
 still trying to justify invoking! In effect, the habeas quid preconditions on contradiction proofs in GA
 defuse the Liar by erecting a circular proof obligation as a roadblock to proving that 𝐿 denotes any
value at all. 𝐿 having no value is not a problem since GA is paracomplete and hence rejects at the
 outset the classical assumption that 𝐿 must necessarily denote some boolean value.
3.1.2 Disjunction and conjunction. GA’s inference rules for conjunction and disjunction are
identical to those of classical logic, and hence omitted from Table 1. Grounded conjunction and
disjunction remain duals that respect all of de Morgan’s laws, unlike intuitionistic systems.
 3.1.3 Implication. As seen in Table 1, implication elimination (→E) in GA is identical to the
 classical and intuitionistic modus ponens rule. Implication introduction (→I ), however, adds the
 habeas quid or dynamic typing precondition ‘𝑝 B’, as in the earlier contradiction-proof rules.
    Consider Curry’s paradox [23], expressible informally via the claim “if I am telling the truth then
 pigs fly” – or formally via a recursive definition of the form ‘𝐶 ≡ 𝐶 → 𝑃’ for any proposition 𝑃.
 Given this definition and the classical or intuitionistic inference rules, we can hypothetically assume
𝐶, unwrap its definition to 𝐶 → 𝑃, and use modus ponens (→E) to get 𝑃 hypothetically. But since we
 have built a hypothetical chain from 𝐶 to 𝑃, classical implication introduction →I allows us to infer
‘𝐶 → 𝑃’ now unconditionally. Substituting 𝐶’s definition again, we get the unconditional truth of 𝐶,
 then by modus ponens again, the unconditional truth of proposition 𝑃 (e.g., “pigs fly”).
    Curry’s paradox illustrates why intuitionistic logic cannot tolerate unrestricted recursive definitions,
 despite rejecting LEM. Attempting this proof in GA, however, the new habeas quid precondition
‘𝑝 B’ in implication introduction rule →I again presents a circular proof obligation. To invoke this
 rule in attempt to prove 𝐶 true, we must first have proven at least that 𝐶 has some boolean value –
 but we find no way to do this without having already applied the implication introduction rule we are
 still trying to justify invoking. Like the Liar paradox, therefore, GA simply leaves Curry’s paradox as
 another statement that harmlessly denotes no provable value, thereby avoiding inconsistency.
3.1.4 Equality. GA obeys the usual symmetry and transitivity rules (Table 1b), and substitution
of equals for equals, as in classical logic with equality. Only the reflexivity rule =R differs, being
unconditional in classical logic, but having a habeas quid precondition in GA.
   Similar to the dynamic booleanness test ‘𝑝 B’, GA applies the habeas quid principle to natural
numbers with a dynamic type-check of the form ‘𝑎 N’. Because GA constrains the domain of
discourse solely to the natural numbers, only natural numbers yield a defined result in GA when
          Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
8                                                                                     and Ananthajit Srikanth

compared. Testing whether 𝑎 is a natural number in GA is thus equivalent to testing whether 𝑎 is
equal to itself – i.e., whether 𝑎 is reflexive. We cannot just assume some GA term 𝑎 yields a natural
number by static typing, but must prove dynamically that it does so, satisfying ‘𝑎 N’ or ‘𝑎 = 𝑎’.

3.1.5 Natural numbers. GA’s natural-number rules broadly follow classical Peano arithmetic
(PA), with small but important differences.
   Because reflexivity is only conditional, GA needs a type-introduction rule 0TI asserting explicitly
that zero is a natural number. This judgment would trivially result from static typing in classical PA,
where any well-formed term denotes a natural number. GA’s bidirectional successor typing rule STIE
similarly asserts that the successor of 𝑎 is a natural number precisely when 𝑎 is a natural number.
   The S≠0I rule states that no successor is equal to zero: i.e., that the successor operation always
generates new larger numbers that never wrap to zero. This rule is unconditional in classical PA, but
GA’s corresponding rule is contingent on 𝑎 having been proven to be a natural number.
   GA’s mathematical induction rule Ind is similarly conventional except for new habeas quid
preconditions. To prove inductively that 𝑝 holds for whatever value an arbitrary term 𝑎 denotes, Ind
first requires not only base-case and inductive-step proofs, but also a proof that term 𝑎 actually yields
a natural number. The required inductive-step proof is now allowed two hypotheses, however: that 𝑝
holds for the induction variable 𝑥, and that 𝑥 is a natural number.

3.2   Expressing and proving termination of recursive computation in GA
Having summarized a few key deduction principles of GA, we now briefly and informally explore
their pragmatic usefulness for reasoning about arithmetic computations on natural numbers.

3.2.1 Proving termination by dynamic typing. Static type systems for informal programming
languages traditionally prove only a safety property: that a typed term never produces any value other
than one of the correct type. These type systems usually prove nothing about liveness or termination,
i.e., whether the typed term ever actually produces a value.
   Type systems for formal languages traditionally preserve this static paradigm. Since classical and
intuitionistic formal systems become inconsistent if recursively-defined functions fail to terminate,
however, recursive definitions must typically be justified by a termination proof that relies on a line
of reasoning orthogonal to the type system: e.g., by building a well-founded set, ordinal, or type
universe “big enough” to contain the desired function and selecting the function from it. GA’s habeas
quid or dynamic-typing proofs, in contrast, double as termination proofs.
   As an example, consider the construction of natural numbers. The premise-free rule 0TI allows us
to conclude ‘0 N’: that zero is a natural number. What this one-line proof’s conclusion really states
is that the term ‘0’ is a terminating computation yielding some particular natural number. Using the
STIE typing rule, we can prove that the term ‘S(0)’ – i.e., 1 – is likewise a terminating computation
yielding a natural number. For any particular natural number 𝑛, we can apply the STIE rule 𝑛 times in
this way to prove that there is a terminating computation yielding the natural number 𝑛.
   Longer proofs in this series, for larger natural numbers, build on shorter termination proofs for
smaller natural numbers. These proofs in effect just symbolically perform the construction, dynamic
typing, and termination-proving of a particular natural number in reverse, starting with smaller
natural numbers, and proceeding to larger numbers built on prior smaller ones. We can thus see how
proving termination and dynamic typing in GA may be equivalently viewed as reverse symbolic
execution of computations, as will become clearer in Section 4.3 on BGA’s operational semantics.

3.2.2 Generalized dynamic typing by induction. Each of the above trivial number-construction
examples constitutes pointwise termination proof, that is, only for specific natural numbers, and not
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                   9


general proof applying to all natural numbers. We can use recursive definitions and the induction
rule Ind to construct uniform, more general dynamic typing and termination proofs, however.
   Consider for example the following recursive definition, using the predecessor operation P and
C-like syntax ‘𝑐 ? 𝑎 : 𝑏’ as a shorthand for ‘if 𝑐 then 𝑎 else 𝑏’ conditional evaluation:
                                even(𝑛) ≡ 𝑛 = 0 ? 1 : 1 − even(P(𝑛))
This recursive definition need not be justified before being introduced and used in GA, but we cannot
 assume it is dynamically well-typed or terminating until we have proven it as such. Such a dynamic
 typing or habeas quid proof is easy using induction, however. Assuming we have already proven
 the constant ‘1 ≡ S(0)’ and subtraction to be terminating, we need to prove ‘𝑛 N ⊢ even(𝑛) N’
 by induction on 𝑛. In the base case 𝑛 = 0, the conditional-evaluation ‘?’ evaluates to 1, reducing
 to our existing proof of ‘1 N’. In the inductive step, we can assume ‘even(𝑛) N’ and must prove
‘even(S(𝑛)) N’. We reach this conclusion by applying the definition, the S≠0I rule, predecessor rules
 not shown in Table 1, and the prior termination proofs for 1 and subtraction.
3.2.3 Primitive recursion. The primitive-recursive functions are central to Skolem’s formal system
now known as PRA [51, 70]. These primitive-recursive functions take natural-number arguments
and yield natural numbers, always terminate, and are constructed inductively from standard initial
functions via two composition operations: function substitution and primitive recursion.
   Primitive recursion expresses many practical computations, including functions with growth far
beyond the exponential. It is nevertheless not Turing complete: the Ackermann function is computable
and defined on every input, but is not primitive recursive [1, 43].
   Any primitive-recursive function is directly expressible in GA, as a structurally-constrained special
case of general recursion. We can moreover prove in GA that any such primitive-recursive function
always terminates, by following the primitive-recursive function composition structure, proving the
termination of simpler primitive-recursive functions first, followed by the more-complex functions
composed from them, and using an inductive proof like that in the even example above for functions
composed via primitive recursion.
3.2.4 General recursion. Any general-recursive function is likewise directly expressible in GA
via unconstrained recursive definitions. Metalogically, a general-recursive function reduces to a
primitive-recursive function and a single existential quantifier or any equivalent “unbounded search”
capability, by virtue of Kleene’s normal form theorem [43, 51]. Intuitively, a primitive-recursive
function can advance a Turing machine or equivalent computational model by one step, or by any
specific number of steps. The remaining crucial ingredient of unbounded search advances the machine
to the first step at which it terminates, if it ever terminates. Both primitive recursion and unbounded
search are directly expressible via recursive definitions in GA.
   Concretely, assume 𝑇 (𝑥, 𝑦) is a primitive-recursive function taking input 𝑥 and a step count 𝑦,
returning 1 + 𝑧 if the computation terminates within 𝑦 steps with output 𝑧, and returning 0 if the
computation has not yet terminated within 𝑦 steps. The recursive function 𝐶 (𝑥, 𝑦) ≡ 𝑇 (𝑥, 𝑦) ≠ 0 ?
P(𝑇 (𝑥, 𝑦)) : 𝐶 (𝑥, S(𝑦)), definable in GA, searches for a 𝑦 for which the underlying step function
𝑇 terminates with a nonzero result. Thus, 𝐶 (𝑥, 0) denotes the computation’s result provided it
terminates; otherwise 𝐶 (𝑥, 0) represents a non-terminating computation with no result.
   For any particular input 𝑥 on which the computation represented by 𝐶 terminates with some result
𝑧, GA can prove that 𝐶 (𝑥, 0) indeed terminates with 𝑧, essentially by executing the computation
itself in reverse as in the simple examples above. If the computation does not terminate on input 𝑥,
however, we will be unable to prove anything about 𝐶 (𝑥, 0) – at least not directly.
   GA’s computational language is, thus, Turing-complete: it is capable of expressing any partial
computable function via recursive definitions, and when a recursive computation terminates on a
          Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
10                                                                                    and Ananthajit Srikanth

particular input, GA can prove that it does so correctly. Subsequent sections will explore these
properties more formally in the contexts of BGA and PGA.


3.3    Isabelle/HOL metatheory framework overview
We now prepare to refocus on the particular concrete systems BGA and PGA with a brief overview
of the metatheory framework in which we developed them.
   Our machine-checked formalizations build on the Isabelle proof assistant, using its higher-order
logic HOL as our metalogic [55]. HOL is a richly-typed classical logic with higher-order functions,
designed to be reducible to Zermelo-Fraenkel set theory with choice (ZFC) [30, 46].
   Our framework includes substantial recursion theory and formal foundations for mathematical
logic such as syntax and Gödel coding, which we summarize here only briefly because these parts of
the framework follow standard practices and are not conceptually novel. For reference, Section A
contains further details including key HOL definitions and theorems from this development.
   Our framework formalizes Cantor pairing, defines a Haskell-style type class coding representing
Gödel-encodable HOL types with an injection into the natural numbers, then instantiates this class
for standard HOL types such as booleans, tuples, lists, and finite sets.
   Complementing the use of HOL’s algebraic datatypes to represent “closed” syntaxes such as
BGA’s, our framework defines and extensively uses a generic syntax that supports variables and
binding via de Bruijn indices, but which is oblivious to the particular operators used in a particular
language such as BGA. We make heavy use of Isabelle’s extensible syntax and its locale facility
for modular reuse of metalogical syntax, definitions, and proofs [3]. These facilities enable most of
our metalogical definitions and proofs simply to declare which target-logic syntax we assume exists
in a given context, and avoid being specific to a fixed syntax as with algebraic datatypes. Because
there are tradeoffs between using closed datatypes and generic syntax, our development uses both
approaches, defining conversions between the two representations to leverage the advantages of each.
   To analyze relationships between different formal systems, our framework also formalizes substan-
tial portions of classical logic and arithmetic, including primitive-recursive arithmetic (PRA). The
framework includes basics of proof theory and model theory, so we can Gödel encode and reason
about proofs explicitly for reflection, and define semantic models used in the proofs.
   The framework develops basic recursion theory, defining primitive-recursive and general-recursive
functions via inductive function composition [43, 51], Gödel-encodable indices for computable
functions, and the primitive recursiveness of many of HOL’s basic natural-number arithmetic,
boolean, list, and finite set operations. This boilerplate constitutes much of the tedious infrastructure
required for Gödel-style reflective reasoning, which serves as the formal foundation for BGA’s
computable logical operators (Section 4.8).
   We initially used denotational semantics based on domain theory [12, 66, 71] to model GA, but
switched to the operational semantics of Section 4.3 when we found it simpler and adequate for
our purposes. As GA’s initial formulation was inspired by domain theory, however, developing the
domain-theoretic approach remains a promising alternative for future work.


4     Metatheory of basic grounded arithmetic (BGA)
Having summarized a few general principles of grounded-arithmetic systems, we now focus on BGA,
a “minimalist” formulation of GA supporting general-recursive computation but no primitive logical
operators. As is traditional, we find it expedient to reduce GA to a minimum for metalogical study;
this motivates BGA as a simplified “kernel” foundation. This formulation of BGA is not necessarily
strictly minimal: we suspect it could still be simplified further, a task we leave to future work.
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                                                                 11

   𝑡 ≡ 𝑣 | 0 | S 𝑡 | P 𝑡 | 𝑡 0? 𝑡 : 𝑡 | 𝑑 (𝑡, 𝑡)                                                          𝑓 ≡𝑡 =𝑡 | 𝑡 ≠𝑡
    (a) Abstract term syntax of BGA                                                             (b) Abstract formula syntax of BGA

                              𝑎 =𝑏           𝑝 ⟨𝑎, . . .⟩                  𝑎 =𝑏              𝑎 ≠𝑏
                                                            =E                    =S                   ≠S
                                      𝑝 ⟨𝑏, . . .⟩                         𝑏 =𝑎              𝑏 ≠𝑎
                     𝑎N                              𝑎 =𝑏                              𝑎 ≠𝑏                                𝑎N
           0I                  S≠0I                               S=IE                               S≠IE                             PI
      0N           S(𝑎) ≠ 0                   S(𝑎) = S(𝑏)                         S(𝑎) ≠ S(𝑏)                           P(S(𝑎)) = 𝑎
                            𝑝 ⟨0, . . .⟩        𝑥 N, 𝑝 ⟨𝑥, . . .⟩ ⊢ 𝑝 ⟨S(𝑥), . . .⟩              𝑎N
                                                                                                        Ind
                                                            𝑝 ⟨𝑎, . . .⟩
                                     𝑐 =0            𝑎N                    𝑐≠0           𝑏N
                                                            ?I1                                  ?I2
                                    (𝑐 0? 𝑎 : 𝑏) = 𝑎                       (𝑐 0? 𝑎 : 𝑏) = 𝑏
                      𝑠 (𝑣 0, 𝑣 1 ) ≡ 𝑏⟨𝑣 0, 𝑣 1 ⟩         𝑎0 N            𝑎1 N         𝑝 ⟨𝑏 ⟨𝑎 0, 𝑎 1 ⟩, . . .⟩
                                                                                                                   ≡I
                                                      𝑝 ⟨𝑠 (𝑎 0, 𝑎 1 ), . . .⟩
                             (c) Inference rules for basic grounded arithmetic (BGA)

                                                              Term reductions
        𝐴𝑗 = 𝑛                             𝑎 ⇓𝑛                  𝑎 ⇓𝑛+1                𝑐⇓0             𝑎 ⇓𝑛             𝑐 ⇓ 1 +𝑚           𝑏 ⇓𝑛
        v𝑗 ⇓ 𝑛        0⇓0            S(𝑎) ⇓ 𝑛 + 1                 P(𝑎) ⇓ 𝑛              𝑐 0? 𝑎 : 𝑏 ⇓ 𝑛                      𝑐 0? 𝑎 : 𝑏 ⇓ 𝑛
                            𝑠 (𝑣 0, 𝑣 1 ) ≡ 𝑏⟨𝑣 0, 𝑣 1 ⟩          𝑎0 ⇓ 𝑛0          𝑎1 ⇓ 𝑛1             𝑏 ⟨𝑎 0, 𝑎 1 ⟩ ⇓ 𝑚
                                                               𝑠 (𝑎 0, 𝑎 1 ) ⇓ 𝑚
                                                            Formula reductions
      𝑎 ⇓𝑛       𝑏 ⇓𝑛         𝑎 ⇓𝑛           𝑏 ⇓𝑚             𝑛 ≠𝑚               𝑎 ⇓𝑛          𝑏 ⇓𝑛                𝑎 ⇓𝑛       𝑏 ⇓𝑚           𝑛 ≠𝑚
        𝑎 =𝑏 ⇓ 1                           𝑎 =𝑏 ⇓ 0                                𝑎 ≠𝑏 ⇓0                                   𝑎 ≠𝑏 ⇓1
                 (d) Big-step structural operational semantics (BSOS) for reduction in BGA

Table 2. Abstract syntax, proof rules, and operational semantics of basic grounded arithmetic (BGA)




4.1    BGA term and formula syntax
BGA maintains the classical tradition of syntactically distinguishing terms, which denote natural
numbers, from formulas, denoting logical truths. Table 2 shows BGA’s term and formula syntax
informally; see Section A.14 for the corresponding Isabelle/HOL datatypes. Terms consist of variable
references, the constant zero, the successor and predecessor operations, an if-zero-else conditional-
evaluation construct in the tradition of LCF and PCF [52, 59], and 2-argument recursive definition
application. Variable references are natural numbers in de Bruijn notation; the generic syntax supports
variable binding although BGA has no binders. BGA uses if-zero-else rather than if-then-else for
conditional evaluation to avoid mutual recursion between terms and formulas, and it restricts recursive
definition application to (exactly) two arguments for simplicity of metalogical definition and analysis.
   A formula in BGA consists only of either a primitive “equals” test (=) on two terms, or else an
“unequals” test (≠). In BGA, the “unequals” operator (≠) is not a shorthand for “not-equals” or
the negation of equality, because BGA omits logical negation as a primitive. An earlier version of
BGA included primitive negation and disjunction, from which the other propositional operators
are derivable. Our original operational semantics for BGA and consistency proof included these
propositional primitives with no difficulty. We found that even negation and disjunction primitives
           Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
12                                                                                     and Ananthajit Srikanth

were not necessary in BGA, however, as they are computationally derivable as described later in
Section 4.8. Further, our recursion representation proofs (Section 4.6) did not need these primitives,
and our completeness proofs (Section 4.5) became simpler without them. BGA thus evolved into a
computation kernel strikingly similar to PCF [59], except that it uses a background list of recursive
definitions to define functions, as described below, in place of PCF’s typed lambda terms.

4.2   Logical inference rules for BGA
Table 2c summarizes BGA’s inference rules for reasoning about natural numbers and computation.
For conciseness these rules are shown in natural-deduction style, although the mechanically-checked
development uses a sequent style that expresses premises explicitly as finite sets in HOL. The HOL
development includes the standard structural rules of proof by hypothesis, weakening, cut, and
specialization (consistent substitution in a judgment’s hypotheses and conclusion). Reordering and
contraction rules are unnecessary because premises are finite sets rather than ordered lists.
  BGA’s rule set notably contains mostly introduction rules, with few elimination rules aside from
substitution of equals for equals =E. We found these rules sufficient for the consistency, completeness,
and function representation proofs below. BGA’s minimal rule set provides no way to ascribe any
value to ‘P(0)’, for example, leaving the predecessor of zero undefined.

4.3   Operational semantics of BGA terms
Unlike classical Peano arithmetic, everything expressible in GA is “just a computation” – though not
necessarily a terminating one. We formalize this fact by assigning terms and formulas a computational
semantics, focusing for now on the minimalistic BGA kernel.
   BGA’s operational semantics has two main parameters affecting its operation: an assignment
𝐴 mapping variables to concrete values, and a list 𝐷 of recursive definitions. In the Isabelle/HOL
formulation of our operational semantics whose precise definition appears in Section A.14, we also
include a step count parameter 𝑠, counting the number of steps a given semantic reduction requires.
   Variables in our HOL development are formally just natural numbers, but we sometimes use
variable symbol notation v𝑖 to express clearly the use of natural number 𝑖 in the role of a variable.
An assignment 𝐴 is a function mapping each variable 𝑖 to a semantic value: either a natural number 𝑟
or a bottom value ‘⊥’ denoting no result. Semantic values are also encoded as natural numbers in our
formulation: 0 represents ⊥ and 1 + 𝑟 represents natural-number result 𝑟 .
   A definition symbol 𝑑 has the form d𝑖 , indexed by a natural number 𝑖. Like variables, definition
symbols are just natural numbers in our formal HOL development; we use the notation d𝑖 only
informally to express the use of natural number 𝑖 in the role of a definition number.
   A definition body is simply an arbitrary BGA term in the syntax defined in Section 4.1. A definition
list is a finite list of definition bodies. For all integers 0 ≤ 𝑖 < |𝐷 |, definition body 𝐷𝑖 represents
the body term associated with definition symbol d𝑖 . The arity 𝑘𝑖 of definition 𝐷𝑖 is the least natural
number greater than the natural-number index 𝑗 of any free variable v 𝑗 appearing in body 𝐷𝑖 . Since
BGA supports only 2-argument function application, only variables 0 and 1 may be free in a valid
BGA function definition. Any definition violating this rule (of any arity other than two) is irreducible
in BGA and hence semantically just a non-terminating computation.
   Each BGA definition 𝐷𝑖 represents a computable function taking two natural-number arguments
and potentially yielding a natural number (if the expressed computation terminates). Each position 𝑖
in the definition list 𝐷 thus represents the definition ‘d𝑖 (v0, v1 ) ≡ 𝐷𝑖 ⟨v0, v1 ⟩’. We place no restrictions
on the definition symbols that may appear within definition bodies – in particular, no requirement that
definitions be defined before being referenced – so definitions may be singly- and mutually-recursive.
GA terms may even contain undefined definitions d𝑖 for 𝑖 ≥ |𝐷 |. Our semantics offer no way to
reduce such a symbol, so an undefined definition simply denotes a nonterminating computation (⊥).
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                     13


 4.3.1 Reduction of BGA terms. Table 2d presents a big-step structural operational semantics,
 or BSOS, for BGA terms [76]. These reduction rules specify inductively how more complex BGA
 terms may reduce to simpler ones, with some BGA terms eventually reducing to a concrete natural
 number. For simplicity we encode the boolean constants T and F, which BGA formulas reduce to, as
 the natural numbers 1 and 0, respectively. There is nothing particularly new or special about BGA’s
 operational semantics; we introduce it only as a tool for metalogical reasoning about BGA.
    The operational semantics uses the assignment 𝐴 only to reduce variable references, and only
 for variables that 𝐴 maps to a natural number. Variables that 𝐴 maps to ⊥ never reduce, which may
 prevent the computation from terminating under that assignment.
    The reduction rule for recursive definitions uses call-by-value semantics, reducing an invocation
 of definition d𝑖 with actual parameters 𝑎 1, 𝑎 2 to a result 𝑟 only once each actual parameter 𝑎 𝑗 has
 reduced to a concrete value 𝑛 𝑗 . Upon substituting these values for the free variables in definition body
 𝐷𝑖 , the result reduces to 𝑟 . Other call semantics would likely work, but we found that call-by-value
 semantics simplify the subsequent reasoning below.
    An important property that BGA’s BSOS has, like those of many sequential programming lan-
 guages, is that the semantic reduction relation is single-valued or deterministic: if ‘𝑡 ⇓ 𝑛 1 ’ and
‘𝑡 ⇓ 𝑛 2 ,’ then ‘𝑛 1 = 𝑛 2 .’ We prove this property by induction on reduction step count.

4.4   Proving consistency by truth preservation
We show that BGA is consistent by the traditional method of proving all of its inference rules truth
preserving, so that valid proofs lead only to true judgments [43, 51].
   Our approach’s main distinction from the standard model-theoretic tradition launched by Tarski [72]
is its use of a computational model – namely the operational semantics above – in place of the meta-
logic’s “raw” semantics of the objects in question (e.g., the classical semantics of natural numbers in
HOL). We are proving in effect that BGA’s inference rules safely navigate between computations
expressible in BGA that terminate and reduce formulas to a “true” value, namely 1.
  Definition 4.1. An assignment 𝐴 satisfies a BGA formula 𝑓 if BGA’s operational semantics
(Section 4.3) eventually, at some step count 𝑠, reduces 𝑓 under 𝐴 to the natural number 1. Assignment
𝐴 satisfies a set 𝐹 of BGA formulas if 𝐴 satisfies every formula 𝑓 ∈ 𝐹 .
   Definition 4.2. A judgment Γ ⊢ 𝑐 is truth preserving if, for any assignment 𝐴 that satisfies all
hypotheses in Γ, 𝐴 also satisfies 𝑐. A proof 𝑃, comprising a finite list of judgments, is truth preserving
if every judgment in 𝑃 is truth preserving.
  Definition 4.3. A formula 𝑓 is a theorem if there is a valid proof using only the rules in Table 2c
and ending in ‘∅ ⊢ 𝑓 ’.
   Definition 4.4. Formula 𝑓 is true if every assignment satisfies 𝑓 .
   Because we are using a computational model, not every BGA term denotes a natural number
and not every BGA formula denotes a truth value: i.e., BGA is paracomplete. The natural-number-
producing properties of terms and the boolean-producing properties of formulas are therefore weaker
in this computational model than they would be under the “raw” classical model of the natural
numbers, often requiring preconditions corresponding to the habeas quid conditions discussed
earlier in Section 3.1. Our HOL formalization extensively uses Isabelle locales [3] to isolate relevant
properties of the computational model needed in particular truth preservation proofs, and to identify
the weakest assumptions apparently sufficient to justify particular inference rules, so that these proofs
are reusable and not specific to BGA. For example, the truth preservation proofs for equality depend
on a locale embodying the non-classical principle that only certain semantic values are comparable
for equality: e.g., in GA, all natural numbers are comparable but ⊥ is not.
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
14                                                                                      and Ananthajit Srikanth

     L EMMA 4.5 ( TRUTH PRESERVATION ). BGA’s inference rules in Table 2c are truth preserving.
  T HEOREM 4.6 ( SEMANTIC SOUNDNESS ). Every theorem of BGA is true in the operational-
semantic model of BGA.
  T HEOREM 4.7 ( SYNTACTIC CONSISTENCY ). There are no terms 𝑡 1, 𝑡 2 such that both ‘𝑡 1 = 𝑡 2 ’
and ‘𝑡 1 ≠ 𝑡 2 ’ are theorems of BGA.
   Syntactic consistency traditionally relies on negation; our formulation merely adapts to the fact
that BGA has primitive equals and unequals operators but no primitive negation. The lack of primitive
negation also results in a need in parts of our reasoning for a metalogical notion of refutation as a
dual of entailment: e.g., ∅ entails ‘0 = 0’ but ∅ refutes ‘0 ≠ 0’.

4.5     Semantic completeness of BGA
Semantic completeness is the converse of semantic consistency or soundness: the property that any
well-formed formula in a formal system that is semantically true is also unconditionally provable
(with no premises). Syntactic completeness, in contrast, is traditionally defined as the property that
for every closed well-formed formula 𝑓 , either 𝑓 or its negation is provable.
   In classical formal systems, semantic and syntactic completeness are generally aligned with each
other – we get either both or neither – but this is not the case for a paracomplete system like GA. The
law of excluded middle (LEM) is embedded in the traditional definition of syntactic completeness, so
a consistent paracomplete system cannot be syntactically complete. Indeed, dropping this expectation,
or even aspiration, is the essence of what defines the term “paracomplete.” The situation is different
for semantic completeness, however.
   Our proof of BGA’s semantic completeness relies on this key intermediate step:
  L EMMA 4.8. For any well-formed term 𝑡 that reduces to a natural number 𝑟 in 𝑠 steps under all
assignments via BGA’s operational semantics, the judgment ‘∅ ⊢ 𝑡 = 𝑟 ’ is provable in BGA.
     P ROOF. By induction over step count, then case analysis over the reductions in Table 2d.              □
  The HOL proof is slightly stronger than Lemma 4.8 in its handling of assignments, but that
additional strength is inessential. The important point is that the inductive structure of the operational
semantics provides “enough information” to construct a BGA equality proof corresponding to any
reduction from a term 𝑡 to some natural-number result 𝑟 . Intuitively, the proof amounts to constructing
longer proofs from shorter proofs, inductively, representing progressively-longer “reverse symbolic
executions” of semantically reduced terms.
  Lemma 4.8 in turn leads to our semantic completeness result:
  T HEOREM 4.9 ( SEMANTIC COMPLETENESS ). Every semantically true formula in BGA is prov-
able unconditionally using the rules in Table 2c.
     P ROOF. By Definition 4.4, we can assume a well-formed formula 𝑓 that reduces to the natural
number 1 under the operational semantics. By case analysis, 𝑓 is either an equals test ‘𝑡 1 = 𝑡 2 ’ or an
unequals test ‘𝑡 1 ≠ 𝑡 2 ’. By Lemma 4.8, there is a BGA proof of ‘𝑡 1 = 𝑟 1 ’ for some natural number
𝑟 1 , and similarly for 𝑡 2 . We reach the completeness conclusion using basic lemmas that ‘𝑟 = 𝑟 ’ is
provable for all 𝑟 , and that ‘𝑟 1 ≠ 𝑟 2 ’ is provable for 𝑟 1 ≠ 𝑟 2 .                                  □
   The important property of BGA enabling this completeness proof is the fact that its semantic model
is a computational model defined within our metalogic HOL, rather than being “the raw semantics”
of HOL itself. As a result, our completeness proof can proceed by induction over the reductions in the
operational semantics. If our model built classically on HOL’s semantics – on the metalogical natural
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                                    15


numbers and associated operators – then we would have no way to prove anything by induction
within HOL over “all possible semantic properties” that those HOL natural numbers have.1 Thus, our
use of an operational-semantic model within HOL rather than the semantics of HOL itself appears
fundamental and essential to BGA’s semantic completeness property.
   At risk of being overly simplistic, what is happening in BGA’s consistency and completeness
proofs is merely the Church-Turing thesis continuing to hold. The BGA proof system is one Turing-
complete model of computation; the operational semantics of BGA is a related but slightly-different
Turing-complete model of computation. The consistency proof is merely a simulation argument in
one direction; the completeness proof is merely a simulation argument in the other direction. There
is no magic: everything about BGA is just computation in the Church-Turing framework.

4.6    Representation of recursive computation
The combination of consistency and completeness in a formal system is not by itself interesting or
surprising. With the benefit of the hindsight we have today, it is a basic and standard proof that the
classical propositional calculus is consistent and complete [51].
   A more interesting prospect, however, is that of a formal system that is consistent, complete, and
powerful enough to reason about arithmetic and computation. A “conventional wisdom” interpretation
of Gödel’s incompleteness results is that no formal system powerful enough to include even just
primitive-recursive arithmetic or Robinson arithmetic [64] can be both consistent and complete.
This interpretation omits two important assumptions of Gödel’s theorems, however: first, that we
are reasoning in a sufficiently-powerful classical metalogic, justifying the contradiction proofs
Gödel used in certain steps; and second, that we are reasoning about a classical target logic. In our
metalogical development of GA, the first of these assumptions still holds, as Isabelle’s HOL is a
powerful classical logic. The second assumption underlying Gödel’s proofs fails to apply to GA,
however, because GA is paracomplete, not classical. There is no contradiction in supposing that a
sufficiently non-classical system might circumvent Gödel’s results.2
   Our results confirm that BGA is sufficiently non-classical. BGA is not only semantically consistent
and complete, but sufficiently powerful to express and carry out (grounded, not classical) formal
reasoning about natural-number arithmetic and arbitrary Turing-complete computation.
   Because it assumes some arbitrary-but-fixed list of recursive definitions 𝐷, BGA is not a single
formal system but a family of formal systems, one for each such list 𝐷. These definition lists now
take on new importance in that we must prove the existence of definition lists that result in BGA
instances having certain properties.
   Our proofs that all recursive functions are representable in BGA build on standard results of
recursion theory [43, 51], in particular about both primitive recursion and general recursion.
   Any two-argument primitive-recursive function 𝑓 (𝑥, 𝑦), in particular, is constructible from four
standard initial functions (zero, successor, left and right projection) and two methods of function
composition: substitution and primitive recursion. We Gödel encode these constructions to assign each
primitive-recursive function a natural number. We use two-argument primitive-recursive functions
for reasoning simplicity: there is no loss in doing so since we can use Cantor pairing to reduce 𝑘 > 2
arguments to two (or even just one, at a cost of more-complex initial functions).

1 By Gödel’s and Tarski’s theorems, assuming HOL is consistent, such proofs could not be carried out within HOL but only

within a strictly-more-powerful meta-meta-logic sufficient to model and reason about HOL.
2 At Gödel’s time, the only alternative logic foundations that showed signs of practical usability were based on Brouwer’s

program of intuitionism. The discovery that the double negation of any theorem of classical Peano arithmetic (PA) was a
theorem of intuitionistic Heyting arithmetic (HA), however, led to the conclusion that intuitionistic systems were no more
“exempt” from Gödel’s theorems than classical systems.
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
16                                                                                      and Ananthajit Srikanth

    Definition 4.10. A 2-argument total function 𝑓 (𝑥, 𝑦) is represented in 𝐵𝐷 , the BGA instance with
 definitions 𝐷, if there is a term pattern 𝑡 ⟨𝑥, 𝑦⟩ such that for all natural numbers 𝑛𝑥 and 𝑛 𝑦 , the formula
‘𝑡 ⟨𝑛𝑥 , 𝑛 𝑦 ⟩ = 𝑓 (𝑛𝑥 , 𝑛 𝑦 )’ is provable in BGA instance 𝐵𝐷 .

   When a function is represented in BGA instance 𝐵𝐷 , consistency ensures that no equality formula
such as the above is provable for any right-hand natural number other than the correct result of 𝑓 .
Our development also handles representation of non-total functions, but this case is not as clean or
straightforward to define because all “native” functions in the classical HOL metalogic are total.
   T HEOREM 4.11 ( PRIMITIVE RECURSIVE FUNCTIONS ). For any 2-argument primitive-recursive
function 𝑓 (𝑥, 𝑦), there is a definition list 𝐷 yielding BGA instance 𝐵𝐷 that represents all primitive-
recursive functions with Gödel codes up through that of 𝑓 .
  P ROOF. By induction on the Gödel code of 𝑓 . Our proof relies on monotonicity properties of
Cantor pairings, and of the Gödel codes of the primitive-recursive functions, such that the Gödel
code of any function 𝑓 depends on is strictly less than the Gödel code of 𝑓 itself.            □

   T HEOREM 4.12 ( PRIMITIVE - RECURSIVE FUNCTION TERMINATION ). For any 2-argument
primitive-recursive function 𝑓 (𝑥, 𝑦) represented in a BGA instance’s definition list 𝐷, BGA can prove
𝑓 (𝑥, 𝑦) terminating for all natural-number arguments 𝑥 and 𝑦: that is, ‘𝑥 N, 𝑦 N ⊢ 𝑓 (𝑥, 𝑦) N’.
     P ROOF. By induction on the structure of the primitive-recursive function 𝑓 .                          □

   A basic result of recursion theory is that any single-argument general-recursive (Turing-complete)
function 𝑓 (𝑥) is expressible by combining a two-argument primitive-recursive step function 𝑓𝑠 (𝑥, 𝑦)
with an unbounded search mechanism – such as an existential quantifier or Kleene’s minimization
operator 𝜇 [43] – to find the least step count 𝑦 for which 𝑓𝑠 (𝑥, 𝑦) ≠ 0, if such 𝑦 exists. If no such 𝑦
exists for some value of the fixed parameter 𝑥, each individual evaluation of the step function 𝑓𝑠 (𝑥, 𝑦)
terminates, but the unbounded search never succeeds, so the represented partial computation diverges
on 𝑥. We can thus use Gödel codes for 2-argument primitive-recursive functions also as indices for
single-argument general-recursive functions, by interpreting the primitive-recursive function as a
step function.
   T HEOREM 4.13 ( GENERAL RECURSIVE FUNCTIONS ). For any 1-argument general-recursive
function 𝑓 (𝑥) defined by primitive-recursive step function 𝑓𝑠 (𝑥, 𝑦), there is a definition list 𝐷 yielding
a BGA instance 𝐵𝐷 that represents 𝑓 (𝑥).
    P ROOF. We construct a definition list 𝐷𝑠 representing step function 𝑓𝑠 , then append to 𝐷𝑠 one
more recursive definition implementing the unbounded search from 0 upward for the first 𝑦 for which
𝑓𝑠 (𝑥, 𝑦) ≠ 0, if such 𝑦 exists.                                                                  □

     This result generalizes readily to 𝑘-argument general-recursive functions via Cantor pairing.
     We finally use a metacircular evaluator to construct 𝐵𝑈 , a universal instance of BGA.
   L EMMA 4.14 ( METACIRCULAR EVALUATION ). There is a BGA instance 𝐵𝑈 that represents a
general-recursive metacircular evaluation function 𝑓𝑈 (⟨𝑓𝑠 , 𝑥⟩) such that, for any general-recursive
function 𝑓 (𝑥) defined by primitive-recursive step function 𝑓𝑠 (𝑥, 𝑦), 𝑓𝑈 (⟨𝑓𝑠 , 𝑥⟩) eventually terminates
with result 𝑟 iff 𝑓 (𝑥) terminates with result 𝑟 .
  T HEOREM 4.15 ( UNIVERSAL RECURSION ). The universal BGA instance 𝐵𝑈 represents every
general-recursive function.
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                             17


4.7    Gödel-style arithmetization and reflection
On the way to his incompleteness theorems, Gödel showed that formal systems powerful enough
to express arithmetic and computation are also powerful enough for reflection, or modeling and
“reasoning about” themselves. Even if Gödel’s theorems do not apply to GA, his reflection techniques
still apply. Gödel-style reflection essentially relies on arithmetization of the proof system: encoding
the system’s syntax and proof rules into arithmetic functions expressible in the system itself.
  T HEOREM 4.16 ( ARITHMETIZATION ). Functions defining the syntax and proof rules of BGA are
represented in the universal BGA instance 𝐵𝑈 .
  P ROOF. Proving this theorem rigorously consists mainly of a large number and variety of tedious
but unsurprising primitive recursiveness proofs.                                                □

4.8    Turing-computable grounded propositional operators
Having established reflection in Gödel’s traditional fashion, we now use it for a different purpose:
to show that a set of grounded logical operators (connectives) that we omitted from BGA’s set of
primitives are nevertheless definable within BGA as general-recursive computations. This works
because all of the grounded propositional logic operators (Section 3) are just computations, which
are thus represented in the universal BGA instance.
   T HEOREM 4.17 ( GROUNDED NEGATION ). For any BGA formula 𝑓 , a formula ‘¬𝑓 ’ is con-
structible in BGA instance 𝐵𝑈 such that for all 𝑡 1, 𝑡 2 , ‘¬(𝑡 1 = 𝑡 2 )’ is provable iff ‘𝑡 1 ≠ 𝑡 2 ’ is provable,
and ‘¬(𝑡 1 ≠ 𝑡 2 )’ is provable iff ‘𝑡 1 = 𝑡 2 ’ is provable.
    P ROOF. The construction of ‘¬𝑓 ’ takes the Gödel code of formula 𝑓 and passes it as an argument
to a computation that reflectively searches for either a positive BGA proof or a negative refutation of
𝑓 , and yields the opposite result.                                                                  □
    T HEOREM 4.18 ( GROUNDED DISJUNCTION ). For any BGA formulas 𝑓1 and 𝑓2 , a formula ‘𝑓1 ∨ 𝑓2 ’
 is constructible in BGA instance 𝐵𝑈 such that ‘𝑓1 ∨ 𝑓2 ’ is true iff either 𝑓1 or 𝑓2 is true, and such that
‘𝑓1 ∨ 𝑓2 ’ is false iff both 𝑓1 and 𝑓2 are false.
  P ROOF. The construction ‘𝑓1 ∨ 𝑓2 ’ expresses a computation that simulates a multi-threaded parallel
search for either (a) a proof of 𝑓1 , (b) a proof of 𝑓2 , or (c) proofs of both ‘¬𝑓1 ’ and ‘¬𝑓2 ’.  □
  T HEOREM 4.19 ( GROUNDED PROPOSITIONAL LOGIC ). All of the grounded propositional con-
nectives (Section 3.1) are representable as computations in the universal BGA instance 𝐵𝑈 .
   P ROOF. The remaining grounded logical operators of conjunction, material implication, and
biconditional are directly definable based on negation and disjunction, as in classical logic. □
    Similarly to Kripke’s theory of truth [45], BGA contains its own truth predicate, which is applicable
 to all grounded sentences. This property may be unsurprising since GA was in part Kripke-inspired,
 but it formally confirms that BGA preserves the raison d’être of Kripke’s theory. This property
 of BGA is unusual mainly by virtue of occurring in a powerful logic supporting arithmetic and
 computation. The constraint to grounded sentences is crucial because BGA’s biconditional ‘𝑝 ↔ 𝑞’
 is provable only when both 𝑝 and 𝑞 are decided. Because BGA is paracomplete and the 𝑇 -schema
‘𝑇 (⌜𝑝⌝) ↔ 𝑝’ is inherently unprovable for undecided sentences, BGA effectively circumvents
 Tarski’s undefinability theorem [72], which assumes a consistent classical formal system.
   T HEOREM 4.20 ( TRUTH PREDICATE ). In the universal BGA instance 𝐵𝑈 there is a truth predicate
𝑇 ⟨𝑣⟩ with free variable 𝑣, such that for all grounded BGA sentences 𝑝 satisfying the habeas quid
condition of booleanness (‘𝑝 B’), BGA proves the biconditional ‘𝑇 (⌜𝑝⌝) ↔ 𝑝’.
           Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
18                                                                                     and Ananthajit Srikanth

         𝑡 =𝑣          variable reference                            1 ≡ S(0)             natural number 1
           | ⊥         non-terminating computation              𝑎 N ≡ (𝑎 = 𝑎)             natural-number type test
           | 0         natural-number constant zero             𝑝 T ≡ (𝑝 = 1)             boolean true test
           | S𝑡        natural-number successor                 𝑝 F ≡ (𝑝 = 0)             boolean false test
           | P𝑡        predecessor (clamping at zero)           𝑝 B ≡ 𝑝 ∨ ¬𝑝              boolean type test
           | 𝑡 ?𝑡 :𝑡   conditional evaluation                 𝑎 ≠ 𝑏 ≡ ¬(𝑎 = 𝑏 )           not-equals
           | 𝑡 [𝑡 ]    higher-order function application      𝑝 ∧ 𝑞 ≡ ¬(¬𝑝 ∨ ¬𝑞)          logical conjunction
           | 𝑡 =𝑡      equality of natural numbers           𝑝 → 𝑞 ≡ ¬𝑝 ∨ 𝑞               logical implication
           | ¬𝑡        logical negation                      𝑝 ↔ 𝑞 ≡ (𝑝 → 𝑞) ∧ (𝑞 → 𝑝 )   logical biconditional
           | 𝑡 ∨𝑡      logical disjunction                 S, K, . . . ≡ S(. . . )        combinator constants
            (a) Abstract term syntax of PGA                (b) Metalogical shorthands used in PGA

Table 3. Abstract term syntax and metalogical shorthands in propositional grounded arithmetic (PGA)




   P ROOF. Unfolding the definitions of biconditional, conjunction, and implication in BGA, we use
reflective arithmetization in 𝐵𝑈 (Theorem 4.16) and semantic completeness (Theorem 4.9).        □

  In summary, BGA represents a foundation for formal reasoning having the important properties of
being semantically and syntactically consistent, semantically complete, and sufficiently powerful to
reason about arithmetic and represent arbitrary Turing-complete computations. These represented
computations include grounded analogs to the logical operators of classical propositional logic, and
BGA’s own truth predicate. Unlike in first-order classical logic or Peano arithmetic, these grounded
logical operators remain firmly planted within the domain of computation.

5     Metatheory of propositional grounded arithmetic (PGA)
We now study a second concrete formulation of grounded arithmetic, propositional grounded
arithmetic or PGA. As its name suggests, PGA’s purpose is to be moderately more powerful and well-
equipped than BGA in logical expressiveness, by including grounded propositional logical operators
as primitives. PGA also has higher-order functions based on combinators, and other enhancements
described below. PGA does not include explicit quantifiers, however, but only implicit top-level
quantification as in BGA and PRA. We first summarize PGA’s syntax, semantics, and inference rules,
then examine how it reduces to (and hence is formally equivalent to) BGA.

5.1    PGA syntax
Table 3a shows the abstract syntax of PGA, and Table 3b lists metalogical shorthands we use.
   Unlike BGA, PGA makes no distinction between terms and formulas: both are syntactically just
terms. The boolean constants T and F are by definition the natural numbers 1 and 0, respectively
(Table 3b). The propositional-logic operators that conventionally would be part of formula syntax
are, in PGA, just natural-number computations yielding either 0 or 1 if they terminate at all.
   Primitive PGA syntax includes variables, the constants ⊥ representing a never-terminating com-
putation and 0 representing the natural number zero, the successor S and predecessor P operators,
“if-then-else” conditional evaluation using C-like syntax ‘𝑐 ? 𝑎 : 𝑏’, higher-order function application
‘f[a]’, equality, logical negation, and disjunction.
   Dynamic type tests, not-equals (≠), and other propositional operators are non-primitive shorthands
defined in terms of the above primitives. The symbols S, K, and I are similarly shorthands for
particular natural numbers encoding the higher-order function combinators of the SKI calculus [35].
PGA does not directly include lambda or let/letrec binders, but these are implementable atop the
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                        19


  𝐴𝑗 = 𝑛                     𝑎 ⇓𝑛           𝑎⇓0         𝑎 ⇓𝑛+1            𝑐⇓1          𝑎 ⇓𝑛   𝑐⇓0   𝑏 ⇓𝑛
   v𝑗 ⇓ 𝑛     0⇓0       S(𝑎) ⇓ 𝑛 + 1      P(𝑎) ⇓ 0          P(𝑎) ⇓ 𝑛       𝑐 ?𝑎 :𝑏 ⇓𝑛         𝑐 ?𝑎 :𝑏 ⇓𝑛
                              𝑎 ⇓𝑛          𝑎 ⇓𝑛      𝑏 ⇓𝑚         𝑎[𝑐] [𝑏 [𝑐]] ⇓ 𝑛
                             I [𝑎] ⇓ 𝑛       K [𝑎] [𝑏] ⇓ 𝑛         S [𝑎] [𝑏] [𝑐] ⇓ 𝑛
                              𝑎 ⇓𝑛       𝑏 ⇓𝑛        𝑎 ⇓𝑛       𝑏 ⇓𝑚       𝑛 ≠𝑚
                                 𝑎 =𝑏 ⇓ 1                      𝑎 =𝑏 ⇓ 0
                     𝑎⇓1         𝑎⇓0            𝑎⇓1            𝑏⇓1          𝑎⇓0         𝑏⇓0
                    ¬𝑎 ⇓ 0      ¬𝑎 ⇓ 1      𝑎 ∨𝑏 ⇓ 1          𝑎 ∨𝑏 ⇓ 1          𝑎 ∨𝑏 ⇓ 0

Table 4. Informal big-step structural operational semantics of propositional grounded arithmetic (PGA)




functionally-complete SKI calculus by combinator conversion [35, 73]. Our primary goal for PGA
was logical expressiveness, not functional-programming convenience.

5.2   PGA semantics
Our Isabelle/HOL development formally defines PGA’s semantics via the reduction to BGA described
below in Section 5.4. For expository purposes, however, Table 4 informally summarizes PGA’s
semantics using the same operational-semantic notation we used in BGA.
   One trivial but illustrative semantic difference between BGA and PGA is that P(0) is undefined
(denotes ⊥) in BGA but reduces to zero in PGA. This intentional difference arises from the distinct
goals of the two systems. BGA’s goal is minimality; we did not need P(0) to be defined, and leaving
it undefined simplified BGA’s semantics and inference rules slightly. PGA’s goal is logical reasoning
power and expressiveness, and for this purpose it is useful for predecessor to be defined at zero –
especially since some of PGA’s typing rules shown later in Table 7 would be unsound otherwise.
This “mismatch” between BGA’s and PGA’s predecessor operators is not a problem because PGA’s
predecessor does not reduce directly to BGA’s predecessor, as detailed below in Section 5.4, but
instead to a primitive-recursive minus one function having the proper semantics for PGA.
   Most of PGA’s primitives embody fairly standard semantics, including the if-then-else (‘𝑐 ? 𝑎 : 𝑏’),
higher-order function application using the SKI combinators, and the propositional negation and
disjunction connectives. The if-then-else and propositional operators taking boolean inputs reduce
only if the relevant inputs are indeed boolean (0 or 1), and otherwise never reduce, thereby denoting ⊥
by default. Evaluation is strict, except for if-then-else, where the not-taken branch need not evaluate
to anything, and disjunction, which follows Kleene’s strong 3-valued semantics [43] by reducing to 1
whenever either operand reduces to 1, even if the other operand never reduces.

5.3   PGA inference rules
Table 5 summarizes PGA’s logical inference rules, Table 6 shows its rules for natural numbers
and computation, and Table 7 lists a set of potentially-useful dynamic-typing rules, most of which
are derivable from the primary rules above. As should be obvious, PGA’s rule set seeks greater
expressiveness and reasoning power over minimality. Many of PGA’s rules are redundant and
derivable from others, including all those for conjunction, implication, and biconditional.
   PGA’s logical rules differ from familiar classical rules mainly in the incorporation of habeas
quid or dynamic typing conditions, as outlined earlier in Section 3. PGA’s boolE1 rule corresponds
to classical negation introduction, refuting a proposition 𝑝 on grounds that assuming 𝑝 leads to a
contradiction – but PGA first requires that 𝑝 be known to be boolean, ‘𝑝 B’. The boolE2 rule similarly
              Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
20                                                                                        and Ananthajit Srikanth

                                                                Logical negation (NOT)
                                                𝑝                     𝑝          ¬𝑝              𝑝 ∨ ¬𝑝
                                                      ¬¬IE                            ¬E                       boolIE
                                           ¬¬𝑝                              𝑞                        𝑝B
                        𝑝B            𝑝 ⊢𝑞            𝑝 ⊢ ¬𝑞                       𝑝B            ¬𝑝 ⊢ 𝑞             ¬𝑝 ⊢ ¬𝑞
                                                                 boolE1                                                       boolE2
                                          ¬𝑝                                                              𝑝
                                                             Logical disjunction (OR)
                                 𝑝                      𝑞                   ¬𝑝          ¬𝑞                    ¬(¬𝑝 ∧ ¬𝑞)
                                         ∨I1                    ∨I2                            ∨I3                            ∨IE
                               𝑝 ∨𝑞                   𝑝 ∨𝑞                      ¬(𝑝 ∨ 𝑞)                        𝑝 ∨𝑞
                               𝑝 ∨𝑞            𝑝 ⊢𝑟         𝑞 ⊢𝑟                      ¬(𝑝 ∨ 𝑞)                   ¬(𝑝 ∨ 𝑞)
                                                                      ∨E1                         ∨E2                         ∨E3
                                                𝑟                                       ¬𝑝                           ¬𝑞
                                                            Logical conjunction (AND)
                           𝑝         𝑞                     ¬𝑝                          ¬𝑞                      ¬(¬𝑝 ∨ ¬𝑞)
                                         ∧I1                          ∧I2                        ∧I3                             ∧IE
                            𝑝 ∧𝑞                      ¬(𝑝 ∧ 𝑞)                    ¬(𝑝 ∧ 𝑞)                          𝑝 ∧𝑞
                               𝑝 ∧𝑞                   𝑝 ∧𝑞                      ¬(𝑝 ∧ 𝑞)             ¬𝑝 ⊢ 𝑟          ¬𝑞 ⊢ 𝑟
                                         ∧E1                    ∧E2                                                           ∧E3
                                𝑝                       𝑞                                             𝑟
                                                                 Material implication
                                     𝑝B             𝑝 ⊢𝑞                  𝑝 →𝑞             𝑝                  ¬𝑝 ∨ 𝑞
                                                           →I                                  →E                       →IE
                                          𝑝 →𝑞                                    𝑞                            𝑝 →𝑞
                                                     Material biconditional (if-and-only-if)
 𝑝B        𝑞B       𝑝 ⊢𝑞         𝑞⊢𝑝                    𝑝 ↔𝑞                𝑝                  𝑝 ↔𝑞             𝑞                (𝑝 → 𝑞) ∧ (𝑞 → 𝑝 )
                                          ↔I                                    ↔ E1                                ↔ E2                              ↔IE
                𝑝 ↔𝑞                                              𝑞                                       𝑝                            𝑝 ↔𝑞
                                                                 Equals and unequals
        𝑎N           𝑎 =𝑏                 𝑎 =𝑏             𝑏 =𝑐                  𝑎 =𝑏           𝑝 ⟨𝑎, . . .⟩              𝑎 ≠𝑏         ¬(𝑎 = 𝑏 )
              =R               =S                                 =T                                           =E                ≠S                ≠IE
       𝑎 =𝑎          𝑏 =𝑎                           𝑎 =𝑐                                𝑝 ⟨𝑏, . . .⟩                      𝑏 ≠𝑎           𝑎 ≠𝑏

               Table 5. Logical inference rules for propositional grounded arithmetic (PGA)




allows proof by contradiction, again provided 𝑝 is boolean. Introducing an implication ‘𝑝 → 𝑞’ via
→I similarly requires 𝑝 to be boolean, and introducing a biconditional ‘𝑝 ↔ 𝑞’ via ↔I requires both
𝑝 and 𝑞 to be boolean.
   In our Isabelle/HOL formalization, all of these inference rules are proven sound by truth preserva-
tion, with respect to PGA’s (BGA-derived) semantics, as further described below. Some of the rules
in the HOL development include well-formedness conditions, which are needed because the formal
development works in a generic syntax not constrained to well-formed PGA terms alone.
Tables 5 to 7 are intended for interpretation strictly with respect to well-formed PGA syntax, and
thus do not need or show such well-formedness conditions.
  T HEOREM 5.1 ( SEMANTIC CONSISTENCY ). For any judgment ‘𝐻 ⊢ 𝑐’ provable in PGA and any
assignment 𝐴 under which all hypotheses in 𝐻 denote 1, conclusion 𝑐 denotes 1.
     P ROOF. By induction over proof length and the truth-preservation of each inference rule.                                                           □

  T HEOREM 5.2 ( SEMANTIC COMPLETENESS ). Every semantically true formula 𝑝 in PGA is
provable unconditionally using PGA’s inference rules (Section 5.3).
     P ROOF. Using BGA’s semantic completeness (Theorem 4.9) on the reduction to BGA of 𝑝.                                                               □
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                                                                  21


                                                                   Natural numbers
                                       𝑎 =𝑏                              𝑎 ≠𝑏                          𝑎N                    𝑎 =𝑎
                      0=I                              S=IE                             S≠IE                    S≠ 0I                 natIE
              0=0                 S(𝑎) = S(𝑏 )                      S(𝑎) ≠ S(𝑏 )                     S(𝑎) ≠ 0                    𝑎N
                                        𝑎N                          𝑎 = S(𝑏 )                     𝑎 =𝑏                      P(𝑎) ≠ P(𝑏 )
                     P=I1                           P=I2                         P=I3                           P=I4                          P≠E
        P(0) = 0                  P(S(𝑎) ) = 𝑎                      P(𝑎) = 𝑏                   P(𝑎) = P(𝑏 )                      𝑎 ≠𝑏
                                        𝑝 ⟨0, . . .⟩          𝑥 N, 𝑝 ⟨𝑥, . . .⟩ ⊢ 𝑝 ⟨S(𝑥 ), . . .⟩         𝑎N
                                                                                                                Ind
                                                                        𝑝 ⟨𝑎, . . .⟩
                                                    Conditional evaluation (if-then-else)
              𝑐       𝑎N                    ¬𝑐          𝑏N                   (𝑐 ? 𝑎 : 𝑏 ) = 𝑑         𝑐, 𝑎 = 𝑑 ⊢ 𝑞          ¬𝑐, 𝑏 = 𝑑 ⊢ 𝑞
                                ?I1                              ?I2                                                                          ?E
          (𝑐 ? 𝑎 : 𝑏 ) = 𝑎                (𝑐 ? 𝑎 : 𝑏 ) = 𝑏                                                  𝑞
                                            Higher-order function combinators S, K, I, R
                                 𝑎N                     𝑎N           𝑏N                         𝑎[𝑐 ] [𝑏 [𝑐 ] ] N
                                           II                               KI                                              SI
                             I [𝑎] = 𝑎                  K [𝑎] [𝑏 ] = 𝑎                  S [𝑎] [𝑏 ] [𝑐 ] = 𝑎[𝑐 ] [𝑏 [𝑐 ] ]
                     𝑎N         𝑏N                                𝑏 [𝑛] [ R [𝑎] [𝑏 ] [𝑛] ] N                                 𝑎N
                                        RI1                                                                 RI2                         sI
                   R [𝑎] [𝑏 ] [0] = 𝑎                  R [𝑎] [𝑏 ] [S(𝑛) ] = 𝑏 [𝑛] [ R [𝑎] [𝑏 ] [𝑛] ]                    s[𝑎] = S(𝑎)

Table 6. Natural-number and computation inference rules for propositional grounded arithmetic (PGA)




                                                         Propositional logic typing rules
        𝑝B                   𝑝B         𝑞B                        𝑝 ∨𝑞 B                       𝑝B          𝑞B                    𝑝 ∧𝑞 B
              ¬TIE                            ∨TI                                 ∨TE                           ∧TI                            ∧TE
       ¬𝑝 B                     𝑝 ∨𝑞 B                        (𝑝 B) ∨ (𝑞 B)                       𝑝 ∧𝑞 B                    (𝑝 B) ∨ (𝑞 B)
             𝑝B          𝑞B                      𝑝 →𝑞 B                                𝑝B      𝑞B                      𝑝 ↔𝑞 B
                                → TI                                → TE                             ↔ TI                              ↔ TE
                  𝑝 →𝑞 B                      (𝑝 B) ∨ (𝑞 B)                            𝑝 ↔𝑞 B                       (𝑝 B) ∧ (𝑞 B)

                                                                 Equality typing rules
                   𝑎N        𝑏N                        𝑎 =𝑏 B                          𝑎N      𝑏N                     𝑎 ≠𝑏 B
                                  =TI                                  =TE                           ≠TI                              ≠TE
                     𝑎 =𝑏 B                     (𝑎 N) ∧ (𝑏 N)                           𝑎 ≠𝑏 B                    (𝑎 N) ∧ (𝑏 N)
                                                          Natural number typing rules
                                                                       𝑎N                      𝑎N
                                                       0TI                     STIE                    PTIE
                                                0N                  S(𝑎) N                   P(𝑎) N
                                                              Computation typing rules
                          ⊥N                  𝑐B          𝑎N            𝑏N                           𝑐 ?𝑎 :𝑏 N
                                 ⊥TE                                          ? TI                                          ? TE
                            𝑝                          𝑐 ?𝑎 :𝑏 N                            (𝑐 B) ∧ ( (𝑎 N) ∨ (𝑏 N) )
                     𝑓 [𝑎] N                            𝑎N                       𝑎N          𝑏N                   𝑎[𝑐 ] [𝑏 [𝑐 ] ] N
                                      appTE                        ITIE                           KTIE                                STIE
                  ( 𝑓 N) ∧ (𝑎 N)                       I [𝑎] N                    K [𝑎] [𝑏 ] N                    S [𝑎] [𝑏 ] [𝑐 ] N
                             𝑎N         𝑏N                         𝑏 [𝑛] [ R [𝑎] [𝑏 ] [𝑛] ] N                       𝑎N
                                                 RTIE1                                            RTIE2                     sTIE
                            R [𝑎] [𝑏 ] [0] N                           R [𝑎] [𝑏 ] [S(𝑛) ] N                       s[𝑎] N

                  Table 7. Dynamic typing rules for propositional grounded arithmetic (PGA)
          Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
22                                                                                    and Ananthajit Srikanth

5.4   Reduction from PGA to BGA
As mentioned above, we formalized the semantics of PGA via reduction to BGA. Any well-formed
PGA term reduces to a corresponding BGA term via a reduction function 𝑅(𝑡), which is primitive-
recursive over the structure of the PGA term 𝑡 and yields a well-formed BGA term 𝑡 ′ intended to be
interpreted in the universal BGA instance 𝐵𝑈 . We briefly summarize these reductions as follows:
      • A variable reference v𝑖 in PGA reduces directly to variable reference v𝑖 in BGA.
      • ⊥ in PGA reduces to P(0) in BGA, which is undefined and hence nonterminating in BGA.
      • The constant 0 in PGA reduces to the corresponding constant 0 in BGA.
      • S(𝑎) in PGA reduces to S(𝑅(𝑎)) in BGA: that is, PGA’s primitive successor operator reduces
        directly to the BGA successor of the correspondingly-reduced subterm.
      • P(𝑎) in PGA reduces not to the BGA predecessor operator but to 𝑚(𝑅(𝑎)), where 𝑚(𝑥) is
        a primitive-recursive minus 1 function with the desired predecessor semantics for PGA. In
        particular, 𝑚(0) = 0, so P(0) in PGA is defined and denotes 0, unlike in BGA.
      • 𝑐 ? 𝑎 : 𝑏 (if-then-else) in PGA reduces to a pair of successive if-zero-else tests in BGA, first
        testing if 𝑅(𝑐) denotes 0 and if so yielding 𝑅(𝑏), then testing if 𝑅(𝑐) denotes 1 and if so
        yielding 𝑅(𝑎), and finally yielding ⊥ (nontermination) in any other case.
      • 𝑓 [𝑎] reduces to a general-recursive function for higher-order function application from
        our development of recursion theory, which (as with all general-recursive functions) is
        represented in the universal BGA instance 𝐵𝑈 . This function interprets 𝑅(𝑓 ) as the Gödel
        code of a primitive-recursive step function 𝑓 (𝑥, 𝑦) taking fixed argument 𝑥 = 𝑅(𝑎) and step
        count 𝑦, and performs an unbounded search for the first 𝑦 such that 𝑓 (𝑥, 𝑦) ≠ 0 if such 𝑦
        exists, yielding 𝑓 (𝑥, 𝑦) − 1 if so and otherwise never terminating. If either 𝑅(𝑓 ) or 𝑅(𝑎)
        fail to reduce to a natural number, or if 𝑅(𝑓 ) reduces to a number not encoding a valid
        primitive-recursive step function, then 𝑓 [𝑎] unconditionally denotes ⊥.
      • 𝑎 = 𝑏 in PGA reduces to 𝑒 (𝑅(𝑎), 𝑅(𝑏)), where 𝑒 (𝑥, 𝑦) is a primitive-recursive function
        represented in 𝐵𝑈 that tests 𝑥 and 𝑦 for equality, returning 1 if 𝑥 = 𝑦 and 0 otherwise.
      • ¬𝑎 reduces to 𝑁 (⌜𝑅(𝑎)⌝), where 𝑁 (𝑥) is the general-recursive function in 𝐵𝑈 reflectively
        implementing logical negation as described in Section 4.8. In particular, 𝑁 (𝑥) takes a Gödel-
        encoded BGA term, informally expressed here as ⌜𝑅(𝑎)⌝ – the encoded reduction to BGA
        of PGA subterm 𝑎 – and yields 0 if an unconditional BGA proof of 𝑅(𝑎) is found, yields 1 if
        an unconditional BGA refutation of 𝑅(𝑎) is found, and never terminates otherwise. Since a
        well-formed BGA formula is either equals ‘𝑎 = 𝑏’ or unequals ‘𝑎 ≠ 𝑏’, a refutation of ‘𝑎 = 𝑏’
        is just a proof of ‘𝑎 ≠ 𝑏’, and a refutation of ‘𝑎 ≠ 𝑏’ is likewise a proof of ‘𝑎 = 𝑏’.
      • 𝑎 ∨ 𝑏 in PGA reduces to 𝑂 (⟨⌜𝑅(𝑎)⌝, ⌜𝑅(𝑏)⌝⟩), where 𝑂 (𝑥) is the general-recursive function
        described in Section 4.8 that reflectively implements grounded logical disjunction. In par-
        ticular, 𝑂 is a general-recursive function represented in 𝐵𝑈 that takes a Cantor pairing of
        Gödel-encoded BGA terms, and uses a parallel proof search to return 1 if an unconditional
        BGA proof of either 𝑅(𝑎) or 𝑅(𝑏) is found, returns 0 if unconditional refutations of both
        𝑅(𝑎) and 𝑅(𝑏) are found, and otherwise never terminates.
   Truth under assignment: These reductions from PGA to BGA are relatively simple and direct,
ignoring the complexity in the underlying implementations within BGA of some of the resulting
terms. There is one further technical challenge embodied in this reduction, however. Our semantic-
correctness proofs of the reflective logical operators in BGA (Section 4.8) currently guarantee only
unconditional results, i.e., with respect to the empty set of hypotheses, or semantically in terms of
truth under all assignments, and not for arbitrary hypotheses or assignments. To define the semantics
of PGA’s logical primitives fully and prove PGA’s inference rules truth preserving, however, we need
a conditional semantics for PGA, allowing for arbitrary finite sets of hypotheses in the proof system
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                  23


and arbitrary assignments at the semantic level. This technical challenge is readily solvable, however,
because in BGA and PGA, any assignment of variables to natural numbers may be converted into a
substitution map of the same variables to corresponding syntactic numerals, which provably denotes
the same semantic value upon substitution into the term. That is, all syntactic contexts in BGA are
transparent: any subterm may be replaced with a semantically-equivalent subterm without changing
the meaning of the context term within which the substitution is done.
   To define the semantics of PGA, therefore, we first use the PGA-to-BGA reduction above to
define an unconditional semantics for PGA in which all variables are implicitly undefined, i.e.,
corresponding to the null (empty) assignment. We then define a corresponding conditional semantics
for PGA, taking an arbitrary assignment 𝐴 of variables to semantic domain elements (either natural
numbers or ⊥), by converting all natural-number elements of 𝐴 into PGA numerals substituted for
the corresponding variables in the PGA term, then employing the underlying unconditional semantics
of the resulting term. Because PGA numerals reduce directly to corresponding BGA numerals, these
substitutions map identically into the BGA term upon reduction. In effect, even though the semantics
of BGA is defined over arbitrary assignments, our development of PGA’s semantics ultimately
uses only the semantics of BGA terms under the empty (all-⊥) assignment, because all variables
assigned natural numbers in PGA assignment 𝐴 have already been replaced with PGA numerals
before reducing the term to BGA. The limitation that our BGA formalization of the reflective logical
operators (Section 4.8) applies only to unconditional provability, or to truth under all assignments in
BGA, is therefore no longer a problem because our formalization of PGA’s semantics depends only
on truth under all assignments at the BGA level.


5.5   Functional and logical expressiveness and reasoning power of PGA
   Functional completeness: Because PGA’s higher-order function-application primitive 𝑓 [𝑎] inter-
prets 𝑓 as the Gödel code of an arbitrary primitive-recursive step function, and every general-recursive
function is expressible as such a step function, PGA’s semantics are functionally complete. We can
take any general-recursive function implemented as a primitive-recursive step function, construct its
Gödel code directly as a PGA numeral (or compute the same number in any other fashion within
PGA), and apply it using PGA’s 𝑓 [𝑎] primitive, yielding correct and well-defined computational
semantics, regardless of how 𝑓 is computed or whether it terminates on argument 𝑎.
   Our proof system for PGA currently provides inference rules only for a few particular general-
recursive functions, representing standard combinators such as S, K, I, R. Of these combinators,
S and K alone are well-known to be functionally complete [35]. Our recursion combinator R
corresponds to the one in Gödel’s “Dialectica” System T [29]. From System T, we also include a
“successor” function as a combinator s, which is extensionally equivalent to PGA’s successor operator.
This redundancy is primarily required to represent any primitive recursive function purely in terms of
PGA function definitions. Other combinators and general-recursive functions could readily be added
to PGA’s proof system, together with truth-preserving inference rules, without requiring changes to
PGA’s semantics. We fully acknowledge that (metalogical) functional completeness is not the same
as (practical) function-definition convenience, however, leaving to future work the important task of
building grounded reasoning systems in which expressing arbitrary recursive functions is not just
provably possible but also expressible using more-familiar notation such as that of popular functional
programming languages.
   Finally, although the precise termination-proving power of PGA (its proof-theoretic ordinal) is
currently unknown, it lies between 𝜔 𝜔 – that of Skolem’s PRA – and 𝜔 1CK , the Church-Kleene ordinal.
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
24                                                                                      and Ananthajit Srikanth

         Rules of inference            C    I    G                     Rules of replacement    C    I    G
         Modus ponens (MP)             ✓    ✓    ✓                     De Morgan’s laws        ✓    ✗    ✓
         Modus tollens (MT)            ✓    ✓    ✓                     Commutation             ✓    ✓    ✓
         Hypothetical syllogism (HS)   ✓    ✓    ✓                     Association             ✓    ✓    ✓
         Disjunctive syllogism (DS)    ✓    ✓    ✓                     Distribution            ✓    ✓    ✓
         Constructive dilemma (CD)     ✓    ✓    ✓                     Double negation         ✓    ✗    𝑃
         Destructive dilemma (DD)      ✓    ✓    ✓                     Transposition           ✓    ✗    ✓
         Absorption (Abs)              ✓    ✓    B                     Material implication    ✓    ✗    ✓
         Simplification (Simp)         ✓    ✓    ✓                     Material equivalence    ✓    ✗    ✓
         Conjunction (Conj)            ✓    ✓    ✓                     Exportation             ✓    ✓    ✓
         Addition (Add)                ✓    ✓    ✓                     Tautology               ✓    ✓    𝑃
Table 8. Copi’s rules of inference and replacement [20]: a comparison between classical, intuitionistic,
and grounded reasoning in PGA. Rules that fail at least partially under intuitionistic logic have an ✗ in
the 𝐼 column. Rules requiring a dynamic boolean-type check in PGA have B in the 𝐺 column. Rules
requiring only a static propositional-formula check in PGA (not a termination proof) show 𝑃 under 𝐺.
Destructive dilemma (DD) appeared only in early editions, and was replaced with Absorption (Abs) in
later editions; each edition thus listed only nine of these ten rules of inference.



   T HEOREM 5.3 ( PRIMITIVE - RECURSIVE FUNCTION TERMINATION ). For any 2-argument primitive-
recursive function 𝑓 (𝑥, 𝑦) represented in PGA via combinators, PGA can prove 𝑓 (𝑥, 𝑦) terminating
for all natural-number arguments 𝑥 and 𝑦: that is, ‘𝑥 N, 𝑦 N ⊢ 𝑓 (𝑥, 𝑦) N’.
     P ROOF. By induction on the structure of the primitive-recursive function 𝑓 .                               □

    Propositional completeness: Since their first publication in 1953, Irving M. Copi’s rules of
 inference and rules of replacement have been central to one of the most influential informal and
 pedagogical formulations of classical logic [20, 21]. Table 8 summarizes the validity of these rules
 in classical, intuitionistic, and grounded reasoning. The table lists all ten rules of inference and
 ten rules of replacement that appeared across the various editions of Copi’s textbook. Only nine
 inference rules appear in each edition because the destructive dilemma (DD) rule in early editions
was replaced with absorption (Abs) in later editions. While all of Copi’s rules of inference remain
valid intuitionistically, five of his rules of replacement fail at least partially under intuitionistic logic.
    As our mechanically-checked analysis confirms, however, 17 of these 20 rules remain valid in PGA
without any new preconditions. Only the absorption inference rule added in more recent editions,
 deriving ‘𝑝 → (𝑝 ∧ 𝑞)’ from ‘𝑝 → 𝑞’, requires a new habeas quid dynamic-typing precondition
‘𝑝 B’. Copi’s replacement rules for double negation ‘𝑝 ≡ ¬¬𝑝’ and tautology ‘𝑝 ≡ 𝑝 ∧ 𝑝’, ‘𝑝 ≡ 𝑝 ∨ 𝑝’
 need only a simple static check that 𝑝 is any propositional operator in PGA that yields nothing other
 than 0 or 1, but 𝑝 need not terminate.3 In contrast with intuitionism, therefore, all of the rules of
 inference and replacement appearing in the first edition of Copi’s textbook [20], largely representing
 logical principles dating back to antiquity, remain valid in PGA. Copi’s rules of replacement, in
 particular, each correspond to a bidirectional rule in Table 5 and a pair of rules in our formalization,
 one in each direction (see Section A.2 for a detailed index).
    This observation suggests that grounded propositional reasoning, as embodied in PGA, appears
 more aligned with the informal and pedagogical traditions of classical logic than is intuitionistic
 logic, affecting only three of Copi’s rules rather than five. The remaining differences, furthermore,
 are easily seen as a divergence in type systems rather than in basic reasoning principles. We see these
 results as suggesting that future mature systems of grounded reasoning could potentially be just as
3 Distinguishing terms from formulas in PGA, like BGA already does, would eliminate these two exception cases.
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                    25


usable and “intuitive” as intuitionistic logic, if not more so. The fact that grounded reasoning allows
unconstrained recursion, while defusing the paradoxes of naïve propositional logic, may arguably
make grounded reasoning more intuitive in some respects even than classical logic.

6   Related work
Church’s inconsistent formal system based on his untyped lambda calculus [16] launched an early
precedent in GA’s general direction by focusing on recursive computation. Church’s system also
anticipated GA in certain details, such as by rejecting the law of excluded middle (like Brouwer’s
intuitionism [8, 34]) while preserving the law of double negation (like GA but unlike intuitionism).
   Scott’s domain theory [66], LCF [52, 53, 67] and PCF [59], together with ideas from Kripke’s
theory of truth [45] and the paracomplete logics it inspired [26,50], contain many of the key ideas that
inspired GA. Scott was also interested in “type-free” approaches to reasoning about computation [65],
and was aware at least of Kripke’s earlier modal-logic work, but neither appears to have “connected”
Kripke’s theory of truth with Scott’s theory of computation. Speculating a bit, perhaps Scott and
Kripke might well have formulated grounded deduction in the 1970s if this connection had occurred.
   Most proof assistants rely for consistency on stratified type theories in the tradition of Russell [75]
and Martin-Löf [48, 49]. Besides avoiding the known logical paradoxes, these type systems aid
automated reasoning by constraining the deduction search space. Dependent type systems as used in
proof assistants like Coq/Rocq [15], Lean [25], and Agda [7], increase expressiveness by allowing
types to depend on computations. Preserving consistency and avoiding Girard’s paradox [28, 39],
however, still requires assigning types to stratified universes, which limits expressiveness, motivates
numerous variations [4], and complicates desirable features such as polymorphism [60] and metapro-
gramming [38]. By presenting an alternative to stratification for preserving consistency, grounded
reasoning as in GA might in the future enable simpler or more flexible dependent-type systems, at a
cost of weaker and less-familiar deduction rules with dynamic habeas quid preconditions.
   A large body of existing work focuses on proving program termination [18, 19, 77] and non-
termination [13, 31, 62]. This work generally relies on classical reasoning about computation. While
GA introduces a different logical approach to termination proving via its habeas quid or dynamic-
typing preconditions, nevertheless we hope and expect that most of the existing work on automated or
semi-automated termination and non-termination proving should be readily portable into a grounded
reasoning context. Working out the details remains for future work, however.
   The way we satisfy habeas quid preconditions or prove termination in GA, essentially by evaluating
potentially-abstract or symbolic GA terms in reverse (Section 3.2.1), is conceptually and stylistically
reminiscent of symbolic execution [2, 24, 32, 41]. Like automated termination proving, however,
symbolic execution generally focuses on achieving useful results automatically (e.g., finding concrete
bugs in deployed software) with manageable time and storage complexity, while managing the
exponential state-space explosion problem. While proving termination in GA is similar in principle to
symbolic execution, we make no pretense that GA’s built-in formal flavor of “symbolic execution” is
actually practical in terms of time or space complexity; we claim only that GA’s form of “symbolic
execution” is Turing computable. We hope and expect that practical symbolic-execution techniques
could be adapted to GA, and are thus orthogonal and complementary to GA’s goals, although we
again leave further exploration of this relationship to future work.

7 Conclusion and future work
Grounded arithmetic takes a step towards practical paracomplete formal reasoning about computation.
GA allows direct expression of unconstrained recursive definitions, including those leading to logical
paradox and inconsistency in classical and intuitionistic formal systems. GA defuses such paradoxes
by adding habeas quid or dynamic-typing preconditions to key propositional-logic inference rules.
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
26                                                                                      and Ananthajit Srikanth

Basic grounded arithmetic or BGA, a computational kernel, is semantically and syntactically consis-
tent, semantically complete, and able to express all general-recursive computation directly, including
grounded logical connectives and BGA’s own truth predicate. Propositional grounded arithmetic or
PGA builds on BGA to provide the richer logical expressiveness of grounded propositional-logic
primitives, as well as higher-order functions based on combinators. Much work remains, however,
for example, to incorporate and prove the consistency of grounded quantifiers, to make grounded
reasoning more type-rich and convenient in practical reasoning about real software, and to resolve
open metalogical questions such as PGA’s termination-proving strength (proof-theoretic ordinal).
   Could GA achieve the “Fregean paradise of ‘type-free’ functions” sought by Church, Curry, and
Scott [65]? On one hand, GA’s habeas quid constraints on inference certainly seem like (dynamic)
typing rules; in that respect GA is obviously not “type-free.” But a more realistic interpretation
of the term “type-free” in this context is an absence of type stratification in the Russell tradition.
This tradition is still reflected in the stratified “universes” needed to keep modern dependent-type
theories (apparently) consistent, for example. GA is free of Russellian type stratification: types
and their properties in GA share exactly the same syntactic and semantic spaces as anything else
expressible in GA, and everything happens in one closed logical universe. Since the key boolean and
natural-number type predicates in GA – ‘𝑎 N’ and ‘𝑎 B’ – are not even primitives in our formulation,
but just abbreviations for ‘𝑎 = 𝑎’ and ‘𝑎 ∨ ¬𝑎’, respectively, merely unfolding these definitions in any
GA term makes it appear quite “type-free” indeed. Even if GA is indeed “type-free” from such a
perspective, is the result a “paradise”? Only time, experience, and further exploration will tell.

References
 [1] Wilhelm Ackermann. Zum Hilbertschen aufbau der reellen zahlen. Mathematische Annalen, 99:118–133, December
     1928.
 [2] Roberto Baldoni, Emilio Coppa, Daniele Cono D’elia, Camil Demetrescu, and Irene Finocchi. A survey of symbolic
     execution techniques. ACM Computing Surveys (CSUR), 51(3):1–39, May 2018.
 [3] Clemens Ballarin. Tutorial to locales and locale interpretation, 2025.
 [4] Andrej Bauer, Philipp G. Haselwarter, and Peter LeFanu Lumsdaine. A general definition of dependent type theories,
     September 2020. arXiv preprint 2009.05539.
 [5] JC Beall, editor. Revenge of the Liar: New Essays on the Paradox. Oxford University Press, February 2008.
 [6] Errett Bishop. Foundations of Constructive Analysis. Academic Press, New York, 1967.
 [7] Ana Bove, Peter Dybjer, and Ulf Norell. A brief overview of Agda - a functional language with dependent types. In 22nd
     International Conference on Theorem Proving in Higher Order Logics (TPHOLs), page 73–78. Springer-Verlag, 2009.
 [8] Luitzen Egbertus Jan Brouwer. Over de Grondslagen der Wiskunde. PhD thesis, Universiteit van Amsterdam, 1907.
 [9] Luitzen Egbertus Jan Brouwer. Brouwer’s Cambridge Lectures on Intuitionism. Cambridge University Press, 1981.
[10] Benjamin Bürki. Grounded verification of recursive trace systems. Master’s thesis, EPFL, June 2026.
[11] Tim Button and Sean Walsh. Philosophy and Model Theory. Oxford University Press, May 2018.
[12] Robert Cartwright, Rebecca Parsons, and Moez AbdelGawad. Domain theory: An introduction, June 2016. arXiv preprint
     1605.05858.
[13] Krishnendu Chatterjee, Ehsan Kafshdar Goharshady, Petr Novotný, and Ðord̄e Žikelić. Proving non-termination
     by program reversal. In 42nd ACM SIGPLAN International Conference on Programming Language Design and
     Implementation (PLDI), pages 1033–1048, June 2021.
[14] Adam Chlipala. Parametric higher-order abstract syntax for mechanized semantics. In 13th International Conference on
     Functional Programming (ICFP), September 2008.
[15] Adam Chlipala. Certified Programming with Dependent Types: A Pragmatic Introduction to the Coq Proof Assistant.
     The MIT Press, December 2013.
[16] Alonzo Church. A set of postulates for the foundation of logic. Annals of Mathematics, 33(2):346–366, April 1932.
[17] Alonzo Church. The Calculi of Lambda-Conversion. Number 6 in Annals of Mathematics Studies. Princeton University
     Press, 1941.
[18] Michael A. Colón and Henny B. Sipma. Practical methods for proving program termination. In International Conference
     on Computer Aided Verification, pages 442–454, January 2002.
[19] Byron Cook, Andreas Podelski, and Andrey Rybalchenko. Termination proofs for systems code. In 27th ACM SIGPLAN
     Conference on Programming Language Design and Implementation (PLDI), June 2006.
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                                     27


[20] Irving M. Copi. Introduction to Logic. Macmillan, 1st edition, 1953.
[21] Irving M. Copi, Carl Cohen, and Victor Rodych. Introduction to Logic. Routledge, 15th edition, 2019.
[22] H. B. Curry. Grundlagen der kombinatorischen logik. American Journal of Mathematics, 52(3):509–536, July 1930.
[23] H. B. Curry. The inconsistency of certain formal logics. Journal of Symbolic Logic, 7(3):115–117, September 1942.
[24] Frank S. de Boer and Marcello Bonsangue. Symbolic execution formally explained. Formal Aspects of Computing,
     33:617–636, February 2021.
[25] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming language. In 28th International
     Conference on Automated Deduction (CADE), pages 625–635, July 2021.
[26] Hartry Field. Saving Truth From Paradox. Oxford University Press, May 2008.
[27] Bryan Ford. Reasoning around paradox with grounded deduction, September 2024. arXiv preprint 2409.08243.
[28] Jean-Yves Girard. Interprétation fonctionnelle et élimination des coupures dans l’arithmétique d’ordre supérieur. PhD
     thesis, 1972.
[29] Kurt Gödel. Über eine bisher noch nicht benützte erweiterung des finiten standpunktes, 1958.
[30] M. J. C. Gordon and T. F. Melham, editors. Introduction to HOL: A theorem proving environment for higher order logic.
     Cambridge University Press, June 1993.
[31] Ashutosh Gupta, Thomas A. Henzinger, Rupak Majumdar, Andrey Rybalchenko, and Ru-Gang Xu. Proving non-
     termination. In 35th annual ACM SIGPLAN-SIGACT symposium on Principles of programming languages (POPL),
     pages 147–158, January 2008.
[32] Jingxuan He, Gishor Sivanrupan, Petar Tsankov, and Martin Vechev. Learning to explore paths for symbolic execution.
     In ACM SIGSAC Conference on Computer and Communications Security (CCS), pages 2526–2540, November 2021.
[33] Arend Heyting. Intuitionism: An introduction. Studies in logic and the foundations of mathematics. North-Holland,
     January 1971.
[34] Arend Heyting, editor. Philosophy and Foundations of Mathematics, volume 1 of L. E. J. Brouwer Collected Works.
     North-Holland, 1975.
[35] J. Roger Hindley and Jonathan P. Seldin. Lambda-Calculus and Combinators: An Introduction. Cambridge University
     Press, 2nd edition, August 2008.
[36] C.A.R. Hoare. An axiomatic basis for computer programming. Communications of the ACM, 12(10):576–580, October
     1969.
[37] William A. Howard. The formulae-as-types notion of construction. In To H.B. Curry: Essays on Combinatory Logic,
     Lambda Calculus and Formalism, pages 479–490. Academic Press, 1980.
[38] Jason Z. S. Hu and Brigitte Pientka. A dependent type theory for meta-programming with intensional analysis. In
     Proceedings of the ACM on Programming Languages, volume 9, pages 416–445, January 2025.
[39] Antonius J. C. Hurkens. A simplification of Girard’s paradox. In International Conference on Typed Lambda Calculi
     and Applications, pages 266–278. Springer Berlin Heidelberg, 1995.
[40] Sascha Kehrli. Formalizing grounded arithmetic atop Isabelle/Pure, September 2025.
[41] James C. King. Symbolic execution and program testing. Communications of the ACM, 19(7):385–394, July 1976.
[42] S. C. Kleene and J. B. Rosser. The inconsistency of certain formal logics. Annals of Mathematics, 36(3):630–636, July
     1935.
[43] Stephen Cole Kleene. Introduction to Metamathematics. North-Holland, 1952.
[44] Gerwin Klein, June Andronick, Kevin Elphinstone, Toby Murray, Thomas Sewell, Rafal Kolanski, and Gernot Heiser.
     Comprehensive formal verification of an OS microkernel. ACM Transactions on Computer Systems (TOCS), 32(1):1–70,
     February 2014.
[45] Saul Kripke. Outline of a theory of truth. The Journal of Philosophy, 72(19):690–716, November 1975.
[46] Ondřej Kunčar and Andrei Popescu. A consistent foundation for Isabelle/HOL. Journal of Automated Reasoning,
     62:531–555, January 2018.
[47] Xavier Leroy, Sandrine Blazy, Daniel Kästner, Bernhard Schommer, Markus Pister, and Christian Ferdinand. CompCert
     – a formally verified optimizing compiler. In Embedded Real Time Software and Systems (ERTS), January 2016.
[48] Per Martin-Löf. An intuitionistic theory of types. Technical report, University of Stockholm, 1972.
[49] Per Martin-Löf. Intuitionistic type theory, June 1980. Notes by Giovanni Sambin of a series of lectures given in Padua,
     June 1980.
[50] Tim Maudlin. Truth and Paradox. Clarendon Press, September 2006.
[51] Elliott Mendelson. Introduction to Mathematical Logic. Routledge, 6th edition, July 2015.
[52] Robin Milner. Implementation and applications of Scott’s logic for computable functions. 7(1):1–6, 1972.
[53] Robin Milner. Models of LCF. Technical report, University of Edinburgh, 1976. Mathematical Centre Tracts.
[54] Robin Milner. Communicating and Mobile Systems: The Pi Calculus. Cambridge University Press, May 1999.
[55] Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. Isabelle/HOL: A Proof Assistant for Higher-Order Logic.
     Springer, April 2002. Lecture Notes in Computer Science, 2283.
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
28                                                                                      and Ananthajit Srikanth

[56] Ulf Norell. Towards a practical programming language based on dependent type theory. PhD thesis, 2007.
[57] Lawrence C. Paulson. A machine-assisted proof of Gödel’s incompleteness theorems for the theory of hereditarily finite
     sets. The Review of Symbolic Logic, 7(3):484–498, April 2014.
[58] Frank Pfenning and Conal Elliott. Higher-order abstract syntax. In Programming Language Design and Implementation
     (PLDI), June 1988.
[59] G.D. Plotkin. LCF considered as a programming language. Theoretical Computer Science, (5):223–255, 1977.
[60] Josselin Poiret, Gaëtan Gilbert, Kenji Maillard, Pierre-Marie Pédrot, Matthieu Sozeau, Nicolas Tabareau, and Éric Tanter.
     All your base are belong to 𝑈 𝑠 : Sort polymorphism for proof assistants. In Proceedings of the ACM on Programming
     Languages, volume 9, pages 2253–2281, January 2025.
[61] Graham Priest. In Contradiction: A Study of the Transconsistent. Clarendon Press, 2nd edition edition, April 2006.
[62] Azalea Raad, Julien Vanegue, and Peter O’Hearn. Non-termination proving at scale. In Proceedings of the ACM on
     Programming Languages, volume 8, pages 246–274, October 2024.
[63] J.C. Reynolds. Separation logic: a logic for shared mutable data structures. In 17th Annual IEEE Symposium on Logic in
     Computer Science, July 2002.
[64] Raphael M. Robinson. An essentially undecidable axiom system. In Proceedings of the International Congress of
     Mathematics, pages 729–730, 1950.
[65] Dana S. Scott. Combinators and classes. In Symposium on Lambda-Calculus and Computer Science Theory, pages 1–26,
     March 1975.
[66] Dana S. Scott. Domains for denotational semantics. In International Colloquium on Automata, Languages and Program-
     ming (ICALP), 1982.
[67] Dana S. Scott. A type-theoretical alternative ISWIM, CUCH, OWHY. Theoretical Computer Science, 121:411–440,
     1993.
[68] Jonathan P. Seldin. The logic of curry and church. In Dov Gabbay, editor, The Handbook of the History of Logic,
     volume 5, pages 819–874. 2009.
[69] Keith Simmons. Universality and the Liar: An Essay on Truth and the Diagonal Argument. Cambridge University Press,
     July 1993.
[70] Thoralf Skolem. Begründung der elementaren arithmetik durch die rekurrierende denkweise ohne anwendung scheinbarer
     veränderlichen mit unendlichem ausdehnungsbereich. Videnskapsselskapets skrifter, I. Matematisk-naturvidenskabelig
     klasse(6), 1923.
[71] Thomas Streicher. Domain-Theoretic Foundations of Functional Programming. World Scientific, December 2006.
[72] Alfred Tarski. The concept of truth in formalized languages. In John Corcoran, editor, Logic, Semantics, Metamathemat-
     ics: Papers from 1923 to 1938. Hackett Publishing Company, December 1983.
[73] D. A. Turner. A new implementation technique for applicative languages. Software: Practice and Experience, 9:31–49,
     1979.
[74] Jean van Heijenoort, editor. From Frege to Gödel: A Source Book in Mathematical Logic, 1879–1931. Source Books in
     History of Sciences. Fourth printing edition, January 2002.
[75] Alfred North Whitehead and Bertrand Russell. Principia Mathematica, volume 1. Rough Draft Printing, 2011.
[76] Glynn Winskel. Formal Semantics of Programming Languages. The MIT Press, February 1993.
[77] Jianan Yao, Runzhou Tao, Ronghui Gu, and Jason Nieh. Mostly automated verification of liveness properties for
     distributed protocols with ranking functions. In Proceedings of the ACM on Programming Languages, volume 8, pages
     1028–1059, January 2024.
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                   29


APPENDIX
A     Key definitions and theorems in HOL formalization of BGA and PGA
This appendix is intended to bridge the results summarized in the main paper with relevant details
of our mechanically-checked development of BGA and PGA in Isabelle/HOL. We first present in
Section A.1 a concise index of theorems stated or implied in the main paper and the Isabelle/HOL
theorems to which they correspond, then subsequent sections provide further background on our Is-
abelle/HOL mechanization approach that may be helpful in navigating and understanding it. Nothing
in this appendix should be essential for understanding either the main paper or the Isabelle/HOL
development considered independently of each other.

A.1    Index of key Isabelle/HOL types, definitions, locales, and theorems
This table briefly lists key elements of the HOL formalization, cross-referencing the relevant sections
of the main paper with particular key concepts, corresponding Isabelle/HOL names, and the theory
file and (when applicable) the locale in which the name is defined or proven.
 Sec Description                Kind       HOL theory file   Locale        Name
 4.1 BGA term syntax            Type       BGA_Syntax                      tm
     BGA formula syntax         Type       BGA_Syntax                      fm
 4.2 BGA inference rules        Inductive BGA_Proof          bga           derives
     Primitive-recursiveness    Sublocale BGA_Primrec        bga_syntax    prf_derives_primrec
 4.3 Operational semantics      Definition BGA_Semantics     bga           os
 4.4 Semantic consistency       Sublocale BGA_Semantics      bga           model_preserves_truth
     Syntactic consistency      Sublocale BGA_Semantics      bga           model_eq_preserves_truth
 4.5 Semantic completeness      Sublocale BGA_Complete       bga           model_complete
 4.6 Primitive recursion        Theorem BGA_RecDef                         bga_ex_stdlib_pri_rep
     PR termination             Theorem BGA_Provable                       pri_rep_nat
     General recursion          Theorem BGA_RecDef                         bga_ex_stdlib_gri_rep
     Metacircular evaluator     Sublocale BGA_Universal      bga_universal bga_std_app
     Universal recursion        Sublocale BGA_Universal      bga_universal bga_univ
 4.7 Arithmetization            Sublocale BGA_LogicOp        bga_univ      bga_sfPf_rep
 4.8 Logical negation           Sublocale BGA_LogicOp        bga_univ      bga_sfPneg_rep
     Logical disjunction        Sublocale BGA_LogicOp        bga_univ      bga_sfPor_rep
     Full propositional logic   Sublocale BGA_LogicOp        bga_univ      sfPf_sfde_pred_rep
     Truth predicate            Sublocale BGA_LogicOp        bga_univ      model_truth_predicate
 5.1 PGA term syntax            Type       PGA_Syntax        pga           tm
 5.3 PGA inference rules        Inductive PGA_Proof          pga           derives
 5.4 Reduction to BGA           Function PGA_Reduce          pga           tmr
     Semantic consistency       Sublocale PGA_Semantics      pga           model_preserves_truth
     Syntactic consistency      Sublocale PGA_Semantics      pga           model_eq_preserves_truth
     Semantic completeness      Sublocale PGA_Semantics      pga           model_complete
     PR termination             Theorem PGA_RecDef                         pridx_to_trm_num
     Truth predicate            Sublocale PGA_Semantics      pga           model_truth_predicate

A.2    Index of PGA formalizations of Copi’s rules of logic
The following table cross-references the nineteen rules of Copi’s classical propositional logic with
their formalization as constructors of PGA’s derives inductive predicate (theory PGA_Proof, locale
pga). Because HOL inductive predicates admit only unidirectional constructors, each of Copi’s ten
rules of replacement (a bidirectional equivalence) is split into one constructor per direction. Each rule
of replacement is added in substitution form 𝑃 CJΓ ⊢ [𝑖 ↦→ 𝐴] 𝑓 K =⇒ wft 𝑓 =⇒ 𝑃 DJΓ ⊢ [𝑖 ↦→ 𝐵] 𝑓 K,
replacing the subformula 𝐴 by 𝐵 uniformly at all free occurrences of the placeholder variable 𝑣𝑖 within
a well-formed context 𝑓 . Interestingly, only Absorption needa a habeas-quid dynamic type-check
𝑝 B absent from Copi’s classical rules.
             Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
30                                                                                       and Ananthajit Srikanth

   The replacement rules for tautology and double negation need simple static (structural) check that
𝑝 is a proposition in PGA yielding no result other than 0 or 1, but 𝑝 need not be proven terminating:
i.e., does not need a full habeas quid precondition. Distinguishing terms from formulas in PGA, as
in BGA and in logic tradition more generally, would eliminate these two exception cases.
     Copi rule            derives rule          Isabelle/HOL formulation
     Rules of inference
     Modus Ponens         pr_impE               𝑃 CJΓ ⊢ 𝑝 → 𝑞K =⇒ 𝑃 CJΓ ⊢ 𝑝K =⇒ 𝑃 DJΓ ⊢ 𝑞K
     (M.P.)
     Modus Tollens        pr_modus_tollens      𝑃 CJΓ ⊢ 𝑝 → 𝑞K =⇒ 𝑃 CJΓ ⊢ ¬𝑞K =⇒ 𝑃 DJΓ ⊢ ¬𝑝K
     (M.T.)
     Hypothetical         pr_hyp_syl            𝑃 CJΓ ⊢ 𝑝 → 𝑞K =⇒ 𝑃 CJΓ ⊢ 𝑞 → 𝑟 K =⇒ 𝑃 DJΓ ⊢ 𝑝 → 𝑟 K
     Syllogism (H.S.)
     Disjunctive Syllo-   pr_disj_syl1          𝑃 CJΓ ⊢ 𝑎 ∨ 𝑏K =⇒ 𝑃 CJΓ ⊢ ¬𝑎K =⇒ 𝑃 DJΓ ⊢ 𝑏K
     gism (D.S.)
                          pr_disj_syl2          𝑃 CJΓ ⊢ 𝑎 ∨ 𝑏K =⇒ 𝑃 CJΓ ⊢ ¬𝑏K =⇒ 𝑃 DJΓ ⊢ 𝑎K
     Constructive         pr_const_dilemma      𝑃 CJΓ ⊢ 𝑝 ∨ 𝑞K =⇒ 𝑃 CJΓ ⊢ 𝑝 → 𝑟 K =⇒ 𝑃 CJΓ ⊢ 𝑞 → 𝑠K =⇒
     Dilemma (C.D.)                             𝑃 DJΓ ⊢ 𝑟 ∨ 𝑠K
     Destructive          pr_dest_dilemma       𝑃 CJΓ ⊢ ¬𝑟 ∨ ¬𝑠K =⇒ 𝑃 CJΓ ⊢ 𝑝 → 𝑟 K =⇒ 𝑃 CJΓ ⊢ 𝑞 → 𝑠K =⇒
     Dilemma (D.D.)                             𝑃 DJΓ ⊢ ¬𝑝 ∨ ¬𝑞K
     Simplification       pr_conjE1             𝑃 CJΓ ⊢ 𝑎 ∧ 𝑏K =⇒ 𝑃 DJΓ ⊢ 𝑎K
     (Simp.)
                          pr_conjE2             𝑃 CJΓ ⊢ 𝑎 ∧ 𝑏K =⇒ 𝑃 DJΓ ⊢ 𝑏K
     Conjunction          pr_conjI1             𝑃 CJΓ ⊢ 𝑎K =⇒ 𝑃 CJΓ ⊢ 𝑏K =⇒ 𝑃 DJΓ ⊢ 𝑎 ∧ 𝑏K
     (Conj.)
     Addition (Add.)      pr_disjI1               𝑃 CJΓ ⊢ 𝑎K =⇒ wff 𝑏 =⇒ 𝑃 DJΓ ⊢ 𝑎 ∨ 𝑏K
                          pr_disjI2               𝑃 CJΓ ⊢ 𝑏K =⇒ wff 𝑎 =⇒ 𝑃 DJΓ ⊢ 𝑎 ∨ 𝑏K
     Absorption (Abs.) pr_absorption              𝑃 CJΓ ⊢ 𝑝 BK =⇒ 𝑃 CJΓ ⊢ 𝑝 → 𝑞K =⇒ 𝑃 DJΓ ⊢ 𝑝 → (𝑝 ∧ 𝑞)K
     Rules of replacement (each 𝑃 CJΓ ⊢ [𝑖 ↦→ 𝐴] 𝑓 K =⇒ wft𝑓 =⇒ 𝑃 DJΓ ⊢ [𝑖 ↦→ 𝐵 ] 𝑓 K)
     De Morgan (De        pr_deM_and1             𝐴 = ¬(𝑝 ∧ 𝑞), 𝐵 = ¬𝑝 ∨ ¬𝑞
     M.)
                          pr_deM_and2             𝐴 = ¬𝑝 ∨ ¬𝑞, 𝐵 = ¬(𝑝 ∧ 𝑞)
                          pr_deM_or1              𝐴 = ¬(𝑝 ∨ 𝑞), 𝐵 = ¬𝑝 ∧ ¬𝑞
                          pr_deM_or2              𝐴 = ¬𝑝 ∧ ¬𝑞, 𝐵 = ¬(𝑝 ∨ 𝑞)
     Commutation          pr_com_or               𝐴 = 𝑝 ∨ 𝑞, 𝐵 = 𝑞 ∨ 𝑝
     (Com.)
                          pr_com_and              𝐴 = 𝑝 ∧ 𝑞, 𝐵 = 𝑞 ∧ 𝑝
     Association (As-     pr_assoc_or1            𝐴 = 𝑝 ∨ (𝑞 ∨ 𝑟 ), 𝐵 = (𝑝 ∨ 𝑞) ∨ 𝑟
     soc.)
                          pr_assoc_or2            𝐴 = (𝑝 ∨ 𝑞) ∨ 𝑟 , 𝐵 = 𝑝 ∨ (𝑞 ∨ 𝑟 )
                          pr_assoc_and1           𝐴 = 𝑝 ∧ (𝑞 ∧ 𝑟 ), 𝐵 = (𝑝 ∧ 𝑞) ∧ 𝑟
                          pr_assoc_and2           𝐴 = (𝑝 ∧ 𝑞) ∧ 𝑟 , 𝐵 = 𝑝 ∧ (𝑞 ∧ 𝑟 )
     Distribution (Dist.) pr_dist1a               𝐴 = 𝑝 ∧ (𝑞 ∨ 𝑟 ), 𝐵 = (𝑝 ∧ 𝑞) ∨ (𝑝 ∧ 𝑟 )
                          pr_dist1b               𝐴 = (𝑝 ∧ 𝑞) ∨ (𝑝 ∧ 𝑟 ), 𝐵 = 𝑝 ∧ (𝑞 ∨ 𝑟 )
                          pr_dist2a               𝐴 = 𝑝 ∨ (𝑞 ∧ 𝑟 ), 𝐵 = (𝑝 ∨ 𝑞) ∧ (𝑝 ∨ 𝑟 )
                          pr_dist2b               𝐴 = (𝑝 ∨ 𝑞) ∧ (𝑝 ∨ 𝑟 ), 𝐵 = 𝑝 ∨ (𝑞 ∧ 𝑟 )
     Double Negation pr_dneg1                     wfprop𝑝 =⇒ 𝑃 CJΓ ⊢ [𝑖 ↦→ ¬¬𝑝 ] 𝑓 K =⇒ wft𝑓 =⇒ 𝑃 DJΓ ⊢
     (D.N.)                                       [𝑖 ↦→ 𝑝 ] 𝑓 K
                          pr_dneg2                wfprop𝑝 =⇒ 𝑃 CJΓ ⊢ [𝑖 ↦→ 𝑝 ] 𝑓 K =⇒ wft𝑓 =⇒ 𝑃 DJΓ ⊢
                                                  [𝑖 ↦→ ¬¬𝑝 ] 𝑓 K
     Transposition        pr_trans1               𝐴 = 𝑝 → 𝑞, 𝐵 = ¬𝑞 → ¬𝑝
     (Trans.)
                          pr_trans2               𝐴 = ¬𝑞 → ¬𝑝, 𝐵 = 𝑝 → 𝑞
     Material Implica- pr_mimp1                   𝐴 = 𝑝 → 𝑞, 𝐵 = ¬𝑝 ∨ 𝑞
     tion (Impl.)
                          pr_mimp2                𝐴 = ¬𝑝 ∨ 𝑞, 𝐵 = 𝑝 → 𝑞
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                    31


   Material Equiva-   pr_meq1a               𝐴 = 𝑝 ↔ 𝑞, 𝐵 = (𝑝 → 𝑞) ∧ (𝑞 → 𝑝 )
   lence (Equiv.)
                      pr_meq1b               𝐴 = (𝑝 → 𝑞) ∧ (𝑞 → 𝑝 ), 𝐵 = 𝑝 ↔ 𝑞
                      pr_meq2a               𝐴 = 𝑝 ↔ 𝑞, 𝐵 = (𝑝 ∧ 𝑞) ∨ (¬𝑝 ∧ ¬𝑞)
                      pr_meq2b               𝐴 = (𝑝 ∧ 𝑞) ∨ (¬𝑝 ∧ ¬𝑞), 𝐵 = 𝑝 ↔ 𝑞
   Exportation (Exp.) pr_exp1                𝐴 = (𝑝 ∧ 𝑞) → 𝑟 , 𝐵 = 𝑝 → (𝑞 → 𝑟 )
                      pr_exp2                𝐴 = 𝑝 → (𝑞 → 𝑟 ), 𝐵 = (𝑝 ∧ 𝑞) → 𝑟
   Tautology (Taut.) pr_taut_or1             𝑃 CJΓ ⊢ [𝑖 ↦→ 𝑝 ] 𝑓 K =⇒ wft𝑓 =⇒ wfprop𝑝 =⇒ 𝑃 DJΓ ⊢
                                             [𝑖 ↦→ 𝑝 ∨ 𝑝 ] 𝑓 K
                      pr_taut_or2            𝑃 CJΓ ⊢ [𝑖 ↦→ 𝑝 ∨ 𝑝 ] 𝑓 K =⇒ wft𝑓 =⇒ wfprop𝑝 =⇒ 𝑃 DJΓ ⊢
                                             [𝑖 ↦→ 𝑝 ] 𝑓 K
                      pr_taut_and1           𝑃 CJΓ ⊢ [𝑖 ↦→ 𝑝 ] 𝑓 K =⇒ wft𝑓 =⇒ wfprop𝑝 =⇒ 𝑃 DJΓ ⊢
                                             [𝑖 ↦→ 𝑝 ∧ 𝑝 ] 𝑓 K
                      pr_taut_and2           𝑃 CJΓ ⊢ [𝑖 ↦→ 𝑝 ∧ 𝑝 ] 𝑓 K =⇒ wft𝑓 =⇒ wfprop𝑝 =⇒ 𝑃 DJΓ ⊢
                                             [𝑖 ↦→ 𝑝 ] 𝑓 K

A.3   Truth preservation and consistency proofs
A standard technique in metamathematics [43] and particularly model theory [11, 51], in a semantic
modeling tradition launched by Tarski [72], is to prove a set of logical inference rules truth-preserving
with respect to a particular semantic model of the formal system in question. If a proof in the target
logic consists solely of truth-preserving steps or judgments, then we can deduce that the proof can
only lead to a conclusion that is true under the semantic model – assuming, of course, that the
metalogic in which we define and analyze this model is itself both powerful enough and trustworthy
(e.g., hopefully at least consistent). By proving that the inference rules lead only to proofs of true
statements, we can infer that the inference rules cannot lead to proofs of false statements, thereby
proving the target logic’s consistency – at least relative to the consistency of our metalogic.
   Standard metalogical practice is to prove a logic’s truth preservation with respect to a model
constructed via classical mathematical tools such as sets and relations. Our development of BGA
diverges from this standard practice, however, by using a computational model – namely BGA’s
operational semantics – to prove that BGA’s inference rules preserve truth in this computational
model. Since BGA’s operational semantics above encodes the true constant T as the natural number
1, we are effectively proving that BGA’s inference rules safely navigate between formulas that, under
suitable conditions to be defined more precisely below, denote computations that always terminate
and reduce to the value 1.
   Because BGA terms in our model do not reduce directly to the mathematical primitives of our HOL
metalogic, but rather to a more-complex operational-semantic relation defined within our metalogic,
our machine-development uses Isabelle locales to avoid fixing a single model, but instead to identify
key properties of a semantic model that are needed to carry out desired model-theoretic lines of
reasoning. The model locale, for example, embodies the basic assumptions we assume any semantic
model has:
locale model =
   fixes val :: "asn ⇒ trm ⇒ any"
   assumes val_var: "val A (vi) = A i"
      and free_vars_val_eq: "asn_equiv A A’ t =⇒ val A t = val A’ t"

   This locale establishes background assumptions that: (a) there is some HOL function val that
determines the semantic value of any term under an assignment 𝐴; (b) the semantic value of a
reference to variable 𝑖 is simply the semantic value that assignment 𝐴 assigns to variable 𝑖; and (c)
the semantic value that val assigns to any term 𝑡 depends on assignment 𝐴 only for variables that
are free in 𝑡: specifically, if assignments 𝐴 and 𝐴′ agree for all variables free in term 𝑡 (asn_equiv),
then 𝐴 and 𝐴′ yield identical semantic values for 𝑡.
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
32                                                                                      and Ananthajit Srikanth

A.3.1 Paracomplete truth and satisfaction of terms and judgments. A classical model simply
assigns one of two values (e.g., T or F) to every well-formed formula in the modeled system. This
standard approach does not work for GA, however, because GA is paracomplete, hence must avoid
assuming that every well-formed formula has a truth value. Our model_true locale, therefore, em-
bodies more minimalistic assumptions about “truth” that avoid classical assumptions but nonetheless
suffice for paracomplete semantic modeling and truth preservation proofs as described below:
locale model_true = model + premodel_vtrue
begin

     satisfaction of hypotheses, conclusions, and judgments
    This model in essence simply assumes there is a HOL predicate vtrue that determines whether any
 given semantic value is a “true” value. There may even be multiple semantic values that are considered
“true”, although in BGA there is only one. More importantly, this locale defines paracomplete notions
 of satisfaction and truth, as summarized briefly below, and more formally in Isabelle/HOL syntax in
 Section A.13.1.
    In Hilbert-style natural-deduction systems of the type we defined for BGA in Table 2c, an
 inference rule consists of zero or more premises and a single conclusion. Premises and conclusions
 are judgments or entailments of the form ‘Γ ⊢ 𝑐’ (or “Γ entails 𝑐”), where Γ is a list of antecedents or
 hypotheses and 𝑐 is the consequent. Intuitively, a judgment expresses a metalogical claim that under
whatever conditions make every hypothesis in Γ true, the consequent 𝑐 is likewise true under the
 same conditions.
    An assignment 𝐴 satisfies BGA term 𝑡 under definition list 𝐷 if 𝑡 reduces to 1 (‘𝑡 ⇓ 1’) under 𝐴
 and 𝐷 via the operational semantics above (HOL predicate tsat in Section A.13.1). A judgment
‘Γ ⊢ 𝑐’ is true under definitions 𝐷 if every assignment 𝐴 that satisfies all hypotheses in Γ under 𝐷
(HOL predicate hsat) also satisfies conclusion 𝑐 under 𝐷. An inference rule is truth preserving for
 BGA if, for any definitions 𝐷 and any instance of the rule whose premises are true judgments, the
 instantiated rule’s conclusion is likewise a true judgment (HOL predicate jt). A proof, consisting of
 a list of judgments, is truth preserving if every judgment is truth preserving (pt).
    Entailment and truth preservation are non-computable notions with respect to the (computable)
 BGA target logic, but this is not a problem since the entailment or turnstile ‘⊢’ is a metalogical, not
 target-logic, construct. Since GA’s material implication operator (‘→’) is not primitive in BGA but
 is instead a computation defined on top of BGA, the distinction between material implication and
 metalogical entailment is pragmatically more crucial in GA than in classical or intuitionistic logic.
Whereas the classical inference rules for implication allow free interchange between the judgments
‘𝑎 ⊢ 𝑏’ and ‘⊢ 𝑎 → 𝑏’, for example, this is not true of GA due to the habeas quid precondition for
 implication introduction (Section 3.1.3).
A.3.2 Truth preservation proofs and consistency of BGA. We leave detailed truth-preservation
proofs to the machine-checked Isabelle/HOL development (Section A.14), and only briefly sketch a
few illustrative examples here.
   Because the only logical operators in our minimized BGA formulation are equals (=) and unequals
(≠) comparisons, the key truth-preservation proofs for BGA depend on three locales embodying
model assumptions about the comparability of natural numbers and their equality and unequality, as
follows:
locale model_cmp = model +
   fixes vcmp :: "any ⇒ bool"           %
locale model_eq = model_bool + model_cmp + trm_eq +
   assumes tbool_eq: "tbool A (ta = tb) ←→ vcmp (val A ta) ∧ vcmp (val A tb)"
      and   tsat_eq: "tbool A (ta = tb) =⇒ tsat A (ta = tb) ←→ val A ta = val A tb"
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                 33


locale model_ne = model_eq + trm_ne +
   assumes tbool_ne: "tbool A (ta ≠ tb) ←→ tbool A (ta = tb)"
      and   tsat_ne: "tbool A (ta ≠ tb) =⇒ tsat A (ta ≠ tb) ←→ ¬tsat A (ta = tb)"

  Corresponding strict models ensure that equality comparisons yield boolean values only (and
exactly) when the arguments are comparable.

   The model_cmp assumes there is a HOL function vcmp that identifies comparable semantic
values on which equals and unequals tests yield a result: in BGA, any natural number is comparable
(but ⊥ is not). The model_eq locale adds the grounded equality assumptions that an equals test
yields a boolean result exactly when both its arguments are comparable, and that when this is the
case, target-logic equality is equivalent to metalogical equality. The model_ne locale, finally, builds
on model_eq by assuming further that the unequals operator ‘≠’ yields a boolean result under the
same conditions, and that when its operators are comparable, assignment 𝐴 satisfies ‘𝑎 ≠ 𝑏’ precisely
when it 𝐴 does not satisfy ‘𝑎 = 𝑏’. Notice that since the only use of negation in these definitions is
metalogical, this formulation works even when the target logic lacks primitive negation, as in the
current minimized formulation of BGA.
   Building on these model-assumption locales, our proof derivation locales complete the formal
proofs that various grounded proof rules are truth preserving. The prf_gd_model_eq locale, for
example, builds on the above model_eq assumptions plus a basic assumption that the model “behaves
well” under multi-variable substitution (model_subm, see Section A.13.1):
locale prf_gd_model_eq = model_eq + model_subm
begin

  Symmetry of equality preserves truth.

  Building on the right set of assumptions, the truth preservation proofs necessary to prove the
consistency of particular inference rules are generally straightforward and unsurprising. We show
here one of the simplest such truth-preservation proofs, for equality symmetry, as an illustrative
example:
lemma jt_eq_sym [intro]: "pt P =⇒ P C [[Γ ⊢ a = b]] =⇒ jt Γ (b = a)"
  In brief, to introduce the truth of the conclusion judgment ‘Γ ⊢ 𝑏 = 𝑎’, we use the introduction rule
jtI to obtain an arbitrary-but-fixed assignment 𝐴, which we may assume satisfies every hypothesis
in Γ (‘hsat 𝐴 Γ ’). But because all prior judgments in proof 𝑃 are already truth preserving (the first
lemma’s first premise pt P) and that proof contains the judgment ‘Γ ⊢ 𝑎 = 𝑏’ (second premise),
assignment 𝐴 must already satisfy ‘𝑎 = 𝑏’. But then by the model_eq assumptions above, this
satisfaction translates to the HOL metalogical equality ‘val A ta = val A tb’, hence ‘val A
tb = val A ta’ by symmetry of metalogical equality, and hence back to 𝐴 satisfying ‘𝑏 = 𝑎’, the
desired conclusion.
   Our formulation of BGA finally “wraps up” this truth-preservation reasoning by instantiating a set
of proof-derivation locales such as prf_gd_model_eq above into the bga locale defining the BGA
system with its current, fixed set of 14 proof derivation rules in the generic syntax:
sublocale prf_gd_model_eq val vtrue vfalse vcmp trmEq
   Once this and various other proof-derivation locales are instantiated, we wrap up the semantic
consistency proof for BGA as a whole – showing that any formula that is provably true is also seman-
tically true in the computational model – by instantiating in BGA the model_preserves_truth
locale:
sublocale pt: model_preserves_truth val vtrue derives
  This locale’s central theorem, entails_consistent, defines semantic consistency as follows:
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
34                                                                                      and Ananthajit Srikanth

locale model_preserves_truth = model_true_derives +
   assumes derives_preserves_truth: "pvt P =⇒ P D [[H ⊢ c]] =⇒ jt H c"

     a model that identifies certain values as false values

lemma entails_consistent: "∅ ⊢ c =⇒ tsat A c"
   That is, for any conclusion 𝑐 provable unconditionally without hypotheses using BGA’s proof
rules, any assignment 𝐴 satisfies 𝑐 in BGA’s semantic model. Because BGA’s operational semantics
is single-valued, in turn (Section 4.3.1), it follows trivially by contradiction that BGA is also
syntactically consistent: that is, there can be no BGA terms 𝑎 and 𝑏 such that both ‘𝑎 = 𝑏’ and ‘𝑎 ≠ 𝑏’
are unconditionally provable.
A.3.3 Truth preservation proofs for grounded propositional operators. Although our mini-
mized formulation of BGA only actually needs truth-preservation proofs for a small set of inference
rules concerning equality and natural numbers, our formal development also includes locale-based
truth-preservation proofs for grounded propositional operators that were primitive in an earlier
version of BGA before this minimization (and which should be reusable in future less-minimal
formalizations). We briefly summarize a few of these to provide an intuitive feel for how the grounded
propositional operators “work” and their similarities and differences from classical and intuitionistic
logic, even though these truth-preservation proof locales are not needed or instantiated in the current
minimized formulation of BGA.
   To prove the bidirectional inference rule ¬¬IE in Table 2c truth preserving, for example, we must
show that under any assignment 𝐴 satisfying all hypotheses Γ under definitions 𝐷, if term 𝑝 evaluates
to 1 then so does ‘¬¬𝑝’, and vice versa. In the forward direction, we simply apply two additional
reduction steps to bring the assumed evaluation ‘𝑝 ⇓ 1’ to ‘¬¬𝑝 ⇓ 1’. In the reverse direction, we
need lemmas proving that the only way we get to ‘¬𝑝 ⇓ 1’ is from ‘𝑝 ⇓ 0’, and similarly for ‘¬𝑝 ⇓ 0’
from ‘𝑝 ⇓ 1’. We prove both of these lemmas by case analysis on the available reductions.
   To prove BGA’s negation-elimination or non-contradiction rule ¬E truth preserving, we must
show that any assignment 𝐴 that satisfies all hypotheses in Γ and makes both ‘𝑝’ and ‘¬𝑝’ reduce to
1, 𝐴 also satisfies the arbitrary conclusion 𝑞. But for ‘¬𝑝’ to reduce to 1, 𝑝 would have to reduce to 0
as well as to 1. Because BGA’s operational semantics is single-valued, this is impossible. We thus
trivially satisfy the rule’s conclusion, by applying the law of non-contradiction metalogically.
   As a negative example of a rule we cannot prove truth preserving with respect to BGA’s operational
semantics, because it isn’t, consider the classical implication-introduction rule →I , without BGA’s
habeas quid precondition ‘𝑝 B’ (Section 3.1.3). We wish to prove that any assignment 𝐴 satisfying all
hypotheses in Γ reduces the BGA term ‘𝑝 → 𝑞’ to 1, but this is just shorthand for ‘¬𝑝 ∨ 𝑞’ (Table 3b).
If 𝑝 reduces to 0 or 𝑞 reduces to 1 then the conclusion is trivially satisfied. If 𝑝 reduces to 1 then
we can use the rule’s classical premise ‘Γ, 𝑝 ⊢ 𝑞’ to infer that 𝑞 likewise reduces to 1. But 𝑝 is an
arbitrary computation, which might reduce to a non-boolean natural number, or might never reduce
at all and thus denote ⊥. We are thus stuck and unable to prove truth preservation for this case, as we
should be.
   To prove BGA’s mathematical induction rule Ind truth preserving, we must show that for any
assignment 𝐴 satisfying the hypotheses in Γ, in which the induction variable 𝑥 is not free, the rule’s
conclusion is true whenever its three premises are true. By the rule’s third habeas quid premise
‘Γ ⊢ 𝑎 N’, we infer that the arbitrary BGA term 𝑎 reduces to some arbitrary but fixed natural number
𝑛. We prove metalogically by induction on 𝑛 that 𝐴 satisfies the rule’s conclusion ‘Γ ⊢ 𝑝 ⟨𝑎, . . .⟩’. The
base case of 𝑛 = 0 is directly satisfied by the rule’s first premise ‘Γ ⊢ 𝑝 ⟨0, . . .⟩’, For the metalogical
inductive step, we can assume the rule’s conclusion is satisfied when we substitute the numeral for 𝑛
for the induction variable 𝑥, and must prove that it is also satisfied when we substitute the numeral
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                     35


for 𝑛 + 1 for 𝑥. The inductive step’s starting assumptions enable us to prove that 𝐴 satisfies the
second premise’s additional hypotheses ‘𝑥 N’ and ‘𝑝 ⟨𝑥, . . .⟩’ under these substitutions, so the second
premise is applicable, allowing us to infer that 𝐴 likewise satisfies ‘𝑝 ⟨S(𝑥), . . .⟩’, thereby completing
the induction step. The induction inference rule is therefore truth preserving.

A.4   HOL proof of semantic completeness
While semantic consistency states that anything provable is true, semantic completeness essentially
states the converse: that anything semantically true is also provable using the available deduction
rules. Our formalization of BGA expresses this property in terms of a model_complete locale,
which we instantiate in BGA:
locale model_complete = well_formed_formula + entails + model_true +
   In essence, for any well-formed formula 𝑐 of BGA (‘wff c’) that is semantically satisfied under
all assignments 𝐴 (i.e., semantically true), there is an unconditional proof of 𝑐 using the available
proof rules.
   In BGA, the deduction rules available are those defined in the derives predicate above (Sec-
tion A.14). In our completeness proofs, however, we found it convenient to produce BGA proofs using
the even-more-minimal unconditional provability rule set pui, which uses the closed HOL datatype
syntax for BGA. From the pui rule set there is a straightforward translation into the derives rule
set (again see Section A.14). This indirection is probably neither necessary nor particularly important;
we merely found it convenient.
   While there is nothing particularly difficult about the completeness proof, it does depend along the
way on the following important lemma:
lemma os_istm_pui: "os A s t r =⇒ istm t
                      =⇒ ∃ l. pui l (fmEq (tm_of_trm (asn_subm A ⇂ t)) (tmNum r))"
   This lemma states in essence that whenever there is an operational-semantic reduction under
assignment 𝐴 in 𝑠 steps, of well-formed term 𝑡 to result 𝑟 , there exists an unconditional proof of some
length 𝑙 of the formula ‘𝑡 ′ = 𝑟 ’, where 𝑡 ′ is merely 𝑡 after substituting numerals from assignment
𝐴 into all free variables (that is, multi-variable substitution using asn_subm A), and 𝑟 is simply
the numeral of the result 𝑟 . In other words, although we are ultimately concerned only with BGA
formulas that reduce to one particular semantic value – the one denoting “true” – to get there we
need the intermediate property that for every BGA term 𝑡 that reduces to any natural number, there is
a BGA proof that 𝑡 indeed equals exactly that natural number.
   From this lemma we then get the corresponding completeness lemma concerning BGA formulas:
lemma os_isfm_pui: "os A s t {|True|} =⇒ isfm t =⇒ ∃ l. pui l (fm_of_trm (asn_subm A ⇂
t))"
   That is, whenever any well-formed formula 𝑡 (‘isfm t’) reduces to the Gödel encoding of True
(1) under assignment 𝐴 in 𝑠 steps, there is an unconditional proof of 𝑡 after applying the appropriate
substitutions from assignment 𝐴. From this lemma we use the translation from the pui to the
derives proof rules to obtain the corresponding completeness property in the generic syntax, as
follows, which in turn satisfies the assumptions embodied in the model_complete locale above:
lemma os_isfm_entails:
   assumes os: "os A s t {|True|} " and t: "isfm t"
   shows "∅ ⊢ (asn_subm A ⇂ t)"

A.5   HOL proofs of recursive function representation
Like our consistency and completeness proofs, the expressiveness proofs in our development of BGA
are split into generic and BGA-specific reasoning components: the former using Isabelle locales to
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
36                                                                                      and Ananthajit Srikanth

prove key theorems based on particular assumptions about otherwise-arbitrary formal systems, the
latter instantiating these locales into BGA in particular.
A.5.1 Locale-based representation of primitive- and general-recursive functions. The con-
sistency and completeness proofs summarized above assume an arbitrary-but-fixed list of recursive
definitions 𝐷, in order to define proof rules and semantics of function application, but this reasoning
was essentially oblivious to the issue of which particular definitions 𝐷 might actually contain. It is at
the present point that we start to care about this question. A BGA instance with an empty definition
list 𝐷, for example, is perfectly allowed but not particularly useful or powerful.
   Our reasoning about representation of recursive functions in GA relies on a set of HOL predicates
that essentially recognize when specific structures of interest appear in the background definition list
𝐷 assumed by the trm_dfns locale (Section A.14.2). For example, the following HOL predicate
determines if some definition 𝑑 structurally expresses one of the four standard initial functions
from which 2-argument primitive-recursive functions are composed – namely zero, successor, left
projection, and right projection:
fun rif_rep :: "dfn ⇒ rifidx ⇒ bool" where
     "rif_rep d (rInit0) = dfn_is d 2 (0)"
   | "rif_rep d (rInitS) = dfn_is d 2 (S (v0))"
   | "rif_rep d (rInitL) = dfn_is d 2 (v0)"
   | "rif_rep d (rInitR) = dfn_is d 2 (v1)"

     GA representation of primitive-recursive function indices as an inductive predicate

  Building on definitions representing these initial functions, the inductive predicate pri_rep
determines if some definition 𝑑 structurally represents a particular primitive-recursive function:
inductive pri_rep :: "dfn ⇒ pridx ⇒ bool" where
     "pri_rep d (prInit i)" if "rif_rep d i"
   | "pri_rep d (prSub g h1 h2)" if "dfn_is d 2 (comp_def_sub dg dh1 dh2)" and
                        "pri_rep dg g" and "pri_rep dh1 h1" and "pri_rep dh2 h2"
   | "pri_rep d (prRec g h h’)" if "dfn_is d 2 (comp_def_rec d dg dh dh’)" and
                        "pri_rep dg g" and "pri_rep dh h" and "pri_rep dh’ h’"

   Definition df represents a general-recursive step function built on an underlying primitive-recursive
step function with definition dg.

   This inductive predicate in effect recognizes when a set of recursive definitions culminating in
definition 𝑑 has a particular standard structure exactly representing a particular primitive-recursive
function, according to standard recursion theory and its formalization in our framework. In particular,
any 2-argument primitive-recursive function is either (a) one of the above four initial functions, (b) a
composition of three existing primitive-recursive functions 𝑔, ℎ 1, ℎ 2 via substitution (comp_def_sub,
see Section A.14.2 for details), or (c) a composition of three existing primitive-recursive functions
𝑔, ℎ, ℎ ′ via primitive recursion (comp_def_rec). The inductive structure of this predicate effectively
“checks” that all the dependencies of 𝑑 are also present with exactly the correct structure within the
list of definitions 𝐷.
   General-recursive functions. A basic theorem of recursion theory, included in our development,
is that any single-argument general-recursive function 𝑓 (𝑥) is expressible via some 2-argument
primitive-recursive step function 𝑓𝑠 (𝑥, 𝑦) taking fixed argument 𝑥 and a step count 𝑦, simulating
𝑓 ’s computation for up to 𝑦 steps, and returning 1 + 𝑟 if 𝑓 (𝑥) terminates with result 𝑟 within
this computational quota, and returning 0 otherwise. If 𝑓𝑠 (𝑥, 𝑦) returns 0 for some 𝑦 indicating no
termination yet, it might be that 𝑓 eventually terminates for some larger 𝑦 ′ > 𝑦, or it might be that 𝑓
never terminates.
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                    37


   Building on this principle, the following HOL predicate determines if some definition d represents
a particular general-recursive function having exactly this structure, building on an underlying
primitive-recursive step function represented exactly by another definition dg:
inductive gri_rep :: "dfn ⇒ pridx ⇒ bool" where
     "gri_rep d g" if "dfn_is d 2 (comp_def_sf d dg)" and "pri_rep dg g"
   The helper comp_def_sf used in this definition yields a definition body of a general-recursive
function 𝑓 (𝑥, 𝑦) that simply performs an unbounded search upward starting from 𝑦 for the first 𝑦 ′ ≥ 𝑦
for which 𝑓𝑠 (𝑥, 𝑦) ≠ 0, if any such 𝑦 ′ exists:
definition comp_def_sf :: "dfn ⇒ dfn ⇒ trm" where
   "comp_def_sf f g ≡ g[v0 , v1 ] 0? f[v0 , S v1 ] : P g[v0 , v1 ]"

  GA representation of the four standard 2-argument initial functions
   In this template, 𝑓 is the definition index of the general-recursive function being defined and 𝑔 is
the definition index of the underlying primitive-recursive step function 𝑓𝑠 .
   Given a suitable choice of definition list 𝐷, therefore, we can structurally represent not only
any primitive-recursive function but also any general-recursive function, as proven in subsequent
theorems below.
A.5.2 Representation of primitive- and general-recursive functions in BGA. Our concrete
formulation of BGA includes and uses BGA-specific HOL predicates equivalent to those above but
using the closed BGA datatypes in place of the generic syntax. Building on these predicates, we
define a tmrep_std assumption over the first 2𝑛 definitions in a definition list, for a given 𝑛. For
each pair of contiguous indices at index (2𝑖, 2𝑖 + 1) for i a nat, we have that the first index represents
a primitive-recursive function, while the second index represents the corresponding general-recursive
function constructed from using the primitive-recursive function as an underlying step function.
definition tmrep_std :: "nat ⇒ bool" where
   "tmrep_std n ≡ 2*n ≤ length tm_dfns ∧
                    (∀ i < n. tm_dfns ! (2*i) = tm_dfn_std_prn i ∧
                              tm_dfns ! (2*i+1) = tm_dfn_std_grn i)"
  A key step we must then perform outside of any BGA instance or locale is proving that there exists
some definition list 𝐷 of any desired length 2𝑛 satisfying the tmrep_std predicate:
lemma tmrep_std_ex: "∃ D. length D = 2*n ∧ bga.tmrep_std D n"
  We can thus construct a definition list representing any finite set of contiguous primitive and
general-recursive function pairs by defining a sufficiently-long 𝐷 with this property.
A.5.3 A universal instance of BGA. Given the above foundations, we now construct a universal
instance of BGA: a single instance with one particular definition list 𝐷 that is capable of simulating
any general-recursive function. This step builds on another key component of our development
of recursion theory: a primitive-recursive step function representing a metacircular evaluator for
arbitrary primitive-recursive functions. The evaluation of arbitrary primitive-recursive functions
is beyond the capabilities of any particular primitive-recursive function, as shown by a standard
diagonal argument. Nevertheless, the step function underlying such a metacircular evaluator can be
primitive recursive.
   Using this metacircular evaluator we build a step function sfApp with index sfiApp representing
a general-recursive function taking a Cantor pair ⟨𝑓𝑠 , 𝑥⟩, where 𝑓𝑠 is the Gödel code of a primitive-
recursive step function and 𝑥 is a natural-number argument. The sfApp step function uses the
metacircular evaluator to simulate the general-recursive computation that 𝑓𝑠 represents, finding the
least 𝑦 for which 𝑓𝑠 (𝑥, 𝑦) ≠ 0 if such exists, and otherwise never terminating. In effect, sfApp
thus implements universal general-recursive function application. While this summary hides a great
           Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
38                                                                                     and Ananthajit Srikanth

deal of nontrivial and tedious formal reasoning, this is in principle “just recursion theory” and not
conceptually new.
   By constructing a definition list 𝐷 sufficient to express this universal function evaluator, we obtain
the bga_universal locale defining a particular instance of BGA provably capable of representing
all general-recursive functions. The following definition and theorem illustrates the result:
definition recf_rep :: "(nat ⇒ nat) ⇒ tc1 ⇒ bool" where
   "recf_rep f c ≡ recf f ∧ istc1 c ∧ (∀ x. ∅ ⊢ c (nx) = n(f x))"

  General-recursive unary function f is represented by term constructor c. The unary primitive-
recursive companion of recf_rep is pr1_rep, completing the representation grid alongside the
binary pr2_rep. Unary primitive recursion is expressed as n2pr (𝜆x y. f x ), and lifts to recf via
n2pr (𝜆x y. ?f x) =⇒ recf ?f (see the pr1_rep_recf_rep bridge), so every recf_rep
use can still exist as they are.

lemma recf_rep_ex: assumes rf: "recf f" shows "∃ c. recf_rep f c"
   The recf_rep predicate indicates that HOL function 𝑓 is a general-recursive total function (recf
f), and that there is a term constructor 𝑐 that represents 𝑓 , by virtue of the equality ‘𝑐 (𝑥) = 𝑓 (𝑥)’ being
provable for all values of argument 𝑥. The recf_rep_ex theorem shows that for any total general-
recursive function 𝑓 , there is such a term constructor 𝑐 representing it within the bga_universal
instance of BGA.
   The universality of bga_universal is not limited to total general-recursive functions: it repre-
sents all partial general-recursive functions as well. This latter property is not as cleanly expressible
in HOL as it is for total functions, however, because all functions in the underlying HOL metalogic
are total, not partial.
   Given that BGA allows arbitrary recursive definitions in its list 𝐷, it should be no surprise that such
definitions can express arbitrary primitive-recursive and general-recursive functions. What might be
more interesting and surprising is that despite its minimality, BGA’s proof system is also capable
of proving the correct result of any Turing-complete, general-recursive function evaluation on any
particular argument 𝑥. BGA’s consistency property guarantees that it cannot prove such equalities
for any wrong result values. Completeness allows us to move freely back and forth between BGA’s
syntactic proof system and its operational-semantic model, working in whichever domain is most
convenient in any given situation.
   Finally, it seems clear that Gödel’s incompleteness theorems cannot apply to, or be provable
about, BGA as target logic. Such a successful adaptation of Gödel’s proofs would directly contradict
the above metalogical results and imply that HOL, and hence ZFC, are inconsistent. Thus, unlike
intuitionistic logic, it appears that BGA evades the usual interpretation of Gödel’s theorems as stating
that “no formal system” can be complete, consistent, and powerful enough to express arithmetic
and computation. Instead it appears such a consistent, complete, and powerful formal system must
merely be sufficiently non-classical.

A.6    HOL proofs of Gödel-style arithmetization and reflection in BGA
Consistent with standard practice since Gödel, the most straightforward way to accomplish such
arithmetization is first to define the relevant syntax- and proof-manipulation functions in the working
metalogic (HOL in our case), use the metalogic to prove those functions primitive-recursive or
general-recursive, then use representability theorems like those above to show that these functions,
like any computation, “transfer” into formulas expressible in the target system (i.e., BGA).
   The first step in arithmetization is to define a Gödel coding for syntax, which our Isabelle/HOL
development accomplishes by making the trm type, representing generic abstract syntax, an instance
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                 39


of the coding class representing Gödel-encodable HOL types having an injection into the natural
numbers:
instantiation trm :: coding
   Using other generic instantiations of the coding class, finite sets of hypotheses likewise become
Gödel-encodable, as do judgments of the form ‘Γ ⊢ 𝑐’, and BGA proofs, which are finite lists of
judgments.
   By far the most long and tedious part of the arithmetization process then amounts to proving a
large number of HOL functions and predicates to be primitive-recursive: in particular, functions to
manipulate finite data structures such as tuples and lists, functions to manipulate the generic syntax,
functions to test whether a natural number encodes a trm in that syntax, functions to test whether
such a trm represents a well-formed term or formula in BGA syntax, and functions to test whether a
list of judgments constitutes a valid proof according to its derives rule set (Section 4.2). Proving
each of BGA’s proof rules in particular represents the bulk of this tedium, despite yielding only
theorems that (today) will surprise no one. This formalization effort culminates in a proof that BGA
instantiates the prf_derives_primrec locale:
locale prf_derives_primrec = prf_derives +
   assumes n2pr_derivesI [intro!]:
              "n2pr (𝜆x y. {|P x y |} ) =⇒ n2pr (𝜆x y. {|H x y |} ) =⇒n2pr (𝜆x y. {|c x y |} )
               =⇒ n2pr (𝜆x y. {|P x y D [[H x y ⊢ c x y ]] |} )"
sublocale prf_derives_primrec derives
   The locale’s n2pr_derivesI states, informally, that if 𝑃, 𝐻 , and 𝑐 are 2-argument primitive-
recursive functions yielding a Gödel-encoded proof, hypothesis list, and conclusion, respectively,
then the derives predicate – determining whether a particular judgment appended to a valid proof
yields another valid proof – is likewise primitive recursive.
   While checking a proof is primitive recursive, the unbounded search for a proof is of course
general recursive. Since our formalization of general recursion relies heavily on their representation
by an underlying primitive-recursive step function, as described above in Section 4.6, we use the
following locale to express the property that there is some step function sfPf embodying the formal
system:
locale sfPf_sfde = well_formed_formula + refutes + sfPf_pr2 +
   assumes sfPf_sfde1: "consistent_ref Γ =⇒ sfde sfPf ⟨ {|Γ |} ,{|c|} ⟩ 1 ←→ entails Γ c"
      and   sfPf_sfde0: "consistent_ref Γ =⇒ sfde sfPf ⟨ {|Γ |} ,{|c|} ⟩ 0 ←→ refutes Γ c"
      and   sfde_sfPf_binary: "sfde sfPf x r =⇒ r ≤ 1"

   Stronger assumptions: provided only that the conclusion is well-formed, then function sfPf enu-
merates all results corresponding to entailment or refutation: even if the hypotheses are inconsistent,
in which case sfPf enumerates both 0 and 1. sfPf enumerates a True result if the hypotheses entail the
conclusion, sfPf enumerates a False result if the hypotheses refute the conclusion, sfPf enumerates
both True and False if the hypotheses are inconsistent; sfPf yields neither result if the hypotheses
neither entail nor refute the conclusion.

   The sfPf_sfde1 assumption states, in brief, that given any consistent set of hypotheses Γ and
well-formed formula 𝑐, the step function sfPf invoked with the pair ⟨⌜Γ⌝, ⌜𝑐⌝⟩ as its fixed (𝑥)
argument, with its step-count (𝑦) parameter allowed to increase without bound, eventually terminates
with value 1 if and only if ‘Γ ⊢ 𝑐’ is provable. The dual assumption sfPf_sfde0 states the same
thing only about (negative) refutation rather than (positive) entailment. We need this second dual
property only because we wish to avoid relying on logical negation as a primitive; it would not
be required in a formulation with primitive negation. The final assumption sfde_sfPf_binary
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
40                                                                                      and Ananthajit Srikanth

of course states simply that the sfPf step function only ever terminates with a binary result (if it
terminates at all). This locale thus embodies sfPf’s correctness criteria.
   To show that this sfPf step function is also representable as a BGA computation, we use this
locale:
locale sfPf_sfde_rep = well_formed_predicate + refutes + rec_fun_rep +
                         sfPf_sfde + sfPf_sfde_rep_tc1Pf + rep_cpair_subs + trm_nat_cons_istc
+
   assumes rep_sfde_sfPf: "rep_sfde sfPf tc1Pf"
      and   wft_tc1Pf: "wft1 tc1Pf"
begin

     Derive a term constructor representing unconditional provability.

  This locale’s first assumption states that there is a single-argument term constructor tc1Pf
representing a general-recursive computation with sfPf as its underlying primitive-recursive step
function.
  Finally, we instantiate the locales above into bga_universal, the universal instance of BGA:
sublocale sfPf_sfde_rep istm isfm entails refutes trm0 trmSuc trmEq sfPf tc1Pf tcCpair


   Instantiating this lemma centrally uses the tedious proof that BGA’s derives predicate and in
turn sfPf function are primitive recursive.

A.7     HOL development of the computable logic operators in BGA
A.7.1 Grounded logical negation. The obvious starting point is logical negation, whose underly-
ing step function we define as follows:
definition sfPu :: n2f where "sfPu x y ≡ sfPf ⟨ {| ∅::trm fset|} ,x ⟩ y"


definition sfPneg :: n2f where
   "sfPneg x y ≡ case sfPu x y of 0 ⇒ 0 | Suc r ⇒ Suc (1-r)"
   The sfPu step function is merely an unconditional version of sfPf above, which searches for
an unconditional proof of some conclusion. The sfPneg step function, in turn, simply inverts the
encoded boolean value of any result from sfPu, yielding the encoded negation of the argument’s truth
value (if any). Since sfPneg is primitive recursive, the general-recursive computation representing
grounded negation in BGA is expressible within the universal instance of BGA.
   Utilizing BGA’s consistency and the fact that sfPneg is a computation representable in BGA, we
then obtain a term constructor for computed negation and these correctness theorems about it:
definition trmNeg :: tc1 ("¬_" [140] 140) where "¬p ≡ tcPneg (n{|p|} ) = 1"
lemma entails_neg_refutes: shows "entails ∅ (¬p) ←→ refutes ∅ p"
lemma refutes_neg_entails: shows "refutes ∅ (¬p) ←→ entails ∅ p"
   That is, for any well-formed formula 𝑝, the negation of 𝑝 is true exactly when 𝑝 is false and vice
versa. If 𝑝 is a formula denoting no truth value – e.g., expressing a non-terminating computation such
as the Liar sentence – then neither does ‘¬𝑝’.
A.7.2 Grounded logical disjunction. Defining grounded logical disjunction as a computation in
BGA is slightly less trivial but follows the same principle:
definition sfPor1 :: n2f where
   "sfPor1 ≡ sfpar (sfonly (𝜆x. sfPu (cpx x)) 1) (sfonly (𝜆x. sfPu (cpy x)) 1)"
definition sfPor0 :: n2f where
   "sfPor0 ≡ sfonly2 (𝜆x. sfPu (cpx x)) 0 (𝜆x. sfPu (cpy x)) 0 0"
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                  41


definition sfPor :: n2f where
   "sfPor x y ≡ if wff (decode (cpx x)) ∧ wff (decode (cpy x))
                   then sfPorw x y else 0"
   These definitions use two step-function combinators from our development of recursion theory:
sfonly 𝑓𝑠 𝑣 terminates only yielding value 𝑣 if the underlying step function 𝑓𝑠 terminates with
value 𝑣, and otherwise never terminating; and sfpar 𝑓1 𝑓2 executes underlying step functions 𝑓1 and
𝑓2 as if in parallel, returning the result of whichever terminates “first” by the step count metric (and
favoring 𝑓1 in case of a tie).
   The step function sfPor1 above expresses a computation that terminates yielding 1 (true) if the
computations representing either of the disjuncts 𝑝 or 𝑞 terminate yielding 1. The step function
sfPor0 terminates with result 0 (false) only if both disjuncts 𝑝 and 𝑞 terminate yielding 0. The sfPor
step function combines these computations in parallel, so that the logical disjunction computation
may return either 1 or 0 (or neither) in the relevant cases.
   Upon proving that this disjunction computation is represented in BGA, we obtain the following
key correctness theorems for grounded disjunction:
definition trmOr :: tc2 (infixr "∨" 130) where "p ∨ q ≡ tcPor ⟨n{|p|} ,n{|q |} ⟩ = 1"
lemma tcPor_entails_iff:
   shows "entails ∅ (p ∨ q) ←→ wff p ∧ wff q ∧ (entails ∅ p ∨ entails ∅ q)"
lemma tcPor_refutes_iff:
   shows "refutes ∅ (p ∨ q) ←→ wff p ∧ wff q ∧ refutes ∅ p ∧ refutes ∅ q"
    That is, as expected in grounded deduction, ‘𝑝 ∨ 𝑞’ is true exactly when either 𝑝 or 𝑞 is true, and
‘𝑝 ∨ 𝑞’ is false exactly when both 𝑝 and 𝑞 are false.
    Since the remaining grounded propositional operators (conjunction, implication, and biconditional)
 are trivially definable in terms of negation and disjunction in the same way as for classical logic, we
 did not construct reflective computations for the other operators, although that could certainly be
 done.

A.8     Recursion theory development in HOL
A.8.1    Cantor pairings.
definition cpair :: "nat ⇒ nat ⇒ nat" where
   "cpair x y = ((x + y) * Suc (x + y)) div 2 + y"

  We next define convenient tuple syntax such that ⟨x,y⟩ represents cpair x y, and ⟨x,y,z⟩
represents ⟨x,⟨y,z⟩⟩ .

   Extraction (projection) of left and right elements of a Cantor pair.
lemma cpair_cpx_simp [simp]: "cpx ⟨x,y ⟩ = x"
lemma cpair_cpy_simp [simp]: "cpy ⟨x,y ⟩ = y"

   A Cantor pairing upper bounds both of its elements.
lemma cpx_le [simp]: "cpx z ≤ z"
lemma cpy_le [simp]: "cpy z ≤ z"

   Cantor pairing is monotonic in both arguments.
lemma cpair_x_le [simp]: "x ≤ ⟨x,y ⟩"
lemma cpair_y_le [simp]: "y ≤ ⟨x,y ⟩"
lemma cpair_x_mono: "x ≤ x’ =⇒ ⟨x,y ⟩ ≤ ⟨x’,y ⟩"
lemma cpair_y_mono: "y ≤ y’ =⇒ ⟨x,y ⟩ ≤ ⟨x,y’⟩"
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
42                                                                                      and Ananthajit Srikanth

A.8.2     Gödel encoding of HOL types.
type_synonym any = nat

     This class denotes any HOL type having a distinguished Gödel coding into the natural numbers.

     A type of class coding has an injection into the natural numbers.
class coding =
   fixes encode :: "’a ⇒ any" ("{|_|} ")
   assumes encode_inj: "inj encode"

     A type of class bicoding has a bijection with the natural numbers.
class bicoding = coding +
   assumes encode_surj: "surj encode"
lemma decode_encode: "decode {|x |} = x"

     Gödel coding of natural numbers, booleans, product types, options, lists, and finite sets.
instantiation nat :: bicoding%
instantiation bool :: coding
instantiation prod :: (coding,coding) coding
instantiation option :: (coding) coding
instantiation list :: (coding) coding
instantiation fset :: (coding) coding
begin

  To encode a finite set we form a set of the linearly-ordered codes of the elements and encode
a sorted list of these codes. There’s a sorted_list_of_fset function already, but not yet a
sorted_list_of_fset_inject rule to go with it.


A.9     Primitive and general recursion
inductive n2pr :: "n2f ⇒ bool" where
   n2prIni: "n2pr f" if "n2init f" |
   n2prSub: "n2pr f" if "f = n2comp_sub g h1 h2" and "n2pr g" and "n2pr h1" and "n2pr
h2" |
   n2prRec: "n2pr f" if "f = n2comp_rec g h h’" and "n2pr g" and "n2pr h" and "n2pr h’"

     inductive definition of 2-argument general-recursive total functions on natural numbers
inductive n2grt :: "n2f ⇒ bool" where
   n2grtIni: "n2grt f" if "n2init f" |
   n2grtSub: "n2grt f" if "f = n2comp_sub g h1 h2" and "n2grt g" and "n2grt h1" and "n2grt
h2" |
   n2prtRec: "n2grt f" if "f = n2comp_rec g h h’" and "n2grt g" and "n2grt h" and "n2grt
h’" |
   n2grtMu:    "n2grt f" if "f = n2comp_mu g" and "n2grt g" and "∀ x. ∃ y. g x y ≠ 0"

     an even-more-general formulation of partial, not just total, general recursion

     Primitive-recursive step functions defining general-recursive computations.
definition sfd :: "n2f ⇒ nat ⇒ step ⇒ nat ⇒ bool" where
   "sfd f x y r ≡ f x y = Suc r ∧ (∀ z<y. f x z = 0)"

     Step function f, when given input x, decides on result r eventually at some step count.
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic     43


definition sfde :: "n2f ⇒ nat ⇒ nat ⇒ bool" where
   "sfde f x r ≡ ∃ y. sfd f x y r"

  Step function f, given input x, never terminates.
definition sfonly :: "n2f ⇒ nat ⇒ n2f" where
   "sfonly f r x y ≡ if sflock f x y = Suc r then Suc r else 0"

  sfonly2 f g similarly returns r only if/when both f and g terminate with result r.
definition sfpar :: "n2f ⇒ n2f ⇒ n2f" where
   "sfpar f g ≡ sflock (𝜆x y. if f x y ≠ 0 then f x y else g x y)"

  sfonly f returns result r if/when f ever returns r, and otherwise never terminates.

A.10    Gödel-encodable 2-argument primitive-recursive function indices
  The four initial functions: zero, successor, left and right projection.
datatype rifidx =
  rInit0 |
  rInitS |
  rInitL |
  rInitR

  give the standard initial functions a Gödel coding.

  Function composition from initial functions, substitution, or primitive recursion.
datatype pridx =
  prInit rifidx |
  prSub pridx pridx pridx |
  prRec pridx pridx pridx

  a datatype indexing the general-recursive (partial) functions

  Form a HOL function from a primitive-recursive function index.
fun pr2fi :: "pridx ⇒ n2f" where
     "pr2fi (prInit ifc) = rif ifc"
   | "pr2fi (prSub g h1 h2) = n2comp_sub (pr2fi g) (pr2fi h1) (pr2fi h2)"
   | "pr2fi (prRec g h h’) = n2comp_rec (pr2fi g) (pr2fi h) (pr2fi h’)"

  Choose any pridx representing a given function f, if f is primitive recursive.

A.11    Metacircular evaluation
  Metacircular evaluation step function.
fun ev :: "pridx ⇒ any ⇒ any ⇒ etree ⇒ etree" where
     "ev f x y (Got r) = Got r"
   | "ev (prInit i) x y (Get E) = Got (rif i x y)"
   | "ev (prSub g h1 h2) x y (Get [Got r1, Got r2, Got r]) = Got r"
   | "ev (prSub g h1 h2) x y (Get [Got r1, Got r2, eg]) =
       Get [Got r1, Got r2, ev g r1 r2 eg]"
   | "ev (prSub g h1 h2) x y (Get [e1, e2, eg]) =
       Get [ev h1 x y e1, ev h2 x y e2, eg]"
   | "ev (prSub g h1 h2) x y (Get []) = Get [Get [], Get [], Get []]"
   | "ev (prRec g h h’) x (0) (Get [Got r]) = Got r"
   | "ev (prRec g h h’) x (0) (Get [eg]) = Get [ev g x 0 eg]"
   | "ev (prRec g h h’) x (0) (Get []) = Get [Get []]"
   | "ev (prRec g h h’) x (Suc y) (Get [Got r1, Got r2, Got r]) = Got r"
   | "ev (prRec g h h’) x (Suc y) (Get [Got r1, Got r2, eh]) =
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
44                                                                                      and Ananthajit Srikanth

         Get [Got r1, Got r2, ev h r1 r2 eh]"
     | "ev (prRec g h h’) x (Suc y) (Get [e1, e2, eh]) =
         Get [ev h’ x y e1, ev (prRec g h h’) x y e2, eh]"
     | "ev (prRec g h h’) x (Suc y) (Get []) = Get [Get [], Get [], Get []]"
     | "ev f x y e = undefined"

     iterate evaluation over s steps

     Metacircular iterated evaluation.
fun ei :: "pridx ⇒ any ⇒ any ⇒ step ⇒ etree" where
     "ei f x y (0) = Get []"
   | "ei f x y (Suc s) = ev f x y (ei f x y s)"

     Predicate: evaluation of (f,x,y ) has terminated by step s.

     Metacircular evaluation predicates.
definition et :: "pridx ⇒ any ⇒ any ⇒ step ⇒ bool" where
   "et f x y s ≡ ∃ r. ei f x y s = Got r"

     The result of evaluating (f,x,y ) provided it has terminated by step s.
definition er :: "pridx ⇒ any ⇒ any ⇒ step ⇒ any" where
   "er f x y s ≡ if et f x y s then SOME r. ei f x y s = Got r else undefined"

     evaluation of (f,x,y ) terminates exactly at step s with the correct result
definition ec :: "pridx ⇒ any ⇒ any ⇒ step ⇒ bool" where
   "ec f x y s ≡ ei f x y s = Got (pr2fi f x y) ∧ (∀ s’ < s. ¬ et f x y s’)"

     we don’t get any results before iterating at least once

     Primitive-recursiveness of evaluation.
lemma n2pr_ev: "n2pr X =⇒ n2pr Y =⇒ n2pr (𝜆x y. {|e x y |} )
                  =⇒ n2pr (𝜆x y. {|ev f (X x y) (Y x y) (e x y)|} )"
lemma n2pr_ei: "n2pr X =⇒ n2pr Y =⇒ n2pr s =⇒ n2pr (𝜆x y. {|ei f (X x y) (Y x y) (s
x y)|} )"
lemma n2pr_etI: "n2pr (𝜆x y. {|f x y |} ) =⇒ n2pr X =⇒ n2pr Y =⇒ n2pr s
                 =⇒ n2pr (𝜆x y. {|et (f x y) (X x y) (Y x y) (s x y)|} )"
lemma n2pr_erI: "n2pr (𝜆x y. {|f x y |} ) =⇒ n2pr X =⇒ n2pr Y =⇒ n2pr s
                =⇒ n2pr (𝜆x y. er (f x y) (X x y) (Y x y) (s x y))"

A.12      Logic syntax
type_synonym var = nat %
type_synonym opr = nat

     a generic abstract syntax for terms with variables, normal operators, and variable binders
datatype trm =
     trmVar var
  | trmOpr opr nat "trm list"

  A type of this class represents a collection of terms in some form that supports membership tests
and structure-preserving mapping of member terms.
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic              45


fun trm_free :: "var ⇒ trm ⇒ bool" where
     "trm_free v (trmVar vr) = (v = vr)"
   | "trm_free v (trmOpr op nb ([])) = False"
   | "trm_free v (trmOpr op nb (t # ts)) = (trm_free (v+nb) t ∨ trm_free v (trmOpr op
nb ts))"

  The set of free variables in a term
definition trm_fresh :: "var ⇒ trm ⇒ bool" where
      "trm_fresh v t ≡ ∀ v’. trm_free v’ t −→ v’ < v"

  Term is closed when it has no free variables.
abbreviation trm_closed :: "trm ⇒ bool" where
     "trm_closed t ≡ trm_fresh 0 t"
fun trm_lift :: "var ⇒ nat ⇒ trm ⇒ trm" where
     "trm_lift v n (trmVar vr) =
       (if vr < v then trmVar vr else trmVar (vr + n))"
   | "trm_lift v n (trmOpr op nb T) =
       trmOpr op nb (map (trm_lift (v+nb) n) T)"

A.13     Grounded arithmetic (GA): generic locale-based reasoning
A.13.1    Locale-based semantic modeling of grounded proof systems including BGA.
locale model =
   fixes val :: "asn ⇒ trm ⇒ any"
   assumes val_var: "val A (vi) = A i"
      and free_vars_val_eq: "asn_equiv A A’ t =⇒ val A t = val A’ t"
locale model_true = model + premodel_vtrue
begin

  satisfaction of hypotheses, conclusions, and judgments
abbreviation tsat :: "asn ⇒ trm ⇒ bool" where
  "tsat A t ≡ vtrue (val A t)"

  Assignment A satisfies all hypotheses in a finite set H.
definition hsat :: "asn ⇒ trm fset ⇒ bool" where
   "hsat A H ≡ ∀ h |∈| H. tsat A h"

   Semantic entailment, meaning that a judgment of the form H ⊢ c preserves truth over all as-
signments. That is, if any assignment A satisfies all hypotheses H then it also satisfies conclusion
c.
definition jt :: "trm fset ⇒ trm ⇒ bool" (infix "|=" 50) where
   "jt H c ≡ ∀ A. hsat A H −→ tsat A c"

  All judgments in proof P preserve truth under all assignments.
definition pt :: "prf_proof ⇒ bool" where
   "pt P ≡ ∀ H c. P C [[H ⊢ c]] −→ jt H c"
locale model_false = model +
   fixes vfalse :: "any ⇒ bool"
begin

  falsity of terms under an assignment
locale model_bool = model_true + model_false +
   assumes vtrue_vfalse_disj: "¬(vtrue v ∧ vfalse v)"
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
46                                                                                      and Ananthajit Srikanth

locale model_subm = model_true +
   assumes val_subm_asn_trm: "val (subm_asn M A) t = val A (M ⇂t)"

     Satisfaction under the all-zero (all-bottom) assignment implies satisfaction under any assignment.
locale model_preserves_truth = model_true_derives +
   assumes derives_preserves_truth: "pvt P =⇒ P D [[H ⊢ c]] =⇒ jt H c"

     a model that identifies certain values as false values

     Semantic modeling of comparability, equality, and logical operators in GA.
locale model_cmp = model +
   fixes vcmp :: "any ⇒ bool"           %
locale model_eq = model_bool + model_cmp + trm_eq +
   assumes tbool_eq: "tbool A (ta = tb) ←→ vcmp (val A ta) ∧ vcmp (val A tb)"
      and   tsat_eq: "tbool A (ta = tb) =⇒ tsat A (ta = tb) ←→ val A ta = val A tb"
locale model_ne = model_eq + trm_ne +
   assumes tbool_ne: "tbool A (ta ≠ tb) ←→ tbool A (ta = tb)"
      and   tsat_ne: "tbool A (ta ≠ tb) =⇒ tsat A (ta ≠ tb) ←→ ¬tsat A (ta = tb)"

  Corresponding strict models ensure that equality comparisons yield boolean values only (and
exactly) when the arguments are comparable.
locale model_eq_preserves_truth = model_eq + model_ne + model_preserves_truth

     a model of the object-type predicate corresponding to comparable objects
locale model_neg = model_truth + trm_neg +
   assumes tbool_neg: "tbool A (¬a) ←→ tbool A a"
      and   tsat_neg: "tbool A a =⇒ tsat A (¬a) ←→ ¬tsat A a"

     A truth-preserving model with negation is syntactically consistent.
locale model_or = model_bool + trm_neg + trm_or +
   assumes tsat_or: "tsat A (a ∨ b) ←→ tsat A a ∨ tsat A b"

   In grounded (partial) logics, the unconditional model_or.tsat_or is too strong: a disjunction
can be true only when both of its operands are well-formed formulas, even if just one of them is true.
This refined model records that constraint in an asymmetric form mirroring the two introduction rules:
a disjunction is true exactly when one operand is true and the other operand is well-formed. Each
disjunct of the characterization thus corresponds to one disjunction-introduction rule, so that those
rules need only the single well-formedness side condition on their non-asserted operand. The side
condition is well-formedness as a formula (the wff predicate), since the operands are propositions.

     Semantic modeling of natural numbers and arithmetic in GA.
locale model_nat = model +
   fixes natv :: "nat ⇒ any"
   assumes natv_inj: "inj natv"
begin

     whether a semantic value denotes some natural number
locale model_nat_only = model_nat + model_bot +
   assumes natv_eq_Suc: "natv = Suc"
locale model_nat_zero = model_nat + trm_nat_zero +
   assumes val_0: "val A 0 = natv 0"
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic   47


locale model_nat_suc = model_nat + trm_nat_suc +
   assumes tnat_suc: "tnat A (S t) ←→ tnat A t"
      and   val_suc: "val A t = natv n =⇒ val A (S t) = natv (Suc n)"

  a model of a predecessor operator that leaves the 0-case behavior unspecified
locale model_nat_pred = model_nat + trm_nat_pred +
   assumes tnat_predE: "tnat A (P t) =⇒ tnat A t"
      and   val_pred_suc: "val A t = natv (Suc n) =⇒ val A (P t) = natv n"
locale model_app2_nat = model_subm + model_cmp + model_type_nat + trm_app2 + trm_dfns
+
   assumes tsat_app2_nat: "dfn_is d 2 b =⇒ tnat A x =⇒ tnat A y =⇒
                            val A (d[x,y]) = val (asn2 (val A x) (val A y)) b"

A.13.2    Truth preservation locales and proofs for grounded deduction rules.
locale prf_gd_model_eq = model_eq + model_subm
begin

  Symmetry of equality preserves truth.
lemma jt_eq_sym [intro]: "pt P =⇒ P C [[Γ ⊢ a = b]] =⇒ jt Γ (b = a)"
lemma jt_eq_trans [intro]: "pt P =⇒ P C [[Γ ⊢ a = b]] =⇒ P C [[Γ ⊢ b = c]] =⇒ jt Γ (a =
c)"
lemma jt_eq_subs [intro]: "pt P =⇒ P C [[Γ ⊢ a = b]] =⇒ P C [[Γ ⊢ [i↣a]p]]
                                                                    ↦      =⇒ jt Γ ([i↣b]p)"
                                                                                      ↦

locale prf_gd_model_ne = model_ne
begin

  Symmetry of not-equals preserves truth.
lemma jt_ne_sym [intro]: "pt P =⇒ P C [[Γ ⊢ a ≠ b]] =⇒ jt Γ (b ≠ a)"

A.14     Basic grounded arithmetic (BGA)
  BGA syntax expressed as closed HOL datatypes.
datatype tm =
     tmVar    nat
  | tm0
  | tmSuc     tm
  | tmPred tm
  | tmIfz     tm tm tm
  | tmApp2 nat tm tm

  boolean formula syntax, directly supporting only equality testing and negation
datatype fm =
     fmEq     tm tm
  | fmNe      tm tm

  BGA has only two types: natural numbers and booleans.

  Injection of closed BGA syntax into generic abstract syntax.
fun tm_to_trm :: "tm ⇒ trm" where
     "tm_to_trm (tmVar v) = trmVar v"
   | "tm_to_trm (tm0) = trmOpr {|to0|} 0 []"
   | "tm_to_trm (tmSuc a) = trmOpr {|toSuc|} 0 [tm_to_trm a]"
   | "tm_to_trm (tmPred a) = trmOpr {|toPred |} 0 [tm_to_trm a]"
   | "tm_to_trm (tmIfz n a b) = trmOpr {|toIfz|} 0 [tm_to_trm n,tm_to_trm a,tm_to_trm b]"
   | "tm_to_trm (tmApp2 d a b) = trmOpr {|toApp2 d |} 0 [tm_to_trm a,tm_to_trm b]"
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
48                                                                                      and Ananthajit Srikanth

   Proof derivation rules for BGA. Like its syntax, BGA includes only a small subset of the inference
rules of full GA. In our development we found it useful to define two slightly-different inference rule
sets for BGA: a set of eleven unconditional proof rules defined by a pui inductive predicate, and a
slightly-larger set of fourteen proof derivation rules defined by a derives inductive predicate.
   The first, most tightly-minimized pui rule set is summarized concisely in Table 2c, or in Is-
abelle/HOL syntax in Section A.14, and is defined in terms of the HOL datatypes tm and fm
corresponding exactly to BGA’s closed syntax as defined above.
   The second derives rule set, shown in Isabelle/HOL syntax in Section A.14, uses the extensible
generic syntax, which allows reasoning using this rule set to take better advantage of Isabelle’s
extensible and reusable locale-based techniques mentioned above, at a cost of requiring the use of
well-formedness predicates to separate the valid BGA terms and formulas out of the less-constrained
generic syntax.
   Our development uses a number of cross-conversion theorems to relate these rule sets to each
other syntactically, and to the operational semantics for BGA described below.
     Unconditional provability rules in terms of the closed BGA syntax type.
inductive pui :: "nat ⇒ fm ⇒ bool" where
     pui_0I:       "pui (Suc l) (fmNat tm0)"
   | pui_eq_sym: "pui (Suc l) (fmEq b a)" if "pui l (fmEq a b)"
                                    ↦
   | pui_eq_subs: "pui (Suc l) ([i↣b]p)"                                        ↦
                                           if "pui l (fmEq a b)" and "pui l ([i↣a]p)"
   | pui_ne_sym: "pui (Suc l) (fmNe b a)" if "pui l (fmNe a b)"
   | pui_suc_ne0: "pui (Suc l) (fmNe (tmSuc a) tm0)" if "pui l (fmNat a)"
   | pui_suc_eqI: "pui (Suc l) (fmEq (tmSuc a) (tmSuc b))" if "pui l (fmEq a b)"
   | pui_suc_neI: "pui (Suc l) (fmNe (tmSuc a) (tmSuc b))" if "pui l (fmNe a b)"
   | pui_predI:    "pui (Suc l) (fmEq (tmPred a) b)" if "pui l (fmEq a (tmSuc b))"
   | pui_ifzI1:    "pui (Suc l) (fmEq (tmIfz c a b) a)" if "pui l (fmEq c tm0)" and "pui
l (fmNat a)"
   | pui_ifzI2:    "pui (Suc l) (fmEq (tmIfz c a b) b)" if "pui l (fmNe c tm0)" and "pui
l (fmNat b)"
   | pui_app2I:    "pui (Suc l) (fmEq (tmApp2 d a b) c)" if "tm_dfn_sub2p d a b t" and
                                                             "pui l (fmNat a)" and "pui
l (fmNat b)" and
                                                             "pui l (fmEq t c)"

     provability in terms of step counts, with the step count elided.

     Proof derivation rules in the generic abstract syntax.
inductive derives :: "prf_proof ⇒ trm fset ⇒ trm ⇒ bool" ("_ D [[_ ⊢ _]]" [50,50,50] 50)
where
     pr_sub1:          "P C [[Γ ⊢ c]] =⇒ wft s =⇒ P D [[[v↣s]Γ
                                                             ↦   ⊢ [v↣s]c]]"
                                                                       ↦
   | pr_hyp:           "wff c =⇒ P D [[c ⊲ Γ ⊢ c]]"
   | pr_wk1:           "P C [[Γ ⊢ c]] =⇒ P D [[a ⊲ Γ ⊢ c]]"
   | pr_cut:           "P C [[Γ ⊢ a]] =⇒ P C [[a ⊲ Γ ⊢ c]] =⇒ P D [[Γ ⊢ c]]"
   | pr_eq_subs:       "P C [[Γ ⊢ a = b]] =⇒ P C [[Γ ⊢ [i↣a]p]]
                                                           ↦    =⇒ isfm p =⇒ P D [[Γ ⊢ [i↣b]p]]"
                                                                                         ↦
   | pr_eq_sym:        "P C [[Γ ⊢ a = b]] =⇒ P D [[Γ ⊢ b = a]]"
   | pr_ne_sym:        "P C [[Γ ⊢ a ≠ b]] =⇒ P D [[Γ ⊢ b ≠ a]]"
   | pr_0:             "P D [[Γ ⊢ 0 N]]"
   | pr_suc_ne0:       "P C [[Γ ⊢ a N]] =⇒ P D [[Γ ⊢ S a ≠ 0]]"
   | pr_suc_eqI:       "P C [[Γ ⊢ a = b]] =⇒ P D [[Γ ⊢ S a = S b]]"
   | pr_suc_eqE:       "P C [[Γ ⊢ S a = S b]] =⇒ P D [[Γ ⊢ a = b]]"
   | pr_suc_neI:       "P C [[Γ ⊢ a ≠ b]] =⇒ P D [[Γ ⊢ S a ≠ S b]]"
   | pr_suc_neE:       "P C [[Γ ⊢ S a ≠ S b]] =⇒ P D [[Γ ⊢ a ≠ b]]"
   | pr_pred_suc_eq: "P C [[Γ ⊢ a N]] =⇒ P D [[Γ ⊢ P (S a) = a]]"
   | pr_nat_ind:       "P C [[Γ ⊢ [i↣0]c]]
                                     ↦      =⇒ P C [[vi N ⊲ c ⊲ Γ ⊢ [i↣S(vi)]c]]
                                                                         ↦       =⇒
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic              49


                           P C [[Γ ⊢ a N]] =⇒ ¬free i Γ =⇒ P D [[Γ ⊢ [i↣a]c]]"
                                                                         ↦
  | pr_ifz_eqI1:          "P C [[Γ ⊢ c = 0]] =⇒ P C [[Γ ⊢ a N]] =⇒ wft b =⇒ P D [[Γ ⊢ (c 0? a :
b) = a]]"
  | pr_ifz_eqI2:          "P C [[Γ ⊢ c ≠ 0]] =⇒ P C [[Γ ⊢ b N]] =⇒ wft a =⇒ P D [[Γ ⊢ (c 0? a :
b) = b]]"

  | pr_app2I:             "dfn_sub2p d x y t =⇒ P C [[Γ ⊢ x N]] =⇒ P C [[Γ ⊢ y N]] =⇒ isfm c
=⇒
                           P C [[Γ ⊢ [i↣t]c]]
                                       ↦      =⇒ P D [[Γ ⊢ [i↣d[x,y]]c]]"
                                                             ↦

  Unconditional BGA proofs in the closed syntax yield proof derivations in the generic syntax.
lemma pui_entails: "pui l f =⇒ {||} ⊢ fm_to_trm f"

  Operational semantics of BGA.
inductive os :: "asn ⇒ step ⇒ trm ⇒ any ⇒ bool" where
     os_varI: "os A (Suc sp) (vi) r" if "A i = Suc r"
   | os_0I:     "os A (Suc sp) (0) 0"
   | os_sucI: "os A (Suc sp) (S a) (Suc ra)" if "os A sp a ra"
   | os_predI: "os A (Suc sp) (P a) ra" if "os A sp a (Suc ra)"
   | os_ifzI1: "os A (Suc sp) (c 0? a : b) ra" if "os A sp c (0)" and "os A sp a ra"
   | os_ifzI2: "os A (Suc sp) (c 0? a : b) rb" if "os A sp c (Suc n)" and "os A sp b rb"
   | os_app2I: "os A (Suc sp) ((d[a,b])) r" if "dfn_is d 2 c" and
                                                  "os A sp a ra" and "os A sp b rb" and
                                                  "os (asn2 (Suc ra) (Suc rb)) sp c r"
   | os_eqI:    "os A (Suc sp) (a = b) {|na = nb|} " if "os A sp a na" and "os A sp b nb"
   | os_neI:    "os A (Suc sp) (a ≠ b) {|na ≠ nb|} " if "os A sp a na" and "os A sp b nb"
definition val :: "asn ⇒ trm ⇒ any" where
   "val A t ≡ if ∃ r s. os A s t r then Suc (SOME r. ∃ s. os A s t r) else 0"

  A given term reduces to at most one semantic value.
lemma os_single_valued: "single_valuedp (os A s)"

  All BGA proof rules preserve truth so BGA is semantically consistent.
sublocale pt: model_preserves_truth val vtrue derives

  No contradictory formulas are provable so BGA is syntactically consistent.
sublocale model_eq_preserves_truth val vtrue vfalse vcmp trmEq trmNe derives

A.14.1    Semantic completeness of BGA.
  Any reduction of term 𝑡 to result 𝑟 is provable in BGA.
lemma os_istm_pui: "os A s t r =⇒ istm t
                      =⇒ ∃ l. pui l (fmEq (tm_of_trm (asn_subm A ⇂ t)) (tmNum r))"

  Any formula that reduces to true is provable in BGA.
lemma os_isfm_pui: "os A s t {|True|} =⇒ isfm t =⇒ ∃ l. pui l (fm_of_trm (asn_subm A ⇂
t))"

A.14.2    Representation of recursive functions in GA.
  Recursive definition lists as background assumptions in grounded formal systems.
locale trm_dfns =
   fixes dfns :: "trm list"
begin

  Determine whether d is the number of a valid k -argument definition with body term b.
            Dimitrios Alexopoulos, Elliot Bobrow, Yusuf Demir, Bryan Ford, Stefan Milenković, Omar Muhammad,
50                                                                                      and Ananthajit Srikanth

definition dfn_is :: "dfn ⇒ nat ⇒ trm ⇒ bool" where
   "dfn_is d k b ≡ d < length dfns ∧ dfns ! d = b ∧ fresh k b"

  Determine whether d is a valid definition, A is a valid arguments list for it, and the result of
substituting these arguments into the definition is result term t.

     Recursive definition templates expressing particular forms of function composition in GA.
definition comp_def_sub :: "dfn ⇒ dfn ⇒ dfn ⇒ trm" where
   "comp_def_sub g h1 h2 ≡ g[h1[v0 , v1 ], h2[v0 , v1 ]]"
definition comp_def_rec :: "dfn ⇒ dfn ⇒ dfn ⇒ dfn ⇒ trm" where
   "comp_def_rec f g h h’ ≡ v1 0? g[v0 , 0] : h[h’[v0 , P v1 ], f[v0 , P v1 ]]"

     Kleene’s minimization operator 𝜇

definition comp_def_mu :: "dfn ⇒ dfn ⇒ trm" where
   "comp_def_mu f g ≡ g[v0 , v1 ] 0? f[v0 , S v1 ] : S v1 "

     evaluation of a step function to its result, assuming it terminates

definition comp_def_sf :: "dfn ⇒ dfn ⇒ trm" where
   "comp_def_sf f g ≡ g[v0 , v1 ] 0? f[v0 , S v1 ] : P g[v0 , v1 ]"

     GA representation of the four standard 2-argument initial functions

     Representation of primitive-recursive functions in GA definitions.
fun rif_rep :: "dfn ⇒ rifidx ⇒ bool" where
     "rif_rep d (rInit0) = dfn_is d 2 (0)"
   | "rif_rep d (rInitS) = dfn_is d 2 (S (v0))"
   | "rif_rep d (rInitL) = dfn_is d 2 (v0)"
   | "rif_rep d (rInitR) = dfn_is d 2 (v1)"

     GA representation of primitive-recursive function indices as an inductive predicate

inductive pri_rep :: "dfn ⇒ pridx ⇒ bool" where
     "pri_rep d (prInit i)" if "rif_rep d i"
   | "pri_rep d (prSub g h1 h2)" if "dfn_is d 2 (comp_def_sub dg dh1 dh2)" and
                        "pri_rep dg g" and "pri_rep dh1 h1" and "pri_rep dh2 h2"
   | "pri_rep d (prRec g h h’)" if "dfn_is d 2 (comp_def_rec d dg dh dh’)" and
                        "pri_rep dg g" and "pri_rep dh h" and "pri_rep dh’ h’"

   Definition df represents a general-recursive step function built on an underlying primitive-recursive
step function with definition dg.

     Representation of general-recursive functions in GA definitions.
inductive gri_rep :: "dfn ⇒ pridx ⇒ bool" where
     "gri_rep d g" if "dfn_is d 2 (comp_def_sf d dg)" and "pri_rep dg g"

     Representation of recursive functions in BGA.
locale bga_dfns = bga_syntax +
   fixes tm_dfns :: "tm list"
locale bga = bga_dfns
     ...
Have a thing? Reasoning around recursion with dynamic typing in grounded arithmetic                 51


A.14.3    Computational logic operators in BGA.
locale sfPf_sfde = well_formed_formula + refutes + sfPf_pr2 +
   assumes sfPf_sfde1: "consistent_ref Γ =⇒ sfde sfPf ⟨ {|Γ |} ,{|c|} ⟩ 1 ←→ entails Γ c"
      and   sfPf_sfde0: "consistent_ref Γ =⇒ sfde sfPf ⟨ {|Γ |} ,{|c|} ⟩ 0 ←→ refutes Γ c"
      and   sfde_sfPf_binary: "sfde sfPf x r =⇒ r ≤ 1"

   Stronger assumptions: provided only that the conclusion is well-formed, then function sfPf enu-
merates all results corresponding to entailment or refutation: even if the hypotheses are inconsistent,
in which case sfPf enumerates both 0 and 1. sfPf enumerates a True result if the hypotheses entail the
conclusion, sfPf enumerates a False result if the hypotheses refute the conclusion, sfPf enumerates
both True and False if the hypotheses are inconsistent; sfPf yields neither result if the hypotheses
neither entail nor refute the conclusion.
locale sfPf_sfde_consistent = sfPf_sfde + consistent_ref_logic + consistent_eq_logic +
entails_wff
locale sfPf_sfde_complete = well_formed_predicate + trm_dfns + refutes_wff +
                              ga_minimal + ga_ifz_eqI +
                              sfPf_sfde_consistent + sfPf_sfde_rep + refutes_eq + prf_model_eq_
locale sfPf_sfde_rep = well_formed_predicate + refutes + rec_fun_rep +
                         sfPf_sfde + sfPf_sfde_rep_tc1Pf + rep_cpair_subs + trm_nat_cons_istc
+
   assumes rep_sfde_sfPf: "rep_sfde sfPf tc1Pf"
      and   wft_tc1Pf: "wft1 tc1Pf"
begin

  Derive a term constructor representing unconditional provability.

  Logical negation.
definition trmNeg :: tc1 ("¬_" [140] 140) where "¬p ≡ tcPneg (n{|p|} ) = 1"
lemma entails_neg_refutes: shows "entails ∅ (¬p) ←→ refutes ∅ p"
lemma refutes_neg_entails: shows "refutes ∅ (¬p) ←→ entails ∅ p"

  Logical disjunction.
definition sfPor1 :: n2f where
   "sfPor1 ≡ sfpar (sfonly (𝜆x. sfPu (cpx x)) 1) (sfonly (𝜆x. sfPu (cpy x)) 1)"
definition sfPor0 :: n2f where
   "sfPor0 ≡ sfonly2 (𝜆x. sfPu (cpx x)) 0 (𝜆x. sfPu (cpy x)) 0 0"
definition sfPor :: n2f where
   "sfPor x y ≡ if wff (decode (cpx x)) ∧ wff (decode (cpy x))
                   then sfPorw x y else 0"
definition trmOr :: tc2 (infixr "∨" 130) where "p ∨ q ≡ tcPor ⟨n{|p|} ,n{|q |} ⟩ = 1"
lemma tcPor_entails_iff:
   shows "entails ∅ (p ∨ q) ←→ wff p ∧ wff q ∧ (entails ∅ p ∨ entails ∅ q)"
lemma tcPor_refutes_iff:
   shows "refutes ∅ (p ∨ q) ←→ wff p ∧ wff q ∧ refutes ∅ p ∧ refutes ∅ q"
