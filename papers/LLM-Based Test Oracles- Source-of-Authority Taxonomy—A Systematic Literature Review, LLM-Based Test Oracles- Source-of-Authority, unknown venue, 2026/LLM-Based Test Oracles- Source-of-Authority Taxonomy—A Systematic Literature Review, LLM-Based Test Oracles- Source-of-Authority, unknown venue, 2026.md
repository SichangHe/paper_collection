                                        ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                      1




                                                LLM-Based Test Oracles: Source-of-Authority
                                                 Taxonomy—A Systematic Literature Review
                                                            Ali Hassaan Mughal iD , Graduate Student Member, IEEE, and Muhammad Bilal iD



                                           Abstract—Large language models (LLMs) increasingly decide                  by judging the output directly [5]–[7]. This is a fast-growing
                                        whether software behaves correctly, either by writing a test oracle           area [8], [9]: most of the reviewed studies appeared in 2025
                                        or by acting as one. Yet two oracles can look identical and rest on           or later.
                                        different ground: one assertion encodes a written specification,
                                        another only what the model learned in training. Prior secondary                 The literature describes these new oracles. It characterizes
                                        studies sort oracles by form or by technique, rarely by the                   them, however, by a feature that does not, by itself, capture
arXiv:2607.05031v3 [cs.SE] 2 Sep 2026




                                        property that governs how far a verdict can be trusted: where its             how far to trust the verdict. Papers sort oracles by their shape,
                                        authority comes from. This systematic literature review, reported             such as an assertion [3] or a metamorphic relation [10], or by
                                        under the Preferred Reporting Items for Systematic Reviews                    the technique used, such as “LLM as a judge” [5], [7]. They
                                        and Meta-Analyses (PRISMA) 2020 guidelines, screens 2,436
                                        records to 54 included studies, extended by citation searching                rarely ask where the verdict’s authority comes from, yet that is
                                        (snowballing) to 83 in total. We read the corpus along three                  what sets the ceiling on how much to trust it. Two oracles can
                                        axes: the source of an oracle’s authority, the form it takes, and             look identical yet rest on different ground. One assertion may
                                        the mechanism that adjudicates it. Just over half of the corpus               encode a written specification; another, with the same syntax,
                                        reaches a verdict with no specification at all. That is what lets             may encode only what the model guessed.
                                        these oracles work on code with no specification to consult, and
                                        what leaves a challenged verdict with less to fall back on. Source               This review organizes the literature by that missing feature:
                                        and mechanism cross-cut rather than coincide, so a label such                 the source of authority, where the correctness of the verdict
                                        as LLM-as-a-judge names how a verdict is produced, not why                    ultimately comes from. We make three contributions:
                                        it should be trusted. Oracle quality is most often judged by
                                                                                                                       • a taxonomy of oracle sources that extends Barr et al. into
                                        resemblance to a known oracle rather than by whether injected
                                        faults are caught. The first question to ask of any LLM oracle is                 the LLM era, kept separate from two questions the litera-
                                        therefore what one would point to in defending its verdict. The                   ture mixes in: the form of the oracle and the mechanism
                                        protocol, search query, and per-study coding sheet are released.                  that computes pass or fail;
                                            Index Terms—Large language models, LLM-as-a-judge, oracle                  • a systematic literature review (SLR), conducted and re-
                                        problem, software quality assurance, software testing, systematic                 ported under the Preferred Reporting Items for Sys-
                                        literature review, test automation, test oracle.                                  tematic Reviews and Meta-Analyses (PRISMA) 2020
                                                                                                                          guidelines [11], that screens 2,436 records down to 54
                                                                 I. I NTRODUCTION                                         included studies, extended by a citation-searching (snow-
                                             OFTWARE now runs in almost every part of daily life,                         balling) round that adds 29 further studies, for 83 in total;
                                        S    and how much we can trust it depends largely on how
                                        well we test it. A test feeds an input to a program, runs it,
                                                                                                                       • a synthesis of what the lens reveals: specification inde-
                                                                                                                          pendence follows almost entirely from the source; source
                                        and then asks one question: is the result correct? The part of                    and mechanism cross-cut rather than coincide; one source
                                        the test that answers that question is the test oracle. A test is                 category goes unoccupied as a primary source of LLM-
                                        only as good as its oracle.                                                       supplied oracles; and the most frequently reported risks
                                           Deciding what counts as correct is hard. For many programs                     are weak oracles and model hallucination.
                                        there is no easy way to know the right answer in advance.
                                        This difficulty has a name, the oracle problem. Barr et al. [1]                  II. BACKGROUND : T HE O RACLE P ROBLEM IN P LAIN
                                        surveyed it before large language models (LLMs) were in wide                                         T ERMS
                                        use. They organized the known ways to obtain an oracle and                    A. What a test oracle is
                                        showed how often a strong oracle is simply missing.                              Every test has four parts. There is an input; the program
                                           LLMs have changed the picture. An LLM can now write                        under test, often called the system under test; the output
                                        an oracle for a program [2]–[4], or act as the oracle itself                  the program produces; and the oracle, the part that decides
                                           This article has been accepted for publication in IEEE Access. This        whether the output is correct (Fig. 1). The first three parts are
                                        is the author’s version which has not been fully edited and content may       usually easy to set up. The oracle is the difficult one.
                                        change prior to final publication. Citation information: DOI 10.1109/AC-         We will use one small function as a running example
                                        CESS.2026.3729738.
                                           This work received no external funding. The authors declare no conflicts   through the whole article: isLeapYear, which should return
                                        of interest.                                                                  true when a year is a leap year. A year is a leap year if it
                                           A. H. Mughal is an Independent Researcher, USA (e-mail: alihassaan-        divides by 4. The exception is years that divide by 100, which
                                        mughal.work@gmail.com).
                                           M. Bilal is with the Technical University of Munich, Germany (e-mail:      are not leap years, unless they also divide by 400. So 2024
                                        m.bilal@tum.de). He is the corresponding author.                              is a leap year, 1900 is not, and 2000 is. To test the function
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                          2




                                                                         Implementation-derived                     false (baseline)
                                                                         the code's own behavior


                                                                         Specification-derived                                   false      ✓
                                                                         the stated leap-year rule


                                                                         Reference-differential                        false (agrees)
                                                                         a second implementation
     test input           program              output

                                                                         Regression-from-prior-version
      1900            isLeapYear              false
                                                                         the previous release's output            false (unchanged)


                                                                         Human-elicited                                          false      ✓
                                         is this correct?
                                                                         a tester's stated answer
                                     ask each authority:

                                                                         Model-parametric                                        false      ✓
                                                                         the model's own knowledge


                                                                         Implicit-intrinsic                                       bool      ✓
                                                                         returns a boolean, no crash                   not a primary source




Fig. 1. The seven sources of oracle authority, illustrated on isLeapYear(1900). The grey dashed box marks the one category no included study uses as
a primary source (it appears as a secondary source in four systems).



we can run it on the input 1900. Suppose it returns false. Is              C. What LLMs add
that correct? Answering that is the oracle’s job. To answer it,               An LLM can take part in the oracle in two ways. It
the oracle must know from somewhere that 1900 is not a leap                can generate an oracle, for example by reading a function’s
year.                                                                      documentation and writing the assertions that check it [4],
                                                                           [15], [16]. Or it can be the oracle, by looking at an output
                                                                           and judging it directly, the way a human reviewer would [5],
B. Why it is hard                                                          [17], [18]. Both were impractical at scale before LLMs, and
                                                                           both are now common. This raises a new question, the subject
   That “from somewhere” is the core difficulty. For                       of this review: when an LLM writes the oracle, or makes the
isLeapYear the right answers are known, so an oracle is                    verdict itself, where does the authority for that verdict come
easy. For most real programs they are not known in advance                 from?
and are costly to work out by hand. This is the oracle problem:
the difficulty of obtaining a reliable way to judge whether an
output is correct.                                                                III. T HE S OURCE - OF -AUTHORITY F RAMEWORK
   Over the years, testers have found partial answers that                   The central idea of our framework is to separate three
avoid needing the exact right answer for every input. An                   questions that the literature usually treats as one.
assertion [12] states a condition the output must meet, such
as that a year reported as a leap year is divisible by 4. A
                                                                           A. Three distinct questions
metamorphic relation [13] compares two related runs instead
of checking one output against a known value. For example,                    When an LLM-based oracle gives a verdict, we can ask
running the function twice on the same year should give the                three things about it.
same result. Differential testing [14] runs two programs that               1) Source of authority. Where does the correctness of the
should agree and treats any disagreement as a possible bug.                    verdict ultimately come from? By authority we mean the
Each of these gives a verdict without a full description of                    artifact or agent whose word makes the verdict count as
correct behavior. Barr et al. [1] surveyed these and other                     correct: what one would point to when defending a pass
techniques in detail.                                                          or a fail.
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                             3



 2) Form. What shape does the oracle take, for example an                                             TABLE I
    assertion or a metamorphic relation?                                   T HE SEVEN SOURCES OF AUTHORITY AGAINST BARR ET AL .’ S ORACLE
                                                                                                   TAXONOMY [1].
 3) Mechanism. How is the pass-or-fail decision computed,
    for example by running an assertion or by asking the                   This review          Barr et al.           Relation
    model to judge?                                                        Specification-       Specified oracles     Retained; widened to
Most prior work answers only the second or third question.                 derived                                    semi-formal and natural-
The first sets the ceiling on trust: an oracle is only as trust-                                                      language specifications
                                                                           Implementation-      Derived oracles       Subdivided: restricted to
worthy as the source its authority rests on. Trust here means              derived                                    artifacts of the current im-
evidential defensibility, the independent ground a verdict can                                                        plementation
appeal to, rather than a measured error rate; the ordering of              Reference-           Pseudo-oracles (a     Renamed; graded by refer-
                                                                           differential         derived subtype)      ence independence
sources is a conceptual claim, not an empirical result of this             Regression-from-     Derived from previ-   Retained
review. The ceiling is also set by the source’s kind, not the              prior-version        ous versions
quality of the individual artifact: a defective specification can          Implicit-intrinsic   Implicit oracles      Renamed
                                                                           Human-elicited       Human oracle          Retained; sharpened to cri-
in practice rank below a well-validated reference implementa-                                                         teria a person supplies
tion.                                                                      Model-parametric     (no counterpart)      Newly introduced: the
                                                                                                                      model’s         parametric
                                                                                                                      knowledge as the authority
B. Seven sources of authority
   The framework distinguishes seven sources of authority
(Fig. 1). The same program output can be judged by any of             the corpus follows this split, including the few boundary cases
them, each drawing on a different authority.                          that cross it.
   In words: an implementation-derived oracle takes the code,            Because every LLM-based oracle is driven by a prompt,
or the tests already written for it, as the authority. It accepts     it is worth fixing what counts as an external specification
what the code currently does, so it catches later changes             here. A prompt’s task instruction, such as decide whether this
but not a bug that is already present. A specification-derived        output is correct or write assertions for this method, is not
oracle takes an external description of intended behavior as          a specification: it directs the oracle without describing the
the authority. The description can be formal, such as a logical       program’s intended behavior. A specification is an explicit,
postcondition; semi-formal, such as a structured rule or a            auditable description of that intended behavior, such as a
Gherkin scenario; or natural-language, such as a docstring or         docstring, a requirement, an application programming interface
a requirement. A reference-differential oracle takes a separate       (API) contract, or a structured rule; when the verdict rests on
implementation as the authority and flags disagreement. A             such an artifact the oracle is specification-derived, regardless
recent variant uses several implementations the LLM writes            of the mechanism that consumes it and regardless of whether
itself and treats their agreement as the expected answer [19],        the artifact was supplied to the oracle or, in one boundary case,
[20]. The strength of this source rests on how independent            synthesized by the model itself into an executable relation
the reference is: an independently developed reference imple-         (Section V). What separates this from a model-parametric
mentation, a differential comparison among existing imple-            oracle is auditability, not authorship: when the description
mentations, and a consensus among implementations the same            of intended behavior is left implicit in the model’s weights
model generates carry successively weaker independence as-            and never externalized into an inspectable artifact, the oracle
sumptions. The remaining four are a model-parametric oracle           is model-parametric. Whether an external specification pre-
(the model’s own knowledge, with no external reference), a            existed, as opposed to being synthesized on the fly, is the
human-elicited oracle (criteria a person supplies), a regression-     separate axis of specification dependence. Specification depen-
from-prior-version oracle (an earlier version as the reference),      dence is therefore a property of what the oracle is given and
and an implicit-intrinsic oracle (crashes or well-formedness),        produces, not of whether a prompt is present. The channel
each defined in Fig. 1.                                               through which a specification reaches the oracle, whether a
   Table I locates the seven sources against Barr et al.’s oracle     system instruction, the user turn, retrieved context, or a file
taxonomy [1]: five categories are retained or renamed from            the oracle reads, likewise does not change the coding: what
established oracle classes, one is subdivided, and one, model-        matters is that an auditable description of intended behavior
parametric authority, is newly introduced. What prior classifi-       is present, not how it arrived.
cations could not express is not the individual categories but           Two further boundaries need fixing, because the same
the axis itself: they organize oracles by how the artifact is         artifact can be described from either side. Human-elicited
obtained or expressed, not by whose authority the verdict rests       against specification-derived turns on the artifact the verdict
on, and it is the latter that the LLM era makes load-bearing.         appeals to, not on who stands behind it: a durable, inspectable
                                                                      description of intended behavior is a specification whoever
C. Specification dependence                                           wrote it, while a criterion a person supplies for this judgment
   The seven sources split by one question: does the oracle           alone, such as a rubric written for the run or a reviewer’s own
need an external specification? In the idealized split, only          decision, is human-elicited. Implementation-derived against
specification-derived oracles do; the other six are defined to        specification-derived turns on how an existing test suite is
reach a verdict without one. Section V examines how closely           used. We code existing tests as implementation-derived, be-
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                              4



cause the reviewed systems read them as a record of what              RQ2 — The three-axis taxonomy. How does the corpus dis-
the code currently does, so the oracle inherits any fault the         tribute across the source of the verdict’s authority, the form
tests already encode. That is a coding rule and not a claim           the oracle takes, and the mechanism that adjudicates it? The
that tests never carry independent requirements: where a study        three parts track the axes the framework keeps apart.
rests its tests on an external requirement the coding records         RQ2.a (Source of authority): From what source does each
a secondary specification-derived source, as it does for two          oracle draw the authority for its verdict, and how closely
of the implementation-derived studies [60], [96]. Each rule is        does the corpus follow the specification-dependence split those
applied through the anchoring quotation recorded for the study,       source definitions imply?
so a reader who would draw the line elsewhere can see which
                                                                      RQ2.b (Form): In what form is the oracle expressed (asser-
sentence the coding rests on.
                                                                      tion, expected output value, metamorphic relation, invariant,
                                                                      property, classifier label, or exception oracle)?
D. Source is not mechanism
                                                                      RQ2.c (Adjudication mechanism and LLM role): How is
   Source and mechanism cross-cut: a single source can be             the pass/fail computed, and what role does the LLM play in
checked by many mechanisms, and a single mechanism can                that computation?
serve many sources. A specification-derived oracle, for ex-
                                                                      RQ3 — Use and gaps. How are the oracles evaluated, how do
ample, can be checked by running an assertion, by matching
                                                                      they fail, and which regions of the taxonomy remain sparse or
against an expected value, or by asking the model to judge.
                                                                      empty?
“LLM as a judge” is a mechanism, not a source: the judge may
be leaning on a specification, on the model’s own knowledge,          RQ3.a (Evaluation): How is each oracle evaluated, and how
or on criteria a person gave it. A few mechanisms recur across        is the oracle’s own correctness assessed?
different sources (Fig. 9).                                           RQ3.b (Failure modes): What failure modes are reported,
                                                                      and how are they mitigated?
                     IV. R EVIEW M ETHOD                              RQ3.c (Gaps): Which regions of the source-by-mechanism
   This SLR was planned, conducted, and reported under the            space are sparse or empty?
PRISMA 2020 statement [11]. The protocol, the frozen search           A guiding hypothesis, examined in the synthesis, is that the
query, the operational criteria, and the per-record screening log     source of authority (RQ2.a) cross-cuts the adjudication mecha-
are released as supplementary material.                               nism (RQ2.c): the two are conceptually distinct and not in one-
                                                                      to-one correspondence, rather than statistically independent.
A. Objective                                                          The same authority can be checked by different mechanisms,
                                                                      and a single mechanism such as LLM-as-judge can draw on
   The review maps and analyzes the literature on LLM-based           different authorities.
test oracles according to the source from which each oracle
draws its verdict authority. A study is within scope if it (i)
                                                                      C. Protocol and registration
produces a test oracle, or (ii) empirically studies how the oracle
is determined, within a pipeline that uses an LLM. Pre-2021              The search query was frozen on 31 May 2026, and the
foundational work is retained as background through citation          inclusion and exclusion criteria were fixed in writing before
only and is excluded from the primary mapping counts. The             screening began. In place of registration in a public registry,
design is aligned with the established methodology for SLRs           this pre-specified protocol is archived openly in the replication
in software engineering of Kitchenham and Charters [21] in            package [22].
its use of a pre-specified protocol, criterion-based screening,
and structured extraction; those guidelines informed how the          D. Eligibility criteria
review was structured rather than being implemented in full.             A record was included only if all of the following held:
PRISMA 2020 [11] supplies the reporting standard.                     I1 (Oracle focus): The work concerns a test oracle, that is, the
                                                                      mechanism that decides expected behavior or pass/fail (asser-
B. Research questions                                                 tions, expected outputs, properties or invariants, metamorphic
   The review is organized around three research questions            relations, differential comparison, or human judgment), rather
(RQ1–RQ3): RQ1 maps the landscape of the literature, RQ2              than only test-input generation or coverage.
characterizes the corpus along the three-axis taxonomy at the         I2 (LLM involvement): An LLM generates, infers, or de-
review’s core, and RQ3 covers how the oracles are used and            termines the oracle, or the study empirically examines how
where they fall short. Within RQ2, the parts on the source            the oracle is determined or behaves in an LLM-based testing
of authority (RQ2.a) and the adjudication mechanism (RQ2.c)           pipeline.
are the main focus.                                                   I3 (Window): Published between January 2021 and
RQ1 — The landscape.                                                  May 2026; for the citation-searching round, the window
RQ1 (Landscape): What software domains, systems under                 extends to that round’s execution date (August 2026). Each
test, languages, models, and adaptation strategies characterize       arm’s window ends on the date that arm was run. Forward
the LLM-based oracle literature?                                      citation searching necessarily reaches work published after
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                               5



the database search was frozen, and holding that round to              OR "differential testing" OR postcondition* OR precondition
the earlier cut-off would discard the studies it was added to               *
                                                                       OR "user acceptance test*" OR "acceptance test*" OR Gherkin
surface. Criterion I4 still applies, so these additions are peer       OR "behavior-driven" OR "behaviour-driven" OR "behavior-
                                                                            driven development"
reviewed like the rest of the corpus.
                                                                       Search = Concept A AND Concept B
I4 (Form): At least four pages, written in English, with
retrievable full text, peer reviewed and indexed (conference,         The query was rendered per database with identical Boolean
journal, or early access).                                            logic and database-specific syntax, restricted to the computing
A record was excluded if any of the following held:                   subject area, without dropping any term, to remove cross-
E1: Testing of LLMs or natural language processing (NLP)              domain false positives such as the food-science and botany
systems (the LLM is the system under test, for example                senses of “Codex” or “Gherkin”. The exact per-database
bias, hallucination, jailbreak, or robustness testing), rather than   queries and the export procedure are in the supplementary
LLMs used for testing software.                                       material.
E2: LLM test or code generation that does not foreground
an oracle (input-only, coverage-only, prefix-only, or program-        G. Selection process
repair-only).
                                                                         Records exported from the three databases were merged
E3: Hardware-verification assertion or oracle generation, for
                                                                      and de-duplicated by normalized DOI, falling back to a
example in SystemVerilog, register-transfer level (RTL), or
                                                                      normalized title when a DOI was absent. This left 2,245
very large-scale integration (VLSI). This is noted as an ad-
                                                                      unique records. Because the high-recall query admitted mostly
jacent line of work in Section VIII.
                                                                      off-topic records, the corpus was too large to screen every
E4: Secondary studies (surveys, systematic reviews, mapping           record twice by hand. We therefore screened in two stages,
studies). These are excluded from the primary set to avoid            an arrangement disclosed in accordance with PRISMA 2020
double counting, and are retained separately for the discussion       item 8 on the use of automation tools. The first stage was a
of related reviews.                                                   recall-oriented automated pre-filter that removes clearly out-
E5: Non-peer-reviewed preprints. These are deliberately ex-           of-scope records; the second was independent human dual
cluded to keep peer review as an evidence-quality bar (crite-         screening that verifies the retained set in full and validates
rion I4). The resulting under-coverage of preprint venues is          the pre-filter’s exclusions on a stratified sample.
reported as a threat to validity (Section VIII).                            a) Stage 1: automated pre-filter: An LLM (Claude
                                                                      Opus 4.8) [23] classified every one of the 2,245 unique records
E6: Editorials, keynotes, posters, tool demonstrations, tutori-
                                                                      against the eligibility criteria from title and abstract. It as-
als, extended abstracts, items under four pages, non-English
                                                                      signed each an include, maybe, or exclude decision and, where
items, and non-retrievable items.
                                                                      applicable, an exclusion reason code (E1–E6). Ambiguous
                                                                      records were assigned maybe and retained, resolving uncer-
E. Information sources                                                tainty toward full-text assessment. This stage retained 178
   We searched three bibliographic databases under institu-           records and excluded 2,067. Each record was supplied to the
tional subscription: Scopus, IEEE Xplore, and the ACM                 model as its title and abstract together with the pre-registered
Digital Library. All searches were executed on 31 May 2026            inclusion and exclusion criteria, and the model returned an
over the field set title, abstract, and keywords, restricted to       include, maybe, or exclude decision with an exclusion reason
the publication window 2021–2026. Scopus indexes a large              code (E1–E6), retaining any record it could not confidently
fraction of IEEE and ACM content and therefore also serves            exclude. Classification was run in June 2026 with the model’s
as a cross-database consolidation source.                             reasoning effort set to its maximum level. The provider’s
                                                                      interface for this model does not expose sampling parameters
F. Search strategy                                                    such as temperature or top-p, so no decoding parameters
                                                                      were varied across records. The screening instruction applied
  The search combines a population concept (LLM terms)                criteria I1–I4 and E1–E6 to the title and abstract alone; the
with a task concept (oracle and testing terms) using a Boolean        per-record decisions and reason codes, together with the exact
AND. The frozen query is:                                             screening instruction, are released for audit [22], and the recall
Concept A (LLM):                                                      and false-omission validation reported below (Table III) is the
"large language model*" OR LLM OR LLMs OR GPT OR ChatGPT OR
      Codex OR Copilot                                                confusion-matrix summary of this stage.
OR Llama OR "Code Llama" OR StarCoder OR Claude OR Gemini
     OR PaLM
                                                                            b) Stage 2: independent human dual screening with val-
OR "generative AI" OR "foundation model*" OR "code language           idation: Two authors then screened a 385-record verification
      model"
                                                                      set, independently and blind both to the model’s labels and to
Concept B (oracle / test):                                            each other. The set comprised all 178 model-retained records
"test oracle*" OR "oracle generation" OR "oracle inference"
      OR "oracle problem"
                                                                      plus a fixed-seed, reason-stratified 10% random sample of 207
OR "assertion generation" OR "test assertion*" OR "                   records from the 2,067 model-excluded records. Screening all
     exception oracle"
OR "metamorphic testing" OR "metamorphic relation*" OR "
                                                                      retained records catches every false positive; the exclusion
     property-based testing"                                          sample estimates how often the model wrongly discards rel-
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                               6



evant work. Each reviewer recorded an Include, Maybe, or              unique full-text records, the duplicated pair counting once)
Exclude decision with a one-line rationale for every record.          and on 83.3% of primary-source codes (8 differences over
   Inter-rater agreement was substantial, measured by Cohen’s         the 48 records both passes judged includable; the remaining
κ [24], a chance-corrected measure of how often two re-               included studies were admitted only at adjudication, so the
viewers agree. On the operative retain-versus-exclude decision        second pass assigned them no source). The 29 studies added
(Retain = Include ∪ Maybe), κ = 0.79 (95% bootstrap [25]              by the citation-searching round were coded in two full passes
confidence interval (CI) [0.72, 0.85]; 90.4% raw agreement).          over all fields, the second revising the primary source in four of
On the finer three-level scale it was κ = 0.64 (95% CI                the 29, a concordance of 86.2% (Table II). Two of those four
[0.57, 0.71]; 81.6% agreement). The 71 disagreements were             revisions moved a study to model-parametric authority, one
reconciled conservatively. Include-versus-Maybe splits, where         from implementation-derived and one from human-elicited,
both reviewers leaned toward retention, were retained. The            which is where the categories are hardest to hold apart in
eight direct Include-versus-Exclude conflicts were decided            practice and where the boundary rules of Section III do most
individually against the full text. Exclude-versus-Maybe splits,      of their work. Every difference was adjudicated against the
where neither reviewer favored inclusion, were excluded. The          pre-registered boundary rules, the four hardest by a fresh
retain-on-uncertainty principle stated above governs the recall-      full-text re-read; six eligibility decisions and two primary-
oriented pre-filter; this human stage is where precision is           source codes were resolved in favor of the first pass, and
applied. Reconciliation yielded a consensus of 115 retained           the two contested source codings [27], [28] are treated as
records (87 include, 28 maybe) and 270 excluded over the              boundary cases in Section VIII. Both coding passes and the
verification set.                                                     per-record adjudication decisions are released [22], so the
      c) Validation of the pre-filter: Treating the human con-        differences can be inspected or re-quantified independently.
sensus as the reference, the model achieved 99.1% recall              Each study’s coding carries an anchoring quotation from its
on the verification set, agreeing with all but one consensus-         full text, so any coding can be re-traced and contested from
retained record. That single miss was itself a borderline case        the released per-study sheet. The synthesis is descriptive: it
reconciled to include only after full-text discussion. On the         reports distributions across the taxonomy and reads gaps off
stratified sample of its own exclusions, the model’s observed         the sparse or empty regions of the source-by-mechanism space.
false-omission rate was 1/207 = 0.48% (exact binomial, or             Effectiveness numbers are not pooled, because the studies
Clopper–Pearson [26], 95% CI 0.01%–2.66%). If this rate               differ too much in benchmark and metric: 64% use a custom
held across the 1,860 model-excluded records not individually         benchmark. A lightweight, non-exclusionary quality appraisal
re-screened, it would imply roughly nine missed relevant              of the included studies, scored on nine items derived from
records (the same interval scaled to the 1,860 unaudited              these coded fields, is reported in Section V-G.
exclusions gives roughly 0 to 50). Because the CI around a
single observed omission is wide, this residual risk is carried                                    TABLE II
as a threat to validity (Section VIII). The sampled exclusions            W HERE THE TWO CODING PASSES PLACED EACH STUDY ’ S PRIMARY
                                                                       SOURCE OF AUTHORITY, FOR THE CITATION - SEARCHING ARM . ROWS ARE
and their decisions are also released for audit [22]. The model        THE FIRST PASS , COLUMNS THE SECOND ; THE DIAGONAL IS AGREEMENT.
was otherwise over-inclusive, retaining 64 consensus-excluded          T HE SAME MATRIX CANNOT BE SHOWN FOR THE DATABASE ARM , WHOSE
                                                                           FIRST PASS WAS REVISED IN PLACE WHEN THE ADJUDICATION WAS
records. Its precision is supplied by the human stage. Table IV
                                                                                APPLIED . C OLUMN ABBREVIATIONS FOLLOW TABLE XI.
sets out the confusion matrix these figures summarize.
                                                                           1st ↓ / 2nd → Human Impl Model Ref-diff Regr Spec Total

H. Data extraction and coding                                              Human          5      .     1       .      .    .       6
                                                                           Impl           .      6     1       .      .    .       7
   Each included study is coded against a 35-field codebook,               Model          .      .     6       .      .    .       6
fixed before extraction and released as supplementary material.            Ref-diff       .      .     .       .      1    .       1
                                                                           Regr           .      .     .       .      1    .       1
The controlled vocabularies are likewise fixed in advance. The             Spec           .      .     .       1      .    7       8
codebook is built on the three axes of Section III: the source             Total          5      6     8       1      2    7      29
of authority (RQ2.a), the form (RQ2.b), and the adjudication
mechanism (RQ2.c). It also adds descriptive fields for the
landscape, the evaluation, and the reported failure modes
(RQ1, RQ3.a, RQ3.b). Source and mechanism are coded as                I. Selection results
two separate variables (Section III). A primary source and,              Figure 2 and Table III report the record flow and screening
where a system is compositional, a secondary source are               reliability. The searches identified 2,436 records, de-duplicated
recorded.                                                             to 2,245. The dominant pre-filter exclusion reason was out-
   All 115 retained records, including the one later found to         of-scope topical drift, records that matched the broad query
duplicate another, were coded against the locked codebook by          terms but did not concern LLM-based software test oracles.
the authors and then re-assessed in a second pass covering            In addition, a backward and forward citation-searching (snow-
the two variables the review’s conclusions rest on, eligibility       balling) round over the 54 studies included from the database
and the primary source of authority, each supported by its            search, executed in August 2026 and screened against the same
own quotation drawn from the full text. The passes concurred          eligibility criteria, contributed 29 further included studies; the
on 80.7% of eligibility decisions (22 differences over the 114        review therefore synthesizes 83 studies in total (Fig. 2).
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                 7



                                                               TABLE III
 S CREENING AND CODING RELIABILITY, AND PRE - FILTER VALIDATION . T HE FIRST BLOCK COVERS THE 385- RECORD VERIFICATION SET; THE SECOND
                            REPORTS HOW FAR THE TWO CODING PASSES CONCURRED , BEFORE ADJUDICATION .


   Measure                                                                            Value
   Reviewer agreement, binary (retain vs. exclude)                                    κ = 0.79; 95% CI [0.72, 0.85]; 90.4%
   Reviewer agreement, three-level (incl./maybe/excl.)                                κ = 0.64; 95% CI [0.57, 0.71]; 81.6%
   Pre-filter recall vs. consensus                                                    99.1% (114/115)
   Pre-filter false-omission rate (sampled exclusions)                                0.48% (1/207; 95% CI 0.01–2.66%; ≈ 9 pro-
                                                                                      jected over 1,860, CI ≈0–50)
   Pre-filter over-inclusion (consensus-excluded yet retained)                        64
   Concordance between the two coding passes, before adjudication
   Eligibility (114 unique full-text records)                                         80.7% (92/114)
   Primary source (48 records both passes judged includable)                          83.3% (40/48)
   Primary source, citation-searching arm (29 studies)                                86.2% (25/29)
   Differences resolved in favor of the first pass                                    8 (6 eligibility, 2 source)



                               TABLE IV                               and excluded.
P RE - FILTER CONFUSION MATRIX OVER THE 385- RECORD VERIFICATION
       SET: ALL 178 MODEL - RETAINED RECORDS TOGETHER WITH A
          REASON - STRATIFIED 10% SAMPLE OF 207 OF THE 2,067
                                                                                                 V. F INDINGS
 MODEL - EXCLUDED RECORDS . T HE EXCLUSION COLUMN IS A SAMPLE            Every number below is computed from the released coding
          RATHER THAN A POPULATION TOTAL , SO IT BOUNDS THE
FALSE - OMISSION RATE BUT DOES NOT GIVE A CORPUS - WIDE PRECISION .
                                                                      sheet [22] and can be reproduced; each study’s coding is listed
                                                                      in Table XI.
                                Human consensus
          Pre-filter decision   Retain   Exclude    Total             A. The landscape: who, what, and when (RQ1)
          Retain                 114        64       178                 The reviewed work is recent and concentrated, most of it
          Exclude                 1        206       207              targeting ordinary software at the unit level: general-purpose
          Total                  115       270       385              software accounts for 54 of the 83 studies. The rest form
                                                                      smaller clusters: embedded or programmable logic controller
                                                                      (PLC) control with six, web and mobile with five each,
                                                                      security with three, two studies each in representational state
J. Full-text eligibility outcome
                                                                      transfer (REST) or API services, graphical user interfaces
    The 115 retained records were assessed at full text against       (GUIs), machine or deep learning (ML/DL) systems, and
the locked criteria of Section IV, recording for each eligibility     autonomous driving systems (ADSs), and the remaining two
decision a supporting evidence quote together with the code-          domains contributing one study each (Fig. 5). The source
book fields of Section IV-H. One record was found to duplicate        of authority varies with the domain. Implementation-derived
another, leaving 114 unique full-text records, of which 54 were       oracles are almost all general-purpose unit-level software,
included [2]–[7], [10], [15]–[20], [27]–[67] and 60 excluded.         16 of 17. Model-parametric oracles split between the neural
The citation-searching round contributed 29 further included          assertion-generation line on general-purpose software (8 of
studies [68]–[96], so the syntheses that follow cover 83 studies.     17) and interactive or visual domains such as mobile apps,
    The dominant exclusion reason, by a wide margin, is E2            GUIs, and ADSs (7 of 17) [18], [54], with the remaining two
(55 of 60). On full reading, these studies use the LLM to             in ML/DL and embedded code. In the interactive domains
generate test inputs, to produce specifications that a static         a plausible reason is that no executable specification is on
solver then proves, to drive exploration whose only failure           offer, leaving the model’s own expectations as often the only
signal is a crash or a log, or to generate test documents for         authority within reach. One study is from 2022, five are from
human execution. In each, the verdict is reached by a non-            2023, ten from 2024, 43 from 2025, and 24 from 2026. As a
LLM mechanism, a differential comparator, a static verifier, or       result, 81% appeared in 2025 or later (Fig. 3). All included
a human reviewer, rather than by an oracle the LLM supplies           work is peer reviewed, spread across 40 venues but led by the
or determines. This criterion cannot be applied reliably from         main software-engineering ones (Table V). Conferences carry
title and abstract, which accounts for the gap between the 115        most of it (51 of 83), with journals a strong second (29) and
apparently oracle-relevant records and the 54 in which an LLM         workshops the remaining three.
supplies or determines the oracle. The remaining exclusions              The studies lean on closed-weight models and on prompting
are three items that are too short or non-research (E6) and two       rather than training. Setting aside the 39 studies that compare
that fail another inclusion criterion. One boundary recurred          several models, the GPT family is the most common single
often enough to state explicitly: an LLM-generated invariant,         choice: 20 studies use a GPT model as their primary, a GPT-
contract, or assertion that is executed against a running system      4-class model in 16 and GPT-3.5 in 4. Most use the model as
is treated as an oracle and included. The same artifact used          it comes, with fine-tuning in 22 (Fig. 6). Closed models (35)
only inside a static proof, by contrast, is treated as verification   outnumber open-weight ones (23), with 25 studies using both
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                                                                         8




                         IDENTIFICATION                                  Identification of studies via databases                                              Via citation searching


                                                     Records identified (databases): 2,436                                                            Citation searching (snowballing)
                                                     Scopus 391 ⋅ IEEE 234 ⋅ ACM DL 1,811                                                             backward + forward over the 54 studies




                                                                                                      Duplicates removed: 191
                                                     After duplicates removed: 2,245




                                                     Automated pre-filter (Claude Opus 4.8)           Excluded (pre-filter): 2,067
                                                                                                      out of scope 1,877; other 190
                                                     2,245 title/abstract, retained 178
                         SCREENING




                                                     Human dual screen: verification n = 385          Excluded at screening: 2,130                    Screened and assessed
                                                                                                      human-verified 270; auto-only 1,860
                                                     178 retained + 207 (10% stratified)                                                              against the same pre-registered criteria

                                                                                                      Pre-filter validation
                                                                                                      κ = 0.79 [0.72, 0.85]
                                                     Retained for full text: 115                      FOR = 0.48%

                                                     consensus: 87 include, 28 maybe
                         ELIGIBILITY




                                                     Full-text assessed: 114 unique                   Excluded at full text: 60                       Additional studies included: 29
                                                                                                      no LLM oracle 55; other 5
                                                     1 duplicate found at full text                                                                   same eligibility criteria applied
                         INCLUDED




                                                                                            INCLUDED STUDIES: 83
                                                                                            54 database search + 29 citation searching




Fig. 2. PRISMA 2020 flow of records: the database-search arm (left, full detail) and the citation-searching arm (right, summarized), converging on the 83
included studies. Per-stage exclusion reasons are in the supplementary material.


                    50                    Source of authority                                                                  B. Where the authority comes from (RQ2.a)
                                            Specification
                                            Implementation                                     N=43

                    40
                                            Model-parametric                                                                      The single largest group of reviewed oracles draws its
                                            Human-elicited
                                            Reference-diff.                                                                    authority from a written description of intended behavior
Number of studies




                                            Regression-prior
                                                                                                      2026: partial year
                                                                                                                               (Fig. 7). Specification-derived oracles account for 35 of the
                    30
                                                                                                                               83. Within them, natural-language artifacts, such as docstrings,
                                                                                                           N=24
                                                                                                                               code comments, requirements, and API documentation, ac-
                    20                                                                                                         count for 23, ahead of semi-formal (7) and formal (5).
                                                                                                                               Implementation-derived oracles, which read expected behavior
                                                                                  N=10
                    10                                                                                                         from the code or existing tests, and model-parametric oracles,
                                                                 N=5                                                           which rely on the model’s own knowledge with no external
                                              N=1
                     0
                                                                                                                               reference, tie as the next largest groups (17 each). Human-
                                              2022              2023              2024         2025        2026*               elicited oracles follow (7). Reference-differential oracles (5)
                                                                            Publication year
                                                                                                                               include a recent variant in which the consensus output of
Fig. 3. Included studies by publication year, stacked by source of authority
                                                                                                                               several model-generated alternative implementations, rather
(2026 partial, hatched).                                                                                                       than an independent reference version, supplies the expected
                                                                                                                               value [19], [20]. One of the seven categories, implicit-intrinsic,
                                                                                                                               remains unoccupied as a primary source, appearing only as a
                                                                                                                               secondary signal in compositional systems. Regression-from-
                                                                                                                               prior-version, unoccupied in the database-search corpus, is
(Fig. 4(a)). Open-science practice is common: 65 of 83 release                                                                 now held by two studies in which a prior version’s behavior
code or data (Fig. 4(b)), and most studies evaluate or validate                                                                anchors an LLM-generated or LLM-judged test [82], [93]
existing ideas rather than propose new ones (Fig. 4(c)). The                                                                   (Section VI-C).
languages tested are mostly Java (35) and Python (18).                                                                            Recording one primary source per study is a coding decision
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                                                            9



           (a) model access                                            (b) data availability                                                        (c) research type

                                                                                                                                 Evaluation                                    38
Closed                                35                     Public                                  65


                                                                                                                                     Validation                           31

  Open                       23                       On-request        1

                                                                                                                                      Proposal             9


   Both                       25                              None            17
                                                                                                                                Experience            5


          0             20              40                            0       20     40       60                                                  0            20              40

                                                                      Number of studies

Fig. 4. Study characteristics: (a) model access, (b) data or code availability, (c) research type.



                           TABLE V                                                              General-SW                                                          54
 L EADING PUBLICATION VENUES ( THOSE WITH AT LEAST TWO STUDIES ;                            Embedded/PLC                    6
                      40 VENUES IN TOTAL ).                                                               Web               5
                                                                                                      Mobile                5

    Venue                                                         Studies                            Security           3
                                                                                             ML/DL-system           2
    Proc. ACM Software Engineering (FSE / ISSTA)                          9                        API/REST         2
    Int. Conf. Software Engineering (ICSE, incl.                          7                               GUI       2
    SEIP)                                                                                  ADS/autonomous           2
    ACM Trans. Software Engineering and Method-                           6               Scientific/numeric        1
    ology (TOSEM)                                                                                      Other        1
    IEEE Transactions on Software Engineering                             6
                                                                                                                0               10       20    30         40   50        60
    (TSE)                                                                                                                                Number of studies
    Int. Conf. Automated Software Engineering                             5
    (ASE)                                                                          Fig. 5. Application domains of the systems under test. Abbreviated labels:
    Int. Conf. Foundations of Software Engineering                        3        General-SW, general-purpose software; ML/DL, machine or deep learning;
    (FSE, incl. ESEC)                                                              PLC, programmable logic controller; API, application programming interface;
    IEEE Conf. Software Testing, Verification and                         3        REST, representational state transfer; GUI, graphical user interface; ADS,
    Validation (ICST)                                                              autonomous driving system.
    Annual Meeting of the Assoc. for Computational                        3
    Linguistics (ACL)
    Information and Software Technology                                   3        signal in compositional designs; and implicit-intrinsic, which
    Lecture Notes in Computer Science (various)                           3        no study uses as its primary source, appears as a secondary
    Int. Conf. AI-powered Software (AIware)                               2
                                                                                   signal in four. The conclusions that follow rest on the primary
    Int. Conf. Automation of Software Test (AST)                          2
    Asia-Pacific   Software     Engineering    Conf.                      2        coding and on the source-by-mechanism structure, and neither
    (APSEC)                                                                        is disturbed by this second reading; what it does show is that
    Int. Symp. Software Testing and Analysis (ISSTA                       2        the one empty category is a consequence of counting primary
    proceedings)                                                                   sources only, not a claim that the signal is absent from the
    IEEE Int. Conf. Software Testing Workshops                            2
                                                                                   corpus. Every secondary source is listed study by study in
    (ICSTW)
                                                                                   Table XI.
    25 further venues with one study each.

                                                                                   C. Specification dependence: an audit of the source coding
                                                                                   (RQ2.a)
rather than a property of the systems, so it is worth reading                         Specification dependence is not posed as a separate research
the corpus a second way, with each study’s secondary source                        question, because the source categories are defined by their
counted alongside its primary one. Sixty-one of the 83 studies                     relation to a specification; it is reported here as an audit of
record a secondary source, giving 144 source labels in all. The                    the RQ2.a coding. Because the sources are defined by their
picture is stable where it matters most: specification-derived                     relation to a specification, the corpus follows the idealized
remains the largest group by a wide margin (42 labels), and                        split in direction, though with a wider partial fringe than
reference-differential and regression-from-prior-version stay                      the database-search corpus alone (Fig. 8). This is a consis-
near the bottom (8 and 7). Two things move. Implementation-                        tency check rather than an empirical discovery. Specification
derived authority passes model-parametric (31 against 27), be-                     dependence is coded as its own field, separately from the
cause code and existing tests are the most common supporting                       source code, so the near-perfect alignment between the two
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                                                                    10



                             (a) models used                                                                        (b) adaptation (multi-valued)

             Multiple                                                       39                      Zero-shot                                                                     44
            GPT-4/4o                                   16
                                                                                                     Few-shot                                                        33
                Other                         9
                                                                                            CoT/reasoning                                                            33
CodeT5/CodeBERT                          7
              GPT-3.5                4                                                                        RAG                       14
           DeepSeek              2
                                                                                                 Fine-tuning                                       22
 Llama/CodeLlama                 2
                                                                                      Agent/multi-agent                             13
              Gemini             2
               Claude            2                                                              Pre-training            3


                             0            10             20       30       40                                       0         10              20            30               40        50

                                                                                  Number of studies

Fig. 6. LLM use: (a) primary model family per study, (b) adaptation strategies (multi-valued). CoT, chain-of-thought; RAG, retrieval-augmented generation.



        Specification                                                  35 (42%)
                                                                                    synthesized reference versions as its expected output, and
                                                                                    its coding records a secondary specification-derived source:
      Implementation                                  17 (20%)
                                                                                    part of the verdict’s authority flows from the specification
    Model-parametric                                  17 (20%)                      that guided the synthesis. Both show the same pattern: the
      Human-elicited                 7 (8%)                                         boundary blurs exactly where the LLM manufactures the
       Reference-diff.           5 (6%)
                                                                                    artifact that other designs take as given. The citation-searching
                                                                                    extension adds six further partial crossings of the same
     Regression-prior        2 (2%)
                                                                                    character, among them the corpus’s second partly-dependent
                         0               10            20        30       40        reference-differential oracle: in each, part of the verdict’s
                                                  Number of studies                 authority flows through a specification-shaped artifact that
                                                                                    the model reads, synthesizes, or internalizes, from docstring
Fig. 7. Primary source of oracle authority (83 studies).
                                                                                    signals inside neural assertion generators to the issue text
                                                                                    behind a regression-catching test.

confirms that the categories behave as defined; this alignment                                                            independent          partly           dependent
is what is expected by construction and is reported as an audit
                                                                                         Specification   26                                                          1
of the taxonomy, not as a finding about the literature; the
substantive result is the source distribution reported above,                         Implementation                                                                                   17


and the specification-independent share simply follows from                          Model-parametric                                                                             14

it. Every implementation-derived oracle (17 of 17) renders its                         Human-elicited                                                                    6
verdict without any external specification, as do 14 of the 17
                                                                                       Reference-diff.                                                           3
model-parametric, six of the seven human-elicited, three of the
five reference-differential, and one of the two regression-from-                      Regression-prior                                                      1


prior-version oracles; the remainder are partly dependent, and                                           −30            −20             −10             0                    10             20

no non-specification source is fully specification-dependent.                                                   Number of studies (dependent ← 0 → independent)

Specification-derived oracles, by contrast, are specification-
                                                                                    Fig. 8. Specification (in)dependence of the verdict, by primary source of
dependent or partly so in 34 of 35 cases. The 42 fully                              authority.
specification-independent studies make up just over half of the
corpus. All but one draw their verdict authority from the code,
the model’s own knowledge, an independent reference, a prior
version, or a human; the exception is the specification-derived                     D. How oracles are expressed and adjudicated (RQ2.b,
oracle that infers its own specification, discussed next.                           RQ2.c)
    The two crossings carry the real information. The                                  Table VI reports oracle form and adjudication mechanism,
one specification-derived oracle that needs no pre-existing                         both multi-valued, so column totals exceed 83. Assertions
specification [51] has the LLM infer executable metamorphic                         dominate the form (56) and runtime assertion execution the
relations; the inferred relation then serves as the specification,                  mechanism (56). The key pattern is the division of labor: in
so the spec is synthesized rather than supplied. In the database-                   65 of 83 studies the LLM generates an oracle artifact that some
search corpus, the one reference-differential oracle that partly                    other mechanism then checks, in 16 it is itself the judge, and
depends on a specification [20] takes the consensus of LLM-                         in two it validates an oracle produced by other means.
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                             11



                            TABLE VI                                  (19). Resemblance to a known oracle is thus the dominant
O RACLE FORM , ADJUDICATION MECHANISM , AND LLM ROLE ( FORM AND       quality signal, rather than mutation-grounded fault detection.
       MECHANISM MULTI - VALUED ; TOTALS EXCEED 83). PBT,
                    PROPERTY- BASED TESTING .

                                                                      F. How the oracles fail (RQ3.b)
           Oracle form (RQ2.b)
           Assertion                                       56            Reported failure modes converge on a small set (Fig. 10).
           Expected-output value                           19         Hallucination is the model asserting behavior the system
           Classifier / judge label                        15         does not exhibit. It is the hazard studies engage with most,
           Metamorphic relation                            12
           Invariant                                       11         surfacing in 60 of 83 studies. A closer reading separates three
           Property / PBT                                   9         overlapping ways studies engage with it (Table VIII): 58 name
           Other (exception oracle)                         2         it as a risk, 44 report observing it empirically in their own
           Adjudication mechanism (RQ2.c)                             results, and 46 apply a concrete mitigation. Among the other
           Runtime assertion execution                     56         modes, the leaders are weak or missing assertions (38), where
           Exact / structural match                        26         the generated oracle is too loose to detect the faults it should,
           LLM-as-judge                                    22
           Human review                                    11
                                                                      and prompt sensitivity (29); then cost or latency (26), flakiness
           Statistical / distributional                     8         or nondeterminism (20), and data contamination (20). Over-
           Formal verification                              6         assertion, an oracle so strict that it rejects correct behavior,
           Semantic / similarity                            4
                                                                      appears in only 11 studies, against 38 for weak or missing
           LLM role (RQ2.c)                                           assertions, making weak oracles the most frequently reported
           Generates oracle artifact (checked otherwise)   65         correctness risk. But how often a failure is reported may not
           Is the oracle / judge                           16         match how often it happens. The 46 mitigations are led by
           Validates an oracle produced by other means      2
                                                                      execution-based filtering, compiling and running a candidate
                                                                      oracle and discarding what fails to compile or rejects known-
                                                                      correct behavior [16], [58]; self-consistency or multi-sample
   The two axes do not line up one to one (Fig. 9).
                                                                      voting [19], [20]; and human review (11 studies, Table VI).
Specification-derived authority is decided by all seven mecha-
nisms; conversely each mechanism draws on between three
and six different sources. Runtime assertion execution, the           G. Study quality appraisal
most common mechanism (56 co-occurrences), serves ev-
                                                                         To characterize the rigor of the corpus without excluding
ery occupied source. LLM-as-judge (22) serves specification-
                                                                      any study, each of the 83 included studies was scored on a
derived, model-parametric, human-elicited, and regression-
                                                                      lightweight nine-item checklist derived from the coded fields
from-prior-version authority, and appears once as a validation
                                                                      (Table IX). The corpus is uniformly strong on the items the
step over an implementation-derived oracle [75]. The LLM’s
                                                                      taxonomy relies on: every study defines its oracle, identifies
role adds a second pattern. In all 16 studies where the
                                                                      an authority source, and discusses its own limitations. Almost
LLM is itself the judge, its authority is a specification, its
                                                                      all also report a benchmark (75 of 83) and a ground-truth
own parametric knowledge, human-elicited criteria, or a prior
                                                                      source (80). It is weakest exactly where the evaluation findings
version, and in none is it implementation-derived or reference-
                                                                      (RQ3.a) already pointed: fault detection is evaluated in 35
differential. With only 16 such studies this is a pattern in the
                                                                      studies and mutation analysis used, as a metric or as an
corpus rather than an established constraint. For those two
                                                                      oracle check, in only 20. We report the nine items individually
sources the LLM writes an artifact that some other mechanism
                                                                      rather than as a summed score: they mix reporting, artifact-
runs. Cataloging oracles by mechanism or form alone, as prior
                                                                      availability, and fault-detection constructs that do not form
secondary studies do, discards this structure.
                                                                      a single validated quality index. Read item by item, they
                                                                      describe a literature that is mature in reporting but light on
E. How well the oracles work (RQ3.a)                                  fault-grounded evaluation, so findings that lean chiefly on the
   Most studies compare against a baseline (65 of 83), but            fault-grounded items (RQ3.a) rest on the weaker part of the
the evaluation ground is fragmented and the oracle’s own              corpus.
correctness is unevenly checked. 64% rely on a custom bench-
mark (53 of 83). The most common shared benchmarks are                                       VI. D ISCUSSION
Defects4J (16) and HumanEval (7), which limits cross-study
comparison. Ground truth is most often human-provided (37)            A. What the findings mean
or taken from existing tests (20), with reference implemen-              Three results stand out, together showing a field that has
tations (15) and specifications (8) behind. Oracle quality is         changed what an oracle rests on.
assessed against ground-truth oracles in 52 studies and by               First, the authority behind LLM-based oracles often does
manual inspection in 19; only 13 use mutation analysis to test        not come from a specification at all. That makes them useful
whether the oracle actually catches injected faults, and 3 do         on everyday software, which rarely has a written specification.
not assess it at all. The dominant reported metrics are accuracy      It also makes them risky: an oracle resting only on the model’s
against a reference (39) and fault detection (35), followed by        own knowledge, with no external anchor at all, can be wrong
precision and recall (31), coverage (19), and mutation score          with no signal that it is.
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                                  12




    Regression-prior (4)                                                                                              Formal verification (6)

                                                                                                                      Semantic (4)
     Reference-diff. (11)
                                                                                                                      Statistical (8)

    Human-elicited (13)
                                                                                                                      Human review (11)




Model-parametric (26)                                                                                                 LLM-as-judge (22)




   Implementation (27)                                                                                                Exact match (26)




       Specification (52)                                                                                             Runtime execution (56)




Fig. 9. Source of authority (left) to the mechanism that adjudicates it (right). Parenthetical numbers are node totals. Each ribbon’s number is that source’s
contribution. All are study co-occurrences (one per mechanism a study uses), so the source totals exceed the primary-source counts of Fig. 7. Unlabeled
ribbons are single studies. Each study contributes its single primary source paired with each mechanism it uses, so no source combinations are introduced; a
numerical version is given in Table VII.

                                                               TABLE VII
  N UMERICAL SOURCE - BY- MECHANISM CO - OCCURRENCE MATRIX BEHIND F IG . 9: ONE COUNT PER ( SOURCE , MECHANISM ) PAIR A STUDY REALIZES ,
OVER THE SEVEN PRINCIPAL MECHANISMS . ROW AND COLUMN TOTALS ARE THE NODE TOTALS OF THE FIGURE (133 CO - OCCURRENCES ACROSS THE 83
 STUDIES ). T HREE STUDIES ADDITIONALLY RECORD AN other MECHANISM ( MUTATION TESTING , A DIFFERENTIAL CROSS - CHECK , AND A RULE - BASED
 MATCHER ), LISTED IN THE APPENDIX BUT OUTSIDE THESE SEVEN . S OURCES ARE SINGLE - VALUED PER STUDY, SO NO SOURCE COMBINATIONS ARISE .


     Source                           Runtime exec     Exact match     LLM-judge      Human review      Statistical   Semantic    Formal verif    Total
     Specification-derived                  25               6              8                7               1            1             4           52
     Implementation-derived                 14               8              1                0               2            1             1           27
     Model-parametric                        6               5              9                2               3            1             0           26
     Human-elicited                          5               3              3                1               1            0             0           13
     Reference-differential                  4               4              0                0               1            1             1           11
     Regression-from-prior-version           2               0              1                1               0            0             0            4
     Total                                  56              26              22              11               8            4             6          133



   Second, the source of authority and the way pass or fail                      strength: the most common reported correctness failure is an
is computed are separate choices (Fig. 9). A label such as                       oracle too weak to catch the bug it should. This compounds
“LLM-as-judge” therefore says nothing about how far to trust                     the hazard studies engage with most, the model’s tendency to
the verdict.                                                                     hallucinate behavior the system never shows.
   Third, the most frequently reported risks concern oracle
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                                   13



                                                                                     N=83
               Hallucination                                         60
                                                                                            the limits of those tests, however, and cannot catch a bug
      Weak/missing assertion                          38
                                                                                            already in the current code.
           Prompt sensitivity                    29                                            In every case the source should be stated plainly.
                Cost/latency                    26                                             How the model obtains that authority does not change which
                   Flakiness               20                                               source it is. A study that uses retrieval-augmented generation
         Data contamination                20                                               (RAG) or an agentic tool call to fetch a specification is still
              Over-assertion         11                                                     specification-derived; one that fetches or executes existing
                                0   10    20    30    40   50   60        70    80
                                                                                            code is still implementation-derived. Twenty-four of the 83
                                                 Number of studies                          studies use RAG or agentic (multi-agent) adaptation (14 and
                                                                                            13 respectively, with 3 studies using both). They span six
Fig. 10. Reported failure modes (multi-valued; dashed line marks the 83                     sources (12 specification-derived, 5 implementation-derived, 3
studies). One-off study-specific modes are omitted.
                                                                                            model-parametric, 2 human-elicited, 1 reference-differential,
                                                                                            1 regression-from-prior-version), indicating that adaptation
                         TABLE VIII
  H OW STUDIES ENGAGE WITH HALLUCINATION , THE MOST COMMON                                  strategy and source of authority are separate, cross-cutting
             FAILURE MODE ( CATEGORIES OVERLAP ).                                           choices.

          Engagement with hallucination                                    Studies
          Named as a risk or threat                                              58         C. Gaps and a research agenda (RQ3.c)
          Empirically observed in own results                                    44
          Mitigation applied                                                     46            Reading the sparse and empty regions of the source-by-
          60 of 83 studies engage in at least one of these ways.                            mechanism space (Fig. 9) and the source totals (Fig. 7) yields
                                                                                            a concrete agenda. The gaps below are an interpretive reading
                             TABLE IX                                                       of where LLM-based oracles have not yet been applied, not
   L IGHTWEIGHT QUALITY APPRAISAL OF THE 83 INCLUDED STUDIES                                an observed empirical result; several are shaped by our review
           ( NON - EXCLUSIONARY; EACH ITEM SCORED 0/1).                                     scope (Section VIII) rather than by the state of practice.
    Quality item                                                                 Studies    Near-empty source categories. One of the seven sources
                                                                                            remains unoccupied, and one nearly so. No included study
    Oracle explicitly defined                                                  83 (100%)
    Authority source identifiable                                              83 (100%)    rests on a purely implicit-intrinsic oracle (crashes or well-
    Threats / limitations discussed                                            83 (100%)    formedness) as the LLM’s contribution: that failure signal
    Ground truth available                                                      80 (96%)    is supplied without an LLM, so such designs fall to E2,
    Dataset / benchmark described                                               75 (90%)
    Code or data released                                                       65 (78%)    and the category surfaces only as a secondary, compositional
    Baseline comparison reported                                                65 (78%)    signal (in four studies). This cell is therefore empty partly
    Fault detection evaluated                                                   35 (42%)    by construction of our scope. Regression-from-prior-version
    Mutation analysis used (metric or oracle check)                             20 (24%)
                                                                                            authority, unoccupied in the database-search corpus, is now
    Items reported individually; not summed into a composite score.
                                                                                            held by two studies in which a prior version’s behavior anchors
                                                                                            an LLM-generated or LLM-judged catching test [82], [93];
                                                                                            with two studies it is the sparsest occupied source. Whether
B. Choosing a source of authority in practice                                               an LLM can add value in the implicit-intrinsic cell, where it
   The taxonomy also reads as a practical guide: the right                                  is currently bypassed, this corpus cannot settle.
source depends on what the project already has.
                                                                                            Empty source-by-mechanism cells. LLM-as-judge is never
   If the code has documentation, such as docstrings or require-
                                                                                            applied to reference-differential authority, and touches
ments, specification-derived oracles are the best-supported
                                                                                            implementation-derived authority only once, as a validation
path. The reviewed work most often turns natural-language
                                                                                            step over an inferred contract [75]: when the authority is the
documentation into assertions that run against the program [2],
                                                                                            code or an independent reference, the included studies other-
[4], [16].
                                                                                            wise execute or match rather than asking the model to judge.
   If there is no specification but a trusted second implementa-
                                                                                            Whether an LLM judge briefed with the implementation or
tion exists, a reference-differential oracle is natural: run both
                                                                                            the reference could outperform exact matching, particularly for
and compare. A newer variant has the LLM write several
                                                                                            outputs that are semantically equivalent but textually different,
implementations and treats their agreement as the expected
                                                                                            is almost untested. Human-elicited authority, sparse in the
answer, removing the need for an existing reference [19], [20].
                                                                                            database-search corpus, now covers seven studies spanning
   If the program is interactive or visual, such as a mobile app
                                                                                            five mechanisms.
or a GUI, the field uses model-parametric oracles. The LLM
judges the output directly from its own knowledge, because                                  Evaluation gaps. The reliance on custom benchmarks (64%)
no executable specification is available [5], [6]. This is the                              and the thin use of mutation analysis to validate oracle fault
least anchored option, so it pairs best with human review or                                detection (13 of 83) together mean the field lacks a shared,
independent cross-checks.                                                                   fault-grounded yardstick for oracle quality. A standard oracle-
   If existing tests already encode expected behavior,                                      evaluation benchmark scored by mutation killing, rather than
implementation-derived oracles can extend them. They inherit                                by textual similarity to a reference oracle, would be valuable.
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                        14



Trust gaps. Hallucination is the hazard studies engage with                   they would leave every source ranking unchanged. The finding
most (60 of 83), but it is named far more often than measured:                most sensitive to them is the narrow majority that reaches a
58 studies flag it as a risk while 44 report observing it. The                verdict without a specification (42 of 83): a worst case in
46 mitigations, in turn, are varied and rarely evaluated for                  which all four additions were specification-derived would turn
residual risk. The weak-assertion failure mode (38) shows                     that majority into a narrow minority, though the substantive
that generated oracles frequently under-constrain behavior                    point, that a large share of these oracles need no specification
in a way that similarity metrics do not detect. Measuring                     at all, holds either way.
oracle strength, beyond oracle-generation accuracy, is the open
problem these findings point to.                                              B. Scope validity
                     VII. R ELATED R EVIEWS                                      The search covered Scopus, IEEE Xplore, and the ACM
                                                                              Digital Library; Web of Science, Springer Link, and dedicated
    Fourteen secondary studies overlap this review’s scope [8],               preprint servers were not queried, and preprint-only work
[9], [97]–[108]. The full per-study analysis is given in Table X.             is therefore under-represented (criterion E5). The citation-
None organizes the oracle literature by the source of verdict                 searching round partially mitigates this boundary, reaching
authority. Where they address the oracle at all, thirteen treat               work indexed outside the three databases through the citation
it by output form or by LLM technique, and one partitions                     graph of the included studies.
it by mechanism [101]. The only oracle-dedicated secondary
                                                                                 LLM-based assertion generation for hardware (criterion E3)
study is a non-systematic roadmap [98]. None reports an
                                                                              is a sizable adjacent literature that we deliberately place out
inter-reviewer agreement coefficient, even among the broad
                                                                              of scope. It is a natural target for a companion review.
reviews of LLMs for software engineering [8], [9]. Nor do
they separate the three questions this review keeps apart: what
shape the oracle takes, how pass or fail is computed, and                     C. Classification validity
where its authority comes from. Among the surveys we iden-                       The source-of-authority code is the review’s central inter-
tified, none is simultaneously oracle-focused, systematically                 pretive judgment and is, like any qualitative coding, subject
searched, organized by source of authority, and reliability-                  to reasonable disagreement at category boundaries. To make it
reported; that is the position this review occupies.                          auditable, every included and excluded record is released [22]
                                                                              with its eligibility decision, the criterion applied, the primary
                            TABLE X                                           and secondary source codes, and an anchoring quotation. The
T HIS REVIEW AGAINST THE 14 RELATED SECONDARY STUDIES ( COUNTS
                         OVER THE 14).
                                                                              load-bearing boundary rules, notably runtime execution versus
                                                                              static proof, the LLM as oracle versus as test-input genera-
 Property                                         Prior reviews     This      tor, and a supplied specification versus a bare task prompt
                                                     (of 14)       review     (Section III), are stated explicitly so that any classification
 Oracle is the primary unit of analysis                 1†          yes       can be re-traced and contested. The source-of-authority coding
 Systematic search with a reported funnel               7           yes       (Section IV-H) is interpretive, so a misclassification could pass
 Organized by source of verdict authority               0           yes       undetected; the anchoring quotations in the released sheet are
 Inter-reviewer agreement (κ) reported                  0           yes
                                                                              the audit trail for exactly this risk. As a sensitivity check, reas-
 † The one oracle-focused secondary study is a non-systematic roadmap (no
                                                                              signing the two contested primary-source codings [27], [28] to
search funnel). One further review partitions oracles by mechanism, counted
                   as not organized by source of authority.                   their alternative readings changes no aggregate count by more
                                                                              than one study and no conclusion of the review.

                  VIII. T HREATS TO VALIDITY                                                         IX. C ONCLUSION
A. Search and screening validity                                                 Test oracles decide whether software behaves correctly, and
   The recall-tuned query admitted many off-topic records.                    LLMs have made it possible to generate them or to use a
These were removed by criterion-based screening (Table III).                  model as one. This review organized that new body of work
   The pre-filter’s exclusions carry the only residual risk:                  by a question the literature usually skips: where does the
the model-excluded records not individually re-screened. The                  verdict’s authority come from? Across 83 studies, the single
audited sample puts the false-omission rate at 0.48% (1/207,                  most common authority is a written description, but just over
Clopper–Pearson exact 95% CI 0.01–2.66%), projecting to                       half need no specification at all. The source categories track
roughly nine (95% CI ≈0–50) missed records across the 1,860                   this split by construction, and the corpus confirms it, crossed
unaudited exclusions. Because the CI around a single observed                 only by a small partial fringe where the model itself supplies
omission is wide, this residual risk is disclosed here, with the              or reads the specification-shaped artifact other designs are
sampled decisions released for audit. It is unlikely to change                handed. The source of authority cross-cuts how pass or fail
the main taxonomy-level findings, and its consequence can be                  is computed, so describing an oracle only by its mechanism
bounded. A missed record would still have had to clear full-                  leaves out what matters most. The most frequently reported
text eligibility, which 54 of the 114 unique full-text records                weaknesses are oracles too weak to catch bugs, and verdicts
did, so the nine projected omissions correspond to roughly four               the model can hallucinate. Its evaluation usually checks re-
further included studies. Distributed like the rest of the corpus,            semblance to a known oracle, and rarely whether the oracle
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738   15



catches faults. The source-of-authority taxonomy reads this
literature on the grounds that set how far a verdict can be
trusted. For practitioners, the first question about any LLM
oracle should be where its authority comes from, since that,
more than the mechanism, is what a pass or fail can ultimately
be defended on. These findings carry the residual uncertainties
disclosed in Section VIII: a small number of records the
automated pre-filter may have missed, databases and preprint
venues not searched, and the interpretive nature of qualitative
classification.

                          A PPENDIX A
                P ER -S TUDY C ATEGORIZATION
   Table XI lists every included study with its primary
and, where compositional, secondary source of authority, its
specification-dependence label, all coded oracle forms and ad-
judication mechanisms, and application domain, so the multi-
valued totals of Tables VI and VII can be reconstructed row
by row. It lets any aggregate count in the synthesis be traced
back to the studies behind it. The complete coding sheet, with
its coded fields and the anchoring quotations, is provided as
supplementary material.
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                              16


                                TABLE XI: The 83 included studies and their complete coding: primary source, secondary
                                source where a system is compositional, specification dependence (Sp), and all applicable
                                oracle forms and adjudication mechanisms, so every multi-valued aggregate in the
                                synthesis (Tables VI and VII) can be reconstructed from this table. Column abbreviations
                                are defined in the note beneath the table.

         ID          Yr     Source      2nd src       Sp Form(s)                    Mechanism(s)                                 Domain
         0001 [29]   2025   Spec        –             D   Assert; Exp-out           Exact                                        web
         0009 [30]   2025   Spec        Human         D   Assert; Property          Human-rev; RT-exec                           general-SW
         0014 [31]   2025   Spec        Human         D   Metam                     LLM-judge; Human-rev                         scientific/numeric
         0017 [32]   2025   Human       Ref-diff      I   Judge                     LLM-judge                                    general-SW
         0018 [33]   2026   Ref-diff    Model         I   Exp-out; Metam            Exact; Statist                               ML/DL-system
         0041 [18]   2024   Model       Human         I   Judge                     LLM-judge                                    mobile
         0043 [34]   2025   Impl        Human         I   Assert; Exp-out           Exact; Statist                               general-SW
         0048 [35]   2026   Impl        –             I   Invar                     RT-exec                                      general-SW
         0072 [36]   2026   Model       Regression    I   Assert                    Exact; Statist                               ML/DL-system
         0083 [37]   2026   Spec        Impl          P   Exp-out                   Exact                                        embedded/PLC
         0087 [38]   2025   Spec        Impl          D   Invar                     LLM-judge                                    API/REST
         0091 [39]   2024   Spec        Model         P   Assert; Exp-out           LLM-judge; RT-exec                           general-SW
         0098 [3]    2025   Impl        Regression    I   Assert                    Exact; RT-exec                               general-SW
         0103 [40]   2025   Human       Ref-diff      I   Judge                     LLM-judge; Statist                           general-SW
         0129 [41]   2025   Impl        Model         I   Assert                    Exact                                        general-SW
         0132 [42]   2025   Impl        –             I   Assert                    RT-exec                                      general-SW
         0137 [43]   2025   Spec        –             D   Assert; Property          RT-exec                                      API/REST
         0161 [44]   2024   Impl        Human         I   Assert                    Exact; RT-exec; Semantic                     general-SW
         0177 [45]   2026   Spec        Impl          D   Assert; Property          RT-exec                                      embedded/PLC
         0183 [46]   2024   Spec        –             D   Assert                    RT-exec                                      general-SW
         0184 [27]   2025   Model       Impl          I   Assert                    Human-rev; RT-exec                           general-SW
         0211 [47]   2024   Spec        –             D   Metam                     RT-exec                                      web
         0213 [48]   2025   Spec        Impl          D   Assert; Metam             LLM-judge; Statist                           general-SW
         0223 [49]   2025   Spec        Human         D   Assert                    Exact; RT-exec                               general-SW
         0231 [50]   2025   Model       Implicit      I   Metam                     Exact                                        embedded/PLC
         0248 [10]   2025   Spec        Model         P   Metam                     Human-rev; RT-exec                           general-SW
         0259 [2]    2025   Spec        Model         P   Assert; Other             Exact; RT-exec                               general-SW
         0261 [51]   2026   Spec        Impl          I   Metam                     RT-exec                                      general-SW
         0279 [52]   2025   Spec        Model         D   Assert; Property          RT-exec                                      general-SW
         0287 [17]   2025   Model       Human         I   Judge                     LLM-judge                                    GUI
         0304 [53]   2025   Spec        –             D   Assert; Exp-out           RT-exec                                      general-SW
         0316 [54]   2023   Model       Human         I   Metam                     Human-rev                                    ADS/autonomous
         0320 [55]   2025   Spec        Impl          D   Assert                    RT-exec                                      mobile
         0323 [56]   2025   Spec        Implicit      P   Metam                     Human-rev; RT-exec                           ADS/autonomous
         0339 [15]   2025   Spec        –             D   Assert; Exp-out           RT-exec                                      general-SW
         0371 [57]   2025   Impl        Regression    I   Assert                    Exact; RT-exec                               general-SW
         0372 [5]    2025   Model       Human         I   Judge                     LLM-judge                                    mobile
         0388 [58]   2025   Impl        Model         I   Assert                    RT-exec                                      general-SW
         0390 [59]   2026   Spec        –             D   Judge                     LLM-judge                                    web
         0406 [60]   2025   Impl        Spec          I   Assert; Invar; Property   Formal; RT-exec                              security
         0408 [61]   2025   Spec        Impl          D   Assert; Invar; Property   Human-rev; RT-exec                           security
         0413 [62]   2025   Impl        –             I   Assert                    Exact                                        general-SW
         0417 [6]    2025   Model       Human         I   Judge                     LLM-judge                                    GUI
         0464 [63]   2026   Model       Implicit      I   Judge; Metam              LLM-judge; Semantic                          mobile
         0698 [16]   2024   Spec        –             D   Assert                    RT-exec                                      general-SW
         0699 [19]   2023   Ref-diff    Model         I   Exp-out                   Exact; RT-exec                               general-SW
         1131 [4]    2025   Spec        Impl          P   Assert; Exp-out           Exact; RT-exec                               general-SW
         1154 [64]   2025   Impl        Regression    I   Assert; Exp-out           Exact; RT-exec                               general-SW
         1311 [65]   2025   Spec        –             D   Exp-out; Property         Exact; RT-exec                               embedded/PLC
         1725 [7]    2025   Spec        Human         D   Assert; Judge             LLM-judge; RT-exec                           web
         1846 [66]   2026   Spec        Impl          D   Assert; Exp-out           LLM-judge; RT-exec                           general-SW
         1850 [28]   2026   Ref-diff    –             I   Metam                     Exact; Formal; RT-exec                       other
         1985 [20]   2026   Ref-diff    Spec          P   Assert; Exp-out           RT-exec; Semantic                            general-SW
         2138 [67]   2026   Spec        Ref-diff      P   Judge                     LLM-judge; Semantic                          general-SW
         2246 [68]   2022   Model       Human         I   Assert; Exp-out           LLM-judge; RT-exec                           general-SW
         2247 [69]   2023   Model       Spec          P   Assert; Judge             Exact; RT-exec                               general-SW
         2248 [70]   2023   Model       Human         P   Assert; Exp-out; Other    RT-exec                                      general-SW
         2249 [71]   2026   Impl        –             I   Assert; Metam             Exact; RT-exec; Statist                      general-SW
         2250 [72]   2026   Impl        –             I   Assert                    Other; RT-exec                               general-SW
         2251 [73]   2024   Human       –             I   Assert                    Exact; RT-exec                               general-SW
         2252 [74]   2026   Human       Model         I   Assert; Exp-out           LLM-judge; Exact; Human-rev; RT-exec         embedded/PLC
         2253 [75]   2026   Impl        Model         I   Assert; Invar             LLM-judge; RT-exec                           general-SW
         2254 [76]   2026   Spec        Implicit      D   Assert; Invar             RT-exec                                      web
         2255 [77]   2025   Spec        Impl          P   Assert; Property          RT-exec                                      general-SW
         2256 [78]   2025   Model       Human         I   Judge                     LLM-judge                                    mobile
         2257 [79]   2024   Spec        Impl          D   Assert; Invar             Formal                                       general-SW
         2258 [80]   2026   Model       Spec          P   Assert; Exp-out           LLM-judge; Exact; RT-exec; Statist           general-SW
         2259 [81]   2026   Spec        –             D   Assert                    Other; RT-exec                               general-SW
                                                                                                                            continued on next page
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                                  17


           Table XI continued
           ID          Yr       Source       2nd src      Sp Form(s)                 Mechanism(s)                               Domain
           2260 [82]   2026     Regression   Human        P   Assert; Judge          LLM-judge; Human-rev; Other; RT-exec       general-SW
           2261 [83]   2026     Impl         Human        I   Assert                 RT-exec                                    general-SW
           2262 [84]   2026     Impl         –            I   Assert                 RT-exec                                    general-SW
           2263 [85]   2025     Model        Impl         I   Assert; Judge          LLM-judge                                  general-SW
           2264 [86]   2025     Human        –            I   Assert                 RT-exec                                    general-SW
           2265 [87]   2025     Human        Regression   I   Assert                 Exact; RT-exec                             general-SW
           2266 [88]   2026     Spec         –            D   Assert; Invar          Formal; Human-rev                          embedded/PLC
           2267 [89]   2025     Spec         Human        D   Invar                  Formal                                     general-SW
           2268 [90]   2025     Human        Spec         P   Assert                 RT-exec                                    general-SW
           2269 [91]   2025     Spec         –            D   Assert; Invar          Formal; Human-rev; RT-exec                 security
           2270 [92]   2026     Model        Impl         I   Assert; Judge          Statist                                    general-SW
           2271 [93]   2024     Regression   –            I   Assert                 RT-exec                                    general-SW
           2272 [94]   2025     Ref-diff     Spec         P   Exp-out                Exact; RT-exec                             general-SW
           2273 [95]   2024     Model        Human        I   Assert; Exp-out        Exact; RT-exec                             general-SW
           2274 [96]   2023     Impl         Spec         I   Invar; Property        RT-exec                                    general-SW


Abbreviations. Source of authority: Spec, specification-derived; Impl, implementation-derived; Model, model-parametric; Ref-diff, reference-differential;
Human, human-elicited; Regression, regression-from-prior-version; Implicit, implicit-intrinsic (a dash denotes no secondary source). Specification dependence
(Sp): D, dependent; P, partly; I, independent. Oracle form: Assert, assertion; Exp-out, expected-output value; Metam, metamorphic relation; Invar,
invariant; Property, property-based testing (PBT); Judge, classifier/judge label; Other, exception oracle. Adjudication mechanism: RT-exec, runtime assertion
execution; Exact, exact/structural match; LLM-judge, large language model as judge; Human-rev, human review; Statist, statistical/distributional; Semantic,
semantic/similarity; Formal, formal verification. Domain: general-SW, general-purpose software; ML/DL, machine/deep learning; PLC, programmable logic
controller; API/REST, application programming interface/representational state transfer; ADS, autonomous driving system; GUI, graphical user interface.
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                                       18



                         DATA AVAILABILITY                                       [12] M. Taromirad and P. Runeson, “Assertions in software testing: Survey,
                                                                                      landscape, and trends,” International Journal on Software Tools for Tech-
   The replication package for this review is openly available                        nology Transfer, vol. 27, no. 1, pp. 117–135, 2025, doi: 10.1007/s10009-
on Zenodo [22] under a CC BY 4.0 license. Its concept                                 025-00794-1.
                                                                                 [13] T. Y. Chen et al., “Metamorphic testing: A review of challenges and
DOI, 10.5281/zenodo.21194940, always resolves to the current                          opportunities,” ACM Computing Surveys, vol. 51, no. 1, pp. 1–27, 2018,
version. It contains the review protocol and extraction code-                         doi: 10.1145/3143561.
book, the frozen search query and screening log, the complete                    [14] M. A. Gulzar, Y. Zhu, and X. Han, “Perception and practices of differen-
                                                                                      tial testing,” in Proc. IEEE/ACM 41st Int. Conf. Software Engineering:
de-duplicated screening funnel with per-record decisions and                          Software Engineering in Practice (ICSE-SEIP), 2019, pp. 71–80, doi:
reasons, the independent dual-screening decisions, the Stage-                         10.1109/ICSE-SEIP.2019.00016.
1 screening prompt, the per-study coding sheet (with an                          [15] S. M. Khandaker, F. Kifetew, D. Prandi, and A. Susi, “AugmenTest:
                                                                                      Enhancing Tests with LLM-Driven Oracles,” Proc. IEEE Conference
anchoring quotation for every study), both coding passes for                          on Software Testing, Verification and Validation (ICST), 2025, doi:
each arm together with the per-record adjudication decisions,                         10.1109/icst62969.2025.10988926.
and the PRISMA 2020 flow diagram and checklist. Publisher                        [16] M. Endres, S. Fakhoury, S. Chakraborty, and S. K. Lahiri, “Can
PDFs, raw database exports, and record abstracts are not                              Large Language Models Transform Natural Language Intent into For-
                                                                                      mal Method Postconditions?,” Proc. ACM Softw. Eng., 2024, doi:
redistributed for copyright reasons. The released per-database                        10.1145/3660791.
exports contain bibliographic metadata only.                                     [17] T. Rosenbach, D. Heidrich, and A. Weinert, “Automated Testing
                                                                                      of the GUI of a Real-Life Engineering Software using Large Lan-
                                                                                      guage Models,” Proc. IEEE International Conference on Software
                         ACKNOWLEDGMENT                                               Testing, Verification and Validation Workshops (ICSTW), 2025, doi:
                                                                                      10.1109/icstw64639.2025.10962502.
   The authors thank Noor Fatima (National University of                         [18] B. Ju et al., “A Study of Using Multimodal LLMs for Non-
                                                                                      Crash Functional Bug Detection in Android Apps,” Proc. Asia-
Sciences and Technology, Pakistan) for her help with the final                        Pacific Software Engineering Conference, APSEC, 2024, doi:
review and corrections of the manuscript. An LLM (Anthropic                           10.1109/apsec65559.2024.00017.
Claude) was used as the recall-oriented screening pre-filter                     [19] T.-O. Li et al., “Nuances Are the Key: Unlocking ChatGPT to
                                                                                      Find Failure-Inducing Tests with Differential Prompting,” Proc. 38th
described in the Methodology, disclosed under PRISMA 2020                             IEEE/ACM International Conference on Automated Software Engineer-
item 8. Every retained and sampled screening decision was                             ing, 2023, doi: 10.1109/ase56229.2023.00089.
verified by independent human dual screening.                                    [20] T. Li et al., “Less Is More: Failing Test Generation with Large
                                                                                      Language Models,” ACM Trans. Softw. Eng. Methodol., 2026, doi:
                                                                                      10.1145/3793675.
                              R EFERENCES                                        [21] B. Kitchenham and S. Charters, “Guidelines for performing system-
                                                                                      atic literature reviews in software engineering,” Keele University and
 [1] E. T. Barr, M. Harman, P. McMinn, M. Shahbaz, and S. Yoo, “The                   Durham University, Joint Tech. Rep. EBSE-2007-01, 2007.
     oracle problem in software testing: A survey,” IEEE Transactions            [22] A. H. Mughal and M. Bilal, “LLM-Based Test Oracles: Source-
     on Software Engineering, vol. 41, no. 5, pp. 507–525, 2015, doi:                 of-Authority Taxonomy - Replication Package,” Zenodo, 2026, doi:
     10.1109/TSE.2014.2372785.                                                        10.5281/zenodo.21194940.
 [2] S. B. Hossain and M. B. Dwyer, “TOGLL: Correct and Strong Test              [23] Anthropic, “Claude Opus 4.8 system card,” Anthropic, San Francisco,
     Oracle Generation with LLMs,” Proc. International Conference on                  CA, USA, May 2026. [Online]. Available: https://www.anthropic.com/
     Software Engineering, 2025, doi: 10.1109/icse55347.2025.00098.                   claude-opus-4-8-system-card.
 [3] S. Primbs, B. Fein, and G. Fraser, “AsserT5: Test Assertion Generation      [24] J. Cohen, “A coefficient of agreement for nominal scales,” Educational
     Using a Fine-Tuned Code Language Model,” Proc. IEEE/ACM Inter-                   and Psychological Measurement, vol. 20, no. 1, pp. 37–46, 1960, doi:
     national Conference on Automation of Software Test, AST, 2025, doi:              10.1177/001316446002000104.
     10.1109/ast66626.2025.00008.                                                [25] B. Efron, “Bootstrap methods: Another look at the jackknife,”
 [4] S. B. Hossain, R. Taylor, and M. Dwyer, “Doc2OracLL: Investigating               The Annals of Statistics, vol. 7, no. 1, pp. 1–26, 1979, doi:
     the Impact of Documentation on LLM-Based Test Oracle Generation,”                10.1214/aos/1176344552.
     Proc. ACM Softw. Eng., 2025, doi: 10.1145/3729354.                          [26] C. J. Clopper and E. S. Pearson, “The use of confidence or fiducial
 [5] Z. Liu et al., “Seeing is Believing: Vision-Driven Non-Crash Func-               limits illustrated in the case of the binomial,” Biometrika, vol. 26, no. 4,
     tional Bug Detection for Mobile Apps,” IEEE Transactions on Soft-                pp. 404–413, 1934, doi: 10.1093/biomet/26.4.404.
     ware Engineering, vol. 51, no. 12, pp. 3452–3466, 2025, doi:                [27] A. Bodicoat, G. Jahangirova, and V. Terragni, “Understanding LLM-
     10.1109/tse.2025.3614469.                                                        Driven Test Oracle Generation,” Proc. 2nd IEEE/ACM International
 [6] Y. Hu et al., “KuiTest: Leveraging Knowledge in the Wild as GUI                  Conference on AI-powered Software, AIware, 2025, doi: 10.1109/ai-
     Testing Oracle for Mobile Apps,” Proc. IEEE/ACM International Con-               ware69974.2025.00011.
     ference on Software Engineering: Software Engineering in Practice           [28] Q. Mang, R. He, S. Zhong, X. Liu, H. Zhang, and A. Cheung, “Au-
     (ICSE-SEIP), 2025, doi: 10.1109/icse-seip66354.2025.00009.                       tomated Discovery of Test Oracles for Database Management Systems
 [7] A. Chevrot, A. Vernotte, J. Falleri, X. Blanc, B. Legeard, and A. Cretin,        Using LLMs,” Proc. ACM Manag. Data, 2026, doi: 10.1145/3802017.
     “Are Autonomous Web Agents Good Testers?,” Proc. ACM Softw. Eng.,           [29] M. Ferreira, L. Viegas, J. P. Faria, and B. Lima, “Acceptance Test
     2025, doi: 10.1145/3728879.                                                      Generation with Large Language Models: An Industrial Case Study,”
 [8] J. Wang, Y. Huang, C. Chen, Z. Liu, S. Wang, and Q. Wang,                        Proc. IEEE/ACM International Conference on Automation of Software
     “Software Testing with Large Language Models: Survey, Landscape,                 Test, AST, 2025, doi: 10.1109/ast66626.2025.00007.
     and Vision,” IEEE Transactions on Software Engineering, 2024, doi:          [30] D. B. Bose, “From Prompts to Properties: Rethinking LLM Code
     10.1109/tse.2024.3368208.                                                        Generation with Property-Based Testing,” Proc. ACM SIGSOFT Sym-
 [9] X. Hou et al., “Large Language Models for Software Engineering: A                posium on the Foundations of Software Engineering, 2025, doi:
     Systematic Literature Review,” ACM Transactions on Software Engi-                10.1145/3696630.3728702.
     neering and Methodology, 2024, doi: 10.1145/3695988.                        [31] J. Huang, M. Li, X. Yang, J. Liu, and S. Yan, “SVPrompt-MR: An
[10] J. Zhang, C.-A. Sun, H. Liu, and S. Dong, “Can Large Language Models             LLM-Based Metamorphic Relation Identification Method with Self-
     Discover Metamorphic Relations? A Large-Scale Empirical Study,”                  Verification Mechanism,” Proc. Asia-Pacific Software Engineering Con-
     Proc. IEEE International Conference on Software Analysis, Evolution              ference, APSEC, 2025, doi: 10.1109/apsec66846.2025.00055.
     and Reengineering, SANER, 2025, doi: 10.1109/saner64311.2025.00011.         [32] A. K. Vajjala et al., “Using Large Language Models to Support
[11] M. J. Page et al., “The PRISMA 2020 statement: an updated guideline              the Workflow of Differential Testing,” Proc. ACM SIGSOFT Sym-
     for reporting systematic reviews,” BMJ, vol. 372, no. n71, 2021, doi:            posium on the Foundations of Software Engineering, 2025, doi:
     10.1136/bmj.n71.                                                                 10.1145/3696630.3728559.
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                                    19



[33] M. Li, D. Li, J. Liu, J. Cao, Y. Tian, and S.-C. Cheung, “Enhancing                in Exploring Edge Cases,” Proc. 2nd IEEE/ACM International Con-
     Differential Testing with LLMs for Testing Deep Learning Libraries,”               ference on AI-powered Software, AIware, 2025, doi: 10.1109/ai-
     ACM Transactions on Software Engineering and Methodology, 2026,                    ware69974.2025.00009.
     doi: 10.1145/3735637.                                                         [53] J. Jagielski, C. Rojas, and M. Abel, “Exploratory Study on Private GPTs
[34] D. Molinelli, L. D. Grazia, A. Martin-Lopez, M. D. Ernst, and                      for LLM-Driven Test Generation in Software and Machine Learning
     M. Pezze, “Do LLMs Generate Useful Test Oracles? An Empirical                      Development,” Proc. International Generative AI and Computational
     Study with an Unbiased Dataset,” Proc. 40th IEEE/ACM Interna-                      Language Modelling Conference (GACLM), 2025, doi: 10.1109/ga-
     tional Conference on Automated Software Engineering, ASE, 2025, doi:               clm67198.2025.11232354.
     10.1109/ase63991.2025.00031.                                                  [54] Y. Zhang, D. Towey, and M. Pike, “Automated Metamorphic-Relation
[35] C. Sun et al., “ClassInvGen: Class Invariant Synthesis Using Large                 Generation with ChatGPT: An Experience Report,” Proc. Interna-
     Language Models,” Lecture Notes in Computer Science, 2026, doi:                    tional Computer Software and Applications Conference, 2023, doi:
     10.1007/978-3-031-99991-8 4.                                                       10.1109/compsac57700.2023.00275.
[36] G. Zeng, J. Luo, Y. Qiao, S. Teng, and A. Liu, “SpaceMutation : An            [55] J. Johnson, J. Mahmud, O. Chaparro, K. Moran, and M. Fazz-
     LLM-assisted mutation testing framework for DNNs in distributed LEO                ini, “Generating Failure-Based Oracles to Support Testing of Re-
     satellites,” Expert Systems with Applications, vol. 323, art. 132431, 2026,        ported Bugs in Android Apps,” Proc. 40th IEEE/ACM International
     doi: 10.1016/j.eswa.2026.132431.                                                   Conference on Automated Software Engineering, ASE, 2025, doi:
[37] B. Metekia, L. Pietrac, and K. Kouiss, “MBSE-Driven PLC Code Gener-                10.1109/ase63991.2025.00182.
     ation and AI-Augmented Test Scenario Validation,” Proc. International         [56] Y. Zhang, T. Y. Chen, M. Pike, D. Towey, Z. Ying, and Z. Q. Zhou,
     Conference on Automation, Robotics and Applications, ICARA, 2026,                  “Enhancing autonomous driving simulations: A hybrid metamorphic
     doi: 10.1109/icara69401.2026.11480393.                                             testing framework with metamorphic relations generated by GPT,”
[38] S. Fischer and C. Klammer, “Automating Invariant Filtering: Leveraging             Information and Software Technology, vol. 187, art. 107828, 2025, doi:
     LLMs to Streamline Test Oracle Generation,” Lecture Notes in Business              10.1016/j.infsof.2025.107828.
     Information Processing, 2025, doi: 10.1007/978-3-031-89277-6 4.               [57] Q. Zhang et al., “Exploring Automated Assertion Generation via
[39] Z. Fan, H. Ruan, S. Mechtaev, and A. Roychoudhury, “Oracle-Guided                  Large Language Models,” ACM Transactions on Software Engineer-
     Program Selection from Large Language Models,” ISSTA, 2024, doi:                   ing and Methodology, vol. 34, no. 3, art. 81, pp. 1–25, 2025, doi:
     10.1145/3650212.3680308.                                                           10.1145/3699598.
[40] A. K. Vajjala et al., “Enhancing Differential Testing: LLM-Powered Au-        [58] I. Hayet, A. Scott, and M. D’Amorim, “ChatAssert: LLM-Based Test
     tomation in Release Engineering,” IEEE/ACM International Conference                Oracle Generation With External Tools Assistance,” IEEE Transactions
     on Software Engineering - Software Engineering in Practice, 2025, doi:             on Software Engineering, vol. 51, no. 1, pp. 305–319, 2025, doi:
     10.1109/icse-seip66354.2025.00059.                                                 10.1109/tse.2024.3519159.
[41] Z. Liu, H. Wang, T. Xu, and B. Wang, “RAG-Driven multiple assertions          [59] J. Quispe, H. Cordova, and L. Wong, “Approach for Generating and
     generation with large language models,” Empirical Software Engineer-               Executing Acceptance Tests Based on Computer Vision and GPT-4,”
     ing, 2025, doi: 10.1007/s10664-025-10641-1.                                        Proc. International Conference on Software Engineering and Computer
                                                                                        Science (CSECS), 2026, doi: 10.1109/csecs69124.2026.11541611.
[42] C. Ni, X. Wang, X. Yin, L. Chen, and G. Ma, “A Cascaded Pipeline for
                                                                                   [60] G. E. Raptis, M. T. Khan, C. Koulamas, and D. Serpanos, “Synthesizing
     Self-Directed, Model-Agnostic Unit Test Generation via LLMs,” Proc.
                                                                                        Inline Security Monitors for ICS Using Generative AI and Formal-
     International Symposium on Software Reliability Engineering, ISSRE,
                                                                                        Bench,” IECON, 2025, doi: 10.1109/iecon58223.2025.11221437.
     2025, doi: 10.1109/issre66568.2025.00037.
                                                                                   [61] G. E. Raptis, M. T. Khan, C. Koulamas, and D. Serpanos, “LLM-based
[43] J. C. Alonso, A. Martin-Lopez, S. Segura, G. Bavota, and A. Ruiz-
                                                                                        Generation of Formal Specification for Run-time Security Monitoring
     Cortés, “SATORI: Static Test Oracle Generation for REST APIs,”
                                                                                        of ICS,” Proc. IEEE International Conference on Cyber Security and
     Proc. 40th IEEE/ACM International Conference on Automated Software
                                                                                        Resilience (CSR), 2025, doi: 10.1109/csr64739.2025.11130130.
     Engineering, ASE, 2025, doi: 10.1109/ase63991.2025.00116.
                                                                                   [62] Q. Zhang et al., “Improving Retrieval-Augmented Deep Assertion Gen-
[44] J. Shin, H. Hemmati, M. Wei, and S. Wang, “Assessing Evaluation                    eration via Joint Training,” IEEE Transactions on Software Engineering,
     Metrics for Neural Test Oracle Generation,” IEEE Transactions on                   vol. 51, no. 4, pp. 1232–1247, 2025, doi: 10.1109/tse.2025.3545970.
     Software Engineering, 2024, doi: 10.1109/tse.2024.3433463.                    [63] Q. Liang, C. Li, F. Yang, and Q. Xu, “A Detection Method for
[45] K. Etemadi, M. Sirjani, M. Helali Moghadam, P. Strandberg, and P.                  Text Input-Induced Non-Crashing Functional Bugs in Mobile GUI
     Pettersson, “LLM-Based Property-Based Test Generation for Guardrail-               Testing,” Proc. International Conference on Advanced Electronic Tech-
     ing Cyber-Physical Systems,” Lecture Notes in Computer Science, 2026,              nology, Computers and Software Engineering (AETCSE), 2026, doi:
     doi: 10.1007/978-3-032-07132-3 3.                                                  10.1109/aetcse69203.2026.11504024.
[46] S. R. R. dos Santos, M. S. Soares, R. E. S. Fernandes, F. G. Rocha,           [64] Y. Shang, Q. Zhang, C. Fang, S. Gu, J. Zhou, and Z. Chen, “A Large-
     M. C. B. dos Santos, and S. Marczak, “Increasing Test Coverage                     Scale Empirical Study on Fine-Tuning Large Language Models for Unit
     by Automating BDD Tests in Proofs of Concepts (POCs) using                         Testing,” Proc. ACM Softw. Eng., 2025, doi: 10.1145/3728951.
     LLM,” Brazilian Symposium on Software Quality (SBQS), 2024, doi:              [65] X. Ma, J. Chen, L. Luo, and Q. Zeng, “LLM-Assisted IoT Testing:
     10.1145/3701625.3701637.                                                           Finding Conformance Bugs in Matter SDKs,” Proc. 31st Annual Inter-
[47] S. Y. Shin, F. Pastore, D. Bianculli, and A. Baicoianu, “Towards                   national Conference on Mobile Computing and Networking, 2025, doi:
     Generating Executable Metamorphic Relations Using Large Language                   10.1145/3680207.3765257.
     Models,” Communications in Computer and Information Science, 2024,            [66] Q. Xu, G. Wang, L. Briand, and K. Liu, “Hallucination to Consensus:
     doi: 10.1007/978-3-031-70245-7 9.                                                  Multi-Agent LLMs for End-to-End JUnit Test Generation,” ACM Trans.
[48] H. Lee, G. An, and S. Yoo, “Metamon: Finding Inconsisten-                          Softw. Eng. Methodol., 2026, doi: 10.1145/3803418.
     cies between Program Documentation and Behavior using Meta-                   [67] Y. Li, Y. Ji, X. Chen, Z. Shen, J. Ge, and B. Luo, “FURINA: A Multi-
     morphic LLM Queries,” Proc. IEEE/ACM International Workshop                        Agent Framework for Automated Patch Correctness Assessment,” ACM
     on Large Language Models for Code, LLM4Code, 2025, doi:                            Trans. Softw. Eng. Methodol., 2026, doi: 10.1145/3811825.
     10.1109/llm4code66737.2025.00020.                                             [68] E. Dinella, G. Ryan, T. Mytkowicz, and S. K. Lahiri, “TOGA: a neural
[49] S. R. R. dos Santos et al., “Automated Test Generation Using LLM                   method for test oracle generation,” Proc. International Conference on
     Based on BDD: A Comparative Study,” International Conference on Web                Software Engineering (ICSE), 2022, doi: 10.1145/3510003.3510141.
     Information Systems and Technologies, WEBIST - Proceedings, 2025,             [69] Z. Liu, K. Liu, X. Xia, and X. Yang, “Towards More Realistic Evaluation
     doi: 10.5220/0013683600003985.                                                     for Neural Test Oracle Generation,” Proc. ACM SIGSOFT Interna-
[50] C. Hazott and D. Große, “LLM-assisted Metamorphic Testing of Embed-                tional Symposium on Software Testing and Analysis (ISSTA), 2023, doi:
     ded Graphics Libraries,” Forum on Specification and Design Languages,              10.1145/3597926.3598080.
     2025, doi: 10.1109/fdl68117.2025.11165405.                                    [70] S. B. Hossain, A. Filieri, M. B. Dwyer, S. Elbaum, and W. Visser,
[51] P. C. Cañizares, P. Gómez-Abajo, E. Guerra, and J. de Lara, “To-                 “Neural-Based Test Oracle Generation: A Large-Scale Evaluation and
     wards metamorphic testing with LLM-based workflows: Metamor-                       Lessons Learned,” Proc. ACM Joint European Software Engineering
     phic relation inference and follow-up test case generation,” Infor-                Conference and Symposium on the Foundations of Software Engineering
     mation and Software Technology, vol. 196, art. 108150, 2026, doi:                  (ESEC/FSE), 2023, doi: 10.1145/3611643.3616265.
     10.1016/j.infsof.2026.108150.                                                 [71] C. Xu, H. Zhu, S. Chen, J. Wu, V. Terragni, and S. C. Cheung, “MR-
[52] H. Tanaka, H. Tanaka, K. Shimari, and K. Matsumoto, “Under-                        Coupler: Automated Metamorphic Test Generation via Functional Cou-
     standing the Characteristics of LLM-Generated Property-Based Tests                 pling Analysis,” Proc. ACM Softw. Eng., 2026, doi: 10.1145/3808213.
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738                                                                                     20



[72] A. Celik and Q. H. Mahmoud, “GEM: A Framework for Strengthening            [92] H. Taherkhani, J. Shin, M. A. Tahir, M. R. H. Misu, V. S. Gattani,
     LLM-Generated Unit Tests Using Mutation Feedback,” Proc. Confer-                and H. Hemmati, “Toward Automated Validation of Language Model
     encia Iberoamericana de Software Engineering (CIbSE), 2026, doi:                Synthesized Test Cases Using Semantic Entropy,” IEEE Transactions
     10.5753/cibse.2026.42441.                                                       on Software Engineering, 2026, doi: 10.1109/TSE.2026.3664287.
[73] Y. He, J. Huang, H. Yu, and T. Xie, “An Empirical Study on Focal           [93] N. Mündler, M. Müller, J. He, and M. Vechev, “SWT-Bench: Test-
     Methods in Deep-Learning-Based Approaches for Assertion Genera-                 ing and Validating Real-World Bug-Fixes with Code Agents,” Ad-
     tion,” Proc. ACM Softw. Eng., 2024, doi: 10.1145/3660785.                       vances in Neural Information Processing Systems (NeurIPS), 2024, doi:
[74] C. Li et al., “AutoOracle: High-Quality C++ Test Oracle Generation via          10.52202/079017-2601.
     Data Quality-Driven and Filtering-Enabled LLMs,” Proc. IEEE/ACM In-        [94] K. Liu et al., “LLM-Powered Test Case Generation for Detecting
     ternational Conference on Software Engineering: Software Engineering            Bugs in Plausible Programs,” Proc. Annual Meeting of the Association
     in Practice (ICSE-SEIP), 2026, doi: 10.1145/3786583.3786868.                    for Computational Linguistics (ACL), 2025, doi: 10.18653/v1/2025.acl-
[75] A. Balestra, A. Nolasco, F. Molina, D. Garbervetsky, R. Degiovanni,             long.20.
     and N. Aguirre, “Improving Dynamic Specification Inference with            [95] S. Alagarsamy, C. Tantithamthavorn, and A. Aleti, “A3Test: Assertion-
     LLM-Generated Counterexamples,” Proc. IEEE International Confer-                Augmented Automated Test case generation,” Information and Software
     ence on Software Testing, Verification and Validation (ICST), 2026, doi:        Technology, 2024, doi: 10.1016/j.infsof.2024.107565.
     10.1109/ICST69053.2026.00059.                                              [96] K. Pei, D. Bieber, K. Shi, C. Sutton, and P. Yin, “Can Large Language
[76] X. Teoh, Y. Lin, D. M. Nguyen, R. Ren, W. Zhang, and J. S.                      Models Reason about Program Invariants?,” Proc. International Confer-
     Dong, “WebTestPilot: Agentic End-to-End Web Testing against Natural             ence on Machine Learning (ICML), PMLR 202, 2023, pp. 27496–27520.
     Language Specification by Inferring Oracles with Symbolized GUI                 [Online]. Available: https://proceedings.mlr.press/v202/pei23a.html.
     Elements,” Proc. ACM Softw. Eng., 2026, doi: 10.1145/3797115.              [97] V. I. T. Perera and D. I. De Silva, “Evaluating Large Language Models
[77] D. Molinelli, A. Martin-Lopez, E. Zackrone, B. Eken, M. D. Ernst, and           for Software Testing: A Systematic Review of Metrics and Practices,”
     M. Pezzè, “Tratto: A Neuro-Symbolic Approach to Deriving Axiomatic             Lecture Notes in Networks and Systems, 2026, doi: 10.1007/978-3-032-
     Test Oracles,” Proc. ACM Softw. Eng., 2025, doi: 10.1145/3728960.               18913-4 27.
[78] Y. Hu et al., “Minuku: Detecting Diverse Display Issues in Mo-             [98] F. Molina, A. Gorla, and M. D’Amorim, “Test Oracle Automation in
     bile Apps with Small-scale Dataset,” Proc. IEEE/ACM International               the Era of LLMs,” ACM Transactions on Software Engineering and
     Conference on Automated Software Engineering (ASE), 2025, doi:                  Methodology, 2025, doi: 10.1145/3715107.
     10.1109/ASE63991.2025.00270.                                               [99] A. Duque-Torres, S. Fischer, and C. Klammer, “Metamorphic Testing
[79] C. Wen et al., “Enchanting Program Specification Synthesis by Large             for Sequential Prediction Models: A Survey of LSTMs and LLMs,”
     Language Models Using Static Analysis and Program Verification,”                Proc. IEEE International Conference on Software Analysis, Evolution
     Lecture Notes in Computer Science, 2024, doi: 10.1007/978-3-031-                and Reengineering - Companion, SANER-C, 2026, doi: 10.1109/saner-
     65630-9 16.                                                                     c67878.2026.00054.
[80] H. Taherkhani, A. DaghighFarsoodeh, M. Chowdhury, H. V.                    [100] J. Zhang, X. Hu, C. Gao, X. Xia, and S. Li, “Enhancing Automated
     Pham, and H. Hemmati, “Consistency Meets Verification: Enhanc-                  Unit Test Generation with Large Language Models: A Systematic
     ing Test Generation Quality in Large Language Models Without                    Literature Review,” ACM Trans. Softw. Eng. Methodol., 2026, doi:
     Ground-Truth Solutions,” Proc. IEEE International Conference on                 10.1145/3802827.
     Software Testing, Verification and Validation (ICST), 2026, doi:           [101] S. Fischer and W. Kloihofer, “LLM Agents for Autonomous System
     10.1109/ICST69053.2026.00039.                                                   Testing: A Semi-structured Literature Review,” Lecture Notes in Busi-
[81] T. Kiecker, J. A. Sparka, M. Reuter, A. Ziegler, and L. Grunske, “CAS-          ness Information Processing, 2026, doi: 10.1007/978-3-032-24216-7 9.
     CADE: Detecting Inconsistencies between Code and Documentation             [102] I. Pysmennyi, R. Kyslyi, and K. Kleshch, “AI-DRIVEN TOOLS IN
     with Automatic Test Generation,” Proc. ACM Softw. Eng., 2026, doi:              MODERN SOFTWARE QUALITY ASSURANCE: AN ASSESSMENT
     10.1145/3808175.                                                                OF BENEFITS, CHALLENGES, AND FUTURE DIRECTIONS,” Tech-
[82] M. Becker et al., “Just-in-Time Catching Test Generation at                     nology Audit and Production Reserves, 2025, doi: 10.15587/2706-
     Meta,” Proc. ACM International Conference on the Foundations                    5448.2025.330595.
     of Software Engineering, Companion (FSE Companion), 2026, doi:             [103] Umama et al., “LLM-Based Code Generation: A Systematic Literature
     10.1145/3803437.3805202.                                                        Review With Technical and Demographic Insights,” IEEE Access, 2025,
[83] G. Zhang and J. Zhai, “POSTCONDBENCH: Benchmarking Correct-                     doi: 10.1109/access.2025.3631952.
     ness and Completeness in Formal Postcondition Inference,” Findings of      [104] Q. Wang, J. Wang, M. Li, Y. Wang, and Z. Liu, “A Roadmap for
     the Association for Computational Linguistics (ACL Findings), 2026,             Software Testing in Open-Collaborative and AI-Powered Era,” ACM
     doi: 10.18653/v1/2026.findings-acl.1768.                                        Trans. Softw. Eng. Methodol., 2025, doi: 10.1145/3709355.
[84] C. C. Le et al., “SpecMind: Cognitively Inspired, Interactive Multi-       [105] A. J. Calderón et al., “On the Use of Artificial Intelligence in Software
     Turn Framework for Postcondition Inference,” Annual Meeting of                  Testing: State of the Art and Application to Satellite Systems,” ACM
     the Association for Computational Linguistics (ACL), 2026, doi:                 Trans. Cyber-Phys. Syst., 2026, doi: 10.1145/3783988.
     10.48550/arXiv.2602.20610.                                                 [106] D. Amalfitano, R. Coppola, D. Distante, and F. Ricca, “AI in GUI-
[85] S. Ruberto, J. Perera, G. Jahangirova, and V. Terragni, “From Im-               based testing: A survey of techniques, tools, and perceived advan-
     plemented to Expected Behaviors: Leveraging Regression Oracles for              tages and limitations,” Journal of Systems and Software, 2026, doi:
     Non-regression Fault Detection using LLMs,” Proc. IEEE International            10.1016/j.jss.2025.112751.
     Conference on Software Testing, Verification and Validation Workshops      [107] P. Sweetser, “Large Language Models and Video Games: A Preliminary
     (ICSTW), 2025, doi: 10.1109/ICSTW64639.2025.10962503.                           Scoping Review,” Proc. 6th ACM Conference on Conversational User
[86] H. Li et al., “Retrieval-Augmented Fine-Tuning for Improving Retrieve-          Interfaces, 2024, doi: 10.1145/3640794.3665582.
     and-Edit Based Assertion Generation,” IEEE Transactions on Software        [108] Q. Song, H. Ye, M. Harman, and F. Sarro, “Generative AI for Testing
     Engineering, 2025, doi: 10.1109/TSE.2025.3558403.                               of Autonomous Driving Systems: A Survey,” ACM Trans. Softw. Eng.
[87] Q. Zhang et al., “Improving Deep Assertion Generation via Fine-Tuning           Methodol., 2026, doi: 10.1145/3806653.
     Retrieval-Augmented Pre-trained Language Models,” ACM Transactions
     on Software Engineering and Methodology, 2025, doi: 10.1145/3721128.
[88] Z. Wang et al., “A Tale of 1001 LoC: Potential Runtime Error-Guided
     Specification Synthesis for Verifying Large-Scale Programs,” Proc. ACM
     Program. Lang., 2026, doi: 10.1145/3798268.
[89] G. Sakkas, P. Sahu, K. Ong, and R. Jhala, “Neurosymbolic Modular
     Refinement Type Inference,” Proc. International Conference on Software
     Engineering (ICSE), 2025, doi: 10.1109/ICSE55347.2025.00090.
[90] Y. W. Zhang, Z. Jin, Z. J. Wang, Y. Xing, and G. Li, “SAGA:
     Summarization-Guided Assert Statement Generation,” Journal of Com-
     puter Science and Technology, 2025, doi: 10.1007/s11390-023-2878-6.
[91] G. E. Raptis, M. T. Khan, C. Koulamas, and D. Serpanos, “Cross-Model
     Evaluation of LLMs for Generating Formal Specification of Distributed
     Industrial Control Systems,” Procedia Computer Science, 2025, doi:
     10.1016/j.procs.2025.10.053.
ACCEPTED FOR PUBLICATION IN IEEE ACCESS. DOI 10.1109/ACCESS.2026.3729738        21



                          Ali Hassaan Mughal (Graduate Student Member,
                          IEEE) has worked as a Senior Software Developer
                          and Team Lead at Xpressdocs, and earlier at Pay-
                          com and a stealth robotics company. His work at
                          Xpressdocs centered on software testing and quality
                          assurance, including the design and evaluation of
                          LLM-based multi-agent systems. He is pursuing an
                          Applied MBA in Data Analytics at Texas Wesleyan
                          University, USA, and holds an M.Sc. in Computer
                          Science from Kansas State University. His research
                          interests include automated software testing, web
application quality assurance, applied machine learning, LLMs, and agentic
AI systems. Earlier he was a graduate teaching and research assistant at
Kansas State University, where he taught core computer science courses and
worked on deep learning for spacecraft trajectory prediction, and a research
intern at Aalto University, Finland, on a human computer interaction project.
He has published in Elsevier, IEEE, and EAI venues. Since 2024 he has
served as a reviewer for Expert Systems with Applications, Computers and
Electrical Engineering, the International Journal of Information Management,
and the ACM Conference on Computer-Supported Cooperative Work and
Social Computing (CSCW).




                         Muhammad Bilal is an AI and Digitalization Con-
                         sultant in the German industrial sector. He holds a
                         Master of Science in Management from the Techni-
                         cal University of Munich, Germany, and has pre-
                         viously worked as a Software Engineer, Business
                         Analyst, and Product Owner. His research interests
                         include the impact of technology on business perfor-
                         mance, product quality analytics, the automation of
                         industrial pipelines, LLMs, and agentic AI systems.
                         His career spans product ownership at Persivia, a
                         clinical AI company; business development at NVi-
sion Quantum Technologies, a quantum biotechnology company; healthcare
software development at Cognitive Healthcare International; and research at
LMU Munich. His current technical work is in agentic systems and LLMs,
covering retrieval-augmented generation, agent orchestration, structured out-
put validation, and the evaluation and grounding verification that decide
whether such systems can be trusted. He has also published on verifying
production LLM applications. His master’s thesis and subsequent research
examine the sustainability and economics of AI, particularly how its energy
use relates to its economic value. He is the corresponding author.
