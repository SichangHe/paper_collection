       Shape Analysis via Second-Order Bi-Abduction

     Quang Loc Le1 , Cristian Gherghina2, Shengchao Qin3 , and Wei-Ngan Chin1
             1
                 Department of Computer Science, National University of Singapore
                       2
                         Singapore University of Design and Technology
                                    3
                                      Teesside University


        Abstract. We present a new modular shape analysis that can synthesize heap
        memory specification on a per method basis. We rely on a second-order bi-
        abduction mechanism that can give interpretations to unknown shape predicates.
        There are several novel features in our shape analysis. Firstly, it is grounded on
        second-order bi-abduction. Secondly, we distinguish unknown pre-predicates in
        pre-conditions, from unknown post-predicates in post-condition; since the former
        may be strengthened, while the latter may be weakened. Thirdly, we provide a
        new heap guard mechanism to support more precise preconditions for heap spec-
        ification. Lastly, we formalise a set of derivation and normalization rules to give
        concise definitions for unknown predicates. Our approach has been proven sound
        and is implemented on top of an existing automated verification system. We show
        its versatility in synthesizing a wide range of intricate shape specifications.


1 Introduction
An important challenge for automatic program verifiers lies in inferring shapes describ-
ing abstractions for data structures used by each method. In the context of heap ma-
nipulating programs, determining the shape abstraction is crucial for proving memory
safety and is a precursor to supporting functional correctness.
   However, discovering shape abstractions can be rather challenging, as linked data
structures span a wide variety of forms, from singly-linked lists, doubly-linked lists,
circular lists, to tree-like data structures. Previous shape analysis proposals have made
great progress in solving this problem. However, the prevailing approach relies on us-
ing a predefined vocabulary of shape definitions (typically limited to singly-linked list
segments) and trying to determine if any of the pre-defined shapes fit the data struc-
tures used. This works well with programs that use simpler shapes, but would fail for
programs which use more intricate data structures. An example is the method below
(written in C and adapted from [19]) to build a tree whose leaf nodes are linked as a list.
  struct tree { struct tree∗ parent; struct tree∗ l; struct tree∗ r; struct tree∗ next}
  struct tree∗ tll(struct tree∗ x, struct tree∗ p, struct tree∗ t)
  { x->parent = p;
    if (x->r==NULL) { x->next=t; return x; }
    else{ struct tree∗ lm = tll(x->r, x, t); return tll(x->l, x, lm); } }
Our approach to modular shape analysis would introduce an unknown pre-predicate
H (as the pre-condition), and an unknown post-predicate G (as the post-condition), as
shown below, where res is the method’s result.
                     requires     H(x, p, t)       ensures     G(x, p, res, t)


A. Biere and R. Bloem (Eds.): CAV 2014, LNCS 8559, pp. 52–68, 2014.

c Springer International Publishing Switzerland 2014
                                         Shape Analysis via Second-Order Bi-Abduction            53

    Using Hoare-style verification and a new second-order bi-abduction entailment
procedure, we would derive a set of relational assumptions for the two unknown pred-
icates. These derived assumptions are to ensure memory safety, and can be systemat-
ically transformed into concise predicate definitions for the unknown predicates, such
as:         H(x,p,t) ≡ x→tree(Dp ,Dl ,r,Dn ) ∧ r=NULL
                        ∨ x→tree(Dp ,l,r,Dn )∗H(l,x,lm)∗H(r,x,t) ∧ r = NULL
              G(x,p,res,t) ≡ x→tree(p,Dl ,r,t) ∧ res=x∧r=NULL
                       ∨ x→tree(p,l,r,Dn )∗G(l,x,res,lm)∗G(r,x,lm,t)∧r=NULL
                                          The derived pre-predicate H captures a bi-
                                       nary tree-like shape that would be traversed by
                                       the method. x→tree(Dp ,Dl ,r,Dn ) denotes that x
                                       refers to a tree node with its parent,l,r and next
                                       fields being Dp , Dl , r and Dn , respectively. We use
  Fig. 1. An example of G(x,p,res,t)   dangling references, such as Dl , Dp , Dn , as generic
markers that denote field pointers that are not traversed by the method. Thus no asser-
tion can be made on any of the D pointers. The post-predicate G, illustrated in Fig 1,
adds parent field links for all nodes, and next field links for just the leaves. 1
   Current shape analysis mechanisms [12,4,6] are unable to infer pre/post specifica-
tions that ensure memory-safety for such complex examples. In this paper, we propose
a fresh approach to shape analysis that can synthesize, from scratch, a set of shape ab-
stractions that ensure memory safety. The central concept behind our proposal is the use
of unknown predicates (or second-order variables) as place holders for shape predicates
that are to be synthesized directly from proof obligations gathered by our verification
process. Our proposal is based on a novel bi-abductive entailment that supports second-
order variables. The core of the new entailment procedure generates a set of relational
assumptions on unknown predicates to ensure memory safety. These assumptions are
then refined into predicate definitions, by predicate derivation and normalization steps.
   By building the generation of the required relational assumptions over unknown
predicates directly into the new entailment checker, we were able to integrate our shape
analysis into an existing program verifier with changes made only to the entailment
process, rather than the program verification/analysis itself. Our proposed shape analy-
sis thus applies an almost standard set of Hoare rules in constructing proof obligations
which are discharged through the use of a new second-order bi-abductive entailment.
   This paper makes the following four primary contributions.
 – A novel second-order bi-abduction guided by an annotation scheme to infer rela-
   tional assumptions (over unknown predicates) as part of Hoare-style verification.
 – A set of formal rules for deriving and normalizing each unknown predicate defini-
   tion from the relational assumptions with heap guard conditions.
 – A sound and modular shape analysis, that is applied on a per method basis2 .
 – Our implementation and experiments on shape inference, closely integrated into an
   automated verification system. The report [21] contains more details of our tool.
 1
     Note that new links formed by the method are colored in red.
 2
     Most existing shape analyses require either global analyses or re-verification after analysis.
     For example, bi-abduction in [6] requires its method’s inferred pre-condition to be re-verified
     due to its use of over-approximation on heap pre-condition which can be unsound.
54      Q.L. Le et al.

2 Logic Syntax for Shape Specification
Separation logic is an extension of Hoare logic for reasoning with heap-based programs
[20,28]. We outline below the fragment underlying the proposed analysis:
              Disj. formula     Φ ::= Δ | Φ1 ∨ Φ2
              Guarded Disj.     Φg ::= Δ | (Δ @ (κ∧π)) | Φg 1 ∨ Φg 2
              Conj. formula     Δ ::= ∃v̄·(κ∧π)
              Spatial formula κ ::= emp | | v→c(v̄) | P(v̄) | U(v̄) | κ1 ∗κ2
              Pure formula      π ::= α | ¬α | π1 ∧π2
              Var (Dis)Equality α ::= v|v1 =v2 |v=NULL|v1 =v2 |v=NULL
              Pred. Defn.       Pdef::= P(v̄) ≡ Φg
              Pred. Dict.       Γ ::= {Pdef
                                          1 , . . . , Pn }
                                                       def

                    P ∈ Known Predicates U ∈ Unknown Predicates
                    c ∈ Data Nodes            v ∈ Variables v̄ ≡ v1 . . .vn

We introduce Δ @ (κ∧π), a special syntactic form called guarded heap that capture a
heap context κ∧π in which Δ holds. Thus, Δ @ (κ∧π) holds for heap configurations
that satisfy Δ and that can be extended such that they satisfy Δ ∗ κ∧π. In Sec.5 we
will describe its use in allowing our shape inference to incorporate path sensitive infor-
mation in the synthesized predicates. The assertion language is also extended with the
following formula for describing heaps: emp denoting the empty heap;  denoting an
arbitrary heap (pointed by dangling reference); points-to assertion, x→c(v̄), specifying
the heap in which x points to a data structure of type c whose fields contain the values
v̄; known predicate, P(v̄), which holds for heaps in which the shape of the memory
locations reachable from v̄ can be described by the P predicate; unknown predicates,
U(v̄), with no prior given definitions. Separation conjunction κ1 ∗κ2 holds for heaps that
can be partitioned in two disjoint components satisfying κ1 and κ2 , respectively. The
pure formula captures only pointer equality and disequality. We allow a special constant
NULL to denote a pointer which does not point to any heap location. Known predicates
P(v̄) are defined inductively through disjunctive formulas Φg . Their definitions are ei-
ther user-given or synthesised by our analysis. We will use Γ to denote the repository
(or set) of available predicate definitions. Through our analysis, we shall construct an
inductive definition for each unknown predicate, where possible. Unknown predicates
that have not been instantiated would not have any definition. They denote data fields
that are not accessed by their methods, and would be marked as dangling pointers.

3 Overview of Our Approach
Our approach comprises three main steps: (i) inferring relational assumptions for un-
known predicates via Hoare-style verification, (ii) deriving predicates from relational
assumptions, (iii) normalizing predicates. For (i), a key machinery is the entailment
procedure that must work with second-order variables (unknown predicates). Previous
bi-abduction entailment proposals, pioneered by [6], would take an antecedent Δante
and a consequent Δconseq and return a frame residue Δframe and the precondition Δpre ,
such that the following holds: Δpre ∗Δante  Δconseq ∗Δframe . Here, all four components
use separation logic formulas based on known predicates with prior definitions.
                                     Shape Analysis via Second-Order Bi-Abduction        55

   Taking a different tact, we start with an existing entailment procedure for separation
logic with user-defined predicates, and extend it to accept formulas with second-order
variables such that given an antecedent Δante and a consequent Δconseq the resulting
entailment procedure infers both the frame residue Δframeand a set (or conjunction) of
relational assumptions (on unknowns) of the form R = ni=1 (Δi ⇒ Φg i ) such that:
                               R ∧ Δante  Δconseq ∗Δframe

 The inferred R ensures the entailment’s validity. We shall use the following notation
Δante   Δconseq ; (R, Δframe ) for this second-order bi-abduction process.
   There are two scenarios to consider for unknown predicates: (1) Δante contains an
unknown predicate instance that matched with a points-to or known predicate in Δconseq ;
(2) Δconseq contains an unknown predicate instance. An example of the first scenario is:
                U(x)   x→snode(n) ; (U(x)⇒x→snode(n)∗U0 (n), U0 (n))

 Here, we generated a relational assumption to denote an unfolding (or instantiation)
for the unknown predicate U to a heap node snode followed by another unknown U0 (n)
predicate. The data structure snode is defined as struct snode { struct snode∗ next}.
A simple example of the second scenario is shown next.
x→snode(NULL)∗y→snode(NULL)        U1 (x) ; (x→snode(NULL)⇒U1 (x), y→snode(NULL))

 The generated relational assumption depicts a folding process for unknown U1 (x) which
captures a heap state traversed from the pointer x. Both folding and unfolding of un-
known predicates are crucial for second-order bi-abduction. To make it work properly
for unknown predicates with multiple parameters, we shall later provide a novel #-
annotation scheme to guide these processes. For the moment, we shall use this annota-
tion scheme implicitly. Consider the following method which traverses a singly-linked
list and converts it to a doubly-linked list (let us ignore the states α1 , .., α5 for now):
struct node { struct node∗ prev; struct node∗ next}
void sll2dll(struct node∗ x, struct node∗ q)
{(α1 ) if (x==NULL) (α2 ) return; (α3 ) x->prev = q; (α4 ) sll2dll(x->next, x); (α5 )}
   To synthesize the shape specification for this method, we introduce two unknown
predicates, H for the pre-condition and G for the post-condition, as below.
                       requires     H(x, q)       ensures    G(x, q)
 We then apply code verification using these pre/post specifications with unknown pred-
icates and attempt to collect a set of relational assumptions (over the unknown predi-
cates) that must hold to ensure memory-safety. These assumptions would also ensure
that the pre-condition of each method call is satisfied, and that the coresponding post-
condition is ensured at the end of the method body. For example, our analysis can infer
four relational assumptions for the sll2dll method as shown in Fig. 2(a).
   These relational assumptions include two new unknown predicates, Hp and Hn , cre-
ated during the code verification process. All relational assumptions are of the form
Δlhs ⇒Δrhs , except for (A3) which has the form Δlhs ⇒Δrhs @ Δg where Δg denotes
a heap guard condition. Such heap guard condition allows more precise pre-conditions
to be synthesized (e.g. Hn in (A3)), and is shorthand for Δlhs ∗Δg ⇒Δrhs ∗Δg .
   Let us look at how relational assumptions are inferred. At the start of the method, we
have (α1 ), shown in Fig. 2 (b), as our program state. Upon exit from the then branch, the
56       Q.L. Le et al.


  (A1).H(x, q) ∧ x=NULL ⇒ G(x,q)                 (α1 ). H(x,q)
  (A2).H(x, q) ∧ x=NULL ⇒                       (α2 ). H(x, q)∧x=NULL
       x→node(xp , xn )∗Hp (xp , q)∗Hn (xn , q) (α3 ). x→node(xp ,xn )∗Hp (xp ,q)∗Hn (xn ,q)∧x=NULL
  (A3).Hn (xn , q) ⇒ H(xn , x) @ x→node(q, xn ) (α4 ). x→node(q, xn )∗Hp (xp , q)∗Hn (xn , q)∧x=NULL
  (A4).x→node(q,xn )∗G(xn ,x) ⇒ G(x,q)          (α5 ). x→node(q, xn )∗Hp (xp , q)∗G(xn , x)∧x=NULL
                 (a)                                           (b)

              Fig. 2. Relational assumptions (a) and program states (b) for sll2dll

verification requires that the postcondition G(x, q) be established by the program state
(α2 ), generating the relational assumption (A1) via the following entailment:

      (α2 )   G(x,q) ; (A1, emp ∧ x=NULL)                                                     (E1)

 To get ready for the field access x->prev, the following entailment is invoked to unfold
the unknown H predicate to a heap node, generating the relational assumption (A2):
     H(x, q)∧x=NULL       x→node(xp ,xn ) ; (A2, Hp (xp ,q)∗Hn (xn ,q) ∧ x=NULL)            (E2)

Two new unknown predicates Hp and Hn are added to capture the prev (xp ) and next
(xn ) fields of x (i.e. they represent heaps referred to by xp and xn respectively). After
binding, the verification now reaches the state (α3 ), which is then changed to (α4 ) by
the field update x->prev = q. Relational assumption (A3) is inferred from proving the
precondition H(xn ,x) of the recursive call sll2dll(x->next, x) at the program state (α4 ):
     (α4 )    H(xn , x) ; (A3, x→node(q,xn )∗Hp (xp ,q)∧x=NULL)                              (E3)

 Note that the heap guard x→node(q, xn ) from (α4 ) is recorded in (A3), and is crucial for
predicate derivation. The program state at the end of the recursive call, (α5 ), is required
to establish the post-condition G(x, q), generating the relational assumption (A4):
     (α5 )    G(x,q) ; (A4, Hp (xp ,q)∧x=NULL)                                                (E4)

    These relational assumptions are automatically inferred symbolically during code
verification. Our next step (ii) uses a predicate derivation procedure to transform (by
either equivalence-preserving or abductive steps) the set of relational assumptions into
a set of predicate definitions. Sec. 5 gives more details on predicate derivation. For our
sll2dll example, we initially derive the following predicate definitions (for H and G):

               H(x, q) ≡ emp ∧ x=NULL ∨ x→node(xp , xn ) ∗ Hp (xp , q) ∗ H(xn , x)
               G(x, q) ≡ emp ∧ x=NULL ∨ x→node(q, xn ) ∗ G(xn , x)

 In the last step (iii), we use a normalization procedure to simplify the definition of
predicate H. Since Hp is discovered as a dangling predicate, the special variable Dp cor-
responds to a dangling reference introduced: H(x, q) ≡ emp ∧x=NULL ∨x→node(Dp , xn )∗
H(xn , x). Furthermore, we can synthesize a more concise H2 from H by eliminating its
useless q parameter: H(x, q) ≡ H2 (x) and H2 (x) ≡ emp∧x=NULL∨x→node(Dp , xn )∗H2 (xn ).
   Our approach currently works only for shape abstractions of tree-like data structures
with forward and back pointers. (We are unable to infer specifications for graph-like
or overlaid data structures yet.) These abstractions are being inferred modularly on a
per method basis. The inferred preconditions are typically the weakest ones that would
                                      Shape Analysis via Second-Order Bi-Abduction         57

ensure memory safety, and would be applicable to all contexts of use. Furthermore, the
normalization step aims to ensure concise and re-useable predicate definitions. We shall
next elaborate and formalise on our second-order bi-abduction process.


4 Second-Order Bi-Abduction with an Annotation Scheme
We have seen the need for a bi-abductive entailment procedure to systematically han-
dle unknown predicates. To cater to predicates with multiple parameters, we shall use
an automatic #-annotation scheme to support both unfolding and folding of unknown
predicates. Consider a predicate U(v1 , .., vn , w1 #, .., wm #), where parameters v1 , .., vn
are unannotated and parameters w1 , .., wm are #-annotated. From the perspective of un-
folding, we permit each variable from v1 , .., vn to be instantiated at most once (we
call them instantiatable), while variables w1 , .., wm are disallowed from instantiation
(we call them non-instantiatable). This scheme ensures that each pointer is instanti-
ated at most once, and avoids formulae, like U3 (y, y) or U2 (r, y)∗U3 (y, x#), from being
formed. Such formulae, where a variable may be repeatedly instantiated, may cause a
trivial FALSE pre-condition to be inferred. Though sound, it is imprecise. From the per-
spective of folding, we allow heap traversals to start from variables v1 , .., vn and would
stop whenever references to w1 , .., wm are encountered. This allows us to properly infer
segmented shape predicates and back pointers. Our annotation scheme is fully auto-
mated, as we would infer the #-annotation of pre-predicates based on which parameters
could be field accessed; while parameters of post-predicates are left unannotated. For
our running example, since q parameter is not field accessed (in its method’s body), our
automatic annotation scheme would start with the following pre/post specification:
              requires     H(x, q#)        ensures    G(x, q)
Unfold. The entailment below results in an unfolding of the unknown H predicate. It is
essentially (E2) in Sec 3, except that q is marked explicitly as non-instantiatable.
         H(x, q#)∧x=NULL     x→node(xp , xn ) ; (A2, Δ1 )              (E2 )
With non-instantiatable variables explicitly annotated, the assumption (A2) becomes:
            A2 ≡ H(x, q#)∧x=NULL ⇒ x→node(xp , xn )∗Hp (xp , q#)∗Hn (xn , q#)
 As mentioned earlier, we generated a new unknown predicate for each pointer field (Hp
for xp , and Hn for xn ), so as to allow the full recovery of the shape of the data structure
being traversed or built. Note that each x, xp , xn appears only once in unannotated forms,
while the annotated q# remains annotated throughout to prevent the pointer from being
instantiated. If we allow q to be instantiatable in (E2 ) above, we will instead obtain:
                      H(x, q)∧x=NULL    x→node(xp , xn ) ; (A2 , Δ1 )
  We get A2 ≡ H(x, q)∧x=NULL ⇒ x→node(xp , xn )∗Hp (xp , q#)∗Hn (xn , q#)∗U2 (q, x#),
where the unfolding process creates extra unknown predicate U2 (q, x#) to capture shape
for q.
   Our proposal for instantiating unknown predicates is also applicable when known
predicates appear in the RHS. These known predicates may have parameters that act
as continuation fields for the data structure. An example is the list segment lseg(x, p)
predicate where the parameter p is a continuation field.
                   ll(x) ≡ emp∧x=NULL ∨ x→snode(n) ∗ ll(n)
                   lseg(x, p) ≡ emp∧x=p ∨ x→snode(n) ∗ lseg(n, p)
58          Q.L. Le et al.

 Where snode (defined in the previous section) denotes singly-linked list node. Note
that continuation fields play the same role as fields for data nodes. Therefore, for such
parameters, we also generate new unknown parameters to capture the connected data
structure that may have been traversed. We illustrate this with two examples:

     U(x)    ll(x) ; (U(x)⇒ll(x), emp)   U(x)   lseg(x, p) ; (U(x)⇒lseg(x, q)∗U2 (q), U2 (p))


The first predicate ll(x) did not have a continuation field. Hence, we did not generate
any extra unknown predicate. The second predicate lseg(x, p) did have a continua-
tion field p, and we generated an extra unknown predicate U2 (p) to capture a possible
extension of the data structure beyond this continuation field.
Fold. A second scenario that must be handled by second-order entailment involves
unknown predicates in the consequent. For each unknown predicate U1 (v̄, w̄#) in the
consequent, a corresponding assumption Δ⇒U1 (v̄, w̄#) @ Δg is inferred where Δ con-
tains unknown predicates with at least one instantiatable parameters from v̄, or heaps
reachable from v̄ (via either any data fields or parameters of known predicates) but
stopping at non-instantiatable variables w̄#; a residual frame is also inferred from the
antecedent (but added with pure approximation of footprint heaps [9]). For example,
consider the following entailment:
                x→snode(q)∗q→snode(NULL)∧q=NULL          U1 (x, q#) ; (Af1 , Δ1 )
The output of this entailment is:
      Af1 ≡ x→snode(q)∧q=NULL⇒U1 (x, q#)         Δ1 ≡ q→snode(NULL)∧x=NULL∧x=q
As a comparison, let us consider the scenario where q is unannotated, as follows:
                 x→snode(q)∗q→snode(NULL)∧q=NULL          U1 (x, q) ; (Af2 , Δ2 )
In this case, the output of the entailment becomes:
      Af2 ≡ x→snode(q)∗q→snode(NULL) ⇒ U1 (x, q) Δ2 ≡ x=NULL∧q=NULL∧x=q
 Moreover, the folding process also captures known heaps that are reachable from #-
parameters as heap guard conditions, e.g. x→node(q, xn ) in our running example (E3):
x→node(q,xn )∗Hp (xp ,q#)∗Hn (xn ,q#)∧x=NULL H(xn , x#)
  ; (Hn (xn , q#) ⇒ H(xn , x#) @ x→node(q, xn ), x→node(q,xn )∗Hp (xp ,q#)∧x=NULL) (E3 )

 Such heap guards help with capturing the relations of heap structures and recovering
those relationships when necessary (e.g. back-pointer x#).
Formalism. Bi-abductive unfold is formalized in Fig. 3. Here, slice(w̄, π) is an aux-
iliary function that existentially quantifies in π all free variables that are not in the set w̄.
                        [SO-ENT-UNFOLD]                           Thus it eliminates from π all
                  κs ≡ r→c(p̄) or κs ≡ P(r, p̄)                  subformulas not related to w̄
 κfields = ∗pj ∈p̄ Uj (pj , v̄i #, v̄n #), where Uj : fresh preds (e.g. slice({x, q}, q=NULL∧y>3)
   κrem = Urem (v̄i , v̄n #, r#), where Urem : a fresh pred       returns q=NULL). In the first
 πa = slice({r, v̄i , v̄n , p̄}, π1 ) πc = slice({p̄}, π2 )       line, a RHS assertion, either a
    σ ≡ (U(r, v̄i , v̄n #) ∧ πa ⇒ κs ∗κfields ∗κrem ∧ πc )        points-to assertion r→c(p̄) or a
     κ1 ∗ κf ields ∗κrem ∧ π1 κ2 ∧ π2 ; (R, ΔR )                  known predicate instance P(r, p̄)
    U(r, v̄i , v̄n #)∗κ1 ∧π1 κs ∗κ2 ∧π2 ; (σ∧R, ΔR )              is paired through the parameter
                                                                  r with the unknown predicate U.
                  Fig. 3. Bi-Abductive Unfolding                  Second, the unknown predicates
                                       Shape Analysis via Second-Order Bi-Abduction            59

Uj are generated for the data fields/parameters of κs . Third, the unknown predicate Urem
is generated for the instantiatable parameters v̄i of U. The fourth and fifth lines compute
relevant pure formulas and generate the assumption, respectively. Finally, the unknown
predicates κfields and κrem are combined in the residue of LHS to continue discharging
the remaining formula in RHS.
     Bi-abductive fold is formalized in Fig. 4. The function reach(w̄, κ1 ∧π1 , z̄#) extracts
portions from the antecedent heap (κ1) that are (1) unknown predicates containing at least
one instantiatable parameter from w̄; or (2) point-to or known predicates reachable from
w̄, but not reachable from z̄. In our running example (the entailment (E3 ) on last page),
the function reach({xn }, x→node(q, xn )∗Hp (xp , q#)∗Hn (xn , q#)∧x=NULL, {x#}) is used to
obtain Hn (xn , q#). More detail on this function is in the report [21]. The heaps(Δ) func-
tion enumerates all known predicate instances (of the form P(v̄)) and points-to instances
(of the form r→c(v̄))) in Δ. The function root(κ) is defined as: root(r→c(v̄)))={r},
root(P(r, v̄)) = {r}. In the first line, heaps of LHS are separated into the assumption
                                                                    κ11 and the residue κ12 .
                            [SO-ENT-FOLD]
         κ11 =reach(w̄, κ1 ∧π1 , z̄#) ∃κ12 · κ1 =κ                  Second, heap guards (and
                                                      11 ∗κ12
 κg = ∗{κ | κ∈heaps(κ12 )∧root(κ)⊆z̄} r̄= κ∈κg root(κ) their root pointers) are in-
   σ ≡ (κ11 ∧slice(w̄, π1 ) ⇒ Uc (w̄, z̄#) @ κg ∧slice(r̄, π1 ))    ferred based on κ12 and
                   κ12 ∧ π1 κ2 ∧ π2 ; (R, ΔR )                      the #-annotated parameters
          κ1 ∧ π1 Uc (w̄, z̄ #) ∗ κ2 ∧ π2 ; (σ∧R, ΔR )              z̄. The assumption is gen-
                                                                    erated in the third line and
                    Fig. 4. Bi-Abductive Folding                    finally, the residual heap is
                                                                    used to discharge the re-
maining heaps of RHS.
Hoare Rules. We shall now present Hoare rules to show how second-order entailment is
used there. For simplicity, we consider a core imperative language (Fig. 5) that supports
heap-based data structures (datat) and methods (meth).
 Prog ::= datat∗ meth∗ datat ::= data c { field∗ }              A method declaration includes a
 field ::= t v t ::= int | bool | void | c | . . .              header with pre-/post-condition
 meth ::= t mn (([ref] t v)∗ ) Φpr Φpo ; {e}                    and its body. Methods can
 e      ::= NULL | kτ | v | v.f | v=e | v.f =e | new c(v ∗ )    have call-by-reference parame-
           | e1 ; e2 | t v; e | mn(v ∗ )| if v then e1 else e2 ters (prefixed with ref). Loops,
                                                                including nested loops, are trans-
                   Fig. 5. The Core Language
                                                                formed to tail-recursive methods
with ref parameters to capture mutable variables. To support shape analysis, code ver-
ification is formalized as a proof of quadruple: {Δpre } e {R, Δpost }, where R accu-
mulates the set of relational assumptions generated by the entailment procedure. The
specification may contain unknown predicates in preconditions and postconditions. We
list in Fig. 6 the rules for field access, method calls and method declaration. Note that
primed variable (e.g. x ) denotes the latest value (of the program variable x). The for-
mula Δ1 ∗v̄ Δ2 denotes ∃r̄· ([r̄/v̄ ]Δ1 ) ∗([r̄/v̄]Δ2 ) (see [9]).
     The key outcome is that if a solution for the set of relational assumptions R can be
found, the program is memory-safe and all the methods abide by their specifications.
Furthermore, we propose a bottom-up verification process which is able to incremen-
tally build suitable predicate instantiations one method at a time by solving the collected
60       Q.L. Le et al.

                                             [SA-CALL]
                 t0 mn ((ref ti vi )m−1i=1 , (tj vj )j=m ) Φpr Φpo ; {e} ∈ Prog
                                                     n

              ρ=[vk /vk ]nk=1 Φpr = ρ(Φpr ) W={v       1 , .., vm−1 } V={vm , .., vn }
                Δ Φpr ; (R, Δ2 ) Δ3 =(Δ2 ∧ ni=m (vi = vi )) ∗V∪W Φpo
                              {Δ} mn(v1 , .., vm−1 , vm , .., vn ) {R, Δ3 }
                      [SA-FLD-RD]                                        [SA-METH]
           data c {t1 f1 , .., tn fn } ∈ Prog                      {Φpr ∧ (u =u)∗ } e {R1 , Δ1 }
           Δ1 x →c(v1 ..vn ) ; (R, Δ3 )                            Δ1 Φpo ; (R2 , Δ2 )
      Δ4 =∃v1 ..vn · (Δ3 ∗x →c(v1 ..vn )∧res=vi )                  Γ = solve(R1 ∪R2 )
                   {Δ1 } x.fi {R, Δ4 }                             t0 mn ((t u)∗ ) Φpr Φpo {e}
                                    Fig. 6. Several Hoare Rules

relational assumptions R progressively. The predicate definition synthesis (solve) con-
sists of two separate operations : predicate synthesis, PRED SYN, and predicate normal-
ization, PRED NORM. That is solve(R) = PRED NORM(PRED SYN(R)). After the method
is successfully verified, the resulting predicate definitions Γ provide an interpretation
for the unknown predicates appearing in the specifications such that memory safety is
guaranteed. By returning Γ, the method verification allows the inferred definitions and
specifications to be consistently reused in the verification of the remaining methods.

5 Derivation of Shape Predicates
Once the relational assumptions have been inferred, we proceed to apply a series of
refinement steps to derive predicate definitions for each pre- and post-predicate. Fig. 7
                                                              outlines our strategy for pred-
    function PRED SYN( R)
                                                              icate synthesis. We use the
     Γ ←∅
                                                              [syn-∗] notation to name re-
     R ← exhaustively apply [syn-base] on R
     Rpre , Rpost ← sort-group(R)                             finement rules. For space rea-
     while Rpre =∅ do                                        sons, we describe some rules
      U , σ ← pick unknown & assumption in Rpre
       pre                                                    and leave the rest to the re-
      Upre
       def ←   apply     [syn-case ],  [syn-group-pre  ], and port [21]. Steps that are left out
         [syn-pre-def ] on σ                                  include: (i) sort-group to de-
      Rpre , Rpost ← inline Upre  def in (Rpre \σ), Rpost     cide on the transformation or-
      discharge Upre obligations                              der of relational assumptions;
      Γ ← Γ ∪ {Upre   def }                                   (ii) rules to process some re-
     end while                                                lational assumptions as proof
     while Rpost =∅ do
                                                              obligations. For example, if the
      Upost , σ ← pick unknown & assumption in Rpost
                                                              result of the recursive method is
      Udef ← apply[syn-group-post ], [syn-post-def ] on σ
       post

      discharge U   post
                          obligations                         field-accessed after the recursive
      Rpost ← Rpost \ σ             Γ ← Γ ∪ {Udef }
                                                  post        call, the post-predicate would
     end while                                                appear as an unknown predicate
     return Γ                                                 for heap instantiation. This must
    end function                                              be processed as an entailment
              Fig. 7. Shape Derivation Outline                obligation, after the definition of
                                                              its post-predicate has been de-
rived; (iii) inline to unfold synthesized predicates in the remaining assumptions.
                                      Shape Analysis via Second-Order Bi-Abduction           61

5.1 Base Splitting of Pre/Post-Predicates
We first deal with relational assumptions of the form Upre (. . .)∗Δ ⇒ Upost (. . .), which
capture constraints on both a pre-predicate and a post-predicate. To allow greater flexi-
bility in applying specialized techniques for pre-predicates or post-predicates, we split
the assumption into two assumptions such that pre-predicate Upre is separated from post-
predicate Upost . Base splitting can be formalized as follows:
                                              [syn-base]
  σ : Upre (x̄)∗κ∧π ⇒ Upost (ȳ) σ1 : Upre (x̄)∧slice(x̄, π)⇒emp        σ2 : κ∧π ⇒ Upost (ȳ)
          κg =∗{κ1 | κ1 ∈heaps(κ)∧pars(κ1 )∩x̄=∅}            w̄= {pars(κ1 ) | κ1 ∈κg }
                σ3 : Upre (x̄)⇒Ufr (x̄) @ κg ∧slice(x̄∪w̄, π)    σ4 : Ufr (x̄) ⇒
                  if is base(x̄, π)=true then (σ1 ∧σ2 ) else (σ∧σ3 ∧σ4 )
The premise contains an assumption (σ ) which could be split. The conclusion captures
the new relational assumptions. There are two scenarios:
(1) The first scenario takes place when the test is base(x̄, π) holds. It signifies that π
contains a base case formula for some pointer(s) in x̄. Note that is base(x̄, π) holds if
and only if (∃ v∈x̄. π v=NULL) or (∃v1 ,v2 ∈x̄.π v1 =v2 ). In such a situation, the as-
sumption σ is split into σ1 and σ2 . This reflects the observation that a pre-predicate
guard will likely constrain the pre-predicate to a base-case with empty heap. This sce-
nario happens in our running example where the assumption (A1) is split to:
         (A1a). H(x, q) ∧ x=NULL ⇒ emp             (A1b). emp ∧ x=NULL ⇒ G(x,q)

(2) If the test is base(x̄, π) fails, there is no base case information available for us to
instantiate Upre (x̄). The assumption σ is not split and kept in the result. To have a more
precise derivation, we would also record the fact that Upre (x̄) has no instantiation under
the current context. To do this, in the second line we record in κg such a heap context (re-
lated to x̄), extract in w̄ related pointers from the context, and introduce a fresh unknown
predicate Ufr as the instantiation for Upre , as indicated by the assumption σ3 in the third
line. Note the heap guard specifies the context under which such an assumption holds.
We also add σ4 into the result, where the new predicate Ufr is instantiated to the afore-
mentioned memory locations (encapsulated by ). Assumptions of the form Ufr (p) ⇒
are being used to denote dangling pointers. We also note that introducing the dangling
predicate Ufr into the guarded assumption σ3 is essential to help relate non-traversed
pointer fields between the pre-predicate Upre and the post-predicate Upost . The function
pars(κ) (the 2nd line) retrieves parameters: pars(r→c(v̄))) = v̄, pars(P(r, v̄)) = v̄.
   As an example, consider splitting (σ5 ) : Upre (p)∗x→node(p,n)∧n=NULL ⇒ Upost (x).
The test is base({p}, n=NULL) fails. In addition to (σ5 ), the splitting returns also
     (σ6 ) : Upre (p) ⇒ Ufr (p) @ (x→node(p,n)∧n=NULL)              (σ7 ) : Ufr (p) ⇒

5.2 Deriving Pre-Predicates
Pre-predicates typically appear in relational assumptions under pure guards π, of the
form Upre (. . .)∧π ⇒ Δ. To derive definitions for these pre-predicates, the first step is to
transform relational assumptions that overlap on their guards by forcing a case analysis
that generates a set of relational assumptions with disjoint guard conditions:
                                      [syn-case]
              U(x̄)∧π1 ⇒Δ1 @ Δ1g U(x̄)∧π2 ⇒Δ2 @ Δ2g π1 ∧π2 ⇒FALSE
                       Δ1 ∧Δ2 ⇒x̄∧ Δ3 Δ1g ∧Δ2g ⇒x̄∧ Δ3g SAT(Δ3g )
 U(x̄)∧π1 ∧¬π2 ⇒Δ1 @ Δ3g          U(x̄)∧π2 ∧¬π1 ⇒Δ2 @ Δ3g          U(x̄)∧π1 ∧π2 ⇒Δ3 @ Δ3g
62        Q.L. Le et al.

 For brevity, we assume a renaming of free variables to allow x̄ to be used as arguments
in both assumptions. Furthermore, we use the ⇒x̄∧ operator to denote a normalization
of overlapping conjunction, Δ1 ∧Δ2 [28]. Informally, in order for Δ1 ∧ Δ2 to hold, it
is necessary that the shapes described by Δ1 and Δ2 agree when describing the same
memory locations. Normalization thus determines the overlapping locations, Δc such
that Δ1 =Δc ∗Δ1 and Δ2 =Δc ∗Δ2 and returns Δc ∗Δ1 ∗Δ2 . We leave a formal defini-
tion of ⇒x̄∧ to the technical report [21]. Once all the relational assumptions for a given
pre-predicate have been transformed such that the pure guards do not overlap, we may
proceed to combine them using the rule [syn-group-pre] shown below. We shall perform
this exhaustively until a single relational assumption for U is derived. If the assump-
tion RHS is independent of any post-predicate, it becomes the unknown pre-predicate
definition, as shown in the rule [syn-pre-def ] below.
                      [syn-group-pre ]                                  [syn-pre-def ]
 U(x̄)∧π1 ⇒ Φg1      U(x̄)∧π2 ⇒ Φg2 π1 ∧π2 ⇒ FALSE            Upre (x̄)⇒Φg       no post(Φg )
           U(x̄) ∧ (π1 ∨π2 ) ⇒ Φg1 ∧π1 ∨ Φg2 ∧π2                       Upre (x̄) ≡ Φg

     For the sll2dll example, applying the [syn-group-pre] rule to (A2) and (A1a) yields:
            (A5). H(x, q) ⇒ x→node(xp , xn )∗Hp (xp , q)∗Hn (xn , q) ∨ emp ∧ x=NULL

  This is then trivially converted into a definition for its pre-predicate, without any
weakening, thus ensuring soundness of our pre-conditions.

5.3 Deriving Post-Predicates
We start the derivation for a post-predicate after all pre-predicates have been derived.
We can incrementally group each pair of relational assumptions on a post-predicate via
the [syn-group-post] rule shown below. By exhaustively applying [syn-group-post] rule all
assumptions relating to predicate Upost get condensed into an assumption of the form:
Δ1 ∨ . . . ∨ Δn ⇒ Upost (x̄). This may then be used to confirm the post-predicate by
generating the predicate definition via the [syn-post-def ] rule.
                     [syn-group-post]                         [syn-post-def ]
             Δa ⇒ Upost (x̄)   Δb ⇒ Upost (x̄)         Δ1 ∨ . . . ∨ Δn ⇒ Upost (x̄)
                    Δa ∨ Δb ⇒ Upost (x̄)              Upost (x̄) ≡ Δ1 ∨ . . . ∨ Δn

 Using these rules, we can combine (A4) and (A1b) in the sll2dll example to obtain:
                    G(x, q) ≡ emp ∧ x=NULL ∨ x→node(q, xn ) ∗ G(xn , x)

5.4 Predicate Normalization for More Concise Definitions

After we have synthesized suitable predicate definitions, we proceed with predicate
normalization to convert each predicate definition to its most concise form. Our current
method, PRED NORM, uses four key steps: (i) eliminate dangling predicates, (ii) elim-
inate useless parameters, (iii) re-use predicate definitions and (iv) perform predicate
splitting. We briefly explain the normalization steps and leave details in the report [21].
The first step deals with dangling predicates which do not have any definition. Though
it is safe to drop such predicates (by frame rule), our normalization procedure replaces
them by special variables, to help capture linking information between pre- and post-
conditions. The second step eliminates predicate arguments that are not used in their
                                         Shape Analysis via Second-Order Bi-Abduction            63

synthesized definitions, with the help of second-order entailment. The third step lever-
age on our entailment procedure to conduct an equivalence proof to try to match a newly
inferred definition with a definition previously provided or inferred. Lastly, to increase
the chance for such predicate reuse, we allow predicates to be split into smaller predi-
cates. This is again done with the help of second-order entailment procedure, allowing
us to undertake such normalization tasks soundly and easily.

6 Soundness Lemmas and Theorem
Here we briefly state several key soundness results, and leave the proof details to the
report [21]. For brevity, we introduce the notation R(Γ) to denote a set of predicate in-
stantiations Γ={U1 (v̄1 )≡Δ1 , ..Un (v̄n )≡Δn } satisfying the set of assumptions R. That is, for
all assumptions Δ ⇒ Φg ∈ R, (i) Γ contains a predicate instantiation for each unknown
predicate appearing in Δ and Φg ; (ii) by interpreting all unknown predicates according
to Γ, then it is provable that Δ implies Φg , written as Γ : Δ Φg .
Soundness of Bi-abductive Entailment. Abduction soundness requires that if all the
relational assumptions generated are satisfiable, then the entailment is valid.
Lemma 1. Given the entailment judgement Δa Δc ; (R, Δf ), if there exists Γ such
that R(Γ), then the entailment Γ : Δa Δc ∗ Δf holds.
Derivation Soundness. For derivation soundness, if a set of predicate definitions is con-
structed then those definitions must satisfy the initial set of assumptions. We argue that
(i) assumption refinement does not introduce spurious instantiations, (ii) the generated
predicates satisfy the refined assumptions, (iii) normalization is meaning preserving.
Lemma 2. Given a set of relational assumptions R, let R be the set obtained by ap-
plying any of the refinement steps, then for any Γ such that R (Γ), we have R(Γ).
Lemma 3. If R contains only one pre-assumption on predicate Upre ,Upre (v̄)⇒Φg and
if our algorithm returns a solution Γ, then (Upre (v̄)≡Φg )∈ Γ. Similarly, if R has a sole
post-assumption on Upost , Φ⇒Upost and if solution Γ is returned, then (Upost (v̄)≡Φ)∈ Γ.

Lemma 4. Given a set of assumptions R, if PRED SYN(R) returns a solution Γ then
R(Γ). Furthermore, if PRED NORM(Γ) returns a solution Γ then R(Γ ).

Theorem 6.1 (Soundness) If Δa             Δc ; (R, Δf ) and Γ=PRED NORM(PRED SYN(R)) then
Γ : ΔaΔc ∗ Δf .

7 Implementation and Experimental Results
We have implemented the proposed shape analysis within HIP [9], a separation logic
verification system. The resulting verifier, called S2, uses an available CIL-based [27]
translator 3 from C to the expression-oriented core language. Our analysis modularly
infers the pre/post specification for each method. It attempts to provide the weakest
possible precondition to ensure memory safety (from null dereferencing and memory
leaks), and the strongest possible post-condition on heap usage patterns, where possible.
Expressivity. We have explored the generality and efficiency of the proposed analy-
 3
     Our translation preserves the semantics of source programs, subject to CIL’s limitations.
64         Q.L. Le et al.

                    Table 1. Experimental Results (c for check and t for traverse)

                 w/o norm. w/ norm.                         w/o norm. w/ norm.
      Example                        Veri.     Example                          Veri.
                 size Syn. size Syn.                        size Syn. size Syn.
  SLL (delete)    9 0.23 2 0.29 0.22           CSLL (t)      8 0.22 5 0.23 0.24
 SLL (reverse)    20 0.21 8 0.22 0.2 CSLL of CSLLs (c) 18 0.24 4 0.23 0.22
   SLL (insert)   13 0.2 11 0.21 0.2          SLL2DLL        18 0.19 2 0.2 0.18
  SLL (setTail)   7 0.16 2 0.18 0.16        DLL (check)      8 0.21 2 0.23 0.19
 SLL (get-last) 20 0.7 17 0.75 0.21        DLL (append)      11 0.2 8 0.2 0.2
 SLL-sorted (c) 11 0.26 2 0.27 0.22           CDLL (c)       23 0.22 8 0.26 0.21
SLL (bubblesort) 13 0.28 9 0.36 0.26 CDLL of 5CSLLs (c) 28 0.39 4 0.66 1.3
SLL (insertsort) 15 0.3 11 0.3 0.27 CDLL of CSLLs2 (c) 29 0.33 4 0.44 0.29
    SLL (zip)     20 0.27 2 0.32 0.24       btree (search)   33 0.23 2 0.24 0.23
   SLL-zip-leq    20 0.27 2 0.27 0.25      btree-parent (t)  11 0.23 2 0.29 0.24
 SLL + head (c) 12 0.24 2 0.71 0.2           rose-tree (c)   14 0.28 14 0.3 0.23
  SLL + tail (c)  10 0.19 2 0.72 0.18           swl (t)      19 0.23 13 0.27 22
  skip-list2 (c)  9 0.28 1 0.32 0.25            mcf (c)      19 0.26 17 0.28 0.26
  skip-list3 (c)  9 0.36 1 0.46 0.3              tll (t)     21 0.23 2 0.25 0.21
SLL of 0/1 SLLs 8 0.25 1 0.26 0.23               tll (c)     21 0.29 2 0.32 0.19
    CSLL (c)      17 0.18 2 0.23 0.21      tll (set-parent)  39 0.24 2 0.35 0.24




sis through a number of small but challenging examples. We have evaluated programs
which manipulate lists, trees and combinations (e.g. tll: trees whose leaves are chained
in a linked list). The experiments were performed on a machine with the Intel i7-960
(3.2GHz) processor and 16 GB of RAM. Table 1 presents our experimental results. For
each test, we list the name of the manipulated data structure and the effect of the veri-
fied code under the Example column. Here we used SLL,DLL,CLL,CDLL for singly-,
doubly-, cyclic-singly-, cyclic-doubly- linked lists. SLL + head/tail for an SLL where
each element points to the SLL’s head/tail. SLL of 0/1 SLLs uses an SLL nested in a
SLL of size 0 or 1, CSLL of CSLLs for CSLL nested in CSLL, CDLL of 5CSLLs for
an CDLL where each node is a source of five CSLL, and CDLL of CSLLs2 for CDLL
where each node is a nested CSLL. The skip lists subscript denotes the number of
skip pointers. The swl procedure implements list traversal following the DeutschSchorr-
Waite style. rose-trees are trees with nodes that are allowed to have variable number of
children, typically stored as linked lists, and mcf trees [16] are rose-tree variants where
children are stored in doubly-linked lists with sibling and parent pointers. In order to
evaluate the performance of our shape synthesis, we re-verified the source programs
against the inferred specifications and listed the verification time (in seconds) in the
Veri. column and the synthesis times in column Syn.. In total, the specification infer-
ence took 8.37s while the re-verification4 took 8.25s.
   The experiments showed that our tool can handle fairly complex recursive methods,
like trees with linked leaves. It can synthesize shape abstractions for a large variety of

 4
     Due to our use of sound inference mechanisms, re-verification is not strictly required. We
     perform it here to illustrate the benefit of integrating inference within a verification framework.
                                       Shape Analysis via Second-Order Bi-Abduction        65

data structures; from list and tree variants to combinations. Furthermore, the tool can
infer shapes with mutual-recursive definitions, like the rose-trees and mcf trees.
   The normalization phase aims to simplify inferred shape predicates. To evaluate its
effectiveness, we performed the synthesis on two scenarios: without (w/o) and with (w/)
normalization. The number of conjuncts in the synthesized shapes is captured with size
column. The results show that normalization is helpful; it reduces by 68% (169/533)
the size of synthesized predicates with a time overhead of 27% (8.37s/10.62s).
Larger Experiments. We evaluated S2 on real source code from the Glib open source
library [1]. Glib is a cross-platform C library including non-GUI code from the GTK+
toolkit and the GNOME desktop environment. We focused our experiments on
                                               the files which implemented heap data
                                               structures, i.e. SLL (gslist.c), DLL
                                 √
           LOC #Proc #Loop # Syn. (sec) (glist.c), balanced binary trees (gtree.c)
 gslist.c 698 33          18 47 11.73          and N-ary trees (gnode.c). In Fig.8 we list
  glist.c 784 35          19 49       7.43     for each file number of lines of code (ex-
 gtree.c 1204 36          14 44       3.69     cluding comments) LOC, number of pro-
 gnode.c 1128 37          27 52 16.34          cedures
                                                 √      (while/for loops) #Proc (#Loop).
                                               # describes the number of procedures
     Fig. 8. Experiments on Glib Programs      and loops for which S2 inferred specifi-
                                               cations that guarantee memory safety. S2
can infer specifications that guarantee memory safety for 89% of procedures and loops
(192/216).5
Limitations. Our present proposal cannot handle graphs and overlaid data structures
since our instantiation mechanism always expands into tree-like data structures with
back pointers. This is a key limitation of our approach. For an example, see the report
[21]. For future work, we also intend to combine shape analysis with other analyses
domains, in order to capture more expressive specifications, beyond memory safety.


8 Related Work and Conclusion
A significant body of research has been devoted to shape analysis. Most proposals are
orthogonal to our work as they focus on determining shapes based on a fixed set of shape
domains. For instance, the analysis in [26] can infer shape and certain numerical prop-
erties but is limited to the linked list domain. The analyses from [32,11,4,15,3,24] are
tailored to variants of lists and a fixed family of list interleavings. Likewise, Calcagno
et al. [7] describes an analysis for determining lock invariants with only linked lists.
Lee et al. [22] presents a shape analysis specifically tailored to overlaid data structures.
In the matching logic framework, a set of predicates is typically assumed for program
verification [31]. The work [2] extends this with specification inference. However, it
currently does not deal with the inference of inductive data structure abstractions.
   The proposal by Magill et al. [26] is able to infer numerical properties, but it is still
parametric in the shape domain. Similarly, the separation logic bi-abduction described
in [6,17] assumes a set of built-in or user-defined predicates. Xisa, a tool presented
 5
     Our current implementation does not support array data structures. Hence, some procedures
     like g tree insert internal cannot be verified.
66      Q.L. Le et al.

by Rival et. al. [8], works on programs with more varied shapes as long as structural
invariant checkers, which play the role of shape definitions, are provided. A later ex-
tension [30] also considers shape summaries for procedures with the additional help of
global analysis. Other similarly parameterized analysis includes [13]. In comparison,
our approach is built upon the foundation of second-order bi-abductive entailment, and
is able to infer unknown predicates from scratch or guided by user-supplied assertions.
This set-up is therefore highly flexible, as we could support a mix of inference and
verification, due to our integration into an existing verification system.
   With respect to fully automatic analyses, there are [5], [16] and the Forester system
[18]. Although very expressive in terms of the inferred shape classes, the analysis pro-
posed by Guo et al. [16] relies on a heavy formalism and depends wholly on the shape
construction patterns being present in the code. They describe a global analysis that
requires program slicing techniques to shrink the analyzed code and to avoid noise on
the analysis. Furthermore, the soundness of their inference could not be guaranteed;
therefore a re-verification of the inferred invariants is required. Brotherston and Goro-
giannis [5] propose a novel way to synthesize inductive predicates by ensuring both
memory safety and termination. However, their proposal is currently limited to a sim-
ple imperative language without methods. A completely different approach is presented
in the Forrester system [18] where a fully automated shape synthesis is described in
terms of graph transformations over forest automata. Their approach is based on learn-
ing techniques that can discover suitable forest automata by incrementally constructing
shape abstractions called boxes. However, their proposal is currently restricted both in
terms of the analysed programs, e.g. recursion is not yet supported, and in terms of the
inferred shapes, as recursive nested boxes (needed by tll) are not supported.
   In the TVLA tradition, [29] describes an interprocedural shape analysis for cut-free
programs. The approach explores the interaction between framing and the reachability-
based representation. Other approaches to shape analysis include grammar-based infer-
ence, e.g. [23] which relies on inferred grammars to define the recursive backbone of
the shape predicates. Although [23] is able to handle various types of structures, e.g.
trees and dlls, it is limited to structures with only one argument for back pointers. [25]
employs inductive logic programming (ILP) to infer recursive pure predicates. While, it
might be possible to apply a similar approach to shape inference, there has not yet been
any such effort. Furthermore, we believe a targeted approach would be able to easily
cater for the more intricate shapes. Since ILP has been shown to effectively synthesize
recursive predicates, it would be interesting to explore an integration of ILP with our
proposal for inferring recursive predicates of both shape and pure properties. A recent
work [14] that aims to automatically construct verification tools has implemented vari-
ous proof rules for reachability and termination properties however it does not focus on
the synthesis of shape abstractions. In an orthogonal direction, [10] presents an analy-
sis for constructing precise and compact method summaries. Unfortunately, both these
works lack the ability to handle recursive data structures.
Conclusion. We have presented a novel approach to modular shape analysis that can
automatically synthesize, from scratch, a set of shape abstractions that are needed for
ensuring memory safety. This capability is premised on our decision to build shape
predicate inference capability directly into a new second-order bi-abductive entailment
                                       Shape Analysis via Second-Order Bi-Abduction           67

procedure. Second-order variables are placeholders for unknown predicates that can
be synthesized from proof obligations gathered by Hoare-style verification. Thus, the
soundness of our inference is based on the soundness of the entailment procedure it-
self, and is not subjected to a re-verification process. Our proposal for shape analysis
has been structured into three key stages: (i) gathering of relational assumptions on un-
known shape predicates; (ii) synthesis of predicate definitions via derivation; and (iii)
normalization steps to provide concise shape definitions. We have also implemented a
prototype of our inference system into an existing verification infrastructure, and have
evaluated on a range of examples with complex heap usage patterns.
Acknowledgement. We thank Quang-Trung Ta for his C front-end integration. We
gratefully acknowledge the support of research grant MOE2013-T2-2-146.


References

 1. Glib-2.38.2 (2013), https://developer.gnome.org/glib/ (accessed November
    13, 2013)
 2. Alpuente, M., Feliú, M.A., Villanueva, A.: Automatic inference of specifications using
    matching logic. In: PEPM, pp. 127–136 (2013)
 3. Berdine, J., Calcagno, C., Cook, B., Distefano, D., O’Hearn, P.W., Wies, T., Yang, H.: Shape
    analysis for composite data structures. In: Damm, W., Hermanns, H. (eds.) CAV 2007.
    LNCS, vol. 4590, pp. 178–192. Springer, Heidelberg (2007)
 4. Berdine, J., Cook, B., Ishtiaq, S.: S LAYER: Memory safety for systems-level code. In:
    Gopalakrishnan, G., Qadeer, S. (eds.) CAV 2011. LNCS, vol. 6806, pp. 178–183. Springer,
    Heidelberg (2011)
 5. Brotherston, J., Gorogiannis, N.: Cyclic abduction of inductively defined safety and termina-
    tion preconditions. Technical Report RN/13/14, University College London (2013)
 6. Calcagno, C., Distefano, D., O’Hearn, P.W., Yang, H.: Compositional shape analysis by
    means of bi-abduction. In: POPL, pp. 289–300 (2009)
 7. Calcagno, C., Distefano, D., Vafeiadis, V.: Bi-abductive resource invariant synthesis. In:
    Hu, Z. (ed.) APLAS 2009. LNCS, vol. 5904, pp. 259–274. Springer, Heidelberg (2009)
 8. Chang, B.-Y.E., Rival, X.: Relational inductive shape analysis. In: POPL, pp. 247–260 (2008)
 9. Chin, W.N., David, C., Nguyen, H.H., Qin, S.: Automated verification of shape, size and
    bag properties via user-defined predicates in separation logic. Sci. Comput. Program. 77(9),
    1006–1036 (2012)
10. Dillig, I., Dillig, T., Aiken, A., Sagiv, M.: Precise and compact modular procedure summaries
    for heap manipulating programs. In: PLDI, pp. 567–577 (2011)
11. Distefano, D., O’Hearn, P.W., Yang, H.: A local shape analysis based on separation logic.
    In: Hermanns, H., Palsberg, J. (eds.) TACAS 2006. LNCS, vol. 3920, pp. 287–302. Springer,
    Heidelberg (2006)
12. Dudka, K., Peringer, P., Vojnar, T.: Predator: A practical tool for checking manipulation of
    dynamic data structures using separation logic. In: Gopalakrishnan, G., Qadeer, S. (eds.)
    CAV 2011. LNCS, vol. 6806, pp. 372–378. Springer, Heidelberg (2011)
13. Gotsman, A., Berdine, J., Cook, B.: Interprocedural Shape Analysis with Separated Heap
    Abstractions. In: Yi, K. (ed.) SAS 2006. LNCS, vol. 4134, pp. 240–260. Springer, Heidelberg
    (2006)
14. Grebenshchikov, S., Lopes, N.P., Popeea, C., Rybalchenko, A.: Synthesizing software veri-
    fiers from proof rules. In: PLDI, pp. 405–416 (2012)
68       Q.L. Le et al.

15. Gulavani, B.S., Chakraborty, S., Ramalingam, G., Nori, A.V.: Bottom-up shape analysis. In:
    Palsberg, J., Su, Z. (eds.) SAS 2009. LNCS, vol. 5673, pp. 188–204. Springer, Heidelberg
    (2009)
16. Guo, B., Vachharajani, N., August, D.I.: Shape analysis with inductive recursion synthesis.
    In: PLDI, pp. 256–265 (2007)
17. He, G., Qin, S., Chin, W.-N., Craciun, F.: Automated specification discovery via user-defined
    predicates. In: Groves, L., Sun, J. (eds.) ICFEM 2013. LNCS, vol. 8144, pp. 397–414.
    Springer, Heidelberg (2013)
18. Holik, L., Lengál, O., Rogalewicz, A., Šimáček, J., Vojnar, T.: Fully automated shape analysis
    based on forest automata. In: Sharygina, N., Veith, H. (eds.) CAV 2013. LNCS, vol. 8044,
    pp. 740–755. Springer, Heidelberg (2013)
19. Iosif, R., Rogalewicz, A., Simacek, J.: The tree width of separation logic with recursive defi-
    nitions. In: Bonacina, M.P. (ed.) CADE 2013. LNCS (LNAI), vol. 7898, pp. 21–38. Springer,
    Heidelberg (2013)
20. Ishtiaq, S., O’Hearn, P.W.: BI as an Assertion Language for Mutable Data Structures. In:
    ACM POPL, London (January 2001)
21. Le, Q.L., Gherghina, C., Qin, S., Chin, W.N.: Shape analysis via second-order bi-abduction.
    In Technical Report, Soc, NUS (February 2014), http://loris-7.ddns.comp.nus.
    edu.sg/˜project/s2/beta/src/TRs2.pdf
22. Lee, O., Yang, H., Petersen, R.: Program analysis for overlaid data structures. In: Gopalakr-
    ishnan, G., Qadeer, S. (eds.) CAV 2011. LNCS, vol. 6806, pp. 592–608. Springer, Heidelberg
    (2011)
23. Lee, O., Yang, H., Yi, K.: Automatic verification of pointer programs using grammar-based
    shape analysis. In: Sagiv, M. (ed.) ESOP 2005. LNCS, vol. 3444, pp. 124–140. Springer,
    Heidelberg (2005)
24. Lev-Ami, T., Sagiv, M., Reps, T., Gulwani, S.: Backward analysis for inferring quantified
    preconditions. Technical Report TR-2007-12-01, Tel Aviv University (2007)
25. Loginov, A., Reps, T., Sagiv, M.: Abstraction Refinement via Inductive Learning. In:
    Etessami, K., Rajamani, S.K. (eds.) CAV 2005. LNCS, vol. 3576, pp. 519–533. Springer,
    Heidelberg (2005)
26. Magill, S., Tsai, M.-H., Lee, P., Tsay, Y.-K.: Automatic numeric abstractions for heap-
    manipulating programs. In: POPL, pp. 211–222 (2010)
27. Necula, G., McPeak, S., Rahul, S., Weimer, W.: CIL: Intermediate Language and Tools for
    Analysis and Transformation of C Programs. In: Horspool, R.N. (ed.) CC 2002. LNCS,
    vol. 2304, pp. 213–228. Springer, Heidelberg (2002)
28. Reynolds, J.: Separation Logic: A Logic for Shared Mutable Data Structures. In: IEEE LICS,
    pp. 55–74 (2002)
29. Rinetzky, N., Sagiv, M., Yahav, E.: Interprocedural shape analysis for cutpoint-free pro-
    grams. In: Hankin, C., Siveroni, I. (eds.) SAS 2005. LNCS, vol. 3672, pp. 284–302. Springer,
    Heidelberg (2005)
30. Rival, X., Chang, B.-Y.E.: Calling context abstraction with shapes. In: POPL, pp. 173–186
    (2011)
31. Rosu, G., Stefanescu, A.: Checking reachability using matching logic. In: OOPSLA,
    pp. 555–574. ACM (2012)
32. Yang, H., Lee, O., Berdine, J., Calcagno, C., Cook, B., Distefano, D., O’Hearn, P.W.: Scalable
    shape analysis for systems code. In: Gupta, A., Malik, S. (eds.) CAV 2008. LNCS, vol. 5123,
    pp. 385–398. Springer, Heidelberg (2008)
