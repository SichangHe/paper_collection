Logical Methods in Computer Science
Volume 15, Issue 2, 2019, pp. 5:1–5:23                                                                Submitted         Oct. 31, 2018
https://lmcs.episciences.org/                                                                         Published         Apr. 30, 2019




                                ALL-PATH REACHABILITY LOGIC

 ANDREI S, TEFĂNESCU a,∗ , STEFAN CIOBÂCĂ b , RADU MEREUTA b,c , BRANDON M. MOORE c,∗ ,
                GRIGORE ROS, U d,c , AND TRAIAN FLORIN S, ERBĂNUT, Ă c,e
     a
         Galois, Inc., USA
         e-mail address: andrei@galois.com
     b
         Alexandru Ioan Cuza University, Romania
         e-mail address: {stefan.ciobaca,radu.mereuta}@info.uaic.ro
     c
         Runtime Verification, Inc., USA
         e-mail address: brandon.moore@runtimeverification.com
     d
         University of Illinois at Urbana-Champaign, USA
         e-mail address: grosu@illinois.edu
     e
         University of Bucharest, Romania
         e-mail address: traian.serbanuta@fmi.unibuc.ro


            Abstract. This paper presents a language-independent proof system for reachability
            properties of programs written in non-deterministic (e.g., concurrent) languages, referred to
            as all-path reachability logic. It derives partial-correctness properties with all-path semantics
            (a state satisfying a given precondition reaches states satisfying a given postcondition on
            all terminating execution paths). The proof system takes as axioms any unconditional op-
            erational semantics, and is sound (partially correct) and (relatively) complete, independent
            of the object language. The soundness has also been mechanized in Coq. This approach
            is implemented in a tool for semantics-based verification as part of the K framework
            (http://kframework.org).


                                                  1. Introduction
Operational semantics are easy to define and understand. Giving a language an operational
semantics can be regarded as “implementing” a formal interpreter. Operational semantics
require little formal training, scale up well and, being executable, can be tested. Thus,
operational semantics are typically used as trusted reference models for the defined languages.
Despite these advantages, operational semantics are rarely used directly for program verifica-
tion (i.e., verifying properties of a given program, rather than performing meta-reasoning
about a given language), because such proofs tend to be low-level and tedious, as they involve
formalizing and working directly with the corresponding transition system. Hoare or dynamic
logics allow higher level reasoning at the cost of (re)defining the language as a set of abstract
proof rules, which are harder to understand and trust. The state-of-the-art in mechanical
 ∗
   Most of the present work was done while still being PhD students at the University of Illinois at
Urbana-Champaign.




l        LOGICAL METHODS
         IN COMPUTER SCIENCE           DOI:10.23638/LMCS-15(2:5)2019
                                                                           ©
                                                                            CC
                                                                                 S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin
                                                                                   Creative Commons
5:2               S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin              Vol. 15:2




program verification is to develop and prove such language-specific proof systems sound
w.r.t to a trusted operational semantics [1–3], but that needs to be done for each language
separately.
     Defining more semantics for the same language and proving the soundness of one semantics
in terms of another are highly uneconomical tasks where real programming languages are
concerned, often taking several years to complete. Ideally, we would like to have only one
semantics for a language, together with a generic theory and a set of generic tools and
techniques allowing us to get all the benefits of any other semantics without paying the price
of defining other semantics. Recent work [4–7] shows this is possible, by proposing a language-
independent proof system which derives program properties directly from an operational
semantics, at the same proof granularity and compositionality as a language-specific axiomatic
semantics. Specifically, it introduces (one-path) reachability rules, which generalize both
operational semantics reduction rules and Hoare triples, and gives a proof system which
derives new reachability rules (program properties) from a set of given reachability rules (the
language semantics).
     However, the existing proof system has a major limitation: it only derives reachability
rules with a one-path semantics, that is, it guarantees a program property holds on one but
not necessarily all execution paths, which suffices for deterministic languages but not for
non-deterministic (concurrent) languages. Here we remove this limitation, proposing the first
generic all-path reachability proof system for program verification.
     Using matching logic [8] as a configuration specification formalism (Section 2), where
a pattern ϕ specifies all program configurations that match it, we first introduce the novel
notion of an all-path reachability rule ϕ ⇒∀ ϕ0 (Section 3), where ϕ and ϕ0 are matching logic
patterns. Rule ϕ ⇒∀ ϕ0 is valid iff any program configuration satisfying ϕ reaches, on any
complete execution path, some configuration satisfying ϕ0 . This subsumes Hoare-style partial
correctness in non-deterministic languages. We then present a proof system for deriving an
all-path reachability rule ϕ ⇒∀ ϕ0 from a set S of semantics rules (Section 4). S consists of
reduction rules ϕl ⇒∃ ϕr , where ϕl and ϕr are simple patterns as encountered in operational
semantics (Section 5), which can be non-deterministic. The proof system derives more general
sequents “S, A `C ϕ ⇒∀ ϕ0 ”, with A and C two sets of reachability rules. Intuitively, A’s
rules (axioms) are already established valid, and thus can be immediately used. Those in
C (circularities) are only claimed valid, and can be used only after taking execution steps
based on the rules in S or A. The most important proof rules are
             Step : W
             |= ϕ → ϕl ⇒∃ ϕr ∈ S ∃FreeVars(ϕl ) ϕl
             |= ∃c (ϕ[c/] ∧ ϕl [c/]) ∧ ϕr → ϕ0          for each ϕl ⇒∃ ϕr ∈ S
                                       S, A `C ϕ ⇒∀ ϕ0
             Circularity :
             S, A `C∪{ϕ⇒∀ ϕ0 } ϕ ⇒∀ ϕ0
                   S, A `C ϕ ⇒∀ ϕ0
Step is the key proof rule which deals with non-determinism: it derives a sequent where ϕ
reaches ϕ0 in one step on all paths. The first premise ensures that any configuration satisfying
ϕ has successors, the second that all successors satisfy ϕ0 ( is the configuration placeholder).
Circularity adds the current goal to C at any point in a proof, and generalizes the various
Vol. 15:2                          ALL-PATH REACHABILITY LOGIC                                  5:3




language-specific axiomatic semantics invariant rules in a language-independent way (this
form was introduced in [4]).
    We illustrate on examples how our proof system enables state exploration (similar to
symbolic model-checking), and verification of program properties (Section 5). We show that
our proof system is sound (Section 7) and relatively complete (Section 8). We describe our
implementation of the proof system as part of the K framework [9] (Section 6).

Contributions. This paper makes the following specific contributions:
(1) A language-independent proof system for deriving all-path reachability properties, with
    (complete) proofs of its soundness and relative completeness; the soundness result has
     also been mechanized in Coq, to serve as a foundation for certifiable verification.
(2) An implementation of it as part of the K framework (http://kframework.org).
     An earlier, shorter version of this paper appeared at RTA-TCLA 2014 [10]. The main
differences are the inclusion of proofs for soundness (Section 7), and relative completeness
(Section 8).

                               2. Topmost Matching Logic
Matching logic [11,12] is a first-order logic (FOL) variant designed for specifying and reasoning
about structure by means of patterns and pattern matching. In this section, we briefly recall
topmost matching logic [8], a subset of the full matching logic theory described in [11,12]. We
employ topmost matching logic to specify and reason about arbitrary program configurations.
For simplicity, we use “matching logic” instead of “topmost matching logic” in this paper. A
matching logic formula, called a pattern, is a first-order logic (FOL) formula with special
predicates, called basic patterns. A basic pattern is a configuration term with variables.
Intuitively, a pattern specifies both structural and logical constraints: a configuration satisfies
the pattern iff it matches the structure (basic patterns) and satisfies the constraints.
     Matching logic is parametric in a signature and a model of configurations, making it
a prime candidate for expressing state properties in a language-independent verification
framework. The configuration signature can be as simple as that of IMP (Fig. 2), or as
complex as that of the C language [13, 14] (with more than 100 semantic components).
     We use basic concepts from multi-sorted first-order logic. Given a signature Σ which
specifies the sorts and arities of the function symbols (constructors or operators) used in
configurations, let TΣ (Var) denote the free Σ-algebra of terms with variables in Var. TΣ,s (Var)
is the set of Σ-terms of sort s. A valuation ρ : Var → T with T a Σ-algebra extends uniquely
to a (homonymous) Σ-algebra morphism ρ : TΣ (Var) → T . Many mathematical structures
needed for language semantics have been defined as Σ-algebras, including: boolean algebras,
natural/integer/rational numbers, lists, sets, bags (or multisets), maps (e.g., for states,
heaps), trees, queues, stacks, etc.
     Let us fix the following: (1) an algebraic signature Σ, associated to some desired
configuration syntax, with a distinguished sort Cfg, (2) a sort-wise infinite set Var of
variables, and (3) a Σ-algebra T , the configuration model, which may but need not be a term
algebra. As usual, TCfg denotes the elements of T of sort Cfg, called configurations.
Definition 2.1 [8]. A matching logic formula, or a pattern, is a first-order logic (FOL)
formula which additionally allows terms in TΣ,Cfg (Var), called basic patterns, as predicates.
A pattern is structureless if it contains no basic patterns.
5:4               S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin             Vol. 15:2




    We define satisfaction (γ, ρ) |= ϕ over configurations γ ∈ TCfg , valuations ρ : Var → T and
patterns ϕ as follows (among the FOL constructs, we only show ∃):
 (γ, ρ) |= ∃X ϕ iff (γ, ρ0 ) |= ϕ for some ρ0 : Var → T with ρ0 (y) = ρ(y) for all y ∈ Var\X
 (γ, ρ) |= π      iff γ = ρ(π)       where π ∈ TΣ,Cfg (Var)
We write |= ϕ when (γ, ρ) |= ϕ for all γ ∈ TCfg and all ρ : Var → T .
    A basic pattern π is satisfied by all the configurations γ that match it; in (γ, ρ) |= π the
ρ can be thought of as the “witness” of the matching, and can be further constrained in a
pattern. For instance, the pattern from Section 5
                       hx := x+1 || x := x+1, x 7→ ni ∧ (n = 0 ∨ n = 1)
is matched by the configurations with code “x := x+1 || x := x+1” and state mapping program
variable x into integer n with n being either 0 or 1. We use italic for mathematical variables
in Var and typewriter for program variables (program variables are represented in matching
logic as constants of sort PVar , see Section 5).
     The “topmost” matching logic variant that we use in this paper is a fragment of the
general matching logic approach proposed in [11, 12], where terms are regarded as predicates
only at the top level, where they have the sort Cfg. The general matching logic approach
in [11, 12] allows the distinctive terms-as-predicates view as well as the mix of logical and
structural constraints at all levels, for any terms of any sorts. As an example, the pattern
above may be equivalently written as
                       hx := x+1 || x := x+1, x 7→ n ∧ (n = 0 ∨ n = 1)i
thus localizing the logical constraints to the actual place in the configuration where they
matter. We remind the reader that in this paper we limit ourselves to “topmost” matching
logic, and that we take the freedom to drop the “topmost” and just call it “matching logic”.
     Next, we recall how matching logic formulae can be translated into FOL formulae, so
that its satisfaction becomes FOL satisfaction in the model of configurations, T . Then, we
can use conventional theorem provers or proof assistants for pattern reasoning.
Definition 2.2 [8]. Let  be a fresh Cfg variable. For a pattern ϕ, let ϕ be the FOL
formula formed from ϕ by replacing basic patterns π ∈ TΣ,Cfg (Var) with equalities  = π. If
ρ : Var → T and γ ∈ TCfg then let the valuation ργ : Var ∪ {} → T be such that ργ (x) = ρ(x)
for x ∈ Var and ργ () = γ.
With the notation in Definition 2.2, (γ, ρ) |= ϕ iff ργ |= ϕ , and |= ϕ iff T |= ϕ . Thus,
matching logic is a methodological fragment of the FOL theory of T . We drop  from ϕ
when it is clear in context that we mean the FOL formula instead of the matching logic
pattern. It is often technically convenient to eliminate  from ϕ, by replacing  with a Cfg
variable c and using ϕ[c/] instead of ϕ. We use the FOL representation in the Step proof
rule in Fig. 1, and to establish relative completeness in Section 8.

                               3. Specifying Reachability
In this section we define one-path and all-path reachability. We begin by recalling some
matching logic reachability [6] notions that we need for specifying reachability.
Vol. 15:2                          ALL-PATH REACHABILITY LOGIC                                 5:5




Definition 3.1 [6]. A (one-path) reachability rule is a pair ϕ ⇒∃ ϕ0 , where ϕ and ϕ0
are patterns (which can have free variables). Rule ϕ ⇒∃ ϕ0 is weakly well-defined iff
for any γ ∈ TCfg and ρ : Var → T with (γ, ρ) |= ϕ, there exists γ 0 ∈ TCfg with (γ 0 , ρ) |= ϕ0 .
A reachability system is a set of reachability rules. Reachability system S is weakly
well-defined iff each rule is weakly well-defined. S induces a transition system (T , ⇒TS )
on the configuration model: γ ⇒TS γ 0 for γ, γ 0 ∈ TCfg iff there is some rule ϕ ⇒∃ ϕ0 in S
and some valuation ρ : Var → T with (γ, ρ) |= ϕ and (γ 0 , ρ) |= ϕ0 . A ⇒TS -path is a finite
sequence γ0 ⇒TS γ1 ⇒TS ... ⇒TS γn with γ0 ,...,γn ∈ TCfg . A ⇒TS -path is complete iff it is not a
strict prefix of any other ⇒TS -path.
      We assume an operational semantics is a set of (unconditional) reduction rules “l ⇒∃
r if b”, where l, r ∈ TΣ,Cfg (Var) are program configurations with variables and b ∈ TΣ,Bool (Var)
is a condition constraining the variables of l, r. Styles of operational semantics using only
such (unconditional) rules include evaluation contexts [15], the chemical abstract machine [16]
and K [9] (see Section 5 for an evaluation contexts semantics). Several large languages have
been given semantics in such styles, including C [13] (more than 3000 rules) and R5RS
Scheme [17]. The reachability proof system works with any set of rules of this form, being
agnostic to the particular style of semantics.
      Such a rule “l ⇒∃ r if b” states that a ground configuration γ which is an instance of
l and satisfies the condition b reduces to an instance γ 0 of r. Matching logic can express
terms with constraints: l ∧ b is satisfied by exactly the γ above. Thus, we can regard such a
semantics as a particular weakly well-defined reachability system S with rules of the form
“l ∧ b ⇒∃ r”. The weakly well-defined condition on S guarantees that if γ matches the
left-hand-side of a rule in S, then the respective rule induces an outgoing transition from γ.
The transition system induced by S describes precisely the behavior of any program in any
given state. In [4–6] we show that reachability rules capture one-path reachability properties
and Hoare triples for deterministic languages.
      Formally, let us fix an operational semantics given as a reachability system S. Then, we
can specify reachability in the transition system induced by S, both all-path and one-path,
as follows:
Definition 3.2. An all-path reachability rule is a pair ϕ ⇒∀ ϕ0 of patterns ϕ and ϕ0 .
        An all-path reachability rule ϕ ⇒∀ ϕ0 is satisfied, S |= ϕ ⇒∀ ϕ0 , iff for all complete
    T
⇒S -paths τ starting with γ ∈ TCfg and for all ρ : Var → T such that (γ, ρ) |= ϕ, there exists
some γ 0 ∈ τ such that (γ 0 , ρ) |= ϕ0 .
        A one-path reachability rule ϕ ⇒∃ ϕ0 is satisfied, S |= ϕ ⇒∃ ϕ0 , iff for all γ ∈ TCfg and
ρ : Var → T such that (γ, ρ) |= ϕ, there is either a ⇒TS -path from γ to some γ 0 such that
(γ 0 , ρ) |= ϕ0 , or there is a diverging execution γ ⇒TS γ1 ⇒TS γ2 ⇒TS · · · from γ.
     The racing increment example in Section 5 can be specified by
   hx := x+1 || x := x+1, x 7→ mi ⇒∀ ∃n (hskip, x 7→ ni ∧ (n = m +Int 1 ∨ n = m +Int 2)
which states that every terminating execution reaches a state where execution of both threads
is complete and the value of x has increased by 1 or 2 (this code has a race).
     A Hoare triple describes the resulting state after execution finishes, so it corresponds
to a reachability rule where the right side contains no remaining code. However, all-path
reachability rules are strictly more expressive than Hoare triples, as they can also specify
intermediate configurations (the code in the right-hand-side need not be empty). Reachability
5:6                 S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin                   Vol. 15:2




 Step : W                                                                            Axiom :
 |= ϕ → ϕl ⇒∃ ϕr ∈ S ∃FreeVars(ϕl ) ϕl
 |= ∃c (ϕ[c/] ∧ ϕl [c/]) ∧ ϕr → ϕ0           for each ϕl ⇒∃ ϕr ∈ S                  ϕ ⇒∀ ϕ0 ∈ A
                            S, A `C ϕ ⇒∀ ϕ0                                          S, A `C ϕ ⇒∀ ϕ0
 Reflexivity :                                          Transitivity :
        ·                                               S, A `C ϕ1 ⇒∀ ϕ2    S, A ∪ C ` ϕ2 ⇒∀ ϕ3
 S, A ` ϕ ⇒∀ ϕ                                                     S, A `C ϕ1 ⇒∀ ϕ3
 Case Analysis :                                             Abstraction :
                ∀                          ∀
  S, A `C ϕ1 ⇒ ϕ      S, A `C ϕ2 ⇒ ϕ                         S, A `C ϕ ⇒∀ ϕ0    X ∩ FreeVars(ϕ0 ) = ∅
          S, A `C ϕ1 ∨ ϕ2 ⇒∀ ϕ                                         S, A `C ∃X ϕ ⇒∀ ϕ0
 Consequence :                                                               Circularity :
  |= ϕ1 → ϕ01       S, A   `C ϕ01 ⇒∀ ϕ02       |= ϕ02 → ϕ2                   S, A `C∪{ϕ⇒∀ ϕ0 } ϕ ⇒∀ ϕ0
                    S, A   ` C ϕ1 ⇒∀ ϕ2                                          S, A `C ϕ ⇒∀ ϕ0


Figure 1: Proof system for reachability. We make the standard assumption that the free
          variables of ϕl ⇒∃ ϕr in the Step proof rule are fresh (e.g., disjoint from those of
          ϕ ⇒∀ ϕ0 ).

rules provide a unified representation for both language semantics and program specifications:
ϕ ⇒∃ ϕ0 for semantics and ϕ ⇒∀ ϕ0 for all-path reachability specifications. Note that,
like Hoare triples, reachability rules can only specify properties of complete paths (that is,
terminating execution paths). One can use existing Hoare logic techniques to break reasoning
about a non-terminating program into reasoning about its terminating components.

                                 4. Reachability Proof System
Fig. 1 shows our novel proof system for all-path reachability. The target language is given as
a weakly well-defined reachability system S. The soundness result (Thm. 7.1) guarantees
that S |= ϕ ⇒∀ ϕ0 if S ` ϕ ⇒∀ ϕ0 is derivable. Note that the proof system derives more
general sequents of the form S, A `C ϕ ⇒∀ ϕ0 , where A and C are sets of reachability rules.
The rules in A are called axioms and rules in C are called circularities. If either A or C
does not appear in a sequent, it means the respective set is empty: S `C ϕ ⇒∀ ϕ0 is a
shorthand for S, ∅ `C ϕ ⇒∀ ϕ0 , and S, A ` ϕ ⇒∀ ϕ0 is a shorthand for S, A `∅ ϕ ⇒∀ ϕ0 ,
and S ` ϕ ⇒∀ ϕ0 is a shorthand for S, ∅ `∅ ϕ ⇒∀ ϕ0 . Initially, both A and C are empty.
Note that “→” in Step and Consequence denotes logical implication.
     The intuition is that the reachability rules in A can be assumed valid, while those in
C have been postulated but not yet justified. After making progress from ϕ (at least one
derivation by Step or by Axiom with the rules in A), the rules in C become (coinductively)
valid (can be used in derivations by Axiom). During the proof, circularities can be added to
C via Circularity, flushed into A by Transitivity, and used via Axiom. The desired
semantics for sequent S, A `C ϕ ⇒∀ ϕ0 (read “S with axioms A and circularities C proves
ϕ ⇒∀ ϕ0 ”) is: ϕ ⇒∀ ϕ0 holds if the rules in A hold and those in C hold after taking at least
one step from ϕ in the transition system (⇒TS , T ), and if C =6 ∅ then ϕ reaches ϕ0 after at
least one step on all complete paths. As a consequence of this definition, any rule ϕ ⇒∀ ϕ0
Vol. 15:2                          ALL-PATH REACHABILITY LOGIC                                 5:7




derived by Circularity has the property that ϕ reaches ϕ0 after at lest one step, due to
Circularity having a prerequisite S, A `C∪{ϕ⇒∀ ϕ0 } ϕ ⇒∀ ϕ0 (with a non-empty set of
circularities). We next discuss the proof rules.
     Step derives a sequent where ϕ reaches ϕ0 in one step on all paths. The first premise
ensures any configuration matching ϕ matches the left-hand-side ϕl of some rule in S and
thus, as S is weakly well-defined, can take a step. Formally, if (γ, ρ) |= ϕ, then there
exists some rule ϕl ⇒∃ ϕr ∈ S and some valuation ρ0 of the free variables of ϕl such that
(γ, ρ0 ) |= ϕl , and thus γ has at least one ⇒TS -successor generated by the rule ϕl ⇒∃ ϕr . The
second premise ensures that each ⇒TS -successor of a configuration matching ϕ matches ϕ0 .
Formally, if γ ⇒TS γ 0 and γ matches ϕ then there is some rule ϕl ⇒∃ ϕr ∈ S and ρ : Var → T
such that (γ, ρ) |= ϕ ∧ ϕl and (γ 0 , ρ) |= ϕr ; then the second premise implies γ 0 matches ϕ0 .
     Designing a proof rule for deriving an execution step along all paths is non-trivial. For
instance, one might expect Step to require as many premises as there are transitions going
out of ϕ, as is the case for the examples presented later in this paper. However, that is not
possible, as the number of successors of a configuration matching ϕ may be unbounded even
if each matching configuration has a finite branching factor in the transition system. Step
avoids this issue by requiring only one premise for each rule by which some configuration ϕ
can take a step, even if that rule can be used to derive multiple transitions. To illustrate
this situation, consider a language defined by S ≡ {hn1 i ∧ n1 >Int n2 ⇒∃ hn2 i}, with
n1 and n2 non-negative integer variables. A configuration in this language is a singleton
with a non-negative integer. Intuitively, a positive integer transits into a strictly smaller
non-negative integer, in a non-deterministic way. The branching factor of a non-negative
integer is its value. Then S |= hmi ⇒∀ h0i. Deriving it reduces (by Circularity and other
proof rules) to deriving hm1 i ∧ m1 >Int 0 ⇒∀ ∃m2 (hm2 i ∧ m1 >Int m2 ). The left-hand-side
is matched by any positive integer, and thus its branching factor is infinity. Deriving this rule
with Step requires only two premises, |= (hm1 i ∧ m1 >Int 0) → ∃n1 n2 (hn1 i ∧ n1 >Int n2 )
and |= ∃c (c = hm1 i ∧ m1 >Int 0 ∧ c = hn1 i ∧ n1 >Int n2 ) ∧ hn2 i → ∃m2 (hm2 i ∧ m1 >Int m2 ).
A similar situation arises in real life for languages with thread pools of arbitrary size.
     Axiom applies a trusted rule. Reflexivity and Transitivity capture the correspond-
ing closure properties of the reachability relation. Reflexivity requires C to be empty to
ensure that all-path rules derived with non-empty C take at least one step. Transitivity
enables the circularities as axioms for the second premise, since if C is not empty, the first
premise is guaranteed to take at least one step. Consequence, Case Analysis and Ab-
straction are adapted from Hoare logic. Ignoring circularities, these seven rules discussed
so far constitute formal infrastructure for symbolic execution.
     Circularity has a coinductive nature, allowing us to make new circularity claims.
We typically make such claims for code with repetitive behaviors, such as loops, recursive
functions, jumps, etc. If there is a derivation of the claim using itself as a circularity, then
the claim holds. This would obviously be unsound if the new assumption was available
immediately, but requiring progress (taking at least one step in the transition system (T , ⇒TS ))
before circularities can be used ensures that only diverging executions can correspond to
endless invocation of a circularity.
     One important aspect of concurrent program verification, which we do not address in
this paper, is proof compositionality. Our focus here is limited to establishing a sound and
complete language-independent proof system for all-path reachability rules, to serve as a
foundation for further results and applications, and to discuss our current implementation of
it. We only mention that we have already studied proof compositionality for earlier one-path
5:8                    S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin                   Vol. 15:2




       IMP language syntax                            IMP evaluation contexts syntax
      PVar ::= program variables                      Context ::=
        Exp ::= PVar | Int | Exp op Exp                         |   hContext, Statei
       Stmt ::= skip | PVar := Exp                              |   Context op Exp | Int op Context
              |    Stmt; Stmt | Stmt || Stmt                    |   PVar := Context | Context; Stmt
              |    if(Exp) Stmt else Stmt                       |   Context || Stmt     | Stmt || Context
              |    while(Exp) Stmt                              |   if(Context) Stmt else Stmt
       IMP operational semantics
      lookup hC, σi[x] ⇒∃ hC, σi[σ(x)]                        op       i1 op i2 ⇒∃ i1 op Int i2
      asgn      hC, σi[x := i] ⇒∃ hC, σ[x ← i]i[skip]         seq      skip; s ⇒∃ s
                                  ∃
      cond1     if(i) s1 else s2 ⇒ s1     if i 6= 0           cond2 if(0) s1 else s2 ⇒∃ s2
                              ∃
      while     while(e) s ⇒ if(e) s; while(e) s else skip    finish skip || skip ⇒∃ skip

 Figure 2: IMP language syntax and operational semantics based on evaluation contexts.

variants of reachability logic [5], showing that there is a mechanical way to translate any
Hoare logic proof derivation into a reachability proof of similar size and structure, but based
entirely on the operational semantics of the language. The overall conclusion of our previous
study, which we believe will carry over to all-path reachability, was that compositional
reasoning can be achieved methodologically using our proof system, by proving and then
using appropriate reachability rules as lemmas. However, note that this works only for
theoretically well-behaved languages which enjoy a compositional semantics. For example,
a language whose semantics assumes a bounded heap size, or which has constructs whose
semantics involve the entire program, e.g., call/cc, will lack compositionality.

                                        5. Verifying Programs
In this section we show a few examples of using our proof system to verify programs based on
an operational semantics. In a nutshell, the proof system enables generic symbolic execution
combined with circular reasoning. Symbolic execution is achieved by rewriting modulo
domain reasoning.
     First, we introduce a simple parallel imperative language, IMP. Fig. 2 shows its syntax
and an operational semantics based on evaluation contexts [15] (we choose evaluation contexts
for presentation purposes only). IMP has only integer expressions. When used as conditions
of if and while, zero means false and any non-zero integer means true (like in C). Expressions
are formed with integer constants, program variables, and conventional arithmetic constructs.
Arithmetic operations are generically described as op. IMP statements are assignment, if,
while, sequential composition and parallel composition. IMP has shared memory parallelism
without explicit synchronization. The examples use the parallel construct only at the top-level
of the programs. The second example shows how to achieve synchronization using the existing
language constructs.
     The program configurations of IMP are pairs hcode, σi, where code is a program
fragment and σ is a state term mapping program variables into integers. As usual, we assume
appropriate definitions for the integer and map domains available, together with associated
operations like arithmetic operations (i1 op Int i2 , etc.) on the integers and lookup (σ(x))
and update (σ[x ← i]) on the maps. We also assume a context domain with a plugging
operation (C[t]) that composes a context and term back into a configuration. A configuration
context consists of a code context and a state. The definition in Fig. 2 consists of eight
Vol. 15:2                                                      ALL-PATH REACHABILITY LOGIC                                                                               5:9



     D                       E            D                         E             D                             E           D                   E
         x:=x+1 || x:=x+1,                    x:=x+1 || x:=m+1,                       x:=x+1 || x:=m+Int 1,                  x:=x+1 || skip,
         x7→m                                 x7→m                                    x7→m                                   x7→m+Int 1
  D                             E         D                             E         D                                 E   D                           E   D                            E
     x:=m+1 || x:=x+1,                        x:=m+1 || x:=m+1,                    x:=m+1 || x:=m+Int 1,                     x:=m+1 || skip,            x:=m+Int 1+1 || skip,
     x7→m                                     x7→m                                 x7→m                                      x7→m+Int 1                 x7→m+Int 1
 D                               E    D                                 E     D                                     E   D                           E   D                            E
  x:=m+Int 1 || x:=x+1,                   x:=m+Int 1 || x:=m+1,                   x:=m+Int 1 || x:=m+Int 1,                 x:=m+Int 1 || skip,             x:=m+Int 2 || skip,
  x7→m                                    x7→m                                    x7→m                                      x7→m+Int 1                      x7→m+Int 1
      D                     E                 D                     E                 D                         E            D                  E
          skip || x:=x+1,                         skip || x:=m+1,                      skip || x:=m+Int 1,                      skip || skip,
          x7→m+Int 1                              x7→m+Int 1                           x7→m+Int 1                               x7→m+Int 1
                                          D                             E             D                         E                                            D                   E
                                          skip || x:=m+Int 1+1,                        skip || x:=m+Int 2,                                                       skip || skip,
                                          x7→m+Int 1                                   x7→m+Int 1                                                                x7→m+Int 2



                                     Figure 3: State space of the racing increment example

reduction rules between program configurations, which make use of first-order variables: x
is a variable of sort PVar ; e is a variable of sort Exp; s, s1 , s2 are variables of sort Stmt;
i, i1 , i2 are variables of sort Int; σ is a variable of sort State; C is a variable of sort Context.
A rule reduces a configuration by splitting it into a context and a redex, rewriting the
redex and possibly the context, and then plugging the resulting term into the resulting
context. As an abbreviation, a context is not mentioned if not used; e.g., the rule op is in
full hC, σi[i1 op i2 ] ⇒∃ hC, σi[i1 op Int i2 ]. For example, configuration hx := (2 + 5) − 4, σi
reduces to hx := 7 − 4, σi by applying the op+ rule with C ≡ x := − 4, σ ≡ σ, i1 ≡ 2 and
i2 ≡ 5. We can regard the operational semantics of IMP above as a set of reduction rules of
the form “l ⇒∃ r if b”, where l and r are program configurations with variables constrained
by boolean condition b. As discussed in Section 3, our proof system works with any rules of
this form.
       Next, we illustrate the proof system on a few examples. The first example shows that our
proof system enables exhaustive state exploration, similar to symbolic model-checking but
based on the operational semantics. Although humans prefer to avoid such explicit proofs
and instead methodologically use abstraction or compositional reasoning whenever possible
(and such methodologies are not excluded by our proof system), a complete proof system
must nevertheless support them. The code x := x+1 || x := x+1 exhibits a race on x: the
value of x increases by 1 when both reads happen before either write, and by 2 otherwise.
The all-path rule that captures this behavior is
      hx := x+1 || x := x+1, x 7→ mi ⇒∀ ∃n (hskip, x 7→ ni ∧ (n = m +Int 1 ∨ n = m +Int 2)
We show that the program has exactly these behaviors by deriving this rule in the proof
system. Call the right-hand-side pattern G. The proof contains subproofs of c ⇒∀ G
for every reachable configuration c, tabulated in Fig. 3. The subproofs for c match-
ing G use Reflexivity and Consequence, while the rest use Transitivity, Step,
and Case Analysis to reduce to the proofs for the next configurations. For example,
the proof fragment below shows how hx := m + 1 || x := x + 1, x 7→ mi ⇒∀ G reduces to
hx := m +Int 1 || x := x+1, x 7→ mi ⇒∀ G and hx := m+1 || x := m+1, x 7→ mi ⇒∀ G:
                                               ...                                                        ...                           ...
Step          D                       E              D                        E           D                       E
                                                                                              x:=m+Int 1 || x:=x+1,   ∀
                                                                                                                           D
                                                                                                                            x:=m+1 || x:=m+1,
                                                                                                                                              E
                                                                                                                                                  ∀
                  x:=m+1 || x:=x+1,
                                          ⇒
                                              ∀       x:=m+Int 1 || x:=x+1,
                                                                                              x7→m                  ⇒ G x7→m                   ⇒ G
                  x7→m
                                                     Dx7→m               E                    D                      E D                    E       CA
                                                      x:=m+1 || x:=m+1,                        x:=m+Int 1 || x:=x+1,     x:=m+1 || x:=m+1,      ∀
                                              ∨       x7→m                                     x7→m                   ∨ x7→m                  ⇒ G
                                                                                                          ∀
                                                                                                                                                                 Trans
                                                         hx := m + 1 || x := x + 1, x 7→ mi ⇒ G
5:10                 S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin                  Vol. 15:2




For the rule hypotheses                                 but lookup and op+ make the
                     D of Step above,E note that all rules
                             x:=m+1 || x:=x+1,
overlap condition ∃c      x7→m             [c/] ∧ ϕl [c/] unsatisfiable, and only one choice
of free variables works for the lookup and op+ rules. For lookup, ϕl is hC, σi[x] and
the overlap condition is only satisfiable if the logical variables C, σ and x are equal to
(x := m + 1 || x := + 1), (x 7→ m), and x, respectively. Under this assignment, the pattern
ϕr = hC, σi[σ(x)] is equivalent to hx := m + 1 || x := m + 1, x 7→ mi, the right branch of the
disjunction. The op+ rule is handled similarly. The assignment for lookup can also witness
the existential in the progress hypothesis of Step. Subproofs for other states in Fig. 3 can
be constructed similarly.
     The next two examples use loops and thus need
to state and prove invariants. As discussed in [4], Cir- f0 = 1;           f1 = 1;
cularity generalizes the various language-specific turn = 1;               turn = 0;
invariant proof rules encountered in Hoare logics. while (f1 && turn) while (f0 && (1 - turn))
One application is reducing a proof of ϕ ⇒∀ ϕ0             skip              skip
                     ∀          0
to proving ϕinv ⇒ ϕinv ∨ ϕ for some pattern in-          x = x + 1;        x = x + 1;
                                                         f0 = 0;           f1 = 0;
variant ϕinv . We first show |= ϕ → ϕinv , and use
Consequence to change the goal to ϕinv ⇒∀ ϕ0 .
                                                         Figure 4: Peterson’s         algorithm
This is claimed as a circularity, and then proved by
                                                                    (threads T0 and T1 )
transitivity with ϕinv ∨ ϕ0 . The second hypothesis
         ∀  0             0   ∀   0
{ϕinv ⇒ ϕ } ` ϕinv ∨ ϕ ⇒ ϕ is proved by Case
Analysis, Axiom, and Reflexivity.
     Next, we can use Peterson’s algorithm for mutual exclusion to eliminate the race as
shown in Fig. 4. The all-path rule ϕ ⇒∀ ϕ0 that captures the new behavior is
                         hT0 || T1 , (f0 7→ 0, f1 7→ 0, x 7→ N )i
                  ⇒∀     ∃t hskip, (f0 7→ 0, f1 7→ 0, x 7→ N +Int 2, turn 7→ t)i
Similarly to the unsynchronized example, the proof contains subproofs of c ⇒∀ ϕ0 for every
configuration c reachable from ϕ. The main difference is that Circularity is used with
each of these rules c ⇒∀ ϕ0 with one of the two threads of c in the while loop (these rules
capture the invariants). Thus, when we reach a configuration c visited before, we use the
rule added by Circularity to complete the proof.
     The final example is the program SUM ≡ “s := 0; LOOP” (where LOOP stands for “while
(n>0) (s := s+n; n := n-1)”), which computes in s the sum of the numbers from 1 up to
n. The all-path reachability rule ϕ ⇒∀ ϕ0 capturing this behavior is
       hSUM, (s 7→ s, n 7→ n)i ∧ n ≥Int 0 ⇒∀ hskip, (s 7→ n ∗Int (n +Int 1)/Int 2, n 7→ 0)i
We derive the above rule in our proof system by using Circularity with the invariant rule
         ∃n0 (hLOOP, (s 7→ (n−Int n0 )∗Int (n+Int n0 +Int 1)/Int 2, n 7→ n0 )i ∧ n0 ≥Int 0) ⇒∀ ϕ0
Previous work [4–7] presented a proof system able to derive similar rules, but which hold
along some execution path, requiring a separate proof that the program is deterministic.

                                         6. Implementation
Here we briefly discuss our prototype implementation of the proof system in Fig. 1 in K [9].
We choose K because it is a modular semantic language design framework, it is used for
teaching programming languages at several universities, and there are several languages
Vol. 15:2                         ALL-PATH REACHABILITY LOGIC                                  5:11




defined in it including C [13], PHP [18], Python, and Java. For brevity, we do not present
K here. We refer the reader to http://kframework.org for language definitions, a tutorial,
and our prototype. As discussed in Section 3, we simply view a K semantics as a set of
reachability rules of the form “l ∧ b ⇒∃ r”.
     The prototype is implemented in Java, and uses Z3 [19] for domain reasoning. It takes
an operational semantics and uses it to perform concrete or symbolic execution. At its core,
it performs narrowing of a conjunctive pattern with reachability rules between conjunctive
patterns, where a conjunctive pattern is a pattern of the form ∃X(π ∧ ψ), with X a set of
variables, π a basic pattern (program configurations with variables), and ψ a structureless
formula. Narrowing is necessary when a conjunctive pattern is too abstract to match the
left-hand side of any rule, but is unifiable with the left-hand sides of some rules. For instance,
consider the IMP code fragment “if (b) then x = 1; else x = 0;”. This code does not
match the left-hand sides of either of the two rules giving semantics to if (similar to cond1
and cond2 in Fig. 2), but it is unifiable with the left-hand sides of both rules. Intuitively, if
we use the rules of the semantics, taking steps of rewriting on a ground configuration yields
concrete execution, while taking steps of narrowing on a conjunctive pattern yields symbolic
execution. In our practical evaluation, we found that conjunctive patterns tend to suffice to
specify both the rules for operational semantics and program specifications.
     For each step of narrowing, the K engine uses unification modulo theories. In our
implementation, we distinguish a number of mathematical theories (e.g. booleans, integers,
sequences, sets, maps, etc) which the underlying SMT solver can reason about. Specifically,
when unifying a conjunctive pattern ∃X(π ∧ ψ) with the left-hand side of a rule ∃Xl (πl ∧ ψl )
(we assume X ∩ Xl = ∅), the K engine begins with the syntactic unification of the basic
patterns π and πl . Upon encountering corresponding subterms (π 0 in π and πl0 in πl ) which
are both terms of one of the theories above, it records an equality π 0 = πl0 rather than
decomposing the subterms further (if one is in a theory, and the other one is in a different
theory or is not in any theory, the unification fails). If this stage of unification is successful,
we end up with a conjunction ψu of constraints, some having a variable in one side and
some with both sides in one of the theories. Satisfiability of ∃X ∪ Xl (ψ ∧ ψu ∧ ψl ) is then
checked by the SMT solver. If it is satisfiable, then narrowing takes a step from ∃X(π ∧ ψ)
to ∃X ∪ Xl ∪ Xr (πr ∧ ψ ∧ ψu ∧ ψl ∧ ψr ), where ∃Xr (πr ∧ ψr ) is the right-hand side of the
rule. Intuitively, “collecting” the constraints ψu ∧ ψl ∧ ψr is similar to collecting the path
constraint in traditional symbolic execution (but is done in a language-generic manner). For
instance, in the if case above, narrowing with the two semantics rules results in collecting
the constraints b = true and b = false.
     The K engine accepts a set of user provided rules to prove together, which capture the
behavior of the code being verified. Typically, these rules specify the behavior of recursive
functions and while loops. For each rule, the K engine searches starting from the left-hand
side for formulae which imply the right-hand side, starting with S the semantics and C all
the rules it attempts to prove. By a derived proof rule called Set Circularity, this suffices to
show that each rule is valid. As an optimization, Axiom is given priority over Step (use
specifications rather than stepping into the code).
     Most work goes into implementing the Step proof rule, and in particular calculating
how ρ |= ∃c (ϕ[c/] ∧ ϕl [c/]) can be satisfied. This holds when ργ |= ϕ and ργ |= ϕl ,
which can be checked with unification modulo theories. To use Step in an automated way,
the K tool constructs ϕ0 for a given ϕ as a disjunction of ϕr ∧ ψu ∧ ψ ∧ ψl over each rule
ϕl ⇒∃ ϕr ∈ S and each way ψu of unifying ϕ with ϕl . As discussed in Section 4, in general
5:12                S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin                Vol. 15:2




this disjunction may not be finite, but it is sufficient for the examples that we considered.
The Consequence proof rule also requires unification modulo theories, to check validity
of the implication hypothesis |= ϕ1 → ϕ01 . The main difference from Step is that the free
variables of ϕ0 become universality quantified when sending the query to the SMT solver.
The implementation of the other proof rules is straight-forward.

                                          7. Soundness
Here we discuss the soundness of our proof system. Unlike the similar results for Hoare logics
and dynamic logics, which are separately proved for each language taking into account the
particularities of that language, we prove soundness once and for all languages.
    Soundness states that a syntactically derivable sequent holds semantically. Because of
the utmost importance of the result below, we have also mechanized its proof. Our complete
Coq formalization can be found at http://fsl.cs.illinois.edu/rl.
Theorem 7.1 (Soundness). If S ` ϕ ⇒∀ ϕ0 then S |= ϕ ⇒∀ ϕ0 .
Proof. Due to Circularity and Transitivity the sets A and C may not remain empty, so
we need to prove a more general statement (Lemma 7.2 below), including hypotheses making
some semantic assumptions about the rules in A and C.
      To express the different assumptions needed about the available rules in A and the
still-unavailable rules in C we define a more specific satisfaction relation. Let δ ∈ {+, ∗}
be a flag and let n ∈ N be a natural number. We define the new satisfaction relation
S |=δn ϕ ⇒∀ ϕ0 by restricting the paths in the definition of S |= ϕ ⇒∀ ϕ0 to length at most
n, and requiring that ϕ be reached after at least one step if δ = +. Formally, we define
S |=δn ϕ ⇒∀ ϕ0 to hold iff for any complete path τ = γ1 ...γk of length k ≤ n and for any ρ
such that (γ1 , ρ) |= ϕ, there exists i ∈ {1, ..., k} such that (γi , ρ) |= ϕ0 and also that this i is
not 1 (i.e. γ1 makes progress) if δ = +.
      Observe that S |= ϕ ⇒∀ ϕ0 iff S |=∗n ϕ ⇒∀ ϕ0 for all n ∈ N. The forward implication
holds because a complete path τ = γ1 ...γk of length k ≤ n is a complete path simpliciter.
The reverse implication holds because given any complete path τ = γ1 ...γk there are choices
(such as k) of n ∈ N with k ≤ n. Theorem 7.1 then follows from Lemma 7.2 by noting that
the hypotheses about A and C are vacuously true when those sets are empty.
                                                                     +
Lemma 7.2. If S, A `C ϕ ⇒∀ ϕ0 then for any n, S |=+      n A and S |=n−1 C imply that
S |=∗n ϕ ⇒∀ ϕ0 , and also that S |=+    ∀ 0
                                   n ϕ ⇒ ϕ if C is not empty.

Proof. To state the conclusion of the lemma more concisely we define flag ∆C to be ∗ if C
is an empty set and + otherwise. The conclusion is S |=∆           ∀ 0
                                                           n ϕ ⇒ ϕ . The proof proceeds
                                                              C
                                                        ∀   0
by induction on the proof tree showing S, A `C ϕ ⇒ ϕ (keeping induction hypotheses
universally quantified over n), using an inner induction over n in the Circularity case.
Circularity: The induction hypothesis states that for any m ∈ N.
                                    +           ∀ 0                ∀ 0
                 if S |=+                                     +
                        m A and S |=m−1 C ∪ {ϕ ⇒ ϕ } then S |=m ϕ ⇒ ϕ .                         (7.1)
                                                                               +
We will strengthen ∆C to + and prove that for any n ∈ N, if S |=+n A and S |=n−1 C then
S |=+      ∀ 0
    n ϕ ⇒ ϕ . Proceed by induction on n.
(1) if n = 0, the conclusion S |=+    ∀ 0
                                 0 ϕ ⇒ ϕ of the implication is vacuously true.
Vol. 15:2                           ALL-PATH REACHABILITY LOGIC                                   5:13




(2) for n > 0, we have an inner induction hypothesis that S |=+                         +
                                                                         n−1 A and S |=n−2 C together
                    +                                                             +
      imply S |=n−1 ϕ ⇒∀ ϕ0 , and must prove that S |=+        n A and S |=n−1 C together imply
      S |=+    ϕ ⇒ ∀ ϕ0 , Instantiating the inner hypothesis with the stronger assumptions about A
             n
      and C gives S |=+             ∀ 0                                             +
                          n−1 ϕ ⇒ ϕ . With other assumptions this gives S |=n−1 C ∪ {ϕ ⇒ ϕ }.
                                                                                                  ∀ 0

      Now we apply the outer induction hypothesis, Equation (7.1), with m = n to conclude
      S |=+        ∀ 0
             n ϕ⇒ ϕ.
      This was the only case that made essential use of the quantification over n in the
conclusion. For the remaining cases, we assume that n ∈ N is already fixed, and assumptions
                     +
S |=+  n A and |=n−1 C are given in addition to the assumptions and inductive hypotheses
coming from the specific proof rule. Inductive hypotheses with the same A and C as the
conclusion will be stated in the form S |=∆               ∀
                                                n ϕa ⇒ ϕb , already specialized to n and applied
                                                  C

to the semantic assumptions on A and C. Furthermore, the remaining cases all prove the
conclusion S |=+            ∀ 0
                    n ϕ ⇒ ϕ directly from the definition, so we also assume that a complete
path τ = γ1 , ..., γk with k ≤ n and a ρ with (γ1 , ρ) |= ϕ are fixed. This leaves the obligation
to find an i ∈ {1, ..., k} such that (γi , ρ) |= ϕ0 and that i > 1 if C is nonempty.
Transitivity: We have inductive hypotheses that S |=∆               n ϕ → ϕ2 , and for any m ∈ N,
                                                                      C
      +                         ∗         0
S |=m A ∪ C implies S |=m ϕ2 → ϕ . Applying the first inductive hypothesis to τ and ρ, we
receive an i such that (γi , ρ) |= ϕ2 . Now we make separate cases on whether i = 1.
• When i = 1, C must be empty, so our assumption S |=+               n A suffices to instantiate the
   second inductive hypothesis at m = n to obtain S |=n ϕ2 → ϕ0 . As (γ1 , ρ) |= ϕ2 we can
                                                                ∗

   apply this to τ and ρ to obtain a j such that (γj , ρ) |= ϕ0 , concluding this case.
• Otherwise, the suffix of τ beginning with γi has length strictly less than n, so it suffices to
   instantiate the second inductive hypothesis at m = n − 1. Our assumptions on C and A
   suffice to conclude S |=+                                 ∗            ∀ 0
                                 n−1 A ∪ C. We obtain S |=n−1 ϕ2 ⇒ ϕ . Applying this to ρ and
   the complete path γi , ..., γk yields j such that (γi+j−1 , ρ) |= ϕ0 . As i + j − 1 > 1, we can
   conclude this case with i + j − 1 whether or not C is empty.
Step: This rule has assumptions |= ϕ → ϕl ⇒∃ ϕr ∈ S ∃FreeVars(ϕl )ϕl , and for any ϕl ⇒∃
                                                  W

ϕr ∈ S |= ∃c (ϕ[c/] ∧ ϕl [c/]) ∧ ϕr → ϕ0 . By the first assumption γ1 is not stuck, so
complete path τ has a second entry γ2 . By the definition of a path, γ1 ⇒TS γ2 . By the
definition of ⇒TS , there exists ϕl ⇒∃ ϕr ∈ S and valuation ρ0 such that (γ1 , ρ0 ) |= ϕl and
(γ2 , ρ0 ) |= ϕr . Let X = FreeVars(ϕ, ϕ0 ) and Y = FreeVars(ϕl , ϕr ). We assume without
loss of generality that X ∩ Y = ∅. Fix any ρ00 which agrees with ρ on X and with ρ0 on
Y . With this choice (γ1 , ρ00 ) |= ϕ, (γ1 , ρ00 ) |= ϕl , and (γ2 , ρ00 ) |= ϕr . By the definition of
satisfaction and the FOL translation, then also (γ2 , ρ00 ) |= ∃c.(ϕ[c/] ∧ ϕl [c/]) and finally
(γ2 , ρ00 ) |= ∃c.(ϕ[c/] ∧ ϕl [c/]) ∧ ϕr . By the second assumption this implies (γ2 , ρ00 ) |= ϕ0 .
As ρ00 agrees with ρ on X, (γ2 , ρ) |= ϕ0 (and 2 > 1), so taking i = 2 concludes this case.
Reflexivity: This rule requires C be empty, and ϕ = ϕ0 , so i = 1 suffices by (γ1 , ρ) |= ϕ.
Axiom: This rule has assumption ϕ ⇒∀ ϕ0 ∈ A. By the assumption on A, S |=+                 n ϕ⇒ ϕ.
                                                                                                   ∀ 0
                                                                0
Applying this to τ and ρ gives an i > 1 with (γi , ρ) |= ϕ , concluding this case.
Consequence: We have inductive hypothesis that S |=∆                           ∀ 0
                                                                     n ϕ1 ⇒ ϕ1 , and assumptions
                                                                       C
                          0       0
|= ϕ → ϕ1 and |= ϕ1 → ϕ . By the first implication (γ1 , ρ) |= ϕ1 as well, so we can apply
the inductive hypothesis with τ and ρ to obtain some i such that (γi , ρ) |= ϕ01 and i > 1 if C
is nonempty. By the second implication, (γi , ρ) |= ϕ0 as well, so this i concludes this case.
Case Analysis: This rule requires ϕ have the form ϕ1 ∨ ϕ2 , and we have inductive
hypotheses S |=∆               ∀ 0           ∆C      ∀ 0
                     n ϕ1 ⇒ ϕ and S |=n ϕ2 ⇒ ϕ . Because (γ1 , ρ) |= ϕ, either (γ1 , ρ) |= ϕ1
                      C
5:14               S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin             Vol. 15:2




or (γ1 , ρ) |= ϕ2 . In either case we can use the respective inductive hypotheses with τ and ρ
to obtain an i such that (γi , ρ) |= ϕ0 and i > 1 if C is nonempty, concluding this case.
Abstraction: This rule requires ϕ have the form ∃Xϕ1 with X 6∈ FreeVars(ϕ0 ), and we
have the inductive hypothesis S |=∆               ∀ 0                                         0
                                       n ϕ1 ⇒ ϕ . Because (γ1 , ρ) |= ∃Xϕ1 there exists a ρ
                                         C
                                                         0
which agrees with ρ except on X such that (γ1 , ρ ) |= ϕ1 . Using the inductive hypothesis
with τ and this ρ0 gives an i such that (γi , ρ0 ) |= ϕ0 , and i > 1 if C is nonempty. As
X 6∈ FreeVars(ϕ0 ), then also (γi , ρ) |= ϕ0 , so this i concludes this case.


                                8. Relative Completeness
Here we show relative completeness: any valid all-path reachability property of any program
in any language with an operational semantics given as a reachability system S is derivable
with the proof system in Fig. 1 from S. As with Hoare and dynamic logics, “relative” means
we assume an oracle capable of establishing validity in the first-order theory of the state,
which here is the configuration model T . Unlike the similar results for Hoare logics, which are
separately proved for each language taking into account the particularities of that language,
we prove relative completeness once and for all languages. An immediate consequence of
relative completeness is that Circularity is sufficient to derive any repetitive behavior
occurring in any program written in any language, and that Step is also sufficient to derive
any non-deterministic behavior!
    We establish the relative completeness under the following assumptions:
            Framework:
            The semantics reachability system S is
            — finite;
            The configuration signature Σ has
            — a sort N;
            — constant symbols 0 and 1 of N;
            — binary operation symbols + and × on N;
            — an operation symbol α : Cfg → N.
            The configuration model T interprets
            — N as the natural numbers;
            — constant and operation symbols on N as corresponding operations;
            — α : Cfg → N as an injective function.
The assumption that S is finite ensures Step has a finite number of prerequisites. The
assumption that the model T includes natural numbers with addition and multiplication is a
standard assumption (also made by Hoare and dynamic logic completeness results) which
allows the definition of Gödel’s β predicate. The assumption that the model T includes some
injective function α : TCfg → N (that is, the set of configurations TCfg is countable) allows the
encoding of a sequence of configurations into a sequence of natural numbers. We expect the
operational semantics of any reasonable language to satisfy these conditions. Formally, we
have the following
Theorem 8.1 (Relative Completeness). For any semantics S satisfying the assumptions
above, if S |= ϕ ⇒∀ ϕ0 then S ` ϕ ⇒∀ ϕ0 .
    We present an informal proof sketch before going into the formal details, Our proof relies
on the fact that pattern reasoning in first-order matching logic reduces to FOL reasoning in
Vol. 15:2                             ALL-PATH REACHABILITY LOGIC                               5:15



                      _
step(c, c0 ) ≡                   ∃FreeVars(µ) (ϕl [c/] ∧ ϕr [c0 /])
                 µ≡ϕl ⇒∃ ϕr ∈S                                                                                !
                                            ^                                                  _
coreach(ϕ) ≡ ∀n∀c0 ...cn  = c0 →               step(ci , ci+1 ) → ¬∃cn+1 step(cn , cn+1 ) →       ϕ[ci /]
                                           0≤i<n                                           0≤i≤n


      Figure 5: FOL encoding of one step transition relation and all-path reachability.

the model T . A key component of the proof is defining the coreach(ϕ) predicate in plain
FOL. This predicate states that every complete ⇒TS -path τ starting at c includes some
configuration satisfying ϕ. We express coreach(ϕ) using the auxiliary predicate step(c, c0 )
that encodes the one step transition relation (⇒TS ). Fig. 5 shows both definitions. As it is,
coreach(ϕ) is not a proper FOL formula, as it quantifies over a sequence of configurations.
This is addressed using the injective function α to encode universal quantification over a
sequence of configurations into universal quantification over a sequence of integers, which
is in turn encoded into quantification over two integer variables using Gödel’s β predicate
(encoding shown in Fig. 6).
      Next, using the definition above we encode the semantic validity of an all-path reachability
rule as FOL validity: S |= ϕ ⇒∀ ϕ0 iff |= ϕ → coreach(ϕ0 ). Therefore, the theorem follows by
Consequence from the sequent S ` coreach(ϕ0 ) ⇒∀ ϕ0 . We derive this sequent by using
Circularity to add the rule to the set of circularities, then by using Step to derive one
⇒TS -step, and then by using Transitivity and Axiom with the rule itself to derive the
remaining ⇒TS -steps (circularities can be used after Transitivity). The formal derivation
uses all eight proof rules.
      Also recall that, as discussed in Section 2, matching logic is a methodological fragment
of the FOL theory of the model T . For technical convenience, in this section we work with
the FOL translations ϕ instead of the matching logic formulae ϕ. We mention that in all
the formulae used in this section,  only occurs in the context  = t, thus we stay inside
the methodological fragment. For the duration of the proof, we let c, c0 , c0 , ..., cn be distinct
variables of sort Cfg which do not appear free in the rules in S). We also let γ, γ 0 , γ0 , ..., γn
range over (not necessarily distinct) configurations in the model T , that is, over elements in
TCfg , and let ρ, ρ0 range over valuations Var → T .

8.1. Encoding Transition System Operations in FOL. Fig. 5 shows the definition
of the one step transition relation (⇒TS ) and of the configurations that reach ϕ on all
and complete paths. The former is a (proper) FOL formula, while the later is not, as it
quantifies over a sequence of configuration. In Section 8.2 we use Gödel’s β predicate to
define coreach(ϕ), a FOL formula equivalent to coreach(ϕ).
     First, we establish the following general purpose lemma
Lemma 8.2. (ρ(c), ρ) |= ϕ iff ρ |= ϕ [c/].
Proof. With the notation in Definition 2.2, (ρ(c), ρ) |= ϕ iff ρρ(c) |= ϕ . Notice that if a
valuation agrees on two variables, then it satisfies a formula iff it satisfies the formula obtained
by substituting one of the two variables for the other. In particular, since ρρ(c) () = ρρ(c) (c),
it follows that ρρ(c) |= ϕ iff ρρ(c) |= ϕ [c/]. We notice that  does not occur in ϕ [c/],
thus ρρ(c) |= ϕ [c/] iff ρ |= ϕ [c/], and we are done.
5:16                 S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin                       Vol. 15:2




    The following lemma states that step(c, c0 ) actually has the semantic properties its name
suggests.
Lemma 8.3. ρ |= step(c, c0 ) iff ρ(c) ⇒TS ρ(c0 ).
Proof. Assume ρ |= step(c, c0 ). Then, by the definition of step(c, c0 ), there exists some
rule µ ≡ ϕl ⇒∃ ϕr ∈ S such that ρ |= ∃FreeVars(µ) (ϕl [c/] ∧ ϕr [c0 /]). Further, since c
and c0 do not occur in µ, there exists some ρ0 which agrees with ρ on c and c0 such that
ρ0 |= ϕl [c/] and ρ0 |= ϕr [c0 /]. By Lemma 8.2, ρ0 |= ϕl [c/] iff (ρ0 (c), ρ0 ) |= ϕl and
ρ0 |= ϕr [c0 /] iff (ρ0 (c0 ), ρ0 ) |= ϕr , so (ρ0 (c), ρ0 ) |= ϕl and (ρ0 (c0 ), ρ0 ) |= ϕr . Since ρ and ρ0
agree on c and c0 , it follows that (ρ(c), ρ0 ) |= ϕl and (ρ(c0 ), ρ0 ) |= ϕr . By Definition 3.1, we
conclude ρ(c) ⇒TS ρ(c0 ).
      Conversely, assume ρ(c) ⇒TS ρ(c0 ). Then, by Definition 3.1, there exist some rule
µ ≡ ϕl ⇒∃ ϕr ∈ S and some ρ0 for which (ρ(c), ρ0 ) |= ϕl and (ρ(c0 ), ρ0 ) |= ϕr . Further,
since c and c0 do not occur in µ, we can choose ρ0 to agree with ρ on c and c0 . Hence,
(ρ0 (c), ρ0 ) |= ϕl and (ρ0 (c0 ), ρ0 ) |= ϕr . By Lemma 8.2, (ρ0 (c), ρ0 ) |= ϕl iff ρ0 |= ϕl [c/] and
(ρ0 (c0 ), ρ0 ) |= ϕr iff ρ0 |= ϕr [c0 /], so ρ0 |= ϕl [c/] and ρ0 |= ϕr [c0 /]. Since the free variables
occurring in ϕl [c/] ∧ ϕr [c0 /] are FreeVars(µ) ∪ {c, c0 } and ρ and ρ0 agree on c and c0 ,
it follows that ρ |= ∃FreeVars(µ) (ϕl [c/] ∧ ϕr [c0 /]). By the definition of step(c, c0 ), we
conclude ρ |= step(c, c0 ).
   The following lemma introduces a formula encoding a complete path of fixed length.
                    V
Lemma 8.4. ρ |=        step(ci , ci+1 )∧ 6 ∃cn+1 step(cn , cn+1 ) iff ρ(c0 ), ..., ρ(cn+1 ) is a
                        0≤i<n
complete ⇒TS -path.
Proof. By Lemma 8.3, we have that ρ(ci ) ⇒TS ρ(ci+1 ) iff ρ0 |= step(ci , ci+1 ), for each
0 ≤ i < n. Further, ρ(c0 ), ..., ρ(cn+1 ) is complete, iff there does not exist γ such that
ρ(cn ) ⇒T
       VS γ. Again, by Lemma 8.3, that is iff ρ |=6 ∃cn+1 step(cn , cn+1 ). We conclude       T
                                                                                                  that
ρ |=      step(ci , ci+1 )∧ 6 ∃cn+1 step(cn , cn+1 ) iff ρ(c0 ), ..., ρ(cn+1 ) is a complete ⇒S -path,
       0≤i<n
and we are done.
   The following lemma states that coreach(ϕ) actually has the semantic properties its
name suggests.
Lemma 8.5. (γ, ρ) |= coreach(ϕ) iff for all complete ⇒TS -paths τ starting with γ it is the
case that (γ 0 , ρ) |= ϕ for some γ 0 ∈ τ .
Proof. First we prove the direct implication. Assume (γ, ρ) |= coreach(ϕ), and let τ ≡
γ0 , ..., γn be a complete ⇒TS -path starting with γ. Then let ρ0 agree with ρ on FreeVars(ϕ)
such that ρ0 (n) = n and ρ0 (ci ) = γi for each 0 ≤ i ≤ n. According to the definition of
coreach(ϕ), we have that
                               ^                                               _
          (γ, ρ0 ) |=  = c0 ∧    step(ci , ci+1 )∧ 6 ∃cn+1 step(cn , cn+1 ) →   ϕ[ci /]
                              0≤i<n                                                    0≤i≤n

Since, γ = γ0 and ρ0 (c0 ) = γ0 , it follows that ρ0 |=  = c0 . Further, by Lemma 8.4, since
ρ0 (c0 ), ..., ρ0 (cn ) is a complete ⇒TS -path, it must be the case that
                                   ^
                          ρ0 |=           step(ci , ci+1 )∧ 6 ∃cn+1 step(cn , cn+1 )
                                  0≤i<n
Vol. 15:2                               ALL-PATH REACHABILITY LOGIC                                       5:17




 coreach(ϕ) ≡        ∀n∀a∀b (∃c (β(a, b, 0, α(c)) ∧  = c)
                       ∧∀i (0 ≤ i ∧ i < n → ∃c∃c0 (β(a, b, i, α(c)) ∧ β(a, b, i + 1, α(c0 )) ∧ step(c, c0 )))
                       ∧∃c (β(a, b, n, α(c))∧ 6 ∃c0 step(c, c0 ))
                       → ∃i (0 ≤ i ∧ i ≤ n ∧ ∃c (β(a, b, i, α(c)) ∧ ϕ[c/])))

                                Figure 6: FOL definition of coreach(ϕ)

Thus, as  does not occur in any ϕ[ci /], we conclude that ρ0 |=
                                                                                      W
                                                                                  ϕ[ci /], that is,
                                                                           0≤i≤n
ρ0 |= ϕ[ci /] for some 0 ≤ i ≤ n. By Lemma 8.2, ρ0 |= ϕ[ci /] iff (γi , ρ0 ) |= ϕ. Since ρ agrees
with ρ0 on FreeVars(ϕ), we conclude that (γi , ρ) |= ϕ.
      Conversely, assume that if τ is a finite and complete ⇒TS -path starting with γ. Then
(γ , ρ) |= ϕ for some γ 0 ∈ τ . Let ρ0 agree with ρ on FreeVars(ϕ). Then we prove that
  0
                                ^                                                         _
        (γ, ρ0 ) |=  = c0 ∧           step(ci , ci+1 )∧ 6 ∃cn+1 step(cn , cn+1 ) →           ϕ[ci /]
                               0≤i<n                                                  0≤i≤n

Specifically, assume (γ, ρ0 ) |=  = c0 ∧
                                                   V
                                                          step(ci , ci+1 )∧ 6 ∃cn+1 step(cn , cn+1 ). As 
                                                  0≤i<n
does not occur in any cci ci+1 , by Lemma 8.4, it follows that ρ0 (c0 ), ..., ρ0 (cn ) is a complete
⇒TS -path. Further, (γ, ρ0 ) |=  = c, implies that ρ0 (c0 ), ..., ρ0 (cn ) starts with γ. Thus, there
exists some 0 ≤ i ≤ n such that (ρ0 (ci ), ρ) |= ϕ, or equivalently, since ρ and ρ0 agree on
FreeVars(ϕ), such that (ρ0 (ci ), ρ0 ) |=Wϕ. By Lemma 8.2, (ρ0 (ci ), ρ0 ) |= ϕ iff ρ0 |= ϕ[ci /].
Therefore, we have that (γ, ρ0 ) |=         ϕ[ci /]. Finally, since ρ0 is an arbitrary valuation
                                          0≤i≤n
which agrees with ρ on FreeVars(ϕ), by the definition of coreach(ϕ) we can conclude that
(γ, ρ) |= coreach(ϕ), and we are done.
     The following lemma establishes a useful property of coreach(ϕ).
Lemma 8.6.
            |= coreach(ϕ) → ϕ ∨ (∃c0 step(c, c0 ) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]))
Proof. We prove that if (γ, ρ) |= coreach(ϕ) then
                (γ, ρ) |= ϕ ∨ (∃c0 step(c, c0 ) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]))
By Lemma 8.5, we have that for all complete ⇒TS -paths τ starting with γ it is the case that
(γ 00 , ρ) |= ϕ for some γ 00 ∈ τ . We distinguish two cases
• (γ, ρ) |= ϕ. We are trivially done.
• (γ, ρ) 6|= ϕ. Then γ must have ⇒TS -successors. Indeed, assume the contrary. Then τ ≡ γ
    is a complete ⇒TS -path. It follows that (γ, ρ) |= ϕ, which is a contradiction. Thus, there
    exists some γ 0 such that γ ⇒TS γ 0 . By Lemma 8.3, that is iff ρ |= ∃c0 step(c, c0 ). Further,
    let γ 0 be a ⇒TS -successor of γ and τ 0 a complete ⇒TS -path starting with γ 0 . Then, γτ is a
    complete ⇒TS -path starting with γ. Thus, there exists some γ 00 ∈ γτ 0 such that (γ 00 , ρ) |= ϕ.
    Since (γ, ρ) 6|= ϕ, it follows that γ 00 ∈ τ 0 . Notice that γ 0 is an arbitrary configuration and
    τ 0 an arbitrary ⇒TS -path, therefore by Lemma 8.5 and Lemma 8.2, we can conclude that
    ρ |= ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /])).
5:18                  S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin               Vol. 15:2




8.2. Formula Gödelization. Fig. 6 defines coreach(ϕ), the FOL equivalent of coreach(ϕ)
using Gödel’s β predicate. Formally, we have the following
Lemma 8.7. |= coreach(ϕ) ↔ coreach(ϕ).
Proof. Let us choose some arbitrary but fixed values for n, a and b, and let ρ0 such that
ρ and ρ0 agree on Var \ {n, a, b} and ρ0 (n) = n and ρ0 (a) = a and ρ0 (b) = b. According to
the definition of the β predicate, there exists a unique integer sequence j0 , ..., jn such that
β(a, b, i, ji ) holds for each 0 ≤ i ≤ n. Since α is injective, we distinguish two cases
• there exists some 0 ≤ i ≤ n such that there is not any γi with α(γi ) = ji
• there exists a unique sequence γ0 , ..., γn such that α(γi ) = ji for each 0 ≤ i ≤ n.
In the former case, if i = n we get that ρ0 6|= ∃c (β(a, b, n, α(c))∧ 6 ∃c0 step(c, c0 ) while if
0 ≤ i < n we get that ρ0 6|= ∃c∃c0 (β(a, b, i, α(c)) ∧ β(a, b, i + 1, α(c0 )) ∧ step(c, c0 )) as in
both cases we can not pick a value for c. Thus, (γ, ρ0 ) does not satisfy left-hand-side of the
implication in coreach(ϕ), and we conclude that (γ, ρ0 ) satisfies the implication.
    In the later case, we have that there is a unique way of instantiating the existentially
quantified variables c and c0 in each sub-formula in which they appear, as they are always
arguments of the β predicate. Thus, (γ, ρ0 ) |= ∃c (β(a, b, 0, α(c)) ∧  = c) iff γ = γ0 . By
Lemma 8.4, we have that
       ρ0 |= ∀i (0 ≤ i ∧ i < n → ∃c∃c0 (β(a, b, i, α(c)) ∧ β(a, b, i + 1, α(c0 )) ∧ step(c, c0 )))
             ∧∃c (β(a, b, n, α(c))∧ 6 ∃c0 step(c, c0 ))
iff γ0 ...γn is a complete ⇒TS -path. Finally, by Lemma 8.2
                       ρ0 |= ∃i (0 ≤ i ∧ i ≤ n ∧ ∃c (β(a, b, i, α(c)) ∧ ϕ[c/]))
iff (γi , ρ0 ) |= ϕ for some 0 ≤ i ≤ n.
     We conclude that (γ, ρ0 ) satisfies the implication in coreach(ϕ) iff
• there is no sequence γ0 , ..., γn such that α(γi ) = ji for each 0 ≤ i ≤ n
• the unique sequence γ0 , ..., γn such that α(γi ) = ji for each 0 ≤ i ≤ n is either not starting
   at γ, not a complete ⇒TS -path or contains some γ 0 such that (γ 0 , ρ) |= ϕ, as ρ and ρ0 agree
   on Var \ {n, a, b}.
     According to the property of β, for each sequence j0 , ..., jn there exist some values for
a and b. Since n, a and b are chosen arbitrary, we conclude that (γ, ρ) |= coreach(ϕ) iff for
all complete ⇒TS -paths τ starting at γ, there exists some γ 0 ∈ τ such that (γ 0 , ρ) |= ϕ. By
Lemma 8.5, we have that the above iff (γ, ρ) |= coreach(ϕ), and we are done.


8.3. Encoding Semantic Validity in FOL. Now we can use the coreach predicate to
encode the semantic validity of a rule ϕ ⇒∀ ϕ0 in FOL. Formally
Lemma 8.8. If S |= ϕ ⇒∀ ϕ0 then |= ϕ → coreach(ϕ0 ).
Proof. Follows from the definition of semantic validity of ϕ ⇒∀ ϕ0 and Lemma 8.5.
Vol. 15:2                                  ALL-PATH REACHABILITY LOGIC                              5:19




8.4. Relative Completeness. A matching logic formula ψ is patternless iff  does not
occur in ψ. Then we have the following lemma stating that we can derive one step on all
paths
Lemma 8.9. S, A `C  = c ∧ ∃c0 step(c, c0 ) ∧ ψ ⇒∀ ∃c0 ( = c0 ∧ step(c, c0 )) ∧ ψ where
ψ is a patternless formula.
Proof. We derive the rule by applying the Step proof rule with the following prerequisites
                                                  _
               |=  = c ∧ ∃c0 step(c, c0 ) ∧ ψ →         ∃FreeVars(ϕl ) ϕl
                                                               ϕl ⇒∃ ϕr ∈S

and for each ϕl ⇒∃ ϕr ∈ S (since  does not occur in ψ)
    |= ∃c00 (c00 = c ∧ ∃c0 step(c, c0 ) ∧ ϕl [c00 /]) ∧ ϕr ∧ ψ → ∃c0 ( = c0 ∧ step(c, c0 )) ∧ ψ
For the first prerequisite, we have the following (using the definition of step(c, c0 ))
                      = c ∧ ∃c0 step(c, c0 ) ∧ ψ
                   →  = c ∧ ∃c0 step(c,
                                      _c )
                                          0

                   ↔  = c ∧ ∃c0               ∃FreeVars(µ) (ϕl [c/] ∧ ϕr [c0 /])
                                          µ≡ϕl ⇒∃
                                               _ϕr ∈S
                                      0
                   →  = c ∧ ∃c                           ∃FreeVars(µ) ϕl [c/]
                                          µ≡ϕl ⇒∃ ϕr ∈S
                                           _
                   → =c∧                           ∃FreeVars(ϕl ) ϕl [c/]
                            _       µ≡ϕl ⇒∃ ϕr ∈S
                   →                      ∃FreeVars(ϕl ) ϕl
                       µ≡ϕl ⇒∃ ϕr ∈S

For the second prerequisite, let ϕl ⇒∃ ϕr ∈ S. Then we have that
                 ∃c00 (c00 = c ∧ ∃c0 step(c, c0 ) ∧ ϕl [c00 /]) ∧ ϕr ∧ ψ
               → ϕl [c/] ∧ ϕr ∧ ψ
               → ∃c0 ( = c0 ∧ ϕl [c/]          0
                                     _ ∧ ϕr [c /]) ∧ ψ
               → ∃c0 ( = c0 ∧               (ϕl [c/] ∧ ϕr [c0 /])) ∧ ψ
                                      µ≡ϕl ⇒ ∃
                                           _ϕr ∈S
                       0        0
               → ∃c ( = c ∧                          ∃FreeVars(µ) (ϕl [c/] ∧ ϕr [c0 /]) ∧ ψ
                                µ≡ϕl ⇒∃ ϕr ∈S
               →    ∃c ( = c ∧ step(c, c0 )) ∧ ψ
                      0      0

and we are done.
     The following three lemmas show that we can derive a rule stating that all the configu-
rations reaching ϕ in the transition system actually reach ϕ.
Lemma 8.10. If
            S, A `  = c ∧ ∃c0 step(c, c0 ) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]) ⇒∀ ϕ
then S, A ` coreach(ϕ) ⇒∀ ϕ.
Proof. By Lemma 8.6
            |= coreach(ϕ) ↔ ϕ ∨ (∃c0 step(c, c0 ) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]))
5:20                S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin              Vol. 15:2




Thus, by Consequence and Case Analysis, it suffices to derive
          S, A ` ϕ ⇒∀ ϕ
          S, A `  = c ∧ ∃c0 step(c, c0 ) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]) ⇒∀ ϕ
The first sequent follows by Reflexivity. The second sequent is part of the hypothesis,
and we are done.
Lemma 8.11.
          S, A `  = c ∧ ∃c0 step(c, c0 ) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]) ⇒∀ ϕ
Proof. Let µ be the rule we want to derive, namely
               = c ∧ ∃c0 step(c, c0 ) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]) ⇒∀ ϕ
Then S, A ` µ follows by Circularity from S, A `{µ} µ. Hence, by Transitivity, it
suffices to derive the two sequents below
        S, A `{µ}  = c ∧ ∃c0 step(c, c0 ) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]) ⇒∀ ϕ0
        S, A ∪ {µ} ` ϕ0 ⇒∀ ϕ
where ϕ0 ≡ ∃c0 ( = c0 ∧ step(c, c0 )) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]). The first sequent
follows by Lemma 8.9 with ψ ≡ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]). For the second sequent,
by Abstraction with {c0 } and Consequence with
          |=  = c0 ∧ step(c, c0 ) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]) → coreach(ϕ)
it suffices to derive S, A ∪ {µ} ` coreach(ϕ) ⇒∀ ϕ. Then, by Lemma 8.10, we are left to
derive
       S, A ∪ {µ} `  = c ∧ ∃c0 step(c, c0 ) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)[c0 /]) ⇒∀ ϕ
that is, S, A ∪ {µ} ` µ, which trivially follows by Axiom and we are done.
Lemma 8.12. S, A ` coreach(ϕ) ⇒∀ ϕ.
Proof. By Lemma 8.10, it suffices to derive
             S, A `  = c ∧ ∃c0 step(c, c0 ) ∧ ∀c0 (step(c, c0 ) → coreach(ϕ)) ⇒∀ ϕ
which follows by Lemma 8.11.
    Finally, we can establish the main result. Assume S |= ϕ ⇒∀ ϕ0 . By Lemma 8.8, we
have that |= ϕ → coreach(ϕ0 ). Further, by Lemma 8.12, we have that S ` coreach(ϕ0 ) ⇒∀ ϕ0 .
Then, by Consequence, it follows that S ` ϕ ⇒∀ ϕ0 .

                                       9. Related Work
Using Hoare logic [20] to prove concurrent programs correct dates back to Owicki and
Gries [21]. In the rely-guarantee method proposed by Jones [22] each thread relies on some
properties being satisfied by the other threads, and in its turn, offers some guarantees on
which the other threads can rely. O’Hearn [23] advances a Separation Hypothesis in the
context of separation logic [24] to achieve compositionality: the state can be partitioned
into separate portions for each process and relevant resources, respectively, satisfying certain
invariants. More recent research focuses on improvements over both of the above methods
and even combinations of them (e.g., [25–28]).
Vol. 15:2                        ALL-PATH REACHABILITY LOGIC                               5:21




     The satisfaction of all-path-reachability rules can also be understood intuitively in the
context of temporal logics. Matching logic formulae can be thought of as state formulae, and
reachability rules as temporal formulae. Assuming CTL∗ on finite traces, the semantics rule
ϕ ⇒∃ ϕ0 can be expressed as ϕ → E          ϕ0 , while an all-path reachability rule ϕ ⇒∀ ϕ0 can
be expressed as ϕ → A3ϕ . However, unlike in CTL∗ , the ϕ and ϕ0 formulae of reachability
                            0

rules ϕ ⇒∃ ϕ0 or ϕ ⇒∀ ϕ0 share their free variables. Thus, existing proof systems for temporal
logics (e.g., the CTL∗ one by Pnueli and Kesten [29]) are not directly comparable with our
approach. In general, CTL∗ formulae only have atomic predicates, while in our approach we
consider only a specific temporal structure (ϕ → A3ϕ0 ), but the matching logic formulae ϕ
and ϕ0 can express more complex state properties.
     This approach has been extended to handle safety properties of distributed system,
specified as rewrite theories [30]. Specifically, it can verify that ϕ is an invariant, or a
co-invariant, of a non-terminating distributed system by checking that ϕ holds after each
application of the Step proof rule. The soundness of the approach is proved by transforming
the underlying transition system from non-terminating to terminating by adding a transition
from each state to a newly-introduced end state (where ϕ does not hold).
     Bae et al. [31], Rocha and Meseguer [32], and Rocha et al. [33] use narrowing to perform
symbolic reachability analysis in a transition system associated to a unconditional rewrite
theory for the purposes of verification. There are two main differences between their work
and ours. First, they express state predicates in equational theories. Matching logic is more
general, being first-order logic over a model of configurations T . Consequently, the Step
proof rule takes these issues into account when considering the successors of a state. Second,
they use rewrite systems for symbolic model checking. Our work is complementary, in the
sense that we use the operational semantics for program verification, and check properties
more similar to those in Hoare logic.
     Dynamic logic [34] adds modal operators to FOL to embed program fragments within
specifications. For example, ψ → [s]ψ 0 means “after executing s in a state satisfying ψ, a
state may be reached which satisfies ψ 0 ”. KeY [35] offers automatic verification for Java
based on dynamic logic. Dynamic logic has been extended to support reasoning about cyber-
physical systems, where the transitions may have a continuous or probabilistic component [36].
Matching logic also combines programs and specifications for static properties, but dynamic
properties are expressed in reachability logic which has a language-independent proof system
that works with any operational semantics, while dynamic logic still requires language-specific
proof rules (e.g., invariant rules for loops).

Language-independent proof systems. A first proof system is introduced in [6], while [5]
presents a mechanical translation from Hoare logic proof derivations for IMP into derivations
in the proof system. The Circularity proof rule is introduced in [4]. Finally, [7] supports
operational semantics given with conditional rules, like small-step and big-step. All these
previous results can only be applied to deterministic programs. The coinductive nature of
this proof system was clarified in [37], which presents a coinduction principle that captures
the essence of the Circularity rule, and which is sufficient for program verification when
used within a system such as ZFC or Coq that already supports basic logical reasoning and
working with collections of configurations.
5:22                 S, tefănescu, Ciobâcă, Mereuta, Moore, Ros, u, and Florin                       Vol. 15:2




                              10. Conclusion and Future Work
This paper introduces a sound and (relatively) complete language-independent proof sys-
tem which derives program properties holding along all execution paths (capturing partial
correctness for non-deterministic programs), directly from an operational semantics. The
proof system separates reasoning about deterministic language features (via the operational
semantics) from reasoning about non-determinism (via the proof system). Thus, all we need
in order to verify programs in a language is an operational semantics for the respective
language.
     We believe that existing techniques such as rely-guarantee and concurrent separation
logic could be used in conjunction with our proof system to achieve semantically grounded
and compositional verification.
     Our approach handles operational semantics given with unconditional rules, like in the
K framework, PLT-Redex, and CHAM, but it cannot handle operational semantics given
with conditional rules, like big-step and small-step (rules with premises). Extending the
presented results to work with conditional rules would boil down to extending the Step
proof rule, which derives the fact that ϕ reaches ϕ0 in one step along all execution paths.
Such an extended Step would have as prerequisites whether the left-hand side of a semantics
rule matches (like the existing Step) and additionally whether its premises hold. The second
part would require an encoding of reachability in first-order logic, which is non-trivial and
most likely would result in a first-order logic over a richer model than T . The difficulty arises
from the fact that Step must ensure all successors of ϕ are in ϕ0 . Thus, this extension is left
as future work.

Acknowledgements. We would like to thank the anonymous reviewers and the FSL members
for their valuable feedback on an early version of this paper. The work presented in this paper
was supported in part by the Boeing grant on "Formal Analysis Tools for Cyber Security"
2014-2015, the NSF grant CCF-1218605, the NSA grant H98230-10-C-0294, the DARPA
HACMS program as SRI subcontract 19-000222, the Rockwell Collins contract 4504813093,
and the (Romanian) SMIS-CSNR 602-12516 contract no. 161/15.06.2010.

                                              References
 [1] Nipkow, T.: Winskel is (almost) right: Towards a mechanized semantics textbook. Formal Aspects of
     Computing 10 (1998) 171–186
 [2] Jacobs, B.: Weakest pre-condition reasoning for Java programs with JML annotations. J. Logic and
     Algebraic Programming 58(1-2) (2004) 61–88
 [3] Appel, A.W.: Verified software toolchain. In: ESOP. Volume 6602 of LNCS. (2011) 1–17
 [4] Ros, u, G., S, tefănescu, A.: Checking reachability using matching logic. In: OOPSLA, ACM (2012)
     555–574
 [5] Ros, u, G., S, tefănescu, A.: From Hoare logic to matching logic reachability. In: FM. Volume 7436 of
     LNCS. (2012) 387–402
 [6] Ros, u, G., S, tefănescu, A.: Towards a unified theory of operational and axiomatic semantics. In: ICALP.
     Volume 7392 of LNCS. (2012) 351–363
 [7] Roşu, G., Ştefănescu, A., Ciobâcă, S., Moore, B.M.: One-path reachability logic. In: LICS, IEEE (2013)
     358–367
 [8] Ros, u, G., Ellison, C., Schulte, W.: Matching logic: An alternative to Hoare/Floyd logic. In: AMAST.
     Volume 6486 of LNCS. (2010) 142–162
 [9] Ros, u, G., S, erbănut, ă, T.F.: An overview of the K semantic framework. J. Logic and Algebraic Program-
     ming 79(6) (2010) 397–434
Vol. 15:2                              ALL-PATH REACHABILITY LOGIC                                                                    5:23




[10] Ştefănescu, A., Ciobâcă, S., Mereuţă, R., Moore, B.M., Şerbănuţă, T.F., Roşu, G.: All-path reachability
     logic. In: RTA. Volume 8560 of LNCS. (July 2014) 425–440
[11] Roşu, G.: Matching logic. Logical Methods in Computer Science 13(4) (December 2017) 1–61
[12] Roşu, G.: Matching logic — extended abstract. In: RTA. Volume 36 of Leibniz International Proceedings
     in Informatics (LIPIcs)., Schloss Dagstuhl–Leibniz-Zentrum fuer Informatik (2015) 5–21
[13] Ellison, C., Ros, u, G.: An executable formal semantics of C with applications. In: POPL, ACM (2012)
     533–544
[14] Hathhorn, C., Ellison, C., Rosu, G.: Defining the undefinedness of C. In: PLDI, ACM (2015) 336–345
[15] Felleisen, M., Findler, R.B., Flatt, M.: Semantics Engineering with PLT Redex. MIT (2009)
[16] Berry, G., Boudol, G.: The chemical abstract machine. Theoretical Computer Science 96(1) (1992)
     217–248
[17] Matthews, J., Findler, R.B.: An operational semantics for Scheme. JFP 18(1) (2008) 47–86
[18] Filaretti, D., Maffeis, S.: An executable formal semantics of PHP. In: ECOOP. Volume 8586 of LNCS.
     (2014) 567–592
[19] de Moura, L.M., Bjørner, N.: Z3: An efficient SMT solver. In: TACAS. Volume 4963 of LNCS. (2008)
     337–340
[20] Hoare, C.A.R.: An axiomatic basis for computer programming. Communications of the ACM 12(10)
     (1969) 576–580
[21] Owicki, S.S., Gries, D.: Verifying properties of parallel programs: An axiomatic approach. Communi-
     cations of the ACM 19(5) (1976) 279–285
[22] Jones, C.B.: Specification and design of (parallel) programs. In Mason, R.E.A., ed.: Information Pro-
     cessing 1983: World Congress Proceedings, Elsevier (1984) 321–332
[23] O’Hearn, P.W.: Resources, concurrency, and local reasoning. Theoretical Computer Science 375(1-3)
     (2007) 271–307
[24] Reynolds, J.C.: Separation logic: A logic for shared mutable data structures. In: LICS, IEEE (2002)
     55–74
[25] Feng, X.: Local rely-guarantee reasoning. In: POPL, ACM (2009) 315–327
[26] Vafeiadis, V., Parkinson, M.J.: A marriage of rely/guarantee and separation logic. In: CONCUR.
     Volume 4703 of LNCS. (2007) 256–271
[27] Reddy, U.S., Reynolds, J.C.: Syntactic control of interference for separation logic. In: POPL, ACM
     (2012) 323–336
[28] Hayman, J.: Granularity and concurrent separation logic. In: CONCUR. Volume 6901 of LNCS. (2011)
     219–234
[29] Pnueli, A., Kesten, Y.: A deductive proof system for CT L∗ . In: CONCUR. Volume 2421 of LNCS.
     (2002) 24–40
[30] Skeirik, S., Ştefănescu, A., Meseguer, J.: A constructor-based reachability logic for rewrite theories. In:
     LOPSTR. Volume 10855 of LNCS., Springer (2017) 201–217
[31] Bae, K., Escobar, S., Meseguer, J.: Abstract logical model checking of infinite-state systems using
     narrowing. In: RTA. (2013) 81–96
[32] Rocha, C., Meseguer, J.: Proving safety properties of rewrite theories. In: CALCO. Volume 6859 of
     LNCS. (2011) 314–328
[33] Rocha, C., Meseguer, J., Muñoz, C.A.: Rewriting modulo SMT and open system analysis. In: WRLA.
     Volume 8663 of LNCS., Springer (2014) 247–262
[34] Harel, D., Kozen, D., Tiuryn, J.: Dynamic logic. In: Handbook of Philosophical Logic. (1984) 497–604
[35] Beckert, B., Hähnle, R., Schmitt, P.H.: Verification of Object-oriented Software: The KeY Approach.
     Springer-Verlag (2007)
[36] Madeira, A., Neves, R., Martins, M.A., Barbosa, L.S.: A dynamic logic for every season. In: SBMF.
     Volume 8941 of LNCS., Springer (2014) 130–145
[37] Moore, B., Peña, L., Roşu, G.: Program verification by coinduction. In: 27th European Symposium on
     Programming (ESOP). (April 2018)




                                                This work is licensed under the Creative Commons Attribution License. To view a copy of this
                                                license, visit https://creativecommons.org/licenses/by/4.0/ or send a letter to Creative
                                                Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or Eisenacher Strasse
                                                2, 10777 Berlin, Germany
