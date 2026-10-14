                                        Specification-Guided Synthesis of Deadlock-Free Communication
                                               Protocol Refinements with Large Language Models
                                                            Yang Li                                       Ping Hou                                Nobuko Yoshida
                                                    University of Oxford                           University of Oxford                        University of Oxford
                                                     Computer Science                                Computer Science                           Computer Science
                                                  Oxford, United Kingdom                          Oxford, United Kingdom                      Oxford, United Kingdom
                                                  yang.li@wolfson.ox.ac.uk                         ping.hou@cs.ox.ac.uk                     nobuko.yoshida@cs.ox.ac.uk

                                        Abstract                                                                 unintended cyclic dependencies, can lead to failures, including dead-
                                        Ensuring behavioural correctness in communication protocols is a         locks. Ensuring that LLM-generated or modified programs preserve
                                        central challenge in distributed software systems, as subtle inconsis-   reliable communication remains an open challenge.
                                        tencies can lead to deadlocks. In such settings, protocol refinement –      Such systems rely on communication protocols to coordinate
                                        the safe substitution of a protocol that preserves correctness and       independently developed components. As systems evolve, proto-
                                        compatibility with other components – is essential. Large language       cols must be adapted to incorporate new functionality or modify
                                        models (LLMs) have demonstrated strong capabilities in code gen-         interaction patterns. Even minor changes can have system-wide
                                        eration and program synthesis, yet lack mechanisms to reliably           effects that are difficult to predict and diagnose. Protocol refinement
                                                                                                                 – replacing a protocol with a behaviourally compatible alternative
arXiv:2607.27964v2 [cs.SE] 2 Aug 2026




                                        produce outputs with correct behaviour. Formal specification ap-
                                        proaches, such as multiparty session types (MPST), offer rigorous        – offers a principled approach to managing this evolution. Nev-
                                        guarantees, including deadlock freedom, but provide limited sup-         ertheless, preserving the intended interaction properties during
                                        port for automatically constructing protocol refinements. In this        this process is non-trivial in practice. In many cases, refinements
                                        paper, we present Syntropy, a framework for synthesising protocol        are constructed manually, making them error-prone and hard to
                                        refinements guided by MPST specifications and LLMs. It incorpo-          validate. This motivates the following research question:
                                        rates refinement constraints directly into the generation process,
                                        ensuring the generated variants satisfy these guarantees. Our com-
                                                                                                                  How can protocol refinements be systematically synthesised while
                                        prehensive evaluation indicates that Syntropy achieves 95.6%–
                                                                                                                  retaining behavioural correctness?
                                        99.5% validity while maintaining high syntactic correctness, and
                                        produces diverse, non-trivial refinements across multiple LLMs.
                                                                                                                     To address this question, we draw on specification techniques
                                        CCS Concepts                                                             such as session types [23], in particular multiparty session types
                                        • Software and its engineering → Software notations and                  (MPST) [24, 44], which are well established for describing com-
                                        tools; • Networks → Network protocols; • Computing method-               munication protocols and reasoning about their behaviour. MPST
                                        ologies → Artificial intelligence.                                       captures global interaction structures and enforcs properties such as
                                                                                                                 communication safety and deadlock freedom. Toolchains for MPST
                                        Keywords                                                                 have been developed for over 30 programming languages [52], fa-
                                        formal specifications, large language models, protocol refinement,       cilitating its adoption in software engineering.
                                        behavioural correctness, constrained generation, session types               MPST further defines refinement relations that allow proto-
                                                                                                                 cols to be transformed into more flexible forms while preserving
                                                                                                                 these properties [21, 22]. Although checking such relations can be
                                        1   Introduction                                                         automated [5–7, 15], generating variants that satisfy refinement
                                        Modern software engineering is increasingly shaped by large lan-         constraints is not straightforward and, in some settings, undecid-
                                        guage models (LLMs) [48], which are widely used to automate pro-         able [8, 27], limiting the automation of protocol refinement.
                                        gramming tasks such as code generation [9], transformation [43],             To bridge this gap, we propose Syntropy, the first framework
                                        and program synthesis [2]. Recent work [35, 36, 43] shows that           combining LLMs with MPST to support the synthesis of protocol
                                        LLMs can produce syntactically correct and functionally useful           refinements, to the best of our knowledge. Given an MPST protocol,
                                        code across diverse tasks, including programs that satisfy certain       Syntropy constructs protocol candidates based on structured repre-
                                        semantic properties such as type safety, indicating their potential      sentations of interaction behaviour and refinement objectives. The
                                        to support complex software development workflows.                       generation process is coupled with validation against refinement
                                           Despite these advances, a key limitation remains: LLM-generated       constraints, ensuring that only valid outputs are retained. This ap-
                                        artefacts do not provide behavioural guarantees by construction,         proach extends LLM-based generation beyond syntactic and local
                                        especially in systems with complex interactions. This is particularly    semantic aspects by incorporating protocol-level requirements, in-
                                        critical in distributed software systems, from microservices [17] to     cluding deadlock freedom. By integrating generative models with
                                        cyber-physical systems [28], where reliability depends on consistent     specification-based verification, Syntropy explores the space of
                                        communication between components as well as local functionality.         valid protocol refinements and produces varied and reliable alter-
                                        Subtle interaction errors, such as incorrect message ordering or         natives that are difficult to construct manually.
                                                                                                                                                                        Yang Li, Ping Hou, and Nobuko Yoshida


                                                                                                                       p?                                              q?

                                      M - Model Store
                                                                                weighted aggregation
                                                                                                                updp         q?                                 updq         p?
standard aggregation         model        model           model


                                                                                                                      updq        m!                                  updp        m!
            P1 - Participant Client   P2 - Participant Client     Pn - Participant Client
                          update 1        update 2             update n                                         std          p?         wtd          p?         std          q?         wtd         q?

                                                                                                                       ...        ...          ...        ...          ...        ...         ...        ...
                                      A - Aggregator
                                                                                                                  (a) Session tree Ta for 𝑇a                           (b) Session tree T′a for 𝑇a′

                 Figure 1: Federated learning protocol
                                                                                                                                              Figure 2: Session trees

              p?updp                                 q?updq                                 p?updp
                                                                                                                 2       Motivation and Background
                m!std
                          q?updq
                                                       m!std
                                                                   p?updp                   m!std      q?updq    Motivation. Fig. 1 depicts the message exchange coordinating
            m!wtd                                 m!wtd                                                          distributed model training, referred to as the federated learning
                                                                                                                 protocol, reflecting communication patterns in centralised feder-
                                                                                                                 ated learning systems [26]. The protocol involves a model store m,
            (a) FSM for a                (b) Reordered FSM for a                (c) Covariant FSM for a
                                                                                                                 clients p1, . . . , p𝑛 , and an aggregator a, and proceeds in phases as
                                                                                                                 follows: (1) Model Distribution: the model store sends the current
                                Figure 3: FSMs for role a
                                                                                                                 global model to all clients; (2) Update Submission: each client per-
                                                                                                                 forms local computation and sends an update to the aggregator;
                                                                                                                 and (3) Aggregation Result: the aggregator combines the updates
   We evaluate Syntropy on two datasets, comprising protocols
                                                                                                                 and sends either a standard or weighted result to the model store.
derived from the literature and synthetic benchmarks, using multi-
                                                                                                                 The model store then updates the global model and redistributes it
ple LLMs of varying sizes: three 7B code models, a general-purpose
                                                                                                                 for the next round.
7B model, and a 32B model. Syntropy attains 95.6%–99.5% va-
                                                                                                                     We consider a minimal instance of the federated learning proto-
lidity across all models, while maintaining strong syntactic cor-
                                                                                                                 col with two clients p and q, enforcing an ordered submission of
rectness (95.4%–98.1%). Furthermore, it produces multiple distinct
                                                                                                                 updates to the aggregator a, where p precedes q.
refinements for each specification, demonstrating its ability to iden-
                                                                                                                     From the perspective of a under synchronous communication, the
tify alternative protocol formulations, rather than trivial varia-
                                                                                                                 local protocol can be represented by a finite state machine (FSM), as
tions. Ablation studies indicate that both specification guidance
                                                                                                                 shown in Fig. 3a, with the following steps: (1) receive (?) updp from
and constraint-based validation are essential for attaining high
                                                                                                                 p; (2) receive updq from q; (3) send (!) aggregated result – either
validity and diversity.
                                                                                                                 std or wtd – to the model store m; and (4) repeat from step 1.
   We additionally compare Syntropy with frontier language mod-
                                                                                                                     In practice, communication is asynchronous and typically mod-
els, demonstrating that, although frontier language models can
                                                                                                                 elled as FIFO message passing. In this scenario, a may receive the
synthesise valid protocol refinements, their coverage across pro-
                                                                                                                 update from q before that from p, violating the ordering in Fig. 3a
tocol specifications remains limited. This highlights the need for
                                                                                                                 and necessitating refinement to account for message reordering. The
the proposed approach, which enables comprehensive protocol
                                                                                                                 refined FSM, shown in Fig. 3b, captures this by admitting the re-
refinement while supporting reproducible evaluation and local de-
                                                                                                                 ception order q followed by p, while preserving the subsequent
ployment with fine-tuned open models.
                                                                                                                 aggregation and response behaviour. As the updates from p and q
   The contributions of this paper are as follows:
                                                                                                                 are independent, the two FSMs are refinements of each other.
• LLM Generation with Behavioural Guarantees. We propose                                                             Furthermore, additional refinements are possible. The general
  a novel approach to enable LLMs to synthesise MPST protocol                                                    protocol in Fig. 1 can be viewed as a contravariant refinement of
  refinements with guaranteed behavioural correctness.                                                           the minimal instance, as it admits a broader class of inputs, while
• Specification-Guided Protocol Refinement. We introduce                                                         covariant refinement arises when the aggregator deterministically
  a systematic encoding of MPST specifications that guides and                                                   produces a single fixed result (Fig. 3c).
  constrains LLM-based generation of protocol refinements.                                                           Such refinements occur naturally in distributed software sys-
• Constraint-Integrated Generation. We design a two-level                                                        tems, where communication patterns are commonly adapted for ef-
  generation workflow that incorporates constraint validation into                                               ficiency, e.g. a service may omit certain responses to reduce latency.
  the synthesis via prefix filtering and subsequent verification.                                                Nevertheless, even minor changes may introduce severe communi-
• Syntropy Framework and Empirical Evaluation. We im-                                                            cation inconsistencies. For example, refining the behaviour of a to
  plement Syntropy and evaluate it across multiple LLMs and                                                      exclude updates from q, while leaving other participants unaffected,
  datasets, demonstrating high validity and generating structurally                                              yields a communication system that violates compatibility, leading
  distinct and non-superficial protocol refinements.
Specification-Guided Synthesis of Deadlock-Free Communication Protocol Refinements with Large Language Models


                                                                                    Direct

                                           LoRA Fine-tuned                                                                                  Subtype Set
             Local Session Types                                              Constrained
                                            Heuristic LLM



                                                                                              Level1: Derivative Check (Every Token)
                                            Weighted Loss
                                                                                                    Coarse Over-approximation
                                                                                                            Fast Pruning
                                                                              Beam Search

                                           BNF-style Prompt
                                        (Syntax + Subtying Rules)
                                                                                     NO                End of Sequence(EOS)?

                                         Syntax Normalization                                                   YES
                                         (Recursion & Brackets)
                                                                                             Level2: Widening-Based Fixpoint Checker
                                                                                                      Finer Over-approximation                Valid&Diverse
                                                                                                            Late Rejection
                                      Existing Data Synthetic Data                                                                                            Subtype Set
                                              Traing Data                                        Constrained Generation with Two-Level Monitoring
                                            Syntropy-Train                                                             Syntropy-Gen


                                                                     Figure 4: Overview of Syntropy


to deadlock. This highlights the challenge of designing correct re-                          Ta associated with 𝑇a . A coinductive tree refinement relation ≲
finements and motivates the application of formal specifications to                          is defined on such session trees, and the asynchronous subtyping
ensure the rigorous synthesis of protocol refinements that preserve                          relation ⩽ is obtained by lifting ≲ to session types.
communication properties.                                                                       Consider the session type (equivalent to FSM in Fig. 3b)
MPST and Asynchronous Subtyping. Multiparty Session Types                                                𝑇a′ = 𝜇t.q?updq .p?updp . ⊕{m!std.t, m!wtd.t},
(MPST) [24, 44] provide a framework for specifying and verifying                             obtained from𝑇a by reordering the inputs. Its session tree T′a , shown
communication protocols. In MPST, the communication behaviour                                in Fig. 2b, is related to Ta by ≲; hence 𝑇a′ ⩽ 𝑇a , indicating that 𝑇a′
of each role (denoted by p, q, s, p′, . . . ∈ R) is described by local                       can safely substitute for 𝑇a .
session types (or simply session types), and protocol refinement                                AMS is undecidable in general [8, 27]. Together with its intrinsic
is formalised as a subtyping relation on these types. In particu-                            complexity, this renders the synthesis of asynchronous subtypes
lar, asynchronous multiparty subtyping (AMS) [22] offers a sound                             substantially non-trivial and inherently error-prone, giving rise to
and complete declarative characterisation of this relation, ensuring                         the main research question of this paper:
that subtypes – i.e. type-based protocol refinements – can safely
replace their supertypes while preserving all desirable communica-
                                                                                              How can subtypes be synthesised automatically under asynchro-
tion safety properties.
                                                                                              nous multiparty subtyping?
   The syntax of session types, ranging over 𝑇 ,𝑇 ′,𝑇𝑖 , . . ., is induc-
tively defined as follows:
       𝑇 F ⊕𝑖 ∈𝐼 p!mi .𝑇𝑖      &𝑖 ∈𝐼 p?mi .𝑇𝑖   𝜇t.𝑇     t end                               To tackle this challenge, we propose a system based on large lan-
                                                                                             guage models, described in the next section.
The constructs ⊕𝑖 ∈𝐼 p!mi .𝑇𝑖 and &𝑖 ∈𝐼 p?mi .𝑇𝑖 denote internal and
external choices, corresponding to sending (!) to or receiving (?)
from role p a label m𝑖 , respectively, where 𝐼 ≠ ∅ and the labels m𝑖 are                     3      Syntropy: A Framework for Asynchronous
pairwise distinct. The type end marks termination (omitted when                                     Subtype Synthesis
unambiguous), while 𝜇t.𝑇 introduces recursion with variable t.
                                                                                             Figure 4 illustrates the overall architecture of Syntropy, a frame-
   The behaviour of the aggregator a in the minimal federated
                                                                                             work for automatically synthesising asynchronous subtypes from
learning protocol is captured by
                                                                                             a source session type. It consists of two complementary modules:
             𝑇a = 𝜇t.p?updp .q?updq . ⊕{m!std.t, m!wtd.t},                                   Syntropy-Train, which trains large language models (LLMs) to
which is an alternative representation of the FSM in Fig. 3a.                                learn subtype generation patterns, and Syntropy-Gen, which lever-
   In AMS, besides covariance (fewer output options) (C1) and con-                           ages the trained model to produce diverse asynchronous subtypes
travariance (more input options) (C2), two forms of asynchronous                             guided by the asynchronous multiparty subtyping introduced in §2,
message reordering are allowed, whereby a subtype may anticipate                             thereby improving syntactic and semantic consistency.
input and output actions of the supertype:
R1. An input from p may be anticipated before a finite number of
                                                                                             3.1       Syntropy-Train: Learning Asynchronous
inputs not from p;
R2. An output to p may be anticipated before a finite number of                                        Subtype Generation
inputs (from any participant), and before outputs not directed to p.                         We fine-tune an open-source model (e.g. Qwen2.5-Coder-7B-Instruct
   To formalise AMS, session types are interpreted as (possibly                              [25]) using LoRA to generate subtypes conditioned on a given ses-
infinite) session trees. For instance, Fig. 2a presents the session tree                     sion type (the supertype). Since a supertype may correspond to an
                                                                                             unbounded number of subtypes under asynchronous subtyping, the
                                                                                                                          Yang Li, Ping Hou, and Nobuko Yoshida


           Table 1: Transformations encoded in prompts                                 guidance for subtype generation. RefA and RefB correspond to
                                                                                       the message reordering rules R1 and R2 in §2, respectively, while
   Rule       Prompt                  Example
                                                                                       RefOut and RefIn capture covariance (C1) and contravariance
   Identity   Subtype identical to    –                                                (C2). Additionally, Identity instantiates the reflexivity of subtyp-
              supertype.
                                                                                       ing, ensuring the existence of at least one valid subtype for every
   Unfold     Unfold recursion via    Valid                                            supertype, namely itself, and Unfold expands recursive types by
              substitution of the     REC_X_OPEN p?m; p!m′ ; REC_X_CLOSE ⇒
              recursive variable.     p?m; p!m′ ; REC_X_OPEN p?m; p!m′ ; REC_X_CLOSE   recursively substituting bound variables.
   RefA       Move recv p?m earlier   Valid p?m; q?m′ ;𝑇 ⩽ q?m′ ; p?m;𝑇
              when roles differ.      Invalid p?m; p?m′ ;𝑇 ⩽ p?m′ ; p?m;𝑇                 Example 3.1 (Multiple Transformations). Consider the supertype:
   RefB       Move send p!m earlier   Valid    p!m; q?m′ ;𝑇 ⩽ q?m′ ; p!m;𝑇                   𝑆 = p?m1 ; lbrace p!m2 ; q?m3 ; r?m4 ; end, p!m5 ; end rbrace
              across independent      Invalid p!m; p!m′ ;𝑇 ⩽ p!m′ ; p!m;𝑇              Under RefA, the subtype
              actions.                                                                      𝑇1 = p?m1 ; lbrace p!m2 ; r?m4 ; q?m3 ; end, p!m5 ; end rbrace
   RefOut     Internal choice:        Valid                                            is obtained, while applying RefOut yields 𝑇2 = p?m1 ; p!m5 .
              subtype offers fewer    lbrace p!m;𝑇1 rbrace ⩽
              labels.                 lbrace p!m;𝑇1 , p!m′ ;𝑇2 rbrace                     Note that 𝑇2 admits multiple transformations (e.g. RefA followed
                                      Invalid                                          by RefOut or directly via RefOut), whereas the generator may
                                      lbrace p!m;𝑇1 , p!m′ ;𝑇3 rbrace ⩽                assign only one as its heuristic label.
                                      lbrace p!m;𝑇1 , p!m′ ;𝑇2 rbrace

   RefIn      External choice:        Valid                                               Training sequences follow a standard format consisting of a sys-
              subtype accepts more    lbrace p?m1 ;𝑇1 , p?m2 ;𝑇2 , p?m3 ;𝑇3 rbrace ⩽
              labels.                 lbrace p?m1 ;𝑇1 , p?m2 ;𝑇2 rbrace                tem prompt, a user prompt, and the corresponding assistant output.
                                      Invalid                                          Prompt tokens are masked in the loss computation (i.e. excluded
                                      lbrace p?m1 ;𝑇1 rbrace ⩽                         from the objective), and loss is computed exclusively over the assis-
                                      lbrace p?m1 ;𝑇1 , p?m2 ;𝑇2 rbrace
                                                                                       tant outputs, corresponding to the generated subtype sequences.
                                                                                       This ensures that the theoretical context serves as conditioning
                                                                                       information rather than a target for imitation.
model is trained to capture structure-preserving transformations                          We adopt a weighted token-level loss, assigning a weight of 1.0 to
and generate diverse and structurally distinct, valid outputs.                         subtype tokens and 0.2 to auxiliary fields, including labels and the
   Our training data consists of session type specifications derived                   number of subtypes. Since both may originate from heterogeneous
from MPST literature [5–7, 15], augmented with synthetically gen-                      sources (e.g. benchmark data or synthetic generation) and do not
erated examples to improve coverage and diversity (see §4.1.1 for                      necessarily reflect canonical transformation patterns (see Thm. 3.1),
details). Each instance is of the form {𝑆, [{𝑇1, l1 }, . . . , {𝑇𝑛 , l𝑛 }], 𝑛},        they are treated as weak supervision signals. This encourages the
where 𝑆 denotes the supertype, 𝑛 the number of subtypes, and for                       model to prioritise learning structurally valid subtype sequences
each 𝑖 ≤ 𝑛, 𝑇𝑖 is a subtype with auxiliary (heuristic) label l𝑖 (e.g. indi-            while mitigating overfitting to auxiliary information.
cating one or multiple transformations). To accommodate variable-                         Finally, the model is fine-tuned using LoRA (rank 64, 𝛼 = 32,
length instances, we employ dynamic padding during training for                        dropout 0.05) with a maximum sequence length of 8k tokens. Train-
efficient batching with minimal overhead. This design exposes the                      ing is performed using AdamW with a cosine learning rate schedule
model to diverse transformation patterns, allowing it to generate                      and a warmup ratio of 0.1 for 3 epochs.
valid subtypes beyond a fixed set of explicitly defined rules.
   To facilitate training, we adapt the syntax of session types in §2
                                                                                       3.2    Syntropy-Gen: Synthesising Asynchronous
into a model-friendly representation:
                                                                                              Subtypes
          𝑇 F p!m;𝑇 p?m;𝑇 end
                                                                                       Syntropy-Gen generates asynchronous subtypes of a given super-
                     lbrace p!m1 ;𝑇1, . . . , p!m𝑛 ;𝑇𝑛 rbrace
                                                                                       type using the trained model. It supports two generation strate-
                     lbrace p?m1 ;𝑇1, . . . , p?m𝑛 ;𝑇𝑛 rbrace
                                                                                       gies: direct generation, where the LLM produces subtype candidates
                     REC_X_OPEN 𝑇 REC_X_CLOSE
                                                                                       guided by transformation rules adopted during training (§ 3.1),
Send and receive actions are explicitly represented in sequential                      and constrained generation, which introduces two-level monitoring
form as p!m;𝑇 and p?m;𝑇 , yielding a well-defined action structure                     mechanisms to enforce asynchronous subtyping constraints and
suitable for sequence modelling; internal and external choices use                     improve generation accuracy.
lbrace · rbrace; recursion is expressed by REC_X_OPEN 𝑇 , bind-
ing X over 𝑇 , with recursive occurrences encoded as REC_X_CLOSE,                      3.2.1 Direct Generation. In the direct generation approach, the
each denoting a continuation to the corresponding binder. These                        trained model is prompted to synthesise subtypes. Generation is
modifications preserve semantics while making structural bound-                        guided by transformation patterns – namely Identity, RefA, RefB,
aries explicit and reducing syntactic ambiguity.                                       RefIn, RefOut, and Unfold– described in § 3.1. These encour-
   For each training instance, we construct a prompt consisting of                     age the model to produce diverse candidates reflecting covariance,
(1) a theoretical context, including transformation descriptions (e.g.                 contravariance, and reordering.
Identity, RefA, RefB, RefIn, RefOut, and Unfold), and (2) the                             In this process, subtypes are derived from the supertype through
instance-specific input. The theoretical context is derived from the                   sequences of transformations, where successive applications ex-
prompt components summarised in Table 1 and provides structured                        pand the set of generated subtypes. Structured guidance is therefore
Specification-Guided Synthesis of Deadlock-Free Communication Protocol Refinements with Large Language Models


Algorithm 1 Constrained Generation with Two-Level Monitoring                         by a corresponding transition in T𝑆 ; for receive nodes, realisability
Input: supertype 𝑆, language model 𝑀, beam size 𝑘                                    is preserved provided that at least one branch of T′ is admitted by
Output: set of candidate subtypes Ω                                                  T𝑆 , possibly after unfolding recursion in T𝑆 to expose further input
  1: T𝑆 ← Parse(𝑆 )                                                                  actions. A prefix is rejected only when no completion of the current
  2: Beams ← { (𝜖, 0.0) }                                                            partial tree can satisfy the subtyping constraints (e.g. because the
  3: 𝐶 ← ∅                                                                           matched node of T𝑆 is end, i.e. the terminal node).
  4: for each decoding step do                                                          This monitor yields a prefix-level over-approximation: any ex-
  5:     for each (seq, score) ∈ Beams do                                            plored prefix that could lead to a valid subtype is preserved, while
  6:         for each (𝑡, 𝑝 ) ∈ Top2𝑘 (𝑀 ) do
                                                                                     some infeasible ones may also be retained. This property is relative
  7:             seq′ ← seq · 𝑡
  8:             T′ ← ParsePrefix(seq′ )
                                                                                     to beam search, which does not exhaustively enumerate all paths,
                ⊲ Level 1 (Derivative Check)                                         and to the generally infinite space of subtypes. In practice, Level
  9:             if T′ ≠ ⊥ and Feasible(T′ , T𝑆 ) then                               1 serves as an efficient per-token filter within beam search. When
 10:                 if 𝑡 = EOS then                                                 Feasible(T′, T𝑆 ) evaluates to false, the corresponding beam is
 11:                     Tf ← Parse(seq′ )                                           pruned immediately, eliminating infeasible regions of the search
                         ⊲ Level 2 (Widening-Based Fixpoint Check)                   space while preserving all potentially valid candidates.
 12:                     if SimCheck(Tf , T𝑆 ) then                                     Candidates that reach an end-of-sequence (EOS) token while
 13:                         Ω ← Ω ∪ {seq′ }                                         satisfying the Level 1 condition are forwarded to Level 2; those that
 14:                 else                                                            produce EOS otherwise are discarded, while all others continue
 15:                     𝐶 ← 𝐶 ∪ { (seq′ , 𝑠𝑐𝑜𝑟𝑒 + log 𝑝 ) }                         under Level 1 monitoring.
 16:     Beams ← Top𝑘 (𝐶 )
                                                                                     Level 2: Widening-Based Fixpoint Checker. When a candidate
                                                                                     reaches an EOS token, it is parsed into a complete session tree Tf
                                                                                     and submitted to a full subtype checker against the input supertype
provided for the LLM to generate pattern-compatible subtypes; how-
                                                                                     𝑆. The checker, implemented as a function SimCheck(Tf, T𝑆 ), is
ever, semantic correctness is not guaranteed as this naïve approach
                                                                                     built on a derivative-based decision procedure for asynchronous
relies entirely on the trained model.
                                                                                     subtyping over session trees [6].
3.2.2 Constrained Generation with Two-Level Monitoring. To im-
                                                                                         The procedure explores pairs of states from Tf and T𝑆 , maintain-
prove the semantic validity of generated subtypes while preserving
                                                                                     ing a worklist of obligations together with the information required
diversity, we employ constrained generation with two-level moni-
                                                                                     to avoid unsound revisiting of recursive configurations. Each obliga-
toring. Our approach is inspired by the asynchronous multiparty
                                                                                     tion is processed according to the structure of the current nodes. For
subtyping framework of [6], which we adapt to guide both prefix-
                                                                                     send nodes, the action exposed by Tf must be matched by a corre-
level filtering and final subtype verification within the constrained
                                                                                     sponding send derivative in T𝑆 ; for receive nodes, the checker re-
generation process.
                                                                                     quires that the branching structure of T𝑆 covers the inputs expected
   The input supertype is first parsed into a session tree, a tree-
                                                                                     by Tf , in accordance with the asynchronous subtyping conditions.
structured representation of a session type, as illustrated in §2. Beam
                                                                                     For terminal nodes, the check succeeds only if the corresponding
search then explores candidate subtypes, while the monitoring
                                                                                     configuration in T𝑆 admits termination.
stages enforce semantic constraints throughout generation.
                                                                                         To ensure termination in the presence of recursion, the checker
   We formalise the constrained generation procedure in Algo-
                                                                                     applies a widening operator at designated recursion points, follow-
rithm 1 and describe its main components below.
                                                                                     ing the abstract interpretation framework of [6]. Widening merges
Level 1: Token-level Derivative Check. Level 1 takes as input                        newly derived configurations with previously explored ones and
a decoded prefix together with the session tree T𝑆 of the input                      detects recurring patterns, thereby ensuring convergence of the
supertype 𝑆, and returns a Boolean indicating whether the prefix                     fixpoint computation. The procedure terminates when the work-
can still be extended to a valid subtype of 𝑆.                                       list is exhausted. Acceptance then indicates that the session type
   At each decoding step, the prefix is incrementally parsed into a                  represented by Tf is a valid subtype of 𝑆.
partially constructed session tree T′ , whose unresolved positions                       This checker accepts only candidates satisfying the asynchro-
are represented by Hole nodes. Since the MPST grammar is deter-                      nous subtyping relation, while some valid ones may be rejected.
ministic, each syntactically valid prefix corresponds to a unique
                                                                                     Correctness and Design Justification. Each output subtype is
partial tree, while Hole nodes denote subtrees to be completed. The
                                                                                     required to pass both a coarse prefix-level filter (Level 1) and a
monitor then performs a lightweight coinductive derivative-based
                                                                                     finer-grained final verification step (Level 2). This two-level design
compatibility check between T𝑆 and T′ to determine whether such
                                                                                     confines computationally expensive subtype checking to complete
an extension remains possible. Specifically, it evaluates a predicate
                                                                                     candidates, while lightweight prefix-level filtering eliminates infea-
Feasible(T′, T𝑆 ), which returns true if T′ admits at least one com-
                                                                                     sible prefixes early during search.
pletion whose corresponding session type is a valid subtype of 𝑆,
                                                                                        Level 2 operates as a conservative checker rather than a complete
and false otherwise.
                                                                                     decision procedure, reflecting the undecidability of asynchronous
   The feasibility check is based on derivative reasoning over ses-
                                                                                     subtyping: accepted candidates are valid, whereas rejection does
sion trees [6], applied to partial constructions. It establishes whether
                                                                                     not imply invalidity.
the behaviour induced by T′ is compatible with that represented by
T𝑆 . For send nodes, each branch generated in T′ must be supported
                                                                                                              Yang Li, Ping Hou, and Nobuko Yoshida


   Additionally, this design promotes output diversity by enabling       literature-derived supertypes (excluding original benchmark sub-
structurally distinct valid subtypes to emerge through different         types) and 97.97% from synthetic supertypes are accepted, indicat-
reorderings and interaction patterns permitted by asynchronous           ing high reliability.
subtyping. An overly restrictive validation step would limit the             Notably, the asynchronous subtyping algorithm in [6] is sound
search space explored by beam search and reduce the diversity of         but not complete, and the checker inherits this limitation. Conse-
generated subtypes. Overall, the two-level design balances semantic      quently, rejected subtypes may be deemed semantically valid. In
correctness with adequate exploration of the candidate space.            addition, practical constraints prevent the checker from handling
Implementation Details. We implement Algorithm 1 using beam              protocols beyond a certain size threshold (e.g. 701 grammar units),
search with beam size 𝑘. At each decoding step, each beam is ex-         such that even identity subtypes may be rejected.
panded using the top-2𝑘 tokens to compensate for pruning by the          Dataset Split. Supertypes are partitioned into training and test
Level 1 filter and preserve diversity. Candidate sequences are ranked    sets. The training set comprises 704 supertypes, yielding 10,800
by cumulative log-probability, and the top-𝑘 candidates are retained     (supertype, subtype) pairs (100 from literature-derived data and
after each step.                                                         604 from synthetic data). To balance learning signals, subtypes
                                                                         generated by different subtyping rules are approximately balanced.
                                                                         The test set consists of 100 representative supertypes (43 from
4     Evaluation                                                         literature-derived data and 57 from synthetic data) and is used as
To comprehensively assess Syntropy, we conduct a systematic              input for evaluation.
empirical evaluation addressing the following research questions.
                                                                         4.1.2 Foundation Model Selection. Qwen2.5-Coder-7B-Instruct [25]
RQ1. How well does Syntropy perform on existing benchmarks,
                                                                         serves as the primary foundation model for our experiments. Un-
and how does it generalise across different LLMs?
                                                                         like a raw pre-trained base model, it is instruction-tuned and opti-
RQ2. How does the performance of Syntropy vary across LLMs               mised for code and structured generation, making it well suited for
fine-tuned with LoRA using training sets of different sizes?             grammar-constrained protocol specifications such as MPST session
RQ3. How do the Syntropy-Train module, the BNF-style prompt,             types. The model balances generation quality and computational
and the two-level monitoring mechanism in Syntropy-Gen affect            efficiency, enabling systematic fine-tuning and controlled ablation
overall performance of Syntropy?                                         studies within reasonable resource constraints. For reproducibility,
RQ4. How robust is Syntropy under different subtyping trans-             a fixed random seed (seed = 42) is used across all experiments.
                                                                            To the best of our knowledge, no prior work has explored the use
formations, including covariance and contravariance (collectively
referred to as variance), as well as reordering?                         of large language models for type-based generation in the context
                                                                         of MPST. Existing research primarily focuses on formal methods
                                                                         rather than learning-based approaches. As a result, no directly
4.1    Experimental Setup                                                comparable baseline method is available.
4.1.1 Dataset Construction. The dataset is constructed by collect-       4.1.3 Evaluation Metrics. To comprehensively assess the perfor-
ing supertypes, which serve as inputs to the framework. Two sources      mance of Syntropy, a multi-metric evaluation framework is adopted,
are considered: literature-derived data and synthetic data.              targeting two main objectives: validity and diversity. Validity is eval-
   The literature-derived data (i.e. existing data) are collected from   uated at both syntactic and semantic levels, while diversity captures
prior work on Multiparty Session Types (MPST) [5–7, 15], covering        variations induced by subtyping transformations, including interac-
real-world communication protocols in domains such as finan-             tion reordering and variance. Semantic validity is further analysed
cial transactions, security, distributed coordination, and service       by transformation type. Five metrics are applied:
orchestration. These protocols provide realistic and semantically        (1) Syntactic Validity. The proportion of generated subtypes
meaningful specifications.                                                   that conform to the formal grammar specification, as verified
   To complement these examples and improve structural cover-                by a dedicated syntax checker.
age, synthetic supertypes are additionally constructed to capture        (2) Semantic Validity. The proportion of syntactically valid
a broader range of communication patterns and structures not                 subtypes accepted by the subtyping checker in [6], used as a
present in existing benchmarks, enabling evaluation across diverse           proxy for semantic correctness. Since the checker is sound but
protocols with varying levels of complexity.                                 not complete, this metric provides a lower bound.
Subtype Generation and Validation. To construct supervised               (3) Reordering vs. Variance Validity. The acceptance rates of
training data, pairs of the form (supertype, subtype) are created,           reordering-based and variance-based transformations under
defining the learning task. For synthetic supertypes, subtypes are           the subtyping checker.
generated through a heuristic procedure inspired by an asynchro-         (4) Transformation Rule Distribution. The frequency of sub-
nous subtyping algorithm [6] and validated using its checker.                typing transformation rules applied during subtype generation,
   For literature-derived supertypes, no canonical target subtype is         including Identity, RefA, RefB, RefIn, RefOut, and Unfold
available. Benchmark cases contain a limited number of reference             (see §3). A subtype with multiple transformations contributes
subtypes, typically one per supertype, providing only a partial view         to each corresponding rule count.
of the refinement space. To enrich the training data, additional         (5) Output Complexity. The average numbers of branches and
subtypes are generated using the same procedure and validated                message exchanges per subtype, reflecting the structural diver-
accordingly. Validation results show that 99.13% of subtypes from            sity of the generated outputs.
   Specification-Guided Synthesis of Deadlock-Free Communication Protocol Refinements with Large Language Models


                                             CodeLlama-7B           Qwen2.5-Coder-32B      Qwen2.5-Coder-7B                                                                                 602       9500      10800
                                             Qwen2.5-7B             StarCoder2-7B

                                  (a) Training Loss vs Tokens                                                                                                      (a) Training Loss vs Tokens
                                  (Window size 20)                                                                                                                 (Window size 5)
                                                                                                                                                              5
                             6
                                                                                                                                                              4
         Training Loss




                                                                                                                                          Training Loss
                             4                                                                                                                                3
                                                                                                                                                              2
                             2
                                                                                                                                                              1            0.121
                             0                                                                 4.2               5.5 5.9                                                                                            2.7            4.2
                                                                                                                                                              0
                                     0           1              2              3           4           5             6                                                0                1               2                  3   4
                                                                      Training Tokens                               ×106                                                                          Training Tokens                 ×106
                                  (b) Gradient Norm vs Tokens                                                                                                      (b) Gradient Norm vs Tokens
                                  (Window size 20)                                                                                                                 (Window size 5)
Gradient Norm (log scale)




                                                                                                                                 Gradient Norm (log scale)
                             6                                                                                                                                4
                             4
                             2                                                                                                                                2

                              1                                                                4.2               5.5
                            0.8                                                                                                                                1           0.121
                            0.6                                                                4.2                                                           0.8
                            0.4                                                                4.2                                                           0.6                                                    2.7
                                                                                                                        5.9                                                                                                        4.2
                                     0           1              2              3           4           5                6                                             0                1               2                  3   4
                                                                      Training Tokens                                  ×106                                                                       Training Tokens                 ×106
                                  (c) Learning Rate vs Tokens                                                                                                      (c) Learning Rate vs Tokens
                                  ×10 4                                                                                                                            ×10 4
                            2.0                                                                                                                              2.0
Learning Rate




                                                                                                                                 Learning Rate
                            1.5                                                                                                                              1.5
                            1.0                                                                                                                              1.0
                            0.5                                                                                                                              0.5
                                                                                                                                                                           0.121
                            0.0                                                                4.2               5.5 5.9                                     0.0                                                    2.7            4.2
                                     0           1              2              3           4           5             6                                                0                1               2                  3   4
                                                                      Training Tokens                               ×106                                                                          Training Tokens                 ×106


                                          Figure 5: Training dynamics across LLMs                                                                                     Figure 6: Training dynamics across data scales

                                                Table 2: Training cost across LLMs                                            rate is well tuned, exhibiting near-optimal behaviour. These results
                                   Model                                      Time (min)                      Tok (M)         suggest that Syntropy can be efficiently fine-tuned with moderate
                                   Qwen2.5-Coder-7B                                20.33                        4.2           computational cost.
                                   CodeLlama-7B                                    41.19                        5.9
                                   StarCoder2-7B                                   32.51                        5.5
                                   Qwen2.5-7B                                      32.55                        4.2           4.2                             RQ1. Benchmark Performance and
                                   Qwen2.5-Coder-32B                               61.61                        4.2
                                                                                                                                                              Cross-LLM Generalisation
                                                                                                                              We evaluate Syntropy on our primary foundation model, Qwen2.5-
   In addition, the comparison with frontier language models (§4.7),
                                                                                                                              Coder-7B, using metrics defined in §4.1.3, including syntactic and
   employs the coverage metric, defined as the proportion of super-
                                                                                                                              semantic validity, transformation rule distribution, and output com-
   types for which at least one subtype is generated. This metric mea-
                                                                                                                              plexity. We further assess its generalisation across additional LLMs,
   sures a model’s applicability across diverse protocol specifications.
                                                                                                                              analysing performance consistency and cross-model applicability.
  4.1.4 Training Configuration. Alongside Qwen2.5-Coder-7B-Ins-                                                               Fig. 7 presents the transformation rule distribution, while the re-
  truct, we fine-tune four additional open-source language models,                                                            maining metrics and computational cost are summarised in Table 3.
  CodeLlama-7B-Instruct [43], Qwen2.5-7B-Instruct [42], StarCoder2-
                                                                                                                              4.2.1 Results on the Primary Foundation Model. We compare two
  7B [29], and Qwen2.5-Coder-32B-Instruct [25], using the same Low-
                                                                                                                              approaches: direct generation and constrained generation (with Two-
  Rank Adaptation (LoRA) configuration with a rank of 64, a learning
                                                                                                                              Level Monitoring), introduced in §3.2, on the full test set.
  rate of 2 × 10−4 , and a batch size of 1. All models are instruction-
  tuned, except for StarCoder2-7B, for which no Instruct variant                                                              Direct Generation (w/o Two-Level Monitoring). Syntactic va-
  is publicly available. For brevity, the “-Instruct" suffix is omitted                                                       lidity reaches 85.0%, while semantic validity – evaluated on syn-
  throughout the remainder of the paper, including figures and tables.                                                        tactically valid outputs – is 60.4%, reflecting substantial semantic
      Training is conducted for 3 epochs, with costs reported in Table 2.                                                     errors despite high syntactic correctness. The transformation rule
  For Qwen2.5-Coder-7B, the average sequence length is 2, 027.5                                                               distribution indicates diverse application of subtyping rules, while
  tokens per sample and the training throughput is approximately                                                              each supertype yields approximately 5 subtypes per rule, with an
  3, 415 tokens per second.                                                                                                   average of 2 branching points and 8 message exchanges.
      Fig. 5 illustrates the training loss curves for all models, with                                                        Generation with Two-Level Monitoring. Syntactic validity in-
  steadily decreasing loss indicating stable optimisation dynamics.                                                           creases to 96.7%, while semantic validity among syntactically valid
  The gradient optimisation process remains stable, and the learning                                                          outputs reaches 99.2%, indicating near-perfect semantic correctness.
                                                                                                                                                                                                                                                      Yang Li, Ping Hou, and Nobuko Yoshida


                                                                                             Table 3: Performance and computational cost across LLMs
                                                                                                              No Monitoring                                                                                                            With Monitoring
                               Model                             Syn. (%)                Sem. (%)               Br. / Msg.                               Time (min) / Tok (M)              Syn. (%)             Sem. (%)                         Br. / Msg.            Time (min) / Tok (M)
                               Qwen2.5-Coder-7B                     85.0                   60.4                 1.83 / 8.07                                    335.69 / 8.6                  96.7                  99.2                           1.93 / 8.54                 1041.56 / 27.5
                               CodeLlama-7B                         72.6                   62.1                 1.87 / 7.18                                   520.15 / 10.4                  98.1                  99.5                           2.22 / 7.00                 1733.71 / 33.5
                               StarCoder2-7B                        85.8                   48.8                 2.04 / 6.67                                    733.60 / 9.1                  95.4                  95.7                           2.06 / 6.58                 1212.12 / 30.2
                               Qwen2.5-7B                           80.4                   60.9                 1.90 / 7.32                                    585.19 / 8.6                  97.0                  96.4                           2.01 / 7.22                 1606.01 / 27.7
                               Qwen2.5-Coder-32B                    81.6                   66.1                 1.92 / 6.66                                   1940.00 / 8.5                  96.3                  95.6                           1.99 / 7.23                 3867.99 / 27.4


                                                                                                  Rules                                                                                                Rules
                                                                                                                                        20000
                                                                                                   Identity                                                                                             RefA                                                                           98.1%                  99.2%
                                                                                                   RefA                                         2517                                                    RefB                         100
                       10000
                                                                                                   RefB                                                                                                 RefIn                              89.0%
                                                                                                                                        17500                                                                                                                                                                 96.7%
                                                                                                   RefIn                                                                                                RefOut                                            86.4%                        93.7%
                                                          4388                                     RefOut                                                                                               Identity                           80.7%
                                                                                                                                                                                                                                                          85.8%
                                                                                                   Unfold                                                                                               Unfold
                                                                                                                                                                                                                                      80                                                                      85.0%




                                                                                                                 Transformation Count
Transformation Count




                                                                                                                                        15000
                        8000                                                                                                                                                                                                                                                           81.9%
                                                                                                                                                                                                                                           79.8%          80.1%




                                                                                                                                                                                                                      Validity (%)
                                                                                                                                        12500
                                 2969                                                      2599                                                                                                                                       60
                        6000                                                                                                                    12328                                                                                                                                  61.8%                  60.4%
                                                          2408             2312                                                         10000

                                                                                                  2114
                                        1977                                                                                                                                                                                          40
                        4000
                                 2577          1835              1671             1603     2332
                                                                                                                                         7500

                                                                                                                                                                                                2969
                                                          2272             1965                   1731                                                                         2480                                                                       31.2%
                                      1701     1135 949        1159             1301
                                                                                                                                         5000
                                                                                                                                                                2465                            153
                                                                                                                                                                                                     1977                             20
                        2000     1052               568                                    1317                                                 2956                           139 1834         2577 216
                                               860 695     756 838         1067                1028                                                                            1909 261
                                 601 701                                        799
                                                                           524 331         611 439
                                                                                                                                         2500
                                                                                                                                                705 925
                                                                                                                                                                1495                1371        1052
                                                                                                                                                                                                       1701                                                 Syntax (w/o Two-Level)         Semantics (w/o Two-Level)
                                 576 427       562 379
                                                    231
                                                           980 496                             314
                                                                                           474 245                                                   237        924 393        982 768
                                                                                                                                                                                                601    701                                                  Syntax (Two-Level)             Semantics (Two-Level)
                                 153 263                   171 211         364
                                                                           153 213
                                                                                                                                                                                                                                           9.7%
                                      216      260
                                               150 251         217              214        149                                                  1320 797             432
                                                                                                                                                                     264       458
                                                                                                                                                                               458 362          576    427                             0
                           0                                                                                                                0                                       245                263                                   0             602                          9500                  10800
                                  w/o w/       w/o w/      w/o w/          w/o w/          w/o w/                                               w/o
                               Qwen2.5-Coder- CodeLlama- StarCoder2-
                                    7B            7B         7B
                                                                           Qwen2.5- Qwen2.5-Coder-
                                                                             7B         32B
                                                                                                                                                       0 w/     w/o
                                                                                                                                                                  602w/        w/o
                                                                                                                                                                                 9500w/         w/o    w/
                                                                                                                                                                                                    10800                                                         Training Pairs


                                                                                                                                (a) Transformation distribution across data scales                                                                 (b) Validity across data scales
   Figure 7: Transformation distribution across
   LLMs                                                                                                                                                  Figure 8: Transformation distribution and validity across data scales


   This improvement from 60.4% to 99.2% demonstrates the effective-                                                                                                           Table 4: Complexity and computational cost across data scales
   ness of the monitoring-based approach, while the transformation                                                                                                                                   No Monitoring                                                 With Monitoring
                                                                                                                                                                               Pairs
   rule distribution and output complexity remain comparable.                                                                                                                             Br. / Msg. Time (min) / Tok (M) Br. / Msg. Time (min) / Tok (M)
   Overhead Analysis. We analyse the computational overhead in-                                                                                                                0     1.76 / 6.78                   1578.16 / 8.5                        2.03 / 8.06                  580.65 / 27.3
   troduced by Two-Level Monitoring. Enabling monitoring increases                                                                                                             602   1.95 / 5.86                    338.48 / 8.5                        2.35 / 6.73                  1120.37 / 27.1
                                                                                                                                                                               9500 2.01 / 8.12                     486.02 / 8.5                        2.13 / 7.66                  1575.50 / 27.3
   token consumption from 8.6M to 27.5M (approximately 3×), mainly                                                                                                             10800 1.83 / 8.06                    335.69 / 8.6                        1.93 / 8.54                  1041.56 / 27.5
   due to additional validation and constraint enforcement. While
   runtime is reported in Table 3, it is not used as the primary cost                                                                                                      modifying the framework. StarCoder2-7B shows a more imbal-
   metric due to its sensitivity to GPU allocation variability in the                                                                                                      anced distribution compared to other models, which is qualitatively
   HTC cluster; token-level overhead serves as the basis for subse-                                                                                                        consistent with the slower convergence reflected in the training
   quent analysis.                                                                                                                                                         dynamics (Fig. 5).
      Despite this additional cost, the monitoring mechanism sub-                                                                                                             Model-level overhead remains consistent, exhibiting trends sim-
   stantially improves semantic validity, indicating a clear trade-off                                                                                                     ilar to those observed for the primary foundation model. This sug-
   between efficiency and correctness. Direct generation is more suit-                                                                                                     gests that the computational characteristics of Syntropy scale
   able for efficiency-oriented scenarios, whereas monitoring-based                                                                                                        predictably across different LLM architectures.
   generation is preferable for correctness-critical applications.                                                                                                         Answer to RQ1. Syntropy achieves strong performance on bench-
                                                                                                                                                                           mark datasets and generalises effectively across different LLMs.
   4.2.2 Cross-LLM Generalisation. We evaluate Syntropy across                                                                                                             Two-Level Monitoring significantly improves semantic validity
   multiple LLMs on the full test set, including CodeLlama-7B,                                                                                                             while maintaining comparable generation behaviour and predictable
   StarCoder2-7B, Qwen2.5-7B, and Qwen2.5-Coder-32B. As shown                                                                                                              computational overhead.
   in Table 3, syntactic validity remains consistently high (95.4%–
   98.1%), while semantic validity reaches up to 99.5%, demonstrating
                                                                                                                                                                           4.3       RQ2. Impact of Training Data Scale on
   robust generalisation across models. These results indicate that                                                                                                                  Performance
   Syntropy is not tied to a specific architecture and exhibits strong                                                                                                     To study how training data scale affects performance, we fine-tune
   cross-model applicability.                                                                                                                                              models with LoRA on increasing numbers of (supertype, subtype)
      The transformation rule distribution (Fig. 7) is generally consis-                                                                                                   pairs. Due to variability in subtype generation, we approximate
   tent, with some variations among models. In particular, CodeLlama-                                                                                                      three regimes (small, large, and near-saturation) using 602, 9, 500,
   7B exhibits limited diversity under default decoding settings, fail-                                                                                                    and 10, 800 pairs, respectively, along with a no-fine-tuning baseline.
   ing to generate certain transformations (e.g. RefA and RefB). To                                                                                                           Fig. 6 reveals that training data size significantly affects con-
   address this, we adopt stochastic beam search with temperature                                                                                                          vergence behaviour, while transformation rule distributions and
   scaling (𝑇 = 1.2), which restores transformation diversity without                                                                                                      both syntactic and semantic validity vary accordingly, as shown in
  Specification-Guided Synthesis of Deadlock-Free Communication Protocol Refinements with Large Language Models


                              Syntax Validity                                         Semantics Validity                       Transformation Distribution                                Avg Branches                                   Avg Messages
                 100 96.7%                                                 100 99.2% 93.9%                             8000        Identity                                3.0
                                91.5%                                                             89.0%                            RefA                                                    2.67                             10             9.29
                                         80.7% 85.0%                                                                   7000        RefB
                                                                                                                                   RefIn                    2969           2.5
                                                                                                                                                                                                                                  8.54              8.06     8.07
                 80                                                        80                                                      RefOut                                                                                    8
                                                                                                                       6000
Percentage (%)




                                                          Percentage (%)
                                                                                                                                   Unfold
                                                                                                                                                                                  1.93              2.03
                                                                                                           60.4%       5000                                                2.0                               1.83
                 60                                                        60




                                                                                                                   Count




                                                                                                                                                                   Count




                                                                                                                                                                                                                    Count
                                                                                                                                1977          2172                                                                           6
                                                                                                                       4000                                 2577           1.5
                 40                                                        40                                          3000                                                                                                  4
                                                                                                                                1701          1669                         1.0
                                                                                                                       2000                           925   1052
                 20                                                        20                                                    701                                       0.5                                               2
                                                                                                                       1000                   942     797   601
                                                                                                                                 427          239           576
                                                                                                                                 263
                                                                                                                                 216          274     237   153
                  0                                                         0                                              0                                               0.0                                               0
                      Full /o Prompt e-tuning onitoring                         Full/o Prompt e-tuningonitoring                Full/o Prompt e-tuningonitoring                   Full/o Prompt e-tuningonitoring                 Full/o Prompt e-tuningonitoring
                        w w/o Fin w/o M                                          w w/o Fin w/o M                                w w/o Fin w/o M                                   w w/o Fin w/o M                                 w w/o Fin w/o M

                                                                                      Figure 9: Ablation results across metrics on Qwen2.5-Coder-7B


  Fig. 8a and Fig. 8b. Additional metrics and computational costs are                                                                                4.4    RQ3. Ablation Study of Syntropy
  reported in Table 4.                                                                                                                                      Components
 No fine-tuning (0 pairs). Without fine-tuning, semantic valid-                                                                                      To understand the contribution of each component in Syntropy, we
 ity is low (9.7%), and generated subtypes are structurally simple,                                                                                  conduct ablation studies on Qwen2.5-Coder-7B using three variants:
 with limited transformation diversity and few reordering cases.                                                                                     w/o Prompt, w/o Fine-tuning, and w/o Two-Level Monitoring. As the
 Two-Level Monitoring improves validity substantially but does not                                                                                   impact of fine-tuning has been analysed in RQ2 (§ 4.3), we focus
 address the lack of structural diversity, highlighting the need for                                                                                 on prompting and monitoring. The results of the ablation study on
 fine-tuning to generate valid and diverse subtypes.                                                                                                 validity, transformation rule distribution, and output complexity
  Small-scale (602 pairs). Fine-tuning yields significant perfor-                                                                                    are illustrated in Fig. 9.
  mance gains. Pre-monitoring semantic validity increases from 9.7%                                                                                  w/o Two-Level Monitoring. This configuration exhibits the most
  to 31.2%, while Two-Level Monitoring maintains validity at 85–90%.                                                                                 severe degradation. Semantic validity drops to 60.4%, considerably
  Structural diversity also improves, with more frequent complex                                                                                     lower than all other configurations (≥ 85%), highlighting that Two-
  transformations. These results indicate that even limited training                                                                                 Level Monitoring is essential for ensuring correctness.
  data provides meaningful improvements, although performance
                                                                                                                                                     w/o Prompt. Removing the BNF-style prompt does not substan-
  remains far from saturation.
                                                                                                                                                     tially degrade validity, as both syntactic and semantic validity re-
  Large-scale (9,500 pairs). At this scale, performance reaches a                                                                                    main above 90%. However, semantic validity decreases from 99.2%
  near-optimal level. Pre-monitoring semantic validity approximately                                                                                 to 93.9%, indicating that prompting contributes to achieving near-
  doubles relative to the 602-pair setting, reaching 98% after Two-                                                                                  perfect correctness. In contrast, structural diversity decreases more
  Level Monitoring. Structural diversity is well balanced, with broader                                                                              noticeably, with fewer reordering transformations, highlighting the
  coverage of complex transformations. This is consistent with the                                                                                   importance of prompting for balanced transformation coverage.
  model having largely converged, with limited scope for further
                                                                                                                                                     Full Syntropy framework. The complete system achieves the
  improvement.
                                                                                                                                                     best overall performance, with 99.2% semantic validity and balanced
 Near-saturation (10,800 pairs). Increasing the training size                                                                                        structural diversity.
 from 9,500 to 10,800 pairs yields only marginal changes (approxi-
                                                                                                                                                     Answer to RQ3. The components serve complementary roles: prompt-
 mately 1%), indicating that performance has effectively saturated.
                                                                                                                                                     ing enhances structural diversity, and Two-Level Monitoring en-
 This implies diminishing returns from further scaling and confirms
                                                                                                                                                     sures correctness. Combined with fine-tuning (RQ2), the full frame-
 that the model has reached a near-saturation regime.
                                                                                                                                                     work achieves the best overall performance. Removing any compo-
 Computational Cost. As shown in Table 4, computational cost                                                                                         nent degrades performance, with monitoring being most critical
 exhibits minimal variation as the training dataset scales from 602                                                                                  for validity and prompting for diversity.
 to 10,800 pairs, incurring only minor differences in token consump-
 tion. This shows that data scaling has limited impact on efficiency.
 The relative overhead introduced by Two-Level Monitoring re-                                                                                        4.5    RQ4. Robustness under Reordering and
 mains consistent with the analysis in § 4.2.1. Overall, the frame-                                                                                         Variance Transformations
 work demonstrates stable and predictable computational behaviour
 across different scales.                                                                                                                            To evaluate the robustness of Syntropy under different subtyping
                                                                                                                                                     transformations, we analyse performance across two core cate-
  Answer to RQ2. Performance improves rapidly as training data
                                                                                                                                                     gories: reordering (RefA and RefB) and variance (RefIn and Re-
  increases, but saturates around 9,500 pairs, beyond which additional
                                                                                                                                                     fOut). As shown in Table 5, both achieve consistently high semantic
  data yields only marginal gains.
                                                                                                                                                     validity across all evaluated models (89.8%–100%), demonstrating
                                                                                                                                                     strong robustness even for structurally complex reordering.
                                                                                                                                                        However, the generated subtype distribution is not balanced,
                                                                                                                                                     with variance cases consistently outnumbering reordering ones. To
                                                                                                                                                     investigate this, we introduce two representative structural cases:
                                                                                                                                  Yang Li, Ping Hou, and Nobuko Yoshida


                                            Table 5: Semantic validity of diverse transformations across LLMs
                                                        Reordering                                                          Variance
       Model                          RefA                  RefB                     Avg.               RefIn               RefOut                  Avg.
       Qwen2.5-Coder-7B           261/263 (99.2%)       421/427 (98.6%)      673/681 (98.8%)        681/701 (97.1%)     1649/1701 (96.9%)     2167/2234 (97.0%)
       CodeLlama-7B               230/231 (99.6%)       377/379 (99.5%)      606/609 (99.5%)        683/695 (98.3%)      554/568 (97.5%)      1100/1125 (97.8%)
       StarCoder2-7B              210/211 (99.5%)       485/496 (97.8%)      682/694 (98.3%)        773/838 (92.2%)     1010/1159 (87.1%)     1695/1887 (89.8%)
       Qwen2.5-7B                 213/213 (100%)        331/331 (100%)       544/544( 100%)         739/799 (92.5%)     1209/1301 (92.9%)     1789/1939 (92.3%)
       Qwen2.5-Coder-32B         314/314 (100.0%)       433/439 (98.6%)      744/750 (99.2%)        973/1028 (94.6%)    1612/1731 (93.1%)     2378/2545 (93.4%)


Table 6: Transformation preferences across two structural cases on                          of the subtyping checker used for validation [6]. While accepted
Qwen2.5-Coder-7B                                                                            subtypes are guaranteed to be correct, rejected cases cannot be con-
                  Reordering                              Variance                          clusively deemed incorrect, introducing uncertainty in evaluating
Case    RefA         RefB          Avg.       RefIn       RefOut          Avg.              borderline cases.
𝑇1 14/15 (93.3%) 4/4 (100%) 18/19 (94.7%) 13/13 (100%) 32/33 (97.0%) 39/40 (97.5%)          Threats to Validity. The validity and diversity of generated sub-
𝑇1↬ 19/19 (100%) 8/8 (100%) 27/27 (100%) 16/16 (100%) 35/35 (100%) 46/46 (100%)             types depend on the characteristics of the underlying LLM. Al-
𝑇2       0      14/14 (100%) 14/14 (100%) 12/12 (100%) 38/38 (100%) 41/41(100%)
                                                                                            though fine-tuning improves performance, generation quality re-
 𝑇1 = REC_X_OPEN p?updp ; q?updq ; lbrace m!std; REC_X_CLOSE,                               mains influenced by the choice of model and may vary under dif-
                                          m!wtd; REC_X_CLOSE rbrace                         ferent configurations.
 𝑇2 = REC_X_OPEN q?updq ; lbrace m!std; REC_X_CLOSE,
                                                                                               In addition, our evaluation focuses exclusively on subtype gen-
                                 m!wtd; REC_X_CLOSE rbrace                                  eration. While consistent performance is observed across multiple
                                                                                            LLMs, we do not assess generalisation to other generation tasks.
and generate their subtypes to analyse the resulting transforma-
                                                                                            Extending the approach beyond subtyping remains an important
tion distribution on Qwen2.5-Coder-7B. In addition, we consider a
                                                                                            direction for future work.
strengthening reordering setting applied to 𝑇1 , where constraints are
introduced to encourage reordering. The results are summarised
in Table 6, where 𝑇1↬ denotes increased reordering.                                         4.7    Comparison with Frontier Language Models
   For 𝑇1 , both RefA and RefB are allowed, yet the generated sub-                          To assess the necessity of a task-specific framework in the presence
types favour RefA, indicating a bias toward transformations aligned                         of modern frontier language models, we compare Syntropy with
with the prefix structure. For 𝑇2 , removing the initial receive ac-                        GPT-5.5 [37] and DeepSeek-V4-Pro [16], representative leading
tion enables RefB-style reordering; consequently, RefA disappears                           proprietary and open-weight models, respectively, in terms of both
while RefB increases, confirming that both reordering types are                             effectiveness and computational cost.
supported when structurally enabled.                                                           Both models are evaluated on the benchmark using the same
   Across both cases, variance transformations exceed reordering                            prompts as the fine-tuned models under their default inference
by approximately two to three times, suggesting that they are easier                        configurations. Table 7 summarises the results, including coverage.
to produce. While strengthening reordering constraints increases
                                                                                            Performance Analysis. The key difference between frontier and
their proportion, variance remains dominant, indicating a persistent
                                                                                            fine-tuned models lies in their ability to generate subtypes across
preference for simpler patterns.
                                                                                            the benchmark. As shown in Table 7, GPT-5.5 and DeepSeek-V4-
Answer to RQ4. Syntropy maintains high semantic validity across                             Pro cover 18% and 4% of benchmark supertypes, respectively. In
both reordering and variance transformations, demonstrating strong                          contrast, all five fine-tuned models provide full coverage.
robustness. However, the model exhibits a preference for simpler                               Among the generated outputs, GPT-5.5 and DeepSeek-V4-Pro ex-
(variance) transformations, while reordering can be partially steered                       hibit syntactic and semantic validity broadly consistent with those
through constraints.                                                                        of the fine-tuned models (Table 3). GPT-5.5 achieves 94.59% syntac-
                                                                                            tic validity and 99.29% semantic validity, while DeepSeek-V4-Pro
4.6     Error Analysis and Threats to Validity                                              records 100.00% and 95.65%, respectively. GPT-5.5 additionally pro-
Syntax Validity. LLMs occasionally produce syntactic errors,                                duces subtypes spanning all transformation categories and shows
including mismatched parentheses, incomplete expressions (e.g.,                             comparable branch and message counts. However, these metrics
ending with < or ;), and unbound recursive variables. These errors                          need to be interpreted in the context of their substantially lower
reduce syntactic validity and are not fully eliminated by syntax                            coverage. We further observe an overall tendency for covered super-
normalisation during fine-tuning. This suggests that LLMs may be                            types to involve fewer message exchanges and simpler structures.
less reliable when handling mathematically structured formats com-                          Cost Analysis. Based on the results from Tables 2, 3 and 7, prompt-
pared to more common code-like syntax. Rather than introducing                              ing frontier models requires fewer tokens and less time than the
dedicated syntax correction techniques, we mitigate these errors                            combined cost of fine-tuning and evaluating the models used in this
indirectly: the two-level monitoring framework filters many invalid                         work. For the latter, the figures include both model training (Table 2)
outputs, while multiple generations ensure a sufficient number of                           and benchmark generation (Table 3), with training accounting for
syntactically valid subtypes.                                                               a modest fraction of the overall expenditure. Following §4.2, token
Semantic Validity. Ensuring semantic validity is challenging due                            consumption remains the primary basis for comparison. The lower
to the undecidable nature of subtyping and the incompleteness                               token usage of frontier models is partly attributable to their limited
Specification-Guided Synthesis of Deadlock-Free Communication Protocol Refinements with Large Language Models


                                    Table 7: Performance and computational cost of prompting frontier models
                    Supertype-Level                                           Generated Subtypes                                                Cost
 Model                   Cov. (%)       Syn. (%)   Sem. (%)    Br. / Msg.    RefA   RefB     RefIn     RefOut   Unfold   Identity    Time (min)        Tok (M)
 GPT-5.5                    18           94.59       99.29     1.78 / 7.30    18       2       49         13      50         52         59.47            0.5
 DeepSeek-V4-Pro             4           100.00      95.65     1.00 / 5.35     4       0       11          0       0         16         41.47            0.5



coverage and significantly fewer subtype candidates per covered su-                  has mainly been studied in the context of constrained decoding.
pertype, averaging 8.22 and 5.75 for GPT-5.5 and DeepSeek-V4-Pro,                    Syntactic constraints, particularly grammar-constrained decoding
respectively, compared with 19.20–35.30 for the fine-tuned models.                   based on context-free grammars, have been extensively explored [3,
Discussion. Taken together, these findings indicate that, although                   4, 20, 38, 40, 47, 49, 51]. Simple context-sensitive features, such as
frontier models can generate valid subtype candidates at lower                       indentation in Python and scope markers in Go, have also been
computational cost, they do not provide sufficient coverage for com-                 incorporated [33, 47].
prehensive subtype generation. The effectiveness gains achieved by                      In addition to syntactic constraints, recent work has investigated
the fine-tuned Syntropy models, while maintaining high validity,                     the enforcement of semantic constraints, such as type safety [35, 36],
therefore justify the need for this work.                                            as well as more general mechanisms, including monitors [1], which
                                                                                     enable user-defined constraint checking during decoding. These
5    Related Work                                                                    approaches inspire the design of our two-level monitoring strat-
                                                                                     egy within constrained generation to enforce semantic correctness
Asynchronous Subtyping. Asynchronous subtyping was initially
                                                                                     constraints of generated protocol refinements in Syntropy.
shown to be sound and complete for binary session types (i.e. in-
volving two participants) in [11]. It was subsequently extended to                   LLM-based Communication Protocols. The automatic gener-
multiparty session types [22], with its formalisation and correct-                   ation of communication protocols among LLM agents has been
ness proof mechanised in Rocq [18]. For a comprehensive survey                       explored, where emergent communication frameworks show that
of asynchronous subtyping, see [10].                                                 shared protocols can arise from decentralised interactions [46],
   Due to the undecidability of asynchronous subtyping [8, 27],                      while alternative schemes, such as embedding-based protocols, en-
even in the binary case, existing work focuses on developing sound,                  able richer information exchange [39]. In addition, LLMs have been
though necessarily incomplete, algorithms for subtyping verifica-                    used to dynamically construct or adapt communication protocols
tion. Approaches such as [5, 7] provide practical checking proce-                    at runtime [32, 41]. These approaches shift from static, human-
dures for binary session types, while [6, 15] extend these ideas to                  designed protocols toward adaptive and learned communication
multiparty settings based on a formal definition of asynchronous                     paradigms; however, their underlying motivation differs from ours
multiparty subtyping [22], which precisely characterises safety-                     and is not grounded in formal specifications.
preserving type refinements, thereby guaranteeing correctness, in-
cluding deadlock freedom. Benchmarks from [5–7, 15] are adopted
                                                                                     6     Conclusion
in the training and evaluation datasets of our framework, while the                  In this paper, we explored how large language models can be ex-
approach and checker in [6] serve as the basis for our constrained                   tended beyond syntactic code generation to provide behavioural
generation and semantic validity checking.                                           guarantees in communication protocols. By embedding formal con-
   However, the automatic generation of valid asynchronous sub-                      straints into the LLM-based generation process, the proposed frame-
types remains unexplored in existing work.                                           work Syntropy enables the construction of protocol refinements
LLMs for Formal Specification. Transformer-based language                            that preserve properties such as deadlock freedom. The results
models [48], such as Qwen-Coder [25], CodeLlama [43], and Star-                      demonstrate that integrating generative models with formal specifi-
Coder [29], have substantially advanced natural language tasks                       cation and verification techniques facilitates correctness-preserving
such as summarisation [13], code generation [9], and program syn-                    synthesis and highlights promising directions for applying LLMs
thesis [2]. Leveraging these strengths, a line of work [12, 14, 19,                  to safety-critical software engineering tasks.
31, 34, 45, 53, 54] investigates the translation of natural language                    In future work, we intend to extend the approach to more general
into formal specifications, particularly temporal logic, to reduce the               formalisms, including choreographies, contract-based models, and
effort and error-proneness. Beyond specification generation, recent                  temporal logics. We further plan to investigate verifier-guided iter-
studies explore improving the reliability of LLM-based program                       ative refinement techniques and the integration of Syntropy into
synthesis by integrating formal reasoning techniques [30, 50], in-                   practical development workflows, including protocol evolution, in-
cluding theorem proving, static analysis, and deductive verification.                teractive design assistance, and verification-aware code generation
   These efforts demonstrate the complementary strengths of LLMs                     within existing toolchains.
and formal methods in supporting the development of trustworthy
software systems, motivating our exploration of integrating LLMs
with the formal specification and verification of communication
protocols.
Constrained Generation with LLMs. Constrained generation
aims to ensure that LLM outputs satisfy specified constraints and
                                                                                                                                         Yang Li, Ping Hou, and Nobuko Yoshida


Data Availability Statement                                                               [11] Tzu-Chun Chen, Mariangiola Dezani-Ciancaglini, Alceste Scalas, and Nobuko
                                                                                               Yoshida. 2017. On the Preciseness of Subtyping in Session Types. Logical Methods
The artifact supporting this work, including the implementation of                             in Computer Science 13, 2 (2017). doi:10.23638/LMCS-13(2:12)2017
Syntropy, trained models, evaluation data, and evaluations of fron-                       [12] Yongchao Chen, Rujul Gandhi, Yang Zhang, and Chuchu Fan. 2023. NL2TL: Trans-
                                                                                               forming Natural Languages to Temporal Logics using Large Language Models.
tier language models, is publicly available via DOI: https://doi.org/                          In Proceedings of the 2023 Conference on Empirical Methods in Natural Language
10.5281/zenodo.21737877. The repository contains all source code,                              Processing, Houda Bouamor, Juan Pino, and Kalika Bali (Eds.). Association for
datasets, and instructions required to reproduce the experiments                               Computational Linguistics, Singapore, 15880–15903. doi:10.18653/v1/2023.emnlp-
                                                                                               main.985
and results reported in this paper.                                                       [13] Bharath Chintagunta, Namit Katariya, Xavier Amatriain, and Anitha Kannan.
                                                                                               2021. Medically Aware GPT-3 as a Data Generator for Medical Dialogue Sum-
                                                                                               marization. In Proceedings of the 6th Machine Learning for Healthcare Conference
                                                                                               (Proceedings of Machine Learning Research, Vol. 149), Ken Jung, Serena Yeung,
References                                                                                     Mark Sendak, Michael Sjoding, and Rajesh Ranganath (Eds.). PMLR, 354–372.
 [1] Lakshya A. Agrawal, Aditya Kanade, Navin Goyal, Shuvendu K. Lahiri, and                   https://proceedings.mlr.press/v149/chintagunta21a.html
     Sriram K. Rajamani. 2023. Monitor-Guided Decoding of Code LMs with                   [14] Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, and
     Static Analysis of Repository Context. In Advances in Neural Information                  Caroline Trippel. 2023. nl2spec: Interactively Translating Unstructured Natural
     Processing Systems 36: Annual Conference on Neural Information Processing                 Language to Temporal Logics with Large Language Models. In Computer Aided
     Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023,                 Verification - 35th International Conference, CAV 2023, Paris, France, July 17-
     Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt,                     22, 2023, Proceedings, Part II (Lecture Notes in Computer Science, Vol. 13965),
     and Sergey Levine (Eds.). http://papers.nips.cc/paper_files/paper/2023/hash/              Constantin Enea and Akash Lal (Eds.). Springer, 383–396. doi:10.1007/978-3-031-
     662b1774ba8845fc1fa3d1fc0177ceeb-Abstract-Conference.html                                 37703-7_18
 [2] Jacob Austin, Augustus Odena, Maxwell I. Nye, Maarten Bosma, Henryk                  [15] Zak Cutner, Nobuko Yoshida, and Martin Vassor. 2022. Deadlock-free asynchro-
     Michalewski, David Dohan, Ellen Jiang, Carrie J. Cai, Michael Terry, Quoc V.              nous message reordering in rust with multiparty session types. In PPoPP ’22: 27th
     Le, and Charles Sutton. 2021. Program Synthesis with Large Language Models.               ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming,
     CoRR abs/2108.07732 (2021). arXiv:2108.07732 https://arxiv.org/abs/2108.07732             Seoul, Republic of Korea, April 2 - 6, 2022, Jaejin Lee, Kunal Agrawal, and Michael F.
 [3] Luca Beurer-Kellner, Marc Fischer, and Martin T. Vechev. 2023. Prompting                  Spear (Eds.). ACM, 246–261. doi:10.1145/3503221.3508404
     Is Programming: A Query Language for Large Language Models. Proc. ACM                [16] DeepSeek-AI. 2026. DeepSeek-V4: Towards Highly Efficient Million-Token Con-
     Program. Lang. 7, PLDI (2023), 1946–1969. doi:10.1145/3591300                             text Intelligence. arXiv:2606.19348 https://arxiv.org/abs/2606.19348
 [4] Luca Beurer-Kellner, Marc Fischer, and Martin T. Vechev. 2024. Guiding LLMs          [17] Nicola Dragoni, Saverio Giallorenzo, Alberto Lluch-Lafuente, Manuel Mazzara,
     The Right Way: Fast, Non-Invasive Constrained Generation. In Forty-first Inter-           Fabrizio Montesi, Ruslan Mustafin, and Larisa Safina. 2017. Microservices: Yester-
     national Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27,          day, Today, and Tomorrow. In Present and Ulterior Software Engineering, Manuel
     2024 (Proceedings of Machine Learning Research, Vol. 235), Ruslan Salakhutdi-             Mazzara and Bertrand Meyer (Eds.). Springer, 195–216. doi:10.1007/978-3-319-
     nov, Zico Kolter, Katherine A. Heller, Adrian Weller, Nuria Oliver, Jonathan              67425-4_12
     Scarlett, and Felix Berkenkamp (Eds.). PMLR / OpenReview.net, 3658–3673.             [18] Burak Ekici and Nobuko Yoshida. 2026. Formalising Asynchronous Session
     https://proceedings.mlr.press/v235/beurer-kellner24a.html                                 Subtyping. ACM Trans. Comput. Logic 27, 3, Article 18 (June 2026), 45 pages.
 [5] Laura Bocchi, Andy King, and Maurizio Murgia. 2024. Asynchronous Subtyping                doi:10.1145/3815176
     by Trace Relaxation. In Tools and Algorithms for the Construction and Analysis of    [19] Francesco Fuggitti and Tathagata Chakraborti. 2023. NL2LTL - a Python Package
     Systems - 30th International Conference, TACAS 2024, Held as Part of the European         for Converting Natural Language (NL) Instructions to Linear Temporal Logic
     Joint Conferences on Theory and Practice of Software, ETAPS 2024, Luxembourg              (LTL) Formulas. In Thirty-Seventh AAAI Conference on Artificial Intelligence, AAAI
     City, Luxembourg, April 6-11, 2024, Proceedings, Part I (Lecture Notes in Computer        2023, Thirty-Fifth Conference on Innovative Applications of Artificial Intelligence,
     Science, Vol. 14570), Bernd Finkbeiner and Laura Kovács (Eds.). Springer, 207–226.        IAAI 2023, Thirteenth Symposium on Educational Advances in Artificial Intelligence,
     doi:10.1007/978-3-031-57246-3_12                                                          EAAI 2023, Washington, DC, USA, February 7-14, 2023, Brian Williams, Yiling
 [6] Laura Bocchi, Andy King, Maurizio Murgia, and Simon Thompson. 2025. Abstract              Chen, and Jennifer Neville (Eds.). AAAI Press, 16428–16430. doi:10.1609/AAAI.
     Subtyping for Asynchronous Multiparty Sessions. In 36th International Confer-             V37I13.27068
     ence on Concurrency Theory, CONCUR 2025, Aarhus, Denmark, August 26-29, 2025         [20] Saibo Geng, Martin Josifoski, Maxime Peyrard, and Robert West. 2023. Grammar-
     (LIPIcs, Vol. 348), Patricia Bouyer and Jaco van de Pol (Eds.). Schloss Dagstuhl -        Constrained Decoding for Structured NLP Tasks without Finetuning. In Proceed-
     Leibniz-Zentrum für Informatik, 10:1–10:19. doi:10.4230/LIPICS.CONCUR.2025.               ings of the 2023 Conference on Empirical Methods in Natural Language Process-
     10                                                                                        ing, EMNLP 2023, Singapore, December 6-10, 2023, Houda Bouamor, Juan Pino,
 [7] Mario Bravetti, Marco Carbone, Julien Lange, Nobuko Yoshida, and Gianluigi                and Kalika Bali (Eds.). Association for Computational Linguistics, 10932–10952.
     Zavattaro. 2019. A Sound Algorithm for Asynchronous Session Subtyping. In                 doi:10.18653/V1/2023.EMNLP-MAIN.674
     30th International Conference on Concurrency Theory, CONCUR 2019, Amsterdam,         [21] Silvia Ghilezan, Svetlana Jaksic, Jovanka Pantovic, Alceste Scalas, and Nobuko
     The Netherlands, August 27-30, 2019 (LIPIcs, Vol. 140), Wan J. Fokkink and Rob van        Yoshida. 2019. Precise subtyping for synchronous multiparty sessions. J. Log.
     Glabbeek (Eds.). Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 38:1–38:16.           Algebraic Methods Program. 104 (2019), 127–173. doi:10.1016/J.JLAMP.2018.12.002
     doi:10.4230/LIPICS.CONCUR.2019.38                                                    [22] Silvia Ghilezan, Jovanka Pantović, Ivan Prokić, Alceste Scalas, and Nobuko
 [8] Mario Bravetti, Marco Carbone, and Gianluigi Zavattaro. 2017. Undecidability of           Yoshida. 2023. Precise Subtyping for Asynchronous Multiparty Sessions. ACM
     asynchronous session subtyping. Inf. Comput. 256 (2017), 300–320. doi:10.1016/J.          Transactions on Computational Logic Volume 24, Issue 2, 14 (2023), 1–73. doi:10.
     IC.2017.07.010                                                                            1145/3568422
 [9] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de                  [23] Kohei Honda, Vasco Thudichum Vasconcelos, and Makoto Kubo. 1998. Lan-
     Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg            guage Primitives and Type Discipline for Structured Communication-Based
     Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf,            Programming. In ESOP. doi:10.1007/BFb0053567
     Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail          [24] Kohei Honda, Nobuko Yoshida, and Marco Carbone. 2016. Multiparty Asynchro-
     Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter,                  nous Session Types. J. ACM 63, 1, Article 9 (2016). doi:10.1145/2827695
     Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fo-         [25] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu
     tios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex            Liu, Jiajun Zhang, Bowen Yu, Keming Lu, Kai Dang, Yang Fan, Yichang Zhang,
     Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji,              An Yang, Rui Men, Fei Huang, Bo Zheng, Yibo Miao, Shanghaoran Quan, Yunlong
     Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike,            Feng, Xingzhang Ren, Xuancheng Ren, Jingren Zhou, and Junyang Lin. 2024.
     Joshua Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight,                 Qwen2.5-Coder Technical Report. arXiv:2409.12186 [cs.CL] https://arxiv.org/
     Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario               abs/2409.12186
     Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. 2021. Eval-            [26] Peter Kairouz, H. Brendan McMahan, Brendan Avent, Aurélien Bellet, Mehdi
     uating Large Language Models Trained on Code. CoRR abs/2107.03374 (2021).                 Bennis, Arjun Nitin Bhagoji, Kallista A. Bonawitz, Zachary Charles, Graham
     arXiv:2107.03374 https://arxiv.org/abs/2107.03374                                         Cormode, Rachel Cummings, Rafael G. L. D’Oliveira, Hubert Eichner, Salim El
[10] Tzu-Chun Chen, Mariangiola Dezani-Ciancaglini, and Nobuko Yoshida. 2024.                  Rouayheb, David Evans, Josh Gardner, Zachary Garrett, Adrià Gascón, Badih
     On the Preciseness of Subtyping in Session Types: 10 Years Later. In Proceedings          Ghazi, Phillip B. Gibbons, Marco Gruteser, Zaïd Harchaoui, Chaoyang He, Lie
     of the 26th International Symposium on Principles and Practice of Declarative             He, Zhouyuan Huo, Ben Hutchinson, Justin Hsu, Martin Jaggi, Tara Javidi, Gauri
     Programming, PPDP 2024, Milano, Italy, September 9-11, 2024, Alessandro Bruni,            Joshi, Mikhail Khodak, Jakub Konečný, Aleksandra Korolova, Farinaz Koushanfar,
     Alberto Momigliano, Matteo Pradella, Matteo Rossi, and James Cheney (Eds.).               Sanmi Koyejo, Tancrède Lepoint, Yang Liu, Prateek Mittal, Mehryar Mohri,
     ACM, 2:1–2:3. doi:10.1145/3678232.3678258                                                 Richard Nock, Ayfer Özgür, Rasmus Pagh, Hang Qi, Daniel Ramage, Ramesh
Specification-Guided Synthesis of Deadlock-Free Communication Protocol Refinements with Large Language Models


     Raskar, Mariana Raykova, Dawn Song, Weikang Song, Sebastian U. Stich, Ziteng             Pre-trained Language Models. In The Tenth International Conference on Learning
     Sun, Ananda Theertha Suresh, Florian Tramèr, Praneeth Vepakomma, Jianyu                  Representations, ICLR 2022, Virtual Event, April 25-29, 2022. OpenReview.net.
     Wang, Li Xiong, Zheng Xu, Qiang Yang, Felix X. Yu, Han Yu, and Sen Zhao. 2021.           https://openreview.net/forum?id=KmtVD97J43e
     Advances and Open Problems in Federated Learning. Found. Trends Mach. Learn.        [41] Sunil Prakash. 2026. LDP: An Identity-Aware Protocol for Multi-Agent LLM
     14, 1-2 (2021), 1–210. doi:10.1561/2200000083                                            Systems. arXiv:2603.08852 [cs.AI] https://arxiv.org/abs/2603.08852
[27] Julien Lange and Nobuko Yoshida. 2017. On the Undecidability of Asynchronous        [42] Qwen, :, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen
     Session Subtyping. In Foundations of Software Science and Computation Structures         Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang,
     - 20th International Conference, FOSSACS 2017, Held as Part of the European Joint        Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang
     Conferences on Theory and Practice of Software, ETAPS 2017, Uppsala, Sweden,             Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue,
     April 22-29, 2017, Proceedings (Lecture Notes in Computer Science, Vol. 10203),          Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tianyi Tang, Tingyu Xia,
     Javier Esparza and Andrzej S. Murawski (Eds.). 441–457. doi:10.1007/978-3-662-           Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan,
     54458-7_26                                                                               Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. 2025. Qwen2.5 Technical
[28] Edward A. Lee. 2008. Cyber Physical Systems: Design Challenges. In 2008                  Report. arXiv:2412.15115 [cs.CL] https://arxiv.org/abs/2412.15115
     11th IEEE International Symposium on Object and Component-Oriented Real-Time        [43] Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xi-
     Distributed Computing (ISORC). 363–369. doi:10.1109/ISORC.2008.25                        aoqing Ellen Tan, Yossi Adi, Jingyu Liu, Tal Remez, Jérémy Rapin, Artyom
[29] Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov,           Kozhevnikov, Ivan Evtimov, Joanna Bitton, Manish Bhatt, Cristian Canton-
     Chenghao Mou, Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, Qian Liu,              Ferrer, Aaron Grattafiori, Wenhan Xiong, Alexandre Défossez, Jade Copet, Faisal
     Evgenii Zheltonozhskii, Terry Yue Zhuo, Thomas Wang, Olivier Dehaene, Mishig             Azhar, Hugo Touvron, Louis Martin, Nicolas Usunier, Thomas Scialom, and
     Davaadorj, Joel Lamy-Poirier, João Monteiro, Oleh Shliazhko, Nicolas Gontier,            Gabriel Synnaeve. 2023. Code Llama: Open Foundation Models for Code. CoRR
     Nicholas Meade, Armel Zebaze, Ming-Ho Yee, Logesh Kumar Umapathi, Jian                   abs/2308.12950 (2023). arXiv:2308.12950 doi:10.48550/ARXIV.2308.12950
     Zhu, Benjamin Lipkin, Muhtasham Oblokulov, Zhiruo Wang, Rudra Murthy                [44] Alceste Scalas and Nobuko Yoshida. 2019. Less is More: Multiparty Session Types
     V, Jason T. Stillerman, Siva Sankalp Patel, Dmitry Abulkhanov, Marco Zocca,              Revisited. Proc. ACM Program. Lang. 3, POPL, Article 30 (Jan. 2019), 29 pages.
     Manan Dey, Zhihan Zhang, Nour Fahmy, Urvashi Bhattacharyya, Wenhao Yu,                   doi:10.1145/3290343
     Swayam Singh, Sasha Luccioni, Paulo Villegas, Maxim Kunakov, Fedor Zhdanov,         [45] David Smith Sundarsingh, Jun Wang, Jyotirmoy V. Deshmukh, and Yiannis
     Manuel Romero, Tony Lee, Nadav Timor, Jennifer Ding, Claire Schlesinger, Hailey          Kantaros. 2026. ConformalNL2LTL: Translating Natural Language Instruc-
     Schoelkopf, Jan Ebert, Tri Dao, Mayank Mishra, Alex Gu, Jennifer Robinson,               tions into Temporal Logic Formulas with Conformal Correctness Guarantees.
     Carolyn Jane Anderson, Brendan Dolan-Gavitt, Danish Contractor, Siva Reddy,              arXiv:2504.21022 [cs.CL] https://arxiv.org/abs/2504.21022
     Daniel Fried, Dzmitry Bahdanau, Yacine Jernite, Carlos Muñoz Ferrandis, Sean        [46] Tadahiro Taniguchi, Ryo Ueda, Tomoaki Nakamura, Masahiro Suzuki, and Akira
     Hughes, Thomas Wolf, Arjun Guha, Leandro von Werra, and Harm de Vries.                   Taniguchi. 2025. Generative Emergent Communication: Large Language Model
     2023. StarCoder: may the source be with you! Trans. Mach. Learn. Res. 2023               is a Collective World Model. CoRR abs/2501.00226 (2025). arXiv:2501.00226
     (2023). https://openreview.net/forum?id=KoFOg41haE                                       doi:10.48550/ARXIV.2501.00226
[30] Xiaohan Lin, Qingxing Cao, Yinya Huang, Haiming Wang, Jianqiao Lu,                  [47] Shubham Ugare, Tarun Suresh, Hangoo Kang, Sasa Misailovic, and Gagandeep
     Zhengying Liu, Linqi Song, and Xiaodan Liang. 2024. FVEL: Interactive Formal             Singh. 2025. SynCode: LLM Generation with Grammar Augmentation. Transac-
     Verification Environment with Large Language Models via Theorem Proving. In              tions on Machine Learning Research 2025 (2025). https://openreview.net/forum?
     Advances in Neural Information Processing Systems 38: Annual Conference on Neu-          id=HiUZtgAPoH
     ral Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, De-   [48] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
     cember 10 - 15, 2024, Amir Globersons, Lester Mackey, Danielle Belgrave, Angela          Aidan N Gomez, Ł ukasz Kaiser, and Illia Polosukhin. 2017. Attention is All you
     Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang (Eds.). http://papers.             Need. In Advances in Neural Information Processing Systems, I. Guyon, U. Von
     nips.cc/paper_files/paper/2024/hash/62c6d7893b13a13c659cb815852dd00d-                    Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett
     Abstract-Datasets_and_Benchmarks_Track.html                                              (Eds.), Vol. 30. Curran Associates, Inc. https://proceedings.neurips.cc/paper_
[31] Zhi Ma, Cheng Wen, Zhexin Su, Xiao Liang, Cong Tian, Shengchao Qin, and                  files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf
     Mengfei Yang. 2025. Bridging Natural Language and Formal Specification-             [49] Bailin Wang, Zi Wang, Xuezhi Wang, Yuan Cao, Rif A. Saurous, and Yoon
     Automated Translation of Software Requirements to LTL via Hierarchical Se-               Kim. 2023. Grammar Prompting for Domain-Specific Language Genera-
     mantics Decomposition Using LLMs. In 40th IEEE/ACM International Conference              tion with Large Language Models. In Advances in Neural Information Pro-
     on Automated Software Engineering, ASE 2025, Seoul, Korea, Republic of, November         cessing Systems 36: Annual Conference on Neural Information Processing Sys-
     16-20, 2025. IEEE, 1208–1220. doi:10.1109/ASE63991.2025.00104                            tems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023,
[32] Samuele Marro, Emanuele La Malfa, Jesse Wright, Guohao Li, Nigel Shadbolt,               Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt,
     Michael J. Wooldridge, and Philip Torr. 2024. A Scalable Communication Pro-              and Sergey Levine (Eds.). http://papers.nips.cc/paper_files/paper/2023/hash/
     tocol for Networks of Large Language Models. CoRR abs/2410.11905 (2024).                 cd40d0d65bfebb894ccc9ea822b47fa8-Abstract-Conference.html
     arXiv:2410.11905 doi:10.48550/ARXIV.2410.11905                                      [50] Zhongyi Wang, Tengjie Lin, Mingshuai Chen, Mingqi Yang, Haokun Li, Xiao
[33] Daniel Melcer, Nathan Fulton, Sanjay Krishna Gouda, and Haifeng Qian.                    Yi, Shengchao Qin, and Jianwei Yin. 2025. Preguss: It Analyzes, It Specifies, It
     2024. Constrained Decoding for Fill-in-the-Middle Code Language Mod-                     Verifies. arXiv:2508.14532 [cs.SE] https://arxiv.org/abs/2508.14532
     els via Efficient Left and Right Quotienting of Context-Sensitive Grammars.         [51] Brandon T. Willard and Rémi Louf. 2023. Efficient Guided Generation for Large
     arXiv:2402.17988 [cs.PL] https://arxiv.org/abs/2402.17988                                Language Models. arXiv:2307.09702 [cs.CL] https://arxiv.org/abs/2307.09702
[34] Daniel Mendoza, Christopher Hahn, and Caroline Trippel. 2024. Translating           [52] Nobuko Yoshida. 2024. Programming Language Implementations with Multiparty
     Natural Language to Temporal Logics with Large Language Models and Model                 Session Types. In Active Object Languages: Current Research Trends, Frank S.
     Checkers. In Formal Methods in Computer-Aided Design, FMCAD 2024, Prague,                de Boer, Ferruccio Damiani, Reiner Hähnle, Einar Broch Johnsen, and Eduard
     Czech Republic, October 15-18, 2024, Nina Narodytska and Philipp Rümmer (Eds.).          Kamburjan (Eds.). Lecture Notes in Computer Science, Vol. 14360. Springer,
     IEEE, 1–11. doi:10.34727/2024/ISBN.978-3-85448-065-5_17                                  147–165. doi:10.1007/978-3-031-51060-1_6
[35] Niels Mündler, Jingxuan He, Hao Wang, Koushik Sen, Dawn Song, and Martin T.         [53] Mengyan Zhao, Ran Tao, Yanhong Huang, Jianqi Shi, Shengchao Qin, and Yang
     Vechev. 2025. Type-Constrained Code Generation with Language Models. Proc.               Yang. 2024. NL2CTL: Automatic Generation of Formal Requirements Specifica-
     ACM Program. Lang. 9, PLDI (2025), 601–626. doi:10.1145/3729274                          tions via Large Language Models. In Formal Methods and Software Engineering:
[36] Shaan Nagy, Timothy Zhou, Nadia Polikarpova, and Loris D’Antoni. 2026. Chop-             25th International Conference on Formal Engineering Methods, ICFEM 2024, Hi-
     Chop: A Programmable Framework for Semantically Constraining the Output                  roshima, Japan, December 2–6, 2024, Proceedings (Hiroshima, Japan). Springer-
     of Language Models. Proc. ACM Program. Lang. 10, POPL (2026), 1905–1932.                 Verlag, Berlin, Heidelberg, 1–17. doi:10.1007/978-981-96-0617-7_1
     doi:10.1145/3776708                                                                 [54] Mengyan Zhao, Ran Tao, Yanhong Huang, Jianqi Shi, Shengchao Qin, and Yang
[37] OpenAI. 2026. Introducing GPT-5.5. https://openai.com/index/introducing-gpt-             Yang. 2024. NL2CTL: Automatic Generation of Formal Requirements Specifi-
     5-5/. Accessed: June 2026.                                                               cations via Large Language Models. In Formal Methods and Software Engineer-
[38] Kanghee Park, Timothy Zhou, and Loris D’Antoni. 2025. Flexible and Efficient             ing - 25th International Conference on Formal Engineering Methods, ICFEM 2024,
     Grammar-Constrained Decoding. arXiv:2502.05111 [cs.CL] https://arxiv.org/                Hiroshima, Japan, December 2-6, 2024, Proceedings (Lecture Notes in Computer
     abs/2502.05111                                                                           Science, Vol. 15394), Kazuhiro Ogata, Dominique Méry, Meng Sun, and Shaoying
[39] Chau Pham, Boyi Liu, Yingxiang Yang, Zhengyu Chen, Tianyi Liu, Jianbo Yuan,              Liu (Eds.). Springer, 1–17. doi:10.1007/978-981-96-0617-7_1
     Bryan A. Plummer, Zhaoran Wang, and Hongxia Yang. 2024. Let Models Speak
     Ciphers: Multiagent Debate through Embeddings. In The Twelfth International
     Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11,
     2024. OpenReview.net. https://openreview.net/forum?id=sehRvaIPQQ
[40] Gabriel Poesia, Alex Polozov, Vu Le, Ashish Tiwari, Gustavo Soares, Christopher
     Meek, and Sumit Gulwani. 2022. Synchromesh: Reliable Code Generation from
