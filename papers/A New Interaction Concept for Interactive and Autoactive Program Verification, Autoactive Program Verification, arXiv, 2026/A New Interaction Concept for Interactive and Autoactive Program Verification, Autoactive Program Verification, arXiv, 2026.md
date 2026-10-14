                                                 A New Interaction Concept for Interactive and
                                                       Autoactive Program Verification
                                                     Wolfram Pfeifer                             Mattias Ulbrich                           Daniel Drodt
                                                 wolfram.pfeifer@kit.edu                         ulbrich@kit.edu                  daniel.drodt@tu-darmstadt.de
                                             Karlsruhe Institute of Technology           Karlsruhe Institute of Technology       Technical University of Darmstadt
                                                    Karlsruhe, Germany                          Karlsruhe, Germany                     Darmstadt, Germany

                                        Abstract                                                            deeper insight into the open proof goal is required to di-
                                        Fully functional program verification is an undecidable—and,        agnose why the automation cannot close it and to decide
                                        hence, inherently difficult—task, that is not automatically         how to intervene. In all cases, understanding of the proof
                                        solvable but typically requires user interaction and guidance.      goal requires expert knowledge of both the program under
arXiv:2605.06972v1 [cs.PL] 7 May 2026




                                        Existing verifiers either work autoactively, requiring the user     verification and the verification tool.
                                        to write annotations in source code, without the possibility to         In this paper we present an integrated interaction con-
                                        inspect the proof state or intervene in case of an unsuccessful     cept that supports users in assessing proof situations and
                                        attempt, or allow interactions on a logical encoding that is        interacting with proofs at the source code level. The central
                                        on a lower level than the user-provided specifications.             idea is to present all available verification information as
                                           We present a novel interaction concept which allows the          overlays on the program source and to enable interaction
                                        user to inspect and interact with the proof state on source         directly at that level. Consequently, proofs that previously
                                        code and specification level. This minimizes the mental gap         required considerable low-level manual intervention can of-
                                        between the representations. We provide an implementation           ten be discharged by iteratively guiding automation without
                                        of the concept as a plugin for the Java verification engine         leaving the specification level. When necessary, users may
                                        KeY, and show with a user study that this prototype can be          still perform fine-grained manual interaction on more de-
                                        beneficial for users to understand the proof state and find         tailed abstraction levels. Conceptually, proof guidance given
                                        defects in source code or specifications.                           interactively should best be recorded as proof scripts on the
                                                                                                            same abstraction level to allow replay and persistence of
                                        Keywords: Program Verification, Deductive Verification, User        manual prover guidance.
                                        Interaction, Java Modeling Language                                     We implemented this interaction concept by combining
                                                                                                            interactive and autoactive verification on top of the deduc-
                                        1   Introduction                                                    tive Java verification engine KeY [1] which is founded on
                                        Deductive software verification has made substantial pro-           a program logic in which inference rules are applied at a
                                        gress in recent years [7, 23, 24, 26], yet its adoption in in-      fine granularity. The base logic is an extension of first-order
                                        dustry remains limited [8]. Verifying non-trivial programs          logic tailored to model Java states; proofs are browsable and
                                        written in real-world programming languages is inherently           interactable in the KeY user interface. This detailed represen-
                                        difficult, and—because the general problem is undecidable—          tation exposes many details of the symbolic state of the open
                                        this difficulty will persist even as tools improve.                 goal and hence allows for subtle proof interactions, but it can
                                           Deductive verification is commonly organized modularly:          also overwhelm users quite easily: It is often hard for a KeY
                                        functions and loops are annotated with specifications (con-         novice to understand why a particular formula appears in the
                                        tracts, loop invariants, etc.), and proofs for program correct-     proof obligation and how it relates to the source program.
                                        ness are constructed from these component specifications.               The proposed interaction concept addresses this gap be-
                                        Successful verification is therefore typically an iterative pro-    tween program and proof by (i) lifting information from the
                                        cess: it rarely succeeds on the first attempt. Instead, a verifi-   technical proof presentations back to the source code level,
                                        cation engineer must inspect remaining proof obligations,           (ii) providing visual references between source code level
                                        determine why a proof attempt failed, and take corrective           statements and their counterparts in the proof, and (iii) en-
                                        action. Broadly speaking, there are three reasons a proof           abling source code level invocation of proof tactics and of
                                        may not succeed:                                                    inference rules on the detailed level and the recording of
                                                                                                            proof scripts. The overall goal is to reduce the cognitive ef-
                                             1. the implementation is incorrect,
                                                                                                            fort required to switch between the source code level mental
                                             2. the specification is incorrect or too weak,
                                                                                                            model and the detailed logical proof model, thereby making
                                             3. the tool’s automation is insufficient to close the proof.
                                                                                                            deductive verification more accessible and productive.
                                           The appropriate response differs between these cases. In             The presented integration is particularly well suited for
                                        the first two, the source code or the specification (or both)       introducing programmers to formal reasoning. Specification
                                        must be adapted to resolve the mismatch. In the third case,
                                                                                    Wolfram Pfeifer, Mattias Ulbrich, and Daniel Drodt


languages are typically designed to be familiar to practition-    /*@ public normal_behavior
ers of the specified language. Much of the Java Modelling           @ requires 0 <= i < a.length && 0 <= j < a.length;
Language (JML) [18], e.g., is designed to be comprehensible         @ ensures a[i] == \old(a[j]) && a[j] == \old(a[i]);
to a Java developer with basic first-order-logic training. By       @ ensures (\forall int k; 0 <= k < a.length;
contrast, understanding failed proof attempts at the logical        @ k != i && k != j ==> a[k] == \old(a[k]));
level often requires more specialized training in logic and         @ assignable a[*];
proof calculi. The approach presented here enables users            @*/
to transition gradually from high-level, specification-level      public void swap(int[] a, int i, int j) {/*...*/}
reasoning to the detail-rich logic backend when required.         Listing 1. JML specification of a swap method. More concise
By narrowing the gap between prover and specification, in-        specification is possible.
teracting with the prover at the specification level offers a
promising way to reduce the learning curve for practitioners.
   The implemented prototype of this proof presentation           int m(int n) {
and interaction concept was evaluated in a small user study         //@ assume n >= 0;
with KeY experts. The results indicate that presenting proof        n++;
information inline in the source reduces cognitive overhead         //@ assert n > 0;
and can speed up some verification tasks, even for users            return n;
more experienced with the traditional sequent view.               }
   The paper is structured as follows: Section 2 contains the             Listing 2. JML assumptions and assertions.
necessary background about JML and KeY. In Section 3, we
present the idea of user interaction on source code level, the
central hypothesis, and our concept of what user interaction      with universal (\forall) and existential (\exists) quantifi-
should look like, independent of the concrete prover it is        cation, implication (==>), and an \old(𝑒) construct which
implemented in. Section 4 refines these ideas and explains        evaluates the JML expression 𝑒 in the state at the beginning
how they are implemented prototypically in the KeY system,        of the current method call, among others. We call the parts
as well as the challenges that had to be solved. The user study   of a JML specification, e.g., the precondition, clauses. The
described in Section 5 demonstrates that our ideas can be         assignable clause specifies the frame condition, i.e., the set
beneficial for interactive verification. Related work is shown    of heap locations that can be modified by the method.
in Section 6, before we conclude with a short summary and            Such a formal contract as the one for swap serves not only
future work ideas in Section 7.                                   to document the method’s expected behavior precisely, it can
                                                                  also be used as input tools like OpenJML [11], VerCors [9],
                                                                  and KeY to verify (or disprove) the implementation’s correct-
2     Background                                                  ness with regard to the contract.
While elements of the interaction concept are not specific to        JML also permits annotations in a method body. Particu-
Java and can be applied to other imperative languages, we         larly relevant for this paper are assertions and assumptions
present it as an extension of existing technologies using the     both used to indicate that an expression is supposed to hold
Java Modeling Language as specification language and the          whenever the respective line with the statement is reached.
Java verification tool KeY as the verification engine.            But there is a difference, as Listing 2 shows: Whereas the
                                                                  assumption n >= 0 in the first line of m is silently assumed
                                                                  to hold without proof, the assertion for n > 0 in the third
2.1   The Java Modeling Language                                  line raises a corresponding proof obligation. Assertions and
The Java Modeling Language (JML) [19], is a behavioral inter-     assumptions may contain JML expressions, e.g., quantified
face specification language for Java and the de facto standard    formulas. The purpose of such annotations are, again, both
for formal specifications in Java. Following the “design by       for documentation but more importantly for prover guidance
contract” paradigm [22], it supports modular program spec-        since they introduce local lemmas that need to be proved
ification where each method is annotated with a method            locally, but that also can make the proof of surrounding proof
contract. Listing 1 exemplarily demonstrates the parts of a       obligations easier.
JML contract. JML is always written in a comment with @ as
the first character. Here, we declare a “normal behavior” case,   2.2   The KeY Tool
i.e., no exception is thrown, with the precondition (requires)    KeY [1, 2] is a deductive verification tool for Java programs
that the parameters i and j are valid indices of the array a      based on the dynamic logic JavaDL, a program-logic variant
and the postcondition (ensures) that a’s values at indices i      of modal first-order logic with Java programs embedded
and j are now swapped while all other values are unchanged.       in modal operators. It introduces state-dependent program
Note that JML expressions are Java expressions extended           variables and two modal operators: the “diamond” ⟨𝑝⟩𝜙 and


Preprint
A New Interaction Concept for Interactive and Autoactive Program Verification


the “box” [𝑝]𝜙, where 𝑝 is a fragment of a Java program and
𝜙 is a JavaDL formula. Intuitively, the formula ⟨𝑝⟩𝜙 holds
in a state iff 𝑝 terminates (without exceptions) when started
in state 𝑠 and, in the poststate after 𝑝, 𝜙 holds; [𝑝]𝜙 is the
partial operator, it holds when ⟨𝑝⟩𝜙 holds or when 𝑝 does
not terminate.
   A proof obligation for the total correctness of a method m
w.r.t. precondition pre and postcondition post can be ex-
pressed in JavaDL in the form pre → ⟨res=m();⟩post.
   To prove a JavaDL formula 𝜙 correct, KeY relies on a se-
quent calculus and shows that the sequent =⇒ 𝜙 can be
derived. Its calculus includes the familiar propositional and
first-order rules, rules for reasoning about boolean values
and integer arithmetics, as well as rules to symbolically exe-                  Figure 1. The KeY GUI. On the left is the proof tree, in the
cute the program fragment in modalities. The rule ifElseSplit                   center the sequent view, and on the right, the code under
below matches when an if-else-statement is encountered and                      verification.
splits the proof goal into two branches: one, where the if’s
condition holds and the then-branch is executed; one where
the condition does not hold and the else-branch is executed.                    from non-trivial properties of non-trivial programs. This
Thereby, all cases are covered. For details of these rules and                  combination of interaction patterns enabled verification of
their implementation, we refer to [2].                                          complex, real-world Java programs such as TimSort [12],
                                                                                LinkedList [16], IdentityHashMap [10] and ips4 o [7]. Nev-
                          Γ, 𝑏  TRUE =⇒ ⟨𝑠 1 ⟩𝜙, Δ
                                                                                ertheless, manual interactions require a great deal of exper-
                          Γ, 𝑏  FALSE =⇒ ⟨𝑠 2 ⟩𝜙, Δ
        ifElseSplit                                                             tise with the program under verification as well as JavaDL
                      Γ =⇒ ⟨if (𝑏) 𝑠 1 else 𝑠 2 ⟩𝜙, Δ                           and KeY’s calculus.
   These symbolic execution rules simplify and evaluate the                        As a middle ground between full automation and manual
code in modalities piecemeal until all modalities have been                     interaction, KeY provides an array of macros, enabling more
fully executed and only first-order formulas remain.                            focused automatic rule applications. With macros, one can,
   In addition to sequent rules like ifElseSplit, KeY offers                    e.g., execute only symbolic execution rules or only propo-
rewrite rules such as 𝑡  𝑡 ⇝ true, which can be applied to                     sitional simplification. This is especially helpful when at-
terms and (sub-)formulas in the sequent. Rules can also have                    tempting to understand a given goal state to uncover why
additional conditions, such as a formula 𝜙 being present in                     verification fails.
the antecedent. This greatly increases the calculus’ flexibility
and expressiveness. For details of the realization of these                     3   User Interaction on Source Code Level
rules in the form of “taclets,” see [25].                                       In this section, we describe our concept for interaction. While
   To model state changes in a total, structured manner,                        we use KeY in the motivation to demonstrate shortcomings of
JavaDL also introduced updates. An elementary update x := 𝑡                     interaction on a low-level logical representation, the concept
represents the state change where variable x now has the                        and ideas in this section are independent.
value of term 𝑡. Updates can be composed to parallel updates,                      KeY’s current interaction pattern typically proceeds as
e.g., x := y ∥ y := x, which represents swapping the values of                  follows: A method is chosen for verification in the GUI, a
variables x and y, and can be applied to terms and formulas,                    JavaDL proof obligation is generated from the method’s JML
e.g., {n := n + 1}(n > 0).                                                      specification and presented as an initial sequent. Then, the
   By relying on JavaDL formulas, KeY avoids the typical                        proof automation is started to attempt verification, with
approach of translating the program under verification to a                     possible interactive steps in between to close some goals
lower-level intermediate language or SMT problem, which                         beyond the prover’s capabilities.
is then verified. Instead, the program is directly embedded                        This approach of expressing a proof obligation in JavaDL
in modalities.                                                                  formulas and proving these formulas with a fine-grained,
   KeY provides a GUI with the sequent shown as an ex-                          precise calculus provides some immediate benefits. No com-
plicit goal state—an, as yet, unproven sequent in the proof                     plexity is hidden and a user can fully inspect the proof steps
state—where a user can manually apply any applicable rules                      and how they changed or introduced proof goals. Further,
directly on selected terms and formulas, permitting a great                     since the formulas may contain Java code directly, there is
deal of control and fine-grained interaction, see Figure 1. At                  a narrower gap between the method to be verified and the
the same time, KeY has a powerful automatic proof mode                          initial proof obligation than achievable with translation to
that is able to discharge many proof obligations stemming                       an intermediate language or SMT.


Preprint
                                                                                      Wolfram Pfeifer, Mattias Ulbrich, and Daniel Drodt


   However, these benefits come at the cost of some complex-       /*@ public normal_behavior
ity: Even the initial proof obligation contains elements not         @ requires 0 <= to;
present in the original program. For instance, since JavaDL is       @ assignable a[0..to];
more expressive than Java, we add preconditions to restrict          @ ensures (\forall int i; 0 <= i < to; a[i] == 0);
possible values of method parameters and states of the heap.         @*/
This discrepancy is compounded by the non-trivial changes          void zero(int[] a, int to) {
to the sequent introduced by rule applications: To model             int j = 0;
Java’s complex semantics accurately, programs are signifi-           /*@ loop_invariant 0 <= j <= to
cantly altered during symbolic execution. Formulas are then            @ && (\forall int k; 0 <= k < j; a[k] == 0);
further simplified, moved around, discarded as irrelevant,             @ assignable a[0..to];
etc. While each step is inspectable and comprehensible, un-            @ decreases a.length - i;
derstanding the relation of a sequent to the program after             @*/
thousands or tens of thousands of rule applications is non-          while (j < to) {
trivial. Similar problems arise from encoding a program in             //@ assume 0 <= to;      // precondition
intermediate languages or SMT, as implicit knowledge of the            //@ assume j < to;       // loop guard
target language is added to the translation, increasing the            //@ assume 0 <= j <= to; // loop invariant ...
gap to the source code.                                                //@ assume (\forall int k; 0 <= k < j; a[k]==0);
   From the case studies of more complex algorithms and data           //@ assert 0 <= j < a.length; // a[j] in bounds
structures completed in recent years [7, 10, 27], we developed         a[j] = 0;
the following hypothesis: To minimize the mental gap, all              ++j;
interactions with the prover should be as close as possible to         //@ assert 0 <= j <= to; // loop invariant ...
the original user input, i.e., the specified source code.              //@ assert (\forall int k; 0 <= k < j; a[k]==0);
   From this central hypothesis, we derive the following             }
points for our concept. First, it is important that users can      }
orient themselves in the proof and understand what has to          Listing 3. The desired output of the new user interaction
be proven in the current proof branch (respectively goal).         pattern. The assertions and assumptions with the gray back-
Second, open goals should be presented inline in the source        ground represent the current proof goal. The method zero
view, in a language and form as close as possible to the orig-     sets all elements of integer array a to zero. Verification
inal user input. Third, the user should be able to perform         fails, as the precondition to < a.length is missing; hence,
interactions to inspect and manipulate directly on this source     the second assertion cannot be shown (a[k] may be out of
view; ideally they should be able to finish the proof without      bounds).
the need to descend to the underlying logical level of the
prover. This also means that not all intermediate steps of the
underlying prover need to be inspectable and manipulatable         that remain to be proven. We must take care to present the
by the user to be able to understand the required actions          formulas as close as possible to their original formulation as
in the proof. Instead, it is sufficient to see the goals in spe-   given by the user. This minimizes the mental gap and allows
cific key points in the proof, while relying on the automatic      the user to investigate the current proof situation without
facilities of the system to fill in the intermediate steps.        needing to know about the underlying logical encoding: It
   Although we apply this approach to KeY and the hypoth-          is sufficient to understand the program and its specification.
esis is built on experience in the KeY system, we maintain         Listing 3 demonstrates the desired result of this approach.
that our conclusion generalizes: Any verification tool where       The use of assumptions and assertions is motivated by the
proving occurs on a lower level then the source code level         fact that these are already present in JML and represent a
must strive to minimize the gap between the two. Presenting        known and intuitive concept for the user. However, since
the remaining goals in a source code level view is a general       they are only used for “capturing” the current state of the
approach, regardless of the concrete verification tool and         prover and presenting the goal, and in particular do not
methodology.                                                       represent assumptions on the input level, they need to be
                                                                   clearly distinguishable from user-given input. In Listing 3,
3.1   The Novel User Interaction Concept                           this is accomplished with a gray background.
Our interaction concept implements a novel approach to                Note that with our concept, we only aim to show a sin-
present a specific open goal state to the user. The formulas       gle proof goal (that is, a single leaf of the proof tree) at the
from the internal logical proof engine should be presented as      same time. The rationale behind this is that while it might be
assertions and assumptions in the source code. Assumptions         possible to display multiple goals at once, it would become
are to represent knowledge about the program collected             unreadable already for very small programs. However, it is
in the current goal. Assertions ought to signify formulas          possible to inspect different goals: When the user navigates


Preprint
A New Interaction Concept for Interactive and Autoactive Program Verification


in the proof tree to a suitable goal, i.e., where symbolic ex-                  //@ ensures a[i] == \old(a[i]) + 8;
ecution and update simplification is completed, the view is                     void inc(int[] a, int i) {
updated accordingly.                                                              a[i] = a[i] + 1;
   By presenting the goal state inline together with (relevant                    l: add(a, i, 7);
parts of) the initial program, we can provide a basis for                         //@ assert a[i] == \old(a[i], l) + 7;
investigating the goal state. We should further aid the user                      //@ assert a[i] == \old(a[i]) + 8;
by highlighting the source of the annotations. For instance,                    }
hovering over the assumption 0 <= to ought to highlight                         Listing 4. Example of the use of the operator \old with label.
the requires clause, as this is the formula’s origin.                           The first assertion refers to two states that are both not the
   To further minimize the gap between proof and specifi-                       pre-state. In contrast to the second assertion, the standard
cation, it is imperative that the terms and formulas are as                     operator without label is not sufficient.
close as possible to the original input. A verifier might, for
example, normalize integer functions and relations to im-
prove automation: 0 <= to would be transformed to the term                         To realize this concept, the verifier must offer some ad-
to > −1. While this is necessary for the prover, it hinders the                 ditional functionality. First, we must be able to track the
user, especially as these normalizations compound. Hence,                       origin of terms and formulas, i.e., whether they come from
we must ensure that terms and formulas are represented                          the precondition, a loop invariant, etc. Second, we must be
closely to their original form.                                                 able to adequately translate terms and formulas from the
   In the same vein, we want to purge implicit information                      logical level back to the source code level.
from the new representation. As stated above, provers often
                                                                                3.1.1 Tracking Origins of Terms and Formulas. To
add implicit preconditions, e.g., restricting the state to possi-
                                                                                track the origin of terms and formulas, they need to be asso-
ble Java heaps, the value range of integer parameters to the
                                                                                ciated with an origin reference. Such a reference must entail
range of Java’s int type, or ensuring that relevant objects
                                                                                a type (e.g., requires), file information, and line and column
have been created. These formulas have no equivalent on
                                                                                ranges.
the specification level, as they are already implicit on that
                                                                                   Implicitly added formulas must be assigned a special “im-
level, and they are only necessary for proving but rarely
                                                                                plicit” type to differentiate them from explicit formulas. Fur-
for goal comprehension. Thus, they must not be added as
                                                                                ther, they can have no file and line/column information, since
assumptions.
                                                                                they do not stem from the source code.
   In program verification, formulas are evaluated in a con-
                                                                                   One might expect that origins are attached to formulas, as
text, that is the current assignment of local variables and
                                                                                they are typically to what specification clauses are translated.
heap state. In our concept, this is represented by the position-
                                                                                However, this tends to break when formulas are split, for
ing of assertions and assumptions: They are inserted into the
                                                                                instance a conjunction into their conjuncts, which automatic
source code in the position corresponding to the state where
                                                                                provers must often do. Therefore, we assign origins to the
they have to be proven respectively are known to hold.
                                                                                lowest entity possible, the operator, i.e., the ∧ in 𝜙 ∧ 𝜓 . If
   However, this is insufficient, since a single formula might
                                                                                no origin is found for a formula, the subterms are searched
relate different program states. Fortunately, JML provides a
                                                                                recursively for origins and their union is shown.
tool for this: the \old operator. In addition to the standard
                                                                                   Once the origins have been assigned to the operators of
form, which only has a term as single parameter and evalu-
                                                                                the initial proof obligation, the verification tool must ensure
ates this term in the pre-state of the method, there is also a
                                                                                that they are maintained, so as to still be available for open
second form available. This second form has a (Java) label
                                                                                goals after the proof attempt failed. We discuss how we solve
as a second parameter, and evaluates the given term in the
                                                                                this for KeY in Section 4.
state at the label. With this operator, it is possible to insert a
formula in a specific line, and still refer to states at different              3.1.2 Translating Terms Back to Source Code Level.
positions in the code. Listing 4 shows an example where the                     With the origin information in place, the next step is to
standard \old without label is not sufficient and the vari-                     translate the formulas from the underlying logical represen-
ant with label is needed. However, note that this requires to                   tation (e.g., a sequent) back to JML. For this, the formulas are
introduce the additional label into the source code.                            classified according to their origin type as either implicit, as-
   We silently assume that there is at most one statement                       sume or assert. Implicit formulas are not shown in the source
per line. Otherwise, the placement of assumptions would be                      code view. Formulas of the other two categories are shown
difficult to compute and unnecessarily difficult to read. Also,                 correspondingly as JML assert or assume statements.
return statements must be of the form return x;, where x                           For the formulas in JML statements, it is important to stay
is a variable or constant, since we cannot insert assertions                    as close as possible to the user input. Therefore, if the formula
after the return.                                                               on the logical layer has a single unique origin, the original
                                                                                string from the user input should be displayed verbatim.


Preprint
                                                                                      Wolfram Pfeifer, Mattias Ulbrich, and Daniel Drodt


This “reverts” all normalization steps that have been done on      /*@ assert (\exists int i; 0<=i<a.length; a[i]>0) \by {
the logical level, for instance rewriting to negation normal         expand on="\invariant_for(this)";
form, polynomial normal form, etc. However, often a formula          witness "(\exists int j; 0<=j<a.length; a[j]>1)"
has been transformed significantly, for example by applying              as="j_0";
equations or combining multiple input formulas, and a direct         instantiate "(\exists int i; 0<=i<a.length; a[i]>0)"
mapping to a JML formula is not possible. In this case, a back-          inst="j_0";
translation has to be applied, which maps operators of the           auto;
logical level back to their corresponding operators in JML.        } @*/
   In addition to the translation of formulas, also the position   Listing 5. Vision how a typical interaction in the KeY GUI—
where to show them in the source code has to be determined.        expanding an invariant, obtaining a Skolem constant, instan-
This is, however, highly dependent on the concrete repre-          tiating a quantifier with it, and closing the proof with the
sentation of state in the logic and thus on the prover the         auto mode—could be persisted as a JML script.
concept is implemented in. For KeY, we discuss a solution in
Section 4.
   Even when all the technical requirements are met, there             The new interaction pattern aims to lift a number of inter-
remains a crucial conceptual limitation: The tracking of ori-      actions that are already supported on the logical level to the
gins and translation back to the source code level is only         source code level. After finishing symbolic execution of the
possible if there is only one symbolic execution. Although         proof obligation (via a number of different macros), running
provers might be capable of verifying relational properties—       the automatic prover is one of the coarse grained interactions
for instance, KeY can reason about information flow and            lifted from the technical to the source code level. Further pos-
dependency contracts [1, 6]—their proof obligations contain        sible proof interactions to guide the prover towards closing a
multiple programs to execute, making translation into a sin-       proof include splitting of conjunctively connected proof obli-
gle Java program impossible. Nevertheless, verification of         gations into parts, introducing case distinctions (so-called
functional correctness remains the most popular use case           cuts), and instantiating quantifiers with JML expressions. For
of KeY and similar tools, reinforcing the relevance of our         improved clarity, it must also be possible to drop individual
approach.                                                          displayed assumption formulas from the goal state if the user
                                                                   deems that they do not contribute to the proof but might
                                                                   rather cause the automation to go astray.
3.2   Advancing Proofs and Proof Scripts                               We retain the possibility of fine-grained user interaction
Representing information in open proof goals in terms of           mechanisms, such as applying elementary proof steps (in-
the original source code and cross-referencing them to their       ference rules) directly on the logic level, without any ab-
logical counterparts are vital prerequisites for enabling the      stractions to the source code level. Although this fall-back
comprehension of proof obligations in program verification.        is intended as a last resort for situations where higher-level
However, presenting proof goals well is insufficient to ad-        interaction is insufficient, experience shows that there are
dress how proofs are conducted at that level; allowing and         genuine cases in which the solution requires interaction at
supporting user interaction to advance the proof is an equally     the logical level, e.g., JavaDL. In such cases, technical de-
important aspect of the process.                                   tails of the surrounding verification condition that are not
   The interaction style that has, traditionally, proved par-      visible at the source level can be crucial for the reasoning.
ticularly successful in KeY is a point-and-click paradigm, in      A typical example arises when one must reason about the
which the user selects the rule to be applied from a context-      “createdness” status of objects. Createdness is not exposed at
sensitive list of applicable inference rules. This approach        the JML level—by design, as JML assumes that all referable
provides fine control over the proof process while sparing         objects are created—whereas the logical level can express
the user from having to memorize the names of the c. 1 500         finer distinctions.
rules implemented in KeY.                                              The extensibility of proofs via mouse interactions, whether
   In comparison, in classical autoactive verification, interac-   at the more abstract source code level or at the more tech-
tion is achieved by composing verification-only statements         nical level, is very user-friendly and allows very targeted
and similar support annotations in the program source code         proof progress in many cases without lengthy text inputs.
guiding the prover and helping it close obligations that can-      A drawback of this form of interaction is that it is little per-
not be discharged fully automatically.                             sistable and is sensitive to small changes in the program
   In the novel interaction concept, we intend to combine          or the specification. Because it is present as user input in a
the benefits of both approaches: To allow high-level user          concrete proof, it can hardly be adapted to changed situa-
interaction in terms of the surrounding source code, but           tions. The application to even slightly different proof trees
to allow at the same time to revert to the technical level if      is challenging [5]. The solution foreseen in the concept is
needed.                                                            the transcription of user interactions as proof scripts at the


Preprint
A New Interaction Concept for Interactive and Autoactive Program Verification


code level. Autoactive provers support annotating assertions
in code with commands for guiding the prover to address
similar challenges. Dafny [20], for example, has annotations
that can be attached to assertions to provide guidance on
how proofs should be conducted. KeY likewise has a new
and experimental mechanism,1 with which proofs can be
annotated at JML assertions. The abstraction level in JML
scripts corresponds to that of interactions at the source code
level.
   It is therefore natural that user interactions (on both levels)
should be recorded as commands in JML proof scripts to
make them accessible for users, and to make them available
in a persistent manner for automatic proof replay. Thus
our concept brings point-and-click interaction to a source
code level view and extends the expressivity of the source
code, permitting rule applications, cuts, macros, etc. as JML
script commands. For instance, a typical interaction in KeY
is that first an invariant is unrolled, a universal quantifier
                                                                                   Figure 2. Screenshot of the prototype implementation.
from this invariant is skolemized resulting in a new constant,
and then an expression containing this constant is provided
as an instantiation for an existentially quantified formula.                     Section 3.1, the generated JML assumptions and assertions
Afterwards, the proof is found automatically by the proof                        that represent the current proof goal are shown inline in the
search strategy. Listing 5 show how such an interaction in                       source view. These insertions for the current goal can be dis-
the GUI could be represented (potentially automatically) as                      tinguished easily from the user-provided specification by the
a script.                                                                        gray background and the missing line numbers. Note that
   This naturally allows for a new KeY workflow: The user                        the formulas exactly correspond to the user input, formula
writes JML commands which advance the proof, introduce                           rewriting and normalization that happened in the underly-
new goals and close some others. If the proof does not close                     ing logical representation is hidden from the user. Finally,
completely, the new view allows low-effort inspection of the                     when hovering with the cursor on the inline assertions/as-
proof state, which leads to refinement of the proof script.                      sumptions, the corresponding formulas on the sequent (in
The cycle continues until the proof succeeds. Examination                        case it is needed as a fallback) are highlighted and vice versa.
and interaction of the logical level remains optional in as                      In addition, the origins of the formula in the source code are
many cases as possible.                                                          highlighted. These highlights enable users to track formulas
                                                                                 and terms and seamlessly switch between the different rep-
4    Prototype Implementation of the                                             resentations. In addition to these presentation features, the
     Concept in KeY                                                              prototype also lifts the macros that are available in the GUI
                                                                                 of KeY to the source code level and makes them available
The interaction concept outlined in Section 3 has been im-
                                                                                 via the context menu, as shown in Figure 2. However, the
plemented in a prototype plugin extension2 for the graphical
                                                                                 possibility to record these high-level interactions as a proof
user interface of KeY comprising some 7 000 lines of Java. A
                                                                                 script is still a vision and the implementation remains future
screenshot of the GUI can be seen in Figure 2. While still
                                                                                 work.
early in development, the prototype contains the following
                                                                                    While implementing the requirements outlined in Sec-
features. First, the symbolically executed lines for the current
                                                                                 tion 3.1, we faced several challenges. We think the solutions
goal are shown with green background, with the most re-
                                                                                 and insights gained are not specific to KeY, but can also give
cently executed line more saturated. A prerequisite for this is
                                                                                 hints how to implement our concept in other interactive
that the symbolic execution has been completed, and no state
                                                                                 provers where interactions are performed on an underly-
transitions in form of modalities or updates are present on
                                                                                 ing logical representation different from the specification
the sequent. Since typically the symbolic execution is done
                                                                                 language.
fully automatic, and steps in between are not interesting for
the user, this is not a hard restriction. Second, as described in                4.1   Assigning Initial Origins
1 See https://keyproject.github.io/key-docs/user/ProofScripts/jml/ for details
                                                                                 Simplified, the proof obligation in KeY’s internal logic JavaDL
on the JML script mechanism in KeY
                                                                                 for a functional method contract 𝐶 = (pre, post, mod, term),
2 The implementation can be found at https://github.com/KeYProject/key/          where 𝐶’s components are JavaDL’s equivalents to requires,
tree/pfeifer/sourceInteractionPrototype                                          ensures, assignable, and measured_by, for instance method


Preprint
                                                                                        Wolfram Pfeifer, Mattias Ulbrich, and Daniel Drodt


m(p1 , . . ., p𝑛 ) is as follows, where self is an object of the     given as a schematic sequent 𝛼 0, 𝛼 1, ... =⇒, where the 𝛼𝑖 can
correct type:                                                        be either in antecedent or succedent. In this case, the new
                                                                 term 𝑡 gets the combined origins of 𝑡 and the 𝛼𝑖 . Intuitively,
   pre → res=self.m(p1 , . . ., p𝑛 ); (post ∧ frame)
                                                                     the rewritten term 𝑡 is the result of combining the 𝛼𝑖 and 𝑠,
We assign corresponding origin types to the subformulas              and thus gets the union of their origins. An example would
in pre, post, and frame while these terms and formulas are           be when 𝛼 is an equation in the antecedent that gets applied
created after parsing the specification. However, this proof         in a formula on the subterm 𝑠.
obligation provides only a very simplified view. In reality,            Apart from this, there are some general schemes we apply
many technical details have to be taken into account. In             to cover other categories of rules. First, terms that are newly
addition to the original precondition pre of the method, there       added by a rule do not get any origin. Second, if the resulting
are many additional formulas added to the premise of the             term (𝑡 in the above example) is a subterm of the matched
implication, which are necessary to faithfully model the Java        term (𝑠), it keeps its original origin. This is crucial to prevent
program in logic. This includes information about the well-          from too much accumulation. Third, terms that stem from
formedness of the heap (wellFormed (heap)), that the object          user input during a rule application (for example the cut rule)
referred to by self is created (self.created  TRUE), the            get a corresponding label, but no file or position information.
exact type of self, and more. When assigning origin types            Finally, all other terms that are not touched by a rule keep
to these implicit formulas, it is important to mark them as          their origins.
implicit to later be able to distinguish them from user inputs.         Two rules are essential for verification of programs: rules
The particular challenge for the implementation was that             for loops and method calls. Due to their complexity, they
these adaptations had to be done in Java code in the core of         are implemented in Java code within the prover core of KeY.
KeY, since this is where the generation of proof obligations         Both of them similarly split the proof into several branches,
happens.                                                             for instance where the loop invariant has to be shown to
                                                                     hold before entering the loop, the body has to be proven to
4.2   Transforming Origins Under Sequent Calculus                    preserve the invariant, and a use case that continues with
      Rules                                                          the symbolic execution of the remaining program while as-
After the initial creation of the proof obligation, all subformu-    suming the loop invariant. We assign position information
las in the sequent have an origin reference assigned, which          to the formulas originating from the specification (such as
already allows tracking where the formulas come from in              the loop invariant), and set distinct origin type labels for
the initial proof obligation. This information in itself can         the generated terms, which allows tracking them through-
already be helpful for the user, for example when variable           out the proof. A particularly interesting case is the “body
names might be changed during generation of the proof obli-          preserves invariant” branch, where the invariant formula
gation formula. However, since the purpose of the origin             appears twice and thus has the same source code position in-
information is to allow for tracking in later goals, it is crucial   formation. We distinguish them via different origin types. In
to know how to transform it under rule applications.                 addition, like in the initial proof obligation, several implicit
    KeY works deductively with a large set of rewriting and          formulas are added, which we again handle with specific
sequent calculus rules (more than 1 500). Most of them are           “implicit” origin types.
written in a domain specific language (called “Taclet lan-
guage”), and they can be classified into several categories.
For these categories, we present a generic scheme that allows        4.3   Translating Formulas from JavaDL back to JML
to maintain the origins throughout the proof. We have to             In the optimal case, when a formula has only a single unique
make sure not to accumulate origins too much, a problem we           origin and only refers to a single program state, its original
faced in earlier experiments: After some rule applications,          JML formula can be shown verbatim in an assertion or an
the origin of even a small subterm could become nearly the           assumption as described in Section 3.1. For cases where this
whole method contract, which is not helpful for the user.            is not possible, we implemented a translation back to JML.
    The first rule category are pure rewriting rules, which          With that, a particular challenge was that due to how the
can take a subterm 𝑠 of an arbitrary formula on either side          sequent calculus works in KeY, many terms get extracted
of the sequent and rewrite it into a different term 𝑡: 𝑠 ⇝ 𝑡.        with the “pull-out” rule into an equation with a new Skolem
In this case, we transfer the origin of 𝑠 to the new term 𝑡.         constant. This increases efficiency during proof search: If a
The intuition is that the formula was transformed without            term occurs multiple times in the sequent, its simplification
dependency to any additional position in source code. This           only has to be performed once. However, this poses a problem
can happen for example for symmetry rules of operators.              for the translation, since these Skolem constants only exist
    The second category is that of conditional rewrite rules.        on the low-level logical representation, but do not have a
It is similar to pure rewriting rules, but here the rule is only     direct counterpart in JML. To solve this challenge, we had to
applicable if an additional condition holds. This condition is       implement an inlining mechanism that reverts the pull-out.


Preprint
A New Interaction Concept for Interactive and Autoactive Program Verification


   A caveat is that the translation is not always possible: The             1 class C {
logical level may contain low-level constructs that cannot                  2   int sum, max;
be represented in JML. In these cases, the user is presented                3   void sumAndMax(int[] a) {
an assert/assume with a clear error message, and the only                   4     sum = 0;
way to continue is in the logical representation. However,                  5     max = 0;
this fall-back should occur rarely (if at all) in practice, since           6     int k = 0;
it only happens when implicit knowledge must be rendered                    7     while(k < a.length) {
but cannot. This is only the case if it stems from user input               8         ...
on the low-level logical view, and it is reasonable to continue             9     }
on this lower level.                                                       10   }
                                                                           11 }
4.4   Computing Positions for Assertions and
      Assumptions                                                                 (a) Example program with two heap assignments and a loop.
For modeling the heap, KeY uses the theory of arrays [21].
We use explicit terms to represent heap states. There are                       anon(                            // loop       line 7
functions select(ℎ, 𝑜, 𝑓 ) and store(ℎ, 𝑜, 𝑓 , 𝑣) to read and                     store(                         // assignment line 5
write from a heap, where ℎ is a heap, 𝑜 and object, 𝑓 a field,                      store(                       // assignment line 4
and 𝑣 a value (for simplicity, we ignore the types here).                             heap, self, C::$sum, 0)
An example term might be select(store(heap, self,                                   self, C::$max, 0),
A::$f, 5), self, A::$f), which with the help of the                               {(self, C::$max)} ∪ {(self, C::$sum)}
axiom selectOfStore could be simplified to 5. For more                            anon_heap_LOOP)
details, we refer to [1, ch. 2].                                                (b) Heap term formalizing all assignments up to line 8 in Figure 3a
   In general, a sequent of a program proof will contain many                   with corresponding line numbers from which the sub-terms origi-
of these terms, corresponding to different chains of read and                   nate.
write statements. The observation here is that every heap
term that occurs in the sequent corresponds to an exact line                    Figure 3. Example of a nested heap term for a program with
in source code. This is the case because such terms only                        heap assignments and a loop.
get created via symbolic execution of the program. If we
allowed a user to insert low-level formulas directly (e.g., via
the cut rule), this assumption would break, and the produced                    For assertions, this works vice versa: The initial position is
sequent could not be translated any more. However, in our                       the last line of the method, and they are shifted upwards
interaction concept the user should stay as long as possible                    until they reach a heap update not contained in the formula
(ideally always) on the code level.                                             or the most recently executed statement.
   An example of a heap term with corresponding line num-                          Formulas referring to multiple states are inserted into the
bers is shown in Figure 3. The function 𝑎𝑛𝑜𝑛 is used to                         code as late as possible, referring to other states with the JML-
anonymize a set of locations on the heap (the fields sum                        inspired operator \old<line>(<term>). This is in contrast
and max of this here). This is done when concrete code is                       to the concept in Section 3.1, where we describe the JML
abstracted by specifications, that is, for loop invariants and                  operator \old(<term>, <label>). However, the latter would
method contracts.                                                               require to introduce many additional labels and sometimes
   For the translation, we construct a heap map for the se-                     even blocks, which would modify and clutter the original
quent. A very similar approach is applied for local variables,                  source code. Since we only use the operator for presenting
which are handled in KeY by producing multiple copies, such                     to the user, a line number is more intuitive and easier to
as k_0, k_1, etc. For readability, we omit further details                      implement correctly.
about that here. With these maps available, the positioning
for assumptions and assertions works as follows. On the                         4.5   Limitations
path through the program corresponding to the current goal,                     Due to the prototypical state of the implementation, there
from the start of the method to the most recently executed                      are currently some limitations. First, the implementation
line, we (virtually) insert the assumptions and shift them                      only works for one of the two loop rules; for the other rule,
downwards, until a statement with a heap change is reached                      a clear error message is given such that the user can change
that is not part of the formula, or the most recently executed                  the settings accordingly. Second, goals where the assignable
statement is reached. For instance, a formula containing the                    clause has to be proven cannot be represented in JML at the
outer store term shown in Figure 3 and no other heap terms                      moment, since the corresponding formula is not expressible.
would be positioned directly in front of the loop, since the                    Third, when a formula deviates too much from the original
start of the loop would be the next line with a heap attached.                  user input or no origin information is found, a best-effort


Preprint
                                                                                      Wolfram Pfeifer, Mattias Ulbrich, and Daniel Drodt


re-translation has to be performed, which is currently only                               Task 1                  Task 2
implemented partially. Finally, the branch corresponding to             Participant   New Source View          Sequent View
the framing clause of a method contract or loop specification                              (min)                   (min)
can currently not be represented in JML, since the corre-                   1                5.0                    11.0
sponding JavaDL formula quantifies over fields, which is not                2               16.5                    11.5
expressible in JML. As a future workaround, there is a func-                3                8.0                     5.0
tion assignable that could be used to represent this formula                4                1.0                    12.0
on JML level, however, this is currently not yet implemented.               5               16.0                     8.0
                                                                            6               12.5                    18.5
                                                                            𝜇                 9.8                   11.0
5     User Study                                                            𝜎                 5.7                    4.1
To evaluate the efficacy of the interaction concept and the
prototype implementation on first contact, we conducted           Table 1. Results of the user study: Reported required times
a pilot user study with six experts in formal verification,       by the individual participants. 𝜇 denotes the average time
most of them seasoned users of the KeY system. The goal           per task and 𝜎 is the standard deviation.
of the study was to find out if interaction on source code
and representing goals inline in source code can support the
user in their verification process. The study is designed to
get a first impression of the new view’s effect on goal state        The study design intentionally favored the original se-
comprehension rather than a representative examination. At        quent view and interaction in two respects. First, partici-
the time the user study was conducted, the prototype did          pants were already familiar with the existing interaction
not yet support proof scripts.                                    model in KeY. Second, they encountered the new features
                                                                  in the first task, so they had to develop their understanding
                                                                  of the program while using the novel interface. Because the
5.1   Study Design                                                second task involved essentially the same program, partici-
Written explanations, source code, a KeY version, and a ques-     pants were already familiar with its structure and only had
tionnaire were provided to the participants. All participants     to locate the second flaw in the sources.
were sufficiently familiar with the KeY system that a general
KeY tutorial was unnecessary.                                     5.2    Results
   The study comprised two verification tasks to be per-          All participants successfully identified the problems in both
formed on two very similar variants of a small program with       parts. Apparently, the new view was sufficiently intuitive:
about 40 lines of Java code and 50 lines of JML specification.    although intentionally no information was provided explain-
The program implements a Caesar cipher over a character           ing the concepts and features of the new view, all partici-
array and contains two methods, each featuring a loop and         pants were able to intuitively understand the idea behind the
several branching statements. Both tasks required correcting      overlaid source annotations, and the semantics of the new
a small flaw in either the source code or the specification;      constructs (for instance the \old operator with line number),
the tasks were designed to be comparable in difficulty.           and could explain them correctly in the questionnaire.
   For the first task, participants were asked to interact with      Half of the participants solved task 1 faster than task 2
the new view with inline overlays (the original sequent view      despite the missing introduction, the order of the related
was not permitted) to identify and locate the flaw that pre-      tasks, and their prior experience with KeY. An overview of
vented verification. A screenshot of the GUI with an open         the reported times required to finish both tasks can be found
goal from this task is shown in Figure 4. Note that the se-       in Table 1. While the average required time is slightly larger
quent view (as normally present in KeY, compare Figure 1)         for task 2 with the old view, the standard deviation is larger
is hidden. Only the source view is shown, where symboli-          with the new one.
cally executed lines, generated assumptions and assertions,          In addition to this quantitative feedback, the study also
and the origin of the assertion that is hovered over with the     collected qualitative feedback in the form of recommenda-
mouse cursor (in magenta) are shown.                              tions and remarks. In particular, some suggestions were to
   In the second task, the participants performed an equiva-      include the type (for instance, if a formula stems from an im-
lent exercise using the original sequent view; overlays were      plicit default in JML) in the display. Also, users particularly
not available. Participants recorded the time they spent on       liked that technical details needed for the representation in
each task. After completing the experiment, they responded        JavaDL, but not present in JML, are not shown at all.
to open-ended questions regarding the new interaction con-           Overall, the study shows that the new concept and imple-
cept and its implementation.                                      mentation can be helpful even for KeY experts, and that a


Preprint
A New Interaction Concept for Interactive and Autoactive Program Verification




Figure 4. Screenshot of the KeY GUI showing an open goal state of the first task of the user study using the new source code
level representation.

view closer to the original representation in the user input                    does reliably show is that, even without prior explanation,
can be beneficial for understanding the sequent. Since the                      participants were able to grasp the new features added to the
new interactive view is not exclusive and can be used in                        tool. One cannot conclude from this pilot study of KeY ex-
combination with the established forms of interaction, users                    perts that a novice to KeY or to deductive verification would
can work with what they find more intuitive and even switch                     benefit from the new view. However, it suggests that even
back and forth within a single proof.                                           experts familiar with KeY’s logical representation and inter-
                                                                                nals seem to find the new view helpful. It stands to reason
5.3   Validity of the Results                                                   that similar benefits can be expected from KeY beginners,
It should be emphasized that this evaluation was intended                       though this remains to be tested.
to provide qualitative evidence and to obtain constructive
feedback about the usefulness and understandability of the                      6   Related Work
proposed source code level interaction concept, not to deliver                  A number of verification tools are based on the autoactive
strong empirical claims about achievable user performance                       approach and, hence, provide interaction patterns similar to
differences based on the reported times. Given the small                        our work. Dafny [20] is a programming language designed to
number of participants, the measured task durations and                         be easily verified and provides an autoactive verifier. Users
the observed differences in completion times must be in-                        typically stay purely on the source code level and guide
terpreted cautiously: they illustrate possible benefits rather                  the underlying SMT solver with annotations like assume and
than constituting statistically generalizable results. Neither                  assert. Interaction on a lower-level, as in KeY, is not possible.
is the sample size sufficient nor are the participants—being                       The verification tool Why3 [14] provides autoactive in-
experts in KeY—representative of the average verification                       teraction similar to Dafny. While some interaction on the
engineer to draw any statistical conclusions. What the study                    level of its programming language WhyML is possible, this


Preprint
                                                                                           Wolfram Pfeifer, Mattias Ulbrich, and Daniel Drodt


is not an end user language, as it is a functional language          be considerably easier than persisting low-level sequent in-
with some logical extensions. Some tools like Creusot [13]           teractions in this way.
use it as a back-end for Rust verification.                             Additionally, we aim to expand the pilot study of the new
   On the other hand, VeriFast [17] targets full program lan-        view and interaction pattern into a full, reliable, and repre-
guages like Java, C, and Rust, similar to KeY. It is purely an       sentative user study aimed both at experts and, crucially, KeY
autoactive prover with annotations to guide the prover.              novices. A suitable setting would be to test these features
   We note that KeY is the only verification tool targeting an       in teaching where KeY is already employed and measure
end user language that provides explicit, fine-grained proof         the effects of the more abstract view on the student’s under-
objects, permitting detailed proof interaction.                      standing of the proof state—a common hurdle for students.
   JML scripts have a number of precursors and related ap-
proaches. Beckert et al. [3] first realized the potential of
extending a verifier such as KeY with a scripting language,          Acknowledgments
simplifying manual proof applications. While their scripts           This work is supported by the German Research Foundation
offer much the same expressiveness and power of the JML              under Grants No. BE 2334/9-1, BU 2924/3-1, HA 2617/9-1,
scripts, the scripts were external, not part of the specification-   and UL 433/3-1.
level code.                                                            We thank Mike Schwörer for his instrumental work on
   Similar in approach, Grebing et al. developed the Dafny           the new interaction view and the user study.
Interactive Verifier Environment (DIVE), which provides a
new GUI for Dafny proofs. This GUI provides access to the
source code, a formula-based logic view, and direct access to        References
proof manipulation in the form of proof scripts and rule ap-          [1] Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, Reiner Hähnle,
                                                                          Peter H. Schmitt, and Mattias Ulbrich (Eds.). 2016. Deductive Software
plications [15]. While conceptually close, DIVE differs from              Verification – the KeY Book: From Theory to Practice. Number 10001 in
our approach in some respects: DIVE extends the autoactive                LNCS. Springer. doi:10.1007/978-3-319-49812-6
Dafny system with an explicit logic view and manual rule              [2] Bernhard Beckert, Richard Bubel, Daniel Drodt, Reiner Hähnle, Florian
applications, whereas KeY is already based on this approach               Lanzinger, Wolfram Pfeifer, Mattias Ulbrich, and Alexander Weigl.
and is now equipped with new abstractions, empowering                     2025. The Java Verification Tool KeY: A Tutorial. In Formal Methods
                                                                          (LNCS, 14934), Andre Platzer, Kristin Yvonne Rozier, Matteo Pradella,
users.                                                                    and Matteo Rossi (Eds.). Springer Nature Switzerland, Cham, 597–623.
                                                                          doi:10.1007/978-3-031-71177-0_32
                                                                      [3] Bernhard Beckert, Sarah Grebing, and Mattias Ulbrich. 2017. An Inter-
                                                                          action Concept for Program Verification Systems with Explicit Proof
7    Conclusion                                                           Object. In Hardware and Software: Verification and Testing, Ofer Strich-
                                                                          man and Rachel Tzoref-Brill (Eds.). Springer International Publishing,
In this paper, we presented a novel interaction concept in-               Cham, 163–178. doi:10.1007/978-3-319-70389-3_11
tegrating interactive and autoactive verification. It helps           [4] Bernhard Beckert, Jonas Klamroth, Wolfram Pfeifer, Patrick Röper,
to bridge the mental gap between the source code level,                   and Samuel Teuber. 2024. Towards Combining the Cognitive Abilities
where program and specification are written, and the logical              of Large Language Models with the Rigor of Deductive Progam Veri-
                                                                          fication. In 12th International Symposium on Leveraging Applications
level, where the proof is conducted when inspecting and
                                                                          of Formal Methods, Verification and Validation (ISoLA 2024). Software
manipulating open proof goals. We implemented the con-                    Engineering Methodologies, Tiziana Margaria and Bernhard Steffen
cept within the deductive Java verifier KeY and conducted a               (Eds.). Springer, 242–257. doi:10.1007/978-3-031-75387-9_15
small user study which indicates that the novel view of the           [5] Bernhard Beckert and Vladimir Klebanov. 2004. Proof Reuse for
program-verification state can indeed help users better un-               Deductive Program Verification. In Proceedings of the Second Inter-
derstand goals and identify and repair flaws in specifications            national Conference on Software Engineering and Formal Methods,
                                                                          Jorge Cuellar and Zhiming Liu (Eds.). IEEE Computer Society, 77–
and source code.                                                          86. doi:10.1109/SEFM.2004.10013
   A promising idea for future work is to use the new inlined,        [6] Bernhard Beckert, Vladimir Klebanov, and Mattias Ulbrich. 2015. Re-
annotated view not only for human users but also as input                 gression Verification for Java Using a Secure Information Flow Calcu-
to other tools. For example, if a goal cannot be proven in                lus. In Proc. 17th FTfJP (FTfJP ’15), Rosemary Monahan (Ed.). ACM,
KeY, the view with the explicit assumptions local to that                 Prague, Czech Republic, 6:1–6:6. doi:10.1145/2786536.2786544
                                                                      [7] Bernhard Beckert, Peter Sanders, Mattias Ulbrich, Julian Wiesler, and
proof goal could be rendered into a file which can be loaded              Sascha Witt. 2024. Formally Verifying an Efficient Sorter. In TACAS
into a bounded model checker. Also, this annotated source                 Proc., Part I (LNCS, 14570), Bernd Finkbeiner and Laura Kovács (Eds.).
file might improve the output of specification-inference ap-              Springer, 268–287. doi:10.1007/978-3-031-57246-3_15
proaches based on large language models [4], since it pro-            [8] Maurice H. ter Beek, Rod Chapman, Rance Cleaveland, Hubert Garavel,
vides more detailed information about local knowledge.                    Rong Gu, Ivo ter Horst, Jeroen J. A. Keiren, Thierry Lecomte, Michael
                                                                          Leuschel, Kristin Yvonne Rozier, Augusto Sampaio, Cristina Seceleanu,
   A second direction is a tighter integration with proofs                Martyn Thomas, Tim A. C. Willemse, and Lijun Zhang. 2024. Formal
scripts: The point-and-click interactions performed on the                Methods in Industry. Form. Asp. Comput. 37, 1 (Dec. 2024), 7:1–7:38.
source view could be recorded into a script, which should                 doi:10.1145/3689374



Preprint
A New Interaction Concept for Interactive and Autoactive Program Verification


 [9] Stefan Blom and Marieke Huisman. 2014. The VerCors Tool for Verifi-             and Systems, Haim Kilov, Bernhard Rumpe, and Ian Simmonds (Eds.).
     cation of Concurrent Programs. In FM 2014: Formal Methods, 19th Intl.           Number 523 in The Kluwer International Series in Engineering and
     Symposium, Singapore (LNCS, 8442), Cliff B. Jones, Pekka Pihlajasaari,          Computer Science. Springer, 175–188. doi:10.1007/978-1-4615-5229-
     and Jun Sun (Eds.). Springer, 127–131. doi:10.1007/978-3-319-06410-             1_12
     9_9                                                                        [19] Gary T. Leavens, David R. Cok, and Amirfarhad Nilizadeh. 2022.
[10] Martin de Boer, Stijn de Gouw, Jonas Klamroth, Christian Jung, Mat-             Further Lessons from the JML Project. In The Logic of Software. A
     tias Ulbrich, and Alexander Weigl. 2023. Formal Specification and               Tasting Menu of Formal Methods: Essays Dedicated to Reiner Hähnle
     Verification of JDK’s Identity Hash Map Implementation. Formal                  on the Occasion of His 60th Birthday, Wolfgang Ahrendt, Bernhard
     Aspects Comput. 35, 3 (Sept. 2023), 18:1–18:26. doi:10.1145/3594729             Beckert, Richard Bubel, and Einar Broch Johnsen (Eds.). Number
[11] David R. Cok. 2011. OpenJML: JML for Java 7 by Extending Open-                  13360 in LNCS. Springer International Publishing, Cham, 313–349.
     JDK. In NASA Formal Methods (LNCS, 6617), Mihaela Bobaru, Klaus                 doi:10.1007/978-3-031-08166-8_15
     Havelund, Gerard J. Holzmann, and Rajeev Joshi (Eds.). Springer,           [20] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Verifier for
     Berlin, Heidelberg, 472–479. doi:10.1007/978-3-642-20398-5_35                   Functional Correctness. In LPAR-16, Revised Selected Papers (LNCS,
[12] Stijn De Gouw, Jurriaan Rot, Frank S. De Boer, Richard Bubel, and               6355), Edmund M. Clarke and Andrei Voronkov (Eds.). Springer, 348–
     Reiner Hähnle. 2015. OpenJDK’s java.utils.Collection.sort() Is Broken:          370. doi:10.1007/978-3-642-17511-4_20
     The Good, the Bad and the Worst Case. In Proc. 27th Intl. Conf. on         [21] John McCarthy. 1963. A Basis for a Mathematical Theory of Compu-
     Computer Aided Verification (CAV), San Francisco (LNCS, 9206), Daniel           tation. In Computer Programming and Formal Systems, P. Braffort and
     Kroening and Corina Pasareanu (Eds.). Springer, 273–289. doi:10.1007/           D. Hirschberg (Eds.). North Holland, 33–69.
     978-3-319-21690-4_16                                                       [22] Bertrand Meyer. 1992. Applying "Design by Contract". Computer 25,
[13] Xavier Denis, Jacques-Henri Jourdan, and Claude Marché. 2022.                   10 (1992), 40–51. doi:10.1109/2.161279
     Creusot: A Foundry for the Deductive Verification of Rust Programs.        [23] Wytse Oortwijn, Marieke Huisman, Sebastiaan J. C. Joosten, and Jaco
     In ICFEM 2022, Proceedings (LNCS, 13478), Adrián Riesco and Min                 van de Pol. 2020. Automated Verification of Parallel Nested DFS. In
     Zhang (Eds.). Springer, 90–105. doi:10.1007/978-3-031-17244-1_6                 TACAS, Armin Biere and David Parker (Eds.). Springer International
[14] Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3 — Where              Publishing, Cham, 247–265. doi:10.1007/978-3-030-45190-5_14
     Programs Meet Provers. In Proceedings of the 22nd European Sympo-          [24] João Pereira, Tobias Klenze, Sofia Giampietro, Markus Limbeck, Diony-
     sium on Programming (LNCS, 7792), Matthias Felleisen and Philippa               sios Spiliopoulos, Felix Wolf, Marco Eilers, Christoph Sprenger, David
     Gardner (Eds.). Springer, 125–128. doi:10.1007/978-3-642-37036-6_8              Basin, Peter Müller, and Adrian Perrig. 2025. Protocols to Code: For-
[15] Sarah Grebing, Jonas Klamroth, and Mattias Ulbrich. 2020. Seamless              mal Verification of a Secure Next-Generation Internet Router. In Proc.
     Interactive Program Verification. In Verified Software. Theories, Tools,        of the 2025 ACM SIGSAC Conference on Computer and Communications
     and Experiments, Supratik Chakraborty and Jorge A. Navas (Eds.).                Security (CCS ’25), Chun-Ying Huang, Jyh-Cheng Chen, and Shiuh-
     Springer International Publishing, Cham, 68–86. doi:10.1007/978-3-              pyng Shieh (Eds.). Association for Computing Machinery, New York,
     030-41600-3_6                                                                   NY, USA, 1469–1483. doi:10.1145/3719027.3765104
[16] Hans-Dieter A. Hiep, Olaf Maathuis, Jinting Bian, Frank S. de Boer,        [25] Philipp Rümmer and Mattias Ulbrich. 2016. Proof Search with Taclets.
     Marko van Eekelen, and Stijn de Gouw. 2020. Verifying OpenJDK’s                 See [1], 107–147. doi:10.1007/978-3-319-49812-6_4
     LinkedList Using KeY. In TACAS (LNCS, 12079), Armin Biere and David        [26] Mohsen Safari, Wytse Oortwijn, and Marieke Huisman. 2021. Auto-
     Parker (Eds.). Springer, Cham, 217–234. doi:10.1007/978-3-030-45237-            mated Verification of the Parallel Bellman–Ford Algorithm. In Static
     7_13                                                                            Analysis, Cezara Drăgoi, Suvam Mukherjee, and Kedar Namjoshi (Eds.).
[17] Bart Jacobs and Frank Piessens. 2008. The VeriFast Program Veri-                Springer International Publishing, Cham, 346–358. doi:10.1007/978-3-
     fier. Technical Report CW-520. Department of Computer Science,                  030-88806-0_17
     Katholieke Universiteit Leuven. http://www.cs.kuleuven.be/~bartj/          [27] Johanna Stuber. 2023. Verification of Red-Black Trees in KeY – A Case
     verifast/verifast.pdf                                                           Study in Deductive Java Verification. Bachelor Thesis. Karlsruhe Insti-
[18] Gary T. Leavens, Albert L. Baker, and Clyde Ruby. 1999. JML: A                  tute of Technology (KIT). doi:10.5445/IR/1000162878
     Notation for Detailed Design. In Behavioral Specifications of Businesses




Preprint
