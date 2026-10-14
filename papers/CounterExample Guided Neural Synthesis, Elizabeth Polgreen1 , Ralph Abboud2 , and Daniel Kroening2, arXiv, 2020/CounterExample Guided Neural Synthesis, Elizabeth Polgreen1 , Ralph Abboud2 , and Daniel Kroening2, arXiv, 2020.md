                                              CounterExample Guided Neural Synthesis

                                                   Elizabeth Polgreen1 , Ralph Abboud2 , and Daniel Kroening2
                                                                  1
                                                                      University of California, Berkeley
                                                                          2
                                                                            University of Oxford
arXiv:2001.09245v1 [cs.LO] 25 Jan 2020




                                               Abstract. Program synthesis is the generation of a program from a
                                               specification. Correct synthesis is difficult, and methods that provide
                                               formal guarantees suffer from scalability issues. On the other hand, neural
                                               networks are able to generate programs from examples quickly but are
                                               unable to guarantee that the program they output actually meets the
                                               logical specification. In this work we combine neural networks with formal
                                               reasoning: using the latter to convert a logical specification into a sequence
                                               of examples that guides the neural network towards a correct solution, and
                                               to guarantee that any solution returned satisfies the formal specification.
                                               We apply our technique to synthesising loop invariants and compare the
                                               performance to existing solvers that use SMT and existing techniques that
                                               use neural networks. Our results show that the formal reasoning based
                                               guidance improves the performance of the neural network substantially,
                                               nearly doubling the number of benchmarks it can solve.


                                         1    Introduction

                                         Program synthesis is the task of automatically generating a program from a
                                         given specification. In its most general form, program synthesis is complex,
                                         and scalable implementation is a challenge. Existing methods typically combine
                                         heuristic search of the space of programs together with an SMT solver that asserts
                                         formally that the candidate program satisfies the specification; a well-known
                                         instance is the CEGIS loop [31]. The key idea of syntax-guided synthesis (SyGuS)
                                         is to ameliorate the scalability issue by imposing restrictions on the search space
                                         by means of a syntactic template provided by the user [4].
                                             In parallel to these developments, machine learning is now known to be able to
                                         solve the program synthesis problem effectively for a particular special case: deep
                                         neural networks can be trained to produce string manipulation programs given
                                         a set of examples of inputs and the desired program outputs [13]. While these
                                         approaches are fast, fully specifying a non-trivial program using input-output
                                         examples only is hard [28], and thus, effective search for a program that provably
                                         satisfies a given logical specification remains an open problem.
                                             In this paper we present two new algorithms that combine formal reasoning
                                         using SAT/SMT solvers with a deep neural network in order to generate programs
                                         that provably satisfy a full logical specification. The first algorithm, Example-
                                         Guided Neural Synthesis, comprises of three steps: 1) we use SMT to convert
                                         the given logical specification into a set of input-output examples; the goal is to
2

generate a set that captures as much of the specification as possible; 2) we use
the neural network to generate candidate programs from the set of input-output
examples; 3) finally, we use SMT to verify whether any of the candidate programs
returned by the network meets the specification. If the network does not return
a correct program, we terminate with no answer.
    We observe that the performance of the neural network is highly dependent
on the quality of the input-output examples provided. We therefore hypothesise
that the neural network might benefit from a refined set of input-output examples.
Thus, the second algorithm, CounterExample Guided Neural Synthesis (CEGNS),
integrates the first algorithm into a CEGIS loop, extracting counterexamples
when the programs generated by the neural network fail to meet the specification,
and using these counterexamples to generate input-output examples. The loop
iterates until the neural network generates a correct program. The loop is not
guaranteed to terminate.
    We evaluate our algorithms using a neural network trained to synthesise
predicates from input-output examples. It is potentially possible to extend our
approach to functions returning bit vectors, or to other logics, though further
network designs need to be explored. We evaluate our algorithms on invariant
synthesis benchmarks from the synthesis competition. The key finding is that
the counterexample guidance significantly increases the performance of the
neural network: CEGNS nearly doubles the number of benchmarks that the
neural network can solve on its own. Overall, CEGNS performs comparably to
a conventional CEGIS implementation [1], but solving a different subset of the
benchmarks.
    The paper is structured as follows: Sections 3 and 4 introduce the architecture
of the neural networks we build our algorithms around, and describes how we
train them; Section 5 and 6 present Example Guided Neural Synthesis and
CounterExample Guided Neural Synthesis; Section 7 describes the experimental
setup, and presents the experimental results; Section 8 discusses related work.


2     Preliminaries

2.1   Program Synthesis

Program synthesis tools solve a second-order existential logic problem that can
be formulated as follows: ∃P. ∀x. σ(P, x) where P ranges over functions, which
are represented by means of programs, x is a ground term corresponding to the
input arguments for the target program, and σ is a quantifier-free formula that
represents the properties that must be satisfied by the program to meet the user’s
specification.
    There are many problems that can be expressed as synthesis problems of the
form above. As an exemplar, we consider the problem of synthesising an invariant
for a given loop. Let x denote a program state, I denote the predicate for the
initial condition, A an assertion, and T a transition relation. Using the criteria
of the invariant track in the SyGuS competition, a predicate P is an invariant if
                                                                                    3

                                                 UNSAT
                             synthesise                      no solution




                             SAT
                        P∗                   c




                                       SAT
                                                 UNSAT
                               verify                        solution P ∗


                             Fig. 1. CEGIS block diagram


it is a model for the following formula:

    ∃P ∀x, x0 .(I(x) ⇒ P (x)) ∧ (P (x) ∧ T (x, x0 ) ⇒ P (x0 )) ∧ (P (x) ⇒ A(x)).


2.2    CounterExample Guided Inductive Synthesis

CounterExample-Guided Inductive Synthesis (CEGIS), illustrated in Fig. 1, is
an iterative process consisting of two phases: a synthesis phase and a verification
phase. Given the specification σ of the desired program, the inductive synthesis
procedure generates a candidate program P ∗ that satisfies σ(P ∗ , x) for a subset
xinputs of all possible inputs. The candidate program P ∗ is passed to the verifi-
cation phase, which checks whether it satisfies the specification σ(P ∗ , x) for all
possible inputs. This is done by checking whether ¬σ(P ∗ , x) is unsatisfiable. If so,
then ∀x.σ(P ∗ , x) is valid, and we have successfully synthesised a solution and
the algorithm terminates. Otherwise, the verifier extracts a counterexample c
from the satisfying assignment, which is then added to the set of inputs passed
to the synthesiser, and the loop reiterates.
    The verification phase is typically implemented using a SAT or a SMT solver.
There is a wide range of options for the inductive synthesis component; a popular
choice is heuristic enumeration in combination with an SMT solver [5]; another
is synthesis using a SAT solver [31]. A well-known limitation of enumeration-,
SAT- and SMT-based techniques is their inability to synthesise constants that
are not given as part of the problem description, which can potentially result in
an inefficient enumeration of the search space.


3     Neural Networks for Synthesising Programs

A neural network consists of a set of neurons that aggregate input values using
a weighted linear combination and a non-linear activation function to return a
single output. The output of a neuron with k inputs is
                                       k
                                   f (Σi=1 (wi · xi ) + b)

where wi denotes the weight for the ith input, xi denotes the value of the ith
input, b denotes the bias and f is the non-linear activation function.
 4

     The input to the neural network in our algorithms is a set of multiple I/O
examples. An I/O example is an assignment to the input parameters of the function
 to be synthesised and a corresponding correct output. The input parameters are
 bitvectors of width 32, and we feed the network both the binary representation
 of the bitvector and the decimal representation of the value normalised to be
 between −1 and 1. The output assignment in each example is a Boolean value.
 Discrete values are represented using an embedding that maps them to real
 numbers. The use of such embedding functions is standard.
     The output of the neural network is a candidate program, represented as a
 sequence of program tokens. The network has a vocabulary of 50 possible program
 tokens, 16 of which are used to represent constants, and the remaining 34 represent
 program instructions, parentheses, and indicators for “start of program” and
“end of program”.
     We empirically explored a variety of neural network architectures. We de-
 scribe a simple network to illustrate our ideas, and a more complex network
with similar architecture to that used in neural program synthesis for string
 manipulation programs [13]. The simple network fails to solve any but the most
 trivial benchmarks (e.g., where true is a sufficiently strong invariant), and so our
 experimental work uses the complex network.


 3.1      Network 1 – A Simple Network



                                                                     arg-
                                                                     max    token 1
 input i
                                                                     arg-
     arg. 1
     arg. 2   ReLU     ReLU       max        ReLU      ReLU
              layer    layer                 layer     layer          ..
     arg. 3                       pool                                 .
              (256)    (128)                 (512)     (5000)
output i
                                                                     arg-
                                                                     arg-
                                                                     max    token 100
      I/O example encoding     aggregation        program decoding



                         Fig. 2. Network 1: the simple network


     Network 1 is a simple feed-forward neural network. In a feed-forward network,
 neurons are organised into layers, where all neurons in a layer have access to the
 same inputs; however, each neuron has its own set of weights. Information in a
 feed-forward network flows forward through these layers, such that the output
 of a layer is the input for the next. No recurrence is used, and thus no neuron
 is used more than once in the computation of the network’s output. Owing to
 this structure, feed-forward architectures can only processes data sequences of
                                                                                 5

bounded length. Data given to feed-forward networks must be preprocessed to
fixed length.
    We set up Network 1 such that it synthesises functions with up to three input
parameters: any missing input parameters are filled with padding data. The
padding data is a learnable variable of the network: it can thus learn a value that
best encodes the non-existence of the corresponding parameter. Network 1, given
in Fig. 2, consists of

 1. a feed-forward network for encoding;
 2. a max-pooling operation aggregating the encodings for each input-output
    example;
 3. a feed-forward network for decoding.

All feed-forward network layer neurons use a ReLU activation function, which is
max{0, x}. This activation function is commonplace [17]. The encoder processes
an I/O example as follows: it concatenates the inputs and the output into a
single vector. This vector is fed into a feed-forward network with two neuron
layers; a first is a hidden layer and the second is the output layer. The output
of this network is a vector of floating-point values called the encoding, which
summarises the I/O example the network is given.
    To process multiple I/O examples, the encoder network is applied separately
to each example, and so produces an encoding for each example. These encodings
are aggregated using the max-pooling operation, which combines the encodings
by taking the maximum value from each element of the vector. The output O of
the max pooling operation applied to k encodings is computed as follows:

                               O[j] = max Enc i [j]
                                      1≤i≤k


where Enc i [j] is the j th dimension of the ith encoding vector. The max pooling
operator is chosen based on its successful use in [13, 27]. Using pooling, the
network can process an arbitrary number of I/O examples by computing the
encoding using the encoder network and consolidating all encodings via the
pooling operation.
    The decoder is another feed-forward network with two neuron layers. The
decoder accepts the aggregated encoding as input, and maps this to a sequence of
program tokens. The final layer of this network contains 5000 neurons, which can
represent programs of up to 100 tokens long, using our vocabulary of 50 tokens.
Each block of 50 neurons generates a single token. We use the softmax function
to convert these floating-point outputs into a discrete probability distribution
over the vocabulary for each token. The final program is computed as the most
likely token obtained from each block of 50 neurons, with the exception of the
first token, which yields the “end of program” symbol.
    This neural network architecture can scale to an arbitrary number of I/O
examples, while also being very fast to run and train due to its feed-forward
structure. However, it lacks representational power. For instance, the decoder
network does not explicitly enforce a dependence between distinct program tokens
6

dictated by its output, whereas this dependency is evident in programs, e.g., the
token “bvgt” is often followed by a constant. Furthermore, the network does
not explicitly account for the order of input parameters, which is critical for
non-commutative program synthesis.


3.2   Network 2 – A Complex Network

Recurrent Neural Networks(RNNs) are designed to recognise patterns in sequences
of data, and have a temporal dimension. Information is cycled in a loop through
the network, and the decision a recurrent network reached at time step t − 1
affects the decision it will reach at the next time step. This memory allows the
network to find correlations between events that are separated by many moments
in time, and means that they can consider sequences of variable length. This
ability to consider a sequence of arbitrary length enables us to consider programs
with arbitrary numbers of input parameters. Network 2 is based on a recurrent
neural network.
    Long-Short Term Memory (LSTM) cells [20] allow RNNs to learn patterns
from sequential data more efficiently, in particular with respect to long-term
dependencies [8]. LSTM cells compute a state representation at every time step of
an input sequence which describes the information it has processed thus far. This
state is represented using two vectors: the cell state and the hidden state. The cell
state serves as memory to retain knowledge over time, while the hidden state is
primarily used to produce the cell’s output. LSTM cell states are updated using
a combination of linear operations (e.g., multiplication and summation), which
are easily differentiable and whose gradient does not decay over time, unlike
most non-linear activations. This helps the network retain information over a
larger number of time steps. An LSTM can be conditioned on the output of a
previous cell by using the final cell state and hidden state of the previous cell as
the current cell’s initial hidden state and cell state. Network 2, shown in Fig. 3,
consists of, for each input-output example:

 1. an input encoder LSTM recurrent network, which receives the input pa-
    rameter values from the input-output pair, fed in sequentially;
 2. an output encoder LSTM cell, which receives the Boolean output embed-
    ding value from the input-output pair and is conditioned on the final cell and
    hidden states of the input encoder network;
 3. a decoder LSTM recurrent network, which is trained on the target pro-
    gram and conditioned on the final output encoder state.

This is a typical architecture for sequence-to-sequence networks [33].
    The final program is obtained by aggregating the outputs of the decoders
using pooling. We then use either greedy decoding on the output of the pooling,
similar to Network 1, or Beam Search, which is a compromise between performing
a time-consuming complete search to find the optimal output sequence and
performing a speedy but sub-optimal greedy decoding. Beam search returns k
output sequences, where k is referred to as the beam size. Beam search computes
                                                                                                                                                                                                7

                                                                                                        Output
                                                      Input Encoder                                                                 Synthesis Decoder
                                                                                                        Encoder
                     LSTM Cell 1                                                                        LSTM Cell 2   LSTM Cell 3

  Input /
  Output
 Example 1
             c0


             h0       II
                           σ1   σ2   tanh σ3
                                               tanh
                                                      c1


                                                      h1
                                                                        c2


                                                                        h2
                                                                             ...
                                                                               ck­1


                                                                               hk­1
                                                                                                   ck


                                                                                                   hk
                                                                                                                             o11            o21
                                                                                                                                                    ...     oP1
                                                                                                                                                                         o(P+1)1

                    Input 1                                  Input 1                    Input 1           Output 1    GO              Program                     Program
                  Argument 1                               Argument 2                 Argument k           Value                      Token 1                     Token p


  Input /
  Output
 Example 2
             c0


             h0
                                                                             ...                                             o12            o22
                                                                                                                                                    ...     oP2
                                                                                                                                                                         o(P+1)2

                     Input                                   Input 2                    Input 2           Output 2    GO              Program                     Program
                  Argument 1               ...             Argument 2                 Argument k           Value                      Token 1                     Token p




                                                                                   ...

                                                                                                        ...



                                                                                                                                                ...
  Input /
  Output
 Example n
             c0


             h0
                                                                             ...                                            o1N             o2N
                                                                                                                                                    ...    oPN
                                                                                                                                                                     o(P+1)N

                    Input n                                  Input n                    Input n           Output 3    GO              Program                     Program
                  Argument 1                               Argument 2                 Argument k           Value                      Token 1                     Token p



                                                                                                                                      Pooling        Pooling                          Pooling
                                                                                                                                       Block          Block        ...                 Block


                                                                                                                                    Output Token   Output Token
                                                                                                                                                                                   Output Token P
                                                                                                                                         1              2




                                                              Fig. 3. Network 2: the complex network


the set of k likely candidate sequences at each time step until all k candidates
have reached an end-of-sequence token, or are longer than a pre-defined limit.
   Though pooling the outputs at this later point incurs extra computational
cost owing to the additional decoders, this approach delivers better results in
practice [13]. Furthermore, the architecture lends itself to extensions, in particular
with regards to incorporating attention [11]. We choose a recurrent synthesis
decoder to overcome the limitations of MLPs, namely the lack of explicit time-
dependence between the decoders’ tokens and the structural upper bound on
output length, albeit at the expense of computational efficiency during training.
   To train Network 2, the output of the decoder is compared with the target
sequence using the cross-entropy loss function, which is computed as follows:
                                                                                     k
                                                                               L = −Σi=1 yi · log(oi )

where o and y are k-dimensional vectors denoting the output and ground-truth
value respectively, and oi and yi denote the ith dimension value of o and y.
To train our model, we use teacher forcing, where the target sequence is fed
into the decoder directly during training and used to compute the next output.
We give the full details of the training approach in the next section.


4        Training the Neural Networks
4.1          Sourcing the Training Data
The performance of a neural network is dependent on the quality and quantity
of the data it is trained on [34]. Neural networks typically require millions of
8

training examples [13, 27]. Given we do not have millions of program synthesis
benchmarks available, in order to obtain a large training data set, we randomly
generate predicates constructed as syntactically correct combinations of bit-vector
instructions. In an ideal world, we would randomly generate benchmarks in the
same format as the SyGuS benchmarks. There are two reasons we elected not
to do this: first, randomly generating logical specifications that are in some way
similar to the problem we want to tackle is a hard problem; and second, in order
to train the network using supervised learning we need to have both the logical
specification and the solution to the logical specification, and finding the solutions
to invariant generation benchmarks is hard.
    Our neural network synthesises programs from I/O examples, where an I/O
example is an assignment to all input parameters of the program to be synthesised,
and a corresponding output that satisfies the specification. Our training data is
a set of candidate programs, each accompanied by a corresponding set of input-
output examples. We have experimentally identified two features of “bad training
data”: 1) multiple programs with different syntax but equivalent semantics, which
we term equivalent mutants 3 , and 2) input-output examples that do not sufficiently
differentiate between programs. To avoid bad training data, we supplement our
program generator with a set of syntactic rules and an SMT-based procedure for
both reducing redundancy and generating informative I/O examples.


Eliminating equivalent mutants We enforce several rules in our random
program generator to reduce the number of equivalent mutants generated. As an
example, shifting a bit vector by any number greater than the bit vector width
always produces the same result as shifting the bit vector by the width. Thus,
we introduce a rule such that no generated program contains any shift operation
with the second operand greater than the width of the first.
    It would be impractical to check whether every program generated is equivalent
to any previous program generated using an SMT solver. However, we do use
an SMT solver to identify a further cause of equivalent mutants: An if-then-else
statement that always returns one of its conditional outputs is semantically
equivalent to the same program without the if-then-else statement, e.g., (z =
z)?x : y is equivalent to x. We identify this equivalence by recursively identifying
leaf operators (i.e., operators without nested ite statements) and checking their
branch satisfiability with an SMT solver. If a branch is infeasible, we replace the
if-then-else statement with the other branch and apply the recursive function
again. We continue until no leaf statements are redundant.
    Further to this, we use an SMT solver to remove certain trivial programs,
namely programs that always return a single constant value, or always return a
single one of the input arguments.


Input-Output Example Generation The simplest way to generate input-
output examples from a known target program is to uniformly generate input
3
    This term is borrowed from the literature on mutation testing.
                                                                                     9

values and to execute the program in order to obtain the corresponding outputs.
This may not differentiate between programs that do not represent a continuous
function mapping the input to output, i.e, they contain features that produce a
discontinuous output such as conditional statements. We generate input-output
examples for each random program such that the examples are informative
with respect to this program, i.e., the input-output covers as many conditional
branches in a program as possible, using a combination of randomly generated
inputs and SMT solving. In order to obtain a distribution of inputs over the
input space when using an SMT solver, we use Z3 version 4.5.1 [25] with the
phase selection set to random.

4.2        Training the network
To train the network, we randomly generate 32 million programs distributed over
programs of up to three input parameters, and of length up to give operations,
with up to one arbitrary constant, in addition to a zero and one constant.
    Of these 32 million programs, redundancy checks discard 2,613,768, leaving
a final training set of 29,386,232 programs. For each program, we generate ten
input-output examples. Training for the networks was done on an AWS p3.xlarge
instance with a Tesla Z100 GPU, and took 75 hours for the complex network.
The network was trained once over the training data (i.e., for one epoch) using
the Adam optimiser [23] and masked cross-entropy loss [24].

5      Example Guided Neural Synthesis
A limitation using neural networks to synthesise programs that meet logical
specifications is that neural networks are best suited to recognising patterns in
input-output examples rather than logical specifications, and, given a specification
and an input, it is not necessarily possible to determine a single correct output
for that input. In Example Guided Neural Synthesis, we use a combination
of SMT solving and heuristics to generate input-output examples that guide
the network to the candidate solution, and rely on the network’s resilience to
noise to overcome this limitation. The EGNS algorithm, illustrated in Fig. 4,
consists of three components: An SMT-solver used to generate a sequence of
input-output examples from the invariant specification; a neural network as
described in Section 3.2; and an SMT solver that checks each solution generated
by the network against the logical specification.


                           input-output             candidate
               Example       examples     Neural    programs               final
    spec                                                        Verifier
               generator                  Network                          program


                       Fig. 4. Example Guided Neural Synthesis
10

5.1   Generating Examples
We use a combination of two approaches to generate input-output examples
from a logical specification: In general the approach we take is to randomly
generate possible input values across the full bitvector range and use an SMT
solver to determine a possible correct output from the program to be synthesised.
If the number of possible correct outputs for a given input is large, we may
generate input-output examples that when combined preclude viable candidate
functions, and we rely on the statistical nature of the neural network to address
this problem.
    In the particular case of invariants we are able to further reduce such incon-
sistencies. Recall that, given a predicate P is an invariant iff ∀x, x0

        (I(x) ⇒ P (x)) ∧ (P (x) ∧ T (x, x0 ) ⇒ P (x0 )) ∧ (P (x) ⇒ A(x))

For a given x, the result of A(x), T (x, x0 ) and I(x) are computable. We thus
look for solutions to the following formula, where P and P 0 are Boolean variables
representing a correct output from P (x) and P (x0 ) respectively:

          ∃P, P 0 , x0 . (I(x) ⇒ P ) ∧ (P ∧ T (x, x0 ) ⇒ P 0 ) ∧ (P ⇒ A(x))     (1)

    In general it is not possible to determine the correct values of P and P 0
(Figure 5). We know P (x) must be true if x is part of the initial conditions
and does not violate the property, and that P (x) must be false if x violates
the property, and that P (x)0 must be false if x0 violates the property. There
is a region of the state space where a valid P should be true because the state
is reachable but we cannot determine that from a single input value x, and a
region of the state space where a satisfying invariant could be either true or false
because the states are unreachable but still satisfy the property. We test three
heuristics: in the first we only generate example pairs that are definitively true
or false; in the second we over-approximate the invariant, and assume that it
returns true for every case where x and x0 satisfy A(x); and in the third we
under-approximate the invariant and assume it returns false for every case where
x and x0 do not satisfy I(x). Note that due to the statistical nature of the neural
network, the use of incorrect input-output examples does not necessarily prevent
the neural network from giving a correct answer. We find that the best results
are obtained from a combination of all three heuristics, i.e., when we cannot
determine the output, we randomly choose true or false.
    If there exists an x that is both in the initial conditions and does not satisfy
the property, Formula 1 is not satisfiable and there no possible invariant. There
are no benchmarks in the set that meet these criteria.
    A limitation of randomly generating inputs across the full range of the bit
vectors is that we may never hit an input for which the invariant is known to
definitely be true or false. In the second approach, we guarantee that we generate
inputs for which the invariant is both true and false by using a SAT solver to
find values for x while asserting that either the initial conditions are true, or
that the property is false and the transition function is true.
                                                                                      11

                                             A(x)

                                           reachable
                                             I(x)
                                          known, true
                                      unknown, true
                                    unknown, don’t care
                                          known, false

                   Fig. 5. Invariant valuation over a 2 dimensional x


6      CounterExample Guided Neural Synthesis
A natural extension to Example Guided Neural Synthesis is CounterExample
Guided Neural Synthesis, where the network is integrated into an iterative process
similar to CEGIS and the next set of examples are chosen based on the previous
set of incorrect programs that were generated by the network, in order to try
to guide the network to a program that meets the specification. The use of a
counterexample-guided loop allows us to fix any incorrect outputs gradually.
    An overview of this architecture is given in Fig. 6. The loop is initialised by
generating a set of random input-output examples as described in Section 5.1.
We over-approximate the invariant when generating the output examples. This
approximation is corrected by counterexamples in subsequent iterations, inspired
by IC3 [9].


                           input-output                  candidate
               Example       examples     Neural         programs               final
    spec                                                             Verifier
               generator                  Network                               program



                                      counterexample
                                       input-output

                    Fig. 6. CounterExample Guided Neural Synthesis




6.1        CounterExample choice
It is known that counterexample choice is key for performance in CEGIS [21].
This is especially true with neural network synthesisers, as these generalise
best when deployed on inputs that are similar to its training inputs. In this
paper, the network trains for synthesis using very well-formed input-output sets
12

which, by construction, cover all execution branches and are restricted to the
program’s working input range, and we endeavour to replicate these informative
input-output sets as far as possible inside the CEGNS loop.

Probable candidate programs The first heuristic we introduce for coun-
terexample selection takes advantage of the complex neural network’s ability to
produce not just one candidate program, but the k most probable candidate
programs. Given k candidate programs and a set of input-output examples,
we introduce a pre-verification step which checks each candidate starting with
the most probable candidate, against the set of input-output examples. It con-
tinues checking candidates until it has found n candidates that satisfy all the
input-output examples, where n is a heuristic parameter given by the user, or
until it has checked the k th program. It returns these programs that satisfied all
input-output examples to the verifier. In the event that no candidates satisfy all
input-output examples, it return the candidate which satisfies the most examples.

Distribution of counterexamples In order to obtain a distribution of coun-
terexamples over the possible values that is as similar as possible to the training
data, we use Z3 as a verifier with the same random phase-selection used for gener-
ating the training data. Though this does not guarantee similarity with training
input-output, owing to Z3 solving a different and more constrained problem when
generating counterexamples, it does increase the variance in counterexamples.

Generation of output examples Each counterexample consists of values as-
signed to the inputs x for which the invariant returned the wrong answer. To
convert this to an input-output example we take the output produced by the
counterexample inputs and negate it. In the case where we receive a counterex-
ample due to states that violate the inductiveness of the candidate invariant (i.e.,
violate P (x) ∧ T (x, x0 ) ⇒ P (x0 )), conventional model checking algorithms must
make a choice whether to remove x from the invariant or to add x0 . Typically they
act in a monotonic way, doing either one or the other. Since we initialise the loop
with an over-approximation of the invariant, we opt for providing the example
that guides the network towards removing x from the invariant. However, due to
the statistical nature of the neural network, and the fact that the sequence of
candidate invariants it generates will not be monotonic, this is not guaranteed
to be the correct answer. As a measure to compensate for potentially generat-
ing input-output examples that are not compatible with a single invariant, we
maintain a finite number of counterexamples, discarding older counterexamples
as new ones are obtained. We also discard duplicate counterexamples.

7     Experimental Results
7.1   Experimental Setup
We use a 12-core 2.40 GHz Intel Xeon E5-2440 with 96 GB of RAM running Linux.
We implement the counterexample generation, the example generation and the
                                                                                 13

program verification in C++ and the neural network in Python. We evaluate
Example Guided Neural Synthesis and CounterExample Guided Neural Synthesis
using a two sets of benchmarks: 1) problems from the loop invariant category
taken from the Syntax Guided Synthesis Competition where we have replaced
unbounded integer types by bit-vector types; 2) benchmarks that correspond
to safety invariants for C programs [12]. We apply a timeout of 600s. Our code,
benchmarks and the scripts in order to run the experiments are available to
download4 .
    We compare with CVC4 [7] version 1.7-prerelease [git master dd9246f3] (CVC4
1.5 was the clear winner of the general track of the 2018 competition), our
implementation of a standard CEGIS loop [12] with an SMT solver as the verifier
and CEGIS(T) [1].
    We compare the two best configurations of CEGNS and EGNS and the solver-
based tools. There were two tools that we would have liked to compare to but were
unable to; the first is LoopInvGen, which narrowly beats CVC4 in the invariant
track of the SyGuS competition [30]. LoopInvGen [26] is limited to arithmetic over
unbounded integers; consequently, we ran it on equivalent benchmarks translated
to use linear integer arithmetic, of which it solved 67 in ∼10 s per benchmark.
However, owing to the semantic gap, some of the benchmarks have different
solutions, and it is unclear whether the performance observed is achievable on
bit vectors. The second tool is Code2Inv [30], a tool based on neural networks for
synthesising loop invariants for C code. Even though Code2Inv takes C files as
input, it treats C integers as unbounded integers. Unfortunately, it was unable
to parse our benchmarks.

7.2    Results
We empirically sample across the following parameters controlling how counterex-
amples are generated:
 1. beam: the number of programs produced by the network at once, e.g., a beam
    of size of k means that the network generates the k most likely programs.
 2. progs: the maximum number of programs returned by the network to the
    verifier, as explained in Section 6.
We find that storing the maximum number of programs possible after each
network call allows us to solve a few more benchmarks than only storing the first
one that satisfies all the input-output examples, although it is slower. A beam size
of 100 solves more benchmarks than a beam size of 10. We opt for maximising
the number of benchmarks solved, in our comparison in our comparison with
other solvers shown in Table 1, and use a beam size of 100, and maximally store
up to 100 programs per network call.
    Example Guided Neural Synthesis solves only 12 benchmarks with beam
size 100 although the runtime is quick. CEGNS solves nearly twice as many
benchmarks as EGNS, demonstrating that the counterexample guidance improves
4
    https://drive.google.com/open?id=1VkCyy7Sbipymn353R4g0BquXORjjs4dL
14

             Table 1. Comparison of CEGNS with the state of the art

                            CEGNS     EGNS      CEGIS     CEGIS(T)    CVC4
       Benchmarks solved         21       12        23          26       53
       Average time (s)      46.3 s    13.7 s     1.5 s      74.3 s    5.5 s




the performance of the neural network, and given a more performant network
CEGNS could be a powerful tool. CEGNS solves a similar number of benchmarks
to our traditional solver-based CEGIS implementation, and solves five benchmarks
that CEGIS fails to solve, and two that CEGIS(T) fails to solve.
    CVC4’s performance based on single invocation in formidable, in terms of
both speed and benchmarks solved. However, in cases where our network and
CVC4 both find a solution, the solution given by the network is typically shorter
and more human readable. This is likely due to the style of the training data, and
is synthesis biased towards human readable answers is an area worth exploring.


7.3   Threats to validity

Benchmark selection: We report an assessment of our approach on a diverse
selection of benchmarks. Nevertheless, the set of benchmarks is limited within the
scope of this paper, and the performance may not generalise to other problems.
Optimality of neural network architecture: We evaluate CEGNS and EGNS on
an empirically chosen neural network architecture; other architectures may be
more performant. The architecture was chosen on the basis of existing literature.
Choice of theories: CEGNS requires a neural network that is trained for the
relevant theory, e.g., linear integer arithmetic, bit vectors etc.; our evaluation is
limited to the theory of bit vectors, and results for other theories may be worse.


8     Related Work

Research applying neural networks to program synthesis typically focuses on
synthesising programs from I/O examples. A main approach for this is supervised
learning.
    For instance, Parisotto et al. introduce the NSPS (Neuro-Symbolic Program
Synthesis) system [27], which synthesise string manipulation programs from I/O
examples using a Recursive-Reverse-Recursive Neural Network that synthesises
programs by incrementally expanding partial programs. Neural GPUs [22] are
capable of learning to perform discrete algorithmic tasks such as reversing a
sequence but the program itself cannot be extracted. RobustFill also synthesises
string manipulation program [13]. The architecture of the neural network of
RobustFill is similar to that we use in CEGNS. Supervised learning methods
require a large set of programs and I/O examples to train, which can be difficult
to generate or acquire, but are very fast to query once trained.
                                                                               15

    Reinforcement learning used to train neural networks for program synthesis [2,
10] does not require I/O examples to generate programs, and uses a solution
checker to generate the reward needed for reinforcement learning; however, the
programs synthesised are typically in restrictive languages with 10 or fewer
operators, so it is not clear whether this approach would scale to synthesising
invariants for bitvector programs.
    Neural networks have also been used to supplement, rather than replace,
conventional program synthesis techniques. For example, Balog et al. [6] develop
DeepCoder, a program synthesis engine that uses a neural network to guide and
augment conventional search techniques.
    Code2Inv is a neural network based tool specifically for synthesising loop
invariants for C programs [30]. The network is designed to mimic a human
synthesising an invariant by working in a compositional fashion. The reported
results are promising, but the tool will not work for loops in C programs where
overflow semantics are critical to the safety of the loop, and in testing, we were
unable to run the tool on any of our benchmarks.
    SMT solvers are frequently used as oracles in formal program synthesis,
including in the CEGIS algorithm first presented for program sketching [31, 32].
Component-based approaches to program synthesis [3, 14–16, 18, 19, 29] are of
interest to us as we feel neural networks would be equally capable of learning how
to assemble programs from a database of components rather than from a set of
instructions. Component based synthesis typically makes use of techniques from
counterexample-guided synthesis [18] to type-directed search with lightweight
SMT-based deduction and partial evaluation [15] and Petri nets [16].
    There exist many algorithms specifically for invariant generation, and, al-
though our algorithm has potential to be extended to more general program
synthesis, it is worth mentioning the similarities. Our counterexample gener-
ation resembles IC3 [9] in the way it refines invariants. LoopInvGen [26] uses
program synthesis based techniques to synthesise loop invariants, and is similarly
data-driven. constraints.



9   Conclusions

We have introduced an Example Guided Neural Synthesis algorithm and a Coun-
terExample Guided Neural Synthesis Algorithm. Both allow application of neural
synthesis to logical specifications. CEGNS is a promising step towards guaranteed
correct neural-network based program synthesis, and performs comparably to a
purely SMT based CEGIS implementation, despite having a poorly performing
network as a core component. We look forward to exploring use of counterexample
guidance with more sophisticated network designs. CEGNS has potential to be
extended to more general program synthesis problems, particularly if used in
combination with a technique such as CEGIS(T), where the counterexamples
returned provide more information than a single counterexample value.
16

References
 1. Abate, A., David, C., Kesseli, P., Kroening, D., Polgreen, E.: Counterexample
    guided inductive synthesis modulo theories. In: CAV (1). Lecture Notes in Computer
    Science, vol. 10981, pp. 270–288. Springer (2018)
 2. Abolafia, D.A., Norouzi, M., Le, Q.V.: Neural program synthesis with priority
    queue training. arXiv preprint arXiv:1801.03526 (2018)
 3. Albarghouthi, A., Gulwani, S., Kincaid, Z.: Recursive program synthesis. In: CAV.
    LNCS, vol. 8044, pp. 934–950. Springer (2013)
 4. Alur, R., Bodı́k, R., Juniwal, G., Martin, M.M.K., Raghothaman, M., Seshia, S.A.,
    Singh, R., Solar-Lezama, A., Torlak, E., Udupa, A.: Syntax-guided synthesis. In:
    FMCAD. pp. 1–8. IEEE (2013)
 5. Alur, R., Radhakrishna, A., Udupa, A.: Scaling enumerative program synthesis via
    divide and conquer. In: TACAS. LNCS, vol. 10205, pp. 319–336 (2017)
 6. Balog, M., Gaunt, A.L., Brockschmidt, M., Nowozin, S., Tarlow, D.: DeepCoder:
    Learning to write programs. arXiv preprint arXiv:1611.01989 (2016)
 7. Barrett, C., Conway, C.L., Deters, M., Hadarean, L., Jovanovic, D., King, T.,
    Reynolds, A., Tinelli, C.: CVC4. In: CAV. LNCS, vol. 6806, pp. 171–177. Springer
    (2011)
 8. Bengio, Y., Simard, P., Frasconi, P.: Learning long-term dependencies with gradient
    descent is difficult. IEEE Transactions on Neural Networks 5(2), 157–166 (1994)
 9. Bradley, A.R., Manna, Z.: Property-directed incremental invariant generation.
    Formal Asp. Comput. 20(4-5), 379–405 (2008)
10. Bunel, R., Hausknecht, M., Devlin, J., Singh, R., Kohli, P.: Leveraging grammar and
    reinforcement learning for neural program synthesis. In: International Conference
    on Learning Representations (2018)
11. Chorowski, J.K., Bahdanau, D., Serdyuk, D., Cho, K., Bengio, Y.: Attention-
    based models for speech recognition. In: Advances in neural information processing
    systems. pp. 577–585 (2015)
12. David, C., Kesseli, P., Kroening, D., Lewis, M.: Danger invariants. In: Formal
    Methods (FM). LNCS, vol. 9995, pp. 182–198. Springer (2016)
13. Devlin, J., Uesato, J., Bhupatiraju, S., Singh, R., Mohamed, A.R., Kohli, P.: Ro-
    bustfill: Neural program learning under noisy I/O. arXiv preprint arXiv:1703.07469
    (2017)
14. Feng, Y., Bastani, O., Martins, R., Dillig, I., Anand, S.: Automated synthesis of
    semantic malware signatures using maximum satisfiability. In: NDSS. The Internet
    Society (2017)
15. Feng, Y., Martins, R., Geffen, J.V., Dillig, I., Chaudhuri, S.: Component-based
    synthesis of table consolidation and transformation tasks from examples. In: PLDI.
    pp. 422–436. ACM (2017)
16. Feng, Y., Martins, R., Wang, Y., Dillig, I., Reps, T.W.: Component-based synthesis
    for complex APIs. In: POPL. pp. 599–612. ACM (2017)
17. Goodfellow, I., Bengio, Y., Courville, A.: Deep Learning. MIT Press (2016), http:
    //www.deeplearningbook.org
18. Gulwani, S., Jha, S., Tiwari, A., Venkatesan, R.: Synthesis of loop-free programs.
    In: PLDI. pp. 62–73. ACM (2011)
19. Gulwani, S., Korthikanti, V.A., Tiwari, A.: Synthesizing geometry constructions.
    In: PLDI. pp. 50–61. ACM (2011)
20. Hochreiter, S., Schmidhuber, J.: Long short-term memory. Neural computation
    9(8), 1735–1780 (1997)
                                                                                     17

21. Jha, S., Seshia, S.A.: Are there good mistakes? A theoretical analysis of CEGIS. In:
    SYNT. EPTCS, vol. 157, pp. 84–99 (2014)
22. Kaiser, L., Sutskever, I.: Neural GPUs learn algorithms. CoRR abs/1511.08228
    (2015)
23. Kingma, D.P., Ba, J.: Adam: A method for stochastic optimization. arXiv preprint
    arXiv:1412.6980 (2014)
24. MacKay, D.J., Mac Kay, D.J.: Information Theory, Inference and Learning Algo-
    rithms. Cambridge University Press (2003)
25. de Moura, L.M., Bjørner, N.: Z3: an efficient SMT solver. In: TACAS. Lecture
    Notes in Computer Science, vol. 4963, pp. 337–340. Springer (2008)
26. Padhi, S., Sharma, R., Millstein, T.D.: Data-driven precondition inference with
    learned features. In: PLDI. pp. 42–56. ACM (2016)
27. Parisotto, E., Mohamed, A.r., Singh, R., Li, L., Zhou, D., Kohli, P.: Neuro-symbolic
    program synthesis. arXiv preprint arXiv:1611.01855 (2016)
28. Peleg, H., Shoham, S., Yahav, E.: Programming not only by example. In: ICSE. pp.
    1114–1124. ACM (2018)
29. Perelman, D., Gulwani, S., Grossman, D., Provost, P.: Test-driven synthesis. In:
    PLDI. pp. 408–418. ACM (2014)
30. Si, X., Dai, H., Raghothaman, M., Naik, M., Song, L.: Learning loop invariants for
    program verification. In: NIPS (2018)
31. Solar-Lezama, A.: Program sketching. STTT 15(5-6), 475–495 (2013)
32. Solar-Lezama, A., Tancau, L., Bodı́k, R., Seshia, S.A., Saraswat, V.A.: Combinato-
    rial sketching for finite programs. In: ASPLOS. pp. 404–415. ACM (2006)
33. Sutskever, I., Vinyals, O., Le, Q.V.: Sequence to sequence learning with neural
    networks. In: NIPS. pp. 3104–3112 (2014)
34. Yu, L., Wang, S., Lai, K.K.: An integrated data preparation scheme for neural
    network data analysis. IEEE Transactions on Knowledge and Data Engineering 18,
    217– 230 (03 2006)
