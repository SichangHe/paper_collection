                                                  Formally Verified Code Synthesis for Structured Data Translation in a
                                                                      Medical Internet of Things


                                                                                      Colin Samplawski 1 Adam D. Cobb 1


                                                                   Abstract                                   In this work, we introduce a code synthesis pipeline that
                                                                                                              formally verifies synthesized code for a Medical Internet
                                                In this work we present a LLM powered, evolu-                 of Things (MIoT) network (Dimitrov, 2016). This work is
arXiv:2606.20776v1 [cs.SE] 18 Jun 2026




                                                tionary code synthesis system for structured data             part of a broader project with the goal of reconfiguring a
                                                translation in a Medical Internet of Things set-              vehicle with medical devices, such that the vehicle is primed
                                                tings. A key challenge in this domain is ensuring             to deliver mobile care. A key challenge of this project is the
                                                that the synthesized code is trustworthy and reli-            integration of novel medical devices to the vehicle’s MIoT
                                                able. To this end, we integrate a formal verifica-            network over time, without assuming any available (human)
                                                tion step into our code synthesis pipeline to ensure          software development expertise. Furthermore, given the
                                                that any generated code is guaranteed to satisfy              safety-critical nature of the system, any automatically syn-
                                                predefined requirements. In particular, we present            thesized code must be performed in a manner that ensures
                                                a case study of integrating a novel device (a pulse           reliability and trust.
                                                oximeter) into the existing network of devices.
                                                Our system generates a formally verified trans-               To tackle this problem, we follow a neuro-symbolic architec-
                                                lation between the device’s JSON schema and                   ture. We use a neural module that uses LLMs as operators
                                                the Fast Healthcare Interoperability Resources                within an evolutionary algorithm (Lange et al., 2025) and
                                                (FHIR) format used by the wider system. This                  a theorem prover module which we have adapted to JSON
                                                formal verification stage ensures structured data             schema verification (Owre & Shankar, 1999). This archi-
                                                translated by the generated code will always be               tecture ensures that the significant reasoning power of the
                                                in the target output schema. We provide a set                 LLM is grounded by the formal theorem prover. As a proof
                                                of experimental results which demonstrate that                of concept, we present a case study of using our proposed
                                                our system is able to consistently generate correct           system to integrate a pulse oximeter into our MIoT envi-
                                                translation at low cost.                                      ronment. We translate the device’s provided JSON schema
                                                                                                              to the more standard Fast Healthcare Interoperability Re-
                                                                                                              sources (FHIR) (Vorisek et al., 2022). We perform a set of
                                                                                                              experiments to analyze the success rate and resource cost
                                         1. Introduction                                                      of using our approach to generate a formally verified trans-
                                                                                                              lation in this setting. We find that our system is able to
                                         Large language model (LLM) powered code synthesis has
                                                                                                              consistently generate correct translations at low cost.
                                         become an increasingly important tool for modern software
                                         development (Jalil, 2025). While these tools can enable              This rest of this paper is structured as follows. In Section
                                         significant gains in productivity, they also introduce sig-          2 we discuss background work and motivation. Then we
                                         nificant risk and novel challenges. LLMs are well known              introduce our approach and summarize its constituent parts
                                         to hallucinate and can introduce subtle vulnerabilities into         in Section 3. In Section 4 we present results of our pulse
                                         the code (Kalai et al., 2025). These problems are further            oximeter case study. Finally we provide an overview of
                                         compounded by the shear scale and speed of LLM code                  future directions and conclude in Section 5.
                                         generation, making manual human verification of critical
                                         code laborious and intractable. These risks are especially           2. Background
                                         acute in safety-critical domains, such as a healthcare.
                                            1
                                                                                                              2.1. Evolutionary Algorithms with LLMs
                                             Computer Science Laboratory, SRI International. Correspon-
                                         dence to: Colin Samplawski <colinsamplawski@gmail.com>.              Significant recent work has considered using LLMs as the
                                                                                                              primary operators inside evolutionary algorithms for code
                                         Proceedings of the Workshop on Structured Data for Health at
                                         the 43 rd International Conference on Machine Learning, Seoul,
                                                                                                              optimization and scientific discovery (Novikov et al., 2025;
                                         South Korea. Copyright 2026 by the author(s).                        Sharma, 2025; Lange et al., 2025). In these systems, the

                                                                                                          1
                          Submission and Formatting Instructions for SD4H Workshop at ICML 2026

LLM replaces traditional mutation and crossover operators
by proposing semantically meaningful program edits, design
variations, or hypotheses conditioned on prior search his-
tory. This approach is appealing because LLMs can exploit
structure in code and scientific text, enabling searches over
large, discrete spaces that would be difficult to explore with
purely random or hand-designed operators. At the same
time, the flexibility of LLM-generated candidates makes
reliability, constraint satisfaction, and evaluation efficiency
central challenges for practical deployment.

2.2. Formal Verification of Synthesized Code
As generative models are increasingly used to synthesize
executable programs, ensuring correctness has become a
central concern. Formal verification provides a principled
framework for checking whether generated code satisfies
specifications such as type safety, functional correctness,
invariants, or resource bounds, rather than relying only on
example-based testing (Herklotz et al., 2021). In synthesis
pipelines, verification can be used either as a post hoc filter
to reject invalid candidates or as part of the search objective
itself, guiding generation toward programs that are provably
correct. This is especially important in high-stakes domains,         Figure 1. Overview of our proposed system. A user provides an
                                                                      input/output schema pair and initial PVS program. The ShinkaE-
where small implementation errors can lead to unsafe or
                                                                      volve loop elicits LLM translation code and formally verifies them.
clinically unacceptable behavior.                                     Upon successful verification the resulting theorem can be then be
                                                                      translated into C code for use in the MIoT environment.
2.3. Healthcare Data Interoperability
Healthcare data interoperability concerns the ability of het-
erogeneous systems to exchange, interpret, and use struc-             from a model ensemble. Additionally, a set of K inspiration
tured clinical information consistently across institutional          programs are selected from the same island. The parent and
and software boundaries (Iroju et al., 2013). Modern in-              inspiration programs, along with their fitness scores, are
teroperability efforts are shaped by standards such as HL7            then provided to the LLM as a prompt. The LLM is then
FHIR (Vorisek et al., 2022), standardized clinical termi-             instructed to choose between editing, re-writing, or mutat-
nologies, and structured exchange formats that aim to make            ing earlier programs to generate a new solution candidate.
patient records, observations, medications, and care plans            This candidate is then scored by the provided evaluator and
computable across platforms. Despite this progress, real-             its results recorded into the database. This process then
world healthcare data remain fragmented, inconsistently               continues in a multi-worker asynchronous loop, working to
coded, and deeply embedded in local workflows, creating               maximize the fitness function.
substantial barriers to reliable automation and downstream
                                                                      In our approach, we use the Prototype Verification System
analytics (Mathew & Pillai, 2015). As a result, methods
                                                                      (PVS) as our evaluator for determining solution fitness. PVS
that generate or transform healthcare software artifacts must
                                                                      is a theorem prover designed to support the formal specifica-
account for both syntactic conformance to standards and
                                                                      tion and verification of complex systems (Owre & Shankar,
semantic alignment with clinical intent.
                                                                      1999). PVS provides a domain-specific language (DSL)
                                                                      which we adapt to support the definition of transformations
3. Approach                                                           between valid JSON schemas. The pipeline then requires an
                                                                      input schema and an output schema. The input schema de-
Our approach, shown in Figure 1, is built on ShinkaEvolve
                                                                      termines the format of the incoming data stream (e.g. from
(Lange et al., 2025). ShinkaEvolve is an open-source im-
                                                                      some medical device) and the output schema determines the
plementation of recent evolutionary code optimization tech-
                                                                      required format of the outgoing data stream (e.g. the patient
niques leveraging LLMs. ShinkaEvolve provides a multi-
                                                                      database in the larger system).
island evolutionary approach which builds an SQL database
of programs and corresponding fitness scores. At each stage,          A theorem is then over a translation between inputs of
a parent program is selected along with an LLM sampled                the input schema type and outputs of the output schema

                                                                  2
                           Submission and Formatting Instructions for SD4H Workshop at ICML 2026

type. The transform is correct only if this theory is proven.       4. Case Study: Integration of a Pulse Oximeter
This is formalized as a set of constraints and core verifica-
tion condition, which is shown in Listing 1. Here we de-            In this section we provide an analysis of a concrete use case
fine input compliant?, output compliant?, and                       of our system for integrating a new device (a pulse oximeter)
transform to be the JSON input schema, JSON output                  into the already existing MIoT environment. The device
schema, and the synthesized theorem respectively.                   comes with a custom JSON schema which encodes a mea-
                                                                    surement of a patient’s pulse and oxygen saturation (shown
In the evolution loop, the LLM is tasked with writing such          in Appendix Listing 3). To be integrated into the larger
a transform in the PVS DSL. In the evaluation phase, we             system, this data must be converted into the Fast Healthcare
then can formally verify if the generated theorem is true.          Interoperability Resources (FHIR) format (shown in Ap-
This results in a binary fitness function: 0 for an invalid         pendix Listing 4), which is a standardized medical format
theorem and 1 for a valid theorem. We note that a challenge         schema that the system already natively understands.
of our approach is that the the DSL of PVS is only weakly
known by the pretrained LLMs (i.e. the GPT family of                As input to the ShinkaEvolve process we provide these two
models (Singh et al., 2025)). For this reason we additionally       known schemas as well as a initial skeleton program which
provide a PVS language reference and an in-context exam-            is shown in Listing 2. This initial program simply returns an
ple transform demonstrating translations between a pair of          empty JSON dictionary for any input. To rigorously analyze
simple schemas in the prompt.                                       the overall performance of ShinkaEvolve for this task, we
                                                                    perform 10 separate experimental runs for this task. We
After this evolution process is complete, we will have a for-       use two separate islands and run each trial for a total of
mally verified translation from one JSON schema to another.         20 generations. A successfully verified PVS translation is
However, the DSL of PVS does not provide code that can              shown in Appendix Listing 5.
be operationalized. We then use additional tooling which
allows us to deterministically transform the verified theorem                    Listing 2. PVS theory initial program
into C code which can efficiently perform the translation           A_B: THEORY
execution inside the MIoT.                                          BEGIN
                                                                      jsltlib: LIBRARY = "../../jslt_pvs/
                                                                          jsltlib/"

                                                                      IMPORTING jsltlib@jsondata
      Listing 1. Constraints and core verification condition
A_B_constraints: THEORY                                               transform(i: jsondata): jsondata = jdict
BEGIN                                                                     (())
  jsltlib: LIBRARY = "../../jslt_pvs/
      jsltlib/"                                                     END A_B
  IMPORTING jsltlib@jsondata

  requires(obj: jsondata): bool = TRUE                              4.1. Aggregate Performance
  ensures(obj, new_obj: jsondata): bool =
      jdict?(new_obj)                                               Table 1 summarizes key performance metrics averaged
END A_B_constraints                                                 across all 10 experimental runs. The earliest successful
                                                                    theorem occurs at generation 5.0 ± 4.3 on average with a
...
                                                                    range of 1–14. We define the success rate to be fraction
A_B_verif: THEORY                                                   of LLM-generated programs that pass verification across
BEGIN                                                               any generation. For this example we obverse a success rate
  IMPORTING A_B_constraints                                         of 37.4 ± 22.4%, reflecting the difficulty of synthesizing
  % plus imports/definitions for                                    correct PVS transform functions.
      input_compliant?, output_compliant?,
      and transform                                                 The average total API cost per experiment is $0.87 ± $0.18,
                                                                    but the cost incurred before the first successful proof is
  correctness: THEOREM
    FORALL (obj: input_compliant):                                  only $0.18 ± $0.19, roughly 20% of the total budget. The
      requires(obj) IMPLIES                                         remaining cost is then spent on continued exploration after
        LET new_obj = transform(obj) IN                             a solution has already been found. The total wall-clock
          output_compliant?(new_obj) AND                            time per experiment averages 42.7 ± 8.1 minutes, with the
              ensures(obj, new_obj)                                 the LLM generation time taking up the majority of this
END A_B_verif
                                                                    time. We find that the PVS verification step is generally fast
                                                                    compared to the LLM generation phase. We observe that the
                                                                    first successful program is found in just 10.4 ± 9.9 minutes

                                                                3
                                       Submission and Formatting Instructions for SD4H Workshop at ICML 2026

  Table 1. Aggregate experiment statistics across 10 independent                     4.3. Solution Convergence
  runs (20 generations each).
                                                                                     A notable finding is that all 10 experiments converge to
                 Metric                                         Mean ± Std           essentially the same solution despite following different
                 Earliest Successful Generation                    5.0 ± 4.3         LLM selection paths and encountering different intermedi-
                 Success Rate                                  37.4 ± 22.4%          ate failures. Every best-of-run program produces the same
                 Total Cost                                     $0.87 ± 0.18         FHIR Observation resource structure. Syntactic variations
                 Cost to First Success                          $0.18 ± 0.19
                 Total Wall-Clock Time (mins)                     42.7 ± 8.1         exist across runs, but the semantic content is identical. This
                 Wall-Clock Time to First Success (mins)          10.4 ± 9.9         convergence suggests that the PVS verification constraint
                                                                                     is highly prescriptive: the output schema, combined with
                                                                                     the proof obligations, admits essentially one valid mapping
                                                                                     from the input. The evolutionary process thus functions
                                                                                     less as an open-ended search and more as an oracle-guided
                 60                                   % Selected                     synthesis procedure.
                                                      % of Successful Programs
                 50
Percentage (%)




                 40
                                                                                     5. Conclusion

                 30                                                                  We have built a fully integrated neuro-symbolic pipeline to
                                                                                     generate formally verified data translation code for a MIoT
                 20                                                                  use case. Specifically, we combined the ShinkaEvolve’s
                                                                                     open-source LLM-based evolutionary algorithm framework
                 10
                                                                                     with a PVS verification module. Our system uses LLMs
                  0                                                                  to generate translations between JSON schemas using the
                          GPT-5     GPT-5-mini       o4-mini       GPT-5-nano        domain-specific language of PVS. These translations can be
                                             Model
                                                                                     formally verified to ensure that the output schema is always
       Figure 2. Selection and success rate of LLMs in the ensemble.                 followed. We have demonstrated our pipeline via a case
                                                                                     study of integrating a pulse oximeter device into our MIoT
                                                                                     environment. We are able to consistently generate formally
                                                                                     verified translations at low cost.
  on average.                                                                        This works is a first step toward trustworthy automatic in-
                                                                                     tegration of novel devices into a existing healthcare infras-
  4.2. LLM Selection                                                                 tructure. In future work we plan to explore integration of a
                                                                                     boarder set of devices, formal verification of the network-
  In our experiments, ShinkaEvolve is configured to use an                           ing component of the system, and integrating the formal
  ensemble of GPT LLMs: O 4- MINI, GPT-5, GPT-5- MINI,                               verification stage into a fully agentic pipeline.
  GPT-5- NANO . At each generation, a member from the en-
  semble is randomly selected to generate a new solution
  candidate. The weights of this sampling process are set                            Acknowledgements
  dynamically using a Thompson sampling bandit approach                              This research was, in part, funded by the Advanced Re-
  (Daniel et al., 2018) based on observed success from prior                         search Projects Agency for Health (ARPA-H). The views
  generations. Figure 2 compares each model’s selection                              and conclusions contained in this document are those of the
  frequency against its share of successful programs across                          authors and should not be interpreted as representing the
  all experiments. gpt-5 accounts for 33.7% of all model                             official policies, either expressed or implied, of the United
  selections but is responsible for 53.5% of successful pro-                         States Government.
  grams. Conversely, o4-mini (25.3% selected, 14.1% of
  successes) and gpt-5-nano (14.7% selected, 4.2% of suc-
  cesses) underperform relative to their selection frequency.                        Impact Statement
  gpt-5-mini performs roughly in proportion (26.3% se-                               This paper presents work whose goal is formally validate
  lected, 28.2% of successes).                                                       LLM generated code for a medical Internet of Things en-
  This demonstrates that the larger and more expensive LLMs,                         vironment. This has the potential impact of making AI-
  such as gpt-5, are in general more accurate and therefore                          powered medical systems more trustworthy and reliable.
  favored in the sampling process. We note that this sampling
  algorithm in ShinkaEvolve considers only an LLMs success
  rate and not its resource cost.

                                                                                 4
                          Submission and Formatting Instructions for SD4H Workshop at ICML 2026

References                                                              Vorisek, C. N., Lehne, M., Klopfenstein, S. A. I., Mayer,
                                                                          P. J., Bartschke, A., Haese, T., and Thun, S. Fast health-
Daniel, J. R., Benjamin, V. R., Abbas, K., Ian, O., and
                                                                          care interoperability resources (fhir) for interoperability
  Zheng, W. A tutorial on thompson sampling. Foundations
                                                                          in health research: systematic review. JMIR medical
  and Trends in Machine Learning, 11(1):1–99, 2018.
                                                                          informatics, 10(7):e35724, 2022.
Dimitrov, D. V. Medical internet of things and big data
  in healthcare. Healthcare informatics research, 22(3):
  156–163, 2016.

Herklotz, Y., Pollard, J. D., Ramanathan, N., and Wick-
  erson, J. Formal verification of high-level synthesis.
  Proceedings of the ACM on Programming Languages,
  5(OOPSLA):1–30, 2021.

Iroju, O., Soriyan, A., Gambo, I., Olaleke, J., et al. Interoper-
   ability in healthcare: benefits, challenges and resolutions.
   International Journal of Innovation and Applied Studies,
   3(1):262–270, 2013.

Jalil, S. The transformative influence of llms on soft-
  ware development & developer productivity. In 2025
  International Conference on Artificial Intelligence, Com-
   puter, Data Sciences and Applications (ACDSA), pp. 1–10.
   IEEE, 2025.

Kalai, A. T., Nachum, O., Vempala, S. S., and Zhang,
  E. Why language models hallucinate. arXiv preprint
  arXiv:2509.04664, 2025.

Lange, R. T., Imajuku, Y., and Cetin, E. Shinkaevolve:
  Towards open-ended and sample-efficient program evolu-
  tion. arXiv preprint arXiv:2509.19349, 2025.

Mathew, P. S. and Pillai, A. S. Big data solutions in health-
 care: Problems and perspectives. In 2015 International
 conference on innovations in information, embedded and
 communication systems (ICIIECS), pp. 1–6. IEEE, 2015.

Novikov, A., Vũ, N., Eisenberger, M., Dupont, E., Huang,
  P.-S., Wagner, A. Z., Shirobokov, S., Kozlovskii, B., Ruiz,
  F. J., Mehrabian, A., et al. Alphaevolve: A coding agent
  for scientific and algorithmic discovery. arXiv preprint
  arXiv:2506.13131, 2025.

Owre, S. and Shankar, N. The formal semantics of pvs.
 Technical report, 1999.

Sharma, A. Openevolve: an open-source evolution-
  ary coding agent, 2025. URL https://github.
  com/algorithmicsuperintelligence/
  openevolve.

Singh, A., Fry, A., Perelman, A., Tart, A., Ganesh, A.,
  El-Kishky, A., McLaughlin, A., Low, A., Ostrow, A.,
  Ananthram, A., et al. Openai gpt-5 system card. arXiv
  preprint arXiv:2601.03267, 2025.

                                                                    5
                             Submission and Formatting Instructions for SD4H Workshop at ICML 2026

     A. Code Listings
     In Listing 3 we display the input schema from the pulse oximeter. In Listing 4 we display the output schema. In Listing 5
     we display an example of a correctly verified PVS theory that translates the input schema to the output schema.

                                                      Listing 3. Input schema
1    {
2        "$schema": "https://json-schema.org/draft-07/schema#",
3        "additionalProperties": false,
4        "properties": {
5          "finger_present": {
6            "description": "Finger detection indicator",
7            "enum": [
8               0,
9               1
10            ],
11            "examples": [
12               1
13            ],
14            "type": "integer"
15         },
16         "pleth": {
17            "description": "Plethysmography reading",
18            "examples": [
19               36
20            ],
21            "maximum": 99,
22            "minimum": 0,
23            "type": "integer"
24         },
25         "pulse_rate": {
26            "anyOf": [
27               {
28                  "maximum": 82,
29                  "minimum": 59
30               },
31               {
32                  "const": 255,
33                  "type": "integer"
34               }
35            ],
36            "description": "Heart rate measurement",
37            "examples": [
38               79
39            ],
40            "type": "integer"
41         },
42         "spo2": {
43            "anyOf": [
44               {
45                  "maximum": 100,
46                  "minimum": 88
47               },
48               {
49                  "const": 127,
50                  "type": "integer"
51               }
52            ],
53            "description": "Blood oxygen saturation percentage",
54            "examples": [
55               98
56            ],
57            "type": "integer"
58         },

                                                                6
                         Submission and Formatting Instructions for SD4H Workshop at ICML 2026

59         "valid": {
60           "description": "Reading validity indicator",
61           "enum": [
62              0,
63              1
64           ],
65           "examples": [
66              1
67           ],
68           "type": "integer"
69         }
70       },
71       "required": [
72          "pleth",
73          "pulse_rate",
74          "valid",
75          "spo2",
76          "finger_present"
77       ],
78       "type": "object"
79   }




                                                          7
                         Submission and Formatting Instructions for SD4H Workshop at ICML 2026

                                                Listing 4. Output schema
1    {
2        "$id": "http://hl7.org/fhir/json-schema/6.0",
3        "$schema": "http://json-schema.org/draft-07/schema#",
4        "description": "See http://hl7.org/fhir/json.html#schema for information about the FHIR
             JSON Schemas.",
5        "properties": {
6          "category": {
7            "description": "A code that classifies the general type of observation being made.",
8            "items": {
9               "properties": {
10                  "coding": {
11                     "properties": {
12                        "code": {
13                           "const": "vital-signs",
14                           "type": "string"
15                        },
16                        "system": {
17                           "const": "http://terminology.hl7.org/CodeSystem/observation-category",
18                           "type": "string"
19                        }
20                     },
21                     "required": [
22                        "system",
23                        "code"
24                     ],
25                     "type": "object"
26                  }
27               },
28               "required": [
29                  "coding"
30               ],
31               "type": "object"
32            },
33            "type": "array"
34         },
35         "code": {
36            "properties": {
37               "coding": {
38                  "items": {
39                     "properties": {
40                        "code": {
41                           "const": "2710-2",
42                           "type": "string"
43                        },
44                        "display": {
45                           "const": "Oxygen saturation in Capillary blood by Oximetry",
46                           "type": "string"
47                        },
48                        "system": {
49                           "const": "http://loinc.org",
50                           "type": "string"
51                        }
52                     },
53                     "required": [
54                        "system",
55                        "code",
56                        "display"
57                     ],
58                     "type": "object"
59                  },
60                  "type": "array"
61               },
62               "text": {


                                                           8
                    Submission and Formatting Instructions for SD4H Workshop at ICML 2026

 63         "const": "SpO2",
 64         "type": "string"
 65        }
 66     },
 67     "required": [
 68        "coding",
 69        "text"
 70     ],
 71     "type": "object"
 72   },
 73   "effectiveDateTime": {
 74      "description": "The time or time-period the observed value is asserted as being true
              .",
 75      "type": "string"
 76   },
 77   "encounter": {
 78      "properties": {
 79         "reference": {
 80            "description": "Encounter (appointment) ID",
 81            "type": "string"
 82         }
 83      },
 84      "required": [
 85         "reference"
 86      ],
 87      "type": "object"
 88   },
 89   "resourceType": {
 90      "const": "Observation",
 91      "type": "string"
 92   },
 93   "subject": {
 94      "properties": {
 95         "display": {
 96            "description": "Patient name",
 97            "type": "string"
 98         },
 99         "reference": {
100            "description": "Patient ID",
101            "type": "string"
102         }
103      },
104      "required": [
105         "reference"
106      ],
107      "type": "object"
108   },
109   "valueQuantity": {
110      "description": "The information determined as a result of making the observation, if
                the information has a simple value.",
111      "properties": {
112         "code": {
113            "const": "%",
114            "type": "string"
115         },
116         "system": {
117            "const": "http://unitsofmeasure.org",
118            "type": "string"
119         },
120         "unit": {
121            "const": "%",
122            "type": "string"
123         },
124         "value": {
125            "description": "The information determined as a result of making the observation

                                                     9
                          Submission and Formatting Instructions for SD4H Workshop at ICML 2026

                      , if the information has a simple value.",
126               "type": "number"
127              }
128           },
129           "required": [
130              "value"
131           ],
132           "type": "object"
133          }
134       },
135       "required": [
136          "resourceType",
137          "category",
138          "code",
139          "subject",
140          "effectiveDateTime",
141          "valueQuantity"
142       ],
143       "type": "object"
144   }




                                                           10
                   Submission and Formatting Instructions for SD4H Workshop at ICML 2026

                                    Listing 5. Verified Correct PVS Theory
A_B: THEORY
BEGIN

  jsltlib: LIBRARY = "../../jslt_pvs/jsltlib/"

  IMPORTING jsltlib@jsondata

  transform(i: jsondata): jsondata =
    LET spo2v: jsondata = json_get_key(i, "spo2"),
         mk = (LAMBDA (k: string, v: jsondata): jpair(k, v))
    IN
       jdict((#
         length := 6,
         seq := [:
           mk("resourceType", jstr("Observation")),
           mk("category",
              jarray((#
                length := 1,
                seq := [:
                  jdict((#
                     length := 1,
                     seq := [:
                        mk("coding",
                           jdict((#
                             length := 2,
                             seq := [:
                                mk("system", jstr("http://terminology.hl7.org/CodeSystem/
                                    observation-category")),
                                mk("code", jstr("vital-signs"))
                             :]
                           #))
                        )
                     :]
                  #))
                :]
              #))
           ),
           mk("code",
              jdict((#
                length := 2,
                seq := [:
                  mk("coding",
                     jarray((#
                        length := 1,
                        seq := [:
                           jdict((#
                             length := 3,
                             seq := [:
                                mk("system", jstr("http://loinc.org")),
                                mk("code", jstr("2710-2")),
                                mk("display", jstr("Oxygen saturation in Capillary blood by
                                    Oximetry"))
                             :]
                           #))
                        :]
                     #))
                  ),
                  mk("text", jstr("SpO2"))
                :]
              #))
           ),
           mk("subject",
              jdict((#


                                                     11
                     Submission and Formatting Instructions for SD4H Workshop at ICML 2026

                 length := 1,
                 seq := [:
                   mk("reference", jstr("Patient/example"))
                 :]
               #))
             ),
             mk("effectiveDateTime", jstr("1970-01-01T00:00:00Z")),
             mk("valueQuantity",
                jdict((#
                  length := 4,
                  seq := [:
                    mk("value", spo2v),
                    mk("unit", jstr("%")),
                    mk("system", jstr("http://unitsofmeasure.org")),
                    mk("code", jstr("%"))
                  :]
                #))
             )
        :]
      #))

END A_B




                                                      12
