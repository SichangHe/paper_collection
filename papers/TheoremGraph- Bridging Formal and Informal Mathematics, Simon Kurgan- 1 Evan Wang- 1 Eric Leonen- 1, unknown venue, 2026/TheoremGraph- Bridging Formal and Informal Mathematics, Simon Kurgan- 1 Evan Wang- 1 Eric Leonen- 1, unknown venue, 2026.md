                                                  TheoremGraph: Bridging Formal and Informal Mathematics
                                                  Simon Kurgan* 1                         Evan Wang* 1                        Eric Leonen* 1
                                                  simku22@uw.edu                        aurasoph@uw.edu                       eol05@uw.edu

                                                   Sophie Szeto1                        Luke Alexander1                     Artemii Remizov1
                                                  slszeto@uw.edu                        lukealex@uw.edu                     aremizov@uw.edu

                                                   Jarod Alper1                       Giovanni Inchiostro1                     Vasily Ilin1
                                                   jarod@uw.edu                        ginchios@uw.edu                        vilin@uw.edu
                                                                                                               1
                                                                                                                   University of Washington Math AI Lab
                                                                                                                            *
                                                                                                                              Equal contribution
                                                                                                                         Correspondence: vilin@uw.edu
arXiv:2606.25363v1 [cs.IR] 24 Jun 2026




                                                               Abstract                              statements by applying inference rules; once es-
                                                                                                     tablished, these statements become premises for
                                             Mathematical knowledge is organized around              subsequent results. Yet in contemporary mathemat-
                                             statements and their dependencies, but this
                                                                                                     ical research, the vast scale and specialization of
                                             structure is exposed unevenly: informal papers
                                             cite mostly at the document level, while for-
                                                                                                     the literature make these dependency structures dif-
                                             mal libraries record fine-grained dependencies          ficult to track. Authors typically cite papers rather
                                             over a much smaller body of mathematics. We             than the exact lemmas, definitions, or theorems
                                             introduce TheoremGraph, a unified statement-            required for a proof, in part because expert read-
                                             level dependency graph spanning both infor-             ers are expected to supply the relevant background.
                                             mal and formal mathematics. On the infor-               This practice avoids the burdens of explicit depen-
                                             mal side, we parse 11.7M theorem-like envi-             dency annotations, but coarsens the structure of
                                             ronments from mathematics arXiv and recover
                                                                                                     mathematical knowledge. As a result, attribution
                                             18.3M candidate directed dependencies, each
                                             labeled by the extractor that proposed it so            may be obscured or rendered imprecise, and re-
                                             downstream users can trade coverage for pre-            lated work may be duplicated when researchers are
                                             cision. On the formal side, we release Lean-            unaware of equivalent or overlapping results. In a
                                             Graph, a Lean 4 elaborator-level extractor pro-         large study of withdrawn arXiv submissions, 2.4%
                                             ducing 388,105 declaration nodes and 11.3M              of categorized withdrawals are ones whose authors
                                             typed edges across 25 Lean projects. We bridge          self-identify as “not novel” (357 of 14,839 cases),
                                             the two graphs by embedding generated natural-
                                                                                                     reflecting work later judged to duplicate or lack
                                             language slogans into a shared semantic space,
                                             linking related statements across papers and
                                                                                                     originality relative to existing results (Rao et al.,
                                             across the informal/formal divide; an LLM               2024).
                                             judge affirms 47,952 such matches above a 0.8              Proof assistants have emerged as an important
                                             cosine floor, with the judge-acceptance rate ris-       tool for making mathematical verification more
                                             ing from 48% across the floor to 87% in the ≥           rigorous and explicit. These systems allow math-
                                             0.9 tier. On formal concept retrieval, our name-
                                                                                                     ematicians to express definitions, theorems, and
                                             and-signature representation with graph expan-
                                             sion comes within 0.5pp of LeanSearch v2’s
                                                                                                     proofs in a formal language whose correctness can
                                             reranked Recall@10 (0.775 vs. 0.780) without            be verified by a trusted kernel. In contrast to infor-
                                             an LM reranker. We release the dataset, extrac-         mal proofs, where references to prior results and
                                             tors, HTTP API, and MCP interface as infras-            routine intermediate arguments are often left im-
                                             tructure for mathematical search, attribution,          plicit, formal proofs must specify each logical de-
                                             and retrieval-augmented reasoning, available at         pendency and enough intermediate structure to be
                                             theoremsearch.com and huggingface.co.                   type-checked by the kernel. As a result, formaliza-
                                                                                                     tion reveals the fine-grained dependency structure
                                         1   Introduction                                            underlying mathematical arguments.
                                         Mathematical knowledge is built upon discrete                  Lean is one of the most prominent modern proof
                                         statements and their dependencies. Beginning with           assistants, based on the calculus of constructions
                                         a chosen set of axioms, mathematicians derive new           and supported by an active open-source ecosys-

                                                                                                 1
tem. Lean’s mathematical library, mathlib4, con-            2     Related Work
tains over 400,000 formalized definitions, lemmas,
theorems, and proofs contributed by the commu-              2.1    Mathematical Information Retrieval
nity across mathematical fields such as algebra,            Early Math IR focused on formula-aware and key-
topology, analysis, and number theory (Lean FRO,            word search, motivated by the fact that mathe-
2026). Despite this rapid growth, formalized math-          matical notation cannot be treated as ordinary
ematics remains much smaller and less comprehen-            text. Benchmarks such as NTCIR-11 Math-2,
sive than the body of informal mathematical knowl-          NTCIR-12 MathIR, and ARQMath formalized re-
edge. Lean’s coverage is strongest in foundational          trieval over mathematical corpora containing both
material, standard undergraduate- and graduate-             formulas and surrounding text, including arXiv,
level mathematics, and a growing number of tar-             Wikipedia, and Math Stack Exchange (Aizawa
geted research-level formalization projects. Its lim-       et al., 2014; Zanibbi et al., 2016; Mansouri et al.,
ited coverage of all research literature caps the           2022). These settings showed that mathemat-
extent to which formal methods can be used to               ical meaning depends on both symbolic struc-
navigate or verify contemporary mathematics at              ture and visual layout, motivating representa-
scale.                                                      tions such as Symbol Layout Trees and Opera-
   In this work, we collect and analyze dependency          tor Trees with formula-specific indexing methods
graphs for both formalized and informal mathemat-           (Zanibbi et al., 2015). More recent work explores
ics. Our main contributions are:                            learned representations: zbMath-BERT studies em-
                                                            beddings for mathematical text (Steinfeldt and
  1. Informal dependency graph. We extract de-
                                                            Mihaljević, 2024), NaturalProofs and Theorem-
     pendency structure from informal mathemat-
                                                            Search apply neural retrieval to informal statements
     ical sources, including arXiv and Lean Com-
                                                            (Welleck et al., 2021; Alexander et al., 2026), and
     munity, recovering 18.3 million dependencies
                                                            LeanSearch retrieves Mathlib declarations from in-
     connecting over 11.7 million statements.
                                                            formal queries via sloganized formal statements
  2. Formal dependency graph. We extract typed              (Gao et al., 2025, 2026). Our work extends sloga-
     declaration-level dependencies from Math-              nized statement retrieval by incorporating explicit
     lib4 and several open-source formalization             dependency structure among mathematical state-
     projects.                                              ments.
  3. Systematic analyses. We perform compre-                2.2    Bibliometrics
     hensive studies of both graphs, examining
                                                            Bibliometric work uses scholarly signals to mea-
     their structural properties and their applica-
                                                            sure influence, relatedness, and field structure. Ci-
     bility to mathematical search, navigation, and
                                                            tation graphs model relationships among papers,
     reasoning.
                                                            authors, and journals; citation-count measures such
  4. Cross-formality bridge. We link informal               as the h-index and journal impact factor summarize
     and formal statements in a shared slogan-              influence directly, while recursive prestige models
     embedding space, yielding 47,952 LLM-                  such as Pinski–Narin influence, Eigenfactor, Cit-
     affirmed (informal, formal) matches; the               eRank, and Życzkowski’s weighted impact factors
     same name-and-signature representation with            weight citations by graph structure, recency, or link-
     graph expansion comes within 0.5pp points of           ing behavior (Garfield, 1972; Hirsch, 2005; Pinski
     LeanSearch v2’s reranked Recall@10 without             and Narin, 1976; Bergstrom, 2007; Walker et al.,
     a reranker.                                            2007; Zyczkowski, 2009). In mathematics, graph-
                                                            based analyses have been applied to Mathlib depen-
  5. Public dataset. We release the resulting for-
                                                            dency structure and proof-assistant libraries as het-
     mal and informal dependency data as a public
                                                            erogeneous networks (Li et al., 2026; Bauer et al.,
     resource for the mathematical and machine-
                                                            2023), while TheoremKB and AutoMathKG con-
     learning communities.
                                                            struct theorem-level graphs for informal sources at
  6. Programmatic access. We provide an API                 smaller scale (Mishra et al., 2024; Bian et al., 2025).
     and MCP interface that allow users, applica-           Our work extends these graph-based perspectives
     tions, and AI agents to query the dependency           to theorem-level dependencies across both informal
     data directly.                                         and formal mathematics.

                                                        2
2.3    Neural Theorem Proving &                            and statements ending mid-clause.
       Autoformalization
                                                               Extractor        Edges Within-paper      External
Neural theorem proving and autoformalization ad-
                                                               Deterministic   5.23M        3.31M    1.92M (79K)
dress complementary stages in converting informal              Heuristic       6.47M        4.77M    1.70M (53K)
mathematics into machine-checked proofs: auto-                 Notation        7.88M        7.88M              –
formalization translates informal statements into              Any             18.32M      14.86M 3.46M (130K)
formal declarations, while theorem proving gener-
ates proofs for those declarations. Recent progress        Table 1: Breakdown of informal dependency edges by
on benchmarks such as miniF2F and PutnamBench              extractor. The Within-paper and External columns are
has increased the importance of retrieval and tool-        not a partition of all edges and need not sum to the
ing for agentic proving systems (Zheng et al., 2022;       Edges total. Per-extractor rows may overlap; the “Any”
                                                           row deduplicates.
Ospanov et al., 2025; Tsoukalas et al., 2024; Re-
quena et al., 2026; Liu et al., 2026). Our work
supports this direction by aligning informal and           Dependency extraction. Each edge is tagged
formal statements with their dependency context.           with the extractor or extractors that proposed it
                                                           (Table 1). The deterministic extractor resolves
2.3.1 Lean Graph                                           \ref-like commands within a paper and \cite
Dependency extraction for formal libraries is well         keys against the paper’s reference list, using arXiv
studied (Alama et al., 2012), and several Lean tools       IDs or title matching; citations that name a target
build declaration-level graphs. Jixia, the extractor       theorem are further resolved to a specific statement.
behind LeanSearch v2 (frenzymath, 2024), emits             The heuristic extractor adds edges from nearby
a raw post-elaboration constant-reference graph;           references, backward discourse cues, and prose ref-
Lean Atlas (Yanahama and Sannai, 2026) splits              erences such as “Theorem 3.2,” with all heuristic
type- and value-level edges and adds confidence            edges constrained to point backward in document
scores, sorry-status, reachability, and visualiza-         order. The notation extractor uses Qwen3-235B-
tion; and leanblueprint (Massot, 2020) provides            A22B-Instruct-2507 to identify notation defined
author-annotated \lean{} links between informal            and used by each statement, then links each use to
LaTeX statements and their formal Lean decla-              the closest prior compatible definition.
rations. LeanGraph is complementary: it classi-
fies dependencies through Lean’s kernel APIs, fil-         Validation. We evaluate the extractor pipeline on
ters kernel artifacts with a documentation-aligned         500 sampled papers using an independent LLM
node set, and refines prior edge taxonomies into           judge, Kimi K2.5. The judge first proposes within-
sig/extends/field and proof/def edges at multi-            paper dependencies from the full statement list,
library scale.                                             then verifies extractor-proposed edges it missed.
                                                           Results are shown in Table 2; examples of rejected
3     Informal Graph                                       and missed edges appear in Appendix A. Each
                                                           released edge retains its extractor label, allowing
We parse over 11.7 million theorem-like state-             users to trade coverage for precision; deterministic
ments from mathematics arXiv papers and recover            edges, for example, achieve 98.8% judge-verified
18.3 million directed dependency edges within and          precision.
across papers.
                                                           4     Formal Graph
Corpus and statement extraction. Our corpus
is the arXiv Kaggle metadata snapshot filtered to          LeanGraph is a Lean 4 elaborator-level extractor
mathematics-tagged papers. For each paper, we              that builds typed declaration-dependency graphs
store metadata, references resolved through Seman-         from compiled Lean projects. Each human-facing
tic Scholar when possible, and the paper’s LATEX           declaration becomes a node, and dependencies are
source. A regex-based parser identifies theorem-           assigned one of six semantic edge types. The Math-
like environments and records each statement’s             lib v4.27–v4.29 graph contains 351K declaration
type, reference number, \label key, body, proof,           nodes and 9.3M within-library edges; across all 25
and local context. We discard malformed or im-             Lean projects, LeanGraph extracts 388,105 nodes
plausible statements, including empty bodies, un-          and 11,335,708 edges in total (including cross-
balanced math delimiters, very short statements,           library).

                                                       3
 Extractor       Edges    Judge-Verified Judge-Rejected          sparse (edge-to-statement ratio ∼1.56), the for-
 Deterministic    5,051     4,989 (98.8%)        62 (1.2%)       mal graph is dense (∼29.2), and no edges initially
 Heuristic        4,616     3,535 (76.6%)    1,081 (23.4%)       connect them. To link equivalent or closely re-
 Notation         6,241     2,665 (42.7%)    3,576 (57.3%)
                                                                 lated statements across papers and across the infor-
 Any             14,481     9,855 (68.1%)    4,626 (31.9%)       mal/formal divide, we map every statement into a
 Judge-only edges (no extractor recovered)          6,372        shared semantic space using slogans, embeddings,
 F1 = 2 TP/(2 TP + FP + FN)                         0.642
                                                                 and nearest-neighbor lookup.
Table 2: Agreement between extracted informal depen-             Slogans. Following prior work on statement-
dency edges and an independent LLM judge on 500
                                                                 level retrieval (Gao et al., 2025; Alexander et al.,
arXiv papers. Assuming the judge to be ground truth,
judge-verified edges are true positives, judge-rejected
                                                                 2026), for each statement, we generate a slo-
extractor edges are false positives, and judge-only edges        gan: a concise, standalone natural-language sum-
are false negatives. Per-extractor rows may overlap; the         mary produced by Qwen3-235B-A22B-Instruct-
“Any” row deduplicates.                                          2507 (Team, 2025). Informal slogans are generated
                                                                 with an escalating prompt chain that adds context
                                                                 only when the previous attempt is self-flagged as
Scope and granularity. LeanGraph runs inside                     insufficient.
Lean 4 over the kernel Environment API, extract-
                                                                    The stages add, in order, the statement body,
ing dependencies from elaborated, type-checked
                                                                 proof and local context, neighboring statements
declarations rather than source text. This gives ac-
                                                                 and outgoing dependencies, and finally a forced
cess to post-elaboration constants and proof terms
                                                                 best-guess slogan. This achieves full coverage over
that source-level parsers, such as lean4export’s
                                                                 11.75M statements, with 70.3% resolved at the min-
Python pipeline (Lean FRO, 2026), cannot reliably
                                                                 imal stage and 98.1% before the final fallback (Ta-
recover.
                                                                 ble 3). For formal declarations, we rank outgo-
Edge types. LeanGraph emits six edge cate-                       ing dependencies by semantic role and pack the
gories. extends captures structure or class inher-               highest-priority mathematically informative con-
itance; field captures dependencies in structure                 text into a fixed-size prompt, filtering ubiquitous
field types; sig captures constants appearing in                 declarations and Lean/kernel plumbing. Exact rank-
declaration signatures; proof captures constants                 ing and filtering rules are given in the released code.
used in theorem proof terms; def captures con-
stants used in non-Prop definition bodies; and                    Stage            Statements       Sufficient Coverage
docref captures valid backtick references in doc-                 minimal             11.75M 8.26M (70.3%)         70.3%
                                                                  standard             3.49M 2.87M (82.1%)         94.7%
strings. This taxonomy separates structural, type-                comprehensive         624K 406K (65.1%)          98.1%
level, value-level, and documentation-level depen-                final                 218K   218K (100%)          100%
dencies, enabling downstream systems to rank or
filter edges by role.                                            Table 3: Slogan rescue rates along the escalating prompt
                                                                 chain.
Node inclusion. A declaration is included when
it satisfies shouldIncludeConstant, a structural
predicate based on Lean’s classification APIs and                Embeddings. Each slogan is embedded into
doc-gen4’s renderability criteria (Lean Prover Com-              R4096 using Qwen3-Embedding-8B (Zhang et al.,
munity, 2026). This removes kernel-generated ar-                 2025a) with a retrieval instruction, then ℓ2 -
tifacts such as auxiliary recursors, noConfusion                 normalized so inner products equal cosine sim-
lemmas, matcher declarations, projections, and par-              ilarity. Vectors are stored in pgvector with an
ent accessors, while retaining user-facing decla-                HNSW index (Malkov and Yashunin, 2018); a
rations. Anonymous instances and tactic objects                  binary-quantized projection is used for fast can-
are kept but tagged with metadata, allowing down-                didate generation.
stream consumers to filter them if needed.
                                                                 Semantic representation. For each target state-
5    Universal Graph                                             ment, we can retrieve semantically similar state-
                                                                 ments using the embedding index. Retrieval first
The informal and formal graphs differ sharply in                 uses binary HNSW to produce an approximate
density and representation: the informal graph is                shortlist, then reranks candidates by full-precision

                                                             4
cosine similarity and keeps matches above a fixed                                    Similarity bin    Decls.
threshold. Figure 6 details the possibilities: for-                                  0.95–1.0             678
mal (or informal) to itself can surface duplicates                                   0.90–0.95          6,636
                                                                                     0.85–0.90         26,807
while formal to informal finds semantic restatement                                  0.80–0.85         66,744
edges (matches).                                                                     0.50* –0.80      112,481
                                                                                     no match         172,311
6       Bridging The Corpora                                                         Total            385,657

Motivation. To bridge the formal and infor-                           Table 4: Candidate match cosine similarity across all
mal graphs into a Universal Graph, we look for                        385,657 swept formal declarations. Shaded rows are
matches: (informal, formal) statement pairs that                      the tiers evaluated using LLM-as-judge. 0.50* is the
                                                                      minimum retrieved similarity and no match represents
express the same mathematical result under the
                                                                      declarations with no informal neighbor at ann_k=50.
same assumptions. A Lean blueprint (Massot,
2020) is a LATEX document that writes out a de-
velopment’s definitions, statements, and proofs in                    reflects the genuine absence of a close informal
human-readable form, and links each statement                         counterpart rather than a search-horizon limitation.
to the Lean declaration that formalizes it through
                                                                      Does retrieval find true counterparts? Embed-
author-written \lean{} annotations. These links
                                                                      ding formal and informal slogans into one shared
give us a small set of such matches1 . Extend-
                                                                      space is what makes cross-modal matching pos-
ing this set and finding such links at scale bet-
                                                                      sible: a formal statement can be paired with its
ter connects Lean to the informal mathematics it
                                                                      informal counterpart directly by embedding simi-
formalizes, and gives neural theorem provers and
                                                                      larity, with no shared vocabulary or surface overlap
auto-formalization systems an accurate scaffold by
                                                                      required. We validate that this similarity actually
which new formalizations can come about.
                                                                      recovers true counterparts using blueprint pairs as
Setup. Our matching pipeline (Figure 1) searches                      a source of truth, where each blueprint annotates
from the smaller, lightly-filtered2 formal graph                      a Lean declaration with a human-written informal
of 385,657 declarations into the informal corpus.                     statement. The informal halves sit in our corpus
For each formal declaration we embed its natural-                     like any other slogan (labeled source=blueprint),
language slogan and retrieve the single most similar                  with the same embeddings and none treated spe-
informal slogan by cosine similarity; that nearest                    cially.
neighbor, with its similarity score, is a candidate                      We take each blueprint’s formal slogan as the
match.3 At ann_k=50 this finds a candidate for                        query and ask which informal slogan is most simi-
55.3% of declarations and yields the similarity dis-                  lar to it in the shared index, then check where the
tribution in Table 4.                                                 annotated informal partner lands in that ranking.
   Modulating ann_k between 500 and 1000 over                         The partner ranks first 43.5% of the time and within
a sample of 200 otherwise-unmatched declarations,                     the top ten 69.9% (Hit@1, Hit@10). Mismatches
we see that deeper search does recover a candidate                    with the annotated partner are mostly not errors:
for 84% and 88% of them respectively, but only                        among formal nodes whose top result is not the
up to a similarity of 0.837 and 0.859. Across all                     annotated partner but is itself a high-similarity can-
400 of these deeper probes only a single candidate                    didate (≥ 0.85), LLM-as-judge rates 65% (n=187)
clears the 0.85 match bar and none reach 0.90, so                     as matches, i.e. valid alternative restatements rather
a missing candidate at ann_k=50 almost always                         than retrieval failures.

    1
                                                                      Judging. To judge matches, a GPT-5.4 judge la-
      1,595 (informal, formal) statement pairs drawn from
blueprints, across 1,308 informal statements and 1,577 for-           bels each candidate, given the declaration name,
mal declarations; one informal statement is often formalized          both slogans, the Lean signature, the arXiv title,
as several Lean lemmas, which is why formals outnumber                and the informal LATEX. The judge returns its deci-
informals.
    2
      We drop constructors (ctor) and compiler-internal auto-         sion as one label with a brief rationale:
generated names, which lack a meaningful natural-language
counterpart. This amounts to 2,448 nodes (0.63%) and leaves              • exact : the same result without caveat; a math-
the 1,595 blueprint pairs intact.                                          ematician could cite one as the other.
    3
      Both graphs are embedded into one shared index, so this
is a cross-modal nearest-neighbor query, not a per-side search.          • inexact : the same underlying result but not

                                                                  5
            1   sources                      2   sloganize          3   embed              4   retrieve                                                                    5   judge



     INFORMAL

     LaTeX stmt                                                  embed
                                          slogan
   arXiv / blueprint      LLM      one-line plain-English      slogan vector
                                description of the statement
    informal graph                                               vi ∈ Rd                                                                                      LLM-as-judge  GPT-5.4

                                                                                                                                                     exact       same result, no caveat
                                                                                    shared index                    candidate match
                                                                                                      formal → informal                    label                 same result up to a generalization,
                                                                                single embedding space                  rank-1 neighbor             inexact      special case, or one direction of an
                                                                                                         rank-1 sweep                                            iff
                                                                                    cosine similarity                 sim. score s = cos
                                                                                                                                                    wrong        different results despite high
                                                                                                                                                                 embedding similarity
                                                                                 one index, both lanes
       Lean decl                                                 embed
                                          slogan
   Mathlib / projects     LLM      one-line plain-English      slogan vector
                                description of the statement
       formal graph                                             vf ∈ Rd                                                                            exact / inexact = match      wrong = non-match

       FORMAL




Figure 1: The matching pipeline. Lean declarations and LATEX statements are each sloganized and embedded into
one shared index; a formal→informal rank-1 cosine query proposes candidate matches, which a single GPT-5.4
judge labels exact / inexact / wrong (exact/inexact count as matches).


         verbatim (a generalization, special case, or                                       Judged matches. Of the 100,799 candidates
         one direction of a bidirectional implication).                                     above the floor5 , GPT-5.4 affirms 47,952 as
                                                                                            matches (48%). Quality concentrates at the high-
   • wrong : different results despite high embed-                                          similarity end: the ≥ 0.9 tier alone gives 6,353
     ding similarity (shared vocabulary or sibling                                          matches (87% of its candidates), and the affirma-
     concepts).                                                                             tion rate rises steadily with similarity across the
                                                                                            band (Figure 2). Running a second, more lenient
We count exact and inexact as matches. GPT-5.4                                              judge (DeepSeek-V4-Pro) over the same candi-
is our judge of record because it is stricter than our                                      dates affirms 61,234 (61%); we keep the stricter
initial choice, Opus 4.8, which a domain expert                                             GPT-5.4 set as our matches and report DeepSeek
found over-generous; since a curated set should fa-                                         as a high-recall comparison.
vor precision, we adopt the stricter judge (selection
and an expert re-grading are in Appendix B.1). The                                         Looking to the future. Embedding both graphs
judge is stable under re-runs: a second independent                                        into one space turns cosine similarity into a signal
GPT-5.4 pass over a random 500-candidate sample                                            of “warmth” that curates high-quality links across
agrees on the match/non-match verdict for 93.2%                                            two large and largely disconnected bodies of math-
of pairs (κ=0.86)4 , so re-running GPT-5.4 rarely                                          ematical writing. These links are hard to surface by
changes a verdict.                                                                         hand yet cheap to check once proposed, and they
                                                                                           give automated formalization systems concrete con-
Where to judge. We judge every candidate at                                                text to build on, speaking to the “dependency is-
cosine similarity 0.8 and above. We set the floor                                          sue” Seed-Prover 1.5 describes, where progress
here, rather than higher, to make the curated set as                                       “typically hinges on synthesizing insights across a
valuable as possible: it captures the broad band of                                        multitude of related papers” (Chen et al., 2025).
inexact matches alongside the exact ones, and
because each edge is stored with its deterministic
                                                                                            7         Retrieval-Augmented Formalization
graph context, later work can re-judge these looser
links with more information and promote inexact                                            We test whether slogan retrieval helps an LLM aut-
ties to exact. We do not go lower because the yield                                        oformalize natural-language statements into Lean.
rate (the fraction the judge affirms as a match)                                           We use a statement-only setting: given an informal
collapses below 0.8: a pilot of 150 candidates per                                         description, claude-sonnet-4-6 generates a sin-
0.1-wide bin confirms only 23% in 0.7–0.8 and 2%                                           gle Lean 4 declaration ending in := sorry, with no
in 0.6–0.7, where judging mostly confirms non-                                             proof. The compiler is available during generation,
matches. Above the floor the match rate climbs                                             with at most three typecheck calls per target.
steeply with similarity (Figure 2).
                                                                                               5
                                                                                                 The retrieval pool holds 100,865 candidates at similarity
   4
     Cohen’s κ corrects agreement for chance: κ = (po −                                     ≥ 0.8 (Table 4); 100,831 were submitted to GPT-5.4 and
pe )/(1 − pe ), where po is the observed agreement and pe the                               32 returned unparseable output, giving these 100,799 valid
agreement expected if the two raters labeled independently at                               labels. Of them, 187 are unjudgeable, leaving 100,612 with
their observed match rates.                                                                 a decisive exact/inexact/wrong verdict.


                                                                                      6
             (a) GPT-5.4, our judge of record.                        (b) DeepSeek, a more lenient high-recall comparison.

Figure 2: Verdict composition by cosine-similarity bin (candidates at ≥ 0.8). Both judges shift from wrong to exact
and inexact as similarity rises; DeepSeek is consistently more generous, so we keep GPT-5.4 as the stricter set of
record and report DeepSeek as a high-recall comparison.


        Cond.         TC      Strict   Eval.   Tok.   Calls       Results. Retrieval improves evaluated correct-
        None          22/24   4/24     5/24    52k    276         ness from 5/24 to 8/24 while using fewer output
        RAG           20/24   6/24     8/24    14k     68
        Library       23/24   5/24     6/24    52k    275         tokens and tool calls than library search (Table 5).
        RAG+Library   24/24   7/24     8/24    37k    188
                                                                  The RAG condition matches RAG+Library on eval-
Table 5: Statement-only autoformalization of 24 Math-
                                                                  uated correctness, but uses 14k output tokens and
lib v4.30 theorems, retrieving over v4.29. Strict = same          68 tool calls, compared with 37k tokens and 188
proposition; Eval. = strict plus high-confidence equiva-          calls. Typechecking alone is not a reliable suc-
lent (claude-opus-4-7-judged, hand-checked). TC =                 cess signal: the ungrounded condition typechecks
typecheck.                                                        22/24 outputs but is evaluated correct on only 5/24.
                                                                  About 10/24 targets fail in every condition, suggest-
                                                                  ing that some informal queries underdetermine the
                                                                  intended Lean statement.
   To reduce memorization, we evaluate on 24 the-
orems introduced in Mathlib v4.30 while retrieving                8    Comparison Against Existing Retrieval
only from the v4.29 corpus. Queries are qwen3-8b
back-translations of the gold Lean signature with                 We benchmark our retrieval system against
the declaration name removed, so the informal                     LeanSearch-v2 (LSv2) (Gao et al., 2026), a Lean-
text must identify the relevant mathematical ob-                  specific retriever. Both systems retrieve flat embed-
jects without relying on the target name. The re-                 ded passages by cosine similarity over the same off-
triever uses slogan representations with a query                  the-shelf embedder (Qwen3-Embedding-8B, 4096-
head trained on typed dependency labels; on a held-               dim, normalized; no fine-tuning), and differ only in
out Mathlib premise benchmark, this improves                      what those passages contain. LSv2 embeds a struc-
R@100 from 0.16 with raw cosine similarity to                     tured passage (kind, type signature, and informal-
0.54. On the 24-target evaluation, top-15 retrieval               ized description, plus the value body for definitions,
recall is 0.161.                                                  classes, and instances) and keeps the fully-qualified
                                                                  name as metadata alongside it; our baseline embeds
   We compare four conditions: None, us-                          the slogan alone.
ing only the informal statement; RAG, adding                         Because the embedder is held fixed, differences
the top retrieved premises; Library, adding a                     trace to representation rather than embedding-
grep tool over the full v4.29 declaration list-                   model strength. Two things still differ: the struc-
ing; and RAG+Library, allowing both.               A              tured fields each side embeds, and the informal
claude-opus-4-7 judge, checked by hand, labels                    text itself (our one-line slogan versus LSv2’s
each output as strict if it states the same proposi-              dependency-grounded description). Our interven-
tion up to notation, and evaluated correct if it is a             tions target the first and do not isolate the con-
high-confidence equivalent restatement.                           tribution of informal-text quality. We evaluate

                                                              7
this baseline on MathlibQR, a benchmark from                           tions a slogan captures well. Second, some queries
the LSv2 team, and ask whether targeted interven-                      are typed as bare name or in Lean syntax rather
tions close the gap: once our passages carry the                       than plain English, and the baseline handles these
same name and signature information as LSv2’s,                         poorly. When both line up, a Lean-style query for a
our pipeline matches LSv2’s full system on recall                      named structure against our baseline finds the right
without reranking.                                                     declaration in the top ten only 12.9% of the time.
Benchmark. MathlibQR is an informal-to-
formal retrieval benchmark that pairs 200 Mathlib
declarations with up to 6 query styles each: plain
English, LATEX, Lean-flavored text, slogan, nick-
name, and a special case. Each is scored by two
ranking metrics6 , Recall@10 and nDCG@10, and
we also report the shallower nDCG cutoffs7 . Be-
cause compared systems are built on continuously-
evolving Mathlib snapshots, a system can miss a
query simply because the target declaration is ab-
sent, rather than retrieval failing.
   The fair-810 subset described in LSv2 controls
for this: its 810 query rows cover 171 of the 200
available target declarations, and each of those tar-
gets is guaranteed to appear in every compared                         Figure 3: What each system embeds for a declaration
system’s corpus. To tie our system into this bench-                    (example: the Lattice class). LeanSearch v2 packs
mark, we run our own retrieval pipeline over our                       declaration kind, informal name and description, and
snapshot of the corresponding Mathlib versions                         type signature into a single embedded passage, plus the
                                                                       value body for definitions, classes, and instances. The
(v4.27 ∪ v4.28), unioned to maximize coverage of
                                                                       fully-qualified name is kept only as metadata, outside
the fair-810 targets) and map LSv2’s target declara-                   the embedded text (Gao et al., 2026). Our baseline
tions onto ours; all 171 are present in our index.                     embeds a single natural-language slogan, with neither
                                                                       the signature nor a lexical handle on the name. The
The representation gap. Our baseline embeds
                                                                       name-and-signature representation and name-matching
only the slogan and scores 0.586 Recall@10 /                           index we introduce below add that channel.
0.380 nDCG@10, 7.1pp and 11.4pp behind LSv2’s
retriever-only baseline (Table 6). LSv2’s embedded
passage carries the type signature and an informal-                    Closing the gap. We group the interventions by
ized description, whereas our slogan carries only a                    what each improves, the ablation in Table 6 adds
one-line gloss (Figure 3); for declarations whose                      them cumulatively across Configurations A-E.
identity is essentially their name, our baseline has                      • Putting the name where queries can reach it
little to match against. This shows up in a few                             (Name/sig; the name-matching index is part of
ways.                                                                       Search). We add a name-and-signature repre-
    First, some declarations like Lattice or                                sentation: a second embedded passage encod-
Functor are their name, meaning that structures or                          ing the declaration’s name, type signature, and
classes with little informal elaboration are poorly                         dependencies. This moves the fully-qualified
retrieved. In the baseline, these are our two weak-                         name, which LSv2 keeps only as metadata,
est kinds with nDCG@10 0.222 and 0.253 (respec-                             into the embedded text itself (Figure 3), giv-
tively), against 0.477 for theorems - whose descrip-                        ing name-like queries an explicit target. We
   6
      Recall@10 is the fraction of queries whose target declara-            also add a name-matching index over decla-
tion appears anywhere in the top 10 retrieved results, ranked by            ration names for the bare-name queries the
similarity. nDCG@10 is a rank-weighted score over the top 10
that rewards ranking the target declaration higher, normalized              embedding may miss. Together these directly
so a perfect ranking scores 1.                                              fix the two error classes from the representa-
    7
      We report nDCG@{1,5,10} and Recall@10, the cut-
offs relevant to interactive search. LSv2 additionally reports
                                                                            tion gap.
Recall@{50,100}, which target deep recall for downstream
premise feeding rather than top-of-list quality, and an LLM-              • Translating the query into our wording
judge ranking we did not replicate.                                         (Search). For queries written tersely or in

                                                                   8
     Lean syntax, which are unlike our slogans, we            their 0.657. Since B and F share the same search
     have a model draft a hypothetical informal               techniques and differ only in what they embed, this
     statement answering it and search with that              swap isolates the representation, rather than the
     alongside the original query. This fuses the             search techniques, as the driver of ranking quality.
     two rankings (HyDE), and phrases the search                 Combining the slogan with the name-and-
     closer to our slogans.                                   signature representation (Configuration D) and then
                                                              adding graph expansion (Configuration E) trades
   • Resolving same-name collisions (Graph).                  ranking for recall: Recall@10 climbs from 0.733
     After retrieving, we follow the dependency               (F) to 0.767 (D) to 0.775 (E), while nDCG@10
     graph one hop up and add each result’s par-              slips from 0.558 (F) to 0.550 (D) to 0.548 (E). The
     ent declarations (Figure 4), which surfaces the          recall-optimized configuration, E, comes within
     general concept when a more specific declara-            0.5pp of LSv2’s reranked recall (0.775 vs. 0.780)
     tion of the same name has outranked it. LSv2             without a reranker;8 neither E nor F matches the
     builds the same graph and uses it to inform              reranked nDCG of 0.623, where the reranker’s pre-
     corpus construction, but does not consult it at          cise ordering leads at every cutoff.
     retrieval time.                                             Per declaration type (Figure 5), the levers pri-
   • Keeping good candidates in the running                   marily improve the categories for which slogans
     (Search). We widen the binary-HNSW short-                were least effective. Structures, classes, definitions,
     list (ann_k) so correct declarations survive             and inductives all benefit, whereas theorem and
     into the full-precision cosine pass rather than          instance, which typically already have descriptive
     being pruned early.                                      slogans, decline slightly. Thus, the interventions
                                                              incur a small cost on well-described declarations
                                                              in exchange for substantial gains on declarations
                                                              identified mainly by name.
                                                                 Across the same 810 queries the interventions
                                                              add +18.9pp Recall@10 and +16.8pp nDCG@10
                                                              over the baseline, while graph expansion con-
                                                              tributes least once the representation is present (E
                                                              vs. D: +0.8pp Recall, −0.2pp nDCG).

                                                              Transfer to MathlibMPR. The same configu-
                                                              ration does not carry over to chained-premise re-
                                                              trieval. On MathlibMPR, applying the QR-tuned
                                                              configuration lowers our group Recall@10 from
Figure 4: Graph expansion on Lattice (Config E). Af-          0.224 to 0.165 against our untuned baseline, so the
ter retrieval we follow the dependency graph one hop up       interventions that help concept retrieval are coun-
and add each candidate’s formal_dependency parents.           terproductive here. The task asks which lemmas a
Their names (SemilatticeInf, SemilatticeSup,                  proof invokes, and those can share no vocabulary
Lattice.toSemilatticeInf)           match     name-like       with the theorem, whereas every technique above
queries the bare slogan misses. LSv2 builds the same          sharpens matching on the meaning of a single dec-
graph but uses it only for informalization, not at            laration. We treat this as a scope boundary, not a
retrieval.
                                                              comparison, and leave chained-premise retrieval to
                                                              future work.
Results The full ablation is in Table 6; two
configurations are worth highlighting. Ranking-               9    Conclusion
optimized Configuration F replaces the slogan with
                                                              We present TheoremGraph, a statement-level de-
the name-and-signature representation, keeping the
                                                              pendency graph linking 11.7M informal arXiv
search techniques (name-matching index, query
rewriting, wider shortlist) but no graph. Without a               8
                                                                    Bootstrap 95% CIs (5000 resamples): Configuration E
reranker, it beats LSv2’s retriever-only baseline on          Recall@10 0.775 [0.746, 0.802], so LSv2’s 0.780 lies within
                                                              the interval (a failure to reject, not an equivalence test); gains
every metric we report, reaching 0.558 nDCG@10                over baseline +18.9pp Recall@10 [+15.1, +22.7] and +16.8pp
against their 0.494 and 0.733 Recall@10 against               nDCG@10 [+13.3, +20.2].


                                                          9
Table 6: MathlibQR fair-810. Component columns show what each of our configurations uses: the informal slogan,
the name-and-signature representation, the search-time techniques (name-matching index, query rewriting, wider
shortlist), and graph expansion. E is recall-optimized, reaching LSv2’s reranked recall to within 0.5pp (0.775 vs.
0.780) without a reranker; F is ranking-optimized.

                                           Components                                  Metrics
   Configuration                Slogan   Name/sig   Search    Graph     nDCG@1      nDCG@5    nDCG@10    R@10
   Ours (A) Baseline              ✓                                        0.201      0.345      0.380   0.586
   Ours (B)                       ✓                   ✓                    0.262      0.441      0.467   0.680
   Ours (C)                       ✓                   ✓           ✓        0.319      0.461      0.504   0.716
   Ours (D)                       ✓         ✓         ✓                    0.343      0.516      0.550   0.767
   Ours (E) recall-optimized      ✓         ✓         ✓           ✓        0.349      0.504      0.548   0.775
   Ours (F) ranking-optimized               ✓         ✓                    0.391      0.534      0.558   0.733
   LSv2 Retriever                                                          0.340      0.472      0.494   0.657
   LSv2 Retriever + reranker                                               0.470      0.601      0.623   0.780




Figure 5: MathlibQR fair-810, Recall@10 by declaration kind, comparing the baseline (Config A) with the full lever
stack (Config E). The interventions concentrate their gains on declarations identified mainly by name (structures,
classes, definitions, and inductives), while theorem and instance, which usually already carry descriptive slogans,
decline slightly. Configurations are defined in Table 6.


statements (18.3M edges) with the Lean ecosystem             10       Limitations
(388,105 declarations across 25 projects, 11.3M
typed edges) through a shared slogan-embedding               TheoremGraph is built from arXiv LATEX source, a
space. Embedding both corpora into one in-                   large structured corpus that does not cover all math-
dex turns cross-formality matching into a nearest-           ematical writing. Informal dependency extraction
neighbor query: an LLM judge affirms 47,952                  is necessarily approximate, so the released graph
matches above a 0.8 cosine floor, affirmed in 87%            preserves per-extractor labels, letting users pick
of its ≥ 0.9-similarity candidates. The same rep-            their own precision–coverage tradeoff.
resentation improves downstream tasks over lex-                 The cross-formality bridge relies on LLM-
ical and dense-only baselines: it raises retrieval-          generated slogans and Qwen3-Embedding-8B em-
augmented autoformalization from 5/24 to 8/24                beddings, and sloganization is lossy. The matching
evaluated-correct targets, and on MathlibQR fair-            judge works from slogans with limited context, and
810 it comes within 0.5pp of LeanSearch v2’s                 our expert calibration covers only ten pairs, so not
reranked Recall@10 (0.775 vs. 0.780) without an              every judge-affirmed match is ground truth. Giv-
LM reranker. We release the dataset, extractors,             ing judges more context, such as the source paper,
HTTP API, and MCP interface as infrastructure                is a natural way to improve cross-corpus linking,
for mathematical search and retrieval-augmented              alongside evaluating alternative slogan generators,
reasoning.                                                   embedding models, rerankers, and a broader judge
                                                             panel. Because matching takes only the single

                                                        10
nearest candidate over an arXiv-only corpus, well-             Carl Bergstrom. 2007. Eigenfactor: Measuring the
known results go unmatched when their counterpart                value and prestige of scholarly journals. College
                                                                 and Research Libraries News, 68(5):314–316.
is absent.
   Our downstream evaluations focus on settings                Rong Bian, Yu Geng, Zijian Yang, and Bing Cheng.
with gold labels: blueprint pairs, 24 autoformal-                2025. Automathkg: The automated mathematical
ization targets, and the MathlibQR fair-810 sub-                 knowledge graph based on llm and vector database.
                                                                 Preprint, arXiv:2505.13406.
set. The same configuration does not transfer to
chained-premise retrieval: applying the QR-tuned               Lukas Blecher, Guillem Cucurull, Thomas Scialom,
settings lowers MathlibMPR group Recall@10                       and Robert Stojnic. 2023. Nougat: Neural optical
from 0.224 to 0.165. Concept retrieval and chained-              understanding for academic documents. Preprint,
                                                                 arXiv:2308.13418.
premise retrieval appear to need different signals,
which we leave to future work.                                 Jiangjie Chen, Wenxiang Chen, Jiacheng Du, Jinyi Hu,
                                                                  Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing Jin,
Data availability. The TheoremGraph dataset,                      Chenggang Li, Wenlei Shi, Zhihong Wang, Mingx-
the LeanGraph and informal extractors, and                        uan Wang, Chenrui Wei, Shufa Wei, Huajian Xin,
the HTTP API and MCP interface are avail-                         Fan Yang, Weihao Gao, Zheng Yuan, Tianyang Zhan,
able at theoremsearch.com.            The judged                  and 3 others. 2025. Seed-prover 1.5: Mastering
                                                                  undergraduate-level theorem proving via learning
formal–informal matches are released at                           from experience. Preprint, arXiv:2512.17260.
huggingface.co/datasets/uw-math-ai/theorem-
matching.                                                      frenzymath. 2024. jixia: A static analysis tool for
   Because arXiv’s default license grants no third-               lean 4. https://github.com/frenzymath/jixia.
                                                                  GitHub repository, accessed 2026-05-23.
party redistribution right, the public release is
restricted to statements carrying an open, redis-              Guoxiong Gao, Haocheng Ju, Jiedong Jiang, Zihan Qin,
tributable license: a subset of 23,399 judged can-               and Bin Dong. 2025. A semantic search engine for
didates, gated for non-commercial research. We                   mathlib4. Preprint, arXiv:2403.13310.
license our own contributions (the slogans, judg-              Guoxiong Gao, Zeming Sun, Jiedong Jiang, Yutong
ments, and metadata) under CC-BY-NC-SA-4.0,                      Wang, Jingda Xu, Peihao Wu, Bryan Dai, and
applied to the compilation as a whole rather than                Bin Dong. 2026. Leansearch v2: Global premise
                                                                 retrieval for lean 4 theorem proving. Preprint,
to the underlying statements; each record addi-
                                                                 arXiv:2605.13137.
tionally carries its statement’s original license in
a source_license field, which governs reuse of                 Eugene Garfield. 1972. Citation analysis as a tool in
that statement’s content.                                        journal evaluation. Science, 178(4060):471–479.

                                                               Xiaojun Guo, Ang Li, Yifei Wang, Stefanie Jegelka,
                                                                 and Yisen Wang. 2025. G1: Teaching llms to reason
References                                                       on graphs with reinforcement learning. Preprint,
Akiko Aizawa, Michael Kohlhase, Iadh Ounis, and                  arXiv:2505.18499.
  Moritz Schubotz. 2014. Ntcir-11 math-2 task
  overview.                                                    J. E. Hirsch. 2005. An index to quantify an individual’s
                                                                  scientific research output. Proceedings of the Na-
Jesse Alama, Lionel Mamane, and Josef Urban. 2012.                tional Academy of Sciences, 102(46):16569–16572.
   Dependencies in formal mathematics: Applica-
   tions and extraction for Coq and Mizar. Preprint,           Jonas Hübotter, Frederike Lübeck, Lejs Behric, An-
   arXiv:1109.3687.                                              ton Baumann, Marco Bagatella, Daniel Marta, Ido
                                                                 Hakimi, Idan Shenfeld, Thomas Kleine Buening,
Luke Alexander, Eric Leonen, Sophie Szeto, Artemii               Carlos Guestrin, and Andreas Krause. 2026. Re-
  Remizov, Ignacio Tejeda, Jarod Alper, Giovanni In-             inforcement learning via self-distillation. Preprint,
  chiostro, and Vasily Ilin. 2026. Semantic search over          arXiv:2601.20802.
  9 million mathematical theorems. arXiv preprint.
                                                               Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick
Artifex Software, Inc. 2026. PyMuPDF Documentation.
                                                                 Lewis, Ledell Wu, Sergey Edunov, Danqi Chen,
  Accessed: 2026-06-22.
                                                                 and Wen tau Yih. 2020. Dense passage retrieval
Michael Artin. 2011. Algebra, 2 edition. Pearson.                for open-domain question answering. Preprint,
                                                                 arXiv:2004.04906.
Andrej Bauer, Matej Petković, and Ljupčo Todor-
  ovski. 2023.    Mlfmf: Data sets for machine                 Lean FRO. 2026. lean4export: Plain-text declaration
  learning for mathematical formalization. Preprint,             export for lean 4. GitHub repository. Accessed: 2026-
  arXiv:2310.16005.                                              05-25.


                                                          11
Lean Prover Community. 2026. doc-gen4: Document                  Delip Rao, Jonathan Young, Thomas Dietterich, and
  generator for lean 4. Accessed May 25, 2026.                     Chris Callison-Burch. 2024.        Withdrarxiv: A
                                                                   large-scale dataset for retraction study. Preprint,
Xinze Li, Nanyun Peng, Simone Severini, and Patrick                arXiv:2412.03775.
  Shafto. 2026. The network structure of mathlib.
  Preprint, arXiv:2604.24797.                                    Borja Requena, Austin Letson, Krystian Nowakowski,
                                                                   Izan Beltran-Ferreiro, and Leopoldo Sarra. 2026.
Minhua Lin, Zongyu Wu, Zhichao Xu, Hui Liu, Xi-                    A minimal agent for automated theorem proving.
  anfeng Tang, Qi He, Charu Aggarwal, Hui Liu, Xi-                 Preprint, arXiv:2602.24273.
  ang Zhang, and Suhang Wang. 2025. A comprehen-
  sive survey on reinforcement learning-based agentic            Christian Steinfeldt and Helena Mihaljević. 2024. Eval-
  search: Foundations, roles, optimizations, evalua-               uation and domain adaptation of similarity models
  tions, and applications. Preprint, arXiv:2510.16724.             for short mathematical texts. In Intelligent Com-
                                                                   puter Mathematics: 17th International Conference,
Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos San-                   CICM 2024, Montréal, QC, Canada, August 5–9,
  tos, Weikun He, Jiawei Liu, Ran Wang, Yunzhou Xie,               2024, Proceedings, page 241–260, Berlin, Heidel-
  Junqiao Zhao, Qiufeng Wang, Lihong Zhi, Jia Li, and              berg. Springer-Verlag.
  Wenda Li. 2026. Numina-lean-agent: An open and
  general agentic reasoning system for formal mathe-             Qwen Team. 2025. Qwen3 technical report. Preprint,
  matics. Preprint, arXiv:2601.14027.                             arXiv:2505.09388.
Yu. A. Malkov and D. A. Yashunin. 2018. Efficient and            George Tsoukalas, Jasper Lee, John Jennings, Jimmy
  robust approximate nearest neighbor search using                 Xin, Michelle Ding, Michael Jennings, Amitayush
  hierarchical navigable small world graphs. Preprint,             Thakur, and Swarat Chaudhuri. 2024. Putnam-
  arXiv:1603.09320.                                                bench: Evaluating neural theorem-provers on
Behrooz Mansouri, Vít Novotný, Anurag Agarwal, Dou-                the putnam mathematical competition. Preprint,
  glas W. Oard, and Richard Zanibbi. 2022. Overview                arXiv:2407.11214.
  of arqmath-3 (2022): Third clef lab on answer re-
                                                                 Dylan Walker, Huafeng Xie, Koon-Kiu Yan, and
  trieval for questions on math. In Experimental IR
                                                                   Sergei Maslov. 2007. Ranking scientific publica-
  Meets Multilinguality, Multimodality, and Interac-
                                                                   tions using a model of network traffic. Journal
  tion: 13th International Conference of the CLEF
                                                                   of Statistical Mechanics: Theory and Experiment,
  Association, CLEF 2022, Bologna, Italy, September                2007(06):P06010–P06010.
  5–8, 2022, Proceedings, page 286–310, Berlin, Hei-
  delberg. Springer-Verlag.                                      Sean Welleck, Jiacheng Liu, Ronan Le Bras, Hannaneh
Patrick Massot. 2020. leanblueprint: A plastex plu-                Hajishirzi, Yejin Choi, and Kyunghyun Cho. 2021.
  gin for writing blueprints of lean formalization                 Naturalproofs: Mathematical theorem proving in nat-
  projects. https://github.com/PatrickMassot/                      ural language. Preprint, arXiv:2104.01112.
  leanblueprint. GitHub repository; originally de-               Banri Yanahama and Akiyoshi Sannai. 2026. Lean
  veloped for the Sphere Eversion Project. Accessed                atlas: An integrated proof environment for scal-
  2026-05-26.                                                      able human-ai collaborative formalization. Preprint,
Mathpix. 2026. Mathpix Markdown: Markdown                          arXiv:2604.16347.
 for math and science. https://mathpix.com/
                                                                 Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chala-
 mathpix-markdown. Accessed: 2026-06-22.
                                                                   mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
Shrey Mishra, Yacine Brihmouche, Théo Delemazure,                  Prenger, and Anima Anandkumar. 2023. Leandojo:
  Antoine Gauquier, and Pierre Senellart. 2024. First              Theorem proving with retrieval-augmented language
  steps in building a knowledge base of mathematical               models. Preprint, arXiv:2306.15626.
  results. In Proceedings of the Fourth Workshop on
  Scholarly Document Processing.                                 Richard Zanibbi, Akiko Aizawa, Michael Kohlhase,
                                                                   Iadh Ounis, Goran Topic, and Kenny Davila. 2016.
Azim Ospanov, Farzan Farnia, and Roozbeh Youse-                    Ntcir-12 mathir task overview. In NTCIR Conference
  fzadeh. 2025. minif2f-lean revisited: Reviewing                  on Evaluation of Information Access Technologies.
  limitations and charting a path forward. Preprint,
  arXiv:2511.03108.                                              Richard Zanibbi, Kenny Davila, Andrew Kane, and
                                                                   Frank Tompa. 2015. The tangent search engine: Im-
Gabriel Pinski and Francis Narin. 1976. Citation influ-            proved similarity metrics and scalability for math
  ence for journal aggregates of scientific publications:          formula search. Preprint, arXiv:1507.06235.
  Theory, with application to the literature of physics.
  Information Processing and Management, 12(5):297–              Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang,
  312.                                                             Huan Lin, Baosong Yang, Pengjun Xie, An Yang,
                                                                   Dayiheng Liu, Junyang Lin, Fei Huang, and Jingren
Stanislas Polu and Ilya Sutskever. 2020. Generative                Zhou. 2025a. Qwen3 embedding: Advancing text
   language modeling for automated theorem proving.                embedding and reranking through foundation models.
  Preprint, arXiv:2009.03393.                                      Preprint, arXiv:2506.05176.


                                                            12
Yizhuo Zhang, Heng Wang, Shangbin Feng, Zhaox-
  uan Tan, Xinyun Liu, and Yulia Tsvetkov. 2025b.
  Generalizable llm learning of graph synthetic
  data with post-training alignment.    Preprint,
  arXiv:2506.00845.
Kunhao Zheng, Jesse Michael Han, and Stanislas
  Polu. 2022. Minif2f: a cross-system benchmark
  for formal olympiad-level mathematics. Preprint,
  arXiv:2109.00110.
Karol Zyczkowski. 2009. Citation graph, weighted im-
  pact factors and performance indices. Scientometrics,
  85.




                                                          13
A    Example Judge-Rejected and Missed Informal Dependencies
For each extractor and for the judge, we present three samples drawn from the 500-paper judge subset.
The first three tables show edges the parser found but the LLM judge rejected; the fourth shows edges
only the judge identified. Statement bodies are reproduced from the parsed LATEX source.
Table 7: Deterministic edges the judge rejected. The first and last are explicit author-declared restatements that the
judge rejected. The second makes an explicit reference to a lemma in the proof.

Source statement                                                Dependency statement
            From “Object-unital groupoid graded rings, crossed products and separability” (arXiv:2001.05164)
Proposition 48. (Theorem 3) Suppose that L/K is a separable Theorem 3. Suppose that L/K is a separable (not necessarily
(not necessarily finite) field extension. Then the object crossed finite) field extension. Then the object crossed product R =
product R = (L/K, β) is separable over R0 if and only if (L/K, β) is separable over R0 if and only if AutK (L) is
AutK (L) is finite. In particular, if L/K is Galois, then R is finite. In particular, if L/K is Galois, then R is separable
separable over R0 = L if and only if L/K is finite.               over R0 = L if and only if L/K is finite.
                     From “Koszul duality and equivalences of categories” (arXiv:math/0012264)
                                                                                           !
Corollary 5.9. Let P be any complex in KomF(U ). (a) Lemma 5.4. Let      Q I ∈ KomCoF(A , d) be (forgetting the dif-
H p G(P ) = H p (k ⊗U P ). (b) P is in NK(U ) iff P and ferential) I = p>0 Homk (A! , N p (−p)). Then H p F (I) =
k ⊗U P are acyclic.                                       0 for p ≤ 0.
               From “Cluster Algebras, Invariant Theory, and Kronecker Coefficients II” (arXiv:1711.00163)
                                                                                                                      m
                                                         flm
Theorem 2. (Theorem 2.0.1.22) There is a rigid potential W      Theorem 2.0.1.22. The rigid potential IQP (3ml , W l ) is a
on 3
   e l such that (3
     m              m fm
                  e l , Wl ) is a polyhedral cluster model.     polyhedral cluster model and its Jacobian algebra is finite-
                                                                dimensional.


Table 8: Heuristic edges the judge rejected. These illustrate a common heuristic failure: sibling theorems in adjacent
positions, where proximity-weighted scoring fires but the two are parallel results rather than a dependency.

Source statement                                                 Dependency statement
                                From “On the spectral ν-continuity” (arXiv:2009.08977)
Theorem 4.2. Let T ∈ Φ(H) be such that T satisfies Theorem 4.1. Let T ∈ Φ(H) be such that 0 ∈             / σw (T ) or
Browder’s theorem. If 0 ∈ acc σw (T ) and (Tn ) is a se- 0 ∈ acc σw (T ). If (Tn ) is a sequence of essentially G1
                                                ν                                  ν
quence of essentially G1 operators such that Tn −
                                                → T , then operators such that Tn −→ T , then σw (Tn ) → σw (T ).
σ(Tn ) → σ(T ).
                             From “Polar Codes for the m-User MAC” (arXiv:1002.0777)
Lemma 7. U2,4 cannot be the uniform rate region of any Lemma 6. A4 ⊂ BMAT4 ⊊ MAT4 .
MAC with four users and binary inputs.
       From “A characterization of Johnson and Hamming graphs and proof of Babai’s conjecture” (arXiv:1912.11427)
Fact A.12. Let X be a generalized 2d-gon of order (s, s) for Theorem A.11. A generalized 2d-gon of order (s, t) exists
2d ≤ 6, s > 1. Then the zero-weight spectral radius of X only for 2d ∈ {4, 6, 8, 12} unless s = t = 1. If s > 1, then
satisfies ξ(X) ≤ 2s.                                         2d ̸= 12.


Table 9: Notation edges the judge rejected. These show the dominant notation-extractor failure mode: shared
symbols (Ω, S, X : Σ → S2 × R) without genuine dependency.

Source statement                                                 Dependency statement
                 From “Padé Approximants, density of rational functions in A∞ (Ω). . . ” (arXiv:1212.4394)
Proposition 6.3. There exist a Jordan domain Ω and a function Lemma 5.4. Let Ω be an open set, Ω ⊆ C. Then for every
f ∈ A(Ω) such that the antiderivative of f is not bounded                                       0
                                                              N ∈ N we have (Ω ∩ D(0, N )) = (Ω ∩ D(0, N )).
inside Ω.
                        From “Weak Convergence of Probability Measures” (arXiv:2007.10293)
Corollary 3.12 (Mapping theorem). Let h : S → S ′ be a Theorem 3.9 (Prokhorov, direct part). If a family of prob-
continuous mapping between two metric spaces. If Pn ⇒ P ability measures Π on (S, S) is tight, then it is relatively
on S and P has a separable support, then Pn h−1 ⇒ P h−1 compact.
on S ′ .




                                                               14
                                Table 9: Notation edges the judge rejected (continued)

Source statement                                                Dependency statement

                        From “The Gauss map of minimal surfaces in S2 × R” (arXiv:2006.09995)
Proposition 4.7. There is no minimal conformal immersion Proposition 4.3. Let X : Σ → S2 × R be a minimal confor-
X : Σ → S2 × R whose Gauss map g is an anti-holomorphic mal immersion and g its Gauss map. Then g is constant if and
non-constant map.                                          only if X(Σ) is part of a vertical cylinder over a geodesic of
                                                           S2 in S2 × R.


Table 10: Edges only the judge identified, typically genuine proof-level dependencies the parser missed because the
author used the prior result implicitly.

Source statement                                                Dependency statement
                    From “Graphs with large chromatic number induce 3k-cycles” (arXiv:1408.2172)
Theorem 8. If G is a connected trinity graph with large Theorem 1. Every vertex r in a connected trinity graph G
chromatic number and r is a vertex of G, there exists a shadow with large chromatic number is the origin of a large-order
or an antishadow.                                              TCP.
                            From “Weak Convergence of Probability Measures” (arXiv:2007.10293)
Theorem 1.6. The following three conditions are equivalent: Definition 1.5. An open cover of A ⊂ S is a class of open
(i) S is separable; (ii) S has a countable base (a class of open sets whose union contains A.
sets such that each open set is a union of sets in the class); (iii)
Each open cover of each subset of S has a countable subcover.
   From “Extension of isometries between unit spheres of finite-dimensional polyhedral Banach spaces” (arXiv:1206.4839)
Corollary 4.3. If dim X = 2, then F is Gateaux differen- Theorem 4.2. In the following cases we can guarantee the
tiable at every non-zero point.                                  Gateaux differentiability of F at a point y ∈ SX : (i) if y ∈
                                                                 Σ(X); (ii) if lin ‫(ג‬y) = X ∗ .




                                                             15
B       Retrieval and Matching Validation
This appendix provides the supporting data for the retrieval and judging claims made in §6. We report
the judge-calibration study behind our choice of judge of record, bidirectional open-pool retrieval on
the blueprint pairs, the cross-project twin candidates surfaced by the same embedding, and the per-bin
judging breakdown with representative judged examples.

B.1      Choosing the judge
Our first judge was Opus 4.8, run on all candidate pairs with a cosine similarity greater than 0.9; a domain
expert then sampled and graded ten of its judged matches. Table 11 shows these ten, each with its Opus 4.8
rating, Our expert’s verdict and abridged note, and the rating GPT-5.4 produced on the same task. Our
expert found Opus to be over-generous on five, over-calling matches as exact where the paper’s result
was only a special case or a different statement. The over-accepted cases recurred in three ways: the Lean
statement was strictly more general than the paper’s; a surface match hid a different underlying definition;
or a more faithful Lean counterpart existed but was never surfaced.
   These slip through because the judge works from compressed evidence. Sloganization abstracts away
the hypotheses and definitions that separate a true match from a near one, so the judge over-indexes on the
slogan. The Lean signature has the same problem from the other side: a generically named type can carry
more specific assumptions than its name suggests, context an author or implementer reads off immediately
but the judge never holds.

B.2      Calibrating the judge of record
Having rejected Opus, we now validate the judge of record. The same domain expert graded a fresh ten
candidates spanning the full ≥ 0.8 band, with GPT-5.4’s verdict visible only after the expert’s own call.
Table 12 shows the result.
   The two disagreements are scope-direction errors in opposite directions.                          On
Measure.finiteAt_nhdsWithin, the informal is the definition of local finiteness and the Lean
lemma is a one-line consequence assuming it; the expert reads this as a level mismatch and grades wrong,
GPT-5.4 softens to inexact. On map_neighborFinset_induce, the Lean lemma is the same structural
statement as the paper’s claim transposed from directed graphs to undirected; the expert reads this as a
faithful cross-category analogue and grades inexact, GPT-5.4 hardens to wrong.
   On the eight agreed verdicts, the expert’s and judge’s rationales tend to name the same distinction
in different words. At the strict-vs-non-strict level (add_lt_add_of_le_of_lt) and at the integration-
theory level (lintegral_prod_right’) GPT-5.4 catches the gap without prompting. We therefore retain
GPT-5.4 as the judge of record, and read the per-bin totals in Table 15 with the understanding that the
strict wrong/inexact split is judge-dependent in the way this calibration documents.

B.3      Open-pool retrieval
We also validated retrieval bidirectionally on the blueprint pairs.9 We queried each pair’s endpoint and
checked whether its annotated partner was returned at rank 1 (Table 13). The two directions search
different candidate sets. In the formal-to-informal direction (f → i), the formal statement queries the
full 11.7M-statement informal corpus, exactly as in the discovery sweep of §6. In the informal-to-formal
direction (i → f ), the informal statement queries only the 36,708 declarations from the formalization
projects, not the full 385,657-declaration formal graph searched in §6. This restriction is appropriate
because every blueprint \lean{} target is a project declaration; the remaining Mathlib and Lean-core
declarations contain no possible answer and would only add distractors.
   We find that disjoint pairs are largely missed across both directions of querying. In particular, 61.2%
[58.9, 63.6] of blueprint pairs are recovered by at least one direction, and 22.3% [20.2, 24.4] are mutual
rank-1. As a non-semantic baseline, we also reran i → f over the same project declarations using
BM25, a standard lexical ranker based solely on weighted query–candidate term overlap. Because the
    9
   Blueprint pairs are the reference standard throughout this appendix. Confidence intervals on the retrieval and twin-count
numbers are 2,000-resample bootstraps (seed 42).


                                                            16
 formal node              sim    Opus 4.8   Expert   GPT-5.4    Expert’s note (abridged)
 append_assoc            0.920      ex        wr       inx      Neither rater grasps the graph structure: Lean’s
                                                                SimpleGraph is loopless (irreflexive), but the paper’s
                                                                graphs allow self-loops. A poor match.
 toMatrix_adjoint        0.968      ex        ex       inx      “Given bases” is imprecise from the slogan, but the pa-
                                                                per means a unitary isomorphism (orthonormal basis),
                                                                so it is exact, though not a faithful translation.
 lt_of_sub_pos           0.909      ex        ex        ex      Agree, up to the convention that N excludes 0; too
                                                                trivial to give any insight.
 inner_tmul              0.927      ex        wr       inx      Lean is wrong: Lean’s is a general lemma on inner
                                                                products of tensor products; the paper’s is a special
                                                                family of word spaces, an instance of Lean’s theorem
                                                                at best.
 measureEntropy          0.915      inx       ex       inx      Outside my area, but Lean’s looks slightly more gen-
                                                                eral; likely a strong match.
 norm_le_interpStrip     0.928      ex        wr       inx      Lean matches the standard Hadamard three-lines the-
                                                                orem, but the paper’s printed Lemma 10 reverses the
                                                                endpoint exponents, so as written it should be judged
                                                                incorrect.
 iff_rTensor             0.942      ex        inx      inx      Exact after specializing to a commutative ring, but the
                                                                paper’s definition is for a left module over a possibly
                                                                noncommutative ring while Mathlib is commutative-
                                                                only. Inexact.
 coveringNumber          0.926      ex        inx       wr      The informal is the usual external covering number;
                                                                Mathlib’s is the internal one (covering set ⊆ A).
                                                                externalCoveringNumber is the better match. Inex-
                                                                act at best.
 exists_prime            0.955      ex        ex        ex      Agree, both are the natural-number form of Bertrand’s
                                                                postulate. An easy one.
 wnorm_mono              0.945      ex        ex       inx      Agree, monotonicity of the weak Lp norm under a.e.
                                                                domination; Lean is more general but a strong match.

Table 11: Expert calibration of ten Opus 4.8 matches at ≥ 0.9. For each candidate: its similarity and the verdicts
of the original judge (Opus 4.8), the expert, and the judge of record (GPT-5.4), with the expert’s abridged note.
 ex =exact, inx =inexact, wr =wrong. Opus matches the expert on four, over-calls exact on five, and is over-strict
on one (measureEntropy); GPT-5.4 is stricter than Opus but, at this sample size, does not fully track the expert.




                                                       17
formal node                                       sim     Expert    GPT-5.4   Expert’s note (abridged)
rpow_add_le_mul_rpow_add_rpow                    0.974        ex      ex      Same inequality. Lean’s NNReal is [0, ∞), potentially
                                                                              slightly stronger than the paper if its R+ is open.
PerfectlyNormalSpace                             0.957        ex      ex      Same definition. The paper’s standing “all spaces
                                                                              are T1” assumption is slightly stronger than Mathlib’s
                                                                              PerfectlyNormalSpace; T1 is bundled separately in
                                                                              T6Space.
LieSubalgebra.lie_mem                            0.927        inx     inx     Lean is a field accessor on an existing LieSubalgebra;
                                                                              the informal asserts the definition plus the inheritance
                                                                              claim that h is itself a Lie algebra.
alternatingGroup_le_. . . _isThreeCycle_mem      0.917        ex      ex      Jordan’s theorem in both. IsPreprimitive differs
                                                                              from classical primitivity only in nonemptiness, forced
                                                                              here by the 3-cycle; faithfulness is automatic from
                                                                              G ≤ Equiv.Perm α.
AEMeasurable.lintegral_prod_right’               0.914        wr      wr      Lean is a.e.-measurability of the inner lower integral
                                                                              on R∞≥0 ; informal is the full vector-valued Bochner
                                                                              Fubini theorem.
Measure.finiteAt_nhdsWithin                      0.882        wr      inx     Informal is the definition of locally finite. Lean is a one-
                                                                              line filter-level consequence assuming it; the faithful
                                                                              counterpart is the class IsLocallyFiniteMeasure.
HasDerivAt.inner                                 0.880        inx     inx     Special case of the informal directional-derivative prod-
                                                                              uct rule, restricted to ordinary derivatives on R → E.
starIsoTerminal_inv                              0.865        wr      wr      Informal is the definition of a terminal object. Lean is
                                                                              an equality between two specific morphisms inside the
                                                                              constructed category WithTerminal C; uses terminal-
                                                                              object machinery without stating the universal prop-
                                                                              erty.
add_lt_add_of_le_of_lt                           0.844        wr      wr      Paper is non-strict on both sides; Lean takes mixed
                                                                              non-strict/strict and concludes a strict inequality. The
                                                                              closer counterpart is add_le_add.
map_neighborFinset_induce                        0.822        inx     wr      Same structural idea but the paper is directed in-
                                                                              neighborhoods in a sub-tournament; Lean is undirected
                                                                              SimpleGraph neighbors. A faithful cross-category ana-
                                                                              logue, not the same statement.

Table 12: Calibration of GPT-5.4 against the expert on ten candidates spanning the full ≥ 0.8 band. ex =exact,
 inx =inexact, wr =wrong. GPT-5.4 agrees with the expert on 8/10 verdicts strictly, and on 9/10 when collapsed to
match/non-match (exact+inexact vs. wrong).




                                                         18
embedding-based method outperforms BM25 at every cutoff, its matches cannot be explained solely by
shared surface vocabulary and instead reflect semantic agreement.

                               Sweep               Hit@1     Hit@5   Hit@10   MRR
                               Embedding f → i       43.5     64.8     69.9    52.5
                               Embedding i → f       42.6     67.0     71.7    53.1
                               BM25 i → f            31.3     53.7     61.0    41.0

Table 13: Open-pool retrieval (%). n is the number of distinct evaluable queries: 1,530 of the 1,577 blueprint
formals for f → i (47 lack an evaluable open-pool partner), 1,308 blueprint informals for i → f . BM25 is a lexical
baseline.



B.4   Match types
Because both graphs are embedded in one space, the same slogan retrieval surfaces three kinds of match
depending on which corpora the query and its neighbor come from (Figure 6): a formal–informal match
(f ↔ i), the matches of §6 which the open-pool retrieval above validates; a cross-project twin (f ↔ f ), the
same result formalized in two projects, which we probe below; and a cross-paper restatement (i ↔ i), the
same result stated in two papers, which we do not pursue here.




Figure 6: Three kinds of match the slogan embedding can surface, by the corpora of the query and its nearest
neighbor: a formal–informal match (f ↔ i), a cross-project twin (f ↔ f ), and a cross-paper restatement (i ↔ i).



B.5   Candidate cross-project twins (f → f )
The same slogan embedding can be swept formal-to-formal across the project declarations to surface
candidate twins: a project lemma whose nearest neighbor is a lemma in a different project. Excluding
same-paper matches and two parallel-formalization repository pairs, 446 [253, 682] pairs sit at cosine
≥ 0.85 (14 at ≥ 0.95); Table 14 lists the highest-cosine ones. Consistent with §6, cosine here is a
candidate signal, not ground truth: these pairs are not judge-confirmed, so the count is a candidate set
rather than a verified twin set. Running the same LLM-as-judge step over these candidates to confirm
genuine twins is a natural extension we have not yet performed.

B.6   Judging breakdown
Table 15 gives the per-bin verdict counts behind Figure 2: for each cosine band, how many judged
candidates each model labels exact, inexact, or wrong, and the resulting match rate (exact+inexact).
Both judges move from almost all matches at the top of the band, a mix of exact and inexact, to
mostly wrong near the floor; DeepSeek is uniformly more generous. The two models judge near-identical
candidate sets, with small per-bin differences in n from parse failures and unjudgeable cases.

                                                        19
             sim Candidate twin pair and shared statement
           0.999 NNReal.coe_comp_dconv (add-combi) ↔ NNReal.coe_comp_cdconv (apap): the R≥0 → R
                 coercion commutes with discrete convolution.
           0.988 Φ′4 _contDiffOn (Sphere-Packing-Lean) ↔ same (sphere-packing-math-inc): Φ′4 is continu-
                 ously differentiable on its domain.
           0.987 neg_cdconv (apap) ↔ neg_conv (add-combi): negation distributes through the convolution.

Table 14: Highest-cosine f → f candidate twins. The top pairs are likely equivalent statements under independent
identifier conventions, but the set as a whole is cosine-surfaced and not judge-confirmed.

                          Sim. bin          n    exact      inexact   wrong      match (%)
                                             GPT-5.4 (judge of record)
                          0.95–1.0        676     290        360        26        650 (96.2)
                          0.90–0.95     6,644   1,391      4,312       941      5,703 (85.8)
                          0.85–0.90    26,755   1,834     14,852 10,069        16,686 (62.4)
                          0.80–0.85    66,537   1,250     23,663 41,624        24,913 (37.4)
                          Total       100,612    4,765       43,187   52,660   47,952 (47.7)
                                       DeepSeek-V4-Pro (lenient comparison)
                          0.95–1.0        678     587         80        11    667 (98.4)
                          0.90–0.95     6,645   4,542      1,678       425  6,220 (93.6)
                          0.85–0.90    26,827 11,151       9,195     6,481 20,346 (75.8)
                          0.80–0.85    66,700 14,951      19,050 32,699 34,001 (51.0)
                          Total       100,850   31,231       30,003   39,616   61,234 (60.7)

Table 15: Per-bin judging breakdown for the two judges over the corrected candidate pool (≥ 0.8 cosine), highest
band first. Column headers are colored by verdict ( exact , inexact , wrong ); exact+inexact count as matches.
GPT-5.4 is our set of record, DeepSeek-V4-Pro a more lenient high-recall comparison; the bold totals contrast the
strict (47.7%) and lenient (60.7%) overall match rates.


B.7   Judged match examples
Tables 16 and 17 show representative GPT-5.4-judged candidate edges from the corrected set, each pairing
the formal Lean statement with its informal arXiv counterpart. Table 16 gives one example per verdict
class so the difference between a match and a false positive is visible; Table 17 gives judge-affirmed
(exact) matches at a high, mid, and low point of the 0.9–1.0 band.




                                                            20
  Formal (Lean)                           Informal statement                             arXiv        sim    verdict
  niven {θ : R} (hθ : ∃ r, θ = ↑r         Let θ be a rational multiple of 2π. If         1410.6912    0.97   exact
  * Real.pi) (hcos : ∃ q, Real.cos        cos(θ) ∈ Q,
                                                     then
  θ = ↑q) : Real.cos θ ∈ {-1, -1 /        cos(θ) ∈ −1, − 12 , 0, 12 , 1 .
  2, 0, 1 / 2, 1}

  SemidirectProduct.mul_def {N :          The semidirect product N ⋊φ H has              2111.00575   0.90   inexact
  Type u_1} {G : Type u_2} [Group         underlying set N × H with
  N] [Group G] {φ : G →* MulAut           (n1 , h1 )(n2 , h2 ) =
  N} (a b : N ⋊[φ] G) : a * b             (n1 φ(h1 )(n2 ), h1 h2 ).
  = ⟨a.left * (φ a.right) b.left,
  a.right * b.right⟩

  Ne.symm {α : Sort u} {a b : α}          For all a, b, if a = b then b = a.             0707.1981    0.90   wrong
  (h : a ̸= b) : b ̸= a

Table 16: Representative GPT-5.4 verdicts from the corrected candidate set, one per class: the verbatim Lean
statement, the paper’s informal statement, the arXiv id, the cosine similarity, and the verdict. exact/inexact count
as matches; wrong (lexically near but mathematically distinct, e.g. Ne.symm: symmetry of ̸= vs. the paper’s =) does
not.




  Formal (Lean)                            Informal statement                            arXiv         sim   verdict
   Aux.sum_inv_le_log
             P        (n : N) (hn :        Pnany1 positive integer n,
                                           For                                           2002.05359   0.98   exact
   1 ≤ n) :     d ∈ Finset.Icc 1 n,          t=1 t ≤ 1 + log n.
   (↑d)−1 ≤ 1 + Real.log ↑n

   Real.cos_sq_add_sin_sq (x : R) :        The identity sin2 x + cos2 x = 1 holds        2312.13525   0.95   exact
   Real.cos x ^ 2 + Real.sin x ^ 2         for x ∈ R.
   = 1
                                                                           
   legendreSym.at_neg_two {p : N}          If p is an odd prime,       −2
                                                                       p
                                                                                = 1 if   2309.02512   0.91   exact
   [Fact (Nat.Prime p)] (hp : p ̸=         p ≡ 1, 3 (mod 8) and −1 if p ≡ 5, 7
   2) : legendreSym p (-2) = ZMod.χ′8      (mod 8).
   ↑p

Table 17: Judge-affirmed (exact) matches from the corrected GPT-5.4 set at a high, mid, and low point of the
0.9–1.0 band (similarity ≈ 0.98 / 0.95 / 0.91): the verbatim Lean statement against the paper’s informal statement.
legendreSym.at_neg_two shows the abstract Lean form (= χ′8 (p)) the judge matched to the paper’s explicit
residue cases.




                                                         21
C    Corpus Composition by Library
Our dependency graph spans 388,105 formal declarations and 9,585,510 within-library dependency
edges across 25 Lean libraries. Mathlib dominates both, supplying 90.5% of declarations and 97.4% of
within-library edges; the Mathlib rows aggregate the v4.27–v4.29 snapshots. The remaining libraries are
research/blueprint developments, each contributing at most a few thousand declarations. Their internal
edge counts are sparser still: most of their dependencies point into Mathlib, and such cross-library edges
are excluded here—each count reflects only edges whose source and target lie in the same library. Table 18
reports declarations and within-library edges side by side.

                                       Declarations                       Within-lib. edges
                            Library                    Count Library                            Count
                            Mathlib (v4.27–v4.29)     351,397 Mathlib (v4.27–v4.29)           9,333,251
                            physlib                     8,205    physlib                        93,688
                            PrimeNumberTheoremAnd       5,108    carleson                       27,553
                            sphere-packing-math-inc     4,125    sphere-packing-math-inc        25,867
                            carleson                    2,852    combinatorial-games            24,666
                            combinatorial-games         2,702    PrimeNumberTheoremAnd          20,818
                            FLT                         2,368    cslib                          15,042
                            cslib                       2,273    FLT                            10,833
                            ClassFieldTheory            1,387    sphere-eversion                 6,740
                            sphere-eversion             1,208    pfr                             5,671
                            pfr                         1,073    ClassFieldTheory                4,482
                            brownian-motion             1,071    brownian-motion                 3,124
                            Sphere-Packing-Lean           821    toric                           2,630
                            apap                          670    HarderNarasimhan                2,320
                            formal-conjectures            639    apap                            2,155
                            toric                         485    flt-regular                     1,361
                            misc-yd                       362    misc-yd                         1,200
                            flt-regular                   344    formal-conjectures                976
                            HarderNarasimhan              309    Sphere-Packing-Lean               945
                            add-combi                     190    PersistentDecomp                  785
                            PersistentDecomp              161    add-combi                         507
                            cam-combi                     132    gibbs-measure                     341
                            gibbs-measure                 113    forbidden-matrix                  308
                            forbidden-matrix               86    cam-combi                         170
                            chandra-furst-lipton           24    chandra-furst-lipton               77
                            Total                     388,105 Total                           9,585,510


Table 18: Corpus composition by library: declarations and within-library dependency edges. Cross-library edges
are excluded; non-Mathlib libraries contribute 36,708 declarations (9.5%) and 252,259 within-library edges (2.6%).




                                                                22
D    Extending the Corpus Beyond arXiv: PDF Ingestion
The informal graph (the Informal Graph section) is built entirely from arXiv LATEX source, which excludes
a large body of mathematical writing—textbooks, lecture notes, and older papers—that exists only as
PDF. As a first step toward extending the corpus beyond arXiv, we built a PDF ingestion tool that recovers
statement-level content from PDF sources in the same schema as our existing non-arXiv ingests (e.g.
ProofWiki). We describe the pipeline and report a single-source run on Artin’s Algebra (Artin, 2011);
we treat this as a feasibility study rather than a contribution to the headline corpus, since the resulting
statements lack the cross-reference structure the deterministic and heuristic extractors rely on.
Two-stage extraction. Optical character recognition over an entire textbook is slow and largely wasted,
since most pages carry no theorem-like content. We therefore split ingestion into a cheap localization
pass and an expensive recognition pass. A pymupdf (Artifex Software, Inc., 2026) text scan first identifies
pages whose text contains a numbered environment header (Theorem, Lemma, Proposition, Corollary,
Definition, and similar) at the start of a line, distinguishing genuine headers from in-text references such
as “by Theorem 1.2.” Each matched page is retained together with a one-page buffer on either side, so that
proofs spilling onto an adjacent page are not truncated. The retained pages are copied into a temporary
PDF, and only that reduced document is passed to Nougat OCR (Blecher et al., 2023), which emits
Mathpix Markdown (.mmd): a Markdown-style format with mathematics in LATEX delimiters (Mathpix,
2026). On Artin’s Algebra, 182 of 555 pages carry a numbered environment header, so OCR runs on
roughly a third of the book plus buffer pages rather than the whole volume.
Statement parsing. The Markdown output is parsed into statement records by a line-oriented pass that
recognizes both Nougat’s bold-header style (**Theorem 1.2**) and plain numbered headers. For each
environment it records the type, the environment number, an optional inline title, the statement body,
and—when present—the proof, which is delimited by a leading Proof marker and a closing QED symbol
(□ or ■). Markdown emphasis is stripped while inline and display math spans are masked and restored
intact, so the recognized LATEX survives the cleaning step. The output is a JSON list of statement records
matching the schema of our other non-arXiv sources, which lets ingested PDFs enter the corpus through
the same path as ProofWiki without a separate LATEX-source stage. Multiple PDFs placed in the input
directory are processed in a single batch.
Feasibility run. Table 19 reports the result of running the pipeline on Artin’s Algebra. The tool recovers
406 statements, 242 of which (59.6%) carry an extracted proof, and every recovered statement retains its
environment number. The recovered counts track—and slightly exceed—a strict line-start header count
of the source PDF (75 theorems, 104 propositions, 59 lemmas, 55 corollaries, 13 numbered definitions),
indicating that the parser captures essentially all numbered environments plus a small number formatted
irregularly.

                                      Type          Recovered      With proof
                                      Proposition            126          91
                                      Theorem                 92          52
                                      Lemma                   81          64
                                      Corollary               66          34
                                      Example                 26           1
                                      Definition              15           0
                                      Total                  406         242

Table 19: PDF ingestion of Artin’s Algebra. “With proof” counts statements for which a delimited proof block was
extracted. Proof-bearing counts are illustrative of the proof-splitting behavior and were not separately validated.

Definition yield and authorial style. The low definition count (15) is not an extraction failure but a
property of the source. The book contains only 13 numbered Definition environments; across 102
occurrences of the word “definition” in the text, the remainder are prose definitions introduced inline
and referred back to throughout (“the definition of matrix multiplication,” “a recursive definition of

                                                        23
the determinant”). Artin formalizes a small definitional core as numbered environments and reuses
it in running prose, so definition yield reflects how a given text sets off its definitions rather than the
recognizer’s coverage. This source-dependence is a general feature of OCR-based ingestion: extraction
recovers what a text marks as a numbered environment, and the proportion of content exposed this way
varies by author and by subject area.
Limitations. PDF-derived statements arrive without the machine-readable cross-reference structure
that drives the informal extractors. There are no \label keys, no \ref commands, and no resolvable
reference list, so the deterministic extractor—which achieves 98.8% judge-verified precision on arXiv
source—cannot propose within-source edges for these statements, and the heuristic extractor is limited
to prose cues such as “Theorem 3.2.” Dependency recovery for PDF sources therefore rests largely on
the notation extractor and on the semantic restatement edges of the universal graph as seen in Section 5.
Bringing PDF sources to parity with arXiv ingestion—in particular, recovering usable within-source
references from OCR’d text—is left to future work.




                                                    24
E     Improving Premise Selection of Theorem-Proving Agents
E.1    Introduction
Automated theorem proving and AI-assisted mathematical reasoning depend on premise selection: given a
target theorem, the system must find earlier lemmas and theorems that can be used in its proof. The quality
of these premises largely determines the size of the proof search problem. A relevant lemma can reduce a
difficult goal to a known argument; an irrelevant neighbor increases the number of proof paths the system
must consider. The main difficulty is that semantic similarity is only a proxy for logical dependence. A
theorem is often close in embedding space to statements about the same objects, notation, or topic. Its
proof, however, may cite earlier results that introduce a tool, a reduction, a classification theorem, or a
structural fact whose statement is semantically distinct from the target. A semantic search system can
therefore retrieve plausible mathematical neighbors while missing the premises that a proof actually uses.
   This experiment examines premise selection in a custom environment that wraps TheoremSearch
(Alexander et al., 2026). TheoremSearch ranks statements by similarity to a natural-language query,
but it does not itself learn which query phrasings are likely to retrieve dependencies. We frame query
generation as a sequential decision problem: Given a target theorem, an agent issues a fixed number of
natural-language queries, observes the results, and is rewarded for retrieving true dependencies.
   This motivates the question of whether reinforcement learning can teach a language model to use
semantic search in a way that respects dependency structure. Our results are mixed: training improves
the base Qwen3-8B policy, but performance plateaus below that of frontier models such as Gemini 3.1
Pro and GPT-5.5. Inspection of the learned queries indicates that the policy can formulate coherent,
mathematically precise searches but generally lacks the detailed knowledge of the literature required to
recognize and retrieve the cited result. A simple expansion over the citation graph recovers substantially
more dependencies, suggesting that much of the remaining signal is encoded in the corpus’s graph
structure rather than in embedding-based similarity alone.

E.2    Methodology
We formulate premise selection as an MDP over the TheoremSearch API. The state contains the target
theorem, represented by its natural-language slogan and LATEX body, together with the set of statements
returned by previous queries. The action is a query string passed to a TheoremSearch API call, which
returns the top-k statements by cosine similarity over Qwen3-Embedding-8B slogan embeddings (Zhang
et al., 2025a). The agent may issue at most H queries. The reward gives +1 for each newly retrieved
true dependency, applies a false-positive penalty −α, and gives a terminal bonus proportional to final
dependency recall.
   The policy is a Qwen3 language model trained to generate query strings conditioned on the current
state. We evaluate dependency recall at k=10 over H=6 queries. We use the same configuration for the
prompted GPT-5.5 and Gemini-3.1-Pro baselines, so comparisons isolate the effect of the query policy
rather than the retrieval budget. At each turn, the policy emits a short reasoning trace before the query.
This matches the prompted baselines and, empirically, accounts for a substantial part of the improvement
over the base model.

Self-distillation objective. The retrieval reward is sparse and non-differentiable: most sampled query
sequences retrieve no true dependencies, and the reward cannot directly supervise individual query tokens.
We therefore train the agent using Self-Distillation Policy Optimization (SDPO) (Hübotter et al., 2026),
which uses the best rollout from a sampled group as a feedback signal for policy improvement. For each
target theorem, we sample G=4 rollouts. We select the rollout with the highest dependency recall and
use its query strings as feedback f . The student policy is then trained to match a feedback-conditioned
teacher policy without receiving that feedback at inference time. The per-token loss is a symmetric
Jensen–Shannon divergence over the generated completion:
                                    X
                      LSDPO (θ) =       JS(πθ (· | x, y<t ) ∥ sg πteacher (· | x, f, y<t )) .
                                    t


                                                      25
The teacher is an exponential moving average of the LoRA weights with αEMA =0.01, and sg denotes
stop-gradient. The feedback is the agent’s own highest-recall query sequence from the sampled group,
rather than the ground-truth dependency list. We additionally evaluate a hybrid SDPO+GRPO objective.
SDPO trains the policy to imitate the highest-reward rollout within a sampled group, while GRPO directly
optimizes expected reward using group-relative advantages. The hybrid objective optimizes the sum of
the SDPO imitation loss and the GRPO policy-gradient loss:

                                   Lhybrid (θ) = LSDPO (θ) + λLGRPO (θ),

with λ ∈ [0, 1]. For our test, we used λ = 0.5.

Training and evaluation context. During sampled training rollouts, the agent sees a compact rendering
of each retrieved statement: the slogan (a natural-language summary of the statement), the paper title, the
first author, and the citation count. This lets the policy condition later queries on earlier results. However,
in greedy evaluation, including retrieved results lowers recall. The longer context shifts the model toward
commenting on previous outputs rather than producing a sharper next query. The final reported policy is
therefore trained with result context but evaluated without it. All trained policies are LoRA adapters of
rank 16 on Qwen3-8B, which update about 0.53% of the model parameters.

Citation-graph expansion. TheoremSearch can also return a statement’s one-hop dependency neigh-
borhood; i.e., all results that are one dependency edge away from the target. Since premise selection is
defined by citation-derived dependencies, we test whether retrieved statements can serve as seeds for graph
expansion. After the policy retrieves statements with embedding search, we add the cross-paper one-hop
graph neighbors of those statements to the candidate set. We never expand the target statement itself. To
prevent data leakage, we also remove any statement from the target’s own paper before computing recall.
This prevents the evaluation from rewarding a shortcut in which the system copies citations from sibling
theorems in the same paper.

E.3   Related work
Premise selection is usually studied inside proof-assistant libraries, where a retriever supplies candidate
premises to a prover. LeanDojo retrieves premises for Lean proofs (Yang et al., 2023), LeanSearch
provides semantic search over Mathlib (Gao et al., 2025, 2026), and earlier work trains language models
to generate proofs directly (Polu and Sutskever, 2020). This project differs in two ways. First, retrieval
itself is the task: the agent is evaluated on whether it recovers dependency edges, not on whether a
downstream prover succeeds. Second, the search space is a broad mathematical corpus indexed by dense
slogan embeddings, closer to dense-passage retrieval (Karpukhin et al., 2020; Zhang et al., 2025a) than to
a single formal library.
   The learning setup is related to RL-based agentic search, in which a language model learns to interact
with a search environment through multi-step interactions (Lin et al., 2025). We train with SDPO as the
objective (Hübotter et al., 2026) because it has been shown to improve sample efficiency and accuracy
over strong RLVR baselines (Hübotter et al., 2026). The graph-augmentation experiment is also related to
work showing that language models can benefit from explicit graph structure (Guo et al., 2025; Zhang
et al., 2025b). In this report, the graph is not learned by the model; it is used at retrieval time to expose
dependency edges adjacent to the statements the model already retrieves.

E.4   Results
Policy improvement saturation. Figure 7 shows validation recall during SDPO training. The untrained
Qwen3-8B policy retrieves, on average, 4% of a target’s true dependencies. Adding a short reasoning trace
and training with SDPO raises recall to 7.9%. After that point, further optimization did not meaningfully
improve the result. A learning rate of 10−6 reaches 7.9%, while 5×10−6 reaches 7.7%. Increasing the
training set from 1,000 to 5,060 targets lowers recall to 5.8%. These results place all trained policies in
the same roughly 6–8% band.

                                                      26
                                Table 20: Dependency recall at (k=10, H=6).

            System                                    Recall   Mean # of retrieved candidates
            Qwen3-8B base                             ∼0.04                   ∼60
            Qwen3-8B SDPO                             0.079                   ∼60
             + cross-paper graph augmentation         0.134                   ∼115
             + same-paper graph augmentation          0.227                   ∼140
            Gemini 3.1 Pro                            0.170                   ∼60
            GPT-5.5                                   0.264                   ∼60




Figure 7: Validation recall (k=10, H=6) over SDPO Figure 8: Recall at k=10. Cross-paper graph expansion
training. Recall rises above the base model and then roughly doubles the trained policy’s recall.
flattens near 8%, below the prompted Gemini baseline.


Citation-graph expansion recovers dependencies that embedding search misses. Cross-paper graph
expansion raises recall from 7.9% to 13.4% (Table 20 and Figure 8). This is because the policy often
retrieves a statement near the target, and that nearby statement may cite some of the same background
results as the target. One graph hop can therefore turn a semantic near miss into a true dependency.
This change closes most of the gap to Gemini-3.1-Pro, although it also increases the candidate set from
roughly 60 statements to roughly 115, so the comparison is not on an equal-budget basis. The same-paper
expansion reaches 22.7%, but this is not a valid result for premise selection. Theorems in the same paper
share references and often have overlapping dependency lists. Allowing expansion through same-paper
siblings therefore lets the method recover citations from the structure of the evaluation set rather than
from a dependency-aware query strategy. For this reason, the cross-paper number is the main graph result.

E.5   Discussion
Query precision. The prompted GPT-5.5 and Gemini-3.1-Pro baselines use the same embedding index
and a comparable query budget, but retrieve more true dependencies than the trained Qwen3 policy. The
trained policy also uses its budget and avoids repeated queries, so the main failure mode is not search
control. Instead, it issues mathematically plausible topic queries that rarely name or characterize the exact
earlier theorem cited by the proof. This also explains the negative ablations: more data provide little
additional signal when most rollout groups contain no successful retrieval.

Graph expansion exposes useful structure. Cross-paper expansion improves recall because a retrieved
statement can be useful even when it is not itself a dependency: if it is close in the citation graph, its
own dependencies may overlap with the target’s. The gain is largest for low-degree targets, where a few
good seeds can cover much of the dependency set (Figure 9). The same-paper diagnostic shows why
this must be evaluated carefully. Same-paper expansion reaches 22.7%, but that gain comes from shared
bibliographies and local paper structure, so it is reported only as leakage.

                                                     27
Figure 9: Recall at k=10 by number of true dependencies. Cross-paper graph expansion is most effective for
low-degree targets.


Limitations. Differences within the 6–8% validation band should be treated cautiously because the
trained-policy validation set has only n=150. However, cross-paper graph expansion adds another 5.5
points, which appears to be the more significant statistic. The graph result also uses a larger candidate set,
increasing retrieval from roughly 60 to roughly 115 statements, so future systems should pair expansion
with re-ranking.

E.6   Conclusion
Reinforcement learning improves a Qwen3-8B query policy for premise selection from roughly 4%
to 7.9% dependency recall at k=10 under a six-query budget. The improvement then saturates across
learning rates and training data scales. This suggests the limiting factor is query precision: the policy
learns plausible mathematical searches, but it rarely identifies the exact prior theorem that the target
proof cites. Cross-paper citation-graph expansion raises recall to 13.4% by using retrieved statements
as hints for dependency traversal. Future work should focus on learned graph expansion, re-ranking
expanded candidates to control budget, and training policies that decide which retrieved statements are
worth expanding.




                                                     28
F     Node Distance and Embedding Distance

We examine whether statements that are closer in the dependency graph also have more similar slogan
embeddings. Specifically, we measure the cosine similarity between pairs of statements separated by a
directed graph distance of d dependency edges. Figure 10 reports results for parent-only trajectories.

F.1   Setup
For each formality and depth d, we collected 1,000 accepted statement pairs. Starting from a randomly
sampled initial statement seed, we repeatedly sampled one parent/dependency uniformly at random. At
depth d, we retained the resulting pair only when its directed shortest-path distance from the seed was
exactly d. Thus, accepted walks contain no directed shortcut of length less than d.
   Each depth was sampled independently. In particular, failed walks were replaced, and a new initial seed
redrawn, until reaching the target number of accepted observations, so the samples at depth d should not
be interpreted as continuations of the same trajectories used at depth d − 1.
   For embedding comparison, we used sloganized statements embedded with Qwen3-8B. Embeddings
are ℓ2 -normalized before cosine similarity is computed as their dot product. Error bars show pointwise
95% normal-approximation confidence intervals for the mean cosine similarity. The dashed horizontal
line denotes a graph-free random-pair baseline, computed separately for the formal and informal corpora
as the mean cosine similarity over 1,000 randomly paired, distinct statements.

F.2   Results




      (a) Informal cosine similarity by d-hop distance.          (b) Formal cosine similarity by d-hop distance.

                    Figure 10: Cosine similarity and node depth for informal and formal graphs.


   Figure 10 shows an overall decline in cosine similarity as directed parent-only graph distance increases
in both graphs. The decline is substantially sharper in the formal graph: mean cosine similarity falls from
approximately 0.54 at depth one to roughly the random-pair baseline by depth six. In contrast, informal
pairs remain highly similar even at larger graph distances, declining from approximately 0.61 at depth
one to about 0.51 at depth six, well above the corresponding random baseline.
   Thus, under parent-only dependency paths, informal statements retain greater embedding similarity over
longer graph distances than formal statements. One possible explanation for the faster decline in the formal
graph is its substantially higher local connectivity. Lean records fine-grained dependencies on definitions,
typeclass instances, inherited structure, and other reusable mathematical infrastructure. Theorems about a
narrow topic may have parent dependencies that connect it to broadly applicable declarations, such as
general algebraic or module-theoretic results. Although these edges represent explicit and valid formal
dependencies, they need not preserve strong high-level semantic similarity in the generated slogan space.
By contrast, informal dependency paths may more often remain within a shared local development or
exposition, allowing statements to retain greater embedding similarity over several graph steps.

                                                          29
F.3   Limitations
This analysis conditions on successful trajectories whose endpoints have usable slogan embeddings and
whose directed shortest-path distance is exactly d. As depth increases, obtaining a fixed number of
accepted pairs may therefore favor seed statements with sufficiently rich local neighborhoods, longer
dependency chains, and reachable embedding-eligible endpoints. The resulting samples may not be
representative of all statements at a given graph distance.
  Moreover, each depth is sampled independently, and seed statements, nodes, and local neighborhoods
may recur across sampled trajectories. The reported pointwise confidence intervals treat observations as
independent and therefore may not fully capture uncertainty induced by overlap among walks.

G     In-Context Literature Search
Research mathematicians often need to identify a known result from a partial description embedded in an
ongoing proof or exposition. We study a related task: recovering a cited theorem from a local passage of
mathematical text after its citation has been removed.

G.1    Methodology
We evaluate whether language models can recover cited mathematical results from redacted arXiv passages
using either unrestricted web search or retrieval over our mathematical statement database. We sampled
149 passages from mathematics arXiv papers released after February 2026. Restricting the sample to
recent papers was intended to reduce the likelihood that the evaluated passages were available in the
models’ pretraining data.
   Each selected passage contained a citation command referring to a named theorem, lemma, proposition,
or analogous statement in another arXiv paper. We replaced the citation with [Citation Needed] and
removed the corresponding bibliographic entry from the source paper’s .bib file. Models received the
same redacted passage and complete remaining bibliography in every condition.
   We evaluate three retrieval settings. In the web-search baseline, models had unrestricted web access.
In the dense-retrieval condition, models could issue repeated searches against our statement database,
receiving the top 10 retrieved candidates for each query. In the graph-based condition, models could
repeatedly search and navigate the statement dependency graph. An exact match requires the model
to return both the correct theorem identifier and the cited paper’s arXiv identifier; a paper-level match
requires recovery of the correct cited arXiv paper, irrespective of the theorem identifier.

G.2    Results

                              System              Exact Match Paper-Level Match
                                              Web Search Baseline
                              ChatGPT 5.4              0.336               0.523
                              Gemini 3.1 Pro           0.570               0.752
                              Claude Sonnet 4.5        0.181               0.443
                                                  Dense Retrieval
                              ChatGPT 5.4                0.228             0.409
                              Gemini 3.1 Pro             0.181             0.409
                              Claude Sonnet 4.5          0.121             0.396
                                             Graph-Based Retrieval
                              ChatGPT 5.4              0.255               0.456
                              Gemini 3.1 Pro           0.289               0.597
                              Claude Sonnet 4.5        0.148               0.322

Table 21: In-context citation recovery on 149 redacted arXiv passages. Exact match requires the correct theorem
identifier and cited paper arXiv identifier; paper-level match requires only the correct cited paper.


  Graph-based retrieval improves exact-match performance relative to dense retrieval for all models, and
improves paper-level retrieval for ChatGPT 5.4 and Gemini 3.1 Pro. However, neither database-backed

                                                        30
method outperforms unrestricted web search. The largest gap occurs for Gemini 3.1 Pro, which reaches a
0.570 exact-match rate with web search compared with 0.289 under graph-based retrieval.
   These results suggest that graph navigation can provide useful additional structure beyond dense
statement retrieval, but that the current retrieval interface and agent behavior do not yet match the
effectiveness of unrestricted web search for this task.

G.3   Limitations
The web-search baseline is not a controlled retrieval comparison. Because the models can issue unrestricted
searches, they may recover the original source paper by searching an exact quotation from the surrounding
passage. Once that paper is identified, the redacted citation can often be recovered directly from the source
document. Thus, web-search performance partly reflects access to the original evaluation instance rather
than solely a model’s ability to infer the missing citation from mathematical context.
   The experiment also permits repeated retrieval and navigation actions without a matched search budget
across conditions. Performance therefore reflects a combination of retrieval quality, agent search strategy,
stopping behavior, and the practical affordances of each interface. In particular, dense retrieval returns a
fixed top-10 candidate set per query, whereas graph-based retrieval permits open-ended local navigation.
   Our evaluation set is limited to 149 examples and contains only citations that explicitly name a theorem-
like result in an arXiv paper. It therefore does not represent the broader range of scholarly citations,
including citations for background, methods, attribution, or entire lines of work. Moreover, the ground-
truth citation may not be the only mathematically appropriate response: a model can identify a related
theorem or an alternative source that supports the passage while still being scored as incorrect.




                                                     31
