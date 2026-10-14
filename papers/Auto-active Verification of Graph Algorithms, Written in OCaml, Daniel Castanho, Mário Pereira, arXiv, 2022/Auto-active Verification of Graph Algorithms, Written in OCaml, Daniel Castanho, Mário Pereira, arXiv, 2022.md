                                             Auto-active Verification of Graph Algorithms,
                                                          Written in OCaml ?

                                                                 Daniel Castanho and Mário Pereira

                                               NOVA LINCS – NOVA School of Science and Technology, Lisbon, Portugal
arXiv:2207.09854v1 [cs.LO] 20 Jul 2022




                                                Abstract. Functional programming offers the perfect ground for build-
                                                ing correct-by-construction software. Languages of such paradigm nor-
                                                mally feature state-of-the-art type systems, good abstraction mecha-
                                                nisms, and well-defined execution models. We claim that all of these
                                                make software written in a functional language excellent targets for for-
                                                mal certification. Yet, somehow surprising, techniques such as deductive
                                                verification have been seldom applied to large-scale programs, written
                                                in mainstream functional languages. In this paper, we wish to address
                                                this situation and present the auto-active proof of realistic OCaml imple-
                                                mentations. We choose implementations issued from the OCamlgraph
                                                library as our target, since this is both a large-scale and widely-used
                                                piece of OCaml code. We use Cameleer, a recently proposed tool for the
                                                deductive verification of OCaml programs, to conduct the proofs of the
                                                selected case studies. The vast majority of such proofs are completed
                                                fully-automatically, using SMT solvers, and when needed we can apply
                                                lightweight interactive proof inside the Why3 IDE (Cameleer translates
                                                an input program into an equivalent WhyML one, the language of the
                                                Why3 verification framework). To the best of our knowledge, these are
                                                the first mechanized, mostly-automated proofs of graph algorithms writ-
                                                ten in OCaml.


                                         1     Introduction
                                         The Verified Software Initiative [11] launched an ambitious program of bringing
                                         formal verification techniques to real world software. In other words, this research
                                         manifesto aimed for the stars: to build the foundations of a world where almost
                                         any piece of software could be verified. Over the course of years, verification
                                         tools have emerged from obscure academic artifacts into industrial standards.
                                         Several large companies are, progressively, starting to include formal methods
                                         into their production life cycle [16,7]. The so-called SMT revolution is a key
                                         factor in the recent success of formal techniques at an industrial scale, as au-
                                         tomated approaches are more easily integrated within large code bases. Also,
                                         automatic verification is more likely to be adopted by the regular programmer,
                                         when compared with interactive counterparts.
                                         ?
                                             This work is partly supported by the HORIZON 2020 Cameleer project
                                             (Marie Skłodowska-Curie grant agreement ID:897873) and NOVA LINCS (Ref.
                                             UIDB/04516/2020)
2         Daniel Castanho and Mário Pereira

    Despite all the advances in deductive verification and proof automation, these
have been seldom applied to the family of functional languages [20]. In this paper,
we wish to remedy the situation, and at the same time make a contribution to the
general effort of building a corpus of large-scale verified software. We present the
formal proof of realistic, widely-used programs written in OCaml, a mainstream
functional language. Our tool of choice is Cameleer [17], a recently proposed
infrastructure for the deductive verification of OCaml-written code.
    We choose to tackle the verification of OCaml modules issued from the
OCamlgraph library [5]. The rational for this choice is twofold: first, this a
widely-used library, making its correctness and safety of utmost importance;
second, graph implementations are complex pieces of software, making it a very
interesting challenge for deductive verification. Our choice might come as a sur-
prise, since OCamlgraph has been extensively used, hence tested in real-world
scenarios. The fact is that recent research has shown that even massively used
libraries are not ironclad, and can hide very subtle bugs [10]. OCamlgraph is no
exception, as demonstrated by the issues reported on the project’s repository1 .

Contributions. We present the formal verification of graph data structures, as
well as graph-manipulating algorithms, written in OCaml. We use OCamlgraph
as our main source of inspiration, and verify the following modules:

    – a persistent data structure representing graphs, with labeled edges;
    – an imperative alternative implementation, with unlabeled edges;
    – a function that checks whether a graph contains a cycle;
    – a breadth-first routine to decide whether there is a path between two vertices,
      in a given graph;
    – an alternative, more efficient and easier to verify, implementation of the said
      path check algorithm.

For the mentioned cycle finding function, instead of directly proving the OCaml-
graph implementation, which only returns a Boolean value, we take a different
route: we instrument such function to a certificate of the cycle, i.e., the list
of vertices that compose form the cycle. As such, we then provide a formally
verified certificate checker, that ensures the returned path is indeed a cycle.
    Our development differs only slightly from the original OCamlgraph pre-
sentation. Our proofs are modular, leveraging on the OCaml module system,
preserving a key aspect of the OCamlgraph library, i.e., its clear separation be-
tween algorithms and underlying graph data structures. Since Cameleer is under
active development, this work doubled as a stress test to the tool and represents
the largest Cameleer development to date. Our entire development (examples,
proofs, and proof sessions) is publicly available online on the project’s GitHub
page2 .
1
    https://github.com/backtracking/ocamlgraph
2
    https://github.com/dCastanho/algocameleer
                 Auto-active Verification of Graph Algorithms, Written in OCaml      3

     2   Cameleer in a nutshell

     As mentioned before, Cameleer is a code verification tool, specifically designed
     to prove OCaml code. It is built on top of Why3 [8], a set of tools to perform de-
     ductive verification of programs. Why3 comes with its own logic language, called
     Why, which is an extension of first-order logic (e.g. adds recursive definitions,
     algebric data types, inductive predicates), and its own programming language,
     called WhyML. A distinctive feature provided by this set of tools is that it
     allows the use of external solvers in its proofs.
         To use Cameleer, we attach GOSPEL [2] notation comments to our OCaml
     code and feed it to the tool. GOSPEL is a behavioral specification language for
     OCaml and it is designed to enable modular verification of data structures and
     algorithms. These comments represent the specification of our code and can
     contain constructs such as preconditions, post-conditions, variants, invariants.
     We can also define predicates and functions using GOSPEL comments, which
     come in handy during our proofs. Here is a small example of a function written
     in OCaml, with GOSPEL comments, which was proved using Cameleer:

1    (*@ open Power *)
2

3    let rec fast_exp x n =
4      if n = 0 then 1
5      else let r = fast_exp x (n / 2) in
6        if n mod 2 = 0 then r * r else r * r * x
7    (*@ r = fast_exp x n
8          requires 0 <= n
9          variant n
10         ensures r = x ^ n *)

         The function exemplified above shows a recursive and efficient way to com-
     pute a fast exponential, which uses some tricks to calculate the exponential using
     only O(log(n)) multiplications instead of O(n).
         Notice the comments started with a @ in the above code. These are the
     GOSPEL comments mentioned before and define the function’s specification,
     which in this case involves one precondition (the requires clause), one post-
     condition (the ensures clause), and one variant. We can also use external mod-
     ules in our proofs (though these modules can only be used in specifications) such
     as the Power module opened at the start of the proof, which allows the use of
     the ˆ symbol.
         Here, we tell our user, that if n is equal or greater than 0, then the result
     will be x to the power of n. Besides indicating what the purpose of the function
     is, we must assure that it is safe - as in, it does not get stuck in an infinite
     loop (recursive or otherwise). For this purpose we add the variant, a value that
     decreases with each call until it reaches a point where the loop ends.
         A small thing to keep in mind is that post-conditions can only be assumed
     to be true if the preconditions are also true when the function is called. For
4       Daniel Castanho and Mário Pereira




          Fig. 1. Visualization of the fast_exp.ml proof in the Why3 IDE


example, if we were to call fast_exp with a negative n, we could not expect the
result to be valid, since our call does not respect the precondition.
    Feeding a file to our tool is simple: after installing Cameeler one must simply
call the command cameleer <filename>.ml. A graphical interface will pop up,
in which all the methods with GOSPEL specification will be listed and can be
selected to be proven. When selected, it is also necessary to choose a theorem
prover already installed. In the case of our example we used Alt-Ergo3 , which
failed to complete the proof right away. Sometimes, it is necessary to split the
conditions of a specification using the command split_vc, which separates the
various conditions to try and prove them one by one, assuming the rest are
true. After this, Alt-Ergo quickly dispatched the proof of our little example. See
Figure 1 for a visualization of this example in the Why3 IDE.
    Cameleer is still in development at this point, and so it lacks compatibility
with some aspects of the core language, such as higher-order functions with side
effects or the inclusion of modules in other modules.


3     OCamlgraph

As aforementioned, OCamlgraph is a graph library written in OCaml. The first
notable aspect of this library is that it "does not provide a single data struc-
ture for graphs but many of them, enumerating all possible variations (19 alto-
gether)—directed or undirected graphs, persistent or mutable data structures,
user-defined labels on vertices or edges, etc.—under a common interface" [6].
This is possible due to OCaml’s flexible and powerful module system.
3
    https://alt-ergo.ocamlpro.com/
                 Auto-active Verification of Graph Algorithms, Written in OCaml       5

         This system offers special modules, called functors4 which are important for
     the second notable feature of this library: the separation of algorithms and data
     structures, meaning that algorithms are built independently from the underlying
     data structure. This makes it so, for instance, it does not matter how the vertices
     and edges are stored, as long as the necessary functions for using the algorithm
     are supplied in the functor’s argument.
         OCamlgraph provides a large level of abstraction with all its modules and
     makes using the library itself incredibly easy, especially since all the graphs end
     up having very similar signatures. However, analyzing the code behind it proved
     to be quite difficult because of this abstraction. Not only that, the existence
     of higher-order functors - functors that instead of returning a module, return
     another functor - was quite troublesome, not just for us who were inspecting
     the code, but for Cameleer itself, that was not prepared to handle things of
     the sort, as mentioned before. Because of this, we were forced to dial down the
     abstraction, creating a single functor that represented one structure, for each
     structure analyzed.

1    include Graph
2    include Path
3

4    module IntComparable = struct
5      type t = int
6      let compare a b = if a = b then 0 else if a < b then -1 else 1
7      let equal a b = a = b
8      let hash a = a
9      let default = 0
10   end
11

12   module DP = Persistent.Digraph.
13       ConcreteLabeled(IntComparable)(IntComparable)
14

15   module CheckPathDP = Path.Check(DP)
16   let () =
17     let g = DP.empty in
18     let g = DP.add_vertex g 1 in
19     ...
20     let g = DP.add_edge g 2 3 in
21     let finder = CheckPathDP.create g in
22     if CheckPathDP.check_path finder 1 3
23         then print_string "Path exists"
24         else print_string "Path does not exist"

         In the simple example shown above, we defined a module (IntComparable)
     that represents an integer, adhering to the COMPARABLE and ORDERED_TYPE_DFT
     signatures, so it can be used as our vertices and edge labels. Afterward, we
     4
         https://ocaml.org/manual/moduleexamples.html#s%3Afunctors
6        Daniel Castanho and Mário Pereira

instantiate our graph’s functor using the module we just defined. Since this
instantiated module adheres to the signature necessary for Path.Check, we can
simply feed it as an argument to the functor. With our modules ready, we can
start building our graph. Notice how each call to a function of DP returns a
new graph, this is what we call a persistent structure in OCamlgraph. There are
also imperative structures in OCamlgraph, which alter the structure in memory
and return unit. If we were to change the type of graph to be used in this
example, we would most likely not have to change anything in our code besides
the instantiating of the module DP - so long as the type of structure remained
the same - because the signatures across graphs are extremely similar.


4     Formally verified case studies

Over the course of this work, we proved four different modules. Two of them
represent data structure implementations: the first is an imperative, unlabeled
digraph5 and the second is a persistent, labeled graph6 . The other two consist
of algorithms over graphs: the first finds a cycle in a given graph7 , and the other
checks whether a path between two given vertices exists. We provide two imple-
mentations of this second algorithm: the first is the original implementation8 ,
and the second is an altered version, which was easier to prove and is slightly
more efficient9 . The two structures were selected to try and cover as many of
the available options for graphs (enumerated in Section 3) as possible, both
of which use concrete (and not abstract) values in their vertices and edges for
simplicity’s sake.
    In this section, we will present small segments of code regarding each module
and explanations about them. For our proofs, we used the following theorem
provers: Z310 , Alt-Ergo, CVC411 and EProver12 . Eprover is a slightly different
prover than the rest but proved itself to be extremely useful, as some proofs could
only be discharged by it. It is also possible to find some statistics regarding the
execution of the proofs in the Appendix.


4.1    Persistent Labeled Graph

As explained before, persistent structures are those where each function creates
a new version of the original structure and returns such version with the desired
change. One of the proved structures is of such kind. It also differs from the
other structure in its edges, where the other is unlabeled and directed. This one
5
   https://github.com/dCastanho/algocameleer/blob/main/proofs/imperative_unlabeled_digraph.ml
6
   https://github.com/dCastanho/algocameleer/blob/main/proofs/persistent_labeled_graph.ml
 7
   https://github.com/dCastanho/algocameleer/blob/main/proofs/find_cycle.ml
 8
   https://github.com/dCastanho/algocameleer/blob/main/proofs/path.ml
 9
   https://github.com/dCastanho/algocameleer/blob/main/proofs/altered_path.ml
10
   https://github.com/Z3Prover/z3
11
   https://cvc4.github.io
12
   https://wwwlehre.dhbw-stuttgart.de/~sschulz/E/E.html
                 Auto-active Verification of Graph Algorithms, Written in OCaml       7

     has generic labels on its edges and they are undirected, which means they go
     both ways. This structure is incorporated in the following module:

1    module PersistentLabeledGraph(Vertex: COMPARABLE)
2                                  (Edge: ORDERED_TYPE_DFT)

         The vertices and their operations are defined with the COMPARABLE signa-
     ture. However, the labels of edges also need to be represented, and for such,
     we use a functor with two arguments like shown above. The second argument
     is what we will use to represent our edges and their operations, through the
     ORDERED_TYPE_DFT signature, as follows:

1    module type COMPARABLE = sig
2      type t
3      val[@logic] compare : t -> t -> int
4      (*@ axiom pre_order : is_pre_order compare *)
5      val hash : t -> int
6      val equal : t -> t -> bool
7    end
8

9    module type ORDERED_TYPE_DFT = sig
10       type t
11       val [@logic] compare : t -> t -> int
12       (*@ axiom pre_order_compare: is_pre_order compare*)
13       val [@logic] default : t
14   end

         These signatures both contain a type and a way to compare elements from it,
     and any module that implements either one must have the represented functions.
     Notice the [@logic] tag associated to the compare and default functions -
     this tag means that these functions can be used in specifications. The compare
     function here is supposed to define an order between the elements of its signature.
     We guarantee this through the axiom inside GOSPEL comments, which indicates
     us that the compare function does represent an order and does not return random
     numbers (the predicate is_pre_order can be found in the standard GOSPEL
     library). This assurance is important because, without it, we could not assume
     anything related to the compare function. The definition and invariants of the
     graph itself are interesting subjects to present:

1    module HM = Map.Make(Vertex)
2

3    module VE = struct
4      type t = Vertex.t * Edge.t
5      let [@logic] compare (x1, y1) (x2, y2) =
6        let cv = V.compare x1 x2 in
7        if cv != 0 then cv else Edge.compare y1 y2
8      (*@ axiom pre_order_compare: is_pre_order compare*)
     8       Daniel Castanho and Mário Pereira

9    end
10

11   module S = Set.Make(VE)
12

13   type t = { self : S.t HM.t }
14   (*@ invariant forall v1. Set.mem v1 self.HM.dom ->
15       forall e. Set.mem e (self.HM.view v1).S.dom ->
16       let (v2, l) = e in
17         Set.mem v2 self.HM.dom /\
18         Set.mem (v1, l) (self.HM.view v2).S.dom *)
         Here, we introduce a module VE which is used for hashing of vertex and
     edge pairs. The graph itself is represented as an adjacencies list - each vertex
     has a set associated to it, representing its outgoing edges. Our sets contain pairs
     (Vertex.t, Edge.t) which store the destination and the label of the edge. This
     means parallel edges are allowed, as long as they have different labels.
         The type takes on the format of a record, however, originally, it was repre-
     sented as an alias type, type t = S.t HM.t. Because type invariants can only
     be applied to record types, we altered it. The invariant guarantees two things:
     that all the successors of a vertex also belong to the graph and that if there
     is an edge (v2, l) in v1’s adjacency list, then the edge (v1, l) exists in v2’s
     adjacency list. This captures the undirectness of the graph.
         In both our structures, we could have chosen to keep the graph type an alias
     type and not have assigned it an invariant. But to make sure these important
     invariants were maintained, we would have had to add them as pre and post-
     conditions to every function that manipulates the graph. We chose to add the
     invariant for two reasons: first, it is safer, as we do not run the risk of forgetting
     to add these conditions; secondly, it was a good opportunity to demonstrate how
     invariants are used and see how Cameleer would handle them in this situation.
         Most proofs in the structure were automatically discharged by at least one of
     our provers. However some times we were forced to interactively help it along in
     some more complicated assertions. An example of one such proof was in the case
     of the find_all_edges function, presented in Figure 2. No prover was able to
     conclude that every member of the list S.elements (HM.find v1 g.self) also
     belonged to the graph. This list represents the successors of the vertex v1 and
     so, according to our invariant, they must belong to the graph. By instantiating
     the invariant with the graph g and vertex v1 as well as the destruction of some
     logical implications (splitting the premise and the condition) Cameleer managed
     to reach this same conclusion.
         Despite many of the proofs being automatic, we had to add some lemmas that
     look very simple, because some times the provers were having hard time reach-
     ing those simple conclusions amidst the proof. When generalized, as a lemma,
     automatic theorem provers were quick to prove them correct. A small example
     is the eq_seq_list shown ahead, which simply states that all elements of a list
     are also represented on the sequence generated from it.
 1   (*@ lemma eq_seq_list : forall l :            (Vertex.t * S.t) list, e.
                  Auto-active Verification of Graph Algorithms, Written in OCaml      9




               Fig. 2. Visualization of the interactive proof for in the Why3 IDE


2                                   List.mem e l -> Seq.mem e (of_list l) *)


    4.2     Cycle finding
    One of OCamlgraph’s cycle detection routines is a function called has_cycle,
    which returns a Boolean, whether or not the graph has a cycle. Interestingly,
    one of the tasks on OCamlgraph’s to-do list, since around 2015, is updating this
    function to return the cycle that was found, instead of simply a Boolean. This
    led us to open a pull request on the OCamlgraph GitHub repository, where we
    propose to add a new function called find_cycle, inspired by has_cycle, which
    returned the cycle found in the form of a list13 .
        Given the complexity of the said find_cycle function, we decided to use
    it for a different kind of proof, one we call proof through a certificate. This
    kind of proof is useful when the function or program we are trying to prove is
    complex, but given the output of it, we can check whether that output is correct
    or not. And so, instead of proving the function itself, we construct a new support
    function, a certificate generator or witness validator so to say, which receives an
    output of the first function and tests whether it is correct, creating a certificate
    for it. Then we prove this support function is correct. However, we still prove
    that the find_cycle function is safe, i.e., it always terminates and does produce
    any exceptional behavior (e.g., unhandled raised exceptions).
        This is exactly what we did. After adding the new find_cycle function, we
    created a function that given a list and a graph, checks if that list represents
    a cycle in the graph. Finally, we proved this function did exactly that. An in-
    teresting feature of this kind of certificate proof, is that our support function
    13
         https://github.com/backtracking/ocamlgraph/pull/116
     10      Daniel Castanho and Mário Pereira

     is largely independent of the implementation of the cycle finder used, so long
     as the returned list is in the format we expect. As mentioned previously, all
     our algorithms are independent of a specific graph implementation, relying on
     receiving it as a module that adheres to a certain signature, as follows:

1    module type T = sig
2      val is_directed : bool
3      module V : COMPARABLE
4      type gt
5      (*@ model dom: V.t fset
6          model suc: V.t -> V.t fset
7          invariant forall v1, v2. Set.mem v1 dom /\
8            Set.mem v2 (suc v1) -> Set.mem v2 dom*)
9       val [@logic] succ : gt -> V.t -> V.t list
10      (*@ l = succ g v
11           requires Set.mem v g.dom
12           ensures forall v'. List.mem v' l -> Set.mem v' g.dom
13           ensures forall v'. List.mem v' l <-> Set.mem v' (g.suc v) *)
14     val all : gt -> V.t list
15     (*@ l = all g
16           ensures forall v. List.mem v l <-> Set.mem v g.dom *)
17   end

         Here, that signature requires the following: a module V that adheres to
     COMPARABLE and is used to represent the vertices of the graph; a type gt, which
     represents the type of our graph; a function succ, which given a graph and a
     vertex, returns its list of successors, and a function all, which given a graph
     returns a list of all its vertices. Originally, both functions provided higher-order
     iterators to iterate over these lists, but due to Cameleer’s current incompatibility
     with these, we changed them to return the lists so we could iterate over them
     manually.
         For our specification to make sense of what the gt type represents, we assign
     a model to it. In this case, our model consists of a finite set (fset) domain, which
     stores the vertices that belong to the graph and a succ function, that given a
     vertex, returns its successors set. This model is used to provide a specification
     of the functions of the signature.

1    let is_path v1 l v2 g =
2        let rec is_succ v = function
3            | [] -> false
4            | v' :: vs -> G.V.equal v' v || is_succ v vs
5        (*@ b = is_succ v l
6            variant l
7            ensures b <-> List.mem v l *)
8        in let rec iter_path = function
9            | [] -> assert false
                 Auto-active Verification of Graph Algorithms, Written in OCaml        11

10            | v' :: v'' :: vs -> is_succ (v'') (G.succ g v') &&
11                    iter_path (v'' :: vs)
12            | v' :: [] -> G.V.equal v' v2
13        (*@ b = iter_path l
14            requires l <> []
15            requires forall v. List.mem v l -> Set.mem v g.G.dom
16            variant l
17            ensures let s = of_list l in
18              b <-> (forall i. 0 <= i < List.length l - 1 ->
19               edge s[i] s[i+1] g) /\ s[List.length l - 1] = v2 *)
20        in match l with
21            | [] -> G.V.equal v1 v2
22            | x :: _ -> is_succ x (G.succ g v1) && iter_path l
23        (*@ b = is_path v1 l v2 g
24            requires Set.mem v1 g.G.dom
25            requires Set.mem v2 g.G.dom
26            requires forall v. List.mem v l -> Set.mem v g.G.dom
27            ensures b <-> is_path v1 (of_list l) v2 g *)

         Cycles, by definition, are paths from a vertex to itself. As such, the simplest
     way to define a cycle is to start by defining a path. The function demonstrated
     above receives a list and two vertices and tests whether the list represents a path
     from v1 to v2. The list itself, does not contain v1 but its last element must be
     v2. We make the verification by first checking whether the head of the list is a
     successor of v1. Then, we take each vertex from the list and check if the one
     that follows it (in the list) is one of its successors (this is done by the iter_path
     function). If the list is empty, then it means there are no other vertices involved,
     so it returns true if v1 and v2 are the same vertex.
         Our function has several preconditions, which can be summed up by saying
     that all vertices involved must belong to the graph, otherwise there is no doubt
     that it is not a path. The function assures us that the returned Boolean is
     equivalent to the one returned by the predicate of the same name, defined as
     follows:
 1   (*@ predicate edge (v1 : G.V.t) (v2 : G.V.t) (g : G.gt) =
 2           Set.mem v2 (g.G.suc v1) *)
 3

 4   (*@ predicate is_path (v1 : G.V.t) (l : G.V.t seq)
 5       (v2 : G.V.t) (g : G.gt) =
 6               let len = Seq.length l in
 7               if len = 0 then v1 = v2 else
 8                 edge v1 l[0] g && l[len - 1] = v2 &&
 9                 Set.mem v1 g.G.dom && forall i : int.
10                  0 <= i < len - 1 -> edge l[i] l[i+1] g *)
         It is easy to see a similarity between the two functions, however, the pred-
     icate can use the logical quantifier forall as well as operate directly over the
     12     Daniel Castanho and Mário Pereira

     model defined in the signature. This function was proved fully automatically by
     Cameleer, though it is still not the certificate creator we want. The certificate
     generator was defined as follows:

1    let is_cycle l g =
2        let rec get_last = function
3        | x :: [] -> x
4        | x :: xs -> get_last xs
5        | [] -> assert false
6        (*@ x = get_last l
7              variant l
8              requires l <> []
9              ensures List.mem x l
10             ensures x = (of_list l)[List.length l - 1] *)
11       in not (is_empty l) &&
12       let v = get_last l in is_path_func v l v g
13   (*@ b = is_cycle_func l g
14         requires forall v. List.mem v l -> Set.mem v g.G.dom
15         ensures b <-> is_cycle (of_list l) g *)

     Now we have to decide how a cycle would be stored in a single list. We ended
     up by choosing the simplest possible representation: given a list, it is a path
     from the last vertex to itself (though technically, there is a path from any of its
     vertices to itself). Given this way of storing cycles, an empty list represents the
     non-existence of a cycle (as in, empty lists cannot be cycles). The function above
     does exactly this verification, once again requiring all its members to be part of
     the graph.
 1    (*@ predicate is_cycle (l : G.V.t seq) (g : G.gt) =
 2         let len = Seq.length l in
 3         len <> 0 /\ is_path l[len - 1] l l[len - 1] g*)
         The predicate used to represent this is once again very similar to the actual
     function, simply calling is_path with the correct values. All these functions
     were proved to adhere to their specifications by Cameleer, meaning that given
     any function which supposedly returns a cycle, we can check whether their result
     is correct or not.
         Since this function is something the OCamlgraph developers have had in
     their to-do list for a while, we made a pull request to add our implementation
     of it to the library. We also raised an interesting point regarding cycle finding -
     in the case where a cycle is not found, returning a correct topological sort of the
     graph can also serve as proof that there are no cycles.


     4.3   Path checking

     For simple path checking between two vertices, OCamlgraph has a type and a
     function, where the type serves as a cache for previously searched values and the
                 Auto-active Verification of Graph Algorithms, Written in OCaml      13

    function uses breadth-first search to find the path between two given vertices, v1
    and v2. In this section we will be explaining the original version of the code14 .
        The implementation is simple but requires two support structures: a queue
    (called q) for vertices to check and a Hash table (called visited) for checked
    vertices. We start the algorithm by adding v1 to q. At each execution of the
    algorithm, we check if the queue is empty, if it is, we stop, returning false - as
    there are no more reachable vertices from v1 - if it is not, we pop the first value,
    v. If the popped value is equal to v2, we have found a path and return true, if
    not, we add v to visited and iterate over its successors, adding them all to the
    queue.
        There were several conditions to be treated as invariants over the execution
    of the algorithm, but due to the use of recursive functions instead of loops, these
    were adapted as pre and post-conditions. The definition of a path is defined just
    like in the previous subsection regarding cycles. However this time we will provide
    a more general definition, which instead of being asked if a given sequence is a
    path, simply checks if there exists such a path.
1    (*@ predicate has_path (v1 : G.V.t) (v2 : G.V.t) (g : G.gt) =
2               exists p : G.V.t seq. is_path v1 p v2 g *)
        Proving the path was found when the function returns true is easy, thanks
    to the invariant that states that the vertices in q are all connected to v1, which
    means if v2 is one of them (when popped), then there is a path between the two.
1    forall v'. Seq.mem v' q.Queue.view -> has_path v1 v' pc.graph
         Proving that when the function returns true, then there is a path, refers to
    the correctness of it, while returning false (instead of unsure, for example) when
    there is no path, refers to its completeness. This last one proved to be much
    more difficult than the first.
         In our algorithm, if q is empty when we start a loop, it means there are no
    more reachable vertices, and so, there is no path between v1 and v2. From a
    programming point of view, this train of thought is natural but logically proving
    it is a different story. The following invariant is how we prove that if the queue
    is empty, then there is no path:
1   has_path v1 v2 pc.graph ->
2       exists w. Seq.mem w q.Queue.view /\ has_path w v2 pc.graph /\
3         not (Set.mem w visited.HV.dom)
        Because if there is a path, then there must be an intermediate unvisited
    vertex in the queue and if there are no more vertices in the queue, this can’t
    happen. With such a property in hand, we were able to prove the completeness
    of the function.
        However, proving this specific condition was not done automatically and
    before we did so we needed an extra invariant.
1    forall v. Set.mem v visited.HV.dom ->
    14
         https://github.com/backtracking/ocamlgraph/blob/master/src/path.ml
    14       Daniel Castanho and Mário Pereira

2         forall s. edge v s pc.graph ->
3             Seq.mem s q.Queue.view \/ Set.mem s visited.HV.dom
        This means that if a vertex is visited, then all its children have either been
    visited or are in the queue. Cameleer easily proved this condition and we pro-
    ceeded to the proof of the previous one, doing so through a case by case analysis:
     1. If v2 is in the queue, then it is easily proven, as it is the vertex we are looking
        for. The condition has_path v2 v2 trivially holds.
     2. If v2 is not in the queue, then we know v1 is in visited, because v1 is the
        first vertex to be popped. So we know that the there is a path from inside
        the visited set (v1) to outside of it (v2) . This path takes an edge v→w,
        where v is in visited and w is in the queue, but not in visited, and is exactly
        the vertex we’re looking for.
         To prove this last case we required the aid of the following ghost function:
    let [@ghost] [@logic] rec intermediate_value p
        (u : G.V.t) (v : G.V.t) ( s : G.V.t list) ( g : G.gt) =
          match s with
          | [] -> assert false
          | x :: xs -> if not (p x) then (u, x, [], xs) else
           let (u', v', s1, s2) = intermediate_value_func p x v xs g
           in (u', v', x::s1, s2)
    (*@ (u', v', s1, s2 ) = intermediate_value p u v s g
        requires p u /\ not (p v) /\ is_path u (of_list s) v g
        variant s
        ensures p u' /\ not (p v') /\ is_path u s1 u' g
        ensures is_path v' s2 v g /\ edge u' v' g *)
        Given a certain property p, which takes the form of a Boolean function, two
    vertices, a list representing their path, and the graph where they belong to, it
    will find the edge in the path which starts in a vertex that respects p and ends
    in a vertex which does not.
        If we instantiate this function with our values v1, v2, our graph, the path used
    by has_path and p = fun x -> Set.mem x visited.HM.dom, it will search for
    the vertex w referred in the second case. We know this vertex will be in the
    queue, because we if v (from the edge v→w) is visited, then all its children are
    either visited or in the queue. If w is not visited, then it must be in the queue.
        Because our path definition uses sequences and not OCaml lists , to be able
    to use this function in our proof correctly (it uses lists and not sequences because
    sequences are not an OCaml construct but a GOSPEL one), we had to create the
    following auxiliary lemma.
1        (*@ lemma intermediate_value :
2        forall p : (G.V.t -> bool), u, v : G.V.t, s : G.V.t seq, g : G.gt.
3          p u -> not p v -> is_path u s v g ->
4            exists u' v' s1 s2. p u' /\ not p v' /\
5               is_path u s1 u' g /\ is_path v' s2 v g /\ edge u' v' g *)
             Auto-active Verification of Graph Algorithms, Written in OCaml   15




         Fig. 3. Visualization of the proof of completeness in the Why3 IDE


    This lemma was what ultimately helped us conclude the proof of complete-
ness and the function explained before was used to prove this lemma. See Figure
3 for a visualization of the proof of the condition in the Why3 IDE.

An alternative method. The way this function is written makes it so the queue
and the visited table have overlapping vertices, which forces us to refer to the
unvisited but reached vertices by the difference of these two. Not only that, it
makes it so the queue might have repeated values and can possibly grow to have
more vertices than there are in the graph. We propose an alternative imple-
mentation that avoids both of these issues: we made visited a ghost structure
and added in a new Hash table by the name of marked; then, instead of adding
successors to the queue with no verification, we first check whether that vertex
has been marked or not. If it has, we simply move on to the next successor; if
it hasn’t, we mark it and add it to the queue; on pop vertices are still added
to visited. This means that visited and q are disjoint and that all the values
in q are distinct. This implementation was also fully proved in Cameleer, with a
simpler completeness proof, given the separation of the values in visited and q


5      Related work
Given the importance of graphs, it makes sense that formal verification of al-
gorithms over graphs is not new. For example, the Why3 gallery of verified
programs contains a small section specifically for graph algorithms15 , including
a breadth-first search such as the one we proved. There are differences, however,
such as the fact that their proof was made in WhyML, Why3’s programming
15
     http://toccata.lri.fr/gallery/graph.en.html
16     Daniel Castanho and Mário Pereira

language, and ours was made in OCaml. Not to mention that our proof was taken
from already written code, instead of a proof-oriented implementation.
    Another example of verified graph algorithms is [15] in which the authors
prove some classic algorithms written in C. The implementations proved in this
particular work were taken from textbooks and included the verification of heaps
and other support structures, along with the rebuttal of some common notions
like how Prim’s Algorithm requires a connected graph.
    In [3] we can find proofs for Tarjan’s strongly connected components algo-
rithm, proved with three different provers: Isabelle/HOL, Coq and Why3.
    Alkassar et al. [1] adjust graph algorithms to produce witnesses that can be
then used by verified validators to check whether the result is correct, similarly
to how we create a certificate and validators for our cycle finding.
    Several other works about formal and informal proof of graph algorithms
and/or programs exist [18,22,13,14,21,19,12,4]. Some focus on the correct treat-
ment of pointers or concurrent structures while other are part of larger libraries.
    As far as we are aware, there is no OCaml graph library currently verified and
we found no works on the correctness of graph structures, only their algorithms.


6    Conclusion and Future work

We presented our verification effort of data structures and algorithms, taking
inspiration from the OCamlgraph library. These proofs were entirely conducted
using the Cameleer tool, with a high-degree of proof automation. We believe our
formal development is an important milestone in the effort of bringing (auto-
mated) verification techniques into real-world software written in OCaml.
    This work led us to extend Cameleer with new features, namely the treatment
for functors instantiation. However, in the grand scheme of things, the subset of
the library we proved is rather small. We intend to keep evolving Cameleer to
handle a larger set of OCaml programs. As such, our plan for the future involves
expanding on both of these topics. Proving more algorithms, like the classic
Prim’s algorithm, and structures, like graphs that use abstract values instead of
concrete ones, will increase the verified subset of the OCamlgraph library. By
adding the ability to handle higher-order iterators to Cameleer, we will fix one of
its major flaws and biggest source of incompatibility with real, already written
code. This last one is complicated, but not impossible, since these iterators are
closely related to classic for each cycles. Following such a route, would allow
us to modularly reason about iteration, as presented by Filliâtre and Pereira [9].
From a practical point of view, this means extending Cameleer with the ability
to identify higher-order iterators and convert them to a piece of WhyML code
that uses its enhanced for loop.


Acknowledgments. We thank António Ravara for his remarks and fruiftul dis-
cussions on draft versions of this paper.
             Auto-active Verification of Graph Algorithms, Written in OCaml          17

References
 1. Alkassar, E., Böhme, S., Mehlhorn, K., Rizkallah, C.: A framework for the ver-
    ification of certifying computations. J. Autom. Reason. 52(3), 241–273 (2014),
    https://doi.org/10.1007/s10817-013-9289-2
 2. Charguéraud, A., Filliâtre, J., Lourenço, C., Pereira, M.: GOSPEL - providing
    ocaml with a formal specification language. In: Proceedings of the Third World
    Congress - The Next 30 Years - Formal Methods. Lecture Notes in Computer
    Science, vol. 11800, pp. 484–501. Springer (2019), https://doi.org/10.1007/
    978-3-030-30942-8_29
 3. Chen, R., Cohen, C., Lévy, J., Merz, S., Théry, L.: Formal proofs of tarjan’s
    algorithm in why3, coq, and isabelle. CoRR abs/1810.11979 (2018), http:
    //arxiv.org/abs/1810.11979
 4. Chen, R., Lévy, J.: A semi-automatic proof of strong connectivity. In: Paskevich,
    A., Wies, T. (eds.) Verified Software. Theories, Tools, and Experiments - 9th In-
    ternational Conference, VSTTE 2017, Heidelberg, Germany, July 22-23, 2017, Re-
    vised Selected Papers. Lecture Notes in Computer Science, vol. 10712, pp. 49–65.
    Springer (2017), https://doi.org/10.1007/978-3-319-72308-2_4
 5. Conchon, S., Filliâtre, J., Signoles, J.: Designing a generic graph library using ML
    functors. In: Morazán, M.T. (ed.) Proceedings of the Eighth Symposium on Trends
    in Functional Programming, TFP 2007, New York City, New York, USA, April 2-4.
    2007. Trends in Functional Programming, vol. 8, pp. 124–140. Intellect (2007)
 6. Conchon, S., Filliâtre, J., Signoles, J.: Designing a generic graph library using
    ML functors. In: Proceedings of the Eighth Symposium on Trends in Functional
    Programming. Trends in Functional Programming, vol. 8, pp. 124–140. Intellect
    (2007)
 7. Cook, B.: Formal reasoning about the security of amazon web services. In: Chock-
    ler, H., Weissenbacher, G. (eds.) Computer Aided Verification. pp. 38–47. Springer
    International Publishing, Cham (2018)
 8. Filliâtre, J.C., Paskevich, A.: Why3 — Where Programs Meet Provers. In: Pro-
    gramming Languages and Systems. pp. 125–128. Springer Berlin Heidelberg (2013)
 9. Filliâtre, J.C., Pereira, M.: A modular way to reason about iteration. In:
    Rayadurgam, S., Tkachuk, O. (eds.) 8th NASA Formal Methods Symposium. Lec-
    ture Notes in Computer Science, vol. 9690. Springer, Minneapolis, MN, USA (Jun
    2016)
10. de Gouw, S., Rot, J., de Boer, F.S., Bubel, R., Hähnle, R.: Openjdk’s
    java.utils.collection.sort() is broken: The good, the bad and the worst case. In:
    Proceedings of the 27th International Conference on Computer Aided Verifica-
    tion. Lecture Notes in Computer Science, vol. 9206, pp. 273–289. Springer (2015),
    https://doi.org/10.1007/978-3-319-21690-4_16
11. Hoare, C., Misra, J., Leavens, G.T., Shankar, N.: The verified soft-
    ware initiative: A manifesto. ACM Comput. Surv. 41(4) (Oct 2009).
    https://doi.org/10.1145/1592434.1592439
12. Hobor, A., Villard, J.: The ramifications of sharing in data structures. In: Gia-
    cobazzi, R., Cousot, R. (eds.) The 40th Annual ACM SIGPLAN-SIGACT Sympo-
    sium on Principles of Programming Languages, POPL ’13, Rome, Italy - January
    23 - 25, 2013. pp. 523–536. ACM (2013), https://doi.org/10.1145/2429069.
    2429131
13. Lammich, P., Neumann, R.: A framework for verifying depth-first search algo-
    rithms. Arch. Formal Proofs 2016 (2016), https://www.isa-afp.org/entries/
    DFS_Framework.shtml
18      Daniel Castanho and Mário Pereira

14. Mehta, F., Nipkow, T.: Proving pointer programs in higher-order logic. Inf. Com-
    put. 199(1-2), 200–227 (2005), https://doi.org/10.1016/j.ic.2004.10.007
15. Mohan, A., Leow, W.X., Hobor, A.: Functional correctness of c implementations of
    dijkstra’s, kruskal’s, and prim’s algorithms. In: Silva, A., Leino, K.R.M. (eds.) Com-
    puter Aided Verification. pp. 801–826. Springer International Publishing (2021)
16. O’Hearn, P.W.: Continuous Reasoning: Scaling the Impact of Formal Methods.
    In: Symposium on Logic in Computer Science. p. 13–25. IEEE (2018), 10.1145/
    3209108.3209109
17. Pereira, M., Ravara, A.: Cameleer: A Deductive Verification Tool for OCaml.
    In: Silva, A., Leino, K.R.M. (eds.) Computer Aided Verification - 33rd In-
    ternational Conference, CAV 2021, July 20-23, Proceedings, Part II. Lec-
    ture Notes in Computer Science, vol. 12760, pp. 677–689. Springer (2021).
    https://doi.org/10.1007/978-3-030-81688-9_31
18. Poskitt, C.M., Plump, D.: Hoare-style verification of graph programs. Fundam.
    Informaticae 118(1-2), 135–175 (2012), https://doi.org/10.3233/FI-2012-708
19. Raad, A., Hobor, A., Villard, J., Gardner, P.: Verifying concurrent graph al-
    gorithms. In: Igarashi, A. (ed.) Programming Languages and Systems - 14th
    Asian Symposium, APLAS 2016, Hanoi, Vietnam, November 21-23, 2016, Pro-
    ceedings. Lecture Notes in Computer Science, vol. 10017, pp. 314–334 (2016),
    https://doi.org/10.1007/978-3-319-47958-3_17
20. Régis-Gianas, Y., Pottier, F.: A Hoare Logic for Call-by-Value Functional Pro-
    grams. In: International Conference on Mathematics of Program Construction
    (MPC) (Jul 2008), http://dx.doi.org/10.1007/978-3-540-70594-9_17
21. Sergey, I., Nanevski, A., Banerjee, A.: Mechanized verification of fine-grained
    concurrent programs. In: Grove, D., Blackburn, S.M. (eds.) Proceedings of the
    36th ACM SIGPLAN Conference on Programming Language Design and Im-
    plementation, Portland, OR, USA, June 15-17, 2015. pp. 77–87. ACM (2015),
    https://doi.org/10.1145/2737924.2737964
22. Wegener, I.: A simplified correctness proof for a well-known algorithm computing
    strongly connected components. Inf. Process. Lett. 83(1), 17–19 (2002), https:
    //doi.org/10.1016/S0020-0190(01)00306-4
             Auto-active Verification of Graph Algorithms, Written in OCaml   19

A     Statistics

A.1    Computer and Environment specs
 – 16 GB of RAM
 – AMD Ryzen 5 1600 Six-Core Processor 3.20 GHz
 – Executed inside WSL 2.0 in Windows 10 64x, with an Ubuntu 20.04 LTS
   distribution
 – Why3 setup to have up to 5 processes running at once

A.2    imperative_unlabeled_digraph.ml

Number of root goals. Total: 22 Proved: 22

Number of sub goals. Total: 79 Proved: 79

Replay time. 7 executions timed, removed maximum and minimum. Statistics
bellow are from the leftover 5 tests.


 Minimum         Maximum     Average
 0m15.768s       0m16.276s   0m16.001s




Statistics per prover.


Prover            Number of Proofs Minimum (s) Maximum (s) Average (s)
Eprover 2.5       27               0.03        2.44        0.24
Alt-Ergo 2.4.0    75               0.00        4.67        0.15
Z3 4.8.7          27               0.01        4.47        0.92
CVC4 1.6          40               0.06        0.25        0.12
20      Daniel Castanho and Mário Pereira

A.3    persistent_labeled_graph.ml

Number of root goals. Total: 28 Proved: 28

Number of sub goals. Total: 219 Proved: 219

Replay time. 7 executions timed, removed maximum and minimum. Statistics
bellow are from the leftover 5 tests.


 Minimum      Maximum      Average
 0m24.661s    0m24.898s    0m24.769s




Statistics per prover.


Prover          Number of Proofs Minimum (s) Maximum (s) Average (s)
Eprover 2.5     67               0.02        6.46        0.60
Alt-Ergo 2.4.0 179               0.01        4.71        0.13
Z3 4.8.7        55               0.01        0.22        0.07
Z3 4.8.7 (noBV) 30               0.01        0.13        0.05
CVC4 1.6        101              0.07        4.33        0.29
             Auto-active Verification of Graph Algorithms, Written in OCaml   21

A.4    find_cycle.ml

Number of root goals. Total: 9 Proved: 9

Number of sub goals. Total: 78 Proved: 78

Replay time. 7 executions timed, removed maximum and minimum. Statistics
bellow are from the leftover 5 tests.


 Minimum         Maximum     Average
 0m18.572s       0m19.298s   0m18.809s




Statistics per prover.


Prover            Number of Proofs Minimum (s) Maximum (s) Average (s)
Eprover 2.5       2                0.13        0.15        0.14
Alt-Ergo 2.4.0    66               0.01        1.73        0.07
CVC4 1.6          6                0.11        23.71       6.86
22      Daniel Castanho and Mário Pereira

A.5    path.ml

Number of root goals. Total: 14 Proved: 14

Number of sub goals. Total: 223 Proved: 223

Replay time. 7 executions timed, removed maximum and minimum. Statistics
bellow are from the leftover 5 tests.


 Minimum         Maximum     Average
 0m22.797s       0m22.933s   0m22.860s




Statistics per prover.


Prover            Number of Proofs Minimum (s) Maximum (s) Average (s)
Eprover 2.5       70               0.02        3.22        0.24
Alt-Ergo 2.4.0    165              0.01        3.85        0.19
Z3 4.8.7          54               0.01        0.13        0.05
CVC4 1.6          75               0.04        5.33        0.29
             Auto-active Verification of Graph Algorithms, Written in OCaml   23

A.6    altered_path.ml

Number of root goals. Total: 15 Proved: 15

Number of sub goals. Total: 325 Proved: 325

Replay time. 7 executions timed, removed maximum and minimum. Statistics
bellow are from the leftover 5 tests.


 Minimum         Maximum     Average
 0m29.238s       0m30.095s   0m29.565s




Statistics per prover.


Prover            Number of Proofs Minimum (s) Maximum (s) Average (s)
Eprover 2.5       104              0.03        4.27        0.25
Alt-Ergo 2.4.0    230              0.01        2.00        0.13
Z3 4.8.7          90               0.01        4.10        0.21
CVC4 1.6          97               0.07        3.56        0.25
