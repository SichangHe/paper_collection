                                         Automatically Building Machine-Checked Assurance Cases
                                         from C Codebases to Requirements
                                         HAOKUN LI† , Zhejiang University, China
                                         ZHONGYI WANG† , Zhejiang University, China
                                         GUANYAN LI, University of Oxford, UK
                                         XIAO YI, The Chinese University of Hong Kong, China
                                         SHENGCHAO QIN, Xidian University, China
arXiv:2609.40119v1 [cs.PL] 30 Sep 2026




                                         JIANWEI YIN, Zhejiang University, China
                                         MINGSHUAI CHEN* , Zhejiang University, China
                                         Large language models (LLMs) have shown promise in automating interactive theorem proving, yet verification
                                         of real-world C codebases requires more than discharging individual proof goals. The task involves jointly
                                         constructing expressive function specifications and their proofs, and ensuring that library interfaces compose
                                         along intended call sequences even without a designated client. This paper presents CCV, an LLM-assisted
                                         framework for building machine-checked assurance cases: structured, auditable artifacts supporting the claim
                                         that a C codebase meets its intended requirements. To model intended cross-interface use in open libraries, CCV
                                         constructs an interface protocol that exposes permitted call sequences and resource assumptions for review,
                                         with a conditional safety guarantee under verified contracts and caller obligations. CCV coordinates two
                                         complementary phases: (i) requirement-guided analysis and bottom-up construction of candidate specifications
                                         and protocols; and (ii) modular proof construction with feedback that revises the specifications and proofs.
                                         Implemented using VST in Rocq, CCV verifies memory safety and leak freedom for all 299 function definitions
                                         across six C benchmarks, including industrial cryptographic components, with less than one person-day of
                                         reported human effort per benchmark. The guarantees depend on disclosed contracts and assumptions; human
                                         review supplies the conformance judgments connecting the formal artifacts to the intended requirements.
                                         CCS Concepts: • Theory of computation → Program verification; Program specifications; • Software
                                         and its engineering → Formal software verification.
                                         Additional Key Words and Phrases: Deductive verification, Separation logic, Large language models, VST/Rocq
                                         ACM Reference Format:
                                         Haokun Li, Zhongyi Wang, Guanyan Li, Xiao Yi, Shengchao Qin, Jianwei Yin, and Mingshuai Chen. 2026.
                                         Automatically Building Machine-Checked Assurance Cases from C Codebases to Requirements. Proc. ACM
                                         Program. Lang. 1, 1 (October 2026), 20 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn

                                         1   INTRODUCTION
                                         C codebases continue to carry the weight of safety-critical systems, and their formal verification rests
                                         on a machine-checked foundation: Hoare-style deductive verification represents intended behavior
                                         by function contracts (a.k.a., specifications) and proves that implementations satisfy them [22].
                                         ∗ Corresponding author
                                         † Both authors contributed equally to this research.


                                         Authors’ Contact Information: Haokun Li, Zhejiang University, Hangzhou, China, College of Computer Science and
                                         Technology, ker@pm.me; Zhongyi Wang, Zhejiang University, Hangzhou, China, College of Computer Science and
                                         Technology, zhongyi.wang@zju.edu.cn; Guanyan Li, University of Oxford, Oxford, UK, guanyan.li.cs@gmail.com; Xiao Yi,
                                         The Chinese University of Hong Kong, Hong Kong, China, yixiao5428@link.cuhk.edu.hk; Shengchao Qin, Xidian University,
                                         Xi’an, China, shengchao.qin@gmail.com; Jianwei Yin, Zhejiang University, Hangzhou, China, College of Computer Science
                                         and Technology, zjuyjw@zju.edu.cn; Mingshuai Chen, Zhejiang University, Hangzhou, China, College of Computer Science
                                         and Technology, m.chen@zju.edu.cn.

                                         2026. ACM 2475-1421/2026/10-ART
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn


                                                                                 Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
2                                                                        Mingshuai Chen, Zhongyi Wang and Haokun Li


Interactive theorem provers (ITPs) support a proof-producing style of verification: an ITP justifies
a formal statement that the code meets its stated contracts, yielding machine-checked evidence for
that statement [28, 33]. Such verification has provided assurance of critical systems, but developing
the necessary contracts and proofs remains costly human work [27, 33].
   Recent work has made substantial progress in using large language models (LLMs) to automate
proof construction (and repair) in ITPs [19, 25, 29, 35, 40, 43, 48, 50]. Yet proof-construction au-
tomation alone does not meet the verification needs of a large real-world C codebase. Typically it
necessitates establishing an end-to-end assurance case [23, 37]: not only formal evidence that the
implementation satisfies its specifications, but also an auditable argument that those specifications,
taken together, conform to the intended requirements. This raises two challenges at different levels.
   First, how to construct function-level verification—the specification of a function and a machine-
checked proof that its body satisfies the specification? The two obligations are coupled: the concrete
form of a specification–what it promises and how it is phrased–decisively shapes whether a body
proof can go through, and proof attempts in turn expose where the specification is too strong, too
weak, or mis-expressed. A usable, provable pair is therefore the outcome of an iterative co-evolution,
not of a single synthesis pass. Methods that construct proofs [19, 25, 29, 35, 40, 43, 48, 50] of stated
theorems take the specification as given, and methods that synthesize contracts [36, 51, 52]—
typically validated by auto-active backends rather than an ITP kernel—stop before a machine-
checked body proof. We develop this first challenge in Section 2.1.
   Second, how to establish library-level conformance—that the exported interfaces, taken together,
conform to the intended requirements? A library is a collection of modules, and the specifications
of its externally callable functions (e.g., typically the module-entry functions) form its interfaces.
An open library has no designated client functions (e.g., a main), a category that a substantial part
of real-world codebases falls into [6, 21]. Verifying an open library therefore raises a common
difficulty: proofs can establish that each module satisfies its interface, but the requirements of a
library are often stated over the order in which its interfaces may be called, and per-module proofs
do not by themselves show that those interfaces, taken together, support the call sequences the
requirements expect. Yet existing LLM-assisted methods stop at function-level verification, leaving
whether the library’s interfaces, taken together, conform to the requirements an open problem that
typically becomes a manual-review obligation. We develop this second challenge in Section 2.2.
   In response to these challenges, we present CCV, an LLM-assisted framework for building
machine-checked assurance cases from C codebases to their requirements. To model intended
cross-interface use in open libraries, CCV constructs an interface protocol that describes permitted
calls, their possible outcomes, and the resources carried between them. The protocol guides the
synthesis of composable interfaces and exposes their call sequences and assumptions for review.
Its soundness theorem provides a conditional safety guarantee under verified function contracts
and the stated caller obligations.
   CCV coordinates specification synthesis and proof construction in two complementary phases.
The first phase uses top-down analysis to derive natural-language function contracts from require-
ments and caller demands, then formalizes these contracts bottom-up and constructs a candidate
interface protocol. The second phase constructs modular proofs that function bodies satisfy their
contracts and that the contracts support the protocol. Proof feedback drives revisions to the
specifications, protocol, and proofs, rather than treating the initial specifications as fixed. This
specification–proof co-evolution connects function-level verification to the library-level require-
ments expressed through the protocol.
   We implement CCV using VST in Rocq and apply it to six C libraries, including four cryptographic
components of openHiTLS. The delivered proofs establish memory safety and leak freedom for all
299 function definitions under disclosed contracts and assumptions, with less than one person-day

Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
Automatically Building Machine-Checked Assurance Cases from C Codebases to Requirements                             3


of reported human effort per benchmark. Machine checking validates the formal evidence; human
review supplies the conformance judgments linking the specifications and protocol to the intended
requirements.

Contributions.
    • An end-to-end assurance-case framework that automates the joint construction of specifica-
      tions and proofs through a two-phase method, with explicit human conformance review.
    • A resource-aware interface protocol that models intended cross-interface use, guides the
      synthesis of composable interfaces, and provides a conditional safety guarantee for protocol-
      following calls.
    • An implementation and evaluation on six C benchmarks, verifying memory safety and leak
      freedom for all 299 function definitions with less than one person-day of reported human
      effort per benchmark.

Paper Structure. After the motivating examples (Section 2), we present the assurance case (Section 3),
interface protocol (Section 4), and two-phase CCV framework (Section 5). We then report the
evaluation (Section 6), discuss related work (Section 7), and conclude (Section 8).

2   BACKGROUND AND MOTIVATION
2.1 Function-Level Verification
Function-level verification is the process of producing, jointly, a specification that states what the
given function is meant to do and a machine-checked proof that the body inhabits that specification.
For example, the function (Fig. 1a) walks a linked list and returns its length. Fig. 1b shows the shape
of a specification in VST/Rocq: it binds a list of logic variables (WITH) and then states a precondition
(PRE) and a postcondition (POST). Each of PRE and POST carries two groups of assertions: a PROP
clause, a conjunction of pure logical propositions that do not depend on the heap, and a SEP clause,
a separating conjunction of spatial predicates describing the heap fragments the function requires
(in PRE) or returns (in POST). The PARAMS and GLOBALS clauses name the formal parameters and
globals, and RETURN names the return value. The proof (Fig. 1c) is a Hoare-style judgment of
the lemma verify_list_length, asserting that the body inhabits its specification. In VST the
proof is built interactively by forward symbolic execution: a tactic (e.g., forward, forward_loop,
forward_if) advances the symbolic proof state—the local environment together with the heap—
past one statement at a time, in the manner of a strongest-postcondition transformer; once the
whole body has been consumed, the remaining goals are closed by pure reasoning.
    The bottleneck of function-level verification lies in the inherent coupling of constructing the
specification and the proof. The nature of this coupling is best seen through a concrete failure.
Take the initial contract of Fig. 1b, which imposes no pure-logic constraints on the input list
(i.e., PROP () in the precondition). It looks unobjectionable: the implementation obviously counts
the elements, and the postcondition states exactly this. The proof, however, does not go through.
forward_loop on the while loop yields the three standard obligations—establishment, preservation,
and termination of the inductive loop invariant—which are discharged routinely. The trouble appears
at the assignment c = c + 1: here forward generates a signed-overflow proof goal, requiring
that the incremented value still fit in an int, since an overflowing addition is undefined behavior
(UB) in C. To proceed, one must revise the specification, strengthening its precondition with the
bound (Zlength xs <= Int.max_signed); under this refinement the overflow goal closes and an
ordinary loop proof succeeds. The specification is thus shaped by the proof, and the proof can advance
only as far as the specification permits—the two co-evolve, each constraining and refining the other.

                                    Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
4                                                                           Mingshuai Chen, Zhongyi Wang and Haokun Li


    struct node { int val; struct node *next; }                (* two versions: the initial (-) and the revised (+) one *)
    struct list { struct node *head; }                        Definition list_length_spec :=
                                                                DECLARE _list_length
    int list_length(struct list *l) {                           WITH l: val, xs: list Z
      int c = 0; struct node *cur = l->head;                    PRE [ tptr t_list ]
      while (cur != NULL) {                                     - PROP ()
        c = c + 1; /* overflow risk */                          + PROP (Zlength xs <= Int.max_signed)
        cur = cur->next;                                           PARAMS (l) GLOBALS () SEP (list_rep l xs)
      }                                                         POST [ tint ] PROP ()
      return c;                                                    RETURN (Vint (Int.repr (Zlength xs)))
    }                                                              SEP (list_rep l xs).

         (a) The list_length function in C.                     (b) The list_length specifications in VST/Rocq.
        Lemma verify_list_length : semax_body Vprog Gprog f_list_length list_length_spec.
        Proof. start_function. forward. (* c = 0 *) forward. (* cur = l->head *)
        forward_loop (EX front rest n, PROP (xs = front ++ rest; Int.signed n = Zlength front)
            SEP (seg h front cur; node_chain cur rest)) break: (EX rest n, PROP (...)).%assert
           (* loop goals: establishment / preservation / exit *)
           - (* establishment *) {...}
           - (* preservation *) forward_if.
             + (* cur ≠ NULL *) forward. (* c = c + 1 *) {...} (* overflow check *)
               forward. (* cur = cur->next *) {...}
             + (* cur = NULL *) forward. (* loop exit *) {...}
           - (* exit: reconstruct the list and return its length *) {...}
        Qed.

    (c) The simplified proof in VST/Rocq; the highlighted tactics discharge the overflow risk at c = c + 1.
Fig. 1. Function-level verification of list_length: (a) the function body which contains a potential overflow,
(b) its specifications in two versions (with the initial and revised differences highlighted), and (c) the proof
against its revised specification.

   The difficulty is far more severe in real-world verification, where contracts are far richer than a
single bound and the point at which a proof stalls is seldom as local as one assignment: determining
whether an obstruction calls for a stronger hypothesis, a sharper invariant, a different specification
shape, or a genuinely weaker requirement is a judgment made against the proof in flight. The
challenge is thus not to produce a specification or a proof in isolation, with the other taken as given
(which is what existing works [19, 25, 29, 35, 36, 40, 43, 48, 50–52] focus on), but to co-evolve them:

     Challenge 1. How to co-evolve the specification and the proof, so as to verify each function?


2.2    Library-Level Conformance
Suppose now that the difficulty of Section 2.1 has been overcome: every function of the library
is proved to satisfy its contract. Yet such function-level verification does not guarantee that the
library conforms to the intended requirements, i.e., library-level conformance, which is a cross-
interface property. It constrains how a call to one interface1 connects to a call to the next, which in
a VST/Rocq proof appears as whether the pre- and post-conditions of a legal call sequence can be
made to meet.
   The library in Fig. 2a has five interfaces. list_length is verified against the revised con-
tract of Fig. 1b, list_push and list_remove are proved to satisfy their specifications in Figs. 2b
1 Here and below, “calling an interface” is shorthand for calling the corresponding externally callable function; formally, the

interface is that function’s specification.


Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
Automatically Building Machine-Checked Assurance Cases from C Codebases to Requirements                             5


  struct list *list_new(void);                    /* allocate an empty list */
  void list_free(struct list *l);                       /* release a list */
  void list_push(struct list *l, int v); /* insert a node with value v at the head; length +1 */
  void list_remove(struct list *l, int v);    /* delete a node with v; do nothing if missed */
  int list_length(struct list *l); /* return the length of l, which is required to <= INT_MAX */

               (a) The five function declarations of the linked-list library (definitions elided).

Definition list_push_spec :=                          Definition list_remove_spec :=
  DECLARE _list_push                                    DECLARE _list_remove
  WITH l: val, v: Z, xs: list Z, gv: globals            WITH l: val, v: Z, xs: list Z, gv: globals
  PRE [ tptr t_list; tint ]                             PRE [ tptr t_list; tint ]
   PROP (repable_signed v)                               PROP (repable_signed v)
   PARAMS (l; Vint (Int.repr v)) GLOBALS (gv)            PARAMS (l; Vint (Int.repr v)) GLOBALS (gv)
   SEP (list_rep l xs; mem_mgr M gv)                     SEP (list_rep l xs; mem_mgr M gv)
  POST [ tvoid ] PROP (...)                             POST [ tvoid ] PROP (...)
- SEP (list_rep l ys; mem_mgr M gv)                   - SEP (list_rep l ys; mem_mgr M gv)
+ SEP (list_rep l (v :: xs); mem_mgr M gv)            + SEP (list_rep l (le_or_id v xs); mem_mgr M gv)

   (b) The simplified list_push specifications.            (c) The simplified list_remove specifications.
Fig. 2. The linked-list library exposes five functions (a). Both versions of the list_push and list_remove
specifications (b)(c), with the initial and revised differences highlighted, are provable; only the revised
(stronger) ones conform to the intended requirements.

and 2c, and the specifications of list_new and list_free are elided. Consider the client func-
tion in Fig. 3, which follows a call sequence the design intends to be legal. Yet in the specifi-
cations of Figs. 2b and 2c, where each function has been individually verified, this client func-
tion may still not be provable, due to a precondition violation. This is because the postcondi-
tions of list_push and list_remove are too weak to meet the precondition of list_length
at the assignment int n = list_length(l). Specifically, the separating spatial predicates (i.e.,
SEP (list_rep l ys; ...)) of the initial postconditions of
list_push and list_remove state that the list at the returning void client() {
point is some list ys, unrelated to the input xs, while list_length           list *l = list_new();
                                                                              list_push(l, 1);
requires the length of the input length to fit in the int range               list_push(l, 2);
(Fig. 1b). Both the initial interfaces in Figs. 2b and 2c are provable—       list_remove(l, 1);
take ys to be the actual result—yet a caller learns nothing about             /* precondition-violation risk */
the current length of the list. To discharge the precondition of              int n = list_length(l);
list_length, one must accumulate the length along the sequence;               list_free(l);
                                                                           }
from a postcondition that names an arbitrary ys this is impossi-
ble. The revised separating predicates in the postconditions repair          Fig. 3. A legal client function.
this: list_push returns v :: xs—the list with v at the head, and
list_remove returns le_or_id v xs—the list with its first v removed, or the list itself if v is
absent. Each is still provable of its body; the difference is that the revised strong forms carry exactly
the length information a sequence of calls needs.
   In a real open library the requirements are a collection of properties—memory safety, absence
of memory leaks, functional correctness—each stated over, and checked against, the sequences of
interface calls that a client may make. Thus the library-level conformance is established by not only
verifying each function, but also ensuring the strength of the interfaces. Yet existing LLM-assisted
methods [19, 25, 29, 35, 36, 40, 43, 48, 50–52] focus on the former, leaving the latter as:




                                    Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
6                                                                        Mingshuai Chen, Zhongyi Wang and Haokun Li


                       ② automatic                  VST/Rocq                 ③ automatic
                     refinement proof                                      soundness proof
    Clight AST                               Function Specification                          Interface Protocol

            ① automatic translation                                ④ manual conformance review

    C Codebase                                                         Design Requirement

                                        Fig. 4. The assurance case built by CCV.

    Challenge 2. How to reconcile the interfaces of a library to conform to its requirements?




3    THE ASSURANCE CASE
Section 2 developed the two primary challenges in constructing an end-to-end assurance case [23, 37]
for a C codebase. This is precisely what CCV builds: a structured, auditable set of artifacts supporting
the claim that the C codebase meets its design requirements.
   Fig. 4 gives an overview of this assurance case. It has five components connected by four kinds
of relations; the three components and two relations in the shaded region are formal artifacts that
CCV produces automatically and VST/Rocq checks. The C codebase is the input under verification,
while the requirements reflect the design intent. Starting from the codebase, CompCert’s front end
mechanically translates the C source into a Clight AST [33] (○). 1 CCV generates specifications for
the Clight functions and proofs that the functions satisfy those specifications (○).   2 For an open
library, CCV also constructs an interface protocol to describe the interface-call sequences permitted
by the requirements, and proves that every interface-call sequence accepted by the protocol is safe
with respect to the verified function specifications (○).
                                                        3 The remaining manual obligation in the
assurance case is to review whether the function specifications and the interface protocol conform
to the requriements (○),
                       4 for instance whether a precondition is too strong or the protocol omits a
legal and safe interface-call sequence. We formalize the interface protocol in Section 4, and explain
how CCV constructs this assurace case in Section 5.
   Fig. 4 depicts the assurance case for an open library, which has no designated client within the
verification scope. When a library instead contains a client (e.g., a main function), that in-scope
client supplies the concrete calling context that an open library lacks. CCV therefore replaces the
interface protocol with a client-level specification and whole-program evidence; the other four
components and three relations (○   1○2 ○),
                                         4 remain.


4    THE INTERFACE PROTOCOL FOR OPEN LIBRARIES
As Section 2.2 showed, function-level verification alone does not establish that a library’s interfaces
conform to its requirements. The root difficulty is that requirements are abstract—their intended
content is a set of legal interface-call sequences—whereas an open library has no client whose
control flow could delimit that set. Verifying library-level conformance therefore requires the expert
to (i) determine which interface-call sequences the requirements permit and (ii) ensure that the
interfaces along those sequences compose, reconciling them where they do not. To support both
tasks, CCV constructs an interface protocol: a state-based model that makes the intended interface-
call sequences and their assumptions explicit for review and guides the synthesis and refinement
of the constituent interfaces.


Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
Automatically Building Machine-Checked Assurance Cases from C Codebases to Requirements                             7


4.1   Protocol States and Behaviors
Definition 1 (Interface). Let F be the set of externally callable functions in an open library. For each
𝑓 ∈ F, its interface 𝐼 𝑓 is the specification
                                                           
                     𝐼 𝑓 ≜ ∀𝑤 ∈ 𝑊 𝑓 . 𝑃 𝑓 (𝑤) 𝑓 args 𝑓 (𝑤) ∃𝑜 ∈ 𝑂 𝑓 . 𝑄 𝑓 (𝑤, 𝑜) ,                    (1)
where
      args 𝑓 : 𝑊 𝑓 → CArgs 𝑓 ,    𝑃 𝑓 : 𝑊 𝑓 → Prop × MPred,           𝑄 𝑓 : 𝑊 𝑓 × 𝑂 𝑓 → Prop × MPred.
Here CArgs 𝑓 is the domain of concrete C argument tuples, Prop the pure propositions, and MPred
the separation-logic resource predicates. 𝑊 𝑓 contains the caller-instantiated logical variables, e.g.
target objects, abstract data, and ownership parameters, while args 𝑓 projects them onto the actual C
arguments; 𝑂 𝑓 contains the post-call logical values associated with a return value or an out-parameter.
The pre- and postconditions 𝑃 𝑓 (𝑤) and 𝑄 𝑓 (𝑤, 𝑜) each consist of a pure proposition and a spatial
resource predicate.                                                                                  ◁
Example 2. To instantiate (1) for list_length in Fig. 1b, take 𝑊length = Val × list Z (the domain
of WITH logical variables), 𝑂 length = Z, 𝑤 = (𝑙, 𝑥𝑠), 𝑜 = 𝑛, argslength (𝑙, 𝑥𝑠) = (𝑙), and
                      𝑃length (𝑤) = (Zlength 𝑥𝑠 ≤ Int.max_signed, list_rep 𝑙 𝑥𝑠),
                     𝑄 length (𝑤, 𝑜) = (return = 𝑛 ∧ 𝑛 = Zlength 𝑥𝑠, list_rep 𝑙 𝑥𝑠).
Here return denotes the mathematical integer represented by the concrete C return value. The two
components of 𝑃 length correspond to VST’s precondition PROP and SEP clauses. For 𝑄 length , the pure
component additionally incorporates the decoded RETURN constraint.                                 ◁
Definition 3 (Interface Protocol). Given the interface functions F of an open library, its interface
protocol is the five-tuple
                                          P ≜ (F, S, ⟦·⟧, G, B).                                        (2)
Let S𝐺 , S𝐵 , and S𝐿 be the state domains for the library’s global variables, resources currently borrowed
from clients, and library-managed objects, respectively. The state space is
                                             S ≜ S𝐺 × S𝐵 × S𝐿 .                                                   (3)
A state 𝜎 = (𝛾, 𝛽, ℓ) ∈ S records these three components from one interface call to the next. Its
separation-logic interpretation ⟦·⟧ : S → MPred is
                                                                              
                 ⟦𝜎⟧ ≜ Inv(𝜎) ∧ GlobalRep(𝛾) ∗ BorrowRep(𝛽) ∗ LibObjRep(ℓ) .                  (4)
Here Inv : S → Prop is a library-maintained invariant over the whole configuration, read as a
pure conjunct of the resource assertion; it may be True when no additional invariant is needed. The
interpretation in each edge pre- and postcondition requires this invariant to hold before the call and to
be re-established afterward.
   For each 𝑓 ∈ F, let Obs 𝑓 be the domain of observable values—returned by 𝑓 or written through its
out-parameters (c.f. 𝑂 𝑓 ). A branch describes one possible result of a call to 𝑓 : the next protocol state,
its observable values, a pure fact about the result, and a residual resource assertion not represented by
that state. Formally, a branch and its type are written as
  𝑏𝑟 ≜ (𝑏𝑟 .next, 𝑏𝑟 .obs, 𝑏𝑟 .prop, 𝑏𝑟 .res) ∈ Branch 𝑓 ,     Branch 𝑓 ≜ S × Obs 𝑓 × Prop × MPred.               (5)
The last two components in (2) are the per-function families
                         G = {𝐺 𝑓 | 𝑓 ∈ F},        𝐺 𝑓 : S × 𝑊 𝑓 → Prop,
                          B = {Br 𝑓 | 𝑓 ∈ F},      Br 𝑓 : S × 𝑊 𝑓 × 𝑂 𝑓 → 2Branch𝑓 .

                                    Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
8                                                                        Mingshuai Chen, Zhongyi Wang and Haokun Li


Here 𝐺 𝑓 (𝜎, 𝑤) is the pure guard for calling 𝑓 , while Br 𝑓 (𝜎, 𝑤, 𝑜) gives the possible branches. Branches
may have the same observable values but different successor states; the protocol does not require
observational determinacy.                                                                                ◁
Example 4. For the simplified linked-list protocol of Fig. 2, its S𝐺 = {𝜇mgr } and S𝐵 = {∅} are trivial
singleton domains, the sole values of which represent the allocator resource mem_mgr 𝑀 𝑔𝑣 and
no tracked borrowed resource, respectively. Take Inv(𝜎) = True for this example. Its S𝐿 can be
instantiated as maps from live handles to abstract lists, i.e. ℓ = {𝑝 ↦→ 𝑥𝑠, . . .} ∈ S𝐿 . Then a state can
be interpreted via
                  ⟦𝜎⟧ = ⟦(𝜇mgr, ∅, ℓ)⟧ ≜ mem_mgr 𝑀 𝑔𝑣 ∗ emp ∗                    ∗       list_rep 𝑝 𝑥𝑠.
                                                                              𝑝↦→𝑥𝑠 ∈ℓ

Thus the state carries the allocator resource together with the concrete representations of all live
library-managed lists. For the list_length interface of Example 2, using the same decoded-return
convention, take Obslength = Z and
             𝐺 length ((𝜇 mgr, ∅, ℓ), (𝑝, 𝑥𝑠)) ≜ 𝑝 ↦→ 𝑥𝑠 ∈ ℓ ∧ Zlength 𝑥𝑠 ≤ Int.max_signed,
                                                 | {z } |                  {z            }
                                                   state membership                  length bound
                                                  
                      Brlength (𝜎, (𝑝, 𝑥𝑠), 𝑛) ≜ (𝜎, 𝑛, 𝑛 = Zlength 𝑥𝑠, emp) .
The guard conjoins the interface’s pure length bound with membership in the protocol state. It is
neither the whole 𝑃 length nor just its pure component: it omits the spatial predicate list_rep 𝑝 𝑥𝑠
and adds state membership; ⟦𝜎⟧ supplies the omitted predicate. For fixed 𝑛, Brlength (𝜎, (𝑝, 𝑥𝑠), 𝑛)
contains one branch because list_length has no further runtime case split. Its four fields say that
the state is unchanged, the observed return is 𝑛, 𝑛 = Zlength 𝑥𝑠, and no resource remains outside
the successor-state interpretation.                                                               ◁
Definition 5 (Protocol Transition). For 𝑓 ∈ F, 𝑤 ∈ 𝑊 𝑓 , and 𝜎, 𝜎 ′ ∈ S, the protocol-transition
judgment is defined by
                  𝑓 (𝑤 )
              𝜎 −−−−→ 𝜎 ′       ⇐⇒       𝐺 𝑓 (𝜎, 𝑤) ∧ ∃𝑜 ∈ 𝑂 𝑓 , 𝑏𝑟 ∈ Br 𝑓 (𝜎, 𝑤, 𝑜). 𝑏𝑟 .next = 𝜎 ′ .          (6)
It states that calling 𝑓 with logical input 𝑤 is permitted at 𝜎 and may produce 𝜎 ′ ; 𝑤 is explicit, while
the implementation-selected outcome and branch remain existential.                                      ◁
Example 6. For the state 𝜎 = (𝜇mgr, ∅, ℓ) in Example 4, Definition 5 requires both the guard and a
branch whose next state is 𝜎. The latter is witnessed by choosing 𝑛 = Zlength 𝑥𝑠 and the singleton
branch defined in Example 4. Substituting the guard gives the following self-transition, which
exists exactly when the target list is recorded in ℓ and the length bound holds:
                    length(𝑝,𝑥𝑠 )
                𝜎 −−−−−−−−−→ 𝜎          ⇐⇒       𝑝 ↦→ 𝑥𝑠 ∈ ℓ ∧ Zlength 𝑥𝑠 ≤ Int.max_signed.                      ◁

4.2    Protocol Edges and Subsumption
The protocol-transition judgment declares an abstract state change, but does not show that the
implementation of 𝑓 supports it. Conversely, the interface 𝐼 𝑓 is indexed only by 𝑓 and does not
describe how one call transforms the resources represented by a particular source state. A protocol
edge connects the two levels by giving a source-state-specific specification of the same function.
Definition 7 (Protocol Edge). For a source state 𝜎 and interface function 𝑓 , define the edge
                                       𝐸                       𝐸
                    𝐸𝜎,𝑓 ≜ ∀𝑤 ∈ 𝑊 𝑓 . 𝑃𝜎,𝑓  (𝑤) 𝑓 args 𝑓 (𝑤) 𝑄 𝜎,𝑓    (𝑤) ,                                     (7)

Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
Automatically Building Machine-Checked Assurance Cases from C Codebases to Requirements                             9


which is a Hoare triple. Its distinction from Definition 1 is that the pre- and postcondition are bound to
(𝜎, 𝑓 ) rather than 𝑓 , specifically,
          𝐸                                              
         𝑃𝜎,𝑓 (𝑤) ≜ 𝐺 𝑓 (𝜎, 𝑤), ⟦𝜎⟧ ∗ BorrowIn 𝑓 (𝑤) ,
          𝐸                                                                                           (8)
        𝑄 𝜎,𝑓 (𝑤) ≜ ∃𝑜 ∈ 𝑂 𝑓 , 𝑏𝑟 ∈ Br 𝑓 (𝜎, 𝑤, 𝑜). 𝑏𝑟 .prop ∧ obs = 𝑏𝑟 .obs, ⟦𝑏𝑟 .next⟧ ∗ 𝑏𝑟 .res .
Here BorrowIn 𝑓 : 𝑊 𝑓 → MPred describes resources borrowed from the caller for this call, in addition
to those represented by 𝜎; it is emp when no additional resources are required. On return, these resources
may be retained in the successor state’s S𝐵 component or returned to the caller through 𝑏𝑟 .res. The
complete spatial postcondition is ⟦𝑏𝑟 .next⟧ ∗ 𝑏𝑟 .res: the first conjunct records resources tracked by the
successor state, and the second contains the residual resources outside that state. The value obs ∈ Obs 𝑓
denotes the observable values produced by the call.                                                      ◁
  An edge is not one transition. It summarizes all branches declared for the same (𝜎, 𝑓 ) pair: its
precondition fixes the source resources and caller obligations, while its postcondition accounts
for every implementation outcome by an observable branch and a successor state. The transition
judgment in (6) is the pure, resource-erased projection of this common guard-and-branch description.
Resources tracked after the call appear in the successor interpretation; every remaining spatial
POST resource appears in 𝑏𝑟 .res.
Definition 8 (Per-Edge Subsumption). For every enabled (𝜎, 𝑓 ) pair, the function interface 𝐼 𝑓
must subsume 𝐸𝜎,𝑓 , written Sub(𝐼 𝑓 , 𝐸𝜎,𝑓 ). After matching their logical parameters, the two essential
assertion-level obligations exhibit a frame 𝐹 such that, for every 𝑤 ∈ 𝑊 𝑓 ,
                    𝐸                                                         𝐸
                  𝑃𝜎,𝑓 (𝑤) ⊢ 𝐹 ∗ 𝑃 𝑓 (𝑤),       𝐹 ∗ ∃𝑜 ∈ 𝑂 𝑓 . 𝑄 𝑓 (𝑤, 𝑜) ⊢ 𝑄 𝜎,𝑓 (𝑤).               (9)
The first entailment establishes that an admissible edge call supplies the interface precondition; the
second requires every interface outcome, recombined with the frame, to fit a declared branch of the edge.
Concrete separation-logic systems impose additional signature, typing, and bookkeeping conditions; (9)
isolates the resource-flow content used here.                                                          ◁
   The same 𝐼 𝑓 is compared with 𝐸𝜎,𝑓 at every source state where 𝑓 is enabled. If 𝐶 𝑓 , the imple-
mentation of 𝑓 , satisfies 𝐼 𝑓 , then specification consequence and Sub(𝐼 𝑓 , 𝐸𝜎,𝑓 ) imply that 𝐶 𝑓 also
satisfies 𝐸𝜎,𝑓 . The precondition direction ensures that a permitted call is within the verified domain
of the interface; the postcondition direction ensures that an actual result cannot escape the declared
outcome abstraction. It does not prove the converse: an extra declared branch may never occur at
runtime.

4.3   Input-Aware Runs and Protocol Soundness
Definition 9 (Input-Aware Run). A run of P is a finite or infinite sequence
                                              𝑓1 (𝑤1 )     𝑓2 (𝑤2 )
                                     𝑟 = 𝜎0 −−−−−→ 𝜎1 −−−−−→ 𝜎2 · · · .
It is valid, written ValidRun P (𝑟 ), when every displayed transition satisfies (6); we also call a valid run
accepted by P. Every prefix of a valid run is again valid, so the accepted language is prefix-closed and
requires no final-state set. The logical input 𝑤𝑘 is therefore the input of that particular call, while the
implementation-selected outcome remains existential. The mechanized representation uses finite lists;
an infinite run is covered safety-wise when all of its finite prefixes are covered.                         ◁
  A valid run records one permitted successor at every position; it does not predict that successor
before execution. For the same (𝑓𝑘 , 𝜎𝑘 −1, 𝑤𝑘 ), another actual outcome may produce 𝜎𝑘′ ≠ 𝜎𝑘 . The
execution then realizes another valid run beginning with that successor, rather than the preselected
path above. This is the intended nondeterminism of the transition judgment, not a protocol failure.

                                    Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
10                                                                       Mingshuai Chen, Zhongyi Wang and Haokun Li


   To connect an abstract run to a real call sequence, two caller-side facts remain external to the
transition judgment. First, the actual C arguments must be those represented by 𝑤𝑘 . Second, at
each call boundary the caller must supply the resources described by BorrowIn 𝑓𝑘 (𝑤𝑘 ), separably
from the persistent resource represented by 𝜎𝑘 −1 and from its own frame. The persistent resource
is assumed independently only at the starting boundary: each edge postcondition returns the
interpretation of the actual successor, which is carried to the next call provided that intervening
client code does not invalidate it. We write Realizes P (𝜋, 𝑟 ) when a concrete client execution 𝜋
obeys these argument and ownership conditions and continues from a successor supplied by a
branch of each call’s edge postcondition, consistent with that call’s actual result and resources. If
the caller cannot distinguish the possible successors, its next call must be justified for every branch
that remains possible, rather than for one preferred successor.
   Let Safe𝐿 (𝜋) mean that every call into the library 𝐿 during 𝜋 is made in a state satisfying the
precondition of its interface; consequently, the verified interface guarantee applies to that call. The
safety predicate concerns the library calls and the properties stated by their interfaces, not arbitrary
client code outside those calls.
   The result relies on two principal machine-checkable hypotheses. (H1) Implementation satisfaction:
every function implementation 𝐶 𝑓 satisfies 𝐼 𝑓 . (H2) Per-edge subsumption: Sub(𝐼 𝑓 , 𝐸𝜎,𝑓 ) holds
for every enabled (𝜎, 𝑓 ). Implementation satisfaction is the function-level evidence described in
Section 5; per-edge subsumption is the protocol-specific obligation.

Theorem 10 (Protocol Soundness). Under H1 and H2, every concrete execution that realizes a valid
input-aware run is safe:

                            ValidRun P (𝑟 ) ∧ Realizes P (𝜋, 𝑟 )         =⇒          Safe𝐿 (𝜋).                (10)

Moreover, whenever such a call returns, the edge postcondition supplies a declared successor state whose
interpretation is available for the next call in the realized run.

   Proof sketch. Proceed over the call positions of 𝑟 . Validity supplies 𝐺 𝑓𝑘 (𝜎𝑘 −1, 𝑤𝑘 ). The realiza-
tion relation supplies the matching C arguments, the carried ⟦𝜎𝑘 −1 ⟧, and the separable borrowed
resources BorrowIn 𝑓𝑘 (𝑤𝑘 ); together these establish the edge precondition. The first subsumption
obligation establishes the interface precondition, and H1 gives the verified call guarantee. If the
call returns, H1 and the second subsumption obligation establish the edge postcondition, yielding a
branch, its actual observations, and ⟦𝑏𝑟 .next⟧. For a realized run, such a branch supplies the next
state interpretation; the ownership conditions preserve it until the next call. The argument applies
to every finite run and hence to every finite prefix of an infinite run.                               □

   The theorem deliberately separates machine evidence from applicability to a client. H1 and H2
are formal proof obligations; whether an unverified client actually passes the recorded 𝑤, supplies
the required borrowed resources, and respects the carried ownership is an exported caller obligation.
CCV does not claim to verify that arbitrary client. Nor does the theorem state that every abstract
valid run has a corresponding C client: it states that every client execution that realizes such a run
is within the verified interface domain.

4.4    Model Quality, Review, and Limits
Protocol soundness is necessary but not sufficient for a useful assurance artifact. An unsatisfiable
precondition can make a subsumption obligation vacuously easy, an overly strong guard can silently
reject intended clients, and an extra branch can describe an outcome that the implementation never
produces. CCV therefore subjects the protocol to three additional forms of scrutiny.

Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
Automatically Building Machine-Checked Assurance Cases from C Codebases to Requirements                            11


Model fidelity. The persistent state must account for the relevant resource situations at interface
boundaries, and every recorded state field must constrain its separation-logic interpretation. The
logical input 𝑤 must correspond to caller-visible arguments; each branch must consistently describe
its result, successor, and resources; resources retained across calls belong in the state, while resources
returned to the caller appear in 𝑏𝑟 .res. These checks constrain the model, but whether its predicates,
guards, and branches express the intended requirements remains a human conformance judgment.

Logical realizability. CCV requires a covering witness: one input-aware valid run that starts from a
grounded initial state (whose borrowed and library-managed components are empty), exercises
every interface function, and whose edge pre- and postconditions are logically satisfiable along that
same run. The witness prevents an entirely empty protocol from passing only through vacuous
obligations and provides a concrete artifact for review. It does not prove that every declared state
is satisfiable, that every branch occurs in the implementation, or that a concrete client program
realizing the witness exists.

Coverage and limits. Together with implementation satisfaction, per-edge subsumption prevents
the protocol from omitting an actual interface outcome from an enabled edge, but it does not
establish that the accepted language is maximal or complete with respect to the requirements.
The review must therefore look for intended client patterns excluded by guards, missing resource
situations, and overly coarse states; any known exclusions are disclosed as limitations rather than
justified as safety requirements. The present model also does not provide a client-side checker,
prove termination or branch liveness, or cover callback and concurrent ownership protocols.
   These review and disclosure obligations are part of the assurance case rather than weaknesses hid-
den outside the theorem. Section 5 explains how CCV derives the guards and branches from require-
ments and interfaces, generates the edge obligations, uses failed proofs to revise the specification–
protocol package, and records the final human confirmation.

5   CCV FRAMEWORK: AN EVIDENCE-PRODUCING WORKFLOW WITH REVIEW
    GATES
CCV is organized as an evidence-producing workflow rather than as a one-shot proof search. Agent-
working states construct a frozen Clight program, analyze its contractual demands, formalize shared
abstractions, and discharge proof obligations. Two explicit human gates review the parts of the
assurance case that are not settled by kernel checking: whether the chosen scope and assumptions
conform to the intended guarantees, and whether the resulting formal artifacts conform to the
intended design. The human decision is on the critical path. A successful run therefore yields both
machine-checkable proof evidence and an auditable record of the human judgments on which its
interpretation depends. Fig. 5 shows the paper-level workflow: yellow states are agent-working
states, blue states are human-involved review gates, and the two exit states report the outcome;
solid arrows advance the assurance artifacts, and dashed arrows request rework. The workflow is
organized around evidence artifacts, not around a single undifferentiated proof task: each agent-
working state produces a layer of Fig. 4 or the machine-checked relation connecting two layers, and
each gate consumes them. All four agent-working states apply both to open libraries and to libraries
with a designated main; the cases differ only in what V_Specify produces—an interface-protocol
configuration for the former and a main-level specification for the latter.
   The workflow implements two complementary phases. In Phase I, V_Analyze derives natural-
language contracts through top-down analysis of requirements and caller demands, and V_Specify
formalizes them bottom-up and constructs a candidate interface protocol for an open library. In
Phase II, V_Prove constructs the function and protocol proofs, with feedback that can revise the

                                    Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
12                                                                        Mingshuai Chen, Zhongyi Wang and Haokun Li


 V_PREPROCESS            V_ANALYZE              V_SPECIFY               V_PROVE                        Agent-working states

                                                                                                       Human-involved states

                          V_REVIEW                                     V_CONFIRM                       Exit states

                                                                                                       Forward transitions

                          V_FAILED                                     V_SUCCEED                       Backward transitions

Fig. 5. CCV’s paper-level verification workflow. Yellow states are agent-working states and blue states are
human-involved review gates. Solid arrows advance the assurance artifacts; dashed arrows request rework.
V_Review is an optional early review gate, whereas a successful run passes through V_Confirm. The figure
deliberately abstracts from operational failure routing and certificate delivery.

candidate specifications and protocol rather than treating them as fixed. Preprocessing and human
review support both phases by establishing the input and assessing the resulting assurance artifacts.
   Three properties of the control flow are worth making explicit. First, the direct edge from
V_Analyze to V_Specify makes the early human review an optional early review gate: when the
scope and risks are already clear, the agent proceeds to formalization directly. Second, V_Review
may send the run back to V_Preprocess: early review can question the frozen Clight program itself,
not merely request proof-script patches, and after such a rework the input binding, the analysis, and
the specifications are all re-established. Third, V_Confirm observes the proof and protocol artifacts
that were actually produced; if they do not faithfully express the reviewer’s decisions, rework enters
as a trackable revision request to V_Prove, not as a disclaimer appended to a report. V_Review is
a risk-sensitive early gate, whereas a successful run always passes through V_Confirm, which
carries the conformance judgment of the specifications and the protocol to the design intent. The
exits are scope-honest: V_Failed reports why the claimed assurance could not be responsibly
delivered, and V_Succeed delivers the assurance package—proof evidence, scope and assumption
disclosure, and the review record—without extending it to universal program correctness.2

5.1    V_Preprocess: Establishing the Frozen Clight Program
V_Preprocess turns the configured C source and its build context into a reproducible, checkable
frozen Clight program, together with the input provenance and a transformation and scope record.
Three kinds of input processing must be distinguished, because they differ in what may be claimed.
For trusted preprocessing and translation, CCV establishes the frozen Clight program by the
regeneration check of Section 3. For a semantics-preserving source transformation, the preservation
claim and the source of its evidence are disclosed separately. For an adaptation that changes
the program under verification or replaces environment behavior with new assumptions, no
preservation of the original C program’s semantics is claimed: the adaptation changes the assurance
scope, is recorded, and becomes an object of V_Review and V_Confirm. This distinction protects
the core claim of Section 3: the reader must know exactly which frozen Clight program was proved,
not merely that some “source code” was involved.

5.2    V_Analyze: From Code and Design Material to Contractual Demands
V_Analyze extracts, from callers, implementations, and design material, the interface functions
that define the library boundary, the contractual demands on each function, functional and resource

2 The implementation contains additional operational states for interruption handling, failure triage, and artifact delivery.

We abstract them away here because they do not add a new assurance relation; their responsibilities are reflected in the
review records and terminal outcomes.


Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
Automatically Building Machine-Checked Assurance Cases from C Codebases to Requirements                            13


invariants, candidate axiomatic specifications of external functions, and—for an open library—
candidate interface-usage constraints. The output is an analysis record with candidate assumptions
and the requirements placed on contracts and on the protocol; natural-language analysis by itself is
not a soundness theorem, and the state claims nothing beyond a documented basis for formalization.
The key discipline is that CCV does not treat specification synthesis as an oracle: it records the
assumptions and the analysis-to-specification choices that later reviews must assess.

5.3   V_Specify: Formalizing Specifications and the Protocol Configuration
V_Specify commits the analysis to formal objects: resource predicates, lemma statements, and
the library’s funspecs, and, for an open library, the interface protocol’s states, state interpretation,
function-labeled transition relation, and source-specific edge specifications. Formalization proceeds
from callees to callers, so that caller contracts can refer to existing callee specifications; the resulting
definitions and obligations are candidates whose proofs remain to be constructed. For an open
library, this configuration also exposes the transition-rule premises and edge preconditions that
determine which runs are accepted; their non-vacuity and conformance remain explicit review
obligations. Because the analysis is natural-language and the output is formal, the state produces an
explicit NL-to-formal change record, so that later review can compare what was approved during
analysis with what was actually formalized. The conformance of the resulting specifications to the
design intent is not guaranteed by any type system or by the fact that they compile; it is a human
judgment deferred to the review gates. The formal semantics of the protocol configuration is given
in Section 4.

5.4   V_Prove: Discharging and Auditing Proof Obligations
V_Prove constructs and checks the body-satisfaction proofs and the shared lemmas, and, for
an open library, discharges the per-edge subsumption checks and instantiates the generic run-
lifting proof underlying protocol soundness. When proof attempts expose a semantic gap, the agent
revisits the affected specifications, representations, or protocol and rechecks their dependent proofs;
otherwise it continues proof construction under the existing contracts. This feedback supports
specification–proof co-evolution within the workflow. Proof construction is accompanied by an
audit of dependencies and coverage, so that the absence of admitted holes and the axioms actually
used are part of the checked evidence rather than a matter of trust in the agent’s report. Proof
success does not imply unconditional correctness beyond the disclosed axiomatic specifications and
assumptions. The two kinds of checking are complementary: the Rocq kernel answers whether the
stated formal obligations are proved, and human confirmation answers whether those statements
say the right thing about the intended design.

5.5   Trust and Assurance Boundaries
The trusted computing base (TCB) of the formal artifacts comprises the Rocq kernel; the VST
program logic and its machine-checked soundness connection to the CompCert Clight semantics;
the configured but unverified preprocessing and front-end path from C to Clight, pinned to the
frozen input by the regeneration check; and the correctness-critical gate code that binds the frozen
source and toolchain configuration to the delivered Clight and proof artifacts. These gates also audit
proof coverage, the absence of proof holes, and all axioms and premises used by the delivered claims.
The case separately discloses the audited logical and model axioms, together with the allocator and
external-function premises on which its proofs depend. The LLM agent is not in the TCB: Rocq
rechecks every formal statement and proof that it proposes, while the correctness-critical gates
validate the source/artifact bindings and audits. Human conformance review is a further explicit
assurance boundary, not a kernel-checked theorem. The resulting formal guarantee is relative to

                                    Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
14                                                                       Mingshuai Chen, Zhongyi Wang and Haokun Li


the CompCert Clight semantics and these disclosed premises; extending it to an executable requires
a downstream verified-compilation step.

6    EVALUATION
We report verification results for six C programs, covering pointer-based data structures and
cryptographic components of openHiTLS. The cases comprise 299 function definitions across 18
translation units (TUs). The verification backend uses Rocq 9.0.0, VST 2.16, and CompCert 3.17.
The results are supported by archived source, specifications, proofs, certificates, and verification
reports.

Benchmarks and results. Table 1 summarizes the verified scope and available run costs. The red–
black tree exercises allocation, parent pointers, rotations, and insertion repair, with a designated
main. The linked-list entry uses roster, a renamed, single-TU variant of the linked-list library that
exercises traversal, deletion, and ownership transfer. The four openHiTLS cases implement ML-DSA
and SLH-DSA signatures, SHA-256/224 hashing, and FrodoKEM key encapsulation, together with
their context-management operations. C LOC counts physical lines of the original implementation
files, excluding headers, preprocessor expansion, and generated Clight syntax. The cryptographic
cases cover the listed modules and their configured C implementations; functions outside this scope
are represented by disclosed external specifications.

              Benchmark           C LOC      TUs     Functions     Time (d)     Tokens (B)   Human (d)
              Red–black tree         287        1            12        1.55             —          <1
              Linked list            148        1            10       ∼0.22           0.22         <1
              ML-DSA              ∼2,439        3           105        ∼7.7          ∼25.9         <1
              SLH-DSA              1,981        5            97           9             —          <1
              SHA-256/224            667        2            25        3.82           5.77         <1
              FrodoKEM             1,747        6            50       17.03          13.26         <1
Table 1. Verification scope and recorded cost. All listed functions, including internal helpers, are verified for
memory safety and leak freedom under disclosed contracts and assumptions. B denotes 109 tokens. Dashes
mark missing time/token records; Human (d) reports human effort in person-days.


   CCV requires delivered proofs to be free of admitted obligations; all six cases pass this gate. All
299 function bodies have machine-checked proofs that they satisfy their specifications. The memory-
safety guarantees hold under the function preconditions and the stated external specifications, with
respect to CompCert Clight semantics. Leak freedom is supported by accounting for heap resources
through deallocation or explicit transfer to the caller. For the linked-list, SLH-DSA, SHA-256/224,
and FrodoKEM libraries, the delivered evidence additionally includes an interface protocol, per-edge
subsumption proofs, and a covering witness. These cases demonstrate function verification and
protocol construction across multiple modules; the largest case contains 105 function definitions.
The cryptographic algorithms’ functional correctness, termination, and concurrency are outside
the scope of these results.

Verification cost. Elapsed time covers the recorded run through delivery, including interruptions
and service delays. For example, FrodoKEM took 17.03 days in total, of which 193.1 hours were
confirmed model-service downtime; subtracting those intervals gives 8.99 days. The token column
reports total recorded usage by the main agent and its subagents, including input, output, and cache
reads, with reasoning included according to the host’s accounting convention. The SHA-256/224
run used GLM-5.3 and GLM-5.3-Flash through OpenCode, whereas FrodoKEM used Claude Opus 5

Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
Automatically Building Machine-Checked Assurance Cases from C Codebases to Requirements                            15


through Claude Code. These measurements describe the recorded executions; different models,
service availability, and accounting conventions preclude a controlled efficiency comparison. SLH-
DSA’s token count and the red–black tree token count remain unavailable in the archived records.
The reported human effort is less than one person-day for each benchmark.
Conformance review in practice. Review of the SHA-256/224 case identified a self-copy input excluded
by the generated contract: CopyCtx(ctx, ctx) reaches a memcpy whose source and destination
overlap. The proof remains valid because its precondition requires disjoint source and destination
resources, but reviewing that exclusion exposed a library defect for investigation and disclosure.
This illustrates the role of requirements-facing review in the assurance case: a provable contract can
still exclude a use that merits scrutiny. The present cases provide evidence of completed verification
on these selected programs, rather than an estimate of success rate over arbitrary C codebases.

7     RELATED WORK
We relate CCV to two bodies of work. Section 7.1 positions the central protocol artifact among
resource-aware interface models and behavioral-interface synthesis; Section 7.2 compares how
verification artifacts are constructed, and what must be trusted, in each approach.

7.1    Resource-Aware API Models and Behavioral Interfaces
Separation-logic and ownership-aware verification already provide the main semantic ingredients
of resource-sensitive API reasoning. VST function specifications describe Hoare-style pre- and
postconditions over C memory [4], and systems such as RefinedC interpret refined ownership
types in a foundational separation logic [42]. These systems can express interfaces that consume a
resource indexed by one abstract configuration and return a resource indexed by another. CCV does
not claim this resource-transformer view as a novelty; it builds on it. Its specific role is to organize
verified exported API contracts into one reviewable central protocol for a library collection, and to
connect that protocol to provider-body proofs and accepted-run closure within a single assurance
workflow.
   At the behavioral level, typestate systems and behavioral-interface methods have long represented
legal method or API-call sequences [14, 44]. More directly, behavioral interface synthesis derives
automata of legal library calls from program models that are safe and, under stated assumptions,
permissive or full [2, 7, 21]. Specification mining and temporal-property inference offer additional
ways to propose API protocols from traces, queries, or temporal templates [3, 32]. CCV therefore
claims neither the first API automaton, nor the first source-derived legal-call language, nor the first
use of refinement feedback to construct a protocol.
   Instead, CCV targets a different assurance boundary. Its central protocol is deliberately design-
shaped rather than an inferred maximal implementation-safe language; its states are interpreted by
VST separation-logic resources; enabled edges are justified by refinement to exported contracts;
and the protocol is exposed for human design-conformance review. The contribution here is the
integration of a reviewed resource protocol layer into the assurance chain for verified C libraries,
not a new general theory of typestate or behavioral-interface synthesis.

7.2    Automating Deductive Verification: ITP, Auto-active, and LLM-Based Approaches
We compare along four axes: what is given as input, what is produced, where a specification’s
content comes from, and what must ultimately be trusted.
Proving given specifications. Most automation for deductive verification takes the specification
as given and discharges proof obligations one goal, lemma, or function at a time; the standard
benchmarks are built in exactly this way. In interactive provers, hammers translate a stated goal

                                    Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
16                                                                       Mingshuai Chen, Zhongyi Wang and Haokun Li


to external automated provers [8, 12], and learning- or LLM-based systems generate, repair, or
decompose proofs of stated theorems [19, 24, 25, 29, 35, 43]. Auto-active verifiers such as Dafny,
Frama-C/WP, and Verus discharge verification conditions with SMT solvers [26, 30, 31]; LLM
assistance in this setting supplies helper assertions for failing verifications [39], proof hints [34], or
whole correctness proofs completing code against its given specification [53]. RefinedC occupies
a middle ground, automating the foundational proof derivation once the user has annotated the
C code with refinement types [42]. Reported evaluations across these lines remain at benchmark
scale, and success rates drop measurably on real code: AutoRocq, the closest recent system to
our setting, proves 12 of 60 lemmas in a Linux kernel case study [49], and one cross-language
vericoding benchmark reports success rates of 27% for Lean against 82% for Dafny [9].

Generating specifications. A second body of work generates the contracts or invariants themselves,
or candidates for them. Classical techniques infer annotations within a fixed candidate space [20],
detect likely invariants from execution traces [16], or use bi-abduction to infer separation-logic
footprints whose reference point is the absence of memory errors rather than functional design
intent [10]. LLM-based generators mostly target auto-active verifiers: goal-directed ACSL anno-
tations validated by a weakest-precondition calculus [51, 52], JML specifications [36, 38], Verus
specifications and proofs synthesized by self-evolution [11], LLM-drafted Dafny contracts frozen
before proving [5], and code–docstring–annotation triples checked for mutual consistency [45]. On
the ITP side, CLEVER benchmarks the joint synthesis of specifications, implementations, and proofs
in Lean [47]; AutoRocq combines Frama-C-generated ACSL contracts with LLM-proposed loop
invariants filtered by value analysis, and discharges the resulting proof obligations in Rocq [49]; and
LeetProof validates an LLM-drafted Lean specification by randomized property-based testing before
any implementation is synthesized, an anchor that by itself exposed defects in roughly 10% of the
reference specifications of two Lean vericoding benchmarks [18]. Such validation remains empirical,
though: over-constrained specifications that the sampled tests happen to satisfy escape detection.
More fundamentally, none of these methods by itself connects a generated specification back to
the intended design: the acceptance criterion is the code’s own behavior, the observed traces, or a
stated target property, and verifier acceptance alone does not imply that a specification is correct
or complete [38]. Separation-logic specifications are the hardest to elicit: in one empirical study of
LLM-generated VeriFast annotations, 94% of all errors traced to separation-logic-verifier-specific
knowledge, with ownership and heap-chunk failures the largest single share [17].

Where specification content comes from. These generators also differ in direction. Most work locally
or bottom-up: a function’s candidate contract is shaped by its own body, documentation, or tests, and
where a call graph is used it schedules generation and validation rather than shaping content [51, 52].
The complementary, caller-driven direction derives a callee’s specification from its uses. Maximal
specification synthesis infers the weakest callee assumptions that make a given client correct,
recursively down the call graph [1]; angelic verification infers acceptable specifications of unknown
environment functions from their usage context, in the service of bug finding [13]; and two
recent LLM-based systems scale the idea to whole codebases, deriving specifications from caller
expectations through natural-language specifications and LLM-mediated Hoare-style reasoning [15],
or through top-down inference in a restricted DSL discharged by bounded model checking [46].
In these caller-driven lines the acceptance anchor is either mechanical or LLM-judged, and the
evidence stops at bug findings or bounded verdicts. CCV’s analysis phase is inspired by the caller-
expectation view of FM-Agent in particular [15]; it differs in that the propagated demands are
recorded as natural-language contracts that a human gate reviews and freezes, and the resulting
specifications are delivered as kernel-checked separation-logic proofs.

Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
Automatically Building Machine-Checked Assurance Cases from C Codebases to Requirements                                     17


Trust boundaries. What must ultimately be trusted also differs. Auto-active pipelines place the
verifier and its toolchain in the trusted computing base, as they provide no independently checkable
proofs [42]; and for any deductive verifier the specification itself remains a trusted input, because
an implementation proof “does not guarantee that the specification describes the behaviour the
user expects” [28]. Foundational multi-modal verifiers remove even the verifier from this base: in
Velvet, the soundness of verification-condition generation is itself a machine-checked Lean theorem,
and a property that survives randomized testing is admitted with sorry rather than entering the
certificate [18]. LLM-based generation changes who writes the artifacts, not who answers for them:
in a recent large Rocq development the agent silently weakened a theorem statement during proof
construction, and the authors conclude that statement review cannot be eliminated [41]. CCV’s
contribution is organizational rather than a new prover: an agent proposes contracts, lemmas,
protocol definitions, and proofs; the Rocq kernel and mechanical gates re-check all formal evidence,
so the agent stays outside the trusted computing base; and designated human gates review the
conformance of the formal artifacts to the selected requirements, recorded as an explicit part of the
machine-checked assurance case. Each of the lines above automates one stage of the path from
code to reviewed evidence; CCV organizes these stages into a single codebase-level workflow.

8   CONCLUSION
We have presented CCV, an LLM-assisted framework for building auditable assurance cases that
connect machine-checked program proofs to the intended requirements. Its two-phase method
co-evolves function specifications and proofs, while an interface protocol models intended cross-
interface use and guides the construction of composable contracts. Using VST in Rocq, CCV
establishes memory safety and leak freedom under disclosed contracts and assumptions for all
299 function definitions across six C benchmarks, including industrial cryptographic components.
Each benchmark requires less than one person-day of reported human effort. The resulting cases
combine automated evidence construction with explicit human conformance review.

REFERENCES
 [1] Aws Albarghouthi, Isil Dillig, and Arie Gurfinkel. 2016. Maximal specification synthesis. In POPL. ACM, 789–801.
     https://doi.org/10.1145/2914770.2837628
 [2] Rajeev Alur, Pavol Cerný, P. Madhusudan, and Wonhong Nam. 2005. Synthesis of interface specifications for Java
     classes. In Proceedings of the 32nd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL
     2005, Long Beach, California, USA, January 12-14, 2005, Jens Palsberg and Martín Abadi (Eds.). ACM, 98–109. https:
     //doi.org/10.1145/1040305.1040314
 [3] Glenn Ammons, Rastislav Bodík, and James R. Larus. 2002. Mining specifications. In POPL. ACM, 4–16. https:
     //doi.org/10.1145/503272.503275
 [4] Andrew W. Appel. 2011. Verified Software Toolchain - (Invited Talk). In Programming Languages and Systems - 20th
     European Symposium on Programming, ESOP 2011, Held as Part of the Joint European Conferences on Theory and Practice
     of Software, ETAPS 2011, Saarbrücken, Germany, March 26-April 3, 2011. Proceedings (Lecture Notes in Computer Science,
     Vol. 6602), Gilles Barthe (Ed.). Springer, 1–17. https://doi.org/10.1007/978-3-642-19718-5_1
 [5] Mantas Baksys, Stefan Zetzsche, Olivier Bouissou, Remi Delmas, Soonho Kong, and Sean B. Holden. 2025. ATLAS:
     Automated Toolkit for Large-Scale Verified Code Synthesis. arXiv:2512.10173
 [6] Lennart Beringer. 2021. Verified Software Units. In Programming Languages and Systems - 30th European Symposium on
     Programming, ESOP 2021, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2021,
     Luxembourg City, Luxembourg, March 27 - April 1, 2021, Proceedings (Lecture Notes in Computer Science, Vol. 12648),
     Nobuko Yoshida (Ed.). Springer, 118–147. https://doi.org/10.1007/978-3-030-72019-3_5
 [7] Dirk Beyer, Thomas A. Henzinger, and Vasu Singh. 2007. Algorithms for Interface Synthesis. In Computer Aided
     Verification, 19th International Conference, CAV 2007, Berlin, Germany, July 3-7, 2007, Proceedings (Lecture Notes in
     Computer Science, Vol. 4590), Werner Damm and Holger Hermanns (Eds.). Springer, 4–19. https://doi.org/10.1007/978-
     3-540-73368-3_4
 [8] Sascha Böhme and Tobias Nipkow. 2010. Sledgehammer: Judgement Day. In Automated Reasoning, 5th International
     Joint Conference, IJCAR 2010, Edinburgh, UK, July 16-19, 2010. Proceedings (Lecture Notes in Computer Science, Vol. 6173),

                                         Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
18                                                                          Mingshuai Chen, Zhongyi Wang and Haokun Li


     Jürgen Giesl and Reiner Hähnle (Eds.). Springer, 107–121. https://doi.org/10.1007/978-3-642-14203-1_9
 [9] Sergiu Bursuc, Theodore Ehrenborg, Shaowei Lin, Lacramioara Astefanoaei, Ionel Emilian Chiosa, Jure Kukovec, Alok
     Singh, Oliver Butterley, Adem Bizid, Quinn Dougherty, Miranda Zhao, Max Tan, and Max Tegmark. 2025. A benchmark
     for vericoding: formally verified program synthesis. arXiv:2509.22908
[10] Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. 2009. Compositional shape analysis by
     means of bi-abduction. In Proceedings of the 36th ACM SIGPLAN-SIGACT Symposium on Principles of Programming
     Languages (POPL 2009), Zhong Shao and Benjamin C. Pierce (Eds.). ACM, 289–300. https://doi.org/10.1145/1480881.
     1480917
[11] Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Hao Yu, Nan
     Duan, Peng Cheng, Fan Yang, Shuvendu K. Lahiri, Tao Xie, and Lidong Zhou. 2024. Automated Proof Generation for
     Rust Code via Self-Evolution. arXiv:2410.15756
[12] Łukasz Czajka and Cezary Kaliszyk. 2018. Hammer for Coq: Automation for Dependent Type Theory. J. Autom.
     Reason. 61, 1-4 (2018), 423–453. https://doi.org/10.1007/s10817-018-9458-4
[13] Ankush Das, Shuvendu K. Lahiri, Akash Lal, and Yi Li. 2015. Angelic verification: Precise verification modulo unknowns.
     In CAV (LNCS, Vol. 9206). Springer, 324–342. https://doi.org/10.1007/978-3-319-21690-4_19
[14] Robert DeLine and Manuel Fähndrich. 2001. Enforcing High-Level Protocols in Low-Level Software. In Proceedings of
     the 2001 ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), Snowbird, Utah, USA,
     June 20-22, 2001, Michael Burke and Mary Lou Soffa (Eds.). ACM, 59–69. https://doi.org/10.1145/378795.378811
[15] Haoran Ding, Zhaoguo Wang, and Haibo Chen. 2026. FM-Agent: Scaling formal methods to large systems via
     LLM-based Hoare-style reasoning. arXiv:2604.11556 [cs.SE]
[16] Michael D. Ernst, Jeff H. Perkins, Philip J. Guo, Stephen McCamant, Carlos Pacheco, Matthew S. Tschantz, and Chen
     Xiao. 2007. The Daikon system for dynamic detection of likely invariants. Sci. Comput. Program. 69, 1-3 (2007), 35–45.
     https://doi.org/10.1016/j.scico.2007.01.015
[17] Wen Fan, Minh Tran, Sanya Dod, Xin Hu, Marilyn Rego, Danning Xie, Jenna DiVincenzo, and Lin Tan. 2026. An
     Empirical Study of LLM-Generated Specifications for VeriFast. arXiv:2606.26490
[18] Yueyang Feng, Dipesh Kafle, Vladimir Gladshtein, Vitaly Kurin, George Pîrlea, Qiyuan Zhao, Peter Müller, and Ilya
     Sergey. 2026. Certified Program Synthesis with a Multi-Modal Verifier. arXiv:2604.16584
[19] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. 2023. Baldur: Whole-Proof Generation and Repair with
     Large Language Models. In Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium
     on the Foundations of Software Engineering. ACM, 1229–1241. https://doi.org/10.1145/3611643.3616243
[20] Cormac Flanagan and K. Rustan M. Leino. 2001. Houdini, an Annotation Assistant for ESC/Java. In Formal Methods
     Europe 2001, Formal Methods for Increasing Software Productivity (FME 2001) (Lecture Notes in Computer Science, Vol. 2021),
     Jose Nelson Amaral and Jiri Matousek (Eds.). Springer, 500–517. https://doi.org/10.1007/3-540-45251-6_29
[21] Thomas A. Henzinger, Ranjit Jhala, and Rupak Majumdar. 2005. Permissive interfaces. In Proceedings of the 10th
     European Software Engineering Conference held jointly with 13th ACM SIGSOFT International Symposium on Foundations
     of Software Engineering, 2005, Lisbon, Portugal, September 5-9, 2005, Michel Wermelinger and Harald C. Gall (Eds.).
     ACM, 31–40. https://doi.org/10.1145/1081706.1081713
[22] C. A. R. Hoare. 1969. An axiomatic basis for computer programming. Commun. ACM 12, 10 (Oct. 1969), 576–580.
     https://doi.org/10.1145/363235.363259
[23] ISO/IEC. 2019. ISO/IEC 15026-1:2019 Systems and Software Engineering - Systems and Software Assurance - Part 1:
     Concepts and Vocabulary.
[24] Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz Odrzygózdź, Piotr Miłoś, Yuhuai
     Wu, and Mateja Jamnik. 2022. Thor: Wielding Hammers to Integrate Language Models and Automated Theorem
     Provers. In Advances in Neural Information Processing Systems 35 (NeurIPS 2022). 8360–8373. arXiv:2205.10893
[25] Saketh Ram Kasibatla, Arpan Agarwal, Yuriy Brun, Sorin Lerner, Talia Ringer, and Emily First. 2026. Cobblestone: A
     Divide-and-Conquer Approach for Automating Formal Verification. In Proceedings of the 48th International Conference
     on Software Engineering (ICSE 2026). 704–716. https://doi.org/10.1145/3744916.3773178 arXiv:2410.19940
[26] Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris Yakobowski. 2015. Frama-C: A software
     analysis perspective. Formal Aspects Comput. 27, 3 (2015), 573–609. https://doi.org/10.1007/s00165-014-0326-7
[27] Gerwin Klein, June Andronick, Kevin Elphinstone, Toby Murray, Thomas Sewell, Rafal Kolanski, and Gernot Heiser.
     2014. Comprehensive Formal Verification of an OS Microkernel. ACM Transactions on Computer Systems 32, 1, Article
     2 (2014), 70 pages. https://doi.org/10.1145/2560537
[28] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock, Philip Derrin, Dhammika Elkaduwe,
     Kai Engelhardt, Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and Simon Winwood. 2009. seL4:
     Formal Verification of an OS Kernel. In Proceedings of the 22nd ACM Symposium on Operating Systems Principles. ACM,
     207–220. https://doi.org/10.1145/1629575.1629596



Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
Automatically Building Machine-Checked Assurance Cases from C Codebases to Requirements                                  19


[29] Andrei Kozyrev, Gleb Solovev, Nikita Khramov, and Anton Podkopaev. 2024. CoqPilot, a plugin for LLM-based
     generation of proofs. In Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering
     (ASE 2024). ACM, 2382–2385. https://doi.org/10.1145/3691620.3695357
[30] Andrea Lattuada, Travis Hance, Jay Bosamiya, Matthias Brun, Chanhee Cho, Hayley LeBlanc, Pranav Srinivasan, Reto
     Achermann, Tej Chajed, Chris Hawblitzel, Jon Howell, Jacob R. Lorch, Oded Padon, and Bryan Parno. 2024. Verus: A
     Practical Foundation for Systems Verification. In Proceedings of the 30th Symposium on Operating Systems Principles
     (SOSP 2024). ACM, 438–454. https://doi.org/10.1145/3694715.3695952
[31] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Verifier for Functional Correctness. In LPAR (Dakar) (Lecture
     Notes in Computer Science, Vol. 6355). Springer, 348–370. https://doi.org/10.1007/978-3-642-17511-4_20
[32] Caroline Lemieux, Dennis Park, and Ivan Beschastnikh. 2015. General LTL Specification Mining. In 30th IEEE/ACM
     International Conference on Automated Software Engineering, ASE 2015, Lincoln, NE, USA, November 9-13, 2015, Myra B.
     Cohen, Lars Grunske, and Michael Whalen (Eds.). IEEE Computer Society, 81–92. https://doi.org/10.1109/ASE.2015.71
[33] Xavier Leroy. 2009. Formal verification of a realistic compiler. Commun. ACM 52, 7 (2009), 107–115. https://doi.org/10.
     1145/1538788.1538814
[34] Chloe R. Loughridge, Qinyi Sun, Seth Ahrenbach, Federico Cassano, Chuyue Sun, Ying Sheng, Anish Mudide,
     Md Rakib Hossain Misu, Nada Amin, and Max Tegmark. 2025. DafnyBench: A Benchmark for Formal Software
     Verification. Transactions on Machine Learning Research (2025). https://openreview.net/forum?id=yBgTVWccIx
[35] Minghai Lu, Benjamin Delaware, and Tianyi Zhang. 2024. Proof Automation with Large Language Models. In
     Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (ASE 2024). ACM,
     1509–1520. https://doi.org/10.1145/3691620.3695521
[36] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2025. SpecGen: Automated Generation of Formal Program
     Specifications via Large Language Models. In ICSE. IEEE, 16–28. https://doi.org/10.1109/ICSE55347.2025.00129
[37] Nikolai Mansourov and Djenana Campara. 2011. Confidence as a product. In System Assurance. Morgan Kaufmann,
     Boston, 23–47. https://doi.org/10.1016/B978-0-12-381414-2.00002-6
[38] Md Rakib Hossain Misu, Iris Ma, and Cristina V. Lopes. 2026. Spec-Harness: Measuring and Improving Behavioral
     Adequacy of LLM-Synthesized Formal Specifications. arXiv:2604.00280
[39] Eric Mugnier, Emmanuel Anaya Gonzalez, Nadia Polikarpova, Ranjit Jhala, and Yuanyuan Zhou. 2025. Laurel:
     Unblocking Automated Verification with Large Language Models. Proc. ACM Program. Lang. 9, OOPSLA (2025),
     1519–1545. https://doi.org/10.1145/3720499
[40] Prasita Mukherjee, Minghai Lu, and Benjamin Delaware. 2025. LLM-Assisted Synthesis of High-Assurance C Programs.
     In ASE. IEEE, 3108. https://doi.org/10.1109/ASE63991.2025.00255
[41] Zoe Paraskevopoulou. 2026. Machine-Generated, Machine-Checked Proofs for a Verified Compiler (Experience Report).
     Proc. ACM Program. Lang. 10, ICFP (2026), 807–826. https://doi.org/10.1145/3828700 arXiv:2602.20082
[42] Michael Sammler, Rodolphe Lepigre, Robbert Krebbers, Kayvan Memarian, Derek Dreyer, and Deepak Garg. 2021.
     RefinedC: automating the foundational verification of C code with refined ownership types. In PLDI ’21: 42nd ACM
     SIGPLAN International Conference on Programming Language Design and Implementation, Virtual Event, Canada, June
     20-25, 2021, Stephen N. Freund and Eran Yahav (Eds.). ACM, 158–174. https://doi.org/10.1145/3453483.3454036
[43] Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin Lerner. 2020. Generating Correctness Proofs with Neural
     Networks. In Proceedings of the 4th ACM SIGPLAN International Workshop on Machine Learning and Programming
     Languages (MAPL 2020). ACM, 1–10. https://doi.org/10.1145/3394450.3397466
[44] Robert E. Strom and Shaula Yemini. 1986. Typestate: A Programming Language Concept for Enhancing Software
     Reliability. IEEE Trans. Software Eng. 12, 1 (1986), 157–171. https://doi.org/10.1109/TSE.1986.6312929
[45] Chuyue Sun, Ying Sheng, Oded Padon, and Clark Barrett. 2024. Clover: Closed-Loop Verifiable Code Generation. In AI
     Verification - First International Symposium, SAIV 2024, Montreal, QC, Canada, July 22–23, 2024, Proceedings (Lecture
     Notes in Computer Science). Springer, 134–155. https://doi.org/10.1007/978-3-031-65112-0_7
[46] Youcheng Sun, Jiawen Liu, Daniel Kroening, and Jason Xue. 2026. Agentic model checking. arXiv:2605.21434 [cs.SE]
[47] Amitayush Thakur, Jasper Lee, George Tsoukalas, Meghana Sistla, Matthew Zhao, Stefan Zetzsche, Greg Durrett,
     Yisong Yue, and Swarat Chaudhuri. 2025. CLEVER: A Curated Benchmark for Formally Verified Code Generation.
     arXiv:2505.13938
[48] Kyle Thompson, Nuno Saavedra, Pedro Carrott, Kevin Fisher, Alex Sanchez-Stern, Yuriy Brun, João F. Ferreira, Sorin
     Lerner, and Emily First. 2025. Rango: Adaptive Retrieval-Augmented Proving for Automated Software Verification. In
     ICSE. IEEE, 347–359. https://doi.org/10.1109/ICSE55347.2025.00161
[49] Haoxin Tu, Huan Zhao, Yahui Song, Mehtab Zafar, Ruijie Meng, and Abhik Roychoudhury. 2026. Agentic Verification
     of Software Systems. Proc. ACM Softw. Eng. 3, FSE (2026), 3558–3581. https://doi.org/10.1145/3808164 arXiv:2511.17330
[50] Hanyang Wang, Xiwei Wu, and Qinxiang Cao. 2026. SL-VC: A Benchmark and Automated Framework for Separation
     Logic Verification Condition Proving. In Proceedings of the 43rd International Conference on Machine Learning (ICML
     2026) (Proceedings of Machine Learning Research, Vol. 306). PMLR, Seoul, South Korea. Equal contribution.


                                        Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
20                                                                         Mingshuai Chen, Zhongyi Wang and Haokun Li


[51] Zhongyi Wang, Tengjie Lin, Mingshuai Chen, Haokun Li, Mingqi Yang, Xiao Yi, Shengchao Qin, Yixing Luo, Xiaofeng
     Li, Bin Gu, Liqiang Lu, and Jianwei Yin. 2026. A Tale of 1001 LoC: Potential Runtime Error-Guided Specification
     Synthesis for Verifying Large-Scale Programs. Proc. ACM Program. Lang. 10, OOPSLA1, Article 160 (2026), 29 pages.
     https://doi.org/10.1145/3798268
[52] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun Li, Shing-Chi Cheung, and Cong Tian.
     2024. Enchanting Program Specification Synthesis by Large Language Models Using Static Analysis and Program
     Verification. In CAV (2) (Lecture Notes in Computer Science, Vol. 14682). Springer, 302–328. https://doi.org/10.1007/978-
     3-031-65630-9_16
[53] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui, Yeyun Gong, Chris Hawblitzel,
     Shuvendu Lahiri, Jacob R. Lorch, Shuai Lu, Fan Yang, Ziqiao Zhou, and Shan Lu. 2025. AutoVerus: Automated Proof
     Generation for Rust Code. Proc. ACM Program. Lang. 9, OOPSLA (2025), 3454–3482. https://doi.org/10.1145/3763174




Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: October 2026.
