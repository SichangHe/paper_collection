                                              Cooperative Verification via Collective Invariant Generation
                                                                         Jan Haltermann∗                                                                 Heike Wehrheim
                                                                        Paderborn University                                                             Paderborn University
                                                                        Paderborn, Germany                                                               Paderborn, Germany
                                                                          jfh@mail.upb.de                                                                 wehrheim@upb.de

                                         ABSTRACT                                                                                    to advances in SAT and SMT solving and on the other hand due
                                         Software verification has recently made enormous progress due                               to novel verification methods like interpolation in model check-
                                         to the development of novel verification methods and the speed-                             ing [37], automata-based software verification [31] or property
                                         up of supporting technologies like SMT solving. To keep software                            directed reachability [16]. Still, automatic verification remains a
arXiv:2008.04551v1 [cs.SE] 11 Aug 2020




                                         verification tools up to date with these advances, tool developers                          complex and error-prone task. In particular, it is often the case that
                                         keep on integrating newly designed methods into their tools, al-                            one tool can verify a particular class of programs, but fails to verify
                                         most exclusively by re-implementing the method within their own                             other classes (or even gives incorrect answers), whereas it is the
                                         framework. While this allows for a conceptual re-use of methods,                            reverse situation for another tool. Moreover, to keep their tools up
                                         it requires novel implementations for every new technique.                                  to date with novel techniques, tool developers keep on integrating
                                             In this paper, we employ cooperative verification in order to avoid                     them by re-implementation within their framework.
                                         re-implementation and enable usage of novel tools as black-box                                  An approach for changing this unsatisfactory situation is co-
                                         components in verification. Specifically, cooperation is employed                           operative verification (for an overview see [13]). Cooperative ver-
                                         for the core ingredient of software verification which is invariant                         ification builds on the idea of letting tools (and thus techniques)
                                         generation. Finding an adequate loop invariant is key to the success                        cooperate on verification tasks, thereby leveraging the tool’s in-
                                         of a verification run. Our framework named CoVerCIG allows a                                dividual strengths. In particular, cooperative verification aims at
                                         master verification tool to delegate the task of invariant generation                       black box combinations of tools, using existing tools off-the-shelf
                                         to one or several specialized helper invariant generators. Their                            without re-implementation. While this sounds like a natural idea,
                                         results are then utilized within the verification run of the master                         its realization poses a number of challenges, the major one being
                                         verifier, allowing in particular for crosschecking the validity of                          the exchange and usage of analysis information. For cooperation,
                                         the invariant. We experimentally evaluate our framework on an                               tools are required to produce (partial) results which other tools can
                                         instance with two masters and three different invariant generators                          understand and employ in their verification run. With conditional
                                         using a number of benchmarks from SV-COMP 2020. The experi-                                 model checking [7], the first proposal of an exchange format for
                                         ments show that the use of CoVerCIG can increase the number of                              verification results was made. A conditional model checker outputs
                                         correctly verified tasks without increasing the used resources.                             its (potentially partial) result in the form of a condition which can
                                                                                                                                     be read by other conditional model checkers in order to complete
                                         CCS CONCEPTS                                                                                the verification task. Since verification tools normally do not un-
                                                                                                                                     derstand conditions, reducers [9, 23] have been proposed to bring
                                         • Software and its engineering → Formal software verifica-
                                                                                                                                     conditions back into a form understandable by verifiers, namely
                                         tion.
                                                                                                                                     into (residual) programs describing the so far unverified program
                                                                                                                                     part. This allows the result of a conditional model checker to be
                                         KEYWORDS
                                                                                                                                     made usable by arbitrary other verifiers. A second type of exist-
                                         Cooperation, Software Verification, Invariant Generation                                    ing result usage is the validation of tool’s results [4, 34], similar to
                                         ACM Reference Format:                                                                       proof-carrying code [38]. Both of these types are sequential forms
                                         Jan Haltermann and Heike Wehrheim. 2020. Cooperative Verification via                       of cooperation: a first verifier starts and a second verifier continues,
                                         Collective Invariant Generation.                                                            either by completing or by validating a first result.

                                         1     INTRODUCTION
                                         Recent years have seen a major progress in software verification                            In this paper, we propose CoVerCIG, a cooperation framework
                                         as for instance witnessed by the annual competition on software                             which complements these existing approaches by a new type of
                                         verification SV-COMP [2]. This success is on the one hand due                               cooperation. Conceptually, this framework (depicted in Figure 1)
                                         ∗ This author was partially supported by the German Research Foundation (DFG) under         consists of a master verifier and a number of helper invariant gener-
                                         contract 418257054.                                                                         ators. The master verifier has the overall control on the verification
                                                                                                                                     process and can delegate tasks to helpers as well as continue its
                                         Permission to make digital or hard copies of part or all of this work for personal or       own verification process with (partial) results provided by helpers.
                                         classroom use is granted without fee provided that copies are not made or distributed
                                         for profit or commercial advantage and that copies bear this notice and the full citation   The helpers run in parallel as black boxes without cooperation.
                                         on the first page. Copyrights for third-party components of this work must be honored.      The task to be delegated is an integral part of software verification,
                                         For all other uses, contact the owner/author(s).
                                                                                                                                     namely invariant generation. The framework allows cooperation
                                         © 2020 Copyright held by the owner/author(s).
                                                                                                                                     via outsourcing the task of invariant generation, leveraging the
                                                                                                                                     strength of specialized invariant generation tools.
                                                                                                                                                             Haltermann and Wehrheim


  Program                                                                                                  • We carry out an extensive experimental evaluation demon-
                                              Master
                                                                                             Result          strating the effectiveness and efficiency of collective invari-
                                              Verifier
 Property                                                            Prog
                                                                                                             ant generation.
                                op         WitnessInjector
                             +Pr                                         +Pr
                      Prog                Witness Witness
                                                                            op

            Mapper            Adapter                             Adapter           Mapper
                                                                                                      2    FUNDAMENTALS
            Task                                                                      Task
                                                                                                      We aim at the cooperative verification of programs written in GNU
                              Invariant                       Invariant
             Helper Invari-                                                 Helper Invari-
                                                                                                      C, focusing on the validation of safety properties. To be able to
             ant Generator            ||        ...          ||             ant Generator             define safety properties, a formal representation of programs as
                                                                                                      well as their semantics is needed. Thus we next briefly introduce
                                                                                                      the syntax and semantics of programs which we consider here.
                                                                                                         We follow the notation of Beyer et al. [6] describing programs
             Figure 1: Collective invariant generation
                                                                                                      as control-flow automata (CFAs). A CFA is basically a control-flow
                                                                                                      graph with edges annotated with program statements. More for-
                                                                                                      mally, a program is represented as a control-flow automaton
   Like for other types of cooperation, the question of the exchange                                  C = (L, l 0 , G), consisting of a set of program locations L, an ini-
format for results comes up. Here, we have chosen correctness wit-                                    tial location l 0 ∈ L and the control-flow edges G, G ⊆ L × Op × L.
nesses [3] for this purpose. Correctness witnesses are employed                                       The set Op contains all possible operations on integer variables2
in witness validation and certify a verifier’s result stating the cor-                                present in the program, namely conditions (as of conditionals and
rectness of a program. These witnesses are particularly well suited                                   loops), assignments, method calls and return statements. Figure 2(a)
for our intended usage, because their format is standardized and                                      shows a C-program taken from the SV-COMP benchmarks3 , and
a number of verifiers already produce correctness witnesses. To                                       Figure 2(b) its corresponding CFA. The program also contains a
account for the incooperation of helper verifiers not producing                                       special error label, used for encoding the property to be verified. The
witnesses, our framework also foresees the inclusion of adapters                                      verification task for this program is to show the non-reachability
transforming invariants into correctness witnesses. We provide an                                     of the error label at location 9, i.e., for our example program the
implementation of two such adapters. Witnesses are then injected                                      verifier has to prove that y equals n after the loop which is true
into the verification run of the master. For stating the task to be                                   (since n is unsigned).
solved by invariant generators we furthermore require mappers                                            For the semantics, we start by defining program states. Let Var
transforming program and property to be proven into a task format                                     denote the set of all integer variables occurring in programs, BExp
understandable by the helper tools. Figure 1 depicts our framework                                    the set of boolean expressions and AExp the set of arithmetic ex-
for collective invariant generation. The framework can be arbitrar-                                   pressions over Var. Then a state σ of the program is a mapping from
ily configured with different masters and helpers, provided that                                      the variables to the integers, i.e., σ : Var → Z. We lift the mapping
suitable adapters and mappers are given.                                                              to also contain the evaluation of arithmetic and boolean expressions
   We have implemented our framework within the CPAchecker                                            so that σ maps AExp to Z and BExp to B. A finite program path
                                                                                                                                                      д0                дn−1
framework [10] and have employed different configurations of it as                                    π is a sequence of transitions ⟨σ0 , l 0 ⟩ → ⟨σ1 , l 1 ⟩ · · · → ⟨σn , ln ⟩,
master verifier. As helper verifiers we have chosen publicly available                                such that σ0 assigns 0 to all variables, ln is a leaf in the CFA and
verification tools, some producing and one not producing witnesses.                                                                                                дi
                                                                                                      (li , дi , li+1 ) ∈ G holds for each transition ⟨σi , li ⟩ → ⟨σi+1 , li+1 ⟩ in
We have then experimentally evaluated 14 different combinations
                                                                                                      π . Infinite program paths are defined analogeously. As for state
of master and helper on benchmarks of the annual competition
                                                                                                      changes in paths: If дi is a boolean expression, method call or return
of software verification SV-COMP [2]. The experiments show an
                                                                                                      statement, then σi = σi+1 holds. If дi is an assignment x = a, where
improvement over the verification capabilities of the master tool,
                                                                                                      a ∈ AExp, then σi+1 = σi [x 7→ σi (a)]. Finally, we denote all paths
without incurring significant overhead. In some cases, the verifica-
                                                                                                      of a program represented by a CFA C by paths(C).
tion time is even decreased in cooperative verification.
Summarizing, we make the following contributions.                                                         Here, we are interested in verifying safety properties of programs
                                                                                                      given as CFAs. For the purpose of this paper, we define a safety
     • We propose a framework for cooperative software verifi-
                                                                                                      property P as a pair of a location ℓ ∈ L and a boolean condition
       cation based on a master-helper architecture for collective
                                                                                                      φ ∈ BExp. There can be multiple safety properties required to hold
       invariant generation.
                                                                                                      in a program. For our example program of Figure 2 the property is
     • We construct 14 different instantiations of the framework us-
                                                                                                      (8, n = y). For the verifier this is encoded in the form
       ing 2 masters and 3 helpers, running both helpers in isolation
       as well as in parallel.                                                                           8: if (!(n==y))
     • For the inclusion of helper verifiers, we implement two                                           9:         Error: return 1;
       adapters, one transforming invariants expressed in the LLVM                                    Later, we will see that different verifers require different encodings
       IR language1 into correctness witnesses, the other modifying                                   of the property to be checked, and hence mappers need to be applied
       a generated witness as to bring it into the right format.                                      to translate property encodings.
                                                                                                      2 In our formalization, we use integer variables only, the implementation covers C
                                                                                                      programs.
1 https://llvm.org/docs/LangRef.html                                                                  3 https://github.com/sosy-lab/sv-benchmarks
Cooperative Verification via Collective Invariant Generation



                                                                                                                                start     q1       o/w
 1   int main() {
 2     unsigned int n = nondet();                              start         1
                                                                                                                                            1,enterFunc
                                                                                 n=nondet()
 3     unsigned int x = n, y = 0;
                                                                             2                                                  o/w       q2       n == x+y
 4     while(x > 0){                                                             x=n
 5        x--;                                                               3                           8                3,enterLoopHead
                                                                                        ¬ (x>0)
 6        y++; }                                                       y=0
                                                                                                                                                  4,else
 7     // Safety property                                                    4             n==y              ¬ (n==y)           o/w       q3                     q5        o/w
 8     if (!(n == y)) {                                                          (x>0)                                                              7,then            7,else
                                                               y++           5                11         9                6,enterLoopHead       4,then
 9       Error: return 1; }                                                      x- -    ret 0           ret1
10     return 0;                                                             6                                                            q4          q6              q7
                                                                                              12       10
11   }
                                                                                                                                            o/w            o/w          o/w
                      (a) C code example                                (b) The corresponding CFA                                   (c) Part of the witness

                                   Figure 2: An example program, its control flow automaton and one witness

<node id="q3">                                                                                     can be equipped with boolean expressions. When all these boolean
    <data key=" invariant ">n == x+y</data>                                                        expressions are either true or false, we call the witness trivial. Source
    <data key=" invariant . scope">main</data>                                                     code guards are of the form location,type where type can be
</node>                                                                                            then, else, enterFunc and enterLoopHead. The guard o/w (other-
<edge source="q2" target ="q3">                                                                    wise) is used if a source code line does not match the other guards
    <data key="enterLoopHead">true</data>                                                          present. Via these labels we can match transitions of the automaton
    <data key=" startline ">3</data>                                                               with edges in the CFA.
    <data key="endline">3</data>                                                                      In Figure 2(c), we see a correctness witness for our example pro-
     ...                                                                                           gram. State q 3 is reached by transitions labelled 3,enterLoopHead
</edge>                                                                                            or 6,enterLoopHead and thus corresponds to the loop head at pro-
                                                                                                   gram location 4. Associated with this state is the invariant n = x +y.
                                                                                                      Syntactically, correctness witnesses are stored in an XML format
 Figure 3: Excerpt of a correctness witness for the example                                        and consist of two parts: (1) general information like the producer
                                                                                                   of the witness or the program associated with the witness, and
                                                                                                   (2) a GraphML representation of the witness automaton. Figure 3
   A CFA (or program) C violates a safety property P = (ℓ, φ) when                                 shows an excerpt of this format for the witness in Figure 2(c). More
the program reaches location ℓ in a state which does not satisfy φ.                                information and a formal specification of correctness witnesses can
More formally, P is violated by C, if there is some path π ∈ paths(C),                             be found in [3].
               д0                дn−1
π = ⟨σ0 , l 0 ⟩ → ⟨σ1 , l 1 ⟩ · · · → ⟨σn , ln ⟩ and some i, 0 ≤ i ≤ n, such
that ℓi = ℓ and σi (φ) = false.
   Cooperatively verifying safety of programs is achieved in our                                   3     CONCEPT
framework via collective (loop) invariant generation. Syntactically,                               In this section, we introduce our novel concept of Cooperative
a loop invariant is a boolean expression associated to a loop head. A                              Verification via Collective Invariant Generation (CoVerCIG), shown
loop invariant needs to hold (1) before the first loop execution and                               in Figure 1. The framework contains two sorts of main components:
(2) after each loop execution. The expression n = x +y, for instance,                              Master verifiers (one) and helper invariant generators (several).
is a loop invariant for the program in Figure 2(a), associated to the                              Next, we state some requirements on and explain the functionality
loop head at location 4. This loop invariant facilitates verification of                           of these components as well as their cooperation.
the safety property, because in conjunction with the negated loop
condition and information about initial variable values it ensures n
to be equal to y after the loop. Other valid loop invariants would                                 3.1        Components of the CoVerCIG-Framework
be x ≥ 0, n = 3 ⇒ y ≤ 5 or true, which however all do not help in                                  The most important component of the framework is the master
proving the safety property. Especially the loop invariant true does                               verifier, which we build out of an existing verifier. The master
not provide any information, as it always is a valid loop invariant.                               is responsible for coordinating the verification process and can,
Thus, we call it a trivial invariant.                                                              if needed, request support from the second type of components,
   As stated before, we chose witnesses (more specifically, correct-                               the helpers, in the form of invariants as described by correctness
ness witnesses) as exchange format during collective invariant                                     witnesses. Hence, the master is also steering the cooperation.
generation. Formally, a witness is a finite state automaton in which                                  In the following, we explain the two sorts of main components
transitions are labelled with so called source code guards and states                              in more detail:
                                                                                                                          Haltermann and Wehrheim


                                                                           Table 1: Overview of the configuration options available
  Invariants over                Invariants over
                     translate                      construct
 IR-variables with               C-variables with               witness
    IR-locations                   C-locations                                       Name                     Description              Values
                                                                                restartMaster            restart the master after      boolean
               Figure 4: Workflow of an adapter                                                           invariant generation
                                                                           termAfterFirstInv              use first witness only      boolean
                                                                                timerM                 maximum time for master        time in s
   Master Verifier A master verifier gets as input the program                                         until requestsForHelp is
     C as CFA and a safety property P. It computes as output a                                                      send
     boolean answer b, stating whether the property holds, and                     timeoutH            maximum time for helpers       time in s
     possibly (but not necessarily) provides an overall witness                                         to generate an invariant
     ω. To be able to process the provided support in form of
     invariants stored inside of correctness witnesses, a master is
     required to implement an internal function called injectWit-
     ness. The function loads a witness, extracts the invariants
                                                                          3.2      Cooperation within CoVerCIG
     present in it and injects them into the analysis of the mas-         After having explained the individual components, we define their
     ter verifier. The witness injection can either happen before         interaction in the framework. In this paper, we focus on the paral-
     (re-)starting the analysis or during runtime. We exemplify           lel execution of several helpers which implement complementary
     the realization of witness injection later.                          approaches so that we can leverage their individual strengths. Al-
   Helper Invariant Generator A helper invariant generator                gorithm 1 describes the form of cooperation. It is steered by several
     gets as input the program C as CFA and a safety property             user configurable options which fix aspects like time and resource
     P. It computes as output a set of invariants, stored in a ver-       limits of master and helpers. Table 1 summarizes the configuration
     ification witness ω ′ . The generated invariants are neither         options. We next describe them in detail.
     required to be helpful for the master verifier nor to be correct.          Master options The following aspects of the master’s behav-
     Thus, helper invariant generators are also allowed to gen-                   ior need to be fixed: First, when to delegate tasks to helpers,
     erate trivial invariants or invariant candidates which might                 and second, how to continue the verification process after
     turn out to be wrong.                                                        invariant generation. For the delegation, we let the master
We cannot expect existing verification tools which we wish to use                 verifier run until it requests support, which can be checked
as helpers to be able to work on CFAs, to understand the safety                   by inspecting the master’s flag requestsForHelp. The mas-
property or to produce witnesses. Hence, we foresee two further                   ter gets a configurable timelimit (called timerM) after which
sorts of components in our framework:                                             it is expected to send this request. By adding such an explicit
                                                                                  request for help, we allow the master to send a request for
   Mapper A mapper transforms the safety property specifica-                      other reasons (besides the timer) in the future. Then, after in-
     tion inside the program into the desired input format of the                 variant generation, the master can either be freshly restarted
     helper. A mapper basically conducts some simple syntac-                      or continued (option restartMaster).
     tic code replacements. For instance, for our running exam-                 Helper option When at least two helpers run in parallel, even-
     ple some helpers might instead require the safety property                   tually one of them first computes a witness. We can then
     to be written as if(!(n==y)){verifier_error();} or                           either (1) directly stop the other helpers, or (2) wait for all
     assert(n==y);                                                                to complete before injecting witnesses into the master. This
   Adapter An adapter generates a correctness witness out of                      option is called termAfterFirstInv.
     the computed loop invariants of a helper. Furthermore, some                Timeouts Finally, similar to the master, we can set a specific
     helper invariant generators work on intermediate represen-                   timeout for the helpers which fixes how long they are al-
     tations (IR) of the C-language (e.g. LLVM) or intermediate                   lowed to try to generate invariants. The timeout option is
     verification languages (e.g. Boogie). In this case, the com-                 called timeoutH.
     puted invariants (formulated in terms of IR-variables) first
                                                                          Next, we explain the CoVerCIG algorithm shown in Algorithm 1 in
     of all need to be translated back to the namespace of the
                                                                          detail. We assume that master and helpers run as threads and can
     C-program.
                                                                          be started and stopped. We furthermore employ methods wait for
The latter transformations happening inside an adapter are shown          waiting until some condition is achieved and join for waiting for
in Figure 4. Initially, the IR-language variables present in the in-      a specific thread to complete.
variants are translated to variables present in the C-program. After         Initially, the master verifier is started without any helper invari-
that, we transform their IR-code locations back to C-code locations.      ant generators running in parallel (line 1), providing the oppor-
For this, many compilers offer debug flags, adding this informa-          tunity to verify programs on its own. It runs standalone until it
tion to the IR. Otherwise, building and matching the CFAs of the          requests for help (either due to not being able to solve the problem
C-program and the IR-program is required. Finally, the pairs of           alone or due to hitting its timer) or it computes a result which is
mapped location and invariant are stored in the form of a witness,        subsequently returned (line 3). Afterwards all helpers are started in
constructable from the CFA.                                               parallel (lines 5 and 6). They also run until they reach their timeout,
Cooperative Verification via Collective Invariant Generation


Algorithm 1 CoVerCIG-algorithm                                                     program traces safe. The master verifier would then run in parallel
Input: C                                                         ▷ CFA             with the four helper invariant generators being called. Let us assume
         P                                           ▷ safety property             that the first helper returns only trivial invariants (after 10s), the
         M                                                     ▷ master            second one an invariant n ≥ y (after 50s), the third one the invariant
         Helpers                                       ▷ set of helpers            n = x +y (after 100s) and the fourth the invariant n −x −y = 0 (after
         conf                                          ▷ configuration             500s). The trivial invariant is ignored (see check in line 8) and when
Output: ω                                                     ▷ witness            the second helper returns a solution, the third and fourth helper are
           b                                                    ▷ result           still not stopped, due to the chosen configuration. The algorithm
  1: M.start(C, P, conf.timerM);                                                   waits until the third helper computes the invariant and the fourth
  2: wait until (M.requestsForHelp ∨ M.hasSolution());                             (only being able to compute an invariant after 500s) hits the timeout.
  3: if (M.hasSolution()) then                                                     Then the master is stopped, the invariants n ≥ y and n = x + y are
  4:     return M.getSolution();                                                   injected and the master is restarted. The master verifier can use
                                                                                   both invariants and might now compute the correct result.
  5: for each H ∈ Helpers do parallel        ▷ run helpers in parallel
  6:     H.start(C, P, conf.timeoutH);
  7:     wait until (H.timedout() ∨ H.hasSolution() ∨ H.stopped());
                                                                                   4     IMPLEMENTATION
  8:     if (H.hasSolution() ∧ nonTrivial(H.getSolution())) then                   To be able to evaluate the performance of our framework CoVer-
  9:         witnesses := witnesses ∪ H.getSolution();                             CIG, we instantiated it with two different master verifiers and three
 10:         if (conf.termAfterFirstInv) then                                      helpers, using existing off-the-shelf invariant generation tools. As
 11:             for each H’ ∈ helpers \{ H } do parallel                          verifiers need to be extended with witness injection for being able
 12:                 H’.stop();                   ▷ stop other helpers             to act as a master, we used the open-source configurable program
 13: if (M.hasSolution()) then
                                                                                   analysis framework CPAchecker [10] for this purpose and em-
 14:     return M.getSolution();                                                   ployed two of its standard instantiations (predicate abstraction and
                                                                                   k-induction). We also decided to implement Algorithm 1 within
 15: if (witnesses , ∅) then                       ▷ invariants found              CPAchecker. For the helper invariant generators – which can be
 16:     if (conf.restartMaster) then                                              used off-the-shelf – we looked at current and past participants of
 17:         M.stop();                                                             the annual competition of software verification SV-COMP [2]. Our
 18:     M.inject(witnesses);          ▷ inject witnesses into master              intention was to find tools which provide complementary tech-
 19:     if (conf.restartMaster) then                                              niques for invariant generation. To this end, we chose the tools
 20:         M.start(C,P, ∞);                                                      SeaHorn [28], UltimateAutomizer [29] and VeriAbs [1]. All
 21: join(M);                                   ▷ wait for M to finish             helper invariant generators are used as black-boxes. An overview
 22: return M.getSolution();                                                       of the techniques employed in these tools is given in Table 2. The
                                                                                   table also states whether the helpers require mappers and adapters.
                                                                                   A more detailed explanation is given next.
a solution is found or they are stopped. Their solutions (invari-
ants) are inserted into the witness set (line 9). Depending on op-                 4.1     Master Verifiers
tion termAfterFirstInv, either all but the first finished helper are               Predicate Abstraction. The first analysis used as master is a pred-
stopped or it is waited until all helpers either computed a solution or            icate abstraction technique [11], conducting predicate refinement
ran into their timeout. If invariants (witnesses) have been computed,              using a CEGAR (counter example guided abstraction refinement)
these are injected into the master (line 18). If the restartMaster                 scheme [20] with lazy-abstraction [33] and Craig interpolation [32].
option is set, the master needs to be stopped before injection and                 Loop heads and error locations are used as locations where abstrac-
restarted afterwards. Then the master continues and completes its                  tions are computed; the computation of the abstraction itself is
verification (without any further request for help) and the result is              done using an SMT solver.
finally returned.                                                                  Witness Injection: For using this technique as master, we extended
   Example 3.1. To explain the framework’s functionality, we de-                   it with witness injection. The purpose of witness injection is the
monstrate the CoVerCIG algorithm on the example presented in                       use of the invariants as given in the witnesses in the running anal-
Figure 2(a). Assume that we instantiate the framework with a mas-                  ysis of the master. It is realized by extracting predicates from the
ter verifier and four helper invariant generators4 . Moreover, we                  invariants and inserting them into the set of available predicates as
configure the framework as follows:                                                maintained by the analysis. If these predicates contain conjunctions
                                                                                   of clauses, these are furthermore split up and inserted individually.
     • restartMaster = true,                                                       Splitting predicates increases the performance due to the fact that
     • terminateAfterFirstInv = false,                                             SMT solvers perform better on many small predicates than on few
     • timerM = 50s, timeoutH = 300s.                                              larger ones5 .
Initially, the master verifier runs standalone and after 50 seconds                   k-Induction. The basic idea of k-induction [25] is to generalize
runtime it requests help. This means that it cannot generate the                   bounded model checking (BMC) [14] via induction. After proving
invariant n = x + y, for example because it rather proves single                   k-bounded program executions safe using BMC, a generalization
4 Later, we will see that more than two helpers does not practically make sense.   5 This has been reported by tool developers and has also shown in our experiments.
                                                                                                                                    Haltermann and Wehrheim


                                                 Table 2: Summary of tools used as helpers

                            Tool                                  Techniques                                Mapper        Adapter
                         SeaHorn             generation and solving of constrained horn clauses                 ✘              ✔
                    UltimateAutomizer      predicate abstraction, automata, path-based refinement               ✘             (✔)
                         VeriAbs               portfolio of 4 different sequential compositions                 ✘              ✘


is aimed for. The applied technique therefore generates auxiliary            Example 4.1. SeaHorn associates invariants to LLVM basic blocks.
invariants that are continuously refined using a CEGAR based              A basic block6 is a code fragment having a single entry location
analysis [5]. These invariants are combined with the information          (the first) and a single exit location (in general the last location
generated by BMC and generalized to a safety proof by successfully        of the block). We obtain the computed invariants in LLVM and
conducting an induction step.                                             the corresponding basic blocks by using the launch parameter
Witness Injection: We also implemented a method for witness injec-        −−show-invars. To construct a witness containing them, we need
tion for k-induction. Witness injection before restarting the analysis    to translate the invariants and find the matching C-code location for
is conducted by proving correctness of witnesses and afterwards           the basic block. For both, we use the LLVM-IR equipped with debug
adding them to the set of invariants maintained by the analysis. For      information, using SeaHornwith launch parameter -g . Thereby,
injecting witness into a running analysis, we periodically check          we obtain the IR-code fragment of the program in Figure 2(a), shown
whether new witnesses are available before each induction step. If        in simplified form and containing the most important debug in-
so, we also check their validity and add them to the set of invariants.   formation as comments. The example contains two Basic Blocks,
                                                                          entry and _bb.

4.2    Helper Invariant Generators                                          1    entry:
We have chosen the existing verification tools SeaHorn, Ulti-               2    v1 = bitcast i32 (...)* @nondet to i32 ()*                            ▷n
mateAutomizer and VeriAbs as helper invariant generators. For               3    v2 = icmp eq i32 v1, 0
this choice, we have inspected the tools participating in the annual        4    br i1 v2, label %error, label %_bb
competition on software verification. UltimateAutomizer has                 5
achieved excellent results in this year’s SV-COMP by taking the sec-        6    _bb:
ond place in the category ”Overall”. Since we already use two main
                                                                            7    v3 = phi i32 [0, %entry], [v6, %_bb]                                  ▷y
components of CPAchecker, the winner in the category ”Overall”
                                                                            8    v4 = phi i32 [v1, %entry], [v5, %_bb]                                 ▷x
this year, inside the masters, we did not also take instantiations of
CPAchecker as helpers into account. Moreover, we have chosen                9    v5 = add i32 v4, -1
VeriAbs, the winning tool in SV-COMP 2020 on ”ReachSafety”,                10    v6 = add i32 v3, 1
the category dealing with safety properties. As third tool we use          11    v7 = icmp eq i32 v5, 0
SeaHorn, a verification tool based on constrained Horn Clauses,            12    br i1 v7, label %error, label %_bb                               ▷line 4
neither currently participating in the SV-COMP nor producing wit-          13    ···
nesses. The three helper invariant generators employ verification
techniques complementary to those of both the other helpers and           SeaHorn computes the invariant v1 − v4 − v3 = 0 for the exam-
the two masters.                                                          ple and associates it with the basic block _bb. At first, we need
   SeaHorn. SeaHorn [28] is a verification tool using Constrained         to transform the variables from the IR to C-variables occurring in
Horn Clauses (CHCs) to solve the verification tasks. SeaHorn con-         the program. In this example we can use the debug information,
structs CHCs for each statement, encoding both data and control           as shown in comments in the code. In general, a more sophisti-
dependencies as well as the safety property. The (recursive) system       cated procedure is needed since LLVM-IR uses a three address code.
of CHC is solved using the solver Spacer [36]. Spacer tries to prove      Therein, complex expressions are split into several statements using
the unsatisfiability of the CHCs, being equivalent to proving the         intermediate variables which are resolved to C-expressions.
program safe, by searching for interpretations of the predicates             Afterwards, the transformed invariant needs to be associated
present in the CHCs. SeaHorn operates on the LLVM intermediate            with the correct location in the C-code. We analyze the LLVM IR
representation. We choose SeaHorn to extend the stack of helpers          program structure to map the basic blocks back to C-locations. In
by a tool being conceptually complementary to the others.                 the example, the block _bb is identified as being the loop of the
   Adapter for SeaHorn. SeaHorn participated in the SV-COMP               program, thus the invariant is mapped to the loop head. For this,
2015, thus it can process the encoding of safety properties used in       we employed some basic functions provided by PHASAR [42] in
our evaluation. Unfortunately, it only returns a boolean answer and       our adapter. Finally, we construct the CFA of the C-program, store
no verification witnesses, hence we had to implement an adapter           the invariants at the nodes and convert the equipped CFA to a
for it. Our adapter follows the general construction explained in         verification witness.
Figure 4 and we exemplify its translation in Example 4.1.
                                                                          6 https://releases.llvm.org/5.0.0/docs/LangRef.html#functions
Cooperative Verification via Collective Invariant Generation


   UltimateAutomizer. UltimateAutomizer’s verification tech-              5.2      Experimental Setup
nique is based on predicate abstraction and on automata construc-         Tools. We based the implemented of our CoVerCIG algorithm on
tions [29–31]. The program is represented as finite automaton and         the CPAchecker7 1.9.1 (8646a85) using MathSat58 as solver within
error labels are final states. UltimateAutomizer then aims at prov-       CPAchecker. For the helper VeriAbs and UltimateAutomizer
ing emptiness of the accepted language of the automaton which is          we used the versions as used in the SV-COMP 20209 . Due to the fact
equivalent to proving safety of the program. Although UltimateAu-         that there is no precompiled binary of SeaHorn, we employ the
tomizer produces verification witnesses, we added an adapter for          docker container of the latest version10 . All three helper invariant
the witnesses due to currently existing technical incompatibilities.      generators are used in their default configuration.
   VeriAbs. VeriAbs is using a portfolio of four different verifi-           During evaluation, we used the following default configurations
cation techniques, each containing several sequentially composed          for our framework: We set termAfterFirstInv and restartMaster
components [1]. The selection of strategies (techniques) from the         to true, setting the timerM to 50s and the timeoutH to 300s. The mas-
portfolio is performed by analyzing the loop structure and intervals      ter and helper used in a specific configuration as well as changes
for variables used in the loop. Depending on the analysis result, one     made to the default configurations are denoted as follows: The
of the following four techniques is applied: (1) random fuzz testing,     configuration kInd-ua-va-100-wait-200 denotes a configuration
(2) techniques to abstract arrays and apply BMC afterwards, (3)           using k-induction as master and the helpers UltimateAutomizer
explicit state model checking followed by standalone invariant gen-       and VeriAbs. The timerM is set to 100s, termAfterFirstInv to
eration techniques or (4) a fixed sequence of different verification      false and timeoutH to 200s. In general, we will use the abbrevia-
approaches.                                                               tions SH for SeaHorn, UA for UltimateAutomizer and VA for
                                                                          VeriAbs.
                                                                             Verification Tasks. The verification tasks used are taken from
5     EVALUATION                                                          the set of SV-COMP 2020 benchmarks11 . As we are interested in
In the following, we evaluate different instantiations of CoVerCIG.       finding suitable loop invariants, we selected all tasks from the
We focus on both effectiveness and efficiency, generally aiming at        category ReachSafety-Loops. To obtain a more broad distribution of
checking whether the use of CoVerCIG can increase the number of           tasks, we randomly selected 55 additional tasks from the categories
correctly solved verification tasks within the same resource limits.      ProductLines, Recursive, Sequentialized, ECA, Floats and Heap,
                                                                          yielding in total 342 tasks.
                                                                             Computing Resources. We conducted the evaluation on three
5.1      Research Questions                                               virtual machines, each having an Intel Xeon E5-2695 v4 CPU with
                                                                          eight cores and a frequency of 2.10 GHz and 16GB memory, running
We start with the feasibility of the approach in general.
                                                                          an Ubuntu 18.04 LTS with Linux Kernel 4.15. We run our experi-
   Feasibility hypothesis: A framework for collective invariant
                                                                          ments using the same setting as in the SV-COMP, giving each task 15
generation can be constructed using existing tools by building
                                                                          minutes of CPU-time on 8 cores and 15GB or memory. We employed
adapters when needed. Evaluation plan: We construct instances
                                                                          Benchexec thereby guaranteeing the resource-limitations [12]. All
of the framework, using instances of predicate abstraction and k-
                                                                          experimental data are available12 .
induction as master verifier and using three off-the-shelf helper
invariant generator. As a result, we obtain 14 different combinations.
   Besides feasibility, we were interested in the following four re-
                                                                          5.3      Experimental Results
search questions.                                                         Feasibility hypothesis. We implemented the CoVerCIG-frame-
                                                                          work as proof-of-concept in the CPAchecker-framework. For this,
                                                                          we had to extend the existing implementations of k-induction and
      RQ1. Can collective invariant generation increase the effective-
                                                                          predicate abstraction with witness injection. For the helper in-
        ness of the master verifier? Evaluation plan: We let the frame-
                                                                          variant generators we did not change a single line of code, only
        work run with a single invariant generator and compare the
                                                                          adding adapters for SeaHorn and UltimateAutomizer. Integrat-
        results to a run where the master verifier runs standalone.
                                                                          ing helpers like VeriAbs, not requiring an adapter or a mapper,
      RQ2. Does cooperation impact the overall efficiency of the
                                                                          can be done within a few lines of code. Although the implementa-
        verification? Evaluation plan: We compare the run time of
                                                                          tion is a proof-of-concept, this shows that the presented framework
        CoVerCIG with one helper against the two master verifiers
                                                                          works in practice and is applicable to all kinds of off-the-shelf helper
        running standalone.
                                                                          invariant generators, those producing verification witnesses and
      RQ3. What is an appropriate time for the master to run before
                                                                          those generating invariants in IR.
        requesting for help? Evaluation plan: We run CoVerCIG in
                                                                             RQ1 (Effectiveness). To evaluate whether a master verifier
        combination with one helper, evaluating the effectiveness of
                                                                          benefits from the support of a helper, we execute a combination
        requesting for help after 50, 100 and 200 seconds.
                                                                          of a master and a helper in the default configuration and compare
      RQ4. Does it pay off to run two invariant generators in par-
        allel? Evaluation plan: We let the framework run with two         7 https://github.com/sosy-lab/cpachecker
                                                                          8 https://mathsat.fbk.eu/
        invariant generators and compare the results to a run, where
                                                                          9 https://gitlab.com/sosy-lab/sv-comp/archives-2020/tree/master/2020
        only a single invariant generator is used. Moreover, we com-      10 suggested by the developers; used docker seahorn/seahorn-llvm5 (4c01c1d)
        pare the two configurations for termAfterFirstInv and             11 https://github.com/sosy-lab/sv-benchmarks/releases/tag/svcomp20

        evaluate timeouts for helpers using 100s and 200s.                12 https://covercig.github.io/
                                                                                                                                           Haltermann and Wehrheim


                1,000                                                                        1,000
                                  kInd                                                                       pred
                               kInd-SH-50                                                                 pred-SH-50
 CPU time (s)




                                                                              CPU time (s)
                               kInd-UA-50                                                                 pred-UA-50
                               kInd-VA-50                                                                 pred-VA-50


                 100                                                                          100

                  50                                                                           50
                    90     100            120            140            160                      90           100            110           120          130
                                      n-th fastest correct result                                                     n-th fastest correct result
                         (a) CoVerCIG using k-induction as master                                (b) CoVerCIG using predicate abstraction as master

                                 Figure 5: Quantile plots for CoVerCIG using both masters and different single helpers.

Table 3: Comparison of the two master verifiers running                                   RQ2 (Efficiency). Next, we evaluate the efficiency of CoVerCIG,
standalone and using a single helper.                                                  analyzing the CPU-time spend solving the verification tasks. As
                                                                                       CoVerCIG eventually shares the CPU time between master and
                   Tool-                 correct             additional                helpers, we expect that more time is needed to compute a correct
                Combination       overall true false        true false                 result after the helper is started.
                                                                                          Figure 5 shows two quantile plots of the verification runs, the left
                 k-induction        146      102     44       -     -
                                                                                       with k-induction and the right with predicate abstraction as master.
                 kInd-SH-50         148      104     44      +3     0
                                                                                       A datapoint (x, y) in the plot means that the verifier computes the
                 kInd-UA-50         158      114     44      +13    0
                                                                                       x-fastest correct results (for a task) in at maximal y seconds. As
                 kInd-VA-50         163      119     44      +19    0
                                                                                       CoVerCIG instances behave like masters standalone in the first 50
                 pred abstr.        116      78      38       -     -                  seconds, we only show results not solved within these 50 seconds.
                 pred-SH-50         122      84      38      +6     0                  We see that for tasks requiring a low amount of time, all instances
                 pred-UA-50         132      94      38      +16    0                  (including the master alone) require a similar amount of CPU time.
                 pred-VA-50         125      87      38      +9     0                  For tasks requiring more time, CoVerCIG is actually often faster,
                                                                                       the extreme being predicate abstraction as master which alone is
                                                                                       unable to solve more difficult tasks in the given time.
                                                                                          We exemplarily also compared the CPU time of k-induction
it to the master running standalone. Here, we are interested in                        standalone with CoVerCIG using VeriAbs as helper per task. It
the number of correct verification results, i.e., the verifier correctly               turns out that sharing does only slightly impact the runtime, as
reporting the safety property to be fulfilled (result true) or not                     shown in Figure 6. The scatter plot compares the CPU time of
(result false). Running standalone, k-induction can correctly solve                    k-induction standalone as master and k-induction supported by
146 of the verification tasks, predicate abstraction 116.                              VeriAbs, in case both tools solved the task correctly. A datapoint
    Table 3 gives the results of this experiment. In the table we see                  (x, y) means that k-induction standalone takes x seconds to solve
the overall number of correct results, the number of correct true                      the task and in combination with VeriAbs y seconds. The red
and correct false results plus the the number of tasks additionally                    dashed box contains all tasks solved within 50 seconds, where both
solved when using a helper. Through the cooperative invariant gen-                     tools behave equally, since the master does not request for help
eration, the performance of both masters is increased. As expected,                    in these cases. We see some tasks for which helping increased the
this applies to verification tasks with fulfilled safety property only,                runtime, but also some for which it decreased it. In most of the
i.e., the invariant generators can help in proving a property to                       cases, the CPU time used by CoVerCIG is not significantly higher.
hold, but cannot help in refuting properties (as they correctly do                        Finally, we compare the average CPU time needed to correctly
not generate invariants in these cases). Besides the additionally                      solve a task. Table 4 shows the average time needed for all tasks
solved tasks, there is also one (for SH and UA) and two (for VA)                       and – in brackets – for the correctly solved tasks only. We observe
tasks, respectively, which cannot be correctly solved anymore. In                      that the runtime increases when only looking at correctly solved
these cases, the master alone consumes nearly all of the CPU time                      tasks (in particular for VeriAbs), however, when considering all
available, hence sharing resources in cooperation with the helpers                     tasks the CPU time is even decreased. The latter effect is due to the
results in a timeout.                                                                  number of timeouts of the master decreasing when cooperating
                                                                                       with helpers. Concluding, we can make the following observation.
     On our data set, the total number of correctly solved tasks
     increases using CoVerCIG by 12% for k-induction and 14% for
     predicate abstraction used as master.                                              13 Due to possible imprecisely measured CPU time of Benchexec, we computed an
                                                                                        upper bound on the runtime.
Cooperative Verification via Collective Invariant Generation


                                          1,000                                                                kInd-SH                      kInd-VA   pred-SH                     pred-VA
      CoVerCIG with kInd-VeriAbs-50 (s)



                                                                                                                         0      1      15                       0      1      3

                                                                                                                                0                                      0
                                                                                                                          2         3                            5         5
                                           100
                                                                                                                                8                                      6

                                                                                                                             kInd-UA                                pred-UA

                                                                                                                   (a) For k-induction                (b) For predicate abstraction
                                            10
                                                                                                              Figure 7: Tasks additionally solved using single helpers


                                                                                                            sends the request early. Asking later sometimes leads to a situation
                                             1
                                                  1                10             100               1,000   where the invariant is obtained too late to be helpful. Hence, we
                                                              k-induction standalone (s)                    employed 50 seconds in our default configuration which we used
                                                                                                            to evaluate RQ1 and RQ2.
Figure 6: Scatter plot comparing kInd and kInd-VeriAbs-50                                                    On our dataset, CoVerCIG performs best when requesting early
                                                                                                             for help, using 50 seconds for timerM.
Table 4: Total CPU time for all tasks and average CPU time
taken for a correct answer in brackets, both in seconds.                                                       RQ4 (Combination of helpers). In RQ4, we were interested
                                                                                                            in finding out (a) whether it is beneficial to run two invariant
                                                    Master                      Master                      generators in parallel, and (b) if yes, which pair is best for this.
                                                  standalone           +SH13    +UA             +VA            To this end, we first of all determined which helper is able to solve
                                                                                                            which of the additionally solved tasks. The result is shown in the
                                 kInd                 491 (50)     489 (63)    477 (68)       482 (107)     Venn diagrams of Figure 7. Surprisingly, SeaHorn – although em-
                                 Pred                 479 (30)     468 (39)    454 (51)        470 (49)     ploying a technique conceptually different to UltimateAutomizer
                                                                                                            and VeriAbs – is not able to solve a single task which not at least
Table 5: Number of correctly verified tasks for different pa-                                               one of the others can.
rameters of timerM                                                                                             Next, we thus studied the number of correctly solved tasks using
                                                                                                            the three possible pairs of helpers, running the two helpers in a pair
                                                                                                            in parallel. Table 6 in the first row shows the results. It in addition
                                          Value           k-induction           predicate abstr.
                                                                                                            also contains results evaluating two values (100 and 200 seconds)
                                          timerM        -SH -UA -VA            -SH -UA -VA
                                                                                                            for parameter timeoutH in a setting when the master waits for all
                                            50s         148      158     163   122      132      125        helpers to complete (not just the first one). A first observation is
                                           100s         148      157     161   122      132      125        that – except for the case of k-induction with UA-VA – the results
                                           200s         148      157     156   122      132      125        show no significant difference when using the default configuration
                                                                                                            or wait-100 or wait-200.
                                                                                                               For checking whether parallel execution of helpers is beneficial,
  On our dataset, collaborative invariant generation does not                                               these numbers need to be compared against those for a single
  negatively impact the effectiveness; in some cases we even see                                            helper as given in Table 3. We see that predicate abstraction benefits
  small improvements.                                                                                       from using two helpers, especially using UltimateAutomizer and
                                                                                                            VeriAbs. Using CoVerCIG with these tools perfectly combines their
   RQ3 (Time for the Master to request for help). To deter-                                                 strengths, thereby increasing the number of correctly solved tasks
mine a preferable time for the master to run alone, we evaluated                                            in total by 17%. In contrast, it turns out that for k-induction none
CoVerCIG using 50, 100 or 200 seconds for timerM. A summary of                                              of the combinations of two helpers outperforms CoVerCIG using
the results is given in Table 5, showing the number of correctly                                            VeriAbs only. For UltimateAutomizer and VeriAbs as helpers,
solved tasks for each instantiation. Both masters achieve their best                                        the total number does not change, only the set of solved tasks. For
result running alone for 50 seconds. For k-induction, a good choice                                         instance, nearly 50% of the additional tasks solved by kind-UA-VA
for timerM plays an important role for its performance. In contrast,                                        are not solved using kInd-UA and vice versa. This result is based
the results of predicate abstraction are not influenced by different                                        on the fact that they have to share the available CPU time in the
values for timerM at all, because predicate abstraction computes its                                        combination. Hence, tasks that are solved using one of them as
correctly given answers on average in 19 seconds after obtaining                                            helper alone could not be solved anymore in a combination because
the invariants by the helpers. When using k-induction, we observe                                           of timeouts. This phenomenon is even more an issue when running
cases where the correct solution is computed only if the master                                             all three helpers in parallel. The combination of all three helpers
                                                                                                                      Haltermann and Wehrheim


Table 6: Number of correctly solved tasks using different               In addition, using a black box integration with defined exchange
forms of cooperation with two helpers running in parallel.              formats allows us to easily exchange or integrate new approaches.
                                                                            There are also existing concepts for collaboration between differ-
    Config         k-induction               predicate abstr.           ent techniques in a black-box manner. Conditional model checking
                SH-    SH-     UA-         SH-     SH-      UA-         is a technique for sequentially composing different model checkers,
                UA     VA      VA          UA      VA      VA           sharing information between the tools in form of conditions [7].
                                                                        Beyer and Jakobs developed a concept for combining model check-
 default        153      156      163      130      130       136
                                                                        ing with testing [8]. Although both approaches enable cooperation,
 wait-100       156      155      161      132      131       136
                                                                        none combines a verification tool and tools for invariant generation.
 wait-200       155      156      155      132      129       135
                                                                            We next shortly discuss three approaches which are conceptually
                                                                        closer to our framework. Frama-C is a framework for code analysis,
                                                                        aiming for analyzing industrial size code [35]. The framework con-
solves only 154 tasks correctly for k-induction and 129 for predicate   tains different plugins, each implementing a verification or testing
abstraction.                                                            technique. The plugins can exchange information in form of ASCL
    On our dataset, CoVerCIG can increase the total number of           source code annotations. Within Frama-C, the analyzers can col-
    correctly solved tasks using UA and VA in parallel; in general      laborate by being either sequentially or parallelly composed. For
    waiting for the other tool to also finish its computation does      this, partial results produced by an analysis can be completed by a
    not pay off.                                                        second one or several partial results computed in parallel are com-
                                                                        posed to a complete result. Frama-C offers the general possibility
                                                                        to define cooperation between existing plugins. To the best of our
                                                                        knowledge, Frama-C does however not provide a conceptual collab-
5.4      Threads to Validity
                                                                        oration of a verification approach and tools for invariant generation
We have conducted our evaluation using a random sample of tasks         driven by the verification approach’s demand for support.
as well as those in the category Loops. Although this guarantees            The approach of using continuously refined invariants for k-
some diversity in the chosen tasks, our findings may not completely     induction [5] uses a lightweight dataflow analysis which can be
carry over to arbitrary real-world programs.                            considered to be a helper for verification. Therein, the supporting
   The experiments are conducted using the reliable framework           invariant generator runs in parallel to the k-induction analysis.
Benchexec on identical machines with same resource limitations,         Compared to our framework, the main difference is the form of
guaranteeing comparable results. As SeaHorn is used within a            cooperation used. Beyer et al. use a white-box integration for the
docker-container, its CPU usage however cannot be measured              cooperation between k-induction and the invariant generator, build-
by Benchexec. We therefore measured its CPU usage externally,           ing hardly wired connections between both analyses and sharing
rounded it up and added it to the measured CPU time, obtaining a        the information inside the tool. Thus, integrating external tools is
lower bound for the correctly solved tasks. Thereby, all results stay   hard to achieve. Moreover, the approach is designed to work for
valid, especially of the best performing instantiations of CoVerCIG,    k-induction only. Note that an analogeous approach is proposed by
as they do not use SeaHorn.                                             Brain et al. [17].
   Our implementation of CoVerCIG relies on the correctness of the          Pauck and Wehrheim proposed CoDiDroid, a framework for
used master verifiers and helpers (which are given) as well as on       cooperative taint flow analysis for Android apps [39]. Within their
the adapters (which we build). An incorrectly translated invariant      framework, different analysis tools with specialized capabilities are
may however influence the performance only negatively.                  combined as black-boxes. CoDiDroid is however tailored to the
   Both master verifiers used as well as UltimateAutomizer and          needs of Android taint flow analysis, thus the exchanged informa-
VeriAbs are participating in the annual SV-COMP, hence they             tion differs. Thus CoDiDroid is not able to orchestrate or exchange
might be tuned to the tasks employed. This does however not             information on safety analysis with shared invariant generation.
influence the validity of the results since our interest is in the          To summarize, there are a lot of existing approaches for coopera-
additional number of tasks solved by cooperation, not the solved        tive verification, but most of them are white-box combinations, and
ones per se.                                                            the only existing black-box combinations are not general enough
                                                                        to allows for collective invariant generation.
6     RELATED WORK
In this paper, we presented a framework for cooperative verification
via collective invariant generation. The idea of collaboration for
verification by combining known techniques has been widely em-
ployed before. For instance, there are combinations of verification     7   CONCLUSION
with testing approaches [18, 19, 21, 22, 24, 26] and with approaches    In this paper, we have presented a novel form of black box cooper-
for invariant generation [15, 17, 27, 40, 41]. The latter combina-      ation for software verification via collective invariant generation.
tions are conducted in a white box manner using strong coupling         Within the configurable framework named CoVerCIG, the so called
between the components, making the addition of a new approach           master verifier steering the verification process is able to delegate
a challenging task. Our framework conceptually decouples the in-        the task of invariant generation to one or several helper invariant
variant generation from the verification, making it more flexible.      generators.
Cooperative Verification via Collective Invariant Generation


   We implemented CoVerCIG within the CPAchecker framework                                   [15] Bruno Blanchet, Patrick Cousot, Radhia Cousot, Jérôme Feret, Laurent
using k-induction and predicate abstraction as master analysis sup-                               Mauborgne, Antoine Miné, David Monniaux, and Xavier Rival. 2003. A static
                                                                                                  analyzer for large safety-critical software. In PLDI, Ron Cytron and Rajiv Gupta
ported by three existing helpers SeaHorn, UltimateAutomizer                                       (Eds.). ACM, 196–207. https://doi.org/10.1145/781131.781153
and VeriAbs. Our evaluation on a set of SV-COMP verification tasks                           [16] Aaron R. Bradley. 2011. SAT-Based Model Checking without Unrolling. In VMCAI
                                                                                                  (LNCS), Ranjit Jhala and David A. Schmidt (Eds.), Vol. 6538. Springer, 70–87.
shows that CoVerCIG increases the number of correctly solved tasks                                https://doi.org/10.1007/978-3-642-18275-4_7
without increasing the overall verification time. The best combi-                            [17] Martin Brain, Saurabh Joshi, Daniel Kroening, and Peter Schrammel. 2015. Safety
nation of helpers, UltimateAutomizer and VeriAbs in parallel,                                     Verification and Refutation by k-Invariants and k-Induction. In SAS (LNCS),
                                                                                                  Sandrine Blazy and Thomas P. Jensen (Eds.), Vol. 9291. Springer, 145–161. https:
yields an increase of 12% for k-induction and 17% for predicate                                   //doi.org/10.1007/978-3-662-48288-9_9
abstraction.                                                                                 [18] Maria Christakis, Peter Müller, and Valentin Wüstholz. 2012. Collaborative
   Next, we plan to enhance the cooperation by analyzing the be-                                  Verification and Testing with Explicit Assumptions. In FM (LNCS), Dimitra Gian-
                                                                                                  nakopoulou and Dominique Méry (Eds.), Vol. 7436. Springer, Berlin, Heidelberg,
havior of the master in order to identify an optimal point to request                             132–146. https://doi.org/10.1007/978-3-642-32759-9_13
for help. Moreover, extending CoVerCIG by additionally taking                                [19] Maria Christakis, Peter Müller, and Valentin Wüstholz. 2016. Guiding dynamic
                                                                                                  symbolic execution toward unverified program executions. In ICSE, Laura K.
error traces found by the helper into account is also scheduled. In                               Dillon, Willem Visser, and Laurie Williams (Eds.). ACM, New York, NY, USA,
addition, we intend to investigate whether a selection of helpers                                 144–155. https://doi.org/10.1145/2884781.2884843
on the basis of the given verification task is beneficial.                                   [20] Edmund M. Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith. 2003.
                                                                                                  Counterexample-guided abstraction refinement for symbolic model checking. J.
                                                                                                  ACM 50, 5 (2003), 752–794. https://doi.org/10.1145/876638.876643
                                                                                             [21] Christoph Csallner and Yannis Smaragdakis. 2005. Check ’n’ Crash: combining
                                                                                                  static checking and testing. In ICSE, Gruia-Catalin Roman, William G. Griswold,
REFERENCES                                                                                        and Bashar Nuseibeh (Eds.). ACM, New York, NY, USA, 422–431. https://doi.org/
 [1] Mohammad Afzal, A. Asia, Avriti Chauhan, Bharti Chimdyalwar, Priyanka Darke,                 10.1145/1062455.1062533
     Advaita Datar, Shrawan Kumar, and R. Venkatesh. 2019. VeriAbs : Verification            [22] Christoph Csallner, Yannis Smaragdakis, and Tao Xie. 2008. DSD-Crasher: A
     by Abstraction and Test Generation. In ASE. IEEE, 1138–1141. https://doi.org/10.             hybrid analysis tool for bug finding. TOSEM 17, 2 (April 2008), 1–37.
     1109/ASE.2019.00121                                                                     [23] Mike Czech, Marie-Christine Jakobs, and Heike Wehrheim. 2015. Just Test What
 [2] Dirk Beyer. 2017. Software Verification with Validation of Results - (Report on              You Cannot Verify!. In FASE (LNCS), Alexander Egyed and Ina Schaefer (Eds.),
     SV-COMP 2017). In TACAS (LNCS), Axel Legay and Tiziana Margaria (Eds.),                      Vol. 9033. Springer, Berlin, Heidelberg, 100–114. https://doi.org/10.1007/978-3-
     Vol. 10206. Springer, Berlin, Heidelberg, 331–349. https://doi.org/10.1007/978-3-            662-46675-9_7
     662-54580-5_20                                                                          [24] Przemyslaw Daca, Ashutosh Gupta, and Thomas A. Henzinger. 2016. Abstraction-
 [3] Dirk Beyer, Matthias Dangl, Daniel Dietsch, and Matthias Heizmann. 2016. Cor-                driven Concolic Testing. In VMCAI (LNCS), Barbara Jobstmann and K. Rustan M.
     rectness witnesses: exchanging verification results between verifiers. In FSE,               Leino (Eds.), Vol. 9583. Springer, Berlin, Heidelberg, 328–347. https://doi.org/10.
     Thomas Zimmermann, Jane Cleland-Huang, and Zhendong Su (Eds.). ACM, New                      1007/978-3-662-49122-5_16
     York, NY, USA, 326–337. https://doi.org/10.1145/2950290.2950351                         [25] Alastair F. Donaldson, Leopold Haller, Daniel Kroening, and Philipp Rümmer.
 [4] Dirk Beyer, Matthias Dangl, Daniel Dietsch, Matthias Heizmann, and Andreas                   2011. Software Verification Using k-Induction. In SAS (LNCS), Eran Yahav (Ed.),
     Stahlbauer. 2015. Witness validation and stepwise testification across software              Vol. 6887. Springer, 351–368. https://doi.org/10.1007/978-3-642-23702-7_26
     verifiers. In ESEC/FSE, Elisabetta Di Nitto, Mark Harman, and Patrick Heymans           [26] Xi Ge, Kunal Taneja, Tao Xie, and Nikolai Tillmann. 2011. DyTa: dynamic
     (Eds.). ACM, New York, NY, USA, 721–733. https://doi.org/10.1145/2786805.                    symbolic execution guided with static verification results. In ICSE, Richard N.
     2786867                                                                                      Taylor, Harald C. Gall, and Nenad Medvidovic (Eds.). ACM, New York, NY, USA,
 [5] Dirk Beyer, Matthias Dangl, and Philipp Wendler. 2015. Boosting k-Induction with             992–994. https://doi.org/10.1145/1985793.1985971
     Continuously-Refined Invariants. In CAV (LNCS), Daniel Kroening and Corina S.           [27] Ashutosh Gupta and Andrey Rybalchenko. 2009. InvGen: An Efficient Invariant
     Pasareanu (Eds.), Vol. 9206. Springer, Cham, 622–640. https://doi.org/10.1007/978-           Generator. In CAV (LNCS), Ahmed Bouajjani and Oded Maler (Eds.), Vol. 5643.
     3-319-21690-4_42                                                                             Springer, 634–640. https://doi.org/10.1007/978-3-642-02658-4_48
 [6] Dirk Beyer, Sumit Gulwani, and David A. Schmidt. 2018. Combining Model                  [28] Arie Gurfinkel, Temesghen Kahsai, Anvesh Komuravelli, and Jorge A. Navas.
     Checking and Data-Flow Analysis. In Handbook of Model Checking, Edmund M.                    2015. The SeaHorn Verification Framework. In CAV (LNCS), Daniel Kroening
     Clarke, Thomas A. Henzinger, Helmut Veith, and Roderick Bloem (Eds.). Springer,              and Corina S. Pasareanu (Eds.), Vol. 9206. Springer, 343–361. https://doi.org/10.
     493–540. https://doi.org/10.1007/978-3-319-10575-8_16                                        1007/978-3-319-21690-4_20
 [7] Dirk Beyer, Thomas A. Henzinger, M. Erkan Keremoglu, and Philipp Wendler.               [29] Matthias Heizmann, Yu-Fang Chen, Daniel Dietsch, Marius Greitschus, Jochen
     2012. Conditional model checking: a technique to pass information between                    Hoenicke, Yong Li, Alexander Nutz, Betim Musa, Christian Schilling, Tanja
     verifiers. In FSE, Will Tracz, Martin P. Robillard, and Tevfik Bultan (Eds.). ACM,           Schindler, and Andreas Podelski. 2018. Ultimate Automizer and the Search
     57. https://doi.org/10.1145/2393596.2393664                                                  for Perfect Interpolants - (Competition Contribution). In TACAS (LNCS), Dirk
 [8] Dirk Beyer and Marie-Christine Jakobs. 2019. CoVeriTest: Cooperative Verifier-               Beyer and Marieke Huisman (Eds.), Vol. 10806. Springer, 447–451. https:
     Based Testing. In FASE (LNCS), Reiner Hähnle and Wil M. P. van der Aalst (Eds.),             //doi.org/10.1007/978-3-319-89963-3_30
     Vol. 11424. Springer, 389–408. https://doi.org/10.1007/978-3-030-16722-6_23             [30] Matthias Heizmann, Yu-Wen Chen, Daniel Dietsch, Marius Greitschus, Alexander
 [9] Dirk Beyer, Marie-Christine Jakobs, Thomas Lemberger, and Heike Wehrheim.                    Nutz, Betim Musa, Claus Schätzle, Christian Schilling, Frank Schüssele, and
     2018. Reducer-based construction of conditional verifiers. In ICSE, Michel Chau-             Andreas Podelski. 2017. Ultimate Automizer with an On-Demand Construction
     dron, Ivica Crnkovic, Marsha Chechik, and Mark Harman (Eds.). ACM, 1182–1193.                of Floyd-Hoare Automata - (Competition Contribution). In TACAS (LNCS), Axel
     https://doi.org/10.1145/3180155.3180259                                                      Legay and Tiziana Margaria (Eds.), Vol. 10206. Springer, Berlin, Heidelberg, 394–
[10] Dirk Beyer and M. Erkan Keremoglu. 2011. CPAchecker: A Tool for Configurable                 398. https://doi.org/10.1007/978-3-662-54580-5_30
     Software Verification. In CAV (LNCS), Ganesh Gopalakrishnan and Shaz Qadeer             [31] Matthias Heizmann, Jochen Hoenicke, and Andreas Podelski. 2013. Software
     (Eds.), Vol. 6806. Springer, Berlin, Heidelberg, 184–190. https://doi.org/10.1007/           Model Checking for People Who Love Automata. In CAV (LNCS), Natasha Shary-
     978-3-642-22110-1_16                                                                         gina and Helmut Veith (Eds.), Vol. 8044. Springer, 36–52. https://doi.org/10.1007/
[11] Dirk Beyer, M. Erkan Keremoglu, and Philipp Wendler. 2010. Predicate abstrac-                978-3-642-39799-8_2
     tion with adjustable-block encoding. In FMCAD, Roderick Bloem and Natasha               [32] Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar, and Kenneth L. McMillan.
     Sharygina (Eds.). IEEE, Washington, DC, USA, 189–197. http://ieeexplore.ieee.                2004. Abstractions from proofs. In POPL, Neil D. Jones and Xavier Leroy (Eds.).
     org/document/5770949/                                                                        ACM, New York, NY, USA, 232–244. https://doi.org/10.1145/964001.964021
[12] Dirk Beyer, Stefan Löwe, and Philipp Wendler. 2019. Reliable benchmarking:              [33] Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar, and Grégoire Sutre. 2002.
     requirements and solutions. Int. J. Softw. Tools Technol. Transf. 21, 1 (2019), 1–29.        Lazy abstraction. In POPL, John Launchbury and John C. Mitchell (Eds.). ACM,
     https://doi.org/10.1007/s10009-017-0469-y                                                    New York, NY, USA, 58–70. https://doi.org/10.1145/503272.503279
[13] Dirk Beyer and Heike Wehrheim. 2019. Verification Artifacts in Cooperative              [34] Marie-Christine Jakobs and Heike Wehrheim. 2014. Certification for configurable
     Verification: Survey and Unifying Component Framework. CoRR abs/1905.08505                   program analysis. In SPIN (LNCS), Neha Rungta and Oksana Tkachuk (Eds.).
     (2019). arXiv:1905.08505 http://arxiv.org/abs/1905.08505                                     ACM, New York, NY, USA, 30–39. https://doi.org/10.1145/2632362.2632372
[14] Armin Biere, Alessandro Cimatti, Edmund M. Clarke, Ofer Strichman, and Yun-             [35] Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris
     shan Zhu. 2003. Bounded model checking. Advances in Computers 58 (2003),                     Yakobowski. 2015. Frama-C: A software analysis perspective. Formal Asp. Comput.
     117–148. https://doi.org/10.1016/S0065-2458(03)58003-2                                       27, 3 (2015), 573–609. https://doi.org/10.1007/s00165-014-0326-7
                                                                                                                                                Haltermann and Wehrheim


[36] Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. 2014. SMT-Based Model         [40] Williame Rocha, Herbert Rocha, Hussama Ismail, Lucas C. Cordeiro, and Bernd
     Checking for Recursive Programs. In CAV (LNCS), Armin Biere and Roderick                Fischer. 2017. DepthK: A k-Induction Verifier Based on Invariant Inference for
     Bloem (Eds.), Vol. 8559. Springer, 17–34. https://doi.org/10.1007/978-3-319-            C Programs - (Competition Contribution). In TACAS (LNCS), Axel Legay and
     08867-9_2                                                                               Tiziana Margaria (Eds.), Vol. 10206. 360–364. https://doi.org/10.1007/978-3-662-
[37] Kenneth L. McMillan. 2018. Interpolation and Model Checking. In Handbook of             54580-5_23
     Model Checking, Edmund M. Clarke, Thomas A. Henzinger, Helmut Veith, and           [41] Sriram Sankaranarayanan, Henny B. Sipma, and Zohar Manna. 2005. Scalable
     Roderick Bloem (Eds.). Springer, 421–446. https://doi.org/10.1007/978-3-319-            Analysis of Linear Systems Using Mathematical Programming. In VMCAI (LNCS),
     10575-8_14                                                                              Radhia Cousot (Ed.), Vol. 3385. Springer, 25–41. https://doi.org/10.1007/978-3-
[38] George C. Necula. 1997. Proof-Carrying Code. In POPL, Peter Lee, Fritz Henglein,        540-30579-8_2
     and Neil D. Jones (Eds.). ACM Press, New York, NY, USA, 106–119. https:            [42] Philipp Dominik Schubert, Ben Hermann, and Eric Bodden. 2019. PhASAR:
     //doi.org/10.1145/263699.263712                                                         An Inter-procedural Static Analysis Framework for C/C++. In TACAS (LNCS),
[39] Felix Pauck and Heike Wehrheim. 2019. Together strong: cooperative Android              Tomás Vojnar and Lijun Zhang (Eds.), Vol. 11428. Springer, 393–410. https:
     app analysis. In ASE, Marlon Dumas, Dietmar Pfahl, Sven Apel, and Alessandra            //doi.org/10.1007/978-3-030-17465-1_22
     Russo (Eds.). ACM, 374–384. https://doi.org/10.1145/3338906.3338915
