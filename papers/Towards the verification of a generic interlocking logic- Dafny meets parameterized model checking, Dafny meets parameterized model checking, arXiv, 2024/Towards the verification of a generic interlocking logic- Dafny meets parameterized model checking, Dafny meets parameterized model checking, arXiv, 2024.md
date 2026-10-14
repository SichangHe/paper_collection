                                              Towards the veriﬁcation of a generic interlocking
                                                                   logic:
                                                Dafny meets parameterized model checking
                                                    Alessandro Cimatti                              Alberto Griggio                              Gianluca Redondi
                                               Fondazione Bruno Kessler (FBK)                Fondazione Bruno Kessler (FBK)                Fondazione Bruno Kessler (FBK)
                                                      cimatti@fbk.eu                                griggio@fbk.eu                               gredondi@fbk.eu
arXiv:2403.00087v1 [cs.LO] 29 Feb 2024




                                         Abstract                                                                       crossing) must be properly operated and that mutual exclu-
                                         Interlocking logics are at the core of critical systems control-               sion between interfering routes is ensured. At a high level
                                         ling the traﬃc within stations. In this paper, we consider a                   of abstraction, an interlocking system can be thought of as
                                         generic interlocking logic, which can be instantiated to con-                  implementing a very articulated mutual exclusion protocol,
                                         trol a wide class of stations. We tackle the problem of pa-                    that we refer to as interlocking logic.
                                         rameterized veriﬁcation, i.e. prove that the logic satisﬁes the                   In this paper, we investigate the use of a formal approach
                                         required properties for all the relevant stations. We present                  to ensure the reliability and integrity of their operations,
                                         a simpliﬁed case study, where the interlocking logic is di-                    as a complement to the standard validation and certiﬁca-
                                         rectly encoded in Dafny. Then, we show how to automate                         tion techniques. Our context is an ongoing activity of RFI
                                         the proof of an important safety requirement, by integrat-                     (the company managing the Italian railways network), aim-
                                         ing simple, template-based invariants and more complex in-                     ing to develop an in-house, framework to design interlock-
                                         variants obtained from a model checker for parameterized                       ing logics and support the development of interlocking sys-
                                         systems. Based on these positive preliminary results, we out-                  tems [3, 5]. One of the goals of this framework is to de-
                                         line how we intend to integrate the approach by extending                      velop a computer-based, in order to go beyond the current
                                         the IDE for the design of the interlocking logic.                              relay-based interlocking technology. Starting from a high-
                                                                                                                        level controlled natural language to describe the interlock-
                                         CCS Concepts: • Software and its engineering → Soft-                           ing logic, a model-based Integrated Development Environ-
                                         ware veriﬁcation; Model checking; System modeling lan-                         ment supports the railways signaling engineers in specify-
                                         guages.                                                                        ing the interlocking logic in a well-structured and semanti-
                                         Keywords: Veriﬁcation, Interlocking logic, Dafny                               cally unambiguous way. Interestingly, the interlocking logic
                                                                                                                        is generic in that it describes the procedures without speciﬁc
                                         ACM Reference Format:                                                          reference to a single, given station; rather, it applies to any
                                         Alessandro Cimatti, Alberto Griggio, and Gianluca Redondi. 2024.               station in a given class. The resulting speciﬁcation is then
                                         Towards the veriﬁcation of a generic interlocking logic: Dafny meets
                                                                                                                        translated into a SysML model, and from there compiled
                                         parameterized model checking. In Proceedings of ACM Conference
                                                                                                                        into executable code. Then, the user can deﬁne a speciﬁc
                                         (Conference’17). ACM, New York, NY, USA, 6 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn
                                                                                                                        station conﬁguration (e.g. the station of the city of Trento),
                                                                                                                        detailing the exact number of components and their interac-
                                         1 Introduction
                                                                                                                        tions. Upon conﬁguration, the code can be tested in a closed
                                         Interlocking systems are complex, safety-critical systems con-                 loop integration with a yard simulator modeling the behav-
                                         trolling the operation of the devices in a railway station. The                ior of trains and physical devices.
                                         main function is the creation of safe routes for trains from                      Formally verifying the interlocking logic is a very impor-
                                         diﬀerent points in the station. This requires that the devices                 tant goal, and several attempts have been made in this direc-
                                         insisting upon a given route (e.g. semaphores, switches, level                 tion [8, 9]. On the one side, we attempted to apply software
                                         Permission to make digital or hard copies of all or part of this work for
                                                                                                                        model   checking techniques on the code conﬁgured with re-
                                         personal or classroom use is granted without fee provided that copies are      spect  to a speciﬁc station. This approach hit a scalability
                                         not made or distributed for proﬁt or commercial advantage and that copies      barrier, due to the sheer size of the resulting, instantiated
                                         bear this notice and the full citation on the ﬁrst page. Copyrights for compo- model. Even more importantly, the results of the veriﬁcation
                                         nents of this work owned by others than ACM must be honored. Abstract-         would be applicable to a speciﬁc station only. On the other
                                         ing with credit is permitted. To copy otherwise, or republish, to post on
                                         servers or to redistribute to lists, requires prior speciﬁc permission and/or
                                                                                                                        side, we tried to tackle the problem of verifying the generic
                                         a fee. Request permissions from permissions@acm.org.                           interlocking logic without instantiating it with respect to
                                         Conference’17, July 2017, Washington, DC, USA                                  a speciﬁc station. We attempt to follow an SMT-based ap-
                                         © 2024 Association for Computing Machinery.                                    proach aiming at devising quantiﬁed invariants. This leads
                                         ACM ISBN 978-x-xxxx-xxxx-x/YY/MM. . . $15.00
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn
Conference’17, July 2017, Washington, DC, USA                                Alessandro Cimatti, Alberto Griggio, and Gianluca Redondi


to large and diﬃcult-to-reason-about formulae, due to the         Guards and eﬀects of a transition may read and or write the
lack of a proper structure.                                       value of variables of the objects in the list of the connected
   Based on these experiences, we are investigating an al-        components connected to the class.
ternative approach, that leverages the object-oriented fea-          The structured natural language used in the sheets has
tures of Dafny to obtain a high-level and natural framework       been designed to be comprehensible even to those not trained
where we tackle the veriﬁcation of generic interlocking log-      in formal languages and incorporates grammatical structures
ics. We present an artiﬁcial but representative case study,       drawn from domain-speciﬁc jargon. Phrases are structured
that shows how we intend to model the problem in Dafny            to ensure traceability to pertinent provisions and regulations.
and show how we verify some generic properties. We hint           For instance, an engineer might specify a transition guard
that automation in the veriﬁcation can be increased by com-       as follows: "Check that all the track segments of the routes
bining template-based generation of simple invariants and         are in a free state."
the use of a parameterized model checker to generate more            In AIDA, the sheets written in controlled natural language
complex, problem speciﬁc invariants. We believe that the          are associated with a number of syntactic and semantic checks
results are quite promising and that the approach is worth        and are translated into a SysML model. From the SysML
investigating further. We discuss the open challenges that        model, it is possible to extract graphical views of the FSM
we still need to solve to make this approach scalable.            for each class. Furthermore, the SysML can be compiled into
                                                                  executable code (Python and C).
2    Developing a Generic Interlocking Logic                         The IDE is complemented by two other tools: TOSCA and
                                                                  Norma. TOSCA implements a number of functions for the
In this section, we overview the approach for the develop-
                                                                  testing of the interlocking logic. It supports the speciﬁcation
ment of a generic interlocking logic [2, 3, 5]. The develop-
                                                                  of test scenarios, using a domain speciﬁc CNL sharing some
ment of the interlocking logic is model-based and starts from
                                                                  features with the CNL for the interlocking logic. Generic, ab-
a domain-speciﬁc controlled natural language (CNL), sup-
                                                                  stract scenarios may refer to any speciﬁc station and can be
ported by the tool AIDA. The interlocking logic is designed
                                                                  automatically instantiated on concrete scenarios. These can
through the creation of sheets, each deﬁning a logical en-
                                                                  then be run on the suitably instantiated software, in closed
tity, also referred to as a class. Examples of entities include
                                                                  loop with a simulator of the trains and trackside devices.
shunting routes, i.e. the high-level process devoted to cre-
                                                                  Automated test case generation oriented to coverage is also
ating a safe path for a train within the station, and lower
                                                                  supported.
level entities such as track segments, switches, level cross-
                                                                     Norma[2] is the tool for the formal analysis of legacy in-
ing, axal counters, and semaphores. Each sheet is divided
                                                                  terlocking systems based on relay technology. The role of
into two parts. The ﬁrst one deﬁnes the structure of the
                                                                  Norma is to extract formulae from the old designs and test
class, i.e. variables, parameters, and notably lists of other
                                                                  that the new speciﬁcations will reﬂect the behavior of the
components that are connected to the class. For example,
                                                                  older systems. The deﬁnition of a semantic correspondence
a shunting route will have lists of the entities it track seg-
                                                                  between the two interlocking technologies is nontrivial and
ments it insists upon, e.g. the track segments that must be
                                                                  relies on the deﬁnition of speciﬁc abstractions [4] to extract
locked before the green light is signaled.
                                                                  properties to be used in veriﬁcation.
   The second part of the sheet describes the behavior of the
                                                                     Within this comprehensive IDE, preliminary experiments
component, which can be thought of as an extended Finite
                                                                  in applying formal veriﬁcation have been attempted, aiming
State Machine. A distinguished state variable, taking values
                                                                  at proving safety properties of the generated C code. The
from an enumerative set, is used to deﬁne the current loca-
                                                                  tool leverages symbolic model-checking techniques for soft-
tion in the FSM. Each state transition is characterized by the
                                                                  ware veriﬁcation, with integration into the Kratos2 model
following elements:
                                                                  checker [11]. This approach, however, did not yield the ex-
    • Source and Destination;                                     pected results. On the one hand, even if the generation of C
    • Triggers, i.e. events that determine the ﬁring of a tran-   code is generic to all conﬁgurations, its subsequent veriﬁca-
      sition (e.g. the reception of a command from an exter-      tion can only take place once the conﬁguration of a speciﬁc
      nal operator, such as "create the route from entrance       station has been provided. This is necessary to meet the re-
      3 to platform 12");                                         strictions of Kratos2, that is unable to deal with objects of
    • Guards, i.e. the conditions that must be satisﬁed to        unspeciﬁed size. As a result, our current capability allows
      enable a particular transition. Determinism is ensured      us to assess the safety of individual stations with regard to
      by explicitly prioritizing guards;                          speciﬁc properties. Furthermore, the veriﬁcation of the C
    • Eﬀects: when a transition is executed, eﬀects are ap-       implementation of the interlocking logic conﬁgured for a
      plied that alter the internal state of the component,       given station incurs scalability problems, due to the large
      and possibly the state of components that are con-          number of components and their complex connections. For
      nected to it.
Towards the verification of a generic interlocking logic:
Dafny meets parameterized model checking                                                      Conference’17, July 2017, Washington, DC, USA

this goal, we could use the generic generated code as an in-      datatype TrackState = Init | Locked | Free
                                                                  datatype TrackDirection = Straight | Reverse
put for Kratos2, but the invariant generation engine of the
model checker is not able to synthesize the correct parame-
                                                                  class Track
terized invariants. Hence, in the rest of this paper, we tackle   {
the parameterized veriﬁcation of the generic interlocking             var state : TrackState
                                                                      var direction : TrackDirection
logic, without assuming that a speciﬁc station conﬁguration
is given.                                                             constructor (d : TrackDirection)
                                                                         ensures this.state =TrackState.Init
                                                                         ensures this.direction =d
                                                                      {
3    Dafny encoding                                                      state :=TrackState.Init;
                                                                         direction :=d;
The features of the Dafny language support a natural encod-           }
ing of the interlocking logic described in previous section.          method lock()
Moreover, the veriﬁcation in Dafny is modular, thus possi-               modifies this
                                                                         ensures this.state =Locked
bly reducing the complexity of the system to verify the sin-             ensures this.direction =old(this.direction)
gle components. We now illustrate a possible Dafny imple-             {
                                                                         this.state :=Locked;
mentation of a simple example, that has been designed to              }
be representative and comprehensive of all the constructs
                                                                      method go_free()
of the interlocking logic. In an ideal scenario, this Dafny              modifies this
code will be generated automatically from SysML within the               ensures this.state =Free
                                                                         ensures this.direction =old(this.direction)
IDE, complementing the generation of C and Python code.               {
Our example consists of a simple station with two kinds of               this.state :=Free;
                                                                      }
components: tracks, representing the track segments, and
routes, modeling the diﬀerent routes for the possible trains.         method change_dir()
                                                                         modifies this
   The track class has two variables: a state variable, and a            ensures this.state =old(this.state)
direction variable, that is used to simulate the presence of             ensures old(this.direction) ≠this.direction
                                                                      {
switches. Similarly, the routes have a state variable and a              if (this.direction =Straight)
Boolean one. In addition, each route is connected to a set                    {
                                                                                   this.direction :=Reverse;
of tracks (the ones used by the route), which should be in a                  }
particular direction.                                                    else {
                                                                              this.direction :=Straight;
   Regarding transitions, we consider for simplicity only one            }
simple method of the route class, that mirrors the transition         }
from an inactive state to an active one. The guard corre-         }
sponds to the condition ‘all the tracks of the route are in
a free state and in the requested direction’, and the eﬀect is
‘assign to all the tracks of the route the state locked’.                   Figure 1. Dafny encoding of the track class
   In the ﬁgures 1 and 2 we can see the two Dafny deﬁnitions
of the classes. We start by deﬁning variables, as we would
ﬁnd them in the initial segment of an AIDA sheet. Subse-
quently, the methods of the class model the transitions in
the second part of the AIDA sheet. The source and destina-        ‘activate route’ method. We suppose that we can generate
tion states, guards, and eﬀects of transitions are translated     such invariants automatically, without the need of an exter-
into a series of preconditions and postconditions for each        nal tool, as they reﬂect the structure of the generated code,
method. The body of each method is populated with a rep-          which is under our control.
resentation of the C code generated by AIDA.                         Lastly, we introduce the concluding segment of the Dafny
   We remark that, unlike the description of the AIDA sheet,      code designed for verifying the safety of the station, in ﬁg-
the formalization of the methods in Dafny introduces a "mod-      ure 3. Within this last code segment, we introduce the con-
iﬁes" clause. Additionally, we must explicitly include equal-     cept of a station, which is portrayed as a collection of routes
ities among variables that remain unchanged in the post-          and tracks. Subsequently, we deﬁne the station’s scheduler,
conditions. The initial challenge in automating Dafny code        a crucial element in the system. This scheduler nondeter-
generation lies in accurately representing these statements.      ministically selects a method that can be executed and pro-
   Up to this point, the veriﬁcation checks performed by          ceeds with its execution.
Dafny are focused on ensuring that the generated code com-           Additionally, we deﬁne the property that we seek to vali-
plies with the speciﬁed requirements. The only invariants         date, named "Secure Station," which corresponds to the prop-
required for this veriﬁcation occur in the while loop of the      erty ‘two incompatible routes cannot be active together’.
Conference’17, July 2017, Washington, DC, USA                                    Alessandro Cimatti, Alberto Griggio, and Gianluca Redondi


include "tracks.dfy"                                             include "tracks.dfy"
                                                                 include "routes.dfy"
datatype RouteState = Init | Active | Wait | Inactive
                                                                 class Station
class Route                                                      {
{                                                                    const routes : set<Route>
    var state : RouteState                                           const tracks : set<Track>
    var change_dir_request : bool
                                                                     ghost predicate ValidStation()
    const used : seq<Track>                                            reads this, this.routes
    const requested_dir : seq<TrackDirection>                        {
                                                                          ∧this.routes ≠{}
    ghost predicate ValidRoute()                                          ∧this.tracks ≠{}
       reads this                                                         ∧( ∀ i •i in this.routes =⇒
       {                                                                       ( ∃ j •j in this.tracks ∧j in i.used))
            |this.used| =|this.requested_dir|                             ∧( ∀ i, t •i in this.routes ∧
       }                                                                       t in i.used =⇒t in this.tracks)
                                                                          ∧∀ r •r in routes =⇒r.ValidRoute()
    constructor (u : seq<Track>, d : seq<TrackDirection>)            }
       requires |u| =|d|                                             ghost predicate NotCompatibleRoutes(a : Route,
       ensures this.state =RouteState.Init                                b : Route)
       ensures this.requested_dir =d                                      reads a, b
       ensures this.used =u                                          {
       ensures change_dir_request =false                                  (∃ i •(i in a.used) ∧(i in b.used)) ∧a ≠b
       ensures ValidRoute()                                          }
    {
       used :=u;                                                     ghost predicate SecureStation ()
       requested_dir :=d;                                                 reads this, this.routes
       state :=RouteState.Init;                                      {
       change_dir_request :=false;                                     ∀ i,j •(i in this.routes) ∧
    }                                                                     (j in this.routes) ∧(NotCompatibleRoutes(i,j))
                                                                          =⇒¬(i.state =Active ∧j.state =Active)
    method activateroute()                                           }
       modifies this, this.used[..]
       requires ValidRoute()                                         ghost predicate SecureInductiveStation()
       requires this.state =Wait                                        reads this, this.tracks, this.routes
       requires ∀ t •t in this.used =⇒t.state =Free                  {
       requires ∀ i •0 ≤ i < |this.used| =⇒                             this.SecureStation() ∧
          this.used[i].direction =this.requested_dir[i]                 ∀ r, t •(r in this.routes ∧t in this.tracks
       ensures ValidRoute()                                                    ∧t in r.used ∧t.state =Free)
       ensures this.state =Active                                                  =⇒¬(r.state =Active)
       ensures this.change_dir_request =                             }
          old(this.change_dir_request)
       ensures (∀ t •t in this.used                                  predicate Precondition(r : Route)
          =⇒t.state =Locked)                                             requires r.ValidRoute()
       ensures (∀ t •t in this.used                                      reads r, r.used
          =⇒t.direction =old(t.direction))                           {
       {                                                                 ∧( ∀ t •t in r.used
          var i :=0;                                                                          =⇒t.state =Free)
          while i < |this.used|                                          ∧( ∀ i •0 ≤ i < |r.used|
               modifies this.used[..]                                              =⇒r.used[i].direction =
               invariant 0 ≤ i ≤ |this.used|                                              r.requested_dir[i])
               invariant ∀ t •t in this.used[..i]                    }
                     =⇒t.state =Locked
               invariant ∀ t •t in this.used                         method StationScheduler()
                     =⇒t.direction =old(t.direction)                    modifies this.routes, this.tracks
          {                                                             requires ValidStation()
               this.used[i].lock();                                     requires SecureInductiveStation()
               i :=i + 1;                                               ensures ValidStation()
          }                                                             ensures SecureInductiveStation()
                                                                        decreases ∗
              this.state :=Active;                                   {
         }                                                              while true
}                                                                           modifies this.routes, this.tracks
                                                                            invariant ValidStation()
                                                                            invariant SecureInductiveStation()
                                                                            decreases ∗
             Figure 2. Dafny encoding of the route class                    {
                                                                                var r : | r in this.routes;
                                                                                match r.state {
                                                                                    case Init ⇒r.deactivate();
                                                                                    case Inactive ⇒r.requestroute();
   The loop of the scheduler tries to establish that the prop-                      case Wait ⇒if Precondition(r)
                                                                                               {r.activateroute();}
erty is preserved by each method. Notably, this preserva-                           case Active ⇒r.deactivateroute()}
tion is not true for the initial property itself, "Secure Sta-              }
                                                                     }
tion." However, the veriﬁcation succeeds when we provide
a stronger inductive invariant that implies the original prop-   }
erty - called "Secure Inductive Station".
                                                                              Figure 3. Dafny encoding of the station
Towards the verification of a generic interlocking logic:
Dafny meets parameterized model checking                                                    Conference’17, July 2017, Washington, DC, USA

  The goal of this project would be to use a parameterized            Then, we deﬁne
model checker to ﬁnd these inductive invariants automati-
cally.                                                                  𝑁𝑜𝑡𝐶𝑜𝑚𝑝𝑎𝑡𝑖𝑏𝑙𝑒 (𝑟 1,𝑟 2) ⇐⇒
                                                                            𝑟 1 ≠ 𝑟 2 ∧ ∃𝑡 : 𝑡𝑟𝑎𝑐𝑘.𝑈 𝑠𝑒𝑑𝑏𝑦(𝑡, 𝑟 1) ∧ 𝑈 𝑠𝑒𝑑𝑏𝑦(𝑡, 𝑟 2),
4     Invariant inference with a
                                                                      and the candidate property, represented by the formula:
      Parameterized Model Checker
Parameterized model checking is a veriﬁcation technique                 ∀𝑟 1, 𝑟 2 : 𝑟𝑜𝑢𝑡𝑒 𝑁𝑜𝑡𝐶𝑜𝑚𝑝𝑎𝑡𝑖𝑏𝑙𝑒 (𝑟 1, 𝑟 2) →
designed to assess whether a given property holds true for                                                                       
                                                                                   ¬(𝑠𝑡𝑎𝑡𝑒 [𝑟 1] = 𝑎𝑐𝑡𝑖𝑣𝑒 ∧ 𝑠𝑡𝑎𝑡𝑒 [𝑟 2] = 𝑎𝑐𝑡𝑖𝑣𝑒) .
all possible system conﬁgurations, making it particularly
valuable for systems with variable sizes or structures. This            using the (implementation of the) algorithm of [7], we can
approach allows for the analysis of system behavior, safety,          ﬁnd (in less than one second) the lemma
and correctness across a range of instances, providing a for-
                                                                        ∀𝑟 : 𝑟𝑜𝑢𝑡𝑒, 𝑡 : 𝑡𝑟𝑎𝑐𝑘 (𝑈 𝑠𝑒𝑑𝑏𝑦(𝑡, 𝑟 ) ∧ 𝑠𝑡𝑎𝑡𝑒 [𝑡] = 𝑓 𝑟𝑒𝑒)
mal framework for universal reliability. Unfortunately, with
the exception of a few cases, parameterized veriﬁcation is                                                  → (𝑠𝑡𝑎𝑡𝑒 [𝑟 ] ≠ 𝑎𝑐𝑡𝑖𝑣𝑒)
undecidable. Nonetheless, in the literature, there are various        which, in conjunction with the original property, is an induc-
approaches that can automatically synthesize invariants for           tive invariant for 𝑆. This is the same invariant as the ‘Secure
parameterized systems [1, 6, 7, 10]. In particular, the algo-         Inductive Station’ in the Dafny code of the station. It’s im-
rithm presented in [7] is an SMT-based algorithm for the              portant to highlight that the symbolic system 𝑆 represents a
veriﬁcation of parameterized systems. In that setting, un-            simpliﬁed version of the station. In this simpliﬁed example,
bounded components are modeled via a theory of a simple               both tracks and routes contain fewer variables compared to
type, and state variables are functions from such types to            their original counterparts.
other theories.                                                          This straightforward illustration portrays an ideal scenario
   Our goal is to use such a model checker to synthesize              where Dafny and a parameterized model checker seamlessly
automatically the inductive invariants that Dafny needs to            collaborate to arrive at a conclusive proof. Without Dafny,
conclude the proof. We illustrate the main concepts of SMT-           the typical approach would require monolithic use of the
based parameterized model checking continuing the last ex-            model checker, but this approach often struggles to scale ef-
ample. To formalize the whole system symbolically, we need            fectively when dealing with exceptionally large models.
to deﬁne a transition system 𝑆 = (𝑋, 𝐼 (𝑋 ),𝑇 (𝑋, 𝑋 ′ )), where
𝑋 is a set of variables, and 𝐼,𝑇 are formulas over some the-          5 Ongoing and Future Work
ory. A key insight here is that we do not need to represent
                                                                      We tackle the problem of formally verifying an interlock-
all the attributes of the class, but only the one relevant to
                                                                      ing logic expressed in a domain speciﬁc language. The main
building the inductive invariant. In this example, we have
                                                                      problem is that the logic is parameterized, in the sense that it
obtained this simpliﬁcation manually, by selecting the vari-
                                                                      is intended to control any station with an arbitrary number
ables that were more signiﬁcant. Ideally, such a selection
                                                                      of components. We preliminarily analyzed a highly simpli-
should be done automatically by some kind of slicing ab-
                                                                      ﬁed case study, with two main insights. First, we conﬁrm
straction, guided by domain-based intuitions.
                                                                      that it is possible to directly encode the main features of
   For this example, the only variables we need are two state
                                                                      the interlocking logic in Dafny in a very natural way. Sec-
variables, one with sort 𝑡𝑟𝑎𝑐𝑘 ↦→ {𝑓 𝑟𝑒𝑒, 𝑙𝑜𝑐𝑘𝑒𝑑 } and one
                                                                      ond, we investigate veriﬁcation and the relation to simple
with sort 𝑟𝑜𝑢𝑡𝑒 ↦→ {𝑎𝑐𝑡𝑖𝑣𝑒, 𝑖𝑛𝑎𝑐𝑡𝑖𝑣𝑒}. The initial formula of
                                                                      invariants (from predeﬁned schemata) and to more complex
the system is:
                                                                      invariants (resulting from the application of parameterized
∀𝑡 : 𝑡𝑟𝑎𝑐𝑘.(𝑠𝑡𝑎𝑡𝑒 [𝑡] = 𝑓 𝑟𝑒𝑒)∧∀𝑟 : 𝑟𝑜𝑢𝑡𝑒.(𝑠𝑡𝑎𝑡𝑒 [𝑟 ] = 𝑖𝑛𝑎𝑐𝑡𝑖𝑣𝑒).    model checker [7]).
                                                                         Given the successful preliminary steps, we intend to ex-
Moreover, we model the dependencies between a route and               tend the IDE for the Interlocking logic to support parame-
its associated tracks with a binary predicate 𝑈 𝑠𝑒𝑑𝐵𝑦 with            terized veriﬁcation. The ﬁrst step will be to devise an en-
sort 𝑟𝑜𝑢𝑡𝑒 × 𝑠𝑡𝑎𝑡𝑒 ↦→ 𝐵𝑜𝑜𝑙. The method ‘activate route’ can           coder to automatically generate Dafny code automatically
thus be modeled with the following formula:                           from SysML. We expect this step to be relatively simple,
                                                                      given that the interlocking logic constructs have a direct
    ∃𝑟 : 𝑟𝑜𝑢𝑡𝑒 𝑠𝑡𝑎𝑡𝑒 [𝑟 ] = 𝑖𝑛𝑎𝑐𝑡𝑖𝑣𝑒∧
                                                                      correspondence to Dafny ones, and back-and-forth trace-
       ∀𝑡1 : 𝑡𝑟𝑎𝑐𝑘 (𝑈 𝑠𝑒𝑑𝑏𝑦(𝑡1, 𝑟 ) → 𝑠𝑡𝑎𝑡𝑒 [𝑡1] = 𝑓 𝑟𝑒𝑒)∧            ability can be achieved. The Dafny code will incorporate
∧𝑠𝑡𝑎𝑡𝑒 ′ [𝑟 ] = 𝑎𝑐𝑡𝑖𝑣𝑒∧∀𝑠 : 𝑟𝑜𝑢𝑡𝑒 (𝑠 ≠ 𝑟 → 𝑠𝑡𝑎𝑡𝑒 ′ [𝑠] = 𝑠𝑡𝑎𝑡𝑒 [𝑠])   both the method bodies, mirroring the C and Python code,
       ∧ ∀𝑡 : 𝑡𝑟𝑎𝑐𝑘.(𝑈 𝑠𝑒𝑑𝑏𝑦(𝑡, 𝑟 ) → 𝑠𝑡𝑎𝑡𝑒 ′ [𝑡] = 𝑙𝑜𝑐𝑘𝑒𝑑            and the preconditions and postconditions, echoing the en-
                                                                      gineers’ natural language speciﬁcations. Second, we will in-
                   ∧ ¬𝑈 𝑠𝑒𝑑𝑏𝑦(𝑡, 𝑟 ) → 𝑠𝑡𝑎𝑡𝑒 ′ [𝑡] = 𝑠𝑡𝑎𝑡𝑒 [𝑡]) .
                                                               
                                                                      tegrate a way to express the properties to be proved, likely
Conference’17, July 2017, Washington, DC, USA                                               Alessandro Cimatti, Alberto Griggio, and Gianluca Redondi


leveraging the language for specifying the abstract scenar-                    [6] Alessandro Cimatti, Alberto Griggio, and Gianluca Redondi. 2021.
ios in the TOSCA environment [3]. Third, we will integrate                         Universal Invariant Checking of Parametric Systems with Quantiﬁer-
the generation of invariants required to show that the inter-                      free SMT Reasoning. In Automated Deduction – CADE 28, André
                                                                                   Platzer and Geoﬀ Sutcliﬀe (Eds.). Springer International Publishing,
locking logic satisﬁes the expected properties. On the one                         Cham, 131–147.
side, we will instrument the encoding to automatically gen-                    [7] Alessandro Cimatti, Alberto Griggio, and Gianluca Redondi. 2022.
erate "simple" invariants via templates, to check the compli-                      Veriﬁcation of SMT Systems with Quantiﬁers. In Automated Technol-
ance of the generated code to speciﬁcation. On the other, we                       ogy for Veriﬁcation and Analysis, Ahmed Bouajjani, Lukáš Holík, and
will integrate a parameterized model checker (and possibly                         Zhilin Wu (Eds.). Springer International Publishing, Cham, 154–170.
                                                                               [8] Alessandro Fantechi, Gloria Gori, Anne E. Haxthausen, and
other invariant generators) to infer invariants for general                        Christophe Limbrée. 2022. Compositional Veriﬁcation of Railway In-
safety properties of the interlocking logic.                                       terlockings: Comparison of Two Methods. In Reliability, Safety, and
   For the latter, we anticipate a more complex path. Param-                       Security of Railway Systems. Modelling, Analysis, Veriﬁcation, and Cer-
eterized model checkers are not designed for tackling large-                       tiﬁcation, Simon Collart-Dutilleul, Anne E. Haxthausen, and Thierry
                                                                                   Lecomte (Eds.). Springer International Publishing, Cham, 3–19.
scale problems. Hence, our plan is to utilize them on smaller
                                                                               [9] Alessio Ferrari and Maurice H. Ter Beek. 2022. Formal Methods in
abstractions derived from the code. After the abstraction is                       Railways: A Systematic Mapping Study. ACM Comput. Surv. 55, 4,
built, we are not interested in ﬁnding immediately an invari-                      Article 69 (nov 2022), 37 pages. https://doi.org/10.1145/3520480
ant: even if the parameterized model checker takes hours to                   [10] Silvio Ghilardi and Silvio Ranise. 2010. MCMT: A Model Checker
synthesize a good invariant, we would be satisﬁed. However,                        Modulo Theories. In Automated Reasoning, Jürgen Giesl and Reiner
                                                                                   Hähnle (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 22–29.
the most hard challenge will likely be ﬁnding the correct
                                                                              [11] Alberto Griggio and Martin Jonáš. 2023. Kratos2: An SMT-Based
abstractions. It could be possible to explore the notion of                        Model Checker for Imperative Programs. In Computer Aided Veriﬁca-
guiding this abstraction process with insights gained from                         tion, Constantin Enea and Akash Lal (Eds.). Springer Nature Switzer-
failed veriﬁcations. Extracting such insights from the Dafny                       land, Cham, 423–436.
veriﬁcation conditions may be arduous, as the formulae gen-
erated by Boogie might be cryptic. As a result, we think that
the design of the abstraction-reﬁnement loop should be con-
ducted outside the realm of Dafny.
   Furthermore, we do not dismiss the idea of a semi-automated
approach, where railway engineers can contribute lemmas
or provide guidance in the abstraction process, potentially
in controlled natural language.

References
 [1] Parosh Aziz Abdulla, A. Prasad Sistla, and Muralid-
     har Talupur. 2018.           Model Checking Parameterized Sys-
     tems.        Springer International Publishing, Cham, 685–725.
     https://doi.org/10.1007/978-3-319-10575-8_21
 [2] Arturo Amendola, Anna Becchi, Roberto Cavada, Alessandro Cimatti,
     Andrea Ferrando, Lorenzo Pilati, Giuseppe Scaglione, Alberto Tac-
     chella, and Marco Zamboni. 2022. NORMA: a tool for the analysis
     of Relay-based Railway Interlocking Systems. In Tools and Algorithms
     for the Construction and Analysis of Systems, Dana Fisman and Grigore
     Rosu (Eds.). Springer International Publishing, Cham, 125–142.
 [3] Arturo Amendola, Anna Becchi, Roberto Cavada, Alessandro Cimatti,
     Alberto Griggio, Giuseppe Scaglione, Angelo Susi, Alberto Tacchella,
     and Matteo Tessi. 2020. A Model-Based Approach to the Design, Veri-
     ﬁcation and Deployment of Railway Interlocking System. In Leverag-
     ing Applications of Formal Methods, Veriﬁcation and Validation: Appli-
     cations, Tiziana Margaria and Bernhard Steﬀen (Eds.). Springer Inter-
     national Publishing, Cham, 240–254.
 [4] Anna Becchi and Alessandro Cimatti. 2022. Abstraction Modulo Sta-
     bility for Reverse Engineering. In Computer Aided Veriﬁcation, Sharon
     Shoham and Yakir Vizel (Eds.). Springer International Publishing,
     Cham, 469–489.
 [5] Roberto Cavada, Alessandro Cimatti, Alberto Griggio, and Angelo
     Susi. 2023. A Formal IDE for Railways: Research Challenges. In Soft-
     ware Engineering and Formal Methods. SEFM 2022 Collocated Work-
     shops, Paolo Masci, Cinzia Bernardeschi, Pierluigi Graziani, Mario
     Koddenbrock, and Maurizio Palmieri (Eds.). Springer International
     Publishing, Cham, 107–115.
