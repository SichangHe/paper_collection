                                        ProofWriter: Generating Implications, Proofs, and Abductive Statements
                                                               over Natural Language

                                                                       Oyvind Tafjord, Bhavana Dalvi Mishra, Peter Clark
                                                                               Allen Institute for AI, Seattle, WA
                                                                         {oyvindt,bhavanad,peterc}@allenai.org




                                                                    Abstract
                                                Transformers have been shown to emulate log-
                                                ical deduction over natural language theories
arXiv:2012.13048v2 [cs.CL] 3 Jun 2021




                                                (logical rules expressed in natural language),
                                                reliably assigning true/false labels to candi-
                                                date implications. However, their ability to
                                                generate implications of a theory has not yet
                                                been demonstrated, and methods for recon-
                                                structing proofs of answers are imperfect. In
                                                this work we show that a generative model,
                                                called ProofWriter, can reliably generate both
                                                implications of a theory and the natural lan-
                                                guage proofs that support them. In particular,
                                                iterating a 1-step implication generator results
                                                in proofs that are highly reliable, and represent
                                                actual model decisions (rather than post-hoc
                                                rationalizations). On the RuleTaker dataset,
                                                the accuracy of ProofWriter’s proofs exceed
                                                previous methods by +9% absolute, and in a
                                                way that generalizes to proof depths unseen in
                                                training and on out-of-domain problems. We
                                                also show that generative techniques can per-
                                                form a type of abduction with high precision:
                                                Given a theory and an unprovable conclusion,
                                                identify a missing fact that allows the conclu-
                                                sion to be proved, along with a proof. These re-
                                                sults significantly improve the viability of neu-            Figure 1: Given facts, rules, and a question all ex-
                                                ral methods for systematically reasoning over                pressed in natural language, ProofWriter answers the
                                                natural language.1                                           question and generates a proof of the answer.

                                        1       Introduction                                                 over statements expressed in natural language, by
                                                                                                             reliably assigning true/false labels to candidate im-
                                        A fundamental goal for AI, dating back to its                        plications. However, simply assigning true/false
                                        earliest years, is automated reasoning: the abil-                    labels is limiting. For practical purposes, systems
                                        ity to draw valid conclusions from explicitly pro-                   should also generate proofs of those labels, so that
                                        vided knowledge (McCarthy, 1959). However, ap-                       their conclusions can be verified and a human-
                                        proaches relying on expressing knowledge in a                        understandable rationale be produced.
                                        formal representation language have sometimes
                                                                                                                Recent work on PRover, by Saha et al. (2020),
                                        proved challenging (Musen and Van der Lei, 1988).
                                                                                                             provided first results towards this goal, assembling
                                        Recent work on RuleTaker (Clark et al., 2020)
                                                                                                             proofs by first classifying which facts, rules, and
                                        demonstrated a modern approach to this goal, in
                                                                                                             connections should be in the proof tree then using
                                        which transformers emulate deductive reasoning
                                                                                                             an Integer Linear Programming (ILP) module to
                                            1
                                                Datasets available at https://allenai.org/data/proofwriter   enforce consistency constraints. However, the gen-
                                                          Taker datasets as well as several new variants. We
                                                          achieve state-of-the-art results in proof generation,
                                                          and strong new baselines for implication enumera-
                                                          tion and abduction over natural language theories.
                                                          Our contributions are thus:
                                                            1. A new method for proof generation for logical
                                                               reasoning over natural language, that obtains
                                                               state-of-the-art results and is faithful to the
                                                               model’s internal decisions.
                                                            2. A method and baseline results for generating
                                                               logical implications of statements in NL.
                                                            3. A method and baseline results for performing
                                                               abduction over natural language statements.
                                                            4. New datasets to promote further research.
                                                          These results significantly improve the viability of
                                                          neural methods for formal reasoning over language.
Figure 2: ProofWriter iteratively generates 1-step im-
plications and their proofs, and adds implications back
into into the context for deeper reasoning. The step-     2   Related Work
wise proof fragments are assembled into full proofs of
N-hop conclusions.                                        Our work builds on the RuleTaker line of research,
                                                          in which transformers learn to emulate a deductive
                                                          reasoning algorithm (Clark et al., 2020). Unlike
erated proofs were imperfect, and there were no           other approaches to reasoning such as parsing to a
guarantees that the model “believed” the proofs that      formal language (Kamath and Das, 2019), imple-
it was reciting, i.e., that its QA module would agree     menting a reasoning algorithm with neural compo-
with the steps shown in the proof. In this paper,         nents (Weber et al., 2019; Rocktäschel and Riedel,
we adopt a different approach, based on generation        2017), or SAT solving (Selsam et al., 2019), these
rather than classification. Our system, ProofWriter,      transformers emulate reasoning over language di-
generates proofs such as that shown in Figure 1 by        rectly, bypassing a formal representation.
iteratively generating 1-hop inferences and their            PRover (Saha et al., 2020), mentioned earlier,
(simple) proofs, adding implications back into the        was the first system to also produce proofs in
context for deeper reasoning, and assembling more         this context, although its post hoc approach meant
complex proofs from the 1-hop fragments (Fig-             that proofs did not necessarily represent the ac-
ure 2). As the accuracy of 1-hop inference is highly      tual model decisions. Gontier et al. (2020) also
reliable, the accuracy of deeper inference and their      explored the generation of answers and proofs, but
proofs is also high. This results in proofs that sub-     in the context of rule induction with (≈ 10) fixed
stantially exceed the earlier method’s accuracy, and      rules to induce. In contrast, ProofWriter generates
also reflect the model’s internal decisions, rather       proofs from explicit NL rules (which may differ
than a post-hoc rationalization (i.e., is a “faithful”    for each problem). Similarly, formal theorem prov-
proof (Subramanian et al., 2020)).                        ing has explored proving mathematical theorems
   The generative approach also affords two other         from fixed, fundamental axioms, e.g., (Polu and
new capabilities. First, ProofWriter generates im-        Sutskever, 2020; Wang and Deng, 2020), while
plications that logically follow from a NL (natural       ProofWriter performs inference with differing sets
language) theory, allowing enumeration of conse-          of rules expressed in natural language.
quences (rather than only assigning truth values to          Our work is also distinct from the large body
pre-conjectured hypotheses). Second, we demon-            of work on rationales and explanation. Work on
strate (a constrained form of) abduction: Given a         rationales aims to identify sentences (or phrases)
theory and an unprovable conclusion, identify a           that caused a model to make a particular decision,
missing fact (if any) that allows the conclusion to       but without an explanation of why that rationale led
be proved when added to the theory, plus its proof.       to the answer (the model’s reasoning is opaque),
   We evaluate our work on a collection of natural        e.g., (DeYoung et al., 2019; Narang et al., 2020).
language reasoning datasets, including the Rule-          Similarly, work on explanations has sought to gen-
    Proof (and Answer)   CQ → AP            Given theory C and hypothesis fact Q, determine Q’s truth A and proof P (if any)
    Enumeration          C → I1 , ..., In   Given C, generate all implications Ii that logically follow.
    Abduction            CQ → fm            Given C and an unprovable fact Q, identify a new fact fm that, when added to C,
                                            would make Q true.

                                 Table 1: The three tasks that ProofWriter performs.

erate human-style justifications, which again are               3.2    Semantics
typically supporting evidence rather than a fully-
                                                                Following prior work, we adopt the semantics of
formed line of reasoning, and without explicit
                                                                Datalog (Ceri et al., 1989): A fact is true if it is ei-
reasoning rules (Camburu et al., 2018; Jhamtani
                                                                ther known (i.e., explicitly stated in the context C),
and Clark, 2020; Inoue et al., 2020). In contrast,
                                                                or (recursively) is the conclusion of a rule whose
ProofWriter produces a deductive chain of reason-
                                                                conditions are true (is “supported”). For handling
ing from what is known to what is concluded, using
                                                                negation, we use two alternative Datalog semantics:
a transformer retrained to reason systematically.
                                                                The first, following prior work, makes the closed-
                                                                world assumption (CWA) and uses negation as fail-
3      Approach                                                 ure (NAF), so that any fact not provable is assumed
                                                                false. Under this semantics, negated facts and neg-
3.1     Definitions
                                                                ative rule conclusions are not allowed (redundant
Let:                                                            under the CWA). The second makes an open-world
     • C be a theory, a set of English sentences C              assumption (OWA), and does allow negative facts
       consisting of facts F and rules R, each ex-              and rule conclusions. Under this semantics, a third
       pressing a logical fact or rule in English. (We          truth value Unknown is also possible.
       also refer to C as the context).
     • Q be a question, a hypothesis fact in English            3.3    Proof Representation
       whose truth is to be determined based solely
                                                                We define a proof P of a fact fq as a directed
       on the information in C.
                                                                acyclic graph (N, E) with nodes n ∈ N and (di-
     • A be an answer, where A ∈ {T rue, F alse}
                                                                rected, untyped) edges e ∈ E. Each node in P is
       (if reasoning using a closed-world assump-
                                                                either a fact f (a ground literal) or a rule r (a logi-
       tion) or A ∈ {T rue, F alse, U nknown}
                                                                cal implication), expressed in English. Each edge
       (open-world assumption).
                                                                in the proof either connects a fact to a rule, denot-
     • P be a proof, described shortly.
                                                                ing that the fact helps satisfy the rule’s condition,
     • I be an implication, a fact that logically fol-
                                                                or connects a rule to a fact, denoting that the fact
       lows from C.
                                                                follows from the instantiated rule. Thus nodes in
                                                                any branch of the proof will alternate between facts
We define three tasks (also see Table 1):
                                                                and rules. Note this definition differs from (and
1. proof (inc. QA): CQ → AP : Given C and
                                                                is richer than) that in PRover, where intermediate
     hypothesis fact Q, what is the truth A and
                                                                conclusions were not part of the proof.
     proof P (if any) of Q?
2. enumeration: C → I1 , ..., In : Which Ii fol-                   Facts in the proof are one of three types: known
     low from C?                                                facts fi ∈ F , negated facts fnaf that cannot be
3. abduction(restricted form) CQ → fm : Which                   proven (false under negation-as-failure (NAF)), and
     extra fact fm will make Q true given C?                    facts fconc that are the conclusions of rules. fi and
                                                                fnaf are leaf nodes of the proof, while the fconc
We reuse (and add to) the RuleTaker datasets for
                                                                are intermediate nodes within the proof. Note that
our work, which include all five elements above.
                                                                fnaf and fconc are by definition not in F . Example
An example of a RuleTaker theory (facts and rules),
                                                                proofs are shown in Figures 1 and 3.
a query, and a proof generated by ProofWriter are
shown in Figure 1. Facts and rules are English
                                                                3.4    Proof Encoding
statements, and implications are English statements
that logically follow from those facts and rules.               As we wish to generate proofs, we need to encode
The original datasets were generated from synthetic             P as a linear structure that can be output by a gen-
logic programs and their implications, using natural            erative model. Facts and rules in the context are
language patterns to produce the English forms.                 explicitly labeled with identifiers (fact1, ..., rule1,
                                                                   of the form: “ $question$ = question ; $context$
                                                                   = theory-sentences”, for example: “$question$ =
                                                                   Erin is big. ; $context$ = sent1: Erin is young.
                                                                   sent2: If ...” The output is of the form: “$an-
                                                                   swer$ = True/False/Unknown : $proof$ = proof ;”,
                                                                   where proof is encoded as described in Section 3.4.
                                                                   For training instances where multiple outputs are
                                                                   valid, we select a single one at random (for mul-
                                                                   tiple proofs, we select among the shortest proofs).
                                                                   Appendix D lists the hyperperameters and gives
Figure 3: An example proof that includes a negated                 input/output examples for each task.
(negation-as-failure) fact.
                                                                   3.6     Task 1: Proof Generation
...) that the proof can refer to, see Figures 1 and 3.2            We evaluate two methods of proof generation:
Then, in the linear proof, rule nodes are denoted                  All-At-Once: We train a model to generate the full
by their identifier (rule1, ...), while fact nodes are                  proof and answer in one go (theory + question
denoted by three types of identifiers: fact1, fact2, ...                → answer + proof).
for facts in the context; naf1, naf2, ... for facts not            Iterative: We first train a model to generate a sin-
in the context and assumed false; and conc1, conc2,                     gle 1-step implication (theory → implication
... for facts concluded by rules. To decode the naf*                   + 1-step-proof), where the implication follows
and conc* identifiers (which by definition are not                      from a single rule application. Then at test
in the context), an additional sequence of the form                     time, we apply this model iteratively, adding
“with conc1: sentence1. conc2: sentence2. ...” is                       each implication to the theory and repeating
appended to the proof.                                                  until no more implications can be found (i.e.,
    To linearize the proof in a format convenient for                   exhaustive forward-chaining). The proof for
a generative model, we conjoin rules and their con-                     any given implication can then be assembled
clusions using a “%” symbol, express conjunctive                        from the 1-step-proof fragments (Figure 2).
rule conditions with a “&” symbol, and use “#” to
denote the inverse implication (“←”). We then ex-                  3.6.1    All-At-Once ProofWriter (“All”)
press the tree using Polish notation. E.g., the proof              The All-At-Once model is trained directly on
tree “((fact1 & fact2) → rule1 → conc1)” (i.e.,                    CQ → AP examples in the datasets (P = “None”
fact1 and fact2 satisfy rule1, concluding conc1)                   if there is no proof of Q). Section 3.5 describes the
would be expressed “# rule1%conc1 & fact1 fact2”.                  i/o format, and Appendix D.1 shows an example.
Thus the 3-step proof from Figure 1 is encoded:
                                                                   3.6.2    Iterative ProofWriter (“Iter”)
       # rule18%conc1 & fact5 # rule12%conc2                       Training: To train the Iterative model, for each
       # rule11%conc3 fact16 ; with conc1:                         theory C in the training data, we create an aug-
       Charlie is quiet. ; conc2: Charlie is                       mented set of training examples with one sequence
       young. ; conc3: Charlie is kind.                            of iteratively inferred facts in turn, each using C
If the question is a known fact, the “depth 0 proof”               plus the previously inferred facts. For example, if
is simply the fact itself (e.g., fact1). If no proof               theory C1 implies I1 , I2 , and I3 , then we create
exists, the symbol “None” is used.                                 four training examples C1 → I1 , C1 ∪ {I1 } → I2 ,
                                                                   C1 ∪ {I1 , I2 } → I3 , and C1 ∪ {I1 , I2 , I3 } →
3.5    Models                                                      “None”. The order of adding the Ii is random but
The ProofWriter models are built on top of the                     constrained such that if a later implication depends
text-to-text pretrained T5 transformer (Raffel et al.,             on an earlier one, the earlier one must be inferred
2020) (T5-11B). We use different textual prompts                   first. For example, if the proof of I3 depends on
for the different tasks. For the task of generating                I2 (determined by inspecting the gold proofs), I2
an answer and a proof, the input to the model is                   must be in the context before I3 is inferred. This
   2
                                                                   ensures that all example inferences are depth 1 (i.e.,
     In practice we name these sent1, sent2, ... without a
fact/rule distinction, but for expository purposes it is helpful   a single rule application). An example input/output
to use different identifiers.                                      for one step is shown in Appendix D.2.
   Testing: To answer and provide the proof for a                 model over our datasets, we create an abductive ver-
particular question/implication, the model gener-                 sion as follows: For each theory C in the train/test
ates all implications and their proofs by iteratively             data, for each unprovable fact Q, identify all alter-
applying the model until no more implications (the                native “missing facts” f actM that, when added to
implication “None”) is generated. It then looks for               C, make Q True. To do this, recall that each NL
the question among them. If found, the answer is                  theory was originally generated from a formal one
True with the proof given. The model also looks                   Cf ormal in a formal representation language (Data-
for the negation of the question3 and its proof. If               log). We first exhaustively enumerate all possible
found, the answer is False with the proof given.                  Qf ormal and f actMf ormal in the formal language
Otherwise, there is no proof (proof = “None”) and                 (this is feasible as the space of predicates and in-
the answer is False (for positive questions, CWA),                dividuals is small), then use a theorem prover to
True (for negative questions, CWA), or Unknown                    test if Cf ormal ∪ {f actMf ormal } implies Qf ormal
(any question, OWA).                                              for all pairs (f actMf ormal , Qf ormal ). For each
                                                                  success, we generate the NL equivalents Q and
3.7    Task 2: Implication Enumeration                            f actM using simple NL generation templates. We
A second desirable reasoning skill is enumerating                 then collect the alternative f actM s for each Q.
implications of a theory (rather than just assign                 The abduction task is then, given C and Q, identify
True/False to a hypothesis). This capability is im-               the set of all alternative f actM s, i.e.:
portant for practical application of the technology.                        C, Q → f actM1 , ..., f actMi
In fact, the Iterative ProofWriter already does this              If there is no single f actM that can be added to
by design, a substantial advantage. To evaluate this              make Q true, then the symbol “None” is output.
(later), we compare this with an “all at once” strat-
egy of generating all implications as a single output             4       Datasets
string, analogous to the All-At-Once strategy for
                                                                  We now evaluate ProofWriter on these three tasks.
generating the full proof as a single string. For
                                                                  We use the original RuleTaker D* datasets (Clark
training this All-At-Once enumerator, and testing
                                                                  et al., 2020), plus we create two new variants: The
both, we gather the list of all implications Ii of each
                                                                  first (CWA) is similar to the original except it fixes
theory C in the train/test data. Each train/test exam-
                                                                  some minor inconsistencies concerning negation
ple is of then of the form: given C, predict all the
                                                                  (details in Appendix A.2). The second (OWA) is
Ii . An example input/output is in Appendix D.3.
                                                                  also similar to the original, except reasoning uses
                                                                  an open-world assumption.
3.8    Task 3: Abduction (Single Fact)
                                                                     We denote these as D*(orig), D*(CWA), and
A third desirable reasoning skill is abduction over               D*(OWA). Each example in each dataset con-
natural language theories, again made possible by                 tains a theory C, a question Q, the answer A
generative models. Abduction has previously been                  (True/False/Unknown), and all possible proofs
studied extensively in formal logic, e.g., (Konolige,             P1 , ..., Pn for that answer (if provable).4 Each the-
1997), and in NLP, e.g., (Hobbs et al., 1993; Bha-                ory is also accompanied with all possible proofs of
gavatula et al., 2020). Here we evaluate whether a                all possible implications, as auxiliary annotations.
generative approach can combine logic and NLP,                       The D* datasets comprise five datasets, named
performing logical abduction over natural language                D0, D1, D2, D3, D5, each containing 100k ques-
knowledge. We do this for a restricted form of ab-                tions. In each dataset, theories and questions are
duction, namely single-fact abduction: Given a                    expressed in templated English (e.g., Figure 1),
theory C and a possible implication Q not prov-                   questions can be positive or negated facts (e.g.,
able from C, identify a new fact fm (other than the               “Charlie is not quiet?”), and answers are equally di-
trivial Q itself) such that C ∪ {fm } implies Q.                  vided into True/False (and Unknown, for the OWA
   We restrict this task to the OWA (open-world)                  versions). Each dataset contains questions whose
setting where questions can naturally have un-                    answers require reasoning up to depths D (D = 0,
known truth values. To train and test an abductive                1, 2, 3, 5). Thus, for example, all questions in D0
   3                                                                  4
     To negate a question, a model can be trained for this            The domain is small enough that all proofs can be enumer-
straightforward task. Here, as our question language is simple,   ated. However, there still can be a large number, e.g., some
a simple regex to add/remove a “not” suffices.                    D5 questions have over 3000 possible proofs.
                  Answer             Proof                                   Answer               Proof
Depth # qns PRover ProofWriter PRover ProofWriter                              ProofWriter         ProofWriter
                                                                       PRover              PRover
0     6299   100       100      98.4      99.6            Test   # qns          All Iter            All Iter
1     4434   99.0      99.1     93.1      98.7            Birds1 40     95.0    100 95.0 92.5       100 95.0
2     2915   98.8      98.6     84.8      97.3            Birds2 40     95.0    100 95.0 95.0       100 95.0
3     2396   99.1      98.5     80.5      94.4            Elec1 162     100    96.9 100     95.1 96.9 100
4     2134   98.8      98.7     72.4      91.0            Elec2 180     100    98.9 100     91.7 98.9 100
5     2003   99.3      99.3     65.1      86.4            Elec3 624     89.7 92.0 95.5 71.8 92.0 95.5
All   20192 99.3       99.2     87.1      96.2            Elec4 4224 84.8 83.3 97.1 80.6 82.0 97.1
                                                          All    5270 86.5 85.5 97.0 80.5 84.5 97.0
Table 2: [Task 1: Proof Generation] Systems trained
and tested on D5(orig), showing the breakdown by          Table 3: [Task 1: Proof Generation] Training on D5,
depth of proof required to answer each question.          test on Birds-Electricity. Both ProofWriter versions
ProofWriter generates significantly more correct proofs   (“All” for All-At-Once, “Iter” for Iterative) outperform
for all depths, achieving a new SOTA on this task.        PRover overall in both answer and proof correctness.
                                                          The Iterative model is also significantly more robust.
are lookup questions, requiring no inference. Each
dataset is split 70/10/20 into train/dev/test.            more correct proofs (last line, +9% absolute), and
   To test generalization, we also use two other          without the complexity of PRover’s heuristic as-
datasets from the original RuleTaker work:                sembly of proof graphs using ILP.
Birds-Electricity: These 6 test-only datasets use         5.1.2    Performance on OOD Rulesets
small, real-world theories written by hand (one per
dataset) to test out-of-distribution model perfor-        We compared ProofWriter’s and PRover’s ability
mance. Details are in Appendix A.3.                       to generalize to the hand-authored Birds-Electricity
ParaRules: This dataset contains 40k questions            rulesets, zero shot. These rulesets are out-of-
against 2k theories expressed in paraphrased nat-         domain (OOD), as their English is not templated
ural language, obtained through crowdsourcing.            and is stylistically different to the training data.
This dataset tests transfer to more natural expres-       We compare the PRover and All-At-Once (“All”)
sions of knowledge. Details are in Appendix A.4.          ProofWriter models trained on D5, plus the Iter-
                                                          ative ProofWriter (“Iter”) trained on D0-D3 theo-
5     Experiments and Results                             ries. The models do not see any Birds-Electricity
                                                          examples during training. The results in Table 3
5.1     Task 1: Proof Generation (Comparison              show that ProofWriter’s proof generation transfers
        with Prior Work)                                  well zero-shot to these hand-authored datasets, with
First, we compare ProofWriter’s ability to gener-         84.5% proof correctness for All-At-Once, and 97%
ate proofs with PRover, the current state-of-the-art.     for the Iterative ProofWriter, indicating better out-
We evaluate both answer accuracy and proof cor-           of-domain generalization for the Iterative version.
rectness. For proof correctness, for a fair compari-      Both ProofWriter models significantly outperform
son, we ignore the intermediate conclusion nodes          PRover (80.5%).
(which PRover does not generate). We then use                We also find ProofWriter obtains more correct
the same strict scoring metric as in PRover (called       proofs (+3%) than PRover on the ParaRules dataset.
FA or Full Accuracy in the PRover paper): the             Details are in Appendix B.1.
proof graph must exactly match a gold proof (i.e.,
                                                          5.2     Task 1: Proof Generation (All-At-Once
be perfectly correct); otherwise, the proof scores 0.
                                                                  vs. Iterative)
5.1.1    Generating Answers and Proofs                    Second, we compare our two approaches to proof
We use the same IID (independent, identically dis-        generation, All-At-Once vs. Iterative, in more de-
tributed) data used for PRover (train/test on dataset     tail. We show that although they have almost iden-
D5(orig)). The results are in Table 2, showing accu-      tical performance for proofs with depths seen in
racies for questions requiring increasingly deeper        training, the Iterative model generalizes better
depths of reasoning to answer. The ProofWriter’s          to proofs of longer depths than seen in training.
results are for the All-At-Once model. (The Itera-        For these comparisons, we use the new D*(CWA)
tive model scores are almost identical, see later Ta-     datasets (which fix some minor errors in D*(orig)),
ble 4.) While answer accuracy is almost perfect for       and also the D*(OWA) datasets to explore perfor-
both systems, ProofWriter generates substantially         mance in an open-world setting.
             Answer                        Proof
         CWA       OWA                CWA        OWA
 Depth All Iter All Iter            All Iter All Iter
 N/A   99.0 99.7 99.4 99.9          99.0 99.7 99.4 99.9
 0     100 100 100 100              100 100 100 100
 1     99.9 99.8 100 99.3           99.6 95.4 99.7 97.8
 2     99.9 99.5 99.9 99.7          98.3 91.7 98.6 97.3
 3     100 99.7 100 99.2            95.8 90.4 96.9 97.1
 4     100 99.7 99.9 99.1           93.1 88.9 94.8 96.5
 5     99.9 98.9 100 98.8           89.3 87.8 91.4 86.4
 All   99.6 99.7 99.7 99.6          97.2 95.4 98.0 97.6

Table 4: [Task 1] Comparison of All-At-Once (“All”)               Table 5: [Task 1] Comparison of the All-At-Once vs.
vs. Iterative (“Iter”) ProofWriter models, trained on             Iterative ProofWriter models, trained on D3 and tested
D5 and D0-D3 respectively, and tested on D5.                      on D5. While scores are mostly similar throughout, the
                                                                  iterative model generalizes substantially better to gen-
5.2.1    Comparison (IID Test Set)                                erate proofs of depths unseen during training (red box).

We train the All-At-Once model on D5 (train), and
the Iterative model using the method described in
Section 3.6.2, using the (∼ 5k) theories from D3
(train) plus ∼ 20% of the D0-D2 (train) theories.5
We then test both models on D5 (test). We mea-
sure both answer and proof accuracies, and also
break down the results by proof depth (using “N/A”
as the proof depth for questions that are not prov-
able). The D5 test set has 2k questions at each
proof depth, plus 8k unprovable questions (proof =
“None”, depth = “N/A’).6
   The results are shown in Table 4, and show that                Figure 4: [Task 1] All-At-Once proofs can be verified
                                                                  by checking each step as a separate QA query.
both ProofWriter versions have similar, high
proof correctness (95%+) on the test set, even
                                                                  5.3   Verifying All-At-Once Proofs
though some proofs are highly complex.
                                                                  Proofs from the Iterative ProofWriter have an ad-
5.2.2    Generalization to Unseen Depths                          ditional desirable property: each proof step is one
We also wish to see how well the models can gener-                that the model explicitly took during the iteration,
ate proofs at depths unseen during training. To do                i.e., the model “believes” the step. In contrast,
this, we train an All-At-Once model on D3, and use                the All-At-Once proofs are a post hoc generated
the same Iterative model as earlier (trained on itera-            string of symbols, and may not reflect steps that
tive examples from theories up to depth 3). We test               ProofWriter would actually make. However, be-
on D5. As D5 contains problems at greater depths                  cause proofs include intermediate conclusions, we
than those seen during training, we can observe the               can alleviate this concern by verifying individual
models’ ability to generalize. We compare with                    steps in the All-At-Once proofs. For example, if a
both the CWA and OWA versions of our datasets.                    generated proof step states that fact2 + fact3 + rule4
   The results are shown in Table 5. As can be                    implies conc1, we can simply ask ProofWriter in
seen, the All-At-Once model has quite poor gen-                   QA mode if this is true (Figure 4). Given the al-
eralization for generating longer proofs than seen                most perfect performance for such simple depth 1
in training, while the Iterative model is more ro-                questions in QA mode (with no distractor facts or
bust (red box).                                                   rules), the ability to verify a correct proof corre-
                                                                  sponds to the accuracy of correctly generating the
    5
      We include D0-D2 theories to have more examples of the-     correct intermediate conclusions conc* in the first
ories with fewer conclusions. The derivative iterative training
data is included in our dataset release.                          place. (Note that an unverified proof is not nec-
    6
      Note this breakdown is slightly different from the one in   essarily wrong, rather cannot be verified as right).
Table 2 where the depth used the original RuleTaker anno-         OWA proofs can be fully verified in this way. For
tations which included a depth for questions without proofs,
based on the deepest proof search that fails. We retained that    CWA theories with NAFs, the verification is only
convention in Table 2 for best comparison with PRover.            partial as NAFs are presumed negative statements
                      Verified Proofs                                     F1              Accuracy
                    CWA          OWA                        Enum   CWA       OWA       CWA       OWA
                   Train on:    Train on:                   Test All Iter All Iter All Iter All Iter
            Depth D3 D5 D3 D5                               D3+  98.9 99.8 99.4 99.6 92.5 98.8 95.5 99.0
            N/A   99.6 99.0 99.4 99.4                       D5   94.5 99.5 94.8 99.4 44.6 93.9 48.9 94.8
            0     100 100 100 100
            1     99.8 99.6 99.7 99.7                       Table 7: [Task 2: Enumeration] Iterative ProofWriter
            2     98.2 98.3 98.6 98.6
                                                            is better at generating all implications than an All-At-
            3     93.2 95.8 94.3 96.8
            4     66.7 92.9 66.1 94.6                       Once strategy. (All-At-Once is trained on D3+Enum,
            5     13.8 89.3 16.4 90.8                       Iterative ProofWriter is the same model as earlier.)
            All   87.2 97.2 87.9 97.9                                      Test: Count F1 Acc
                                                                           D3-Ab 7067 97.4 94.5
Table 6: [Task 1: Proof Generation] The All-At-Once                        D5-Ab 7181 97.3 93.5
model’s ability to verify its proofs. For proofs within
depths seen during training, almost all correct proofs      Table 8: [Task 3: Abduction] Given a theory C and an
(Tables 5 and 4, columns 5 and 7) can be verified. How-     unprovable conclusion Q, predict all alternative facts
ever, for proofs at unseen depths, the proportion that      that, when added to C, make Q provable.
can be verified drops rapidly (trained on D3, test on
depths 4,5). In contrast, Iterative ProofWriter’s proofs    Table 7, and show that the Iterative ProofWriter
are always verified, by definition of its algorithm.        is better at implication enumeration than the
                                                            simple All-At-Once strategy. In particular, the All-
which require the full theory to verify.                    At-Once strategy struggles for problems at depths
   We measured the percentage of correct, verified          unseen in training (second row), although it does
proofs, shown in Table 6. Provided proofs are               well on its own test set despite the complicated un-
within the depths seen during training, almost all          ordered output it has to generate (up to 16 different
correct proofs can be verified. However, at depths          implications in D3, 21 in D5).
deeper than seen at training, the proportion that
can be verified drops rapidly. In contrast, the Iter-       5.5     Task 3: Abduction (Single Fact)
ative ProofWriter’s proofs are always verified, as          Fourth and finally, we evaluate performance on
by definition they are assembled from single step           a second new task, namely abduction over nat-
inferences that the model actually took.                    ural language theories, again made possible by
                                                            generative models. Analogous to implication enu-
5.4   Task 2: Implication Enumeration
                                                            meration, we create a derivative abductive dataset
Third, we evaluate ProofWriter’s performance on             of C, Q → f actM1 , ..., f actMi examples, where
a new task, namely enumerating implications of              C ∪ {f actMi } results in Q becoming provable as
a theory (rather than just assign True/False to a           described in Section 3.8. We create such D*-Ab
hypothesis). We compare the All-At-Once and                 datasets from the D*(OWA) datasets.
Iterative strategies as described in Section 3.7.
   To train All-At-Once, and test both, we created          5.5.1    Results (IID)
an enumerative dataset of C → {I1 , ..., In } exam-         We trained a model on D3-Ab (train), and then
ples (Section 3.7). For this we sample theories             tested on both D3-Ab (test) and D5-Ab (test). We
C in the D0-D3 datasets and gather the list of all          evaluate the results by comparing the predicted
implications Ii for each theory C. We call this enu-        and gold f actM s, measuring both F1 and “perfect
merative dataset D3+Enum. We similarly create               match” Accuracy (1 when F1=1, 0 otherwise). The
a D5-Enum dataset from theories in (only) D5 to             results are shown in Table 8, and indicate that the
test OOD conclusion generation. We create CWA               model performs well overall (85%+ scores). We
and OWA versions of both.                                   also broke down the recall of f actM s by proof
   We train All-At-Once on D3-Enum (train), then            depth required to prove Q given C and f actM .
test both models on D3-Enum (test) and D5-Enum              This is shown in Table 9, indicating that it is harder
(test). For metrics, we measure F1 scores by com-           to identify a f actM that completes a deeper proof.
paring the individual predicted implications with           The similarity of D3-Ab and D5-Ab scores sug-
the gold Ii , as well as the exact-match correct-           gests that D5-Ab is not out-of-domain for this task:
ness of the predicted set of implications {I1 , ..., In }   Although depths for provable D5 facts are deeper
(one point if the set exactly matches the gold, bar         than D3, this task concerns unprovable facts, which
ordering, zero otherwise). The results are shown in         may not be distributed differently to D3-Ab.
 Gold Proof    Test on D3-Ab       Test on D5-Ab         (which would similarly need to be controlled). Sec-
 Depth      # Gold Acc (recall) # Gold Acc (recall)
 N/A         2155       97.73    2170       97.74        ond, as the theory grows by one fact per iteration,
 1           4813       98.46    4731       98.73        there is a risk of exceeding the transformer’s input
 2           1719       96.22    1986       96.17        token limit (512 tokens by default), hence limiting
 3            688       90.26     915       92.79
 4            153       75.82     330       82.73        the size of theories that can be handled. For larger
 5             19       36.84      96       78.13        theories, a retrieval mechanism might be needed to
                                                         manage the facts and rules available to the reasoner.
Table 9: [Task 3: Abduction] Recall of abduced facts
by proof depth. The data suggests that it is harder to   6.2    Abduction and Implicit Knowledge
identify a f actM that completes a deeper proof.
                                                         Recently, LeapOfThought (Talmor et al., 2020)
5.5.2 Generalization to New Tasks                        showed that RuleTaker-like models could be re-
To assess out-of-domain generalization, we also          trained to reason with a combination of explicit
evaluate how well the trained abductive model            and implicit knowledge, rather than requiring all
performs on an abductive version of the Birds-           rules to be stated explicitly (the implicit knowledge
Electricity(OWA) theories, zero-shot (created us-        coming from the latent knowledge acquired dur-
ing the same approach, Section 3.8). We find that        ing pretraining (Petroni et al., 2019)). Now, given
ProofWriter has perfect zero-shot performance for        an abductive capability such as the one we have
the simple Birds rulebases, but progressively re-        presented, we have a mechanism for materializing
duced performance for the Electricity theories as        the implicit knowledge used to answer a question,
they get more complex (dropping to 64% F1, 62%           and hence generating the full proof of its answer:
Accuracy for one rulebase), indicating that the ab-      Given a LeapOfThought conclusion, first abduce
ductive task is only partly solved (Appendix B.2).       the “missing” (implicit) fact(s) required for an ex-
                                                         plicit proof, then use ProofWriter to generate that
6     Discussion                                         proof. This is a significant step forward to help
                                                         understand a model’s decisions when both implicit
6.1    All-At-Once vs. Iterative Strategies
                                                         and explicit knowledge has been used.
While the All-At-Once approach to proof genera-
tion is simple, efficient, and effective, it does not    7     Summary and Conclusion
generalize as well to proofs of greater depth than
                                                         While it is remarkable that transformers can learn to
seen at training. In contrast, the Iterative approach
                                                         systematically reason over language, such methods
is robust to generalization. Even though errors at
                                                         will have limited impact if they cannot also explain
each iteration accumulate, the reliability of 1-step
                                                         their answers. In this work, we showed the first
inference is so high that such error accumulations
                                                         application of generative techniques to this task,
remain small. The Iterative architecture, namely a
                                                         and demonstrated how proofs, implication enumer-
simple model embedded in a recursive loop (rather
                                                         ations, and abductive inferences can be generated,
than single seq2seq model), illustrates how trans-
                                                         exceeding the prior state-of-the-art in proof gener-
formers can be used in a “scale-invariant” way,
                                                         ation by +9% (absolute). In addition, the Iterative
i.e., performance is largely unchanged by the scale
                                                         ProofWriter robustly generalizes to deeper proofs
(here reasoning depth) of the problem. In addition,
                                                         and more varied language than seen in training,
as proofs are built from actual inference steps taken
                                                         and produces proofs that reflect (i.e., are faithful to)
by the model, they are by definition “faithful” to
                                                         the model’s actual inference decisions. Finally, the
the model’s inference steps, rather than being a
                                                         abductive capability offers the potential for gener-
post hoc rationalization.
                                                         ating proofs when both explicit and implicit knowl-
   However, there are also some drawbacks to the
                                                         edge are used, by materializing the implicit knowl-
Iterative approach: First, it is inefficient and un-
                                                         edge needed to complete the proof. Together, these
guided, proving everything possible and only then
                                                         significantly improve the viability of neural meth-
looking for the answer and proof for a particu-
                                                         ods for systematically reasoning over language in
lar question. In fact, this is a limitation of un-
                                                         practical settings. The ProofWriter datasets are
constrained forward-chaining in general, hence es-
                                                         available at https://allenai.org/data/proofwriter
tablished techniques for guiding forward-chaining
could be applied, e.g., a best-first expansion strat-    Acknowledgements: We thank Google for provid-
egy, or using a backward-chaining strategy instead       ing the TPUs for conducting experiments.
References                                                Sharan Narang, Colin Raffel, Katherine Lee,
                                                            A. Roberts, Noah Fiedel, and Karishma Malkan.
Chandra Bhagavatula, Ronan Le Bras, Chaitanya               2020. WT5?! training text-to-text models to explain
  Malaviya, Keisuke Sakaguchi, Ari Holtzman, Han-           their predictions. ArXiv, abs/2004.14546.
  nah Rashkin, Doug Downey, S. Yih, and Yejin
  Choi. 2020. Abductive commonsense reasoning. In         F. Petroni, Tim Rocktäschel, Patrick Lewis, A. Bakhtin,
  ICLR’20.                                                   Y. Wu, Alexander H. Miller, and S. Riedel. 2019.
                                                             Language models as knowledge bases? In EMNLP.
Oana-Maria Camburu, Tim Rocktäschel, Thomas
  Lukasiewicz, and Phil Blunsom. 2018. e-SNLI: Nat-       Stanislas Polu and Ilya Sutskever. 2020. Generative
  ural language inference with natural language expla-       language modeling for automated theorem proving.
  nations. In Advances in Neural Information Process-       ArXiv, abs/2009.03393.
  ing Systems, pages 9539–9549.
                                                          Colin Raffel, Noam Shazeer, Adam Roberts, Katherine
S. Ceri, G. Gottlob, and L. Tanca. 1989. What you al-       Lee, Sharan Narang, M. Matena, Yanqi Zhou, W. Li,
   ways wanted to know about datalog (and never dared       and Peter J. Liu. 2020. Exploring the limits of trans-
   to ask). IEEE Trans. Knowl. Data Eng., 1:146–166.        fer learning with a unified text-to-text transformer. J.
                                                            Mach. Learn. Res., 21:140:1–140:67.
Peter Clark, Oyvind Tafjord, and Kyle Richardson.
                                                          Tim Rocktäschel and S. Riedel. 2017. End-to-end dif-
  2020. Transformers as soft reasoners over language.
                                                            ferentiable proving. In NeurIPS.
  In IJCAI’20.
                                                          Swarnadeep Saha, Sayan Ghosh, Shashank Srivastava,
Jay DeYoung, Sarthak Jain, Nazneen Rajani,                  and Mohit Bansal. 2020. PRover: Proof gener-
   E. Lehman, Caiming Xiong, R. Socher, and                 ation for interpretable reasoning over rules. In
   Byron C. Wallace. 2019. ERASER: A benchmark              EMNLP’20.
   to evaluate rationalized nlp models. In ACL.
                                                          Daniel Selsam, Matthew Lamm, Benedikt Bünz, Percy
Nicolas Gontier, Koustuv Sinha, Siva Reddy, and             Liang, Leonardo de Moura, and David L. Dill. 2019.
  C. Pal. 2020. Measuring systematic generalization         Learning a SAT solver from single-bit supervision.
  in neural proof generation with transformers. In          In ICLR.
  NeurIPS’20.
                                                          Sanjay Subramanian, Ben Bogin, Nitish Gupta, Tomer
J. Hobbs, Mark E. Stickel, Douglas E. Appelt, and           Wolfson, Sameer Singh, Jonathan Berant, and Matt
   P. Martin. 1993. Interpretation as abduction. Arti-      Gardner. 2020. Obtaining faithful interpretations
   ficial Intelligence, 63:69–142.                          from compositional neural networks. In ACL.

N. Inoue, Pontus Stenetorp, and Kentaro Inui. 2020.       Alon Talmor, Oyvind Tafjord, P. Clark, Y. Goldberg,
  R4C: A benchmark for evaluating RC systems to get         and Jonathan Berant. 2020. LeapOfThought: Teach-
  the right answer for the right reason. In ACL.            ing pre-trained models to systematically reason over
                                                            implicit knowledge. In NeurIPS.
Harsh Jhamtani and P. Clark. 2020. Learning to ex-
                                                          Ming-Zhe Wang and Jun Deng. 2020. Learning to
  plain: Datasets and models for identifying valid rea-
                                                            prove theorems by learning to generate theorems. In
  soning chains in multihop question-answering. In
                                                            NeurIPS.
  EMNLP.
                                                          Leon Weber, Pasquale Minervini, Jannes Münchmeyer,
Aishwarya Kamath and Rajarshi Das. 2019. A survey           Ulf Leser, and Tim Rocktäschel. 2019. Nlprolog:
  on semantic parsing. In AKBC’19.                          Reasoning with weak unification for question an-
                                                            swering in natural language. In ACL.
K. Konolige. 1997. Abductive theories in artificial in-
  telligence. In Principles of Knowledge Representa-
  tion.

John McCarthy. 1984. Applications of circumscription
  to formalizing common sense knowledge. In NMR.

John W. McCarthy. 1959. Programs with common
  sense. In Proc. Tedding Conf. on the Mechanization
  of Thought Processes, pages 75–91.

Mark A Musen and Johan Van der Lei. 1988. Of brit-
 tleness and bottlenecks: Challenges in the creation
 of pattern-recognition and expert-system models. In
 Machine Intelligence and Pattern Recognition, vol-
 ume 7, pages 335–352. Elsevier.
            Appendix: ProofWriter: Generating Implications, Proofs,
               and Abductive Statements over Natural Language
A     Datasets: Additional Details                         A.2    Repairs to the RuleTaker Datasets
A.1    Statistics                                          The original RuleTaker theories were intended to
Some overall statistics for the updated RuleTaker          be full Datalog theories, but contained three occa-
CWA and OWA datasets are in Table 10. The                  sional violations in the with-negation theories:
number of implications per theory can reach 20                1. Some theories contained negated facts (e.g.,
and above, and the proof depths go up to 10, even                “Bob is not red”) and/or rules with negated
though the proof depths of the associated questions               conclusions. Such statements are redundant
are limited to the dataset depth (e.g., depth 3 for               under a CWA, and not allowed according to
D3).                                                              formal Datalog specifications.
                                                              2. Some theories included rules with a free vari-
                                # impl   depth                    able in a negated condition (e.g., “If someone
    Dataset     # th  # qns min/mean/max max
    CWA:                                                          is not blue then Bob is happy.”). Such rules
    D0         27020 100002    0/1.0/18    8                      are not allowed according to formal Datalog
    D1         12965 100012    1/1.9/17    6                      specifications, as the possible groundings of
    D2          9138 100014    2/3.3/18    5
    D3          7067 100024    3/5.1/16    7                      the variable require meta-information about
    D5          4935 100030    5/9.8/21   10                      the theory as a whole.
    Birds/Elec 140    5270     0/2.0/6     4                  3. A bug in the stratification checker led to a few
    ParaRules 2403 40022       3/4.3/14    5
    OWA:                                                          theories being included that were not stratifi-
    D0         26978 100000    0/0.8/18    5                      able, and hence may have multiple, valid truth
    D1         12933 100014    1/1.7/14    6                      assignments for their facts.
    D2          9033 100010    2/3.1/14    5
    D3          6940 100036    3/4.8/16    6               As a result, the theories were regenerated (with
    D5          4752 100030    5/9.1/21   10               the same distribution over number of facts, rules,
    Birds/Elec 140    5270     0/1.2/6     3
    ParaRules 2403 40022       3/4.3/14    5               condition, etc.) to create the D*(CWA) datasets,
                                                           avoiding these issues.
Table 10: Statistics for the CWA and OWA datasets,            The D*(OWA) datasets are similar to the
giving the number of theories, questions and implica-      D*(orig) datasets, but evaluated without a CWA,
tions per theory. Note that the maximum implication
                                                           i.e., negation-as-failure (NAF) is replaced with hard
proof depth can go higher than the maximum proof
depth for the included questions (e.g., for D5 the maxi-   negation. The theories with negation were again re-
mum questions depth is 5, but there are implications up    generated to ensure they were stratifiable (to avoid
to depth 10 which are include in the enumeration task).    negation cycles), but they still retain negated facts
                                                           and rule conclusions. The truth values of the ques-
                                                           tions were recomputed using an OWA, resulting in
Table 11 describes overall statistics for the datasets     answers True/False/Unknown.
for Task 3: Abduction. Each abduction question
can have zero or more missing facts as answer, and         A.3    The Birds-Electricity Datasets
the proof depths can go up to 11.
                                                           The RuleTaker “birds” rulebase is a well-known
                                   # missing   max         logic problem illustrating the use of “abnormal-
                                      facts   proof        ity” predicates (McCarthy, 1984),7 , and converted
Dataset               # th # qns min/mean/max depth
D0-Ab                18011 85705    0/0.8/15    6          into English by hand. The dataset contains a sin-
D1-Ab                10448 49808    0/0.8/12    7          gle theory of six rules (e.g., “If someone is a bird
D2-Ab                 7092 37245    0/0.9/11    6          and wounded then they are abnormal.”) and seven
D3-Ab                 5633 34915    0/1.1/11    8
D5-Ab                 4362 35213     0/1.2/9   11          facts (e.g., “Bill is wounded”), and forty questions
Birds-Electricity-Ab 140 3940       0/0.24/4    4          against this theory (i.e., 40 test examples total).
                                                           Birds1 and Birds2 differ solely in the English word-
Table 11: Statistics for the Abduction datasets, giving    ing (e.g., “Bill is flying” vs. “Bill can fly”).
the number of theories, abduction questions, number of
missing facts per question and maximum proof depth.           7
                                                                https://www.doc.ic.ac.uk/∼mjs/teaching/KnowledgeRep491/
                                                           ExtendedLP 491-2x1.pdf, p5
                 Answer             Proof                           Test Dataset: # qns F1     Acc
     # qns PRover ProofWriter PRover ProofWriter                    Birds1-Ab       14 100.00 100.00
 D=0 2968   99.7      99.9     99.4      99.9                       Birds2-Ab       14 100.00 100.00
 1   2406   98.6      99.3     97.3      99.3                       Elec1-Ab       114 89.47 89.47
 2   1443   98.2      98.3     88.7      97.7                       Elec2-Ab       126 90.25 88.89
 3   1036   96.5      98.2     89.9      96.5                       Elec3-Ab       456 81.79 76.32
 4   142    88.0      91.5     76.1      83.1                       Elec4-Ab      3216 85.77 83.99
 All 8008   98.4      99.1     95.1      98.5                       All           3940 85.66 83.53

Table 12: [Task 1: Proof Generation] Train on D3         Table 13: [Task 3: Abduction] Zero-shot scores of the
+ ParaRules, test on (only) ParaRules. Both systems      D3-Ab model on the Birds-Electricity-Ab rulebases.
demonstrate robustness to more complex linguistic ex-
pressions in the theories, with ProofWriter obtaining
3% higher proof correctness.                             plex natural language in the input, with ProofWriter
                                                         obtaining 3% higher proof correctness.

   The four RuleTaker “electricity” datasets contain     B.2    Abduction: Generalization to New Tasks
examples of reasoning about toy electrical cicuits
                                                         Section 5.5.2 summarized the results of testing
using a small set of general rules about circuits.
                                                         abductive reasoning on abductive versions of the
Examples in each dataset are built using a fixed
                                                         Birds-Electricity(OWA) theories. The detailed re-
set of general rules per dataset, ranging from five
                                                         sults are shown in Table 13, showing perfect zero-
rules (Elec1) to twelve rules (Elec4). Each example
                                                         shot performance for the simple Birds rulebases,
in these datasets contains the general rules, plus
                                                         but progressively reduced performance for the Elec-
between two and five facts describing a particular
                                                         tricity theories as they get more complex. This indi-
circuit, with a set of questions about the circuit,
                                                         cates that the abductive task remains only partially
e.g., Q: “The light bulb is glowing?” A: True.
                                                         solved by our generative model.
A.4    The ParaRules Dataset
                                                         C     Results with T5-large
The RuleTaker “ParaRules” dataset contains 40k
questions against 2k theories expressed in para-         In the main part of the paper we trained ProofWriter
phrased natural language, obtained by having             starting from the largest available T5-11B model
crowdworkers rephrase the templated English facts        (11 billion parameters). If we instead use the more
and rules from sampled original theories into more       manageable T5-large model (770 million parame-
varied natural language. For example, “Bob is cold.”     ters), the scores generally go down, but typically
might be rephrased “In the snow sits Bob, crying         by a small amount.
from being cold”; or “Alan is round. Alan is blue.          In Tables 14 and 15 we show two examples of
Alan is kind.” might be rephrased “Alan, who is          this, for the All-At-Once and Iterative ProofWriter
round and also kind, tends to be rather blue”; or “If    models respectively, when training on the D3
someone is kind then they are young.” might be           dataset and evaluating on D5. We see the T5-large
rephrased “A kind person will certainly be young.”.      model is a bit worse on higher depth proof accuracy
While the previous datasets contain synthetic lan-       in the All-At-Once model, but is otherwise quite
guage, ParaRules tests the models’ ability to reason     competitive.
over more human-like paraphrased language.
                                                         D     Hyperparameters and I/O Examples
B     Additional Results
                                                         We fine-tune the models on the training set using
B.1    Results on the OOD ParaRules Dataset              the default hyperparameters (including the Adafac-
We also test the robustness of ProofWriter’s proof       tor optimizer) in the T5 library.8 We use the largest
generation to theories that use more varied natural      T5-11B model for the main results, fine-tuned for
language, summarized in Section 5.1.2. Following         40k steps (batch size 8), selecting the checkpoint
(Clark et al., 2020) and (Saha et al., 2020), we train   with highest validation score (usually the final step).
on the combined training partitions of D3(orig) and      See Appendix C for results using the smaller T5-
ParaRules, then test on the ParaRules test parti-        large.
tion. The results in Table 12 show that PRover and           8
                                                               https://github.com/google-research/text-to-text-transfer-
ProofWriter (All-At-Once) are robust to more com-        transformer
             Answer               Proof                             the dog then it is not red. sent9: The mouse does not chase the
         CWA       OWA       CWA        OWA                         tiger. sent10: If something visits the mouse then the mouse is
Depth large 11B large 11B large 11B large 11B
                                                                    red. sent11: The tiger visits the lion. sent12: The tiger does
N/A    98.4 99.6 97.4 99.4 98.4 99.6 97.4 99.4
0      100 100 100 100 100 100 100 100                              not eat the mouse. sent13: The mouse is nice. sent14: The
1      100 99.9 99.9 99.9 99.4 99.7 99.3 99.8                       lion does not eat the tiger. sent15: If the tiger visits the dog
2      99.8 99.4 99.7 99.8 97.5 98.2 97.6 98.8                      and the dog is not big then the dog chases the mouse. sent16:
3      100 99.2 99.7 99.8 90.4 93.4 91.2 94.5                       The lion visits the tiger. sent17: If something chases the lion
4      98.9 95.4 99.5 99.3 38.6 69.9 46.9 71.4                      and it visits the dog then it chases the dog. sent18: The dog
5      92.3 72.9 98.9 93.7 12.4 27.4 24.4 35.1                      is nice. sent19: If something chases the lion then it is big.
All    98.4 96.6 98.7 99.0 83.4 88.9 85.6 90.2                      sent20: If something eats the lion then it is not cold.
                               ¡                                    OUTPUT: $answer$ = True ; $proof$ = # sent7@int1 &
                                                                    sent16 # sent8@int2 # sent17@int3 & sent1 # sent5@int4 #
Table 14: [Task 1] Comparing T5-large vs T5-11B for                 sent19@int5 sent1 ; with int1: The lion is not nice. ; int2: The
the All-At-Once models trained on D3 and evaluated                  tiger is not red. ; int3: The tiger chases the dog. ; int4: The
on D5. T5-large is actually a bit ahead of T5-11B on                tiger visits the dog. ; int5: The tiger is big.
answer accuracy (for CWA), although the proof correct-                 If we translate back from Polish Notation, this
ness is noticeably higher with T5-11B.
                                                                    proof corresponds to ((sent16 & ((((sent1 & ((sent1
             Answer               Proof                             → sent19 → int5) → sent5 → int4)) → sent17 →
         CWA       OWA       CWA        OWA
Depth large 11B large 11B large 11B large 11B
                                                                    int3)) → sent8 → int2)) → sent7 → int1)
N/A    99.0 99.7 99.2 99.9 99.0 99.7 99.2 99.9
0      100 100 100 100 100 100 100 100                              D.2    Iterative Proof Generation (one step)
1      98.8 99.8 99.1 99.3 95.0 95.4 97.5 97.8
2      98.3 99.5 98.9 99.7 91.0 91.7 96.4 97.3                      In this task we ask the model to generate one valid
3      98.6 99.7 98.4 99.2 89.0 90.4 95.5 97.1                      implication of the theory with proof of depth 1. If
4      98.0 99.7 97.5 99.1 86.3 88.9 93.4 96.5
5      97.7 98.9 96.5 98.8 85.4 87.8 82.3 86.4                      no such implication exists, instead generate ”None”
All    98.7 99.7 98.8 99.6 94.4 95.4 96.4 97.6                      as the answer.
                                                                    INPUT: $answer$ ; $proof$ ; $question$ = What is one single-
Table 15: [Task 1] Comparing T5-large vs T5-11B for                 hop inference? ; $context$ = sent1: If something eats the
the Iterative ProofWriter trained on D0-D3 and evalu-               cow and it is big then the cow sees the bald eagle. sent2:
ated on D5. T5-11B is systematically slightly better.               If something likes the bald eagle then it is rough. sent3: If
                                                                    something eats the dog then it likes the cow. sent4: Big things
                                                                    are young. sent5: If something likes the cow then it eats the
   For all tasks in this paper, the model input and                 cow. sent6: If something sees the bald eagle then the bald
output are plain textual strings in a certain format.               eagle eats the cow. sent7: If something likes the bald eagle
The format is slightly more verbose than strictly                   then the bald eagle is kind. sent8: If something sees the bald
necessary, as it is compatible with a more general                  eagle then the bald eagle eats the dog. sent9: The bald eagle
                                                                    eats the cow. sent10: The bald eagle sees the dog. sent11: The
framework combining different views of the task.                    dog is big. sent12: The cow likes the bald eagle. sent13: The
This is not typically an issue, although there are                  bald eagle is young. sent14: The dog sees the cow. sent15:
a few cases where the iterative model reaches the                   The bald eagle is kind. sent16: The dog is young. sent17:
default 512 token limit of T5 when adding impli-                    The bald eagle sees the cow. sent18: The bald eagle is rough.
                                                                    sent19: The cow eats the bald eagle. sent20: The dog is cold.
cations to the theory. We now show input/output                     sent21: The dog likes the cow. sent22: The dog eats the bald
examples for proof generation (All-At-Once and                      eagle. sent23: The dog eats the cow. sent24: The bald eagle
(one step of) the Iterative approaches), implication                likes the dog. sent25: The bald eagle likes the cow. sent26:
generation (All-At-Once approach; Iterative impli-                  The cow sees the bald eagle. sent27: The cow sees the dog.
                                                                    OUTPUT: $answer$ = The cow is rough. ; $proof$ = # sent2
cation generation is a side-effect of Iterative proof               sent12
generation), and abduction.
                                                                       During evaluation time, we would then take this
D.1    All-At-Once Proof Generation                                 output and append it to the theory as ”sent28: The
                                                                    cow is rough.” and repeat the question. If a sub-
In this task we are given a theory and question, and
                                                                    sequent proof then references ”sent28”, we know
need to produce an answer (True/False/Unknown)
                                                                    already that this was derived using the proof ”#
and proof with intermediates.
                                                                    sent2 sent12”.
INPUT: $answer$ ; $proof$ ; $question$ = The lion is not
nice? ; $context$ = sent1: The tiger chases the lion. sent2:
The lion is not big. sent3: If something visits the dog and it is   D.3    All-At-Once Implication Enumeration
kind then it visits the mouse. sent4: The dog chases the lion.
sent5: If something is big then it visits the dog. sent6: The
                                                                    In this task we ask the model to simply output all
tiger eats the dog. sent7: If something visits the tiger and the    valid implications of a theory, without generations
tiger is not red then it is not nice. sent8: If something chases    proofs in this case.
INPUT: $answer$ ; $proof$ ; $question$ = What are all the
inferences? ; $context$ = sent1: The tiger chases the lion.
sent2: The lion is not big. sent3: If something visits the dog
and it is kind then it visits the mouse. sent4: The dog chases
the lion. sent5: If something is big then it visits the dog. sent6:
The tiger eats the dog. sent7: If something visits the tiger and
the tiger is not red then it is not nice. sent8: If something
chases the dog then it is not red. sent9: The mouse does not
chase the tiger. sent10: If something visits the mouse then
the mouse is red. sent11: The tiger visits the lion. sent12:
The tiger does not eat the mouse. sent13: The mouse is nice.
sent14: The lion does not eat the tiger. sent15: If the tiger
visits the dog and the dog is not big then the dog chases the
mouse. sent16: The lion visits the tiger. sent17: If something
chases the lion and it visits the dog then it chases the dog.
sent18: The dog is nice. sent19: If something chases the lion
then it is big. sent20: If something eats the lion then it is not
cold.
OUTPUT: $answer$ = The dog is big. The tiger is big. The
dog visits the dog. The tiger visits the dog. The dog chases
the dog. The tiger chases the dog. The dog is not red. The
tiger is not red. The lion is not nice.
  This particular theory has 9 valid implications,
around average for D5 theories. (The number of
implications can be as high as 21).

D.4 Iterative Implication Enumeration
Iterative implication generation is a side-effect of
Iterative proof generation, hence the input/output
(one step) is the same as in Appendix D.2.

D.5 Abduction
In this task we ask the model to output all alterna-
tive missing facts, separated by a comma, that can
be (separately) added to a theory so as to prove the
given implication to be True.
INPUT: $answer$ ; $question$ = Dave is rough. ; $context$
= triple1: Anne is white. triple2: Charlie is young. triple3:
Dave is round. triple4: Erin is quiet. rule1: If someone is
rough and young then they are blue. rule2: Rough, white
people are smart. rule3: All smart people are rough. rule4:
All white people are smart. rule5: If someone is young then
they are smart. rule6: All smart people are rough.
OUTPUT: $answer$ = Dave is young. , Dave is smart.
   This particular abduction question has 2 alterna-
tive missing facts. Any one of them when added to
the input theory is sufficient to prove the implica-
tion ‘Dave is rough’.
