                                            Natural Language to First-Order Logic LLM-based Autoformalization
                                                                Andrea Brunello1               Cristian Curaba1          Luca Geatti1

                                                        Michele Mignani1∗               Angelo Montanari1             Nicola Saccomanno1
                                                                                    1
                                                                                      University of Udine, Italy
                                                                                     name.surname@uniud.it
                                                                                          ∗
                                                                                              Corresponding author.


                                                               Abstract                                   their flexibility and general-purpose linguistic com-
                                            Large Language Models (LLMs) have renewed                     petence make autoformalization feasible across a
                                                                                                          wide range of domains (Mensfelt et al., 2026). Sec-
arXiv:2610.12030v1 [cs.CL] 8 Oct 2026




                                            interest in autoformalization. Yet, when First-
                                            Order Logic (FOL) is considered as the target                 ond, no systematic survey of LLM-based autofor-
                                            formalism, the field still lacks a unified task for-          malization for FOL currently exists, despite FOL
                                            mulation and a systematic survey. This paper                  offering a well-established balance between expres-
                                            addresses this gap: we first provide a principled             sive power and algorithmic tractability. Surveys
                                            definition for the FOL-autoformalization task
                                                                                                          for other formalisms, such as Linear Temporal
                                            by distinguishing Ontology Extraction from
                                            Logical Translation, showing how their confla-
                                                                                                          Logic (Germiniani et al., 2025) and SQL (Moham-
                                            tion obscures (cross-study) evaluation; we re-                madjafari et al., 2024), already play a pivotal role
                                            view existing datasets, evaluation metrics, and               in their respective landscapes. Third, autoformal-
                                            LLM-based methods, including fine-tuning,                     ization underpins a wide range of relevant applica-
                                            prompting, and verification-based refinement;                 tions. In reasoning tasks, symbolic methods such
                                            we identify open challenges in benchmarking,                  as theorem provers and Satisfiability Modulo The-
                                            semantic evaluation, ontology-aware methods,                  ories (SMT) solvers are reliable and explainable,
                                            and end-to-end applications.
                                                                                                          but require inputs in a precise logical format; auto-
                                        1    Introduction                                                 formalization is thus crucial for converting NL task
                                                                                                          instances into appropriate representations. Recent
                                        In the literature, autoformalization is broadly de-
                                                                                                          work shows that inserting a formalization step and
                                        fined as the task of automatically generating state-
                                                                                                          invoking symbolic tools can outperform directly
                                        ments in a target formalism that capture the seman-
                                                                                                          prompting an LLM to solve multi-step logical rea-
                                        tics of a Natural Language (NL) sentence (Szegedy,
                                                                                                          soning problems (Ye et al., 2023; Olausson et al.,
                                        2020; Mensfelt et al., 2026; Wu et al., 2022). Al-
                                                                                                          2023; Pan et al., 2023; Callewaert et al., 2025),
                                        though NL is well-suited for everyday human com-
                                                                                                          with FOL yielding the best performance in certain
                                        munication, its flexibility, expressiveness, and in-
                                                                                                          settings (Beiser et al., 2025). Beyond reasoning,
                                        herent ambiguity make it ill-suited for interaction
                                                                                                          reliable formalization tools could make formal ver-
                                        with automated reasoning tools, which require in-
                                                                                                          ification accessible to non-experts and enable scal-
                                        puts to be unambiguous and specified within a for-
                                                                                                          able verification of large text corpora, an especially
                                        mal semantic framework. Early work relied on rule-
                                                                                                          important prospect for AI safety approaches that
                                        based systems (Kamath and Das, 2018) and con-
                                                                                                          regard formal guarantees as essential (Dalrymple
                                        trolled natural languages (Kuhn, 2014), while more
                                                                                                          et al., 2024). The significance of autoformaliza-
                                        recent approaches have adopted neural network-
                                                                                                          tion in FOL has also been demonstrated in logi-
                                        based methods (Jiang and Cai, 2024). Despite the
                                                                                                          cal fallacy detection (Lalwani et al., 2024), argu-
                                        considerable research effort devoted to autoformal-
                                                                                                          mentation mining (Sun et al., 2025), legal reason-
                                        ization, the field still lacks a unified formulation
                                                                                                          ing (Alam et al., 2023), and anomaly detection (Jin
                                        and a systematic survey when First-Order Logic
                                                                                                          et al., 2025).
                                        (FOL) is considered as the target formalism. Here,
                                        we address this gap.
                                                                                                          Our contribution. We provide a detailed descrip-
                                        Why this survey. The motivations are threefold.                   tion of the FOL-autoformalization task (Section 2)
                                        First, Large Language Models (LLMs) have re-                      aimed at resolving existing ambiguities. Surveying
                                        shaped the autoformalization research landscape:                  the existing literature, we then focus on evalua-
tion, covering datasets and metrics (Section 3), and       is faithful—is not well-defined.
methods proposed to achieve autoformalization via
LLMs (Section 4). Finally, we highlight open prob-         2.2   Ontology: Signature, Labelling, Theory
lems and directions for future research (Section 5).       We use the term ontology for the structure relative
                                                           to which a FOL formula represents NL content.
2     Autoformalization Definition                         We define it as a triple: Ω = ⟨σ, L, T ⟩, whose
                                                           components are as follows.
Despite a growing body of work on FOL-
autoformalization—both as an engineering com-              Signature σ. A FOL signature is a set of non-
ponent and as a task of independent interest—the           logical symbols with their arities: constants,
field lacks a shared, precise formulation of what          function symbols, and predicate symbols. Sig-
the task requires. Informal descriptions typically         nature σ specifies the vocabulary available for
present autoformalization as the translation of a          translation. In the running example: σ =
NL text into a FOL formula that preserves its se-          {A, B, Cube/1, Tet/1, LeftOf/2}.
mantic content. This formulation is ambiguous: it
leaves open what formal machinery the formula is           Labelling L. The labelling is a possibly partial
interpreted over, and it does not specify under what       function that maps each symbol s ∈ σ to an NL
conditions a formula counts as correct or faithful.        meaning-specification L(s). For our p, for instance,
   In this section we give a more precise account.         L(Cube) = “x is a cube”, When L is fully specified,
We argue that any formalization in FOL is relative         we call ⟨σ, L⟩ a labelled signature. It is the labelled
to an ontology—a structure comprising a formal             signature—not the signature alone—that permits
vocabulary, a labelling of that vocabulary with in-        assessment of whether φ faithfully formalizes p.
tended NL meanings, and a background theory.               Raw translation output exposes σφ but typically
The raw translation p ∈ NL 7→ φ ∈ FOL, typ-                leaves L implicit, conventional, or underspecified.
ically found in the literature, is therefore an ab-        Theory T . The theory is a possibly empty
breviation for a richer artifact. We then introduce        set of FOL sentences over σ that encode back-
Definition 1 for the FOL-autformalization task-            ground axioms, taxonomic relations, and domain-
   We provide FOL background in Appendix A.                specific assumptions. In our example, the formula
                                                           “∀x (Cube(x) → ¬Tet(x))” that expresses that no
2.1    Formulas and Ontological Commitments
                                                           object is simultaneously a cube and a tetrahedron,
Consider the sentence: p := “The cube A is                 can be an element of T . In many sentence-level
on the left of the tetrahedron B.” A natural               datasets, T is empty or left implicit. When auto-
FOL candidate is: φ := Cube(A) ∧ Tet(B) ∧                  formalization feeds into reasoning or verification,
LeftOf(A, B); φ contains the non-logical symbols           however, the theory is often essential: a formula
{A, B, Cube/1, Tet/1, LeftOf/2}, which jointly             that is faithful relative to one theory may be inade-
constitute the signature σφ that φ is written over.        quate relative to another. 1
The signature is derivable from the formula alone.
   What is not derivable from φ alone is the in-           2.3   (Not) Uniqueness of Ontological Choices
tended meaning of these symbols. Nothing in                A single NL sentence does not necessary determine
φ determines that Cube(x) means “x is a cube”              a unique formalization—due to ambiguity, syn-
rather than, say, “x is a room” or any other ar-           onymy, or granularity choices—even relative to a
bitrary unary property. The suggestive symbol              fixed ontology. It also does not determine a unique
names give a strong pragmatic hint, but hints are          ontology. Consider p′ := “Every student passed
not meanings: a formula with symbols renamed               some exam.” Three candidate formalizations
P1 (c1 ) ∧ P2 (c2 ) ∧ R(c1 , c2 ) is logically identical   are: φ1 = ∀x   Student(x) → ∃y (Exam(y) ∧
to φ, yet gives no hint at all.                            Passed(x, y)) , φ2 = ∀x Student(x) →
   This has a direct consequence for evaluation.               1
                                                                 The term “ontology” is used inconsistently in the liter-
Two formulas φ and φ′ may disagree not only                ature: some work uses it to mean what we call a labelled
in logical structure but also in what the symbols          signature (Brunello et al., 2026b), while knowledge represen-
they use are intended to mean. Without fixing              tation and ontology learning more commonly use it to include
                                                           axioms as well (Armary et al., 2025; Du et al., 2024). We
the intended meanings, the problem of comparing            adopt the broader usage, and refer explicitly to the labelled
formalizations—or judging whether any single one           signature or the theory when the distinction matters.
                        
PassedSomeExam(x) , φ3 = ∀x Student(x) →               knowledge given as input, which may include, e.g.,
∃y ∃g (Exam(y)∧Grade(x, y, g)∧Sufficient(g)) .          contextual information or a (partial) specification
   From a formal perspective, these are not syntac-     of an ontology Ω̃ = ⟨σ̃, L̃, T̃ ⟩.
tic variants: each relies on a different signature,        FOL-autoformalization is the task of automati-
labeling, and potentially a different background        cally producing, from ⟨p, K⟩, a pair ⟨φ, Ω⟩, with
theory (see Figure 1). Formula φ1 represents pass-      Ω = ⟨σ, L, T ⟩, where L and T may possibly be
ing as a binary relation between individuals; φ2        empty, i.e., left implicit. Specifically, φ is a FOL
absorbs both the exam and the passing event into        formula over σ that represents the content of p rel-
a single unary predicate; φ3 introduces grades as       ative to Ω: under the meanings assigned by L and
a refined object. Crucially, the choice of signature    the constraints imposed by T , φ holds if and only
is not merely a matter of style: it determines both     if p is true.
what can be represented about the NL sentence
p′ and what can subsequently be inferred from its          The components of Ω may be given as output or
formalization. For instance, φ2 cannot adequately       left implicit. The signature σ is always recoverable
represent information about which exam a student        from φ itself. The labelling function L, when omit-
passed, since the exam is not represented as an indi-   ted, leaves the intended NL meaning of the symbols
vidual but is compiled away inside the unary predi-     in σ implicit: the grounding of the formula to nat-
cate; similarly, neither φ1 nor φ2 can represent in-    ural language must then be inferred from context.
formation about a student’s grade, since grades are     Similarly, the background theory T , when omitted,
absent from their signatures entirely. These are not    imposes no additional constraints on the interpre-
failures of translation but direct consequences of      tation of σ, potentially leaving the semantics of φ
the ontological commitments each formula adopts.        underspecified. The richer the specification of Ω,
                                                        the more verifiable the output φ becomes.
   In the absence of further information, there is
no principled reason to prefer one signature over          Definition 1 is deliberately general: different
another; however, these differing ontological com-      task variants arise by varying what K is and which
mitments make some formalizations more suitable         components of Ω are required to be explicit. Two
than others depending on the context in which they      extremes are worth noting. At one end, raw trans-
will be used. For instance, if p′ is expected to be     lation—the most common variant in the literature—
only one sentence within a larger corpus concern-       doesn’t consider Ω̃ in K and requires only φ as
ing different kinds of exams, the ontology under-       output, leaving L and T implicit. At the other
lying φ2 is likely inadequate, since it conflates the   end, full autoformalization requires producing both
concept of an exam with the act of a student pass-      φ and the complete Ω, and is the most theoreti-
ing it; a signature in which the exam is reified as     cally complete instantiation of the definition. The
an independent object would be preferable. Like-        strength of this definition lies precisely in its abil-
wise, if other sentences in the corpus explicitly       ity to capture both extremes—and everything in
discuss grades, the ontology underlying φ3 is the       between—within a single unified framework.
best-suited of the three considered here, since it is      Another variant present in the literature (see
the only one capable of representing and reasoning      Brunello et al. (2026b)) is the Logical Translation
about that information at all.                          (LT), where the input context K contains an on-
   This observation implies that evaluating aut-        tology Ω = ⟨σ, L⟩, and the output is the formula
oformalization systems by comparing formulas            φ (and the same Ω provided in input). LT is rele-
directly—without accounting for the ontologies          vant when a domain ontology already exists and
they presuppose—conflates two distinct sources          the goal is to produce formalizations compatible
of disagreement: different translations of the same     with it. This frequently occurs in formal verifica-
NL content, and different ontological choices about     tion pipelines or multi-sentence corpora requiring
how to represent that content at all.                   consistent predicate use across formulas.
                                                           Furthermore, LT is important since it provides a
2.4   FOL-autoformalization Definition                  useful decomposition of the full autoformalization
                                                        task, as noted in (Brunello et al., 2026b). Since LT
We provide now a precise definition of the task.
                                                        assumes Ω, they propose to consider the comple-
Definition 1 (FOL-autoformalization task) Let           mentary task of Ontology Extraction (OE): given
p be a NL text, and let K be optional background        contextual information and the NL text p, the goal
                                             p′ = “Every student
                                             passed some exam.”

                                                                                  φ3 : ∀x (Student(x) →
                                                                                  ∃y ∃g (Exam(y)∧
    φ1 : ∀x (Student(x) →               φ2 : ∀x (Student(x) →                       Grade(x, y, g) ∧
    ∃y (Exam(y) ∧ Passed(x, y)))        PassedSomeExam(x))                        Sufficient(g)))
    Signature: Student(x),              Signature: Student(x), Passed-           Signature: Student(x),
    Exam(x), Passed(x,y)                SomeExam(x)                              Exam(x), Grade(x,y,z), Suf-
    Labelling: “x is a student”, “x     Labelling: “x is a student”, “x          ficient(x)
    is an exam”, “x passed y”           passed some exam”                        Labelling: “x is a student”, “x
                                                                                 is an exam”, “x scores z in y”,
                                                                                 “x is sufficient”

Figure 1: A single NL sentence p′ admits multiple formalizations φ1 , φ2 , φ3 , each committing to a different
signature. The three formulas can be considered all correct but they express information differently.


is to construct the specific ontology Ω required to      with the field of ontology learning and common-
formalize p adequately. OE becomes the critical          sense knowledge acquisition (Armary et al., 2025;
subtask whenever a reusable ontology must be es-         Du et al., 2024), which have their own methods and
tablished before LT can proceed. For instance, it is     evaluation frameworks. Accordingly, we focus on
needed when bootstrapping a domain vocabulary            the evaluation of FOL formulas: this can be done
from a set of NL documents (legal texts, engineer-       either directly or via proxy tasks.
ing specifications) that will later serve as the basis
for formalizing arbitrary sentences in that domain.      Evaluation via Proxy Tasks. A fundamental
   This decomposition is not the only possible one,      challenge is the cost of obtaining ground-truth for-
but it gives dignity to the distinct nature of these     mulas: correct FOL annotations require significant
subtasks, the separate sources of error they intro-      expertise, making large-scale direct evaluation of-
duce, and the different communities whose meth-          ten prohibitive. Proxy tasks offer a practical alterna-
ods are relevant to each (Ontology Learning and          tive, measuring whether the formalization succeeds
Autoformalization). As we discuss in Section 3.2,        at a downstream application rather than against a
it also enables theoretically grounded evaluation.       ground truth. Any application can serve this role,
                                                         provided formalization success is clearly reflected
3     Autoformalization Evaluation                       in the overall outcome; for example, Lalwani et al.
                                                         (2024) use formalization for logical fallacy detec-
Here we explore the datasets and metrics used in
                                                         tion, while Karia et al. (2024) formalize a NL sen-
the literature for evaluation, deferring their use in
                                                         tence back from a FOL formula and checks equiva-
performance-enhancement methods to Section 4.
                                                         lence with the original.
Ontology Evaluation. In principle, evaluation               In practice, though, most of the literature uses
should assess both the quality of the ontology           Natural Language Inference (NLI) task as a proxy.
and that of the resulting FOL formula. In prac-          In NLI, given premises p1 , . . . , pn and a conclu-
tice, no existing work explicitly evaluates signature    sion c, the task is to determine whether c is logi-
quality, even when the OE/LT decomposition is            cally entailed by the premises. This entailment re-
acknowledged—a gap shared with ontology learn-           lation should be preserved under formalization: if
ing, where evaluation is also conducted indirectly       p1 , . . . , pn , c are formalized as φ1 , . . . , φn , ψ, then
via downstream tasks (Du et al., 2024). In FOL-          c is entailed by (resp., contradicts) the premises
autoformalization, signature quality is therefore        p1 , . . . , pn if and only if ψ (resp., ¬ψ) is derivable
assessed only implicitly: a correct formula is taken     from the premises φ1 , . . . , φn . This methodology
as evidence that the employed symbols constitute         has well-known limitations (Brunello et al., 2026b):
an adequate signature. Similarly for the theory, that    entailment agreement between NL and FOL can oc-
is considered by only a small portion of the FOL-        cur even with incorrect formulas; a mismatch can
autoformalization literature (Lalwani et al., 2024;      arise from any subset of incorrectly formalized sen-
Callewaert et al., 2025), and substantially overlaps     tences; and NL entailment may rely on background
                     Generation Type                            first-order theorem prover is used to check whether
 Dataset                                       No. of Pairs
                   NL            FOL
 FOLIO           Human        Human (*)          ∼3800
                                                                the entailments are preserved by the FOL formal-
 GGC             Human        Human (*)          ∼280           ization, filtering out the instances in which a mis-
 MALLS            LLM            LLM             ∼28K           match occurs. GGC collects students’ FOL submis-
 ProverQA        LLM (*)      Rule-based         ∼17K           sions in response to Tarski’s World exercises from
 Willow           LLM            LLM             ∼16K
 PROOFFOL        Human         LLM (*)           ∼10K
                                                                the textbook Language, Proof and Logic (Barker-
 Text2log       Rule-based Rule-based (*)        ∼100K          Plummer et al., 2011b), labelled using an automatic
                                                                grading tool that enforces syntactic and semantic
Table 1: Overview of NL–FOL datasets. ‘Generation               coherence.
Type’ indicates who generates NL and FOL. Asterisks
                                                                   LLM generation underlies Willow, MALLS,
denote that the output is obtained by a translation (from
the NL or the FOL part); no asterisk indicates joint            PROOFFOL, and the NL side of ProverQA. Willow
generation.                                                     extends ∼ 300 human-validated NL–FOL pairs to
                                                                16K using GPT-4, discarding outputs that fail a
                                                                grammar check; NL–FOL alignment is only par-
knowledge not captured by the formalization.2                   tially verified. MALLS collects 28K NL–FOL
   We focus on direct evaluation here, and refer                pairs by prompting GPT-4 to generate NL sen-
the reader to Madaan et al. (2025) for a dedicated              tences and then to formalize them using a dynamic
treatment of the NLI setting.                                   n-gram counter to encourage diversity. In addition,
                                                                a human-checked subset of 1K examples is used
3.1   Datasets                                                  to identify frequent errors, which are then targeted
We review how existing datasets pairing a NL sen-               by rule-based filters to remove such mistakes from
tence to a FOL formula (NL–FOL) are constructed                 the remaining dataset. PROOFFOL uses GPT-4o
and validated. We discuss FOLIO (Han et al.,                    to formalize the premises and conclusions of
2024), Willow (Deveci, 2024), MALLS (Yang                       ProofWriter (Tafjord et al., 2021), retaining only in-
et al., 2024), ProverQA (Qi et al., 2025), PROOF-               stances where the theorem prover’s verdict matches
FOL (Thatikonda et al., 2024), Text2log (Lev-                   the source dataset’s ground truth, thereby enforcing
kovskyi and Li, 2021), and the private (but available           both syntactic well-formedness and label consis-
on request) Grade Grinder Corpus (GGC) (Barker-                 tency. ProverQA inverts the direction: an LLM gen-
Plummer et al., 2011a). A high-level summary is                 erates NL stories with human-interpretable mean-
provided in Table 1. Purely NLI datasets without                ings for predicate symbols, while the FOL side is
a validated FOL layer are excluded from the main                produced by a symbolic generator, guaranteeing
body of the paper, as they are not directly usable for          logical structure by construction.
autoformalization evaluation. Further information                  Rule-based generation appears in Text2log and
about these datasets, and what would need to be                 in the symbolic part of ProverQA and, in both
supplied to make them usable for the autoformal-                cases, most validation is intrinsic to the generator.
ization task, is provided in Appendix B.                        Text2log uses predefined grammar rules (through
                                                                an ad hoc CCG-based semantic parser) to formal-
Generation and validation methods. Three                        ize in FOL template-based NL sentences, creating
main generation paradigms recur across the consid-              roughly 100K NL–FOL pairs. FOL is correct by
ered datasets, often in combination: human gener-               construction, but the range of covered NL instances
ation, LLM generation, and rule-based generation.               is limited and strongly template-driven.
Despite some of the procedures provide a degree of
validation per se (e.g., human generation), they are            Discussion. The generation and validation
sometimes complemented with additional checks.                  choices have direct implications on how each
   Human generation is used for FOLIO and for                   dataset should be used in autoformalization.
the GGC corpus. FOLIO is a NLI dataset con-                        Datasets with expert-written NL and FOL pairs
sisting of ∼ 500 different stories with a total of              plus solver-based checks, such as FOLIO and the
∼ 2400 premises and ∼ 1400 conclusions, written                 GGC corpus, provide the strongest available ba-
in NL and then formalized to FOL by experts. A                  sis for evaluation. Despite the human-conducted
   2
                                                                generation and the solver-based label-consistency
     Some limitations can be mitigated by generating multiple
conclusions depending on different premise subsets, or by       tests, several independent analyses (Pei et al., 2025;
using datasets that do not require background knowledge.        Yang et al., 2024; Brunello et al., 2026b) document
the presence of annotation errors in FOLIO. In par-             LogicSim(φ, φ̂) := pd + tp + ld + IoU ,
ticular, Brunello et al. (2026a) found a high rate              where pd and tp are the absolute differences
of ambiguous and incorrect formalizations in the                in the number of distinct predicates and total
validation split of FOLIO and in a subset of the                predicate occurrences, respectively; ld is the
MALLS test set; the authors show that these anno-               difference in logical operators and quantifiers;
tation errors can substantially skew reported model             and IoU measures the overlap between the
performance, and consequently released corrected                predicate sets of φ and φ̂.
versions of these datasets for use in evaluating mod-
els on this task.                                         While easy to compute, syntactic metrics ignore
   Large-scale LLM-generated datasets typically         the semantic content of FOL formulas, yielding
guarantee syntactic well-formedness but do not          inadequate results (Brunello et al., 2026b). Thus,
explicitly validate NL–FOL semantic alignment.          they are often neglected, or used alongside more
Systematic error patterns consequently persist, as      semantically informed measures, described next.
acknowledged by the authors of MALLS and Wil-           3.2.2 Semantic Metrics
low and further documented in Brunello et al.
                                                        Semantic metrics evaluate whether a candidate for-
(2026b). A similar consideration applies to rule-
                                                        mula φ and a reference φ̂ convey the same meaning.
based datasets like Text2log, where template-
                                                        Direct semantic comparison requires addressing
driven NL may not reflect the linguistic variation
                                                        two dimensions in sequence.
encountered in realistic settings.
                                                        Symbol Matching. Before any semantic compar-
3.2   Metrics                                           ison can be made, the symbols of φ must be linked
Direct evaluation of FOL formalization focuses on       to those of φ̂—an instance of the anchoring prob-
comparing a predicted formula φ̂ with a ground          lem (Harnad, 1999). Two strategies appear in the
truth formula φ. We categorize the metrics pro-         literature. The first is syntactic matching: Vossel
posed in the literature into syntactic and semantic,    et al. (2025) use Levenshtein distance (Levenshtein,
based on which aspects of the formulas they assess.     1965) to align predicate symbols across signatures
                                                        by surface-form similarity, a fragile approach that
3.2.1 Syntactic Metrics
                                                        fails when synonymous concepts receive different
By syntactic metrics, we refer to metrics that treat    names or distinct concepts share one. The second
formulas as syntactic objects, ignoring semantic        strategy is to provide the signature directly as part
meaning. A preliminary syntactic validity check         of the task input, as in the LT variants. This elim-
ensures that the generated formula conforms to the      inates the matching problem by construction and
rules of the formalism; once correctness is verified,   is one of the strongest motivations for the OE/LT
several approaches can be applied:                      distinction of Section 2.
   • Exact Match evaluates whether two formulas         Formula Closeness. Once symbol matching is
     are identical under string comparison, typi-       established, the question is how to measure the
     cally after normalization preprocessing (Vos-      semantic distance between the two formulas. In the
     sel et al., 2025).                                 literature, we can find two metrics.
   • In Tree Edit Distance, instead, formulas are          Logical equivalence assigns 1 if and only if φ ≡
     represented as syntax trees, and the minimum-      φ̂, 0 otherwise: it is theoretically well-founded
     cost sequence of node edit operations to trans-    but binary, thus unsuitable as a possible training
     form one into the other is computed (Brunello      objective (see Section 4.1).
     et al., 2024).                                        LE score (Yang et al., 2024) relaxes this by treat-
                                                        ing the formulas propositionally (Smullyan, 1968)
   • BLEU Score (Papineni et al., 2002), the stan-      and computing the ratio of truth assignments un-
     dard NLP metric, can be applied to FOL for-        der which they agree, yielding a continuous value
     mulas after tokenization with an ad-hoc tok-       in [0, 1]. However, by treating formulas proposi-
     enizer tailored for FOL syntax (Yang et al.,       tionally it discards quantifier structure entirely—
     2024).                                             precisely what is believed to be the aspect of FOL
                                                        most challenging to produce correctly.3
   • LogicSim is a metric proposed by
                                                           3
     Lopez-Ponce and Bel-Enguix (2025) as                      More precisely, in the original formulation (Yang et al.,
   Almost all works implicitly target the raw trans-             from purely human-annotated corpora to large-
lation variant, treating autoformalization as a single           scale synthetic resources.
monolithic step, an approach that has a direct im-
pact on evaluation. Conflicting empirical results in             Supervised Fine-tuning (SFT). The most com-
the literature—some works reporting strong LLM                   mon strategy updates all model weights, or a subset
performance on NL–FOL translation (Yang et al.,                  of them via methods such as Low-Rank Adaptation,
2024), others reporting poor performance (Han                    using supervised NL–FOL training pairs. Since ef-
et al., 2024)—can be traced to heterogeneous eval-               fective fine-tuning requires a substantial amount
uation setups arising from different implicit task               of data, most works rely on existing benchmarks.
formulations (Brunello et al., 2026b). The decom-                For example, Vossel et al. (2025) combine MALLS
position introduced in Section 2 addresses these in-             and Willow to increase diversity and reduce overfit-
consistencies and, together with the metric consid-              ting, while Xu et al. (2024) augment data through
erations above, motivates a clear recommendation:                systematic symbol renaming and NL instructions
when direct semantic comparison is needed, since                 to promote semantic learning over surface memo-
reliable methods for symbol matching across differ-              rization. When existing datasets are insufficient, ad
ent signatures are currently lacking, the labelled sig-          hoc datasets can be constructed synthetically. For
nature should be provided as input—resolving sym-                instance, Hahn et al. (2022) employ a rule-based
bol matching by construction—and logical equiva-                 pipeline combining established symbolic parsing
lence used as the sole evaluation metric.                        techniques (Clark and Curran, 2004; Bos, 2015) to
                                                                 convert NL sentences into FOL formulas at scale.
4     LLM-based Autoformalization Methods
Since current LLMs can be readily prompted to                    Reinforcement Learning (RL). Some authors
perform FOL-autoformalization, the research has                  adopt RL in place of, or in addition to, supervised
largely focused on techniques for enhancing their                fine-tuning. Yang et al. (2024) train LogicLLAMA
performance. A major distinction can be made be-                 using a combination of the BLEU score and the LE
tween methods that fine-tune the LLM (Section 4.1)               score (Section 3.2) as a reward function measuring
and those that aim to improve performance without                similarity between the candidate translation φ̂ and
modifying the model’s internal weights, instead                  the ground truth φ, motivated by the observation
relying on prompting strategies (Section 4.2) or                 that a purely autoregressive fine-tuning objective
incorporating a verification stage (Section 4.3).                did not yield optimal performance.
   Virtually all methods in the FOL-
autoformalization literature implicitly target                   Preference Optimization. Motivated by strong
raw translation (p → φ), and OE-specific methods                 results in other generative settings, preference opti-
are largely absent from the literature. As discussed             mization methods have also been explored. Lopez-
in Section 3.2, no metrics are developed for direct              Ponce and Bel-Enguix (2025) propose a Direct
evaluation of a labelled signature’s quality, making             Preference Optimization (DPO) procedure start-
it difficult to optimize or compare OE methods in                ing from FOLIO, where accepted options corre-
isolation. This represents a structural gap that we              spond to ground-truth formalizations and rejected
discuss further in Section 5.                                    options to LLM-generated alternatives, augmented
                                                                 with quality scores encoding preference strength.4
4.1    Fine-tuning Strategies                                    Viswanadha et al. (2025) further study DPO and
                                                                 KTO (Kahneman–Tversky Optimization), finding
Fine-tuning consists of taking a pre-trained model
                                                                 that KTO after SFT outperforms both SFT alone
that already encodes broad linguistic and world
                                                                 and SFT with DPO.
knowledge and specializing it on a task-specific
dataset. Various techniques can be applied, ranging
from full-parameter updates to parameter-efficient               4.2      Prompting Strategies
approaches such as Low-Rank Adaptation, and                      Multiple prompting strategies have been explored
2024), symbol matching is not performed independently from       to enhance the capabilities of pre-trained LLMs in
formula closeness estimation: the authors select the predicate   autoformalization without modifying their weights.
matching that maximises the LE score itself. This conflates
the two dimensions and introduces additional shortcomings
                                                                    4
discussed in (Brunello et al., 2026b).                                  The scores derivation procedure is not fully specified.
4.2.1    Agnostic Methods                                 errors and fixes (Pan et al., 2023; Callewaert et al.,
In the autoformalization setting, general-purpose         2025). The loop repeats until a valid formula is
prompting techniques such as Few-Shot prompt-             produced or an iteration limit is reached.
ing, In-Context Learning (ICL), Chain-of-Thought             A complementary approach constrains decoding
(CoT), Tree-of-Thoughts, and Self-Consistency are         itself, restricting the output vocabulary at each step
commonly used and typically yield performance             to tokens that yield a grammatically valid continua-
gains, as shown for instance by Han et al. (2024).        tion (Raspanti et al., 2025).

4.2.2    Task-specific Methods                            4.3.2   Semantic Verification
Prompting can also be tailored with task-specific         Semantic verification is an open challenge. Assess-
instructions (meta-prompting): rather than asking         ing whether a FOL formula faithfully captures the
the model to produce a formula directly, the prompt       meaning of a NL sentence requires bridging two
decomposes the task into explicit stages. For exam-       fundamentally different representations, which lies
ple, Pei et al. (2025); Hu et al. (2025) first instruct   beyond the reach of standard theorem provers. Still,
the model to identify a suitable labelled signature       formal tools can provide partial semantic feedback:
(i.e., perform OE) and then carry out the LT step.        when autoformalizing a corpus of NL sentences
This staged decomposition is precisely the opera-         into a set of axioms (Callewaert et al., 2025), satis-
tionalization of the OE/LT distinction, discussed         fiability checks can reveal theory-level inconsisten-
above. Some works further interpose a theory re-          cies, and unsatisfiable core extraction can pinpoint
covery step: Lalwani et al. (2024); Nananukul et al.      offending formulas to guide refinement.
(2025); Wen et al. (2025) ask the LLM to select              For richer semantic feedback, several works turn
among candidate relational axioms before perform-         to LLMs themselves. One line of work gener-
ing translation. Ryu et al. (2025) decompose the          ates multiple candidate formalizations and aggre-
formalization into extracting the logical structure       gates them via self-consistency and majority voting.
of the sentence, splitting it into simpler compo-         Olausson et al. (2023) find that aggregating multi-
nents, and performing a sequential translation from       ple generations reduces syntactic errors, especially
subcomponents to the full formula.                        for weaker models, and Brunello et al. (2026b) ob-
   Beyond such decompositions, ICL-style meth-            serve complementary error patterns across model
ods are also adapted. Hu et al. (2025) use retrieval-     families, motivating ensembling strategies.
augmented generation (RAG): a knowledge base                 A second line of work prompts an LLM to
of NL–FOL pairs is built from existing datasets           directly refine a candidate formalization, like in
and enriched with instances where the model previ-        Brunello et al. (2026a). To mitigate the fallibility of
ously failed. Given an input sentence p, the closest      LLM judges, several strategies have been explored:
examples in the knowledge base (according to sen-         augmenting the context with a knowledge base of
tence embeddings) are retrieved and inserted into         NL–FOL pairs including human-corrected formal-
the prompt as contextual demonstrations.                  izations (Hu et al., 2025); prompting the model
                                                          to compare two candidates and select the better
4.3     Output Verification and Refinement Loops          one (Kirtania et al., 2024); and fine-tuning a ded-
Feedback-based methods iteratively refine an              icated verification model on triplets (p, φpert , φ),
LLM’s output after an initial formalization attempt.      where p is the NL sentence, φpert an incorrect
The verification step may rely on formal tools or         (perturbed) formalization, and φ is the ground
on the LLM itself, to target either syntactic or se-      truth (Thatikonda et al., 2024).
mantic correctness.                                          Finally, some approaches combine LLM judg-
                                                          ment with formal verification. Ryu et al. (2025)
4.3.1    Syntactic Verification                           iteratively compare pairs of candidate formaliza-
The most widely adopted form of verification              tions (φ, φ′ ): if they are logically equivalent, one
checks whether the generated formula conforms             is selected arbitrarily; otherwise an SMT-generated
to the target formalization via a syntax checker or       counterexample is passed to the LLM to discrimi-
theorem prover. Error messages are fed back into          nate between them. Amrollahi et al. (2026) intro-
the prompt to localize and correct mistakes (Deng         duce a roundtrip framework where an SMT solver
et al., 2024; Quan et al., 2024); some works further      checks equivalence between a formalization and
augment the prompt with a curated list of common          its back-translation, and an LLM judge diagnoses
mismatches to guide targeted repair.                     2025); analogous strategies for FOL remain prelim-
                                                         inary (Frydman, 2025). A closer exchange of ideas
Discussions and takeaways. Drawing strong
                                                         across formalisms—covering intermediates, post-
conclusions aimed at answering "Which is the cur-
                                                         training strategies, and multi-step pipelines—could
rent best approach to FOL-autoformalization?" is
                                                         substantially advance the field. At the methodologi-
difficult for two compounding reasons: the absence
                                                         cal level, almost no existing work explicitly targets
of standardized evaluation protocols (and task defi-
                                                         OE as a standalone task; developing fine-tuning ob-
nition) makes cross-paper comparisons difficult to
                                                         jectives and prompting strategies that adhere to the
achieve, and the annotation noise documented in
                                                         OE/LT decomposition, and engaging more directly
commonly used benchmarks (Section 3.1) further
                                                         with the ontology learning literature (Armary et al.,
limits the significance of performance differences
                                                         2025; Du et al., 2024), represents a largely open
witnessed when using different solutions.
                                                         research agenda.
   What is reasonable to conclude is that frontier
reasoning models with simple CoT achieve strong          Towards end-to-end applications. The connec-
results on the LT task (Brunello et al., 2026b); fine-   tion between autoformalization research and down-
tuning smaller models on specific datasets is a vi-      stream applications—formal verification, legal rea-
able approach to achieve SOTA performance in a           soning, AI safety—remains largely implicit. End-
specific context and with less computation (and          to-end pipelines that reliably formalize corpora of
time) at inference phase. On top of that, prompt-        NL specifications are almost entirely absent. Clos-
ing techniques (like meta-prompting, decomposing         ing this gap is a crucial next step, allowing concrete
complex sentences into simpler subcomponents,            application requirements to steer the future direc-
or RAG) can boost the performance of fine-tuned          tion of the research field.
models or already capable ones. Finally, adding a
verification layer on top of any pipeline seems ben-     Limitations
eficial as well. While syntactic verification repre-
sents a robust enhancement across model families,        This survey does not provide a comparative em-
semantic verification addresses a genuinely differ-      pirical analysis across enhancement strategies or
ent and harder problem, making it essential for reli-    across LLMs. This is partly by design: as dis-
able autoformalization in practice. SAT solvers of-      cussed throughout, the absence of standardized
fer rigorous but partial feedback (Callewaert et al.,    evaluation protocols makes cross-paper compar-
2025; Amrollahi et al., 2026), while LLM-based           isons unreliable, and one contribution of this work
verification can cover the full semantic dimension       is precisely to clarify the conceptual distinctions—
but lacks formal guarantees and depends heavily          most notably the OE/LT decomposition—that such
on model capability.                                     a standardization would require. By focusing on
                                                         LLM-based methods, we also set aside earlier sym-
5   Open Problems and Future Directions                  bolic and neural approaches, which are only briefly
                                                         contextualized in the introduction. Although the
We conclude by highlighting open issues in current       surveyed literature evolves rapidly and specific re-
research and outlining directions for future work.       sults may become outdated, we believe that the
On evaluation protocols and benchmarks.                  contributions of this work are largely independent
Many evaluation pipelines conflate distinct stages       of the specific models and datasets available at any
of autoformalization—OE and LT—making it dif-            given time, and thus retain their value as the land-
ficult to identify where models struggle. We advo-       scape continues to develop.
cate for standardized evaluation protocols along-
side larger, higher-quality benchmarks that are
                                                         References
more heterogeneous in domain, formula complex-
ity, and linguistic variation. These benchmarks          Mohammad Nazmul Alam, Md. Shahin Kabir, and
must also capture overlooked challenges like natu-        Arun Verma. 2023. Data and knowledge engineering
                                                          for legal precedents using first-order predicate logic.
ral language ambiguity.                                   GCAT 2023, pages 1–8.
On autoformalization methods. A work on LTL              Daneshvar Amrollahi, Jerry Lopez, and Clark Barrett.
autoformalization has begun to explore structured          2026. Faithful Autoformalization via Roundtrip Ver-
intermediate representations (Germiniani et al.,           ification and Repair. CoRR.
Pauline Armary, Cheikh Brahim El-Vaigh, Ouassila Lab-      Stephen Clark and James R. Curran. 2004. Parsing
  bani Narsis, and Christophe Nicolle. 2025. Ontology         the WSJ using CCG and log-linear models. In ACL
  learning towards expressiveness: A survey. Com-            2004, pages 103–110. Association for Computational
  puter Science Review, 56:100693.                            Linguistics.

Dave Barker-Plummer, Richard Cox, and Robert Dale.         David Dalrymple, Joar Skalse, Yoshua Bengio, Stuart
  2011a. Student translations of natural language into       Russell, and 1 others. 2024. Towards guaranteed safe
  logic: The Grade Grinder corpus release 1.0. In            AI: A framework for ensuring robust and reliable AI
  EDM, pages 51–60.                                          systems. CoRR, abs/2405.06624.

David Barker-Plummer, Jon Barwise, and John                Shujie Deng, Honghua Dong, and Xujie Si. 2024. En-
  Etchemendy. 2011b. Language, Proof, and Logic,             hancing and evaluating logical reasoning abilities of
  2nd edition. Center for the Study of Language and          large language models. In ICLR 2024 Workshop on
  Information/SRI.                                           Secure and Trustworthy Large Language Models.

                                                           İbrahim Ethem Deveci. 2024. Transformer models for
Clark Barrett and Cesare Tinelli. 2018. Satisfiability
                                                               translating natural language sentences into formal
  Modulo Theories. In Edmund M. Clarke, Thomas A.
                                                               logical expressions. Master’s thesis, Middle East
  Henzinger, Helmut Veith, and Roderick Bloem, edi-
                                                               Technical University.
  tors, Handbook of Model Checking, pages 305–343.
  Springer International Publishing, Cham.                 Rick Du, Huilong An, Keyu Wang, and Weidong Liu.
                                                             2024. A short review for ontology learning from text:
Alexander Beiser, Nysret Musliu, and David Penz. 2025.       Stride from shallow learning, deep learning to large
  Intermediate languages matter: Formal languages            language models trend. CoRR, abs/2404.14991.
  and LLMs affect neurosymbolic reasoning. In SE-
  MANTiCS 2025, volume 4064 of CEUR Workshop               Francis Frydman. 2025. EXa-LM: A controlled natural
  Proceedings. CEUR-WS.org.                                  language bridge between large language models and
                                                             first-order logic solvers. Preprints.
Johan Bos. 2015. Open-domain semantic parsing with
  boxer. In NODALIDA 2015, May 11-13, 2015, vol-           Samuele Germiniani, Daniele Nicoletti, and Graziano
  ume 109 of Linköping Electronic Conference Pro-            Pravadelli. 2025. A systematic literature review on
  ceedings, pages 301–304. Linköping University Elec-        mining LTL specifications. IEEE Access, 13:48950–
  tronic Press / Association for Computational Linguis-      48998.
  tics.
                                                           Christopher Hahn, Frederik Schmitt, Julia J. Tillman,
Andrea Brunello, Cristian Curaba, Luca Geatti, Michele       Niklas Metzger, Julian Siber, and Bernd Finkbeiner.
  Mignani, Angelo Montanari, and Nicola Sacco-               2022. Formal specifications from natural language.
  manno. 2026a. Fixing folio and malls: Ver-                 CoRR, abs/2206.01962.
  ified annotations and an LLM-assisted frame-
  work to focus human relabeling.             Preprint,    Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhent-
  arXiv:https://arxiv.org/abs/2606.02837. To appear          ing Qi, Martin Riddell, Wenfei Zhou, James Coady,
  at EMNLP 2026.                                             David Peng, Yujie Qiao, Luke Benson, Lucy Sun,
                                                             Alexander Wardle-Solano, Hannah Szabó, Ekaterina
Andrea Brunello, Riccardo Ferrarese, Luca Geatti, En-        Zubova, Matthew Burtell, Jonathan Fan, Yixin Liu,
  rico Marzano, Angelo Montanari, and Nicola Sac-            Brian Wong, Malcolm Sailor, and 16 others. 2024.
  comanno. 2024. Evaluating LLMs capabilities at             FOLIO: natural language reasoning with first-order
  natural language to logic translation: A preliminary       logic. In EMNLP 2024, pages 22017–22031. Associ-
  investigation. In OVERLAY 2024, volume 3904                ation for Computational Linguistics.
  of CEUR Workshop Proceedings, pages 103–110.
                                                           Stevan Harnad. 1999. The symbol grounding problem.
  CEUR-WS.org.
                                                              CoRR, cs.AI/9906002.
Andrea Brunello, Luca Geatti, Michele Mignani, An-         Ruikang Hu, Shaoyu Lin, Yeliang Xiu, and Yongmei
  gelo Montanari, and Nicola Saccomanno. 2026b. Do           Liu. 2025. LTRAG: enhancing autoformalization and
  LLMs really struggle at NL-FOL translation? reveal-        self-refinement for logical reasoning with thought-
  ing their strengths via a novel benchmarking strategy.     guided RAG. In ACL 2025, pages 2483–2493. Asso-
  In AAAI 2026, pages 30094–30103. AAAI Press.               ciation for Computational Linguistics.
Benjamin Callewaert, Simon Vandevelde, and Joost           Peng Jiang and Xiaodong Cai. 2024. A survey of se-
  Vennekens. 2025. VERUS-LM: a versatile frame-              mantic parsing techniques. Symmetry, 16(9):1201.
  work for combining LLMs with symbolic reasoning.
  CoRR, abs/2501.14540.                                    Er Jin, Qihui Feng, Yongli Mou, Gerhard Lake-
                                                             meyer, Stefan Decker, Oliver Simons, and Johannes
Peter Clark, Oyvind Tafjord, and Kyle Richardson. 2020.      Stegmaier. 2025. LogicAD: Explainable anomaly
  Transformers as soft reasoners over language. In           detection via VLM-based text feature extraction. In
  IJCAI 2020.                                                AAAI 2025, pages 4129–4137. AAAI Press.
Aishwarya Kamath and Rajarshi Das. 2018.   A                Ali Mohammadjafari, Anthony S. Maida, and Raju Got-
  survey on semantic parsing.  arXiv preprint                 tumukkala. 2024. From natural language to SQL:
  arXiv:1812.00978.                                           review of LLM-based text-to-SQL systems. CoRR,
                                                              abs/2410.01066.
Rushang Karia, Daniel Bramblett, Daksh Dobhal, Pulkit
  Verma, and Siddharth Srivastava. 2024. ∀uto∃val:          Terufumi Morishita, Gaku Morio, Atsuki Yamaguchi,
  Autonomous assessment of LLMs in formal synthesis           and Yasuhiro Sogawa. 2024. Enhancing reasoning
  and interpretation tasks. Preprint, arXiv:2403.18327.       capabilities of LLMs via principled synthetic logic
                                                              corpus. ArXiv, abs/2411.12498.
Shashank Kirtania, Priyanshu Gupta, and Arjun
  Radhakirshna. 2024. LOGIC-LM++: multi-step
                                                            Navapat Nananukul, Yue Zhang, Ryan Lee, Eric Boxer,
  refinement for symbolic formulations. CoRR,
                                                              Jonathan May, Vibhav Giridhar Gogate, Jay Pu-
  abs/2407.02514.
                                                              jara, and Mayank Kejriwal. 2025. Logicalthought:
Tobias Kuhn. 2014. A survey and classification of con-        Logic-based ontological grounding of LLMs for high-
  trolled natural languages. Computational linguistics,       assurance reasoning. CoRR, abs/2510.01530.
  40(1):121–170.
                                                            Theo Olausson, Alex Gu, Benjamin Lipkin, Cedegao E.
Abhinav Lalwani, Tasha Kim, Lovish Chopra, Christo-           Zhang, Armando Solar-Lezama, Joshua B. Tenen-
  pher Hahn, Zhijing Jin, and Mrinmaya Sachan. 2024.          baum, and Roger Levy. 2023. LINC: A neurosym-
  Autoformalizing natural language to first-order logic:      bolic approach for logical reasoning by combining
  A case study in logical fallacy detection. arXiv            language models with first-order logic provers. In
  preprint arXiv:2405.02318.                                  EMNLP 2023, pages 5153–5176. Association for
                                                              Computational Linguistics.
Long Hei Matthew Lam, Ramya Keerthy Thatikonda,
  and Ehsan Shareghi. 2024. A closer look at tool-          Liangming Pan, Alon Albalak, Xinyi Wang, and
  based logical reasoning with LLMs: The choice of            William Yang Wang. 2023. Logic-LM: Empower-
  tool matters. In ALTA 2024, pages 41–63. Associa-           ing large language models with symbolic solvers for
  tion for Computational Linguistics.                         faithful logical reasoning. In Findings of the Associ-
                                                              ation for Computational Linguistics: EMNLP 2023,
Vladimir I. Levenshtein. 1965. Binary codes capable of
                                                              pages 3806–3824. Association for Computational
  correcting deletions, insertions, and reversals. Soviet
                                                              Linguistics.
  physics. Doklady, 10:707–710.
Oleksii Levkovskyi and Wei Li. 2021. Generating pred-       Kishore Papineni, Salim Roukos, Todd Ward, and Wei-
  icate logic expressions from natural language. In           Jing Zhu. 2002. Bleu: a method for automatic evalu-
  SoutheastCon 2021, pages 1–8.                               ation of machine translation. In Proceedings of the
                                                              40th annual meeting of the Association for Computa-
Jian Liu, Leyang Cui, Hanmeng Liu, Dandan Huang,              tional Linguistics, pages 311–318.
   Yile Wang, and Yue Zhang. 2020. Logiqa: A
   challenge dataset for machine reading compre-            Yu Pei, Yongping Du, and Xingnan Jin. 2025. Fover:
   hension with logical reasoning. arXiv preprint             First-order logic verification for natural language rea-
   arXiv:2007.08124.                                          soning. Trans. Assoc. Comput. Linguistics, 13:1340–
                                                              1359.
Junnan Liu. 2025. Few-shot natural language to first-
  order logic translation via code generation. In           Chengwen Qi, Ren Ma, Bowen Li, He Du, Binyuan Hui,
  NAACL 2025 - Volume 1, pages 10939–10960. Asso-             Jinwang Wu, Yuanjun Laili, and Conghui He. 2025.
  ciation for Computational Linguistics.                      Large language models meet symbolic provers for
                                                              logical reasoning evaluation. In ICLR 2025.
FernandoFrancisco Lopez-Ponce and Gemma Bel-
  Enguix. 2025. Into the limits of logic: Alignment
                                                            Xin Quan, Marco Valentino, Louise A. Dennis, and An-
  methods for formal logical reasoning. In MathNLP
                                                              dré Freitas. 2024. Verification and refinement of nat-
  2025, pages 112–123. Association for Computational
                                                              ural language explanations through LLM-symbolic
  Linguistics.
                                                              theorem proving. In EMNLP 2024, pages 2933–2958.
Lovish Madaan, David Esiobu, Pontus Stenetorp, Bar-           Association for Computational Linguistics.
  bara Plank, and Dieuwke Hupkes. 2025. Lost in
  inference: Rediscovering the role of natural language     Federico Raspanti, Tanir Ozcelebi, and Mike Holen-
  inference for large language models. In NAACL 2025          derski. 2025. Grammar-constrained decoding makes
  - Volume 1, pages 9229–9242. Association for Com-           large language models better logical parsers. In ACL
  putational Linguistics.                                     (Volume 6: Industry Track), pages 485–499. Associa-
                                                              tion for Computational Linguistics.
Agnieszka Mensfelt, David Tena Cucala, Santiago
  Franco, Angeliki Koutsoukou-Argyraki, Vince Trenc-        Hyun Ryu, Gyeongman Kim, Hyemin S. Lee, and
  senyi, and Kostas Stathis. 2026. Towards a common           Eunho Yang. 2025. Divide and translate: Composi-
  framework for autoformalization. In AAAI 2026,              tional first-order logic translation and verification for
  pages 40971–40980. AAAI Press.                              complex logical reasoning. In ICLR 2025.
Abulhair Saparov and He He. 2022. Language models          Yuan Yang, Siheng Xiong, Ali Payani, Ehsan Shareghi,
  are greedy reasoners: A systematic formal analysis         and Faramarz Fekri. 2024. Harnessing the power of
  of chain-of-thought. In ICLR 2022.                         large language models for natural language to first-
                                                             order logic translation. In ACL 2024, pages 6942–
Raymond Merrill Smullyan. 1968. First-Order Logic.           6959. Association for Computational Linguistics.
  Springer Verlag.
                                                           Xi Ye, Qiaochu Chen, Isil Dillig, and Greg Durrett.
Yang Sun, Guanrong Chen, Hamid Alinejad-Rokny,               2023. SatLM: Satisfiability-aided language models
  Jianzhu Bao, Yuqi Huang, Bin Liang, Kam-Fai Wong,          using declarative prompting. In NeurIPS 2023.
  Min Yang, and Ruifeng Xu. 2025. Learning first-
  order logic rules for argumentation mining. In ACL       Weihao Yu, Zihang Jiang, Yanfei Dong, and Jiashi Feng.
  (Volume 1: Long Papers), pages 14133–14148. Asso-          2020. ReClor: A reading comprehension dataset
  ciation for Computational Linguistics.                     requiring logical reasoning. In ICLR 2020.

Christian Szegedy. 2020. A promising path towards aut-     Wanjun Zhong, Siyuan Wang, Duyu Tang, Zenan Xu,
  oformalization and general artificial intelligence. In    Daya Guo, Jiahai Wang, Jian Yin, Ming Zhou, and
  CICM, volume 12236 of Lecture Notes in Computer           Nan Duan. 2021. AR-LSAT: investigating analytical
  Science, pages 3–20. Springer.                            reasoning of text. CoRR, abs/2104.06598.

Oyvind Tafjord, Bhavana Dalvi, and Peter Clark. 2021.      A      First-Order Logic
  ProofWriter: Generating implications, proofs, and
  abductive statements over natural language. In Find-     We provide here a brief introduction to First-Order
  ings of ACL-IJCNLP 2021, pages 3621–3634, Online.        Logic (FOL), covering the concepts needed to fol-
  Association for Computational Linguistics.               low the main article. Readers seeking a more
                                                           comprehensive treatment can consult standard text-
Ramya Keerthy Thatikonda, Jiuzhou Han, Wray L. Bun-
  tine, and Ehsan Shareghi. 2024. Strategies for im-       books such as (Smullyan, 1968).
  proving nl-to-fol translation with LLMs: Data genera-
  tion, incremental fine-tuning, and verification. CoRR,   A.1     Syntax
  abs/2409.16461.                                          Two key notions to understand FOL are those of
Jidong Tian, Yitian Li, Wenqing Chen, Liqiang Xiao,        signature and terms.
   Hao He, and Yaohui Jin. 2021. Diagnosing the first-     Definition 2 (Signature) A signature σ is a tuple
   order logical reasoning ability through LogicNLI.
                                                           (V, C, F, R) such that:
   In EMNLP 2021, pages 3738–3747. Association for
   Computational Linguistics.
                                                                • V is a (countably infinite) set of variables;
Koushik Viswanadha, Deepanway Ghosal, and Somak
  Aditya. 2025. LOGICPO: efficient translation of               • C is a set of constant symbols;
  nl-based logical problems to FOL using LLMs and
  preference optimization. CoRR, abs/2506.18383.                • F is a set of function symbols, each with its
                                                                  arity;
Felix Vossel, Till Mossakowski, and Björn Gehrke.
  2025. Advancing natural language formalization                • R is a set of relation/predicate symbols, each
  to first order logic with fine-tuned LLMs. CoRR,                with its arity;
  abs/2509.22338.
                                                           and V ∩ C ∩ F ∩ R = ∅.
Chengyao Wen, Qiang Cheng, Shaofei Wang, Zhizhen
  Liu, Deng Zhao, and Lei Liang. 2025. Logic-thinker:         The set of terms in FOL is defined inductively
  Teaching large language models to think more log-        as follows:
  ically. In Findings of EMNLP 2025, pages 12955–
  12969. Association for Computational Linguistics.            1. every variable in V and every constant in C is
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus N.              a term;
  Rabe, Charles Staats, Mateja Jamnik, and Christian
  Szegedy. 2022. Autoformalization with large lan-             2. if t1 , . . . , tn are terms and f ∈ F is a function
  guage models. In NeurIPS 2022.                                  symbol with arity n, then f (t1 , . . . , tn ) is a
                                                                  term.
Fangzhi Xu, Zhiyong Wu, Qiushi Sun, Siyu Ren, Fei
  Yuan, Shuai Yuan, Qika Lin, Yu Qiao, and Jun Liu.        Definition 3 (Syntax of FOL) An atomic formula
  2024. Symbol-LLM: Towards foundational symbol-
  centric interface for large language models. In ACL
                                                           over the signature σ = V ∪ C ∪ F ∪ R is a string
  2024, pages 13091–13116. Association for Computa-        of type r(t1 , . . . , tn ) such that r ∈ R is a relation
  tional Linguistics.                                      symbol with arity n and ti is a term, for all i ∈
{1, . . . , n}. The set of FOL formulas φ over the           • for all p ∈ R or arity n, a set pA ⊆ (DA )n .
signature σ is inductively defined as follows:
                                                            Given a σ-structure A and a variable evaluation
      φ := p(t1 , . . . , tn ) | ¬φ | φ ∧ φ | φ ∨ φ |     V : V → DA , for each term t, we define AV (t)
            φ → φ | φ ↔ φ | ∃xφ | ∀xφ,                    inductively as follows:

where the operators ¬, ∧, ∨, →, ↔ stand respec-             1. if t ∈ V, then AV (t) = V (t);
tively for the negation, the conjunction, the disjunc-      2. if t ∈ C, then AV (t) = tA ;
tion, the implication, and the equivalence, while
∃, ∀ denote the existential and universal quantifiers.      3. if t = f (t1 , . . . , tn ) with f ∈ F, then
   Among the logical symbols mentioned above,                  AV (t) = fA (AV (t1 ), . . . , AV (tn )).
parentheses can also be used to clarify which subex-
pressions a logical connective applies to. For            In the following, we define the semantics of FOL.
improved readability, parentheses are sometimes           Definition 5 Let φ be an FOL formula over the
omitted; in such cases, the following operator            signature σ, let A be a σ-structure and let V be
precedence is assumed (from highest to lowest):           a variable evaluation. We define the fact that AV
{¬, ∃, ∀}, ∧, ∨, →, ↔.                                    satisfies φ, denoted with AV |= φ, inductively as
   A variable x is said to be quantified if it falls      follows:
within the scope of a quantifier such as ∀x (univer-
sal) or ∃x (existential). Otherwise, it is considered        • AV |= p(t1 , . . . , tn ) iff (V (t1 ), . . . , V (tn )) ∈
a free variable. A formula may contain both free               pA , for all p ∈ R;
and quantified variables: when a formula contains
                                                             • AV |= ¬φ iff AV ̸|= φ;
no free variables, it is called a closed formula or a
statement.                                                   • AV |= φ ∧ φ′ iff AV |= φ and AV |= φ′ ;
   Although the syntax described above is the
most common, alternative conventions can also                • AV |= φ ∨ φ′ iff AV |= φ or AV |= φ′ ;
be adopted. For instance, one may adhere to the
                                                             • AV |= φ → φ′ iff AV ̸|= φ or AV |= φ′ ;
syntactic rules of theorem provers to facilitate inter-
action with such tools, or encode FOL formulas in            • AV |= φ ↔ φ′ iff AV |= φ → φ′ and AV |=
a functional style, thereby recasting autoformaliza-           φ′ → φ;
tion as a code-generation task and exploiting large
code-oriented datasets, as in (Liu, 2025; Pei et al.,        • AV |= ∃xφ iff there exists a d ∈ DA such that
2025).                                                         AV ′ |= φ, where V ′ (x) = d and V ′ (y) =
   In this survey, we do not distinguish among these           V (y) for all y ̸= x;
syntactic variants of FOL, as their differences are
                                                             • AV |= ∀xφ iff for all d ∈ DA we have that
largely superficial. It is nonetheless worth noting
                                                               AV ′ |= φ, where V ′ (x) = d and V ′ (y) =
that (Lam et al., 2024) reports that the standard
                                                               V (y) for all y ̸= x.
symbolic representation of FOL formulas yields
higher performance than alternative encodings.               We say that A satisfies φ, denoted with A |= φ,
                                                          iff AV |= φ, for all variable evaluations V . Given
A.2     Semantic and SMT solvers
                                                          two FOL formulas φ and φ′ over the signature σ,
We now define the semantics of FOL. The core of           we say that φ is equivalent to φ′ when AV |= φ
this definition is the notion of σ-structure, for any     iff AV |= φ′ , for all σ-structures A and all variable
signature σ.                                              assignments V : this is the same to say that AV |=
Definition 4 Let σ = V ∪ C ∪ F ∪ R be a signa-            φ ↔ φ′ for all σ-structures A and all variable
ture. A σ-structure A is given by:                        assignments V .
                                                             It is worth to notice that these notions, here pre-
   • a domain DA ̸= ∅;                                    sented in the general case, become clearer when
   • for all c ∈ C, an element cA ∈ DA ;                  φ is a statement. In this case, since there are no
                                                          free variables, the fact that AV |= φ doesn’t de-
   • for all f ∈ F of arity n, a function fA :            pend on the variable assignment V . For any two
     (DA )n → DA ;                                        statement φ and φ′ , they are equivalent when for
any σ-structure A, we have that A |= φ iff A |= φ′ ,        ture.
or equivalently, A |= φ ↔ φ′ .                                  Table 2 lists some datasets originally developed
   For every FOL formula φ, it is possible to trans-        to evaluate reasoning in NL, for which no FOL
form it into an equivalent formula, over the same           counterpart is available. To make them usable for
signature, such that the negation (¬) appears only          FOL-autoformalization, an annotator would need
in front of atomic formulas. This normal form is            to manually formalize the NL sentences that com-
called Negation Normal Form (NNF, for short). We            pose each dataset into FOL.
define (·)nnf as the function such that, given in in-           Table 3 lists datasets also developed for rea-
put any FOL formula φ it returns its equivalent             soning tasks, in which the FOL formulas are not
formula in NNF.                                             shipped as an explicit text field but can be recov-
   To verify the equivalence between two formulas           ered with some effort using rule-based techniques
φ and φ′ over the same signature σ, we employ               applied to the NL sentences. In several of these
SMT (Satisfiability Modulo Theories) solvers (Bar-          datasets (like Tafjord et al. (2021) or Tian et al.
rett and Tinelli, 2018). These solvers are highly           (2021)), generation proceeds by first producing a
efficient tools for deciding the satisfiability of first-   reasoning skeleton in FOL and then translating the
order formulas; that is, they determine whether,            FOL formulas into NL via rule-based templates.
given a first-order formula φ over a signature σ as         Since the translation rules are known, this process
input, there exists a σ-structure A and a variable          can in principle be reversed to recover the original
assignment V such that AV |= φ.                             FOL formulas even when they are not distributed
   An SMT solver typically consists of two main             with the dataset. However, in these cases the map-
components: a Boolean solver that handles the               ping between NL sentence and FOL formula is
propositional structure of φ (often based on the            expected to be straightforward, precisely because
DPLL or CDCL algorithms, as in classical SAT                it is rule-based and template-driven; consequently,
solvers) and a theory solver that resolves conjunc-         it is unlikely to offer a representative picture of the
tions of formulas belonging to a specific theory,           difficulty involved in formalizing a free-form NL
such as LRA (Linear Real Arithmetic). Over the              sentence.
past decades, driven by the remarkable efficiency
of SAT solvers, SMT solvers have evolved into
powerful tools for automated reasoning, and they
now play a crucial role in tasks such as formal
verification and planning.
   The problem of checking equivalence between
two statements φ and φ′ over the signature σ is
transformed to a satisfiability problem. Specifi-
cally, the statements φ and φ′ are equivalent if and
only if the statement ¬(φ ↔ φ′ ) is not satisfiable.
Formally, A |= φ ↔ φ′ for all σ-structures A if
and only if there does not exist a σ-structure A such
that A |= ¬(φ ↔ φ′ ).

B    Further NLI Datasets
As explained in Section 3, NLI datasets can be
used to evaluate FOL-autoformalization (via proxy
tasks), provided that the reasoning pattern in-
stantiated in each example can be represented in
FOL. However, some of these datasets were devel-
oped for other evaluation purposes and therefore
need to be supplemented with additional compo-
nents before they can be used to evaluate FOL-
autoformalization. In the following we will briefly
discuss the most recent datasets used in the litera-
               Dataset                                NL            FOL           No. of Instances
               ReClor (Yu et al., 2020)              Human      Not available          ∼6k
               LogiQA (Liu et al., 2020)             Human      Not available         ∼8.7k
               AR-LSAT (Zhong et al., 2021)          Human      Not available          ∼2k

 Table 2: Reasoning datasets that require external annotation to be usable for FOL-autoformalization evaluation.




  Dataset                                                               NL           FOL          No. of Instances
  RuleTaker/ProofWriter (Clark et al., 2020; Tafjord et al., 2021)   Rule-based   Recoverable         ∼500k
  PrOntoQA (Saparov and He, 2022)                                    Rule-based   Recoverable         Variable
  LogicNLI (Tian et al., 2021)                                       Rule-based   Recoverable          ∼20k
  FLD×2 (Morishita et al., 2024)                                     Rule-based   Recoverable         ∼100k

Table 3: Reasoning datasets whose FOL annotation is not shipped as a text field but it is recoverable, with some
effort, by inspecting the dataset’s generation procedure, in order to be usable for FOL-autoformalization evaluation.
