                                                    Lightyear: Using Modularity to Scale BGP Control Plane
                                                                        Verification
                                                                Alan Tang                                                 Ryan Beckett                                Steven Benaloh
                                                                     UCLA                                                     Microsoft                                     Microsoft

                                                       Karthick Jayaraman                                                   Tejas Patil                                Todd Millstein
                                                                  Microsoft                                                   Microsoft                                       UCLA

                                                                                                                      George Varghese
                                                                                                                                 UCLA
arXiv:2204.09635v2 [cs.NI] 20 Sep 2023




                                         ABSTRACT                                                                                    causing a network outage. Many earlier techniques try to rem-
                                         Current network control plane verification tools cannot scale to                            edy this by verifying configurations against specified end-to-end
                                         large networks because of the complexity of jointly reasoning about                         network behavior. For instance, Minesweeper [4] models network
                                         the behaviors of all network nodes. We present a modular approach                           behavior using SMT constraints, ARC [10] and Tiramisu [1] use
                                         to control plane verification, where end-to-end network properties                          graphs, and Plankton [22] uses explicit-state model checking.
                                         are verified via a set of purely local checks on individual nodes                              These techniques provide strong guarantees, frequently reason-
                                         and edges. The approach targets verification of reachability prop-                          ing about network behavior over all possible external announce-
                                         erties for BGP configurations, and provides guarantees in the face                          ments and/or link failures. However, a key open problem is to scale
                                         of arbitrary external route announcements and, for some proper-                             these techniques to large networks. While these approaches attempt
                                         ties, arbitrary node/link failures. We have proven the approach                             to scale through various means, they are not efficient enough to
                                         correct and implemented it in a tool Lightyear. Experimentally                              be used today on large real-world networks such as the wide-area
                                         we show Lightyear scales dramatically better than prior control                             networks of hyperscalers.
                                         plane verifiers. Further, Lightyear has been used for six months                               This lack of scalability is fundamentally caused by a shared limi-
                                         to verify properties of a major cloud provider network containing                           tation of earlier approaches: they model and reason about network
                                         hundreds of routers and tens of thousands of edges, finding and                             behavior monolithically. They analyze the network configuration
                                         fixing bugs in the process. To our knowledge no prior control-plane                         and routing processes as a whole, exhaustively exploring all possi-
                                         verification tool has been shown to scale to that size and complexity.                      ble control-plane behaviors induced by the complex interactions
                                         Our modular approach also makes it easy to localize configuration                           among all configuration directives and protocols. As the size of
                                         errors and enables incremental re-verification.                                             the network grows, the number of possible network states grows
                                                                                                                                     exponentially, limiting their ability to scale. By contrast, verifica-
                                         CCS CONCEPTS                                                                                tion has scaled to large systems in other domains, like software or
                                         • Networks → Network reliability;                                                           hardware, through modular checking. In this style, subsystems (e.g.,
                                                                                                                                     a software function or hardware module) are verified independently
                                         KEYWORDS                                                                                    to meet local specifications (e.g., a precondition/postcondition pair)
                                         Network Verification, BGP, Modular Reasoning                                                that together imply a desired global property [11, 14, 21]. Prior
                                                                                                                                     work has used modularity to scale data-plane analysis [12], but
                                         ACM Reference Format:                                                                       modularizing control-plane verification is more challenging due to
                                         Alan Tang, Ryan Beckett, Steven Benaloh, Karthick Jayaraman, Tejas Patil,                   complex routing protocols and policies.
                                         Todd Millstein, and George Varghese. 2023. Lightyear: Using Modularity                         This paper presents a modular approach to network control
                                         to Scale BGP Control Plane Verification. In ACM SIGCOMM 2023 Conference
                                                                                                                                     plane verification. Like prior verifiers, Lightyear takes as input a
                                         (ACM SIGCOMM ’23), September 10, 2023, New York, NY, USA. ACM, New
                                                                                                                                     network’s configuration and a global property to verify. To ensure
                                         York, NY, USA, 14 pages. https://doi.org/10.1145/3603269.3604842
                                                                                                                                     the property, Lightyear additionally requires the user to provide
                                                                                                                                     local constraints that should hold on individual routers and edges.
                                         1     INTRODUCTION                                                                          Lightyear then automatically produces a set of local checks on
                                         Routing in networks today is controlled using low-level configura-                          individual nodes and edges that (1) verify the user’s local constraints
                                         tion on individual routers, which often leads to errors, potentially                        and (2) ensure that these constraints imply the given end-to-end
                                                                                                                                     property.
                                         Permission to make digital or hard copies of part or all of this work for personal or          We focus on BGP since it is ubiquitous and in many networks is
                                         classroom use is granted without fee provided that copies are not made or distributed       the most complex process that impacts the data plane’s forward-
                                         for profit or commercial advantage and that copies bear this notice and the full citation   ing behavior. Our approach targets two common classes of BGP
                                         on the first page. Copyrights for third-party components of this work must be honored.
                                         For all other uses, contact the owner/author(s).                                            reachability properties. First, safety properties on individual routers
                                         ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA                                      intuitively ensure that “bad” routes never reach a particular node.
                                         © 2023 Copyright held by the owner/author(s).                                               This includes common properties like filtering bogons, preventing
                                         ACM ISBN 979-8-4007-0236-5/23/09.
                                         https://doi.org/10.1145/3603269.3604842                                                     transit between peers, and ensuring isolation. Second, we target
ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA                                                                                  Tang et al.


liveness properties, which intuitively ensure that a “good” route
will eventually be accepted or forwarded at a particular location.                        Network           R1                   ISP1
This includes many control-plane reachability queries, for example
that a route received from one neighbor will be sent to another.
    Modularizing control-plane verification is challenging. Control                          R3
plane behavior depends on the interaction of complex configura-
                                                                                                            R2
tions with BGP, a distributed message-passing protocol. A classical
way to reason modularly about protocols is through invariants                                                                X
indexed by time [2], and/or employ temporal logic [17]. This re-                                                                 ISP2
quires significant effort and expertise. Instead, we demonstrate that                     Customer
                                                                                                                         ✓
in practice a wide range of desired properties can be modularly
verified without making time explicit. Reasoning modularly about
liveness properties is particularly challenging; it requires that the        Figure 1: Example network with safety and liveness properties
modular checks together imply an end-to-end path through the
                                                                             (shown intuitively by the purple arrows). Routes from ISP1 should
network. We describe a natural approach to ensure this using two
                                                                             not be sent to ISP2 (safety). Routes from Customer should reach ISP2
                                                                             (liveness).
kinds of constraints: path constraints that ensure the feasibility of a
"good" path, and no-interference invariants that ensure good paths
cannot be prevented.                                                            We used Lightyear to verify multiple properties for BGP in a
    We have formalized our approach to modular control plane veri-           large cloud provider’s wide-area network, which has hundreds of
fication, proved its correctness, and built a tool called Lightyear          routers and tens of thousands of BGP peerings. To our knowledge
based on it. Lightyear’s approach offers several advantages over             no prior verification tool that reasons about all possible external
the prior work, as summarized in Table 1:                                    route announcements has been demonstrated at this scale. We also
    Scalability: Lightyear performs a linear number of checks                ran tests on synthetic networks to show how well Lightyear scales.
in the network size (number of nodes and edges). Further, each                  In summary, we make the following contributions:
check depends only on the complexity of an individual node’s                    (1) Modularity: A novel solution to scaling control plane veri-
configuration. Prior approaches that reason about the joint behavior                fication by checking individual routers locally.
of all nodes’ policies scale at least quadratically, if not exponentially.      (2) Formalization: A formal model of BGP routing that we use
Lightyear’s local checks are also trivially parallelizable and enable               to prove correctness of the modular approach.
incremental re-checking when configurations change.                             (3) System: A tool Lightyear built using our approach, which
    Strong Guarantees: If all of Lightyear’s local checks are satis-                has been running in a hyperscaler for six months.
fied, then the specified network property is guaranteed to hold for             (4) Evaluation: A demonstration of Lightyear’s ability to scale
all possible external route announcements from neighbors. Further,                  to very large networks experimentally.
for safety properties our guarantees hold even in the presence of            This work does not raise any ethical issues.
arbitrary node or link failures, though this is not true in general
for liveness properties. As shown in the first two rows of the table,
                                                                             2   APPROACH OVERVIEW
of the prior work only Minesweeper [4] supports reasoning about              In this section we show how Lightyear works with the example in
both external route announcements and failures.                              Figure 1. In the example network, each edge represents a connection
    Localization: While prior approaches identify incorrect be-              between BGP speakers. The network contains three BGP routers:
havior, the resulting counterexample is global, making it difficult          R1, R2, and R3. R1 and R2 each have an ISP as an external neighbor.
to determine which router and policy is erroneous. By contrast, a            R3 is connected to an external neighbor that is a customer. The
local-check violation in Lightyear directly indicates the erroneous          network satisfies two properties. First, it satisfies the standard no-
router and policy.                                                           transit property that routes originating from ISP1 should not be
    Lightyear’s main tradeoff is that users must specify local con-          advertised to ISP2, and second, it satisfies the property that routes
straints. However, for networks designed in a modular and struc-             from Customer, with appropriate prefixes, should eventually be
tured fashion, only a few simple constraints are required for any            sent to ISP2. The former is a safety property, holding when a certain
desired end-to-end property. For example, network nodes are com-             event never occurs, and the latter is a liveness property, holding
monly partitioned into roles, such as border or core, each with its          when a event must eventually occur. Both are network-wide policies
own responsibilities; nodes in the same role will typically have the         in that they depend on the interaction of multiple routers to achieve
same local constraints.                                                      the correct result.
    In addition, the scalability and localization properties of our             Existing control-plane verifiers [1, 4, 10, 22, 24] would verify
tool make it easy for users to hypothesize an initial set of local           these properties by creating a representation of the possible data
constraints and then refine them iteratively based on feedback. We           planes that can result from the entire network’s configuration and
used this approach to produce the local constraints in our real-             then searching this representation for counterexamples. This joint
world experiments (see below), having brief discussions with the             representation of all network node behaviors has inherent scalabil-
network operators based on Lightyear’s feedback in order to either           ity limitations.
determine that an identified issue was a real configuration error or            However, we observe that network configurations are highly
to update our local invariants appropriately.                                structured and modular by design. Each router contains route maps
Lightyear: Using Modularity to Scale BGP Control Plane Verification               ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA


                                                                                             Plankton [22]       ARC [10]
                                                    Minesweeper [4]         BagPipe [24]
                                                                                             Tiramisu [1]       Hoyan [26]
        Tool Feature                                                                                                            Lightyear

        Analyzes all peer BGP routes                                                                #                #
        Analyzes failures                                                        #                                                    G
                                                                                                                                      #
        Checks safety and liveness properties                                    G
                                                                                 #
        Verification is fully automatic                                                                                               G
                                                                                                                                      #
        Near linear scaling with network size                #                   #                  #                #
        Localizes bugs in configurations                     #                   #                  #                #
                                    Table 1: Comparison of prior verification tools with Lightyear.


(also called route policies and route filters), which define an import            As shown in the first line of Table 2, the no-transit property
and export policy on each BGP peering session, determining which               specifies that no route transmitted over the edge from R2 to ISP2
routes are rejected, which are accepted, and how accepted routes               should originate at ISP1. To enable the expression of rich properties,
are transformed. Each route map plays a particular role in the assur-          Lightyear allows users to define ghost attributes that conceptually
ance of desired global properties. For example, in the network from            update message headers with additional fields. This is a common
Figure 1 the no-transit property can be ensured using a common                 technique in software verification, where additional variables are
approach based on communities: (1) R1’s import policy marks re-                introduced that do not affect the computation but allow for easier
ceived routes from ISP1 with a BGP community (a simple 32-bit tag)             property specification [9]. In the table, FromISP1(𝑟 ) is a boolean
with value 100:1 (2) R2’s export policy filters routes tagged with             ghost variable that is defined by the user to be false in all originated
100:1 when advertising to ISP2, and (3) no other import or export              routes, set to true by the import filter on R1 from ISP1, and left
policy strips community 100:1 from routes that it advertises.                  unchanged by all other filters.
    Note that each of the above behaviors is node-local and pertains              Network Invariants: Users must also specify invariants that
to an individual BGP route map. Unlike Lightyear, prior control                are true for routes at locations within the network. While in prin-
plane verification tools are not aware of this modular structure               ciple the user could specify a different invariant for each network
and so cannot leverage it. Alternatively, one could envision making            location, many locations play the same role in the network and have
a tool that simply performs a set of user-specified local checks               the same behavior with respect to the desired end-to-end property.
like the ones above. However, in that case there is no guarantee               In our example, there are only three network invariants, shown in
that together they imply the desired end-to-end property. Even in              Table 2, which correspond exactly to the three node-local behav-
this simple example, the fact that it is necessary to check the third          iors described earlier that ensure the no-transit property. First, no
condition above is subtle and easily missed.                                   assumption is made about the routes coming from ISP1 to R1, so
    Figure 2 shows the architecture of Lightyear. Like prior control-          the associated predicate is True. Second, routes coming from R2 to
plane verifiers, it takes as input the network configuration and an            ISP2 should not come from ISP1. Note that this invariant is identical
end-to-end property to verify. However, Lightyear requires the                 to the end-to-end property, which is common but need not be the
user to provide additional local constraints that capture the modular          case. Third, all other locations in the network should satisfy the
structure of the configurations. From these inputs Lightyear gen-              key correctness invariant: routes from ISP1 must be tagged with
erates a set of local checks on individual nodes in the network and            the community 100:1.
uses a constraint solver to verify each one. If all of these local checks         For many safety properties, like in the example above, invariants
succeed, then the end-to-end property is guaranteed to hold, for               follow a straightforward three-part structure. First, very little is
all possible external route announcements from neighbors and, for              assumed about routes coming from outside the network (so the
safety properties, for all possible link and node failures in the net-         associated local invariant is True or similarly nonrestrictive). Sec-
work. Otherwise, Lightyear provides concrete counterexamples                   ond, the desired global property should hold at the corresponding
for each failed local check.                                                   location in the network (the edge from R2 to ISP2 in the above
    In the rest of this section, we show how Lightyear modularly               example). Third, there is a key invariant that holds in the rest of
verifies the two properties for the network in Figure 1.                       the network, which intuitively describes how the network ensures
                                                                               the global property. In our example above, the invariant specifies
2.1    Safety Properties                                                       the fact that the network uses the community 100:1 to keep track
End-to-end Property: For safety properties, the end-to-end prop-               of the routes that came from ISP1. In general this invariant restricts
erty of interest is specified as a pair of a particular location in the        the routes that can flow through the network to be of a limited
network and a predicate on all routes reaching that location. Many             kind, for example a specific set of prefixes or containing specific
network policies fall into this class of properties, for example bogon         attribute values such as the MED, local preference or communities.
filtering; ensuring that a network only advertises routes to its own           Notably, this three-part decomposition is analogous to the modular
destinations; and forms of isolation between nodes or groups of                verification of software [11], which typically involves a precondi-
nodes. Such properties can also express complex constraints among              tion that is assumed to hold initially, a postcondition to be proven,
BGP attributes, for example that prefixes in a specific range always           and one or more inductive invariants that hold throughout each
have a particular local preference or MED value.                               execution and are sufficient to imply the postcondition.
ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA                                                                          Tang et al.


                           Inputs                                Lightyear                                Results


                         Network                                    Parse
                       Configurations                           Configurations                            Property
                                                                                     All Checks           Verified!
                          Property                                Generate              Pass
                        to be Verified                          Local Checks
                                                                                                      Counterexamples
                     Network Invariants,                            Run                               for Failed Checks
                      Path Constraints                          Local Checks        Some Checks
                                                                                       Fail


                                                  Figure 2: The architecture of Lightyear.

         Type                       Location(s)         Logical Formula          Description
         End-to-end Property        R2 → ISP2           ¬FromISP1(𝑟 )            No routes sent to ISP2 come from ISP1
                                    ISP1 → R1    True                     ISP1 can send our network any route
          Network Invariants        R2 → ISP2    ¬FromISP1(𝑟    )         No routes sent to ISP2 come from ISP1
                                    Nodes and other
                                                 FromISP1(𝑟 )
                                                                          Routes from ISP1 are tagged with community 100:1
                                    edges in network
                                                 ⇒ 100:1 ∈ Comm(𝑟 )
                                    ISP1 → R1     (True ∧ 𝑟 ′ = Import(ISP1 → R1, 𝑟 ))
                                                 ⇒ (FromISP1(𝑟 ′ ) ⇒ 100:1 ∈ Comm(𝑟 ′ ))
                              R2 → ISP2           ((FromISP1(𝑟 ) ⇒ 100:1 ∈ Comm(𝑟 )) ∧ 𝑟 ′ = Export(R2 → ISP2, 𝑟 ))
                                                 ⇒ ¬FromISP1(𝑟 ′ )
          Generated Checks    Other Edge 𝐸        ((FromISP1(𝑟 ) ⇒ 100:1 ∈ Comm(𝑟 )) ∧ 𝑟 ′ = Export(𝐸, 𝑟 ))
                                                 ⇒ (FromISP1(𝑟 ) ⇒ 100:1 ∈ Comm(𝑟 ))
                                                  ((FromISP1(𝑟 ) ⇒ 100:1 ∈ Comm(𝑟 )) ∧ 𝑟 ′ = Import(𝐸, 𝑟 ))
                                                 ⇒ (FromISP1(𝑟 ) ⇒ 100:1 ∈ Comm(𝑟 ))
Table 2: Using Lightyear to prove the no-transit property from Figure 1. The user-provided global property and local invariants
are show in blue. Lightyear-generated local verification checks are shown in yellow.
        Type                         Location(s)         Logical Formula          Description
        End-to-end Property          R2 → ISP2           HasCustPrefix(𝑟 )        Customer prefixes are advertised to ISP2
        Assumption                   Customer → R3       HasCustPrefix(𝑟 )        Assume customer routes are advertised to R3
                                     R3, R2,             HasCustPrefix(𝑟 )        Routes from customer are accepted/forwarded
        Path Constraints             R3 → R2             ∧¬ 100:1 ∈ Comm(𝑟 )      and not tagged with community 100:1
                                     R2 → ISP2           HasCustPrefix(𝑟 )        Routes are forwarded to ISP2
                                     Customer → R3       (HasCustPrefix(𝑟 ) ∧ 𝑟 ′ = Import(Customer → R3, 𝑟 ))
                                                         ⇒ (HasCustPrefix(𝑟 ′ ) ∧ ¬100:1 ∈ Comm(𝑟 ′ ))
                                                         ((HasCustPrefix(𝑟 ) ∧ ¬100:1 ∈ Comm(𝑟 )) ∧ 𝑟 ′ = Export(R3 → R2, 𝑟 ))
                                                         ⇒ (HasCustPrefix(𝑟 ′ ) ∧ ¬100:1 ∈ Comm(𝑟 ′ ))
        Propagation Checks           R3 → R2
                                                         ((HasCustPrefix(𝑟 ) ∧ ¬100:1 ∈ Comm(𝑟 )) ∧ 𝑟 ′ = Import(R3 → R2, 𝑟 ))
                                                         ⇒ (HasCustPrefix(𝑟 ′ ) ∧ ¬100:1 ∈ Comm(𝑟 ′ ))
                                     R2 → ISP2           ((HasCustPrefix(𝑟 ) ∧ ¬100:1 ∈ Comm(𝑟 )) ∧ 𝑟 ′ = Export(R2 → ISP2, 𝑟 ))
                                                         ⇒ HasCustPrefix(𝑟 ′ )
         No-interference Checks R3, R2            HasCustPrefix(𝑟 )      Routes accepted at R3 and R2 with a customer
         (Safety Properties)                      ⇒ ¬100:1 ∈ Comm(𝑟 ) prefix must not have community 100:1
Table 3: Using Lightyear to prove the liveness property from Figure 1. The user-provided global property, and path constraints
are show in blue. The propagation checks are shown in yellow for the path is Customer → R3 → R2 → ISP2. The no-interference
checks are safety properties proven using their own invariants (not shown).
Lightyear: Using Modularity to Scale BGP Control Plane Verification                     ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA


    Importantly, these local invariants are far from complete specifi-               network and predicate. However, here the predicate indicates that
cations of the network’s routing behavior. Rather, local invariants                  a route satisfying the property will eventually reach that location.
need only describe the constraints on routes that are necessary                      The property in Table 3 shows that a route with a customer prefix
to ensure the particular global property of interest. For example,                   will eventually be sent from R2 to ISP2. If the routes of interest
suppose that our example network uses a route’s local preference                     come from a neighbor, as in this case, then the property will only be
value to choose among multiple routes to a destination. Since the                    provable under the assumption that the neighbor advertises such a
local preference values don’t pertain to our no-transit property, this               route. Users can optionally specify such an assumption, as shown
behavior need not be specified.                                                      in the table.
    Generated Checks: Given the invariants provided from the                            Path and Constraints: As with safety properties, users need to
user, Lightyear automatically generates local checks to validate                     provide a set of local constraints on individual network locations,
the given network invariants. Importantly, each local check per-                     but they take a different form for liveness properties. Users must
tains to a single BGP filter on a single network router, applied to                  provide a path through the network that the desired route can
messages from a specific neighbor. Together these checks imple-                      take to reach the destination from the source, along with local
ment a form of assume-guarantee reasoning [14, 21]: each location’s                  constraints for each edge and node along the path. The path does
network invariant is proven under the assumption that the network                    not need to be unique. Intuitively, each local constraint indicates
invariants of its directly connected locations hold. As we prove                     the properties of the "good" routes that will reach that particular
later, together these checks imply that all local invariants in the                  location, and together they constitute a witness that a "good" route
network are respected.                                                               will eventually reach its intended destination. As shown in Table 3,
    Table 2 shows the local checks that Lightyear automatically                      our example has two path constraints: at locations R3, R2, and R3
generates for our running example. The first check ensures that the                  → 𝑅2 there will eventually be a route with the customer prefix that
import filter at R1 on the edge from ISP1 to R1 establishes the key                  does not have the community 100:1, and at R2 → ISP2 there will
invariant FromISP1(𝑟 ) ⇒ 100:1 ∈ Comm(𝑟 ). Since that filter tags                    eventually be a route with the customer prefix. It is important that
all routes with community 100:1, the check is easily provable by a                   routes from Customer do not have the community 100:1, or else
constraint solver. The second check ensures that the key invariant                   they will be dropped at R2, due to the way that the earlier no-transit
is sufficient to ensure that routes from ISP1 are not exported on                    property is ensured. As described earlier, the local and concrete
the edge from R2 to ISP2. Since the export filter at R2 on that edge                 feedback from Lightyear can be used iteratively to identify these
drops all routes that are tagged with 100:1, the check passes. The                   conditions.
third set of checks ensure that the key invariant is preserved by all                   Propagation Checks: In order to prove the liveness property
other import and export filters in the network. Since these filters                  two types of checks need to be performed. First, there are local
never strip community 100:1 from a route, the checks pass.1 Lastly                   checks that together imply that a route will in fact traverse the given
(not shown in the table), Lightyear must check that the invariant                    path, in the absence of interference from other possible paths. These
on the edge from R2 to ISP2 implies the end-to-end property. This                    checks are analogous to the generated checks for safety properties
check is trivial since the two properties are identical.                             shown earlier. Notably, in order for the first propagation check in
    Output: If the configuration contains errors, Lightyear returns                  Table 3 to be satisfied, the import policy at R3 must not accept any
a counterexample for each local check that did not pass. In our                      routes tagged with community 100:1. One way to ensure this is
example, suppose that R1’s import filter accidentally does not add                   for the policy to strip communities from all accepted routes. The
the community 100:1 for some routes received from ISP1. In that                      other two checks are straightforward.
case, the first generated check in Table 2 would fail, producing a                      No-interference Checks: Finally, liveness properties require
counterexample consisting of a concrete route that is accepted by                    an additional set of checks. Since BGP only selects the best route
R1 but does not get the community 100:1 added to it. This coun-                      available from all of a router’s neighbors, it is not enough to show
terexample directly indicates the route policy that is responsible                   that filters do not reject "good" routes along our path. It is also
for the error and concretely illustrates the specific local property                 necessary to show that other routes in the network can never
that was violated. Counterexamples from Lightyear are also be                        interfere, at any node along the path. To do this, we also check
helpful in refining local invariants that are not precisely known in                 that any route with the same prefix as a "good" route that can be
the beginning. For example, a user might write a local invariant for                 accepted by a node on the path is also "good" — it also satisfies the
some network location but forget to account for a specific corner                    corresponding path constraint. For our example, at R3 and R2, routes
case. In that case Lightyear will identify an “error" due to a failed                with a customer prefix are checked to never have the community
local check, and the associated counterexample informs the user                      100:1. This constraint ensures that if routes for customer prefixes
how to refine that local invariant to more closely match the network                 arrive along other paths and are preferred to those arriving on our
location’s behavior.                                                                 path, those routes will still satisfy the desired property (i.e., they
                                                                                     will be sent from R2 to ISP2). Note that this means that our approach
2.2      Liveness Properties                                                         does not require that the specified path be unique in the network,
End-to-end Property: For liveness properties, the end-to-end                         so we can verify liveness properties even in some scenarios where
property of interest is also a pair of a particular location in the                  there is routing redundancy. The no-interference constraint is itself
                                                                                     a safety property, and so in general it must be proven using the
1 There are also some analogous checks for originated routes, but they are omitted   machinery shown in the previous subsection, with its own set of
here for simplicity.                                                                 local invariants (not shown in the table).
ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA                                                                               Tang et al.


    Output: As in the previous example, Lightyear returns a con-          Let Routes denote the set of all routes. We will use Comm(𝑟 ) to
crete counterexample for each failed propagation check and no-            refer to the Comm field of the route 𝑟 , Prefix(𝑟 ) to refer the prefix
interference check. For example, if R3’s import policy does not           of 𝑟 , and so on. Real BGP messages contain a few other attributes
properly strip the community 100:1 from accepted routes, then             as well, which could be incorporated into this model. Routes can
Lightyear will produce a concrete example illustrating this fact,         also be extended with additional “ghost” attributes, such as the
allowing the user to easily understand and localize the error.            FromISP1 attribute from Section 2. This is described in Section 4.4.
    In summary, Lightyear’s approach to control-plane verification           We model the BGP network policy as consisting of three func-
leverages the modular structure that is already present in the net-       tions, which can be derived from the BGP and route-map configu-
work configurations. By requiring the user to make this structure         rations of each router:
explicit through a set of local invariants at each location, Lightyear        (1) Import : Edges × Routes → Routes ∪ {Reject}
soundly reduces checking an end-to-end network property to a set              (2) Export : Edges × Routes → Routes ∪ {Reject}
of checks that each pertain to a single BGP import or export filter.          (3) Originate : Edges → P(Routes)
We formalize our approach and prove its correctness in Sections 4         The first two correspond to the import and export route maps
and 5.                                                                    which are defined in the router configurations. The third models the
    This approach has numerous benefits over the prior, monolithic        router’s ability to advertise static routes or routes from other proto-
approaches. First, our approach is highly scalable, since the number      cols into BGP. For an edge 𝐴 → 𝐵 and a route 𝑟 , Import(𝐴 → 𝐵, 𝑟 )
of checks is linear in the number of edges in the BGP network             either returns the route produced when applying the import fil-
graph. Second, Lightyear’s modular checks provide a very strong           ter at 𝐵 to the route 𝑟 sent from 𝐴 or returns Reject if the im-
guarantee. For both safety and liveness properties, the approach          port filter rejects the route. Export(𝐴 → 𝐵, 𝑟 ) either returns the
handles all possible external route announcements from neighbors.         route produced when applying the export filter at 𝐴 to the route
For safety properties, it additionally provides resilience to arbitrary   𝑟 sent to 𝐵 or returns Reject if the export filter rejects the route.
failures "for free," since it proves that "bad" routes are not received   Originate(𝐴 → 𝐵) returns the set of routes that are originated at
without making any assumptions about the paths that they might            𝐴 and sent to 𝐵.
traverse. Third, the modular approach naturally supports incre-
mental verification when a node is updated: only the local checks         3.2    BGP Traces
pertaining to that node must be re-checked. Finally, modularity has
large benefits for error localization and understanding: the failure      We model the semantics of BGP as a set of allowed traces. Our
of a local check directly pinpoints the erroneous import or export        semantics is a variant of that from the Bagpipe tool [24].
filter and the local invariant that it fails to satisfy.                     A trace is a sequence of events. There are three types of events
                                                                          that we consider: recv, slct, and frwd. For 𝑟 ∈ Routes, 𝑅 and 𝑁 ∈
3     FORMAL MODEL OF BGP                                                 Routers, and 𝑁 → 𝑅 and 𝑅 → 𝑁 ∈ Edges:
In this section we define a model of BGP in terms of traces and              (1) recv(𝑁 → 𝑅, 𝑟 ) occurs when 𝑅 receives route 𝑟 from neigh-
axioms on traces. This model is used in the next two sections to                 bor 𝑁
make Lightyear’s approach precise and to prove its correctness.              (2) slct(𝑅, 𝑟 ) occurs when 𝑅 selects 𝑟 as the best route for a
                                                                                 destination and installs it
3.1    BGP Topologies and Policies
                                                                             (3) frwd(𝑅 → 𝑁 , 𝑟 ) occurs when 𝑅 forwards route 𝑟 to the
We model a network’s BGP configuration as consisting of two parts:               neighbor 𝑁
a topology and a policy. A BGP network topology is a tuple of the         We denote the set of all traces as Traces.
form (Routers, Externals, Edges), where:                                     A valid trace is one that could occur for a given topology and
   (1) Routers is the set of routers for which the user provides          policy, according to the BGP semantics. We formalize the notion
       configurations.                                                    of trace validity as a set Valid ⊆ Traces of traces that satisfy
   (2) Externals is the set of external routers. That is, there is no     specific properties. We consider a trace to be valid, and hence part
       provided configuration, but each such router is an eBGP or         of the set Valid, if it satisfies a set of safety axioms, and a set
       iBGP peer with at least one router in Routers.                     of liveness axioms. These axioms are stated in Appendix A. The
   (3) Edges is the set of directed edges corresponding to BGP            safety axioms are used to prove the correctness of safety checks
       peering sessions.                                                  and state necessary conditions for an event to be in the trace. For
The network topology forms a graph with Routers ∪ Externals               example, if a slct event is in the trace, then there must be a recv
as the set of nodes and Edges as the set of edges. We will use the        event earlier and Import must have transformed the received route
notation 𝐴 → 𝐵 to refer the directional edge (𝐴, 𝐵) in the topology.      into the selected route. The liveness axioms are used to prove the
   A BGP route (or route advertisement) is modeled as a tuple             correctness of liveness checks and state sufficient conditions to
        (Prefix, ASPath, NextHop, LocalPref, MED, Comm)                   show that an event occurs later in the trace. For example, if a slct
where:                                                                    event occurs, then the result of Export applied to the selected route
   (1) NextHop, LocalPref, and MED are integer values                     will be used in a fwrd event.
   (2) Prefix is a pair consisting of an IP address and a length, both       In our model, external neighbors can send different announce-
       of which are integer values                                        ments in different traces, and events at different locations can occur
   (3) ASPath and Comm are lists of integer values representing           in any order.
       the BGP path and the community tags, respectively.
Lightyear: Using Modularity to Scale BGP Control Plane Verification        ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA


4     SAFETY VERIFICATION IN LIGHTYEAR                                  its local invariant. If the router 𝐵 is external then the import check
In this section, we describe Lightyear’s approach for modularly         is not performed, and similarly if the router 𝐴 is external then the
verifying safety properties and prove its correctness.                  export and originate checks are not performed. In our implemen-
                                                                        tation of Lightyear, the local checks are performed by modeling
4.1    Inputs for Safety Checks                                         import and export filters using SMT constraints and invoking an
Lightyear requires three inputs from the user in order to check         SMT solver to validate each check or provide a counterexample.
safety properties. The first input, the network configurations, is          Finally, Lightyear checks that the network invariants 𝐼 imply
standard. As described previously, the configurations are used to       the network property (ℓ, 𝑃). This is done simply by requiring that
build the BGP topology as well as the policy functions.                 𝐼 ℓ ⊆ 𝑃, i.e. that the network invariant for ℓ implies the network
    The second input is the network safety property, which requires     property 𝑃. Again this check is performed with an SMT solver.
that all route announcements that can reach a particular location       4.3    Correctness
satisfy certain constraints. Formally, a network safety property is a
pair (ℓ, 𝑃) where:                                                      We have proven the correctness of our approach to modular safety
               (ℓ, 𝑃) ∈ (Routers ∪ Edges) × P(Routes)                   verification.
Here ℓ is a location, either a router or an edge, and 𝑃 is a set of         Theorem: Given a BGP topology and policy, a network property
routes matching a particular constraint. In practice, users directly    (ℓ, 𝑃), and network invariants 𝐼 , let 𝐶 be the set of Import, Export,
specify a logical constraint on route attributes that represents 𝑃.     and Originate checks that Lightyear generates. If all checks in
    Each safety property (ℓ, 𝑃) corresponds to a property of all pos-   𝐶 pass and 𝐼 ℓ ⊆ 𝑃, then for all 𝑇 ∈ Valid, 𝑟 ∈ Routes, 𝑅, 𝑁 ∈
sible valid traces, as defined in the previous section — all routes     Routers:
that can reach location ℓ must satisfy 𝑃. Formally, a network sat-           • if ℓ = 𝑅 and slct(𝑅, 𝑟 ) ∈ 𝑇 , then 𝑟 ∈ 𝑃
isfies a property (ℓ, 𝑃) if for all 𝑇 ∈ Valid, 𝑟 ∈ Routes, 𝑅, 𝑁 ∈            • if ℓ = 𝑅 → 𝑁 and frwd(𝑅 → 𝑁 , 𝑟 ) ∈ 𝑇 ∨ recv(𝑅 → 𝑁 , 𝑟 ) ∈
Routers, 𝑅 → 𝑁 ∈ Edges:                                                         𝑇 , then 𝑟 ∈ 𝑃
      • if ℓ = 𝑅 and slct(𝑅, 𝑟 ) ∈ 𝑇 , then 𝑟 ∈ 𝑃                       Proof: See Appendix B.
      • if ℓ = 𝑅 → 𝑁 and frwd(𝑅 → 𝑁 , 𝑟 ) ∈ 𝑇 ∨ recv(𝑅 → 𝑁 , 𝑟 ) ∈
                                                                        4.4    Ghost Attributes
        𝑇 , then 𝑟 ∈ 𝑃
For example, the combination of the location (𝑅1 → 𝑅2) and con-         To increase Lightyear’s expressiveness, users can define ghost
straint 1:1 ∈ Comm(𝑟 ) together specify the property that if the        attributes, which conceptually extend each route with additional
event frwd(𝑅1 → 𝑅2, 𝑟 ) or the event recv(𝑅1 → 𝑅2, 𝑟 ) are in a         fields. For example, the FromISP1(𝑟 ) ghost attribute from Section 2
valid trace, then 𝑟 should always have the community 1:1.               is used to indicate whether 𝑟 originated from ISP1. A ghost attribute
    Finally, Lightyear’s third input is a set of network invariants,    is defined by specifying the set of values that the attribute can
one per location in the given network. Formally, the network in-        take, along with updates to the Import, Export, and Originate
variants are modeled as a set of pairs denoted 𝐼 :                      functions that make up the given network’s policy (Section 3.1).
                 𝐼 ⊆ (Routers ∪ Edges) × P(Routes)                          In the case of FromISP1(𝑟 ) from Figure 1, it can be defined as a
Each element of the set has the form (ℓ, 𝑃), where ℓ is a location      boolean attribute with the following behavior:
and 𝑃 is a set of routes, as in the network property defined above.           • the import filter on ISP1 → R1 sets FromISP1 to true
The semantics of each pair is a property of traces, analogous to the          • the import filters on ISP2 → R2 and Customer → R3 set
semantics of network properties shown above.                                    FromISP1 to false
    We require that there exist exactly one pair in 𝐼 per location in         • other filters leave FromISP1 unchanged
the given network, and we use the notation 𝐼 ℓ to denote the set 𝑃 of         • all originated routes have FromISP1 set to false
routes associated with location ℓ in 𝐼 . We also require that 𝐼𝑅→𝑁 =        Other natural network properties can be expressed using ghost
Routes for each edge 𝑅 → 𝑁 where 𝑅 ∈ Externals. In other                attributes. For example, a WaypointR attribute that is true only for
words, we make no assumption about routes coming from external          routes processed by a particular router 𝑅 can be defined by specify-
neighbors but rather assume that any route may be advertised.           ing that filters on 𝑅 set WaypointR to true, origination as well as im-
                                                                        port filters from external neighbors at other routers set WaypointR
4.2    Local Checks                                                     to false, and all other filters in the network leave WaypointR un-
Given the network configuration, network property (ℓ, 𝑃), and net-      changed.
work invariants 𝐼 , Lightyear generates the following local checks          Ghost attributes do not affect the description of Lightyear or
for each edge 𝐴 → 𝐵 in the network topology, which validate each        proof of its correctness above, as they do not depend on the specific
location’s network invariant using assume-guarantee reasoning:          set of attributes that are in a route.
   (1) Import: For all 𝑟, 𝑟 ′ ∈ Routes, if 𝑟 = Import(𝐴 → 𝐵, 𝑟 ′ )
       and 𝑟 ′ ∈ 𝐼𝐴→𝐵 , then 𝑟 = Reject ∨ 𝑟 ∈ 𝐼𝐵 .                      4.5    Fault Tolerance for Safety Properties
   (2) Export: For all 𝑟, 𝑟 ′ ∈ Routes, if 𝑟 = Export(𝐴 → 𝐵, 𝑟 ′ )      A significant benefit of Lightyear’s approach to control-plane
       and 𝑟 ′ ∈ 𝐼𝐴 , then 𝑟 = Reject ∨ 𝑟 ∈ 𝐼𝐴→𝐵 .                      verification of safety properties is that it supports reasoning about
   (3) Originate: For all 𝑟 ∈ Routes, if 𝑟 ∈ Originate(𝐴 → 𝐵),          failures “for free.” That is, if all of Lightyear’s checks pass, then
       then 𝑟 ∈ 𝐼𝐴→𝐵 .                                                  the given network property is guaranteed to hold not only in the
For example, the first check verifies that the import route map at      failure-free case but also in the presence of arbitrary node and link
𝐵 on the edge 𝐴 → 𝐵 satisfies 𝐼𝐵 , assuming that 𝐴 → 𝐵 satisfies        failures.
ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA                                                                                Tang et al.


   Lightyear soundly reasons about failures because of our over-            If ℓ𝑖 = 𝑅 ∈ Routers, then:
approximate notion of trace validity (Section 3.2 and Appendix A).                           𝐶𝑖 (𝑟 ) ∧ 𝑟 ′ = Export(𝑅 → 𝑁 , 𝑟 )
Specifically, any trace that is feasible according to the given BGP                           =⇒ 𝑟 ′ ≠ Reject ∧ 𝐶𝑖+1 (𝑟 ′ )
topology and passes the import and export filters along the cor-            and if ℓ𝑖 = 𝑅 → 𝑁 ∈ Edges, then:
responding path is considered valid. Hence, every trace that can                             𝐶𝑖 (𝑟 ) ∧ 𝑟 ′ = Import(𝑁 → 𝑅, 𝑟 )
occur under any failure scenario is already considered valid. By our
                                                                                                  =⇒ 𝑟 ′ ≠ Reject ∧ 𝐶𝑖+1 (𝑟 ′ )
correctness theorem, all of these traces satisfy the property (ℓ, 𝑃).          No interference: Next, we need to verify that it is not possible
                                                                            for a router along the path to select a "bad" route with the same
5     LIVENESS VERIFICATION IN LIGHTYEAR                                    prefix as a "good" route. Let Prefix(𝐶𝑖 ) refer the set of prefixes
We now describe how Lightyear checks liveness properties modu-              with at least one route in 𝐶𝑖 :
larly. Proving liveness properties modularly is more difficult than                               {𝑝 | 𝑝 = Prefix(𝑟 ) ∧ 𝑟 ∈ 𝐶𝑖 }
proving safety properties, since it requires showing both that "good"       Then at each router ℓ𝑖 along the path we must prove the following
routes are allowed and that interfering routes are not.                     safety property:
                                                                                          (ℓ𝑖 , Prefix(𝑟 ) ∈ Prefix(𝐶𝑖 ) =⇒ 𝐶𝑖 (𝑟 ))
5.1    Inputs for Liveness Checks                                           These properties can be proven using our existing approach for
                                                                            proving safety properties (Section 4), given appropriate local in-
The inputs for a liveness check consist of the following:                   variants.
    (1) The network configurations                                             Implying the network property: The above checks ensure
    (2) A liveness property (ℓ, 𝑃) ∈ {Routers∪Edges}×P(Routes)              that all of the local 𝐶𝑖 constraints in fact hold. Finally, Lightyear
    (3) A path (ℓ1, . . . , ℓ𝑛 = ℓ) where ℓ𝑖 ∈ {Routers ∪ Edges}            generates a local check that 𝐶𝑛 ⊆ 𝑃, similar to the analogous check
    (4) A constraint 𝐶 1 . . . 𝐶𝑛 for each location in the path, where      for safety properties, to ensure that the local constraints imply the
        𝐶𝑖 ∈ P(Routes)                                                      desired end-to-end liveness property.
The property (ℓ, 𝑃) represents a liveness property of all valid traces,
namely that there will eventually be a route at ℓ that satisfies 𝑃.
                                                                            5.3    Correctness
Formally, this means for all 𝑇 ∈ Valid, either:                             We have proven the correctness of our approach to modular safety
      • ℓ ∈ Routers and there exists 𝑟 ′ such that slct(ℓ, 𝑟 ′ ) ∈ 𝑇        verification.
        and 𝑃 (𝑟 ′ ) holds, or                                                 Theorem: Given the following:
      • ℓ ∈ Edges and there exists 𝑟 ′ such that frwd(ℓ, 𝑟 ′ ) ∈ 𝑇 and           • The network configurations
        𝑃 (𝑟 ′ ) holds                                                           • A liveness property (ℓ, 𝑃)
    The path (ℓ1, ℓ2, . . . , ℓ𝑛−1, ℓ𝑛 = ℓ) is a sequence of routers and         • A path 𝑆 = (ℓ1, ℓ2, . . . , ℓ𝑛−1, ℓ𝑛 = ℓ)
edges that we expect the route to travel across. We require that it              • A constraint for each location 𝐶 1 . . . 𝐶𝑛
represents an actual topological path in the network: if ℓ𝑖 = 𝑅 ∈           For all valid traces 𝑇 , if all of the following are true:
Routers then for some 𝑁 , ℓ𝑖+1 = 𝑅 → 𝑁 , and if ℓ𝑖 = 𝑅 → 𝑁 ,                   (1) all checks (propagation, no interference) pass
then ℓ𝑖+1 = 𝑁 . For example, ISP1 → R1, R1, R1 → R3, R3, R3 →                  (2) there exists 𝑟 such that recv(ℓ1, 𝑟 ) ∈ 𝑇 ∧ 𝐶 1 (𝑟 )
Customer is a path in the network from Figure 1. The last location             (3) 𝐶𝑛 ⊆ 𝑃
ℓ𝑛 must be the location ℓ of the end-to-end property that we are               (4) there are no link failures along the path
verifying.                                                                  then there exists 𝑟 ′ such that either:
    The constraints 𝐶 1 . . . 𝐶𝑛 are properties that represent the set of        • ℓ ∈ Routers and there exists 𝑟 ′ such that slct(ℓ, 𝑟 ′ ) ∈ 𝑇
"good" routes that reach each ℓ𝑖 along the path. They play a role                   and 𝑃 (𝑟 ′ ) holds, or
analogous to the local invariants 𝐼 ℓ𝑖 for proving safety properties,            • ℓ ∈ Edges and there exists 𝑟 ′ such that frwd(ℓ, 𝑟 ′ ) ∈ 𝑇 and
described earlier. The property 𝐶 1 for the first location in the path             𝑃 (𝑟 ′ ) holds
is simply assumed to hold; in practice it is usually an edge coming         Proof: See Appendix C.
from an external router, in which case it is not possible to prove.         Notably, the correctness only depends on there being no link failures
Rather, the best we can do is prove that if that router sends a "good"      along the given path, so the property holds even if there are failures
route, then it will eventually reach its intended destination in the        elsewhere.
network.
                                                                            6     EVALUATION
5.2    Local Checks
                                                                            6.1    Cloud WAN
The checks for liveness can be broken up into two parts: checks             We used Lightyear to modularly verify properties of the wide-area
that prove propagation along the given path, and checks that prove          network (WAN) of a major cloud provider, containing hundreds
there is no interference from outside routes.                               of routers and tens of thousands of peering sessions. In doing so,
   Propagation along a path: These checks are analogous to the              we show that: (1) important behavioral properties in real-world
local checks performed for safety verification, but they are only           networks can be expressed in Lightyear; (2) these properties can
checked along the given path. Together they ensure that the import          be proven through a combination of modular checks; (3) this ap-
and export filters along the path (ℓ1, . . . , ℓ𝑛 ) do not drop "good"      proach scales, allowing properties to be verified quickly; and (4) if
routes. Specifically, for all valid traces 𝑇 and 𝑖 < 𝑛:                     a local check does not succeed, it produces actionable information,
Lightyear: Using Modularity to Scale BGP Control Plane Verification          ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA

         Type             Locations (𝑙)       Logical Formula (𝐼𝑙 )       Description
         End-to-end       Any R in            𝐹𝑟𝑜𝑚𝑃𝑒𝑒𝑟 (𝑟 ) =⇒
                                                                          Bogon prefixes from peers should not be accepted
         Property         network             Prefix(𝑟 ) ∉ Bogons
                                              𝐹𝑟𝑜𝑚𝑃𝑒𝑒𝑟 (𝑟 ) =⇒
                          𝑅 ∈ Routers                                     Bogon prefixes from peers should not be accepted at routers
                                              Prefix(𝑟 ) ∉ Bogons
         Network          Internal edges      𝐹𝑟𝑜𝑚𝑃𝑒𝑒𝑟 (𝑟 ) =⇒
                                                                          Bogon prefixes from peers should not be sent along edges
         Invariants       R1 → R2             Prefix(𝑟 ) ∉ Bogons
                          Other               𝑇𝑟𝑢𝑒                        Edges to and from external peers are unconstrained
       (a) End-to-end property and network invariants needed to verify that the network does not accept bogons from external peers.

      Type            Locations (𝑙)        Logical Formula (𝐼𝑙 )                   Description
      End-to-end                           𝐹𝑟𝑜𝑚𝑅𝑒𝑔𝑖𝑜𝑛(𝑟 ) =⇒                       Routers outside a region should not accept
                      𝑅 ∉ Region
      Property                              Prefix(𝑟 ) ∉ ReusedIPs                 routes with reused addresses from that region
                                           𝐹𝑟𝑜𝑚𝑅𝑒𝑔𝑖𝑜𝑛(𝑟 ) ∧
                      𝑅 ∈ Region            Prefix(𝑟 ) ∈ ReusedIPs =⇒              Routes with reused addresses are tagged with a com-
                                           RegionalComms ∩ Comm(𝑟 ) = {𝐶}          munity for that region and no other region
      Network                              𝐹𝑟𝑜𝑚𝑅𝑒𝑔𝑖𝑜𝑛(𝑟 ) =⇒                       Routers outside a region should not accept
                      𝑅 ∉ Region
      Invariants                            Prefix(𝑟 ) ∉ ReusedIPs                 routes with reused addresses from that region
                      R1 → R2              𝐼𝑅1                                     Edges have same invariant as sending router
                      E→R                  Comm(𝑟 ) = ∅                            Routes from external peers have no communities
 (b) End-to-end property and network invariants needed to verify that reused addresses are not accepted by any router outside the region.

      Type            Locations (𝑙)        Logical Formula (𝐼𝑙 )                  Description
      End-to-end                           𝐹𝑟𝑜𝑚𝑅𝑒𝑔𝑖𝑜𝑛(𝑟 ) ∧                       𝑅2 inside a region eventually accepts a route
                      𝑅2 ∈ Region
      Property                             Prefix(𝑟 ) ∈ ReusedIPs                 with reused addresses from that region
                      Edge from data       𝐹𝑟𝑜𝑚𝑅𝑒𝑔𝑖𝑜𝑛(𝑟 ) ∧                       Assume there is a route from the data center to
      Assumption
                      center 𝐷 → 𝑅1        Prefix(𝑟 ) ∈ ReusedIPs                 𝑅1 with a reused prefix
                                           𝐹𝑟𝑜𝑚𝑅𝑒𝑔𝑖𝑜𝑛(𝑟 ) ∧
      Path                                                                        𝑅1 and 𝑅2 eventually select a route with reused
                      𝑅1, 𝑅2, 𝑅1 → 𝑅2      Prefix(𝑟 ) ∈ ReusedIPs ∧
      Constraints                                                                 prefixes and the regional community
                                           RegionalComms ∩ Comm(𝑟 ) = {𝐶}
(c) End-to-end property and path constraints needed to verify that reused addresses are eventually selected by each WAN router in that region.
We assume that the route flows from the data center along the path 𝐷 → 𝑅1 → 𝑅2 .

                      Table 4: End-to-end properties and network invariants for three use cases in the WAN.


indicating a bug in either a specific route map or a specific local       local invariants written as a C# function using the Zen constraint
invariant. To our knowledge no prior tool that verifies properties        solving library [28], and to specify the routers and policies of in-
of all possible external announcements from neighbors has been            terest. The Zen library translates the functions into SMT formulas
demonstrated to scale to such a size.                                     that are solved by Z3 [7]. For each local check that fails, the tool
   We used Lightyear to verify two classes of properties that the         returns a counterexample consisting of a specific route map and a
wide-area network must satisfy. In all cases we determined the            concrete input route that leads to a violation.
intended network behavior by inspecting the configurations and                Internet Peering Policies: We used Lightyear to verify that
talking with the network operators, and the local constraints were        11 different kinds of "bad" routes are never accepted from peers.
written based on that intent. This process was typically iterative.       Each of these properties can be expressed as a safety property on
That is, we would write an initial property specification and its set     each node 𝑅 in the network of the following form:
of local invariants based on our current understanding of how the                            (𝑅, {𝑟 |𝐹𝑟𝑜𝑚𝑃𝑒𝑒𝑟 (𝑟 ) =⇒ 𝑄 (𝑟 )})
network operates. If Lightyear reported violations of local checks,       with different properties 𝑄 (𝑟 ). These include properties like not
we would inspect the counterexamples and discuss with opera-              accepting bogons or routes with invalid AS paths. An example of
tors, either determining that the bugs are real errors or identifying     the invariants for the no-bogons property is shown in Table 4a. The
special cases that led to refined local invariants and (sometimes)        network has a set of Internet edge routers, that peer with Internet
refined end-to-end property specifications.                               service providers, other cloud providers, and customers, and so
   Implementation: We implemented Lightyear as a tool in C#.              act as gateways between the cloud provider and the Internet. The
The tool parses and extracts the BGP policy along with import             wide-area network ensures that "bad" routes are not admitted by
and export route maps from each configuration, while supporting           filtering them at all of the Internet edge routers.
common attributes of BGP routes such as communities, AS path,                 As mentioned earlier, running Lightyear to check these prop-
MED, local preference, along with common route map features, like         erties is an iterative process, which involves refining the local con-
matching on and setting attributes. The tool allows users to provide      straints based on operator feedback. In the end, through this process
ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA                                                                                Tang et al.


Lightyear identified 11 actual configuration errors. These included        of interest must not only have the community 𝐶, but they also
cases where a route map denied more traffic than intended, and             must not be tagged with any other region’s community. Otherwise,
inconsistencies between the filters of edge routers that are intended      these routes could be accidentally accepted by other regions. The
to have similar behavior. For example, in one case, among the hun-         local constraints validate this property, and the WAN enforces it by
dreds of similarly defined peering sessions, it was discovered that a      deleting all communities on routes coming from the data centers,
handful had ad-hoc policies that filtered AS paths differently. All        before adding the community 𝐶.
of the findings were latent bugs that did not have an immediate               The communities used in each region were documented in a
impact, but could become impactful in the presence of failures or          metadata file, which made it easy for us to write the local constraints
changes in the external announcements received from neighbors.             for each region. In one case, Lightyear found a violation where a
Further, because Lightyear is sound the operators can be sure that         router used a community that was not present in the metadata file.
these are the only violations of the desired end-to-end properties.        The operators acknowledged that this was a bug that could cause
As of this writing, all identified errors are prioritized for fixing by    some traffic to be redirected. Lightyear was able to verify all other
network engineers.                                                         local checks, for both the safety and the liveness properties.
   Verification with Lightyear is highly scalable. The maximum
time that it took Lightyear to sequentially run all of the local
                                                                           6.2    Scaling Experiments
checks for any single property was 15 minutes, across all devices in       To illustrate the scaling benefits of modular checking, we compared
the network. As another data point, an automation that sequentially        Lightyear with Minesweeper [4] on synthetic test cases. For a fair
ran the local checks for four of the properties across all of the          comparison, we created an implementation of Lightyear that is
hundreds of edge routers took a total of 16 minutes. Given that            built on top of the same parser and constraint generation system as
each of these checks can be run independently on each device               Minesweeper. This is a different implementation from the one used
configuration, it would also be easy to parallelize these checks           on the cloud network. We use a BGP full mesh where each router
in the future in order to scale horizontally for a large number of         is connected to one external neighbor through eBGP and all other
devices.                                                                   routers through iBGP. This leads to a total of 𝑁 2 edges in a network
   While using Lightyear to verify these 11 properties, we also            of size 𝑁 . The network’s configuration is relatively simple, with
learned best practices for writing properties. Initially, we combined      each eBGP connection using only prefix and community filters.
multiple properties into a single property for Lightyear to check.         We checked a no-transit safety property, similar to the example in
However, we found that writing multiple simpler properties, with           Figure 1.
associated simpler local constraints, was not only easier to write            Figure 3 provides details on these results by comparing the
and debug but also was usually faster to run, since the constraints        number of SMT variables and constraints generated by each tool,
are simpler for the underlying SMT solver to process.                      as well as the amount of time used to solve the SMT constraints
   Proper IP Reuse: In the second use case, Lightyear verified             compared to the total computation time. As the network size in-
proper usage of reused IPs within the network. The cloud network is        creases, Minesweeper requires several orders of magnitude more
partitioned into dozens of regions, and some private IPv4 addresses        SMT variables and constraints than the maximum number required
are reused in different regions. There is a safety property that traffic   by Lightyear for any local check (compare Figures 3a and 3b). As
sent to these private addresses must stay within the region, and also      a result, SMT solving time dominates the run time of Minesweeper
a liveness property that routes to reused addresses are advertised         and is the limiting factor on its ability to scale, while for Lightyear
to other WAN routers in the same region. We verified both of these         the solving time is a relatively small portion of the total time (com-
properties for all regions in the network.                                 pare Figures 3c and 3d). Minesweeper does not terminate within
   The safety property to verify is as follows, for each router 𝑅 that     two hours when run on a network of size 40, while Lightyear
is not part of the region of interest:                                     verifies a network of size 100 in 5.5 minutes.
      (𝑅, {𝑟 | 𝐹𝑟𝑜𝑚𝑅𝑒𝑔𝑖𝑜𝑛(𝑟 ) =⇒ Prefix(𝑟 ) ∉ ReusedIPs})
Here 𝐹𝑟𝑜𝑚𝑅𝑒𝑔𝑖𝑜𝑛(𝑟 ) is a ghost variable that is set to true only
                                                                           7     RELATED WORK
on routes coming from external routers in the particular region,           Control Plane Verification: State-of-the-art approaches to net-
and ReusedIPs is the set of prefixes that are reused. The liveness         work control-plane verification were summarized in Table 1. Unlike
property requires that in each region, a route with a reused prefix        Lightyear, these approaches are all monolithic — they require
from the data center routers can reach all other routers in that           joint analysis of the configurations of all nodes — which dramat-
region, possibly going through one intermediate router. That is,           ically limits scalability. Compared to Lightyear, Minesweeper’s
for every pair of WAN routers 𝑅1 and 𝑅2 in the same region, if 𝑅1          worst case complexity is exponential in the network size. Other
is connected to a data center router 𝐷, then routes with a reused          improvements not only reduce generality but are at least quadratic
prefix can travel 𝐷 → 𝑅1 → 𝑅2 .                                            in the network size even when using specialized algorithms. Most
   The WAN enforces these properties by tagging routes for reused          approaches make tradeoffs in expressiveness, for example giving
IP addresses with a region-specific community 𝐶 when they are              up the ability to reason about all possible BGP announcements
received from data centers. Routers in the same region then accept         from neighbors [1, 10, 22, 27]. In contrast, Lightyear’s modular
routes tagged with that community, while routers in other regions          approach only requires reasoning about individual BGP route maps
reject them. The local constraints we used to verify the safety            in isolation and so is highly scalable. Lightyear also provides guar-
and liveness properties are shown in Table 4b and 4c respectively.         antees across all possible external announcements and, for safety
One subtlety is that routes to reused IP addresses in the region           properties, arbitrary failures.
Lightyear: Using Modularity to Scale BGP Control Plane Verification                  ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA

                                             Number of Variables (left)                                                       Maximum Number of Variables (left)
                                            Number of Constraints (right)                                                    Maximum Number of Constraints (right)
                  20,000,000                                                                                  4,000
                  15,000,000
 Count




                                                                                                Count
                  10,000,000                                                                                  2,000
                   5,000,000
                          0                                                                                        0
                                10    20    30    40 50 60 70 80        90 100                                          10   20   30    40 50 60 70 80         90 100
                                                 Number of Routers                                                                     Number of Routers

(a) Number of variables and constraints generated by                                           (b) The maximum number of variables and constraints
Minesweeper for synthetic networks.                                                            in any single local check generated by Lightyear.
                                     Constraint Solving Time (left)                                                               Constraint Solving Time (left)
                                          Total Time (right)                                                                           Total Time (right)
                  600                                                                                             600
 Time (seconds)




                                                                                                 Time (seconds)
                  400                                                                                             400

                  200                                                                                             200
                                                    Exceeds 2hrs
                    0
                          10   20    30     40 50 60 70 80         90 100                                               10   20   30    40 50 60 70 80         90 100
                                           Number of Routers                                                                           Number of Routers

(c) Time used by Minesweeper to verify a property of                                            (d) Time used by Lightyear to verify a property in
synthetic networks. Runtime for networks with 40                                                synthetic networks, not including time to parse con-
routers or more exceeds two hours, not including time                                           figurations.
to parse configurations.

                                     Figure 3: Comparing Lightyear and Minesweeper on synthetic networks of various sizes.


   rcc [8] validates important properties of BGP configurations,                  is orthogonal to this line of work; the two approaches could be
largely through local checks on individual configuration. However,                combined.
rcc is limited to specific "best practice" policies, and there is no                 Data Plane Verification: Other tools check properties of for-
guarantee that the local checks together ensure the desired end-to-               warding state, rather than network configurations [3, 13, 15, 16, 18,
end properties.                                                                   19, 25]. These approaches generally require joint reasoning about
   Closest to our work are recent techniques for modular control-                 the entire network. A recent exception is RCDC [12], which mod-
plane verification, Kirigami [23] and Timepiece [2], which also use               ularly verifies global reachability contracts in a data center via
assume-guarantee reasoning for the control plane via local invari-                local checks. However, RCDC is specific to one data center design
ants. However, each approach makes a different set of tradeoffs                   and does not provide a general framework for decomposing global
than Lightyear. Kirigami’s local invariants require the exact routes              property checks into local checks. Another approach [20] exploits
that will arrive on a particular edge. Because these invariants are               abstraction, such as symmetries, to scale data-plane verification.
fully concrete, Kirigami cannot reason about arbitrary route an-                     Modular Verification: Assume-guarantee reasoning [14, 21]
nouncements from neighbors or give guarantees in the presence of                  enables modular verification in other domains. A global property
failures.                                                                         is modularized by providing each system component with local
   Timepiece allows for expressive local invariants and properties,               invariants that it must satisfy, assuming other components satisfy
using an explicit notion of time. In Timepiece, routing protocols                 their invariants. Lightyear applies this methodology to networks
have discrete, synchronized time steps, and in each step, each router             to generate the local checks that each BGP policy must satisfy.
computes the best route among those it receives. This model allows                   Verification often requires identifying inductive invariants, prop-
Timepiece to specify and check temporal-logic properties but re-                  erties that hold over some unbounded space of system states, such
quires users to provide complex local invariants for each node that               as the iterations of a loop [11]. Such invariants arise naturally in
are explicitly indexed by time. In our model routes can be sent and               networks and enable many locations to use the same local invariant.
arrive in arbitrary orders, and we demonstrate how to specify and                 Typically, a small set of nodes establishes an inductive invariant
check common safety and liveness properties without explicit time.                (e.g., by attaching a community), and this invariant holds through
   Another line of work has improved scalability of control-plane                 the network as long as other nodes “do no harm” (e.g., never remove
verification through forms of abstraction [5, 6]: the full network is             communities).
analyzed monolithically, but irrelevant or redundant configuration
information is abstracted away to simplify the analysis. Our work
ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA                                                                                                          Tang et al.


8    CONCLUSION                                                                         [14] C. B. Jones. 1983. Specification and design of (parallel) programs. In Proceedings
                                                                                             of IFIP ’83, R. E. A. Manson (Ed.). IFIP, North-Holland, 321–332.
Exploiting symmetries in network verification [20] is natural be-                       [15] Peyman Kazemian, George Varghese, and Nick McKeown. 2012. Header Space
cause of hardware design patterns such as fat trees. Similarly, ex-                          Analysis: Static Checking for Networks. In Proceedings of the 9th USENIX Confer-
                                                                                             ence on Networked Systems Design and Implementation (NSDI’12). USENIX Associ-
ploiting modularity in control plane verification is natural because                         ation, Berkeley, CA, USA, 9–9. http://dl.acm.org/citation.cfm?id=2228298.2228311
of design patterns in the way configurations are written and main-                      [16] Ahmed Khurshid, Wenxuan Zhou, Matthew Caesar, and P. Brighten Godfrey. 2012.
                                                                                             Veriflow: Verifying Network-wide Invariants in Real Time. SIGCOMM Comput.
tained in well engineered networks. We have confirmed this hy-                               Commun. Rev. 42, 4 (Sept. 2012), 467–472. https://doi.org/10.1145/2377677.2377766
pothesis in six months of deployment at a major cloud vendor.                           [17] Leslie Lamport. 1994. The Temporal Logic of Actions. ACM Transactions on
Further, Lightyear finesses the need to reason about time to prove                           Programming Languages and Systems 16, 3 (1994), 872–923.
                                                                                        [18] Nuno P. Lopes, Nikolaj Bjørner, Patrice Godefroid, Karthick Jayaraman, and
safety and liveness, offering a sweet spot between expressiveness                            George Varghese. 2015. Checking Beliefs in Dynamic Networks. In 12th USENIX
and complexity that has worked well for many desired properties                              Symposium on Networked Systems Design and Implementation (NSDI 15). USENIX
in our network.                                                                              Association, Oakland, CA, 499–512. https://www.usenix.org/conference/nsdi15/
                                                                                             technical-sessions/presentation/lopes
   In Lightyear, users must provide local network constraints.                          [19] Haohui Mai, Ahmed Khurshid, Rachit Agarwal, Matthew Caesar, P Brighten
While in our experience it has been easy to determine these con-                             Godfrey, and Samuel Talmadge King. 2011. Debugging the data plane with
                                                                                             anteater. ACM SIGCOMM Computer Communication Review 41, 4 (2011), 290–
straints, we believe it is possible to instead learn local invariants                        301.
automatically from configurations in the future, for example when                       [20] Gordon D. Plotkin, Nikolaj Bjørner, Nuno P. Lopes, Andrey Rybalchenko, and
properties are enforced via communities.                                                     George Varghese. 2016. Scaling network verification using symmetry and surgery.
                                                                                             In Proceedings of the 43rd Annual ACM SIGPLAN-SIGACT Symposium on Principles
                                                                                             of Programming Languages, POPL 2016, St. Petersburg, FL, USA, January 20 - 22,
REFERENCES                                                                                   2016, Rastislav Bodík and Rupak Majumdar (Eds.). ACM, 69–83. https://doi.org/
                                                                                             10.1145/2837614.2837657
 [1] Anubhavnidhi Abhashkumar, Aaron Gember-Jacobson, and Aditya Akella. 2020.          [21] Amir Pnueli. 1984. In Transition From Global to Modular Temporal Reasoning
     Tiramisu: Fast Multilayer Network Verification. In 17th USENIX Symposium                about Programs. In Logics and Models of Concurrent Systems (NATO ASI Series),
     on Networked Systems Design and Implementation (NSDI 20). USENIX Associ-                Krzysztof R. Apt (Ed.), Vol. 13. Springer, 123–144.
     ation, Santa Clara, CA, 201–219. https://www.usenix.org/conference/nsdi20/         [22] Santhosh Prabhu, Kuan Yen Chou, Ali Kheradmand, Brighten Godfrey, and
     presentation/abhashkumar                                                                Matthew Caesar. 2020. Plankton: Scalable network configuration verification
 [2] Timothy Alberdingk Thijm, Ryan Beckett, Aarti Gupta, and David Walker. 2023.            through model checking. (2020).
     Modular Control Plane Verification via Temporal Invariants. Proc. ACM Program.     [23] Tim Alberdingk Thijm, Ryan Beckett, Aarti Gupta, and David Walker. 2022.
     Lang. 7, PLDI, Article 108 (jun 2023), 26 pages. https://doi.org/10.1145/3591222        Kirigami, the Verifiable Art of Network Cutting. (2022). https://doi.org/10.48550/
 [3] Carolyn Jane Anderson, Nate Foster, Arjun Guha, Jean-Baptiste Jeannin, Dexter           ARXIV.2202.06098
     Kozen, Cole Schlesinger, and David Walker. 2014. NetKAT: Semantic Foundations      [24] Konstantin Weitz, Doug Woos, Emina Torlak, Michael D. Ernst, Arvind Krish-
     for Networks. In Proceedings of the 41st ACM SIGPLAN-SIGACT Symposium on                namurthy, and Zachary Tatlock. 2016. Scalable Verification of Border Gateway
     Principles of Programming Languages (POPL ’14). Association for Computing Ma-           Protocol Configurations with an SMT Solver. SIGPLAN Not. 51, 10 (Oct. 2016),
     chinery, New York, NY, USA, 113–126. https://doi.org/10.1145/2535838.2535862            765–780. https://doi.org/10.1145/3022671.2984012
 [4] Ryan Beckett, Aarti Gupta, Ratul Mahajan, and David Walker. 2017. A Gen-           [25] Hongkun Yang and Simon S Lam. 2015. Real-time verification of network proper-
     eral Approach to Network Configuration Verification. In Proceedings of the              ties using atomic predicates. IEEE/ACM Transactions on Networking 24, 2 (2015),
     Conference of the ACM Special Interest Group on Data Communication (SIG-                887–900.
     COMM ’17). Association for Computing Machinery, New York, NY, USA, 155–168.        [26] Fangdan Ye, Da Yu, Ennan Zhai, Hongqiang Harry Liu, Bingchuan Tian, Qiaobo
     https://doi.org/10.1145/3098822.3098834                                                 Ye, Chunsheng Wang, Xin Wu, Tianchen Guo, Cheng Jin, Duncheng She, Qing
 [5] Ryan Beckett, Aarti Gupta, Ratul Mahajan, and David Walker. 2018. Control Plane         Ma, Biao Cheng, Hui Xu, Ming Zhang, Zhiliang Wang, and Rodrigo Fonseca. 2020.
     Compression. In Proceedings of the 2018 Conference of the ACM Special Interest          Accuracy, Scalability, Coverage: A Practical Configuration Verifier on a Global
     Group on Data Communication (SIGCOMM ’18). Association for Computing Ma-                WAN. In Proceedings of the Annual Conference of the ACM Special Interest Group
     chinery, New York, NY, USA, 476–489. https://doi.org/10.1145/3230543.3230583            on Data Communication on the Applications, Technologies, Architectures, and Pro-
 [6] Ryan Beckett, Aarti Gupta, Ratul Mahajan, and David Walker. 2019. Abstract              tocols for Computer Communication (SIGCOMM ’20). Association for Computing
     Interpretation of Distributed Network Control Planes. Proc. ACM Program. Lang.          Machinery, 599–614. https://doi.org/10.1145/3387514.3406217
     4, POPL, Article 42 (dec 2019), 27 pages. https://doi.org/10.1145/3371110          [27] Fangdan Ye, Da Yu, Ennan Zhai, Hongqiang Harry Liu, Bingchuan Tian, Qiaobo
 [7] Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In            Ye, Chunsheng Wang, Xin Wu, Tianchen Guo, Cheng Jin, Duncheng She, Qing
     Tools and Algorithms for the Construction and Analysis of Systems, C. R. Ramakr-        Ma, Biao Cheng, Hui Xu, Ming Zhang, Zhiliang Wang, and Rodrigo Fonseca. 2020.
     ishnan and Jakob Rehof (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,          Accuracy, Scalability, Coverage: A Practical Configuration Verifier on a Global
     337–340.                                                                                WAN. In Proceedings of the Annual Conference of the ACM Special Interest Group on
 [8] Nick Feamster and Hari Balakrishnan. 2005. Detecting BGP Configuration Faults           Data Communication on the Applications, Technologies, Architectures, and Protocols
     with Static Analysis. In Proceedings of the 2Nd Conference on Symposium on              for Computer Communication (SIGCOMM ’20). Association for Computing Ma-
     Networked Systems Design & Implementation - Volume 2 (NSDI’05). USENIX As-              chinery, New York, NY, USA, 599–614. https://doi.org/10.1145/3387514.3406217
     sociation, Berkeley, CA, USA, 43–56. http://dl.acm.org/citation.cfm?id=1251203.    [28] Zen [n. d.]. Zen. https://github.com/microsoft/Zen. ([n. d.]).
     1251207
 [9] Jean-Christophe Filliâtre, Léon Gondelman, and Andrei Paskevich. 2016. The
     spirit of ghost code. Formal Methods in System Design 48, 3 (2016), 152–174.       Appendices are supporting material that has not been peer-reviewed.
[10] Aaron Gember-Jacobson, Raajay Viswanathan, Aditya Akella, and Ratul Mahajan.
     2016. Fast Control Plane Analysis Using an Abstract Representation. In Proceed-    A     BGP TRACE AXIOMS
     ings of the 2016 ACM SIGCOMM Conference (SIGCOMM ’16). ACM, New York,
     NY, USA, 300–313. https://doi.org/10.1145/2934872.2934876                          The safety axioms consist of the following properties, for all 1 ≤
[11] Charles Antony Richard Hoare. 1969. An axiomatic basis for computer program-       𝑘 ≤ 𝑛:
     ming. Commun. ACM 12, 10 (1969), 576–580.
[12] Karthick Jayaraman, Nikolaj Bjørner, Jitu Padhye, Amar Agrawal, Ashish Bhar-          (1) If 𝐴𝑘 = recv(𝑁 → 𝑅, 𝑟 ), then either:
     gava, Paul-Andre C Bissonnette, Shane Foster, Andrew Helwer, Mark Kasten, Ivan           (a) 𝑁 ∈ Externals, or
     Lee, Anup Namdhari, Haseeb Niaz, Aniruddha Parkhi, Hanukumar Pinnamraju,                (b) there exists 𝑗 < 𝑘 such that 𝐴 𝑗 = frwd(𝑁 → 𝑅, 𝑟 )
     Adrian Power, Neha Milind Raje, and Parag Sharma. 2019. Validating Datacenters
     at Scale. In Proceedings of the ACM Special Interest Group on Data Communication      (2) If 𝐴𝑘 = slct(𝑅, 𝑟 ), then there exists 𝑗 < 𝑘, 𝑟 ′ ∈ Routes, and
     (SIGCOMM ’19). Association for Computing Machinery, New York, NY, USA,                     𝑁 ∈ Routers∪Externals such that 𝐴 𝑗 = recv(𝑁 → 𝑅, 𝑟 ′ )
     200–213. https://doi.org/10.1145/3341302.3342094
[13] Karthick Jayaraman, Nikolaj Bjørner, Geoff Outhred, and Charlie Kaufman. 2014.
                                                                                                and 𝑟 = Import(𝑁 → 𝑅, 𝑟 ′ )
     Automated Analysis and Debugging of Network Connectivity Policies. Technical          (3) If 𝐴𝑘 = frwd(𝑅 → 𝑁 , 𝑟 ), then either:
     Report MSR-TR-2014-102. Microsoft.                                                       (a) 𝑟 ∈ Originate(𝑅 → 𝑁 ), or
Lightyear: Using Modularity to Scale BGP Control Plane Verification            ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA


      (b) there exists 𝑗 < 𝑘 and 𝑟 ′ ∈ Routes such that 𝐴 𝑗 =              Case 𝐴𝑘+1 = frwd(𝑅 → 𝑁 , 𝑟 ), so we have to show that 𝑟 ∈ 𝐼𝑅 . By
           slct(𝑅, 𝑟 ′ ) and 𝑟 = Export(𝑅 → 𝑁 , 𝑟 ′ )                      the trace validity axioms, either:
   The liveness axioms depend on the BGP route preference relation,            (1) 𝑟 ∈ Originate(𝑅 → 𝑁 ). Then from the Originate check in
which selects routes to the same prefix by comparing their local                   𝐶 for 𝑅 → 𝑁 we have that 𝑟 ∈ 𝐼𝑅→𝑁 .
preference, AS paths, and other attributes. We say that 𝑟 1 > 𝑟 2 if 𝑟 1       (2) There exists 𝑗 < 𝑘 + 1 and 𝑟 ′ ∈ Routes such that 𝐴 𝑗 =
is preferred over 𝑟 2 . The liveness axioms consist of the following               slct(𝑅, 𝑟 ′ ) and 𝑟 = Export(𝑅 → 𝑁 , 𝑟 ′ ). From the inductive
properties, for all 1 ≤ 𝑘 ≤ 𝑛:                                                     hypothesis, we have that 𝑟 ′ ∈ 𝐼𝑅 . Then from the Export
    (1) If all of the following are true:                                          check in 𝐶 for 𝑅 → 𝑁 , we can conclude that 𝑟 ∈ 𝐼𝑅→𝑁 .
        • 𝐴𝑘 = slct(𝑅, 𝑟 ) ∈ 𝑇                                                 Now we prove the correctness theorem for Lightyear, which
        • 𝑟 ′ = Export(𝑅 → 𝑁 , 𝑟 ) with 𝑟 ′ ≠ Reject                       says that Lightyear’s checks are sufficient to ensure that the given
        then there exists 𝑗 > 𝑘 such that 𝐴 𝑗 = frwd(𝑅 → 𝑁 , 𝑟 ′ )         network property holds, for all valid traces.
    (2) If 𝑟 ∈ Originate(𝑅 → 𝑁 ) then there exists 𝑗 > 𝑘 such that         Theorem: Given a BGP topology and policy, a network property
        𝐴 𝑗 = frwd(𝑅 → 𝑁 , 𝑟 )                                             (ℓ, 𝑃), and network invariants 𝐼 , let 𝐶 be the set of Import, Export,
    (3) If 𝐴𝑘 = frwd(𝑅 → 𝑁 , 𝑟 ) and there is no link failure along        and Originate checks that Lightyear generates. If all checks in
        𝑅 → 𝑁 , then there exists 𝑗 > 𝑘 such that 𝐴 𝑗 = recv(𝑁 →           𝐶 pass and 𝐼 ℓ ⊆ 𝑃, then for all 𝑇 ∈ Valid, 𝑟 ∈ Routes, 𝑅, 𝑁 ∈
        𝑅, 𝑟 )                                                             Routers:
    (4) If all of the following are true:                                        • if ℓ = 𝑅 and slct(𝑅, 𝑟 ) ∈ 𝑇 , then 𝑟 ∈ 𝑃
        • 𝐴𝑘 = recv(𝑁 → 𝑅, 𝑟 )                                                   • if ℓ = 𝑅 → 𝑁 and frwd(𝑅 → 𝑁 , 𝑟 ) ∈ 𝑇 ∨ recv(𝑅 → 𝑁 , 𝑟 ) ∈
        • 𝑟 ′ = Import(𝑁 → 𝑅, 𝑟 ) with 𝑟 ′ ≠ Reject                                𝑇 , then 𝑟 ∈ 𝑃
        • For all neighbors 𝑁 ′ ≠ 𝑁 and routes 𝑟 ′′ :                      Proof: There are two cases:
           if Prefix(𝑟 ) = Prefix(𝑟 ′′ ) and recv(𝑁 ′ → 𝑅, 𝑟 ′′ ) ∈ 𝑇 ,        (1) ℓ = 𝑅 and slct(𝑅, 𝑟 ) ∈ 𝑇 . From the earlier lemma we have
           then 𝑟 ′ > Import(𝑁 → 𝑅, 𝑟 ′′ )                                         that 𝑟 ∈ 𝐼 ℓ , and since 𝐼 ℓ ⊆ 𝑃 it follows that 𝑟 ∈ 𝑃.
        then there exists 𝑗 > 𝑘 such that 𝐴 𝑗 = slct(𝑅, 𝑟 ′ ) ∈ 𝑇 .            (2) ℓ = 𝑅 → 𝑁 and frwd(𝑅 → 𝑁 , 𝑟 ) ∈ 𝑇 ∨ recv(𝑅 → 𝑁 , 𝑟 ) ∈ 𝑇 .
                                                                                   Again from the earlier lemma we have that 𝑟 ∈ 𝐼 ℓ , and since
B    CORRECTNESS PROOF FOR SAFETY
                                                                                   𝐼 ℓ ⊆ 𝑃 it follows that 𝑟 ∈ 𝑃.
In this section we prove that Lightyear’s modular approach to                  Note that our reasoning does not depend on BGP converging as
control-plane verification is correct.                                     traces can be infinite.
   First we state and prove the key lemma, which says that the local
checks are sufficient to ensure that the network invariants 𝐼 hold,        C    CORRECTNESS PROOF FOR LIVENESS
for all valid traces.
                                                                           In this section, we prove the correctness of the modular checks for
Lemma: Given a BGP topology and policy as well as network                  liveness properties.
invariants 𝐼 , let 𝐶 be the set of Import, Export, and Originate checks    Theorem: Given the following:
that Lightyear generates. If all checks in 𝐶 pass, then for all 𝑇 ∈             • The network configurations
Valid, 𝑟 ∈ Routes, 𝑅, 𝑁 ∈ Routers:                                              • A liveness property (ℓ, 𝑃)
       • if slct(𝑅, 𝑟 ) ∈ 𝑇 , then 𝑟 ∈ 𝐼𝑅                                       • A path 𝑆 = (ℓ1, ℓ2, . . . , ℓ𝑛−1, ℓ𝑛 = ℓ)
       • if frwd(𝑅 → 𝑁 , 𝑟 ) ∈ 𝑇 ∨ recv(𝑅 → 𝑁 , 𝑟 ) ∈ 𝑇 , then 𝑟 ∈              • A constraint for each location 𝐶 1 . . . 𝐶𝑛
          𝐼𝑅→𝑁                                                             For all valid traces 𝑇 , if all of the following are true:
Proof: The proof is by induction on the length of the (partial) trace         (1) all checks (propagation, no interference) pass
𝑇.                                                                            (2) there exists 𝑟 such that recv(ℓ1, 𝑟 ) ∈ 𝑇 ∧ 𝐶 1 (𝑟 )
Base case: For a partial trace of length 0, there are no events, so           (3) for all 𝑟 , 𝐶𝑛 (𝑟 ) =⇒ 𝑃 (𝑟 )
the statement is vacuously true.                                              (4) there are no link failures along the path
Inductive case: Suppose 𝑇 = 𝐴1, 𝐴2, . . . , 𝐴𝑘+1 . We assume by in-
                                                                           then there exists 𝑟 ′ such that either:
duction that the statement is true for 𝐴1, 𝐴2, . . . , 𝐴𝑘 . We do a case
                                                                                • ℓ ∈ Routers and there exists 𝑟 ′ such that slct(ℓ, 𝑟 ′ ) ∈ 𝑇
analysis on the event 𝐴𝑘+1 :
                                                                                   and 𝑃 (𝑟 ′ ) holds, or
Case 𝐴𝑘+1 = recv(𝑁 → 𝑅, 𝑟 ), so we have to show that 𝑟 ∈ 𝐼 𝑁 →𝑅 .
                                                                                • ℓ ∈ Edges and there exists 𝑟 ′ such that frwd(ℓ, 𝑟 ′ ) ∈ 𝑇 and
By the trace validity axioms, either:
                                                                                   𝑃 (𝑟 ′ ) holds
    (1) 𝑁 ∈ Externals. In this case we know that 𝐼 𝑁 →𝑅 = Routes,
                                                                           Proof: Consider a valid trace 𝑇 . By the assumption, there exists 𝑟 1
          so 𝑟 ∈ 𝐼 𝑁 →𝑅 .
                                                                           such that recv(ℓ1, 𝑟 1 ) ∈ 𝑇 and 𝐶 1 (𝑟 1 )
    (2) There exists 𝑗 < 𝑘 + 1 such that 𝐴 𝑗 = frwd(𝑁 → 𝑅, 𝑟 ). Then
                                                                              There must exists at least one router 𝑅 = ℓ 𝑗 and a route 𝑟 𝑗 such
          by the inductive hypothesis we have that 𝑟 ∈ 𝐼 𝑁 →𝑅 .
                                                                           that slct(𝑅, 𝑟 𝑗 ) is in the trace and Prefix(𝑟 𝑗 ) = Prefix(𝑟 1 ). If
Case 𝐴𝑘+1 = slct(𝑅, 𝑟 ), so we have to show that 𝑟 ∈ 𝐼𝑅 . From the
                                                                           there are no routers outside the path that have their routes ac-
trace validity axioms, we know that there exists 𝑗 < 𝑘 + 1, 𝑟 ′ ∈
                                                                           cepted then 𝑟 2 = Import(ℓ1, 𝑟 1 ) is the most prefered route at ℓ2 , so
Routes, and 𝑁 ∈ Routers∪Externals such that 𝐴 𝑗 = recv(𝑁 →
                                                                           slct(ℓ2, 𝑟 2 ) will be in the trace. If there are routers outside the path
𝑅, 𝑟 ′ ) and 𝑟 = Import(𝑁 → 𝑅, 𝑟 ′ ). From the inductive hypothesis,
                                                                           that have their routes accepted, then by the no interference check,
we know that 𝑟 ′ ∈ 𝐼 𝑁 →𝑅 . Therefore by the Import check in 𝐶 for
                                                                           it must be that the router accepted at ℓ 𝑗 will satisfy 𝐶 𝑗 (𝑟 𝑗 ).
𝑁 → 𝑅, we can conclude that 𝑟 ∈ 𝐼𝑅 .
ACM SIGCOMM ’23, September 10, 2023, New York, NY, USA                                                                                 Tang et al.


   Consider the last router that accepts a route from a neighbor          If 𝑙𝑖 = 𝑁 → 𝑅 ∈ Edges, then we know that frwd(ℓ𝑖 , 𝑟𝑖 ) ∈ 𝑇
outside the path. We will use induction to show that all locations ℓ𝑖     and 𝐶𝑖 (𝑟𝑖 ), and we want to show that there exists 𝑟𝑖+1 such that
between it and the end will have a route satisfying 𝐶𝑖 :                  slct(ℓ𝑖+1, 𝑟𝑖+1 ) ∈ 𝑇 and 𝐶𝑖+1 (𝑟𝑖+1 ). This holds because:
Base case: Take the last router 𝑅 = ℓ 𝑗 , where there exists 𝑟 𝑗 , 𝐶 𝑗          • let 𝑟𝑖+1 = Import(ℓ𝑖 , 𝑟𝑖 )
such that slct(ℓ 𝑗 , 𝑟 𝑗 ) ∈ 𝑇 and 𝐶 1 (𝑟 𝑗 ). We have shown above that         • recv(ℓ𝑖 , 𝑟𝑖 ) ∈ 𝑇 (from liveness axiom given no link failures)
there must be one.                                                              • 𝑟𝑖+1 ≠ Reject and 𝐶𝑖+1 (𝑟𝑖+1 ) (from the propagation check)
Inductive step: If ℓ𝑖 = 𝑅 ∈ Routers, then we know that the event                • We know that R and any router after R in the path did not
slct(ℓ𝑖 , 𝑟𝑖 ) ∈ 𝑇 and 𝐶𝑖 (𝑟𝑖 ) from the inductive hypothesis. We want             accept any routes from any neighbors not in the path, so
to show that there exists 𝑟𝑖+1 such that frwd(ℓ𝑖+1, 𝑟𝑖+1 ) ∈ 𝑇 and                 𝑁 → 𝑅, so we know slct(ℓ𝑖+1, 𝑟𝑖+1 ) ∈ 𝑇 and 𝐶𝑖+1 (𝑟 ′ )
𝐶𝑖+1 (𝑟𝑖+1 ). This is true because:                                           From this, we know that at ℓ𝑛 , there exists a route 𝑟𝑛 such that
     • let 𝑟 ′ = Export(ℓ𝑖+1, 𝑟𝑖 )                                        𝐶𝑛 (𝑟𝑛 ) and either frwd(ℓ𝑛 , 𝑟𝑛 ) ∈ 𝑇 or slct(ℓ𝑛 , 𝑟𝑛 ) ∈ 𝑇 . 𝐶𝑛 (𝑟𝑛 ) =⇒
     • slct(ℓ𝑖 , 𝑟𝑖 ) ∈ 𝑇 and 𝐶𝑖 (𝑟𝑖 ) (from the inductive hypothesis)    𝑃 (𝑟𝑛 ), which is what we wanted to prove. Again, note that our rea-
     • 𝑟 ′ ≠ Reject and 𝐶𝑖+1 (𝑟𝑖+1 ) (from the propagation check)         soning does not depend on BGP converging as traces can be infinite.
     • frwd(ℓ𝑖+1, 𝑟𝑖+1 ) ∈ 𝑇 (from the liveness axiom)
