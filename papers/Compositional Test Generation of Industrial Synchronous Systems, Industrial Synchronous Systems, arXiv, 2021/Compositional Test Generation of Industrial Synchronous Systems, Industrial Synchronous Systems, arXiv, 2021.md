                                                     Compositional Test Generation of
                                                      Industrial Synchronous Systems

                                               Daisuke Ishii1 , Takashi Tomita1 , Kenji Onishi2 , and Toshiaki Aoki1
                                                       1
                                                          Japan Advanced Institute of Science and Technology
                                                              {dsksh,tomita,toshiaki}@jaist.ac.jp
                                                        2
arXiv:2112.05411v1 [cs.SE] 10 Dec 2021




                                                          Gaio Technology Co., LTD. onishi.k@gaio.co.jp


                                               Abstract. Synchronous systems provide a basic model of embedded sys-
                                               tems and industrial systems are modeled as Simulink diagrams and/or
                                               Lustre programs. Although the test generation problem is critical in the
                                               development of safe systems, it often fails because of the spatial and
                                               temporal complexity of the system descriptions. This paper presents
                                               a compositional test generation method to address the complexity is-
                                               sue. We regard a test case as a counterexample in safety verification,
                                               and represent a test generation process as a deductive proof tree built
                                               with dedicated inference rules; we conduct both spatial- and temporal-
                                               compositional reasoning along with a modular system structure. A proof
                                               tree is generated using our semi-automated scheme involving manual ef-
                                               fort on contract generation and automatic processes for counterexample
                                               search with SMT solvers. As case studies, the proposed method is applied
                                               to four industrial examples involving such features as enabled/triggered
                                               subsystems, multiple execution rates, filter components, and nested coun-
                                               ters. In the experiments, we successfully generated test cases for target
                                               systems that were difficult to deal with using the existing tools.


                                         1   Introduction
                                         Many industrial products containing embedded computers, as exemplified typi-
                                         cally by automobiles, are developed using a model-based approach. Synchronous
                                         systems are useful in the co-modeling of such embedded systems [2]. In indus-
                                         trial sites, dedicated modeling tools such as MATLAB/Simulink and SCADE
                                         are used to achieve rapid prototyping of the products. Because the products are
                                         to be deployed in a safety-critical environment, assuring their quality is manda-
                                         tory, as standards such as ISO 26262 demand. A state-of-the-art solution to this
                                         is coverage testing, which ensures that a product is exercised exhaustively to
                                         satisfy a criterion consisting of objective properties in a system description. In
                                         the modeling phase, developers invest effort in building a test suite that ful-
                                         fills coverage criteria, e.g. MC/DC, with tool support. For example, Simulink is
                                         equipped with the Simulink Design Verifier (SLDV) toolbox for this purpose.
                                              Automated test-suite generation scales up to a certain complexity and prod-
                                         uct size; however, we are aware of cases in which the testing phase becomes stuck
                                         as a result of uncovered objectives. Test generation tends to fail because of sys-
                                         tem descriptions unsupported by the tools and the computational complexity of
searching for a test case. As for generic software, there have been a number of test
generation methods proposed for synchronous systems. For instance, it has been
reported that an incomplete approach, e.g. a random search or a Monte-Carlo
method, increases the coverage rate [22, 20, 17, 21, 18, 23]. However, in our exper-
iments with industrial products, there still remain some objectives not achieved
through using the available tools.
    Industrial synchronous systems involve both spatial and temporal complexity
and any methods/tools may suffer from it. Spatial complexity is primarily intro-
duced by a composition of multiple atomic nodes, which might be connected
circularly. Temporal complexity is introduced in a system by nodes involving
long counters and nodes that behave with different clocks. Complexity is in-
creased further by additional features such as composition of filter nodes and
combinational nodes and equipment of an activation port to nodes.
    While there might always be a complex system that is difficult to analyze with
existing methods, we take a compositional approach using a divide-and-conquer
process on the spatial and temporal composition of a target. Using a tool such
as Kind2 [8], which supports compositional description and model checking, can
be expected to be effective. The objective of this research is to leverage this idea
in a semi-automated method and to apply it to several industrial systems. The
contributions of this paper are as follows:


 – A compositional test generation method based on static analysis with SMT
   solvers. We first formalize the problem in terms of safety verification, con-
   structing a counterexample compositionally. After describing the link be-
   tween Simulink diagrams, Lustre programs, and a classical assume-guarantee
   (AG) rule by Alur and Henzinger [3], we propose inference rules for spatial
   and temporal composition. To reduce the complexity and to facilitate our
   compositional reasoning, we express test cases and interface contracts be-
   tween modules with templates of input/output streams. Finally, we propose
   a set of manual and automated methods to identify test cases and contracts.
 – Case studies on compositional test generation of industrial examples. First,
   we present two example Simulink models developed in an industrial site and
   extract their essential parts in two other simpler examples. We then report
   how the proposed method is applied to test generation of the examples. Last,
   we report the experimental results including comparisons with the results of
   two existing tools.

    The remainder of the paper is organized as follows. Sect. 2 reviews related
work. Sect. 3 introduces basic definitions that formalize synchronous systems,
a motivating example, and two languages (modeling tools), Simulink and Lus-
tre. Sect. 4 formalizes the test generation problem and provides templates for
streams. Sect. 5 presents our method for compositional test generation. In Sect. 6,
we describe the four examples and the test generation process. Sect. 7 reports
the experimental results.
2     Related Work
Proprietary tools such as SLDV 3 and Reactis 4 are often used in the testing
phase of industrial synchronous systems. Although these produce test cases for
achieving a high coverage rate for many systems, there are those whose descrip-
tions are not supported and those for which test generation takes a long time.
The examples in this paper include such cases.
    Various test generation methods for synchronous systems have been pro-
posed, including symbolic execution with random search [22, 20, 17, 21], Monte-
Carlo numerical simulation [23], meta-heuristic search [18], model-based test-
ing [10], and mutation testing [25, 11]. Each of these analyzes the target in its
entirety as a monolithic system and can encounter excessive amount of computa-
tion when a system becomes large and test cases become rare. Testing methods
have been proposed in other domains that combine compositional analysis and
random search [14, 13, 19]. We expect that such methods will be studied in the
future for synchronous systems.
    Compositional modeling and verification of synchronous systems have been
studied for decades [15, 3, 12]. This work aims to apply their results to industrial
case studies, primarily by using the AG rule in [3] for circular compositions.
Henzinger and others have also considered composition and abstraction on the
temporal direction [3, 16]. We propose a different rule for temporal composi-
tion. More recently, compositional model checking for Lustre programs has been
implemented in the tools, Kind2 [8, 9] and Zustre,5 which make use of state-
of-the-art SMT solvers. The AG reasoning by Kind2 addresses only the spatial
direction of modules with a restricted form of composition. This paper pro-
poses a more generic spatial-temporal composition method using the rule in [3]
and other rules. Some algorithms for compositional analysis on circular modules
(which are not synchronous systems) have been proposed [1, 19]. Automation for
synchronous systems is a future work.


3     Synchronous Systems
In this work, we consider synchronous systems taken from industry. We describe
a basic model in Sect. 3.1, two dedicated languages, Simulink and Lustre, in
Sect. 3.2, some extensions for industrial use in Sect. 3.3, and the complexity of
industrial systems in Sect. 3.4.

3.1   Basic Synchronous Model
We use typed variables to describe synchronous systems. Types include bool,
int and real, referring to {true, false}, Z and R, respectively. We also consider
typed expressions constructed with typed variables.
3
  https://www.mathworks.com/products/simulink-design-verifier.html.
4
  https://www.reactive-systems.com/.
5
  https://github.com/coco-team/zustre.
    As a basic model of discrete, reactive and synchronous computation, we con-
sider a set of compositional nodes represented as Mealy machines [15, 3, 2].
Definition 1. A node of name n is a tuple Nn = (In , On , Sn , Init n , React n )
where each of In , On and Sn is a set of input/output/state variables (In ∩ On ∩
Sn = ∅), Init n is an initial condition description, and React n is a reaction
description. We denote the domains of In , On and Sn by D(In ), D(On ) and
D(Sn ), respectively. Init n is interpreted as a subset of D(Sn ). We have a reaction
in D(Sn )×D(In )×D(On )×D(Sn ) by an interpretation of React n ; and an execution
of a node (of length k) is formalized as a stream i.e. a sequence of reactions
                       i0 /o0    i1 /o1             ik−1 /ok−1
                  s−1 −−−→ s0 −−−→ s1 · · · sk−2 −−−−−−−→ sk−1 ,
where s ∈ D(Sn ), i ∈ D(In ) and o ∈ D(On ) and s−1 satisfies Init n . A
sequence of values (i0 /o0 · · · ik−1 /ok−1 ) taken from an execution is called a trace.
   Next, we introduce the implementation relation and the composition mech-
anism for the synchronous nodes, following the formalization in [3].
Definition 2. We say a node Nm implements a node Nn if (i) On ⊆ Om ,
(ii) In ⊆ Im ∪ Om , (iii) a dependency in the evaluation of x ∈ In ∪ On on y ∈ In
is preserved in Nm , and (iv) for every trace t of Nm , the projection of t onto On
is a trace of Nn . We denote this relation by Nm |= Nn .
The implementation relation is reflexive and transitive.
Definition 3. Given two compatible nodes Nn = (In , On , Sn , Init n , React n ),
where n ∈ {1, 2}, O1 ∩ O2 = ∅ and React 1 ∪ React 2 is acyclic, we consider the
parallel composition N1 || N2 = (I, O, S, Init, React), where I = (I1 ∪ I2 ) \ O,
O = O1 ∪ O2 , S = S1 ∪ S2 , Init = (Init 1 , Init 2 ) and React = React 1 ∪ React 2 .
Commutativity and associativity of the composition operator follow from the
definition. The languages described in the next subsection support an equivalent
of composite nodes, and their processors must check various properties, including
acyclicity above and causality, based on the DAG representation of React n . We
allow implicit renaming of state variables if a collision occurs in a composition.
Otherwise, a renaming of a variable x (of whatever kind) to y is denoted by
Nn [x := y]. We also denote replacement of an initial condition Init n with e by
Nn [Init n := e].
Example 1. We model a counter with a “hold” mode as a synchronous node
NCnt , where ICnt = {En}, OCnt = {C}, and React Cnt is described as
                             (
                               1 + pre(C) if En = true,
                        C=
                               pre(C)     otherwise.

Here (and hereafter), the expression pre(X) is interpreted as “the value of ex-
pression X in the previous round,” and we formalize it with a state variable
named “pre(X).” Accordingly, the state variable set is to be SCnt = {pre(C)},
and the initial condition is Init Cnt ≡ (pre(C) = 0). As an example of executions
of NCnt , when an input stream (false true false true) is fed, the output is (0 1 1 2).
3.2    Modeling Languages
We assume two representations of synchronous nodes, Simulink diagrams and
Lustre programs, described with the respective languages. Our case study sys-
tems are originally modeled with Simulink, and we use Lustre to explain the
proposed method in the following sections.
    Simulink 6 is a MATLAB toolbox for modeling synchronous (and hybrid)
systems using a GUI. It can be used to model with either a continuous timeline
or a timeline discretized with a fixed sample time; in this work, we assume the
latter and abstract each time with the number of accumulated sample times, as
in [24, 5]. Simulink diagrams, often called models, are hierarchical directed graphs
with edges, called lines, and nodes, called blocks, of various kinds. Fig. 1 shows
an example. Simulink models are modularized by encapsulating portions into
subsystem blocks. The example in Fig. 1 contains two subsystems, Filter and
Counter. In this work, we regard each Simulink model and each subsystem in a
model as a synchronous node. In addition, each line is regarded as a variable of a
node. Lines of Simulink are typed as machine-representable numbers e.g. int64
and double. In this work, we idealize them as mathematical types; analysis with
actual types is a future work.
    Lustre [7] is a programming language for describing synchronous nodes. For
example, the following code describes the content of the upper subsystem in
Fig. 1 as a node.
    node Filter (In: real) returns (FOut: bool)
    var Sum, D1, D2, Flt: real;
    let
      Sum = 0.0582*In - (-1.49*D1) - 0.884*D2;
      D1 = 0.0 -> pre Sum;    D2 = 0.0 -> pre D1;
      Flt = Sum - D2;         FOut = Flt > 0.5;
    tel
A Lustre program is easily associated with a synchronous node counterpart.
The code above describes a node with the elements IF = {In}, OF = {FOut},
SF = {pre(Sum), pre(D1)}, and Init F ≡ (pre(Sum) = pre(D1) = 0) (the name
Filter is abbreviated). Note that, we need not regard Sum, D1, D2 and Flt as
variables because their values are local to an evaluation of the reaction at a
round. The let section describes Init F and React F . For instance, the sentence
D1 = 0.0 -> pre Sum; is interpreted as follows. In the first transition, D1 is
assigned 0 (the initial value of pre(Sum) is 0); in the following transitions, D1 is
assigned the value of Sum in the previous round.
    There are several works on translation from Simulink to Lustre [6, 24, 5].
We assume that Simulink models are translated using a variant of the existing
methods. Some of the translation techniques are described in the next subsection.
Example 2. We consider “a filter and a counter,” a synchronous system that
consists of a second-order filter and a counter. This is represented as the Simulink
diagram in Fig. 1. In Lustre, the top-level system is described as
6
    https://www.mathworks.com/products/simulink.html
                  1
                  In
                                                                       > 0.5    1
                                               Z-1   D1                        FOut
                              Sum
      1      In                                                  Flt                  FOut
                                                                                                   1
      In
                                                                                                   Out
                                               Z-1   D2




                                          Filter

                                                                                             x10


                                          En

                                                                                      COut
                                    Z-1                   >= 1            1
                                                                       COut                  x1
                                    C



                                     Counter



              Fig. 1. Example Simulink model: “A filter and a counter” (Sys1).


  node Sys1 (In: real) returns (Out: bool) var FOut, COut: bool;
  let FOut = Filter(In); COut = Counter(RateTransition(FOut, 10));
      Out = FOut and COut;                                                                          tel

The description of Filter is shown above. RateTransition is a predefined node
and will be explained in Sect. 4.2. The Counter node is described as
  node Counter (En: bool) returns (COut: bool) var En_: bool; C_,C: int;
  let En_ = En -> ((pre En_) or En);
      C_ = 0 -> if (not pre En_) then 0 else (1 + pre C);
      C = 0 -> if En then C_ else pre C;
      COut = false -> if En then C >= 1 else pre COut;               tel

The description of the reaction is more complicated than Ex. 1, and the behav-
ior is slightly different. Some details of the description and ideas behind it are
explained in the following.


3.3        Other Features of Industrial Simulink Models

This section describes major features found in industrial Simulink models, and
how they are translated into Lustre.
   The first feature we examine is conditionally executed subsystems (CESs).
These are equipped with Enable and Trigger ports to control whether the
subsystem is activated. In Fig. 1, the Counter subsystem equips an Enable port
(named En). The subsystem updates the output value iff the enable signal is non-
zero; otherwise, the previous output value is retained unchanged (by default).
   We translate a CES into a Lustre node with additional input variables that
represent the control; every sentence in its description is conditioned with the
control inputs. In [24], CESs are described in a similar manner but using Lustre’s
when operator, which is not supported in some implementations (e.g. Kind2). An
example is the description of the Counter node. For each reaction, its original
description, e.g. the assignment to C_, and the conditioning with the control
input, e.g. the assignment to C, are described. Special care is taken for cases in
which the node is disabled initially and later outputs the initial value 0 when
activated.
    Second, industrial models often involve multiple rates, the use of several sam-
ple times.7 Sample times are specified in a model in various ways. In Fig. 1, two
RateTransition blocks specify the sample time of their output streams. The
block x1 sets the “default” sample time to 1; then, for the Counter subsystem,
the sample time is set to 10 with another block x10.
    Although translation from a multi-rate Simulink model into Lustre can be
performed simply with the when operator [24, 5], we translate such models in
a lengthy way (without when) as follows: (i) we determine the default sample
time as the GCD of the specified sample times; (ii) when multiple sample times
are used in a subsystem, we describe each portion with the same sample time
as a Lustre node, and describe the subsystem as a composite node; (iii) when
a subsystem (or a portion) has a coarser sample time than the default, it is
translated into a Lustre node with an additional input variable, as for the Enable
port; (iv) a Lustre node with a slower rate is instantiated with a RateTransition
node of the specified rate given as an input. An example translation is shown as
the Sys1 and Counter nodes, where the input En of Counter is also used for the
clock control and is fed RateTransition(FOut, 10) in Sys1.
    Third, Simulink supports handling multiplex streams by grouping several
lines with the Mux block. These can be simply translated into Lustre using Lus-
tre’s arrays or records [24]. In this work, we translated them using a set of bare
variables to avoid possible overhead.


3.4     Spatial and Temporal Complexity of Synchronous Systems

Spatial complexity correlates with the number of node compositions made. Con-
versely, large system descriptions tend to involve multiple synchronous nodes as
in Ex. 2. Then, analysis of a composite description can be processed node-wise.
However, the connection between the nodes matters in a compositional analysis;
for instance, circular referencing between two nodes and CESs that introduce
dependency between nodes make it difficult to analyze separately.
    The features in previous subsection may affect also the temporal complexity.
Use of CESs brings complexity not only in space but also in time because a
CES operates on activated rounds, which can be segmented. Multiple rates in a
system increase the number of (global) rounds taken in a sub-node due to the
rate ratio. Also, filter nodes such as Filter in Ex. 2, well characterized in the
frequency domain, bring a difficulty to analyze them in the time domain.
7
    Simulink also handles variable sample offsets. We omit this for the sake of simplicity.
4     Test Generation and Template Nodes

In this work, test generation is regarded as safety verification, which checks
whether the target top-level node satisfies the test objective in a round of an
execution (Sect. 4.1). In Sect. 4.2, we introduce templates of synchronous nodes
to specify test cases and intermediate signal streams that serve as contracts in
compositional reasoning (cf. Sect. 5).


4.1   Test Generation Problem

We consider safety properties φ on a synchronous node Nn to describe test
objectives and intermediate properties.

Definition 4. The syntax of safety properties φ is as follows.

             e ::= (Predicate on On ) | (Boolean combination of e),
             φ ::= e | e@s | φ ∧ φ,

where s ∈ N represents a round of executions.

Intuitively, for every trace of Nn , a property of the form e (resp. e@s) means
that the output in every round (resp. in the round s) satisfies e. We denote by
o |= φ that the valuation with an output value o ∈ D(On ) satisfies φ.

Definition 5. We interpret a safety property φ as a synchronous node N[φ] =
(∅, O[φ] , S[φ] , Init [φ] , React [φ] ) with nondeterministic behaviors. When φ ≡ e, S[φ] =
                                   /o
∅ and React [φ] describes {s∅ −→ s∅ | o |= e}; when φ ≡ e@s, S[φ] = {c},
                                           /o
Init [φ] = 0 and React [φ] describes {sc −→ sc + 1 | (sc , o) |= (c = s ⇒ e)}; when
φ ≡ φ1 ∧φ2 , we rename the counter variables if necessary, and merge the reaction
descriptions of N[φ1 ] and N[φ2 ] .

A node N[φ1∧φ2] is equivalent to N[φ1] || N[φ2] iff O[φ1] ∪ O[φ2] = ∅.

Definition 6. Given a target node Nn and an objective eobj (a proposition on
On ), a test generation problem asks to find a test case T , a synchronous node,
such that T || Nn |= N[eobj @s] holds for some s.


4.2   Synchronous Node Templates

To synthesize test cases and intermediate properties in a test generation, we use
templates to represent a set of streams of interest. We can consider Lustre’s const
-value streams as a template for constant-value streams. Other templates are
described using synchronous nodes with constant parameters and input streams;
for example, the Step and Square templates are described as follows.
    node Step (const s: int; v1, v2: ’a) returns (Out: ’a)
    var c: int;
    let c = 0 -> (pre c) + 1; Out = if c < s then v1 else v2;                     tel

    node Square (const t, p: int; v1, v2: ’a) returns (Out: ’a)
    var c, l: int;
    let c = 0 -> (pre c) + 1;
        l = 0 -> if c+p-(pre l) >= 2*t then (pre l) + 2*t else (pre l);
        Out = if c+p-l >= t then v1 else v2;                            tel

These nodes represent respectively a temporal concatenation of two streams v1
and v2 at the round s and a square wave of half-length t and phase shifting
p that evaluates to either v1 or v2. In the descriptions above, ’a denotes a
polymorphic type, which is used for space efficiency and is to be replaced with
a primitive type regarding the context. The last two inputs of Step and Square
are not const for utility (e.g. to build multiple step streams). In addition, we
restrict the parameter values to s > 0 for Step and t ≥ 2 and 0 ≤ p < 4t for
Square.8

Example 3. A test objective for checking that the Filter node in Fig. 1 outputs
the value true at step 10 is described by a safety property (FOut = true)@10 (or
simply FOut@10). The node implements a band-path filter for which the Flt
block outputs greater values when a signal stream with a specific frequency is
input. For instance, the objective is fulfilled with the input Square(5, 1, −1, 1).

    As an adapter between nodes with different rates, we use the template
RateTransition for nodes that synchronize a stream En_ with a clock signal
stream of interval s.
    node RateTransition (En_: bool; const s: int) returns (En: bool)
    var c: int;
    let c = 1 -> if pre c >= s then 1 else (pre c) + 1;
        En = if c <= 1 then En_ else false;                                       tel

Every node that runs with a slower rate than the default is equipped with a
control input (see Sect. 3.3); hence, a RateTransition instance is set at the
upstream to configure the rate. In the following, we denote a RateTransition
instance with interval s connected to a node Nn by RT s,n .

Example 4. A composition of Filter and Counter, as in Fig. 1, must be adapted
with a RateTransition instance to modify the rate of Counter. The composition
is described as

              NFilter || NRateTransition [En_ := FOut, s := 10] || NCounter .

We abbreviate the above as NFilter || RT 10,Counter || NCounter .
8
    These constraints are specified as preconditions using Kind2’s annotation language.
5     Compositional Test Generation
In this section, we present a compositional test generation scheme, summarized
in the following four steps.
 1. Specification of the composition. Our method assumes that modellers specify
    a systems as a composition of synchronous nodes. Along with the composi-
    tion, we construct an outline proof tree based on the dedicated inference rules
    (Sect. 5.2). Here, the nodes of the tree are declarations of implementation
    relations, in which some nodes in the composites might be parameterized.
 2. Inference of test cases and contracts. Each of the declarations above can con-
    tain a special node that represents a test case or a contract, an intermediate
    property on the node interface. We leave this unknown in Step 1; in this
    step, we fill the blanks using both automated inference performed by SMT
    solvers and additional human efforts.
 3. Consistency checking between contracts. Once the parameters are instan-
    tiated, the tree is viewed as an outline of compositional safety verification.
    Some parts of it are validated automatically using existing tools (e.g. Kind2).
    If validation succeeds, the test cases generated in Step 2 can be expected to
    work for the entire system.
 4. Refinement based on a counterexample. Failure of the check in Step 3 results
    in a counterexample, which is an execution that violates a contract. After
    analyzing it, we can go either to Step 2 to modify the contracts or to Step 1
    to modify the deduction tree e.g. by applying a temporal decomposition rule.

5.1     Translation into Combinational Nodes
Combinational nodes [2] are synchronous nodes with no state variables. For the
purpose of temporal-compositional analysis of nodes, we translate a node into
a combinational one in such a way that the internal states become externally
visible and their initial values are given externally.
Definition 7. Let Nn be a node and eSn be a proposition on Sn . C(Nn , eSn )
represents a composition of the following two nodes:
 (i) The (combinational) node (In∪Sn , On∪Sn0 , ∅, true, React 0n ), where Sn0 is a set
     of fresh variables {x0 | x ∈ Sn }, and React 0n is equivalent to React n except
     that the assignments x0 := next(x) are appended for each x ∈ Sn , where
     next(x) represents the value of x in the next round, which must be described
     in React n .
(ii) The node (Sn0 , Sn , Sn00 , e00Sn , React 00n ), where Sn00 = {pre(x0 ) | x0 ∈ Sn0 }, e00Sn is
     equivalent to eSn except that x ∈ Sn is replaced with x00 ∈ Sn00 , and React 00n
     describes the assignments ∀x ∈ Sn , x := pre(x0 ).

Example 5. Let us consider the node Cnt that is a translation of Ex. 1 in Lustre.
    node Cnt (En: bool) returns (C: int)
    let C = if En then 1 + pre C else pre C;                                                  tel
             N1 || Nb |= Na                           C(Nn , Init n ) |= N[e0Sn @j]
             N2 || Na |= Nb                            C(Nn , eSn ) |= N[e@k]
                                   (AG)                                            (Temp)
           N1 || N2 |= Na || Nb                           Nn |= N[e@j+k+1]

                                Nn || RT s,n |= N[φ]
                                                                        (RT)
                  Nn [@ := @r] || RT rs,n |= N[φ] [@ := @r]

      N1 |= Na Na |= Nb Nb |= N2
                                             (Cons)                            (IP:φ0 ⇒ φ)
               N1 |= N2                                      N[φ0 ] |= N[φ]

Fig. 2. Inference rules for compositional test generation. N , where  ∈ {1, 2, a, b, n},
represents an arbitrary synchronous node.


Here, we denote the state variable pre(C) by pC. The two components of C(NCnt ,
Init Cnt ) are described as follows.
   node Cnt_c1 (En: bool; pC: int) returns (C, pC’: int)
   let C = if En then 1 + pC else pC;
       pC’ = C;                                                                          tel

   node Cnt_c2 (pC’: int) returns (pC: int)
   let pC = 0 -> pre pC’                                                                 tel

Lemma 1. For a node Nn , (i) C(Nn , Init n ) |= Nn , and (ii) for every trace t of
Nn , there is a trace of C(Nn , Init n ) whose projection onto On is t.

5.2   Deduction System for Compositional Reasoning
We propose a deduction system for constructing a proof tree for compositional
reasoning regarding the implementation relation between synchronous nodes.
Definition 8. The rules AG, Temp, RT, Cons and IP are as shown in Fig. 2.
    Compositional reasoning for systems that involve synchronized concurrent
nodes is conducted using assume-guarantee (AG) methods [12, 3], with each node
in the system associated with a contract, an assumption on the inputs, and a
guarantee on the outputs. In Fig. 2, the rule AG is intended for the AG reasoning
on spatial-compositional nodes. This rule allows each component N1 and N2
to be analyzed separately when combined with a portion of the consequence
nodes. Given a safety property N[φ1∧φ2] , it is translated as N[φ1] || N[φ2] (when
O[φ1] ∪ O[φ2] = ∅) and an AG composition can be applied.
    The rule Temp provides a method for temporal-compositional reasoning.
When verifying a property at the (j + k + 1)-th round, it splits the reachabil-
ity problem into two portions and allows verification with analyzing up to round
j or k. To observe the internal states and modify the initial states, this rule
requires the transformation in Def. 7. Let e, eSn and e0Sn be propositions on the
variables in On , Sn and Sn0 (cf. Def. 7), respectively.
    The rule RT enables temporal shrinking of a verification task to 1/r (r ∈ N>1 )
when a rate transition is applied to the target node. Nn [@ := @r] denotes
to replace every property of the form e@ described in Nn to e@r. With this
rule, an analysis up to step k suffices when checking φ ≡ e0 @rk.
    The rule Cons represents logical consequence with respect to the implemen-
tation relation. The rule IP translates logical consequence between contracts into
the implementation relation.

Lemma 2. The rules in Def. 8 (and Fig. 2) are sound.

Proof sketch. The soundness of AG is proved in [3]. For Temp, suppose that
the goal does not hold and contains a counterexample. Then, if the state in the
j-th round of the counterexample does not satisfy eSn , it contradicts with the
first premise; otherwise, it contradicts with the second premise. For other rules,
the soundness is straightforward from the definitions of RTrs,n , implementation
relation, and safety properties.


5.3   Basic Procedures

This section proposes some procedures for Steps 2–4 for performing static anal-
yses on node descriptions.


Model checking using an SMT solver. Given a node Nn and a safety e@k,
bounded model checking (BMC) [4] checks whether Nn |= N[e@k] using an off-
the-shelf SMT solver. In our compositional deduction, we rely on this procedure;
in addition to the rules in Fig. 2, we use the rule below to represent a proof made
with a BMC.

                                                 (V)
                                 Nn |= N[e@k]

A BMC process is based on an encoding of the fact Nn |= N[¬e] into a logic
formula. If checking the satisfiability by a trace of length k +1 results in UNSAT,
then the fact Nn |= N[e@k] is proved. Otherwise, a result of SAT indicates a
counterexample, a valuation of the encoded formula that represents an execution
satisfying (¬e)@k.


Test generation as safety falsification. Given a test generation problem
with an objective eobj , we use a BMC to generate a test case T automatically.
Here, in contrast to the previous paragraph, we perform a BMC to falsify the
safety ¬eobj ; hence, we encode eobj @k, for each k ≥ 0. A result of SAT for some
k indicates a counterexample for ¬eobj ; then, we construct a test case T such
that T || Nn |= N[eobj @k] holds.
Test generation with templates. In general, test generation considers a large
search space i.e. arbitrary streams of length k + 1 or less. We are able to use the
template nodes in Sect. 4.2 to reduce the search space to a set of meaningful
signal streams, depending on the context. We perform a BMC on the safety
of the system T 0 || Nn using a template T 0 ; then, it instantiates the template
parameters with a SAT valuation.

Pre- and postcondition inference. As mentioned earlier, contract inference
is important in compositional reasoning. Basically, we deduce contracts manually
based on the reaction description of a node. Otherwise, the following methods
will be useful: (i) Constant propagation. A system description may contain a
constant, e.g. a threshold used for a case analysis. It is useful for bounding in-
put/output domains. (ii) Invariant generation. Recent SMT solvers are equipped
with a function for deducing a lemma from a given formula. This function is
useful for deducing invariants of synchronous nodes; e.g., Kind2 implements this
function. (iii) Use of templates. We can assume a template for an interface of a
composite and try to generate an invariant for its parameters.


6     Examples
This section describes four examples
                                                       Sys. 1 Sys. 2 Sys. 3 Sys. 4
of compositional test generation fol-
                                            |I|/|O|        1/1 2/1 4/4 19/2
lowing the steps explained at the be-
                                            # blocks        22     54 215 281
ginning of the previous section. The
                                            # compo’s 3/0 3/2 4/14 3/4
latter two target systems, Sys. 3 and
Sys. 4, are excerpted from industrial products whose test objectives are difficult
to achieve using existing tools, as explained later. The first two systems, Sys. 1
and Sys. 2, are simplified versions of Sys. 3 and Sys. 4, respectively, intended
to explain the compositional process using the proposed method. Each example
is described with both Simulink and Lustre. Some data on the Simulink models
representing their sizes are shown in the table above, which shows the numbers
of the top-level input variables |I| and output variables |O|, the number of blocks
in the Simulink model (excluding the inport/outport blocks), and the number
of components in the direction of space/time handled by the proposed method.
At the end of every case study, the test case generated is confirmed to achieve
the objective with simulation using Simulink.

6.1    A Filter and a Counter
We recall Ex. 2. The objective here is to observe the output (Out) becomes true
in a bounded execution, i.e. eobj ≡ (Out = true).
    For the composition of the back-end part, we modify the node Sys1 as:
    node Sys1_m (In: real) returns (Out, FOut, COut: bool)
    let FOut = Filter(In); COut = Counter(RT(FOut, 10));
        Out = Back(FOut, COut);                                               tel
                          T || NF || N[COut@20]    |=    N[FOut@10∧FOut@20]          (1)
               RT 1,C || NC || N[FOut@1∧FOut@2]    |=    N[COut@2]                   (2)
                         T || NF || RT 10,C || NC |=     N[FOut@10∧(FOut∧COut)@20]   (3)
            T || NF || RT 10,C || NC || N[Out@ 20 ] |=   N[(FOut∧COut)@20]           (4)
                        NB || N[(FOut∧COut)@20]    |= N[Out@ 20 ]                    (5)
                    T || NF || RT 10,C || NC || NB |= N[Out@ 20 ]                    (6)

                             (V)            (V)
                       (1)            (2)
                                            (RT,AG)
                               (3)
                                     (Cons,IP)                  (V)
                               (4)                        (5)
                                                                (AG,Cons)
                                            (6)

       Fig. 3. Outline of test generation of “a filter and a counter” (Sys1_m).


Here, the node Back is described as:
  node Back (FOut, COut: bool) returns (Out: bool)
  let Out = FOut and COut;                                                           tel
   As for Step 1, we determine an outline of the test generation process based on
the composition of the nodes Front, Counter and Back (henceforth, F, C and B,
respectively), which is illustrated as the proof tree in Fig. 3. The tree consists of
the declarations of the implementation relations (1)–(6). The terms surrounded
by boxes are unknown in Step 1 and are identified in the later steps. In the tree,
the test case is denoted by T . As a result, the proof succeeds with

                          T = NSquare(5,1,−1,1) [Out := In],                          (7)

which is an instance of the Square template placed at the input of NF .
    Let us look into the tree from bottom to top. At the bottom, the AG rule
is applied, with the system divided as T || NF || RT10,F || NC and NB . Before ap-
plying AG, we strengthen the consequent by a composition with a contract
node; the contract (FOut ∧ COut)@20, identified in Step 2, is a precondition for
NB to output true (it is checked by Eq. (5)). In the other branch, Eq. (4) is ob-
tained by strengthening the antecedent and weakening the consequent of Eq. (3).
Above that, the AG rule is applied again with the composition of T || NF and
RT10,F || NC . To obtain Eq. (2), we apply the RT rule to shrink the timeline
for 1/10. The consequent COut@2 of Eq. (2) does not affect the other branch
(Eq. (1)), because the scopes do not overlap, i.e., COut ∈/ OT ∪ OF .
    The inference of the contracts (boxed terms in Fig. 3) performed in Step 2
is outlined as follows.
 i. We obtain the property ∃s, (FOut ∧ COut)@s by a precondition calculus for
    the postcondition ∃s, Out@s of NB .
 1         In1
 In1
                                   XZ

 2         In2
 In2                                          1
                                         XZ                     Z-1    1    Fb
                                              XZ
                      GD_X                                            Fb

           In1


                                              2          >= 2          2
           In2                     YZ    YZ                                 Out   1
                                              YZ                      Out
                                                                                  Out

           Fb
                                                         Z
                      GD_Y



          Fig. 4. Simulink model of “two guarded decrementers” (Sys2).


 ii. We analyze NC using an SMT solver. We assume that the constant enable
     signal true is provided and falsify the property ¬COut (we omit ¬FOut since
     FOut is out of the scope). It succeeds with k = 2.
iii. We check whether a stream of length 21 whose values are true in rounds 10
     and 20 can be output from NF . For this check, we add to NF a monitor
        FOut_d10 = Delay <<10>> (false, FOut);
    using a variable delay node whose output is false initially and FOut delayed
    for 10 rounds in the following. Then, we falsify ¬(FOut d10∧FOut), assuming
    a square-wave signal stream. The falsification does not succeed with k = 10
    but succeeds with k = 20, yielding the test case (7). This proves Eq. (1).
iv. Finally, we assume the enable stream for the rounds 1 and 2 and falsify
    ¬COut@2. It fails, thereby proving Eq. (2).

6.2    Two Guarded Decrementers
The second example involves a circular interconnection between components and
also illustrates the use of the rule Temp for temporal decomposition. Fig. 4 shows
a Simulink model of the example, which consists of three nodes (subsystems).
The model receives two real-valued streams as inputs and outputs a Boolean
stream. The nodes GD_X and GD_Y are almost equivalent except for the condition
described and an additional conditioning at the end of GD_Y. Each of them
describes a control gate for checking some conditions on the input values, and
also a decrementer that affects the decision by the gate; we omit the details
owing to space limitations. Another node Z receives inputs XZ and YZ of types
bool and int and checks some conditions; the value of XZ represents whether
decrementing finishes (true) or not (false); YZ evaluates to either 2 (when Fb is
true), 1 (when decrementing finishes) or 0 (otherwise).
    We consider the test generation problem with eobj ≡ (Out = true). We
translate the Simulink model into a Lustre program and apply the proposed
method. As in the previous subsection, we show the resulting proof tree and
then explain the process of compositional test generation.
                        ..                                               ..
                         .                                                .
   T1 ||C(NSys2 ,Init Sys2 ) |= N[eSys2 @100]          T2 ||C(NSys2 , eSys2 ) |= N[Out@ 101 ]
                                                                                                (Temp)
                                T || NSys2 |= N[Out@ 202 ]

           T2 || C(NX , eX ) || N[YZ≥1@101 ∧ YZ=2@101]        |=   N[XZ@100] || T2               (8)
         C(NY , eY ) || N[Fb@101] || N[XZ@100] || T2          |=   N[YZ≥1@100 ∧ YZ=2@101]        (9)
       T2 || C(NX , eX ) || C(NY , eY ) || N[Fb ∧ Out@101]    |= N[XZ ∧ YZ≥1@100 ∧ YZ=2@101]    (10)
   C(NZ , ¬pre(Fb)) || N[(XZ ∧ YZ≥1)@100 ∧ (YZ=2)@101] |=          N[Fb ∧ Out@101]              (11)
     T2 || C(NX , eX ) || C(NY , eY ) || C(NZ , ¬pre(Fb)) |= N[Out@ 101 ]                       (12)

                              (V)            (V)
                        (8)            (9)
                                             (AG,Cons)                 (V)
                               (10)                             (11)
                                                                       (AG,Cons)
                                                (12)

      Fig. 5. Outline of test generation of “two guarded decrementers” (Sys2).


    Fig. 5 illustrates the proof tree. The root of the overall tree is depicted in the
top part. We denote the overall composite node by NSys2 and the composite of
the sub-nodes translated into combinational nodes (Def. 7) by C(NSys2 , e), where
e is a conjunction of the initial conditions of the sub-nodes. Again, the terms
obtained by additional inferences are enclosed with boxes. The test case T is
temporally decomposed into T1 and T2 . The generated T in the end is composed
of nested Step templates, where the stream In1 is specified as a four-step stream

                  TIn1 = NStep(101, Step(1,1.2,0.8), Step(176,−0.6,−0.8)) ,

where TIn1 represents a sub-node for the output In1, and the stream In2 is set
as a two-step stream.
    Fig. 5 also illustrates the right-hand side branch that is built above the second
premise of the root (we abbreviate GD_X and GD_Y as X and Y). The sub-goal is
discharged by a temporal decomposition. It is based on a strategy of executing
two decrementers in sequence (first X and then Y); we verify the decrementing
behavior of each node separately, for rounds 0, . . . , 100 and rounds 101, . . . , 202.
eX and eY represent the intermediate state at the round 100. The stream for the
variable Fb is expected to be valued false except for the final round 202; thus,
we set the initial condition ¬pre(Fb) in Eq. (12). The rest of the proof tree is
constructed with an application of AG, some rewritings of properties, and node
decompositions.
    The inference of the contracts in Step 2 is outlined as follows:

 i. As a first trial, we attempt to falsify the objective without the temporal
    decomposition. We deduce a precondition ∃s, (XZ ∧ YZ ≥ 1)@s by analyzing
     the node Z. Then, we can falsify the precondition for the nodes X and Y, both
     with the bound 101; the Square template is set to In1 and Constant is set
     to In2; as a result, we obtain a test case T1 or T2 for X or Y, respectively.
     However, the two test cases differ and it can be verified with a further analysis
     that there are no common test cases of length 101 or less.
 ii. We take the above-mentioned strategy to decrement X and Y in series and
     to decompose temporally. Applying the rule Temp requires the intermediate
     condition eSys2 ; here, we simply perform a numerical simulation to obtain
     the state at round 101. For the first phase, we use T1 as a test case and
     compute eSys2 with a simulation.
iii. For the second phase, by falsifying the precondition ∃s, (YZ ≥ 1)@s for the
     node C(NY , eY ), we obtain a test case T20 of length 101. We must check ad-
     ditionally that inputting T20 to C(NX , eX ) satisfies the precondition ∃s, XZ@s
     after 101 rounds.
iv. Finally, we concatenate T1 and T20 to obtain the test case T . To construct
     the proof tree, we also need contracts of C(Sys2, eSys2 ) at round 100, i.e.
     (XZ ∧ YZ ≥ 1)@100, due to the feedback Fb.

6.3   PM Motor Control
The third example, which describes a model of a motor and its controller, uses
three sample times, s = 5 × 10−5 , 20s and 100s, and requires a large number
of rounds to fulfill the objective at the base sample rate. We generated a test
case for observing a specific value as a top-level output. We omit the details of
the target because it is an in-house product and would be lengthy; instead, we
report the process of compositional test generation.
    We separated the top-level spatially into three modules and a sub-module into
two; we denote the composition as (N1 || N2 ) || (N20s || N100s ) (the latter names
represent the local sample times). In the system, the nested counter in the node
N20s is the main cause of the test case being long. Based on the numerical
simulation of the system, we found that the objective requires decrementing the
counter three times and it takes at least 865×20 = 17 300 rounds. To this end, we
applied the rules RT and Temp to analyze the behavior in a temporally separated
and shrunken way; to separate the behavior into 12 segments of lengths 59–83
as combinational nodes, we used the intermediate conditions on the internal
counter that is incremented or reset every round.
    The other nodes were exercised to synchronize with the behavior of N20s .
Since the node N1 , which contains the output variable in the objective, is com-
binational, its invariant precondition for the objective was calculated. N2 was
separated with Temp, and it was verified that the first module reaches a con-
stant state with a particular input; then, the rate of the second module N100s
was shrunk using RT, and it was verified that it fulfills a necessary intermediate
condition induced from the objective with an instance of the Step template of
length 173.
    Finally, we obtained a test case of length 17 301, which consists of three
one-step streams and one three-step stream.
6.4   Extended Two Guarded Decrementers

The last example is an industrial model that involves two guarded decrementers
as in Sys2. We report a summary of the test process.
    We separated the model spatially into three as N1 || N2 || N3 ; N1 is located
upstream of others, and N2 is located upstream of N3 . Because we could not
find, in the experiments, an intermediate condition (as a template instance) on
the interface variables between N1 and either of N2 or N3 , we analyzed N1 || N2
and N1 || N3 combined into one node each.
    For the first composite N1 || N2 , we performed a manual constant propagation
in the node description, and we found that the node outputs a constant stream
assuming some condition on the input. This constant output was assumed as a
contract in the analysis of the other composite.
    The composite N1 || N3 contains the two decrementers and they are required
to be exercised separately. Different from the process in Sect. 6.2, we did not
apply further spatial composition to N3 because some peripheral behaviors were
difficult to describe in a contract and the spatial size was not critical for analysis.
We simply applied the rule Temp to split the temporal analysis into four; as a
result, we obtained the fragments of the test case of length 50 or 52 for four
combinational translations of N1 || N3 .
    The test case obtained is of length 204, which consists of (i) eight constant
streams, (ii) eight four-step streams, (iii) two one-step streams, and (iv) one
composite square and four-step stream.


7     Experiments

This section reports the experimental results on the test generation of Systems 1–
4 in the previous section. Sect. 7.1 shows the statistical data on the experiments
using our compositional method. Sect. 7.2 presents the results with the existing
tools for comparisons. The experiments were conducted using a 2.2GHz Intel
Xeon E5-2650v4 processor with 128GB of RAM. The descriptions in Lustre
and Simulink and the SMT-LIB scripts for validation are available at https:
//dsksh.github.io/vmcai2021.zip.


7.1   Compositional Test Generation

We have partially automated the proposed method using Kind2 (version 1.2.0),
which is equipped with the Z3 SMT solver (version 4.8.8). In the experiments,
first, most of the test cases and contracts were obtained by falsifying the ob-
jectives and intermediate conditions with BMC implemented in Kind2. This is
an incremental process in which the bounds to analyze are gradually increased;
thus, a shortest counterexample will be obtained if one exists. For comparison,
we have also tried to generate test cases by falsifying the objectives against entire
systems. Second, once the proof tree for compositional test generation was built,
                          Table 1. Experimental results.

                          Sys. 1           Sys. 2         Sys. 3        Sys. 4
          Comp.   (0.80 + 0.03)s   (12.2 + 0.09)s   (134 + 0.4)s   (250 + 13)s
          Mono.             1.1s             790s           TO             TO
          SLDV             0.03s      Undecided             TO             TO
          TMC          65s (112)              TO         52s (2)           TO



we described manually the inference rules in Def. 8 and the tree in an SMT-LIB9
script; then, it was processed by Z3 to validate every inference performed in the
proof tree. In the description, the rule RT was detailed to ease matching with
the target terms for the efficiency of solving; also, the rewriting rules for some
equivalent terms were described.
    The CPU time taken in the test generation processes is shown in two of
the rows of Table 1. The row “Comp.” shows the time in the form of (x + y)s,
which means xs and ys were taken in the falsification using Kind2 and the
validity/consistency checking using Z3, respectively. The row “Mono.” shows
the time taken in the monolithic falsification on the entire systems. “TO” is for
the timeout in 3 600s.


7.2    Comparison with Existing Tools

Some of the examples have difficulties with the existing tools. We give compar-
ison results as evidence.
     We first compared with the testing of Simulink models using SLDV (Sect. 2)
on MATLAB (R2019b). In the experiment, we specified ¬eobj as a “Proof Ob-
jective” in the Simulink model and performed a “Property Proving” with SLDV.
The results are shown in the row “SLDV” of Table. 1. For Sys. 1, a test case was
generated more efficiently than in the analysis with Kind2; however, for other
examples, test generations failed or did not terminate in 3 600s; the execution
for Sys. 2 reported “UNDECIDED WITH COUNTEREXAMPLE” after 14s,
probably, in our view, because some blocks used were not supported.
     Second, we compared with an in-house tool that implements the template-
based Monte-Carlo method [23] (called “TMC” here). TMC repeatedly instanti-
ates a given template for each input port of the Simulink model and simulates
it until the objective is fulfilled. We configured the templates that were iden-
tified in the previous section for each system; the lengths of simulations were
set ten times longer than the length of our test cases for the efficiency of TMC.
The row “TMC” shows the execution time and the number of simulations (the
averages for ten executions). A test case was generated for Sys. 1 but the re-
sult indicated that handling of filters was not efficient even with an appropriate
template. Sys. 3 was processed efficiently with one to four trials. In fact, the
solutions of the objective are not rare in this example; in such a case, exercising
with random input of a particular length is an efficient strategy. n the contrary,
9
    http://smtlib.cs.uiowa.edu.
test generation for Sys. 2 and 4 did not succeed with 33 331 and 6 196 trials in
5 hours.
     In the experiments, SLDV and TMC could not handle Systems 2–4 and Sys. 2
and 4, although they worked efficiently when possible. We conjecture that SLDV
uses static analysis on models and therefore suffers from the complexity issue.
When it fails, we cannot know the exact reason since it is a black-box tool. Yet
TMC is a simple method that considers the target as a black box, but it works
efficiently for many systems [23]. However, since it is an incomplete method,
there would be some instances that are difficult to handle. For example, when
an objective has a rare solution as in Sys. 2 and 4, TMC is disadvantageous.


8   Conclusion and Future Work

We presented a compositional test generation method for synchronous systems
and four case studies on industrial Simulink models.
    Simulink models were translated into Lustre programs, and associated with
classical formalizations of synchronous systems. Test generation was performed
using the proposed scheme, by first drawing a proof tree with “blank squares”
and then filling the blanks using either a manual or an automatic process for in-
ferring the contracts. In test generation, the rules AG, Temp and RT address the
spatial and temporal complexity, respectively. It was shown that the method can
be automated partially using Kind2 and Z3. Full automation of the generation
and validation of proof trees is left for future work.
    In the case studies, it was necessary to understand the content of the system
descriptions and to infer the contracts. It could become routine that modelers
provide such contracts preliminarily. Otherwise, automated inference of the con-
tracts and/or an interactive tool that encourages the modelers to provide hints
for a contract could be developed in future work. We also consider that spec-
ifying a contract will facilitate co-modeling as it will refine the compositional
model of a system. Our experiments imply that systems such as Sys. 4 can be
analyzed using a random simulation. Hybrid methods of compositional reasoning
and random simulation might be another research direction.


References
 1. Abd Elkader, K., Grumberg, O., Păsăreanu, C.S., Shoham, S.: Automated circular
    assume-guarantee reasoning. Formal Aspects of Computing 30(5), 571–595 (2018)
 2. Alur, R.: Synchronous Model. In: Principles of Cyber-Physical Systems,
    chap. 2, pp. 13–64. MIT Press (2015), http://mitpress.mit.edu/books/
    principles-cyber-physical-systems
 3. Alur, R., Henzinger, T.A.: Reactive modules. Formal Methods in System Design
    15(1), 7–48 (1999)
 4. Biere, A., Cimatti, A., Clarke, E.M., Zhu, Y.: Symbolic Model Checking without
    BDDs. In: TACAS. pp. 193–207. LNCS 1579 (1999), http://portal.acm.org/
    citation.cfm?id=691738
 5. Bourbouh, H., Garoche, P.l., Loquen, T., Noulard, E., Pagetti, C.: CoCoSim, a
    code generation framework for control/command applications. In: ERTS. pp. 1–11
    (2020)
 6. Caspi, P., Curic, A., Maignan, A., Sofronis, C., Tripakis, S., Niebert, P.: From
    simulink to SCADE/Lustre to TTA: A layered approach for distributed embedded
    applications. ACM SIGPLAN Notices 38(7), 153–162 (2003)
 7. Caspi, P., Pilaud, D., Halbwachs, N., Plaice, J.A.: LUSTRE: A declarative language
    for programming synchronous systems. In: POPL. pp. 178–188 (1987)
 8. Champion, A., Mebsout, A., Sticksel, C., Tinelli, C.: The KIND 2 Model
    Checker. In: CAV. pp. 510–517. LNCS 9780 (2016), https://doi.org/10.1007/
    978-3-319-41540-6
 9. Champion, A., Gurfinkel, A., Kahsai, T., Tinelli, C.: CoCoSpec: A mode-aware
    contract language for reactive systems. In: SEFM. pp. 347–366. LNCS 9763 (2016)
10. Gadkari, A.A., Yeolekar, A., Suresh, J., Ramesh, S., Mohalik, S., Shashidhar, K.C.:
    AutoMOTGen : Automatic Model Oriented Test Generator for Embedded Control
    Systems. In: CAV. pp. 204–208. LNCS 5123 (2008)
11. Garoche, P.L., Howar, F., Kahsai, T., Thirioux, X.: Testing-based compiler vali-
    dation for synchronous languages. In: NFM. pp. 246–251. LNCS 8430 (2014)
12. Giannakopoulou, D., Namjoshi, K.S., Pasareanu, C.S.: Compositional Reasoning.
    In: Handbook of Model Checking, chap. 12, pp. 345–383. Springer (2018)
13. Giannakopoulou, D., Pasareanu, C.S., Blundell, C.: Assume-guarantee testing for
    software components. IET Software 2(6), 547–562 (2008)
14. Godefroid, P.: Compositional dynamic test generation. In: POPL. pp. 47–54 (2007),
    http://portal.acm.org/citation.cfm?doid=1190216.1190226
15. Halbwachs, N., Lagnier, F., Raymond, P.: Synchronous Observers and the Verifi-
    cation of Reactive Systems. In: Algebraic Methodology and Software Technology
    (AMAST). pp. 83–96 (1993)
16. Henzinger, T.A., Qadeer, S., Rajamani, S.K.: Assume-guarantee refinement be-
    tween different time scales. In: CAV. pp. 208–221. LNCS 1633 (1999)
17. Kanade, A., Alur, R., Ivančić, F., Ramesh, S., Sankaranarayanan, S., Shashidhar,
    K.C.: Generating and analyzing symbolic traces of simulink/stateflow models. In:
    CAV. pp. 430–445. LNCS 5643 (2009)
18. Matinnejad, R., Nejati, S., Briand, L.C., Bruckmann, T.: SimCoTest: A Test Suite
    Generation Tool for Simulink/Stateflow Controllers. In: ICSE. pp. 585–588 (2016),
    http://dl.acm.org/citation.cfm?doid=2889160.2889162
19. McMillan, K.L., Zuck, L.D.: Compositional testing of internet protocols. In:
    SecDev. pp. 161–174 (2019)
20. Pasareanu, C.S., Schumann, J., Mehlitz, P., Lowry, M., Karsai, G., Nine, H.,
    Neema, S.: Model Based Analysis and Test Generation for Flight Software. In:
    Third IEEE International Conference on Space Mission Challenges for Information
    Technology. pp. 83–90 (2009), http://ieeexplore.ieee.org/document/5226844/
21. Peranandam, P., Raviram, S., Satpathy, M., Yeolekar, A., Gadkari, A., Ramesh, S.:
    An Integrated Test Generation Tool for Enhanced Coverage of Simulink/Stateflow
    Models. In: DATE. pp. 308–311 (2012)
22. Satpathy, M., Yeolekar, A., Ramesh, S.: Randomized Directed Testing (REDI-
    RECT) for Simulink/Stateflow Models. In: EMSOFT. pp. 217–226 (2008)
23. Tomita, T., Ishii, D., Murakami, T., Takeuchi, S., Aoki, T.: Template-Based Monte-
    Carlo Test-Suite Generation for Large and Complex Simulink Models. IEICE
    Transactions on Fundamentals of Electronics, Communications and Computer Sci-
    ences E103-A(2), 451–461 (2020)
24. Tripakis, S., Sofronis, C., Caspi, P., Curic, A.: Translating Discrete-Time Simulink
    to Lustre. ACM Transactions on Embedded Computing Systems 4(4), 779–818
    (2005)
25. Zhan, Y., Clark, J.A.: Search-based mutation testing for simulink models. GECCO
    2005 - Genetic and Evolutionary Computation Conference pp. 1061–1068 (2005)
