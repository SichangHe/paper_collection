                                             The CAISAR Platform: Extending the Reach of
                                             Machine Learning Specification and Verification

                                         Michele Alberti , François Bobot , Julien Girard-Satabin , Alban Grastien ,
                                                           Aymeric Varasse , and Zakaria Chihani

                                                      Université Paris-Saclay, CEA, List, F-91120, Palaiseau, France
                                                                    firstname.lastname@cea.fr
arXiv:2506.12084v2 [cs.SE] 20 Jan 2026




                                                                       julien.girard2@cea.fr
                                                                             Software Heritage
                                                             aymeric.varasse@softwareheritage.org


                                                 Abstract. The formal specification and verification of machine learning
                                                 models have advanced remarkably in less than a decade, leading to a pro-
                                                 fusion of verification tools that provide mathematical guarantees about
                                                 model properties. However, this growing diversity risks ecosystem frag-
                                                 mentation, making it difficult to compare tools beyond narrowly defined
                                                 benchmarks. Moreover, much of the progress to date has focused on a
                                                 limited class of properties, particularly local robustness. While existing
                                                 tools are increasingly effective at verifying such properties, more complex
                                                 ones, such as those involving multiple neural networks, remain beyond
                                                 their capabilities: these properties cannot currently be expressed in their
                                                 specification languages, nor can they be directly verified. This applies
                                                 even to the winning verification tools of the International Verification of
                                                 Neural Networks Competition (VNN-Comp).
                                                 In this tool paper, we present CAISAR, an open-source platform for spec-
                                                 ifying and verifying properties of machine learning models, with partic-
                                                 ular focus on neural networks and support vector machines. CAISAR
                                                 provides a high-level language for specifying complex properties and in-
                                                 tegrates several state-of-the-art verifiers for their automatic verification.
                                                 Through concrete use cases, we show how CAISAR leverages automated
                                                 graph-editing techniques to translate high-level specifications into queries
                                                 for the supported verifiers, bridging the (embedding) gap between user
                                                 specifications and the corresponding ones that are actually verified.

                                                 Keywords: Formal Specification and Verification, Machine Learning


                                         1     Introduction
                                         In recent years, the formal methods (FM) community has made significant
                                         progress, going from the very first neural network (NN) verifiers [33,28], suffering
                                         from scalability issues, to a wide range of tools capable of handling increasingly
                                         large NNs [29,40,4,24,31,35]1 and diverse machine learning (ML) models, like
                                         Support Vector Machines (SVM) [34,20] and boosted trees [3].
                                             From this Cambrian explosion of tools, we draw the following observations:
                                         1
                                             For a comprehensive overview of the field, we refer readers to the survey in [38].
A focus on a narrow set of properties Research on the formal verification of ML
models has largely concentrated on a restricted class of properties, most notably
local robustness. Given an input x, a model f , and a perturbation bound ϵ ∈ R,
local robustness is defined as the requirement that

                         ∀x′ . ∥x − x′ ∥ ≤ ϵ =⇒ f (x) = f (x′ ).

Several variants of this definition have been proposed [13], including K-Lipschitz
robustness [5] and strong classification robustness [26]. The emphasis on local
robustness is motivated by the nature of modern ML models, which frequently
operate on high-dimensional inputs such as images or text. In such settings,
formulating functional specifications is often impractical—if not impossible—
whereas local robustness remains applicable and well-defined. While this has
not prevented researchers from proposing higher-level specifications—including
fairness constraints [37], semantic transformations robustness [6] or providing
formally-grounded explanations [8,42]—we argue that the field remains primarily
centered on robustness properties. As previously noted [19], there is an urgent
need for more expressive specification languages that would enable the formal
verification of a broader range of semantic properties of ML models.

Limitations on the expressiveness of input languages The current de-facto stan-
dard for specifying properties is the VNN-LIB language, adopted by the Verifi-
cation of Neural Network Competition (VNN-Comp) [12,11,10]. As the VNN-LIB
was originally designed to handle the community focus towards the specification
and verification of local robustness properties of NNs, it exhibits certain limita-
tions. First, the size of specification increases with the size of the NN, making
it cumbersome for a human to write, and even more so to read and maintain.
Second, VNN-LIB restricts specifications to conjunctions of linear arithmetic con-
straints over inputs and outputs, which are the only authorized free variables.
    More formally, let x ∈ Rd be a vector and xc its c-th element, f : Rd 7→ Rp
be a function representing an NN that takes a d-dimensional vector as input
and returns a p-dimensional vector, K ⊆ {1, . . . , p} be a (possibly empty) set
of integers, and a, b ∈ Rd and c, d ∈ Rp be vectors. A VNN-LIB specification is
then equivalent to the following formula:

      ∀x ∈ Rd . ∀y ∈ Rp . y = f (x) =⇒
                  ^                     ^                ^
                      ai ≤ xi ≤ bi =⇒ (   cj ≤ yj ≤ dj ∧   yp ≤ yk ),
                i=0..d                      j=0..p                 k∈K

which specifies that if the input is within a polyhedron defined by a and b, then
the output should be within the polyhedron defined by c and d, and its p-th
element should be lower than all others in K.
   Such a formulation prevents expressing properties on multiple NNs [2], hyper-
properties [43,9], or any specification yielding uninterpreted functions. Promising
high-level specification languages exist, notably the one in Vehicle [21], that need
to be both expressive enough and compile down to a vast range of verifiers to
take advantage of the profusion of existing tools.
Difficulty to compare and select a verifier A profusion of solutions implies the
burden of choice. For now, this burden is mostly taken by the end-user of verifi-
cation tools. Comparing the capabilities of tools is a first prerequisite to lift that
burden. This need for comparison is partially addressed with the VNN-Comp,
where tools are evaluated against benchmarks proposed by the community. How-
ever, as displayed in [30], this is but one of the numerous facets for evaluating
the quality of verifiers. Indeed, depending on the property to check or the im-
plementation specifics of a ML model, some verifiers may not be suitable, or
underperform compared to others [30], making it difficult to assess the strengths
and weaknesses of specific verifiers. It is thus necessary to provide a systematic
and principled way to compare verifiers against the same basis.

A gap between the specified and proven programs Formal verification is a multi-
faceted activity that usually involve multiple steps: writing a specification, de-
veloping a program, encoding the specification into a suitable tool and ensuring
the program is correct regarding the encoded specification.
    A common struggle is to ensure that each step of the process is trustworthy
and coherent one with another, that is to say, that the proof run on a particular
program is meaningful with regard to a specification that was provided. One
possible solution is to couple writing the specification and generating the code,
like in the industrial software SCADE2 . However, machine learning has its own
peculiarities. For instance, it is common to apply transformations on the inputs
of a neural network during the evaluation pipeline to normalize inputs regarding
a certain training set distribution. Such transformations are not specified inside
the NN, but done at runtime. Furthermore, most tools express specifications
with real arithmetic, whereas NNs compute floating points numbers. VNN-LIB
assumes that the companion program to verify is a NN, but without specifying
anything towards it, or the transformations on inputs. This creates an embedding
gap [22,19]: the specification the program is checked against follows an unspeci-
fied transformation. Ideally, a complete specification should be unambiguous on
the transformations applied to an input.

    In this paper, we present a way to lift these limitations within the open-
source verification platform CAISAR [1]. We present and implement a higher-level
specification language that allows users to express complex properties, includ-
ing properties with multiple ML models. CAISAR proposes an automated and
principled way to translate specifications written in a higher-level language to 9
verification tools—including the winners of the VNN-Comp. CAISAR is thus able
to express properties and send them to existing off-the-shelf verification tools
without modifying them. Its maturity allowed it to be used in industrial settings
on non-public use-cases, although this paper focuses on illustrating the platform
through simple examples (see Section 3).
2
    https://www.ansys.com/en-gb/products/embedded-software/ansys-scade-suite
Fig. 1: The overall functional architecture of CAISAR. Significant extensions to the
original Why3 platform are outlined in shaded rectangles.



Artifact Availability Statement An artifact—including instructions, datasets,
and experiment scripts—reproducing the results in this paper is publicly avail-
able at https://doi.org/10.5281/zenodo.16902886.


2   General Architecture and Core Components

The general architecture of CAISAR is depicted in Fig. 1. CAISAR builds upon
the design of Why3 [25] and makes extensive use of the Why3 API. Why3 is
a mature platform for deductive program verification, applied across a wide
range of domains, from robotic navigation algorithms [36] to the formalization
and verification of quantum programs [15]. It provides a rich input language for
specifying, implementing, and formally verifying the correctness of algorithms.
Verification proceeds by generating verification conditions, which are dispatched
to a variety of automated and interactive provers via composable transforma-
tions. A dedicated verification condition generator (VCG) translates a program
together with its specifications into logical goals. Finally, Why3 offers a unified
text-based configuration mechanism for each supported solver.
    CAISAR adapts those components to the specific needs of verification of ML
models. To include ML into the specification and ease vector computation, we
extend the Why3 input language with several built-ins as described in Section 2.1.
To handle those extensions, we modify the internal Why3 interpretation engine as
described in Section 2.3. To represent ML components in Why3, we build a Neural
Intermediate Representation (NIR) described in Section 2.2; Section 3.2 describes
how to translate SVMs to valid NIR representations. High-level specifications are
currently not directly amenable for provers. In such cases, we translate part of
the Why3 specification directly as a new NIR as explained in Section 2.3, using
automated graph editing that incorporates part of Why3 terms within the NIR.
Finally, a list of supported provers is presented in Section 2.3.
2.1     The Specification Language
CAISAR supports specifications written in WhyML3 , the specification and pro-
gramming language of Why3. It exhibits three key qualities: it is strongly typed
to prevent type errors, expressive to specify properties beyond local robustness,
and high-level to bridge the embedding gap inherent of VNN-LIB (see Section 1).
Specifically, WhyML enables writing properties of (multiple) ML models, treating
them as pure (i.e. side-effect free), abstract functions that operate on vectors.
    To support this abstraction, CAISAR extends the Why3 standard library with
dedicated theories, such as the theory Model of ML models, and Vector of
finite-length arrays. These theories define types, predicates and functions neces-
sary to specify properties about ML models, vectors and their operations.
    We present the grammar of the language in Fig.2. A CAISAR specification is
then a WhyML sequence of type, predicate and function definitions.


      ⟨decl ⟩ ::= type ⟨tId ⟩ = ⟨type⟩     ⟨expr ⟩ ::= ⟨id ⟩
                | predicate ⟨id ⟩                    | ⟨built-in⟩
                     ⟨binder ⟩∗ = ⟨expr ⟩            | ⟨expr ⟩⟨expr ⟩
                | function ⟨id ⟩                     | (⟨expr ⟩,. . . ,⟨expr ⟩)
                    ⟨binder ⟩∗ ⟨spec⟩∗ = ⟨expr ⟩     | let ⟨id ⟩ = ⟨expr ⟩ in
                                                     | if ⟨expr ⟩ then ⟨expr ⟩
    ⟨type⟩ ::= ⟨tId ⟩
                                                       else ⟨expr ⟩
             | ⟨type⟩ → ⟨type⟩
                                                     | ⟨expr ⟩⟨bop⟩⟨expr ⟩
             | (⟨type⟩,. . . ,⟨type⟩)
                                                     | forall⟨binder ⟩.⟨expr ⟩
             | vector ⟨type⟩
                                                     | exists⟨binder ⟩.⟨expr ⟩
             | int | bool | float | string
                                                     | not⟨expr ⟩
             | model
                                                     | i ∈ Integer
 ⟨binder ⟩ ::= ⟨id ⟩ | (⟨id ⟩ : ⟨type⟩)              | {true, false} ∈ Boolean
    ⟨spec⟩ ::= requires {⟨expr ⟩}                    | f ∈ Float | s ∈ String
              | ensures {⟨expr ⟩}                  ⟨built-in⟩ ::= read_model ⟨expr ⟩
      ⟨bop⟩ ::= ≤ | ≥ | < | >                                   | length ⟨expr ⟩
              | +|−|×|/                                         | has_length ⟨expr ⟩ ⟨expr ⟩
              | ∧|∨|→                                           | ⟨expr ⟩[⟨expr ⟩]
                                                                | ⟨expr ⟩@@⟨expr ⟩
Fig. 2: Grammar of CAISAR’s high-level specification language. The nonterminal
⟨built-in⟩ denotes WhyML functions having a special interpretation in CAISAR.


    Examples of specifications are shown in Fig.3 and Fig.4. Fig.3 shows a specifi-
cation where the output of a first NN is perturbed and then passed as an input to
a second NN, requiring the classification of the second NN to be a certain class.
This example illustrates how to naturally express properties involving multiples
NN, intermediate computations on inputs and outputs, and NN composition. On
the other hand, property in Fig.4 specifies that two NNs produce output vectors
that differ by at most δ over their entire, valid input domain.
3
    https://www.why3.org/doc/syntaxref.html
1      goal sequencing:
2        let nn1 = Model.read_model "path/to/nn1.onnx" in
3        let nn2 = Model.read_model "path/to/nn2.onnx" in
4        let dataset = Dataset.read_dataset "path/to/csv" in
5        let eps = (0.01:t) in
6        CSV.forall_ dataset (fun l e →
7          forall perturbed_e.
8            has_length perturbed_e (length e) →
9            FeatureVector.valid feature_bounds perturbed_e →
10           let perturbation = perturbed_e - e in
11           ClassRobustVector.bounded_by_epsilon perturbation eps →
12           let out_1 = nn_1@@perturbed_e in
13           let out_2 = nn_2@@out_1 in
14           forall j. Label.valid label_bounds j → j ̸= l →
15           out_2[l] .≥ out_2[j]
16       )


     Fig. 3: CAISAR specification about the output prediction of a composition of NNs.
     The specification begins by declaring a verification goal named sequencing. Lines
     2-4 introduce two NNs and the dataset by loading their ONNX model and CSV files,
     followed by line 5 which sets the perturbation ϵ of the first input to 0.01. Line 6 ensures
     the specification will be checked against all samples in the dataset. Lines 7-11 define
     a perturbed vector that has the same length of the original vector and have the same
     bounded values. Lines 12-13 describe the computation: the input of the first NN is
     perturbed, then the computation is performed, and the composition by the second NN
     takes place. Finally, line 14-15 assert that the prediction for the given output label is
     always the preferred one.

1      goal equality_up_to_delta:
2        let nn1 = Model.read_model "path/to/nn1.onnx" in
3        let nn2 = Model.read_model "path/to/nn2.onnx" in
4        let delta = (0.125:t) in
5        forall input. Vector.has_length input 5 →
6          (forall i. 0 ≤ i < Vector.length input → 0.0 .≤ input[i] .≤ 1.0) →
7            let output1 = nn1 @@ input in
8            let output2 = nn2 @@ input in
9            .- delta .≤ output1[0] .- output2[0] .≤ delta


     Fig. 4: CAISAR specification about the output equality up-to δ between two NNs. The
     specification begins by declaring a verification goal named equality_up_to_delta.
     Lines 2-3 introduce two NNs by loading their ONNX model files, followed by line 4
     which sets the tolerance threshold δ to 0.125. Lines 5-6 constraint the input vector to
     be of length 5 with elements in [0.0, 1.0]. Lines 7-8 then apply both NNs to this input
     using the @@ operator for model application. Finally, line 9 asserts that the absolute
     difference between the first output components of both networks is bounded by δ.



         The built-ins currently have no explicit definition inside WhyML; rather
     their semantics is determined via interpretation, a process described in more
     detail in Section 2.3. For instance, the Model theory provides the built-ins
     read_model s, which introduces a model in a specification by reading the
     filename s, and m @@ v, which returns a (output) vector obtained by apply-
     ing model m to (input) vector v. Similarly, the Vector theory provides several
     built-ins such as, among others, length v to return the length of vector v,
has_length v i to check whether vector v has length i, v[ i ] to retrieve the
element at position i of vector v, and forall_ v f to verify that predicate f
holds for every element of vector v.


2.2   The Neural Intermediate Representation
Preliminaries on ONNX The Open Neural Network Exchange (ONNX) is
an intermediate representation described via the Protocol Buffer 4 interface lan-
guage. It is vastly supported within state-of-the-art machine learning frameworks
like PyTorch or TensorFlow. ONNX describes a directed acyclic graph (DAG)
whose nodes are operators describing computations on multidimensional arrays,
called tensors, and edges describe the flow of data. An example of ONNX graph
is available in Fig.5.
    At the time of writing, ONNX defines 193 operators5 . Below, we provide an
informal semantics for a subset of these operators used later in the paper:
 – Add(x, y) (respectively, Sub, Mul, Div) performs element-wise addition (re-
   spectively, subtraction, multiplication, and division) of tensors x and y,
   which are assumed to have the same shape;
 – Concat(x, y) appends tensor y to tensor x along a specified axis;
 – Gather(x, y) selects values from tensor x at indices specified by tensor y,
   that is, Gather(x, y) = xyi ;
 – Gemm(x, y) performs matrix multiplication of tensors x and y, optionally
   followed by the addition of a bias term c;
 – Sign(x) returns an integer tensor y such that yi = 1 whenever xi > 0,
   yi = −1 whenever xi < 0, and yi = 0 otherwise;
 – ReLU(x) applies to tensor x the rectified linear function max(0, x) element-
   wise;
 – Input designates the entry point of the graph6 .




Fig. 5: Example of an ONNX graph, obtained using the netron tool. Gemm stands for
GEneralized Matrix Multiplication, while Relu is the Rectified Linear Unit function.



4
  https://protobuf.dev/
5
  https://github.com/onnx/onnx/blob/main/docs/Operators.md
6
  In plain ONNX, the entry point is specified via graph metadata. We define an oper-
  ator Input explicitly here for clarity.
Representing Machine Learning Components CAISAR defines a Neural In-
termediate Representation (NIR) to model machine learning components. Similar
to ONNX, a NIR is a DAG, where each node encodes an operation, its input and
output shapes, and the computation type. The NIR language supports a subset
of the ONNX Intermediate Representation v8 and ONNX Opset v13 standards7 .
The full list of supported operators is available in the CAISAR source code.
    CAISAR can parse various machine learning models into NIR, including neural
networks in the ONNX and NNet formats, and support vector machines exported
in a format compliant with the scikit-learn [39] framework. Gradient boosting
machines are currently handled via a separate pipeline.
    The NIR is implemented as a pure recursive OCaml variant type. Its signature
is compatible with the ocamlgraph [18] library, enabling efficient graph traversal
and transformation.
    CAISAR also supports back-translation from NIR into multiple target formats.
It can generate valid ONNX models, and leverages prior work [27] to compile
control-flow representations of neural networks into the SMT-LIB (and its subset,
VNN-LIB) format, enabling interoperability with a range of off-the-shelf solvers.


Automated Transformations of SVM to NIR CAISAR is able to reason
about Support Vector Machines (SVM) by translating them into equivalent NIR.
    SVMs are classical ML models used for classification. Given an input vector
x and assuming m classes, the model outputs a vector y ∈ Rm where each
component ycl is the score associated with the class cl ∈ {1, . . . , m}.
    We first consider the binary case (m = 2). In this setting, training identifies
a subset of the samples, called support vectors, that lie on or near the margin
of separation between the two classes. Together with their learned coefficients,
these vectors define a hyperplane that partitions the input space into two regions,
one for class cl1 and the other for class cl2 .8
    Multiple support vectors can contribute to the separation of the two classes.
Each class clj has a (possibly different) number kj of support vectors, denoted
Sclj ,1 , . . . , Sclj ,kj . Classification is based on the (signed) distance between the
input x and each hyperplane defined by the support vectors, denoted x ⊗ Sclj ,ℓ ,
indicating how confidently the corresponding support vector classifies the input.
    An optional non-linear function f can be applied to these distances, which
are then scaled by a scalar cclj ,ℓ , called the dual coefficient. The resulting values
are summed over all support vectors of the class, and a bias term i, called the
intercept, is added. This leads to the following formula:

               X                                                X
      i+                   (ccl1 ,ℓ ∗ f (x ⊗ Scl1 ,ℓ )) −                   (ccl2 ,ℓ ∗ f (x ⊗ Scl2 ,ℓ )).
           ℓ∈{1,...,k1 }                                    ℓ∈{1,...,k2 }

7
    https://onnx.ai/onnx/operators/index.html
8
    This geometric interpretation is valid for the linear case; for models using Radial
    Basis Function (RBF) kernels, the separation is non-linear, which we omit here for
    simplicity.
                       Kernel
               S                     c         i
                       params

      X      Gemm         f        Gemm       Add       Sign      Gemm          Y

           kernel computation             one vs. one        adding up scores


                        Fig. 6: NIR representation of an SVM.



The input x is classified as belonging to class cl1 if the sum is positive, and to
class cl2 if it is negative (the probability that it equals zero is negligible).
    For SVMs with more than two classes, we adopt the one-versus-one (ovo)
scheme. A binary classifier is trained for each pair of classes, using dual coeffi-
cients and intercepts specific to that pair. (The support vectors associated with
each class remain the same, although some dual coefficients may be zero, effec-
tively ignoring certain support vectors in a given comparison.) For each input,
the SVM counts how many times each class is selected in these pairwise com-
parisons. For instance, with 10 classes, the output is a vector of 10 integers, each
between 0 and 9. It should be clear that ties—where two or more classes share
the highest score—can occur, but are rare in the case of binary classification.
    The translation of an SVM into a NIR is illustrated in Fig. 6. The first stage
computes the kernel, which involves taking the product of the support vectors
with the input, optionally followed by the non-linear function f . The second
stage performs the one-versus-one comparisons: kernel values are multiplied by
the dual coefficients, the intercept is added, and a positivity check determines
the predicted class for each pair of classes. Finally, the last layer aggregates these
pairwise scores to produce a final score for each class.
    CAISAR currently supports Linear and Polynomial kernels, as well as Radial
Basis Function (RBF) kernels.


2.3   The Verification Module
CAISAR leverages the Why3 architecture to generate verification conditions for its
supported provers. A high-level WhyML specification first undergoes an interpre-
tation phase, during which constants and computable expressions are evaluated
and lifted to the top level. This is followed by a series of formula-wide transfor-
mations, handled by Why3 ’s modular infrastructure. Prover-specific transfor-
mations may then be applied before translating the result into the input format
of the target prover. Finally, Why3 coordinates the execution of provers and
collects their results, presenting them back to the user.
    The remainder of this section describes how this general workflow is adapted
to ML programs.
Interpretation of Built-Ins To convert a high-level WhyML specification into
lower-level VNN-LIB conditions accepted by existing verifiers, CAISAR interprets
the built-ins defined in Section 2.1 as follows:

 – Reading models and datasets. The built-in function read_model is treated
   as a pure function that loads an ONNX model from a given file path. Note
   that we do not add I/O capabilities to Why3 as read_model only performs
   read-only access to the file system. Semantically, it is modeled as a math-
   ematical function mapping valid ONNX file paths to their corresponding
   parsed models.
   Similarly, read_dataset reads a labeled dataset from a CSV file and re-
   turns a vector of label-features pairs. Accessing this vector at a fixed index
   yields the corresponding data point.
 – Vector computation and access. To manipulate vectors, mapi applies a user-
   defined function to each element of a vector whose size is statically known.
   The operator @@ applies a ML model—obtained via read_model—to a vec-
   tor of inputs and returns an output vector. Standard indexing v[i] retrieves
   the i-th element of the vector v.
 – Quantification. Bounded quantifications over vectors are interpreted as quan-
   tifications over their individual elements, assuming the vector’s size is fixed
   and known—either explicitly provided or inferred from hypotheses. The re-
   duction engine in Why3 maintains symbolic representations of each vector
   element, enabling the interpretation of mapi and similar higher-order con-
   structs.

Limitations While interpretation enables the expression of rich specifications,
some WhyML constructs remain outside its scope. Specifically, universal quantifi-
cation over vectors is unsupported when the vector’s shape cannot be determined
statically. Since VNN-LIB is a fragment of the SMT-LIB theory of Quantifier-Free
Linear Real Arithmetic (QF_LRA), quantifiers must be eliminated to generate
valid verification conditions. In particular, formulas involving alternating quan-
tifiers are not directly supported.


Embedding Specifications within Neural Networks

Illustrative example Let nn1 and nn2 be two NNs with one (resp. two) inputs
and one output each. Consider the following WhyML expression:

                   nn2 @@(nn1 @@(x1 ), x1 + ϵ) + nn1 @@(x0 )

In this expression, nn1 is applied to both x0 and x1 ; the result of nn1 @@(x1 ) is
used as the first input to nn2 , whose second input is x1 + ϵ. Let H be a valid
QF_LRA formula defining bounds on x1 , x2 and ϵ. Then, the formula
   ∀x0 , x1 , ϵ. H(x0 , x1 , ϵ) →
                             composition of nns
               z                }|                         {                     (1)
               nn2 @@(nn1 @@(x1 ),            x1 + ϵ       ) + nn1 @@(x0 ) > 0
               |     {z    }                  | {z }
               multiple networks      operation on the input

illustrates several limitations of the VNN-LIB format discussed in Section 1:
 1. It includes a nontrivial computation on the input, x1 + ϵ;
 2. It composes multiple networks, nn1 and nn2 ;
 3. It feeds the output of one network (nn1 ) into another (nn2 ).
    These constructs are not directly supported by VNN-LIB, preventing the spec-
ification and verification of such formulas.
    However, it is possible to lift these limitations by embedding part of the spec-
ification within a new neural network, say nn3 . The resulting formula becomes:

                  ∀x0 , x1 , ϵ. H(x0 , x1 , ϵ) → nn3 @@(x0 , x1 , ϵ) > 0         (2)

Here, nn3 encodes the entire computation: the arithmetic on inputs, the nested
evaluation of networks, and the final comparison. A representation of the NIR
corresponding to nn3 is shown in Fig.7. Embedding multiple networks within
a single NIR allows specifications that involve their composition, while incorpo-
rating fragments of WhyML expressions into the NIR enables more expressive
specifications that capture computations over both inputs and outputs.
    The key insight is that certain WhyML expressions can be encoded as ONNX
operators, effectively relocating parts of the specification into the neural network
itself. This approach not only enables the expression of richer specifications
that are otherwise inexpressible in VNN-LIB, but also leverages the fact that
ONNX operators are more widely supported by state-of-the-art verifiers. Com-
bined with the interpretation mechanism introduced in Section 2.3, this strategy
significantly broadens the class of properties that can be formally specified and
verified for machine learning programs.


            Gather(0)           nn1


Input       Gather(1)           nn1                                        Add
                                            Concat             nn2
            Gather(2)           Add

Fig. 7: Gather(0) (resp. Gather(1)) extracts x0 (resp. x1 ) and Gather(2) extracts ϵ
from the Input node. The first Add node computes x1 +ϵ. Nodes nn1 nn2 represents
inlined nn1 and nn2 control flows. Finally, Concat prepares the inputs of nn2 .
Integrating WhyML Terms into NIR Given a WhyML formula ϕ(S, N , P, Q),
with N a non-empty set of NNs, S a set of universally quantified variables
that represents both inputs and outputs of NNs, P a precondition and Q a
postcondition, the goal is to write a new formula ϕ′ (S ′ , N ′ , P ′ , Q′ ), equivalent
to ϕ, with N ′ consisting of a single NN.
     To do so, we perform a structural analysis of ϕ, heavily relying on OCaml
pattern-matching capabilities. First, WhyML terms t describing operations not
supported by VNN-LIB are matched. Then, subterms ti s are selected top-down.
If ti can be translated into NIR nodes, then CAISAR generates a new NIR with the
properly inserted nodes, removes the computation from the Why3 formula and
replaces the proper symbols. A table representing the correspondance between
WhyML terms and NIR operators is shown in Fig.8.



                  Je1 + e2 KM = Add(Je1 KM , Je2 KM )
                  Je1 − e2 KM = Sub(Je1 KM , Je2 KM )
                  Je1 ∗ e2 KM = Mul(Je1 KM , Je2 KM )
                   Je1 /e2 KM = Div(Je1 KM , Je2 KM )
                     J−e1 KM = Mul(J−1.KM , Je2 KM )
                     J⟨id ⟩KM = Gather(Input, M (⟨id ⟩))
    Jnn@@(e1 , . . . , en )[c]KM = Gather(Apply(nn, Concat(Je1 KM , . . . , Jen KM )), c)
               Apply(nn, g) = P arser(nn)[Input ← g]


Fig. 8: Mapping between WhyML expressions and NIR nodes. All nodes are one-
dimensional tensors. A transformation J·KM is parametrized by a mapping of input
symbols ⟨id ⟩ ∈ S towards NIR input indices. For NNs nn1 and nn2 , nn1 [Input ← nn2 ]
builds a copy of nn1 where the input g is replaced by nn2 .




Limitations In principle, our approach applies to any WhyML expression that
can be encoded as NIR nodes. For instance, ONNX includes an If operator
for representing conditionals. However, such constructs are rarely supported by
existing verifiers, often requiring formula splitting and thereby increasing the
number of generated verification conditions. Consequently, we restrict ourselves
to simple arithmetic operations expressible within the QF_LRA fragment.
    Moreover, the translation of WhyML formulas relies on a flattened representa-
tion of the inputs, requiring the insertion of multiple one-dimensional NIR nodes.
Since NN verifiers are typically optimized for high-dimensional tensor computa-
tions, this flattening introduces overhead, as empirically evaluated in Section 3.1.
    More broadly, the question of how much of the specification should be em-
bedded within the neural network itself remains open. There is an inherent
trade-off between, on the one hand, the expressiveness and conciseness afforded
to the user, and on the other hand, the tractability of the resulting verification
conditions.


Provers CAISAR supports the following ML-specific verification tools: α-β-
CROWN [40], PyRAT [31], Marabou [29,41], nnenum [4], AIMOS [32], SAVer [34].
Thanks to the Why3 platform and the NIR, it supports translating specifications
into the SMT-LIB format, compliant with CVC5 [7], Z3 [23] and Alt-Ergo [17]
provers. It also supports gradient-boosted trees generated with the XGBoost li-
brary [16]. Each prover is automatically detected by CAISAR if installed. An
experimental distribution of CAISAR using the Nix declarative package manager
bundles CAISAR, Marabou and Python-based provers. By default, CAISAR brings
an appropriate configuration for each prover. It is possible for the user to define
alternative prover configurations in the caisar-detection-data.conf file.
The user only needs to specify the desired command-line options in this file, a
name for the custom configuration, and run CAISAR by specifying said name.


3     Use Cases and Evaluation
CAISAR provides a publicly available manual9 , including classical examples from
the ACAS Xu benchmark and local robustness on MNIST. It was also used in in-
dustrial contexts [14], for instance in the DeepGreen10 project and Confiance.ai11
program. In the following, we also illustrate CAISAR capabilities to specify prop-
erties beyond local robustness properties.


3.1   Formal Verification of ACAS Xu with Unnormalized Inputs
We consider the classical ACAS Xu benchmarks, originally presented in [28] with
a subtle, but important difference. The original paper presents the benchmark
with unnormalized values. For instance, property ϕ1 is written as follows:

          P(x) = x[ρ] ≥ 55947.691 ∧ x[vown] ≥ 1145 ∧ x[vint] ≤ 60
                       =⇒ Q(y) = y[coc] < 1500

However, the actual property specifications encoded in Marabou exhibit normal-
ized values12 . As neural networks require normalized inputs, this is expected;
however it creates a gap between the specification expressed in terms of expert-
domain knowledge and the actual values checked during verification. This embed-
ding gap was identified as a major obstacle [19] to actionable formal specification.
    Fortunately, specifying the normalization process inside the WhyML speci-
fication will produce an ONNX file that normalizes its input according to the
9
   https://caisar-platform.com/documentation
10
   https://deepgreen.ai
11
   https://confiance.ai
12
   Values available on the Marabou GitHub repository.
     specification. The network will then compute normalized results, which can then
     be returned to the original output space. As long as the normalization and denor-
     malization processes are well-specified, the specification can be expressed on the
     original input and output. Fig.9 provides a WhyML excerpt of such specification.


1         let function normalize_t i mean range = (i .- mean) ./ range
2         let function denormalize_t i mean range = (i .* range) .+ mean
3         let function normalize_input i = Vector.mapi i normalize_by_index
4
5         let function denormalize_output_t o =
6           denormalize_t o
7             (7.51888402010059753166615337249822914600372314453125:t)
8               (373.9499200000000200816430151462554931640625:t)
9
10        let runP1 (i: input) : t
11          requires { has_length i 5 ∧ valid_input i }
12          requires { intruder_distant_and_slow i }
13          ensures { result .≤ (1500.0:t) } =
14            let j = normalize_input i in
15            let o = (nn @@ j)[clear_of_conflict] in
16            (denormalize_output_t o)


             Fig. 9: A WhyML specification for the unnormalized ACAS Xu ϕ1 property.



         In Table 1, we report runtimes on the original (normalized) ACAS Xu prop-
     erties as well as their unnormalized counterparts. For PyRAT, our graph-editing
     technique preserves the verification outcome for all properties. However, the
     additional overhead is significant enough to cause many timeouts within the
     allocated runtime budget. For nnenum, results remain consistent except for oc-
     casional crashes, which stem from a known bug in its ONNX parsing module. By
     contrast, maraboupy, the Python wrapper of Marabou, exhibits incorrect behav-
     ior: it reports counterexamples for properties ϕ4 , ϕ5 , and ϕ9 , where none should
     exist according to the original specification. Even more concerning, maraboupy
     finds a counterexample for the normalized version of ϕ10 , in direct contradiction
     with Marabou itself, which correctly verifies the property. During our experi-
     ments, maraboupy raised degradation warnings about floating-point arithmetic
     on ϕ10 , which may explain this discrepancy. In particular, CAISAR outputs spec-
     ifications using IEEE 754 double-precision floating-point arithmetic, whereas
     the ACAS Xu networks—and the instances generated from them—operate exclu-
     sively in single precision. Further investigation revealed an inconsistency between
     the plain Marabou solver, which supports only a limited set of ONNX operators,
     and its maraboupy, which supports a broader set. This issue was reported to the
     Marabou developers13 .
         Nevertheless, this example displays how CAISAR allows users to compare
     multiple provers on the same specification; further helping to build a case on the
     correctness of a program.
     13
          https://github.com/NeuralNetworkVerification/Marabou/issues/882
Table 1: ACAS Xu benchmarks on selected verifiers, averaged over three runs. The string
next to the property indicates the Reluplex [28] neural network it was verified against.
Columns Tn (resp. Tu ) report the time (in seconds) required by verifiers to answer on
the original (resp. the unnormalized) queries, while columns An (resp. Au ) report the
actual answers on the original (resp. the unnormalized) queries. A ✓ indicates that a
property is satisfied, a ✗ that a counterexample has been found, a            
                                                                      that a timeout is
reached, and a ? that a runtime crash occurred. Failures of Marabou are expected on
unnormalized properties, as the Concat operator, mandatory for our approach, is not
supported.

 Property          Marabou               maraboupy               PyRAT              nnenum
                Tn An Tu Au         Tn An      Tu     Au   Tn An Tu         Au  Tn An Tu Au
      ϕ1                                            
               3.00 (?) 3.00 (?) 5.00 (✓) 243.00 ( ) 8.00 (✓) 11.00 (✓) 4.00 (✓) 4.00 (✓)
      ϕ2                                            
              37.00 (✓) 3.00 (?) 26.00 (✓) 243.00 ( ) 19.00 (✓) 38.00 (✓) 4.00 (✓) 6.00 (?)
      ϕ3                                                              
              243.00 ( ) 5.00 (?) 243.00 ( ) 243.00 ( ) 246.00 ( ) 246.00 ( ) 4.00 (✓) 4.00 (✓)
      ϕ4                                                                  
              44.00 (✓) 5.00 (?) 36.00 (✓) 4.00 (✗) 25.00 (✓) 246.00 ( ) 4.00 (✓) 4.00 (✓)
      ϕ5                                                                 
              102.00 (✓) 5.00 (?) 93.00 (✓) 5.00 (✗) 246.00 ( ) 246.00 ( ) 4.00 (✓) 5.00 (✓)
      ϕ6                                                                 
              558.00 (✓) 5.00 (?) 566.00 (✓) 1925.00 ( ) 156.00 (✓) 426.00 ( ) 7.00 (✓) 13.00 (?)
      ϕ7                                                              
              485.00 ( ) 5.00 (?) 484.00 ( ) 484.00 ( ) 246.00 ( ) 246.00 ( ) 119.00 (✗) 4.00 (?)
      ϕ8                                                                
              485.00 (✗) 5.00 (?) 8.00 (✗) 248.00 ( ) 246.00 ( ) 246.00 ( ) 4.00 (✗) 4.00 (✗)
      ϕ9                                                                  
              182.00 (✓) 5.00 (?) 222.00 (✓) 5.00 (✗) 61.00 (✓) 246.00 ( ) 6.00 (✓) 9.00 (✓)
      ϕ10                                                                 
              83.00 (✓) 3.00 (?) 151.00 (✗) 245.00 (✗) 13.00 (✓) 246.00 ( ) 4.00 (✓) 5.00 (✓)




3.2         On the Correctness of SVM Parsing
In the context of one-versus-one (ovo) classification, consider an SVM f , a point
x ∈ Rd , a class cl ∈ N, and a perturbation bound ϵ ∈ R. The local robustness
property requires that for all x′ ∈ Rd such that ∥x−x′ ∥ ≤ ϵ, the class maximizing
the output of f remains cl.
    For evaluation, we considered the model linear-1k from the MNIST do-
main provided by the developers of SAVer14 with the associated dataset15 . We
provided the robustness property to CAISAR using the translation from SVM to
NIR described in Section 2.2, and used PyRAT as verifier. We then compared the
results with those produced by SAVer.
    The results are presented in Table 2. The answers produced by CAISAR are
consistent with those of SAVer, but obtained at a runtime approximately two
orders of magnitude higher, independently of whether the robustness property
holds. It should be noted, however, that SAVer was designed specifically for the
verification of robustness properties and cannot be applied to other classes of
properties. In addition, SAVer no longer appears to be under active development,
casting doubts on its long-term usability. By contrast, CAISAR is designed as
14
   The model is available at https://github.com/abstract-machine-learning/
   data-collection/tree/master/domains/mnist/models/svm/linear-1k.dat.zip
15
   The dataset is available at https://github.com/abstract-machine-learning/
   data-collection/blob/master/domains/mnist/datasets/test-set.csv.zip
Table 2: Runtime comparison between SAVer and CAISAR. Valid indicates that robust-
ness holds for the instance. The two solvers agree on the result.
       Instance            Result         SAVer (ms)      PyRAT via CAISAR (ms)
            0               Valid              35                 19,101
            1              Invalid             49                 20,740
            2               Valid              53                 18,552
            3               Valid              41                 22,001
            4               Valid              45                 20,464
            5               Valid              47                 19,300
            6               Valid              43                 20,546
            7               Valid              48                 19,802
            8              Invalid             43                 20,111
            9               Valid              42                 20,957



a general specification and verification framework, and ongoing work aims to
improve its performance on this class of problems.


3.3    Composition of Neural Networks

We evaluated CAISAR on two illustrative specifications concerning multiple NNs:
a property about the output of the sequential composition of two NNs (Fig. 3)
and the comparison of outputs between two NNs (Fig. 4). Both serve as repre-
sentative examples of practical verification tasks, such as quantifying the effect
of quantization or ensuring correctness of composed models.
    For the first specification (see Fig. 3), which involves sequential composition
of NNs, we evaluated CAISAR with maraboupy, nnenum and PyRAT as verifiers.
Within a runtime budget of one hour, maraboupy could not prove the property
(most likely by finding a counterexample), while both nnenum and PyRAT timed
out (see Table 3). It is worth noting that Marabou cannot be used as a backend
prover for this property, since it does not support all ONNX operators required
to encode the sequential combination of the two networks.



      Table 3: Verification results of the sequential composition property of Fig. 3.
                                 Prover             Result
                               maraboupy            Invalid
                                 nnenum            Timeout
                                  PyRAT            Timeout



   For the second specification (see Fig. 4), the results are not revealing, as all
provers ultimately reach timeouts without producing a conclusive answer.
   Overall, these experiments demonstrate that CAISAR can express non-trivial
properties beyond local robustness, dispatching their verification to multiple
backend tools, though performance and conclusiveness remain highly dependent
on the underlying prover.


4   Conclusion
Historically, the formal verification of human-written software evolved from tools
able to verify simple properties to large-scale platforms (e.g. Why3) capable of
handling higher-level properties, decomposing them into smaller properties, and
dispatching them to back-end solvers and analyzers. The AI field, and in partic-
ular ML, already advanced to the first stage of such evolution. We present the
extensible, open-source CAISAR platform, that aims to embody the next stage
of that similar evolution, with emphasis on an expressive language where higher-
level properties can be described, as well as the compilation of these properties
into inputs that existing solvers can handle. We also expanded the range of what
is possible to specify with the clear goal of encouraging the community to target
such specifications in the next versions of their solvers. The authors are keen for
any request for collaboration or special needs, such as handling particular model
architectures or properties.
    Of particular interest is the integration of confidence-based properties, as well
as expanding the set of supported tools. We are also actively developing heuristics
to inform the validation process, particularly through past accumulated knowl-
edge of successful runs (e.g. on use-cases involving X type of properties on Y
type of model with Z activation functions, provers A gave the best results with
configuration C, therefore a suggested strategy is to start with A on use-cases
with similar characteristics to X, Y and Z). An ongoing collaboration is focused
on bridging the validation process with requirement-based engineering.
    CAISAR is made available online, with clear documentation as well as tuto-
rials that can be used in teaching classes to infuse the paramount importance of
safety in the minds of future generations of ML developers. CAISAR’s existence
goes beyond this sole publication: it has the durable support of CEA-List and
a dedicated developing team, giving the platform the stable future necessary for
long-term support.


Acknowledgements This work was partially supported by the SAIF project
(ANR-23-PEIA-0006) and the DeepGreen project (ANR-23-DEGR-0001) funded
by the “France 2030” government investment plan managed by the French Na-
tional Research Agency (ANR).
    The authors thank Serge Durand for his help with Marabou and PyRAT, and
Augustin Lemesle and Julien Lehmann for fruitful discussions.


References
 1. Alberti, M., Bobot, F., Chihani, Z., Girard-Satabin, J., Lemesle, A.: CAISAR:
    A platform for Characterizing Artificial Intelligence Safety and Robustness. In:
    AISafety. CEUR-Workshop Proceedings, Vienne, Austria (Jul 2022), https://hal.
    archives-ouvertes.fr/hal-03687211
 2. Athavale, A., Bartocci, E., Christakis, M., Maffei, M., Nickovic, D., Weissenbacher,
    G.: Verifying global two-safety properties in neural networks with confidence.
    In: Gurfinkel, A., Ganesh, V. (eds.) Computer Aided Verification. pp. 329–351.
    Springer Nature Switzerland, Cham (Jun 2024). https://doi.org/10.48550/arXiv.
    2405.14400, http://arxiv.org/abs/2405.14400, zSCC: 0000000 arXiv:2405.14400
    [cs] type: article
 3. Audemard, G., Lagniez, J.M., Marquis, P.: On the Computation of Contrastive
    Explanations for Boosted Regression Trees. IOS Press (Oct 2024). https://doi.
    org/10.3233/faia240600
 4. Bak, S.: Nnenum: Verification of ReLU Neural Networks with Optimized Abstrac-
    tion Refinement. In: Dutle, A., Moscato, M.M., Titolo, L., Muñoz, C.A., Perez,
    I. (eds.) NASA Formal Methods. pp. 19–36. Lecture Notes in Computer Sci-
    ence, Springer International Publishing, Cham (2021). https://doi.org/10.1007/
    978-3-030-76384-8_2
 5. Balan, R., Singh, M., Zou, D.: Lipschitz properties for deep convolutional networks
    (2017). https://doi.org/10.48550/ARXIV.1701.05217
 6. Balunovic, M., Baader, M., Singh, G., Gehr, T., Vechev, M.: Certifying Geometric
    Robustness of Neural Networks. In: Advances in Neural Information Processing
    Systems. vol. 32. Curran Associates, Inc. (2019), https://papers.nips.cc/paper/
    2019/hash/f7fa6aca028e7ff4ef62d75ed025fe76-Abstract.html
 7. Barbosa, H., Barrett, C.W., Brain, M., Kremer, G., Lachnitt, H., Mann, M., Mo-
    hamed, A., Mohamed, M., Niemetz, A., Nötzli, A., Ozdemir, A., Preiner, M.,
    Reynolds, A., Sheng, Y., Tinelli, C., Zohar, Y.: cvc5: A versatile and industrial-
    strength SMT solver. In: Fisman, D., Rosu, G. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems - 28th International Conference, TACAS
    2022, Held as Part of the European Joint Conferences on Theory and Prac-
    tice of Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings,
    Part I. Lecture Notes in Computer Science, vol. 13243, pp. 415–442. Springer
    (2022). https://doi.org/10.1007/978-3-030-99524-9_24, https://doi.org/10.1007/
    978-3-030-99524-9_24
 8. Bassan, S., Katz, G.: Towards Formal XAI: Formally Approximate Minimal Ex-
    planations of Neural Networks, pp. 187–207. Springer Nature Switzerland (2023).
    https://doi.org/10.1007/978-3-031-30823-9_10
 9. Boetius, D., Leue, S.: Verifying global neural network specifications using hyper-
    properties (2023)
10. Brix, C., Bak, S., Johnson, T.T., Wu, H.: The fifth international verification of
    neural networks competition (vnn-comp 2024): Summary and results (2024). https:
    //doi.org/10.48550/ARXIV.2412.19985, https://arxiv.org/abs/2412.19985
11. Brix, C., Bak, S., Liu, C., Johnson, T.T.: The fourth international verification of
    neural networks competition (vnn-comp 2023): Summary and results (2023)
12. Brix, C., Müller, M.N., Bak, S., Johnson, T.T., Liu, C.: First three years of the
    international verification of neural networks competition (vnn-comp) (2023)
13. Casadio, M., Komendantskaya, E., Daggitt, M.L., Kokke, W., Katz, G., Amir, G.,
    Refaeli, I.: Neural network robustness as a verification property: a principled case
    study. In: International Conference on Computer Aided Verification. pp. 219–231.
    Springer (2022)
14. CEA: Caisar (May 2024), https://catalog.confiance.ai/records/px81f-r1p78
15. Chareton, C., Bardin, S., Bobot, F., Perrelle, V., Valiron, B.: An Auto-
    mated Deductive Verification Framework for Circuit-building Quantum Programs,
    pp. 148–177. Springer International Publishing (2021). https://doi.org/10.1007/
    978-3-030-72019-3_6
16. Chen, T., Guestrin, C.: XGBoost: A scalable tree boosting system. In: Proceedings
    of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and
    Data Mining. pp. 785–794. KDD ’16, ACM, New York, NY, USA (2016). https://
    doi.org/10.1145/2939672.2939785, http://doi.acm.org/10.1145/2939672.2939785
17. Conchon, S., Coquereau, A., Iguernlala, M., Mebsout, A.: Alt-Ergo 2.2. In: SMT
    Workshop: International Workshop on Satisfiability Modulo Theories. Oxford,
    United Kingdom (Jul 2018), https://hal.inria.fr/hal-01960203
18. Conchon, S., Filliâtre, J.C., Signoles, J.: Designing a Generic Graph Library us-
    ing ML Functors. In: Morazán, M.T., Nilsson, H. (eds.) The Eighth Symposium
    on Trends in Functional Programming. vol. TR-SHU-CS-2007-04-1, pp. XII/1–13.
    Seton Hall University, New York, USA (Apr 2007), https://usr.lmf.cnrs.fr/~jcf/
    publis/ocamlgraph-tfp07.ps
19. Cordeiro, L.C., Daggitt, M.L., Girard-Satabin, J., Isac, O., Johnson, T.T., Katz,
    G., Komendantskaya, E., Lemesle, A., Manino, E., Šinkarovs, A., Wu, H.: Neural
    network verification is a programming language challenge. In: Vafeiadis, V. (ed.)
    Programming Languages and Systems. pp. 206–235. Springer Nature Switzerland
    (2025). https://doi.org/10.1007/978-3-031-91118-7_9
20. Cristianini, N., Ricci, E.: Support Vector Machines, pp. 928–932. Springer US,
    Boston, MA (2008). https://doi.org/10.1007/978-0-387-30162-4_415, https://doi.
    org/10.1007/978-0-387-30162-4_415
21. Daggitt, M.L., Kokke, W., Atkey, R., Arnaboldi, L., Komendantskya, E.: Vehicle:
    Interfacing neural network verifiers with interactive theorem provers (2022). https:
    //doi.org/10.48550/ARXIV.2202.05207, https://arxiv.org/abs/2202.05207
22. Daggitt, M.L., Kokke, W., Atkey, R., Slusarz, N., Arnaboldi, L., Komendantskaya,
    E.: Vehicle: Bridging the embedding gap in the verification of neuro-symbolic pro-
    grams (2024). https://doi.org/10.48550/ARXIV.2401.06379
23. de Moura, L., Bjørner, N.: Z3: An Efficient SMT Solver. In: Ramakrishnan, C.R.,
    Rehof, J. (eds.) Tools and Algorithms for the Construction and Analysis of Sys-
    tems. pp. 337–340. Lecture Notes in Computer Science, Springer, Berlin, Heidel-
    berg (2008). https://doi.org/10.1007/978-3-540-78800-3_24
24. Durand, S., Lemesle, A., Chihani, Z., Urban, C., Terrier, F.: ReCIPH: Relational
    Coefficients for Input Partitioning Heuristic. WFVML 2022 (Jul 2022), https://
    inria.hal.science/hal-03926281, poster
25. Filliâtre, J.C., Paskevich, A.: Why3 - Where Programs Meet Provers. In: Felleisen,
    M., Gardner, P. (eds.) Programming Languages and Systems. pp. 125–128. Lecture
    Notes in Computer Science, Springer, Berlin, Heidelberg (2013). https://doi.org/
    10.1007/978-3-642-37036-6_8
26. Fischer, M., Balunovic, M., Drachsler-Cohen, D., Gehr, T., Zhang, C., Vechev,
    M.: DL2: Training and querying neural networks with logic. In: Chaudhuri, K.,
    Salakhutdinov, R. (eds.) Proceedings of the 36th International Conference on Ma-
    chine Learning. Proceedings of Machine Learning Research, vol. 97, pp. 1931–1941.
    PMLR (09–15 Jun 2019), https://proceedings.mlr.press/v97/fischer19a.html
27. Girard-Satabin, J., Charpiat, G., Chihani, Z., Schoenauer, M.: CAMUS: A Frame-
    work to Build Formal Specifications for Deep Perception Systems Using Simulators.
    In: ECAI 2020 - 24th European Conference on Artificial Intelligence. Santiago de
    Compostela, Spain (Jun 2020), https://hal.inria.fr/hal-02440520
28. Katz, G., Barrett, C., Dill, D.L., Julian, K., Kochenderfer, M.J.: Reluplex: An
    Efficient SMT Solver for Verifying Deep Neural Networks, pp. 97–117. Springer
    International Publishing (2017). https://doi.org/10.1007/978-3-319-63387-9_5
29. Katz, G., Huang, D.A., Ibeling, D., Julian, K., Lazarus, C., Lim, R., Shah, P.,
    Thakoor, S., Wu, H., Zeljić, A., Dill, D.L., Kochenderfer, M.J., Barrett, C.: The
    Marabou Framework for Verification and Analysis of Deep Neural Networks. In:
    Dillig, I., Tasiran, S. (eds.) Computer Aided Verification, vol. 11561, pp. 443–
    452. Springer International Publishing, Cham (2019). https://doi.org/10.1007/
    978-3-030-25540-4_26
30. König, M., Bosman, A.W., Hoos, H.H., van Rijn, J.N.: Critically assessing the state
    of the art in neural network verification. Journal of Machine Learning Research
    25(12), 1–53 (2024), http://jmlr.org/papers/v25/23-0119.html
31. Lemesle, A., Lehmann, J., Gall, T.L.: Neural network verification with pyrat
    (2024). https://doi.org/10.48550/ARXIV.2410.23903
32. Lemesle, A., Varasse, A., Chihani, Z., Tachet, D.: AIMOS: Metamorphic Testing
    of AI - AnIndustrial Application. WAISE 2023 (2023)
33. Pulina, L., Tacchella, A.: Never: a tool for artificial neural networks veri-
    fication. Annals of Mathematics and Artificial Intelligence 62(3–4), 403–425
    (jul 2011). https://doi.org/10.1007/s10472-011-9243-0, https://doi.org/10.1007/
    s10472-011-9243-0
34. Ranzato, F., Zanella, M.: Robustness verification of support vector machines. In:
    Chang, B.Y.E. (ed.) Static Analysis. pp. 271–295. Springer International Publish-
    ing, Cham (2019)
35. Singh, G., Ganvir, R., Püschel, M., Vechev, M.: Beyond the Single
    Neuron Convex Barrier for Neural Network Certification. In: Wallach,
    H., Larochelle, H., Beygelzimer, A., Alché-Buc, F.d., Fox, E., Garnett,
    R. (eds.) Advances in Neural Information Processing Systems 32, pp.
    15098–15109. Curran Associates, Inc. (2019), http://papers.nips.cc/paper/
    9646-beyond-the-single-neuron-convex-barrier-for-neural-network-certification.
    pdf
36. Trojanek, P., Eder, K.: Verification and testing of mobile robot navigation al-
    gorithms: A case study in spark. In: 2014 IEEE/RSJ International Conference
    on Intelligent Robots and Systems. pp. 1489–1494. IEEE (Sep 2014). https:
    //doi.org/10.1109/iros.2014.6942753
37. Urban, C., Christakis, M., Wüstholz, V., Zhang, F.: Perfectly Parallel Fairness
    Certification of Neural Networks. arXiv:1912.02499 [cs] (Dec 2019)
38. Urban, C., Miné, A.: A Review of Formal Methods applied to Machine Learning.
    arXiv:2104.02466 [cs] (Apr 2021)
39. van der Walt, S., Schönberger, J.L., Nunez-Iglesias, J., Boulogne, F., Warner, J.D.,
    Yager, N., Gouillart, E., Yu, T., the scikit-image contributors: scikit-image: image
    processing in Python. PeerJ 2, e453 (6 2014). https://doi.org/10.7717/peerj.453,
    https://doi.org/10.7717/peerj.453
40. Wang, S., Zhang, H., Xu, K., Lin, X., Jana, S., Hsieh, C.J., Kolter, J.Z.: Beta-
    CROWN: Efficient Bound Propagation with Per-neuron Split Constraints for Com-
    plete and Incomplete Neural Network Robustness Verification, http://arxiv.org/
    abs/2103.06624
41. Wu, H., Isac, O., Zeljić, A., Tagomori, T., Daggitt, M., Kokke, W., Refaeli, I.,
    Amir, G., Julian, K., Bassan, S., Huang, P., Lahav, O., Wu, M., Zhang, M., Komen-
    dantskaya, E., Katz, G., Barrett, C.: Marabou 2.0: A versatile formal analyzer of
    neural networks (2024). https://doi.org/10.48550/ARXIV.2401.14461
42. Wu, M., Wu, H., Barrett, C.: Verix: Towards verified explainability of deep neural
    networks (2023)
43. Xie, X., Kersting, K., Neider, D.: Neuro-symbolic verification of deep neural net-
    works. In: Raedt, L.D. (ed.) Proceedings of the Thirty-First International Joint
    Conference on Artificial Intelligence, IJCAI-22. pp. 3622–3628. International Joint
    Conferences on Artificial Intelligence Organization (7 2022). https://doi.org/10.
    24963/ijcai.2022/503, https://doi.org/10.24963/ijcai.2022/503, main Track
