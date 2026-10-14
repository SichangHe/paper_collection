            Pragmatic Uses of AI in Formal
         MethodsBased Railway Projects: Early
          Lessons and Perspectives (Extended
                      Abstract)

            Thierry Lecomte(B) , Dalay Almeida, and Norman Maury

                          CLEARSY, Aix En Provence, France
                            thierry.lecomte@clearsy.com


       Abstract. This extended abstract reports on recent industrial activities
       exploring pragmatic and controlled uses of AI in railway systems devel-
       oped with formal methods. First, large language models are used to syn-
       thesize and query large-scale railway technical specifications, improving
       accessibility while requiring systematic human validation. Second, early
       experiments assess AI-assisted generation of interactive proof scripts for
       B method proof obligations, showing initial productivity gains but sub-
       stantial research challenges. Third, AI-based perception is integrated into
       railway safety functions, where machine learning acts solely as a proposer
       whose outputs are redundantly checked by a formally verified safety con-
       troller. Finally, a proof of concept applies multimodal language models
       to relay-based railway interlocking systems, automatically transforming
       relay diagrams into propositional logic specifications applicable to new
       diagrams. The results confirm that AI-assisted formalization is feasible
       and accessible, opening promising perspectives for advancing automation
       and trustworthiness in railway formal verification.


       Keywords: formal methods · safety critical · software development ·
       railway


1    Introduction
The integration of machine learning (ML) into safety-critical railway systems
raises signiﬁcant challenges for certiﬁcation, as current safety standards require
transparent, fully speciﬁed system designs, whereas ML models are inherently
opaque after training. This extended abstract presents several research activities,
completed during collaborative projects and in-house investigations. These activ-
ities address various safety engineering concerns related to the development of
critical railway systems, including the analysis of technical documentation, assis-
tance with interactive formal model veriﬁcation, the transformation of technical
diagrams into formal models, and the use of AI to create a safe image analysis
system. Although the activities are diverse and speciﬁc, they nevertheless yield
a number of common lessons.
 c The Author(s) 2026
A. Sampaio and M. Stoelinga (Eds.): FM 2026, LNCS 16557, pp. 605–609, 2026.
https://doi.org/10.1007/978-3-032-26220-2_29
606      T. Lecomte et al.

2     Activities and Results
Four main activities were carried out in 2025 and are summarised below.


2.1    Easing Interaction with Technical Specifications

The work of a software engineer often involves reviewing technical documenta-
tion, which is frequently written by other individuals or companies. For example,
speciﬁcations for embedded railway software can run to several hundred or even
thousands of pages. Understanding such content therefore requires a considerable
amount of reading time. LLMs were used to facilitate this process by generat-
ing summaries and answering technical questions that combine information from
multiple sections. The documents analysed in PDF and DOCX format are either
proprietary technical documents or public documents (ERTMS/ETCS subsets1 ).
To ensure the conﬁdentiality of external documents, the LLMs were operated on
the company’s internal computing infrastructure.
    Overall, the implementation of this feature was perceived as facilitating the
understanding of new technical documentation and led to noticeable time savings
(up to 30% gain when discovering new technical document). However, limitations
were encountered, probably related to the amount of text to be analysed and
the presence of numerous images. On several occasions, certain elements were
not taken into account in the responses provided by the LLMs. While we were
pleasantly surprised by the correct and well-argued response to our ﬁrst question
about the safety of an ETCS feature, the responses provided were often partial,
sometimes inaccurate, and occasionally speculative.
    The conclusion of this work is that systematic veriﬁcation of the responses
returned by LLMs is necessary to check their accuracy before they can be relied
upon for any engineering activity (analysis, development, testing).


2.2    Assistance with Interactive Proof

The research is aimed at demonstrating how AI techniques can be applied to
support the B formal method [3] without weakening safety guarantees. A key
contribution is the use of machine learning to guide and accelerate formal proof
activities, notably through predictive support for automated provers. The work
shows that AI can reduce manual proof eﬀort while preserving correctness and
traceability. Another important result is the deﬁnition of AI architectures suit-
able for industrial constraints, with fully local inference ensuring data conﬁden-
tiality. The research also extends AI support to software engineering tasks such
as code analysis and project description. Practical demonstrations and experi-
ments illustrate the feasibility of the approach in real engineering workﬂows.
    The results highlight improved eﬃciency in veriﬁcation activities. A gain up
to 20% was obtained when selecting the best automatic prover to apply instead of
1
    https://www.era.europa.eu/era-folder/archived-set-specifications-3-etcs-b3-r2-
    gsm-r-b1.
            Pragmatic Uses of AI in Formal MethodsBased Railway Projects       607

applying static proof tactics. Overall, this work supports the view of trustworthy
AI as an enabler of formal methods rather than a replacement. It positions AI
assisted formal veriﬁcation as a realistic path toward scalable, safe industrial
systems.

2.3   AI-Based Perception Integrated Into Railway Safety
The research [4] addresses the fundamental challenge of integrating machine
learning into safety-critical railway systems governed by strict certiﬁcation stan-
dards. Its main contribution is the proposal and evaluation of a proof of concept
architecture that constrains the role of machine learning to perception and can-
didate generation, while delegating all safety decisions to a formally developed
controller. The work recognizes that machine learning models are inherently
opaque and therefore incompatible with existing railway safety standards when
used directly in vital functions. To overcome this limitation, the research intro-
duces a certiﬁed-control-inspired architecture (Fig. 1) in which machine learning
outputs are validated by an independent safety controller.




               Fig. 1. ML with verifiable results + safety controller.


    The safety controller is speciﬁed, developed, and veriﬁed using the B method,
ensuring full traceability from safety requirements to executable code. The app-
roach is illustrated through a free track detection use case, where a convolutional
neural network proposes a candidate free track path from camera images. This
candidate is then checked by the safety controller against explicit geometric and
physical constraints derived from railway domain knowledge. A key safety prop-
erty guarantees that the computed free track distance is always conservative
with respect to real obstacles. The research details how safety properties are
systematically reﬁned into veriﬁable sub properties covering algorithms, code,
and execution platform. Experimental results show that unsafe or imperfect
machine learning outputs can be safely rejected. Overall, the work demonstrates
a credible pathway for the trustworthy use of AI in certiﬁed railway systems by
combining advanced perception with formally proven safety logic, while clearly
emphasizing the necessity of expert validation and further industrial maturation

2.4   Transforming Relay Diagrams Into Formal Specification
In the continuation of research on the formal veriﬁcation of relay-based diagrams
[2], a research eﬀort [1] was aimed at automating the formal analysis of relay
608     T. Lecomte et al.

based railway interlocking systems, which are still widely deployed in operational
networks. The main contribution is a proof of concept showing that a multimodal
large language model can directly interpret relay circuit diagrams and generate
formal speciﬁcations in propositional logic. The approach removes the need for
manual reinterpretation or redrawing of diagrams, which are traditionally error
prone and time consuming. Using prompt engineering, the model is guided to
produce speciﬁcations compatible with B method based analyses. Experimental
results on academic and industrial SNCF diagrams demonstrate that the AI can
correctly capture system behaviour and detect anomalies such as ringbell eﬀects
and short circuits. The study highlights both the strengths and limitations of
general purpose AI when applied to context speciﬁc railway conventions. It shows
that modern AI models can act as end to end translators from legacy engineering
artefacts to formal models. The work emphasizes that expert validation remains
essential for safety critical use.


3     Conclusion and Perspectives
LLMs clearly help engineers throughout the development cycle, even on con-
ﬁdential technical subjects, showing signiﬁcant recent progress. However, their
tendency to hallucinate requires systematic veriﬁcation, limiting their use to
supporting roles rather than direct certiﬁcation activities. Since late 2025, new
applications are emerging—documentation synthesis, test case generation, and
technical environment integration—with further breakthroughs expected in the
coming months.

Acknowledgements. The work and results described in this article were partly
funded by the projects “New Methods for Safety Demonstration” managed by Interna-
tional Union of Railways and H2020-ECSEL “AIDOaRT” focusing on AI-augmented
automation.



References
1. Almeida, D., Glemarec, L.: From relay-based railway interlocking circuits to formal
   specification: an AI-driven approach, pp. 25–34 (2025)
2. Almeida, D., Oliveira, M., Bezerra, P., Bon, P., Collart-Dutilleul, S.: CSP specifica-
   tion and verification of relay-based railway interlocking systems, pp. 97–106 (2022)
3. Butler, M., Körner, P., Krings, S., Lecomte, T., Leuschel, M., Mejia, L.F., Voisin,
   L.: The first twenty-five years of industrial use of the b-method. In: ter Beek,
   M.H., Ničković, D. (eds.) Formal Methods for Industrial Critical Systems, pp. 189–
   209. Springer International Publishing, Cham (2020). https://doi.org/10.1007/978-
   3-030-58298-2 8
4. Lecomte, T.: Formal development of a safety controller for machine learning outputs
   in vital railway systems. In: ter Beek, M.H., Teixeira, L. (eds.) Formal Methods:
   Foundations and Applications, pp. 196–206. Springer Nature Switzerland, Cham
   (2026). https://doi.org/10.1007/978-3-032-12086-1 11
            Pragmatic Uses of AI in Formal MethodsBased Railway Projects          609

Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
   The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
