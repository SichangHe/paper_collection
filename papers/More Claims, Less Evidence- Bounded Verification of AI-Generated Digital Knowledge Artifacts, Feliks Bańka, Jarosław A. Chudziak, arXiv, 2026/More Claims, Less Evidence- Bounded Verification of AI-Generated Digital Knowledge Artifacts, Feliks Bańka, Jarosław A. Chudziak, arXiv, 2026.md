                                                       More Claims, Less Evidence:
                                                   Bounded Verification of AI-Generated
                                                       Digital Knowledge Artifacts

                                                               Feliks Bańka and Jarosław A. Chudziak

                                            Institute of Computer Science, Warsaw University of Technology, Warsaw, Poland
                                                     feliks.banka.stud@pw.edu.pl, jaroslaw.chudziak@pw.edu.pl
arXiv:2610.05547v1 [cs.AI] 4 Oct 2026




                                                Abstract. Digital libraries, repositories, and AI-mediated knowledge
                                                services increasingly rely on generative systems to produce summaries,
                                                descriptions, and other multi-claim knowledge objects. Yet generation
                                                can scale far more easily than verification capacity: a reviewer may need
                                                to decide whether an object is suitable for publication or downstream use
                                                after checking only a small fraction of its claims. This creates a fundamen-
                                                tal gap between claim-level verification and confidence in the object as a
                                                whole. The central question is therefore what a successful partial check
                                                implies about the reliability of the complete artifact when its size grows
                                                but the verification budget does not. This paper contributes a Bayesian
                                                model of bounded verification centered on the Predictive Value of Pass
                                                (PVP). The model predicts that evidentiary value decreases as artifacts
                                                grow under fixed verification capacity, improves with larger verification
                                                budgets, and is especially fragile when errors are sparse. Controlled ex-
                                                periments on FEVEROUS and FEVER support these predictions and
                                                show that adding supported claims around a fixed number of false or un-
                                                supported claims can make passing more likely while making a pass less
                                                informative.1 The model further yields the minimum verification budget
                                                required to maintain a target PVP, providing a practical component for
                                                AI-assisted quality-assurance workflows in which generated knowledge
                                                objects must be checked before publication or downstream use.

                                                Keywords: digital libraries · generative AI · information quality ·
                                                bounded verification · quality-assurance workflows


                                        1      Introduction
                                        Digital libraries, repositories, and other AI-supported knowledge services in-
                                        creasingly produce long-form outputs rather than isolated answers: summaries,
                                        reports, explanations, collection descriptions, and decision-support materials
                                        [26,25,11,4,3]. These outputs can be broken down into statements about facts,
                                        evidence, assumptions, or intermediate reasoning steps [10]. They support infor-
                                        mation access, review, and later use by people or other systems [7]. Reliability
                                        1
                                            Code      and       outputs:            https://github.com/latent-systems-lab/
                                            bounded-verification
2       F. Bańka and J. A. Chudziak

is assessed claim by claim, while the resulting knowledge object is typically con-
sumed as a whole [23].
    However, the ability to generate many claims does not imply the ability to
verify all of them [10,23]. Classical sampling and inspection methods study set-
tings in which only a limited subset of a larger population can be checked [6,13,2].
For AI-generated knowledge objects, this creates a gap: generation can produce
many plausible claims, while repository staff or other reviewers may be able to
inspect only a small subset [9]. As illustrated in Figure 1, a small number of
false or unsupported claims may therefore become diluted among many sup-
ported ones while the verification budget remains fixed. The key issue is not
only whether a partial check detects an error, but how much trust should be
placed in the complete object after it passes. In particular, adding supported
claims around a fixed number of false or unsupported claims can make passing
more likely while making a pass less informative. This matters in digital-library
and repository settings because such a pass may influence whether a generated
summary or description is shown to users or used by other services [25,24].
    We study this problem using a Bayesian bounded-verification model. An
object contains n auditable claims, a verifier checks only b of them, and an
unreliable object may contain f false or unsupported claims. Our central quantity
is the Predictive Value of Pass (PVP), the posterior probability that an object is
reliable given that it passed the bounded check. This shifts attention from error
detection alone to the information conveyed by a successful check. We analyze
how this value changes with object size, verification budget, and whether errors
are sparse, and use the model in reverse to ask how much verification is needed
to maintain a desired reliability level.
    This paper provides a Bayesian interpretation of bounded verification for AI-
generated digital knowledge objects. We define PVP for interpreting successful
partial checks and show that, under fixed verification capacity, a pass becomes
less informative as object size grows. We characterize the resulting true-claim
padding effect, evaluate its dependence on object size, verification budget, and
error sparsity using FEVEROUS and FEVER, and derive the minimum verifi-
cation budget required to maintain a target PVP.


2   Related Work and Positioning

Recent digital-library research applies LLMs to AI-supported access and con-
versational repository services [26,25]. Related work uses language models for
knowledge organization, subject indexing, and the evaluation of derived infor-
mation structures [12,18,24]. Work on library AI implementation emphasizes
human oversight, output quality, and resource constraints [9], while interface in-
terventions can encourage fact-checking of generated content [14]. Related work
on verifiable AI reasoning similarly uses explicit intermediate representations
to create inspectable points within otherwise complex reasoning pipelines [15].
As these systems create or derive information objects for retrieval, description,
                                                                               More Claims, Less Evidence                         3

                     Small artifact                                                           Large artifact

                 Few claims (n = 10)                                                        Many claims (n = 80)

    ✓    ✓       ✓      ×   ✓    ✓     ✓       ✓   ✓                       ✓    ✓    ✓    ✓    ✓    ✓       ...   ×   ✓   ✓   ✓
                                                          Add many
         1 false claim among few claims                  true claims            Same 1 false claim hidden among many claims
                                                          (true-claim
                                                           padding)
                     Audit budget: b = 3                                                  Audit budget: b = 3

             ✓              ✓              ✓                                         ✓             ?              ✓
                                                          Same audit
                                                         budget (b = 3)

                                                          Same false
                                                          claim (f = 1)


                       ✓ PASS                                                                  ✓ PASS
                        High trust                                                              Low trust


                        💡    Key insight: With a fixed audit budget, larger artifacts are more likely to pass
                                     while the pass is less informative about overall quality.



Fig. 1. Bounded verification of AI-generated digital knowledge artifacts. As artifact
size grows under fixed verification capacity, unsupported claims can be diluted among
supported ones, so a partial check provides posterior evidence, not a certificate of
whole-object reliability.


and organization, their use raises questions about how much trust the complete
object warrants when only some generated claims can be checked [25,24].
    Acceptance sampling and sequential analysis make decisions from limited
inspections rather than full population checks [6,21]. Bayesian lot quality assur-
ance sampling further connects bounded samples with predictive reliability [13].
We instead analyze posterior reliability after a partial audit passes, building on
this predictive interpretation of limited inspection [13]. Our focus is how that
reliability changes with artifact size under a fixed inspection budget [6,2].
    FEVER and FEVEROUS evaluate whether claims are supported by textual
or structured evidence [19,1]. Related benchmarks extend evidence-based ver-
ification to scientific claims, contrastive evidence, tables, and semi-structured
data [20,16,5,8]. Long-form factuality methods decompose generated outputs
into verifiable claims, but checking every claim remains costly [10,17]. Recent
work therefore seeks more efficient factuality-evaluation pipelines [23,22]. These
methods estimate or improve factuality [10,23], whereas we ask a complemen-
tary receiver-side question: when only b of n claims can be checked, how much
evidence does a successful check provide about the complete object as n grows?


3       Bounded Verification of AI-Generated Digital
        Knowledge Artifacts

We now formalize bounded verification as a Bayesian inference problem. The
model is deliberately minimal: an artifact consists of auditable claims, the verifier
4       F. Bańka and J. A. Chudziak

checks only a bounded subset, and the receiver updates trust after observing
whether the artifact passes. We use uniform random sampling as a controlled
baseline for isolating the effect of bounded verification capacity.

3.1   Audit Model and Predictive Value of Pass
The audit model abstracts a generated artifact as a collection of claims, some
of which may be false or unsupported. It has latent type θ ∈ {G, B}, where G
denotes a reliable object and B one containing false or unsupported claims. The
receiver has prior P (θ = G) = p and P (θ = B) = 1 − p.
    A bounded audit checks b claims sampled uniformly without replacement,
with 1 ≤ b ≤ n. When b = n, the audit becomes full verification; our main
interest is the bounded regime b ≪ n. A type-B object contains f false or
unsupported claims, with 1 ≤ f ≤ n. We focus on sparse-error settings, where
f ≪ n, since a small number of problematic claims may then be hidden inside a
large output. For example, an object containing 40 claims, 2 of which are false,
passes an audit of 5 claims whenever the verifier misses both errors.
    Formally, the artifact passes whenever none of the audited claims is false or
unsupported. Thus, the bad-pass probability is
                                                         n−f
                                                             
                                                          b
                    q(n, f ; b) = P (pass | θ = B, f ) = n .
                                                              b

A reliable artifact passes with probability P (pass | θ = G) = 1. Because q(n, f ; b)
only describes how often unreliable artifacts evade detection, we focus on poste-
rior reliability after a pass.
    The central quantity in this paper is the Predictive Value of Pass:

                         PVP(n, f ; b) = P (θ = G | pass).

By Bayes’ rule,
                                                  p
                       PVP(n, f ; b) =                          .
                                         p + (1 − p)q(n, f ; b)
    PVP measures how much trust a receiver should place in an artifact after it
passes a bounded audit. This differs from the pass rate itself. An artifact can
become more likely to pass as it grows, while the fact that it passed becomes
less informative about its reliability.

3.2   Evidentiary Dilution
As n grows while f and b remain fixed, each false or unsupported claim occupies
a smaller fraction of the artifact. A fixed-size audit is therefore less likely to
sample a problematic claim. This is the mechanism behind evidentiary dilution.
Proposition 1 (Evidentiary dilution). For fixed audit budget b and fixed
false-claim count f , over valid configurations with n ≥ max{b, f }, PVP(n, f ; b)
weakly decreases as artifact size n increases.
                                                    More Claims, Less Evidence      5

      If n − f < b, then q(n, f ; b) = 0. Once n − f ≥ b, we use the product form
                                              b−1
                                              Y   n−f −j
                              q(n, f ; b) =              .
                                              j=0
                                                   n−j

Every factor is nonnegative and increases with n, so q(n, f ; b) is nondecreasing in
this region. Moving from n − f < b, where q = 0, into this region also preserves
monotonicity. Hence PVP weakly decreases, proving the proposition.
    To connect this quantity to decisions, suppose accepting a reliable artifact
yields value V > 0, while accepting an unreliable artifact incurs loss L > 0. The
receiver accepts after a pass when

          EU (Accept | pass) = PVP(n, f ; b)V − (1 − PVP(n, f ; b))L ≥ 0.

Equivalently, acceptance is justified only when PVP(n, f ; b) ≥ τ , where τ =
L/(V + L). Thus, a successful audit may cease to justify acceptance once the
artifact becomes sufficiently large relative to the audit budget.
    For large n, the bad-pass probability and the corresponding audit-budget
rule are approximated by

                                                         n    1
                        q(n, f ; b) ≈ e−bf /n ,     b≈     log .
                                                         f    q0

Thus, maintaining a fixed bad-pass rate, and therefore a fixed PVP under a
fixed prior, requires audit effort to grow roughly linearly with artifact size in
sparse-error regimes.


3.3     Required Verification Budget

The practical inverse question is how large the verification budget must be to
maintain target posterior reliability η. We therefore define

               bmin (n, f, η) = min{b ∈ {1, . . . , n} : PVP(n, f ; b) ≥ η}.

The quantity bmin captures the verification effort required to maintain that re-
liability standard. For p = 0.5 and f = 2, maintaining PVP ≥ 0.8 requires
checking 5 of 10 claims but 40 of 80; for PVP ≥ 0.9, the corresponding budgets
are 7 and 53. Consistent with the scaling relation above, maintaining a fixed η
under sparse errors requires verification effort to grow with n.


4      Empirical Evaluation of Model Predictions

We evaluate the model by applying bounded audits to artifacts constructed from
labeled claims. We use gold labels as an oracle verifier to isolate verification
capacity from verifier error.
6      F. Bańka and J. A. Chudziak

4.1   Research Hypotheses

The model yields three testable predictions. H1: With fixed verification bud-
get b and a fixed number f of false or unsupported claims, increasing artifact
size n raises the bad-pass probability and lowers PVP. H2: Increasing b makes
unsupported claims less likely to be missed and raises PVP. H3: Evidentiary
dilution is stronger when errors remain sparse than when their number grows
proportionally with n.


4.2   Experimental Setup

Benchmark-derived claims retain their natural-language wording and evidence
while their support status is externally labeled. This allows us to vary object
composition and audit capacity without conflating bounded verification with
verifier accuracy. The evaluation is therefore a receiver-side stress test rather
than an end-to-end factuality benchmark.
    We use FEVEROUS as the main benchmark because it provides claim labels
grounded in both textual and tabular evidence. We use FEVER as a text-only
robustness check for the main true-claim padding result. In both datasets, sup-
ported claims are treated as reliable, while refuted or not-enough-information
claims are treated as false or unsupported.
    We construct each evaluated object as a set of benchmark claims. Reliable
objects contain only supported claims, whereas unreliable ones contain n − f
supported and f false or unsupported claims. Claims are sampled from dataset
label pools without duplication within an object; reuse across objects is allowed.
Unless otherwise stated, we use sizes n ∈ {10, 20, 40, 80}, false-claim counts
f ∈ {1, 2, 5}, audit budgets b ∈ {3, 5, 10}, and prior p = 0.5. For each configura-
tion and latent type, we construct 1,000 objects and run 20 independent audit
simulations per object using a fixed random seed.
    For each object, the audit samples b claims uniformly without replacement
and passes if all are supported. We estimate the empirical bad-pass rate qb(n) =
Pb(pass | θ = B), the overall pass rate, and the empirical Predictive Value of
Pass PVP(n)
       [        = Pb(θ = G | pass). The overall pass rate is computed under the
prior p = 0.5, so P (pass) = p + (1 − p)b   q (n). The experimental configurations
and parameter ranges are summarized in Table 1. We compare these empirical
quantities with the theoretical predictions from Section 3.
    We report Wilson confidence intervals for empirical pass rates; they are small
relative to the plotted effects and omitted from the main figures for readability.


4.3   Empirical Results

The following experiments test the three model predictions by varying artifact
size, verification budget, and error density.
                                                                                                            More Claims, Less Evidence                    7

    Table 1. Experimental configuration varying artifact size, audit budget, and number
    of false claims.

                                     Component               Values                                    Purpose
                                     Artifact size n 10, 20, 40, 80 object growth
                                     Audit budget b 3, 5, 10        verification capacity
                                     False claims f 1, 2, 5         sparse errors
                                     Main dataset FEVEROUS structured verification
                                     Robustness      FEVER          text-only verification
                                                             True-claim padding (b=5)

                                     A. Bad-pass rate                                                                 B. Predictive Value of Pass
                1.0                                                                                   1.0




                                                                           Predictive Value of Pass
                0.8                                                                                   0.8
Bad-pass rate




                0.6                                                                                   0.6
                0.4                                                                                   0.4
                0.2                                                                                   0.2
                0.0                                                                                   0.0
                      10   20   30      40        50    60       70   80                                    10   20     30     40        50    60   70   80
                                      Artifact size (n)                                                                      Artifact size (n)

                                               f=1 empirical          f=2 empirical                               f=5 empirical
                                               f=1 theoretical        f=2 theoretical                             f=5 theoretical

    Fig. 2. True-claim padding on FEVEROUS with audit budget b = 5: as artifact size
    grows, unreliable artifacts pass more often while PVP falls. Solid lines show empirical
    estimates and dashed lines the exact model.



    E1: True-claim padding. E1 tests H1 by increasing artifact size through sup-
    ported claims while holding b and f fixed.
        Figure 2 shows this pattern clearly. On FEVEROUS with b = 5 and f = 2,
    increasing artifact size from n = 10 to n = 80 raises the bad-pass rate from
    0.220 to 0.880, while PVP falls from 0.820 to 0.532. The overall pass rate si-
    multaneously increases from 0.610 to 0.940. Over the same range, verification
    coverage b/n falls from 50% to 6.25%. Thus, artifacts pass more often, but pass-
    ing becomes weaker evidence of reliability. The same qualitative trend appears
    for f = 5: the bad-pass rate increases from 0.003 at n = 10 to 0.720 at n = 80,
    while PVP decreases from 0.997 to 0.581.
        Empirical estimates follow the exact model across configurations. The same
    pattern also appears on FEVER. For f = 2, increasing n from 10 to 80 raises
    the bad-pass rate from 0.222 to 0.878, while PVP decreases from 0.818 to 0.533.


    E2: Audit budget sensitivity. E2 tests H2 by varying the audit budget b. As pre-
    dicted, larger audit budgets improve the evidentiary value of a pass by reducing
    the probability that all problematic claims are missed. For example, on FEVER-
    OUS with n = 80 and f = 5, increasing b from 3 to 10 reduces the bad-pass rate
    from 0.819 to 0.500 and raises PVP from 0.550 to 0.667.
8       F. Bańka and J. A. Chudziak

   Increasing a fixed audit budget delays evidentiary dilution but does not re-
move the size effect as n continues to grow: larger budgets shift PVP upward,
while each fixed-budget curve still declines with n.

E3: Sparse versus denser errors. E3 tests H3 by comparing fixed sparse errors
with errors that grow proportionally with n. With sparse f = 2, PVP decreases
from 0.817 at n = 10 to 0.531 at n = 80; when errors grow proportionally
as f = ⌈0.20n⌉, PVP remains more stable, moving from 0.819 to 0.761. Large
artifacts with a small number of hidden errors are therefore especially difficult
to interpret under bounded auditing. This regime is relevant to otherwise high-
quality generated knowledge objects, where most claims may be supported while
a few consequential errors remain difficult to detect under bounded review.


5   Discussion, Implications, and Limitations

A partial audit should not be treated as proof that the whole object is reliable:
its value depends on object size, audit budget, and whether errors are sparse.
The experiments highlight a pattern: bounded verification is least informative
when an object is largely correct but contains only a few hidden errors, because
those errors become easier to miss as the object grows. For generated summaries,
descriptions, and briefs in repositories or digital-library services, quality assur-
ance should either scale verification with the number of auditable claims or limit
output length [9]. The required-budget calculation makes the needed verification
effort explicit. In a repository workflow, a generated summary, description, or
research brief can undergo bounded review [25]. PVP and the required-budget
calculation can then indicate whether the result supports release, calls for more
checks or fuller review, or warrants withholding before later use [24].
    Our controlled study uses claim sets drawn from benchmarks with known bi-
nary labels, uniform random audits, and perfect verification of sampled claims.
It separates the effect of verification capacity from verifier error but does not
evaluate real objects generated by LLMs or human fact-checking [10], or auto-
matic factuality verifiers [23,22]. Real objects may also contain claims of unequal
importance and correlated errors.
    Future work should measure these effects on repository objects under other
audit policies. These include non-uniform inspection and imperfect human or
automatic verification. It should also study natural LLM-generated repository
or digital-library objects under these more realistic conditions.


6   Conclusion

AI-generated knowledge objects can grow faster than the resources available to
verify them. This creates a gap between claim-level checking and trust in the
whole object: when only part of an object can be inspected, a successful check
                                                  More Claims, Less Evidence         9

does not by itself reveal how reliable the complete object is. We studied this ques-
tion under bounded verification, where object size can grow while verification
capacity remains limited.
    Our main contribution is the Predictive Value of Pass (PVP), a Bayesian
measure for interpreting successful partial verification. We show that adding
supported claims around a fixed number of false or unsupported claims can
make an unreliable object more likely to pass while making that pass less infor-
mative. Experiments on FEVEROUS and FEVER show the same effect, and the
minimum-budget calculation shows how verification effort must scale to preserve
a target reliability level. In AI-assisted curation workflows, PVP can therefore
inform whether a generated object is ready for release after bounded review or
requires additional verification.


References
 1. Aly, R., Guo, Z., Schlichtkrull, M., Thorne, J., Vlachos, A., Christodoulopou-
    los, C., Cocarascu, O., Mittal, A.: FEVEROUS: Fact extraction and VERi-
    fication over unstructured and structured information. In: Proceedings of the
    Neural Information Processing Systems Track on Datasets and Benchmarks.
    vol. 1 (2021), https://datasets-benchmarks-proceedings.neurips.cc/paper/
    2021/hash/68d30a9594728bc39aa24be94b319d21-Abstract-round1.html
 2. Avenhaus, R., von Stengel, B., Zamir, S.: Inspection games. In: Aumann,
    R.J., Hart, S. (eds.) Handbook of Game Theory with Economic Applications,
    vol. 3, chap. 51, pp. 1947–1987. Elsevier (2002). https://doi.org/10.1016/
    S1574-0005(02)03014-X
 3. Bańka, F., Chudziak, J.A.: Multihedge: Adaptive coordination via retrieval-
    augmented control. In: Computational Science – ICCS 2026. Lecture Notes in
    Computer Science, vol. 16784, pp. 446–454. Springer, Cham (2026). https://doi.
    org/10.1007/978-3-032-29924-6_39
 4. Bańka, F., Chudziak, J.A.: Toward explanatory equilibrium: Verifiable reasoning as
    a coordination mechanism under asymmetric information. AAMAS 2026 Workshop
    on Explainable and Trustworthy Multi-Agent Systems (EXTRAAMAS) (2026),
    https://arxiv.org/abs/2604.09917
 5. Chen, W., Wang, H., Chen, J., Zhang, Y., Wang, H., Li, S., Zhou, X., Wang, W.Y.:
    TabFact: A large-scale dataset for table-based fact verification. In: International
    Conference on Learning Representations (2020), https://openreview.net/forum?
    id=rkeJRhNYDH
 6. Dodge, H.F., Romig, H.G.: Sampling Inspection Tables: Single and Double Sam-
    pling. John Wiley & Sons, New York (1944), https://books.google.com/books?
    id=XXk3AAAAMAAJ
 7. Gebru, T., Morgenstern, J., Vecchione, B., Wortman Vaughan, J., Wallach, H.,
    Daumé III, H., Crawford, K.: Datasheets for datasets. Communications of the
    ACM 64(12), 86–92 (2021). https://doi.org/10.1145/3458723
 8. Gupta, V., Mehta, M., Nokhiz, P., Srikumar, V.: INFOTABS: Inference on tables as
    semi-structured data. In: Proceedings of the 58th Annual Meeting of the Associa-
    tion for Computational Linguistics. pp. 2309–2324. Association for Computational
    Linguistics, Online (2020). https://doi.org/10.18653/v1/2020.acl-main.210,
    https://aclanthology.org/2020.acl-main.210/
10      F. Bańka and J. A. Chudziak

 9. Mergel, I., Kühler, J., Schumann, A.L., Schmidt, C.: Recommendations for the AI
    implementation in libraries. In: Mergel, I., Schmidt, C. (eds.) AI Innovations in
    Public Services, pp. 181–197. Springer, Cham (2026). https://doi.org/10.1007/
    978-3-032-01344-6_14
10. Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W.t., Koh, P., Iyyer, M., Zettle-
    moyer, L., Hajishirzi, H.: FActScore: Fine-grained atomic evaluation of factual
    precision in long form text generation. In: Bouamor, H., Pino, J., Bali, K. (eds.)
    Proceedings of the 2023 Conference on Empirical Methods in Natural Language
    Processing. pp. 12076–12100. Association for Computational Linguistics, Singa-
    pore (Dec 2023). https://doi.org/10.18653/v1/2023.emnlp-main.741, https:
    //aclanthology.org/2023.emnlp-main.741/
11. Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B.,
    Spitzer, E., Raji, I.D., Gebru, T.: Model cards for model reporting. In: Proceedings
    of the Conference on Fairness, Accountability, and Transparency. pp. 220–229.
    ACM, Atlanta, GA, USA (2019). https://doi.org/10.1145/3287560.3287596
12. Nandini, D., Blöthner, S., Larch, M., Schönfeld, M.: Organising knowledge from
    text: Prompt-based triple extraction and graph enrichment with large language
    models. In: Linking Theory and Practice of Digital Libraries. Lecture Notes in
    Computer Science, vol. 16097, pp. 53–70. Springer, Cham (2026). https://doi.
    org/10.1007/978-3-032-05409-8_5
13. Olives, C., Pagano, M.: Choosing a design to fit the situation: How to im-
    prove specificity and positive predictive values using bayesian lot quality as-
    surance sampling. International Journal of Epidemiology 42(1), 346–355 (2013).
    https://doi.org/10.1093/ije/dys230
14. Osop, H., Chia, D.C.Y., Lee, C.S., Goh, D.H.L.: Nudgr: A context-aware digital
    nudge intervention to promote fact-checking of GenAI content. In: Intelligence and
    Equity: Shaping the Future of Knowledge. Lecture Notes in Computer Science,
    vol. 16242, pp. 116–125. Springer, Singapore (2026). https://doi.org/10.1007/
    978-981-95-4861-3_10
15. Sadowski, A., Chudziak, J.A.: On verifiable legal reasoning: A multi-agent frame-
    work with formalized knowledge representations. In: Proceedings of the 34th ACM
    International Conference on Information and Knowledge Management. pp. 2535–
    2545. CIKM ’25, Association for Computing Machinery, New York, NY, USA
    (2025). https://doi.org/10.1145/3746252.3761057
16. Schuster, T., Fisch, A., Barzilay, R.: Get your Vitamin C! robust fact verifica-
    tion with contrastive evidence. In: Proceedings of the 2021 Conference of the
    North American Chapter of the Association for Computational Linguistics: Hu-
    man Language Technologies. pp. 624–643. Association for Computational Linguis-
    tics, Online (2021). https://doi.org/10.18653/v1/2021.naacl-main.52, https:
    //aclanthology.org/2021.naacl-main.52/
17. Song, Y., Kim, Y., Iyyer, M.: VeriScore: Evaluating the factuality of verifiable
    claims in long-form text generation. In: Al-Onaizan, Y., Bansal, M., Chen, Y.N.
    (eds.) Findings of the Association for Computational Linguistics: EMNLP 2024.
    pp. 9447–9474. Association for Computational Linguistics, Miami, Florida, USA
    (Nov 2024). https://doi.org/10.18653/v1/2024.findings-emnlp.552, https:
    //aclanthology.org/2024.findings-emnlp.552/
18. Tan, Z., D’Souza, J.: Toward purpose-oriented topic model evaluation enabled
    by large language models. International Journal on Digital Libraries 26 (2025).
    https://doi.org/10.1007/s00799-025-00429-5, article 23
                                                    More Claims, Less Evidence          11

19. Thorne, J., Vlachos, A., Christodoulopoulos, C., Mittal, A.: FEVER: A large-
    scale dataset for fact extraction and VERification. In: Proceedings of the 2018
    Conference of the North American Chapter of the Association for Computational
    Linguistics: Human Language Technologies. pp. 809–819. Association for Compu-
    tational Linguistics, New Orleans, Louisiana (2018). https://doi.org/10.18653/
    v1/N18-1074, https://aclanthology.org/N18-1074/
20. Wadden, D., Lin, S., Lo, K., Wang, L.L., van Zuylen, M., Cohan, A., Hajishirzi, H.:
    Fact or fiction: Verifying scientific claims. In: Proceedings of the 2020 Conference on
    Empirical Methods in Natural Language Processing. pp. 7534–7550. Association for
    Computational Linguistics, Online (2020). https://doi.org/10.18653/v1/2020.
    emnlp-main.609, https://aclanthology.org/2020.emnlp-main.609/
21. Wald, A.: Sequential Analysis. Wiley (1947), https://books.google.com/books?
    id=HlNtAAAAMAAJ, wiley mathematical statistics series
22. Wan, Y., Tan, H., Zhu, X., Zhou, X., Li, Z., Lv, Q., Sun, C., Zeng, J., Xu, Y.,
    Lu, J., Liu, Y., Guo, Z.: FaStFact: Faster, stronger long-form factuality eval-
    uations in LLMs. In: Findings of the Association for Computational Linguis-
    tics: EMNLP 2025. pp. 23814–23854. Association for Computational Linguistics,
    Suzhou, China (2025). https://doi.org/10.18653/v1/2025.findings-emnlp.
    1295, https://aclanthology.org/2025.findings-emnlp.1295/
23. Wei, J., Yang, C., Song, X., Lu, Y., Hu, N., Huang, J., Tran, D., Peng,
    D., Liu, R., Huang, D., Du, C., Le, Q.V.: Long-form factuality in large
    language models. In: Advances in Neural Information Processing Systems.
    vol. 37, pp. 80756–80827 (2024). https://doi.org/10.52202/079017-2567,
    https://proceedings.neurips.cc/paper_files/paper/2024/hash/
    937ae0e83eb08d2cb8627fe1def8c751-Abstract-Conference.html
24. Xu, Y.S., Mohd Khalid, Y.I.A., Kassim, M.S.S.: Automatic subject indexing: How
    has it evolved and where is AI taking it? In: Intelligence and Equity: Shaping the
    Future of Knowledge. Lecture Notes in Computer Science, vol. 16242, pp. 3–21.
    Springer, Singapore (2026). https://doi.org/10.1007/978-981-95-4861-3_1
25. Yang, L., Zhang, Z.: Developing an AI-enhanced conversation application on
    DSpace: Technical procedure and details. In: Sustainability and Empowerment
    in the Context of Digital Libraries. Lecture Notes in Computer Science, vol.
    15493, pp. 189–197. Springer, Singapore (2025). https://doi.org/10.1007/
    978-981-96-0865-2_15
26. Zerhoudi, S., Granitzer, M.: Generative agents navigating digital libraries. In:
    Sustainability and Empowerment in the Context of Digital Libraries. Lecture
    Notes in Computer Science, vol. 15493, pp. 171–188. Springer, Singapore (2025).
    https://doi.org/10.1007/978-981-96-0865-2_14
