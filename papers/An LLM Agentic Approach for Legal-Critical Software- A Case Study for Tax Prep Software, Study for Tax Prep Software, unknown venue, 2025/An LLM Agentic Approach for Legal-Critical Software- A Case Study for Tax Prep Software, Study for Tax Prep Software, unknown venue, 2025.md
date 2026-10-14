                                           An LLM Agentic Approach for Legal-Critical Software: A Case
                                                          Study for Tax Prep Software
                                                                    Sina Gogani-Khiabani                                                                  Ashutosh Trivedi
                                                                 University of Illinois Chicago                                                    University of Colorado Boulder
                                                                      Chicago, IL, USA                                                                   Boulder, CO, USA
                                                                       sgoga3@uic.edu                                                              ashutosh.trivedi@colorado.edu

                                                                        Diptikalyan Saha                                                                 Saeid Tizpaz-Niari
                                                                           IBM Research                                                             University of Illinois Chicago
                                                                          Bangalore, India                                                               Chicago, IL, USA
                                                                       diptsaha@in.ibm.com                                                                 saeid@uic.edu
arXiv:2509.13471v2 [cs.SE] 4 Mar 2026




                                        Abstract                                                                                    CCS Concepts
                                        As Large Language Models (LLMs) continue to advance in their abil-                          • Software and its engineering → Software verification and
                                        ity to process both natural and programming languages, they show                            validation; Automated static analysis; • Computing methodolo-
                                        promise for translation tasks in domains with strict compliance                             gies → Natural language processing; • Information systems
                                        requirements. Yet ensuring consistency in legally critical settings                         → Decision support systems; • General and reference → Law.
                                        remains challenging due to inherent limitations such as natural
                                        language ambiguity and the tendency to hallucinate. This paper                              Keywords
                                        explores an agentic approach that leverages LLMs for the develop-                           LLMs, Agentic AI, Tax Preparation Software, Metamorphic Testing
                                        ment of legal-critical software. We use U.S. federal tax software as a
                                        representative case study, where natural language tax code must                             ACM Reference Format:
                                                                                                                                    Sina Gogani-Khiabani, Ashutosh Trivedi, Diptikalyan Saha, and Saeid Tizpaz-
                                        be translated precisely into executable logic.
                                                                                                                                    Niari. 2026. An LLM Agentic Approach for Legal-Critical Software: A Case
                                           A central challenge in developing legal-critical software from                           Study for Tax Prep Software. In 2026 IEEE/ACM 48th International Conference
                                        specifications lies in test case generation, which suffers from the                         on Software Engineering (ICSE ’26), April 12–18, 2026, Rio de Janeiro, Brazil.
                                        oracle problem: determining the correct output for a given scenario                         ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3744916.3764575
                                        often requires interpreting legal statutes. Prior work has proposed
                                        metamorphic testing as a solution by evaluating equivalence across                          1    Introduction
                                        similarly situated individuals. A key innovation of our work is a
                                                                                                                                    Large Language Models (LLMs) have the potential to transform
                                        higher-order generalization of metamorphic tests, motivated by our
                                                                                                                                    legal-critical software development by automating the interpre-
                                        tax preparation case study, in which system outputs are compared
                                                                                                                                    tation and implementation of complex regulatory requirements.
                                        across structured shifts among similar individuals. Since manually
                                                                                                                                    Legal-critical systems in domains such as finance, healthcare, and
                                        generating such higher-order relations is tedious and error-prone,
                                                                                                                                    compliance demand highly accurate translations of natural lan-
                                        our agentic paradigm is well suited to automate test case generation.
                                                                                                                                    guage statutes into executable code. Ensuring correctness, consis-
                                           We design and implement Synedrion, an assembly of LLM-
                                                                                                                                    tency, and compliance in these domains is particularly challenging
                                        based agents simulating roles in real-world software development
                                                                                                                                    due to the intricacy of legal language, the frequency of regulatory
                                        teams handling legal documents. The framework includes a meta-
                                                                                                                                    updates, and the absence of explicit oracles for validation. Meet-
                                        morphic testing agent that produces counterexamples while trans-
                                                                                                                                    ing these challenges requires principled methodologies that both
                                        lating tax code into executable software. Our findings indicate
                                                                                                                                    minimize errors and fully exploit the capabilities of LLMs. In this
                                        that Synedrion, when employing smaller language models (e.g.,
                                                                                                                                    work, we introduce an agentic approach to LLM-driven legal-critical
                                        GPT-4o-mini), can outperform frontier models (e.g., GPT-4o and
                                                                                                                                    software development, using U.S. federal tax preparation software
                                        Claude-3.5) in complex tax code generation tasks, achieving a
                                                                                                                                    (tax software) as a representative case study.
                                        worst-case pass rate of 45% compared with 9%–15%. We thus make
                                        the case for LLM-driven agentic methodologies as a pathway for                              Tax Preparation Software. With an estimated 72 million Americans
                                        generating robust, trustworthy legal-critical software from natural                         relying on tax software to file their returns in 2020, tax prepara-
                                        language specifications.                                                                    tion systems exemplify legal-critical software due to their strin-
                                                                                                                                    gent compliance requirements and central role in enforcing tax
                                        Permission to make digital or hard copies of all or part of this work for personal or       laws [13, 19, 37, 39]. Ensuring compliance while maintaining us-
                                        classroom use is granted without fee provided that copies are not made or distributed       ability makes the development of such systems inherently com-
                                        for profit or commercial advantage and that copies bear this notice and the full citation
                                        on the first page. Copyrights for third-party components of this work must be honored.      plex [10, 14, 26, 37], requiring expertise in both mission-critical
                                        For all other uses, contact the owner/author(s).                                            software engineering and legal interpretation. Tax software must
                                        ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                         faithfully implement and update the tax code—a structured body
                                        © 2026 Copyright held by the owner/author(s).
                                        ACM ISBN 979-8-4007-2025-3/26/04                                                            of statutes and regulations governing the computation of taxes
                                        https://doi.org/10.1145/3744916.3764575                                                     for individuals and businesses. Translating these provisions into
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                        Sina Gogani-Khiabani, Ashutosh Trivedi, Diptikalyan Saha, and Saeid Tizpaz-Niari


executable logic poses multiple challenges, including statutory am-
biguity, intricate eligibility criteria, and interdependencies among
tax rules. The evolving nature of tax law further demands frequent
software updates, which heightens the risk of implementation er-
rors. Such errors are well documented: for example, OpenTaxSolver
misapplied Earned Income Tax Credit (EITC) eligibility rules [37],
and TaxSlayer blocked eligible taxpayers from claiming Affordable
Care Act (ACA) credits [35], underscoring the difficulty of faith-
fully encoding legal regulations into compliant software. Given
these complexities—from legal ambiguity to continual regulatory
change—tax software provides an ideal testbed for exploring LLM-
based legal software development, where LLMs can support the
interpretation, updating, and compliance with evolving tax law.

Metamorphic Testing. A fundamental principle of common law, stare
decisis, dictates that similar cases should yield similar rulings. This
ensures consistency and fairness by binding decisions to precedent        Figure 1: Synedrion—an LLM multi-agent framework for
and comparative reasoning. It also enables the expression of legal        implementing tax software from legal documents.
properties through case comparisons—an approach that naturally
aligns with metamorphic testing in software validation. Following
Tizpaz-Niari et al. [37], we connect stare decisis to metamorphic
testing as a means of validating legal-critical software.                 web pages, and publicly available code, these models are increas-
    Metamorphic testing addresses the oracle problem—where the            ingly applied to software engineering tasks [12, 15, 22]. However,
correct output is unknown—by ensuring relative correctness be-            LLMs face significant challenges, including token constraints, sus-
tween input pairs. This mirrors stare decisis by enforcing consis-        ceptibility to hallucinations, and the absence of a persistent state
tency across similar cases. For instance, while a taxpayer’s exact        across sessions. More critically, LLMs struggle with the inher-
liability may be uncertain, we can assert that a blind taxpayer should    ent ambiguity of software requirements expressed in natural lan-
receive a higher deduction than an otherwise identical non-blind          guage. For instance, our experiments reveal that when prompted to
taxpayer. Formally: For any two individuals identical except for blind-   “calculate tax based on progressive brackets”, an LLM may
ness, the blind taxpayer’s liability must be less than or equal to that   incorrectly apply the highest tax rate to an entire income rather
of the non-blind taxpayer.                                                than only to the portion exceeding lower bracket thresholds. Such
    Prior research [37] has applied metamorphic testing to tax soft-      errors highlight a fundamental disconnect between natural lan-
ware by comparing outputs across similarly situated individuals           guage specification, code generation, and verification.
rather than relying on absolute correctness. However, conventional        Our Approach. We posit that the structured, formal nature of legal
metamorphic testing, which relies on pairwise comparisons, may            language in tax amendments, combined with concrete examples,
overlook systematic errors. A case in point is progressive taxation: a    makes tax-related content particularly suitable for automatic trans-
faulty tax program that applies a flat tax rate across all incomes may    lation into executable software via LLMs. Recent work [23] has
still satisfy pairwise metamorphic relations (e.g., higher income         highlighted the potential of LLMs to assume traditional roles in
leading to higher tax) while violating the principle of progressivity.    software development, motivating an agentic approach [6, 23] in
    To address these limitations, we introduce higher-order metamor-      which specialized agents—each with defined intentions, responsi-
phic relations evaluating rates of change across multiple taxpayer        bilities, and actions—collaborate in system design.
profiles. Instead of verifying that a higher-income taxpayer owes            We introduce Synedrion, a multi-agent framework (Figure 1)
more tax than a lower-income one, our method examines whether             for translating legal documents into executable software. A central
the rate of tax increase reflects statutory progressive structures.       innovation is the higher-order metamorphic testing agent (HMT),
    Since manually specifying higher-order metamorphic relations          which improves robustness by detecting systematic errors in LLM-
is tedious and error-prone, we leverage LLM agents trained to infer       generated tax software. We further provide an empirical analysis of
metamorphic properties from legal documents, structured examples,         six legal tax publications, assessing the contributions of individual
and domain-specific heuristics. Metamorphic testing thus provides a       agents within our framework and evaluating their effectiveness
structured way to enforce legal consistency by grounding validation       across different LLM capabilities and tax code complexities.
in comparative properties rather than absolute correctness. Our
higher-order metamorphic testing agent extends this framework by          Results. Our study shows that baseline LLMs struggle to generate
capturing broader legal reasoning patterns and detecting systematic       accurate tax software directly from legal code. In contrast, our multi-
discrepancies that traditional pairwise comparisons may miss.             agent framework demonstrates that smaller models can match or
                                                                          outperform frontier baselines. Addressing RQ1–RQ4, we find that
LLMs for Code Generation. LLMs—such as ChatGPT, Llama, and                while strong single models perform well in simpler cases, they
Claude—have demonstrated rapid advancements in capabilities               falter under complexity; our multi-agent design sustains perfor-
and applications. Trained on vast corpora of text, including books,       mance across scenarios. Higher-order metamorphic testing further
An LLM Agentic Approach for Legal-Critical Software: A Case Study for Tax Prep Software                                  ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


strengthens robustness by uncovering systematic errors conven-                            some subset of labels 𝐿 ⊆ L. This higher-order formulation broad-
tional testing overlooks. Finally, empirical analysis highlights the                      ens metamorphic testing by evaluating functional requirements
role of domain-specific agents, such as TaxExpertAgent and Meta-                          across multiple related cases simultaneously, enabling detection of
morphicTestingAgent, in achieving substantial gains in functional                         systematic errors that pairwise comparisons might overlook.
correctness. Together, these results underscore the benefits of struc-
                                                                                          Motivating Example. To illustrate higher-order metamorphic rela-
tured agent collaboration for legally critical software.
                                                                                          tions with continuous numerical inputs, consider the U.S. progres-
                                                                                          sive tax system as outlined in IRS Publication 17. Tax liability is
2    Tax Software and Metamorphic Relations
                                                                                          not a linear function of income but follows a bracketed structure,
For convenience, we abstractly represent a functional model of tax                        where portions of income are taxed at different rates. For example,
software as a tuple (𝑋, F ), where:                                                       a single-status taxpayer is taxed at 10% on income up to $11,600
     • 𝑋 = {𝑋 1, 𝑋 2, . . . , 𝑋𝑛 } is the set of variables corresponding                  (𝑏 1 ) and at 12% on income from $11,601 to $47,150 (𝑏 2 ). Thus, an
       to fields on an individual’s tax return form. These variables                      individual earning $20,000 owes:
       include age, a numerical variable for the individual’s age;                             • $1,160 on the first $11,600 (10%),
       blind, a Boolean variable indicating whether the individual                             • $1,008 on the remaining $8,400 (12%),
       is blind; and sts, the filing status with values such as MFJ                            • Total: $2,168.
       (married filing jointly) and MFS (married filing separately).
                                                                                          A 4-ary relation can capture a monotonicity property:
     • F : D1 × D2 × · · · × D𝑛 → R is the function computed by
       the software, where each D𝑖 is the domain of variable 𝑋𝑖 .                              𝜙 4 : ∀x, x′   (x ≡𝐼 x′ ) ∧ (x.𝐼 ≥ x′ .𝐼 ) =⇒ F (x) ≥ F (x′ ).
       We write D for the Cartesian product D1 × D2 × · · · × D𝑛 .
                                                                                          This ensures that higher income implies at least as much tax. How-
For an individual taxpayer 𝑥 ∈ D, we write 𝑥 (𝑖) for the value                            ever, it fails to detect systematic errors. For instance, a faulty imple-
of the 𝑖-th variable, or 𝑥 .lab for the value of the variable labeled                     mentation applying a flat 12% tax to all income (e.g., taxing $20,000
lab. Since the ground-truth outcome for any input 𝑥 is difficult to                       at 12% = $2,400 instead of $2,168) would still satisfy monotonicity.
predict exactly, testing the functional correctness of tax software                       Likewise, for deductions (e.g., medical expenses), pairwise checks
encounters the oracle problem [7], wherein the expected output for                        can confirm that liability decreases as expenses increase, but not
a given input is unavailable.                                                             whether the decrease follows the correct statutory proportion. To
   To address this, we draw on metamorphic testing for tax soft-                          capture such errors, we introduce an 8-ary relation that compares
ware [28, 36, 37]. The key observation is that while exact output for                     rates of change across multiple income levels:
a given taxpayer profile may be unknown, the relationship between
outputs for related taxpayers can be expressed. For example, rather                           𝜙 8 : ∀x1, x2, y1, y2, (x1 ≡𝐼 y1 ) ∧ (x2 ≡𝐼 y2 )∧
than requiring an oracle for a blind taxpayer, one can compare two                                   (x1 .𝐼 = x2 .𝐼 < y1 .𝐼 < y2 .𝐼 ∈ [$11,601−$47,150])
individuals differing only in blindness, and require the software to
                                                                                                                           F (x1 ) − F (y1 )  F (x ) − F (y )
assign the blind individual a lower tax burden.                                                                     =⇒       x1 .𝐼 −y1 .𝐼    − x22.𝐼 −y2 .𝐼 2   < 0.12.
   Let L be the set of all labels. Given 𝐿 ⊆ L and an individual x ∈
                                                                                             This ensures that the marginal tax rate remains within the ex-
D, we often wish to express properties relating to a counterfactual
                                                                                          pected bracket, rejecting flat-rate implementations. A slight varia-
individual x′ ∈ D who is identical to x except possibly on the labels
                                                                                          tion further enforces within-bracket consistency, requiring taxpayers
in 𝐿. We denote this relationship as x ≡𝐿 x′ , meaning that x and x′
                                                                                          in the same bracket to face the same rate:
are similar with respect to all labels outside 𝐿. Formally,
                                                                                                          F (x1 ) − F (y1 )    F (x2 ) − F (y2 )
                   x ≡𝐿 x′     =⇒       ∀ℓ ∉ 𝐿, x.ℓ = x′ .ℓ.                                                                ≈                    .
                                                                                                             x1 .𝐼 − y1 .𝐼       x2 .𝐼 − y2 .𝐼
For instance, consider the higher standard deduction available to                         Such higher-order relations provide a stronger criterion, catching
blind individuals. We can express the corresponding relation as:                          systematic errors that simpler monotonicity checks cannot.
                                    
    ∀x, x′ x ≡ {blind} x′ ∧ x.blind      =⇒ F (x) < F (x′ ).
                                                                                          3     Tax Software from Legal Documents
Higher-Order Metamorphic Relations. In the context of tax software,                       Given a tax software system F synthesized from the natural lan-
prior work [36, 37] has primarily relied on pairwise metamorphic                          guage of the tax code, our work addresses the fundamental chal-
relations, where two inputs are compared based on an expected                             lenge of verifying its functional correctness against legal require-
directional change. While this approach is sound—any violation                            ments. The absence of a definitive oracle for tax outcomes, coupled
directly signals a bug—it may fail to capture more complex discrep-                       with the incompleteness of traditional tests, makes conventional
ancies spanning multiple test cases.                                                      metamorphic testing insufficient. To overcome this, we leverage
   To increase coverage, we extend beyond quaternary relations                            higher-order metamorphic relations as a central solution. The key
(relating two inputs and outputs) and adopt n-ary metamorphic                             challenges, then, lie in automatically inferring these specifications
relations [4]. These are expressed as                                                     from tax regulations and generating comprehensive test cases that
                                                                                          effectively exercise them.
                           𝜙 (x1, y1, . . . , x𝑛 , y𝑛 ),
                                                                                             To realize this approach, we introduce a multi-agent system that
where (x1, . . . , x𝑛 ) are base test cases, (y1, . . . , y𝑛 ) are follow-ups,            automates specification inference, code generation, and validation.
and each pair (x𝑖 , y𝑖 ) satisfies an equivalence constraint x𝑖 ≡𝐿 y𝑖 for                 Our system consists of five specialized agents, each with a distinct
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                           Sina Gogani-Khiabani, Ashutosh Trivedi, Diptikalyan Saha, and Saeid Tizpaz-Niari


role in the pipeline: a Tax Expert Agent, two Coder Agents, a Senior
Coder Agent, and a Metamorphic Agent. Figure 1 illustrates how
these agents interact, highlighting their collaboration in synthesiz-
ing and verifying tax software against legal requirements.

3.1      Individual Agents and Division of Labor
The overarching goal of our multi-agent system is to autonomously
generate, validate, and refine tax calculation functions to ensure
accuracy and compliance with tax rules. Each agent contributes
specialized capabilities toward this objective. By assigning distinct
roles, we can leverage the strengths of different LLMs and promote
a more efficient, robust development process.

3.1.1 TaxExpertAgent. This agent serves as the initial interpreter
of the legal text. It parses tax regulations and converts them into
                                                                          Figure 2: Schematic of Higher Order Metamorphic Relations
a structured JSON representation. It also produces JSON-based
specifications for individual functions required in tax software,
describing their purpose, inputs, outputs, calculations, and edge
cases. The output JSON must conform to a predefined schema that           LLM, we apply slightly different temperature settings (e.g., a 0.1–
validates data types (e.g., tax rates as numbers), required fields, and   0.2 variation). This encourages diverse outputs and exploration of
structural integrity (e.g., verifying that tax_brackets for a filing      alternatives without destabilizing the process.
status is an array of objects, each with a threshold and a rate).         Function Description (Example): Each CoderAgent receives detailed
   If the generated JSON fails schema validation, the agent regener-      instructions through JSON-formatted function descriptions, ensur-
ates it until compliance is achieved. For example, the JSON structure     ing adherence to specifications and avoiding hardcoded values by
for tax brackets may include keys for filing statuses, each contain-      referencing tax rules via JSON keys. An example of such a descrip-
ing bracket thresholds and corresponding rates. A JSON output             tion for the calculate_tax function is provided next:
from TaxExpertAgent for bracket calculation is shown below:
                                                                          {
{                                                                              "function_name": "calculate_tax",
    "tax_brackets": {                                                          "inputs": {
       "single": [                                                                "income": { "type": "float", "constraints": ["income >= 0"] },
          { "threshold_amount": 9950, "rate_decimal": 0.1 },                      "status": { "type": "string", "constraints": [
          { "threshold_amount": 40525, "rate_decimal": 0.12 },                       "in ['single', 'married_filing_jointly']"
          { "threshold_amount": 86375, "rate_decimal": 0.22 }                     ]}
       ],                                                                      },
       "married_filing_jointly": [...]                                         "outputs": {
    },                                                                            "tax_due": { "type": "float", "rounding": 2 }
    "standard_deductions": {                                                   },
       "single": {                                                             "calculations": [
          "base_amount": 12400,                                                   { "step": "apply_brackets", "formula": "income * t_rate", ... }
          "additional_elderly": 1650,                                          ]
          "additional_blind": 1650                                             ...
       },                                                                 }
       ...
    }                                                                     This structured JSON input ensures that CoderAgent implementa-
}                                                                         tions remain accurate, consistent, and aligned with tax rules.

3.1.2 Senior Coder and Coder Agents. Within our framework, the            3.2        Higher-Order Metamorphic Testing Agent
CoderAgent and SeniorCoderAgent collaborate to generate the               Integrated into the sequential workflow, the MetamorphicAgent re-
Python code for tax functions. Guided by JSON-based specifica-            ceives generated code from the SeniorCoderAgent and subjects it
tions from the TaxExpertAgent, the CoderAgent instances produce           to rigorous metamorphic testing. Previously, Tizpaz-Niari et al. [37]
code that adheres to defined inputs, outputs, constraints, and edge       manually extracted metamorphic relations from the legal tax doc-
cases. The two CoderAgent instances participate in an internal re-        uments. Srinivas et al. [34] presented a few-shot in-context learn-
view and refinement cycle orchestrated by the SeniorCoderAgent.           ing to automatically infer metamorphic specifications from legal
First, one CoderAgent generates an initial implementation, and            documents. Following this literature, we initially implement ba-
then the SeniorCoderAgent evaluates this code against the spec-           sic metamorphic testing, perturbing single inputs (e.g., income)
ification. If the implementation is satisfactory, it is accepted; oth-    and verifying that the resulting change in the output aligns with
erwise, the SeniorCoderAgent provides feedback, and the second            expected directional relationships (e.g., increased income should
CoderAgent generates a revised version incorporating these cor-           lead to increased tax). However, we face two key challenges: i) gen-
rections. Although both CoderAgent instances use the same base            erating metamorphic specifications via LLMs in the language of
An LLM Agentic Approach for Legal-Critical Software: A Case Study for Tax Prep Software                                 ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


 Goal: Suggest input tuples for income for a Threshold Jump test.                         detects a metamorphic relation violation—indicating unexpected
 Understanding the Test: Verify that the software correctly handles                       tax behavior—it provides concrete counterexamples to iteratively
 discrete jumps in the rate of change when an input crosses a tax-rule                    enhance the reliability and correctness of the tax software.
 boundary (e.g., a tax bracket).
                                                                                          Example: Publication 970. . The American Opportunity Tax Credit
 Key Requirements for Tuples (𝑥𝑏 , 𝑥 1 , 𝑥 2 ):
                                                                                          (AOTC), outlined in IRS Publication 970, follows a tiered structure
     • Threshold Targeting: Identify a specific tax bracket boundary                      to incentivize the first $4,000 of educational expenses. Specifically,
       from the provided legal text.
                                                                                          it covers 100% of the first $2,000 and 25% of the next $2,000, with
     • Values Around Threshold: Place 𝑥𝑏 and 𝑥 1 just below the thresh-
       old, and 𝑥 2 just above, ensuring a crossing between 𝑥 1 and 𝑥 2 .
                                                                                          a maximum credit of $2,500. A basic 4-ary metamorphic relation
     • Meaningful Jumps: Ensure the increment from 𝑥 1 to 𝑥 2 is large                    may only check whether increasing qualified expenses leads to a
       enough to trigger a distinct change in the tax output.                             higher credit. However, a higher-order relation can examine the
                                                                                          rate of increase in credit as expenses vary.
 Task: Suggest at least four tuples testing different bracket jumps. Respond
                                                                                              The MetamorphicAgent can verify whether the marginal in-
 with a valid JSON containing a list of tuples.
                                                                                          crease in credit is significantly higher for expenses in the $0-$2,000
 Example Response Format:                                                                 range (100%) compared to the $2,001-$4,000 range (25%). Addi-
 {                                                                                        tionally, it can ensure that the credit increase ceases once expenses
     "suggested_tuples": [
                                                                                          exceed $4,000, as the credit cap is reached. By analyzing these chang-
       {
          "input_tuple": [35000, 40525, 48000],                                           ing rates of credit increase for the label {𝑞𝑢𝑎𝑙𝑖 𝑓 𝑖𝑒𝑑_𝑒𝑥𝑝𝑒𝑛𝑠𝑒𝑠}, the
          "reason": "Testing 12% to 22% bracket jump"                                     agent enables more precise validation and error detection.
       },
                                                                                          "discrepancies": [
       ...
                                                                                            {
     ]
                                                                                              "input": "qualified_expenses",
 }
                                                                                              "test_category": "ProportionalIncrease",
                                                                                              "filing_status": "single",
                                                                                              "base_value": 1000,
Figure 3: Summary of the HMT prompt provided to the                                           "new_value_1": 2000,
MetamorphicAgent for the ThresholdJump test category.                                         "new_value_2": 3000,
                                                                                              "verification_result": "FAIL",
                                                                                              "verification_reason": "Credit rate increase isn't consistent
                                                                                                with AOTC's tiered structure. The rate should decrease after
first-order logic is challenging, even for 4-ary relations, and ii) the                         $2000 expenses, but it remains proportionally same.",
                                                                                              "initial_tax": 1000.00,
directional oracle misses many existing bugs.
                                                                                              "modified_tax_tuple": [ 7400.00, 6200.00, 5000.00 ],
    The MetamorphicAgent is engineered to analyze the rate of                                 "Rate_change_base (R1)": 1.20,
change in tax calculations across multiple, related input variations,                         "Rate_change_follow-up (R2)": 1.20
not just pairwise comparisons of the directional change. This allows                        }
us to encode more precise relationships and increase the soundness                        ]

of our code generation. The agent considers three categories for
                                                                                          Worked Example: Generating a Threshold Jump Test. To illustrate
metamorphic relations: i) proportional increase that verifies pro-
                                                                                          how the MetamorphicAgent generates higher-order test cases, we
portional changes in tax output for incremental input changes; ii)
                                                                                          present a worked example for the Threshold Jump category target-
threshold jump that tests expected “jumps” in tax rate change when
                                                                                          ing the income input. The objective is to verify that tax calculation
inputs cross critical thresholds; and iii) saturation that validates tax
                                                                                          reflects the discrete jump in marginal rates when income crosses a
outputs remain invariant when inputs are within saturation ranges.
                                                                                          bracket boundary, a defining feature of progressive taxation.
    Figure 2 illustrates our higher-order metamorphic relations. In
                                                                                             The agent receives a detailed prompt that first explains the meta-
this chart, the horizontal axis (“Credit Input”) marks the specific
                                                                                          morphic property being tested and then provides instructions for
input that is being tested: the base input (𝑥𝑏 ), the first modification
                                                                                          generating valid inputs. A summary of this prompt is shown in
(𝑥 1 ), and the second modification (𝑥 2 ). The black solid line from
                                                                                          Figure 3. Specifically, the LLM is asked to identify a tax threshold
𝑥𝑏 to 𝑥 1 establishes the baseline rate of change. At 𝑥 2 , the chart
                                                                                          from the legal context (e.g., the boundary between the 12% and 22%
shows three possible (expected) outcomes for the tax benefit: the red
                                                                                          brackets at $40,525 for a single filer) and generate a tuple of three
dashed line represents a proportional increase—indicating that the
                                                                                          income values (𝑥𝑏 , 𝑥 1, 𝑥 2 ) positioned to straddle this threshold.
tax benefit changes at the same rate as the baseline; the green dashed
                                                                                             Given this prompt, a capable LLM might return the tuple (35000,
line indicates a threshold jump where the tax benefit increases more
                                                                                          40525, 48000) for a single filer. The test then compares two rates
steeply once a critical input threshold is exceeded; and the yellow
                                                                                          of change relative to the baseline 𝑥𝑏 :
dashed line depicts saturation, where the tax benefit remains nearly
invariant despite further increases in input.                                                  • The first rate of change, 𝑅1 , is computed between the baseline
    Instead of manually encoding metamorphic relations in first-                                 𝑥𝑏 and the first modification 𝑥 1 , which lies at the bracket
order logic, we instruct an LLM-based MetamorphicAgent to gen-                                    boundary. Since both points are effectively within the 12%
erate test cases. Using natural language descriptions, tax rules,                                 marginal tax bracket, the rate is
illustrative examples, and the required output format, the agent                                                     𝐹 (𝑥 1 ) − 𝐹 (𝑥𝑏 )
generates diverse test cases for the given input category. When it                                            𝑅1 =                      ≈ 0.12.
                                                                                                                         𝑥 1 − 𝑥𝑏
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                         Sina Gogani-Khiabani, Ashutosh Trivedi, Diptikalyan Saha, and Saeid Tizpaz-Niari


      • The second rate of change, 𝑅2 , is computed between the same       4.1     Experimental Setup
        baseline 𝑥𝑏 and the second modification 𝑥 2 , which crosses        4.1.1 Benchmarks. To evaluate the effectiveness of LLMs in the tax
        into the 22% bracket. This rate reflects the average change        software domain, we design six benchmarks derived from the U.S.
        over a range that includes income taxed at 22% rate:               federal income tax code. These benchmarks progress in difficulty,
                                     𝐹 (𝑥 2 ) − 𝐹 (𝑥𝑏 )                    from basic computations to complex multi-form scenarios:
                              𝑅2 =                      .
                                         𝑥 2 − 𝑥𝑏
                                                                              (1) Benchmark 1: Brackets and Standard Deductions. A
The metamorphic test passes if the implementation shows 𝑅2 >𝑅1 ,                  foundational task requiring the calculation of income tax
confirming that the average tax rate over the wider range (𝑥𝑏 to                  based on income and filing status, incorporating tax brackets,
𝑥 2 ) is higher than over the initial range (𝑥𝑏 to 𝑥 1 ), as expected in          standard deductions, and age/blindness adjustments.
a progressive system. A faulty implementation, such as applying               (2) Benchmark 2: Earned Income Tax Credit (EITC) [2].
a flat rate, would fail this test because 𝑅1 and 𝑅2 would be approx-              Adds the refundable EITC, which supports low-to-moderate
imately equal. As a sanity check, we manually reviewed a subset                   income workers and families. The LLM must compute credits
of generated test tuples during development to ensure they were                   using income, filing status, and number of children, while
logically sound (e.g., values straddled meaningful thresholds).                   handling the EITC’s nonlinear phase-in and phase-out rules.
                                                                              (3) Benchmark 3: Child Tax Credit (CTC) and Other De-
3.3      Multi-Agent Collaboration                                                pendent Credit (ODC) [3]. Expanding the scope further,
Our framework employs a team of specialized agents, each con-                     this benchmark includes the CTC and ODC, which provide
tributing distinct capabilities to the tax code generation process.               tax benefits to families with children and other dependents.
Below, we outline their collaborative interactions.                               The LLMs must account for phase-out thresholds and credit
                                                                                  amounts, which vary based on income and filing status.
Code Generation. The workflow begins with the TaxExpertAgent,                 (4) Benchmark 4: American Opportunity Tax Credit [18].
which produces tax rule data in JSON format for specific scenar-                  This benchmark focuses on the AOTC, a tax credit for quali-
ios. This JSON is refined until it satisfies schema requirements.                 fied education expenses. To accurately compute the credit
Once it is validated, the TaxExpertAgent generates JSON-based                     amount, the LLMs must consider various factors, includ-
function specifications describing each required function’s purpose,              ing income, filing status, qualified expenses, scholarships,
inputs, outputs, edge cases, and computational steps. These serve                 enrollment status, and the student’s year in school.
as blueprints for the SeniorCoderAgent, which coordinates multi-              (5) Benchmark 5: Itemized Deductions [32]. This bench-
ple CoderAgent instances to implement code that accesses values                   mark introduces the complexity of itemized deductions, al-
from the tax-rule JSON rather than hardcoding constants. This                     lowing taxpayers to deduct certain expenses from their Ad-
design simplifies updates, improves debugging, and enforces con-                  justed Gross Income (AGI) if they exceed the standard deduc-
sistency. The SeniorCoderAgent then selects the best candidate                    tion. Key deductions include medical expenses that surpass
implementations from the coders.                                                  7.5% of AGI, a capped state and local tax (SALT) deduction
                                                                                  of $10,000, as well as deductible home mortgage interest,
Metamorphic Testing. The MetamorphicAgent serves as the driver                    charitable contributions, and casualty or theft losses.
of our counterexample-guided refinement process, working closely              (6) Benchmark 6: 1099-R Distributions and Penalties [1].
with the SeniorCoderAgent. It applies higher-order metamorphic                    The most complex benchmark in our suite, Scenario 6, cen-
relations derived from tax law descriptions to automatically gen-                 ters on retirement and pension distributions reported on
erate test cases and detect discrepancies—violations of expected                  IRS Form 1099-R. It requires computing taxable amounts for
tax behavior. For each discrepancy, it reports the triggering in-                 distributions from diverse sources such as IRAs, annuities,
puts, outputs, and implicated functions. The SeniorCoderAgent                     and pensions. Key challenges include handling capital gains,
then uses these counterexamples to repair the corresponding func-                 applying penalties for early withdrawals under specific con-
tions. Through this iterative feedback loop, guided by higher-order               ditions, and correctly processing exception codes that waive
testing, the framework steadily improves both the robustness and                  these penalties. Accurate implementation also demands use
functional correctness of the generated code.                                     of the IRS Simplified Method to determine the non-taxable
   Our results reflect the outcome of a single run of the framework—              portion of annuity distributions based on factors like cost
from initial JSON specifications through code generation, metamor-                basis and annuitant age. Finally, the system must manage
phic testing, and refinement by the SeniorCoderAgent.                             distribution codes in both string and numeric formats and
                                                                                  apply conditional logic tailored to taxpayer circumstances.
4     Experiments
We conduct a comprehensive evaluation of our multi-agent frame-            4.1.2 Large Language Models. We evaluate the capabilities of sev-
work for tax software generation. Our experiments are designed             eral large language models (LLMs) in automating the process of
to measure how well LLMs, both standalone and embedded in our              generating and validating tax software from natural legal code:
agentic system, can translate U.S. federal tax law into executable
code. We benchmark performance across six progressively complex               (1) GPT-4o (OpenAI). A large-scale language model with 200
tax scenarios derived from IRS publications, ranging from basic                   billion parameters. Known for its advanced natural language
bracket computations to retirement distributions (1099-R).                        understanding and robust code generation capabilities, it
An LLM Agentic Approach for Legal-Critical Software: A Case Study for Tax Prep Software                               ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


       excels in complex tasks requiring nuanced language com-                            regions). Where scope overlapped with open-source tools (e.g.,
       prehension and precise syntactic structure, making it indis-                       OpenTaxSolver [31], Colorado Toolbox [8]), we performed targeted
       pensable in generating precise tax-related functions.                              spot-checks at boundaries to check the correctness of our oracle
   (2) GPT-4o-mini (OpenAI). A smaller and faster variant of                              implementations.
       GPT-4o, with 8 billion parameters. GPT-4o-mini offers im-
                                                                                          4.2.3 Evaluation Metric. In this study, we considered two com-
       proved computational efficiency, making it a suitable choice
                                                                                          mon evaluation metrics for code generation: Pass@k and Partial
       for tasks where speed is prioritized over the depth of lan-
                                                                                          Pass@k, which measure the success rate of generating correct
       guage modeling. This distinction highlights GPT-4o-mini as
                                                                                          solutions within 𝑘 attempts. Pass@k reflects the proportion of gen-
       a small-scale model in contrast to the large-scale GPT-4o.
                                                                                          erations passing all test cases. However, because many benchmarks
   (3) Claude 3.5-Sonnet (Anthropic). A large language model
                                                                                          here involve complex requirements, most LLMs failed to pass all
       developed by Anthropic, emphasizing safety and user align-
                                                                                          tests, making Pass@k an unsuitable measure of performance.
       ment in language processing.
                                                                                             Instead, we chose Partial Pass@k as our primary metric, which
   (4) Llama 3.1-70B (Meta). An open-source model developed by
                                                                                          measures the average percentage of successful test cases over 𝑘
       Meta with 70 billion parameters, representing a large-scale
                                                                                          generations of code. For a comprehensive assessment, we report
       LLM in the Llama family.
                                                                                          the following variants:
   (5) Llama 3.1-8B (Meta). A smaller variant in the Llama family
       with 8 billion parameters. Despite its smaller scale, Llama                             • Partial Pass@10: Average percentage of successful test
       3.1-8B is highly practical, as it can run on edge devices.                                cases across 10 generations, providing an overview of per-
                                                                                                 formance across attempts.
4.1.3 Prompting Approach. To evaluate the capabilities of LLMs in                              • Partial Pass@1: Highest percentage of test cases passed in
translating tax code to tax software, we employ two promptings:                                  a single generation, reflecting best-case performance.
   (1) Zero-Shot Prompting. This generates code autonomously                                   • Worst@10: Lowest percentage of successful test cases across
        based on its general understanding of natural language, tax                              10 generations, representing worst-case performance.
        rules, and programming without any other context.                                 4.2.4 Technical Details. Our experiments were conducted on an
   (2) Step-Wise Chain-of-Thought (COT) Prompting. In Step-                               Amazon Web Services (AWS) g5.8xlarge Ubuntu server, equipped
       Wise Chain-of-Thought approach [42], the LLM is guided                             with GPU support. The framework used for implementing the agen-
        through the task with structured interactions in two stages:                      tic approach in this project was the agentlite library by Salesforce
      (a) Reasoning Stage. The LLM is prompted to reason through                          [24], which provided the necessary abstractions for orchestrating
          the tax rules and specific tax code requirements. This stage                    multi-agent interactions. Symbolic execution was carried out using
          encourages the model to identify key tax policies —e.g., in-                    the Z3 solver [9] to generate and validate test cases based on the
          come thresholds, applicable deductions, and credit limits—                      tax benchmarks. Temperature value for all the models is set to 0.5.
          and to organize these elements logically.
     (b) Code Generation Stage. In the second interaction, the                            4.3    Research Questions
          LLM uses its structured reasoning from the first stage to
                                                                                          We investigate the following questions:
          generate the necessary code.
                                                                                           RQ1 How effectively do baseline LLMs, using zero-shot and step-
4.2     Evaluation Metric and Technical Details                                                 wise chain-of-thought prompting, perform in generating
                                                                                                tax software code across scenarios of varying complexity?
4.2.1 Symbolic Executions. To thoroughly evaluate the generated                            RQ2 How does our LLM-based multi-agent design compare to
tax code, we apply symbolic execution techniques on the ground-                                 the baseline LLMs?
truth tax software. By running symbolic execution on the ground-                           RQ3 How does the integration of the metamorphic testing agent
truth tax software, we collect test cases reflecting each tax bench-                            contribute to the correctness of the generated tax software?
mark’s expected logic and outcomes. These generated test cases are                         RQ4 What is the contribution of each agent in the collaborations?
then used to evaluate the generated code by comparing its outputs                               and what are the cost-accuracy trade-offs?
against the ground-truth software.
                                                                                          4.3.1 RQ1. Baseline LLM Techniques. In examining RQ1, we evalu-
4.2.2 Ground-Truth Oracle & Cross-Reference. We evaluate syn-                             ate the baseline performance of large language models (LLMs) in
thesized programs against a hand-authored reference implemen-                             generating tax software directly from tax code across two prompt-
tation fixed to Tax Year 2021 and aligned strictly with the rules                         ing methods: Zero-Shot and Step-Wise Chain-of-Thought (CoT).
described in our scenarios (§4.1). The oracle spans 10 reference
functions covering: progressive bracket computation (by filing sta-                       Zero-Shot Results (Table 1). Under the zero-shot prompting ap-
tus), standard deductions including age/blind add-ons, EITC phase-                        proach, where models receive minimal guidance, we observe clear
in/plateau/phase-out, CTC/ODC thresholds, AOTC’s 100%/25% tiers                           trends in performance based on model size and task complexity:
with a $2,500 cap, itemized deductions (SALT cap; medical 7.5%                                • Superior Performance of Large Models in Simple Sce-
AGI floor), and 1099-R taxable amounts, early-withdrawal penal-                                  narios. Large models such as GPT-4o (200B parameters)
ties, and the IRS Simplified Method. To ensure the correctness of                                and Claude 3.5 (175B parameters) achieve high partial pass
the oracle implementations, we perform stress-testing at bound-                                  rates in simpler benchmarks. Both models reach PP@1 scores
aries (bracket knees, phase-in/out breakpoints, and cap/saturation                               of over 95% in Scenarios 1 through 5.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                   Sina Gogani-Khiabani, Ashutosh Trivedi, Diptikalyan Saha, and Saeid Tizpaz-Niari


                Table 1: Zero shot prompting results                                        substantial improvements in Scenario 6, reaching a PP@1
                                                                                            score of 42% and a PP@10 of 31%.
  Model          Metric       Scen.1    Scen.2   Scen.3   Scen.4   Scen.5   Scen.6        • Small Models Show Limited Benefit from CoT in Com-
                 PP@1         53%       0%       0%       0%       15%      0%
    llama 8b     PP@10        19%       0%       0%       0%       3%       0%
                                                                                            plex Scenarios. CoT prompting provides only marginal
                 worst@10     4%        0%       0%       0%       0%       0%              improvements for smaller models, such as Llama 8B and
                 PP@1         100%      71%      92%      42%      18%      0%              GPT-4o-mini. For example, GPT-4o-mini shows minimal
   llama70b      PP@10        51%       27%      46%      24%      5%       0%              gains in Scenario 6 with a PP@10 of just 9%, indicating that
                 worst@10     32%       8%       15%      10%      0%       0%
                 PP@1         100%      83%      12%      23%      32%      4%              CoT prompting alone does not significantly enhance smaller
  gpt-4o-mini    PP@10        88%       40%      8%       6%       10%      2%              models’ abilities to handle complex tax logic.
                 worst@10     62%       10%      0%       0%       0%       0%
                 PP@1         100%      91%      94%      98%      98%      23%      Answer RQ1: Claude 3.5 with CoT prompting outperforms other
     gpt-4o      PP@10        95%       82%      71%      62%      56%      18%      models. While it achieves an accuracy up to 98% in benchmarks
                 worst@10     88%       65%      37%      18%      27%      5%       with low-to-moderate complexity, it reaches PP@1 and PP@10
                 PP@1         100%      100%     96%      97%      98%      39%
   claude 3.5    PP@10        100%      86%      96%      97%      93%      29%
                                                                                     scores of 42% and 31% in the most challenging benchmark.
                 worst@10     100%      72%      96%      97%      84%      14%
                                                                                     4.3.2 RQ2. Agentic Design for Tax Software. We evaluate our agen-
                                                                                     tic framework Synedrion with three underlying language models:
   Table 2: Step-Wise Chain of though prompting results
                                                                                     1) GPT-4o-mini (8B), 2) GPT-4o, and 3) Claude-3.5-Sonnet. As
                                                                                     claude-3.5 -sonnet demonstrated the strongest baseline perfor-
  Model          Metric       Scen.1    Scen.2   Scen.3   Scen.4   Scen.5   Scen.6
                 PP@1         59%       0%       0%       0%       0%       0%       mance in our initial zero-shot and chain-of-thought experiments,
    llama 8b     PP@10        31%       0%       0%       0%       0%       0%       we aimed to assess if the agentic framework could further amplify
                 worst@10     12%       0%       0%       0%       0%       0%       its capabilities. We also consider GPT-4o-mini and its larger vari-
                 PP@1         100%      98%      98%      28%      32%      0%
   llama70b      PP@10        78%       47%      71%      12%      11%      0%
                                                                                     ants GPT-4o to test the agentic framework with a range of models
                 worst@10     56%       10%      11%      0%       0%       0%       and demonstrate its effectiveness across diverse LLM capabilities.
                 PP@1         100%      82%      10%      5%       2%       21%      The results, detailed in Table 3, illustrate the effectiveness of our
  gpt-4o-mini    PP@10        84%       46%      6%       2%       1%       9%       agentic approach, which we designed to enable a smaller model
                 worst@10     72%       0%       3%       0%       0%       0%
                 PP@1         100%      98%      93%      68%      64%      28%
                                                                                     to achieve accuracy close to and, in some cases, surpassing that of
     gpt-4o      PP@10        96%       84%      78%      53%      53%      14%      larger, frontier models when using baseline prompting techniques.
                 worst@10     91%       77%      67%      41%      27%      9%
                 PP@1         100%      100%     98%      99%      98%      42%
   claude 3.5    PP@10        100%      94%      98%      98%      98%      31%                Table 3: Performance of the Agentic framework
                 worst@10     100%      85%      98%      96%      98%      15%
                                                                                      Agents      Model         Metric     Scen.1   Scen.2   Scen.3   Scen.4   Scen.5   Scen.6
                                                                                                                PP@1       100%     100%     97%      94%      89%      78%
     • Sharp Declines in Complex Scenarios. As the benchmark                                      gpt-4o-mini   PP@10      100%     100%     92%      84%      75%      62%
                                                                                                                worst@10   100%     100%     88%      75%      61%      45%
       complexity increases, most models show a drop in perfor-                         Coder                   PP@1       100%     100%     100%     100%     95%      89%
       mance, with Scenario 6 (1099-R distributions) being partic-                    +S-Coder      gpt-4o      PP@10      100%     100%     97%      94%      91%      83%
                                                                                      +T-Expert                 worst@10   100%     100%     93%      89%      84%      72%
       ularly challenging. For example, GPT-4o achieves a PP@1                                                  PP@1       100%     100%     100%     100%     100%     93%
       score of 23% and PP@10 of 18%, while Claude 3.5 achieves                                   claude-3.5    PP@10      100%     100%     100%     100%     98%      85%
                                                                                                                worst@10   100%     100%     100%     100%     95%      78%
       PP@1 of 39% and PP@10 of 29%. These results suggest that
       zero-shot prompting alone may be insufficient for handling
       multi-step tax rules involving multiple dependencies and
       conditional calculations.                                                     High Performance Across Scenarios. The agentic approach consis-
     • Limited Capability of Smaller Models in All Scenarios.                        tently delivers high performance across all benchmarks. For simpler
       Small models such as Llama 8B and GPT-4o-mini (8B pa-                         scenarios (1 & 2), GPT-4o-mini, GPT-4o, and claude-3.5 all reach
       rameters) struggled across benchmarks, showing low partial                    100% on both PP@1 and PP@10. In more complex benchmarks, such
       pass rates in all cases except the simplest one.                              as Scenario 6, claude-3.5 achieved PP@1, PP@10, and worst@10
                                                                                     scores of 93%, 85%, and 78%, respectively.
Step-Wise Chain-of-Thought Results (Table 2). The chain-of-thought
                                                                                     Improvement of the Worst-case Accuracy. A key advantage of the
(CoT) prompting yields substantial improvements in both accuracy
                                                                                     agentic approach is its capacity to maintain consistency in accuracy.
and consistency, particularly for large models:
                                                                                     For example, GPT-4o-mini achieves a worst@10 score of 45% in
    • Enhanced Consistency and Accuracy in Large Models.                             Scenario 6, a significant improvement compared to 9% for CoT re-
       CoT prompting boosts accuracy by a small margin, but it im-                   sults. Similarly, claude-3.5-sonnet achieves a significantly higher
       proves consistency of models, especially in moderately com-                   worst@10 score of 78% in Scenario 6.
       plex benchmarks. For instance, GPT-4o achieves worst@10
       scores of 77% in Scenario 2, up from 65% in zero-shot.                        Enabling Small Models to Handle Complex Reasoning Tasks. In zero-
    • Top-Performing Model in Complex Scenarios. Claude                              shot and CoT settings, smaller models (e.g., GPT-4o-mini and Llama
       3.5 shows the highest scores across complex benchmarks,                       8B) often failed to pass any test cases in complex benchmarks, with
      with near-perfect PP@10 scores in Scenario 5 (98%) and                         PP@1 and worst@10 scores close to 0%. By contrast, the agentic
An LLM Agentic Approach for Legal-Critical Software: A Case Study for Tax Prep Software                                ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


GPT-4o-mini achieved PP@10 scores of 75% and 62% in Scenario 5
and 6, respectively.
 Answer RQ2: Our multi-agent design with a smaller model like
 GPT-4o-mini shows performance similar to or better than fron-
 tier baseline models. With claude-3.5 agents, our framework
 achieved PP@1, PP@10, and worst@10 scores of 93%, 85%, and
 78%, respectively, in the most complex scenario.

4.3.3 RQ3. Contributions of Metamorphic Agent. Next, we inte-
grate the MetamorphicAgent into our agentic framework. We ana-
lyze the contributions of two levels of metamorphic testing: 4-ary
metamorphic testing (MT) and higher-order metamorphic testing
(HMT). Table 4 presents the performance improvements achieved
by incorporating these metamorphic testing approaches.                                          Figure 4: Token Usage: without MT, MT, and HMT.
Metamorphic Testing. (MT). We first generate counterexamples by
directional changes in tax calculations (e.g., increasing income                          Tax Expert Agent while keeping other agents on GPT-4o-mini
should increase tax). This shows notable improvements. For in-                            improves robustness (see Worst@10 scores).
stance, in Scenario 6 with GPT-4o-mini, incorporating 4-ary MT                               The integration of Metamorphic Testing Agents provides a sig-
improved the worst@10 score from 45% (without MT) to 55%. Sim-                            nificant synergistic boost to the agentic framework, primarily en-
ilarly, with GPT-4o, the worst@10 metric in Scenario 6 rose from                          hancing robustness and reliability. Adding 4-ary MT demonstrably
72% to 83% with 4-ary MT, demonstrating robustness even with a                            improves worst@10 scores, indicating increased resilience. For ex-
stronger LLM. PP@10 for all scenarios also increased 5-10%.                               ample, in Scenario 6, HMT increased GPT-4o-mini’s worst@10 69%
                                                                                          and GPT-4o’s worst@10 to an impressive 88%.
Higher-order Metamorphic testing. (HMT). Building upon 4-ary MT,
we introduced Higher-order Metamorphic Testing (HMT) incorpo-                             Token Usage and Computational Cost Breakdown: A detailed to-
rating n-ary metamorphic relations. The performance gains with                            ken usage analysis reveals key computational cost considerations,
HMT are even more pronounced, especially in robustness met-                               particularly the balance between input and output tokens across
rics. In Scenario 6 with GPT-4o-mini, HMT further improved the                            different phases of our framework. As depicted in Figure 4, token
worst@10 score to 69%. The most striking improvement is observed                          consumption increases with scenario complexity. For Scenario 1,
with GPT-4o in Scenario 6, where HMT pushes the worst@10 score                            basic agentic code generation totals 18,457 tokens, with metamor-
to 88% (MT achieves a score of 72%). HMT enables the framework                            phic testing dramatically increasing this to 77,438 tokens, primarily
to generate a fully correct code even in the most complex scenario.                       due to a surge in input prompt tokens. This trend is amplified in
                                                                                          Scenario 6, the most complex case, where code generation totals
PP@10 and Convergence with Metamorphic Testing: Both MT and                               111,081 tokens while incorporating Higher-Order Metamorphic
HMT contribute to improve the PP@10 score. HMT consistently                               Testing leads to a substantial increase to 450,134 tokens.
yields the highest PP@10 scores, especially in complex scenarios.                          Answer RQ4: Our results show that TaxExpertAgent and
For example, in Scenario 6 with GPT-4o-mini, PP@10 reaches 68%                             MetamorphicTestingAgents are critical components of our
with MT and further increases to 75% with HMT.                                             framework. Metamorphic Testing, especially HMT, significantly
 Answer RQ3: While generating counterexamples via metamor-                                 enhances robustness in the worst-case code generation.
 phic testing (MT) improves the functional correctness of tax soft-
 ware, Higher-order MT provides superior gains, especially in                             4.4    Discussion
 complex scenarios. For example, HMT improves worst@10 scores
 by 14% over the MT for GPT-4o-mini in Scenario 6.                                        Code-Specific LLMs. We selected general-purpose LLMs over mod-
                                                                                          els specifically tuned for code generation. The rationale for selecting
4.3.4 RQ4. Analysis of Different Agents. This section analyzes each                       those models is driven by the need for models demonstrating ex-
agent’s distinct and synergistic contributions within our multi-                          pertise in natural legal language processing, code generation, and
agent framework. Table 5 summarizes the performance across vari-                          metamorphic test cases. While there are models specialized for code
ous agents and LLM capabilities.                                                          generation, the task at hand requires a deep understanding of tax
                                                                                          regulations, often expressed in complex legal language.
Agents’ Contributions. The Tax Expert Agent consistently emerges
                                                                                          Few-Shot Learning. Few-shot prompting typically involves provid-
as one of the most impactful individual agents. As demonstrated in
                                                                                          ing sample code snippets as examples for the LLM, guiding it to
Table 5, adding the Tax Expert Agent to the "Coder Only" setup (with
                                                                                          generate similar solutions. However, in the tax software domain,
GPT-4o-mini) dramatically increased PP@1 scores from 12% to 97%
                                                                                          providing sample code may lead to outcomes that are more about
for a medium complexity scenario. This agent’s ability to structure
                                                                                          pattern replication than an in-depth understanding of the tax logic.
tax rules and create precise function descriptions is needed for accu-
rate code generation, particularly as scenario complexity increases.                      Agents with varying LLM capabilities. While exploring all LLM com-
Furthermore, leveraging a more powerful LLM like GPT-4o for the                           binations is infeasible, we perform a set of experiments to gain
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                  Sina Gogani-Khiabani, Ashutosh Trivedi, Diptikalyan Saha, and Saeid Tizpaz-Niari


   Table 4: Our framework with MetamorphicAgent. MT and HMT refer to regular and higher-order metamorphic testing.

                                        Agents                  Model           Metric    Scen.1   Scen.2   Scen.3   Scen.4   Scen.5   Scen.6
                                                                               PP@1       100%     100%     97%      94%      89%      78%
                                                           gpt-4o-mini         PP@10      100%     100%     92%      84%      75%      62%
                                                                               worst@10   100%     100%     88%      75%      61%      45%
                                                                               PP@1       100%     100%     100%     100%     95%      89%
                            Coder + S-Coder + T-Expert     gpt-4o              PP@10      100%     100%     97%      94%      91%      83%
                                                                               worst@10   100%     100%     93%      89%      84%      72%
                                                                               PP@1       100%     100%     100%     100%     100%     93%
                                                           claude-3.5-sonnet   PP@10      100%     100%     100%     100%     98%      85%
                                                                               worst@10   100%     100%     100%     100%     95%      78%
                                                                               PP@1       100%     100%     96%      94%      88%      80%
                                                           gpt-4o-mini         PP@10      100%     100%     94%      88%      83%      68%
                                                                               worst@10   100%     100%     91%      83%      78%      55%
                                                                               PP@1       100%     100%     100%     100%     98%      91%
                         Coder + S-Coder + T-Expert + MT   gpt-4o              PP@10      100%     100%     97%      94%      92%      86%
                                                                               worst@10   100%     100%     94%      92%      89%      83%
                                                                               PP@1       100%     100%     100%     100%     100%     93%
                                                           claude-3.5-sonnet   PP@10      100%     100%     100%     100%     99%      90%
                                                                               worst@10   100%     100%     100%     100%     98%      86%
                                                                               PP@1       100%     100%     100%     94%      89%      81%
                                                           gpt-4o-mini         PP@10      100%     100%     95%      91%      86%      75%
                                                                               worst@10   100%     100%     92%      89%      82%      69%
                                                                               PP@1       100%     100%     100%     100%     100%     100%
                        Coder + S-Coder + T-Expert + HMT   gpt-4o              PP@10      100%     100%     100%     96%      95%      93%
                                                                               worst@10   100%     100%     100%     94%      91%      88%
                                                                               PP@1       100%     100%     100%     100%     100%     100%
                                                           claude-3.5-sonnet   PP@10      100%     100%     100%     100%     99%      95%
                                                                               worst@10   100%     100%     100%     100%     98%      93%


some insights into when agents are heterogeneous. For instance, in                  5     Related Work
configurations where the TaxExpertAgent utilized GPT-4o while                       Research on multi-agent systems for automated code generation,
CoderAgent and SeniorCoderAgent used GPT-4o-mini, we ob-                            debugging, and testing has made considerable progress.
served a PP@10 score of 73% in Scenario 6, compared to a score of
62% for all GPT-4o-mini agents and 83% for all GPT-4o agents. This                  Agent-Based Code Generation. Several studies focus on agent-based
shows that a heterogeneous design may well bounded by smaller                       code generation and testing. For instance, AgentCoder [16] orga-
and larger homogeneous agents. We left further analysis in this                     nizes agents to generate and refine code through iterative feed-
direction to the future work.                                                       back, creating a modular structure for complex tasks. Similarly,
                                                                                    CodeChain [21] divides projects into smaller, manageable sub-
Legal-Critical Software. Although we focused on the US-based tax
                                                                                    modules refined through self-revisions, allowing for better inte-
prep software, the key takeaway is the application of the agentic
                                                                                    gration to address intricate coding tasks. In a related approach,
approach with metamorphic testing for legal-critical software [11,
                                                                                    SoapFL [30] includes agents dedicated to validation and fault identi-
26, 27]. For example, our framework can be used to find errors in
                                                                                    fication, ensuring that issues are promptly identified. Recent frame-
poverty management systems (e.g., the Pennsylvania “Do I Qual-
                                                                                    works such as ReAct [41] and Reflexion [33] emphasize the benefits
ify?” [29]) where the prior work relied on manual interpretation and
                                                                                    of interleaving reasoning with action and self-reflection.
assumed the presence of multiple versions of the same software [11].
Our approach can automate policy translation into executable code                   Feedback Mechanisms. Feedback loops are crucial for refining code
and validate it with metamorphic testing.                                           quality. SelfRefine [25] builds in feedback mechanisms that en-
Limited Categories of Higher-Order MT. Despite HMT’s improved                       able agents to iteratively analyze and improve their outputs (e.g.,
bug detection capabilities over basic MT, our approach does not                     source-code generation), while CodePlan [5] incorporates planning
guarantee identifying and eliminating all potential errors. Further-                capabilities to adjust actions based on previous changes adaptively.
more, our HMT inherently focuses on three categories of metamor-
phic relations and does not guarantee that all possible tax calcula-                Debugging and Fault Localization. Debugging and fault localization
tion behaviors or edge cases will be covered.                                       are also critical. SoapFL [30] utilizes specialized agents for project-
                                                                                    level code review to identify errors through detailed inspection,
Ground-Truth Software. Our evaluation significantly depends on                      and RCAgent [38] adds memory components to track decisions,
the correctness of ground-truth tax software. We manually check                     facilitating error localization in cloud systems.
the correctness of our reference code by inspecting the source code,
stress-testing at boundaries, and cross-referencing to open-source                  Metamorphic Testing. For testing without known correct answers,
tax software toolkits. Due to the lack of formal guarantees, our                    metamorphic testing is especially effective. Recent work such as
reference implementations may contain logical bugs.                                 METAL [17] can automate generation of metamorphic relations.
An LLM Agentic Approach for Legal-Critical Software: A Case Study for Tax Prep Software                                      ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


                            Table 5: Comparative Results of Abolishing Agents with Varying LLM Capabilities.

                           Agents              Model           Metric    Scenario 1   Scenario 2   Scenario 3   Scenario 4    Scenario 5   Scenario 6
                                                               PP@1        100%          83%          12%          23%           32%           4%
                                             gpt-4o-mini       PP@10        88%          40%           8%           6%           10%           2%
                                                              worst@10      62%          10%           0%           0%           0%            0%
                                                               PP@1        100%          91%          94%          98%           98%          23%
                         Coder Only            gpt-4o          PP@10        95%          82%          71%          62%           56%          18%
                                                              worst@10      88%          65%          37%          18%           27%           5%
                                                               PP@1        100%         100%          96%          97%           98%          39%
                                          claude-3.5-sonnet    PP@10       100%          86%          96%          97%           93%          29%
                                                              worst@10     100%          72%          96%          97%           84%          14%
                                                               PP@1        100%         100%          97%          94%           89%          78%
                                             gpt-4o-mini       PP@10       100%         100%          92%          84%           75%          62%
                                                              worst@10     100%         100%          88%          75%           61%          45%
                            Coder                              PP@1        100%         100%         100%         100%           95%          89%
                          +S-Coder             gpt-4o          PP@10       100%         100%          97%          94%           91%          83%
                          +T-Expert                           worst@10     100%         100%          93%          89%           84%          72%
                                                               PP@1        100%         100%         100%         100%          100%          93%
                                          claude-3.5-sonnet    PP@10       100%         100%         100%         100%           98%          85%
                                                              worst@10     100%         100%         100%         100%           95%          78%
                                                               PP@1        100%         100%          96%          94%           88%          80%
                                             gpt-4o-mini       PP@10       100%         100%          94%          88%           83%          68%
                                                              worst@10     100%         100%          91%          83%           78%          55%
                           Coder                               PP@1        100%         100%         100%         100%           98%          91%
                          +S-Coder             gpt-4o          PP@10       100%         100%          97%          94%           92%          86%
                       +T-Expert + MT                         worst@10     100%         100%          94%          92%           89%          83%
                                                               PP@1        100%         100%         100%         100%          100%          93%
                                          claude-3.5-sonnet    PP@10       100%         100%         100%         100%           99%          90%
                                                              worst@10     100%         100%         100%         100%           98%          86%
                                                               PP@1        100%         100%         100%          94%           89%          81%
                                             gpt-4o-mini       PP@10       100%         100%          95%          91%           86%          75%
                                                              worst@10     100%         100%          92%          89%           82%          69%
                           Coder                               PP@1        100%         100%         100%         100%          100%         100%
                          +S-Coder             gpt-4o          PP@10       100%         100%         100%          96%           95%          93%
                      +T-Expert + HMT                         worst@10     100%         100%         100%          94%           91%          88%
                                                               PP@1        100%         100%         100%         100%          100%         100%
                                          claude-3.5-sonnet    PP@10       100%         100%         100%         100%           99%          95%
                                                              worst@10     100%         100%         100%         100%           98%          93%



Collaborative Frameworks. Collaborative frameworks boost the ef-                             At the same time, our study highlights important challenges. Test
fectiveness of these systems. Gentopia [40] organizes agents in                           case generation in legally critical domains continues to suffer from
a network where each insight contributes to reliable outcomes.                            the oracle problem, where correct outputs are difficult to determine
Other architectures [20, 43], such as layered or tree-like structures,                    without expert interpretation. While higher-order metamorphic
efficiently manage agent interactions. Unified approaches like RCA-                       testing mitigates this, it also introduces significant computational
gent [38] integrate error localization and solution generation into a                     overhead, as shown in our token usage analysis. Moreover, although
collaborative process. The key innovation of our work lies in integrat-                   smaller models like GPT-4o-mini can outperform frontier LLMs
ing legal experts into the multi-agent system design and introducing                      under our agentic framework, scaling these methods to other legal
a metamorphic testing agent within the code generation process.                           domains will require careful balance between accuracy, efficiency,
                                                                                          and interpretability.
                                                                                             Ultimately, this research points toward a broader vision: LLM-
6    Conclusion
                                                                                          driven agentic methodologies that combine domain expertise with
This work introduced an agentic approach for generating reliable                          systematic testing can translate complex legal rules into transparent,
tax software from complex legal tax codes, with a central focus on                        verifiable, and trustworthy software, advancing accountability and
metamorphic testing. Our multi-agent system, comprising special-                          accessibility in critical public services.
ized agents for tax expertise, code generation, and quality control,
effectively interprets, structures, and translates intricate tax regu-                    Acknowledgments
lations into executable code. The iterative feedback loops within
                                                                                          This project has been partially supported by NSF under grants CCF-
the agentic framework, particularly driven by the Metamorphic
                                                                                          2532965, CCF-2317206, and CCF-2317207. Ashutosh Trivedi is a
Agent, enable continuous refinement and ensure high reliability
                                                                                          Royal Society Wolfson Visiting Fellow and gratefully acknowledges
and accuracy, especially in handling deductions, credits, and retire-
                                                                                          the support of the Wolfson Foundation and the Royal Society.
ment distributions. Future work can extend our agentic approach to
other legal-critical software, such as poverty management systems,
offering a robust pathway for translating complex legal texts into
dependable executable software.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                        Sina Gogani-Khiabani, Ashutosh Trivedi, Diptikalyan Saha, and Saeid Tizpaz-Niari


References                                                                                     Caiming Xiong, and Silvio Savarese. 2024. AgentLite: A Lightweight Library for
 [1] IRS Forms 1099-R and 5498. 2021. Instructions for Forms 1099-R and 5498.                  Building and Advancing Task-Oriented LLM Agent System. ArXiv abs/2402.15538
     https://www.irs.gov/instructions/i1099r. Online.                                          (2024). https://api.semanticscholar.org/CorpusID:267938239
 [2] IRS 596. 2021. Earned Income Credit (EIC). https://www.irs.gov/pub/irs-pdf/          [25] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah
     p596.pdf. Online.                                                                         Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Sean
 [3] IRS 8812. 2021. Credits for Qualifying Children and Other Dependents. https:              Welleck, Bodhisattwa Prasad Majumder, Shashank Gupta, Amir Yazdanbakhsh,
     //www.irs.gov/forms-pubs/about-schedule-8812-form-1040. Online.                           and Peter Clark. 2023. Self-Refine: Iterative Refinement with Self-Feedback.
 [4] John Ahlgren, Maria Berezin, Kinga Bojarczuk, Elena Dulskyte, Inna Dvortsova,             arXiv:2303.17651 [cs.CL]
     Johann George, Natalija Gucevska, Mark Harman, Maria Lomeli, Erik Meijer,            [26] Jeanna Matthews, Marzieh Babaeianjelodar, Stephen Lorenz, Abigail Matthews,
     et al. 2021. Testing Web Enabled Simulation at Scale Using Metamorphic Testing.           Mariama Njie, Nathaniel Adams, Dan Krane, Jessica Goldthwaite, and Clinton
     In 2021 IEEE/ACM 43rd International Conference on Software Engineering: Software          Hughes. 2019. The Right To Confront Your Accusers: Opening the Black Box of
     Engineering in Practice (ICSE-SEIP). IEEE, 140–149.                                       Forensic DNA Software. In Proceedings of the 2019 AAAI/ACM Conference on AI,
 [5] Ramakrishna Bairi, Atharv Sonwane, Aditya Kanade, Vageesh D. C., Arun Iyer,               Ethics, and Society (AIES ’19). 321–327. https://doi.org/10.1145/3306618.3314279
     Suresh Parthasarathy, Sriram Rajamani, B. Ashok, and Shashank Shet. 2024.            [27] Jeanna Neefe Matthews, Graham Northup, Isabella Grasso, Stephen Lorenz,
     CodePlan: Repository-Level Coding using LLMs and Planning. Proceedings                    Marzieh Babaeianjelodar, Hunter Bashaw, Sumona Mondal, Abigail Matthews,
     of the ACM on Software Engineering 1, FSE, Article 31 (July 2024), 24 pages.              Mariama Njie, and Jessica Goldthwaite. 2020. When Trusted Black Boxes Don’t
     https://doi.org/10.1145/3643757                                                           Agree: Incentivizing Iterative Improvement and Accountability in Critical Software
 [6] A Bandura. 2001. Social cognitive theory: an agentic perspective. Annual Review           Systems. Association for Computing Machinery, 102–108. https://doi.org/10.
     of Psychology 52 (2001), 1–26. https://doi.org/10.1146/annurev.psych.52.1.1               1145/3375627.3375807
 [7] Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, and Shin Yoo. 2015.        [28] Rohan Padhye. 2024. Software engineering methods for ai-driven deductive legal
     The Oracle Problem in Software Testing: A Survey. IEEE Transactions on Software           reasoning. In Proceedings of the 2024 ACM SIGPLAN International Symposium on
     Engineering 41, 5 (2015), 507–525. https://doi.org/10.1109/TSE.2014.2372785               New Ideas, New Paradigms, and Reflections on Programming and Software. 85–95.
 [8] Colorado Tax-Aide Program. 2024. Colorado Resource Toolbox. https://cotaxaide.       [29] Pennsylvania Department of Human Services. 2022. COMPASS HHS Do I Qualify?
     org/tools/. Accessed: 2025-09-13.                                                         https://www.compass.state.pa.us/Compass.Web/Screening. Accessed: 2025-09-
 [9] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An efficient SMT solver. In              13.
     International conference on Tools and Algorithms for the Construction and Analysis   [30] Yihao Qin, Shangwen Wang, Yiling Lou, Jinhao Dong, Kaixin Wang, Xiaoling Li,
     of Systems. Springer, 337–340.                                                            and Xiaoguang Mao. 2024. SoapFL: A Standard Operating Procedure for LLM-
[10] Nel Escher and Nikola Banovic. 2020. Exposing Error in Poverty Management                 based Method-Level Fault Localization. IEEE Transactions on Software Engineering
     Technology: A Method for Auditing Government Benefits Screening Tools. Proc.              (2024).
     ACM Hum. Comput. Interact. 4, CSCW (2020), 064:1–064:20. https://doi.org/10.         [31] Aston Roberts. 2024. Open Tax Solver. https://sourceforge.net/projects/
     1145/3392874                                                                              opentaxsolver/. Online.
[11] Nel Escher and Nikola Banovic. 2020. Exposing Error in Poverty Management            [32] IRS Schedule-A. 2021. Itemized Deductions. https://www.irs.gov/pub/irs-pdf/
     Technology: A Method for Auditing Government Benefits Screening Tools. Pro-               f1040sa.pdf. Online.
     ceedings of the ACM on Human-Computer Interaction 4, CSCW1, Article 64 (May          [33] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and
     2020), 20 pages. https://doi.org/10.1145/3392874                                          Shunyu Yao. 2023. Reflexion: Language agents with verbal reinforcement learning.
[12] Angela Fan, Beliz Gokkaya, Mark Harman, Mitya Lyubarskiy, Shubho Sengupta,                Advances in Neural Information Processing Systems 36 (2023), 8634–8652.
     Shin Yoo, and Jie M Zhang. 2023. Large language models for software engineering:     [34] Dananjay Srinivas, Rohan Das, Saeid Tizpaz-Niari, Ashutosh Trivedi, and
     Survey and open problems. arXiv preprint arXiv:2310.03533 (2023).                         Maria Leonor Pacheco. 2023. On the Potential and Limitations of Few-Shot
[13] Sina Gogani-Khiabani, Varsha Dewangan, Nina Olson, Ashutosh Trivedi, and                  In-Context Learning to Generate Metamorphic Specifications for Tax Prepara-
     Saeid Tizpaz-Niari. 2025. Technical Challenges in Maintaining Tax Prep Software           tion Software. arXiv:2311.11979 [cs.SE] The Proceedings of the Natural Legal
     with Large Language Models. arXiv:2504.18693 [cs.SE] https://arxiv.org/abs/               Language Processing Workshop, EMNLP 2023.
     2504.18693 In Fourteenth Annual IRS-TPC Joint Research Conference on Tax             [35] TaxPrep4Free.org. 2017. TaxSlayer Pro Online Quirks (Bugs, Tips, Workarounds,
     Administration.                                                                           etc...). https://ty2016.taxprep4free.org/TaxSlayer/Quirks.html. Online; ACA
[14] Sina Gogani-Khiabani, Ashutosh Trivedi, ShinPing Chyi, and Saeid Tizpaz-Niari.            calculation issues section; accessed 2026-03-03.
     2025. Performance of LLMs on VITA test: potential for AI-assisted tax returns        [36] Saeid Tizpaz-Niari, Shiva Darian, and Ashutosh Trivedi. 2024. Metamorphic
     for low income taxpayers. Artificial Intelligence and Law (2025), 1–22.                   Debugging for Accountable Software. arXiv:2409.16140 [cs.SE] https://arxiv.org/
[15] Abram Hindle, Earl T Barr, Mark Gabel, Zhendong Su, and Premkumar Devanbu.                abs/2409.16140 In the 3rd International Workshop on Programming Languages
     2016. On the naturalness of software. Commun. ACM 59, 5 (2016), 122–131.                  and the Law (ProLaLa’24).
[16] Dong Huang, Jie M Zhang, Michael Luck, Qingwen Bu, Yuhao Qing, and Heming            [37] Saeid Tizpaz-Niari, Verya Monjezi, Morgan Wagner, Shiva Darian, Krystia
     Cui. 2023. Agentcoder: Multi-agent-based code generation with iterative testing           Reed, and Ashutosh Trivedi. 2023. Metamorphic Testing and Debugging of
     and optimisation. arXiv preprint arXiv:2312.13010 (2023).                                 Tax Preparation Software. In 2023 IEEE/ACM 45th International Conference
[17] Sangwon Hyun, Mingyu Guo, and M Ali Babar. 2024. METAL: Metamorphic                       on Software Engineering: Software Engineering in Society (ICSE-SEIS). 138–149.
     Testing Framework for Analyzing Large-Language Model Qualities. In 2024 IEEE              https://doi.org/10.1109/ICSE-SEIS58686.2023.00019
     Conference on Software Testing, Verification and Validation (ICST). IEEE, 117–128.   [38] Zefan Wang, Zichuan Liu, Yingying Zhang, Aoxiao Zhong, Jihong Wang, Fengbin
[18] Internal Revenue Service. 2025. Form 8863: Education Credits (American Oppor-             Yin, Lunting Fan, Lingfei Wu, and Qingsong Wen. 2024. RCAgent: Cloud Root
     tunity and Lifetime Learning Credits). https://www.irs.gov/pub/irs-pdf/f8863.pdf.         Cause Analysis by Autonomous Agents with Tool-Augmented Large Language
     PDF; accessed 2026-03-03.                                                                 Models. In Proceedings of the 33rd ACM International Conference on Information
[19] Internal Revenue Service. 2026. Six Reasons Why You Should File Your Taxes                and Knowledge Management (CIKM ’24). Association for Computing Machinery,
     Electronically — YouTube Video Text Script. https://www.irs.gov/newsroom/six-             New York, NY, USA, 4966–4974. https://doi.org/10.1145/3627673.3680016
     reasons-why-you-should-file-your-taxes-electronically-youtube-video-text-            [39] IBIS World. 2023. Tax Preparation Services in the US — Market Size, Industry Anal-
     script. Online; accessed 2026-03-03.                                                      ysis, Trends and Forecasts. https://www.ibisworld.com/united-states/market-
[20] Md Ashraful Islam, Mohammed Eunus Ali, and Md Rizwan Parvez. 2024. Map-                   research-reports/tax-preparation-services-industry/. Online.
     coder: Multi-agent code generation for competitive problem solving. In Proceed-      [40] Binfeng Xu, Xukun Liu, Hua Shen, Zeyu Han, Yuhan Li, Murong Yue, Zhiyuan
     ings of the 62nd Annual Meeting of the Association for Computational Linguistics          Peng, Yuchen Liu, Ziyu Yao, and Dongkuan Xu. 2023. Gentopia. ai: A collabo-
     (Volume 1: Long Papers). 4912–4944.                                                       rative platform for tool-augmented llms. In Proceedings of the 2023 Conference
[21] Hung Le, Hailin Chen, Amrita Saha, Akash Gokul, Doyen Sahoo, and Shafiq                   on Empirical Methods in Natural Language Processing: System Demonstrations.
     Joty. 2024. CodeChain: Towards Modular Code Generation Through Chain of                   237–245.
     Self-revisions with Representative Sub-modules. In The Twelfth International Con-    [41] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan,
     ference on Learning Representations. https://openreview.net/forum?id=vYhglxSj8j           and Yuan Cao. 2023. React: Synergizing reasoning and acting in language models.
[22] Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov,            In International Conference on Learning Representations (ICLR).
     Chenghao Mou, Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, et al. 2023.       [42] Zihan Yu, Liang He, Zhen Wu, Xinyu Dai, and Jiajun Chen. 2023. Towards
     Starcoder: may the source be with you! arXiv preprint arXiv:2305.06161 (2023).            Better Chain-of-Thought Prompting Strategies: A Survey. arXiv preprint
[23] Junwei Liu, Kaixin Wang, Yixuan Chen, Xin Peng, Zhenpeng Chen, Lingming                   arXiv:2310.04959 (2023).
     Zhang, and Yiling Lou. 2024. Large language model-based agents for software          [43] Daoguang Zan, Ailun Yu, Wei Liu, Dong Chen, Bo Shen, Yafen Yao, Wei Li,
     engineering: A survey. arXiv preprint arXiv:2409.02977 (2024).                            Xiaolin Chen, Yongshun Gong, Bei Guan, Zhiguang Yang, Yongji Wang, Lizhen
[24] Zhiwei Liu, Weiran Yao, Jianguo Zhang, Liangwei Yang, Zuxin Liu, Juntao Tan,              Cui, and Qianxiang Wang. 2025. CodeS: Natural Language to Code Repository via
     Prafulla Kumar Choubey, Tian Lan, Jason Wu, Huan Wang, Shelby Heinecke,                   Multi-Layer Sketch. ACM Transactions on Software Engineering and Methodology
                                                                                               (2025).
