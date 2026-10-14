                                                         Compilation as Multi-Language Semantics
                                                                                                 William J. Bowman
                                                                                             University of British Columbia
                                                                                                  Vancouver, BC, CA
                                                                                              wjb@williamjbowman.com

                                         ACM Reference Format:                                                          A.v ::= .. | (AS S.e)
                                                                                                                                                           S.e ::= .. | (SA A.e)
                                         William J. Bowman. 2021. Compilation as Multi-Language Seman-                  A.n ::= .. | (AS S.e)
                                                                                                                                                             e ::= S.e | A.e
                                         tics. In Workshop on Principles of Secure Compilation (PriSC). ACM,            A.e ::= .. | (AS S.e)
                                         New York, NY, USA, 3 pages.
                                                                                                                                   Fig. 1. 𝜆 sa Syntax (excerpts)
arXiv:2509.19613v1 [cs.PL] 23 Sep 2025




                                         1    Extended Abstract                                                to A-normal form (ANF). This pass is a good example and
                                         Modeling interoperability between programs in different lan-          stress test. The A-reductions are tricky to define because
                                         guages is a key problem when modeling compositional and               they reorder a term with respect to its context, while the
                                         secure compilation. Multi-language semantics provide a syn-           other passes locally transform a term in an arbitrary context.
                                         tactic method for modeling language interopability (Matthews             The source is a standard dynamically typed functional
                                         2007), and has proven useful in compiler correctness and se-          imperative language, modeled on Scheme. It has a call-by-
                                                                                                                                                                     λs
                                         cure compilation (Ahmed 2015; Ahmed and Blume 2011; New               value heap-based small-step semantics, (H S.e1) → (H S.e2),
                                         et al. 2016; Patterson and Ahmed 2017; Perconti and Ahmed             where H represents the heap and S.e is represents a source
                                         2014).                                                                expression.1 We omit the syntax and reduction rules for
                                            Unfortunately, existing models of compilation using multi-         brevity.
                                         language semantics duplicate effort. Two variants of each                The target language is essentially the same, but the syntax
                                         compiler pass are defined: a syntactic translation on open            is restricted to A-normal form: all computations A.n require
                                         terms, and a run-time translation of closed terms at multi-           values A.v as operands; expressions A.e cannot be nested and
                                         language boundaries (Ahmed and Blume 2011; New et al.                 only explicitly compose and sequence intermediate compu-
                                                                                                                                                              λa
                                         2016). One must then prove that both definitions coincide.            tations A.n. The reduction relation, (H A.e1) → (H A.e2), does
                                            We introduce a novel work-in-progress approach to uni-             not require a control stack.
                                         formly model both variants as a single reduction system on               To develop a multi-language semantics, we embed syntac-
                                         open terms in a multi-language semantics. This simultane-             tic terms from each language into a single syntax, defined
                                         ously defines the compiler and the interoperability semantics.        in Figure 1. We extend each meta-variable with boundary
                                         It also has interesting semantic consequences: different re-          terms (SA A.e) (“Source on the outside, ANF on the inside”)
                                         duction strategies model different compilation strategies, and        and (AS S.e) (“ANF on the outside, Source on the inside”).
                                         standard theorems about reduction imply standard compiler                The translation to ANF can be viewed as a reduction sys-
                                         correctness theorems. For example, we get a model of ahead-           tem in the multi-language. We define the A-reductions in
                                         of-time (AOT) compilation by normalizing cross-language               Figure 2. These rules are essentially standard (Flanagan et
                                         redexes; the normal form with respect to these redexes is a           al. 1993), but we modify them to make boundary transitions
                                         target language term. We model just-in-time (JIT) compila-            explicit. The A-reductions have the form S.e →ᵃ S.e, reducing
                                         tion as nondeterministic evaluation in the multi-language: a          source expressions in the multi-language. Each A-reduction
                                         term can either step in the source, or translate then step in         rewrites a source expression in a source evaluation context,
                                         the target. We prove that confluence of multi-language reduc-         transforming the control stack into a data stack. For exam-
                                         tion implies compiler correctness and part of full abstraction;       ple, the A-lift rule lifts a trivial computation, let-binding it
                                         and that subject reduction implies type-preservation of the           and providing the let-bound name (a value) in evaluation
                                         compiler.                                                             position, explicitly sequencing the computation A.n with
                                            An example instance: Reduction to A-normal form                    the evaluation context S.E. The side-conditions syntactically
                                            Our approach generalizes from high-level to low-level              encode termination conditions, preventing A-reductions of
                                         transformations of a wide array of language features. To              target redexes and in empty evaluation contexts.
                                         demonstrate this, we have developed a 5-pass model compiler              We supplement the multi-language A-reductions with the
                                         from a Scheme-like language to an x86-64-like language.               standard boundary cancellation reductions, given in Figure 3.
                                         Here, we model one interesting compiler pass: reduction               These apply under any multi-language context C.

                                         PriSC, Online                                                         1 We use a prefix followed by a dot (.) to distinguish terms in each language—

                                         2021.                                                                 the prefix S for source terms and the prefix A for ANF terms.
PriSC, January 2021, Online                                                                                                     William J. Bowman

                                                                                    λs                                           λs
       A.e →ᵃ (SA A.e)                                 [A-normal]          (H1 S.e1) → (H2 S.e2)                      (H1 S.e1) → (H2 S.e2)
                                                                                    λsa
                                                                                                   [S-Interp]                   λsa
                                                                                                                                                    [AS-Interp]
      S.E[(let ([A.x S.e] .) S.e2)]                [A-merge-l]             (H1 S.e1) ⇒ (H2 S.e2)                (H1 (AS S.e1)) ⇒ (H2 (AS S.e2))
   →ᵃ (SA (let ([A.x (AS S.e)] .) (AS S.E[S.e2])))
                                                                                     λa                                           λa
       where (not (equal? [·] S.E))                                        (H1 A.e1) → (H2 A.e2)                      (H1 A.e1) → (H2 A.e2)
                                                                                                    [A-Run]                                          [SA-Run]
      S.E[(begin S.er . S.e)]                         [A-merge-b]                    λsa
                                                                           (H1 A.e1) ⇒ (H2 A.e2)
                                                                                                                                 λsa
                                                                                                                (H1 (SA A.e1)) ⇒ (H2 (SA A.e2))
   →ᵃ (SA (begin (AS S.er) . (AS S.E[S.e])))
       where (not (equal? [·] S.E))                                                                        A.e1 ˢ→ᵃ A.e2
                                                                                                                               [JIT]
      S.E[(if A.v S.e1 S.e2)]                              [A-join]                                             λsa
                                                                                                       (H1 A.e1) ⇒ (H1 A.e2)
   →ᵃ (SA (letrec ([j (λ (x) S.E[x])])
             (if A.v (AS (j S.e1)) (AS (j S.e2)))))
       where S.E ∈ A.Cn, j, x fresh                                                        Fig. 5. 𝜆 sa Multi-language Reduction

      S.E[A.n]                                              [A-lif]          Note that terms already in the heap are not translated,
   →ᵃ (SA (let ([x A.n]) (AS S.E[x])))                                    which corresponds to an assumption that the language mem-
       where S.E ∈ A.Cn, A.n ∈ A.v, x fresh                               ory models are identical. We could lift this restriction by
                                                                          adding multi-language boundaries to heap values and ex-
               Fig. 2. The A-reductions (excerpts)                        tending translation reductions to apply in the heap.
                                                                             The multi-language reduction allows reducing in the source,
            C[(AS (SA A.e))] →ˢᵗ C[A.e] [Boundary-1]                      modeling interpretation, or translating then reducing in the
             C[(SA (AS S.e))] →ˢᵗ C[S.e] [Boundary-2]                     target, modeling JIT compilation before continuing execu-
                                                                          tion. This does not model speculative optimization; equip-
                                                                          ping the multi-language with assumption instructions as
                Fig. 3. 𝜆 sa Boundary Reductions                          done by Flückiger et al. (2018) might support modeling this.
                                                                             Standard meta-theoretic properites of reduction impliy
T ::= C[(AS [·])]                                e1 →ᵃ e         e1 →ˢᵗ e standard compiler correctness results.
     | C[(lambda (x .) (AS [·]))]            T[e1] ˢ→ᵃ T[e]      e1 ˢ→ᵃ e    Subject reduction of the multi-language semantics implies
                                                                          type-preservation of the compiler. This is simple for our
               Fig. 4. 𝜆 sa Translation Reductions                        present compiler, since the type system is simple, but the
                                                                          theorems applies for more complex type systems.
   In Figure 4 we define the translation reductions. These                Theorem 1 (Subject Reduction implies Type Preservation).
extend the A-reductions to apply under any translation con-               If (Γ ⊢ e1 : τ and e1 ˢ→ᵃ* e2 implies Γ ⊢ e2 : τ) then
text T. The construction of the translation context for ANF is            (S.Γ ⊢ S.e : S.τ and S.e ⇓ᵃⁿᶠ A.e implies ∃A.Γ,A.τ. A.Γ ⊢ A.e : A.τ).
a little unusual, but the intuition is simple: a translation con-
text identifies a pure source expression under any context,                  We derive compiler correctness from confluence.
                                                                                                                       λsa
including under a target/source boundary. The context A.Cm                 Conjecture 1 (Confluence). If (H e) ⇒* (H1 e1) and
                                                                                 λsa                     λsa                    λsa
corresponds to an ANF context that can have any expression                 (H e) ⇒* (H2 e2) then (H1 e1) ⇒* (H3 e3) and (H2 e2) ⇒* (H3 e3)
in the hole. In one step, the translation reductions can per-
form either one A-reduction or one boundary cancellation.                     Note the multi-language semantics can reduce open terms,
   From the translation reductions, we derive AOT compila-                 so confluence implies correctness of both the AOT and the
tion as normalization with respect to translation reductions.              JIT compiler. As an example, whole-program correctness is
                                                                           a trivial corollary of confluence.
Definition 1 (ANF Compilation by Normalization).
                                                                           Corollary 2 (Whole-Program Correctness).
                                                                                       λs                                        λa
  (AS S.e) ˢ→ᵃ* A.e           A.e ˢ→ᵃ                                      If (() S.e) →* (H S.v) and S.e ⇓ᵃⁿᶠ A.e then (() A.e) →* (H A.v) such
             S.e ⇓ᵃⁿᶠ A.e                                                  that A.v is equal to S.v.
   Finally, we define the multi-language semantics in Figure 5.               Multi-language semantics provide a strong attacker model
This defines all possible transitions in the multi-language.               through contextual equivalence. A context C models an at-
A term can either take a step in the source language, or                   tacker that can provide either source or target code or data
a translation step, or a step in the target language. Multi-               as input and observe the result. Contextual equivalence is
language reduction is indexed by a heap, H, which is used                  extended to relate reduction configurations, not just terms,
by the source and target reductions but not the translation                to enable the definition to apply to the JIT model.
reductions.
Compilation as Multi-Language Semantics                                                                    PriSC, January 2021, Online


Definition 2 (Contextual Equivalence). (H1 e1) ≈ (H2 e2) if        Cormac Flanagan, Amr Sabry, Bruce F. Duba, and Matthias Felleisen.
for all multi-language contexts C, (H1 C[e1]) and (H2 C[e2]) co-      The Essence of Compiling with Continuations. In Proc. Interna-
              λsa
terminate in ⇒.                                                       tional Conference on Programming Language Design and Imple-
                                                                      mentation (PLDI), 1993. doi:10.1145/155090.155113
  We define secure compilation of both the AOT and JIT             Olivier Flückiger, Gabriel Scherer, Ming-Ho Yee, Aviral Goel, Amal
models as full abstraction: contextual equivalence is pre-            Ahmed, and Jan Vitek. Correctness of speculative optimiza-
served and reflected through multi-language reduction.                tions with dynamic deoptimization. Proceedings of the ACM
Theorem 3 (Full Abstraction (multi-language)). Suppose                on Programming Languages (PACMPL) 2(POPL), pp. 1–28, 2018.
        λsa                     λsa                                   doi:10.1145/3158137
(H1 e1) ⇒ (H1′ e1′) and (H2 e2) ⇒ (H2′ e2′).
Then (H1 e1) ≈ (H2 e2) if and only if (H1′ e1′) ≈ (H2′ e2′).       Robert Bruce Matthews Jacob And Findler. Operational Se-
                                                                      mantics for Multi-language Programs. In Proc. Sympo-
   The normally easy part of full abstraction, within the             sium on Principles of Programming Languages (POPL), 2007.
multi-language, is now a direct consequence of confluence,            doi:10.1145/1190216.1190220
since both compilation and contextual equivalence are de-          Max S. New, William J. Bowman, and Amal Ahmed. Fully Ab-
fined by multi-language reduction. The hard part, showing             stract Compilation via Universal Embedding. In Proc. Inter-
any multi-language context (attacker) is emulated by a source         national Conference on Functional Programming (ICFP), 2016.
context, remains.                                                     doi:10.1145/2951913.2951941
                                                                   Daniel Patterson and Amal Ahmed. Linking Types for Multi-
Bibliography                                                          Language Software: Have Your Cake and Eat It Too. In Proc.
                                                                      Summit oN Advances in Programming Languages (SNAPL), 2017.
Amal Ahmed. Verified Compilers for a Multi-language World. In
                                                                      doi:10.4230/LIPIcs.SNAPL.2017.12
  Proc. Summit oN Advances in Programming Languages (SNAPL),
                                                                   James T. Perconti and Amal Ahmed. Verifying an Open Compiler
  2015. doi:10.4230/LIPIcs.SNAPL.2015.15
                                                                      Using Multi-language Semantics. In Proc. European Symposium
Amal Ahmed and Matthias Blume. An Equivalence-Preserving
                                                                      on Programming (ESOP), 2014. doi:10.1007/978-3-642-54833-8_8
  CPS Translation via Multi-Language Semantics. In Proc. Inter-
  national Conference on Functional Programming (ICFP), 2011.
  doi:10.1145/2034773.2034830
