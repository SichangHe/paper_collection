                                          FaithformBench: Benchmarking Faithfulness of Mathematical Chain-of-Thought
                                                                     Autoformalisation
                                         Rob Cornish1∗ , Iacopo Ghinassi1∗ , Po-Hung Yeh1∗ , Shuqi Liu1 , Qiyuan Xu1 , Haoxuan Yin2 , Dominik
                                                                 Wagner1 , Wenda Li3 , Yee Whye Teh2 , Luke Ong1
                                                                                     1
                                                                                       Nanyang Technological University, Singapore
                                                                                         2
                                                                                           University of Oxford, United Kingdom
                                                                                     3
                                                                                       The University of Edinburgh, United Kingdom


                                                                       Abstract                                Perturbed input: “x ∈ R, 3x = 5. Conclude 3x+2 = 51.”
                                                                                                               (The original omnimath-629 example correctly uses 45 instead of 51.)
                                           Autoformalisation (AF) systems map natural-language reason-
                                           ing steps into formal statements in a proof assistant such as
                                           Lean. We consider how to assess the faithfulness of these sys-      Expected output                        Observed output (Kimina)
                                           tems. Existing approaches require expensive human-annotated         theorem faithful_AF                    theorem unfaithful_AF
                                           ground truth, or rely on LLM judges or embedding models,
arXiv:2608.10916v1 [cs.CL] 11 Aug 2026




                                                                                                                (x : R) (h : 3^x = 5) :                (x : N) (h : 3^x = 5) :
                                           which come with limited guarantees of accuracy. In addition,          3^(x+2) = 51 := by                     3^(x+2) = 51 := by
                                           these methods typically only consider inputs that are known            sorry                                  exfalso
                                           to be correct, and therefore do not assess whether the AF                                                     ... -- Proof here
                                           translates incorrect inputs faithfully. To address these lim-
                                           itations, we propose a new benchmark for AF faithfulness           Figure 1: Existing AF methods often produce provable outputs
                                           that is cheap to apply, sound under weak assumptions, and          even when their input is invalid. This example was obtained
                                           assesses both positive and negative examples. Our method is        by perturbing omnimath-629. The input is invalid, but
                                           based on automatically generating perturbed reasoning steps        Kimina silently modified the type of x so the claim follows
                                           that are designed to render them invalid, and then measur-         ex falso (since 3x = 5 is never satisfiable when x ∈ N). For
                                           ing validity preservation on unperturbed steps and invalidity      the unperturbed input, which had 45 instead of 51, Kimina
                                           preservation on perturbed steps. We apply our method to eight      gave x the correct type R.
                                           AF systems across four mathematical datasets, and observe
                                           pervasive sycophancy: many AFs “silently correct” invalid
                                           inputs into provable statements. The most validity-preserving
                                           fine-tuned AFs are also the most sycophantic, suggesting a          • Comparing the output of the AF method against a dataset
                                           tension between validity and invalidity preservation in current        of human-checked ground-truth formalisations, such as
                                           AF systems.                                                            BEq (Liu et al. 2025b) and GTED (Liu et al. 2025c);
                                                                                                               • Using LLM judges or embedding models to detect whether
                                         Code and data —                                                          the outputs of the AF align semantically with its input
                                           https://github.com/Ighina/FaithformBench                               (Jana et al. 2025).
                                                                                                              These approaches involve contrasting tradeoffs. On the one
                                                                 1   Introduction                             hand, while usually very reliable, human-annotated datasets
                                         Autoformalisation (AF) systems translate natural-language            are very slow and expensive to obtain. On the other hand,
                                         reasoning steps into formal mathematical statements that can         while fast and scalable, neural methods come with no guar-
                                         then be verified by proof assistants like Lean (de Moura             antees of accuracy, and can fail to recognise subtle errors in
                                         and Ullrich 2021), Rocq (Coquand and Huet 1988), and                 formalisation. In addition, both approaches typically assume
                                         Isabelle (Paulson 1990). There is growing interest in using          that the input natural language statements are correct, and
                                         AF to verify the chain-of-thought (CoT) reasoning of large           so do not test whether the AF system can preserve errors in
                                         language models (LLMs), with the idea being to formalise             incorrect statements, which is crucial for applications such as
                                         each step individually and check its correctness using a proof       CoT verification where the entire point is to identify reasoning
                                         assistant (Quan et al. 2025; Zhou and Zhang 2025; Liu et al.         steps that are incorrect.
                                         2025a). For these use-cases, it is crucial that the AF system           In this work, we propose a novel assessment methodology
                                         is faithful: the meaning of the formal statements it produces        whose tradeoff profile complements these two extremes, and
                                         should match that of the original natural language statements.       that considers incorrect statements as well as correct ones.
                                            In turn, it is crucial to have a reliable way to assess the       Our key idea is not to assess faithfulness in full generality,
                                         faithfulness of a given AF system. Two key approaches exist          but instead to focus specifically on detecting two key failure
                                         at present:                                                          modes: error induction, in which a correct input maps to a false
                                                                                                              formal statement, and silent correction, in which an incorrect
                                            ∗
                                                These authors contributed equally.                            input maps to a true formal statement. Our methodology is
based on perturbing correct natural language statements to         Autoformalisation and Formal Verification in the Wild
create incorrect ones, and then checking whether the AF            Wu et al. (2022) set the stage by bridging natural language and
system correctly preserves validity or invalidity accordingly.     machine-verifiable code, while Zhou et al. (2024) sharpened
This approach does not require human-annotated datasets, and       this mandate by grounding quantitative reasoning through
so is cheap and scalable to apply in practice. At the same time,   autoformalised checks. Recent efforts focus on making ver-
under weak assumptions, it comes with stronger guarantees          ification more granular: Herald (Gao et al. 2024b) was an
of soundness compared with automated approaches such as            early work that released its dataset and formaliser. This was
LLM judges. In particular, if a model fails our benchmark,         followed by Zhou and Zhang (2025) and Liu et al. (2025a),
then we can be confident that one of the two failure modes is      which utilise step-by-step formal feedback to catch reasoning
present, and therefore that the AF method is not faithful.         errors mid-solution, effectively acting as a running companion
                                                                   rather than a post-hoc audit. ProofBridge (Jana et al. 2025)
Contributions     Our contributions are as follows:                aligns natural language and formal proofs via shared semantic
1. We formalise the faithfulness of AF systems in a way that       embeddings, while StepFun-Formaliser (Wu et al. 2025) fuses
   encompasses invalid as well as valid inputs, and identify       knowledge with reasoning.
   two failure modes (error induction and silent correction)
                                                                   Sycophancy in LLM Sycophancy (Perez et al. 2023;
   that can be soundly detected using a proof assistant.
                                                                   Sharma et al. 2024) in general refers to an LLM’s tendency
2. We introduce a scalable and general-purpose methodol-           to agree with the user’s opinions or preferences, even if they
   ogy for estimating lower bounds on the prevalence of            are false or unethical. In the context of mathematics, a strand
   each failure mode. Our approach is based on automati-           of work (Liu et al. 2026; Kirichenko et al. 2025; Xue et al.
   cally perturbing valid reasoning steps, and is sound under      2025) has been devoted to studying how an LLM will answer
   weak assumptions, without requiring human-annotated             an ill-formed (underspecified or unreasonable) mathematical
   examples.                                                       question. BrokenMath (Petrov, Dekoninck, and Vechev 2025)
3. We present FaithformBench, a benchmark obtained by              is closest to our work: they study sycophancy in (natural
   applying our methodology to ProcessBench (Zheng et al.          language) theorem proving, where an LLM might come up
   2025). FaithformBench consists of 12,784 reasoning steps        with a hallucinated proof in natural language for an incorrect
   and perturbed counterparts across four mathematical             statement. In formalised theorem proving, that problem is not
   datasets of increasing difficulty. We publicly release this     too harmful because the proof will simply be rejected by the
   benchmark and use it to evaluate the faithfulness of eight      proof checker. In this paper, we identify and study a novel
   AF systems.                                                     type of sycophancy that arises in autoformalisers, specifically,
Specifically, we evaluated 4 fine-tuned AF methods (Goedel         LLMs fine-tuned to translate natural language statements into
(Lin et al. 2025), Herald (Gao et al. 2024b), Kimina (Wang         Lean representations such as Goedel, StepFun, Kimina and
et al. 2025), Stepfun-Formaliser (Wu et al. 2025)), and 4          Herald.
general-purpose foundation models (Claude Opus 4.7, GPT            Data, Benchmarks, and Evaluation Metrics The rapid
5.2, Gemini 3.1 Pro, and Qwen Plus). We found:                     scaling of autoformalisation models has necessitated more
1. All the fine-tuned models exhibited high levels of silent       rigorous benchmarks and nuanced evaluation metrics. To
   correction, rather than faithfully representing the input       this end, datasets such as Herald (Gao et al. 2024b) provide
   (see Figure 1 for an example).                                  essential natural-language-annotated Lean 4 data. However,
                                                                   evaluating formalisation on these complex datasets goes
2. The more capable a fine-tuned model was in formalising          beyond mere binary correctness; it requires assessing the
   correct CoTs, the more likely it was to silently correct        structural alignment and faithfulness of the generated code.
   errors.                                                         Recent metrics offer more precise, semantically-grounded
3. Compared to the fine-tuned models, the general-purpose          measurements of this formalisation quality: Generalized Tree
   models exhibited significantly lower rates of silent correc-    Edit Distance (GTED) (Liu et al. 2025c) quantifies structural
   tion.                                                           similarity, while Bidirectional Extended Definitional Equiv-
                                                                   alence (BEq) (Liu et al. 2025b) leverages formal-grounded
                    2   Related Work                               equivalence to measure accuracy. For the CoT process, Pro-
Neural Theorem Proving and Formalisation Neural theo-              cessBench (Zheng et al. 2025) audits steps in natural language;
rem proving is a rapidly evolving field. LeanDojo (Yang et al.     we audit steps in formal language, building upon this line of
2023) introduces a retrieval-augmented generation (RAG)            inquiry.
framework. LEGO-Prover (Wang et al. 2024a) emphasizes
the automated synthesis and reuse of lemmas as LLM skills.                    3    Faithful Autoformalisation
Draft, Sketch, and Prove (Jiang et al. 2023) proposes that         Reasoning steps For our purposes, a reasoning step is
NTP models can first generate natural language proof drafts,       simply a natural language string x that asserts some conclusion
then formalize them into formal proofs. DeepSeek-Prover-           based on some assumptions. For example:
V1.5 (Xin et al. 2025) applies Reinforcement Learning and               “Let a, b, and c be real numbers, where a > b and (1)
Monte-Carlo Tree Search. DeepSeek-Prover-V2 (Ren et al.                 b > c. Then a > c follows.”
2025), Seed Prover (Chen et al. 2025), and Kimina (Wang            We are deliberately loose about the “encoding” used for x,
et al. 2025) further incorporate CoT in their reasoning.           which can vary significantly between datasets. For example, x
may consist of unstructured text describing a “raw” reasoning        This input is clearly invalid. Intuitively, the output of a faithful
trace, or a JSON object, or something else entirely.                 AF system should also capture this error as follows:
   The methodology we develop below could straightfor-
wardly be applied to systems that process a sequence of                             a, b, c : R, a > b, b > c ⊢ c > a.
reasoning steps (i.e. a chain-of-thought) rather than only a         Failure modes of faithfulness As the previous examples
single one. However, here we follow the standard practice            illustrate, a faithful AF system must satisfy the following
of analyzing CoTs in a step-wise manner (Miao, Teh, and              conditions for each input x:
Rainforth 2023; Lightman et al. 2023; Zhou and Zhang 2025;
Liu et al. 2025a; Zheng et al. 2025).                                  • Validity preservation: If x is valid, then AF(x) should be
                                                                         true.
AF systems We denote the AF method under assessment                    • Invalidity preservation: If x is invalid, then AF(x) should
by AF. This takes a reasoning step x as input and tries to               be false.
produce an output AF(x) that encodes a sequent as follows:
                                                                     On their own, these conditions are not sufficient for faithful-
                       ϕ1 , . . . , ϕn ⊢ ψ,                   (2)    ness. For example, the following AF system satisfies both
                                                                     conditions:
where ϕ1 , . . . , ϕn are premises, and ψ is the conclusion. The                          
sequent (2) is typically encoded in some formal system, and                                 ⊢ 0 = 0 if x is valid
                                                                                    x 7→                                         (6)
asserts that ψ follows from the conjunction of ϕ1 , . . . , ϕn via                          ⊢ 0 = 1 if x is invalid.
its inference rules. This high-level format is general enough
to encompass all AF systems we are aware of.                         This would clearly not be faithful, since the output throws
   In practice, an AF can fail for a variety of reasons, e.g.        away almost all the information contained in the input. More
by exceeding a token budget or if its output is syntactically        generally, if AF is not faithful for an input x, then necessarily
invalid. We write AF(x) = ∅ to denote that any such failure          either (i) it failed to produce a syntactically correct output
mode occurred.                                                       (i.e. AF(x) = ∅), or (ii) its output must exhibit one of the
                                                                     following failure modes:
Lean AFs In our experiments, we focus specifically on
AFs whose output (2) is encoded in Lean (de Moura and                1. Error induction: x is valid, but AF(x) is false
Ullrich 2021). The premises ϕi will express either typing            2. Silent correction: x is invalid, but AF(x) is true
assumptions on variables (e.g. “a is a real number”) or              3. Semantic drift: neither of the previous two cases holds,
propositional assumptions (e.g. “a > b”). The conclusion                 but the output still does not correspond semantically to x
ψ will always be a further proposition (e.g. “a > c”). The               in some way.
overall statement (2) then asserts that for all values of the        The AF system (6) suffers from the third failure mode here.
variables in question (e.g. a, b, c), the conclusion ψ follows
from the propositional assumptions. A full example is as             Detecting unfaithfulness The Lean kernel provides a
follows:                                                             trusted way to verify that a given formal statement of the form
              a, b, c : R, a > b, b > c ⊢ a > c.            (3)      (2) is true or false. To verify that it is true, we can simply try
In Lean syntax, this becomes the following:                          to find a proof that is accepted by the kernel. For the example
                                                                     of (4), this means trying to replace the sorry with an actual
      theorem transitivity :                                         proof of the theorem. To verify that (2) is false, we can try
        ∀ (a b c : R) (p : a > b)                             (4)    to refute it, i.e. find a proof of its logical negation instead. In
          (q : b > c), a > c := by sorry                             other words, we can try to find values for the variables such
Here sorry indicates that the proof is not actually provided.        that the propositional premises ϕi are true, but the conclusion
This is standard for AF tasks: the AF system is only required        ψ is false. For the example of (4), this means trying to prove
to produce a formal statement of the theorem, and not an             the following:
actual proof of it.                                                   ∃ (a b c : R) (p : a > b) (q : b > c),
                                                                          ¬(a > c)                                                   (7)
Faithfulness We now consider how we would like an AF
system ideally to behave. Intuitively, the output AF(x) should       If we are successful, then we know that (2) is false.
have the same logical “meaning” as the input x. In this case,           In turn, this gives a trusted way to detect the first two
we say the AF is faithful for x. We say that an AF is unfaithful     failure modes of unfaithfulness described above. In particular,
for x if it fails to produce a faithful output (including by         if we are given an input x that is valid, but determine the
producing no output at all, i.e. AF(x) = ∅). For example,            AF output (2) is false, then we can conclude that the AF is
it is clear that (3) is a faithful formalisation of the input        error-inducing for this input. Likewise, if we are given an
(1). Faithfulness seems to constitute the end-goal of most AF        input x that is invalid, but determine the AF output (2) is
methods we are aware of in practice (in some cases implicitly).      true, then we can conclude that the AF has performed a silent
   The input (1) is an example of a valid reasoning trace.           correction. Importantly, this approach is sound: if either case
However, the concept of faithfulness also applies to invalid         occurs, we can be very confident we have found a real failure
inputs. Consider the following modification to (1) in red:           mode of the AF system.
      “Let a, b, and c be real numbers, where a > b and                 Importantly, this method of detecting unfaithfulness is
      b > c. Then c > a follows.”
                                                              (5)    incomplete. In particular, it would not detect the semantic
drift failure mode exhibited by (6). Likewise, since proof          We then calculate the following statistics:
synthesis is in general uncomputable, it is possible the prover                     #{i | zi = ⊥}                 #{i | z̄i = ⊤}
fails to find a proof for either (2) or its negation, even if one       FNR :=                         FPR :=
of them is actually true. Despite this, as we show empirically,                            N                            N
the above detection strategy is able to extract considerable                         #{i | AF(xi ) = ∅} + #{i | AF(x̄i ) = ∅}
                                                                        AFFR :=
information about a variety of AF methods across a range of                                              2N
problem domains.                                                    where 1 ≤ i ≤ N . Here FNR, FPR, and AFFR stand for
                                                                    “false negative rate”, “false positive rate”, and “autoformalisa-
          4    Benchmarking Faithfulness                            tion failure rate” respectively. Under assumptions (8) and (9),
                                                                    we have
We now describe our method for estimating the prevalence of
the failure modes from Section 3.                                     • If FNR is large, then the AF method is often error-
                                                                        inducing. This is because xi is (usually) valid, but if
Dataset We assume access to a dataset of N reasoning steps              zi = ⊥, then AF(xi ) is false.
{x1 , . . . , xN }. We do not assume that any xi is accompanied       • If FPR is large, then the AF method often silently corrects
by a ground truth formalisation. Our key assumption is as               its input. This is because Pert(xi ) is (usually) invalid, but
follows:                                                                if z̄i = ⊤, then AF(Pert(xi )) is true.
                                                                    The quantity AFFR measures the percentage of inputs for
            A high proportion of the xi are valid.           (8)
                                                                    which the AF system fails to produce a syntactically correct
In our experiments, we obtain our data from ProcessBench            output altogether. We aggregate the failure cases AF(xi ) = ∅
(Zheng et al. 2025), which consists of CoTs that have been          and AF(x̄i ) = ∅ into a single statistic since both have the
human-annotated as valid, although other data could be used         same interpretation (i.e. no output produced).
as a drop-in replacement.                                           Unfaithfulness Lower Bound We further aggregate these
                                                                    observed failure events into a single summary statistic. Specif-
Perturbation function We denote by Pert a perturbation
                                                                    ically, we consider the fraction of the 2N total examples (both
function. This takes as input a reasoning step x and returns
                                                                    perturbed and unperturbed) for which some failure event
another reasoning step Pert(x) by slightly modifying x in
                                                                    above occurs. For unperturbed examples, this means either
some way. For example, given the input (1) from earlier, Pert
                                                                    zi = ⊥ or AF(xi ) = ∅, and for the perturbed examples, either
might return something like (5) as its output. We leave the
                                                                    z̄i = ⊤ or AF(x̄i ) = ∅. We denote this fraction by UFLB
exact implementation details of Pert flexible, with our only
                                                                    (“Unfaithfulness Lower Bound”). Since the failure events are
requirement being the following:
                                                                    mutually exclusive (e.g. AF(xi ) = ∅ implies zi = ∅ ̸= ⊥),
       A high proportion of the Pert(xi ) are invalid.       (9)    we have
                                                                                           1          1
In this work, we consider LLM-based implementations of                          UFLB = FNR + FPR + AFFR.
                                                                                           2          2
Pert, as well as a deterministic approach based on regexes.
                                                                    Under assumptions (8) and (9), each failure event above
Prover We require access to a prover that we denote by              implies that the AF was unfaithful, and so UFLB estimates
Prove. This takes as input an unproven formal statement y           a lower bound on the proportion of inputs on which the AF
of the form (2), and tries to find a proof for it. For any given    was unfaithful. Moreover, a failure of the prover can only
y, three outcomes are relevant for us, which we denote as           decrease UFLB, so a weak Prove loosens this bound but
follows:                                                            never invalidates it. If UFLB is large, we can therefore be
                                                                    confident that the AF is often unfaithful. On the other hand,
 • Prove(y) = ⊤ if the prover finds a proof of y.                   if UFLB is small, then we must be more careful about what
 • Prove(y) = ⊥ if the prover refutes y by finding a proof          conclusions to draw.
   of its logical negation (e.g. (7) in the case that y is given    Contingency analysis The UFLB provides an aggregate
   by (4) from earlier).                                            snapshot of the overall degree to which the AF is unfaithful.
 • Prove(y) = ∅ if the prover fails to find a proof for both y      For diagnostic purposes, we found it instructive also to exam-
   and its negation (or if y = ∅ itself).                           ine the pairs (zi , z̄i ) associated with each input xi . Here the
                                                                    following cases are possible:
The third case ∅ here is included to cover proof search
timeouts (which are inevitable for some inputs due to Gödel’s       1. Faithfulness: zi = ⊤ and z̄i = ⊥, i.e. the unperturbed
incompleteness theorem).                                                formalisation is provable, while the perturbed one is not.
                                                                        This is the outcome that a faithful AF would produce.
Failure statistics We now introduce statistics that quantify        2. Sycophancy: zi = z̄i = ⊤, i.e. both formalisations are
the extent to which an AF system suffers from the failure               provable. This outcome would occur for an AF that is
modes defined above. For each xi in our dataset, we compute             sycophantic and always silently corrects invalid inputs.
                     x̄i := Pert(xi )                               3. Abstention: zi = z̄i = ⊥, i.e. neither formalisation is
                                                                        provable. We conjecture this may occur if the input xi is in
        zi := Prove(AF(xi )) z̄i := Prove(AF(x̄i )).                    some sense too “difficult” for the AF to process altogether.
4. Inversion: zi = ⊥ and z̄i = ⊤, i.e. the opposite of                Perturbation effectiveness and DAG structure correctness
   validity preserving. (This counterintuitive case occurred          Recall that a key assumption of our method is (9). To ensure
   very rarely in practice.)                                          this holds, we used 3 SOTA LLMs to judge (Zheng et al.
5. Inconclusive: zi = ∅ or z̄i = ∅, i.e. the AF does not              2023) the effectiveness of Pert in producing invalid reasoning
   produce a syntactically valid output, or the provability           chains. The perturbations were judged on average as effective
   of the AF output could not be determined, in either the            in 97.8% of the total 12,784 reasoning steps.
   perturbed or unperturbed case.                                        To further validate such numbers, four annotators labelled
                                                                      219 stratified items across the four datasets, on disjoint subsets
The above interpretations are mainly suggestive, and unlike           with shared gold questions, and a meta-reviewer checked the
UFLB do not come with strict guarantees under the assump-             full annotations. Human agreement with GPT-5.2 is 95.9%
tions we have made. For example, the pathological AF in               overall (90.0% on GSM8K, 98.6% on MATH, 95.5% on
(6) above would also exhibit “faithfulness” according to the          OlympiadBench, 95.1% on OmniMATH). In 7 of the 9
above definition. However, we have found empirically that             disagreements the LLM judged a perturbation invalid where
these descriptions do often seem reasonable.                          the human judged it valid, so the LLM panel is stricter than
                                                                      humans and the 2.2% contamination rate reported above is,
                   5    FaithformBench                                if anything, an overestimate. Recomputing our main metric
We used our methodology described above to produce a                  after excluding every perturbation judged invalid changes no
concrete, reproducible faithfulness benchmark using the data          value by more than 0.01 for any model on any dataset.
from ProcessBench (Zheng et al. 2025). We refer to our                   For DAG parsing, we manually inspected a sample of
benchmark as FaithformBench. See Figure 2 for an overview.            210 nodes and found accuracies of 100% (GSM8K), 94.2%
                                                                      (MATH), 95.6% (OlympiadBench) and 96.7% (OmniMATH).
5.1   Dataset                                                         The errors we found were missing dependencies, redundant
                                                                      dependencies and redundant nodes, and none of them invali-
We extracted a dataset of individual reasoning steps from             dated a step or a chain, which could only happen if a critical
ProcessBench (Zheng et al. 2025), a human-verified bench-             dependency were omitted, and we did not observe this.
mark for LLM mathematical reasoning aggregated from four                 We have also used the annotating LLM itself to self-check
datasets of increasing difficulty: GSM8K (Cobbe et al. 2021),         the declarative statement classification step, yielding 100%
MATH (Hendrycks et al. 2021), OlympiadBench (He et al.                of self-agreement across the board. A manual validation of
2024), and Omni-MATH (Gao et al. 2024a).                              such numbers on 200 randomly sampled steps yielded an
    ProcessBench contains 3,400 reasoning chains expressed            agreement with the self-judge of 95.5%, where the majority of
in natural language. Each reasoning chain contains potentially        cases of disagreement however included the LLM judge being
many individual reasoning steps, and the whole chain is               more conservative than the human annotator (i.e. labeling
labelled by human experts as either free of errors or not. As a       something as non-declarative, while the judge labeled it as
preprocessing step, we selected the error-free subset, obtaining      declarative), therefore excluding more rather than including
1,179 reasoning chains. Next, following previous literature on        potential sources of noise.
autoformalising reasoning steps (Zhou and Zhang 2025), we
converted each chain into a DAG whose edges denote logical                           6    Experimental Results
dependency. We then extracted each node together with its
parents to form an individual reasoning step. In total, this          We used our benchmark to evaluate four custom AF methods
filtering pipeline produced 1,179 processed reasoning chains          from the literature: Goedel (Lin et al. 2025) (8B), Herald
and 12,784 individual reasoning steps xi .                            (Gao et al. 2024b) (7B), Kimina (Wang et al. 2025) (7B),
                                                                      and StepFun (Wu et al. 2025) (7B). We also evaluated four
5.2   Perturbations                                                   frontier LLM models: Claude Opus 4.7 (Anthropic 2026),
                                                                      GPT 5.2 (OpenAI 2025), Gemini 3.1 Pro (Google 2026) and
As described in Section 3, a key part of our methodology              Qwen Plus (Qwen Team 2025), which are much larger but
is a perturbation function Pert. For the experiments we               not fine-tuned for autoformalization.
report here, we used an LLM with a perturbation-generation               For the prover component of our approach (i.e. Prove from
prompt for this purpose. In Appendix C we additionally report         Section 4), we used DeepSeek-Prover-V2 (Ren et al. 2025).
results where Pert is obtained from a deterministic strategy          All FNR, FPR, AFFR, and UFLB statistics we report below
based on regexes. Our prompt was based on the perturbation            are computed over at least 1,282 data points, and so their 95%
procedure introduced by Petrov, Dekoninck, and Vechev                 confidence intervals are negligible (half-widths ≤ 0.03) and
(2025), but modified to operate on individual reasoning               therefore omitted.
steps rather than complete reasoning chains. The prompt
encourages the LLM to preserve as much of a reasoning step            6.1   Specialised Autoformaliser Results
as possible, but to subtly modify it so it becomes invalid.           Figure 3 shows the FNR, FPR, AFFR and UFLB metrics
Figure 1 gives an example of an actual perturbed reasoning            obtained on FaithformBench with the 4 specialised AFs. From
step from our benchmark (in this case produced by the regex-          the figure it is evident that:
based perturbation of Appendix C). We applied Pert to each of
the original xi , giving a dataset of 12,784 pairs (xi , Pert(xi ))   FNR The AFs have a relatively low rate of producing
of unperturbed and perturbed reasoning steps.                         formalisations of valid statements that are then refuted, which
        ProcessBench (NL)                                 Perturbation                                          Formalisation                                      Proof
               ID: gsm8k-216                                                                     - Perturbed               - Perturbed             - Perturbed           - Perturbed
                                            – Unperturbed       – Perturbed                      - Direct                  - Negation              - Direct              - Negation
                                                              ′
                                          [S4 ] Tue = 4 + 1 [S4 ] Tue = 4 / 2                    theorem                   theorem                 ... := by             ... := by
 [S1 ] Mon rain = 2.
                                                S2        S3                                     rain_bad                  rain_not                 simp                  intro h
 [S2 ] 2×Mon = 4.                                                         S2        S3
                                                                                                  (mon := 2)                : ¬ (∀ ...,             rfl                   have : 5 ̸= 2
 [S3 ] Tue = (2×Mon) +1.                                                                          (tue :=                       tue = 4/2)          - Failed               := by decide
 [S4 ] Tue = 4 + 1.                                  S4                         ′                2*mon+1)                   := by sorry             - (Expected)          - ✓Proved
                                                                               S4
                                                                                                  : tue = 4/2
 [S5 ] Tue = 5.
                                                                                                  := by sorry




Figure 2: An LLM parses ProcessBench’s natural language steps into a DAG. We then perturb and formalise the nodes associated
with the parents into a pair of opposing statements: a direct one and its negation. The prover will try to show both statements and
compile the proofs; if the formalisation preserves the invalidity, the compilation will support the negation.

                    Goedel                                         Herald                                               Kimina                                       Stepfun
0.5                                       0.5                                                    0.5                                              0.5
0.4                                       0.4                             0.49       0.50        0.4                                              0.4
                                                 0.35          0.46                                                            0.44    0.45
                0.19                                                                                     0.24
0.3    0.14               0.20            0.3                                                    0.3                0.40                          0.3     0.19
                                  0.21                                                                                                                            0.34      0.34    0.33
0.2                                       0.2                                                    0.2                                              0.2
0.1                                       0.1                                                    0.1                                              0.1
0.0                                       0.0                                                    0.0                                              0.0
      GSM8K     MATH    Olymp.    Omni.         GSM8K          MATH      Olymp.      Omni.              GSM8K      MATH       Olymp.   Omni.            GSM8K     MATH     Olymp.   Omni.

                                                                 FPR (i.e. silent corrections)           FNR (i.e. error inducing)       AFFR (i.e. AF failure)


Figure 3: FPR, FNR, AFFR measures for the SOTA AF methods used across the 4 different datasets. The numbers in black
indicate the UFLB values. In all cases, large numbers indicate more unfaithful behaviour.

                Claude-Opus-4.7                                Gemini-3.1-Pro                                           GPT-5.2                                    Qwen-Plus
0.5                                       0.5                                                    0.5                                              0.5
0.4                                       0.4                                                    0.4                                              0.4
0.3                                       0.3                                                    0.3                                              0.3                       0.33    0.35
                                                                          0.16                                                 0.26                               0.28
                                                 0.08                                0.18                0.14       0.23               0.26
0.2    0.09                       0.14    0.2                  0.14                              0.2                                              0.2     0.17
                0.12      0.13
0.1                                       0.1                                                    0.1                                              0.1
0.0                                       0.0                                                    0.0                                              0.0
      GSM8K     MATH     Olymp.   Omni.         GSM8K          MATH      Olymp.      Omni.              GSM8K      MATH       Olymp.   Omni.            GSM8K     MATH     Olymp.   Omni.

                                                                FPR (i.e. silent corrections)           FNR (i.e. error inducing)        AFFR (i.e. AF failure)


              Figure 4: FPR, FNR, AFFR for the four general purpose LLMs, with UFLB scores shown on top in black.


is to be expected. Goedel is consistently the best (lowest) for                                        other 3 datasets, reflecting observations in the literature about
overall FNR, reflecting existing literature (Lin et al. 2025).                                         the difficulty of autoformalising real-world mathematical
                                                                                                       statements (Zhang, Valentino, and Freitas 2025).
FPR Goedel consistently attains the highest FPR, particu-
                                                                                                          When combining the 3 scores into our UFLB metric,
larly on the three more difficult datasets. Together with the
                                                                                                       Goedel leads the board, followed by Stepfun and, with a
FNR results and the uniformly high FPR on GSM8K across
                                                                                                       wider gap, by Kimina and Herald. Notice that Goedel attains
AFs, this suggests that Goedel is often successfully silently
                                                                                                       this lead despite having the highest FPR, with its advantage
correcting invalid statements while formalising them. While
                                                                                                       driven by its much lower FNR and AFFR.
this behaviour is likely a side effect of the model training, and
may be beneficial from a theorem-proving perspective, it is                                            6.2      General Purpose LLM Results
problematic when the AF is employed in a CoT verification
                                                                                                       Figure 4 illustrates FPR, FNR, AFFR and UFLB measures
pipeline, where invalidity preservation is essential.
                                                                                                       using four frontier models. Strikingly all models exhibit lower
AFFR The AFFR largely follows the FNR in ranking,                                                      levels of sycophancy than the specialised AFs. The models
with weaker models like Herald exhibiting the most failures.                                           with the lowest UFLB, Claude Opus 4.7 and Gemini 3.1
While most models have a relatively low AFFR for the easiest                                           Pro, improve on the best specialised AF (Goedel) on every
GSM8K, only Goedel manages below 10% failure for the                                                   dataset, driven primarily by substantially lower FPR, while
                                                                                            100%                                                                                              100%
        GSM8K           71.2           21.4          0.9                0.5           6.1                GSM8K          53.8              17.5          7.8             2.6            18.3
                                                                                            80%                                                                                               80%

         MATH           46.9           20.8          1.7                0.9          29.7   60%            MATH         28.9              14.0          4.5             1.5            51.2   60%

 OlympiadBench          37.3           18.0          3.3                0.7          40.7   40%    OlympiadBench        22.1              11.7          6.0             1.4            58.7   40%

                                                                                            20%                                                                                               20%
      OmniMATH          36.8           15.8          3.0                0.6          43.7             OmniMATH          23.6              11.6          7.7             1.2            55.9
                                                                                            0%                                                                                                0%

                                    y




                                                                                                                                      y
                                                     n



                                                                  on



                                                                                   ve




                                                                                                                                                       n



                                                                                                                                                                      n



                                                                                                                                                                                     ve
                        s




                                                                                                                         s
                                  nc




                                                                                                                                    nc
                     es




                                                                                                                      es
                                                  tio




                                                                                                                                                    io



                                                                                                                                                                    io
                                                                                 si




                                                                                                                                                                                     si
                                                                    i
                                                                 rs




                                                                                                                                                    t



                                                                                                                                                                  rs
                                  a




                                                                                                                                  ha
                   ln




                                                                                                                    ln
                                                en




                                                                                                                                                 en
                                                                               lu




                                                                                                                                                                                   lu
                                ph




                                                              ve




                                                                                                                                                                ve
                 fu




                                                                                                                  fu
                                                                              nc




                                                                                                                                                                                 nc
                                                                                                                                op
                                             st




                                                                                                                                               st
                              co
             ith




                                                            In




                                                                                                               ith




                                                                                                                                                              In
                                           Ab




                                                                                                                                             Ab
                                                                            co




                                                                                                                                                                               co
                                                                                                                                 c
                            Sy




                                                                                                                              Sy
           Fa




                                                                                                             Fa
                                                                         In




                                                                                                                                                                             In
                                           (a) Goedel                                                                                       (b) StepFun
                                                                                            100%                                                                                              100%
        GSM8K           43.2           21.9          10.8               3.6          20.5                GSM8K          28.4              21.6        12.6              2.3            35.1
                                                                                            80%                                                                                               80%

         MATH           19.0           13.2          7.5                1.8          58.5   60%            MATH         19.2              13.6          7.0             1.6            58.6   60%

 OlympiadBench          12.8           8.0           7.3                1.9          70.0   40%    OlympiadBench        14.9              8.8           9.2             1.5            65.6   40%

                                                                                            20%                                                                                               20%
      OmniMATH          15.3           9.6           8.2                2.1          64.8             OmniMATH          15.4              10.1          9.1             1.6            63.8
                                                                                            0%                                                                                                0%
                                      cy




                                                                                                                                       cy
                                                     n



                                                                  on



                                                                                   ve




                                                                                                                                                      n



                                                                                                                                                                         n



                                                                                                                                                                                      ive
                        s




                                                                                                                          s
                      es




                                                                                                                       es
                                                   tio




                                                                                                                                                    tio




                                                                                                                                                                      io
                                  an




                                                                                                                                     an
                                                                                si
                                                                    i




                                                                                                                                                                                    us
                                                                 rs




                                                                                                                                                                   rs
                   ln




                                                                                                                    ln
                                                en




                                                                                                                                                 en
                                                                                lu
                                 ph




                                                                                                                                  ph
                                                              ve




                                                                                                                                                                ve



                                                                                                                                                                                  cl
                 fu




                                                                                                                 fu
                                                                              nc
                                              st




                                                                                                                                               st




                                                                                                                                                                                 n
                             co




                                                                                                                                co
             th




                                                            In




                                                                                                               th




                                                                                                                                                              In
                                           Ab




                                                                                                                                             Ab
                                                                          co




                                                                                                                                                                              co
              i




                                                                                                                i
                            Sy




                                                                                                                              Sy
           Fa




                                                                                                             Fa
                                                                         In




                                                                                                                                                                             In
                                           (c) Kimina                                                                                           (d) Herald

Figure 5: Contingency analysis of unperturbed/perturbed pairs as defined in Section 4 for the analysed AFs on different datasets.


keeping FNR and AFFR low at the same time. AFFR is                                                                                   7          Conclusion
also generally lower for the frontier models than for the
specialised AFs, which can be explained by the considerably                                        Our results reveal a tension in current AF training: the systems
smaller size and context length of the latter. Finally, our                                        best at preserving validity on correct inputs are also the most
results indicate that the frontier models achieve uniformly                                        prone to silent correction on incorrect ones. This suggests
better invalidity preservation than the specialised AFs, and                                       that AF pipelines implicitly conflate faithful translation with
can be less unfaithful overall than every specialised AF.                                          producing a provable statement. This poses a pitfall in the
                                                                                                   CoT verification setting, where incorrect inputs are precisely
                                                                                                   the cases of interest.
6.3    Contingency Analysis                                                                           In our view, addressing this tension poses an important open
                                                                                                   problem for AF systems intended for verification. One natural
Figure 5 illustrates the relationships between unperturbed-                                        direction is to train AF systems with deliberate exposure
perturbed pairs following the 5 categories (described in Sec-                                      to invalid inputs, so they learn to preserve errors rather
tion 4) for the analysed AFs.                                                                      than repair them. Another is to extend the perturbation-
   Overall, the patterns from the figures reflect the previously                                   based methodology we propose to other natural-to-formal
reported results, with Goedel leading across the board on                                          translation tasks (e.g., formal specifications, code-from-spec)
Faithfulness and presenting the least Inconclusive, while also                                     where silent correction has similar costs.
having the highest sycophancy rate for MATH, OmniMath
and OlympiadBench. It is noticeable how the union of all
types of failures leads to high Inconclusive rates for the other                                                                          Limitations
3 AFs and how the edge cases of Abstention and Inversion                                           Our method does not assess semantic drift in full generality,
are low for every model.                                                                           and is therefore not complete: even if the UFLB metric is
   Focusing on Goedel, the contingency analysis aligns with                                        very small, this does not imply that the AF is necessarily
what we have observed already: excluding the inconclusive                                          faithful. For example, the AF in (6) would return a perfect
cases (comprising both prover and AF failures), we can see                                         UFLB score, but is clearly unfaithful. In addition, our method
that the Faithfulness and Sycophancy categories capture the                                        relies on access to a strong prover for the component Prove.
vast majority of cases, with Abstention and Inversion relegated                                    If this is not powerful enough, then the method may return
to edge cases. Moreover, Faithfulness and Sycophancy tend                                          inconclusive results even when applied to an AF that is clearly
to decrease together as the dataset becomes difficult. This                                        error inducing or silently correcting. Overall, we therefore
is unsurprising: since modern AFs are finetuned to produce                                         recommend that FaithformBench be used as one diagnos-
correct Lean proofs, silently correcting an error in the input                                     tic measure among others when evaluating autoformalisers,
while formalising it is a likely side effect of its training.                                      rather than as a complete certificate of reliability on its own.
                   Acknowledgements                                 Sketch, and Prove: Guiding Formal Theorem Provers with
RC was supported by the National Research Foundation,               Informal Proofs. In The Eleventh International Conference
Singapore, under a National Research Foundation Fellowship          on Learning Representations, ICLR 2023, Kigali, Rwanda,
in Artificial Intelligence (Award No. NRFFIAI1-2024-0014).          May 1-5, 2023. OpenReview.net.
   IG, PHY, SL, and LO were supported by the Singapore              Kirichenko, P.; Ibrahim, M.; Chaudhuri, K.; and Bell, S. J.
Global AI Venture Programme grant (AIVP-2024-002).                  2025. AbstentionBench: Reasoning LLMs Fail on Unanswer-
                                                                    able Questions. arXiv:2506.09038.
                         References                                 Lee, J.; Mukherjee, S.; Hakkani-Tur, D.; and Hockenmaier,
Anthropic. 2026. Claude Opus 4.7. Model announcement                J. 2025. ReasoningFlow: Semantic Structure of Complex
and documentation.                                                  Reasoning Traces. arXiv:2506.02532.
Chen, J.; Chen, W.; Du, J.; Hu, J.; Jiang, Z.; Jie, A.; Jin, X.;    Lightman, H.; Kosaraju, V.; Burda, Y.; Edwards, H.; Baker,
Jin, X.; Li, C.; Shi, W.; Wang, Z.; Wang, M.; Wei, C.; Wei,         B.; Lee, T.; Leike, J.; Schulman, J.; Sutskever, I.; and Cobbe,
S.; Xin, H.; Yang, F.; Gao, W.; Yuan, Z.; Zhan, T.; Zheng, Z.;      K. 2023. Let’s Verify Step by Step. arXiv:2305.20050.
Zhou, T.; and Zhu, T. H. 2025. Seed-Prover 1.5: Mastering           Lin, Y.; Tang, S.; Lyu, B.; Yang, Z.; Chung, J.; Zhao, H.;
Undergraduate-Level Theorem Proving via Learning from               Jiang, L.; Geng, Y.; Ge, J.; Sun, J.; Wu, J.; Gesi, J.; Lu, X.;
Experience. arXiv:2512.17260.                                       Acuna, D.; Yang, K.; Lin, H.; Choi, Y.; Chen, D.; Arora, S.;
Cobbe, K.; Kosaraju, V.; Bavarian, M.; Chen, M.; Jun, H.;           and Jin, C. 2025. Goedel-Prover-V2: Scaling Formal Theorem
Kaiser, L.; Plappert, M.; Tworek, J.; Hilton, J.; Nakano, R.;       Proving with Scaffolded Data Synthesis and Self-Correction.
Hesse, C.; and Schulman, J. 2021. Training Verifiers to Solve       CoRR, abs/2508.03613.
Math Word Problems. CoRR, abs/2110.14168.                           Liu, C.; Yuan, Y.; Yin, Y.; Xu, Y.; Xu, X.; Chen, Z.; Wang,
Coquand, T.; and Huet, G. 1988. The Calculus of Construc-           Y.; Shang, L.; Liu, Q.; and Zhang, M. 2025a. Safe: En-
tions. Information and Computation, 76(2–3): 95–120.                hancing Mathematical Reasoning in Large Language Models
de Moura, L.; and Ullrich, S. 2021. The Lean 4 Theorem              via Retrospective Step-aware Formal Verification. In Che,
Prover and Programming Language. In Automated Deduction             W.; Nabende, J.; Shutova, E.; and Pilehvar, M. T., eds., Pro-
– CADE 28, volume 12699 of Lecture Notes in Computer                ceedings of the 63rd Annual Meeting of the Association for
Science, 625–635. Springer.                                         Computational Linguistics (Volume 1: Long Papers), ACL
                                                                    2025, Vienna, Austria, July 27 - August 1, 2025, 12171–12186.
Gao, B.; Song, F.; Yang, Z.; Cai, Z.; Miao, Y.; Dong, Q.; Li,
                                                                    Association for Computational Linguistics.
L.; Ma, C.; Chen, L.; Xu, R.; Tang, Z.; Wang, B.; Zan, D.;
Quan, S.; Zhang, G.; Sha, L.; Zhang, Y.; Ren, X.; Liu, T.;          Liu, Q.; Zheng, X.; Lu, X.; Cao, Q.; and Yan, J. 2025b.
and Chang, B. 2024a. Omni-MATH: A Universal Olympiad                Rethinking and Improving Autoformalization: Towards a
Level Mathematic Benchmark For Large Language Models.               Faithful Metric and a Dependency Retrieval-based Approach.
ArXiv, abs/2410.07985.                                              In The Thirteenth International Conference on Learning
Gao, G.; Wang, Y.; Jiang, J.; Gao, Q.; Qin, Z.; Xu, T.; and         Representations, ICLR 2025, Singapore, April 24-28, 2025.
Dong, B. 2024b. Herald: A Natural Language Annotated                OpenReview.net.
Lean 4 Dataset. CoRR, abs/2410.10878.                               Liu, Y.; Liu, X.; Sun, Z.; and Hu, W. 2026. Answering
Google. 2026. Gemini 3.1 Pro: A smarter model for your most         the Unanswerable Is to Err Knowingly: Analyzing and Mit-
complex tasks. Model announcement and documentation.                igating Abstention Failures in Large Reasoning Models.
                                                                    arXiv:2508.18760.
He, C.; Luo, R.; Bai, Y.; Hu, S.; Thai, Z. L.; Shen, J.; Hu, J.;
Han, X.; Huang, Y.; Zhang, Y.; Liu, J.; Qi, L.; Liu, Z.; and Sun,   Liu, Y.; Zhu, T.; Liu, X.; Chen, Y.; ZhaoXuan, L.; Zhang,
M. 2024. OlympiadBench: A Challenging Benchmark for                 J.; Bao, K.; Luo, T.; et al. 2025c. Generalized Tree Edit
Promoting AGI with Olympiad-Level Bilingual Multimodal              Distance (GTED): A Faithful Evaluation Metric for Statement
Scientific Problems. In Ku, L.; Martins, A.; and Srikumar,          Autoformalization. In 2nd AI for Math Workshop @ ICML
V., eds., Proceedings of the 62nd Annual Meeting of the             2025.
Association for Computational Linguistics (Volume 1: Long           Miao, N.; Teh, Y. W.; and Rainforth, T. 2023. SelfCheck:
Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024,           Using LLMs to Zero-Shot Check Their Own Step-by-Step
3828–3850. Association for Computational Linguistics.               Reasoning. CoRR, abs/2308.00436.
Hendrycks, D.; Burns, C.; Kadavath, S.; Arora, A.; Basart,          OpenAI. 2025. GPT-5 System Card. Technical report, OpenAI.
S.; Tang, E.; Song, D.; and Steinhardt, J. 2021. Measuring          System card / technical report for the GPT-5 family.
Mathematical Problem Solving With the MATH Dataset.                 Paulson, L. C. 1990. Isabelle: The Next 700 Theorem Provers.
CoRR, abs/2103.03874.                                               In Odifreddi, P., ed., Logic and Computer Science, 361–386.
Jana, P.; Kale, K.; Tanriverdi, A. E.; Song, C.; Vishwanath,        London: Academic Press.
S.; and Ganesh, V. 2025. ProofBridge: Auto-formalization            Perez, E.; Ringer, S.; Lukosiute, K.; Nguyen, K.; Chen, E.;
of Natural Language Proofs in Lean via Joint Embeddings.            Heiner, S.; Pettit, C.; Olsson, C.; Kundu, S.; Kadavath, S.;
CoRR, abs/2510.15681.                                               Jones, A.; Chen, A.; Mann, B.; Israel, B.; Seethor, B.; McK-
Jiang, A. Q.; Welleck, S.; Zhou, J. P.; Lacroix, T.; Liu, J.;       innon, C.; Olah, C.; Yan, D.; Amodei, D.; Amodei, D.; Drain,
Li, W.; Jamnik, M.; Lample, G.; and Wu, Y. 2023. Draft,             D.; Li, D.; Tran-Johnson, E.; Khundadze, G.; Kernion, J.;
Landis, J.; Kerr, J.; Mueller, J.; Hyun, J.; Landau, J.; Ndousse,   11953–11974. Miami, Florida, USA: Association for Compu-
K.; Goldberg, L.; Lovitt, L.; Lucas, M.; Sellitto, M.; Zhang,       tational Linguistics.
M.; Kingsland, N.; Elhage, N.; Joseph, N.; Mercado, N.; Das-        Wu, Y.; Huang, D.; Wan, R.; Peng, Y.; Shang, S.; Cao,
Sarma, N.; Rausch, O.; Larson, R.; McCandlish, S.; Johnston,        C.; Qi, L.; Zhang, R.; Du, Z.; Yang, J.; and Hu, X. 2025.
S.; Kravec, S.; El Showk, S.; Lanham, T.; Telleen-Lawton,           StepFun-Formalizer: Unlocking the Autoformalization Poten-
T.; Brown, T.; Henighan, T.; Hume, T.; Bai, Y.; Hatfield-           tial of LLMs through Knowledge-Reasoning Fusion. CoRR,
Dodds, Z.; Clark, J.; Bowman, S. R.; Askell, A.; Grosse, R.;        abs/2508.04440.
Hernandez, D.; Ganguli, D.; Hubinger, E.; Schiefer, N.; and
Kaplan, J. 2023. Discovering Language Model Behaviors               Wu, Y.; Jiang, A. Q.; Li, W.; et al. 2022. Autoformalization
with Model-Written Evaluations. In Rogers, A.; Boyd-Graber,         with Large Language Models. In Advances in Neural Infor-
J.; and Okazaki, N., eds., Findings of the Association for Com-     mation Processing Systems, volume 35. Curran Associates,
putational Linguistics: ACL 2023, 13387–13434. Toronto,             Inc.
Canada: Association for Computational Linguistics.                  Xin, H.; Ren, Z.; Song, J.; Shao, Z.; Zhao, W.; Wang, H.;
Petrov, I.; Dekoninck, J.; and Vechev, M. T. 2025. BrokenMath:      Liu, B.; Zhang, L.; Lu, X.; Du, Q.; Gao, W.; Zhang, H.; Zhu,
A Benchmark for Sycophancy in Theorem Proving with LLMs.            Q.; Yang, D.; Gou, Z.; Wu, Z.; Luo, F.; and Ruan, C. 2025.
CoRR, abs/2510.04721.                                               DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback
Quan, X.; Valentino, M.; Dennis, L. A.; and Freitas, A. 2025.       for Reinforcement Learning and Monte-Carlo Tree Search.
Faithful and Robust LLM-Driven Theorem Proving for NLI              In The Thirteenth International Conference on Learning
Explanations. In Che, W.; Nabende, J.; Shutova, E.; and             Representations.
Pilehvar, M. T., eds., Proceedings of the 63rd Annual Meeting       Xiong, Z.; Cai, Y.; Li, Z.; and Wang, Y. 2025. Mapping
of the Association for Computational Linguistics (Volume 1:         the Minds of LLMs: A Graph-Based Analysis of Reasoning
Long Papers). Association for Computational Linguistics.            LLMs. In Christodoulopoulos, C.; Chakraborty, T.; Rose,
Qwen Team. 2025. Qwen3 Technical Report. Technical                  C.; and Peng, V., eds., Proceedings of the 2025 Confer-
report, Alibaba Group. Technical report for the Qwen3 model         ence on Empirical Methods in Natural Language Processing,
family.                                                             17751–17763. Suzhou, China: Association for Computational
Ren, Z. Z.; Shao, Z.; Song, J.; Xin, H.; Wang, H.; Zhao,            Linguistics. ISBN 979-8-89176-332-6.
W.; Zhang, L.; Fu, Z.; Zhu, Q.; Yang, D.; Wu, Z. F.; Gou,           Xue, B.; Zhu, Q.; Wang, R.; Wang, S.; Wang, H.; Hu, M.; Mi,
Z.; Ma, S.; Tang, H.; Liu, Y.; Gao, W.; Guo, D.; and Ruan,          F.; Wang, Y.; Shang, L.; Liu, Q.; and Wong, K.-F. 2025. Reli-
C. 2025. DeepSeek-Prover-V2: Advancing Formal Mathe-                ableMath: Benchmark of Reliable Mathematical Reasoning
matical Reasoning via Reinforcement Learning for Subgoal            on Large Language Models. arXiv:2507.03133.
Decomposition. CoRR, abs/2504.21801.                                Yang, K.; Swope, A.; Gu, A.; Chalamala, R.; Song, P.; Yu, S.;
Sharma, M.; Tong, M.; Korbak, T.; Duvenaud, D.; Askell, A.;         Godil, S.; Prenger, R.; and Anandkumar, A. 2023. LeanDojo:
Bowman, S. R.; Durmus, E.; Hatfield-Dodds, Z.; Johnston,            Theorem Proving with Retrieval-Augmented Language Mod-
S. R.; Kravec, S.; Maxwell, T.; McCandlish, S.; Ndousse,            els. In Neural Information Processing Systems (NeurIPS).
K.; Rausch, O.; Schiefer, N.; Yan, D.; Zhang, M.; and Perez,
                                                                    Zhang, L.; Valentino, M.; and Freitas, A. 2025. Autoformal-
E. 2024. Towards Understanding Sycophancy in Language
                                                                    ization in the Wild: Assessing LLMs on Real-World Mathe-
Models. In The Twelfth International Conference on Learning
                                                                    matical Definitions. In Christodoulopoulos, C.; Chakraborty,
Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024.
                                                                    T.; Rose, C.; and Peng, V., eds., Proceedings of the 2025
OpenReview.net.
                                                                    Conference on Empirical Methods in Natural Language Pro-
Wang, H.; Unsal, M.; Lin, X.; Baksys, M.; Liu, J.; Santos,          cessing. Association for Computational Linguistics.
M. D.; Sung, F.; Vinyes, M.; Ying, Z.; Zhu, Z.; Lu, J.; Saxcé,
H. d.; Bailey, B.; Song, C.; Xiao, C.; Zhang, D.; Zhang,            Zheng, C.; Zhang, Z.; Zhang, B.; Lin, R.; Lu, K.; Yu, B.; Liu,
E.; Pu, F.; Zhu, H.; Liu, J.; Bayer, J.; Michel, J.; Yu, L.;        D.; Zhou, J.; and Lin, J. 2025. ProcessBench: Identifying Pro-
Dreyfus-Schmidt, L.; Tunstall, L.; Pagani, L.; Machado, M.;         cess Errors in Mathematical Reasoning. In Che, W.; Nabende,
Bourigault, P.; Wang, R.; Polu, S.; Barroyer, T.; Li, W.-D.;        J.; Shutova, E.; and Pilehvar, M. T., eds., Proceedings of the
Niu, Y.; Fleureau, Y.; Hu, Y.; Yu, Z.; Wang, Z.; Yang, Z.; Liu,     63rd Annual Meeting of the Association for Computational
Z.; and Li, J. 2025. Kimina-Prover Preview: Towards Large           Linguistics (Volume 1: Long Papers), ACL 2025, Vienna,
Formal Reasoning Models with Reinforcement Learning.                Austria, July 27 - August 1, 2025, 1009–1024. Association
                                                                    for Computational Linguistics.
Wang, H.; Xin, H.; Zheng, C.; Liu, Z.; Cao, Q.; Huang,
Y.; Xiong, J.; Shi, H.; Xie, E.; Yin, J.; Li, Z.; and Liang,        Zheng, L.; Chiang, W.-L.; Sheng, Y.; Zhuang, S.; Wu, Z.;
X. 2024a. LEGO-Prover: Neural Theorem Proving with                  Zhuang, Y.; Lin, Z.; Li, Z.; Li, D.; Xing, E. P.; Zhang, H.;
Growing Libraries. In The Twelfth International Conference          Gonzalez, J. E.; and Stoica, I. 2023. Judging LLM-as-a-
on Learning Representations.                                        Judge with MT-Bench and Chatbot Arena. arXiv preprint
Wang, R.; Zhang, J.; Jia, Y.; Pan, R.; Diao, S.; Pi, R.; and        arXiv:2306.05685.
Zhang, T. 2024b. TheoremLlama: Transforming General-                Zhou, J. P.; Staats, C.; Li, W.; Szegedy, C.; Weinberger, K. Q.;
Purpose LLMs into Lean4 Experts. In Al-Onaizan, Y.; Bansal,         and Wu, Y. 2024. Don’t Trust: Verify - Grounding LLM
M.; and Chen, Y.-N., eds., Proceedings of the 2024 Confer-          Quantitative Reasoning with Auto-formalisation. In ICLR,
ence on Empirical Methods in Natural Language Processing,           1–20.
Zhou, K.; and Zhang, L. 2025. Step-Wise Formal Verifica-
tion for LLM-Based Mathematical Problem Solving. arXiv
preprint arXiv:2505.20869.
                                                 A     Benchmark Details
As part of our contributions, we release the FaithformBench benchmark together with two derived artefact datasets (Faithform-AF
and Faithform-LLMs) we produced in performing the experiments described in the main paper, in the hope they might foster
further research in the area. We also release the version of the benchmark including Regex perturbations (see Appendix C),
instead of LLM ones (FaithformBench-Regex). More details about such datasets are included below:

A.1   Benchmark A: FaithformBench
Description This benchmark evaluates step-level autoformalisation of mathematical chain-of-thought (CoT) reasoning under
clean and perturbed conditions.
Task Definition. Each instance corresponds to a single reasoning step extracted from a verified mathematical CoT. Given the
natural-language step and associated metadata, models are evaluated on producing a correct formal representation consistent with
the proof context.
Data Source. The dataset is derived from ProcessBench, which aggregates CoT solutions for mathematical problems from
GSM8K, MATH, OlympiadBench, and OmniMath. ProcessBench augments these problems with reasoning chains generated by
Qwen-2.5-Instruct and Llama-3-Instruct. While prompting details are not fully specified, the resulting outputs are structured
into discrete reasoning steps.
Data Construction. Only reasoning chains verified as correct by ProcessBench are retained. These chains are decomposed into
individual steps, each annotated with dependency and inference metadata. Each verifiable step is then paired with a perturbed
counterpart generated by the BrokenMath-style LLM-based perturbation function described in the main paper. Perturbations
operate at the step level and preserve the original problem identity.
Dataset Statistics. The benchmark contains 27,866 reasoning steps spanning 1,179 unique problems: 15,082 original steps
extracted from the reasoning chains, of which 12,784 are verifiable, plus the 12,784 LLM-perturbed counterparts of the verifiable
steps. The remaining 2,298 original steps are unverifiable (declarative) statements, which are retained as context for dependent
steps but excluded from the analysis. The resulting 25,568 verifiable steps, divided equally among perturbed and unperturbed
ones, are those analysed in the main text. A summary of the dataset fields is shown in Table 1.

               Field                        Description
               step_content                 Natural-language reasoning step
               is_perturbed                 Perturbation indicator
               type_of_perturbation         {unperturbed, brokenmath-style_llm}
               problem_id                   Source problem identifier
               node_id                      Step index within CoT
               statement_type               e.g., computation, logical
               proof_type                   {deduction, assumption, axiom}; predominantly deduction
               depencies                    References to prior steps (field name as released)
               dependencies_content         Contents of the referenced prior steps
               inference_rule               Inference rule identified in pre-processing (may be missing), e.g. arithmetic
               verification_note            Notes for verification from pre-processing step

                                         Table 1: Schema for Benchmark A instances.

  The majority of steps correspond to computational reasoning, with arithmetic inference rules being the most frequent.

A.2   Benchmark B: FaithformBench-Regex
Description This benchmark is the counterpart of FaithformBench in which the perturbed steps are produced by the rule-based
(regex) perturbation strategy mentioned in the main paper, rather than by the LLM-based one. It supports the comparison between
perturbation strategies reported in Appendix C.
Task Definition. Identical to Benchmark A: each instance corresponds to a single reasoning step extracted from a verified
mathematical CoT, and models are evaluated on producing a correct formal representation consistent with the proof context.
Data Source. Identical to Benchmark A: the dataset is derived from the error-free subset of ProcessBench, decomposed into
individual reasoning steps with dependency and inference metadata.
Data Construction. The unperturbed steps are exactly those of Benchmark A. Each verifiable step is paired with a perturbed
counterpart generated by the rule-based regex perturbation function (seeded, and hence reproducible). Perturbations operate at
the step level and preserve the original problem identity.
   Field                           Description
   step_content                    Natural-language reasoning step
   is_perturbed                    Perturbation indicator
   type_of_perturbation            {unperturbed, regex_perturbed, brokenmath-style_llm}
   problem_id                      Source problem identifier
   node_id                         Step index within CoT
   autoformaliser_model            {Goedel, Kimina, Stepfun, Herald}
   autoformaliser_output           The autoformalised Lean statement (without proof) corresponding to step_content
   prover_output                   The output of the prover, i.e. the autoformalised Lean statement, but this time with proof.
   proof_result                    {AF-Fail, Inconclusive, Proved, Refuted}

                                          Table 2: Schema for Benchmark C instances.


Dataset Statistics. The benchmark contains 27,866 reasoning steps spanning 1,179 unique problems: 15,082 original steps
extracted from the reasoning chains, of which 12,784 are verifiable, plus the 12,784 regex-perturbed counterparts of the verifiable
steps. The remaining 2,298 original steps are unverifiable (declarative) statements, which are retained as context for dependent
steps but excluded from the analysis. The schema is identical to that of Benchmark A (Table 1), with type_of_perturbation
taking values in {unperturbed, regex_perturbed}.

A.3    Benchmark C: Faithform-AF
Goal. This benchmark evaluates the quality and usability of automatically generated Lean statements and proofs corresponding
to mathematical chain-of-thought (CoT) reasoning steps. It is intended for training and evaluating LLM-based autoformalisers for
automatic verification of CoTs.
Task Definition. Each instance augments a reasoning step from Benchmark A with an autoformalised Lean statement and proof.
Given the natural-language step and metadata, models are evaluated on producing or verifying Lean formalisations consistent
with the mathematical intent of the step.
Data Source. The benchmark is constructed by applying four state-of-the-art autoformalisation models (Goedel (8B), Kimina
(7B), Stepfun (7B), and Herald (7B)) to all verifiable instances of Benchmark A. For each reasoning step, the corresponding
Lean statement and proof produced by each model are recorded.
Data Construction. For every verifiable step in Benchmark A, each autoformalisation model generates a Lean formalisation.
The resulting statements and proofs are evaluated using the verification protocol described in the main paper, and the outcomes
are stored alongside the original step metadata. This produces one instance per (reasoning step, autoformaliser) pair, preserving
perturbation labels and problem identities from Benchmark A.
Dataset Statistics. The benchmark contains 102,272 instances corresponding to the 4 autoformalisations of each of the
25,568 verifiable steps of Benchmark A (unperturbed and LLM-perturbed). The release additionally contains the 51,136
autoformalisations of the 12,784 regex-perturbed variants from Benchmark B, which support the perturbation-robustness analysis
of Appendix C, for a total of 153,408 instances. A summary of the dataset schema is provided in Table 2.
Summary Statistics. The dataset spans 1,179 unique problems and 38,352 unique reasoning steps (12,784 unperturbed,
12,784 LLM-perturbed and 12,784 regex-perturbed). Each step is paired with four autoformalisations. The majority of instances
correspond to computational reasoning with arithmetic inference rules.
Intended Use. This benchmark is designed for fine-tuning and evaluating LLM-based autoformalisers, particularly for automatic
verification and robustness analysis of mathematical CoTs.

A.4    Benchmark D: Faithform-LLMs
This benchmark is exactly the same as Faithform-AF, but this time it is constructed by applying four frontier LLMs—GPT 5.2,
Gemini 3.1 Pro, Qwen Plus, and Claude Opus 4.7—to the reasoning steps in Benchmark A. Models are prompted to generate
unproved Lean statements as in the previous case; the full prompt specification is provided in Appendix G.

A.5    Benchmark-specific Limitations.
These limitations concern the released artefacts specifically; for the limitations of our methodology and findings, we refer
the reader to the Limitations section of the main paper. Lean formalisations inherit errors and biases from the underlying
autoformalisation models. Verification outcomes reflect both reasoning quality and idiosyncrasies of Lean proof search. The
benchmark does not enforce global proof coherence across full reasoning chains.
A.6    Data and Code release.
To obtain the datasets described in this appendix, together with the code used to generate and evaluate them, see the project
repository at https://github.com/Ighina/FaithformBench.

                                                      B    Detailed Results
In Table 3, we include the tables describing the detailed occurrences of each outcome category for all four fine-tuned AFs and all
four general-purpose LLMs across the 4 datasets. Specifically, we identified 4 possible outcomes:
1. Proved: this is equivalent to the ⊤ in the main text, that is: the prover could generate a correct proof for the input statement but
    not for its negation.
2. Refuted: this is equivalent to the ⊥ in the main text, that is: the prover could generate a correct proof for the negation of the
    input statement but not for the input statement.
3. AF-Fail: this represents a failure of the autoformalisation step, i.e. the case in which AF(x) = ∅ in the main text. It aggregates
    extraction failures and type-check failures.
4. Inconclusive: the autoformaliser did not fail, but the prover could not establish either the statement or its negation. This
    includes cases where the prover’s output did not compile, or where it altered the input formalised statement (beyond replacing
    the by sorry) rather than proving it as given. These occurrences are not counted as failure events in the main analysis; they
    only contribute to the total number N of elements considered.
   The results mostly reflect what we observed in the main text, but this time showing the individual results for the perturbed sets
(1st and 3rd rows) and the unperturbed ones (2nd and 4th). The corresponding results for the regex-perturbed variants of the same
steps, together with a comparison between the two perturbation strategies, are reported in Appendix C.
   The Proved and Refuted columns clearly highlight how the general LLMs are generally quite good in our case, especially if we
look at Claude Opus 4.7 and Gemini 3.1 Pro, where the first exhibits the most occurrences in Proved for the unperturbed cases,
while Gemini 3.1 Pro has the highest Refuted count for the perturbed ones. Both have a relatively low number of AF-Fail and
Inconclusive over all.

                                        C     Robustness to Perturbation Method
The results in the main text (and in Appendix B) are obtained with the BrokenMath-style LLM-based perturbation function (Petrov,
Dekoninck, and Vechev 2025). A natural question is whether our conclusions depend on this particular choice of Pert. To assess
this, we repeated the full evaluation of the four fine-tuned autoformalisers on FaithformBench-Regex (see Appendix A), in which
each verifiable step is instead paired with a counterpart produced by a rule-based, regex perturbation function.
Regex-based perturbation function. The regex perturber applies a hierarchy of regular-expression-based transformations. It
first attempts two numeric edits: changing the rightmost numeric literal (by a random offset of up to half its magnitude) and
swapping an arithmetic or comparison operator (biased towards the rightmost occurrence); both edits can apply to the same step
and, as most steps contain equations, they successfully perturb the majority of the dataset. Only when neither edit applies does
the perturber fall back to negation: if the statement already contains a “not” it removes it, otherwise it inserts “not” after the first
modal or copular verb (e.g., transforming “is larger than” into “is not larger than”); as a final fallback, it prepends the string “It is
false that” to the entire statement. Unlike the LLM-based perturber, this procedure is LLM-free and fully reproducible given the
fixed random seed of our released configuration, but it is also more templated and can occasionally produce a statement that
is still true (e.g., turning “17 is odd” into “13 is odd”), which motivated our choice of the LLM-based strategy as the primary
perturbation method.
Full regex results. Table 4 reports the detailed outcome counts of the four fine-tuned autoformalisers on the regex-perturbed
steps, in the same format as Table 3; the unperturbed rows are identical to those of Table 3 and are not repeated.
Comparison with the LLM-based perturbations. Table 5 reports, for every autoformaliser, dataset and outcome category,
the difference (in percentage points) between the outcome shares obtained under the regex-based and the LLM-based (BK)
perturbations.
   The two perturbation strategies yield closely aligned outcome distributions: the mean absolute difference across all model–
dataset–outcome cells is 2.5 percentage points (1.4 for Herald, 2.0 for Kimina, 2.5 for Stepfun and 4.2 for Goedel), and the
relative ranking of the four autoformalisers on every dataset is unchanged. AF-Fail rates in particular are almost identical under
the two strategies (mean absolute difference of 1.1 percentage points), confirming that the perturbation method does not affect the
models’ ability to produce well-formed Lean output.
   The only sizeable deviation concerns Goedel on the three harder datasets (MATH, OlympiadBench, OmniMATH), where
roughly 9–11 percentage points of mass move from Refuted to Proved when switching from the LLM-based to the regex-based
perturbations. This is consistent with the more templated nature of the regex perturbations, which makes the injected error easier
for a strong model to detect and silently correct; it therefore reinforces, rather than contradicts, the main finding that Goedel is the
autoformaliser most prone to silent correction. Overall, we conclude that our results, and all qualitative conclusions drawn from
them in the main text, are robust to the choice of perturbation method.
                                   Goedel                                                Kimina                                                 Stepfun                                             Herald
                                 (perturbed)                                           (perturbed)                                            (perturbed)                                         (perturbed)
                                                                                                                                                                                                                                    100%

       GSM8K        22           948               15       297          29            729            172          352           37           840            132          273         151         590              182       359
                                                                                                                                                                                                                                    80%


         MATH      187           2,184          659        1,011        957            1,309          1,018        757           865          1,572          847          757         1,259       1,346            645       791    60%



                                                                                                                                                                                                                                    40%
 OlympiadBench     295           2,239          1,030      1,009        1,361          1,211          1,370        631           965          1,601          1,284        723         1,605       1,488            837       643

                                                                                                                                                                                                                                    20%
    OmniMATH       239           1,396          679         574         868            823            739          458           563          1,072          795          458         1,012       934              487       455
                                                                                                                                                                                                                                    0%

                                 Goedel                                                Kimina                                                  Stepfun                                              Herald
                              (unperturbed)                                         (unperturbed)                                           (unperturbed)                                        (unperturbed)
                                                                                                                                                                                                                                    100%

       GSM8K        18             17              34      1,213         30            209            122          921           35           149            102          996         177         218              144       743
                                                                                                                                                                                                                                    80%


         MATH      212           128            558        3,143        972            518            712         1,839          793          338            671         2,239        1,217       474              549      1,801   60%



                                                                                                                                                                                                                                    40%
 OlympiadBench     342           221            885        3,125        1,383          636            1,014       1,540          902          480            960         2,231        1,570       709              730      1,564

                                                                                                                                                                                                                                    20%
    OmniMATH       276           139            612        1,861        863            429            625          971           551          354            620         1,363        990         432              439      1,027
                                                                                                                                                                                                                                    0%

                                   GPT-5.2                                         Gemini-3.1-Pro                                         Claude-Opus-4.7                                          Qwen-Plus
                                 (perturbed)                                        (perturbed)                                             (perturbed)                                           (perturbed)
                                                                                                                                                                                                                                    100%

       GSM8K        19           1,039             37       187            0           1,236               7           39        22           1,097               6       157         108         863              194       117
                                                                                                                                                                                                                                    80%


         MATH      418           2,728          416         479         228            3,256          355          202           208          3,160          311          362         821         2,044            825       351    60%



                                                                                                                                                                                                                                    40%
 OlympiadBench     501           3,000          593         479         197            3,640          503          233           178          3,518          442          435         1,094       1,948            1,108     423

                                                                                                                                                                                                                                    20%
    OmniMATH       365           1,788          381         354         213            2,177          314          184           178          2,098          325          287         745         1,277            569       297
                                                                                                                                                                                                                                    0%

                                 GPT-5.2                                           Gemini-3.1-Pro                                         Claude-Opus-4.7                                          Qwen-Plus
                              (unperturbed)                                        (unperturbed)                                           (unperturbed)                                         (unperturbed)
                                                                                                                                                                                                                                    100%

       GSM8K        20           122               27      1,113           1           170                 9      1,102          30              26               8      1,218        158             54           155       915
                                                                                                                                                                                                                                    80%


         MATH      447           536            349        2,709        241            477            290         3,033          238          173            293         3,337        818         291              802      2,130   60%



                                                                                                                                                                                                                                    40%
 OlympiadBench     481           895            621        2,576        195            819            408         3,151          195          384            346         3,648        1,077       427              1,047    2,022

                                                                                                                                                                                                                                    20%
    OmniMATH       336           462            350        1,740        213            443            283         1,949          193          170            261         2,264        725         260              584      1,319
                                                                                                                                                                                                                                    0%
                                 D




                                                                                       D




                                                                                                                                              D




                                                                                                                                                                                                  D
                   L




                                                E



                                                            D




                                                                        L




                                                                                                      VE




                                                                                                                   D




                                                                                                                                 L




                                                                                                                                                             VE




                                                                                                                                                                          D




                                                                                                                                                                                      L




                                                                                                                                                                                                                 VE




                                                                                                                                                                                                                             D
                   AI




                                                                      AI




                                                                                                                               AI




                                                                                                                                                                                    AI
                                               V
                              TE




                                                                                    TE




                                                                                                                                            TE




                                                                                                                                                                                                 TE
                                                           VE




                                                                                                                  VE




                                                                                                                                                                         VE




                                                                                                                                                                                                                            VE
                                            SI




                                                                                                  SI




                                                                                                                                                          SI




                                                                                                                                                                                                               SI
                 -F




                                                                    -F




                                                                                                                             -F




                                                                                                                                                                                  -F
                             U




                                                                                   U




                                                                                                                                          U




                                                                                                                                                                                              U
                                                          O




                                                                                                                 O




                                                                                                                                                                        O




                                                                                                                                                                                                                           O
                                           LU




                                                                                                 LU




                                                                                                                                                        LU




                                                                                                                                                                                                              LU
             AF




                                                                   AF




                                                                                                                            AF




                                                                                                                                                                                 AF
                         EF




                                                                               EF




                                                                                                                                       EF




                                                                                                                                                                                            EF
                                                        PR




                                                                                                               PR




                                                                                                                                                                      PR




                                                                                                                                                                                                                         PR
                                        C




                                                                                             C




                                                                                                                                                      C




                                                                                                                                                                                                           C
                         R




                                                                               R




                                                                                                                                      R




                                                                                                                                                                                          R
                                       N




                                                                                             N




                                                                                                                                                    N




                                                                                                                                                                                                          N
                                      O




                                                                                            O




                                                                                                                                                   O




                                                                                                                                                                                                       O
                                   C




                                                                                         C




                                                                                                                                                 C




                                                                                                                                                                                                      C
                                 IN




                                                                                       IN




                                                                                                                                              IN




                                                                                                                                                                                                  IN




Table 3: Detailed results of the four fine-tuned autoformalisers (top two rows: perturbed, unperturbed) and four frontier
general-purpose LLMs used as formalisers (bottom two rows: perturbed, unperturbed) on the four datasets. The perturbed rows
use the LLM-based approach to perturbations described above. AF-FAIL aggregates extraction failures and type-check failures.
Results for the regex-perturbed variants are reported in Appendix C.



                                                                                                  D             Pre-processing

In this part we describe in more depth the various pre-processing steps that we have performed to obtain the final reasoning
chains used in our main experiments.
                                Goedel                                               Kimina                                            Stepfun                                           Herald
                           (regex-perturbed)                                    (regex-perturbed)                                 (regex-perturbed)                                 (regex-perturbed)
                                                                                                                                                                                                                        100%

       GSM8K         17          917             25       323          25           765            118       374         40           764             180       298        148          626             172       336
                                                                                                                                                                                                                        80%


         MATH       176         1,761           658      1,446        1,022         1,370          861       788         851          1,457           774       959        1,183        1,336           666       856   60%



                                                                                                                                                                                                                        40%
 OlympiadBench      281         1,762           1,027    1,503        1,506         1,179          1,196     692         968          1,392           1,338     875        1,444        1,548           864       717

                                                                                                                                                                                                                        20%
    OmniMATH        236         1,147           676       829         930           844            647       467         555          955             815       563        950          980             470       488
                                                                                                                                                                                                                        0%
                                 D




                                                                                    D




                                                                                                                                      D




                                                                                                                                                                                        D
                     L




                                               VE




                                                          D




                                                                      L




                                                                                                   VE




                                                                                                             D




                                                                                                                         L




                                                                                                                                                      VE




                                                                                                                                                                D




                                                                                                                                                                            L




                                                                                                                                                                                                        VE




                                                                                                                                                                                                                   D
                   AI




                                                                    AI




                                                                                                                       AI




                                                                                                                                                                         AI
                                TE




                                                                                 TE




                                                                                                                                    TE




                                                                                                                                                                                      TE
                                                         VE




                                                                                                            VE




                                                                                                                                                               VE




                                                                                                                                                                                                                 VE
                                             SI




                                                                                                 SI




                                                                                                                                                   SI




                                                                                                                                                                                                     SI
                 -F




                                                                  -F




                                                                                                                     -F




                                                                                                                                                                       -F
                            U




                                                                                U




                                                                                                                                  U




                                                                                                                                                                                    U
                                                        O




                                                                                                           O




                                                                                                                                                              O




                                                                                                                                                                                                                O
                                           LU




                                                                                              LU




                                                                                                                                                 LU




                                                                                                                                                                                                   LU
             AF




                                                                 AF




                                                                                                                    AF




                                                                                                                                                                      AF
                           EF




                                                                            EF




                                                                                                                               EF




                                                                                                                                                                                 EF
                                                      PR




                                                                                                         PR




                                                                                                                                                            PR




                                                                                                                                                                                                              PR
                                         C




                                                                                             C




                                                                                                                                               C




                                                                                                                                                                                                 C
                          R




                                                                            R




                                                                                                                              R




                                                                                                                                                                                R
                                       N




                                                                                          N




                                                                                                                                             N




                                                                                                                                                                                               N
                                      O




                                                                                         O




                                                                                                                                           O




                                                                                                                                                                                             O
                                     C




                                                                                      C




                                                                                                                                         C




                                                                                                                                                                                           C
                                 IN




                                                                                    IN




                                                                                                                                      IN




                                                                                                                                                                                        IN
Table 4: Detailed results of the four fine-tuned autoformalisers on the regex-perturbed variants of the 12,784 verifiable steps,
across the four datasets. Cells report absolute counts and row-normalised percentages, in the same format as Table 3. AF-FAIL
aggregates extraction failures and type-check failures.

                                                      Model      Dataset                                ∆AF-Fail ∆Refuted ∆Inconcl. ∆Proved
                                                      Goedel     GSM8K                                       −0.4              −2.4                         +0.8        +2.0
                                                                 MATH                                        −0.3             −10.5                         −0.0       +10.8
                                                                 OlympiadBench                               −0.3             −10.4                         −0.1       +10.8
                                                                 OmniMATH                                    −0.1              −8.6                         −0.1        +8.8
                                                      Kimina GSM8K                                           −0.3                 +2.8                      −4.2           +1.7
                                                             MATH                                            +1.6                 +1.5                      −3.9           +0.8
                                                             OlympiadBench                                   +3.2                 −0.7                      −3.8           +1.3
                                                             OmniMATH                                        +2.1                 +0.7                      −3.2           +0.3
                                                      Stepfun GSM8K                                          +0.2                 −5.9                      +3.7           +2.0
                                                              MATH                                           −0.3                 −2.8                      −1.8           +5.0
                                                              OlympiadBench                                  +0.1                 −4.6                      +1.2           +3.3
                                                              OmniMATH                                       −0.3                 −4.1                      +0.7           +3.6
                                                      Herald     GSM8K                                       −0.2                 +2.8                      −0.8           −1.8
                                                                 MATH                                        −1.9                 −0.2                      +0.5           +1.6
                                                                 OlympiadBench                               −3.5                 +1.3                      +0.6           +1.6
                                                                 OmniMATH                                    −2.1                 +1.6                      −0.6           +1.1

Table 5: Difference in outcome shares (percentage points, regex-perturbed minus LLM-perturbed) for the four fine-tuned
autoformalisers on the perturbed splits. Positive values indicate that the outcome is more frequent under the regex-based
perturbations.


D.1     Filtering of original Datasets
As a first step, we have filtered the various datasets as augmented with reasoning chains and presented in ProcessBench (Zheng
et al. 2025), such that:
                                  Dfiltered = {(x, y, r) ∈ DProcessBench | ∀si ∈ r : error(si ) = false}                   (10)
where x represents the input question, y is the ground-truth answer, r = (s1 , s2 , . . . , sn ) denotes the reasoning chain, si represents
the i-th step in the reasoning chain, and error(si ) ∈ {true, false} indicates whether step si contains an error.

D.2     DAG-parsing and Statement Classification
DAG-parsing As mentioned in the main text, we have parsed each reasoning chain into a DAG-like structure in order to obtain
the individual steps and the exact dependencies for those steps and reduce noise, as proposed in (Zhou and Zhang 2025). We
follow recent work that parses free-form chain-of-thought traces into structured reasoning graphs that have shown how this
task can be easily performed by existing LLMs (Lee et al. 2025; Xiong et al. 2025) and we use a SOTA LLM to perform this
step, i.e. GPT 5.2; to ensure the DAG processing was correct, we have prompted GPT 5.2 itself to self-judge the results of the
dependencies assignments for each DAG node. Figure 6 confirms that the model is able to perform this passage almost perfectly
for each of the analysed datasets.
    In addition to this automatic check, we manually inspected a sample of 210 DAG nodes, as reported in the main paper, finding
accuracies of 100% on GSM8K, 94.2% on MATH, 95.6% on OlympiadBench and 96.7% on OmniMATH. The errors we found
were missing dependencies, redundant dependencies and redundant nodes; none of them invalidated a step or a chain, which
could only happen if a critical dependency were omitted, and we did not observe this. The self-judge evaluation of Figure 6 thus
serves as a complementary automatic check to this human audit. Even in the cases in which the model might have done an error,
it is useful to remember that this might not automatically lead to an error in autoformalisation, since the step might still be valid
even if a not fundamental dependency is missing and/or an extra unrelated dependency is included. We therefore conclude that it
is safe to assume this preprocessing step will not negatively affect final results significantly.




                        Figure 6: Self-evaluation of DAG parsing step for the 4 datasets using GPT 5.2.


Statement Classification At the same time, we included in the prompt the request to GPT 5.2 to classify each statement si into
li ∈ Lmulti , with Lmulti including seven statement types defined as following:
1. Computation: Statements involving arithmetic or algebraic calculations. These steps perform numerical operations, evaluate
   expressions, or compute mathematical results. Examples include adding numbers, multiplying terms, evaluating functions, or
   performing matrix operations.
2. Logical: Statements that involve logical inference or deductive reasoning. These include conditional statements (if-then),
   implications (therefore, thus, hence), logical conclusions drawn from premises, or applications of logical rules and principles.
3. Declarative: Statements that assign values to variables, define new variables, or declare mathematical objects. These steps
   introduce notation, set up the problem space, or establish what symbols represent. Examples include "Let x = 5" or "Define
   f (x) = x2 + 1".
4. General Knowledge: Statements that invoke known facts, established theorems, mathematical properties, or domain-specific
   knowledge. These steps apply existing mathematical results without deriving them, such as citing the Pythagorean theorem,
   trigonometric identities, or well-known formulas.
5. Simplification: Statements that simplify algebraic expressions, reduce fractions, combine like terms, or transform expressions
   into simpler equivalent forms. These steps make expressions more compact or easier to work with without changing their
   fundamental value or meaning.
6. Substitution: Statements that replace variables or expressions with their equivalent values or alternative representations.
   These steps involve plugging in known values, replacing variables based on prior definitions, or substituting one expression
   for another based on established equalities.
7. Verification: Statements that check, validate, or confirm the correctness of a result. These steps involve testing solutions,
   verifying that answers satisfy given conditions, checking work, or confirming that a derived result is consistent with problem
   constraints.
   Based on the nature of declarative assignments being unverifiable and very high frequency in the initial annotation, we partition
the statements into a set of "Declarative" statements D and "Other" statements O using the indicator function I(si ):
                                                         
                                                           D if si is declarative
                                                I(si ) =
                                                           O otherwise
   The thus obtained Declarative statements are the unverifiable statements that we exclude from our analysis as described in the
Dataset section (Section 5.1) of the main paper.
   Also in this case, we employ an LLM judge to assess the correctness of this further preprocessing step. Figure 7 shows the
results of applying the same self-judging mechanism we have used for verifying the correctness of the DAG dependency parsing,
that is we used GPT 5.2 and prompted it to evaluate if each input statement type was correctly classified as belonging to D or to
O. According to this self-evaluation, the classification step contains no errors for any dataset analysed. A further manual audit
of 200 randomly sampled steps (described in the main text) agreed with the self-judge in 95.5% of cases, with disagreements
predominantly involving the judge being more conservative than the human annotator.




                   Figure 7: Self-evaluation of statement classification step for the 4 datasets using GPT 5.2.

  Finally we also prompt GPT 5.2 to include additional information such as any inference rule that was identified as being
represented in the input statement and any note about how the step itself might be verified. Inference rules and notes on verification
have not been used in the present work, but they are released together with our datasets (see Section A). Below we include the
prompt used in this step:

SYSTEM PROMPT:
You are an expert in mathematical logic and proof theory.
Your task is to analyze mathematical reasoning chains and
represent them as directed acyclic graphs (DAGs).

For each step in the reasoning:
1. Classify it as axiom/assumption (no dependencies) or
deduction (depends on prior steps)
2. Identify the type of statement (computation, logical
inference, etc.)
3. Determine if it’s verifiable (can be independently checked)
4. List all dependencies (previous steps it relies on)
5. Name the inference rule used if it’s a deduction

DO NOT INCLUDE THE PROBLEM STATEMENT AMONG THE DAG STEPS.

Be precise and thorough in your analysis.
PROMPT:
Analyze this mathematical reasoning chain and convert it
into a structured DAG:

{reasoning_chain}

Create a complete DAG representation with:
- Each reasoning step as a node
- Proper dependency relationships
- Hilbert-style proof annotations
- Verifiability assessment
- Statement type classification


                                E    Perturbation Prompt and Perturbation Validity
As explained, our perturber is based on a classic text-to-text approach modulated from Petrov, Dekoninck, and Vechev (2025), in
which we invoke an LLM giving the current reasoning step xi as input and we obtain a perturbed version Pert(xi ).
  When generating FaithformBench, we used GPT-5.2 to produce perturbations. Below, we report the prompt we used for this
purpose:
SYSTEM PROMPT:
You will be given a single reasoning step from a Chain-of-Thought mathematical solution. I
,→ want you to modify the mathematical claim, calculation, or deduction within this step so
,→ that it becomes mathematically false or logically invalid. Follow these instructions
,→ carefully:

1. **Minimal Modification:**
- Only alter the specific mathematical conclusion, equation, or deduction in the step. Keep
,→ the premise, the introductory text, and the overall formatting of the step intact.

2. **Contradict the Original Truth:**
- The change you make should result in an invalid logical leap or a false mathematical
,→ statement. If this step were formalized in a theorem prover like Lean, the proof of this
,→ specific step must fail.

3. **Maintain Plausibility:**
- Do not make the statement obviously nonsensical (e.g., do not write 1 = 2). The error
,→ should look like a plausible LLM hallucination, a common student misconception, or a
,→ subtle algebraic mistake.

4. **Avoid Easy Refutations:**
- The new step should not be trivially disprovable at a glance. For example, if modifying a
,→ polynomial expansion or a derivative, introduce a subtle sign error, drop a coefficient,
,→ or alter a bound slightly, rather than replacing the whole expression with something
,→ unrelated.

5. **Change Key Expressions:**
- Modify values, bounds, formulas, or logical operators (e.g., changing \leq to <, altering
,→ an exponent, or changing a congruence relation) so that the step no longer logically
,→ follows from standard mathematical axioms or the implicit previous steps.

6. **Only Output the Rewritten Step:**
- Your output must be the full, newly rewritten step only. Do not include explanations,
,→ apologies, or the original prompt.

7. **If Not Perturbable:**
- If the step is pure text or a meta-commentary without any mathematical claim or deduction
,→ that can be subtly falsified, output "Not applicable."

PROMPT:
Here is the step I want you to modify:

{original_step}

   Our analysis relies on the fact that our perturber is able to produce valid perturbation, i.e. perturbations that correctly modify
the truth value of an otherwise correct mathematical statement or perturb it in such a way that any subsequent step depending on
it will change its truth value.
   Given the importance of assessing the thus defined validity of the perturbations, we have designed an LLM-as-a-judge approach
for evaluating such property. Specifically, we have used 3 frontier models to judge whether the perturbations were valid. The
LLMs were given the unperturbed and the perturbed version of each statement and they had to decide whether the perturbation
applied correctly changed the truth value of the input statement, as we have defined above. Figure 8 shows the result of such
evaluation procedure on our LLM-based perturbations.
   From the figure it is evident that a low number of perturbations were deemed to be invalid by the three judges, confirming our
assumption that the perturbations correctly generated incorrect statements: averaged over the judges and the 12,784 perturbed
steps, 97.8% of the perturbations were judged effective.
   To further validate these numbers, we conducted a human audit, whose headline figures are also reported in the main paper.
Four annotators labelled 219 stratified items across the four datasets, working on disjoint subsets with shared gold questions, and
a meta-reviewer checked the full annotations. Human agreement with GPT-5.2 is 95.9% overall (90.0% on GSM8K, 98.6% on
MATH, 95.5% on OlympiadBench, 95.1% on OmniMATH). In 7 of the 9 disagreements the LLM judged a perturbation invalid
where the human judged it valid, so the LLM panel is stricter than the human annotators and the 2.2% contamination rate is, if
anything, an overestimate. Finally, recomputing our main metrics after excluding every perturbation judged invalid changes no
value by more than 0.01 for any model on any dataset.
SYSTEM PROMPT:
You are a rigorous mathematical verifier.

Your task is to determine whether a perturbation applied to a correct
mathematical solution resulted in an actually incorrect statement,
or whether the statement remains mathematically correct
despite the perturbation.

You must follow these rules strictly:

1. Focus only on mathematical correctness.

  * Ignore differences in wording, reasoning style, or
  intermediate steps.
  * A flawed or different reasoning process is acceptable if the
  final statement is still correct.

2. Independently verify the result.

  * Do NOT trust either the original or perturbed solution.
  * Recompute the result from scratch OR verify equivalence
  algebraically/symbolically.
  * Do not rely on surface similarity.

3. Extract and compare final claims.

  * Identify the final mathematical claim in the perturbed solution.
  * If needed, also identify the final claim in the original
  solution.
  * Compare both against your independently derived ground truth.

4. Equivalence rules:
   Consider the perturbation INEFFECTIVE if the perturbed
   statement is still mathematically correct, including cases where:

  * The final numeric answer is correct
  * Expressions are algebraically equivalent
  (e.g., expanded vs factored forms)
  * The statement is logically equivalent or truth-preserving

  Consider the perturbation EFFECTIVE if:

  * The final result is mathematically incorrect
  * A mathematical error changes the truth value of the statement
  * Hidden issues invalidate the statement (e.g., division by
  zero, domain violations, incorrect generalization)

5. Edge cases:

  * If incorrect reasoning accidentally leads to a correct
  final result, label it INEFFECTIVE_PERTURBATION.
  * A statement just defines variables or facts without any
  mathematical statement to be independently verified:
  in this cases judge
  EFFECTIVE_PERTURBATION if the variable assignment or statement
  was effectively changed by the perturbation
  * Pay attention to domain constraints, sign errors, and invalid
  transformations.

Process:
Step 1: Extract the final claim from the perturbed solution.
Step 2: Solve or verify the problem independently.
Step 3: Compare the perturbed claim with the correct result.
Step 4: Decide the label.
Figure 8: Invalid perturbation rates reported by GPT-5.2, Gemini 3.1 Pro and Qwen Plus used as LLM judges divided by dataset.
The number of perturbations that are deemed ineffective is clearly higher for more difficult datasets and lower for GSM8K,
reflecting the fact that perturbing a more challenging mathematical statement appears to be more difficult. Notice the high level of
agreement shown by the 3 LLMs which is largely driven by the high agreement in judging a perturbation as valid, while GPT 5.2
appears to be more strict than the other 2 LLMs in adjudicating a perturbation as invalid.



Output format (JSON only):
{
"label": "INEFFECTIVE_PERTURBATION" or "EFFECTIVE_PERTURBATION",
"is_correct": true or false,
"final_claim": "extracted final statement from perturbed solution",
"ground_truth": "independently computed correct result",
"reason": "brief explanation of why the perturbed statement
is correct or incorrect"
}

---

Original correct solution:
{original_solution}

Perturbed solution:
{perturbed_solution}

Question:
Did the perturbation make the statement mathematically incorrect,
or is it still correct?


                                                 F    Experimental Details
F.1   Autoformalisation Protocol
Formaliser Parameters We ran the four specialised autoformalisers with greedy decoding (temperature zero) to minimise
stochastic noise, allowing up to 16,384 generated tokens per call; the exception is Herald, whose Llama-2-based architecture has a
4,096-token context window, for which generation is capped at 2,048 tokens (its Lean outputs are well below this length). Instances
whose full prompt exceeds 4,000 characters are marked as AF-Fail without being sent to the model. To ensure robustness, we
processed the data in batches.
Initial Parsing The pipeline begins by parsing the Lean code generated by the model. We specifically extract the theorem
from the final code block and attempt to isolate both its body and its parameters. This step acts as our first filter: if we cannot
successfully extract either component, we classify the instance as an AF-Fail and exclude it from downstream processing.
Successful instances are then passed to the prover.

F.2   Proving and Verification
Once autoformalisation is complete, we subject the theorems to a two-stage verification process: type-checking and automated
proving.
Typechecking First, we compile the extracted theorem using a ‘by sorry‘ tactic to verify its syntactic correctness. Any theorem
that fails to compile is flagged as a TC-Fail. In all reported results, TC-Fail is aggregated with the extraction failures of the
previous stage into the single AF-Fail category (AF(x) = ∅ in the main text).
  Second, for every valid theorem, we construct a corresponding negation to test for invalidity. We parse the theorem’s parameters
and body to form a negation statement. If the theorem includes parameters (e.g., ∀x, P (x)), we construct the negation as
¬(∀x, P (x)); if it is parameter-free, we simply negate the body.
  Finally, we put both the direct statement and its negation to the test. We feed both simultaneously into the DeepSeek-Prover-V2-
(7B) (Ren et al. 2025) and evaluate the results at pass@2. This yields three mutually exclusive outcomes:
 • Proved: The prover verifies the direct statement.
 • Refuted: The prover verifies the negation statement (indicating the original formalisation was invalid).
 • Inconclusive: The prover fails to verify either statement.

F.3   Compute Environment
All experiments were run on a dedicated on-premise server. The system is an ASUS ESC8000A-E13 (non-MGX) equipped with
a single AMD EPYC 9555 CPU (64 cores, 3.20 GHz base frequency, up to 4.40 GHz boost, 256 MB L3 cache) and 384 GB of
ECC system memory. GPU computation was provided by three NVIDIA H200 NVL Tensor Core GPUs, each with 141 GB of
HBM3e memory.
   The server runs Ubuntu 22.04 LTS (with limited testing on Ubuntu 24.04 LTS) and uses the NVIDIA CUDA Toolkit and
cuDNN. Autoformalizers and provers were executed directly on the host machine using publicly available Hugging Face models.

                                                   G     Prompts Details
In our experiments, we have also evaluated four general-purpose frontier LLMs (Claude Opus 4.7, GPT 5.2, Gemini 3.1 Pro and
Qwen Plus) to output the autoformalisation of the input reasoning steps. In designing the prompt for this task we have used
few-shot in-context learning as a prompting technique that has been proven to be effective in formalising informal language to a
formal one (Wang et al. 2024b). The full prompt we have used is reported below:

# System Instruction:
You are an expert in Lean 4 formalization. Your task is to
autoformalize informal mathematical problems into Lean 4 code.

** Fidelity is paramount **: Do NOT correct the user’s mathematical statements.
If the input contains a mathematical error (e.g., "1 + 1 = 3"), you must formalize
it exactly as written (1 + 1 = 3).

** Only By Sorry Statements **: Instead of a proof, ALWAYS
just conclude the theorem with the usual Lean placeholder
"by sorry": your task is to autoformalize the statement not to prove it

** Goal **: We expect the Lean compiler to throw an error
if the statement is false. Do not try to prevent this error.

# Examples:

## Example Input 1:
CONTEXT: 256 = 2^8. We know that log_2(256) = 8.
STATEMENT: log_2(256) = 8

## Example Output 1:
‘‘‘
import Mathlib
import Aesop
set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

theorem my_favorite_theorem : Real.logb 2 256 = 8 := by
  sorry
‘‘‘

## Example Input 2:
CONTEXT: Mr. Josue’s initial capital was \$5000. The first
bank gave him \$4000. The second bank gave him \$8000.
STATEMENT: 5000 + 4000 + 8000 = 14365

## Example Output 2:
‘‘‘
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

-- Note: This theorem will fail in Lean because the math is incorrect,
-- but the formalization is faithful to the input.
theorem my_favorite_theorem : 5000 + 4000 + 8000 = 14365 := by
  sorry
‘‘‘

## Example Input 3:
CONTEXT: Solve for x in the expression ((-2)^2 - 11) / (-2 + 1).
STATEMENT: ((-2)^2 - 11) / (-2 + 1) = 7 ∧ 7 < -1

## Example Output 3:
‘‘‘
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

-- Note: This theorem will fail in Lean because 7 is not less than -1.
theorem my_favorite_theorem : ((-2 : R)^2 - 11) / (-2 + 1) = 7 ∧ (7 : R) < -1 := by
  sorry
‘‘‘

User Input:
CONTEXT: {context_variable}

STATEMENT: {informal_problem_variable}

Lean 4 Output:


                                                 H    Qualitative Analysis
H.1    Sycophancy Examples
In this section, we illustrate the distinct patterns of sycophancy we observed in the autoformalisers we evaluated. Each pattern is
a failure of alignment (the AF’s output drifts away from the meaning of the perturbed input) rather than a failure of logic (the
produced Lean theorem is, in each case, a valid theorem in Lean – it is simply not the theorem the natural-language step asked
for). All Lean snippets are quoted verbatim from the model output; ... marks omitted proof detail.
Example 1: Silent Correction (Stepfun) Problem ID: gsm8k-390. The original step is “Compute orange candies:
O = 2 × 54 = 108.” We perturb the final value, asserting that 2 × 54 = 118. The autoformaliser ignores the perturbed value and
emits a theorem whose conclusion is the correct arithmetic.
theorem my_favorite_theorem (T R O : N) (h0 : T = 232) (h1 : R = 54) (h2 : O = 2 * R) :
    O = 108 := by
  have h_main : O = 108 := by
    rw [h2 ]
    rw [h1 ]
    <;> norm_num
    <;> rfl
  apply h_main

Example 2: Tautology – Abandoning Content (GPT-5.2) Problem ID: math-617. The original step is “Therefore, the
length of the line segment is 13 units.”; we perturb it to “12 units.” Rather than re-encoding the distance computation, the
formaliser strips away all mathematical context (the points, the formula) and merely reflects the numeral it was handed, yielding
a reflexivity proof.
theorem my_favorite_theorem : (12 : R) = 12 := by
  have h : (12 : R) = 12 := by
    rfl
  exact h

Example   3: Tautology – Abandoning Content (Qwen Plus) Problem ID: math-792. The original counting step yields
 11     5
    
  4   − 4 = 330 − 5; we perturb the right-hand side to 330 − 10. The formaliser strips the combinatorial content entirely,
producing the trivial reflexivity 330 − 10 = 330 − 10.
theorem my_favorite_theorem : 330 - 10 = 330 - 10 := by
  have h : 330 - 10 = 330 - 10 := by
    -- This is a tautology, so we can use the reflexivity of equality to prove it.
    rfl
  exact h
                                                                                                                     1
Example 4: Type-Coercion Collapse (Qwen Plus) Problem ID: omnimath-697. The original step factors n2 +5n+4                   =
      1                                      1                                        2
(n+1)(n+4) ; we perturb the factoring to (n+2)(n+3) (clearly false: (n + 2)(n + 3) = n  + 5n + 6). The formaliser quantifies n
as a natural number: over N, 1/k = 0 whenever k > 1, so both sides collapse to 0 and the (wrong) factoring becomes trivially
provable.
theorem my_favorite_theorem : ∀ n : N, 1 / (n^2 + 5*n + 4) = 1 / ((n+2)*(n+3)) := by
  have h_main : ∀ n : N, 1 / (n^2 + 5*n + 4) = 0 := by
    intro n
    have h1 : n^2 + 5*n + 4 > 1 := by ...
    have h2 : 1 / (n^2 + 5*n + 4) = 0 := by
      apply Nat.div_eq_of_lt
      <;> nlinarith
    exact h2
  ...

Example 5: Hypothesis Smuggling – False Premise (Kimina) Problem ID: gsm8k-245. The original step is “1000/2 =
500”; we perturb it to “1000 − 2 = 686” (this example is drawn from the regex-perturbed variant of the step, released in
FaithformBench-Regex). Rather than rejecting the falsehood, the formaliser smuggles in a mutually inconsistent bundle of
premises (rates and totals that cannot all hold), derives False from them, and uses that contradiction to close the goal.
theorem my_favorite_theorem (rate_A rate_B : R) (h_rate_A : rate_A = 5)
    (h_rate_B : rate_B = 2 * rate_A)
    (h_total : 1000 * rate_A + 1000 * rate_B = 686 * rate_A + 686 * rate_B) :
    1000 - 2 = 686 := by
  have h_false : False := by
    have h1 : rate_B = 10 := by
      rw [h_rate_B]
      rw [h_rate_A]
      ...
    have h2 : 1000 * rate_A + 1000 * rate_B = 686 * rate_A + 686 * rate_B := h_total
    rw [h_rate_A, h1 ] at h2
    norm_num at h2 ⊢
    <;> linarith
  have h_main : 1000 - 2 = 686 := by
    exfalso
    exact h_false
  exact h_main
Example 6: Hypothesis Smuggling – Assumed Conclusion (Claude Opus 4.7) Problem ID: gsm8k-259. The original
step states “Change = (amount paid) − (total cost)”; we perturb the operator, replacing − with +. Rather than refuting the false
equation, the formaliser introduces the very equation it should have rejected as a hypothesis h, and then “proves” it by exact h.
theorem my_favorite_theorem (change amount_paid total_cost : R)
    (h : change = amount_paid + total_cost) : change = amount_paid + total_cost := by
  have h_main : change = amount_paid + total_cost := by
    -- The proof is straightforward because the goal is exactly the hypothesis ‘h‘.
    exact h
  exact h_main

Example 7: Ex Falso Quodlibet via Impossible Constraint (Kimina) Problem ID: omnimath-629. The original problem
assumes x ∈ R with 3x = 5; the perturbed step (drawn from the regex-perturbed variant of the benchmark, FaithformBench-Regex)
asserts the conclusion 3x+2 = 51 (the correct value is 9 · 5 = 45). The formaliser silently narrows the type of x to N. But since
no natural number satisfies 3x = 5 (we have 31 = 3 and 32 = 9), the hypothesis is unsatisfiable, and the goal – like any goal –
follows by ex falso.
theorem my_favorite_theorem (x : N) (h : 3^x = 5) : 3^(x + 2) = 51 := by
  have h1 : False := by
    have h2 : x ≤ 2 := by
      by_contra! h3
      have h4 : 3 ^ x ≥ 3 ^ 3 := by
        apply Nat.pow_le_pow_of_le_right
        norm_num
        linarith
      ...
    interval_cases x <;> norm_num at h ⊢ <;> omega
  have h2 : 3^(x + 2) = 51 := by
    exfalso
    exact h1
  exact h2
  This is the example featured in Figure 1 of the main paper.
Example 8: Quantifier Weakening (Qwen Plus) Problem ID: olympiadbench-510. With a = log2 x, b = log2 y, c =
log2 z, the original step records the linear system 3a + 2b + 2c = 12, 2a + 3b + 2c = 24, 2a + 2b + 3c = 30 that follows
from the problem. We perturb the third equation to 2a + 2b + 3c = 32 – false given the original problem’s log-constraints.
The formaliser drops the binding to x, y, z entirely and replaces “solve this system” with the trivially-true existence claim
“∃a, b, c ∈ R satisfying these three equations”.
theorem my_favorite_theorem :
  ∃ (a b c : R),
    (3 * a + 2 * b + 2 * c = 12) ∧
    (2 * a + 3 * b + 2 * c = 24) ∧
    (2 * a + 2 * b + 3 * c = 32) := by
  ...

H.2    Refuted Examples
In the following example, the formaliser fails to prove a statement that is intended to be true in the original context. This failure
typically arises from a literal translation that ignores implicit assumptions (notably domain constraints), producing a statement
that is provably false in its formal context and so refuted by counterexample.
Example 1: Missing Domain Constraint (Herald) Problem ID: omnimath-778. We intend to prove an algebraic identity
that holds when abc = 1 over the roots of x3 + 3x − 1 (in particular, the relations a3 = 1 − 3a, etc. are required). Herald instead
quantifies over arbitrary complex numbers a, b, c, dropping the root constraint. Over C without that constraint the identity fails:
the prover refutes the formalised theorem via the witness (1, −1, −1). (Herald uses descriptive theorem names rather than the
placeholder my_favorite_theorem.)
theorem not_a_cub_plus_b_cub_plus_c_cub_eq_3_full :
    ¬ (∀ (a b c : C) (habc : a * b * c = 1), a ^ 3 + b ^ 3 + c ^ 3 = 3) := by
  have h_main : (∃ (a b c : C), a * b * c = 1 ∧ a ^ 3 + b ^ 3 + c ^ 3 ̸= 3) := by
    use 1, (-1 : C), (-1 : C)
    constructor
    · -- Prove that 1 * (-1) * (-1) = 1
       norm_num
    · -- Prove that 1^3 + (-1)^3 + (-1)^3 ̸= 3
       norm_num [pow_three]
       ...
  have h_final : ¬ (∀ (a b c : C) (habc : a * b * c = 1), a ^ 3 + b ^ 3 + c ^ 3 = 3) := by
    intro h
    rcases h_main with ⟨a, b, c, h1 , h2 ⟩
    have h3 := h a b c h1
    exact h2 h3
  exact h_final

                               I   Artifact, Reproducibility and AI Use Declarations
To support transparency and reproducibility in our research, we provide the following details regarding the scientific artifacts,
datasets and models utilized in this work.

I.1   Artifact Usage, Citations, and Licensing
This research makes use of several existing scientific artifacts, including datasets, software packages, and both open-weight and
proprietary language models. We appropriately cite the creators of all artifacts in our references.
  For data manipulation, metric aggregation, and model inference, we utilized standard Python packages including numpy,
pandas, and the Hugging Face transformers library. API calls for proprietary models were managed using the official
openai, anthropic, and google-genai Python packages.
  Our primary evaluation dataset, ProcessBench, is distributed under the Apache-2.0 license. Similarly, we utilized several
specialized open-weight autoformalizers, all of which are distributed under the Apache-2.0 license:
 • StepFun-Formalizer-7B (7B parameters)
 • Goedel-Formalizer-V2-8B (8B parameters)
 • Herald-7B (7B parameters)
 • Kimina-Autoformalizer-7B (7B parameters)
The Apache-2.0 license explicitly permits the use, modification, and distribution of these artifacts for academic research.
Furthermore, we evaluated several proprietary models—specifically GPT 5.2, Gemini 3.1 Pro, Claude Opus 4.7, and Qwen
Plus. Our experimental usage of these models strictly adheres to their respective Terms of Service, which fully admit our
research-oriented use case. Our application of all aforementioned datasets, autoformalization models, and APIs is strictly confined
to academic research, benchmarking, and evaluation, remaining entirely consistent with their intended use cases.

I.2   Data Considerations
The ProcessBench dataset is a human-verified benchmark for LLM mathematical reasoning, consisting of natural-language
reasoning chains aggregated from GSM8K, MATH, OlympiadBench and Omni-MATH, with human expert annotations of
whether each chain is free of errors. Due to the inherent nature of this specialized mathematical domain, the dataset does not
contain personally identifying information (PII) or offensive content.

I.3   AI Assistance in Paper Preparation
In accordance with recent conference guidelines regarding the use of Large Language Models (LLMs) in scientific research,
we declare the use of AI assistants—specifically, Anthropic’s Claude and Google’s Gemini—during the preparation of this
manuscript. These models were employed as auxiliary tools to assist with routine coding tasks, debugging, and the drafting and
refinement of prose in certain sections of the paper.
   We emphasize that all core concepts, theoretical frameworks, experimental designs, and methodological decisions were
entirely human-ideated. The authors rigorously reviewed, edited, and validated all AI-generated code and text to ensure accuracy,
scientific integrity, and originality. The human authors assume full and final responsibility for the entirety of the content, results,
and claims presented in this work.
