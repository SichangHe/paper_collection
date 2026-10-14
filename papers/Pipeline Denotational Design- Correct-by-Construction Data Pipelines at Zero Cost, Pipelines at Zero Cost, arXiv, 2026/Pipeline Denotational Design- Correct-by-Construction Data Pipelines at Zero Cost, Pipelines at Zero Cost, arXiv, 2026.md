                                             Pipeline Denotational Design: Correct-by-Construction Data
                                                               Pipelines at Zero Cost
                                                                                                     Nikos Karayannidis
                                                                                                           Independent
                                                                                                          Athens, Greece
                                                                                                        nkarag@gmail.com

                                         ABSTRACT                                                                   (the measurement campaign is in progress). Finally, because the
                                         Pipeline Denotational Design (PDD) is a design-first methodology           guarantee rests on grain alone, the same design-time check reaches
                                         for building data pipelines that are correct by construction. As AI        beyond pipelines to the AI-generated queries run over semantic
                                         agents generate pipeline code at scale, the bottleneck shifts from         layers and ontologies—a correctness layer that stack otherwise
                                         writing pipelines to verifying them—and the errors that matter             lacks.
                                         most, such as grain inconsistencies that silently inflate aggregates,
                                         are invisible to schema checks, type checks, and tests on sampled          1   INTRODUCTION
                                         data. PDD designs pipelines in a semantic domain rather than in            Data pipelines at enterprise scale are staggeringly complex. A sin-
                                         code: a design is composed from a typed algebra of operations—the          gle analytics platform integrates dozens of heterogeneous sources—
arXiv:2608.12375v1 [cs.DB] 23 Jul 2026




                                         Pipeline Design Algebra (PDA), one such instantiation—in which             operational databases, APIs, message queues, blob storage—through
                                         every well-typed composition is grain-correct by construction. Rest-       thousands of interdependent transformation units, across several
                                         ing on grain alone, this guarantee is universal: it holds for any grain-   persistence layers (landing, integration, serving—the medallion
                                         inferring operation set, over any engine, batch or streaming (PDA          bronze/silver/gold layers), in a mix of cadences from streaming and
                                         being our choice). Correctness is established in three layers—grain,       micro-batch to periodic batch. This complexity is hard to under-
                                         behavioral class, and domain—all at design time, at zero cost, with no     stand, reason about, debug, and evolve; and verifying that a pipeline
                                         access to data: grain by a data-independent type-level computation         is correct at this scale has always been a struggle. Tests help but
                                         (CalcG), behavioral class by the type checker, and the domain rules        do not suffice—as Dijkstra put it, “program testing can be used to
                                         by a proof-carrying composition over operation contracts. This             show the presence of bugs, but never to show their absence”—and
                                         rests on a theorem (Pipeline Correctness): the three layers discharge      the bugs that matter most slip through precisely the tests engi-
                                         grain, behavioral class, and every contract-derivable obligation with      neers rely on. Worse, AI agents now generate pipeline code at scale,
                                         no data access, and a proof-carrying composition collapses what            faster than anyone can review it, amplifying inconsistency and
                                         remains to a single input-boundary check—so a pipeline is correct by       error. The problem this paper addresses is therefore twofold: tame
                                         construction against its specification, and the only data-dependent        this complexity, and verify correctness with guarantees stronger
                                         residue is whether real inputs meet the design’s preconditions (data       than testing can give.
                                         quality, not code correctness). PDD generates that boundary check             The errors that matter are silent. Consider a data engineer—or,
                                         as SQL/PySpark verification queries, provably faithful to their spec-      increasingly, an AI agent—building a report that combines revenue
                                         ification. Correctness by construction is a spectrum, not a single         from one fact table with units sold from another, aggregated per
                                         fixed point: the same design can be verified at three levels of rigor—     customer and date. The two facts have different grains: one row per
                                         by running checks against the data at runtime, by the deployed             customer-channel-date, the other per customer-product-date. The
                                         type-level checker (which decides grain and behavioral class au-           natural query joins on the common columns and aggregates:
                                         tomatically, needing no external solver), or by machine-checked
                                                                                                                    SELECT customer_id, date, SUM(revenue), SUM(units)
                                         proofs in Agda/Lean 4. The stronger the guarantee, the less is left
                                                                                                                    FROM sales_channel JOIN sales_product USING (customer_id,
                                         to check at runtime, and a team chooses where on this spectrum to          date)
                                         sit by a pipeline’s criticality, complexity, and scale. This recasts the   GROUP BY customer_id, date
                                         engineer’s role: an AI agent instantiates a pre-verified pattern and
                                         ships a machine-checkable correctness certificate—an Agda proof            It compiles, runs, and returns the expected result grain—yet it sys-
                                         or an evidence ledger—so the human validates only a compact, data-         tematically inflates both metrics. The join creates a cross product
                                         anchored specification and checks the certificate, a proof-carrying        over the unmatched grain components (channels against products),
                                         discipline for AI-generated pipelines. We realize the methodology          duplicating every row before aggregation. This is a fan trap, and it
                                         end-to-end in a production toolchain—a design tool, a typed frame-         is invisible to schema validation, type checking, and unit tests on
                                         work that implements the algebra, and code-generation that com-            small data: with one channel and one product per customer-date the
                                         piles a verified design into a faithful implementation—and set out         cross product is 1 × 1 and the numbers look right. The root cause is
                                         an evaluation on production pipelines spanning multiple patterns,          a grain inconsistency—an unintended change in the level of detail at
                                         behavioral classes, and modeling paradigms—a three-arm protocol            which data is represented—and it surfaces only in production, after
                                         targeting design-time defect capture, the zero-cost discharge ratio,       the data has been processed, loaded, and consumed downstream.
                                         generated-query yield, and code-generation faithfulness against               Who verifies AI-generated pipelines? Errors of this kind are about
                                         ad-hoc, runtime-data-quality, and LLM-without-design baselines             to get worse. AI agents now generate pipeline code at scale, from
natural-language prompts, faster than any human can review it.                    Correctness in three layers, at design time, at zero cost. PDD ver-
The agents are fluent at producing code that runs; they are no                ifies a pipeline in three layers (§6): grain (does the output grain
better than the engineer at noticing that the result is silently wrong.       match the target?), behavioral class (does each operation respect
The question the field must answer is not “can an agent write                 the read/write semantics of entities, events, versioned records, . . . ?),
a pipeline?”—it plainly can—but who verifies that the pipeline is             and domain (do the business rules hold?). All three are verified at de-
correct? Testing does not scale to the volume of generated code,              sign time, at zero cost—with no access to data: grain by a type-level
and—as the fan trap shows—tests on sampled data do not even                   computation, behavioral class by the type checker, and the domain
catch the bugs that matter. The remedy is not better detection—the            rules by a proof-carrying composition that establishes them on the
data that triggers such a bug and the verification query that would           output given the design’s input preconditions. A data engineer con-
catch it seldom coincide—but prevention: pipelines designed so the            trols the pipeline he builds, not the data a provider sends through
bug cannot be written, in the discipline of making illegal states             it; so the one thing left for runtime is to check that those inputs
unrepresentable [19] (§6.6). The same question is spreading to the            meet the preconditions—data quality, not code correctness—which
read path: agents increasingly generate queries too, over semantic            the method discharges as auto-generated, provably faithful valida-
layers and ontologies that say where and how to ask but not whether           tion queries. The slogan “provably correct pipelines at zero cost,
the answer is correct—so the same design-time guarantee is what               by construction” is thus literal: a pipeline’s correctness is settled
that stack is missing (§9).                                                   before any data is read.

    From verification to synthesis. This paper is Part II of a two-
part program. Part I [14] established the theory and verification:                Three concerns, cleanly separated. Runtime testing conflates three
it formally defines the denotation of data—grain, entity key, be-             questions that PDD keeps apart. (i) Design correctness—does the
havioral class—with computable grain-inference rules and proves               pipeline meet its specification?—is a property of the code, settled
the grain homomorphism on which everything here rests, so that                at design time by a type system (the Pipeline Correctness Theorem,
given a pipeline annotated with grains, the CalcG algorithm decides           §6): as in Agda or Lean 4, business rules become types and a proof-
whether the output grain matches the target’s declared grain—a                carrying composition propagates pre/postconditions so the design
data-independent, decidable, zero-cost check. Verification answers            type-checks against its stated target contract before any data flows.
“is this pipeline correct?”. This paper takes the next step—synthesis         (ii) Implementation faithfulness—does the executable compute what
and methodology—and answers “how do I build a pipeline that can-              the design denotes?—is discharged not by data but by the grain
not be incorrect?”. We present Pipeline Denotational Design (PDD): a          homomorphism (§3) and compilation-correctness (Thm. 6.5), which
methodology in which pipelines are composed from a typed algebra              carry the design’s meaning to the running engine. (iii) Data quality—
of operations (the Pipeline Design Algebra, PDA) where every well-            do real inputs satisfy the design’s assumed preconditions?—is the
typed composition is grain-correct by construction, and the residual,         one genuinely data-dependent question, the boundary every typed
genuinely data-dependent obligations are discharged as automati-              system keeps against untyped external data. Design-time checking
cally generated verification queries. The algebra it instantiates, PDA,       eliminates code bugs (grain mismatches, BC violations, spurious
is to data pipelines what a typed query builder (e.g. LINQ, jOOQ,             joins); the homomorphism governs the design-to-executable gap;
Opaleye) is to raw SQL, and what Codd’s relational algebra [6] is to          and the generated queries guard against data bugs at that bound-
pre-relational data wrangling: a small algebra with laws in which             ary. The checker is a role. At its dependent-types limit ‘mostly at
correctness is a structural property—settled by construction—rather           design time’ becomes ‘fully at design time’: in PDL—the Pipeline De-
than a test result. The two comparisons stress complementary facets:          sign Language, our embedded DSL for pipeline design in Agda and
static type-safety (a malformed pipeline is rejected before it runs)          Lean 4, encoding PDA and its constraint logic—even the boundary
and a foundational algebra with equational laws (compose and rea-             constraints become types, so a design that type-checks is completely
son, rather than hand-code)—and PDA claims both at once, one                  correct, carrying a machine-checked proof a reviewer discharges by
level up: over whole pipelines, not single queries.                           recompiling; the runtime residue then shrinks to the one check no
                                                                              type system can absorb—that untyped incoming data meets the de-
   Three levers on complexity. PDD attacks the twofold problem                sign’s preconditions. PDD-Toolchain as deployed sits one notch left
on three fronts. Simplicity by abstraction: designers reason in the           of that limit: the /pdd tool plays the checker role with an evidence
semantic domain (grain, entity key, behavioral class), formally but           document over the grain, behavioral-class, and contract-derivable
away from engine-specific code, so the centre of gravity moves                obligations—lighter than a proof assistant, but enough to make the
from implementation to meaning. Uniformity by patterns: a small,              principle practical in production. §6.7 places the two on one spec-
typed vocabulary of operations and pre-verified patterns makes                trum. This is the data-pipeline instance of software engineering’s
every pipeline look the same modulo its data domain (a pattern                tests-vs-types-vs-proofs spectrum: with only schemas (structure)
is a pipeline parameterized by that domain, §5), turning bespoke              and untyped operations, a pipeline’s sole handle on correctness is
plumbing into reusable structure. The design as a contract with               to run it and test outputs—the data tests the field relies on today,
AI : the denotational design is a formal blueprint an agent must              which on sampled data miss the grain bugs that matter. A type
satisfy and provide design-time evidence for, so AI accelerates               system rich enough to carry data with its denotation and operations
delivery without amplifying error. Simplicity and uniformity tame             as contracts propagated through composition [14] moves code cor-
the complexity; the contract, together with the three correctness             rectness to design time and confines runtime checks to data quality
layers below, verifies the pipeline’s correctness.                            alone.
                                                                          2
   The engineer’s new role: author the spec, check the certificate. Pre-         specification—the only question left for data is whether real
vention reshapes who does what. Formal verification is only ever as              inputs meet that leaf precondition. It delivers prevention, not
good as its specification—a proof discharges the properties you state            detection—grain, behavioral-class, and fan/chasm-trap bugs
and is silent on the one you forgot—and PDD turns that classical                 become unrepresentable (§6.6).
limitation into a division of labor. Its specification is not a natural-       • A verification spectrum (§6.7): the same PDD design can be
language wish but the data denotation (𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅]) of                 checked at three levels of rigor—runtime queries against the data,
source and target, plus the pre/postcondition business rules (PDLC               the deployed type-level checker (which decides grain and behav-
Step 1, §2.3); and much of it is not the engineer’s to author—the                ioral class automatically, with no external solver), or machine-
source denotation is inferred from data during the data-source anal-             checked Agda/Lean 4 proofs. The stronger the check, the less is
ysis any pipeline already does, PDD or not, and the grain and                    left to verify at runtime—from a check at every node down to a
behavioral-class obligations are derived—so the properties most                  single check at the input. A team picks its level by a pipeline’s
easily forgotten (don’t double-count, respect versioning) cannot                 criticality, complexity, and scale: correctness by construction is
be omitted, and what remains his is small: the target model and                  a dial, not a fixed cost.
its business predicates. Given that spec, the agent does not free-             • PDD Universality (Thm. 3.2): the guarantee rests on grain
style: it faithfully instantiates the designated pipeline pattern for            alone, so any grain-inferring operation set—over batch or stream-
that layer—each layer of the architecture has one or more pre-                   ing carriers—instantiates PDD, with worked instantiations for
verified patterns (§5)—carrying the data from the source denotation              PDA, relational algebra, and the dataflow model.
to the target’s without violating a constraint, and emits a machine-
                                                                               • The Pipeline Design Algebra (PDA, §4), the concrete instru-
checkable certificate of correctness—an Agda proof at the PDL end,
                                                                                 ment we instantiate: four morphism classes (Capture/Transfor-
an evidence ledger at the deployed end. The trust model is thus
                                                                                 m/Declare/Apply) and a ∼30-operation catalog, each carrying
proof-carrying [20]: the agent is an untrusted producer that must
                                                                                 a contract fixing how it transforms grain, behavioral class, and
ship a certificate; the human is the trusted consumer who does only
                                                                                 cardinality; composition operators and pre-verified patterns for
two things—validate the spec (the irreducible act no verifier can
                                                                                 which well-typed composition is grain-correct by construction
perform) and check the certificate (recompile the proof, or review
                                                                                 (Thm. 5.1), plus a faithful bridge from design to executable code.
the ledger). Because proofs are costly to produce but cheap to check,
this is exactly what makes delegating synthesis to an AI safe. The             • PDL, the Pipeline Design Language (§10): a dependently-typed
engineer’s role shifts from writing and reviewing code—infeasible                embedding of PDA and its constraint logic in Agda/Lean 4 with
at the scale AI now generates it—to authoring a compact, data-                   by-construction pipeline-correctness proofs—the proof end of
anchored specification and checking the certificate rather than the              the tests–types–proofs spectrum, mechanized end-to-end on a
code. Whether the agent reliably reaches a faithful instantiation is             real pipeline.
a separate, empirical question, which our evaluation answers by                • A production realization, PDD-Toolchain (§7): a design tool,
comparing pipelines built with and without PDD (§8).                             a typed framework implementing the PDA operations on a real
                                                                                 engine, and code-generation that compiles a verified design into
   A production realization. We realize the methodology end-to-end               a faithful implementation—in production use on an enterprise
in PDD-Toolchain (§7): a design tool that produces and verifies a                program, not a proof of concept.
formal design, a typed PySpark framework (EDB) implementing the                • An evaluation design on real production pipelines (§8)—
PDA operations on a real engine, and code-generation that compiles               design-time defect capture, the zero-cost discharge ratio,
a verified design into a faithful implementation plus its verification           generated-query yield, code-generation faithfulness, cross-
queries. PDD-Toolchain is in production use on an enterprise data-               pipeline uniformity, and runtime residue-collapse—that builds
engineering program—not a proof of concept—and is the source of                  each pipeline three ways along the verification spectrum:
our evaluation (§8).                                                             without PDD (an agent codes directly from the specification,
   Contributions.                                                                with no formal design), with PDD checked by the deployed
                                                                                 evidence-emitting checker, and with PDD proved in PDL
• Pipeline Denotational Design (PDD, §2): a design-first                         (Agda/Lean 4). The contrast isolates the design step from the
  methodology that settles a pipeline’s correctness at design                    LLM’s coding ability (no-PDD vs. deployed) and measures
  time, at zero cost, by designing in a semantic domain and                      what the proof end adds (proved vs. deployed). Ad-hoc
  deriving the implementation to match—grounded in the grain                     hand-written pipelines and runtime-only data-quality tooling
  homomorphism (§3) that makes design-level reasoning provably                   serve as reference points that locate the arms on the wider
  faithful to the data.                                                          landscape—the latter notably unable to express the grain and
• A three-layer correctness framework (§6)—grain (CalcG),                        behavioral-class defects at all.
  behavioral class (typing), and domain (contract-derivable at zero
  cost; data-dependent as generated, provably-faithful queries,
  Thm. 6.5)—unified by the Pipeline Correctness Theorem                        Together they make correctness-by-construction for data pipelines
  (Thm. 6.6): the structural layers are discharged with no data                a practical methodology: grounded in theory (the grain homomor-
  access, and the proof-carrying composition collapses the                     phism), broad (three layers, not grain alone), realized in production,
  residual data-dependent obligations to a single input-boundary               and evaluated quantitatively on real pipelines against agentic and
  check, so the design is correct by construction against its                  runtime-data-quality baselines.
                                                                           3
Table 1: The meaning function [[·]], overloaded by argument                              2.2    Four Denotations, One Methodology
category: for each category C it gives a model [[C]] and a
                                                                                         PDD assigns meaning at four levels, each the subject of a later
semantic function [[·]] C : C → [[C]] (after Elliott [10]). The
                                                                                         section: the denotation of data (§3)—what data is: grain, entity key,
data-type row is the foundational case (Part I [14]); the next
                                                                                         behavioral class; the denotation of operations (§4)—what a transfor-
rows map the concrete artifacts that realize it, and the last
                                                                                         mation intends: a PDA operation with a contract; the denotation of
gives a data constraint (a business rule or integrity require-
                                                                                         pipelines (§5)—what an end-to-end workflow means: a composition
ment) its denotation—a FOL predicate, realized concretely as
                                                                                         of those operations; and the denotation of data constraints (§6)—
a verification query.
                                                                                         what a requirement means: a first-order-logic predicate. Working
                                                                                         in this domain makes designs precise (formal types remove ambi-
    Argument                   [[ · ]] Meaning (PDD)                                     guity), composable (the meaning of the whole is the composition
    data type 𝑅                →     (𝐺 [𝑅 ], 𝐸𝐾 [𝑅 ], 𝐵𝐶 [𝑅 ] ): denotation             of the meanings of the parts), verifiable (correctness conditions are
                                     of data [14]                                        decidable or provable), and implementation-independent (a design
    table / DataFrame / file   →     collection 𝐶 𝑅 carrying                             is a specification, not code tied to one engine).
                                     (𝐺 [𝑅 ], 𝐸𝐾 [𝑅 ], 𝐵𝐶 [𝑅 ] )                             The fourth denotation is worth a closer look, as it carries the
    SQL / PySpark / dbt step   →     PDA operation (declarative intent)                  domain layer of §6. A business rule, integrity constraint, or data-
    ETL pipeline               →     Pipeline Source Target (a function)                 integration rule denotes a first-order-logic predicate, realized in
    data constraint            →     FOL predicate: a (Pre, Intra, Post)                 the type system as a static relation between input and output
                                     spec
                                                                                         (ConsStatic) or a stateful one over a target’s before/after state
                                                                                         (ConsDynamic), and bundled with its precondition into a (Pre,
                                                                                         Intra, Post) specification. Such a specification attaches to a pipeline
2     PIPELINE DENOTATIONAL DESIGN                                                       or sub-pipeline (a pipeline is a DAG of pipelines) and propagates
PDD adapts denotational design [10]—specifying a system by a                             through the DAG via the pipeline operators (§5), each composition
precise mathematical meaning and deriving the implementation                             discharging the obligation that one step’s Post entails the next
to match it—to data pipelines. Rather than designing in terms of                         step’s Pre. Its concrete realization is a verification query, faithful to
SQL queries, PySpark jobs, or Airflow DAGs, the engineer designs                         the predicate by Theorem 6.5—so a design’s two implementations,
in a semantic domain and lets the implementation be generated to                         its code and its checks, are both derived from its denotation, each
agree with that design; we call this the executable design.                              with a faithfulness guarantee.
                                                                                             This mirrors what Codd established for queries—but at the level
2.1      The Semantic Function                                                           of meaning. Codd gave queries a semantic foundation, the relational
                                                                                         model, under which a query’s meaning is fixed independently of
The bridge between the two worlds is a semantic function [[·]], a
                                                                                         how it is written or which algebra evaluates it. Grain theory does
structure-preserving map from concrete artifacts to their mean-
                                                                                         the same for pipelines: the semantic domain (𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅])—
ings (Table 1). A table, DataFrame, or file denotes a data collection
                                                                                         with computable grain-inference rules (the denotation function)
𝑐 : 𝐶 𝑅 (§4.1) carrying a grain 𝐺 [𝑅], entity key 𝐸𝐾 [𝑅], and be-
                                                                                         and a compositional homomorphism (§3)—settles a pipeline’s cor-
havioral class 𝐵𝐶 [𝑅]; a SQL/PySpark/dbt transformation denotes
                                                                                         rectness by meaning, before any operation set or engine is fixed.
a declarative PDA operation (§4); an entire ETL pipeline denotes
                                                                                         PDD is the denotational-design discipline over that domain; PDA (§4)
a function Pipeline Source Target (§5); and a business rule or in-
                                                                                         is one algebra that realizes it—chosen because its operations model
tegrity requirement denotes a data constraint—a first-order-logic
                                                                                         data-engineering intent, but replaceable by relational algebra, the
predicate (§6). Following the discipline of denotational design [10],
                                                                                         dataflow model’s primitives [1], or a typed PySpark—any operation
[[·]] is a single meaning function overloaded by the category of
                                                                                         set whose steps carry grain-inference rules (as PDA’s do), so CalcG
its argument—written [[·]] C when the category C is ambiguous
                                                                                         can thread the denotation through composition (PDD Universality,
and dropped otherwise; for each category it fixes a model [[C]]
                                                                                         Theorem 3.2). The foundation is the semantic domain, not the oper-
and a map [[·]] C : C → [[C]]. Its most fundamental case is the
                                                                                         ations: the semantic domain is to PDA as the relational model is to
data type itself: a type 𝑅 denotes the denotation of data [[𝑅]] =
                                                                                         relational algebra. The payoff, developed in §6, is a three-layer cor-
(𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅]) of Part I [14], the triple every collection car-
                                                                                         rectness framework—grain, behavioral class, and domain—under a
ries. The defining property of [[·]] is that it is a homomorphism:
                                                                                         single principle: a pipeline’s correctness is a property of its code,
                          [[𝑝 src]] = [[𝑝]] [[src]].                           (1)       settled at design time. The three layers discharge it before any data
                                                                                         flows (Pipeline Correctness, Theorem 6.6); what remains for runtime
The meaning of running a pipeline on data equals the meaning                             is not correctness but data quality—whether the inputs meet the
of the pipeline applied to the meaning of the data. Equation (1) is                      design’s preconditions.
what lets design and implementation be developed independently
and stay synchronized: reasoning carried out on the design (the
right-hand side) is faithful to what the code actually computes                          2.3    The Pipeline Development Life Cycle
(the left-hand side). §3 proves that this homomorphism holds—it                          PDD structures pipeline construction as a four-step life cycle
is the grain homomorphism of grain theory—and explains why it                            (PDLC)—a development life cycle for data pipelines—that carries
is computable, which is what turns the principle into a practical                        a design from semantics to a correct, optimized implementation
method.                                                                                  (Table 2). The rest of the paper follows this spine.
                                                                                     4
Table 2: The Pipeline Development Life Cycle. Correctness                       3     BACKGROUND: GRAIN THEORY AND THE
is established once, at design time (Step 2), and preserved                           GRAIN HOMOMORPHISM
through implementation (Step 3) and optimization (Step 4).
                                                                                This section recalls grain theory and the homomorphism (1) that
                                                                                PDD rests on. This material is Part I [14]: it defines the denotation
   Step               Artifact              Correctness evidence      §
                                                                                of data and its inference rules and proves the grain homomorphism—
   1. Prerequisites   data semantics,       —                        —          the foundation this paper (Part II) builds the methodology on. The
                      business rules
   2. PDD             denotational design   CalcG, type checker,     3–6        theory is developed in full, with proofs, there; here we give a self-
                      (blueprint)           generated queries                   contained account of the results the synthesis story needs, with
   3. Executable      implementation        1:1 conformance, query    7
   design             (code)                results on data
                                                                                intuition in place of formal proof, and defer every proof to [14]. The
   4. Optimized       tuned pipeline        semantics-preserving     5, 7       one result in this section that is new—PDD Universality (Thm. 3.2)—
   impl.                                    rewrites                            is a contribution of Part II and flagged as such. The denotation of
                                                                                data it builds is a triple (𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅])—the grain, entity
                                                                                key, and behavioral class of a type—that says what each element
Step 1 (Prerequisites). Gather, for every source and target, the                represents, which entity it is about, and how it must be read and
data semantics (𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅])—the output of data-source                written.
analysis and data modeling—and document the business rules and
cross-system integration logic from requirements analysis.
                                                                                3.1    Grain: the Irreducible Core of a Type
Step 2 (Pipeline Denotational Design). Express the what of the
                                                                                The grain 𝐺 [𝑅] of a type 𝑅 is its level of detail: the irreducible
pipeline—its transformation logic—in PDA, and the business rules
                                                                                identifying core that uniquely determines—and so represents—any
as first-order-logic predicates in the constraint language (PDL). Cor-
                                                                                element of 𝑅 [14]. Formally, a grain is a type 𝐺 that is isomorphic
rectness is then established at design time: CalcG verifies the grain                                                 
transformation, the type checker verifies behavioral-class transi-              to 𝑅 (via the grain function 𝑓𝑔 : 𝐺 −→ 𝑅) and irreducible: no proper
tions and the well-formedness and composition of the business-rule              sub-type of 𝐺 is still isomorphic to 𝑅. The grain is thus the canonical
predicates, and the data-dependent obligations are emitted as verifi-           minimal representative of 𝑅’s isomorphism class—the atom of the
cation queries (§6). The output is a correct denotational design—the            type, the smallest type carrying 𝑅’s full identifying structure. Any
blueprint the implementation must follow.                                       two grains of 𝑅 are themselves isomorphic, so the grain is unique up
Step 3 (Executable Design). Implement the blueprint with a li-                  to isomorphism and every result below is independent of how it is
brary whose operations match PDA closely (1:1 in many cases),                   named (e.g. a WeatherObservation has grain ObservationId, equiv-
yielding an executable design that conforms fully to the PDD; run-              alently StationId × ObservationDtm). An OrderLineItem has grain
ning it—then its verification queries—confirms the data-dependent               OrderId × LineItemId; aggregating line items by order coarsens the
layer on real data. Because the homomorphism (§3) makes the imple-              grain to OrderId. Grain may be internal—its fields are columns of 𝑅,
mentation’s meaning equal the design’s, conformance is structural               as above—or external: a collection of monthly balances is identified
rather than incidental.                                                         by BalanceDate, which is not a stored field. The inverse of the grain
                                                                                function is the grain projection grain𝑅 : 𝑅 → 𝐺 [𝑅], which extracts
Step 4 (Optimized Implementation). Finally, tune the exe-
                                                                                each element’s identifying component.
cutable design for operational constraints—performance, cost,
scalability—selectively and only as needed. Optimizations are                      Type-level field-set operations. Throughout, a (product) type is
applied as semantics-preserving pipeline rewrites (pipeline equiva-             identified with its set of fields, and grain theory lifts the set op-
lence, §5), so the correctness established in Steps 2–3 is preserved            erations to types [14]: 𝑅1 ∪𝑡 𝑦𝑝 𝑅2 , 𝑅1 ∩𝑡 𝑦𝑝 𝑅2 , and 𝑅1 −𝑡 𝑦𝑝 𝑅2 are
by construction.                                                                the union, intersection, and difference of field sets, and 𝑅1 ⊆𝑡 𝑦𝑝 𝑅2
Human effort concentrates on Step 1—authoring and validating the                holds when 𝑅1 ’s fields are contained in 𝑅2 ’s. These act on schemas,
specification (the source and target denotation plus the business               at the type level—no data—and are the workhorse of grain com-
rules); Steps 2–4 then derive the design, check it, and preserve its            putation: the grain lattice below, CalcG (§6), the equi-join grain
correctness, each producing evidence the engineer consumes rather               𝐺 [𝑅1 ] ∪𝑡 𝑦𝑝 (𝐺 [𝑅2 ] −𝑡 𝑦𝑝 𝐽𝑘), and the result-type entry of every
than constructs (§1).                                                           operation contract are all written with them.

                                                                                   A guaranteed key. The grain projection is injective: distinct ele-
2.4       Running Example
                                                                                ments have distinct grains [14]. The grain is therefore a superkey
We thread one example throughout: a customer-order pipeline. Or-                that the type itself guarantees—it plays the role of a primary key, but
der events (grain CustomerId×OrderDtm, behavioral class IsEvent)                as a type-level property fixed by the schema rather than a collection-
are read incrementally, enriched by a lookup to a versioned IsMul-              level constraint that must be declared and that filtering or a careless
tiVersion customer table and a product table, then aggregated into              transformation can silently break. This is exactly what lets a data
a per-customer summary (grain CustomerId, class IsEntity) and                   collection be kept grain-unique by construction (§4.1).
upserted into the target. This small pipeline already exercises a cap-
ture, a grain-safe join, an aggregation that changes the grain, and                Compositional, idempotent, universal. The grain operator dis-
a stateful apply—and, as §6 shows, CalcG proves its grain correct               tributes over the type constructors—𝐺 [𝑅1 ×𝑅2 ] = 𝐺 [𝑅1 ]×𝐺 [𝑅2 ] and
before any data is read, while flagging the fan-trap variant of §1 as           𝐺 [𝑅1 + 𝑅2 ] = 𝐺 [𝑅1 ] + 𝐺 [𝑅2 ]—and is idempotent, 𝐺 [𝐺 [𝑅]] = 𝐺 [𝑅]
a design error.                                                                 (the grain of a grain is itself). By the same recipe, grain extends
                                                                            5
                             𝑅1 ∩𝑡 𝑦𝑝 𝑅2 (coarsest)                            3.3    Entity and Entity Key: a Grain Within the
                       ≤𝑔                             ≤𝑔                              Grain
                  𝑅1                                       𝑅2                  Every element is about some subject—its entity—and the entity key
                                                                               𝐸𝐾 [𝑅] is the grain of that subject (𝐸𝐾 [𝑅] ⊆𝑡 𝑦𝑝 𝐺 [𝑅]): the minimal
                        ≤𝑔                            ≤𝑔                       fields identifying who or what the element pertains to. Unlike the
                              𝑅1 ∪𝑡 𝑦𝑝 𝑅2 (finest)                             grain, which is computed mathematically, the entity is a declared
                                                                               semantic property, fixed by domain analysis (“what is this data
                                                                               about?”) [14]. When the element is the subject, the entity key is
Figure 1: The grain lattice for two incomparable types. The
                                                                               the whole grain: an OrderLineItem’s subject is the line item itself,
least upper bound 𝑅1 ∩𝑡 𝑦𝑝 𝑅2 (top) is the finest common coars-
                                                                               so 𝐸𝐾 [𝑅] = 𝐺 [𝑅] = OrderId × LineItemId. When the element is
ening; the greatest lower bound 𝑅1 ∪𝑡 𝑦𝑝 𝑅2 (bottom) the coars-
                                                                               an occurrence or version of a subject, the entity key is a proper
est common refinement. Join inference resolves incompara-
                                                                               part of the grain—a grain within the grain: a customer version
ble grains through these operations.
                                                                               (grain CustomerId × FromDtm) is about a customer, so 𝐸𝐾 [𝑅] =
                                                                               CustomerId. The entity key is the reconciliation point across types of
                                                                               different grain: a current-state Customer table (grain CustomerId)
                                                                               and its SCD-2 history (grain CustomerId × FromDtm) describe the
                                                                               same customers at different detail, and so must agree on entity key—
compositionally to every algebraic data type: products, sums, and the          entity preservation, the collection relation =𝑒𝑘 (§6), which is strictly
inductive (lists, trees) and coinductive (streams) types built from            more informative than a cardinality check (|𝑐 1 | = |𝑐 2 |) because
them [14]. Grain theory is in this sense type-universal. The one               it reveals which entities are present or missing. This is what lets
subtlety is infinite data: a stream’s grain is itself infinite—finitely        data at one grain be joined, integrated, or augmented with data at
presented as a type expression, but with no finite carrier. It acquires        another (§5).
a finite grain the moment the stream is windowed or partitioned,
the grain becoming the partition key 𝐾 (a per-station daily window             3.4    Behavioral Class: Grain Determines
has grain StationId × Day)—which is precisely the form in which a
                                                                                      Behavior
stream processor evaluates an unbounded input. Grain reasoning
thus covers batch and streaming uniformly: a windowed stage is                    One schema, many behaviors. The same fields admit different
verified exactly as a table is (§4.1).                                         grains, and each grain is a different kind of data. For Customer with
                                                                               fields (CustomerId, Name, . . . , FromDtm, CreatedOn):
                                                                                • grain CustomerId—an entity: each row is a customer’s current
3.2    Grain Relations and the Grain Lattice                                       state;
Three relations compare the grains of two types [14]. Types are                 • grain CustomerId × FromDtm—versioned: each row is a time-
grain-equivalent, 𝑅1 ≡𝑔 𝑅2 , when their grains are isomorphic—                     stamped state, valid over an interval;
equivalently, when 𝑅1  𝑅2 : they represent the same entities at the            • grain CustomerId × CreatedOn—an event: each row is an im-
same detail, possibly from different perspectives. They are grain-                 mutable creation occurrence.
ordered, 𝑅1 ≤𝑔 𝑅2 (“𝑅1 refines 𝑅2 ”), when a surjection 𝐺 [𝑅1 ] ↠
                                                                               One table, three grains, three correct ways to read and write it—so
𝐺 [𝑅2 ] exists, so 𝑅1 carries at least as much detail as 𝑅2 ; equiva-
                                                                               without a declared grain the data cannot be interpreted at all. In
lently a one-to-many map 𝑅1 ↠ 𝑅2 exists. This is the structural
                                                                               practice engineers resolve this ambiguity by guesswork (column
pattern of a foreign key (many-to-one): e.g. OrderDetail ≤𝑔 Order
                                                                               names, sample data, tribal knowledge), the root cause of the trans-
via (orderId, lineItemId) ↦→ orderId. Ordering is a partial order up
                                                                               formation errors of §1. What the grain pins down is the type’s
to isomorphism, and—being surjection existence at the type level—it
                                                                               behavior.
is the structural counterpart of a functional dependency, admitting
an Armstrong-style axiomatization that propagates declared order-                 Behavioral class. A type’s behavioral class 𝐵𝐶 [𝑅] is its behavior:
ings [14]. Finally, 𝑅1 and 𝑅2 are grain-incomparable, 𝑅1 ⟨⟩𝑔 𝑅2 , when         the grain together with the dependency among elements that the grain
neither refines the other—the configuration behind the fan trap of             incorporates [14]. A field changes behavior only when it enters the
§1, where two facts of incomparable grain are joined and silently              grain—in the example above one set of Customer fields becomes
inflate an aggregate.                                                          independent entities, time-ordered states, or creation events purely
    Under ≤𝑔 the space of types forms a bounded lattice (Figure 1).            by its grain. This is why behavior, not domain meaning, dictates
Any two types 𝑅1, 𝑅2 have a least upper bound 𝑅1 ∩𝑡 𝑦𝑝 𝑅2 , their finest       the code. The dependency is what separates classes that share a
common coarsening, and a greatest lower bound 𝑅1 ∪𝑡 𝑦𝑝 𝑅2 , their              grain shape: IsEvent elements are immutable occurrences under a
coarsest common refinement; on product types these are computed                happened-before order, whereas IsMultiVersion elements are states
by intersection and union of the grain field sets. The lattice is what         valid over an interval under an effective-before order, with the
makes grain inference compositional: each operation’s output grain             added invariant that consecutive versions of an entity must differ
is obtained from its inputs’ grains by these field-set operations, and         in payload—so IsMultiVersion ⊂ IsEvent is a genuine refinement,
the incomparable grains arising from a join are resolved through               not a renaming. Because 𝐵𝐶 [𝑅] is determined by grain, it is read
the lattice—the basis of the inference rules of §3.6 and the CalcG             off the schema; the five core classes form a hierarchy and a hand-
algorithm of §6.                                                               ful of them unify the data-modeling paradigms—relational/3NF,
                                                                           6
Table 3: The five core behavioral classes [14]. A type’s behavior is its grain together with the inter-element dependency the grain
incorporates; that dependency—not the grain shape—is what separates the classes (e.g. IsEvent vs. IsMultiVersion). The classes
form a hierarchy, IsMultiVersion ⊂ IsEvent ⊃ IsSeqEvent ⊃ IsSnapshot, each subclass adding constraints, and they subsume
the standard data-modeling paradigms. Only transaction facts are IsEvent; periodic-snapshot facts are IsSnapshot.

   Behavioral class      Grain 𝐺 [𝑅 ]               Inter-element dependency incorporated in the grain                Modeling-paradigm constructs it subsumes
   IsEntity              𝐸𝐾 [𝑅 ]                    none—independent entities (no ordering field in the grain)        relational (3NF) entity; Kimball SCD-1 dimension; Data
                                                                                                                      Vault hub; master / reference data
   IsEvent               𝐸𝐾 [𝑅 ] × EventDtm         happened-before partial order; elements are immutable             Kimball transaction fact; event log; event-sourced
                                                    occurrences (append-only)                                         stream; audit trail
   IsMultiVersion        𝐸𝐾 [𝑅 ] × FromDtm          effective-before order; each element is a state valid over an     Kimball SCD-2 dimension; Data Vault satellite;
                                                    interval; consecutive same-entity versions must differ in         temporal / bitemporal table
                                                    payload
   IsSeqEvent            𝐸𝐾 [𝑅 ] = EventDtm         strict total order—a single global sequence, no concurrency       time series; sequential ledger; CDC stream feed
   IsSnapshot            𝐸𝐾 [𝑅 ] = SnapshotDtm      strict total order; each element covers the complete entity       Kimball periodic-snapshot fact; monthly balance
                                                    population at its snapshot time                                   snapshot


                                                                                                                                   𝜑 (ℎ)
dimensional, Data Vault, document, time-series, event-sourced,                                                          𝐺 [𝑅1 ]             𝐺 [𝑅2 ]
and graph (Table 3). Order-indexed analogues (IsOrdered, IsSe-
                                                                                                                    grain𝑅1                      grain𝑅2
qOrdered), an N:M relation class (IsNMRelation, e.g. Data Vault
links and graph edges), and a parent–child mixin (HasParent) ex-                                                          𝑅1                   𝑅2
                                                                                                                                     ℎ
tend the taxonomy. Together these form the type-level denotation
[[𝑅]] = (𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅])—and they carry precisely what the                          Figure 2: The grain homomorphism. The two paths from 𝑅1
schema cannot. A schema is only structure. The fields of Customer                          to 𝐺 [𝑅2 ] agree: transforming then projecting to grain equals
do not, by themselves, say what each row represents (its level of                          projecting to grain then applying the grain lift. The top row
detail, fixed by 𝐺 [𝑅]), which entity it integrates on (its integration                    reasons about grain alone; the bottom row about full types.
point, 𝐸𝐾 [𝑅]), or how it may be read and written (𝐵𝐶 [𝑅])— the very
questions any correct transformation must answer. A design that is
declarative of its intent, and verifiable as such, therefore cannot act
on bare schemas: it must act on types that carry their denotation                          never touching the data on the bottom row. This is precisely the
[[𝑅]]. That denotation is the object the algebra of §4 manipulates                         homomorphism (1) of §2, and the foundation of Theorem 5.1.
and the layers of §6 verify.
                                                                                           3.6      Why PDD Is Computable
3.5     Why PDD Holds: The Grain                                                           A homomorphism alone would be only an abstract guarantee. PDD
        Homomorphism                                                                       is a practical method because two further ingredients make the
The homomorphism (1) that licenses design-time reasoning is a                              grain lift computable without touching data. First, grain theory sup-
theorem of grain theory. Write grain𝑅 : 𝑅 → 𝐺 [𝑅] for the grain                            plies inference rules: for every relational-algebra operation there
projection. For any transformation ℎ : 𝑅1 → 𝑅2 , its grain lift—the                        is an explicit rule that computes the output grain from the input
grain component of the transformation’s denotation [[ℎ]], captur-                          grains (restriction and extension preserve it, projection and group-
ing its grain-to-grain content and discarding all payload—is the                           ing change it, equi-join follows 𝐺 [𝑅1 ] ∪𝑡 𝑦𝑝 (𝐺 [𝑅2 ] −𝑡 𝑦𝑝 𝐽𝑘)), each
composite                                                                                  established and proved in [14] (Thms. 36–42). These rules are 𝜑 (ℎ)
                                                                                           made concrete—they say exactly what each operation’s denotation
          𝜑 (ℎ) = grain𝑅2 ◦ ℎ ◦ grain𝑅−11 : 𝐺 [𝑅1 ] → 𝐺 [𝑅2 ].                             is, as a finite computation on field sets, resolved through the grain
                                                                                           lattice of §3.2. Second, because 𝐵𝐶 [𝑅] is determined by the grain,
It is what CalcG computes (the entity-key and behavioral-class
                                                                                           the denotation (𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅]) is recomputable after every
components are determined alongside it, §4.2); we keep the distinct
                                                                                           step and acts as an active constraint system, rejecting semantically
name to mark that it tracks only the grain.
                                                                                           invalid operations at design time. Thus after each operation the
Theorem 3.1 (Grain homomorphism [14]). For any ℎ : 𝑅1 →                                    three questions that matter—what is the result’s grain, entity key, and
𝑅2 , grain projection commutes with transformation: grain𝑅2 ◦ ℎ =                          behavioral class?—are all answerable at the type level, which is ex-
𝜑 (ℎ) ◦ grain𝑅1 (Figure 2). Moreover the grain lift is compositional,                      actly what §4–6 exploit to verify pipelines at zero cost. The specific
𝜑 (ℎ 2 ◦ℎ 1 ) = 𝜑 (ℎ 2 )◦𝜑 (ℎ 1 ), and ℎ is a surjection iff 𝜑 (ℎ) is (so 𝑅1 ≤𝑔 𝑅2         PDA operators of §4 are one such instantiation; any transforma-
exactly when 𝜑 (ℎ) is surjective).                                                         tion language with computable grain inference would support PDD
                                                                                           equally. Because the inference rules act on field sets and the pipeline
The commutativity holds by construction (the lift is built to make                         DAG, never on the elements, grain reasoning is independent of a
grain-level reasoning faithful); the content is the compositionality.                      collection’s cardinality: a windowed stream is verified exactly as a
By Theorem 3.1, the grain-level meaning of a whole pipeline is the                         table is, finiteness being a property of PDA’s batch carrier rather
composition of the grain-level meanings of its steps—so a designer                         than of the grain theory (§4.1). Part I already observes that its CalcG
can reason about an entire pipeline on the top row of Figure 2,                            verification algorithm is not tied to relational algebra: it needs only
                                                                                      7
a computable per-operation grain rule over a finite DAG, and win-              Table 4: The grain rule CalcG[op] (𝐺 in ) is the same finite field-
dowed collections supply one for streaming pipelines [14]. We make             set computation across operation sets and carriers: a group-
this a universality result: grain is defined for every algebraic data          by sets the grain to its key, an equi-join unions the input
type (§3.1), and PDD inherits that universality over the operation             grains minus the join key, a window adds itself to the grain.
set and the carrier as well.                                                   PDA instantiates a pattern that relational algebra and the
                                                                               dataflow model share.
Theorem 3.2 (PDD Universality). Let Op be a grain-inferring
operation set—operations over grain-theoretic types, realized over
                                                                                Operation set        Operation              CalcG[op] (𝐺 in )
any carrier 𝐹 (a container type—PDA’s finite-bag collection, a                  (carrier)
stream, . . . ), in which every op ∈ Op carries a faithful grain
rule CalcG[op], i.e. [[op 𝑐]] = CalcG[op] [[𝑐]] for every input 𝑐.              Relational algebra   equi-join ⊲⊳ 𝐽 𝑘       𝐺 [𝑅1 ] ∪𝑡 𝑦𝑝 (𝐺 [𝑅2 ] −𝑡 𝑦𝑝
                                                                                (relations)                                 𝐽𝑘)
Then for every pipeline 𝑝 composed from Op: (i) the homomor-
                                                                                                     aggregation 𝛾𝑋         𝑋
phism [[𝑝 src]] = [[𝑝]] [[src]] holds; (ii) CalcG[𝑝] is computable              PDA (finite bags)    lookup 𝐽 𝑘             𝐺 [𝑅1 ] ∪𝑡 𝑦𝑝 (𝐺 [𝑅2 ] −𝑡 𝑦𝑝
by threading the per-operation rules through the pipeline DAG,                                                              𝐽𝑘)
CalcG[op1 >> op2 ] = CalcG[op2 ] ◦ CalcG[op1 ]; and (iii) grain                                      groupby-ek             𝐸𝐾 [𝑅 ]
correctness—whether CalcG[𝑝] (𝐺 [Source]) = 𝐺 [Target]—is decid-                Dataflow             GroupByKey             𝐾
able at design time, with no data access. Design-time verification (§6)         (bounded/
therefore applies to any such Op, of which PDA is one instance. The             unbounded)
denotation is total on the types involved because grain extends to                                   windowed               𝐾 × Window
arbitrary algebraic data types, inductive and coinductive alike [14];                                GroupByKey
and since decidability needs only finite schemas, not finite data, the
carrier 𝐹 may be unbounded.
                                                                               verifiable. Every operation acts on a data collection, the container
   Proof sketch. Everything rests on the rules being exact. Faith-             we define first.
fulness says that running an operation and then reading off its                Remark 4.1 (PDA is one instantiation). Nothing in this section is
grain gives the same answer as applying that operation’s rule to               load-bearing for PDD in the way the semantic domain (§2) is. Any
the input’s grain: [[op 𝑐]] = CalcG[op] [[𝑐]]. Chaining operations             operations that model concrete transformations and admit com-
therefore chains their rules: for 𝑝 = op1 >> · · · >> op𝑛 , applying the       putable grain inference after each step would support PDD equally
rules in order turns the source grain into the pipeline’s output grain,        (PDD Universality, Theorem 3.2)—relational algebra, the dataflow
[[𝑝 𝑐]] = CalcG[op𝑛 ] · · · CalcG[op1 ] [[𝑐]] (a one-line induction on         model’s primitives, or a typed PySpark all serve, over carriers rang-
the chain; this is the compositionality of the grain homomorphism,             ing from relations to unbounded streams. PDA is the instantiation
§3)—which is exactly (i) and (ii). Threading the per-operation rules           we choose because its operations model data-engineering intent
through the DAG this way is the CalcG verification algorithm of                directly. The foundation is the semantic domain—grain, behavioral
Part I: walk the DAG in topological order, reusing a computed grain            class, and entity key, with their inference rules—not these particular
at a fan-out and applying the binary rule at a fan-in [14]. For (iii),         operations.
each rule is a finite computation on field sets and the DAG is finite,
so the target check CalcG[𝑝] (𝐺 [Source]) = 𝐺 [Target] terminates              4.1    The Data Collection
without reading any data—in time 𝑂 (|𝑉 | · 𝑘 · |𝐹 |) for field-set rules       Where grain theory (§3) reasons about data types, the algebra acts
(a DAG of |𝑉 | operations, fan-in 𝑘, at most |𝐹 | fields per type) [14].       on data collections. Colloquially, a data collection is a dataset with
Finally, a grain is defined for every algebraic data type [14], and no         a guaranteed primary key—its grain. Formally, the meaning of a
rule inspects the data—only the schema—so an unbounded stream                  concrete data source—a table, a Parquet file, a Spark DataFrame,
is verified exactly as a finite table. Full proof in Appendix A.       □       a window of a stream—is a data collection 𝑐 : 𝐶 𝑅: a finite, un-
                                                                               ordered bag whose elements are kept grain-unique by construc-
                                                                               tion. It is built from two primitives, ∅𝑐𝑜𝑙𝑙 and an insertion that
4    THE PIPELINE DESIGN ALGEBRA                                               adds an element only if no element with the same grain is already
PDA is the concrete instrument with which this paper instantiates              present, so every collection satisfies the grain-uniqueness invari-
PDD—one grain-inferring operation set among those Theorem 3.2                  ant ∀𝑟 1, 𝑟 2 ∈ 𝑐. grain 𝑟 1 = grain 𝑟 2 ⇒ 𝑟 1 = 𝑟 2 . The abstraction is
admits (relational algebra and the dataflow model are others), cho-            implementation-independent: the carrier is any type constructor
sen because its operations model data-engineering intent directly.             𝐶 : Set → Set—a functor—that supports the collection interface
The methodology rests on the semantic domain (§2), not on these                (∅𝑐𝑜𝑙𝑙 , the grain-unique insert-coll, delete-coll, and the foldr
particular operations; this section fixes the vocabulary the rest of           catamorphism) and maintains that invariant; lists, bags, database
the paper is written in.                                                       tables, and DataFrames are all instances. Type extractors—GetG,
   In PDD, the meaning of a concrete data operation—a SQL query,               GetEK, GetBC—then recover its semantics (𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅])
a PySpark transformation, a dbt model—is a PDA operation. PDA                  from the schema alone, so designs are portable across engines.
operations are declarative: they express the intent of a transforma-           The collection is not part of the grain-theory denotation, which
tion (the what) without prescribing an implementation (the how),               is collection-free (§3)—it is the carrier that PDA’s operation set
which is what makes a design engine-independent and formally                   commits to. Grain theory assumes only a bare “finite bag” to state
                                                                           8
its inference rules over relational algebra operations, and a grain           Table 5: The operation-contract schema. Every PDA opera-
denotation never inspects the carrier; PDA, by contrast, needs one:           tion instantiates these rows; class defaults are stated once
the write operations of §4.5 are element-level merges, and the class          per class and only deviations are repeated.
invariants below (⊆𝑐 , completeness, grain-unique maintenance) are
collection-level—none is visible to grain alone. The carrier is finite              Group        Row          Meaning
not because grain theory demands it, but because PDA’s opera-
                                                                                    Conditions   Pre / Post  input requirements; guarantees on
tions are batch captures, transforms, and applies over datasets; a                                           the result
streaming operation set would denote the same grains over an un-                    Type-level   Result type how 𝐹 relates to 𝑅 (= 𝑅, ⊆𝑡 𝑦𝑝 𝑅,
bounded carrier. Only at execution—the Executable Design (§7)—is                                             𝑅 ∪𝑡 𝑦𝑝 𝐷, . . . )
the carrier realized concretely, as a typed finite collection such as a                          Grain       𝐺 [Res]: preserved / declared /
DataFrame.                                                                                                   computed
                                                                                                 BC          𝐵𝐶 [Res]: preserved / declared (the
4.2    Four Morphism Classes                                                                                 lens)
                                                                                                 Entity key 𝐸𝐾 [Res]: preserved / derived (from
Every PDA operation belongs to exactly one of four classes. Three
                                                                                                             grain + BC)
act on data—reading, transforming, and writing—and a fourth acts                    Coll-level   Elements    Res ⊆𝑐 𝑐, or new elements
only at the type level:                                                                                      constructed
      IsCapture 𝐴 = 𝐴 → 𝐴           read (endomorphism)                                          Entities    entity-key containment
      IsTransform 𝐴 𝐵 = 𝐴 → 𝐵       transform (pure function)                                    Cardinality bounds on ∥Res∥
                                                                                                 Keys        key/superkey preservation
      IsDeclare 𝐴 𝐵 = 𝐴 → 𝐵         re-declare (type-level only)
                                                                                    Algebraic    Laws        idempotent, assoc., commutative,
      IsApply 𝐴 = 𝐴 → 𝐴 → 𝐴         write (binary merge)                                                     identity, . . .
where 𝐴, 𝐵 range over arbitrary types; every catalog operation
instantiates them at a collection (𝐴 = 𝐶 𝑅). Leaving the classes
polymorphic, rather than fixing the carrier to 𝐶 ·, is what lets a            single global entity). The grain does not pin the BC down by it-
pipeline range over a composite type such as the product built                self; it offers a finite menu of admissible lenses, each gated by a
by < × > (§5). A capture filters but never adds or alters elements            dependent-type constraint—the grain CustomerId×Updated_at ad-
(op 𝑐 ⊆𝑐 𝑐). A transform is a pure, total function that may change            mits IsEntity, or IsEvent/IsMultiVersion on Updated_at when their
the type, grain, and behavioral class. A declare changes only the             constraints hold—and the engineer declares which lens to view the
denotation—the declared grain, behavioral class, and derived entity           data through (a declare-⟨bc⟩—a declare, §4.7—can re-lens a type
key—performing no operation on the data; it is the one family with            even when nothing else about it changes). The entity key is then de-
no relational-algebra analogue, sound under a precondition (its               rived from the grain and the chosen BC by that class’s own rule, so
declared grain is a key of the input) discharged at design time (§6.3).       the determination order is grain → BC → EK; the contract records
An apply merges incoming data into a before-state, with an explicit           BC as declared, EK as derived. Hence an operation that preserves
conflict-resolution rule.                                                     the grain and keeps the lens preserves BC and EK automatically—
   The three data acts are the stages of the Capture–Transform–               captures and applies are BC-correct for free—and only a grain- or
Apply (CTA) pipeline anatomy that §5 composes into pipelines; a               lens-changing transform must declare a new BC, whose admissibil-
declare acts only on the type and adds no stage, as its composition           ity is discharged at the type level by the dependent-type constraint
shows.                                                                        gating that lens (§6). The whole denotation (𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅])
Proposition 4.2 (Declares compose away). A declare changes the                is thus fixed and checked at design time; only domain constraints
denotation but touches no data, so on its own it is neither a capture         (Layer 3) are ever data-dependent, and those are business rules over
(which keeps the denotation) nor a transform (which touches data). Its        values, not the denotation.
precondition—the declared grain is a key of the input—is established
only by a data operation that makes that grain a key (a capture or            4.3      Operation Contracts
transform such as pick, checkout, groupby); another declare, doing            Every operation carries a contract: a fixed-schema table stating its
no data work, cannot supply it, so declares do not chain. Hence a             precondition, postcondition, and the way it transforms type, grain,
grain-changing declare is always adjacent to a capture or transform,          entity key, behavioral class, element/entity containment, cardinality,
and the composite (𝐶 ◦ 𝐷, 𝐷 ◦ 𝐶, 𝑇 ◦ 𝐷, 𝐷 ◦ 𝑇 ) both touches data             keys, and which algebraic laws it satisfies (Table 5). Contracts are
and changes the type—a transform. A declare therefore introduces              not documentation—they are the proof obligations that the three
no pipeline stage: it folds into a process-phase transform, leaving the       correctness layers of §6 discharge. To keep the catalog compact,
CTA anatomy intact.                                                           each class states its defaults once; an operation’s contract lists only
   Grain, lens, and key. The three type-level properties are total:           deviations.
every collection has a grain 𝐺 [𝑅], a behavioral class 𝐵𝐶 [𝑅], and
an entity key 𝐸𝐾 [𝑅]—none is ever absent (a scalar aggregate such             4.4      Capture: Reading Data
as a customer count is its own irreducible grain, 𝐸𝐾 [𝑅] = 𝐺 [𝑅],             Captures are endomorphisms; each behavioral class has canonical
an IsEntity; a sequential-event log has 𝐸𝐾 [𝑅] = 𝐺 [𝑅] equal to               captures that enforce its intended read pattern (Table 6). Read-
the event timestamp, which indexes the successive states of its               ing an IsEvent log is a time-window delta; reading the current
                                                                          9
Table 6: The capture catalog. Each capture is canonical for                    Table 7: The apply catalog. Conflict resolution distinguishes
the behavioral classes shown; all preserve grain and BC.                       the operations; all preserve grain and BC and are idempotent.

 Operation            Canonical for        Reads                                     Operation        Canonical for    Conflict resolution
 full                 IsEntity,            the entire collection                     append           IsEvent          first-writer-wins
                      IsNMRelation                                                   upsert           IsEntity         last-writer-wins
 cdc                  IsEntity             rows new/changed vs. a                    replace          IsEntity         stateless (discard before)
                                           before-state                              merge-delete     IsEntity         symmetric difference
 delta(lo,hi)         IsEvent              events in a time window                   commit-append    IsMultiVersion   append if payload changed
 snapshot(t)          IsSnapshot           the snapshot at time 𝑡                    commit-upsert    IsMultiVersion   SCD2: append + close prior
 checkout(t)          IsMultiVersion       latest version per entity ≤
                                           𝑡
 asof(t)              poly.                BC-dispatched “state as of             Apply is pure: no mutable state, no state logic. Although an ap-
                                           𝑡”                                  ply writes, it is a pure function apply : 𝐴 → 𝐴 → 𝐴 of an
 filter(P)            any                  rows satisfying 𝑃                   immutable before-state and source, returning a fresh collection
 pick(𝐺,ord,dir)      any                  top-ranked row per 𝐺-
                                                                               𝑟 = apply before new; nothing is updated in place. Its stateful
                                           partition
                                                                               condition Intra (Thm. 6.6) is therefore a plain predicate relating
                                                                               the two values in hand—for a no-salary-cut policy on an IsEntity
                                                                               target,
state of an IsMultiVersion table is a checkout at a timestamp—the
point-in-time query familiar from Kimball SCD-2 dimensions and                       Intra(before, 𝑟 ) ≡ ∀𝑒 ∈ 𝑟, 𝑒 0 ∈ before. key(𝑒) = key(𝑒 0 )
Data Vault satellites; a full scan of a versioned table is deliberately                                   ⇒ 𝑒.salary ≥ 𝑒 0 .salary,
not canonical—it must be requested explicitly through the con-                 discharged by comparing the result 𝑟 against before directly. Be-
verter pattern below. All captures share the defaults: result type             cause the before-state is an explicit value rather than a mutated
= 𝑅, grain/EK/BC preserved, Res ⊆𝑐 𝑐, and ∥Res∥ ≤ ∥𝑐 ∥.                        cell, the aliasing and interference that motivate state logics (separa-
   Converter pattern. To apply a non-canonical capture, first convert          tion logic, frame rules) cannot arise: referential transparency gives
the behavioral class with a declare (§4.7). For example, full ◦                non-interference for free, and predicates over distinct collections
declare-entity reads all entities of a multi-version collection—               compose with ∧, not a separating conjunction. This is why the same
making an otherwise dangerous full read of a temporal table explicit           Hoare-style, refinement/dependent-typed discipline (§10) covers
and auditable, rather than an accident.                                        every morphism class, writes included, with no state-logic caveat.

   pick generalizes checkout. pick(𝐺, ord, dir) keeps the top-                 4.6     Transform: Reshaping Data
ranked row per 𝐺-partition—an endomorphism (the result rows                    Transforms are the algebra’s expressive core. They subdivide into
are unchanged, just fewer) that preserves grain and BC while                   families (Table 8), of which the joins are the most consequential
establishing 𝐺 as a key of the result. checkout is its IsMultiVersion          for correctness. Each transform is a pure, foldr-derived function
instance (partition by entity, rank by version time); pick lifts the           with a denotational spec; since the value-level meaning is classical
pattern to any type and ordering. This is why it is a capture, not             relational algebra, we summarize the catalog by what composition
a transform: it selects rows rather than declaring a new grain.                and correctness turn on—its effect on grain, behavioral class, and
Restoring a coarser grain after a -low fan-out is then a pick                  type.
followed by a re-lens (§6.3)—the selection establishes the key, the
re-lens declares the grain.                                                       Set operations. union, diff, intersect, sym-diff (and id) are
                                                                               grain-based, same-type, same-BC, and grain-preserving; under an
4.5     Apply: Writing Data                                                    agreement precondition they form a Boolean algebra.
Apply operations merge incoming data new into a before-state                       Joins. Every join assigns the two collections distinct roles—a
before. All satisfy two invariants—completeness (every source grain            primary 𝑅1 (the one flowing through the pipeline) and a supplemen-
appears in the result) and idempotency (re-applying the same source            tary 𝑅2 —and its result grain is fixed at the type level by the join
is a no-op)—and are distinguished by a conflict-resolution rule for            grain-inference theorems of [14] (principally the equi-join grain
grains present in both arguments (Table 7). The catalog reveals a              theorem, Thm. 37). The grain-ordered equi-joins vary along two
clean symmetry: append (first-writer-wins) and upsert (last-writer-            axes. Row preservation separates lookup, which keeps a primary
wins) differ by exactly one delete-coll:                                       row only when it matches (inner), from augment, which keeps ev-
         append = foldr insert-coll,                                           ery primary row and leaves the supplementary fields empty when
                                                                               it does not (left-outer). Grain direction is set by the ordering: the de-
         upsert = foldr (insert-coll ◦ delete-coll).
                                                                               fault forms require 𝑅1 ≤𝑔 𝑅2 —the primary is the finer side—whose
The multi-version applies (commit-append, commit-upsert) im-                   witness is the join function, so no key is named and each primary
plement the SCD Type 2 pattern: append a new version only when                 row has at most one match; the result then preserves the primary
the payload changed, and (for commit-upsert) close the previous                grain, 𝐺 [Res] = 𝐺 [𝑅1 ]—no fan-out, no fan trap, by construction.
version.                                                                       The -low variants invert the ordering (𝑅2 ≤𝑔 𝑅1 ): the primary
                                                                          10
descends to the finer supplementary grain, 𝐺 [Res] = 𝐺 [𝑅2 ], a de-            customer’s current state as of time 𝑡:
liberate fan-out the engineer declares by choosing the variant. The                   src | > checkout 𝑡 >> declare-entity cust_id
free equi-joins lookup-on/augment-on—the explicit-key counter-                                >> sel-safe payload.
parts of lookup/augment, with the on 𝑗𝑘 1 𝑗𝑘 2 clause as sugar—and
natural-join (keyed on shared columns) take the join key directly              checkout 𝑡 (a capture, Table 6) keeps the latest version per entity
and need no grain ordering. semi-join and anti-join keep the                   ≤ 𝑡, preserving the grain but establishing CustID as a key of its
primary rows that respectively do and do not match; each returns a             result. declare-entity cust_id (a declare, Table 9) re-lenses to
sub-collection of the primary, so 𝐺 [Res] = 𝐺 [𝑅1 ]. A theta-join, fi-         (CustID, CustID, IsEntity)—its precondition, that CustID is a key,
nally, matches on an arbitrary predicate—no key relates the inputs—            discharged by checkout’s postcondition at the type level, with no
so the result takes the Cartesian grain 𝐺 [𝑅1 ] × 𝐺 [𝑅2 ].                     data touched. Finally sel-safe payload (a transform, Table 8) drops
                                                                               the now-redundant FromDtm—a safe payload reduction, since the
   Selections. The value selections are grain-preserving projections           declared grain CustID is retained. The result type is 𝐶 CustVer −𝑡 𝑦𝑝
on the data: sel-safe drops payload while keeping all grain                    FromDtm with denotation (CustID, CustID, IsEntity): one current-
columns (grain and BC preserved), and sel-grain/sel-ek project                 state row per customer, an entity. Every step’s denotation—and the
to the bare grain/entity-key values. All are genuine projections               capture→declare hand-off—is settled at design time, before any
and always well-defined. The grain- and BC-changing re-lenses—                 data is read.
declare-entity, declare-event, . . . —are a separate class: they
touch no data and are treated in §4.7.                                         5     SYNTHESIZING PIPELINES BY
   Enrichment, grouping, and structure. enrich extends each                          COMPOSITION
element with computed or window-derived columns (grain-                        §4 gave the operations; this section composes them into pipelines.
preserving); groupby-* aggregates, declaring the grouping                      This is the synthesis side of the verification–synthesis duality: where
columns as the new grain and BC; and explode unnests a nested                  CalcG (§6) verifies that a given DAG is grain-correct, the operators
field, inheriting the nested type’s grain under a grain-disjointness           here construct a pipeline as a single well-typed function Source →
precondition. (Row selection per partition—pick—is a capture,                  Target whose correctness is guaranteed by the way it was built.
§4.4, not a transform.) Together with the captures, declares (§4.7),
and applies, these operations form the complete vocabulary that                5.1    The Pipeline Type and the CTA Constructor
pipeline designs are written in; every one of them comes with the              A pipeline is a function from a before-state and a source to a new
contract that the next sections exploit.                                       target state:
                                                                                     Pipeline Source Target = Target → Source → Target,
4.7    Declare: Re-declaring the Denotation
A declare-⟨bc⟩ changes only a collection’s denotation—its grain,               where Source and Target are arbitrary types. The CTA constructor
behavioral class, and derived entity key—and performs no opera-                instantiates them at collections (𝐶 𝑅); keeping the type polymorphic
tion on the data (Table 9). It is the one operation family with no             lets the pipeline product < × > range over a product S1 × S2 —a pair
relational-algebra counterpart: where a transform reshapes tuples,             of collections, not a collection of pairs. The before-state enables
a declare re-interprets the same rows under a new grain. Each                  stateful applies (upsert, append); a stateless pipeline simply passes
takes the projections naming the new grain components and is                   ∅𝑐𝑜𝑙𝑙 , written [ pip ] 𝑆𝐿 . The canonical way to build a pipeline is the
sound under a single precondition—the declared grain is a key of               CTA constructor, which wires a capture, a transform, and an apply
the input—discharged at design time by the preceding operation’s               into the data flow
Keys postcondition and checked by the type checker; nothing is                              [ capture ⇒ transform ⇒ apply ] = 𝜆 trg src.
read (§6.3). This is the operational core of denotational design: a                          src | > capture >> transform >> apply trg,
grain is declared and verified, not computed.                                  where | > is pipe-forward (𝑥 | > 𝑓 = 𝑓 𝑥) and >> is forward composi-
The precondition is the declare’s only contract with the rest of the           tion ((𝑓 >> 𝑔) 𝑥 = 𝑔(𝑓 𝑥)). Read left to right, the source is captured,
pipeline, and it is deliberately indifferent to how the key was estab-         transformed, then applied to the target—exactly the engineer’s
lished—this is the strength of the approach. Whether the preceding             mental model of a data flow.
step is a checkout, a pick, a groupby, or an arbitrarily long sub-
pipeline, all the declare requires is that step’s Keys postcondition—          5.2    Composition Operators
that the target grain is a key of its output; the declare neither knows
                                                                               A handful of operators express any pipeline topology (Table 10). For-
nor cares what produced that guarantee. Only when no such guar-
                                                                               ward composition >> chains the operations inside a CTA and, once
antee holds must the collapse first be defined, by any operation
                                                                               before-states are supplied, chains whole pipelines (a stateless medal-
whose contract establishes the key (e.g. checkout, pick, groupby,
                                                                               lion Landing → Integration → Serving is [ 𝑝 1 ] 𝑆𝐿 >> [ 𝑝 2 ] 𝑆𝐿 >> 𝑝 3 ).
or bespoke), before the re-lens applies.
                                                                               Two operators combine independent pipelines: the pipeline product
   Worked example: a versioned dimension to its current state. The             < × > splits a product source across two branches (parallel fan-out),
four classes compose in one line—using pipe-forward | > and for-               while the pipeline fork < && > feeds one source to both branches
ward composition >> (Table 10, §5). Let src : 𝐶 CustVer be an                  and pairs their targets—the way a single pattern maintains two col-
SCD2 customer dimension—an IsMultiVersion type with denota-                    lections at once, e.g. a current-state table and its history. Pipeline
tion (CustID × FromDtm, CustID, IsMultiVersion). To read each                  sequencing >> 𝑝 chains sub-pipelines by materializing each prefix
                                                                          11
Table 8: The transform catalog: result grain 𝐺 [Res] and behavioral class 𝐵𝐶 [Res] for each operation (“pres.” = preserved from
the input). The groupby-⟨bc⟩ family (like the declares of §4.7) has one operation per behavioral class; the declared class fixes the
result grain—IsEntity: 𝐸𝐾 [𝑅]; IsEvent: 𝐸𝐾 [𝑅] × EventDtm; IsMultiVersion: 𝐸𝐾 [𝑅] × FromDtm; IsSeqEvent: EventDtm; IsSnapshot:
SnapshotDtm; IsOrdered: 𝐸𝐾 [𝑅] × OrdType; IsSeqOrdered: OrdType; IsNMRelation: 𝐺 1 × 𝐺 2 .

   Operation                          𝐺 [ Res ]                           𝐵𝐶 [ Res ]           Description
   Set operations (same type)
   id                                 𝐺 [𝑅 ]                              pres.                identity
   union,      diff,     intersect,   𝐺 [𝑅 ]                              pres.                grain-based Boolean algebra
   sym-diff
   Joins (primary 𝑅1 , supplementary 𝑅2 )
   lookup                             𝐺 [𝑅1 ]                             𝐵𝐶 [𝑅1 ]             grain-safe inner join; 𝑅1 ≤𝑔 𝑅2 forces 𝐽𝑘 = 𝐺 [𝑅2 ] (at most one match);
                                                                                               unmatched primary rows dropped
  augment                             𝐺 [𝑅1 ]                             𝐵𝐶 [𝑅1 ]             grain-safe left-outer join; every primary row kept
  lookup-low, augment-low             𝐺 [𝑅2 ]                             𝐵𝐶 [𝑅2 ]             inverted ordering (𝑅2 ≤𝑔 𝑅1 ); primary descends to the finer grain
  semi-join, anti-join (incl.         𝐺 [𝑅1 ]                             𝐵𝐶 [𝑅1 ]             keep primary rows with / without a match (Res ⊆𝑐 𝑐 1 )
  -on)
  lookup-on,        augment-on,       𝐺 [𝑅1 ] ∪𝑡 𝑦𝑝 (𝐺 [𝑅2 ] −𝑡 𝑦𝑝 𝐽𝑘 )   follows grain        explicit-key equi-join (Thm. 37), no ordering required; equals 𝐺 [𝑅1 ] iff 𝐽𝑘
  natural-join                                                                                 covers 𝐺 [𝑅2 ] . natural-join: 𝐽𝑘 = 𝑅1 ∩𝑡 𝑦𝑝 𝑅2
  theta-join                          𝐺 [𝑅1 ] × 𝐺 [𝑅2 ]                   follows grain        arbitrary predicate 𝜃 ; Cartesian grain
   Selections
   sel-safe                           𝐺 [𝑅 ]                              pres.                drop payload, keep all grain columns
   sel-grain                          𝐺 [𝑅 ]                              pres.                project to grain values
   sel-ek                             𝐸𝐾 [𝑅 ]                             IsEntity             project to entity-key values
   Enrichment (grain-preserving)
   enrich,      enrich-metadata,      𝐺 [𝑅 ]                              pres.                extend each row with computed, metadata, or window-derived fields
   enrich-window
   Grouping and aggregation
   agg                                𝐺 [𝐴]                               IsEntity             scalar aggregate: whole collection → one row
   groupby- ⟨ bc ⟩                    declared                            ⟨ bc ⟩               partition by the grouping key (the new grain) and aggregate
   Structural
   explode                            𝐺 [𝑆 ]                              𝐵𝐶 [𝑆 ]              unnest a nested-collection field; grows cardinality (sub-collections grain-
                                                                                               disjoint)


Table 9: The declare catalog: one re-lens per behavioral class.                             Table 10: Pipeline operators. Any DAG topology is expressible
Each declares the grain and BC shown (and derives the entity                                with >>, < × >, and flattenp; the fork < && > and pipeline-
key) with no data operation, under the precondition that the                                sequencing >> 𝑝 are derived conveniences for dual-target
declared grain is a key of the input (§6.3).                                                and multi-stage patterns.

    Operation                      Declares grain            Declares BC                     Operator              Meaning
    declare-entity                𝐸𝐾 [𝑅 ]                    IsEntity                        𝑥 |>𝑓                 pipe-forward: 𝑓 𝑥
    declare-event                 𝐸𝐾 [𝑅 ] × EventDtm         IsEvent                         𝑓 >> 𝑔                forward composition 𝑔 ◦ 𝑓 : chains operations, and
    declare-multiversion          𝐸𝐾 [𝑅 ] × FromDtm          IsMultiVersion                                        before-state-applied pipelines
    declare-seq-event             EventDtm                   IsSeqEvent                      [ pip ] 𝑆𝐿            stateless projection: pip ∅𝑐𝑜𝑙𝑙
    declare-snapshot              SnapshotDtm                IsSnapshot                      pip1 < × > pip2       pipeline product: split a product source across two
    declare-ordered               𝐸𝐾 [𝑅 ] × OrdType          IsOrdered                                             branches
    declare-seq-ordered           OrdType                    IsSeqOrdered                    pip1 < && > pip2      pipeline fork: feed one source to both branches, pair
    declare-nm-relation           𝐺1 × 𝐺2                    IsNMRelation                                          the two targets
                                                                                             pip1 >> 𝑝 pip2        pipeline sequencing: prefix stateless, last stage state-
                                                                                                                   ful
                                                                                             flattenp              flatten nested product tuples
                                                                                             𝑓 >>> 𝑔               proof-carrying composition (§6)
statelessly while the last stage stays stateful; it is the idiomatic way a
composite pattern wires its stages. Finally, flattenp restructures the
nested tuples that products create. The three topology-forming op-                          5.3    Well-Typed Composition is Grain-Correct
erators already suffice: any DAG—sequential, parallel, or arbitrary
                                                                                            The payoff of building pipelines this way is that grain correctness is
fan-in/fan-out—is a combination of >>, < × >, and flattenp (< && >
                                                                                            not checked after the fact—it is a property of well-typedness. Each
and >> 𝑝 are definable from them), reducing a whole pipeline to one
                                                                                            operation’s contract fixes how it transforms grain (§4.3), and CalcG
composable function. The operators obey the expected laws—>>
                                                                                            composes these rules functionally (§6). Hence:
is associative with identity id, and < × > distributes over >>—so
designs can be refactored and optimized with machine-checkable                              Theorem 5.1 (Compositional grain correctness). For pipelines
equivalences.                                                                               pip1, pip2 and the operators of Table 10, CalcG[pip1 >> pip2 ] =
                                                                                       12
CalcG[pip2 ] ◦ CalcG[pip1 ] and CalcG[pip1 < × > pip2 ] =                       Table 11: All three correctness layers are established at design
CalcG[pip1 ] × CalcG[pip2 ]. Consequently, if every stage’s contract            time, at zero cost—with no access to data. Only data-dependent
is satisfied, the composed pipeline’s output grain is determined—and            constraints add a runtime check, and it validates the inputs
a design whose computed grain equals the declared target grain is               (data quality), not the code.
grain-correct by construction (Thm. 6.1).
                                                                                    Layer               Establishes (design time, zero   Runtime input
Because composition of grain rules mirrors composition of opera-                                        cost)                            check
tions, a designer never reasons about the whole pipeline at once:
                                                                                    Grain               output grain = target (CalcG)    —
local well-typedness at each stage yields global grain correctness.
                                                                                    Behavioral class    operations respect their BC      —
This is the precise sense in which PDD is to data pipelines what                                        (typing)
type-safe query construction is to SQL.                                             Domain (contract-   ⊆𝑐 , ≡𝑔 , cardinality bounds     —
                                                                                    derivable)          (contracts)
5.4    Pipeline Patterns                                                            Domain     (data-   FK, ranges, business rules,      generated
                                                                                    dependent)          given input preconditions        query
Most production pipelines are instances of a few recurring shapes.
Since a pipeline denotes a function (§2, §5), a pattern denotes a
parametrically polymorphic function—a map from data semantics
(𝐺 [·], 𝐸𝐾 [·], 𝐵𝐶 [·] of its sources and target) to a concrete CTA                 apply. Each sub-pattern is verified in isolation, so Augmentation
pipeline—whose operations are fixed but whose types, grains, and                    is grain-correct by construction from its parts.
arities vary. Patterns consume their semantic constraints as evi-               Patterns compose exactly as pipelines do—by >> 𝑝—and the com-
dence: append consumes IsEvent evidence, lookup consumes grain-                 posite of patterns is again a pattern: a CTA whose capture is the
ordering evidence. Variable arity (e.g. 𝑛 providers, an FK chain of             first sub-pattern’s capture, whose apply is the last’s, and whose
depth 𝑘) is handled by the iter combinator, iter op [𝑐 1, . . . , 𝑐𝑛 ] =        transform is everything between. The named vocabulary is there-
op 𝑐 1 >> · · · >> op 𝑐𝑛 , over which CalcG distributes. A pattern is           fore closed under composition (Augmentation is one instance of that
correct when every valid instantiation is correct—verified once,                closure), giving a small, pre-verified set of pipeline shapes from
symbolically, on the parametric types, then reused for free at every            which real pipelines are assembled and, by Theorem 5.1, inherit
instantiation. PDA ships three named patterns:                                  grain correctness automatically.
• Ingestion (external source → staging): a full or incremental
  extract. The extract mode fixes the apply—replace (full refresh)              6     THREE-LAYER CORRECTNESS
  or append (incremental)—and, critically, may change the staging               PDD establishes pipeline correctness in three layers (Table 11), all
  collection’s behavioral class.                                                at design time, at zero cost—with no access to data. This is the cen-
• Staging-to-Landing (staging → persistent landing): promotes                   tral claim of the paper, and it is a theorem: a pipeline’s correctness
  the staged data to a dual target—a current-state collection and a             is a property of its code, settled before any data flows (Pipeline
  history collection—written together with the fork < && >. The                 Correctness, Thm 6.6), under the design’s assumptions about its
  staging BC fixes each target’s BC and apply: an entity source, for            inputs. A data engineer controls the pipeline he builds, not the
  instance, yields an IsEntity current state maintained by upsert               data a provider sends through it; so the one obligation that gen-
  and an IsEvent history maintained by append, with the cross-                  uinely depends on data—whether the inputs meet those assumed
  target invariant that the latest point-in-time of the history equals          preconditions—is data quality, not code correctness, and it leaves
  the current state.                                                            the zero-cost correctness of the code untouched. The method dis-
• Augmentation (Landing → Integration → Serving): the                           charges that obligation as auto-generated validation queries at the
  medallion workhorse, and itself the composition—via >> 𝑝—of                   input boundary every typed system keeps against untyped external
  four pre-verified sub-patterns,                                               data. Code bugs are eliminated by construction, at zero cost; data
                                                                                bugs are caught at that boundary.
           augmentation = delta-unif. >> 𝑝 delta-augment
                            >> 𝑝 stage-prep >> 𝑝 target-load,                   6.1      Layer 1: Grain Correctness via CalcG (Zero
   each of which is again a CTA. Delta-unif. builds a target-grain dri-                  Cost)
   ver delta—the target records to (re)process this run—by navigat-             The grain inference rules of Part I [14] assign every PDA opera-
   ing every provider to the target entity key according to its kind:           tion a grain transformation that involves only finite set operations
   direct providers carry the full target EK (projected with sel-ek),           (∪𝑡 𝑦𝑝 , ∩𝑡 𝑦𝑝 , −𝑡 𝑦𝑝 , ⊆𝑡 𝑦𝑝 ) on field sets. The grain-computation op-
   semi-direct providers carry the target entity but lack some EK               erator CalcG[op] (𝐺 in ) applies these rules; for example captures,
   columns (completed row-preservingly via augment/enrich), and                 applies, set operations, enrich, and sel-safe preserve the input
   indirect providers do not carry the target entity (navigated via             grain, groupby sets the grain to the grouping columns, and an equi-
   lookup, dropping rows that fail), then unifies them with iter                join yields JoinGrain(𝐺 1, 𝐺 2, 𝐽𝑘) = 𝐺 1 ∪𝑡 𝑦𝑝 (𝐺 2 −𝑡 𝑦𝑝 𝐽𝑘) (Thm. 37).
   union. Delta-augment adds the business content, joining in the               CalcG composes functionally over pipelines, CalcG[op1 >> op2 ] =
   augmentation collections with iter augment. Stage-prep en-                   CalcG[op2 ] ◦ CalcG[op1 ], which is what makes Theorem 5.1 hold.
   riches and re-lenses the result to the target’s behavioral class                A pipeline is grain-correct when the data it produces lands at
   (declare-⟨bc⟩); and target-load writes it with a BC-dispatched               exactly the intended level of detail: for every source, the grain of
                                                                           13
its output collection equals the target’s declared grain 𝐺 [Target].             as the witness on purpose: that 𝑅 ≡𝑔 𝐾 holds for some isomorphism
This is a semantic property of the pipeline’s output—the one a                   is weaker—an arbitrary surjection between grain-equivalent types
fan trap or a missing aggregation violates (§1)—yet, by the grain                need not be injective; it is 𝑘 itself being the isomorphism that yields
homomorphism (§3), it is decidable without running the pipeline.                 injectivity.)
Theorem 6.1 (Data-independent grain correctness [14]). A                            Proof sketch. (1)⇒(2) is immediate: injective on the type 𝑅
pipeline pip : Pipeline (𝐶 Source) (𝐶 Target) is grain-correct iff               implies injective on the elements of every collection. (2)⇒(1), con-
CalcG[pip] (𝐺 [Source]) = 𝐺 [Target]. The check operates entirely on             trapositively, turns a type-level collision 𝑘 𝑟 1 = 𝑘 𝑟 2 with 𝑟 1 ≠ 𝑟 2
the type-level schema and its declared determinations—foreign keys               (whose grains differ by Grain Uniqueness [14]) into a two-element
and declared grains, which are metadata, not data—so it needs no                 collection on which 𝑘 is no superkey. (1)⇔(3): a surjection is injec-
data access; CalcG is total and decidable, running in 𝑂 (|𝑉 | · 𝑘) time          tive iff it is a bijection, so 𝑘 injective on 𝑅 coincides with 𝑘 being
on a DAG of |𝑉 | operations with fan-in 𝑘.                                       an isomorphism 𝑅  𝐾 (clause (3)), whence 𝑅 ≡𝑔 𝐾. Minimality is
    Running example. For the customer-order pipeline—order                       the Grain Inference Theorem’s irreducibility condition [14]. Full
events (grain CustomerId × OrderDtm) joined to customers and                     proof in Appendix A.                                                 □
products, then aggregated to a per-customer summary (grain                       Remark 6.3 (The quantifier is enforced, not observed). Clause (2)
CustomerId)—CalcG threads the grain through the chain: delta                     cannot be checked against data: a finite collection can always be
preserves CustomerId × OrderDtm; lookup on products preserves                    filtered until a proper sub-projection becomes a key (a given collec-
it (grain-ordered, no fan-out); groupby-ek sets it to CustomerId;                tion may key on less than the grain)—a key is not inferable from
upsert preserves it. The computed grain CustomerId equals the                    any single instance, which is why relational systems enforce keys
target’s declared grain, so the design is grain-correct—established              as declared constraints rather than infer them. Here the quantifier
before any data is read. Had the designer used lookup-low                        is discharged at the type level, never empirically—the grain is in-
(fan-out) or omitted the grouping, CalcG would report a grain                    jective on 𝑅 by construction (§3)— and, for the re-graining below,
mismatch, the signature of a double-counting or row-multiplication               only over the collections a preceding operation actually produces,
bug.                                                                             on which that operation’s postcondition guarantees the key. The
                                                                                 pipeline is the enforcer; the type-checker is the auditor.
6.2    Layer 2: Behavioral-Class Correctness
       (Compile Time)                                                            Corollary 6.4 (Design-Time Sound Re-Grain). declare-⟨bc⟩ 𝑘
                                                                                 re-declares its input at grain 𝐾 and class ⟨bc⟩ under the precondi-
Each operation declares its behavioral-class constraint as a type
                                                                                 tion that 𝑘 is a key of every input; by Theorem 6.2 this makes 𝐾
parameter, and the type checker enforces it: a delta on an IsEntity
                                                                                 the grain of the re-declared type Res. Hence for any PDA pipeline
collection, or an append to an IsEntity target, is a type error. Non-
                                                                                 𝑡 : 𝐶 𝐴 → 𝐶 𝐵—one operation or arbitrarily many—whose con-
canonical reads must go through the explicit converter pattern
                                                                                 tract guarantees that 𝑘 is a key of 𝑡 𝑐 for every 𝑐, the composition
(§4.4). By the BC-preservation principle, grain correctness already
                                                                                 𝑡 >> declare-⟨bc⟩ 𝑘 is sound by construction: 𝑡’s postcondition
implies BC preservation wherever grain is preserved, so this layer
                                                                                 discharges the precondition on every collection 𝑡 produces, the type-
adds only the cases where BC is deliberately changed—and those
                                                                                 checker verifies the composition at design time, and the result denota-
are caught at compile time, for free.
                                                                                 tion is (𝐺 [] = 𝐾, 𝐵𝐶 [] = ⟨bc⟩, 𝐸𝐾 [] derived from 𝐾)—with no data
6.3    Sound Re-Graining: From Collection Keys to                                read.
       Type Grain                                                                   Proof sketch. The precondition makes the input grain-unique
The deliberate grain/BC changes of Layer 2 are the declares                      at 𝐾, so by Theorem 6.2 𝐾 is its grain; and since the re-lens does no
declare-⟨bc⟩ of §4.7: each re-lenses a collection, declaring a                   data action—dropping and choosing nothing—declaring 𝐺 [] = 𝐾
new grain 𝐾 and behavioral class ⟨bc⟩. A re-lens carries no data                 is sound. 𝑡’s postcondition supplies the key on every collection
operation; it is sound exactly when the data already keys on 𝐾.                  𝑡 produces, discharging the precondition over the image, so the
Pinning down “keys on 𝐾” needs a bridge between the collection                   composition type-checks with no premise depending on data; the
level, where keys are observed, and the type level, where grain lives.           result denotation is the one declare-⟨bc⟩ declares. Full proof in
Throughout, 𝑘 : 𝑅 ↠ 𝐾 is a field-set projection (the double-headed               Appendix A.                                                         □
arrow ↠ denotes a surjection: 𝐾 retains a subset of 𝑅’s fields, so 𝑘
                                                                                    Why a key, and what Res is. Minimality is mandatory, not a re-
is onto 𝐾). Call such a 𝑘 a superkey of a collection 𝑐 : 𝐶 𝑅 when it
                                                                                 finement: a bare superkey gives only grain-equivalence (𝑅 ≡𝑔 𝐾
is injective on the elements of 𝑐, and a key when it is moreover
                                                                                 with 𝐺 [𝐾] ⊂𝑡 𝑦𝑝 𝐾), under which the contract’s claim 𝐺 [Res] = 𝐾
minimal—no proper sub-projection of 𝑘 is still injective.
                                                                                 would be false. The re-lens performs no data action—it neither ag-
Theorem 6.2 (Universal Superkey is the Grain). For a field-set                   gregates nor selects—so it drops and merges nothing, type-checking
projection 𝑘 : 𝑅 ↠ 𝐾 (so 𝑘 is surjective), the following are equivalent:         exactly when a witness establishes the precondition. And because
(1) 𝑘 is injective on the type 𝑅; (2) 𝑘 is a superkey of every collection        no data is touched, Res keeps the input’s schema (Schema(Res) ≡
𝑐 : 𝐶 𝑅; (3) 𝑘 is itself grain-preserving—a grain isomorphism 𝑅                 Schema(𝑅)) yet carries a different denotation ([[Res]] ≠ [[𝑅]]); since
𝐾 witnessed by 𝑘, whence 𝑅 ≡𝑔 𝐾. Moreover 𝐾 is a grain of 𝑅                      identity in denotational design is semantic—𝐴 = 𝐵 ⇐⇒ [[𝐴]] =
(irreducible, 𝐺 [𝐾] = 𝐾) iff no proper sub-projection of 𝑘 satisfies (1)–        [[𝐵]] [10]—Res is a distinct grain-theoretic type, the same structure
(3)—minimality is type-level, not per-collection. (Clause (3) names 𝑘            re-lensed to a new grain and class, not an isomorphic alternative
                                                                            14
grain of 𝑅 (the CustomerEntity-vs-CustomerMVersion distinction                 Table 12: Collection relations (the complete family). sel-ek
of Part I [14]).                                                               is the entity-key projection, Gr(𝑐) = {grain 𝑒 | 𝑒 ∈ 𝑐} its set of
                                                                                                               ∼
                                                                               grain values, and 𝑓 : GetG 𝑐 1 −
                                                                                                              → GetG 𝑐 2 a grain isomorphism
   The postcondition is all that matters. Not which operation, nor             witnessing GetG 𝑐 1 ≡𝑔 GetG 𝑐 2 ; 𝑓 [Gr(𝑐 1 )] = {𝑓 (𝑣) | 𝑣 ∈ Gr(𝑐 1 )}
how long the pipeline: checkout (one version per entity), pick                 is the image of a set under 𝑓 . Because grain is a superkey
(one row per partition key), or any pipeline ending in such a step             (the grain projection is injective; §3), a collection is deter-
all supply the key. This is exactly the IsMultiVersion → IsEntity              mined by Gr(·), so =𝑔 may compare grain-value sets rather
re-grain of §4.7 (checkout >> declare-entity >> sel-safe),                     than elements. ⊇𝑔 is grain generalization—a partition into
where checkout’s postcondition supplies the key and the                        specializations. The key predicates take a field-set projection
declare-entity re-lens is the type-level move the corollary                    𝑘 : 𝑅 → Key on the left and a collection on the right; IsKeyOf
justifies. When 𝑘 is not a key of the input, the re-lens does not              adds minimality, and the grain projection is always a key
apply—collapsing then requires choosing a representative, the                  (§3). The equality/subset blocks run strongest to weakest:
job of group-by (which aggregates) or pick (which selects by a                 =𝑐 ⇒ =𝑔 ⇒ =𝑒𝑘 (and =𝑔 ⇒ =# ), ⊆𝑐 ⇒⊆𝑔 ⇒⊆𝑒𝑘 .
declared ordering), not of a re-lens.
                                                                                   Relation             Definition
   Stricter target classes. Beyond the grain, a stricter target class
carries its own structural invariant (e.g. consecutive versions differ,            𝑐 1 =𝑐 𝑐 2           ∀𝑒 ∈ 𝑐 1 . 𝑒 ∈ 𝑐 2 ∧ ∀𝑒 ∈ 𝑐 2 . 𝑒 ∈ 𝑐 1
for IsMultiVersion) as a further precondition on the re-lens, dis-                 𝑐 1 =𝑔 𝑐 2           GetG 𝑐 1 ≡𝑔 GetG 𝑐 2 ∧ 𝑓 [Gr(𝑐 1 ) ] = Gr(𝑐 2 )
charged the same way—by a preceding operation’s postcondition,                     𝑐 1 =𝑒𝑘 𝑐 2          sel-ek 𝑐 1 =𝑔 sel-ek 𝑐 2
                                                                                   𝑐 1 =# 𝑐 2           |𝑐 1 | = |𝑐 2 |
at the type level.
                                                                                   𝑐 1 ⊆𝑐 𝑐 2           ∀𝑒 ∈ 𝑐 1 . 𝑒 ∈ 𝑐 2
                                                                                   𝑐 1 ⊂𝑐 𝑐 2           𝑐 1 ⊆𝑐 𝑐 2 ∧ ¬(𝑐 2 ⊆𝑐 𝑐 1 )
6.4    Layer 3: Domain Correctness                                                 𝑐 1 ⊆𝑔 𝑐 2           ∃𝑃 . filter 𝑃 𝑐 2 =𝑔 𝑐 1
The third layer covers business rules beyond grain and BC. Its                     𝑐 1 ⊆𝑒𝑘 𝑐 2          ∃𝑃 . filter 𝑃 𝑐 2 =𝑒𝑘 𝑐 1
constraints are not opaque predicates: they are drawn primarily                                          Ó                Í
                                                                                   𝑐 ⊇𝑔 {𝑐𝑖 }𝑖=1
                                                                                             𝑛
                                                                                                            𝑖 𝑐 𝑖 ⊆𝑔 𝑐 ∧    𝑖 |𝑐 𝑖 | = |𝑐 |
from a structured vocabulary—the collection relations of Table 12—in
three scopes: element (∀𝑒 ∈ 𝑐. 𝑃 𝑒), collection (a predicate over one              𝑘 IsSuperKeyOf 𝑐     ∀𝑒 1 , 𝑒 2 ∈ 𝑐. 𝑘 𝑒 1 = 𝑘 𝑒 2 ⇒ 𝑒 1 = 𝑒 2
collection, e.g. grain-uniqueness), and cross-collection (a predicate              𝑘 IsKeyOf 𝑐          𝑘 IsSuperKeyOf 𝑐 ∧ 𝑘 minimal
relating several, e.g. a foreign key). The constraints that matter most
are these relations: a foreign key is a subset (⊆), and uniqueness is a
grain-key (IsKeyOf—equivalently a superkey; the grain projection
is always one, §3). Their implication hierarchies (=𝑐 ⇒=𝑔 ⇒=𝑒𝑘 ;
⊆𝑐 ⇒⊆𝑔 ⇒⊆𝑒𝑘 ) express strictness gradations a single first-order                  Data-dependent constraints (specification + generated query).
predicate cannot—the same FK at three strengths (identical values,             What is left—foreign-key integrity on values, value ranges, partition
up to grain isomorphism, up to entity key). Arbitrary first-order-             counts, and arbitrary business predicates—genuinely depends
logic predicates enter only as an escape hatch, for business rules             on the data. PDD specifies these primarily through the collection
that reduce to no relation. This choice is not cosmetic—it is the              relations—a foreign key as an asserted subset ⊆, uniqueness as
crux of the layer’s cost. Only a relation can be free: a property a            a grain-key IsKeyOf—and, for business rules that reduce to no
contract guarantees as a collection relation is discharged at zero             relation, as arbitrary first-order-logic predicates (the escape hatch).
cost, at design time, whereas a raw first-order predicate is always            All are carried as a (Pre, Intra, Post) triple, type-checked for well-
specification-time—it generates a boundary query regardless. The               formedness and composed through the proof-carrying operator
collection relations are therefore not an alternate encoding of the            >>>, which discharges each Post𝑛 ⇒ Pre𝑛+1 obligation at composi-
same FOL predicates; they are precisely the fragment the pipeline’s            tion time (intermediate obligations that are contract-derivable are
own contracts discharge for free, so stating a constraint relationally         inherited as axioms, so the engineer proves only what is genuinely
is what draws it onto the zero-cost, code-correctness side of the              new). This discharge is itself design-time: the >>> obligations
line rather than the data-quality side (§6). Domain correctness                are type-level, settled before any data flows, so the pipeline is
accordingly splits by cost.                                                    correct by construction given its preconditions, and what genuinely
                                                                               depends on data is only whether the inputs satisfy the resulting leaf
    Contract-derivable constraints (zero cost). Many collection-level          preconditions—a data-quality question. This full discharge is the
relations follow from operation contracts alone, by structural in-             proof-backed reading: collapsing every intermediate obligation to a
duction over the pipeline—no data required. A pipeline built from              leaf precondition requires actually proving the Post𝑛 ⇒ Pre𝑛+1
captures automatically produces a subset of its input (⊆𝑐 , hence ⊆𝑔           entailments, which the dependently-typed realization (PDL)
and ⊆𝑒𝑘 ) with bounded cardinality; an apply’s result differs from its         does mechanically (§6.7). The deployed /pdd checker discharges
before-state by exactly its source; grain-type equivalence ≡𝑔 follows          the structural layers but does not prove these entailments; it
wherever CalcG shows grain preservation; and because the grain                 emits a verification query at each node where a data-dependent
projection is always a key (§3), grain-uniqueness (grain IsKeyOf 𝑐)            constraint is declared. Either way the constraint is not a hole in
is free as well. These extend the zero-cost guarantee beyond grain             code correctness but a data-quality control point—at the input
and BC at no specification cost.                                               boundary under a proof, at each declaring node otherwise.
                                                                          15
   Collection relations and referential integrity. The constraints              Theorem 6.6 (Pipeline Correctness). Let
above draw on a small algebra of collection relations (Table 12)
                                                                                                 pip : Pipeline (𝐶 Source) (𝐶 Target)
grading how two collections correspond—by elements (=𝑐 , ⊆𝑐 ), by
grain up to isomorphism (=𝑔 , ⊆𝑔 : the same data under different                carry a constraint specification (Pre, Intra, Post): Pre a precondition
schemas, e.g. CustomerId ↔ Username), or by entity (=𝑒𝑘 , ⊆𝑒𝑘 :                 on the source, Post the target property (its grain, behavioral class,
the same entities at possibly different grains, e.g. a multi-version            and domain predicates), and Intra the stateful condition of any apply.
history and its current state). These grade referential integrity: the          If (i) pip is BC-well-typed, (ii) CalcG[pip] (𝐺 [Source]) = 𝐺 [Target],
foreign key “𝑐 1 ’s FK column is contained in 𝑐 2 ’s grain” is strict           and (iii) composition discharges every internal obligation Post𝑖 ⇒
under ⊆𝑐 (keys match by value), a grain FK under ⊆𝑔 (match up                   Pre𝑖+1 , then for every source collection 𝑐,
to representation—a DeptID resolves against a DeptSlug-keyed
                                                                                                 𝑐 |= Pre =⇒ pip 𝑐 |= Post ∧ Intra,
table), or an entity-key FK under ⊆𝑒𝑘 (an event stream’s keys
resolve against the entity table despite a finer grain). The hierarchy          and this implication is established with no data access. The sole data-
grades strictness; cost is a separate axis, set by provenance. A ⊆              dependent obligation is whether 𝑐 |= Pre—a data-quality check at the
that an operation’s contract guarantees—a capture’s output ⊆𝑐 its               input boundary, not a property of the pipeline’s code.
input, with the implied ⊆𝑔 /⊆𝑒𝑘 —is contract-derivable and free at
every level. A ⊆ asserted between independent collections—any                      Proof sketch. The conclusion conjoins the three layers, each
FK constraint, strict or up-to-isomorphism—is data-dependent                    discharged statically. Grain: by Theorem 6.1, (ii) forces the output
and compiles to the anti-join of §6.5. Uniqueness (IsKeyOf) and                 grain to equal the target’s, data-independently. Behavioral class: (i)
generalization/partition (⊇𝑔 ) grade the same way: free when an                 is decided by the type checker. Domain: the specification composes
operation’s contract establishes the key or partition (a groupby                by structural induction over the pipeline DAG—each operation
makes its grouping projection a key, a pick its partition projection),          is correct against its own contract, Preop ⇒ (Postop ∧ Intraop ),
data-dependent—and compiled to a grouping query—when asserted                   true by the operation’s denotation, and the obligations (iii) chain
of independent data.                                                            these so the leaf Pre entails the target Post; contract-derivable
                                                                                intermediate obligations are inherited as axioms (§6.4). All three
6.5    From Specifications to Verification Queries                              discharges are type-level, so the entailment holds with no data
A well-formed FOL predicate has syntactic structure that compiles               read. Proved in the semantic domain, it transfers to the concrete
mechanically to a verification query in SQL or PySpark: ∀𝑟 ∈ 𝑐. 𝑃               run by the grain homomorphism (§3), and each domain predicate’s
becomes SELECT * FROM c WHERE NOT (P), FK(𝑐 1, 𝑓 , 𝑐 2 ) becomes                runtime check is faithful to its specification by Theorem 6.5. Full
an anti-join, Unique(𝑐, 𝑓 ) a GROUP BY . . . HAVING COUNT(*)>1,                 proof in Appendix A.                                                □
and so on. Each query is designed to return the empty set exactly
                                                                                Theorem 6.6 is the unified-correctness predicate of the Agda PDL
when its predicate holds.
                                                                                encoding (§10). It is what makes “settled at design time” precise:
Theorem 6.5 (Compilation correctness). For every well-formed                    the implication Pre ⇒ Post is pure code analysis, and the only
predicate 𝑃 and its compiled query 𝑄 (𝑃),                                       data residue is the input-boundary check of §6.7—data quality, not
                                                                                code correctness. The one further obligation, that the executable
             𝑃 holds ⇐⇒ 𝑄 (𝑃) returns the empty set.
                                                                                faithfully realizes the design, is discharged by the grain homomor-
Because the compilation is structural recursion over the predicate              phism (Thm. 6.5), again without reading data. Note too that the
syntax, there is no manual translation step at which the test can drift         theorem is stated against the design’s declared Post: it guarantees
from the specification.                                                         the pipeline computes what its specification says, not that the spec-
                                                                                ification captures intent—the latter is what the human reviews on
This closes the loop. The pipeline architect writes the design and its
                                                                                the design.
constraints once; the design’s correctness is checked from structure
alone, at zero cost; and the only runtime artifacts—the data-quality
                                                                                6.6    Prevention, Not Detection
checks the data engineers actually run—are generated from the
same specification, guaranteed by Theorem 6.5 to test exactly what              The three layers do more than verify a finished design; they make
was specified. Putting the layers together, a pipeline is correct by            whole classes of bug unrepresentable—the discipline of making ille-
construction when CalcG[pip] (𝐺 [Source]) = 𝐺 [Target] (grain),                 gal states unrepresentable [19], where a property carried by the type
the design is BC-well-typed (BC), and the domain triple holds                   system is not a test that might fail but a state that cannot be written.
(domain)—all three established at design time given the inputs’                 The mechanism is the behavioral class: it fixes, at the type level,
preconditions, eliminating double counting, spurious join records,              which reads and writes are well-typed and at what grain. Temporal
grain mismatches, and BC violations by construction rather than                 reads are gated by the class—checkout, the current-version read,
by testing. The full constraint language and its mechanization in               requires IsMultiVersion—and collapsing a collection to a coarser
Agda PDL are in-progress (§10); the FOL→SQL generator is already                grain requires a key that only such a read establishes. We make
implemented in PDD-Toolchain (§7).                                              this concrete with two real bugs, each a costly silent error that
   The three layers together formalize the paper’s organizing                   ships through tests, and each the same omission: using a versioned
principle—a pipeline’s correctness is a property of its code, settled at        (IsMultiVersion) collection without the checkout its canonical read-
design time—as a single data-independence theorem.                              ing demands. One is on the read side, one on the write side; in both,
                                                                                the wrong design is caught at design time—by /pdd today, on any
                                                                           16
 -- Dim : IsMultiVersion   (grain EK x FromDtm)                               Table 13: The same versioning bug under four development
 -- a current-state lookup needs Dim at entity grain                          modes. Only a typed design prevents it; the others can at best
 -- WRONG: re-lens an all-versions read to entity grain
 dimEnt = dim |> full |> declare-entity ek
                                                                              detect it, and only with the exact triggering data and the exact
 --   declare-entity needs ek IsKeyOf input;                                  verification query.
 --   a full read has many versions/entity -> unmet
 -- RIGHT: checkout makes ek a key (one current row
 --   per entity), discharging the precondition                                     Development mode       Artifact the engineer      Prevented?
 dimEnt = dim |> checkout t |> declare-entity ek                                                           controls
                                                                                    jump-in-and-code       code only                      no
Figure 3: Read side. full reads all versions; presenting the                        NL spec →              prose, silent on version       no
dimension at entity grain needs the re-lens declare-entity,                         implement (human       grain
whose key precondition (ek IsKeyOf input) only checkout—                            or LLM)
the canonical IsMultiVersion read—discharges. /pdd flags the                        black-box agentic      nothing reviewable             no
missing checkout at design time; in the dependently-typed                           codegen
                                                                                    PDD (typed design)     typed design                   yes
PDL the unmet precondition makes the all-versions design
                                                                                                           (IsMultiVersion)
ill-typed.

 -- stg: one row per line item; each file re-sends
 -- an order's COMPLETE line-item set
 -- WRONG: treat each line item as its own event                              line item, the tempting design keeps the latest file per line item—but
 snap = reads |> pick {lineKey} file DESC
 -- latest file PER LINE ITEM; a dropped line is                              a dropped line item is still the latest for itself, so it is never deleted
 -- still "latest for itself" => never deleted                                (Fig. 4, top). The fix is to state the input’s true semantics: each file
 -- RIGHT: the file versions the ORDER                                        is a new version of the order, not the line item. Typed that way, the
 snap = reads
    |> groupby-multiversion {orderKey} {file}                                 algebra reconstructs the order version (groupby-multiversion),
                            {lines = collect(*)}                              checkouts the latest file per order, and explodes back to line-item
    |> checkout now      -- latest file per order
    >> explode lines     -- back to line-item rows
                                                                              rows—dropping the deleted one by construction (Fig. 4, bottom).
                                                                              This sharpens the principle: a behavioral-class label is necessary but
                                                                              not sufficient; declaring the input IsEvent type-checks yet still ad-
Figure 4: Write side. Keeping the latest file per line item (top)             mits the wrong pick. Only the right class and grain—IsMultiVersion
never deletes a dropped line item. Typing the input as IsMul-                 at the order grain—forces the correct checkout.
tiVersion at the order grain forces an order-level checkout
(bottom) that drops it by construction.                                           Prevention versus the detection lottery. Each bug is invisible to
                                                                              today’s defenses. It produces a wrong result only on a specific data
                                                                              pattern—a historical-only address, a line item dropped between two
pipeline, and ruled out by the type level itself in the dependently-          files—that sampled tests rarely contain, and a runtime check catches
typed PDL (§6.7).                                                             it only if someone already suspected the versioning and wrote ex-
   Example 1: an over-broad read. A pipeline maintains an SCD2                actly that assertion. Prevention depends on neither coincidence—
customer dimension Dim (IsMultiVersion, grain CustomerKey ×                   and the alternative is demonstrably unreliable. Under the code-first
EffectiveDt). To find the customers affected by a changed address—            status quo both bugs were committed by experienced data engineers
the address carries no customer key—it looks the address up against           working without a denotational design; and, given the same inputs
Dim and UNIONs the matched keys into the upsert delta. The natural            (the natural-language specification and schemas) but no design,
code reads all versions of Dim, so an address that belonged to a past         both were reproduced by a frontier model, Anthropic’s Opus 4.8
version of a customer still matches and emits a spurious key; the tar-        (1M-context). Neither human expertise nor model capability sub-
get then accrues bogus new versions. (The UNION is a red herring—it           stitutes for the design step. Table 13 contrasts the development
is correct; the emitted key is a distinct wrong inclusion, not a du-          modes: ad-hoc coding, a natural-language spec implemented by a
plicate to collapse.) PDD prevents this by grain: the lookup needs            human or an LLM, and black-box agentic codegen all can ship the
Dim at entity grain (one current row per customer), reached only              bug, whereas a typed design makes it unrepresentable.
through the re-lens declare-entity, whose precondition—that
the customer key is a key of its input—holds only after checkout              6.7    The Verification Spectrum: Two Realizations
collapses each customer to its current version. An all-versions read                 of the Checker
cannot discharge it: /pdd flags the missing checkout at design time
                                                                              The three layers describe what must hold; they do not fix how
on any pipeline, and in the dependently-typed PDL the unmet pre-
                                                                              strongly it is established. That is a separate axis—software engineer-
condition makes the design ill-typed by construction (Fig. 3, §6.7).
                                                                              ing’s tests–types–proofs spectrum (§10)—and the same PDD design
checkout is the canonical read for IsMultiVersion.
                                                                              can be checked at more than one point on it, because the “checker”
   Example 2: a missed deletion. A source re-sends, in every file, an         of §1 is a role, not a fixed tool. PDD-Toolchain realizes that role
order’s complete set of line items; a line item removed upstream sim-         two ways (Table 14), and the choice is monotone: the richer the type
ply stops appearing, with no delete record. Flattened to one row per          system, the less is left for runtime.
                                                                         17
Table 14: Two realizations of the checker on one PDD design,                  the pipeline, a cost the deployed checker instead pays per node.
against the runtime-test baseline. The residue shrinks mono-                  And one obligation is not data quality at all: that the executable
tonically as assurance strengthens: structural obligations fall               faithfully realizes the design under the non-determinism the se-
to design-time typing, data-dependent obligations fall to a                   mantic domain abstracts away—evaluation order, non-associative
machine-checked proof, and only the untyped-input bound-                      floating-point reduction—which the grain homomorphism (§3) and
ary is irreducible.                                                           compilation-correctness (Thm. 6.5) govern, not a boundary query.
                                                                              Within those bounds PDL does more than raise assurance from
   Checker           Code-correctness       Runtime residue                   reviewed to machine-checked; it shrinks the runtime footprint from
                     assurance                                                a check at every node to a single check at the boundary.
   tests (ad-hoc +   none—run and inspect   a query per node, for                 Across both realizations the artifact the human consumes is a cer-
   DQ tools)         outputs                everything                        tificate—a machine-checked proof (PDL) or an evidence ledger (the
   /pdd (types;      grain + BC +           data-dependent checks             deployed checker)—so verifying a design reduces to checking that
   deployed)         contract-derivable,    (FK, ranges, business             certificate, a cheap and delegable act. Validating the specification
                     discharged at design   rules), per node                  itself—that its target denotation and business predicates capture
                     time as AI-reviewed                                      intent—remains the one irreducibly human task (§1); it is where a
                     evidence                                                 proof, silent on the property one forgot to state, cannot help.
   PDL (proofs;      all layers, business   input boundary only
   Agda/Lean 4)      predicates included,
                     machine-checked                                          7   PDD-TOOLCHAIN
                                                                              The methodology of §§4–6 is realized end-to-end by PDD-Toolchain,
                                                                              a design-first system in production use. It has three cooperating
                                                                              components plus the human workflow that ties them together.
    At the runtime-test end, every obligation is a query against mate-
rialized data—one or more per DAG node, in the manner of dbt’s per-              Design and verification. The design tool (a Claude skill, /pdd)
node tests [7]. The /pdd checker moves the structural obligations—            takes the source and target data semantics (𝐺 [·], 𝐸𝐾 [·], 𝐵𝐶 [·])
grain, behavioral class, and the contract-derivable constraints—to            and produces a PDD design—a formal specification of the pipeline,
design time, discharging them into an evidence document and leav-             expressed in the PDA operator algebra. It discharges grain cor-
ing only the genuinely data-dependent constraints (FK integrity,              rectness with CalcG, BC correctness by typing, and the contract-
value ranges, business predicates) as generated queries (§6.5). At the        derivable domain constraints automatically; it emits the remaining
dependent-types end, PDL—the Pipeline Design Language, an em-                 data-dependent obligations as FOL predicates compiled to SQL
bedding of PDA and its constraint logic in Agda/Lean 4—lifts even             verification queries (Thm. 6.5); and it produces a human-readable
those predicates to types: a value violating a precondition cannot            evidence document recording every CalcG step, BC check, derived
be constructed, so a design that type-checks carries a machine-               constraint, and generated query. It is the source of this paper’s
checked proof that its output meets grain, behavioral class, and the          zero-cost verification and auto-generated queries.
business predicates. The type-checker is the proof, discharged by
recompiling (agda –safe).                                                        EDB — the executable target. The Executable Design Builder
    Two points sharpen what the proof end buys. First, the residue            (EDB) is a typed PySpark framework of 90+ reusable operations
never vanishes: a deployment engine (Databricks, Snowflake, Big-              implementing the PDA catalog (delta, cdc, checkout, augment,
Query) ingests untyped external data, so the typed preconditions              lookup, sel-*, append/upsert/commit-upsert, SCD2, hashing,
cannot be enforced on the inputs; they must be checked, which                 validation). Because each EDB operation carries its PDA contract,
is the input-boundary query the executable design emits (PDLC                 a correct design maps to correct code one operation at a time, and
Step 3, §2.3). A proof establishes “if the inputs meet their precondi-        grain/BC correctness “falls out” of one-line typed calls. This 1:1
tions then every downstream collection is correct”; the boundary              PDA→EDB correspondence is what makes the EDB program an
query checks the antecedent. Second, the proof is what collapses the          executable design (§2.3)—an implementation whose meaning equals
residue to that boundary. For a deterministic design this backward            the design’s by the homomorphism (§3)—and shows that PDA is
propagation is always available: a target predicate 𝑃 on the output           realizable on a production engine.
is, verbatim, a predicate on the inputs—namely 𝑃 precomposed with
the pipeline’s denotation [[pip]]—so the proof-carrying composi-                 Code generation — design to deployment. A family of Claude
tion (§6.4) rewrites each per-node constraint into a condition at             skills (/build-ddl, /build-pip, /build-jobs) compiles a PDD
the input. The per-node data-quality queries the deployed checker             design into the executable design: DDL, a faithful EDB implementa-
emits—potentially hundreds across a large DAG, one or more per                tion plus its validation queries, and deployable job bundles (PDLC
transformation output—are then entailed by the boundary check                 Step 3). The human verifies the design; the agent generates the code;
and become formally redundant: with the inputs verified, every                the generated queries verify the data. This is the answer to “who
intermediate and target node is correct by the proof. Two honest              verifies AI-generated pipelines?”—the design is the artifact a human
caveats. What collapses is the residue’s location, not always its             can check and an agent can faithfully compile. Operational tuning
cost: for an emergent constraint—one with no local pre-image on               for performance, cost, and scale (PDLC Step 4) is then applied as
the source, e.g. a per-group sum bound—the boundary predicate                 semantics-preserving rewrites (§5), preserving the guarantees by
is that aggregation and is no cheaper to check than recomputing               construction.
                                                                         18
   Deployment context and reproducibility. PDD-Toolchain is in pro-            RQ6
duction use on an enterprise data-engineering program—not a proof                    What are the developer-effort and code-size deltas versus
of concept—where the design-first workflow builds a portfolio of                     ad-hoc and LLM-without-design baselines?
pipelines across a three-layer (landing / integration / serving) archi-        RQ7
tecture over many heterogeneous source systems. We treat deploy-                     What does a fully mechanized PDL design establish beyond
ment figures purely as context, never as measured results: reported                  the deployed /pdd checker, and by how much does the proof
build-step speedups, for instance, are bounded end-to-end by the                     collapse the runtime residue (per-node data-quality checks →
non-coding share of delivery (requirements analysis, data access,                    a single input-boundary check)?
review, governance), so a large local speedup is a modest end-to-end
one—the measured results are the controlled study of §8. Because
the executable-design framework is proprietary, the reproducible               8.2    Case Studies, Arms, and Protocol
artifact accompanying this paper is the method’s outputs—formal
                                                                                  Case studies. We use five sanitized production case studies cho-
designs, evidence documents, generated verification queries, and
                                                                               sen to span three diversity axes—pipeline pattern, target behavioral
the PDL/Agda mechanization—rather than the engine itself.
                                                                               class, and modeling paradigm (Table 15)—demonstrating breadth
                                                                               across the space where correctness matters, not grain alone. Four
8     EVALUATION DESIGN                                                        already exist as PDD designs with evidence documents (Landing-
This preprint fixes the methodology and the evaluation design; the             Vault, Dim2-Order, Ft-Order-Rev., Customer-Summary); a pure
measurement campaign is in progress and the quantitative results               Ingestion case completes the coverage matrix.
will appear in a later revision. This section states the central claim
under test, the research questions, and the three-arm protocol.
                                                                                  Three arms, two reference points. We build each pipeline unit
                                                                               three ways with an agent. Arm A (with PDD, deployed): the de-
   We evaluate the central claim of the paper—most pipeline correct-           sign is produced and checked by the /pdd tool, which emits an evi-
ness is dischargeable at design time at zero cost, leaving only data-          dence document over grain, BC, and contract-derivable obligations;
dependent obligations as auto-generated verification queries—on real           we report Arm A for all five cases. Arm B (with PDD, proved):
production pipelines built with PDD-Toolchain. The evaluation asks             the design is mechanized in PDL (Agda), with grain, behavioral
whether the methodology delivers on three fronts: that it is broad             class, and one business predicate proved and no postulate on the
(multiple patterns, behavioral classes, and modeling paradigms, not            critical path, so that compilation is verification; we anchor Arm B
grain alone), that it prevents the defects agentic coding ships, and           on the running-example pipeline (Customer-Summary). Arm C
that its benefits are measured (defect capture, discharge, effort, and         (without PDD): the same LLM generates the pipeline directly from
faithfulness). The unit of analysis is a pipeline unit—one target table        natural-language requirements, with no formal design step. The
built by one pipeline.                                                         contrast C vs. A isolates the contribution of the design from the
                                                                               LLM’s coding ability—the central question of the paper—while B vs.
                                                                               A measures what the proof end of the verification spectrum (§6.7)
8.1    Research Questions                                                      adds over the deployed checker. Two further reference points locate
RQ1                                                                            these on the wider landscape: ad-hoc hand-written PySpark/SQL
      Does design-first catch correctness defects at design time               (the pre-PDD “before” state) and runtime-only data-quality tooling
      that ad-hoc and LLM-generated pipelines ship to runtime or               (Great Expectations/Deequ). A capability matrix (Table 16) shows
      production?                                                              that grain and BC defects are inexpressible in runtime DQ tools,
RQ2                                                                            independent of any counts.
      What fraction of a pipeline’s correctness obligations is dis-
      charged at zero cost (CalcG grain + BC typing + contract-
                                                                                  Ground truth and protocol. Defects are established two ways: a
      derivable constraints) versus requiring a data-dependent run-
                                                                               controlled seeded-fault catalog drawn from a fixed taxonomy (grain-
      time check?
                                                                               mismatch, BC-violation, fan/chasm-trap, missing-provider, non-
RQ3                                                                            unique join-key, FK-orphan, NULL-key, SCD2 temporal-overlap)—
      How many verification queries are auto-generated per                     several seeded from real documented design-time catches, including
      pipeline, and what classes of real defects do they catch on              the FK-augmentation fault classes catalogued in the case material
      production data?                                                         (fk-augmentation-pattern)—and historical bug mining of the pre-
RQ4                                                                            PDD tracker for the same domains. Each case is built under all
      Is code generation faithful—does the generated EDB code                  arms; defects are graded blind against the taxonomy by a rater
      preserve every correctness property asserted by the design?              unaware of which arm produced the artifact. We instrument the
RQ5                                                                            toolchain to emit a machine-readable obligation ledger (RQ2)—one
      How uniform are the resulting pipelines—what fraction of                 row per CalcG step, BC check, contract-derivable relation, and data-
      each pipeline’s operations is drawn from the shared pattern              dependent predicate, already latent in the evidence documents—tag
      vocabulary, and how small is the structural distance between             each generated query by constraint type (RQ3), and log the design-
      pipelines of the same pattern?                                           op→EDB-call trace plus a differential test (RQ4).
                                                                          19
Table 15: Case-study portfolio. Coverage spans patterns {In-                         9    BEYOND PIPELINES:
gestion, Staging-to-Landing, Augmentation, Aggregation},                                  CORRECT-BY-CONSTRUCTION QUERIES
behavioral classes {Entity, Event, MultiVersion, Snapshot},
and paradigms {Kimball, Data Vault, source-native}.                                  Nothing in PDD is specific to pipelines. A pipeline is a DAG of grain-
                                                                                     bearing transformations; a query is a single one—the one-node case.
                                                                                     CalcG verifies a whole DAG at design time (§6); a fortiori it verifies
  Case study          Pattern              Target BC            Paradigm
                                                                                     one query—indeed the fan trap that opened this paper (§1) is a query.
  Landing-Vault       Staging-to-Landing   Entity + Event       Data Vault           So the correctness the method establishes—output grain, behavioral-
  Dim2-Order          Augmentation         MultiVer. (SCD2)     Kimball dim
  Ft-Order-Rev.       Augmentation         Event (fact)         Kimball/DV           class-respecting reads, no spurious fan-out—applies unchanged to
  Customer-Summary    Aggregation          Entity               Kimball agg.         the queries an analyst, a BI tool, or an AI agent issues on top of the
  Ingestion (new)     Ingestion            MultiVer./Snap.      source-native
                                                                                     data assets a pipeline builds.
                                                                                         This has become urgent. The AI-enabled data stack now being
Table 16: Defect-class capability matrix: where each approach                        assembled across the industry—knowledge graphs and ontologies,
catches each defect class. D = design-time, R = runtime, “–                          semantic layers, and natural-language-to-SQL agents—turns a busi-
” = inexpressible.                                                                   ness question into a query automatically. These layers solve a real
                                                                                     problem: they tell an agent where to look and how to phrase a query
      Defect class              PDD    GE/Deequ        ad-hoc      LLM               in the organization’s vocabulary. But that is a different question
                                                                                     from correctness. A semantic layer certifies that a query is well-
      Grain mismatch             D          –            R          R
                                                                                     formed against the model; it does not certify that the query computes
      BC violation               D          –            R          R
      Fan/chasm trap             D          –            R          R
                                                                                     the intended number. An agent navigating an ontology can emit
      FK orphan                 D/R         R            R          R                SQL that is syntactically valid and semantically plausible yet logi-
      Value range / NotNull     D/R         R            R          R                cally wrong, and—run against live data—return a confident wrong
                                                                                     answer with no error raised. The guarantee the industry is racing
                                                                                     to deploy is one of fluency, not correctness.
8.3    Planned Analyses                                                                  The failure modes are the same grain and behavioral-class er-
The measurement campaign is in progress; per research question                       rors PDD prevents in pipelines, now on the read path. (1) The fan
we will report: RQ1 defect capture by phase (design-time vs. es-                     trap. Asked for total revenue alongside total units, an agent joins
cape to runtime/production) across arms, expecting PDD’s mass                        a revenue fact (one row per customer per order line) to a units
at the design phase and the no-design arm’s at runtime; RQ2 the                      fact (one row per customer per shipment) on customer id. The
per-layer obligation ledger (grain / BC / contract-derivable / data-                 grains are incomparable, so the join cross-multiplies over the un-
dependent) and the zero-cost ratio—counts already extractable from                   matched components: a customer with three order lines and four
the existing evidence documents; RQ3 generated-query yield by                        shipments yields twelve rows—revenue summed four times, units
constraint type and confirmed defects on production snapshots;                       three. The result lands at the requested (customer) grain and looks
RQ4 code-generation faithfulness via the design-op→EDB-call                          right; both totals are silently inflated. (2) The all-versions read. A di-
trace and differential testing; RQ5 pipeline uniformity—share of                     mension whose attributes change over time—a customer’s segment,
operations drawn from the shared pattern vocabulary and struc-                       a product’s list price—is correctly modeled as versioned records
tural edit-distance within a pattern; RQ6 developer-effort and code-                 with effective dates (an IsMultiVersion/SCD2 table) that must be
size deltas against the ad-hoc and no-design arms; and RQ7 the                       read at a point in time (a checkout). An agent that does not know
proof-anchor residue-collapse for Customer-Summary (per-node                         this reads every version: an entity revised mid-period appears more
data-dependent checks → a single input-boundary check). The ca-                      than once, its measures double-counted; join that table to a fact
pability matrix below (Table 16) is structural and independent of                    and each fact row matches every historical version, inflating counts
any counts: grain and behavioral-class defects are inexpressible in                  and sums in lockstep. Both are invisible to schema validation and
runtime data-quality tooling.                                                        to the semantic layer, because neither is a schema violation—each
                                                                                     is a grain/behavioral-class violation, exactly the layer of meaning a
8.4    Threats to Validity                                                           schema omits (§3).
                                                                                         Correct-by-construction at design time is the guarantee these
The case studies come from one enterprise domain; we mitigate
                                                                                     architectures lack. A query’s grain and behavioral-class correctness
with breadth across patterns, behavioral classes, and paradigms,
                                                                                     are decided from the schema denotations and the query’s structure
and argue the patterns are domain-independent. The no-design arm
                                                                                     alone (§6), so they can be settled before the query runs—the moment
(C) isolates the design’s contribution from the LLM’s coding ability.
                                                                                     it is generated, not after a human notices the numbers are too
Blind grading, an independently defined seeded-fault catalog, and
                                                                                     large. The same CalcG that types a pipeline types a query; the same
historical-bug cross-checks mitigate author-built bias. Faithfulness
                                                                                     behavioral-class discipline that forbids an unchecked versioned read
is checked by differential testing in addition to static tracing. Effort
                                                                                     in a pipeline forbids it in a query. PDD is, in this light, not merely
figures are reported only from measured timestamps and LOC;
                                                                                     a way to build correct data pipelines but a candidate correctness
the deployment numbers of §7 are clearly labeled as context. A
                                                                                     layer for the AI-enabled data architecture end to end—from the
sanitized artifact (designs, evidence documents, generated queries,
                                                                                     pipelines that build the data assets to the AI-generated queries
obligation ledgers, and the seeded-fault catalog) accompanies the
paper for reproducibility.
                                                                                20
that answer business questions over them. Realizing that layer—                schemas and instances as functors and give transformations a com-
extending the design tool and its verification to the query/semantic-          positional semantics; grain theory is complementary and deliber-
layer boundary, and evaluating it—is ongoing work; the point here              ately lighter, fixing a single computable invariant—the denotation
is that it demands no new theory, only the grain and behavioral-class          (𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅])—rather than a full categorical model, so in-
denotations this paper already computes.                                       ference stays a finite field-set computation. Data provenance [12]
                                                                               tracks where a value came from; grain tracks the orthogonal axis of
                                                                               at what level of detail it is represented—the axis on which double
10    RELATED WORK                                                             counting and fan traps live. None of these lines makes pipeline
   A spectrum: tests, types, proofs. Software engineering assures              correctness a design-time, type-level property; that is what PDD
correctness along a spectrum—runtime tests, static type checks,                contributes.
and machine-checked proofs [9]. Its type–proof end is one lineage:
a Hoare triple {𝑃 } 𝐶 {𝑄 } [13] states a program’s correctness relative
to a specification and discharges it compositionally; a refinement
type [22] folds the precondition into the type and has an SMT solver
discharge it automatically, trading expressiveness for push-button
checking; a dependent type (Agda, Lean 4 [9], F* [26], which spans                 Our position. PDD moves pipeline correctness leftward on that
both) lifts the restriction and asks the programmer for a proof term,          spectrum—from tests toward types and proofs—by making data se-
trading automation for full expressiveness. The axis is thus not only          mantics typeable: in the manner of denotational design [10], a type
how strongly correctness is established but at what automation–                carries its denotation (𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅]) [14], and operations
expressiveness trade-off. Data engineering today sits almost entirely          carry contracts propagated through composition—a Hoare-style
at the runtime-test end. Dataflow and orchestration frameworks                 {Pre} pip {Post} discipline [13] over collections, in which grain,
(Spark [28], Airflow [2], dbt), and streaming dataflow models [1, 3,           behavioral-class, and contract-derivable correctness are decided
5], execute pipelines but make no correctness guarantee about the              before any data is read. Crucially, PDD does not commit to a single
transformation itself; data-quality tools (Great Expectations [11],            point on the spectrum: it instantiates the correctness once and lets a
Deequ [23], dbt tests [7]) check assertions against materialized               team choose how strongly to discharge it by the pipeline’s criticality,
data at runtime. Because a schema captures only structure, these               complexity, and scale (§6.7). The deployed /pdd checker occupies
runtime checks are the only handle such systems have—and, run                  the automated, refinement-type-like middle [22]: grain inference
on sampled or partial data, they miss precisely the grain errors that          (CalcG) and behavioral-class typing are decidable, domain-specific
silently corrupt aggregates (§1); even property-based testing [16]             decision procedures—playing the role SMT plays for a refinement-
explores values, not grain semantics. Type-safe query construction             type checker, but purpose-built for grain, so the structural layers
(LINQ [18], Quill, Slick) pushes some checks to compile time, but              need no general solver at all. We do not leave the proof end as-
types over a relational schema still carry no notion of grain, entity,         pirational either: PDA and its constraint logic are embedded in
or behavioral class, so the errors that matter remain invisible to             Agda/Lean 4 as the Pipeline Design Language (PDL), a dependently-
them.                                                                          typed realization in which we mechanize a complete case-study
                                                                               pipeline end to end (§8), so the proof column of the spectrum is
   Semantic layers and AI-generated queries. Metrics and semantic              demonstrated, not merely cited; the full operation catalog is in
layers—dbt’s Semantic Layer and MetricFlow [8], and Malloy [17]—               progress. Because the denotation and CalcG are computed from
let teams declare dimensions, measures, and the grain of a metric,             schemas alone, the guarantee is universal over the operation set and
and are the closest industrial kin to “designing in a semantic do-             carrier (PDD Universality, §3): the same design-time verification
main.” But they model grain in order to generate consistent queries,           applies to a pipeline written in relational algebra, in PDA, or in the
not to verify a transformation: the declared grain is trusted, never           dataflow model’s windowing operators [1]—over a finite table or
checked against what a query actually computes, and the check is               an unbounded stream alike. PDD is thus a verification layer atop
neither data-independent nor decidable. In parallel, LLM text-to-              any grain-inferring algebra, where the frameworks above execute
SQL [15, 27] turns a natural-language question into a query directly;          pipelines but verify none. Crucially, this separates the two concerns
benchmarks reward execution accuracy on examples, not a guaran-                that runtime testing conflates: code correctness becomes a design-
tee that a generated query is grain-correct on all inputs. Both lines          time, type-level property (the Pipeline Correctness Theorem, §6),
answer where and how to query; neither answers whether the query               while runtime checks are confined to data quality—validating that
is correct—the grain and behavioral-class check PDD supplies at                inputs meet the design’s assumed preconditions. PDA brings to
design time, and the reason the method extends from pipelines to               data pipelines what Codd’s algebra [6] brought to ad-hoc data ma-
the queries that run over these layers (§9).                                   nipulation: a typed algebra in which correctness is structural, not
                                                                               a test result; PDD is the denotational-design discipline that com-
   Foundations: dependencies, categories, provenance. Grain ordering           poses it over the semantic domain. The resulting division of labor
is the type-level analogue of a functional dependency—a surjec-                is proof-carrying [20]: the untrusted generator ships a checkable
tion between grains lifts the determinacy that Armstrong’s ax-                 certificate—a machine-checked proof or an evidence ledger—and
ioms [4] give for attributes from columns to whole types (§3).                 trust reduces to validating the specification and checking the cer-
Category-theoretic models of databases—functorial data migra-                  tificate, never re-reading generated code at a scale no human can
tion [25], algebraic databases [24], and attributed 𝐶-sets [21]—treat          review.
                                                                          21
                                                                                                                                       ∼
11     CONCLUSION                                                                      the same as 𝑘 being an isomorphism 𝑅 −      → 𝐾 witnessed by 𝑘 itself
PDD answers “who verifies AI-generated pipelines?” by moving the                       (3); either way 𝑅  𝐾, hence 𝑅 ≡𝑔 𝐾. (This is why clause (3) must
verdict to design time: PDA makes well-typed composition grain-                        name 𝑘 as the witness rather than assert the bare 𝑅 ≡𝑔 𝐾: an
correct by construction, and the three-layer framework settles code                    arbitrary surjection between grain-equivalent types need not be
correctness before any data flows, at zero cost—the Pipeline Correct-                  injective—only 𝑘’s being the isomorphism gives injectivity.)
ness Theorem (§6): the structural layers are discharged with no data                       Minimality. Suppose 𝑘 satisfies (1)–(3), so 𝐾  𝑅. By defini-
access and a proof-carrying composition collapses what remains                         tion 𝐾 is a grain of 𝑅 precisely when it is moreover irreducible:
to a single input-boundary check, so a pipeline is correct by con-                     no proper subtype 𝐾 ′ ⊂𝑡 𝑦𝑝 𝐾 is isomorphic to 𝑅 (Grain Inference
struction against its specification, the only residue being whether                    Theorem [14], condition (iii)). Two observations rewrite this irre-
real inputs meet that precondition. Business rules enter as a fourth                   ducibility as a condition on 𝑘. First, since 𝑘 is a field-set projection
denotation, data constraints—first-order-logic predicates that prop-                   (𝐾 a subset of 𝑅’s fields), the proper subtypes 𝐾 ′ ⊂𝑡 𝑦𝑝 𝐾 are exactly
agate through the pipeline and compile to the only check that                          the images of the proper sub-projections 𝑘 ′ : 𝑅 ↠ 𝐾 ′ of 𝑘 (those
survives to runtime, an input-boundary data-quality test, generated                    retaining a proper subset of 𝐾’s fields): subtypes of 𝐾 and sub-
rather than hand-written. Correctness by construction is thus a dial,                  projections of 𝑘 correspond one-to-one. Second, by the equivalence
not a fixed point: the same design spans the tests–types–proofs                        (1)⇔(3) already proved, applied to 𝑘 ′ , such a 𝑘 ′ satisfies (1)–(3) iff
spectrum (§6.7)—from runtime queries, through the deployed /pdd                        𝐾 ′  𝑅. Composing the two, “some proper subtype 𝐾 ′ ⊂𝑡 𝑦𝑝 𝐾 is
checker (grain and behavioral class as decidable, domain-specific                      isomorphic to 𝑅” and “some proper sub-projection 𝑘 ′ of 𝑘 satisfies
decision procedures in place of a general SMT solver), to machine-                     (1)–(3)” are the same statement; negating, 𝐾 is irreducible—hence a
checked Agda/Lean 4 proofs—and a team chooses its point by a                           grain—iff no proper sub-projection of 𝑘 satisfies (1)–(3). The quan-
pipeline’s criticality, complexity, and scale. The deployed checker                    tification is over sub-projections, a type-level notion, so minimality
carries the method in production across our case studies, while a                      is type-level, not per-collection.                                     □
full PDL mechanization in Agda shows the proof end is reachable
                                                                                            Proof of Theorem 3.2. Let 𝑝 = op1 >> · · · >> op𝑛 ; the DAG
for a real pipeline, collapsing the runtime residue to the boundary
                                                                                       case follows by topological order.
alone. And because correctness is computed from grain, not data,
                                                                                            Denotation totality. Every type appearing in 𝑝 is an al-
the method is universal over the operation set and carrier (PDD
                                                                                       gebraic data type, and grain—hence the denotation [[𝑅]] =
Universality, §3)—PDA over batch collections is one instance, a win-
                                                                                       (𝐺 [𝑅], 𝐸𝐾 [𝑅], 𝐵𝐶 [𝑅])—is defined for every ADT, inductive
dowing algebra over unbounded streams another. And the method
                                                                                       or coinductive [14]. So [[·]] is total on the types 𝑝 traverses,
is not even specific to pipelines: a query is a single grain-bearing
                                                                                       independently of the carrier 𝐹 chosen to hold the data.
transformation—the one-node case—so the same design-time check
                                                                                            (i)–(ii) Homomorphism and rule composition. By hypothesis each
certifies the AI-generated queries that run on top of the data assets,
                                                                                       op𝑖 is faithful: [[op𝑖 𝑐]] = CalcG[op𝑖 ] [[𝑐]]. We show [[𝑝 𝑐]] =
a correctness layer the ontology/semantic-layer stack otherwise
                                                                                       (CalcG[op𝑛 ] ◦ · · · ◦ CalcG[op1 ]) [[𝑐]] by induction on 𝑛. The base
lacks (§9). The engineer’s role shifts accordingly: he authors and
                                                                                       case 𝑛 = 1 is faithfulness of op1 . For the step, write 𝑞 = op1 >>
validates the specification—the data denotation of source and tar-
                                                                                       · · ·>>op𝑘 and 𝐶𝑞 = CalcG[op𝑘 ] ◦· · ·◦CalcG[op1 ], so the induction
get and the business rules—and checks the certificate the agent
                                                                                       hypothesis reads [[𝑞 𝑐]] = 𝐶𝑞 [[𝑐]]. Then
ships (a machine-checked proof, or an evidence ledger), while the
algebra and the generated queries verify the rest. This is a proof-                                 [[(𝑞 >> op𝑘+1 ) 𝑐]] = CalcG[op𝑘+1 ] [[𝑞 𝑐]]
carrying [20] discipline for AI-generated pipelines: an untrusted                                                        = CalcG[op𝑘+1 ] (𝐶𝑞 [[𝑐]]),
producer, a cheaply-checkable certificate, and a human freed to do
the one thing no verifier can—get the specification right. Future                      by faithfulness of op𝑘+1 (on input 𝑞 𝑐) then the induction hypothesis.
work extends the PDL mechanization from the exemplar to the full                       This is the homomorphism (i); reading off its grain component is
operation catalog, instantiates PDD on a streaming carrier, broad-                     the rule composition (ii)—the compositionality of the grain homo-
ens the pattern library, and realizes the query-layer checker of §9                    morphism (Thm 3.1).
for AI-generated queries over semantic layers.                                            (iii) Decidability. CalcG[𝑝] threads the 𝑛 per-operation rules
                                                                                       through the DAG by the CalcG verification algorithm of Part I—
                                                                                       sequential composition is function composition of the per-vertex
A     DEFERRED PROOFS                                                                  steps, fan-out reuses a computed grain, and fan-in applies the binary
    Proof of Theorem 6.2. Throughout, 𝑘 : 𝑅 ↠ 𝐾 is a field-set                         rule, so the three patterns exhaust the DAG [14]. Each rule is a finite
projection, so 𝐾 retains a subset of 𝑅’s fields and 𝑘 is surjective.                   operation on field sets (∪𝑡 𝑦𝑝 , ∩𝑡 𝑦𝑝 , −𝑡 𝑦𝑝 , ⊆𝑡 𝑦𝑝 ) over the schemas of
    (1)⇒(2): the elements of any collection 𝑐 : 𝐶 𝑅 are values of 𝑅,                   𝑝’s types; the pipeline is a finite DAG and every schema is a finite
so a projection injective on the type 𝑅 is injective on the elements                   field set, so CalcG[𝑝] (𝐺 [Source]) is computed in finitely many
of 𝑐, hence a superkey of every 𝑐.                                                     steps and compared to 𝐺 [Target] by decidable field-set equality—no
    (2)⇒(1): contrapositive. If 𝑘 𝑟 1 = 𝑘 𝑟 2 with 𝑟 1 ≠ 𝑟 2 , then grain 𝑟 1 ≠        data is read. Part I bounds this at 𝑂 (|𝑉 | ·𝑘 · |𝐹 |) time and 𝑂 (|𝑉 | · |𝐹 |)
grain 𝑟 2 by Grain Uniqueness [14] (the grain projection is injective),                space for field-set inference rules, on a DAG of |𝑉 | vertices with
so {𝑟 1, 𝑟 2 } is a well-formed grain-unique collection of type 𝐶 𝑅—and                fan-in 𝑘 and at most |𝐹 | fields per type [14]; for a general grain-
𝑘 is not a superkey of it. Hence 𝑘 is not a superkey of every 𝑐.                       inferring Op the cost is 𝑂 (|𝑉 |) times the per-operation rule cost.
    (1)⇔(3): 𝑘 is given as a surjection, and a surjection is injective                 The data’s cardinality, hence whether 𝐹 is bounded, never enters: a
iff it is a bijection, i.e. an isomorphism. So 𝑘 injective on 𝑅 (1) is                 windowed stream is verified exactly as a finite table.                       □
                                                                                  22
    Proof of Theorem 6.6. Write pip = op1 >> · · · >> op𝑛                                   [3] Michael Armbrust, Tathagata Das, Joseph Torres, Burak Yavuz, Shixiong Zhu,
for a linear chain; the DAG case is identical taken in topo-                                    Reynold Xin, Ali Ghodsi, Ion Stoica, and Matei Zaharia. 2018. Structured Stream-
                                                                                                ing: A Declarative API for Real-Time Applications in Apache Spark. In Proceedings
logical order. Each layer is discharged on the type-level data                                  of the 2018 ACM SIGMOD International Conference on Management of Data. ACM,
[[·]] = (𝐺 [·], 𝐸𝐾 [·], 𝐵𝐶 [·]) and on the constraint specification,                            601–613.
                                                                                            [4] William W. Armstrong. 1974. Dependency structures of data base relationships.
never on a collection.                                                                          In Information Processing 74: Proceedings of IFIP Congress. North-Holland, 580–
    Grain. CalcG composes step by step,                                                         583.
                                                                                            [5] Paris Carbone, Asterios Katsifodimos, Stephan Ewen, Volker Markl, Seif Haridi,
           CalcG[op1 >> op2 ] = CalcG[op2 ] ◦ CalcG[op1 ]                                       and Kostas Tzoumas. 2015. Apache Flink: Stream and Batch Processing in a
                                                                                                Single Engine. IEEE Data Engineering Bulletin 38, 4 (2015), 28–38.
(§6.1), so CalcG[pip] is the composite of the per-operation rules. Hy-                      [6] E. F. Codd. 1970. A Relational Model of Data for Large Shared Data Banks.
                                                                                                Commun. ACM 13, 6 (1970), 377–387. https://doi.org/10.1145/362384.362685
pothesis (ii) states this composite carries 𝐺 [Source] to 𝐺 [Target];                       [7] dbt Labs. 2026. dbt (data build tool) Documentation: Data Tests. https://docs.
by Theorem 6.1 the output collection’s grain equals the target’s, for                           getdbt.com/docs/build/data-tests. Accessed June 2026.
every input, with no data access.                                                           [8] dbt Labs. 2026. dbt Semantic Layer and MetricFlow. https://docs.getdbt.com/
                                                                                                docs/use-dbt-semantic-layer/dbt-sl. Accessed June 2026.
    Behavioral class. Each operation’s BC pre/postcondition is a type                       [9] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem Prover and
parameter, so (i)—the chain type-checks—makes every BC transition                               Programming Language. In Proceedings of the 28th International Conference on
admissible by construction; the deliberate changes are the re-lenses                            Automated Deduction (CADE-28) (Lecture Notes in Computer Science), Vol. 12699.
                                                                                                Springer, 625–635. https://doi.org/10.1007/978-3-030-79876-5_37
of §6.3, sound by Corollary 6.4.                                                           [10] Conal M. Elliott. 2009. Denotational Design with Type Class Morphisms. In
    Domain. Let (Pre𝑖 , Intra𝑖 , Post𝑖 ) be the contract of op𝑖 , with Pre =                    Technical Report 2009-01, LambdaPix. See also “Denotational design with type
                                                                                                class morphisms,” conal.net.
Pre1 and Post = Post𝑛 . Each operation is correct against its own                          [11] Great Expectations. 2026. Great Expectations: Data Quality Testing and Docu-
contract—Pre𝑖 (𝑐) ⇒ Post𝑖 (𝑐, op𝑖 𝑐) ∧ Intra𝑖 (. . . )—by its denotation                        mentation. https://greatexpectations.io/. Accessed June 2026.
(the (spec) clause), independently of data. We show by induction                           [12] Todd J. Green, Grigoris Karvounarakis, and Val Tannen. 2007. Provenance
                                                                                                Semirings. In Proceedings of the 26th ACM SIGMOD-SIGACT-SIGART Symposium
on 𝑖 that 𝑐 |= Pre implies the prefix op1 >> · · · >> op𝑖 produces a                            on Principles of Database Systems (PODS). ACM, 31–40.
state satisfying Post𝑖 . Base: op1 from Pre1 = Pre. Step: the induction                    [13] C. A. R. Hoare. 1969. An Axiomatic Basis for Computer Programming. Commun.
hypothesis gives Post𝑖 of the intermediate state; obligation (iii),                             ACM 12, 10 (1969), 576–580. https://doi.org/10.1145/363235.363259
                                                                                           [14] Nikos Karayannidis. 2027. Grain Theory: Type-Level Granularity Correctness in
Post𝑖 ⇒ Pre𝑖+1 —discharged at composition time, or inherited as                                 Data Pipelines. In Proceedings of the ACM SIGMOD-SIGACT-SIGAI Symposium
an axiom when contract-derivable (§6.4)—supplies Pre𝑖+1 , and the                               on Principles of Database Systems (PODS). Under submission. Extended version
                                                                                                with full proofs: arXiv:2601.00995.
correctness of op𝑖+1 yields Post𝑖+1 . At 𝑖 = 𝑛 this is pip 𝑐 |= Post,                      [15] Jinyang Li, Binyuan Hui, Ge Qu, Jiaxi Yang, Binhua Li, Bowen Li, Bailin Wang,
the Intra conjuncts accumulated along the chain. Every implication                              Bowen Qin, Ruiying Cao, Ruiying Geng, et al. 2023. Can LLM Already Serve as
used is type-level, so the entailment is established without reading                            a Database Interface? A Big Bench for Large-Scale Database Grounded Text-to-
                                                                                                SQLs. In Advances in Neural Information Processing Systems (NeurIPS).
𝑐.                                                                                         [16] David R. MacIver, Zac Hatfield-Dodds, et al. 2019. Hypothesis: A New Approach
    Transfer to the concrete domain. The argument lives in the seman-                           to Property-Based Testing. Journal of Open Source Software 4, 43 (2019), 1891.
tic domain [[·]]. The grain homomorphism [[pip 𝑐]] = [[pip]] [[𝑐]]                              https://doi.org/10.21105/joss.01891
                                                                                           [17] Malloy Authors. 2026. Malloy: An Experimental Language for Describing Data
(§3) makes the grain and BC reasoning faithful to the executed                                  Relationships and Transformations. https://www.malloydata.dev/. Accessed
pipeline; each domain predicate is interpreted over the same col-                               June 2026.
                                                                                           [18] Erik Meijer, Brian Beckman, and Gavin Bierman. 2006. LINQ: Reconciling Object,
lections, and its compiled runtime check returns the empty set                                  Relations and XML in the .NET Framework. In Proceedings of the 2006 ACM
iff the predicate holds (Theorem 6.5). Hence 𝑐 |= Pre ⇒ pip 𝑐 |=                                SIGMOD International Conference on Management of Data. ACM, 706. https:
Post ∧ Intra holds concretely, and the only obligation that consults                            //doi.org/10.1145/1142473.1142552
                                                                                           [19] Yaron Minsky. 2011. OCaml for the Masses. Commun. ACM 54, 11 (2011), 53–58.
data is 𝑐 |= Pre.                                                          □                    https://doi.org/10.1145/2018396.2018413
                                                                                           [20] George C. Necula. 1997. Proof-Carrying Code. In Proceedings of the 24th ACM
   Proof of Corollary 6.4. The precondition “𝑘 is a superkey of                                 SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL).
the input 𝑐 ′ ” says exactly that 𝑐 ′ is grain-unique at 𝐾 (Thm. 6.2,                           106–119. https://doi.org/10.1145/263699.263712
                                                                                           [21] Evan Patterson, Owen Lynch, and James Fairbanks. 2022. Categorical Data
collection reading), so 𝑐 ′ is a well-formed collection of the re-                              Structures for Technical Computing. Compositionality 4, 5 (2022).
declared type and the re-lens neither drops an element nor chooses                         [22] Patrick M. Rondon, Ming Kawaguchi, and Ranjit Jhala. 2008. Liquid Types. In
                                                                                                Proceedings of the 29th ACM SIGPLAN Conference on Programming Language
a representative—it is an identity on data. By hypothesis 𝑡’s post-                             Design and Implementation (PLDI). 159–169. https://doi.org/10.1145/1375581.
condition makes 𝑘 a key of 𝑡 𝑐 for every input 𝑐, discharging the                               1375602
precondition on every collection in the image of 𝑡; the type-checker                       [23] Sebastian Schelter, Dustin Lange, Philipp Schmidt, Meltem Celikel, Felix Biess-
                                                                                                mann, and Andreas Grafberger. 2018. Automating Large-Scale Data Quality
verifies the composition with no premise depending on data. The                                 Verification. Proceedings of the VLDB Endowment 11, 12 (2018), 1781–1794.
result denotation is the one declare-⟨bc⟩ declares—grain 𝐾, class                               https://doi.org/10.14778/3229863.3229867
                                                                                           [24] Patrick Schultz and Ryan Wisnesky. 2017. Algebraic Data Integration. Journal
⟨bc⟩, entity key derived from 𝐾—and is exact when the postcondi-                                of Functional Programming 27 (2017), e24.
tion gives a minimal key (Thm. 6.2).                               □                       [25] David I. Spivak. 2012. Functorial data migration. Information and Computation
                                                                                                217 (2012), 31–51.
                                                                                           [26] Nikhil Swamy, Cătălin Hriţcu, Chantal Keller, Aseem Rastogi, Antoine Delignat-
REFERENCES                                                                                      Lavaud, Simon Forest, Karthikeyan Bhargavan, Cédric Fournet, Pierre-Yves Strub,
 [1] Tyler Akidau, Robert Bradshaw, Craig Chambers, Slava Chernyak, Rafael J.                   Markulf Kohlweiss, Jean-Karim Zinzindohoue, and Santiago Zanella-Béguelin.
     Fernández-Moctezuma, Reuven Lax, Sam McVeety, Daniel Mills, Frances Perry,                 2016. Dependent Types and Multi-Monadic Effects in F*. In Proceedings of the
     Eric Schmidt, and Sam Whittle. 2015. The Dataflow Model: A Practical Approach              43rd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming
     to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-              Languages (POPL). 256–270. https://doi.org/10.1145/2837614.2837655
     of-Order Data Processing. Proceedings of the VLDB Endowment 8, 12 (2015),             [27] Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li,
     1792–1803.                                                                                 James Ma, Irene Li, Qingning Yao, Shanelle Roman, Ye Zhang, and Dragomir
 [2] Apache Software Foundation. 2026. Apache Airflow. https://airflow.apache.org/.             Radev. 2018. Spider: A Large-Scale Human-Labeled Dataset for Complex and
     Accessed June 2026.                                                                        Cross-Domain Semantic Parsing and Text-to-SQL Task. In Proceedings of the 2018
                                                                                      23
     Conference on Empirical Methods in Natural Language Processing (EMNLP).                 Franklin, Ali Ghodsi, Joseph Gonzalez, Scott Shenker, and Ion Stoica. 2016.
[28] Matei Zaharia, Reynold S. Xin, Patrick Wendell, Tathagata Das, Michael Armbrust,        Apache Spark: A Unified Engine for Big Data Processing. Commun. ACM 59, 11
     Ankur Dave, Xiangrui Meng, Josh Rosen, Shivaram Venkataraman, Michael J.                (2016), 56–65. https://doi.org/10.1145/2934664




                                                                                        24
