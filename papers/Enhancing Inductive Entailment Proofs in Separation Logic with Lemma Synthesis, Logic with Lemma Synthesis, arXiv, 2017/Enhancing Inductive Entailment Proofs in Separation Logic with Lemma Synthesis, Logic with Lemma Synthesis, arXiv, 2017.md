                                             Enhancing Inductive Entailment Proofs in Separation
                                                        Logic with Lemma Synthesis

                                                                                  Quang Loc Le ⋆
arXiv:1710.06515v2 [cs.PL] 12 May 2018




                                                                              Teesside University, UK



                                                 Abstract. This paper presents an approach to lemma synthesis to support ad-
                                                 vanced inductive entailment procedures based on separation logic. We first pro-
                                                 pose a mechanism where lemmas are automatically proven and systematically ap-
                                                 plied. Our lemmas may include universal guard and/or unknown predicate. While
                                                 the former is critical for expressivity, the latter is essential for supporting rela-
                                                 tionships between multiple predicates. We further introduce lemma synthesis to
                                                 support (i) automated inductive reasoning together with frame inference and (ii)
                                                 theorem exploration. For (i) we automatically discover and prove auxiliary lem-
                                                 mas during an inductive proof; and for (ii) we automatically generate a useful set
                                                 of lemmas to relate user-defined or system-generated predicates. We have imple-
                                                 mented our proposed approach into an existing verification system and tested its
                                                 capability in inductive reasoning and theorem exploration. The experimental re-
                                                 sults show that the enhanced system can automatically synthesize useful lemmas
                                                 to facilitate reasoning on a broad range of non-trivial inductive proofs.

                                                 Keywords: Lemma Synthesis, Induction Proving, Theorem Exploration, Sepa-
                                                 ration Logic, User-Defined Predicate.


                                         1 Introduction

                                         Separation logic (SL) [20,36] has been well established for reasoning about heap-based
                                         programs. Frame rule in SL enables modular (compositional) reasoning in the presence
                                         of the heap and is essential for scalability [22,43,10]. In the last decade, a large num-
                                         ber of proof systems for SL have been studied [4,7,10,18,11,27]. Generally speaking,
                                         the key challenges of these systems are to support bi-abduction (automated frame in-
                                         ference [4,11] and logical abduction [10,24,42]), and automated induction proving [7]
                                         in SL fragments with inductive predicates. While the use of general inductive predi-
                                         cates attains expressive power, a powerful entailment procedure supporting the induc-
                                         tive predicates needs to meet the following two main challenges.
                                             Induction Reasoning. Entailment checks involving inductive predicates normally
                                         require induction. For an indirect solution, existing works employed lemmas that are
                                         consequences of induction. These lemmas were either hardwired for a set of predefined
                                         predicates (i.e. lists [4]), or automatically generated (for normalization of shape analysis
                                         [24], or for some predefined classes of predicates [17]). While these lemma approaches
                                         ⋆
                                             This work was done in part when the author was a PhD student in National University of
                                             Singapore.
can handle induction reasoning for some specific predicates, they could not support in-
duction in general proofs. Brotherston et. al. make an important step towards automating
general induction reasoning in SL with cyclic entailment proofs [7,9]. Recently, authors
in [12] managed induction by a framework with historical proofs. However, these proof
systems [7,12] did not consider frame inference. Thus, they provide limited support for
the frame rule as well as modular verification.
     Completeness. Past works introduce decision procedures for SL decidable frag-
ments including hardwired lists [4,5,14,31], or even user-defined predicates with some
syntactic restrictions [18]. However, the SL fragment with (arbitrary) user-defined pred-
icates (and arithmetic constraints) is, in general, undecidable. Entailment procedures for
this general fragment typically trade off completeness for expressiveness [7,11,16,27].
To enhance the completeness of program verification, there have been efforts of ex-
ploring relations between predicates via user-supplied lemmas [4,7,9,16,22,30]. While
such a static approach puts creative control back into the users’ hands, it is not fully
automatic and is infeasible to support inductive proofs relying on auxiliary lemmas of
dynamically synthesized predicates (like those in [8,24]).
     In this work, we propose an approach to lemma synthesis for advanced induc-
tive proofs in a SL fragment with user-defined predicates and Presburger arithmetic.
Our technical starting point is an entailment procedure for user-defined predicates (i.e.
those procedures in the spirit of [11]) combined with second-order bi-abduction [24].
We extend this proof system with a new mechanism where lemmas are automatically
generated, proven and systematically applied. Finally, we apply lemma synthesis into
theorem exploration.
     Frame inference has been studied in SL entailment procedures like [4,11,32]. Intu-
itively, these systems prove validity of an entailment ∆a ⊢∆c by unfolding user-defined
predicates, subtracting heap predicates until halting at sequents with empty heap (i.e.
the emp predicate in SL) in the consequent, such that ∆f ⊢emp∧πr and then, conclude
the entailment is valid with the frame ∆f , denoted by ∆a ⊢∆c ❀ ∆f . However, these
systems did not provide a direct solution for general induction proofs. We tackle this
challenging of frame inference for inductive entailment proofs via the new lemma sys-
thesis. Our key insight is that the entailment check ∆a ⊢∆c ❀∆f is semantically equiv-
alent to the check ∆a ⊢∆c ∗∆f ❀emp. To infer frame for inductive entailment checks
like the former, we will prove the latter check inductively while inferring frame ∆f
abductively. Concretely, we assume frame as an unknown predicate U, construct the
conjecture lemma l1 :∆a →∆c ∗U, and finally inductively prove this lemma and abduc-
tively infer a definition of the predicate U. The benefit of the use of lemma synthesis
in our approach is twofold. First, our proposed approach is easily integrated into exist-
ing proof systems with lemma mechanism i.e. [30,16]. Second, the synthesized lemmas
(i.e. l1 ) are accumulated for reuse in future.
     Lemmas in our system may include universally quantified guards and unknown
predicates. We will use the notation ∆[v̄] to stand for a formula with free variables v̄.
Our lemmas with universal guards 1 have the form ∀v̄ · H(v̄)∧G(v̄) → B(v̄) whereas
universal guard G and body B may include unknown predicates whose definitions need
to be inferred. While guards over universal variables make our mechanism very ex-
 1
     We will refer lemma with universal guard as universal lemma.


                                               2
pressive, unknown predicates enable us to synthesize generic lemmas i.e. those with
weak(est) guards and strong(est) bodies. The meaning of lemmas is interpreted in clas-
sic semantics [20] i.e. for the lemma above ∀v̄ · H(v̄)∧G(v̄) |= B(v̄); the LHS exactly
entails the RHS (with empty heap in residue). Our lemma proving is based on the prin-
ciple of cyclic proof [7,9], and can support induction proving. For universal lemma
synthesis, given the entailment check ∃ē·∆a ∧G(ē) ⊢ ∆c , our system would generate
the lemma lemma l2 : ∀ē·∆a ∧P(ē) → ∆c , whereas P is a newly-inferred predicate.
    Our predicate inference mechanism is based on the principle of second-order bi-
abduction (SOBD), for shape domain [24] and for pure (non-shape) domains [42], which
is an extension of bi-abduction [10] to user-defined predicates. A SOBD entailment pro-
cedure takes two SL formulas ∆ante and ∆conseq as inputs. It infers missing hypotheses
R? and residual frame ∆f rame ?. R? is a set of Horn clause-based constraints over un-
known variables of ∆ante and ∆conseq . These constraints have the form of logical im-
plication i.e. ∆L ⇒∆R . The set R? can be solved to obtain definitions of the unknown
predicates by the algorithms in [24,42].
    In inductive reasoning, theory exploration is a technique for automatically gener-
ating and proving useful lemmas for sets of given functions, constants and datatypes
[13,23,28]. In our context, theory exploration is meant for discovering useful lemmas
for a set of given user-defined predicates. In SL, this technique was indeed presented
[4,17]. Like [17] and unlike [4], our approach is automation-based. Different from these,
our technique is capable of generating lemmas with newly-inferred user-defined predi-
cates i.e. those that are synthesized while proving the lemmas.
    The novelty of our proof system is the lemma synthesis with predicate inference.
Our primary contributions are summarized as follows:
 – We propose a new mechanism where universal lemmas are soundly synthesized
   and systematically applied.
 – We synthesize lemmas to support inductive proofs together with frame inference
   and theorem exploration.
 – We have implemented the proposal in an entailment procedure, called S, and in-
   tegrated S into a modular verification. Our experiments on sophisticated inductive
   proofs show that our approach is promising for advancing state-of-the-art in auto-
   mated verification of heap-manipulating programs.


2 Motivation and Overview

2.1 Entailment Procedure using Universal Lemma Synthesis

We extend an entailment procedure with basic inference rules (i.e. [7,11]) to inference
capability with the second-order bi-abduction (SOBD) mechanism [24] and a new lemma
mechanism. This lemma mechanism enhances the inference rules with a set of external
and proven lemmas L. These lemmas can be initially supplied by users as well as ad-
ditionally and dynamically synthesized while the entailment is proven. The enhanced
entailment procedure is formalized as follows: ∆ante ⊢L ∆conseq ❀ (R, ∆frame ) such
that: L∧R∧∆ante |= ∆conseq ∗∆f rame . Consequently, inference rules of the starting
system are using the augmented lemmas L in the new system as the following:

                                           3
                    ∆l1 ⊢ ∆r1 ❀ (R1 ,∆R1 ) ... ∆li ⊢ ∆ri ❀ (Ri ,∆Ri )
                                  ∆1 ⊢ ∆2 ❀ (R,∆R )
                     ∆l1 ⊢L ∆r1 ❀ (R1 ,∆R1 ) ... ∆li ⊢L ∆ri ❀ (Ri ,∆Ri )
                 =⇒                   ∆1 ⊢L ∆2 ❀ (R,∆R )

For a standard proof system for SL with inductive predicates, please refer to [11]. (A
summary is presented in App. A.) We shall propose [LAPP] and [LAPP−∀] rules for
lemma application (Sec. 4), [LSYN] rule for lemma synthesis, [R∗] rule for heap split,
and [AU], [AF], [AU−P], [AF−P] rules for predicate inference (Sec. 5).
   To illustrate how our proof system can support induction reasoning together with
complex frame inference, consider the following entailment check VC0
                             ll last(t,t′ )∗ll(y) ⊢∅ t′ 7→c1 (q)
 pred ll(root)≡emp∧root=null ∨ ∃q·root7→c1 (q)∗ll(q)
 pred ll last(root,s)≡root7→c1 (null)∧root=s ∨ ∃q·root7→c1 (q)∗ll last(q,s);
whereas struct c1 {c1 ∗ next; }. VC0 is a verification condition generated to verify
memory safety of programs that access the last element (i.e. g list append in glist.c
of GLIB library [1] - see App. C.2). In the predicate definitions above, we use basic
SL notations to express heaps, e.g. empty predicate (i.e. emp), points-to predicate (i.e.
root7→c1 (p) asserts a concrete heap cell bound with an allocated data type c1 , pointed-
to by the variable root and linked with downstream pointer p via the field next).
    To infer frame for this inductive entailment check, we assume the frame be a un-
known predicate, i.e. U2 (t,t′ #,q,y), and form the following conjecture:
                lemma c: ll last(t,t′ )∗ll(y) → t′ 7→c1 (q)∗U2 (t,t′ #,q,y)
Then, we prove its validity and infer a set of relational assumptions as:
                      σ1 : ∗ll(y)∧t′ =t∧q=null ⇒ U2 (t,t′ ,q,y)
                      σ2 : t7→c1 (q1 )∗U2 (q1 ,t′ ,q2 ,y) ⇒ U2 (t,t′ ,q2 ,y)
From σ1 and σ2 , we synthesize the following definition for U2
   U2 (root,t′ ,q,y)≡ll(y)∧root=t′ ∧q=null ∨ ∃ q1 · root7→c1 (q1 )∗U2 (q1 ,t′ ,q,y);
Finally, using theorem exploration presented in Sec 6 ( and App. B), we generate the
following two-way separating lemmas 2 to normalize the predicate U2 :
           lemma conseq0:U2 (root,t′ ,q,y) ↔ U3 (root,t′ )∗ll(y)∧q=null
           U3 (root,t′ )≡emp∧root=t′ ∨ ∃ q1 · root7→c1 (q1 )∗U3 (q1 ,t′ );
To sum up, our system successfully proves and derives U3 (t,t′ )∗ll(y)∧q=null as
frame of VC0 . We present an example for universal lemma synthesis in App. C.1.

2.2 Modular Verification with Lemma Synthesis
                                  In modular verification of heap-based programs,
1 void check(struc c2 ∗ a)
                                  specifications of recursive methods and loop in-
2 { while(a->val==1)a=a->next;
                                  variants normally relate to recursive predicates;
3 while(a->val==2)a=a->next;
                                  consequently, compositionally verifying these
4 assert a->val==3;
                                  specifications requires both induction reason-
5 return; }
                                  ing and frame inference. Our proposed approach
    Fig. 1. Code of method check.
                                  brings the best support for such verification.
 2
     We refer A↔B as two-way lemma, a short form of two reverse lemmas: A→B and B→A.


                                           4
    Consider the code fragment in Fig. 1. This code fragment checks whether list seg-
ment pointed by a is decomposed into three regions: a list segment of 1 values (the
while loop at line 2), a list segment of 2 values (the while loop at line 3), and a 3-value
node (the assertion at line 4). We assume that the method check (while loop at line 2,
line 3) has been supplied with the s1 (s2 , and s3 resp.) specification as:
(s1 ) requires ls1(a,p1 )∗ls2(p1 ,p2 )∗p2 7→c2 (3, null) ensures true ;
(s2 ) requires ls1(a,p3 )∗p3 7→c2 (v1 ,p4 )∧v1 6=1 ensures ls1(a,p3 )∗p3 7→c2 (v1 ,p4 )∧a′ =p3 ;
(s3 ) requires ls2(a,p5 )∗p5 7→c2 (v2 ,p6 )∧v2 6=2 ensures ls2(a,p5 )∗p5 7→c2 (v2 ,p6 )∧a′ =p5 ;

 whereas a′ is value of a after the loop; the data structure and the predicates ls1, ls2
are defined as: struct c2 {int val; struct c2 ∗ next; }
         pred ls1(root,s)≡emp∧root=s              pred ls2(root,s)≡emp∧root=s
         ∨ ∃ q· root7→c2 (1, q)∗ls1(q,s);         ∨ ∃q· root7→c2 (2,q)∗ls2(q,s);

 As a (bottom-up) modular verification, the loops are verified prior to the verification of
the method check; and the correctness of a method is reduced to the validity of appro-
priate verification conditions generated. Our system generates verification conditions
to ensure absence of memory errors (no null dereference, no double free and no mem-
ory leak), validity of functional calls/loops via compositional pre-/post- conditions and
post-conditions holding. For illustrating the proposed approach, we briefly discuss the
reasoning on the verification condition (VC1 ) that was generated before the loop at line
2 (to prove that the current context can imply the loop invariant):


    ls1(a,p1 )∗ls2(p1 ,p2 )∗p2 7→c2 (3, null) ⊢∅ ls1(a,p3 )∗p3 7→c2 (v1 ,p4 )∧v1 6=1

    (The lemma store L=∅ means there are no user-supplied lemmas.) VC1 requires both
induction reasoning (for the ls1a,p1 predicate) and frame inference to prove safety of
the rest of the program. Hence, this entailment is beyond the capability of most existing
SL verification systems (like [30,7,11,27,32]).
    Instead of instantiating and deducing a frame like [4,11], we assume frame as an un-
known predicate and infer this predicate via abduction. This inference was implemented
in the proposed inference rule [LSYN]. Concretely, the proof of VC1 is as follows:

     lemsyn(∆a , ∆c , ∅)❀(lemma l3 : ∆l → ∆r ∗U(root,p1 ,p2 ,p3 ,p4 ,v1 ),true )
       ls1(a,p1 )∗ls2(p1 ,p2 )∗p2 7→c2 (3, null) ⊢∅ ∆l [a/root] ❀ emp∧true
           ls1(a,p1 )∗ls2(p1 ,p2 )∗p2 7→c2 (3, null)
              ⊢∅ ls1(a,p3 )∗p3 7→c2 (v1 ,p4 )∗U(v̄)∧v1 6=1 ❀ (true ,U(v̄))

whereas U(w̄)≡U(a#,p1 ,p2 ,p3 #,p4 ,v1 ). The lemma l3 was synthesized as

        lemma l3 : ls1(root,p1 )∗ls2(p1 ,p2 )∗p2 7→c2 (3, null)
            → ls1(root,p3 )∗p3 7→c2 (v1 ,p4 )∗U(root,p1 ,p2 ,p3 ,p4 ,v1 )∧v1 6=1

      pred U(a,p1 ,p2 ,p3 ,root,v1 ) ≡ root=null∧a=p1 ∧p1 =p2 ∧a=p3 ∧v1 =3
        ∨ root7→c2 (v1′ , v4′ )∗U(a,p1 ,p2 ,p3 ,v4′ ,v1′ )∧a=p1 ∧a=p3 ∧v1 =2∧v1′ 6=1
The proof derived for the lemma l3 will be presented in detail in Sec 5.2.

                                              5
    For automation, we integrated the proposed proof system into S2 [24], a specifica-
tion inference system. Simultaneously, we enhanced S2 beyond the shape domain. We
show how the proposed lemma synthesis was integrated into a modular verification with
incremental specification inference over shape and size properties in App. C.3.


3 Preliminaries
A Fragment of Separation Logic. The syntax of the fragment is as follows.

   Φ ::= ∆ | Φ1 ∨ Φ2 ∆ ::= ∃v̄· (κ∧π) κ ::= emp | r7→c(t̄) | P(t̄) | U(t̄) | κ1 ∗κ2
   π ::= π∧φ | φ | p(t̄) φ ::= α | i | ∃v· φ | ∀v· φ | ¬φ | φ1 ∧φ2 | φ1 ∨φ2
       pred P(v̄)≡Φ(v̄)  c ∈ Data Types        ti , v, r ∈ Var   t̄ ≡ t1 , . . ., tn

A formula Φ can be a disjunctive formula (Φ1 ∨ Φ2 ). A conjunctive formula ∆ is con-
joined by spatial formula κ and pure formula π. All free variables are implicitly univer-
sally quantified at the outermost level. null is a special heap location. In the predicate
r7→c(t̄), r is a root variable. For abduction reasoning, our fragment also includes un-
known predicates, spatial (U(t̄)) and pure (p(t̄)) second-order variables, whose defini-
tions need to be inferred [24,42]. Pure formulas are constraints over (in)equality α (on
pointers), and Presburger arithmetic i. Note that v1 6=v2 and v6=null are short forms
for ¬(v1 =v2 ) and ¬(v=null), respectively. We occasionally use a sequence (i.e. t̄) to
denote a set when it is not ambiguous. We omit π when it is true . A formula without
any user-defined predicate instances is referred as a base formula.           Wn
User-Defined (UD) Predicate. A UD predicate P is defined as W    pred P(v̄)≡ i=1 (∃w̄i · ∆i );
                                                                   n
whereas P is predicate name. v̄ is a set of formal parameters. i=1 ∃w̄i · ∆i is a predicate
definition. ∃w̄i · ∆i (i ∈ 1...n) is a branch of the disjunction. In each branch, we require
that variables which are not in formal parameters must be existentially quantified.
                                                                     Wn
Definition 1 (Root Parameter) Given UD predicate P: P(v̄)≡ i=1 (∃w̄i · ∆i );, a pa-
rameter r∈v̄ is a root if for any base formula κ∧π derived by unfolding the predicate
instance P(v̄), r is either a root of a points-to predicate (r7→ occurs in κ) or r=null.

We syntactically detect root parameters as follows. A formal parameter r∈v̄ is a root
if any branch κi ∧πi , i∈{1...n}, one of the following four conditions holds: (i) r is a root
variable of a points-to predicate (r7→ occurs in κi ); (ii) r equals to null: πi =⇒ r=null;
(iii) r equals to another root parameter: πi =⇒ r=s, where s∈v̄; or (iv) r is a root pa-
rameter of another UD predicate. Without loss of generality, we will write P(r, v̄) to
indicate that r is a root parameter. A predicate with multiple root parameters will be
considered to transform into multiple predicates with single root parameter in Sec. 6.
Unfolding. The function unfold(∆, j) unfolds once the jth UD predicate instance, i.e.
Pj (t̄j ), of the formula ∆. The steps are formalized as follows:
               Wn                               ′          ′
    Pj (v̄)≡ i=1 (∃w̄i · κi ∧πi ) fresh w̄i ρi =[w̄i /w̄i ] κ′i = κi [ρi ] πi′ = πi [ρi ]
                          ρ0 =[t̄i /v̄]    κ′′i = κ′i [ρ0 ] πi′′ = πi′ [ρ0 ]
                                                   Wn              ′
            unfold(∃w̄0 · Pj (t̄j )∗κ0 ∧π0 , j) ❀ i=1 (∃w̄0 ∪w̄i · κ0 ∗ κ′′i ∧π0 ∧πi′′ )
First, the function looks up the definition of P, refreshes the existential quantifiers. Sec-
ond, formal parameters are substituted by the actual parameters. Finally, substituted

                                             6
definition is combined (and normalized) with residual formula as in the RHS of ❀. We
will refer to recursive predicate instances of unfolded heap formula κi as descendant
predicate instances (of the jth UD predicate instance).


4 Lemma Mechanism
Lemma Formalism. In general, lemmas in our system are formalized as:
                    lemma id: ∀v̄·∃w̄1 ·Rl ∗∆l (v̄) → ∃w̄2 ·Rr ∗∆r (v̄).
Our lemmas are used to relate two reachable heap regions starting from a same root
pointer of the root predicates Rl and Rr . A root predicate is a points-to or a UD predi-
cate. Without loss of generality, we require that the root pointer of a root predicate is
explicitly denoted with the preserved name root. For frame inference, LHS and RHS
must capture the same heaps (i.e. ∀v̄·∃w̄1 ·Rl ∗∆l (v̄) ⊢L ∃w̄2 ·Rr ∗∆r (v̄)❀( , emp∧π).
We occasionally use id to indicate the lemma.
Lemma Application. During proof search, proven lemmas are considered as external
inference rules. We assume that free variables of a lemma are renamed to avoid clashing
before the lemma is applied. The application of a lemma id is formalized as follows.
                                        [LAPP]
          (lemma id Rl ∗κl ∧G→∆r )∈L ∆1 ⊢L κl [ρ] ∧ G[ρ] ❀ (R1 , Φr1 )
                ρ = match(Rl , R1 )     Φr1 ∗∆r [ρ] ⊢L ∆2 ❀ (R2 , ΦR )
                            R1 ∗∆1 ⊢L ∆2 ❀ (R1 ∧R2 , ΦR )
The lemma id is applied into the above entailment through three steps. First, we match
the predicate R1 of the antecedent with root predicate Rl . (We note that Rl must contain
a root pointer.) Rl and R1 are matched and unified by a partial function match. If the
matching is successful, match produces substitutions as follows:
                   match(root7→c(t̄)), x7→c(w̄)) = [w̄/t̄] ◦ [x/root]
                   match(P(root,t̄), P(x,w̄))          = [w̄/t̄] ◦ [x/root]
Second, we prove guard and identify cut of the antecedent in the first line. Last, we
combine the residue of the antecedent with RHS of the lemma before continuously
proving the consequent (of the entailment) in the second line.
Universal  VLemma Application. The universal guard ∀G is equivalent to infinite con-
junction ρ G[ρ]. ∀G makes the lemmas with universal guard more expressive. How-
ever, it also prevents applying these lemmas into entailments with instantiated (existen-
tial) guards as the second step of the above lemma application rule could not be estab-
lished (i.e. ∃ x ∆ 6 ⊢∀ x ∆). While mechanism in [30] was based on “delayed guard”,
we now propose guard instantiation, a sound solution for universal lemma application.
In order to apply a universal lemma into an entailment with instantiated (existential)
guard, we present a technique that dynamically and intelligently instantiates universal
guard (of the lemma) before really deploying this lemma. Concretely, our technique will
substitute universal guard by a finite set of its instances. The soundness of this technique
is based on the following theorem.

Theorem 1 (Lemma Instantiation). Let ∆ante and ∆conseq be antecedent and con-
sequent of an entailment check. Let L be a set of universal lemmas and let L′ be a

                                             7
set of instantiated lemmas obtained by substituting each ∀v̄G(v̄) in a universal guard
by a finite conjunction of its instantiations. If ∆ante ⊢L′ ∆conseq is valid then so is
∆ante ⊢L ∆conseq .
Proof. Semantically, a guard with universal variables ∀v̄G(v̄) implies a conjunction of
its instantiations. As such universal guard ∀v̄G(v̄) is on the left-hand side of lemmas,
a proof system with inference rules L′ implies the corresponding proof system with
inference rules L. Thus, if ∆ante ⊢L′ ∆conseq is valid then so is ∆ante ⊢L ∆conseq . 
Inspired by quantifier instantiation in Simplify [15], we symbolically select “relevant”
instantiations over universal variables of a guard by looking up substitutions over the
universal variables such that the instantiated lemma suffices to prove the validity of a
given entailment. The substitutions are selected through shape predicate matching [11]
(the corresponding action used in [16] is subtracting.). The application of lemmas with
universal variables is formalized as:
                                     [ENT−LAPP−∀]
 (lemma id ∀v̄·Rl ∗∆l ∧G(v̄)→∆r )∈L ρ=ρm ◦ins(v̄) ∆1 ⊢L ∆l [ρ] ❀ (R1 , Φr1 )
 ρm =match(Rl , R1 ) Φr1 ∗∆r [ρ] ⊢L ∆2 ❀ (R2 , Φr2 ) Φr2 ⊢L G(v̄)[ρ] ❀ (R3 , ΦR )
                          R1 ∗∆1 ⊢L ∆2 ❀ (R1 ∧R2 ∧R3 , ΦR )
In the rule above, after head matching, we rename universal variables and obtain the
substitution by the function ins. This substitution helps to instantiate quantified vari-
ables in both universal guard of the lemma and existential guard of the antecedent.
    Symbolic “relevant” instantiations are selected during the course of the left entail-
ment at line 2 and are captured in the residue Φr2 . Finally, “relevant” instantiations are
used to prove the instantiated guard of the right entailment at line 2. We implement the
selection of the symbolic “relevant” instantiations via by instantiation mechanism in
[11]. We summarize the mechanism in App. A.


5 Automated Inductive Entailment Procedure
In Fig. 5, we propose new six inference rules; [R∗] is for cutting heaps; [LSYN] is for
dynamically generating and proving auxiliary lemmas; and the rest is for generating
relational assumptions while checking entailment. [R∗] rule, a revision (with frame in-
ference) of the Monotonicity rule [20], helps to generate smaller sub-goals, and then
to generate more reusable lemmas. In this rule, FV returns free variables of a formula.
Two necessary conditions to apply the rule [LSYN] are: (i) root predicates of the an-
tecedent (LHS) and the consequent (RHS), Ra and Rc , must share a same root pointer;
(ii) Rr must be a defined predicate instance i.e. P(x, w̄). Here, ▽(w̄, π) is an auxiliary
function that existentially quantifies in π all free variables that are not in the set w̄. We
present the lemsyn procedure in the subsection 5.1.
     In [AU] and [AF] rules, R(r,t̄) is either r7→c(t̄) or known (defined) P(r,t̄), or un-
known predicate U′ (r,t̄,w̄ #). We use # notation in unknown predicates to guide abduc-
tion and proof search. We only abduce on pointers without #-anotated. Uf (w̄, t¯′ ) is an-
other unknown predicate generated to capture downstream heaps. After abduced point-
ers will be annotated with # to avoid double abduction. New unknown predicate Uf is
only generated if at least one parameter is not annotated with # (i.e. w̄ ∪ t¯′ 6=∅). To avoid

                                              8
                                               [R∗]
     FV(∆c1 ) ∩ FV(∆c2 )={}            ∆a ⊢L ∆c1 ❀ (R1 , Φf1 )            Φf1 ⊢L ∆c2 ❀ (R2 , Φf2 )
                               ∆a ⊢L ∆c1 ∗∆c2 ❀ (R1 ∧R2 , Φf2 )
                                            [LSYN]
 lemsyn(Rl ∗κa ∧πa ,Rc ∗∆c ),L)❀(lemma l:∀v̄∀ē·Ra ∗κa ∧▽(v̄, πa )∧P(v̄, ē)→Rc ∗∆c ∗U(v̄),R)
                        ρm = match(Rl , Ra ) ρi =ins(ē) ρ=ρm ◦ρi
           (Ra ∗κa ∧πa )[ρi ] ⊢L (Ra ∗κa ∧▽(v̄, πa )∧P(v̄, ē))[ρ] ❀ (true , emp∧πf1 )
                                 ∀v̄∃ē·Ra ∗κa ∧πa ⊢L Rc ∗∆c ❀ (R, U(v̄)[ρ])
                                                           [AU]
                      σ ≡ U(r,w̄, z̄ #) ⇒ R(r,t̄)∗Uf (w̄, t¯′ , z̄ #, r #)∧▽(w̄ ∪ {r}, π1 )
            t¯′ = t̄ \ (w̄ ∪ z̄ ∪ {r})         Uf (w̄, t¯′ , z̄ #, r #)∗κ1 ∧π1 ⊢L κ2 ∧π2 ❀ (R, ∆f )
                          U(r, w̄, z̄ #)∗κ1 ∧π1 ⊢L R(r,t̄)∗κ2 ∧π2 ❀ (σ∧R, ∆f )
                                                            [AF]
                      σ ≡ R(r,t̄)∗Uf (w̄, t¯′ , z̄ #, r #)∧▽(w̄ ∪ {r}, π1 ) ⇒ U(r,w̄, z̄ #)
          t¯′ = t̄ \ (w̄ ∪ z̄ ∪ {t})        κ1 ∧ π1 ⊢L Uf (w̄, t¯′ , z̄ #, r #)∗κ2 ∧ π2 ❀ (R, ∆f )
                          R(r,t̄)∗κ1 ∧π1 ⊢L U(r, w̄, z̄ #)∗κ2 ∧π2 ❀ (σ∧R, ∆f )
                                                        [AU−P]
                π≡∀(FV(π1 ) ∪ FV(π2 ) \ w̄)¬π1 ∨π2                     π6=false       σ ≡ P(w̄) ⇒ π
                                  κ1 ∧P(w̄)∧π1 ⊢L emp∧π2 ❀ (σ, κ1 ∧π1 )
                                                        [AF−P]
                      π=XPure(κ1 )∧π1               π =⇒ π2               σ ≡ ▽(w̄, π) ⇒ P(w̄)
                                  κ1 ∧π1 ⊢L emp∧P(w̄)∧π2 ❀ (σ, κ1 ∧π1 )

              Fig. 2. Inference Rules for Lemma Synthesis with Predicate Inference.
conflict between abduction rules and other (unfolding, subtraction) during proof search,
all root pointers in a heap formula must be annotated with # in unknown predicates.
For examples, in our system while the formula x7→c1 (y)∗U1 (x#,y) is valid, the for-
mula x7→c1 (y)∗U1 (x, y) is invalid. For the check x7→c1 (null)⊢L x7→c1 (y)∗U1 (x#,y),
our proof search will apply subtraction the heap pointed by x rather than abdution. We
illustrate the [AF] rule with the following example:
                    XPURE
                             emp∧true ⊢L emp∧true ❀(true ,emp∧true )
     AF
          y7→c1 (null)⊢L U2a (y,x#)❀(σ1 : y7→c1 (null)∧true ⇒ U2 (y,x#),emp∧true )
AF
     x7→c1 (y)∗y7→c1 (null)⊢L U2 (x,y)❀(σ1 ∧ (x7→c1 (y)∗U2a (y,x#) ⇒ U2 (x,y)),emp∧true )

In the second application of [AF] rule, no new unknown predicate was introduced as
there was no pointers without #-anotated.
[AU−P] and [AF−P] rules abduce on pure and applied on consequent which has empty
heap. XPure procedure soundly transforms a heap formula into a pure formula [11].

5.1 Lemma Synthesis - lemsyn Procedure
Given the entailment check ∀v̄∃ē·Ra ∗κa ∧πa ⊢L Rc ∗∆r ∗∆c , our lemsyn procedure syn-
thesizes the lemma ∀v̄∀ē·Ra ∗κa ∧▽(v̄, πa )∧P(v̄, ē) → Rc ∗∆r ∗U(v̄) through three steps:
conjecture construction, lemma proving and predicate synthesis.
Conjecture Construction. At this step, lemsyn enriches the original check with either
pure unknown predicate P(v̄, ē) (for universal lemma) or shape unknown predicate U(v̄)

                                                    9
(for frame inference). While the former is only added if there exist existential variables
in LHS, the latter is only added if the sets of universal variables over pointers of LHS
and RHS are not identical. We note that in the former, to prepare for universal guard
inference, we need to existentially quantifies the pure formula; in the latter, ∆r is a
minimum closure of connected heaps of Rc . The unknown predicate is generated with
parameters that are union of free variables of LHS and RHS. Among these, pointer-
based parameters are annotated with # following the principle that instantiation (and
subtraction) are done before abduction. The detail is as follows: (i) all intersection vari-
ables of LHS and RHS are #-annotated; (ii) roots pointers of RHS are #-annotated; (iii)
remaining pointers are not #-annotated.
Lemma Proving. Our lemma proving, lemprove procedure, is based on the principle
of cyclic proof [7,9]. Two steps of this proof technique are: back-link form (i.e. link-
ing current sequents to a historical sequent); and global trace condition checking. We
implement these steps via lemma application. The procedure lemprove is formalized
as:
           Wn                         [LEM−PROVE]
                 ∆
             i=1 i  ≡unfold(∆    l , j)   ∆i ⊢L∪{link} ∆r ❀ (Ri , emp∧πi )
                                                         V
                       (lemma link: ∆l → ∆r , L) ❀ ni=1 Ri
To prove the conjecture link, lemprove looks up a j th UD predicate instance in ∆l to
apply [LU] rule. For a successful proving, any disjunct ∆i obtained from the unfolding
of ∆l must imply ∆r with empty heap in the residue. This unfolded predicate instance is
a progressing point. Induction hypothesis is encoded by the lemma link; induction on
such predicate instance is performed as an application on this lemma into a descendant
predicate instance of the unfolded predicate instance. We denote such application is
cyclic lemma application. We note that the lemma synthesis may be nested; it means
our system would speculate additional lemmas while proving a lemma.
    In cyclic term [7,9], the initial lemma is a bud, entailment check which applied
cyclic lemma application is companion of the bud above, and proof that are removed all
cyclic lemma applications is a pre-proof. A path in a pre-proof is a sequence of sequent
occurrences (entailment checks) derived by applying inference rules. For soundness, a
pre-proof must be a cyclic proof; it must satisfy the global trace condition i.e. for every
infinite path there is infinitely many progressing points. We state the condition that a
proof derived by our system is indeed a cyclic proof in the following lemma.
                                                                                th
Lemma 1 (Soundness). If all descendant predicate instances of the   Vnunfolded j UD
predicate instance have involved in a cyclic lemma application, then i=1 Ri ∧∆l |= ∆r .

Proof. A path in the proof is infinite if it includes the descendant predicate instances
(of the j th UD predicate instances) as these predicate instances may unfolded infinitely.
If every the descendant predicate instances has involved in a cyclic lemma application,
it has infinitely progressing points and thus the global trace condition is satisfied. Then
our proof is a cyclic proof.                                                             

Predicate Synthesis. If the conjecture link contains unknown
                                                      Vn       predicates, we infer
by SOBD a conjunction set of relational constraints R= i=1 Ri (over the unknown
predicates) such that R∧∆l |= ∆r . After that we deploy those algorithms in [24,33]

                                            10
                                                            emp∧v1′ 6=1∧v1 =2 ⊢{l3 ;l4 } emp∧v1 6=1
                                                            ❀ (true ,emp∧..)
                                                       AF
                                                            U(v¯4 )∧v1′ 6=1∧v1 =2
                                                            ⊢{l3 ;l4 } U1 (v¯5 )∧v1 6=1 ❀ (σ3 ,emp∧..)
                                                       AF
         emp∧p4 =null∧v1 =3                                  p4 7→c2 (v1′ ,p′4 )∗U(v¯4 )∧v1′ 6=1∧v1 =2
         ⊢{l3 ;l4 } emp∧v1 6=1 ❀ (true ,emp∧..)              ⊢{l3 ;l4 } U(v¯2 )∧v1 6=1 ❀ (σ3 ∧σ2 ,..)
AF                                                  LAPP
          emp∧p4 =null∧v1 =3⊢{l3 ;l4 } U(v¯3 )               ls2(p4 ,p2 )∗p2 7→c2 (3, null)∧v1 =2
          ∧v1 6=1 ❀ (σ1 ,emp∧..)                              ⊢{l3 ;l4 } U(v¯2 )∧v1 6=1
     M                                             M
              a7→c2 (3, null)⊢{l3 ;l4 }                a7→c2 (2,a1 )∗ls2(a1 ,p2 )∗p2 7→c2 (3, null)∧
              a7→c2 (v1 ,p4 )∗U(v¯3 )∧v1 6=1           ⊢{l3 ;l4 } a7→c2 (v1 ,p4 )∗U(v¯2 )∧v1 6=1
            ls2(a,p2 )∗p2 7→c2 (3, null)⊢{l3 } a7→c2 (v1 ,p4 )∗U(v¯2 )∧v1 6=1 ❀ (σ3 ∧σ2 ∧σ1 ,emp∧..)


                            Fig. 3. Derivation tree for proving of lemma l4 .

to solve the set R and obtain definitions for the predicates. Due to the nested lemma
synthesis, a predicate is synthesis at the scope it has been introduced. After that its
corresponding relational assumptions are canceled, i.e. not forwarded to outer scope.

Two-way Lemmas. For each lemma synthesized, we always consider to generate its re-
verse lemma. For each pair of such two-way lemmas, one with unknown predicates will
be inferred (and proven); another is substituted with the newly-inferred predicates prior
to proven. For the former, we choose the conjecture with more case splits i.e. more UD
predicates in the LHS. We hope that proving such conjecture will generate more sub-
goals and thus more relational assumptions would be generated. The more assumptions
our system generates, the more meaningful predicate definitions is synthesized.


5.2 Motivating Example Revisit

Our system started proving l3 by unfolding predicate ls1(a,p1 ) (like [LU]) as follows.
     ls2(a,p2 )∗p2 7→c2 (3, null)                           a7→c2 (1, a1 )∗ls1(a1 ,p1 )∗ls2(p1 ,p2 )∗
      ⊢{l3 } ls1(a,p3 )∗p3 7→c2 (v1 ,p4 )∗U(v¯1 )∧v1 6=1     p2 7→c2 (3, null) ⊢{l3 } ∆c
         ls1(a,p1 )∗ls2(p1 ,p2 )∗p2 7→c2 (3, null)⊢∅ ls1(a,p3 )∗p3 7→c2 (v1 ,p4 )∗U(v̄)∧v1 6=1

whereas ∆c ≡ls1(a,p3 )∗p3 7→c2 (v1 ,p4 )∗U(a#,p1 ,p2 ,p3 #,p4 ,v1 )∧v1 6=1, and
v̄≡{a#,p1 ,p2 ,p3 #,p4 ,v1 }, v¯1 ≡{a#,a,p2 ,p3 #,p4 ,v1 }. (In all tree derivations below, we
discard the [XPURE] rule on top for simplicity.)
Base Case. Proof of the left subgoal was derived as:
                          emp∧true ⊢{l3 ;l4 } emp∧true ❀ (true , emp∧true )
               LSYN                                                                          R
                      ls2(a,p2 )∗p2 7→c2 (3, null)⊢{l3 } a7→c2 (v1 ,p4 )∗U(v¯2 )∧v1 6=1
RU
      ls2(a,p2 )∗p2 7→c2 (3, null)⊢{l3 } ls1(a,p3 )∗p3 7→c2 (v1 ,p4 )∗U(v¯1 )∧v1 6=1❀(R1 ,emp∧..)

whereas v¯2 ≡{a#,a,p2 ,a#,p4 ,v1 }, and the nested conjecture l4 was constructed as:
        lemma l4 :ls2(a,p2 )∗p2 7→c2 (3, null)→a7→c2 (v1 ,p4 )∗U(v¯2 )∧v1 6=1
Proof of the conjecture l4 was derived as in Fig. 3, whereas (v¯3 )≡(a#,a,a,a#,p4 ,v1 ),

                                                    11
(v¯4 )≡(a#,a,p2 ,a#,p′4 ,v1′ ), (v¯5 )≡(a#,a,p2 ,a#,p4 #,v1 ,p′4 ,v1′ ). Inferred assumptions are:

   σ1 : p4 =null∧v1 =3 ⇒ U(a,a,a,a,p4 ,v1 )
   σ2 : p4 7→c2 (v1′ ,p′4 )∗U1 (a,a,p2 ,a,p4 ,v1 ,p′4 ,v1′ )∧v1′ 6=1∧v1 =2 ⇒ U(a,a,p2 ,a,p4 ,v1 )
   σ3 : U(a,a,p2 ,a,p′4 ,v1′ )∧v1′ 6=1∧v1 =2 ⇒ U1 (a,a,p2 ,a,p4 ,v1 ,p′4 ,v1′ )

Since U1 was introduced at this scope, before return to outer scope, U1 has been synthe-
sized as pred U1 (a,a,p2 ,a,p4 ,v1 ,root,v1′ )≡∃p4 ·U(a,a,p2 ,a,root,v1′ )∧v1′ 6=1∧v1 =2. The
set assumptions forwarded to outer scope is: R1 ≡σ1 ∧σ2 .
Induction Case. Proof of the right subgoal was derived as:
                               emp∧v1 6=1 ⊢{l3 } emp∧v1 6=1 ❀ (σ4 ,emp∧..)
                        AF
                             U(v¯7 )∧v1 6=1 ⊢{l3 } U(v¯1 )∧v1 6=1 ❀ (σ4 , emp∧..)
   M
       ls1(a1 ,p′3 )∗p′3 7→c2 (v1′ ,p′4 )∗U(v¯6 )∧v1′ 6=1 ⊢{l3 } ls1(a1 ,p3 )∗p3 7→c2 (v1 ,p4 )∗U(v̄)∧v1 6=1
LAPP
       ls1(a1 ,p1 )∗ls2(p1 ,p2 )∗p2 7→c2 (3, null) ⊢{l3 } ls1(a1 ,p3 )∗p3 7→c2 (v1 ,p4 )∗U(v̄)∧v1 6=1
   M
                    a7→c2 (1, a1 )∗ls1(a1 ,p1 )∗ls2(p1 ,p2 )∗p2 7→c2 (3, null)
                       ⊢{l3 } a7→c2 (1, a1 )∗ls1(a1 ,p3 )∗p3 7→c2 (v1 ,p4 )∗U(v̄)∧v1 6=1
       RU
            a7→c2 (1, a1 )∗ls1(a1 ,p1 )∗ls2(p1 ,p2 )∗p2 7→c2 (3, null) ⊢{l3 } ∆c ❀(σ4 ,emp∧..)
whereas (v¯6 )≡(a1 #,p1 ,p2 ,p′3 #,p′4 ,v1′ ), (v¯7 )≡(a1 #,p1 ,p2 ,p3 #,p4 ,v1 ), and the inferred
assumption is: σ4 : U(a1 ,p1 ,p2 ,p3 ,p4 ,v1 )∧v1 6=1 ⇒ U(a,p1 ,p2 ,p3 ,p4 ,v1 )
Now, the predicate U is synthesized from the set of assumptions σ1 ∧σ2 ∧σ4 .


5.3 Soundness
Lemma 2. The rules [R∗] and [LSYN] in Fig. 5 preserve soundness.
Our [R∗] rule is derived from the Monotonicity rule showing that spatial conjunction is
monotone with respect to implication [20]:
                                 ∆a1 |=∆c1       ∆a2 |=∆c2
                                   ∆a1 ∗∆a2 |=∆c1 ∗∆c2
The soundness of [LSYN] is derived from the meaning of frame, i.e. ∆a ⊢∆c ❀∆f rame
holds iff ∆a |=∆c ∗∆f rame , and the design of our lemma mechanism, i.e. lemma l:∆l →∆r
is valid iff ∆l ⊢∆r ❀emp holds.
Soundness of abduction rules. Since we only apply proven lemmas, it is sound to as-
sume that lemma store is empty (no user-supplied lemmas) and discard this lemma store
in our soundness proofs. We introduce the notation R(Γ ) to denote a set of predicate
definitions Γ ={U1 (v̄1 )≡Φ1 , ..Un (v̄n )≡Φn } satisfying the set of assumptions R. That
is, for all assumptions ∆l ⇒ ∆r ∈ R, (i) Γ contains a predicate definition for each
unknown predicate appearing in ∆l and ∆r ; (ii) by interpreting all unknown predicates
according to Γ , then it is provable that ∆l implies ∆r , written as Γ : ∆l ⊢ ∆r .
Lemma 3. Given the entailment judgement ∆a ⊢ ∆c ❀ (R, ∆f ), if there exists Γ such
that R(Γ ), then the entailment Γ : ∆a ⊢ ∆c ∗ ∆f holds.
Abduction soundness requires that if all the relational assumptions generated are satis-
fiable, then the entailment is valid.

                                                    12
6 Theorem Exploration
We present a mechanism to explore relations for UD predicates by using lemma synthe-
sis. The mechanism is applied for some sets of either statically user-supplied or dynami-
cally analyser-synthesized predicates. The key idea is that instead of requiring designers
of proof systems to write lemmas for a specific UD predicate (like in [4]), we provide for
them a mechanism to design lemmas for a general class of UD predicates. And based on
the design, our system will automatically generate specific and on-demand lemmas for
a specific UD predicate. In this section, we demonstrate this mechanism through three
such classes. Concretely, our system processes each UD predicate in four steps. First, it
syntactically classifies the predicate into a predefined class. Second, it follows struc-
ture of the class to generate heap-only conjectures (with quantifiers). Third, it enriches
the heap-only conjectures with unknown predicates for expressive constraint inference.
Last, it invokes the lemprove procedure to prove these conjectures, infer definitions for
the unknown predicates and synthesize the lemmas. Especially, whenever a universal
lemma L→R is proven, its reverse (the lemma R→L) is also examined. Proven lem-
mas will be applied to enhance upcoming inductive proofs.
     In the next subsection and App. B, we present theorem exploration in three classes
of UD predicates. In each class, we present step 1 and step 2; steps 3 and 4 are identical
to the lemsyn procedure in Sec. 5.1.

6.1 Generating Equivalence Lemmas
Step 1. Intuitively, given a set S of UD predicates and another UD predicate P (which is
not in S), we look up all predicates in S which are equivalent to P. This exploration is
applied to any new (either supplied or synthesized) UD predicate P.
Step 2. Heap-only conjecture to explore equivalent relation of two predicates (e.g.
P(x, v̄) and Q(x, w̄)) is generated as: ∃t¯1 ·P(root, v̄)→∃t¯2 ·Q(root, w̄), whereas t¯1 =v̄\w̄
and t¯2 =w̄\v̄. The shared root parameter x has been identified by examining all permu-
tations of root parameters of the two predicates. For example, with lln and lsegn in Sec.
2, our system examines conjecture: lemma eql ∃p·lsegn(root,p,m)→lln(root,n).
At step 3, the unknown predicate U is added to infer constraints over leaf variables p, m,
and n as: lemma eql ∃p·lsegn(root,p,m)∧U1 (p,m,n)→lln(root,n). At step 4, the
conjecture eql is proven and a definition of U1 is inferred as: U1 (p,m,n)≡p=null∧m=n.
For the equivalence, our system also generates and proves the reverse lemma of eql
as: lemma eqr lln(root,n)→∃p·lsegn(root,p,m)∧p=null∧m=n.
    This technique can be applied to match a newly-inferred definition synthesized by
shape analyses (i.e. [8,24]) with existing predicates of a supplied library of predefined
predicates. For specification inference, we eagerly substitute a newly-inferred predi-
cate in specifications by its equivalent-matching predicate from the library. This makes
inferred specifications more understandable. Furthermore this also helps to avoid in-
duction proving on proof obligations generated from these specifications.

7 Implementation and Experiments
We have implemented the proposed ideas into an entailment procedure, called S3 , start-
ing from SLEEK entailment procedure [11]. S invokes Z3 [26] to discharge satisfiabil-
 3
     S was initially implemented for the SLCOMP competition [38].


                                              13
 Ent.                           Proven                         CyclicSL S #syn
  1           lseg(x,t)∗lseg(t,null) ⊢∅ lseg(x,null)             0.03 0.06 1
  2      lseg(x,t)∗t7→c1 (y)∗lseg(y,null) ⊢∅ lseg(x,null)        0.03 0.08 1
  3     lseg(x,t)∗lseg(t,y) ∗ y7→c1 (null) ⊢∅ lseg(x,null)       0.03 0.11 2
  4   lseg(x,t)∗lseg(t,y)∗bt(y)∧y6=null ⊢∅ lseg(x,y) ∗ bt(y)     TO    0.21 2
  5 lseg(x,t)∗lseg(t,y)∗lseg(y,z)∧y6=z ⊢∅ lseg(x,y) ∗ lseg(y,z) 3.00 0.57 1
  6             x7→c1 (y)∗rlseg(y,z) ⊢∅ rlseg(x,z)               0.02 0.10 1
  7             nlseg(x,z)∗z7→c1 (y) ⊢∅ nlseg(x,y)               0.02 0.04 1
  8            nlseg(x,z)∗nlseg(z,y) ⊢∅ nlseg(x,y)               0.03 0.06 1
  9             glseg(x,z)∗z7→c1 (y) ⊢∅ glseg(x,y)               0.02 0.04 1
  10           glseg(x,z)∗glseg(z,y) ⊢∅ glseg(x,y)               0.02 0.04 1
  11               dlseg(u,v,x,y) ⊢∅ glseg2 (u,v)                0.07 0.04 1
  12     dlseg(w,v,x,z)∗dlseg(u,w,z,y) ⊢∅ dlseg(u,v,x,y)         0.04 0.11 1
  13       listo(x,z)∗listo(z,null) ⊢∅ liste(x,null)             0.06 0.06 2
  14       liste(x,z)∗liste(z,null) ⊢∅ liste(x,null)             0.18 0.12 3
  15           listo(x,z)∗liste(z,y) ⊢∅ listo(x,y)               4.33 0.88 3
  16       binPath(x,z)∗binPath(z,y) ⊢∅ binPath(x,y)             0.03 0.06 1
  17             binPath(x,y) ⊢∅ binTreeSeg(x,y)                 0.12 0.08 1
  18  binTreeSeg(x,z)∗binTreeSeg(z,y) ⊢∅ binTreeSeg(x,y)         0.20 0.66 1
  19       binTreeSeg(x,y)∗binTree(y) ⊢∅ binTree(x)              0.06 0.03 1
  20                  sortll(x,min) ⊢∅ ll(x)                      X    0.05 1
  21            sortlln(x,min,size) ⊢∅ lln(x,size)                X    0.12 1
  22          sortlln(x,min,size) ⊢∅ sortll(x,min)                X    0.08 1
  23  lsegn(x,y,sz1 )∗lsegn(x,z,sz2 ) ⊢∅ lsegn(x,z,sz1 +sz2 )     X    0.12 1
  24   lsegn(x,y,size1 )∗lsn(x,size2 ) ⊢∅ lsn(x,size1 +size2 )    X    0.10 1
  25     lseg(x,tl)∗tl7→c1 (y)∗lseg1(y,ty) ⊢∅ lseg1(x,ty)         X    0.10 1
  26           avl(x,size,height,bal) ⊢∅ btn(x,size)              X    0.08 1
  27              tll(x,ll,lr,size) ⊢∅ btn(x,size)                X    0.07 1
               Table 1. Entailment Checking with Auxiliary Lemma Synthesis

ity over pure formulas. We have also integrated S into S2 [24] and extended the new
system to support a modular verification with partially supplied specification and incre-
mental specification inference. In the following, we experiment S and the enhanced S2
in entailment and program verification problems. The experiments were performed on
a machine with the Intel i7-960 (3.2GHz) processor and 16GB of RAM.
Entailment Check. In Table 1, we evaluate CyclicSL and S on inductive entailment
problems without user-supplied lemmas (i.e. L=∅). Ent 1-19 are shape-only problems;
they were taken from Smallfoot [4] (Ent 1-5), and CyclicSL [7,9] (Ent 6-19). Ent 20-
27 are shape-numerical problems. We used sortll for a sorted list with smallest value
min, and tll for a binary tree whose nodes point to their parents and leaves are linked
as a singly-linked list [18,24]. Time is in second. TO (X) denotes timeout (30s) (not-
yet-support, resp.). The last column #syn shows the number of lemmas our generated
to prove the entailment check. The experimental results show that S can handle a wider
range of inductive entailment problems. The experiments also demonstrate the effi-
ciency of our implementation; for 18 problems which both tools successfully verified,
while it took CyclicSL 8.29 seconds, it took S only 3.14 seconds.
Modular Verification for Memory Safety. We enhance S2 to automatically verify a
wide range of programs with a higher level of correctness and scalability. In more detail,
it automatically verifies those programs in [30] (e.g. bubble sort, append method of

                                           14
list with tail - like lllast predicate in App. C.2) without any user-supplied lemma. By
generating consequence parallel separating lemmas, it also successfully infers shape
specifications of methods which manipulate the last element of a singly-linked list (i.e.
g slist concat in gslist.c) and a doubly-linked list (i.e. g list append in glist.c)
of GLIB library [1] (See App. C.2). By generating equivalence lemmas, matching a
newly-inferred UD predicate with predefined predicates in S2 is now extended beyond
shape-only domain.
     We evaluated the enhanced S2 on the cross-platform C library Glib open source [1].
                               wo.                We experimented on heap-manipulating
             LOC #Pr #Lo √              √w.       files, i.e. singly-/doubly-linked lists
                             # sec. # sec.
   gslist.c 698 34 18 41 2.19 47 2.30             (gslist.c/glist.c), balanced binary trees
    glist.c 784 32 19 39 3.20 46 3.39             (gtree.c) and N-ary trees (gnode.c). In
   gtree.c 1204 32 8 36 3.46 36 3.48              Fig.4 we list for each file the number
  gnode.c 1128 38 27 52 7.52 53 7.58              of lines of code (excluding comments)
                                                  LOC, number of procedures
                                                                        √        (while/for
       Fig. 4. Experiments on Glib Programs       loops) #Pr (#Lo). # and sec. show the
number of procedures/ loops and time (in second) for which the enhanced S2 can verify
memory safety without (wo.) and with (w.) the lemma synthesis component. With the
lemma synthesis, the number of procedures/loops was successfully verified increases
from 168 (81%) to 182 (88%) with the overhead of 0.38 seconds.


8 Related Work and Conclusion

Entailment Procedure in SL. Past works in SL mainly focus on developing decision
procedures for a decidable fragment combining linked lists (and trees) with only equal-
ity and inequality constraints [4,14,31,32,29]. Smallfoot [3,4], provided strong semantic
foundations and proof system with frame inference capability for the above fragment.
Some optimization on segment feature for the fragment with linked list was presented in
[14,31,32,29]. Recently, Iosif et. al. extended decidable fragment to restricted UD pred-
icates [18]. [40] presented a comprehensive summary on computational complexity of
deciding entailment in SL with UD predicates. Our work, like [11,34], targets on an un-
decidable SL fragment including (arbitrary) UD predicates and numerical constraints.
Like [11,34], we trade completeness for expressiveness. Beyond the focus of [11,34],
we provide inductive reasoning in SL using lemma synthesis.
Lemma Mechanism in SL. Lemma is widely used to enhance the reasoning of heap-
manipulating programs. For examples, lemmas are used as alternative unfoldings be-
yond predicates’ definitions [30,9], external inference rules [16], or intelligent gener-
alization to support inductive reasoning [7]. Unfortunately, these systems require user
to supply those additional lemmas that might be needed for a proof. In our work, we
propose to automatically generate lemmas either dynamically for inductive reasoning
or statically for theorem exploration.
Induction Reasoning. For a manual and indirect solution for inductive reasoning in
SL, Smallfoot [4] presented subtraction rules that are consequent from a set of lem-
mas of lists and trees. Brotherston et. al. proposed a top-down approach to automate
inductive proofs using cycle proof [6]. To avoid infinite circular proof search, the cyclic

                                            15
technique stops expanding whenever current sequent is a repetition of a similar proof
pattern detected from historical proof tree. Cyclic proof was successfully implemented
in first-order logic [9], and separation logic [7]. Circularity rule, a similar mechanism to
cyclic, was also introduced in matching logic [37]. [12] managed induction by a frame-
work with historical proofs. Our proposal extends these systems with frame inference
and gives better support for modular verification of heap-manipulating programs.
Auxiliary Lemma Generation. In inductive theorem reasoning, auxiliary lemmas are
generated (and proven) either top-down to support inductive proofs (e.g. IsaPlanner
[19], Zeno [39] and extension of CVC4 [35]) or bottom-up to discover theorem (e.g.
IsaCosy [23] and HipSpec [13]) and [28]. The center of these techniques are heuristics
to generate useful lemmas for sets of given functions, constants and datatypes. Typi-
cally, while the top-down proposals (i.e. [39]) suggest new lemmas by replacing some
common sub-term in a stuck goal by a variable, the bottom-up proposals (i.e. [13]) gen-
erate lemmas to compute equivalence functions for functional programs. In our work,
we introduce both top-down and bottom-up approaches into an entailment procedure
in SL. To support inductive entailment proofs dynamically, we generate auxiliary con-
jectures with unknown predicates to infer either universal guard or frame. To support
theorem discovery, we synthesize equivalence, split/join/reverse and separating conjec-
tures. This mechanism can be extended to other heuristics to enhance proofs of a widen
class of UD predicates.


9 Conclusion

Lemmas have been widely used to enhance the capability of program verification sys-
tems. However, existing reasoning systems of heap-manipulating programs via separa-
tion logic rely on user to supply additional lemmas that might be needed for a proof.
In this paper, we have presented a mechanism for applying, proving and synthesiz-
ing lemma in a SL entailment procedure. We have shown an implementation that has
a higher level of automation and completeness for benchmarks taken from inductive
theorem proving and software verification sources. Our evaluation indicates that induc-
tive proofs benefit from both bottom-up and top-down lemmas generated by our new
approach. It also shows that synthesized lemmas are relevant and helpful to proving
a conjecture. Future work includes extending the incremental inference mechanism to
other pure domains, e.g. bag/set domain.
References

 1. Glib-2.38.2. https://developer.gnome.org/glib/, 2013. [Online; accessed 30-May-2015].
 2. Aws Albargouthi, Josh Berdine, Byron Cook, and Zachary Kincaid. Spatial interpolants. In
    ESOP, pages 634–660. 2015.
 3. J. Berdine, C. Calcagno, and P. W. O’Hearn. A Decidable Fragment of Separation Logic. In
    FSTTCS ’04. Springer-Verlag, December 2004.
 4. J. Berdine, C. Calcagno, and P. W. O’Hearn. Symbolic Execution with Separation Logic. In
    APLAS, volume 3780, pages 52–68, November 2005.
 5. A. Bouajjani, C. Dragoi, C. Enea, and M. Sighireanu. Accurate invariant checking for pro-
    grams manipulating lists and arrays with infinite data. In ATVA, pages 167–182. 2012.


                                             16
 6. J. Brotherston. Cyclic proofs for first-order logic with inductive definitions. In Proceedings
    of TABLEAUX-14, volume 3702 of LNAI, pages 78–92. Springer-Verlag, 2005.
 7. J. Brotherston, D. Distefano, and R. L. Petersen. Automated cyclic entailment proofs in
    separation logic. In CADE, pages 131–146, 2011.
 8. J. Brotherston and N. Gorogiannis. Cyclic abduction of inductively defined safety and ter-
    mination preconditions. In SAS ’14, number 8723 in LNCS, pages 68–84, 2014.
 9. J. Brotherston, N. Gorogiannis, and R. L. Petersen. A generic cyclic theorem prover. In
    Proceedings of APLAS-10, LNCS, pages 350–367. Springer, 2012.
10. Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. Compositional
    shape analysis by means of bi-abduction. In POPL, pages 289–300, 2009.
11. W.N. Chin, C. David, H.H. Nguyen, and S. Qin. Automated verification of shape, size and
    bag properties via user-defined predicates in separation logic. SCP, 77(9):1006–1036, 2012.
12. Duc-Hiep Chu, Joxan Jaffar, and Minh-Thai Trinh. Automatic induction proofs of data-
    structures in imperative programs. PLDI’15, 2015.
13. Koen Claessen, Moa Johansson, Dan Rosn, and Nicholas Smallbone. Automating inductive
    proofs using theory exploration. In CADE ’24, volume 7898, pages 392–406. 2013.
14. B. Cook, C. Haase, J. Ouaknine, M. Parkinson, and J. Worrell. Tractable reasoning in a
    fragment of separation logic. In CONCUR, volume 6901, pages 235–249. 2011.
15. David Detlefs, Greg Nelson, and James B. Saxe. Simplify: A theorem prover for program
    checking. J. ACM, 52(3):365–473, May 2005.
16. Dino Distefano and Matthew J. Parkinson J. jstar: Towards practical verification for java. In
    OOPSLA ’08, pages 213–226, New York, NY, USA, 2008. ACM.
17. Constantin Enea, Mihaela Sighireanu, and Zhilin Wu. On automated lemma generation for
    separation logic with inductive definitions. ATVA, 2015. To appear.
18. R. Iosif, A. Rogalewicz, and J. Simácek. The tree width of separation logic with recursive
    definitions. In CADE, pages 21–38, 2013.
19. Andrew Ireland and Alan Bundy. Productive use of failure in inductive proof. Journal of
    Automated Reasoning, 16(1-2):79–111, 1996.
20. S. Ishtiaq and P.W. O’Hearn. BI as an assertion language for mutable data structures. In
    ACM POPL, pages 14–26, London, January 2001.
21. Shachar Itzhaky, Nikolaj Bjrner, Thomas Reps, Mooly Sagiv, and Aditya Thakur. Property-
    directed shape analysis. In CAV, pages 35–51. 2014.
22. B. Jacobs, J. Smans, P. Philippaerts, F. Vogels, W. Penninckx, and F. Piessens. Verifast: A
    powerful, sound, predictable, fast verifier for c and java. In NFM, pages 41–55. 2011.
23. Moa Johansson, Lucas Dixon, and Alan Bundy. Conjecture synthesis for inductive theories.
    J. Autom. Reason., 47(3):251–289, October 2011.
24. Quang Loc Le, Cristian Gherghina, Shengchao Qin, and Wei-Ngan Chin. Shape analysis via
    second-order bi-abduction. In CAV, volume 8559, pages 52–68. 2014.
25. Quang Loc Le, Jun Sun, and Wei-Ngan Chin. Satisfiability modulo heap-based programs.
    In CAV 2016, July 2016.
26. Leonardo M. and Nikolaj B. Z3: An Efficient SMT Solver. In TACAS, 2008.
27. Parthasarathy Madhusudan, Xiaokang Qiu, and Andrei Stefanescu. Recursive proofs for
    inductive tree data-structures. In POPL, pages 123–136, New York, NY, USA, 2012. ACM.
28. Roy McCasland, Alan Bundy, and Autexier Serge. Automated discovery of inductive theo-
    rems. Studies in Logic, Grammar and Rhetoric, 10(23), 2007.
29. JuanAntonio Navarro Prez and Andrey Rybalchenko. Separation logic modulo theories. In
    APLAS, volume 8301, pages 90–106. 2013.
30. H. H. Nguyen and W.-N. Chin. Enhancing program verification with lemmas. In CAV, pages
    355–369, 2008.
31. Juan Antonio Navarro Pérez and Andrey Rybalchenko. Separation logic + superposition
    calculus = heap theorem prover. In PLDI, pages 556–566, 2011.


                                               17
32. R. Piskac, T. Wies, and D. Zufferey. Automating separation logic using smt. In Natasha
    Sharygina and Helmut Veith, editors, CAV, volume 8044, pages 773–789. 2013.
33. C. Popeea and W.-N. Chin. Inferring disjunctive postconditions. In ASIAN, pages 331–345,
    2006.
34. X. Qiu, P. Garg, A. Ştefănescu, and P. Madhusudan. Natural proofs for structure, data, and
    separation. In PLDI, pages 231–242, New York, NY, USA, 2013. ACM.
35. Andrew Reynolds and Viktor Kuncak. Induction for smt solvers. In VMCAI, volume 8931,
    pages 80–98. Springer Berlin Heidelberg, 2015.
36. J. Reynolds. Separation Logic: A Logic for Shared Mutable Data Structures. In IEEE LICS,
    pages 55–74, 2002.
37. Grigore Rosu and Andrei Stefanescu. Checking reachability using matching logic. In OOP-
    SLA ’12, pages 555–574, New York, NY, USA, 2012. ACM.
38. Mihaela Sighireanu and David R. Cok. Report on SL-COMP 2014. http://www.liafa.univ-
    paris-diderot.fr/slcomp14/, 2014. [Online; accessed Jun-2015].
39. William Sonnex, Sophia Drossopoulou, and Susan Eisenbach. Zeno: An automated prover
    for properties of recursive data structures. In TACAS, pages 407–421. 2012.
40. Antonopoulos Timos, Gorogiannis Nikos, Haase Christoph, Kanovich Max, and Ouaknine
    Joël. Foundations for decision problems in separation logic with general inductive predicates.
    In FoSSaCS 2014, pages 411–425, 2014.
41. Antoine Toubhans, Bor-YuhEvan Chang, and Xavier Rival. Reduced product combination
    of abstract domains for shapes. In VMCAI, pages 375–395. 2013.
42. M.-T. Trinh, Q.-L. Le, C. David, and W.-N. Chin. Bi-abduction with pure properties for
    specification inference. In APLAS, pages 107–123. 2013.
43. H. Yang, O. Lee, J. Berdine, C. Calcagno, B. Cook, D. Distefano, and P. W. O’Hearn. Scal-
    able shape analysis for systems code. In CAV, pages 385–398, 2008.




                                                18
A    Separation Entailment Procedure


                   [INC1]                                     [INC2]
     x7→c(v̄)∗∆1 ⊢L ∆2 ∧x=null ❀ (∅, κ)          ∆1 ∧x=null ⊢L x7→c(v̄)∗∆2 ❀ (∅, κ)
                  [M]                                             [PRED−M]
       ρ=[v̄/w̄] πeq = freeEQ(ρ)                          ρ=[v̄/w̄] πeq = freeEQ(ρ)
    ∆1 ∧πeq ⊢L ∆2 [v̄/w̄] ❀ (R, Φf )                  ∆1 ∧πeq ⊢L ∆2 [v̄/w̄] ❀ (R, Φf )
 x7→c(v̄)∗∆1 ⊢L x7→c(w̄)∗∆2 ❀ (R, Φf )           P((r, v̄))∗∆1 ⊢L P((r, w̄))∗∆2 ❀ (R, Φf )

          W         [LU]                            W           [RU]
           ∆ui = unfold(P(v̄)∗∆1 , 0)                 ∆fi = unfold(P(v̄)∗∆2 , 0)
      ∆ui ∗∆1 ⊢L ∆2 ❀ (Ri , Φi ) i=1...n         ∆1 ⊢L ∆fi ∗∆2 ❀ (Ri , Φi ) i=1...n
                         V       W
       P(v̄)∗∆1 ⊢L ∆2 ❀ ( Ri , Φi )                  ∆1 ⊢L P(v̄)∗∆2 ❀ (Ri , Φi )
                        [ALIAS]                                  [XPURE]
         y7→c(v̄)∗κ1 ∧x=y∧π1 ⊢L ∆2 ❀ (R, ΦR )           XPure(κ1 )∧π1 =⇒ π2 ❀ R
         x7→c(v̄)∗κ1 ∧x=y∧π1 ⊢L ∆2 ❀ (R, ΦR )           κ1 ∧π1 ⊢L π2 ❀ (R, κ1 ∧π1 )

                    Fig. 5. Basic Inference Rules for Entailment Checking
    Entailment procedure between ∆a and ∆c is formalized as follows:

                                 ∆a ⊢L ∆c ❀ (R, Φf )

The entailment outputs residual frame Φf and a set of relational assumptions R. (For
simplicity, we discard footprints and existential quantifiers of consequent in this discus-
sion.) Inference rules are presented in Fig. 5.
    To derive a proof for an entailment check, our system deduces antecedent into two
parts (i) relevant one would be subsumed by models of the consequent; (ii) the rest will
be inferred as residual frame. To do that, it subtracts (match) heap two sides until heap
in the consequent is empty (via the [∗M], [LU], [RU] inference rules). After that, it se-
mantically check the validity for the implication of the pure part by using external SMT
solvers and theorem provers (via [XPURE] inference rule). Typically, an entailment
check is performed as follows.

 – Subtracting. Match up identified heap chains. Starting from identified root point-
   ers, the procedure keeps matching all their reachable heaps with [M] and [PRED−M]
   rules. The former (latter) rule matches two points-to (user-defined, resp.) predi-
   cates in antecedent and consequent if they have an identified root. After that, it uni-
   fies corresponding fields
                           Vnof matched roots by using auxiliary function freeEQ(ρ):
   freeEQ([ui /vi ]ni=1 ) = i=1 {ui = vi }.
 – Unfolding. Derive alternative heap chains. When the procedure is unable to make
   a progress on matching, it will look up alternative chains for matching through
   unfolding heap predicates. While the unfolding in the antecedent ([LU] rule) does
   cases split, the unfolding in the consequent ([RU] rule) does proof search.
 – XPure Reducing. Reduce entailment checking on separation logic to implication
   checking on the first order-logic with [XPURE] rule. This reduction was presented
   in [25]. When the consequent remains empty heap, e.g. emp ∧ πc , the procedure

                                            19
      employs [XPure] inference rule to decide the entailment result. Firstly, this rules
      make use of the XPure reduction to transform the combination of remain heaps in
      the antecedent and footprints into the first order-logic formula on the combination
      of pure domains, e.g. πa . Then it checks the implication πa =⇒ πc . Technically, to
      perform such implication checking, the following satisfiability check is performed:
      sat(πa ∧ ¬(πc )). If it returns unsat, the result of the implication is valid; it returns
      sat, the result of the implication is invalid; otherwise, the result of the implication
      is unknown.
During the heap chains matching, aliasing relation on pointers are considered to intro-
duce alternative proofs via [ALIAS] rule.
Instantiation Mechanism. A variable is instantiable if it is an actual parameter of a UD
predicate instance in the consequent (RHS) and is quantifier-free. This mechanism is
applied for predicate matching rule [11] (corresponding rule used in [16] is subtracting)
and predicate folding rule [11] (corresponding rule used in [7] is unfolding predicate in
RHS). Whenever a match of a UD predicate instance occurs, the entailment procedure
binds its instantiable parameters coming from the RHS with corresponding variables
from the antecedent (LHS) and moves the equality constraints to the LHS. Whenever a
UD predicate instance in the RHS is unfolded, our proof system moves pure constraints
over instantiable (actual) parameters of the unfolded formulas to the LHS. Moreover,
this mechanism is proven sound and is able to enhance the completeness of entailment
procedure for a SL fragment including UD predicates with pure properties [11].


B Theorem Exploration
B.1    Generating Reverse/Split/Join Lemmas
Step 1. This subsection explores theorem over segment predicates as follows.
Definition 2 (Segment Predicate) A predicate SP(r, v̄, s) is a segment predicate if r is
a root parameter and for any base formula ∆ which is derived by unfolding SP(r, v̄, s),
s is a leaf pointer reached from r. We will refer s as a segment parameter.
For instance, linked-list segment predicate with size property is defined as follows:
pred glsegn(root,s,n)≡emp∧root=s∧n=0 ∨ ∃ q· root7→c1 (q)∗glsegn(q,s,n−1);
The predicate glsegn above may be an acyclic list, or a complete cyclic list, or a lasso
(an acyclic fragment followed by a cycle). The acyclic list segment predicate lsegn
(Sec. 2) is a special segment predicate. Tree segment predicates can be found in [7].
     A UD predicate is syntactically classified as segment predicate if it has one root
parameter r and one segment parameter s such that s is a leaf pointer which is reached
from r. A UD predicate is syntactically classified as acyclic segment predicate if it is a
segment predicate and the formula r6=s occurs in all inductive branches.
Step 2. Reverse lemmas explore relations between reverse directions of linked heaps
i.e. forwardly and backwardly linked list from root parameter to segment parameter in
inductive branches of segment predicates. Our implementation for reverse lemmas cur-
rently restricts for reachable heaps linked by points-to predicates and segment predicate

                                              20
instances. With a segment predicate Q(root, w̄, s), for each inductive branch ∃w̄i ·∆i ,
reverse linked heaps ∃w̄i ·∆ir of is examined as follows: (i) mark reachable heaps, a set
of points-to predicates and segment predicate instances from root to s; (ii) swap root
and s. Now, s is a root variable of either a points-to predicate or a segment predicate
instance; (iii) starting from the heap predicate with s, reverse the reachable heaps fol-
lowing the links. (For each points-to predicate, swap points-to variable with downstream
field variable of the links. For each segment predicate instance, swap root parameter and
segment parameter); (iv) keep the rest of ∆i unchanged.
Reverse conjectures are initially generated over reachable heaps as: ∃w̄i ·∆ir →Q(root,w̄,s).
    For example, with segment list glsegn above, we generate the following lemma:
lemma rev1 ∃ q· q7→c1 (s)∗glsegn(root,q,n−1) → glsegn(root,n,s). Heap-only con-
jecture to explore join relation for the segment predicate P(x, w̄, s) (x is a root parame-
ter and s is a segment parameter) is generated as:
                    ∃z,w̄1 , w̄2 · P(x, w̄1 , z)∗P(z, w̄2 , s) → ∃w̄·P(x, w̄, s)
   Two heap-only conjectures to explore join relation for the acyclic segment predicate
Q(x, w̄, s) of data type data c{fi :vi ; } are generated as:
               ∃z, w̄1 , w̄2 · Q(x, w̄1 , z)∗Q(z, w̄2 , null) → ∃w̄·Q(x, w̄, null)
and
      ∃z, w̄1 , w̄2 · Q(x, w̄1 , z)∗Q(z, w̄2 , s)∗s7→c(w̄3 ) → ∃w̄, w̄3 ·Q(x, w̄, s)s7→c(w̄3 )
    Similarly, split heap-only conjecture ∆ → ∆1 ∗∆2 is generated as a opposite form
of the corresponding join heap-only conjecture ∆1 ∗∆2 → ∆.

B.2    Generating Separating Lemmas
Step 1. This subsection explores relations over UD predicates including either parallel
or consequence separating parameters. Two parameters of a predicate are parallel sep-
arating if they are both root parameters (e.g. those of the predicate zip, Sec. 5.1). Two
parameters of a predicate are consequence separating if one is root parameter and an-
other parameter is internal variable reachable from the root in all base formulas derived
by unfolding the predicate (e.g. those of the predicate Upost , Sec. C.3). We generate these
separating lemmas to explicate separation globally. As a result, the separation of actual
parameters is visible from analyses. This visible separation enables strong updates in
modular heap analysis or frame inference in modular verification.
Step 2. Suppose r1 , r2 are consequence or parallel parameters in Q(r1 , r2 , w̄), heap
conjecture is generated as: Q(r1 , r2 , w̄) → Q1 (r1 )∗Q2 (r2 )∗Q3 (w̄).
    For example, the zip predicate is suggested to split through the following parallel
separating conjecture: lemma para zip(root,r2 ) → Q1 (root)∗Q2 (r2 ).

C     More Examples
C.1 Universal Lemma Synthesis
To illustrate the lemma synthesis, consider the following entailment check E1

                                                21
       ∃k·lln(x, n)∧n≥k∧k≥0∧i=k∧j=n−k ⊢∅ ∃p·lsegn(x,p,i)∗lln(p, j)
We define the lln (lsegn) predicate to describe an acyclic singly-linked list null-
terminated (segment, respectively) over the data type c1 with size property n as follows:
pred lln(root,n)≡emp∧root=null∧n=0               pred lsegn(root,s,n)≡emp∧root=s∧n=0
∨ ∃ q· root7→c1 (q)∗lln(q,n−1);                  ∨ ∃ q· root7→c1 (q)∗lsegn(q,s,n−1)∧root6=s;
 whereas struct c1 {c1 ∗ next; }. E1 verifies that the list x can be split into two smaller
list segments. (The list y is the residue.) To derive a proof for E1 , our system automat-
ically generates the following auxiliary conjecture with universal guards and unknown
predicate P :
    lemma sp ∀n,a,b·lln(root,n)∧P (n,a,b) → ∃p · lsegn(root,p,a)∗lln(p,b).
and its reverse conjecture
    lemma jn ∀n,a,b·∃p·lsegn(root,p,a)∗lln(p, b) → lln(root, n)∧P (n,a,b).
Our system will prove the validity of one lemma and infer definition of P , simultane-
ously. After that, this inferred definition of P is substituted into another lemma before
this lemma is proven. As jn has more predicates, it may need more case splits. Thus
we choose jn for inference since it would generate more relational constraints and our
system can obtain more precise definition of P. To prove jn, our lemma proving com-
ponent unfolds the predicate lsegn(root,p,a) in the antecedent and generates the two
subgoals E2 and E3 as
E2 : ∀n,a,b·∃p·lln(p, b)∧root=p∧a=0 ⊢{jn} lln(root, n)∧P (n,a,b)
E3 : ∀n,a,b∃p,q1 ,a1 ·root7→c1 (q1 )∗lsegn(q1 ,p,a1 )∗lln(p, b)∧a=a1 +1 ⊢{jn} lln(root, n)∧P (n,a,b)
 Inspired by cyclic proof systems [6,7,37,12], our system has employed the lemma jn
as induction hypothesis for proving E2 and E3 . For E2 , we subtract (match) the predicate
lln pointed by root in both sides, instatiate n and generate the following assumption
to successfully prove the rest of RHS:
                             R2 : a=0∧n=b∧b≥0 ⇒ P (n,a,b)
For E3 , we unfold the predicate lln pointed by root in RHS (recursive case), subtract
points-to predicate pointed by root in both sides, apply lemma jn and generate the
following assumption to successfully prove the rest of RHS:
       R3 : n=n1 +1∧a=a1 +1∧P (n1 ,a1 ,b)∧n1 ≥0∧a1 ≥0∧b≥0 ⇒ P (n,a,b)
Using a fixed point computation (i.e. FixCalc [33]) to solve R2 ∧R3 , a definition of P
can be derived as P (n,a,b)≡n=a+b∧n≥b∧b≥0. The lemma jn is synthesized as:
lemma jn ∀n,a,b·∃p·lsegn(root,p,a)∗lln(p, b) → lln(root, n)∧n=a+b∧n≥b∧b≥0
Moreover, our system also successfully verifies the lemma sp (substituted with P ) as:
lemma sp ∀n,a,b·lln(root, n)∧n=a+b∧n≥b∧b≥0 → ∃p·lsegn(root,p,a)∗lln(p, b)
Now, jn and sp can be soundly applied for upcoming proof search. By applying the
lemma sp, our entailment procedure can prove the validity of E1 and inferring the
residue as: ∆frame ≡emp∧n≥k∧k≥0∧i=k∧j=n−k∧i=a′ ∧j=b′ .


C.2 Modular Verification with Last Element


                                            22
1 c1 ∗ append shape(c1 x, c1 y)                   To illustrate how our proof system can sup-
2 /∗requires ll(x)∗ll(y)∧x6=null                  port induction reasoning together with complex
3 ensures ll(res) ∗ /                             frame inference, consider the modular verifica-
4 {c1 ∗t=x;                                       tion of the method append shape in Fig. 6. This
5 while(t->next) t=t->next;                       method appends a list pointed by y to the end of
6 t->next=y;                                      a list pointed by x. The user provides its pre-post
7 return x; }                                     specification (lines 2-3) and the predicates ll
Fig. 6. Code of method append shape.
                                                             pred ll(root)≡emp∧root=null
                                                             ∨ ∃ q· root7→c1 (q)∗ll(q);
whereas struct c1 {c1 ∗ next; }. The while loop is annotated with the natural invariant
as follows: requires ll(t)∧t6=null ensures ll last(t,t′ ), whereas t′ is the value
of t after the loop and the predicate ll last is supplied as 4
                     pred ll last(root,s)≡root7→c1 (null)∧root=s
                     ∨ ∃ q· root7→c1 (q)∗ll last(q,s);
    As a (bottom-up) modular verification, the loops are verified prior to the verifica-
tion of the method check; and the correctness of a method is reduced to the validity of
appropriate verification conditions generated. Our system generates verification condi-
tions to ensure absence of memory errors (no null dereference, no double free and no
memory leak), validity of functional calls/loops via compositional pre-/post- conditions
and post-conditions holding.
    The most challenging step to verify this example is the proving of absence of null
dereference at line 6. The symbolic state is computed before line 6 is
                                  ll last(t,t′ )∗ll(y)∧t=x∧x6=null
For memory safety at line 6, our system generates the following proof obligation
                           ll last(t,t′ )∗ll(y)∧t6=null ⊢∅ t′ 7→c1 (q)
Since the information of t′ is deeply embedded in the base case of predicate ll last,
this entail check challenges existing SL proof systems. Additionally for a proper rea-
soning, a proof system also needs to infer the frame as the list ll(y) and a list segment
from t to the node before t′ . Inferring such frame is nontrivial. Our system generates
the conjecture:
            lemma c: ll last(t,t′ )∗ll(y)∧t6=null → t′ 7→c1 (q)∗U2 (t,t′ #,q,y)
Then, proves its validity as follows.
                                         (Base)              (Induction)
            ll last(t,t )∗ll(y)∧t6=null⊢∅ t 7→c1 (q)∗U2 (t,t′ #,q,y)❀(σ1 ∧σ2 , emp)
                           ′                        ′



                                          emp⊢{c} emp❀(σ1 , emp)
                      AF
                               ll(y)∧t′ =t∧q=null∧t6=null⊢{c} U2 (t,t′ #,q,y)
           M
               (Base): t7→c1 (null)∗ll(y)∧t′ =t∧t6=null⊢{c} t′ 7→c1 (q)∗U2 (t,t′ #,q,y)
 4
     Indeed, this invariant is the outcome of the state-of-the-art shape analysis tools like [8,24]
     when they are used for invariant inference.


                                                        23
                                        emp⊢{c} emp❀(σ1 , emp)
                        AF
                             t7→c1 (q1 )∗U2 (q1 ,t′ #,q2 ,)⊢{c} U2 (t,t′ #,q2 ,y)
            M
                t7→c1 (q1 )∗t′ 7→c1 (q2 )∗U2 (q1 ,t′ #,q2 ,y)⊢{c} t′ 7→c1 (q)∗U2 (t,t′ #,q,y)
 LAPP
        (Induction): t7→c1 (q1 )∗ll last(q1 ,t′ )∗ll(y)∧t6=null⊢{c} t′ 7→c1 (q)∗U2 (t,t′ #,q,)

Relational assumptions are inferred as:
                   σ1 : ∗ll(y)∧t′ =t∧q=null∧t6=null ⇒ U2 (t,t′ ,q,y)
                   σ2 : t7→c1 (q1 )∗U2 (q1 ,t′ ,q2 ,y) ⇒ U2 (t,t′ ,q2 ,y)
From σ1 and σ2 , our system synthesizes the following definition for U2 as
U2 (root,t′ ,q,y)≡ll(y)∧root=t′ ∧q=null∧root6=null∨∃q1 ·root7→c1 (q1 )∗U2 (q1 ,t′ ,q,y);
Using theorem exploration presented in Sec 6 and App. B, our system generate the
following two-way lemma to normalize the predicate U2 :
   lemma conseq0:U2 (root,t′ ,q,y) ↔ U3 (root,t′ )∗ll(y)∧q=null∧root6=null
with U3 is a newly-inferred predicate as follows.
             U3 (root,t′ )≡emp∧root=t′ ∨ ∃ q1 · root7→c1 (q1 )∗U3 (q1 ,t′ );
In summary, our system successfully proves validity and infers frame for the entailment.
    We present a reasoning on both shape and size properties of a more complicated
revision of the append method in App. C.3.

C.3 Modular Verification with Incremental Specification Inference

         1 c1 ∗ append(int n, int m){                   7 c1 ∗ create ll(int s){
         2 c1 ∗x=creat ll(n);                           8 if(s=0) return null;
         3 c1 ∗y=creat ll(m);                           9 else {
         4 c1 ∗t=x;                                     10 c1 ∗ p=malloc(c1 );
         5 while(t->next) t=t->next;                    11 p->next=create ll(s−1);
         6 t->next=y; return x; }                       12 return p; }

                                  Fig. 7. Code of method append.
    In order to minimize the burden of program verification, we pursue a compositional
verification of programs whose specifications are partially supplied. Concretely, the user
is only required to provide specifications of pre/post conditions for critical methods and
loop invariants whereas specifications of the rest are inferred automatically. This speci-
fication inference has been implemented incrementally for the combined domains. such
that shape-only specifications are inferred first and then constraints over pure domains
are additionally synthesized . In the context of heap-manipulating programs, recursive
methods and loop invariants normally relate to recursive predicates; consequently, com-
positionally verifying these specifications requires both inductive reasoning and frame
inference. Our proposed approach brings the best support for such verification.
To illustrate how our proof system is used to compositionally and incrementally verify
heap-manipulating programs, consider the method append in Fig. 7 which appends a list
pointed by y to the end of a list pointed by x. The user provides the predicates lln, lsegn
(Sec. 2) and append’s specification as: requires n>0∧m≥0 ensures lln(res,m+n).

                                                  24
     Verifying safety properties that require both heap and data reasoning has been stud-
ied in the literature, e.g. abstract interpretation [41], TVLA [21] and interpolation [2].
Different to these proposals, ours is compositional and based on the proposed induc-
tive proof system. We enhance inference techniques [8,24,42] to generate specification
and invariant for the combined domains of the method create ll and while loop (of
pre/post condition). Our verification is bottom-up (i.e. verifying the method create ll
and while loop before the method append) and incremental (i.e. analyzing shape and
then size property for the loop invariant inference). Concretely, our system inferred the
specification for create ll and while loop as: requires s≥0 ensures lln(res,s) and
(s3 ) requires ∃q·t7→c1 (q)∗lln(q,i)∧i≥0 ensures lsegn(t,t′ ,j)∗t′ 7→c1 (null)∧j=i, resp.
     In the following, we present the specification inference for the loop. To infer shape
specification of the loop invariant the system initially generates specification with two
unknown shape predicates as follows: requires Upre (t) ensures Upost (t, t′ ), whereas
t′ is the value of t after the loop. Using the modular shape analysis in [24], the predicate
Upre and Upost are synthesized as
Upre (root) ≡ ∃q·root7→c1 (q)∗U1 (q)
U1 (root)      ≡ emp∧root=null ∨ ∃ q· root7→c1 (q)∗U1 (q)
Upost (root,l) ≡ root7→c1 (null)∧root=l ∨ ∃ q· root7→c1 (q)∗Upost (q,l)∧root6=l
whereas U1 is an auxiliary predicate. Whenever receiving these predicate definitions, our
theorem exploration component will generate new lemmas to study interesting proper-
ties of these predicates. In this example, our system generates the following lemmas to
explicate the separation between two parameters of the predicate Upost :
            lemma consep Upost (root,l) ↔ U2 (root,l)∗l7→c1 (null)
            U2 (root,s) ≡ emp∧root=s ∨ ∃ q· root7→c1 (q)∗U2 (q,s)∧root6=s
Then, the shape invariant of the loop is constructed as follows:
             requires ∃q·x7→c1 (q)∗U1 (q) ensures U2 (x,x′ )∗x′ 7→c1 (null)
To extend the above shape invariant with the size property, we first use predicate exten-
sion [42] to automatically append the size property into U1 (Un1 ) and U2 (Un2 )
Un1 (root,n) ≡ emp∧root=null∧n=0 ∨ ∃ q· root7→c1 (q)∗Un1 (q,n−1)
Un2 (root,s,n) ≡ emp∧root=s∧n=0 ∨ ∃ q· root7→c1 (q)∗Un2 (q,s,n−1)∧root6=s
Our theorem exploration, again, generates two lemmas to match Un1 with lln and Un2
with lsegn as: Un1 (root,n)↔lln(root,n) and Un2 (root,s,n)↔lsegn(root,s,n).
After that, we generate specification with unknown pure predicates P2 , P3 :
requires ∃q·t7→c1 (q)∗lln(q,i)∧P2 (i) ensures lsegn(t,t′ ,j)∗t′ 7→c1 (null)∧P3 (i,j)
whereas P2 and P3 are placeholders to capture constraints over the size variables. Us-
ing SOBD for pure properties inference [42], the following definitions are synthesized:
P2 (i)≡i≥0 and P3 (i,j)≡j=i. Finally, loop invariant is inferred as the specification s3 .
This loop invariant is now used in the verification of the main method append. To verify
the correctness and memory safety (no null-dereference and no leakage) of append, our
system generates and successfully proves the following three verification conditions: 5
 5
     For simplicity, we discard the verification conditions at line 2 and line 3.


                                                   25
VC1 . lln(x,n)∗lln(y,m)∧n>0∧m≥0 ⊢L ∃q·t7→c1 (q)∗lln(q,i)∧i≥0
      ❀(true ,lln(y,m)∧x=t∧t6=null∧n=i−1∧n>0∧i≥0) // line 5, pre- proving (of loop)
VC2 . lsegn(t,t′ ,j)∗t′ 7→c1 (null)∗lln(y,m)∧i=j∧x6=null∧n=i−1∧n>0 ⊢L t′ 7→c1 ( )
      ❀(true ,lsegn(t,t′ ,j)∗lln(y,m)∧i=j∧x=t∧t6=null∧n=i−1∧n>0)∧m≥0
               // before line 6, no null-dereference
VC3 . lsegn(res,t′ ,j)∗t′ 7→c1 (y)∗lln(y,m)∧i=j∧x=t∧t6=null∧n=i−1∧n>0∧m≥0
       ⊢L lln(res,m+n) ❀(true ,emp∧x=t∧t6=null∧n=i−1∧n>0∧i≥0)
               // after line 6, post-condition, no leakage
 whereas L is the set of lemmas either supplied by the user or generated by our system
(i.e. to explore predicate relations like the conseq lemmas above).
We highlight two advantages achieved from our proposed approach. First, if the two-
way lemma consep was not synthesized, the condition VC2 would be generated as:
Upost (t,t′ )∗lln(y,m)∧x=t∧i=j∧t6=null∧n=i−1∧n>0 ⊢L t′ 7→c1 ( ). We are not aware
of any proof systems that are capable of discharging such obligation and inferring the
residual frame, simultaneously. Second, simultaneously automated proving VC3 and in-
ferring its residual heap emp (to confirm no memory is leaked) require nontrivial induc-
tive reasoning which is not supported by most existing SL entailment procedures.




                                         26
