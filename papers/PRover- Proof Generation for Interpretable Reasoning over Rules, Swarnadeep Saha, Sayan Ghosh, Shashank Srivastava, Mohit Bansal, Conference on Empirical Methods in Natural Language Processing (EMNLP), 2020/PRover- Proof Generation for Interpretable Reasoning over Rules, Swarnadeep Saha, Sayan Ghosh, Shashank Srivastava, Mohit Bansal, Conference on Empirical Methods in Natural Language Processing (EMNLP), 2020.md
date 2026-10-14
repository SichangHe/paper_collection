                                             PROVER: Proof Generation for Interpretable Reasoning over Rules


                                             Swarnadeep Saha    Sayan Ghosh   Shashank Srivastava Mohit Bansal
                                                                       UNC Chapel Hill
                                                   {swarna, sayghosh, ssrivastava, mbansal}@cs.unc.edu




                                                                                                                   Question (logic)
                                                              Abstract
                                                                                                                                                    Proof
                                                                                                         Logical      Relevant        Theorem
                                            Recent work by Clark et al. (2020) shows                     Theory       Axioms           Prover
                                                                                                                                                    Answer
                                            that transformers can act as “soft theorem                              (a) Formal Reasoning
arXiv:2010.02830v1 [cs.CL] 6 Oct 2020




                                            provers” by answering questions over explic-                           Question (NL)

                                            itly provided knowledge in natural language.
                                            In our work, we take a step closer to emu-                    Text
                                                                                                         Corpus
                                                                                                                   Relevant Facts
                                                                                                                   and Rules (NL)
                                                                                                                                      Transformer
                                                                                                                                        Network
                                                                                                                                                    Answer

                                            lating formal theorem provers, by proposing                             (b) RuleTakers
                                            PROVER, an interpretable transformer-based                              Question (NL)
                                            model that jointly answers binary questions
                                                                                                                                                     Proof
                                            over rule-bases and generates the correspond-                 Text     Relevant Facts     Transformer
                                                                                                         Corpus    and Rules (NL)       Network
                                            ing proofs. Our model learns to predict nodes                                                           Answer
                                                                                                                      (c) PRover
                                            and edges corresponding to proof graphs in an
                                            efficient constrained training paradigm. Dur-          Figure 1: Block diagram showing that PROVER is a
                                            ing inference, a valid proof, satisfying a set         closer linguistic analog of formal reasoning.
                                            of global constraints is generated. We con-
                                            duct experiments on synthetic, hand-authored,          1988), and backed by the recent successes of trans-
                                            and human-paraphrased rule-bases to show               formers (Vaswani et al., 2017) in NLP, Clark et al.
                                            promising results for QA and proof generation,         (2020) propose a new version of the problem by
                                            with strong generalization performance. First,
                                                                                                   replacing the formal representations of rule-bases
                                            PROVER generates proofs with an accuracy
                                            of 87%, while retaining or improving perfor-           with natural language (English). Specifically, their
                                            mance on the QA task, compared to RuleTak-             task requires predicting the truth value of a state-
                                            ers (up to 6% improvement on zero-shot eval-           ment by reasoning over a set of facts and rules,
                                            uation). Second, when trained on questions re-         all expressed in natural language. Figure 2 shows
                                            quiring lower depths of reasoning, it general-         some examples of the task. Clark et al. (2020)
                                            izes significantly better to higher depths (up to      propose RuleTakers, a fine-tuned RoBERTa model
                                            15% improvement). Third, PROVER obtains
                                                                                                   (Liu et al., 2019b) to show that transformers can
                                            near perfect QA accuracy of 98% using only
                                            40% of the training data. However, generating          act as “soft theorem provers” by predicting the fi-
                                            proofs for questions requiring higher depths of        nal answer in such reasoning-based problems with
                                            reasoning becomes challenging, and the accu-           high accuracy.
                                            racy drops to 65% for “depth 5”, indicating sig-          We argue that to use transformers for natural
                                            nificant scope for future work.1                       language reasoning reliably, they should be able
                                                                                                   to generate proofs that provide rationales for the
                                        1   Introduction                                           predicted answer. Proof generation is vital for em-
                                                                                                   ulating formal reasoning but also for moving to-
                                        Developing systems that can understand and rea-            wards human-interpretable models that alleviate
                                        son over explicitly provided knowledge has been a          concerns about the black-box nature of deep archi-
                                        fundamental goal of AI (Newell and Simon, 1956).           tectures (Rudin, 2019). Towards this, we present
                                        Owing to the challenges posed in reasoning over            PROVER, a transformer-based model that jointly
                                        formal representations (Musen and Van Der Lei,             answers questions over natural language rule-bases
                                          1
                                            Our code and models are publicly available at https:   and generates corresponding proofs. Figure 1 il-
                                        //github.com/swarnaHub/PRover.                             lustrates our method as a closer linguistic analog
of formal reasoning, as it generates proofs along       2019) and ROPES (Lin et al., 2019). Unlike our
with answers. However, unlike formal reasoners,         task, most of these require reasoning over implicit
PROVER can operate on natural language text that        rules, the focus being on language understanding
provides the underlying theory, rather than rely on     and one step of rule application. Multi-hop QA
formal logical representations. Such methods that       datasets like HotpotQA (Yang et al., 2018) require
combine interpretability and flexibility in reasoning   multiple reasoning steps, but the inference rules
can have wide applications across domains.              needed are again implicitly inferred, rather than
    PROVER’s architecture consists of three modules     explicitly provided. Our task also bears similar-
that together generate answers along with proofs.       ity with Natural Language Inference (MacCartney
In this work, proofs are represented as directed        and Manning, 2014), but NLI also allows unsup-
graphs consisting of the relevant rules and facts       ported inferences by filling gaps in explicitly stated
needed to prove or disprove the question statement.     knowledge (Dagan et al., 2013).
Section 3.1 contains details of this representation.
A QA module predicts a binary answer for the ques-      Formal Reasoning and Neural Theorem Prov-
tion, a node module chooses which rules and facts       ing: Semantic parsing (Zettlemoyer and Collins,
are part of the proof, and an edge module predicts      2005; Berant et al., 2013; Berant and Liang, 2014)
the presence and the direction of the edges between     of multi-sentence texts into logical forms has
the chosen nodes. Model training minimizes a joint      proved to be challenging, restricting the application
cross-entropy loss over the three modules. To guide     of semantic parsers to formal reasoning systems
the model to predict edges between valid nodes          (Kamath and Das, 2019). PROVER bypasses this
only, we enforce global constraints on the structure    expensive and error-prone process and attempts to
of the proof during training, by masking out labels     solve the problem in an end-to-end manner, without
for impossible edges, resulting in a more efficient     any intermediate logical representations.
learning problem. PROVER generates valid proofs            Our approach is conceptually similar to a body
during inference by solving an ILP over the edge        of work on Neural Theorem Proving (Weber et al.,
potentials, subject to multiple semantic constraints,   2019) that has focused on developing theorem
such as ensuring proof graph connectivity. Our          provers by combining reasoning from symbolic
contributions are:                                      techniques with the possibility of differentiable
• We present PROVER, an interpretable joint model       learning from neural networks. These include
   that learns to reason over natural language rule-    neuro-symbolic methods for table comprehension
   bases and generate corresponding proofs.             (Neelakantan et al., 2016), executing basic com-
• PROVER performs similarly or improves upon            positional programs (Reed and de Freitas, 2016),
   state-of-the-art QA accuracy for the task, with up   SAT solving (Selsam et al., 2019), formula embed-
   to 6% improvement on zero-shot evaluation, and       ding (Abdelaziz et al., 2020), approximate (DNF)
   generates exact proofs at 87% accuracy. Unlike       model counting (Abboud et al., 2020), etc. How-
   RuleTakers, it does not require additional fine-     ever, PROVER diverges from these in working with
   tuning on the RACE (Lai et al., 2017) dataset.       free-form natural language input to generate proofs
• PROVER demonstrates significantly better gen-         similar to formal reasoners.
   eralization. When trained on lower depth ques-
   tions, it shows better QA accuracy (up to 15%)       Model Interpretability: PROVER follows a sig-
   on higher depth ones.                                nificant body of previous work on developing in-
                                                        terpretable neural models for NLP tasks to fos-
2   Related Work                                        ter explainability. Several approaches have fo-
                                                        cused on formalizing the notion of interpretabil-
Our work is related to multiple bodies of previous
                                                        ity (Rudin, 2019; Doshi-Velez and Kim, 2017;
work in NLP and formal reasoning.
                                                        Hase and Bansal, 2020), tweaking features for local
QA and NLI: The rule reasoning task is related          model interpretability (Ribeiro et al., 2016, 2018)
to reasoning tasks that have been proposed recently.    and exploring interpretability in latent spaces (Joshi
These include tasks in the bAbI dataset (Weston         et al., 2018; Samangouei et al., 2018). Our work
et al., 2015), synthetically generated probe tasks      can be seen as generating explanations in the form
(Richardson et al., 2020) or reading comprehension      of proofs for an NLP task. While there has been
tasks in datasets such as QuaRTz (Tafjord et al.,       prior work on generating natural language explana-
        Facts :                                                                 Rules:
        F1: The circuit includes the battery. F2: The wire is metal.            R6: If the circuit is powered and the circuit is complete and the wire is conducting then
        F3: The circuit includes the bell.                                      the current runs through the circuit.
        Rules :                                                                 R7: If the current runs through the circuit and the circuit includes the light bulb then the
        R1: If the circuit includes the battery and the battery is not flat     current runs through the light bulb.
        then the circuit is powered.                                            R8: If the current runs through the circuit and the circuit includes the bell then current
        R2: If the circuit includes the switch and the switch is on then the    runs through the bell.
        circuit is complete.                                                    R9: If the current runs through the circuit and the circuit includes the radio then current
        R3: If the circuit does not have the switch then the circuit is         runs through the radio.
        complete.                                                               R10: If the current runs through the light bulb then the light bulb is glowing.
        R4: If the wire is metal then the wire is conducting.                   R11: If the current runs through the bell then the light bell is ringing.
        R5: If the wire is plastic then the wire is not conducting.             R12: If the current runs through the radio then the radio is playing.

         Q1: The wire is not                Q2: The current runs       NAF                                                  R12               R9             FAIL
         conducting. [ Answer : F ]         through the circuit.                         R1                 R6
                                            [ Answer : T ]               F1
            F2             R4                                                                                               Q3: The radio is playing. [ Answer : F]
                                                                                         R3          F2              R4
                                                                        NAF
        Facts :                                           Rules :
        F1: The bald eagle eats the lion.                 R1: If the lion is green and the lion is not kind then the lion sees the bald eagle.
        F2: The bald eagle sees the tiger.                R2: If someone sees the lion then they eat the mouse.
        F3: The lion chases the bald eagle.               R3: If someone is kind and not green then they see the bald eagle.
        F4: The lion eats the mouse.                      R4: If someone is rough then they see the lion.
        F5: The mouse eats the tiger.                     R5: If someone sees the lion and they do not eat the tiger then the tiger is rough.
        F6: The tiger eats the bald eagle.                R6: If someone eats the bald eagle and the bald eagle is not kind then the bald eagle is rough.
        F7: The tiger is red.                             R7: If someone does not eat the lion then the lion is big.
                                                          R8: If someone is kind then they do not eat the mouse.
         Q4: The bald eagle eats the mouse. [ Answer : T ]                     Q5: The tiger does not eat the mouse. [ Answer : F ]

             F6                                                                 F6
                            R6              R4             R2                                  R6              R4
                                                                                                                              R5              R4             R2
            NAF                                                                NAF
                                                                                                              NAF

Figure 2: Diagram showing two rule-bases with rules, facts, questions, answers and proofs. PROVER answers all
the questions correctly and also generates all the corresponding proofs accurately in the above scenarios.

tions for multiple NLP tasks, including NLI (Cam-                                             {T rue, F alse} and generates a proof P.
buru et al., 2018), commonsense reasoning (Rajani
et al., 2019; Zhang et al., 2020) and generic text                                            3.1         Proof Representation
classification tasks (Liu et al., 2019a), our nov-                                            A proof, P = (N , E), is a directed graph with
elty lies in generating compositional explanations                                            nodes n ∈ N and edges e ∈ E. Each node is
consisting of proof graphs that detail the chain of                                           either a fact f ∈ F , a rule r ∈ R or a special NAF
reasoning, starting from language. We use a max-                                              node (Negation As Failure, as described below).
flow ILP formulation for checking proof graph con-                                            Edges in the proof are directed either from a fact (or
nectivity (Even and Tarjan, 1975). Multiple ap-                                               NAF ) to a rule or from a rule to another rule. These
proaches for NLP tasks such as sentiment analysis                                             indicate that a fact (or NAF ) is consumed by a rule,
and content selection (Pang and Lee, 2004; Barzi-                                             or the output of a rule (a new fact) is consumed by
lay and Lapata, 2005; Bansal et al., 2008) have                                               another rule, respectively. We use these constraints
been framed as optimal flow problems on graphs.                                               both during PROVER’s training and inference, as
                                                                                              described later in the paper. Formally, we have:
Program Synthesis with Transformers: Exist-
ing works show that transformers already capture                                                                                     P = (N , E)
some knowledge from pre-training for algorithm                                                                       N ⊆ R ∪ F ∪ NAF
emulation (Talmor et al., 2019) or can be fine-tuned                                                                                E ⊆N ×N
for tasks like semantic parsing (He and Choi, 2020),
translation (Wang et al., 2019), symbolic integra-                                            Figure 2 shows examples of two contexts (consist-
tion (Lample and Charton, 2020) and mathematics                                               ing of facts and rules), five questions about the con-
(Saxton et al., 2019). In our work, we also employ                                            texts, along with their answers and proofs. Each
a transformer-based pre-trained language model                                                proof has a depth (Q1 ’s proof has a depth of 1).
(RoBERTa (Liu et al., 2019b)) but for the down-                                               The maximum proof depth in all the datasets con-
stream task of rule-based reasoning.                                                          sidered in this work (Clark et al., 2020) is 5. Proofs
                                                                                              in the datasets are of three types:
3   Method
                                                                                              Successful proof with NAF: The proof of Q1 in
Each input to PROVER is a context C (consisting                                               Figure 2 is one such such example. F2 acts on R4
of facts F and rules R) and a question Q, about                                               to prove that “The wire is conducting.” and hence
the context. PROVER predicts the answer A ∈                                                   the answer is false.
Successful proof with NAF: Given a statement                      consists of three modules: (1) QA module, (2)
s, NAF in logic programming is a non-monotonic                    Node module, and (3) Edge module. The QA mod-
inference rule used to derive “not s” (negation of                ule is exactly the same as the RuleTakers model
the statement) from failure to derive s. Hence, a                 (Clark et al., 2020), thus allowing us to directly
proof may contain NAF node(s), representing the                   evaluate the effectiveness of our node and edge
truthfulness of the negation of statement(s) that                 modules. The input to RoBERTa is the concate-
cannot be proved using the set of rules. Consider                 nation of the context and the question, separated
the proofs for Q4 and Q5 where the NAF node in                    by the [SEP ] tokens. The context is represented
Q4 represents “The bald eagle is not kind.”.                      by concatenating the text consisting of facts and
                                                                  rules. Formally, if the rules and facts are denoted
Failed proof: This happens when a statement
                                                                  by {RFi }ki=1 and the question by Q, the input is
cannot be derived using the given rule-base and
the shallowest branch of the proof tree that fails is                [CLS] {RFi }ki=1 [SEP ][SEP ] Q [SEP ]
shown. Q3 ’s proof in Figure 2 is an example as
“The radio is playing.” cannot be proved.                         QA Module: The output of RoBERTa contains
   Note that a proof can have edges between two                   an embedding for each token in the context and
rules in both directions. E.g., consider the edges                a global embedding corresponding to the [CLS]
R4 → R5 and R5 → R4 in Q5 ’s proof in Figure 2.                   token. The QA classification head HQA is a se-
A node can have more than two incoming edges –                    quence of two linear layers with dropout proba-
the node R6 in Q2 has three incoming edges from                   bility of p. Formally, if t[CLS] denotes the [CLS]
R1 , R3 , and R4 .                                                token embedding, we obtain the class-wise prob-
                                                                  ability values PQA using the softmax function σ.
3.2      Task Description
Each training example is a tuple (Ci :=                                          PQA = σ(HQA (t[CLS] ))
{Fi , Ri }, Qi , Ai , Pi ) consisting of a context (set                                          (i)
                                                                  Node Module: Let {wj }m        j=1 denotes the m to-
of rules and facts), a question, the corresponding
                                                                  kens corresponding to RFi . Assuming the corre-
answer, and a proof. Generating a proof graph
                                                                  sponding RoBERTa embeddings are denoted by
requires (1) identifying the nodes (set of relevant
                                                                  {tw(i) }m
                                                                          j=1 , we learn a representation tRFi for each
facts, NAF and rules) that are part of the proof,                     j

(2) identifying the edges connecting these nodes,                 RFi , by performing a mean pooling MP of the
and (3) verifying a set of global constraints such as             constituent token embeddings.
proof connectivity that ensure a valid proof.                                     tRFi = MP ({tw(i) }m
                                                                                                     j=1 )
   For the first, we predict a binary label over each                                                  j

rule, fact and NAF denoting their presence or ab-                 We also learn a representation of the NAF node
sence in the proof. For the second, we also predict               tN AF as a linear transformation on t[CLS] . Note
binary labels denoting the presence or absence of                 that due to the self-attention layers of RoBERTa,
each edge. For the third, we enforce constraints                  t[CLS] summarizes the set of all derivable facts
during both training and inference (Section 3.4).                 given the context and the question. We want the
During training, we mask out the edge labels2 cor-                NAF node to encode information about all facts
responding to (1) self-loops, (2) edges between                   containing negation (e.g.,“The bald eagle is not
absent nodes, and (3) edges between facts to facts                kind” in Q4 ’s proof of Figure 2) in the context.
and rules to facts. This enforces a semantic con-                 These are taken as true as their positive counter-
straint that the set of candidate edges in the ensuing            parts (“The bald eagle is kind”) are non-derivable
proof is consistent with the chosen set of nodes,                 given the context. Thus, if a statement s cannot be
and also simplifies the learning problem, since a                 derived from the facts and the rules in a context,
smaller number of edges need to be labeled.                       the NAF node should infer that “not s” is true. We
                                                                  model this notion of the negation of all unprovable
3.3      PROVER: Joint QA and Proof
                                                                  statements (given a context) by learning NAF as
         Generation Model
                                                                  a function of everything provable in the context,
Figure 3 shows the architecture of PROVER, built                  encoded by the t[CLS] embedding.3
on top of RoBERTa (Liu et al., 2019b). Our model
                                                                     3
                                                                       We note that a proof can have multiple NAF nodes, each
   2
       The masked edges do not contribute to the training loss.   representing a different negated fact. Since the datasets label
                                                                      [1, 0, -100, . . . . . . . . . . . . . . . , 1]
                     [1, 1, 0, . . . . . . . . . . . . . , 1, 1]                                                              RF1
                                                                                    Edge Labels                                           RF2      ...    RFk   ...     RFi
                                 Node Labels
                                                                                                                              NAF
          False                                                                     Edge Classifier
                                                                                                                                               NAF

        QA Label
                               Node Classifier                                                                              Q - The tiger does not eat the mouse.
                                                                   𝑡(𝑅𝐹1,𝑅𝐹2 ) 𝑡(𝑅𝐹2,𝑅𝐹1 )                    𝑡(𝑁𝐴𝐹,𝑅𝐹𝑘 )
                                                                                                                            RF1 – The tiger eats the bald eagle.
                                                                                                                            RF2 – If someone eats the bald eagle and the bald
           QA                                                                                                               eagle is not kind then the bald eagle is rough.
        Classifier                                                                                                          .......
                                                                                                                            RFi - ………………………………………..
                                                                                                                            ……..
                             𝑡𝑅𝐹1                 𝑡𝑅𝐹2                                           𝑡𝑅𝐹𝑘            𝑡𝑁𝐴𝐹       RFn – If someone sees the lion and they do not eat
                                                                                                                            the tiger then the tiger is rough.



          𝑡[𝐶𝐿𝑆]     𝑡𝑤 1 . . . 𝑡     1   𝑡𝑤 2 . . . 𝑡𝑤 2 RoBERTa Embeddings 𝑡𝑤 𝑘 . . . 𝑡𝑤 𝑘
                       1          𝑤𝑎         1           𝑏                                   1            𝑠



                      (1)      (1) (2)     (2)                                             (𝑘)
                     𝑤1 . . . 𝑤𝑎 𝑤1 . . . 𝑤𝑏                        RoBERTa               𝑤1 . . . 𝑤𝑠(𝑘)


          [CLS]            RF1                   RF2                                             RFk             <SEP>         <SEP>                 Q            <SEP>

Figure 3: Architecture diagram of PROVER. The presence and absence of nodes/edges are labeled by 1 and 0 respectively while
-100 represents masked out edges.

The node classifier HN ode has a similar architecture                                      LQA , LN ode and LEdge denote the three losses, the
to the QA classifier and predicts a presence and                                           overall loss L is given by:
absence probability score for each node.
                                                                                                                 L = LQA + LN ode + LEdge
       PN ode = σ(HN ode ({tRFi }ki=1 , tNAF ))                                            3.4          ILP Inference for Global Constraints
Edge Module: Now, given the representations                                                As mentioned previously, during inference, we en-
of each fact, rule and NAF , we learn a represen-                                          force additional constraints on the structure of the
tation for each edge between these. Formally, we                                           predicted proof graph. For this, we frame infer-
define the edge embedding t(RFi ,RFj ) from node                                           ence as Integer Linear Program (ILP) optimization,
RFi to node RFj by concatenating their individual                                          which we describe next. We follow the generative
embeddings tRFi and tRFj with their element-wise                                           process of a graph wherein the nodes are defined
difference (which gives the directionality vector).                                        first, followed by the edges on that set of nodes.
                                                                                           Thus, we fix the nodes first based on the predictions
                                                                                           by the node module of our model and maximize
      t(RFi ,RFj ) = [tRFi , tRFj , (tRFj − tRFi )]                                        a global score over the set of edges only. This re-
                                                                                           duces the large search space and ensures that all
The above formulation also helps learn separate                                            constraints can be expressed as linear expressions.
representations for edges RFi → RFj and RFj →
                                                                                           Proof Connectivity Formulation: An impor-
RFi . This is essential for our task as a proof can
                                                                                           tant constraint is to ensure that the predicted
have edges between two rules in both directions.
                                                                                           proof graphs are connected.4 To check if a proof
In Section 4.7, we see that this formulation leads
                                                                                           graph P is connected, we define an augmented
to a near perfect empirical performance in predict-
                                                                                           graph Paug = (Naug , Eaug ) with two added nodes
ing the directionality of edges. The edge classifier
                                                                                           “source” and “sink”. We add an edge from the
HEdge outputs probability scores representing the
                                                                                           source to any one of the nodes x in P. We also
presence and absence of each edge.
                                                                                           define edges from all nodes in P to the sink.
    PEdge = σ(HEdge ({t(RFi ,RFj ) }k+1
                                    i,j=1 ))                                                                                     Naug = N ∪ {source, sink}
                                          tRFk+1 = tNAF                                    Eaug = E ∪ {(source, x)} ∪ {(n, sink)∀n ∈ N }
 We train our model by using binary cross-entropy                                          Having defined Paug , we can reduce the graph
loss for each of the three modules. Formally, if                                           connectivity in P to a maximum flow problem
                                                                                              4
all these as NAF , we collapse all the NAF nodes into a single                                  Proofs are directed graphs. We check connectivity in the
node and learn a unified representation for them.                                          equivalent undirected graphs.
(Leighton and Rao, 1999) in Paug (Even and Tar-             fact. Next, to ensure proof connectivity, we first
jan, 1975). For this, we define the capacity variable       define the flow constraints in Equations 5 and 6 con-
c(m,n) for each edge, m → n in Paug , as follows.           strained by the flow variables f(m,n) for each edge
                                                            m → n. These maintain the capacity constraints
      c(source,x) = |N | and c(x,source) = 0                (the flow at each edge should be less than its ca-
  ∀n ∈ N , c(n,sink) = 1 and c(sink,n) = 0                  pacity) and the flow conservation constraints (the
                 ∀m, n ∈ N , c(m,n) = |N |                  total flow through the incoming edges at a node is
            c(m,n) = 0 if m ∈
                            / N or n ∈
                                     /N                     equal to the total flow through the outgoing edges).
                                                            Equation 7 ensures connectivity in the proof graph,
Now, there can be a maximum total flow of |N |              by enforcing the total flow to be |N |. Finally, we
from the source to the sink, if and only if the graph       ensure that the proof connectivity is checked on
is connected. We use this flow formulation to pro-          the valid edges only (which are part of the proof)
vide additional constraints for our ILP inference           through the last constraint, since a max-flow of |N |
procedure that ensure connectivity of proof graphs.         is achievable for any connected graph.

Final Optimization Problem: Our maximiza-                   4     Experiments
tion objective, subject to the connectivity constraint
and all other constraints (that ensure a valid proof)       Our experiments evaluate the effectiveness of
is as follows. Let φ(m,n) represent the probability         PROVER (PR), our joint QA, and proof model
that an edge m → n is present, as predicted by              against RuleTakers (RT). Details of our experimen-
PROVER. We want to infer 0/1 assignments for our            tal setup are in the appendix.
optimization variables e(m,n) (a value of 1 means
the edge is part of the proof, while 0 means it is          4.1    Datasets and Evaluation Metrics
not) such that the following objective is maximized:        We conduct experiments on all the three sets of
                                                            datasets introduced in Clark et al. (2020) and con-
                       X                                    sisting of gold answers and proofs. Further details
        argmax                 (φ(m,n) e(m,n) +
       e(m,n) ,f(m,n) m,n,m6=n                              of the datasets can be found in the appendix.
                                                            DU0-DU5: The first set consists of five datasets,
                 (1 − φ(m,n) )(1 − e(m,n) ))                each containing 100k questions with theories in
subject to constraints:                                     synthetic language and requiring reasoning paths
                                                            up to depth D (D = 0, 1, 2, 3, 5). We refer to these
  ∀m, n ∈ F ∪ R ∪ NAF , e(m,n) ∈ {0, 1}               (1)   datasets as DU0, DU1, DU2, DU3 and DU5, where
            e(m,n) = 0, if m ∈
                             / N or n ∈
                                      /N              (2)   DU stands for “Depth Upto”.
                                                            Birds-Electricity: It consists of two test-only
           e(m,n) = 0, if m ∈ F and n ∈ F             (3)
                                                            datasets of 5k samples used to evaluate the out-
           e(m,n) = 0, if m ∈ R and n ∈ F             (4)   of-distribution performance of the models.
       ∀m, n ∈ Naug , 0 ≤ f(m,n) ≤ c(m,n)             (5)   ParaRules: ParaRules consists of 40k questions
                                                            against 2k theories expressed in paraphrased natu-
                           X
           ∀n ∈ Naug ,             f(m,n)
                          m:(m,n)∈Eaug
                                                            ral language, obtained through crowdsourcing.
                                  X                            We evaluate QA performance through accuracy.
                          =                  f(n,o)   (6)   For proofs, we introduce three metrics: (1) Node
                              o:(n,o)∈Eaug
                                                            Accuracy (NA): Fraction of examples where the
                              f(source,x) = |N |      (7)   predicted node set matches exactly with the gold
            ∀m, n ∈ Naug , e(m,n) + e(n,m)                  node set, (2) Edge Accuracy (EA): Fraction of ex-
                          −(f(m,n) /|N |) ≥ 0         (8)   amples where the predicted edge set match exactly
                                                            with the gold set, and (3) Proof Accuracy (PA):
   Note that N , F , and R refer to the set of pre-         Fraction of examples where the generated proof
dicted nodes (from the model), the set of facts, and        matches exactly with the gold proof. For examples
the set of rules, respectively. Equations 2, 3 and          with multiple gold proofs, we give credit if the pre-
4 ensure that edges are present only when the cor-          diction matches exactly with any one of the proofs.
responding nodes are present and that there are             We also evaluate Full Accuracy (FA), denoting the
no edges between two facts and from a rule to a             fraction of samples where both the answer and the
                     QA                                                                            QA
 D      Cnt                    NA     EA     PA     FA                              Cnt                           NA            EA      PA    FA
                RT        PR                                                                  RT        PR
 0      6299    100    100     98.6   98.5   98.4   98.4    B1                        40    97.5    95.0          92.5          92.5   92.5   92.5
 1      4434    98.4   99.0    93.3   95.1   93.2   93.1    B2                        40     100    95.0          95.0          95.0   95.0   95.0
 2      2915    98.4   98.8    85.9   84.8   84.8   84.8    E1                       162    96.9    100           95.1          96.3   95.1   95.1
 3      2396    98.8   99.1    82.3   80.5   80.5   80.5    E2                       180    98.3    100           91.7          93.3   91.7   91.7
 4      2134    99.2   98.8    77.7   72.5   72.5   72.4    E3                       624    91.8    89.7          72.3          73.1   72.3   71.8
 5      2003    99.8   99.3    76.0   65.1   65.1   65.1    E4                      4224    76.7    84.8          81.4          81.3   80.6   80.6
 All   20192    99.2   99.3    89.2   87.5   87.1   87.1    All                     5270    80.1    86.5          81.3          81.4   80.7   80.5

Table 1: QA comparison between RT and PR for vary-         Table 2: Zero-shot performance comparison on the
ing depths along with node, edge, proof and full accu-     Birds-Electricity dataset after training on DU5.
racy for PROVER on DU5. Cnt = Sample Count.
                                                                                                             RT    PR
                                                                                                                                       98.6
                                                                                    100
proof are exactly correct.                                                                                               89.6          98.9
                                                                                    90




                                                                  Accuracy on DU5
                                                                                    80                  73.7             83.9
4.2    QA and Proof Results for Varying Depths                                      70
                                                                                           68.7



We first train and evaluate PROVER on the train                                     60
                                                                                                        63.5
                                                                                    50
and test splits of the DU5 dataset, and compare its                                 40
                                                                                           53.5


QA performance with RuleTakers for questions                                               DU0          DU1
                                                                                                           Train Datasets
                                                                                                                         DU2           DU3


of varying depths (D). Table 1 shows these re-
                                                           Figure 4: QA performance comparison between
sults and the proof-related metrics for PROVER.            PROVER and RuleTakers with models trained on DU0,
The corresponding validation set results can be            DU1, DU2 and DU3 and tested on DU5.
found in the appendix. Overall, and at each depth,
PROVER matches the QA performance of Rule-                 PROVER on the Birds-Electricity dataset (Table 2).
Takers. PROVER is also able to generate exact              The DU5-trained model is tested on six datasets,
proofs fairly accurately at 87%. Perhaps unsur-            two from the birds domain (B1, B2) and another
prisingly, we find that edge prediction is a harder        four from the electricity domain (E1, E2, E3, E4).
task than node prediction, and performance wors-           Overall, our model achieves a 6% QA improve-
ens with increasing depth due to an increasingly           ment over RuleTakers. More importantly, PROVER
large number of edges to be labeled. The proof             outperforms RuleTakers by 8% on the hardest and
accuracy matches the edge accuracy at each depth,          largest E4 subset of the data. The proof accuracy is
suggesting that proofs are almost always correct if        also fairly high, demonstrating good proof genera-
the edges are correct. Similarly, the full accuracy        tion ability of our model for out-of-distribution data
matches the proof accuracy, showing that the pre-          as well. Similar to the test results on DU5, the full
dicted answer is almost always correct when the            accuracy matches the proof accuracy, demonstrat-
corresponding proof is correct. This points to an          ing proof consistency with the predicted answers.
interesting observation – QA is easier than node           We show examples of proofs generated by PROVER
prediction, which in turn is easier than edge pre-         in Figure 2 and in the appendix.
diction. All the datasets experimented with exhibit
this behavior, as we also describe later. Proof gen-       4.4         Generalization to Higher Depths
eration becomes harder with increasing depth (and          We evaluate the generalization ability of PROVER
hence, more nodes and edges), as the exact proof           compared to RuleTakers by training models on the
generation accuracy drops to 65% for depth 5. On           train splits of DU0, DU1, DU2 and DU3, and test-
analyzing further, we find that on average, PROVER         ing the QA performance on the overall test set for
correctly predicts 6 out of 7 edges present in a           DU5, which includes questions with higher depth
depth 5 proof. Overall, PROVER is interpretable            than seen during training. The corresponding val-
yet efficient, as it generates proofs fairly accurately    idation set and proof-related results can be found
without any loss in QA performance.                        in the appendix. As shown in Figure 4, PROVER,
                                                           when trained on depth 0 examples only, performs
4.3    Zero-Shot Evaluation                                significantly better than RuleTakers with an im-
Following previous work (Clark et al., 2020), we           provement of 15%. A similar trend is observed for
now test the out-of-distribution performance of            DU1 and DU2, where PROVER improves by 10%
                     QA                                           Count    QA     NA     EA     PA     FA
 D      Cnt                    NA     EA     PA     FA
                RT        PR                                      10k      87.1   48.1   44.7   44.0   42.7
                                                                  30k      97.8   77.9   73.2   72.5   72.4
 0     2968    99.8   99.7     99.5   99.9   99.5   99.4
                                                                  70k      99.3   89.2   87.5   87.1   87.1
 1     2406    99.3   98.6     98.0   98.9   98.0   97.3
 2     1443    98.2   98.2     89.2   88.9   88.9   88.7    Table 4: Comparison of PROVER models trained with
 3     1036    96.7   96.5     92.1   90.0   90.0   89.9
 4      142    90.1   88.0     87.3   76.1   76.1   76.1    varying amount of training data on DU5. Count = Num-
                                                            ber of training examples.
 All   8008    98.8   98.4     96.0   95.8   95.4   95.1

Table 3: Comparison of models trained on DU3 and            study. These ablated variants also provide natural
ParaRules training sets and tested on ParaRules test set.   baselines for our proof-related results. Specifically,
                                                            we train and test the following models on DU5: (1)
and 6%, respectively. On DU3, both models show              QA+Node: We train a model consisting of only
high and comparable performance. PROVER’s su-               the QA and Node modules; (2) No NAF: We train
perior generalization ability can be attributed to          a model using random NAF embeddings; (3) Un-
the extra training supervision incorporated in the          constrained Train (UT) + No ILP: We remove
form of proofs and an inductive bias for making             constraints both during training and inference; (4)
proof-based predictions. While proof construction           Unconstrained Train (UT) + ILP: We remove
for supervised training is expensive, PROVER’s su-          constraints only during training; (5) No Connec-
perior QA results on out-of-distribution data (Table        tivity: Finally, we train a model where we only re-
2) and higher depth questions is a potential first          move the connectivity constraint during inference.
step to showing that limited proof supervision can          More details about these models in appendix.
still lead to effective generalization.                         The QA accuracy is mostly unaffected in all our
                                                            models and all but “No NAF” have similar node
4.5    Varying Training Data Size
                                                            accuracy. The “No NAF” model does not learn a
We explore varying the amount of training data              representation for NAF, leading to 5-6% drop in
from 10k to 30k to all the examples (70k) in DU5.           both node and edge accuracy. The 5-6% drop in
As shown in Table 4, when trained with only 40%             edge and proof accuracy for the “Unconstrained
of the data, PROVER obtains a near-perfect QA               Train + No ILP” model, compared to PROVER,
accuracy of 97.8%. Thus, for QA, PROVER’s joint             shows that removing constraints results in a harder
training with proofs can compensate for the lack of         learning problem and the model fails to automati-
training data. Proof generation, however, is much           cally learn all the constraints. The proof accuracy
harder and with increased training data, the rate of        improves slightly when we add constraints only dur-
increase in proof accuracy is much more gradual.            ing inference (“Unconstrained Train + ILP”). The
                                                            connectivity constraint provides only marginal im-
4.6    Evaluation on Complex Language                       provement as our model mostly predicts connected
We also test PROVER’s ability to generate proofs            proofs without any explicit supervision. Specifi-
for more human-like natural language theories.              cally, only 57 examples have disconnected proofs
More details on the ParaRules dataset can be found          without this constraint. The overall PROVER model
in the appendix. Following Clark et al. (2020), we          outperforms all variants in full accuracy.
train a model by combining the DU3 and ParaRules                To better understand the loss of accuracy for
training partitions and test on the ParaRules test par-     higher depth proofs, we perform error analysis of
tition. Table 3 again shows that PROVER matches             PROVER for the depth 5 subset of DU5. We find
the QA performance of RuleTakers, and also gen-             that our NAF learning module is highly accurate –
erates proofs with a high accuracy of 95%. Follow-          PROVER correctly predicts NAF in a proof 95% of
ing previous trends, the proof accuracy drops as            the time. Among all examples with incorrectly pre-
the depth increases, and QA performance is higher           dicted node sets, 42% are such that the predicted set
than for node prediction, which in turn is higher           is a subset of the gold set while for 25% examples,
than for edge prediction.                                   it is a superset, demonstrating that our model tends
                                                            to underestimate the number of essential rules and
4.7    Ablation and Error Analysis                          facts. PROVER almost perfectly identifies the di-
Table 5 analyzes the effectiveness of the individ-          rection of edges. We find only 1 example where
ual components of PROVER through an ablation                the proof is incorrect solely due to the incorrect
                      QA     NA     EA     PA     FA     explanation generation system. However, other
    QA+N+E (PR)       99.3   89.2   87.5   87.1   87.1   tasks may require imposing additional constraints
    QA+N              99.4   88.9      -      -      -   to ensure valid explanations.PROVER’s inference
    QA (RT)           99.2      -      -      -      -
    No NAF            99.5   83.1   82.3   81.7   81.7
                                                         mechanism can be extended to incorporate these.
    UT + No ILP       99.4   90.1   83.0   81.9   81.9
    UT + ILP          99.4   90.1   83.4   82.9   82.8   Broader Implications in Formal Logic:
    No Connectivity   99.3   89.2   87.8   87.0   87.0   PROVER’s framework is not conceptually
                                                         constrained to a particular logic fragment.
Table 5: Ablation studies of PROVER showing the im-
portance of each component and constraints.              PROVER uses the idea that applying a rule to
                                                         fact(s) can produce new fact(s). All logic frag-
                                                         ments from formal logic fit this idea and may only
identification of directionality. Further, 21% of the    differ in the nature of the graphs generated. For
incorrectly predicted edges are subsets of the gold      a fact “Robin is a bird” and a rule with universal
sets, while 35% are supersets.                           quantification “All birds can fly”, PROVER’s graph
                                                         will have an edge from the fact to the rule to
5     Discussion and Future Work                         generate “Robin can fly”. We experiment with
                                                         datasets which already contain negations in facts.
Graph-based Explanations: While we have
                                                         While these datasets currently do not contain
presented PROVER as a model that can emulate
                                                         disjunctions, our graphical representations of
formal reasoning, it has further potential use as an
                                                         proofs allow an easy extension in such scenarios.
explanation generation system. PROVER generates
                                                         E.g., if there is a disjunction rule “If X or Y then
compositional explanations in the form of graphs
                                                         Z” instead of a conjunction rule “If X and Y then
and QA systems, in general, can potentially benefit
                                                         Z”, only the shape of the graph changes. In the
from generating such graphical explanations. For
                                                         former, Z is proved by either an edge from X
example, in multi-hop QA tasks, the node module
                                                         or from Y to the rule, while in the latter, both
can choose all the relevant sentences in the context
                                                         edges have to be necessarily present. Inferences
and the edge module can identify the flow of infor-
                                                         over modals like “might” and disjunction rules
mation between these to arrive at the answer (in
                                                         like “If X then Y or Z” will mean that both the
the presence of task-specific constraints). Graph-
                                                         answer and the proof will be probabilistic. In such
ical explanations, in contrast to natural language
                                                         scenarios, PROVER’s unweighted proof graphs
ones, are more structured and can allow explicit
                                                         can be extended to weighted ones to represent this
modeling of causality (and are easier to evaluate, as
                                                         probabilistic nature.
opposed to free-form natural language generation).
We hope that PROVER will encourage further work          6   Conclusion
towards developing interpretable NLP models with
structured explanations.                                 We introduce PROVER, an interpretable joint
                                                         model that answers binary questions over natural
QA and Proof Consistency: Currently,                     language rule-bases and generates corresponding
PROVER predicts the answer and generates the             proofs. The proofs are generated through the node
proof by jointly optimizing the QA, node and edge        and edge modules of the model in the presence
modules using a shared RoBERTa model. Another            of multiple global constraints during training and
modeling choice could explicitly condition the           ILP inference. Our model improves state-of-the-
QA module on the node and edge modules so                art QA accuracy in the zero-shot scenario by 6%
that the answer is predicted from the proof. We          and generates proofs accurately. PROVER also
empirically verify the consistency between the           generalizes much better to higher depth questions
predicted answer and the generated proof by              with up to 15% absolute improvement in QA per-
showing that the full accuracy matches the proof         formance over RuleTakers. PROVER’s modeling
accuracy. However, in scenarios where questions          is relatively generic, and similar proof generation
have open-ended answers, generating answer               methods can be explored in traditional multi-hop
from a ‘proof’ in a consistent manner needs              QA tasks. PROVER can also be a helpful aid to
more exploration. PROVER’s constraints like              formal reasoners in scenarios where rules are fuzzy
ensuring connectivity are necessary constraints          and creating rule-bases in a formal language is te-
for generating valid proofs for any graph-based          dious or infeasible.
7   Acknowledgements                                     Ido Dagan, Dan Roth, Mark Sammons, and Fabio Mas-
                                                            simo Zanzotto. 2013. Recognizing textual entail-
We thank the reviewers for their helpful feed-              ment: Models and applications. Synthesis Lectures
back. This work was supported by DARPA MCS                  on Human Language Technologies, 6(4):1–220.
Grant N66001-19-2-4031, NSF-CAREER Award                 Finale Doshi-Velez and Been Kim. 2017. Towards a
1846185, DARPA YFA17-D17AP00022, ONR                        rigorous science of interpretable machine learning.
Grant N00014-18-1-2871, Microsoft Investigator              arXiv preprint arXiv:1702.08608.
Fellowship, and Munroe & Rebecca Cobey Fel-              Shimon Even and R Endre Tarjan. 1975. Network flow
lowship. The views in this article are those of the        and testing graph connectivity. SIAM journal on
authors and not the funding agency.                        computing, 4(4):507–518.

                                                         Peter Hase and Mohit Bansal. 2020. Evaluating ex-
                                                           plainable AI: Which algorithmic explanations help
References                                                 users predict model behavior?     In Proceedings
                                                           of the 58th Annual Meeting of the Association for
Ralph Abboud, Ismail Ilkan Ceylan, and Thomas              Computational Linguistics.
  Lukasiewicz. 2020. Learning to reason: Leverag-
  ing neural networks for approximate DNF counting.      Han He and Jinho Choi. 2020. Establishing strong
  In Proceedings of the 34th AAAI Conference on            baselines for the new decade: Sequence tagging,
  Artificial Intelligence.                                 syntactic and semantic parsing with bert. In The
                                                           Thirty-Third International Flairs Conference.
Ibrahim Abdelaziz, Veronika Thost, Maxwell Crouse,
   and Achille Fokoue. 2020.        An experimental      Shalmali Joshi, Oluwasanmi Koyejo, Been Kim, and
   study of formula embeddings for automated theo-         Joydeep Ghosh. 2018. xGEMs: Generating exam-
   rem proving in first-order logic. arXiv preprint        plars to explain black-box models. arXiv preprint
   arXiv:2002.00423.                                       arXiv:1806.08867.

Mohit Bansal, Claire Cardie, and Lillian Lee. 2008.      Aishwarya Kamath and Rajarshi Das. 2019. A sur-
 The power of negative thinking: Exploiting label dis-     vey on semantic parsing. In Automated Knowledge
 agreement in the min-cut classification framework.        Base Construction (AKBC).
 In COLING 2008: Companion Volume: Posters,              Guokun Lai, Qizhe Xie, Hanxiao Liu, Yiming Yang,
 pages 15–18.                                              and Eduard Hovy. 2017. RACE: Large-scale read-
                                                           ing comprehension dataset from examinations. In
Regina Barzilay and Mirella Lapata. 2005. Collec-          Proceedings of the 2017 Conference on Empirical
  tive content selection for concept-to-text genera-       Methods in Natural Language Processing, pages
  tion. In Proceedings of the conference on Human          785–794.
  Language Technology and Empirical Methods in
  Natural Language Processing, pages 331–338. As-        Guillaume Lample and François Charton. 2020.
  sociation for Computational Linguistics.                 Deep learning for symbolic mathematics.     In
                                                           8th International Conference on Learning
Jonathan Berant, Andrew Chou, Roy Frostig, and             Representations, ICLR 2020. OpenReview.net.
  Percy Liang. 2013. Semantic parsing on freebase
  from question-answer pairs. In Proceedings of the      Tom Leighton and Satish Rao. 1999. Multicommodity
  2013 conference on empirical methods in natural          max-flow min-cut theorems and their use in design-
  language processing, pages 1533–1544.                    ing approximation algorithms. Journal of the ACM
                                                           (JACM), 46(6):787–832.
Jonathan Berant and Percy Liang. 2014. Seman-
  tic parsing via paraphrasing.    In Proceedings        Kevin Lin, Oyvind Tafjord, Peter Clark, and Matt Gard-
  of the 52nd Annual Meeting of the Association            ner. 2019. Reasoning over paragraph effects in sit-
  for Computational Linguistics (Volume 1: Long            uations. In Proceedings of the 2nd Workshop on
  Papers), pages 1415–1425.                                Machine Reading for Question Answering, pages
                                                           58–62, Hong Kong, China. Association for Compu-
                                                           tational Linguistics.
Oana-Maria Camburu, Tim Rocktäschel, Thomas
  Lukasiewicz, and Phil Blunsom. 2018. e-SNLI:           Hui Liu, Qingyu Yin, and William Yang Wang. 2019a.
  Natural language inference with natural language         Towards explainable NLP: A generative explanation
  explanations. In Advances in Neural Information          framework for text classification. In Proceedings
  Processing Systems, pages 9539–9549.                     of the 57th Annual Meeting of the Association for
                                                           Computational Linguistics, pages 5570–5581.
Peter Clark, Oyvind Tafjord, and Kyle Richardson.
  2020. Transformers as soft reasoners over lan-         Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-
  guage.       In International Joint Conference on        dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,
  Artificial Intelligence.                                 Luke Zettlemoyer, and Veselin Stoyanov. 2019b.
  RoBERTa: A robustly optimized bert pretraining ap-     Pouya Samangouei, Ardavan Saeedi, Liam Naka-
  proach. arXiv preprint arXiv:1907.11692.                 gawa, and Nathan Silberman. 2018. ExplainGAN:
                                                           Model explanation via decision boundary crossing
Bill MacCartney and Christopher D Manning. 2014.           transformations. In Proceedings of the European
   Natural logic and natural language inference. In        Conference on Computer Vision (ECCV), pages
   Computing meaning, pages 129–147. Springer.             666–681.
Mark A Musen and Johan Van Der Lei. 1988. Of brit-       David Saxton, Edward Grefenstette, Felix Hill, and
 tleness and bottlenecks: Challenges in the creation       Pushmeet Kohli. 2019. Analysing mathematical rea-
 of pattern-recognition and expert-system models. In       soning abilities of neural models. In International
 Machine Intelligence and Pattern Recognition, vol-        Conference on Learning Representations.
 ume 7, pages 335–352. Elsevier.
                                                         Daniel Selsam, Matthew Lamm, Benedikt Bünz, Percy
Arvind Neelakantan, Quoc V. Le, and Ilya Sutskever.        Liang, Leonardo de Moura, and David L. Dill.
  2016. Neural programmer: Inducing latent pro-            2019. Learning a SAT solver from single-bit super-
  grams with gradient descent. In 4th International        vision. In 7th International Conference on Learning
  Conference on Learning Representations, ICLR             Representations, ICLR 2019, New Orleans, LA,
  2016, Conference Track Proceedings.                      USA, May 6-9, 2019. OpenReview.net.

Allen Newell and Herbert Simon. 1956. The logic          Oyvind Tafjord, Matt Gardner, Kevin Lin, and Peter
  theory machine–a complex information processing          Clark. 2019. QuaRTz: An open-domain dataset of
  system. IRE Transactions on information theory,          qualitative relationship questions. In Proceedings
  2(3):61–79.                                              of the 2019 Conference on Empirical Methods
                                                           in Natural Language Processing and the 9th
Bo Pang and Lillian Lee. 2004. A sentimental educa-        International Joint Conference on Natural Language
  tion: Sentiment analysis using subjectivity summa-       Processing (EMNLP-IJCNLP), pages 5941–5946,
  rization based on minimum cuts. In Proceedings           Hong Kong, China. Association for Computational
  of the 42nd annual meeting on Association for            Linguistics.
  Computational Linguistics, page 271. Association
  for Computational Linguistics.                         Alon Talmor, Yanai Elazar, Yoav Goldberg, and
                                                           Jonathan Berant. 2019. oLMpics–on what lan-
Nazneen Fatema Rajani, Bryan McCann, Caiming               guage model pre-training captures. arXiv preprint
  Xiong, and Richard Socher. 2019. Explain yourself!       arXiv:1912.13283.
  leveraging language models for commonsense rea-        Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
  soning. In Proceedings of the 57th Annual Meeting        Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz
  of the Association for Computational Linguistics,        Kaiser, and Illia Polosukhin. 2017. Attention is
  pages 4932–4942.                                         all you need. In Advances in neural information
Scott E. Reed and Nando de Freitas. 2016. Neu-             processing systems, pages 5998–6008.
  ral programmer-interpreters. In 4th International      Qiang Wang, Bei Li, Tong Xiao, Jingbo Zhu,
  Conference on Learning Representations, ICLR             Changliang Li, Derek F. Wong, and Lidia S. Chao.
  2016, San Juan, Puerto Rico, May 2-4, 2016,              2019. Learning deep transformer models for ma-
  Conference Track Proceedings.                            chine translation. In Proceedings of the 57th Annual
                                                           Meeting of the Association for Computational
Marco Tulio Ribeiro, Sameer Singh, and Carlos
                                                           Linguistics, pages 1810–1822, Florence, Italy. As-
 Guestrin. 2016. ”Why should I trust you?”: Explain-
                                                           sociation for Computational Linguistics.
 ing the predictions of any classifier. In Proceedings
 of the 22nd ACM SIGKDD international conference         Leon Weber, Pasquale Minervini, Jannes Münchmeyer,
 on knowledge discovery and data mining, pages             Ulf Leser, and Tim Rocktäschel. 2019. NLPro-
 1135–1144.                                                log: Reasoning with weak unification for question
                                                           answering in natural language. In Proceedings of
Marco Tulio Ribeiro, Sameer Singh, and Carlos              the 57th Annual Meeting of the Association for
 Guestrin. 2018. Anchors: High-precision model-            Computational Linguistics, pages 6151–6161, Flo-
 agnostic explanations. In Thirty-Second AAAI              rence, Italy. Association for Computational Linguis-
 Conference on Artificial Intelligence.                    tics.
Kyle Richardson, Hai Hu, Lawrence S Moss, and            Jason Weston, Antoine Bordes, Sumit Chopra, Alexan-
  Ashish Sabharwal. 2020.      Probing natural lan-         der M Rush, Bart van Merriënboer, Armand Joulin,
  guage inference models through semantic fragments.        and Tomas Mikolov. 2015. Towards AI-complete
  In Thirty-Fourth AAAI Conference on Artificial            question answering: A set of prerequisite toy tasks.
  Intelligence.                                             arXiv preprint arXiv:1502.05698.
Cynthia Rudin. 2019. Stop explaining black box ma-       Thomas Wolf, Lysandre Debut, Victor Sanh, Julien
  chine learning models for high stakes decisions and      Chaumond, Clement Delangue, Anthony Moi, Pier-
  use interpretable models instead. Nature Machine         ric Cistac, Tim Rault, Rémi Louf, Morgan Fun-
  Intelligence, 1(5):206–215.                              towicz, et al. 2019. Huggingface’s transformers:
    State-of-the-art natural language processing. arXiv          A.2   Dataset Details
    preprint arXiv:1910.03771.
                                                                 Below we briefly describe the three sets of datasets
Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio,
                                                                 we conduct experiments on.8 Each dataset has a
  William Cohen, Ruslan Salakhutdinov, and Christo-              train, validation and test split, except for the zero-
  pher D Manning. 2018. HotpotQA: A dataset for di-              shot test-only one. Further details about these can
  verse, explainable multi-hop question answering. In            be found in Clark et al. (2020).
  Proceedings of the 2018 Conference on Empirical
  Methods in Natural Language Processing.                        DU0-DU5: The first set consists of five datasets,
                                                                 each containing 100k questions with theories in
Luke S. Zettlemoyer and Michael Collins. 2005. Learn-            synthetic language and requiring reasoning paths
  ing to map sentences to logical form: Structured
  classification with probabilistic categorial grammars.
                                                                 up to depth D (D = 0, 1, 2, 3, 5). For example,
  In Proceedings of the Twenty-First Conference on               D = 0 means the true facts can be proved by sim-
  Uncertainty in Artificial Intelligence, UAI’05, page           ple lookup in the context. The samples are ran-
  658–666. AUAI Press.                                           domly split 70/10/20 into train/dev/test partitions
                                                                 such that there is no overlap of theories between
Hongming Zhang, Xinran Zhao, and Yangqiu Song.                   the partitions.
  2020.     WinoWhy: A deep diagnosis of es-
  sential commonsense knowledge for answering                    Birds-Electricity: The second set consists of
  Winograd schema challenge. In Proceedings of
  the 58th Annual Meeting of the Association for                 two test-only datasets used to evaluate robustness
  Computational Linguistics (ACL).                               and out-of-distribution performance of the models.
                                                                 The contexts are about birds and an electric circuit,
A     Appendix                                                   and consist of 5k samples in total. The vocabulary
                                                                 of entities, attributes and predicates, apart from
A.1    Experimental Setup                                        is() are all new at test time.

We build our model on top of the Hugging Face                    ParaRules: The final dataset, ParaRules consists
Transformers library (Wolf et al., 2019).5 All hyper-            of 40k questions against 2k theories expressed in
paramters are chosen based on the best validation                paraphrased natural language, obtained through
set performance (Full Accuracy) of the correspond-               crowdsourcing. While the previous datasets con-
ing dataset. We use RoBERTa-large (Liu et al.,                   tain synthetic language, ParaRules tests the models’
2019b) as the pre-trained Language Model and all                 ability to reason over more human-like paraphrased
our models are trained using a batch size of 8 and               language.
a maximum sequence length of 300. We train the
                                                                 A.3   QA and Proof Results for Varying
models for a maximum of 5 epochs using an ini-
                                                                       Depths
tial learning rate of 10−5 , with linear decay and a
weight decay of 0.1 . The dropout probability is                 Table 7 shows the DU5 validation set performance
chosen to be 0.1. The random seed used in all the                of PROVER trained on the training split of DU5.
experiments is 42. Each epoch of PROVER takes                    PROVER obtains a near perfect QA accuracy and
2.5 hours to run on one V100 Volta GPU. The total                a proof accuracy of 88%. While the QA accuracy
number of parameters of PROVER is similar to that                remains equally high at all depths, the proof accu-
of RoBERTa-large (355M ). Batch size and learn-                  racy drops with increasing depth. Full accuracy
ing rate are manually tuned in the range {8,16} and              matches the proof accuracy, demonstrating consis-
{10−5 , 2 ∗ 10−5 } respectively. The ILP is modeled              tency between the predicted answers and generated
using PuLP.6 Proofs in the datasets are represented              proofs.
as bracketed strings, which are pre-processed into
                                                                 A.4   Generalization to Higher Depths
graph representations consisting of unique nodes
and edges. The maximum number of facts and                       In Table 6, we provide detailed results of
rules corresponding to a context is 25.7                         PROVER’s generalization ability to higher depth
                                                                 questions. Specifically, we evaluate four models,
    5
      https://github.com/huggingface/                            trained on the training splits of DU0, DU1, DU2
transformers                                                     and DU3 and tested on the validation and test splits
    6
      https://pypi.org/project/PuLP/
    7                                                              8
      Further details of our best hyperparameters can be found       https://rule-reasoning.apps.allenai.
in the attached code as part of the supplementary material.      org/
                                  QA                 NA                EA                 PA                 FA
                             Dev      Test     Dev        Test   Dev        Test   Dev         Test   Dev         Test
                     DU0     68.3     68.7     45.3     46.0     49.3       49.5   43.8        44.4   42.3        42.8
                     DU1     73.2     73.7     66.4     66.3     64.5       64.3   63.9        63.8   61.8        61.9
                     DU2     89.3     89.6     76.6     76.4     73.1       73.1   72.6        72.6   72.3        72.3
                     DU3     98.3     98.6     85.5     85.0     79.9       79.5   79.4        79.1   79.4        79.1

Table 6: Performance of PROVER trained on the training splits of DU0, DU1, DU2 and DU3 and tested on the
validation and test splits of DU5.


      D      Cnt    QA     NA        EA       PA       FA           ular person) and the rules from a theory and then
      0      3116    100   98.7     98.6     98.5     98.5          asking crowdworkers to paraphrase these in their
      1      2304   98.8   92.5     94.9     92.2     92.2          own words. For example, a fact group “Alan is
      2      1436   99.2   86.1     85.6     85.6     85.6
      3      1165   98.7   85.1     82.8     82.8     82.8
                                                                    blue. Alan is rough. Alan is young.”, may be re-
      4      1041   98.8   81.2     76.9     76.9     76.9          worded into “Alan is on the young side, but rough.
      5       990   99.3   78.3     67.4     67.4     67.4          He often feels rather blue.”. Thus, unlike the pre-
      All   10068   99.3   90.0     88.6     88.0     88.0          vious datasets where the proof graphs are com-
                                                                    posed of facts and rules, ParaRules proofs are com-
Table 7: Performance of PROVER trained on the train-                posed of fact groups and rules.9 PROVER obtains
ing split of DU5 and tested on the validation split of
                                                                    high QA and proof accuracy on complex human-
DU5.
                                                                    parapharsed rule-bases, showing good generaliza-
                                                                    tion on such language. However, the proof ac-
      D      Cnt    QA     NA       EA       PA       FA
                                                                    curacy again drops as the depth of the questions
      0     1485    99.9   99.6     99.7     99.5     99.5          increases.
      1     1180    99.7   99.3     99.5     99.3     99.3
      2      727    99.4   91.5     91.5     91.5     91.3
      3      524    98.5   92.0     90.3     90.3     90.3             A.6      Ablation Models and Simpler Baselines
      4       81     100   87.6     72.8     72.8     72.8
      5        7     100    100        0        0        0          We provide brief descriptions of our ablation mod-
      All   4004    99.6   96.8     96.2     96.1     96.0
                                                                    els. These are (1) QA+Node: We model PROVER
                                                                    consisting of only the QA and Node modules.
Table 8: PROVER results on the ParaRules validation                 Since there is no edge module, this model does
set after training on DU3+ParaRules training splits.                not require any constrained training or inference;
                                                                    (2) No NAF: We train a model using random NAF
                                                                    embeddings with no learning. This helps us un-
of DU5. We have shown previously that PROVER                        derstand the effectiveness of our NAF learning;
does significantly better than RuleTakers (Clark                    (3) Unconstrained Train + No ILP: Through this
et al., 2020) on QA generalization. The proofs,                     model, we study the effectiveness of our global
however, do not generalize that well. Note that                     constraints. Specifically, no edges are masked for
depth 0 proofs are rather simple (consisting of a                   training and during inference, the edge labels are
single fact) and a model trained on only such proofs,               predicted based on the model’s probability scores
unsuprisingly, fails to generate proofs for higher                  only; (4) Unconstrained Train + ILP: Here the
depth questions. However, the proof results start                   constraints are employed only during inference.
improving as the model gets trained on more com-                    Note that the reverse configuration, constrained
plex proofs and reaches an accuracy of 79%, when                    training without ILP inference, is not included as
trained on DU3 questions.                                           the edge logits for the masked out labels would
                                                                    be random (since they are not learned). (5) No
A.5       Evaluation on Complex Language
                                                                    Connectivity: Finally, we train a model where we
In Table 8, we report the ParaRules validation set                          9
                                                                         The original ParaRules dataset released by Clark et al.
results of PROVER trained on the combination of                     (2020) has proofs for the unparaphrased theories (consisting
DU3 and ParaRules training splits (following previ-                 of facts and rules). Using the mapping from a fact to the
ous work (Clark et al., 2020)). ParaRules is created                corresponding fact group, we replace the fact nodes in the
                                                                    proof graph with the corresponding fact group nodes. Note
by first separating the fact groups (a fact group is                that this is done to report proof accuracy for this dataset as
the set of all facts in the theory concerning a partic-             well.
only remove the connectivity constraint during ILP        chains of reasoning needed in the inference pro-
optimization, keeping everything else same.               cess. Figure 6 shows three more accurate proofs
   We also experiment with simpler baselines for          generated by PROVER for three questions from the
edge prediction like training a Random Forest with        DU5 datset.
lexical features (BLEU scores, length difference,
word overlap, etc.) and this obtains a much lower
edge accuracy of 47%. This fails primarily because
(1) proof graphs can contain NAF which account
for 9% of the data and edges from it cannot be
learned without learning a latent representation; (2)
overlap features are mostly symmetric and hence
are not enough for learning directionality; (3) there
is lack of overall context information.

A.7   Critical Sentence Identification
Clark et al. (2020) provide an initial solution to-
wards generating explanations for the predicted
answers by using a post-hoc method – they re-
move each fact or rule from the theory and check
if the predicted answer changes with the new the-
ory. They define all such rules and facts which
flip the answer as critical sentences. If an example
has multiple gold proofs, a critical sentence is one
which is present in all the proofs. We argue that
this leave-one-out analysis is not ideal for multi-
ple reasons - (1) This does not work if the theory
has negations, (2) This only predicts the presence
or absence of rules and facts, and does not look
at the entire chain of reasoning, which our model
achieves through the edge module. In our final ex-

                Accuracy   Precision   Recall   F1
   RuleTakers       74.5        98.7     86.9   92.4
   PROVER           78.1        98.7     87.2   92.6

Table 9: Comparison of critical sentence identification
on the No Negation subset of DU5 test set.

periment, we still apply the leave-one-out-strategy
on the no-negation subset of the DU5 test set for
a direct comparison with RuleTakers. As shown
in Table 9, our model identifies the exact critical
sentences in an example in 78% of the cases, a 4%
improvement over RuleTakers.

A.8   Proofs Generated by PROVER
In Figure 5, we show two rule-bases, one about
electric circuits and another about birds from the
Birds-Electricity dataset. PROVER not only an-
swers the questions correctly but also generates
the proofs accurately. These proofs are complex
because of the presence of NAF and also the long
Facts :                                                             Rules :
F1: The circuit has the battery. F2: The switch is on.              R6: If the circuit has the switch and the switch is on then the circuit is
F3: The circuit has the bell.                                       complete.
                                                                    R7: If the circuit does not have the switch then the circuit is complete.
Rules :                                                             R8: If the circuit is powered and the circuit is complete then the current
R1: If the circuit has the battery then the circuit is powered.     runs through the circuit.
R2: If the circuit does not have the battery then the circuit       R9: If the current runs through the circuit and the circuit has the light bulb
is dead.                                                            then the light bulb is glowing.
R3: If the circuit is dead then the bell is not ringing.            R10: If the current runs through the circuit and the circuit has the bell
R4: If the circuit is dead then the radio is not playing.           then the bell is ringing.
R5: If the circuit is dead then the light bulb is not glowing.      R11: If the current runs through the circuit and the circuit has the radio
                                                                    then the radio is playing.
Q1: The current runs through the circuit. [ Answer : T ]                                                   Q2: The bell is ringing. [ Answer : T ]
              F1             R1                                          F1            R1
                                          R8                                                         R8             R10
                             R7                                         NAF            R7
            NAF                                                                                       F3

 Facts :                                                            Rules :
 F1: Arthur is a bird. F2: Arthur is not wounded.                   R1: If someone is an ostrich then they are a bird.
 F3: Bill is an ostrich. F4: Colin is a bird.                       R2: If someone is an ostrich then they are abnormal.
 F5: Colin is wounded. F6: Dave is not an ostrich.                  R3: If someone is an ostrich then they cannot fly.
 F7: Dave is wounded.                                               R4: If someone is a bird and wounded then they are abnormal.
                                                                    R5: If someone is wounded then they cannot fly.
                                                                    R6: If someone is a bird and not abnormal then they can fly.
       F4
                     R4                                                                    F1
       F5                                                                                               R6
                                                                                                                 Q4: Arthur can fly. [ Answer : T ]
                   Q3: Colin is not abnormal. [ Answer : F ]                              NAF



Figure 5: Examples of proofs generated by PROVER for four questions on two rule-bases about electric circuits
and birds from the Birds-Electricity dataset. PROVER not only answers the questions correctly but also accurately
predicts the long reasoning chains with multiple branches.




Facts :                                                     Rules :
F1: The bear visits the tiger. F2: The cat is kind.         R1: If something visits the bear then it sees the bear.
F3: The mouse is green. F4: The mouse is kind.              R2: If something sees the bear then the bear likes the cat.
F5: The mouse sees the tiger. F6: The tiger is rough.       R3: If something visits the cat then the cat visits the bear.
F7: The tiger visits the cat.                               R4: If something sees the bear and the bear likes the cat then it is cold.
                                                            R5: Cold things are rough.
                                                            R6: If something is green and it likes the tiger then the tiger visits the mouse.


Q1: The cat sees the bear. [ Answer : T ] Q2: The cat is not cold. [ Answer : F]                              Q3: The tiger is cold. [ Answer : F]

  F7           R3             R1                F7             R3          R1            R2
                                                                                                      R4         R4            R1           FAIL
                                                               F7          R3            R1



Figure 6: Examples of proofs generated by PROVER for three questions on a rule-base from the DU5 dataset. The
proof corresponding to the last question is a failed case.
