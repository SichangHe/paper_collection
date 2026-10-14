                                                 T ORCH L EAN : F ORMALIZING N EURAL N ETWORKS IN L EAN

                                                                                                  A P REPRINT


                                                                        Robert Joseph George1 , Jennifer Cruden1 , Will Adkisson2 ,
                                                                         Xiangru Zhong3 , Huan Zhang3 , Anima Anandkumar1
                                                                                     1
                                                                                       California Institute of Technology
                                                                                    2
                                                                                      Washington University in St. Louis
                                                                                 3
arXiv:2602.22631v2 [cs.MS] 24 May 2026




                                                                                   University of Illinois Urbana-Champaign




                                                                                                 A BSTRACT
                                                     Neural networks are increasingly deployed in scientific, safety critical, and mission critical pipelines,
                                                     yet verification and analysis are often performed outside the programming environment that defines,
                                                     runs, and exports the model. This separation creates a semantic gap between the executed network
                                                     and the analyzed artifact: guarantees can depend on implicit conventions about operator semantics,
                                                     tensor layouts, preprocessing, floating-point behavior, graph transformations, accelerated kernels,
                                                     and externally produced certificates. We present T ORCH L EAN, a unified framework for formalizing,
                                                     executing, and verifying neural networks in Lean 4. T ORCH L EAN treats learned models as executable
                                                     programs and first-class mathematical objects with a shared semantics for computation, verification,
                                                     and theorem proving. The framework provides a PyTorch style API for typed tensors, layers, objec-
                                                     tives, optimizers, automatic differentiation, and graph programs, together with eager and compiled
                                                     execution paths that lower to a common computation-graph representation. T ORCH L EAN supports
                                                     exact and finite-precision tensor semantics, verified reverse-mode differentiation for supported graph
                                                     programs, interval and affine bound propagation, CROWN/LiRPA style certificate checking, import
                                                     and export workflows, and CUDA-backed execution through explicit FFI boundaries. It also includes
                                                     formal semantic layers for modern learning systems, including attention and FlashAttention, state-
                                                     space sequence models, diffusion and sampling processes, probability kernels, reinforcement-learning
                                                     objectives and Markov decision processes, and self-supervised objectives such as masked autoencod-
                                                     ing, JEPA-style predictive views, and variance/correlation-based anti-collapse losses. Together, these
                                                     components provide a semantic foundation for verified machine learning, where executable neural
                                                     network artifacts, verification procedures, runtime boundaries, and mathematical claims can be stated
                                                     and related inside a single theorem-proving environment1 .

                                         Keywords neural networks · verification · formalization · automatic differentiation · Lean


                                         1       Introduction

                                         Neural networks are increasingly embedded in systems where mistakes have physical or societal cost, and the machine
                                         learning community is correspondingly placing more weight on guarantees that go beyond empirical accuracy: robust-
                                         ness to perturbations, satisfaction of hard safety and stability constraints, and conservative bounds on quantities derived
                                         from a network’s computation. This has driven an active verification ecosystem spanning solver-based approaches that
                                         reduce verification queries to constraint solving, such as Reluplex and Marabou for piecewise-linear networks [Katz
                                         et al., 2017, 2019], as well as scalable relaxation and abstract interpretation methods that compute certified enclosures
                                         by bound propagation Gowal et al. [2018], Zhang et al. [2018], Singh et al. [2019]. Surveys and systems papers
                                         emphasize that such techniques are central to validating learning-enabled components in autonomy, control, and other
                                         high-assurance pipelines Xiang et al. [2018]. Despite this progress, turning verifier outputs into dependable guarantees
                                         remains difficult in practice. The issue is not only the strength of a verifier, but also the meaning of the artifact being
                                         verified. A trained network may appear as a PyTorch nn.Module, an exported ONNX or FX graph, a compiler IR, a
                                             1
                                                 Code is available athttps://github.com/lean-dojo/TorchLean
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                            A P REPRINT



CUDA-backed runtime computation, an external CROWN certificate, or a mathematical object in a paper proof. These
artifacts are connected by exporters, graph rewrites, scalar semantics, layout conventions, and runtime libraries. If
these boundaries are not made explicit, a property can be proved about one object while the deployed system executes
another. We highlight four concrete failure modes.




Figure 1: T ORCH L EAN provides a shared semantic layer for verified machine learning. Model code, imported
graphs, modern ML workflows, scientific ML artifacts, and certificates are funneled into a common typed tensor and
operator-tagged SSA/DAG graph semantics in Lean. Execution, automatic differentiation, bound propagation, and
certificate checking are all performed against this shared representation, enabling checked claims in robustness, control,
scientific machine learning, and bug detection while keeping external runtimes and solvers as explicit boundaries.
(1) Export boundaries create semantic drift. In modern workflows, the trained model is a program, while verifiers
typically consume an exported or recompiled surrogate, such as TorchScript, ONNX, FX, or a custom verification
IR. This conversion boundary is exactly where subtle mismatches arise. Trace-based export can miss control flow
and dynamic behavior, and even when export succeeds, the resulting graph may only reflect the operations executed
in a particular run PyTorch Contributors [2025]. Interchange formats also version operator sets and require models
to declare the opsets they rely on ONNX Contributors [2026]. Thus, the meaning of an exported network becomes
entangled with tool, version, and backend assumptions that can drift across runtimes. Figure 2 summarizes this gap.
                                             Standard pipeline
                                                    ?            ?
                                 PyTorch      Export       ONNX            Verifier (CROWN/LiRPA)

                                           T ORCH L EAN pipeline
                                      Lean 4 (machine-checked semantics)

                                T ORCH L EAN program                 Shared IR             Verifier (CROWN)


Figure 2: Semantic gap: the standard pipeline (top) chains PyTorch → Export → ONNX → Verifier, with potential
drift at each conversion step; T ORCH L EAN (bottom) keeps a single shared IR as the semantic target for both execution
and verification (Verifier artifacts are checked against this same meaning).
(2) Floating-point semantics can invalidate idealized guarantees. Most verification methods are stated over real
arithmetic or over simplified numerical models, while deployment uses IEEE-754 arithmetic with rounding, overflow,
underflow, NaNs, infinities, signed zeros, mixed precision, and backend-specific algorithm choices IEEE Standards
Association [2019]. Several lines of work show that treating floating point as an implementation detail can invalidate
verification conclusions. Jia and Rinard [2020] demonstrated that numerical error can be exploited to refute robustness
claims, motivating conservative modeling of finite-precision effects. More recently, Szász et al. [2025] argue that


                                                                      2
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                            A P REPRINT



theoretical soundness for a real-valued model does not automatically imply practical soundness for deployed floating-
point networks, and Hwang et al. [2025] show that robust approximation results for floating-point networks require
explicit finite-precision semantics.
(3) Certification often stops short of the executed workflow. Neural networks are brittle to worst-case perturbations
and distribution shifts, motivating certified robustness and safety properties rather than empirical testing alone Szegedy
et al. [2013], Goodfellow et al. [2014]. This need is especially acute for learning-enabled components in control
and autonomy, where verification must connect to the implemented artifact Xiang et al. [2018]. It also appears in
scientific machine learning. For example, physics-informed neural networks use automatic differentiation to enforce
PDE residuals, so meaningful certificates may need to cover both function values and derivatives Raissi et al. [2019].
These settings require a pipeline in which execution, differentiation, and certification refer to the same model semantics.
(4) Real ML bugs often live at semantic boundaries. Empirical studies of deep learning bugs show that many failures
are not exotic theorem-proving corner cases, but ordinary semantic boundary errors: wrong tensor shapes, unintended
broadcasting, dtype conversions, layout assumptions, padding conventions, train/eval state, masking mistakes, data
preprocessing mismatches, and compiler or runtime transformations Islam et al. [2019], Humbatova et al. [2020], Shen
et al. [2021]. These bugs are especially dangerous for verification because they can preserve surface-level compatibility
while changing the property actually being checked. A robustness certificate for the wrong padding convention, attention
mask, batch axis, or exported graph is still a certificate, but not for the intended computation.
We address these challenges with T ORCH L EAN, a unified framework for formalizing, executing, and verifying neural
networks in L EAN 4. Lean is both a practical functional programming language and an interactive theorem prover
with a small trusted kernel, extensible automation, metaprogramming, and code generation Moura and Ullrich [2021],
Ebner et al. [2017]. This makes it well suited to our goal: not only to state properties of neural networks, but to
implement the surrounding pipeline while making its semantic assumptions explicit. T ORCH L EAN provides a PyTorch
style API for typed tensors, layers, models, objectives, optimizers, automatic differentiation, and training workflows.
Programs execute eagerly or lower to a shared operator-tagged SSA/DAG computation-graph IR, which serves as the
common semantic target for execution, differentiation, verification, and certificate checking. Prior work has formalized
neural-network reasoning in other proof assistants, including Isabelle/HOL tooling for importing models and proving
safety or correctness properties Brucker and Stell [2023]. We build in Lean because it combines proof checking with a
growing ecosystem for mathematics and computer science, including mathlib (The mathlib Community, 2020) and
recent efforts such as CSLib (Barrett et al., 2026). In this setting, T ORCH L EAN treats the network definition as the
semantic ground truth and organizes specification, runtime execution, and verification around the same graph semantics.
We summarize our contributions as follows.
• T ORCH L EAN: PyTorch style neural-network programming in L EAN. We provide a Lean based API for defining
  tensors, layers, models, objectives, optimizers, data loaders, and multi-epoch training loops. The runtime supports
  eager execution and a compiled mode that lowers programs to the shared IR. CPU execution is supported by default,
  while CUDA-backed dense/matmul and batched-matmul paths, reductions, broadcasts, views, convolution and
  pooling families, FFT/spectral kernels, normalization kernels, attention/fused-attention paths, gather/scatter utilities,
  positional/RoPE helpers, and selective-scan-style sequence kernels are exposed through explicit native FFI boundaries.
  These kernels are treated as runtime interfaces, not as silently verified code.
• A shared IR for execution, differentiation, and verification. T ORCH L EAN compiles supported programs to an
  operator-tagged SSA/DAG computation graph with a precise denotation. The same graph object is used by the
  executor, compiled evaluator, reverse-mode automatic differentiation, IBP/CROWN style bound propagation, and
  certificate checking. For the supported fragment, we prove a graph-parametric reverse-mode theorem: backprop
  computes the adjoint Fréchet derivative of [[G]] for any well-typed graph G satisfying local derivative-correctness
  hypotheses.
• Explicit scalar and finite-precision semantics. The same definitions can be instantiated over exact mathematical
  scalars for proofs, executable finite-precision scalars for runtime behavior, and interval or affine domains for bounds.
  We provide a rounding model for proofs, executable IEEE-style binary32 components, endpoint interval reasoning,
  and explicit external-producer boundaries, including Arb/FLINT-style oracles for rigorous transcendental enclosures
  when needed.
• Verification and certificate checking on the shared semantics. On the shared IR, T ORCH L EAN implements IBP,
  CROWN/LiRPA style affine relaxations, and certificate checking. External artifacts are not accepted as guarantees
  by fiat; they are checked against the graph semantics consumed by Lean. We validate this pipeline on robustness,
  control-style safety, PINN and derivative-bound examples, VNN-COMP style ONNX/VNN-LIB slices, and regression
  tests designed to expose semantic boundary failures.
• Modern ML workflows and semantic bug checks. T ORCH L EAN includes runnable and formalized components
  for supervised vision and tabular models, GPT-style attention, FlashAttention specifications, Mamba/state-space


                                                            3
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                            A P REPRINT



    layers, diffusion and sampling processes, FNO/PINN-style scientific ML, PPO/Gymnasium rollouts, Markov-kernel
    MDP semantics, self-supervised objectives such as MAE and JEPA-style predictive views, PyTorch round trips, 3D
    vision certificates, and a bug zoo of semantic boundary checks. Python, Julia, Arb/FLINT, PyTorch, Gymnasium,
    CUDA, and CROWN family solvers appear as explicit producers or runtimes; Lean remains the checker for the
    formal artifacts that cross those boundaries.

2     Methodology
Computation graphs and our IR (definitions). Modern ML systems commonly represent a model as a computation
graph: a directed graph in which nodes are primitive operations (e.g., MatMul, Conv, ReLU) and edges carry tensors
(intermediate values) between operations. This is the standard representation used by deployment/exchange formats
such as ONNX, where a graph is a side-effect-free computation composed of nodes that call operators and whose
dataflow must admit a topological evaluation order. A graph is a directed acyclic graph (DAG) if it has no directed
cycles; equivalently, it admits a topological evaluation order.
An intermediate representation (IR) is a compiler style, machine- and language-independent program representation
designed to be a stable target for analysis and transformation. In T ORCH L EAN, the IR is an operator-tagged computation
graph: each node carries an explicit operator tag identifying the primitive it denotes, such as linear, relu, conv2d,
attention, or softmax, together with shape metadata. Execution and verification therefore interpret nodes by the
same primitive semantics rather than by an implicit convention inherited from an external framework. We store graphs in
static single assignment (SSA) form: every intermediate value is defined exactly once and then referenced by subsequent
nodes. SSA is a standard compiler IR discipline that simplifies dataflow reasoning and enables deterministic evaluation
and induction over the node list Cytron et al. [1991].
Mathematically, for a scalar semantics α and tensor shape s, write Tensorα (s) for tensors of shape s with scalar entries
interpreted in α. Each operator tag τ has a typed signature sig(τ ) = (s1 , . . . , sk ) → s and a denotation
                              [[τ ]]α : Tensorα (s1 ) × · · · × Tensorα (sk ) → Tensorα (s).
A well-typed SSA/DAG graph G denotes a function
                  [[G]]α : Tensorα (s1 ) × · · · × Tensorα (sm ) → Tensorα (t1 ) × · · · × Tensorα (tr ),
obtained by evaluating nodes in topological order. The same syntax can be interpreted over exact reals, finite-precision
execution domains, intervals, or affine relaxations:
                                [[G]]R ,    [[G]]Float32 ,   [[G]]Interval ,    [[G]]Affine .

Our goal is to eliminate the semantic gap between the model that is executed during training or inference and the
model that is analyzed by bounds or certificates. T ORCH L EAN treats the network definition as the single semantic
reference point and provides multiple interpretations over the same meaning. Concretely, a model compiles to a shared
operator-tagged computation-graph IR in SSA/DAG form, so the denotation is total and deterministic by evaluation
in topological order. This IR is the common target for (i) training and inference, (ii) verified reverse-mode automatic
differentiation, and (iii) Lean based bound propagation and certificate checking. External verifiers are optional producers
rather than trusted authorities: their outputs are interpreted as certificates checked against the Lean semantics of the
shared graph, reducing the trusted computing base.
Beyond standard feed-forward networks, the same interface also supports modern workflow-level operators and
objectives. Attention and FlashAttention style fused operators are specified by equivalence to masked scaled dot-product
attention,
                                                                     QK ⊤
                                                                                 
                                  Attn(Q, K, V, M ) = softmax √ + M V,
                                                                         d
where the mask is part of the formal operator semantics. Diffusion/sampling steps, reinforcement-learning returns and
Bellman operators, state-space sequence layers, and self-supervised masking or view objectives are represented as typed
specifications connected to the same graph and tensor semantics.

2.1    Specification layer

Mainstream ML frameworks represent tensor shapes dynamically: tensors carry runtime shapes, and incompatibilities
surface late, often as runtime exceptions or subtle semantic bugs. Empirically, tensor shape faults are among the most
prevalent classes of deep learning bugs and frequently lead to crashes Wu et al. [2021]. T ORCH L EAN takes a semantic


                                                             4
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                           A P REPRINT



view: shape constraints are part of the type of a tensor, so ill-shaped programs are unrepresentable. This makes theorem
statements cleaner, reduces repeated “shapes match” side conditions, and moves many plumbing errors from testing to
type checking.
Core datatypes (shapes and tensors). A tensor is indexed by a scalar domain α and a shape s; shapes form an
inductive tree, where common ML shapes are nested applications of dim. Tensors are represented structurally as total
index functions. This functional view is well suited for proofs: tensor operations are defined by recursion on shape,
and extensional equality reduces tensor equality to pointwise equality. The specification layer intentionally does not
commit to a storage layout such as row-major or column-major order, making it suitable as a semantic reference across
execution backends.
/-- Shape-indexed tensors. -/
inductive Tensor (a : Type) : Shape -> Type where
  | scalar : a -> Tensor a .scalar
  | dim    : forall {n s}, (Fin n -> Tensor a s) ->
             Tensor a (.dim n s)

In this model,
                     Tensorα (scalar) = α,          Tensorα (dim(n, s)) = Fin(n) → Tensorα (s).
Thus a tensor is a total function over a finite index set. Pointwise maps, zips, reductions, reshapes, broadcasts, and
masks are explicit typed operations. In particular, broadcasting is not a silent runtime convention; it is represented by a
shape transformation with its own typing and semantic lemmas.
Typed modules (compositional networks). At the specification level, each layer is a typed morphism between tensor
spaces,
                                        L : Tensorα (sin ) → Tensorα (sout ),
so composing networks is analogous to composing nn.Modules in PyTorch, but with shape contracts enforced by the
type checker. In T ORCH L EAN, trainable parameters are carried as a shape-indexed heterogeneous list, one tensor per
parameter shape, so parameter routing is type-driven. Composition is only definable when intermediate shapes match;
ill-shaped networks do not typecheck.
For example, a linear layer with W : Tensorα (dout × din ),      b : Tensorα (dout ) denotes
                                                                 X
                                           LinearW,b (x)i = bi +      Wij xj .
                                                                  j<din
The same definition can be interpreted over R for proof level reasoning, over Float32 or IEEE32Exec for execution,
or over interval and affine domains for verification. Because repeated functional updates, such as SGD or Adam steps,
can build long closure chains, T ORCH L EAN provides materialization, which rebuilds a tensor into an array-backed
normal form with the same extensional meaning but faster evaluation.
Modern operator contracts. The specification layer also records contracts for modern neural-network components.
Masked attention is specified directly as a mathematical operator, with causal, padding, or arbitrary masks included in the
input semantics. FlashAttention style fused or tiled implementations are related to this denotation by equality theorems
at the specification level, rather than by treating a fused kernel as a new informal primitive. Sequence/state-space layers
are specified as finite recurrences; diffusion and sampling components are specified by noising and denoising transition
maps; reinforcement-learning components are specified by returns, temporal-difference residuals, and Bellman-style
operators; and self-supervised objectives are specified by explicit view, mask, and target contracts.

2.2   Runtime layer

Design target. The runtime layer connects proof level definitions to runnable training and inference. The user-facing
workflow mirrors PyTorch: define a module, run a forward pass, call backward, and update parameters. The key
difference is that runtime execution is organized around a verifier semantic target. A T ORCH L EAN program can run
eagerly, recording a dynamic tape, or compile to the shared operator-tagged SSA/DAG IR consumed by differentiation,
bound propagation, and certificate checking.
Training and data path. The runtime includes reusable ML infrastructure rather than only isolated forward passes:
CSV/NPY loaders, minibatch tensor loaders, JSON training logs, parameter import/export, checkpointing, and optimiz-
ers including SGD, momentum, Adagrad, RMSProp, Adam, AdamW, and Adadelta. A typical training loop has the
usual mathematical shape                                                      
                                            θt+1 = Opt θt , ∇θ L(θt ; Bt ), st ,
where Bt is the minibatch, st is optimizer state, and the loss is computed by a T ORCH L EAN program with a chosen
scalar semantics. The important point is that the same model parameters θt , loss graph, and gradient computation can
later be lowered to the verifier IR rather than reconstructed through an informal export path.


                                                            5
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                                A P REPRINT



 import torch.nn as nn                                            open TorchLean

# Model + optimizer (semantics live in the runtime)              -- Model + samples (compiled mode)
  model = nn.Linear(2, 1)                                          def model := sequential [linear 2 1, relu]
  opt = torch.optim.SGD(model.parameters(), lr=0.2)                def samples := [(x1, y1), (x2, y2), (x3, y3)]

# Training data                                                  -- Explicit Float32 semantics for this run
  x = torch.tensor([[1.,0.],[0.,1.],[1.,1.]])                    def main : IO Unit := do
  y = torch.tensor([[2.],[-3.],[-1.]])                             let mod <- instantiate model (scalar := IEEE32Exec) .
                                                                      compiled
# Training loop (autodiff + updates external)                      let opt := Optim.sgd (scalar := IEEE32Exec) (lr := 0.2)
  for step in range(10):                                           for step in [0:10] do
    opt.zero_grad()                                                  let loss := mse (mod.forward batch.x) batch.y
    loss = nn.functional.mse_loss(model(x), y)                       backward loss
    loss.backward(); opt.step()                                      opt.step mod.params



Figure 3: PyTorch vs. T ORCH L EAN. We highlight comparable blocks: model/setup (yellow), data (blue), loop
structure (purple), and per-step updates (green). In T ORCH L EAN, the same model can be executed, lowered to the
shared IR, differentiated, and passed to verification.
Two execution modes, one semantic target. Eager mode executes operations immediately and records a tape in the
style of define-by-run systems. Each tape entry stores the operator tag, parent references, forward values needed by the
VJP rule, and an accumulator for cotangents. Compiled mode lowers the same program to the shared operator-tagged
SSA/DAG IR and evaluates that graph. This is not torch.compile-style kernel optimization. Its role is semantic: it
produces the graph object that theorems and checkers consume.
For a program p with parameters θ, lowering produces a graph G and parameter store Pθ . The intended correspondence
is
                             p ⇓ (G, Pθ )      =⇒        evalsrc (p, θ, x) = [[G]]α (Pθ , x),
for the supported forward fragment and scalar semantics α. This is the semantic bridge that allows us to develop in a
PyTorch-like style while proving properties of the graph artifact.
Reverse-mode AD. Reverse-mode automatic differentiation is proved once at the graph level. Let G be a well-typed
SSA/DAG graph over R, let [[G]] be its denotation, and let ȳ be an output cotangent. Backpropagation computes the
adjoint derivative:                                                          ∗
                                         backprop(G, x, ȳ) = D[[G]](x) ȳ.
Operationally, this is implemented by a reverse topological sweep:
                                                                     
                             v̄i += VJPτj ,i vi1 , . . . , vik , v̄j   for every edge i → j.
Accumulation is essential: if a value is consumed by multiple downstream nodes, the corresponding cotangent is the
sum of all downstream contributions. The graph theorem follows by composing local derivative-correctness lemmas for
primitive operators.
  Theorem 2.1: Reverse-mode AD correctness
  Let G be a well-typed SSA/DAG computation graph over R with input context Γ. Assume GraphFDeriv
  Correct G. Define bpG (x, seed) := backpropVec(G, x, seed). Then for any input x and cotangent seed,
                                                                  ⊤
                                 bpG (x, seed) = D (evalVec G)(x) seed.
  For non-smooth primitives, such as ReLU at 0, we use the pointwise variant GraphFDerivCorrectAt under
  explicit side conditions; the executable convention is deterministic at kink points.

For classification losses and embedding-style models, the runtime separates differentiable tensor values from non-
differentiable integer data. Labels, token ids, and row indices are provided through a separate index channel. Gradients
flow through floating-point tensor values, such as an embedding table, but not through the integer selectors:
                         W 7→ W [idx]      is differentiable in W,      idx is a read-only selector.
This avoids mixed-dtype differentiable graphs while still supporting common ML patterns such as cross-entropy with
integer labels and embedding lookup.
CUDA and Lean FFI. T ORCH L EAN also provides an optional native runtime path through Lean’s foreign-function
interface. In the default build, CPU implementations and stubs keep the repository portable. With CUDA enabled, Lean


                                                             6
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                           A P REPRINT



external declarations call C/CUDA wrappers that allocate or receive device buffers, dispatch kernels, and return runtime
handles or copied tensors to Lean. The CUDA surface includes dense matrix operations, cuBLAS-backed matmuls and
batched matmuls, deterministic reductions, broadcasts, views, reshapes, convolution/pooling and transposed-convolution
kernels, FFT/spectral kernels for FNO-style examples, softmax/log-softmax, normalization kernels, attention-oriented
and fused-attention kernels, gather/scatter utilities, positional/RoPE helpers, and selective-scan-style sequence kernels.
A typical boundary has the following shape: Lean exposes a typed wrapper, while the implementation lives in C/CUDA.
The CUDA path is exposed through Lean @[extern] declarations; the detailed FFI surface and native wrapper contracts
are described in Appendix D. A representative boundary is:

                        Listing 1: Representative CUDA runtime boundary through Lean FFI.
@[extern "torchlean_cuda_buffer_bmm"]
opaque bmm
  (A B : Buffer) (batch m n p : UInt32) : Buffer

@[extern "torchlean_cuda_buffer_flash_attention_fwd"]
opaque flashAttentionFwd
  (Q K V mask : Buffer)
  (hasMask batch n d : UInt32) (scale : Float) : Buffer

The CUDA path is deliberately not hidden inside the logic. Native kernels are not Lean theorems and are not part of
Lean’s trusted kernel. Each native call is attached to a formally specified operator tag τ , whose meaning is already
given by the shared semantics. The intended conformance statement is nativeτ (x) ≈ [[τ ]]Float32 (x), under explicit
preconditions about shape, dtype, layout, device memory, aliasing, rounding mode, reduction order, and determinism.
When this agreement is tested rather than proved, it is recorded as a runtime conformance assumption. Thus CUDA
provides an execution backend, not a second semantics.
This distinction matters for kernels whose hardware behavior may depend on scheduling or library choices. For example,
parallel reductions and some pooling/attention backward passes may use nondeterministic accumulation orders; cuBLAS
and custom CUDA kernels may select implementation variants; and fused attention kernels may change memory layout
and evaluation schedule. In T ORCH L EAN, the theorem-facing claim is stated against the graph/operator semantics,
while the CUDA implementation is required to refine that semantics under a declared deployment configuration.
Interop as producer/checker plumbing. Runtime support also includes PyTorch state-dict import/export, PyTorch
graph-capture import into the torchlean.ir.v1 dialect, IR-to-PyTorch code generation, JSON artifact loaders, Julia
subprocess wrappers for small certificate producers, a Gymnasium bridge for RL rollouts, PPO-style rollout helpers,
and an Arb/FLINT oracle path for validated numeric enclosures. These integrations are not hidden inside theorem
statements. External tools produce weights, traces, rollouts, candidate bounds, or enclosures; Lean either checks the
property-bearing artifact or records a named oracle/conformance assumption.
The runtime layer therefore has two roles. It makes T ORCH L EAN usable as an ML programming environment, and it
preserves the semantic path from executable artifacts to checked claims. The price is that high performance backends
and external producers remain explicit boundaries. This is intentional: the paper’s formal claims are about the Lean
graph semantics and the artifacts Lean checks, not about unverified native code by default.

2.3   Floating Point Semantics

Many verification claims hinge on subtle numerical behavior such as rounding, overflow/underflow, NaN/Inf propagation,
signed zeros, non-associativity, mixed precision, and library-level conventions for operations such as min, max, pooling,
reductions, and transcendental functions. IEEE 754 standardizes floating-point formats, rounding rules, and exceptional
values IEEE Standards Association [2019]. In Lean, however, the built-in runtime floating-point types are opaque to
the kernel: floating-point values are not encoded in the logic, so the kernel cannot compute with or reason about them
without additional assumptions. Consequently, T ORCH L EAN separates fast execution from proved semantics and makes
the trust boundary explicit.
For explicit numeric semantics, T ORCH L EAN makes numerical assumptions first-class by instantiating the same
model over multiple scalar domains α, each serving a distinct role. We use α = R for clean reference semantics
in analytic reasoning and verified differentiation; enclosure domains such as α = Interval and affine domains
for sound region-wise bounds in verification pipelines; and explicit finite-precision semantics for execution. For
executable Float32, we provide IEEE32Exec, a Lean-defined bit-level model of IEEE-754 binary32, including signed
zeros, subnormals, NaNs/Infs, and rounding behavior. In parallel, we provide proof level rounding-on-R models for
compositional error envelopes, where each primitive is specified as “compute in R then round” with lemmas that bound


                                                            7
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                            A P REPRINT

Table 1: Trust and scalar semantics in T ORCH L EAN, including explicit native runtime and validated-numerics bound-
aries.
Mode                           Purpose                                  Semantics and trust
R                              Proofs, reference Autograd               Exact real arithmetic; reference semantics for
                                                                        theorem statements.
Interval / affine              IBP, CROWN/LiRPA bounds                  Sound enclosure domains with proved transfer
                                                                        rules where available.
FP32 / NF                      Rounding-aware theorems                  Round-on-R proof model with compositional
                                                                        error envelopes.
IEEE32Exec                     Executable Float32 model                 Lean-defined binary32 semantics for core ops;
                                                                        hardware matching is separate.
Arb/FLINT oracle               Rigorous transcendentals                 External validated ball/interval enclosures; ex-
                                                                        plicit non-kernel oracle boundary.
Lean Float32                   Fast execution                           Runtime implementation opaque to the kernel;
                                                                        treated as a deployment assumption or validated
                                                                        backend.
CUDA/native FFI                Accelerated examples                     Optional Lean FFI-backed execution for se-
                                                                        lected kernels; governed by native primitive
                                                                        agreement contracts.
and compose rounding error through whole graphs, in the spirit of verified floating-point libraries such as Flocq [Boldo
and Melquiond, 2011].
Lean’s runtime Float and Float32, CUDA kernels, cuBLAS/cuFFT, and vendor libraries remain available for fast
execution, but they are treated as explicitly trusted or validated backends due to kernel opacity and native runtime
boundaries. In addition, T ORCH L EAN builds an interval/enclosure layer spanning both proof level and executable
semantics. We implement Float32 endpoint interval arithmetic on top of IEEE32Exec and prove operation-level
soundness theorems that computed endpoint boxes conservatively enclose the corresponding real or extended-real
interpretations. For rigorous transcendental bounds, we optionally integrate Arb/FLINT via an explicit oracle boundary,
using it as a certificate/enclosure generator while keeping the trusted computing base explicit.
FP32/NF ↔ IEEE32Exec: internal refinement. For the IEEE-754 core arithmetic implemented in IEEE32Exec, we
prove an internal refinement to the FP32 round-on-R model on finite executions, excluding NaN/Inf and overflow. We
establish per-operator theorems of the form toReal(op(x, y)) = fp32Round(· · · ) and lift them to a compositional
bridge showing that real-valued evaluation of IEEE32Exec expressions agrees with the corresponding FP32/NF
specification on the finite path.

2.4   Verification layer

Verification is a statement about semantics. The verification layer expresses goals as Lean theorems about the
denotation of a compiled graph [[G]]: robustness margins, output bounds, invariance and safety constraints, Lyapunov or
barrier inequalities, PINN residual bounds, ODE corridor conditions, spline certificate obligations, and dataset-backed
certified-accuracy claims. The verifier is not the claim. It is a mechanism for producing intermediate bounds, relaxations,
witnesses, or constraints which are then checked and used to discharge a semantic property of [[G]]. All enclosure
theorems are stated against a specified execution semantics; relating results to hardware Float32 or CUDA execution
is an explicit refinement or validation assumption at the deployment boundary.
Native bound propagation over the shared IR. Because the computation-graph IR is operator-tagged and typed,
bound propagation operates on the same object used by execution, eliminating any separate export semantics to trust.
Formally, bounds live in an abstract domain D with a concretization map γ to sets of concrete values. A local abstract
transformer τb for an operator τ is sound when
                                                                                                    
                          xi ∈ γ(ai ) for all i =⇒ [[τ ]](x1 , . . . , xk ) ∈ γ τb(a1 , . . . , ak ) .
Soundness for a full graph follows by induction over the same topological node order that defines [[G]].
We include a sound core of interval bound propagation (IBP) Gowal et al. [2018], which propagates node wise enclosures
[li , ui ] forward through the graph using per-operator transfer rules stated against the same operator denotations that
define [[G]]. Building on this, T ORCH L EAN implements CROWN/LiRPA style affine propagation Zhang et al. [2018], Xu
et al. [2020], including forward affine propagation and objective-dependent backward components. Affine relaxations
capture correlations that intervals miss and typically yield substantially tighter output bounds through compositions of
linear layers and monotone activations. Both IBP and affine propagation are anchored to the same IR denotation, rather
than to an external verifier-side model.


                                                            8
                                           T ORCH L EAN: Formalizing Neural Networks in Lean                                                                    A P REPRINT



                   α = R (proofs)                          α = Rat/Float32/IEEEExec (execution)                                 α = Interval/FP32 (bounds)


                   Specification                                            Runtime                                                    Verification
               mathematical semantics                                 execution and training                                       bounds and certificates


                        Core                                                Autograd                                                        IBP
                   Tensors, shapes                                      Reverse-mode AD                                               Interval bounds
                     Ops over α                                          Tape and graph                                              Sound propagation


                        Layers                                           T ORCH L EAN                                                 CROWN/LiRPA
                Linear, conv, attention                                 PyTorch style API                                             Affine relaxations
                 Normalization, etc.                                   Eager and compiled                                             Dual certificates


                     Models                                          Training and workflows                                          Certificate checking
              MLP, CNN, Transformer                                   Optimizers, RL, SSL                                          Native checkers + CLI
           RNN/LSTM/GRU, SSM, diffusion                              Sampling, import/export                                      external artifacts optional

                                                                         optional
                                                                           build / interfaces
                                                                                   compile

                 compile   Optional import / lowering                                                     Optional execution backend         verify / check
                            Python, Julia, PyTorch                                                         CUDA, cuBLAS, cuFFT
                                  ONNX, FX                                                                      custom kernels
                                          lower / import                                                      execute via FFI
                                                                   Operator tagged shared IR
                                                                   SSA/DAG computation graph
                                                  single semantic target for execution, verification, and lowering


Figure 4: Comprehensive architecture of T ORCH L EAN. The specification, runtime, and verification layers share a
single operator-tagged SSA/DAG computation-graph IR as the semantic target. Models are defined once, executed or
trained by the runtime, and verified through CROWN bounds and certificate checking against the same graph semantics.

Certificates and a reduced trusted computing base. When stronger tightness is required than the native engines
provide, T ORCH L EAN adopts a certificate/checker architecture: external solvers act as producers of artifacts, while
Lean checks the finite data needed to conclude a theorem about [[G]] Necula [1997]. The checker validates shapes,
operator tags, topological order, parent bounds, local inequalities, phase constraints, and final property obligations. The
intended theorem shape is
                                    checkCert(G, Φ, C) = true =⇒ Φ([[G]]).
In this style, we support an α/β-CROWN certificate dialect in which the certificate supplies IBP pre-activation boxes,
per-node affine bounds, α parameters for unstable-ReLU lower relaxations, and optional β phase vectors encoding
active/inactive constraints consistent with the IBP intervals Xu et al. [2021], Wang et al. [2021]. The checker replays
the same per-node step semantics in Lean and accepts only if the provided bounds match the recomputed or checked
obligations under the declared canonicalization policy.
Broader verification workflows. The current verification layer also includes graph-CROWN/LiRPA entry points,
executable certificate checkers, robustness workflows, VNN-COMP style ONNX/VNN-LIB slices, PINN graph builders
and derivative-residual bound helpers, ODE corridor certificates, spline and piecewise-polynomial certificate checks, 3D
geometry certificates, Lyapunov/CROWN oracle-backed workflows, and regression tests for graph rewrite or backend
drift. These workflows differ in how much is proved internally and how much is delegated to external producers, but
they follow the same discipline: each accepted claim is tied to a graph, tensor, or certificate semantics stated in Lean.

3   Results
We evaluate T ORCH L EAN as a semantic ML systems stack. A model definition can be executed for training or inference,
lowered to a typed operator-tagged graph, analyzed by native bound and differentiation passes, and validated by
certificate checkers against one mathematical denotation. The goal is not to outperform specialized training frameworks
or solver-optimized verifiers, but to make the object being trained, differentiated, bounded, checked, and accelerated
semantically visible. The results are organized around three components. First, we show that the framework supports
recognizable modern ML workflows rather than only toy verifier networks. Second, we keep the VNN-COMP style
mini-suite and the original three case studies: certified robustness, neural-controller verification, and PINN residual
bounds. Third, we add semantic bug examples showing how typed shapes, masking contracts, and explicit numerical
semantics catch failures that can otherwise survive ordinary execution or export.
Model families and modern workflow coverage. Figure 5 summarizes the current executable surface. The examples
exercise ordinary ML structure: minibatch loaders, multiple epochs, optimizer state, saved parameters, loss curves,


                                                                                     9
                                T ORCH L EAN: Formalizing Neural Networks in Lean                           A P REPRINT




Figure 5: Representative model families exercised in T ORCH L EAN. The examples cover vision, transformer-style
language models, Mamba/state-space sequence models, diffusion/sampling, Fourier-neural-operator/scientific ML
workflows, and reinforcement learning. The plotted curves illustrate executable training and evaluation workflows
across these model families. The formal role of the examples is that each can be connected to the typed tensor, runtime,
graph-lowering, finite-precision, and checking infrastructure described in the methodology.

sampling loops, rollout tensors, imported weights, and generated certificates. They also exercise the newer parts of
the codebase: CUDA/native FFI paths for dense/matmul and batched-matmul kernels, reductions, broadcasts, views,
convolution/pooling and transposed-convolution kernels, FFT/spectral operators, softmax/log-softmax, normalization,
attention/fused attention, gather/scatter, positional/RoPE helpers, selective-scan-style sequence kernels, and shape
operations; PyTorch/ONNX/VNN-LIB interop; Arb/FLINT validated-numerics calls; Gymnasium/PPO-style RL
bridges; and semantic regression tests.
These examples are not leaderboard training results; they show that verification-oriented semantics can be attached to
workflows that look like recognizable ML programs. A CNN or FNO example stresses tensor shapes, convolution-
al/spectral operators, finite-precision execution, and optional CUDA kernels. A GPT-style model stresses tokenization,
causal masking, generation, and attention semantics. A Mamba/state-space example stresses recurrence, scan-like
execution, and non-anticipation. Diffusion and self-supervised examples stress masking, views, schedules, latent
variables, and reconstruction or prediction losses. RL examples stress rollouts, returns, advantages, policy/value
artifacts, and simulator boundaries.
For these model families, the meaningful result is not only that Table 2: VNN-COMP style MNIST-FC slice.
an example runs, but that the surrounding development exposes Checked rows are Lean-verified; CUDA is an un-
a specification surface. FlashAttention style blocked or fused trusted GPU producer.
implementations are related to this denotation at the specifica-           Path           Method      Safe/n Time
tion level; CUDA kernels remain execution backends behind
                                                                           Lean           IBP           0/30  6.05s
Lean FFI boundaries. State-space models are specified by fi-               Lean           CROWN-Obj     6/30 22.60s
nite recurrences and scan contracts, diffusion models by noising           Lean           CROWN+α      6/30  14.21s
and denoising transitions, RL by rollout algebra, returns, advan-          CPU producer   α-CROWN      13/30  8.39s
tages, finite MDP views, Markov-kernel MDP semantics, and                  CUDA producer α-CROWN       13/30  7.67s
Bellman-style operators, and self-supervised learning by finite
mask/view/target objectives.
Verification artifacts and producer/checker boundaries. The verification stack is evaluated as a checker-oriented
system. Native IBP and CROWN/LiRPA style passes operate over the shared IR. External solvers, Python/Julia scripts,
Arb/FLINT, CUDA kernels, and imported ONNX or VNN-LIB files are treated as producers or runtime boundaries.
Lean checks the shape, graph, interval, affine, and schema obligations that are sufficient for the theorem being claimed,


                                                          10
                                T ORCH L EAN: Formalizing Neural Networks in Lean                           A P REPRINT




Figure 6: Neural-controller workflow in three execution settings. Certification claims are checked against the shared
operator-tagged SSA/DAG IR semantics in Lean; external optimizers and runtime systems act as untrusted producers.
or records a named assumption when the producer itself is outside the kernel. Thus a successful verification result
is a statement about the Lean-side graph semantics, not an implicit claim that every external runtime or exporter has
been verified. We adopt the VNN-COMP convention that each benchmark instance is an ONNX network paired with a
VNN-LIB property specification VNN-COMP [2024], VNN-LIB [2021]. A lightweight Python export step converts
ONNX/VNN-LIB into compact JSON bundles consumed by a Lean runner, which checks a sufficient UNSAT condition
by replaying IBP/CROWN style bounds against the shared IR semantics (fast runtime Float). Table 2 reports both
fully checked TorchLean results and CUDA-backed producer results on the same MNIST-FC slice. The checked rows
are Lean-verified claims about the shared IR. The CUDA row uses an α-CROWN GPU producer on an NVIDIA A100
to generate stronger candidate bounds; those GPU results become trusted TorchLean claims only when the exported
artifacts are replayed by the Lean checker.
Certified Robustness. We certify an ℓ∞ margin condition for a digits linear classifier (sklearn digits, 8×8→64
features; 64→10; ε = 0.02). The model is nominally correct on 349/360 test inputs and certified robust on 318/360 by
a Lean checker that replays the exported bound artifact and verifies the standard logit-margin inequality (Appendix E).
The checker is lightweight (0.032 ms average, 0.057 ms maximum per example), but the point is semantic rather than
competitive: robustness is attached to the checked graph, not to an unchecked training script or exporter.
Neural controller. We consider a two stage controller-verification workflow: external training/search proposes a neural
feedback controller u(x) together with a Lyapunov candidate V (x), and Lean then certifies region-based safety/stability
by checking CROWN/LiRPA enclosures for Lyapunov inequalities over input regions (Appendix E). This setup mirrors
recent two stage stabilizing-controller pipelines: Stage 1 learns an initial region of attraction using Zubov-inspired
boundary sampling, and Stage 2 fixes this region and iteratively refines the networks to eliminate counterexamples
(CEGIS) discovered within it Li et al. [2025]. We bound V (x) and V̇ (x) = ∇V (x) · f (x, u(x)) on a region, using
verified autograd to compute ∇V , and discharge the resulting Lyapunov/safety conditions as Lean-checked statements
about the shared semantic model. Figure 6 compares three execution settings for this workflow: (i) Python-only
(Stage 1+2 in PyTorch Float32, with optional Lean checking), (ii) all-T ORCH L EAN, and (iii) hybrid (Stage 1 in PyTorch,
Stage 2 and post-checking in T ORCH L EAN). Holding Stage 1 weights fixed and using a common Stage 2 baseline
(width 100; 10 PGD candidates; 1 PGD step), Python Stage 2 takes ≈ 0.015s and yields 9/10 positive-loss candidates,
while T ORCH L EAN Stage 2 under explicit IEEE-754 Float32 semantics (IEEE32Exec) takes ≈ 1212s and yields 7/10
positives; T ORCH L EAN additionally computes a native CROWN enclosure for the scalar loss over a small input box
(e.g., an upper bound ≈ 0.1869).
PINN residual bounds. We demonstrate full verification of physics-informed neural networks trained to satisfy PDEs.
The workflow begins with training a PINN model in Python (e.g., viscous Burgers equation ut + u · ux − νuxx = 0)
using PyTorch autograd to compute derivatives for the PDE residual loss. After training, we export weights to JSON and
load them into Lean. For verification, we compute bounds on u(x) via IBP/CROWN, and compute interval enclosures
for u′ (x) and u′′ (x) via dedicated first/second-derivative bound-propagation passes on the same operator-tagged graph
(covering the smooth ops used in the PINN demos, e.g. tanh and linear layers), rather than by recursively differentiating
the backward graph. These bounds are then combined to certify that the PDE residual |R(uθ )(x)| is bounded within
tolerance ε at verification points (Appendix E).
Semantic bug examples. Figure 7 shows three representative semantic boundary failures. The first is a shape/broad-
casting bug: a bias b ∈ RC should be applied to logits X ∈ RB×C as Yij = Xij + bj , but a wrong broadcast axis can


                                                           11
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                             A P REPRINT




Figure 7: Representative semantic boundary bugs. Left: typed shape semantics distinguishes intended row-wise bias
addition from an unintended broadcast. Middle: temporal and masking contracts expose causal-mask or KV-cache leaks
in sequence models. Right: explicit finite-precision semantics separates a stable log-sum-exp/log-softmax computation
from a naive Float32 implementation that can overflow or produce NaNs.

silently change the function while still producing a plausible tensor. The second is a temporal bug in sequence models:
an incorrect causal mask or stale KV-cache entry can allow future-token information to influence the current output.
The third is a numerical bug: a naive log-sum-exp or log-softmax computation can overflow under Float32, while the
stable formulation remains finite. These examples are small by design. They are not meant to be benchmark wins; they
isolate the kind of error that makes verification pipelines fragile. In each case, the model may execute, export, or even
produce a plausible downstream artifact, while the intended semantics has changed.
Numerical semantics stress tests. Numerical stress tests explain why we make scalar semantics explicit rather than
treating floating point as an implementation detail. Endpoint evaluation alone is not a reliable enclosure mechanism for
transcendentals, whereas the Arb-backed pipeline provides rigorous real enclosures (Appendix D). For core arithmetic,
directed rounding matters: a ties-to-even addition can be enclosed by IEEE32Exec directed endpoints but collapse
under naive runtime Float32. Signed-zero guards can also force principled widening, for example when an interval
denominator contains both real zero and signed-zero floating encodings.
4   Related work
Neural network verification (solver-based and bound-propagation). Neural network verification is central in safety
and robustness analysis Kaulen et al. [2025], Li et al. [2025], Ji et al. [2025], Chen et al. [2024]. Broadly, the literature
spans (i) solver-based methods such as Reluplex and Marabou [Katz et al., 2017, 2019], which encode verification
problems as satisfiability/constraint queries, and (ii) abstract-interpretation / relaxation methods such as IBP Gowal
et al. [2018], Moore et al. [2009] and linear bound propagation (CROWN/DeepPoly and related abstractions) Dvijotham
et al. [2018], Gehr et al. [2018], Raghunathan et al. [2018], Singh et al. [2018, 2019], Wang et al. [2018], Wong and
Kolter [2018], Zhang et al. [2018]. These tools often operate on exported artifacts (ONNX/TorchScript/custom IRs)
and therefore inherit an additional trust boundary at the export/interpretation step. This pipeline is standardized and
stress-tested in VNN-COMP, where instances are packaged as an ONNX network together with a VNN-LIB property
specification Brix et al. [2024], VNN-COMP [2024], VNN-LIB [2021], making the export/interface boundary an
explicit part of the evaluation regime.
CROWN family optimizers and certificate checking. CROWN family methods derive output bounds by propagating
sound linear relaxations of nonlinearities and viewing the result through a dual objective; α-CROWN [Xu et al., 2021]
tightens bounds by optimizing relaxation parameters, and β-CROWN integrates splitting/branch-and-bound to further
tighten bounds Wang et al. [2021]. T ORCH L EAN implements a Lean based CROWN/LiRPA core over our shared
operator-tagged IR semantics (proved-sound IBP, a basic forward affine pass, and an objective-dependent backward/dual
pass). Reimplementing the full α/β-CROWN optimization stack inside Lean including the parameter-optimization
heuristics and branch-and-bound search is ongoing work. When strongest current tightness is needed, we instead treat
external solvers as untrusted producers and check their exported bounds/certificates against the same IR semantics,
keeping the trusted computing base to a small checker.
Formalization in theorem provers and Lean infrastructure. ITPs have been used to formalize ML-relevant
mathematics (e.g., generalization bounds Bagnall and Stewart [2019], activation-function libraries Aleksandrov and
Völlinger [2023], and network translations Gummersbach et al. [2025]). Lean’s ecosystem (notably mathlib (The
mathlib Community, 2020)) makes these developments practical, but full pipeline neural verification remains hard


                                                            12
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                            A P REPRINT



because it requires tensor representations that scale to modern architectures, a sound differentiation story, and numerical
semantics that are explicit enough to connect proofs to execution. TensorLib provides a verified tensor library for
Lean [Lean Prover Community, 2025b] and, as of this writing, is under active development.
SciLean, verified floats, and complementary developments. SciLean is a Lean based library for scientific computing
with array abstractions and automatic differentiation Contributors [2023]. T ORCH L EAN targets a different point in
the design space: typed tensor computation graphs with shape-indexed tensors, a graph-parametric reverse-mode
correctness theorem for SSA/DAGs, and certificate-checked verification workflows. On numerics, verified floating-point
frameworks such as Flocq [Boldo and Melquiond, 2011] motivate the separation we use between rounding models for
proofs (FP32/NF) and an executable IEEE-style kernel (IEEE32Exec), with an explicit trust boundary to runtime floats.
HopfieldNet formalizes Hopfield/Boltzmann-style energy arguments in Lean Cipollina et al. [2025]. Our Hopfield
material is positioned as a complementary case study within a shared tensor/graph semantics: we mechanize the
standard energy-decrease and convergence-style results in the same framework; see Appendix E.3.

5   Discussion
T ORCH L EAN is best understood as a semantics layer for neural network systems rather than as a replacement for
existing training frameworks or specialized verifiers. The main design choice is to make the network definition
the semantic reference point and to connect execution, differentiation, bound propagation, certificate checking, and
external artifacts to a shared operator-tagged SSA/DAG IR. This addresses a common source of fragility in verified
ML workflows: the artifact that is trained, exported, optimized, or executed is often not exactly the artifact that
is analyzed. In T ORCH L EAN, this boundary is made explicit. Imported ONNX/VNN-LIB files, PyTorch or Julia
producers, Arb/FLINT enclosures, CROWN family certificates, Gymnasium rollouts, and CUDA/native kernels are
treated as producers or runtime interfaces whose artifacts must either be checked in Lean or recorded as named
assumptions. This separation is also important for modern ML workflows. Verification is no longer only about small
feed-forward classifiers. Attention masks, FlashAttention style fused operators, state-space scans, diffusion schedules,
self-supervised views, RL returns, and scientific ML residuals all carry mathematical contracts that can be broken by
small implementation choices. T ORCH L EAN makes these contracts visible as typed specifications. The current system
therefore supports two complementary uses: proving semantic properties of supported graph fragments, and detecting
semantic boundary failures such as shape/broadcasting mistakes, causal-mask leaks, unstable losses, export drift, and
certificate inconsistencies.
The main limitations are coverage and conformance. The verified fragment is necessarily smaller than the full surface of
PyTorch, CUDA, and modern ML libraries. Extending T ORCH L EAN requires adding operator semantics, local derivative
rules, abstract transformers, finite-precision models, and certificate checkers for new primitives. Native CUDA execution
is useful for scale, but it remains outside Lean’s kernel; connecting it more tightly to the formal semantics requires
stronger conformance testing, verified wrappers, or eventually verified kernels for important primitives. Similarly,
external certificate producers are useful for tightness and performance, but the formal guarantee comes only from what
the Lean checker validates. These limitations are deliberate: the system favors explicit boundaries over implicit trust.

6   Conclusion
T ORCH L EAN advances a semantic approach to verified machine learning. Models are written as executable neural
network programs, lowered to a shared operator-tagged SSA/DAG IR, and interpreted by execution, automatic
differentiation, bound propagation, and certificate checking through the same formal semantics. This makes it possible
to state machine-checked claims about robustness, control-oriented safety, scientific ML residuals, VNN-style imported
artifacts, and semantic regression tests without relying on an informal export pipeline. The framework combines a
PyTorch style Lean API, typed tensors and layers, verified graph-level differentiation, explicit floating-point semantics,
native IBP/CROWN style verification, certificate checking, optional CUDA-backed execution through Lean FFI, and
interop with PyTorch, Python, Julia, Arb/FLINT, Gymnasium, and CROWN family tools. The contribution is not that
every external producer or runtime is verified inside Lean. Rather, T ORCH L EAN makes clear which claims are checked
by Lean, which artifacts are replayed or validated, and which runtime or oracle assumptions remain outside the kernel.
The broader value of this approach is that it gives multiple communities a shared semantic object to build on. Verification
researchers can check certificates against executable models; ML systems researchers can study export, compilation,
numerical, and backend boundaries with formal contracts; and scientific ML, control, and robotics researchers can
connect learned components to residual, safety, or stability claims without losing the semantics of the implemented
system. Verified ML also needs shared infrastructure in the spirit of what PyTorch provided for empirical ML: a substrate
where models, tools, transformations, and artifacts can be composed. Lean has demonstrated this model through
mathlib (The mathlib Community, 2020), and emerging libraries such as CSLib (Barrett et al., 2026) point toward
similar foundations for verified software. T ORCH L EAN contributes to this ecosystem by connecting neural-network
computation, formal semantics, and certificate based verification in one theorem-proving environment.


                                                            13
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                          A P REPRINT



References
Andrei Aleksandrov and Kim Völlinger. Formalizing piecewise affine activation functions of neural networks in coq,
  2023. URL https://arxiv.org/abs/2301.12893.
Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, and
 Nicolas Ballas. Self-supervised learning from images with a joint-embedding predictive architecture. In Proceedings
 of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 15619–15629, 2023.
Alexander Bagnall and Gordon Stewart. Certifying the true error: Machine learning in coq with verified gener-
  alization guarantees. Proceedings of the AAAI Conference on Artificial Intelligence, 33(01):2662–2669, 2019.
  doi:10.1609/aaai.v33i01.33012662. URL https://ojs.aaai.org/index.php/AAAI/article/view/4115.
Adrien Bardes, Jean Ponce, and Yann LeCun. Vicreg: Variance-invariance-covariance regularization for self-supervised
  learning. In International Conference on Learning Representations, 2022.
Clark Barrett, Swarat Chaudhuri, Fabrizio Montesi, Jim Grundy, Pushmeet Kohli, Leonardo de Moura, Alexandre
  Rademaker, and Sorrachai Yingchareonthawornchai. CSLib: The Lean Computer Science Library. arXiv preprint
  arXiv:2602.04846, 2026. doi:10.48550/arXiv.2602.04846. URL https://arxiv.org/abs/2602.04846.
Richard Bellman. Dynamic Programming. Princeton University Press, 1957.
Sylvie Boldo and Guillaume Melquiond. Flocq: A unified library for proving floating-point algorithms in Coq. In
  Proceedings of the 20th IEEE Symposium on Computer Arithmetic (ARITH), 2011. doi:10.1109/ARITH.2011.40.
  URL https://dl.acm.org/doi/10.1109/ARITH.2011.40.
Nicolas Brisebarre, Guillaume Hanrot, Jean-Michel Muller, and Paul Zimmermann. Correctly Rounded Evaluation of a
  Function: Why, How, and at What Cost? ACM Computing Surveys, 2025. doi:10.1145/3747840.
Christopher Brix, Stanley Bak, Taylor T. Johnson, and Haoze Wu. The fifth international verification of neu-
  ral networks competition (VNN-COMP 2024): Summary and results. arXiv preprint arXiv:2412.19985, 2024.
  doi:10.48550/arXiv.2412.19985. URL https://arxiv.org/abs/2412.19985.
Achim D. Brucker and Amy Stell. Verifying feedforward neural networks for classification in isabelle/hol. In Formal
  Methods, 2023. doi:10.1007/978-3-031-27481-7_24. URL https://www.isa-afp.org/entries/Neural_
  Networks.html.
Shaoru Chen, Lekan Molu, and Mahyar Fazlyab. Verification-aided learning of neural network barrier functions with
  termination guarantees. In 2024 American Control Conference (ACC), pages 3610–3617. IEEE, 2024.
Matteo Cipollina, Michail Karatarakis, and Freek Wiedijk. Formalized hopfield networks and boltzmann machines,
 2025. URL https://arxiv.org/abs/2512.07766.
SciLean Contributors. Scilean: Scientific computing in lean. Software, 2023. URL https://github.com/lecopivo/
  SciLean.
George Cybenko. Approximation by superpositions of a sigmoidal function. Mathematics of Control, Signals, and
  Systems, 2:303–314, 1989. doi:10.1007/BF02551274.
Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman, and F. Kenneth Zadeck. Efficiently computing static
  single assignment form and the control dependence graph. ACM Transactions on Programming Languages and
  Systems, 13(4):451–490, 1991. doi:10.1145/115372.115320.
Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré. FlashAttention: Fast and memory-efficient exact
  attention with IO-awareness. In Advances in Neural Information Processing Systems, volume 35, pages 16344–16359,
  2022.
Krishnamurthy Dvijotham, Robert Stanforth, Sven Gowal, Timothy Mann, and Pushmeet Kohli. A dual approach to
  scalable verification of deep networks. In Proceedings of the 34th Conference on Uncertainty in Artificial Intelligence
  (UAI 2018), 2018. URL https://auai.org/uai2018/proceedings/papers/204.pdf. arXiv:1803.06567.
Gabriel Ebner, Sebastian Ullrich, Jared Roesch, Jeremy Avigad, and Leonardo de Moura. A metaprogramming
  framework for formal verification. Proceedings of the ACM on Programming Languages, 1(ICFP):34:1–34:29, 2017.
  doi:10.1145/3110278. URL https://dl.acm.org/doi/10.1145/3110278.
Flocq Developers. Flocq: Theoretical background (floats for coq). https://flocq.gitlabpages.inria.fr/
  theos.html, 2025.
Timon Gehr, Matthew Mirman, Dana Drachsler-Cohen, Petar Tsankov, Swarat Chaudhuri, and Martin Vechev. Ai2:
  Safety and robustness certification of neural networks with abstract interpretation. In 2018 IEEE symposium on
  security and privacy (SP), pages 3–18. IEEE, 2018.


                                                           14
                                T ORCH L EAN: Formalizing Neural Networks in Lean                         A P REPRINT



Ian J. Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining and harnessing adversarial examples. arXiv
  preprint arXiv:1412.6572, 2014. doi:10.48550/arXiv.1412.6572.
Sven Gowal, Krishnamurthy Dvijotham, Robert Stanforth, Rudy Bunel, Chongli Qin, Jonathan Uesato, Relja
  Arandjelović, Timothy Mann, and Pushmeet Kohli. On the effectiveness of interval bound propagation for
  training verifiably robust models. In NeurIPS Workshop on Security in Machine Learning, 2018. URL
  https://arxiv.org/abs/1810.12715.
Leo Alexander Gummersbach, Kim Völlinger, and Andrei Aleksandrov. A formally verified neural network converter
  for the interactive theorem prover coq. In Philipp Rümmer and Zhilin Wu, editors, Theoretical Aspects of Software
  Engineering, pages 197–214, Cham, 2025. Springer Nature Switzerland.
Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, and Ross Girshick. Masked autoencoders are scalable
  vision learners. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages
 16000–16009, 2022.
Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In Advances in Neural Information
  Processing Systems, volume 33, pages 6840–6851, 2020.
Kurt Hornik. Approximation capabilities of multilayer feedforward networks. Neural Networks, 4(2):251–257, 1991.
  doi:10.1016/0893-6080(91)90009-T.
Nargiz Humbatova, Gunel Jahangirova, Gabriele Bavota, Vincenzo Riccio, Andrea Stocco, and Paolo Tonella. Taxonomy
  of real faults in deep learning systems. In Proceedings of the ACM/IEEE 42nd International Conference on Software
  Engineering, ICSE 2020, pages 1110–1121, New York, NY, USA, 2020. Association for Computing Machinery.
  doi:10.1145/3377811.3380395.
Geonho Hwang, Wonyeol Lee, Yeachan Park, Sejun Park, and Feras Saad. Floating-point neural networks are
  provably robust universal approximators. In Computer Aided Verification (CAV 2025), volume 15932 of Lecture
  Notes in Computer Science, pages 301–326. Springer, 2025. doi:10.1007/978-3-031-98679-6_14. URL https:
 //doi.org/10.1007/978-3-031-98679-6_14. Full version: arXiv:2506.16065.
IEEE Standards Association. IEEE Standard for Floating-Point Arithmetic (IEEE Std 754-2019). https://standards.
  ieee.org/standard/754-2019.html, 2019.
Md Johirul Islam, Giang Nguyen, Rangeet Pan, and Hridesh Rajan. A comprehensive study on deep learning bug
 characteristics. In Proceedings of the 2019 27th ACM Joint Meeting on European Software Engineering Conference
 and Symposium on the Foundations of Software Engineering, ESEC/FSE 2019, pages 510–520, New York, NY, USA,
 2019. Association for Computing Machinery. doi:10.1145/3338906.3338955.
Chenxi Ji, Yangge Li, Xiangru Zhong, Huan Zhang, and Sayan Mitra.  Abstract Rendering: Cer-
  tified Rendering Under 3D Semantic Uncertainty. In Advances in Neural Information Process-
  ing Systems, volume 38, 2025.   URL https://papers.nips.cc/paper_files/paper/2025/hash/
  976c391cba6bf0bb70f6edd7f89cd23c-Abstract-Conference.html.
Kai Jia and Martin C. Rinard. Exploiting verified neural networks via floating point numerical error. arXiv preprint
  arXiv:2003.03021, 2020. URL https://arxiv.org/abs/2003.03021.
Guy Katz, Clark Barrett, David L. Dill, Kyle Julian, and Mykel J. Kochenderfer. Reluplex: An efficient SMT
  solver for verifying deep neural networks. In Rupak Majumdar and Viktor Kuncak, editors, Computer Aided
 Verification (CAV 2017), volume 10426 of Lecture Notes in Computer Science, pages 97–117. Springer, July 2017.
  doi:10.1007/978-3-319-63387-9_5. URL http://theory.stanford.edu/~barrett/pubs/KBD+17.pdf.
Guy Katz, Derek A. Huang, Duligur Ibeling, Kyle Julian, Christopher Lazarus, Rachel Lim, Parth Shah, Shantanu
 Thakoor, Haoze Wu, Aleksandar Zeljić, David L. Dill, Mykel J. Kochenderfer, and Clark Barrett. The marabou
  framework for verification and analysis of deep neural networks. In Computer Aided Verification (CAV 2019), volume
 11561 of Lecture Notes in Computer Science, pages 443–452. Springer, 2019. doi:10.1007/978-3-030-25540-4_26.
  URL https://doi.org/10.1007/978-3-030-25540-4_26.
Konstantin Kaulen, Tobias Ladner, Stanley Bak, Christopher Brix, Hai Duong, Thomas Flinkow, Taylor T. Johnson,
  Lukas Koller, Edoardo Manino, ThanhVu H. Nguyen, and Haoze Wu. The 6th international verification of neu-
  ral networks competition (VNN-COMP 2025): Summary and results. arXiv preprint arXiv:2512.19007, 2025.
  doi:10.48550/arXiv.2512.19007. URL https://arxiv.org/abs/2512.19007.
Lean Prover Community. Floating-point numbers (lean reference manual), 2025a. URL https://lean-lang.org/
  doc/reference/latest/Basic-Types/Floating-Point-Numbers/. Accessed: 2026-05-24.
Lean Prover Community. TensorLib: A verified tensor library in Lean. GitHub repository, 2025b. URL https:
  //github.com/leanprover/TensorLib.


                                                         15
                                T ORCH L EAN: Formalizing Neural Networks in Lean                         A P REPRINT



Haoyu Li, Xiangru Zhong, Bin Hu, and Huan Zhang. Two-stage learning of stabilizing neural controllers via zubov
  sampling and iterative domain expansion. arXiv preprint arXiv:2506.01356, 2025.
Ramon E Moore, R Baker Kearfott, and Michael J Cloud. Introduction to interval analysis. SIAM, 2009.
Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language. In Automated
  Deduction – CADE 28, volume 12699 of Lecture Notes in Computer Science, pages 625–635. Springer, 2021.
  doi:10.1007/978-3-030-79876-5_37. URL https://doi.org/10.1007/978-3-030-79876-5_37.
George C. Necula. Proof-carrying code. In Proceedings of the 24th ACM SIGPLAN-SIGACT Symposium on Principles
  of Programming Languages (POPL), pages 106–119, 1997. doi:10.1145/263699.263712. URL https://dl.acm.
  org/doi/10.1145/263699.263712.
ONNX Contributors. ONNX versioning documentation (ir and operator set versioning). https://onnx.ai/onnx/
 repo-docs/Versioning.html, 2026. Accessed: 2026-05-24.
Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming
  Lin, Natalia Gimelshein, Luca Antiga, et al. PyTorch: An imperative style, high-performance deep learning
  library. Advances in Neural Information Processing Systems, 32, 2019. URL https://proceedings.neurips.
  cc/paper_files/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html.
Martin L. Puterman. Markov Decision Processes: Discrete Stochastic Dynamic Programming. Wiley, 1994.
PyTorch Contributors. torch.onnx — pytorch documentation (limitations of trace-based onnx export and numeric
  differences across runtimes). https://docs.pytorch.org/docs/stable/onnx, 2025. Accessed: 2026-05-24.
Aditi Raghunathan, Jacob Steinhardt, and Percy Liang. Certified defenses against adversarial examples. In International
  Conference on Learning Representations (ICLR), 2018. URL https://openreview.net/forum?id=Bys4ob-Rb.
  arXiv:1801.09344.
Maziar Raissi, Paris Perdikaris, and George Em Karniadakis. Physics-informed neural networks: A deep learning
 framework for solving forward and inverse problems involving nonlinear partial differential equations. Journal of
 Computational Physics, 378:686–707, 2019. doi:10.1016/j.jcp.2018.10.045.
John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel. High-dimensional continuous
  control using generalized advantage estimation. In International Conference on Learning Representations, 2016.
Qingchao Shen, Haoyang Ma, Junjie Chen, Yongqiang Tian, Shing-Chi Cheung, and Xiang Chen. A comprehensive
  study of deep learning compiler bugs. In Proceedings of the 29th ACM Joint Meeting on European Software
  Engineering Conference and Symposium on the Foundations of Software Engineering, ESEC/FSE 2021, pages
  968–980, New York, NY, USA, 2021. Association for Computing Machinery. doi:10.1145/3468264.3468591.
Gagandeep Singh, Timon Gehr, Matthew Mirman, Markus Püschel, and Martin Vechev. Fast and effective robustness
  certification. In Advances in Neural Information Processing Systems, volume 31, pages 10825–10836, 2018.
  URL https://papers.neurips.cc/paper/2018/hash/f2f446980d8e971ef3da97af089481c3-Abstract.
  html.
Gagandeep Singh, Timon Gehr, Markus Püschel, and Martin Vechev. An abstract domain for certifying neural networks.
  Proceedings of the ACM on Programming Languages, 3(POPL):41:1–41:30, 2019. doi:10.1145/3290354. URL
  https://dl.acm.org/doi/10.1145/3290354.
Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. In International Conference
   on Learning Representations, 2021a.
Yang Song, Jascha Sohl-Dickstein, Diederik P. Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Score-
  based generative modeling through stochastic differential equations. In International Conference on Learning
  Representations, 2021b.
Richard S. Sutton and Andrew G. Barto. Reinforcement Learning: An Introduction. MIT Press, 2 edition, 2018.
Attila Szász, Balázs Bánhelyi, and Márk Jelasity. No soundness in the real world: On the challenges of the verification
  of deployed neural networks, 2025. URL https://arxiv.org/abs/2506.01054.
Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian Goodfellow, and Rob Fergus.
  Intriguing properties of neural networks. arXiv preprint arXiv:1312.6199, 2013. doi:10.48550/arXiv.1312.6199.
The mathlib Community. The Lean Mathematical Library. In Proceedings of the 9th ACM SIGPLAN International
  Conference on Certified Programs and Proofs, CPP 2020, pages 367–381, New Orleans, LA, USA, January 2020.
  ACM. doi:10.1145/3372885.3373824. URL https://doi.org/10.1145/3372885.3373824.
VNN-COMP. International verification of neural networks competition, 2024. URL https://vnn-comp.github.io/.
 Accessed: 2026-05-24.


                                                          16
                                T ORCH L EAN: Formalizing Neural Networks in Lean                          A P REPRINT



VNN-LIB. A standard for neural network verification specifications, 2021. URL https://www.vnnlib.org/.
  Accessed: 2026-05-24.
Shiqi Wang, Kexin Pei, Justin Whitehouse, Junfeng Yang, and Suman Jana. Efficient formal safety analysis of neural
  networks. Advances in Neural Information Processing Systems, 31, 2018.
Shiqi Wang, Huan Zhang, Kaidi Xu, Xue Lin, Suman Jana, Cho-Jui Hsieh, and Zico Kolter. Beta-crown: Efficient
  bound propagation with per-neuron split constraints for neural network robustness verification. In Advances in
  Neural Information Processing Systems, 2021. URL https://proceedings.neurips.cc/paper/2021/hash/
  fac7fead96dafceaf80c1daffeae82a4-Abstract.html.
Eric Wong and J. Zico Kolter. Provable defenses against adversarial examples via the convex outer adversarial polytope.
  In International Conference on Machine Learning, pages 5286–5295. PMLR, 2018.
Dangwei Wu, Beijun Shen, and Yuting Chen. An empirical study on tensor shape faults in deep learning systems, 2021.
  URL https://arxiv.org/abs/2106.02887.
Weiming Xiang, Patrick Musau, Ayana A. Wild, Diego Manzanas Lopez, Nathaniel Hamilton, Xiaodong Yang, Joel
  Rosenfeld, and Taylor T. Johnson. Verification for machine learning, autonomy, and neural networks survey. arXiv
  preprint arXiv:1810.01989, 2018. doi:10.48550/arXiv.1810.01989.
Kaidi Xu, Zhouxing Shi, Huan Zhang, Yihan Wang, Kai-Wei Chang, Minlie Huang, Bhavya Kailkhura, Xue Lin, and
  Cho-Jui Hsieh. Automatic perturbation analysis for scalable certified robustness and beyond. Advances in Neural
  Information Processing Systems, 33:1129–1141, 2020.
Kaidi Xu, Huan Zhang, Shiqi Wang, Yihan Wang, Suman Jana, Xue Lin, and Cho-Jui Hsieh. Fast and complete:
  Enabling complete neural network verification with rapid and massively parallel incomplete verifiers. In International
  Conference on Learning Representations, 2021.
Dmitry Yarotsky. Error bounds for approximations with deep relu networks. Neural Networks, 94:103–114, 2017.
  doi:10.1016/j.neunet.2017.07.002.
Jure Zbontar, Li Jing, Ishan Misra, Yann LeCun, and Stéphane Deny. Barlow twins: Self-supervised learning via
  redundancy reduction. In Proceedings of the 38th International Conference on Machine Learning, volume 139 of
  Proceedings of Machine Learning Research, pages 12310–12320, 2021.
Huan Zhang, Tsui-Wei Weng, Pin-Yu Chen, Cho-Jui Hsieh, and Luca Daniel. Efficient neural network robustness
  certification with general activation functions. Advances in Neural Information Processing Systems, 31:4939–4948,
  2018. URL https://arxiv.org/abs/1811.00866.
Paul Zimmermann. Why transcendentals and arbitrary precision? https://members.loria.fr/PZimmermann/
  talks/why.pdf, 2005.




                                                          17
                                   T ORCH L EAN: Formalizing Neural Networks in Lean                          A P REPRINT



A      Appendix Overview

  Appendix guide

    Part              Topic                                What to look for
    Appendix B        T ORCH L EAN frontend and graph Program modes, module API, lowering to the shared IR,
                      semantics                       graph-level AD, node correctness, and the native runtime/FFI
                                                      boundary.
    Appendix C        Modern workflow semantics       Attention/FlashAttention contracts, RL/MDP semantics, dif-
                                                      fusion and probability layers, SSL objectives, and model-
                                                      family contracts.
    Appendix D        Numerical semantics             IEEE-style execution, rounded-real models, interval/enclo-
                                                      sure semantics, Arb/FLINT oracles, and hardware/runtime
                                                      trust assumptions.
    Appendix E        Verification and certificates   IBP, CROWN/LiRPA, certificate schemas, VNN-COMP
                                                      style import, controller/PINN checks, and worked examples.
    Appendix F        Approximation theorems          Universal approximation over reals and the Float32 execution
                                                      direction.
    Appendix G        Limitations and discussion      Coverage limits, runtime conformance gaps, and future ex-
                                                      tensions.


    Reading conventions
    Proved means a Lean theorem over the stated semantics. Checked means a Lean executable checker validates a
    finite artifact or recomputes a local obligation. Boundary means an external runtime, solver, simulator, or numerical
    producer is used through an explicit assumption or conformance contract rather than silently trusted.


B      T ORCH L EAN: a PyTorch style front end with a single semantic target
T ORCH L EAN is our user-facing interface for building and training neural networks. It provides a PyTorch-like
programming model where users write models using familiar operations (linear layers, convolutions, activations), but
with a crucial difference: the same model definition can execute in two modes that share a unified semantic foundation.
This design eliminates the semantic gap between training code and verification analysis.

B.1     Core design: unified semantics for execution and analysis

Our core design choice is to treat the computation graph as the semantic target for both execution and reasoning.
In T ORCH L EAN, programs lower to a typed, operator-tagged graph IR: nodes are primitive operators (e.g., matrix
multiplication or ReLU) and edges carry tensor values. We store graphs in SSA/DAG form: each intermediate value is
defined exactly once (SSA), and the dataflow graph is acyclic (DAG). These constraints are standard compiler discipline,
but they are also exactly what we want here: evaluation is deterministic by a topological order, and proofs can proceed
by induction over that order while reusing the same operator semantics that the runtime executes.
In T ORCH L EAN, the SSA/DAG representation serves multiple purposes simultaneously:

           • Execution: The graph can be evaluated to compute forward values and gradients.
           • Formal reasoning: The graph has a precise mathematical denotation [[G]] that we can state theorems about.
           • Verification: Bound propagation algorithms operate directly on the graph structure.

This unified representation is what makes the system work: there is no “export step” that might introduce semantic drift
between the model as written and the model as analyzed.

The invariant used by the rest of the section The important invariant is simple: every runtime artifact that enters
a theorem has a graph node, a shape, and a denotation. If a node id is i, then the value table produced by execution,
the cotangent table produced by reverse mode, and the bound table produced by verification all refer to the same i.


                                                             18
                                             T ORCH L EAN: Formalizing Neural Networks in Lean                                                    A P REPRINT



Table 3: Verified scope in T ORCH L EAN (summary). “Proved” means a Lean theorem over the stated semantics;
“Checked” means a small executable validator that re-computes or validates constraints; “Assumed/External” marks
trust boundaries or future work. Appendix E also tabulates operator level verification coverage.

Component                       What the paper claims (scope)                                                    Status                 Where

Shared IR semantics         Operator tagged SSA/DAG IR with a precise denotation reused by execution             Kernel-checked defini- Sections 2, B
                            and verification.                                                                    tions
Reverse-mode AD             Backpropagation equals the adjoint Fréchet derivative for well-typed SSA/DAG         Proved                 Theorem 2.1, Appendix B
                            graphs over R, assuming local per-op derivative correctness (with a pointwise
                            variant for non-smooth ops).
T ORCH L EAN compilation    “Compiled mode” produces the verifier IR; full compiler correctness for arbi-        Proved (fragment) / Fu- Theorems B.1–B.2
                            trary T ORCH L EAN programs is not yet proved.                                       ture (full)
IBP / CROWN operators       Sound transfer rules and relaxations for a curated set of operators; additional      Mixed (proved subset)   Appendix E
                            ops use conservative fallbacks or are treated as unsupported in the strongest
                            theorems.
Certificate checking        Small Lean checkers validate certificate structure and the final enclosure con-      Checked (plus proved   Section 3, Appendix E
                            straints needed to discharge a theorem about [[G]].                                  core)
External solvers (e.g. α/β- Used only as untrusted certificate producers; full optimizer internals are outside   Assumed/External       Section 3, Appendix E
CROWN)                      the checked certificate scope in this work.
Float32 semantics           Executable IEEE-754 binary32 model (IEEE32Exec) and proof-level rounding             Proved (internal)      Section 2.3, Appendix D
                            models (FP32/NF), with an internal refinement on finite executions.
Hardware Float32 link       Connecting deployed Float32 hardware/runtime behavior to IEEE32Exec is               Assumed/External       Section 6, Appendix D.1
                            target-specific and not discharged in this work.


                                                                             v
                                                                             v̄1         v
                                                                                         v̄2           ȳ
                                                         x         MatMul          Add         ReLU         y




                                                        W




                                                         b


Figure 8: Example SSA/DAG computation graph: y = ReLU(W x + b). Each intermediate value (v1 , v2 ) is assigned
once. Forward pass (solid arrows) evaluates nodes in topological order. Backward pass (dashed arrows) propagates
gradients in reverse topological order, accumulating at each node.


This prevents a common failure mode in mixed systems: the proof talks about one tensor while the runtime or verifier
silently talks about another. The invariant can be summarized as
                                                ∀i < |G|,            vi = [[Gi ]]α (ρ)         and    vi ∈ γ(Bi )
whenever evaluation and bound propagation both succeed. Here ρ is the input and parameter environment, Bi is the
abstract value stored for node i, and γ is the concretization map for the chosen abstract domain. The same statement is
used in different ways: execution establishes the left equality, IBP or CROWN establishes the right containment, and
certificate checking recomputes the finite obligations that connect the two.
                                Listing 2: Schematic public model definition through the stable facade.
import NN.API.Public
open NN

-- One model definition is used by execution, compilation, and checking.
def tiny : Spec.Model :=
  Linear (in := 4) (out := 8)
    |>.then ReLU
    |>.then (Linear (in := 8) (out := 1))

#eval tiny.run (Tensor.ones [1, 4])

Listing 2 shows the intended surface shape: the user writes a small model once, then chooses an execution or verification
view. The appendix code listings use the same convention. They are schematic when the exact repository module names
are not part of the paper claim; the theorem statements remain about the graph semantics, not about a particular file
layout.


                                                                                   19
                                       T ORCH L EAN: Formalizing Neural Networks in Lean                                 A P REPRINT



                                                                     User code:
                                                           let y = relu(linear(x, W, b))


                                                    e  t                                   com
                                                 rpr                                           pile
                                             inte


                       Eager backend                                                                  Compiled backend
                       Runtime tape                                                                    SSA/DAG graph
                         (dynamic)                                                                         (static)
                                           corresp
                                                     ondence    Unified semantic target:   direct
                                                               Well-typed SSA/DAG graph
                                                                  with denotation [[G]]


Figure 9: Two execution paths to a unified semantic target. The same T ORCH L EAN program can be interpreted eagerly
(building a tape dynamically) or compiled (building a static graph upfront). Both paths produce computations that share
the same well-typed SSA/DAG denotation, enabling unified reasoning about execution and verification.


                         Listing 3: Schematic IR objects shared by evaluation and verification.
inductive OpKind where
| input | const | linear | matmul | add | relu | tanh | softmax
| conv2d | flatten | reduceSum | mseLoss

structure Node where
  id       : Nat
  kind     : OpKind
  parents : List Nat
  outShape : Shape

structure Graph where
  nodes     : Array Node
  inputIds : List Nat
  outputIds : List Nat

-- SSA/DAG well orderedness: parents of node i have smaller ids.
def wellOrdered (G : Graph) : Prop :=
  forall n, n in G.nodes.toList ->
    forall p, p in n.parents -> p < n.id

This IR is intentionally small. Adding a new primitive starts by adding a tag, a shape rule, and a denotation for that tag.
Only after that do we add derivative rules, interval rules, affine relaxations, or native runtime implementations.

B.2   Execution modes and compilation to IR

T ORCH L EAN supports two execution modes that share the same semantic foundation but differ in when and how
the computation graph is constructed. Eager mode (imperative, tape-based). In eager mode, operations execute
immediately as you call them, similar to PyTorch’s default behavior. As operations run, they are recorded into a
computation tape: a dynamic data structure that stores the sequence of operations and their dependencies. This tape is
built incrementally during the forward pass, and then used during the backward pass to compute gradients. The key
property of eager mode is that it matches the familiar “define-by-run” workflow: you write code that looks like ordinary
function calls, and the tape is constructed implicitly as a side effect. This makes debugging straightforward (you can
inspect intermediate values immediately) and allows dynamic control flow (if statements, loops with data-dependent
bounds).
Eager mode (tape semantics vs. graph semantics). Operationally, eager execution builds a tape on the fly; semantically,
each completed run induces a well-typed SSA/DAG graph G that matches the run’s forward values, and whose
backpropagation matches the tape’s backward pass. This correspondence is the bridge that lets us develop and debug in
eager mode while still applying graph-level theorems (autograd correctness, bounds, and certificate checking) to the
same semantic target (Theorem B.2).
Compiled mode (static graph). In compiled mode, the T ORCH L EAN program is analyzed upfront to construct a static
SSA/DAG graph representation. This is “compilation” only in the sense of lowering to a formal IR for reasoning and
verification; it is not intended to compete with torch.compile-style kernel fusion or hardware-level optimization. The
compiled graph is exactly the object that formal theorems reason about: it has a precise denotation [[G]], and we can


                                                                           20
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                           A P REPRINT



state and prove correctness properties about it. The advantage of compiled mode is that the graph structure is explicit
and available for analysis before execution, so bound propagation algorithms, certificate checkers, and proofs all operate
on the same graph object that the runtime evaluates. See Appendix B.8 for details.

B.3   Native runtime and Lean FFI boundary

The runtime layer includes optional native execution paths implemented through Lean’s FFI. These paths are useful for
larger examples, but they are intentionally separated from theorem statements. At the Lean level, a native call is an
opaque or external function with checked metadata around it; at the C/CUDA level, it is ordinary systems code that
manages memory and calls kernels. The purpose of the boundary is to keep the semantic claim precise: Lean proves
facts about the graph/operator denotation, and native execution is admitted only through an explicit agreement contract.
A typical primitive therefore has three pieces:

1. a specification, such as a tensor operator [[τ ]]α ;
2. a runtime implementation, such as a CPU, CUDA, cuBLAS, or cuFFT path;
3. a conformance condition, stating when the runtime result agrees with the specified finite-precision semantics.

For example, a CUDA matrix multiplication call is not itself a proof of matrix-multiplication correctness. The formal
statement is conditional on a deployment contract such as
                                      cudaBmm(A, B) =tol [[bmm]]Float32 (A, B),
where =tol may be exact bit equality for a deterministic path or an explicit tolerance/conformance relation for a tested
backend. The contract also records shape, dtype, layout, device, and determinism assumptions.
                            Listing 4: Schematic checked call pattern for a native backend.
/-- The theorem-facing operator is still the spec operator. -/
def matmulSpec (A B : Tensor Float32 s) : Tensor Float32 t := ...

/-- The runtime path is an optional implementation boundary. -/
def matmulCudaChecked (A B : RuntimeTensor) : IO RuntimeTensor := do
  checkShape A.shape expectedLeft
  checkShape B.shape expectedRight
  checkDevice A.device .cuda
  Cuda.Buffer.bmm A.buffer B.buffer

This is also why CUDA examples in the paper are phrased as accelerated executions or conformance-tested runtime
paths, not as verified CUDA kernels. The value of adding the FFI path is practical: it makes longer runs, larger tensors,
FNO/spectral examples, and attention-style examples feasible while preserving the formal boundary that the checker
relies on.
Compilation process. When you write a T ORCH L EAN program, it’s a backend-generic definition that can run in
different modes. But for verification, we need a concrete graph structure that we can reason about formally. The
compilation process transforms a T ORCH L EAN program into an operator-tagged IR graph. Here’s how it works: the
compiler walks through the program structure, and for each operation (like linear, relu, softmax), it creates a
corresponding IR node with the appropriate operation kind and shape information. Parameters are stored separately in
a parameter store, and the graph structure captures the data dependencies between operations. For the forward-only
fragment underlying our verification demos, we make this precise by proving a semantics-preservation theorem: the
compiled IR evaluator agrees with the fragment’s source evaluator for all inputs and parameters.
The proof is easier to read if the compiler is separated into two maps. The first map extends the graph with new nodes
and returns their ids; the second map interprets the generated graph. The preservation theorem then states that the source
evaluator and the graph evaluator build the same tensor, or fail for the same explicit reason. This exception-valued form
is useful in Lean because it keeps shape errors visible instead of hiding them under partial functions.
                        Listing 5: Schematic lowering interface used by the forward fragment.
inductive EvalError where
| missingParent | shapeMismatch | unsupportedOp

structure CompileState where
  graph : Graph


                                                           21
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                           A P REPRINT



  params : ParamStore

def emitNode (st : CompileState) (k : OpKind)
    (parents : List Nat) (s : Shape) : Prod CompileState Nat :=
  -- returns the updated graph and the fresh SSA id
  ...

def lowerForward (p : ForwardProg) (st : CompileState) :
    Except EvalError (Prod CompileState Nat) :=
  match p with
  | .input j       => pure (st, st.graph.inputIds[j]!)
  | .linear W b x => do
      let (st, xid) <- lowerForward x st
      let (st, wid) <- emitNode st .const [] W.shape
      let (st, bid) <- emitNode st .const [] b.shape
      let (st, mid) <- emitNode st .matmul [wid, xid] (linearOut W)
      emitNode st .add [mid, bid] (linearOut W)
  | .relu x        => do
      let (st, xid) <- lowerForward x st
      emitNode st .relu [xid] (shapeOf x)

The actual development uses the repository’s concrete program and graph datatypes, but the proof obligation has this
shape: every emitted node uses only earlier node ids, every emitted shape matches the operator contract, and the
evaluator for the emitted node agrees with the source operation at the corresponding program point.
Proved forward compiler correctness. We isolate a first-order, SSA-style forward fragment and prove that lowering it
to the operator-tagged IR preserves semantics. The theorem is stated over exception-valued evaluation: both the source
semantics and the IR semantics return either a value (ok) or an explicit failure (error) when shape/type constraints are
violated. Stating the result at this level preserves successful runs and well-defined failure behavior. The same invariant
later lifts from the forward fragment to graph-level reasoning.
  Theorem B.1: Forward lowering correctness

  Let lower(p, θ) be the IR obtained by lowering a forward program p with parameters θ, and let Evalsrc and Evalir
  denote exception-valued evaluation of the source fragment and IR, respectively. Then for all inputs x,
                                       Evalir (lower(p, θ), x) = Evalsrc (p, θ, x).

The following theorem targets the verifier/demo fragment. A single theorem for arbitrary user-written T ORCH L EAN
programs in the current higher-order/tagless-final embedding requires a logical-relations or parametricity development,
or a different frontend encoding; that extension remains future work.
  Theorem B.2: Eager–graph correspondence

  For any fixed eager execution run that produces a computation tape T with forward values vi and a backward pass
  that computes gradients gi , there exists a well-typed SSA/DAG graph G such that:
         • Forward correspondence: the eager forward values agree with the graph denotation (vi = [[G]](x)i for
           all nodes i).
         • Backward correspondence: the eager backward gradients agree with graph backpropagation (gi =
           backpropCtx(G, x, seed)i for all nodes i).


B.4   T ORCH L EAN programs, Modules, and API design

The core idea behind T ORCH L EAN is that a neural network model is a backend-generic program built from a small,
well-defined Ops interface. This avoids maintaining separate semantics for eager execution and compiled graphs: the
same T ORCH L EAN program can be interpreted by an eager backend that records a computation tape (as in PyTorch), or
by a compiler backend that statically builds an SSA/DAG graph representation suitable for proofs and verification. Both
paths share the same semantic meaning.
To make this concrete, consider a simple model consisting of a linear layer followed by a vector softmax, written as a
backend-generic T ORCH L EAN program:


                                                           22
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                            A P REPRINT



def softmaxModel {a : Type} [Context a] [DecidableEq Shape] :
    TorchLean.Program a (paramShapes ++ [xShape]) yShape :=
  fun {m} _ _ =>
    fun w b x => do
      let logits <- TorchLean.linear (m := m)
        (inDim := inDim) (outDim := outDim) w b x
      TorchLean.softmax (m := m) (s := yShape) logits


This definition is polymorphic in the scalar type α (which can be Float, IEEE32Exec, or R) and in the backend monad
m, which allows the same model to be executed in different contexts. The resulting term is structured enough to be
compiled into our intermediate representation and fed directly to verification passes, reducing the gap between “the
model as written” and “the model as verified.”
For supervised learning workflows, we package models together with their training setup using a ScalarModuleDef
structure. This bundles the initial parameters with a scalar loss function into a single object:
structure ScalarModuleDef (paramShapes inputShapes : List Shape) where
  initParams : Torch.TList Float paramShapes
  loss :
    forall {a : Type}, [Context a] -> [DecidableEq Shape] ->
      TorchLean.Program a (paramShapes ++ inputShapes) Shape.scalar


We store initial parameters as Float literals primarily for ergonomic reasons: it keeps small examples readable, allowing
us to write tensorND! blocks without constantly fighting type casts. The cast from Float to the chosen scalar backend
is treated as part of the workflow layer rather than part of the core semantics, which keeps the specification layer clean
while maintaining flexibility.
Using this structure, a typical training loop is similar to PyTorch code. When instantiating a module, we choose both
the scalar backend (via a Float -> a cast function) and the execution mode (.eager or .compiled):
open Runtime.Autograd.TorchLean.Module

let m <- defn.instantiate (cast := cast) (backend := .eager)
for _ in List.range T do
  let _ <- ScalarModule.forward m xs
  let _ <- ScalarModule.backward m xs
  ScalarModule.step m lr xs


For stateful optimizers (e.g. Adam), we can step using an explicit optimizer state aligned with the parameter shapes:
open Runtime.Autograd.TorchLean

let opt := Optim.adam (lr := lr) (beta1 := 0.9) (beta2 := 0.999) (epsilon := 1e-8)
let st <- ScalarModule.initOptim m opt
for _ in List.range T do
  let st’ <- ScalarModule.stepWith m opt st xs
  -- continue with st’


We introduce this wrapper to match the expected workflow (define a model, run a training loop) while keeping the
resulting computation connected to the same SSA/DAG graph semantics that our proofs and verifiers consume.
Some workloads require integer-valued indices sourced from data (e.g., class labels for classification losses, or token/row
indices for embedding lookups). Mainstream frameworks typically represent these indices as integer tensors that
participate in the same runtime graph, even though gradients do not flow through the indices themselves. T ORCH L EAN
makes this separation explicit: the differentiable graph remains single-dtype over the chosen scalar domain, while
indices are provided through a separate non-differentiable channel in the Session interface. In the Session interface,
users supply scalar or batched indices as external inputs, and index-dependent operators (e.g., row-gather / embedding
lookup) treat these indices as read-only selectors while gradients flow only through the floating-point tensor values (e.g.,
into the embedding matrix). This design avoids mixed-dtype graphs while still supporting standard ML patterns such as
cross-entropy with integer labels and embedding-style table lookups.
What is fderiv / HasFDerivAt? In Lean/mathlib, fderiv denotes the (Fréchet) derivative of a function between
finite-dimensional real vector spaces, represented as a linear map; HasFDerivAt is the predicate that a function has a
specified Fréchet derivative at a point. Informally, this is the standard Jacobian-level notion of differentiability: for
f : Rn → Rm , fderiv returns the Jacobian Df (x) as a linear operator, and reverse-mode backpropagation computes
its adjoint action on a cotangent seed. For non-smooth or domain-sensitive primitives (e.g., ReLU at 0, log at nonpositive
inputs), we prove a pointwise variant that requires explicit side conditions ruling out those problematic points.


                                                                23
                                        T ORCH L EAN: Formalizing Neural Networks in Lean                                               A P REPRINT



Table 4: Autograd operator coverage (Fréchet-derivative level). “Global” means we have a NodeFDerivCorrect
proof (a HasFDerivAt theorem without side conditions). “Pointwise” means we prove NodeFDerivCorrectAt under
explicit hypotheses that rule out non-differentiable points (e.g., no zeros/ties). Operators listed under “Not covered”
may still be executable (and may have a deterministic backprop convention), but are not claimed correct at the level of
classical derivatives.

OpKind / primitive                 Global HasFDerivAt                              Pointwise (side conditions)                      Not covered

Linear / shape ops                 add, sub, mul_elem, linear, matmul, –                                                            –
                                   conv2d, broadcastTo, reshape, flatten,
                                   permute, reduce_sum, reduce_mean, sum,
                                   concat (curated axes), swap_first_two,
                                   transpose3d_last_two
Smooth nonlinearities / losses     tanh, sigmoid, exp, square, sinh, cosh, –                                                        –
                                   softplus,      gelu     (tanh    approximation),
                                   silu, softmax/log_softmax (curated axis),
                                   layernorm (curated axis), mse_loss, cross-
                                   entropy/NLL/BCE/KL pointwise losses, smooth
                                   surrogates safe_log and smooth_abs (with
                                   ε > 0)
Non-smooth / domain-sensitive      –                                                 relu, abs, log, inv, sqrt, max_elem/min_elem   –
                                                                                     (no ties)
Structured graph families          fixed-mask dropout, scaled dot-product attention, –                                              full GPT/ViT stacks,
                                   unmasked MHA, residual MHA, post-norm trans-                                                     masked causal de-
                                   former sublayers, BatchNorm-like graphs, one-step                                                coder blocks,        full
                                   Elman RNN, gather-row / embedding lookup ad-                                                     recurrent/state-space
                                   jointness                                                                                        sequence       theorems,
                                                                                                                                    FNO        spectral-conv
                                                                                                                                    training paths
Nondifferentiable / workflow ops   –                                               –                                                detach,
                                                                                                                                    rand_uniform,
                                                                                                                                    stochastic        masks
                                                                                                                                    beyond       fixed-mask
                                                                                                                                    dropout,            pool-
                                                                                                                                    ing       (max_pool2d,
                                                                                                                                    avg_pool2d),          ex-
                                                                                                                                    ecutable           CUD-
                                                                                                                                    A/cuBLAS/cuFFT
                                                                                                                                    kernels




-- Sketch: indices are non-differentiable; gradients flow into emb only.
sess   := Session.new(...)
emb    := const(sess, W)         -- differentiable parameter tensor
idx    := input_indices(sess)    -- non-differentiable indices from data
rows   := gather_rows(sess, emb, idx)
loss   := ...
backward(loss) -- dW accumulates; no gradients w.r.t. idx



Operator coverage across layers. T ORCH L EAN exposes a shared set of primitives through the operator-tagged
IR (NN.IR.OpKind) for both eager execution and proof-linked compiled execution. Autograd correctness is estab-
lished for a curated subset of these primitives at the Fréchet-derivative level: Table 4 summarizes which ops are
proved globally (NodeFDerivCorrect/HasFDerivAt), which are proved pointwise under explicit side conditions
(NodeFDerivCorrectAt for non-smooth or domain-sensitive ops), and which are not covered by classical-derivative
proofs (though they may remain executable under deterministic conventions). For verifier integration, the T ORCH -
L EAN→IR compiler targets a conservative forward, first-order fragment, while the LiRPA stack provides IBP broadly
and a basic CROWN-style affine pass with sound fallbacks when tighter relaxations are not implemented. Appendix B.6
gives the corresponding coverage details.
Control flow, variable-length sequences, indexing, and state. Our verified/compiled semantics targets SSA/DAG
computation graphs: a finite, side-effect-free dataflow artifact evaluated in topological order. As a result, data-dependent
branching and loops are not directly part of the verifier IR. Instead, dynamic control flow is handled by reification into a
finite graph when the structure is known at compile time—for example, unrolling an RNN/GRU/LSTM cell for a fixed
seqLen, or representing Transformers as acyclic attention blocks. This restriction matches the intended verification
regime: certificates and proofs are stated about a fixed graph denotation [[G]], rather than about an open-ended program
whose control flow depends on runtime data.
Indexing requires special care because most indexing operators consume integer-valued indices (labels, token ids,
embedding row selectors) that are inherently non-differentiable and introduce mixed-dtype graphs (float activations


                                                                         24
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                           A P REPRINT



plus integer tensors). Mainstream ML runtimes permit such mixed graphs, but they complicate a semantic setting where
we want a single, uniform scalar domain for the differentiable graph (to support clean denotations, autograd theorems,
and bound propagation). T ORCH L EAN therefore separates concerns: the differentiable graph remains single-dtype over
the chosen scalar domain, while indices are supplied through an explicit non-differentiable channel in the Session
API (e.g., scalar/batched naturals for labels and lookup indices). Index-dependent ops (e.g., embedding lookup / row
gather) treat these indices as read-only selectors; gradients flow only through the floating-point values (e.g., into the
embedding table or downstream layers), not through the indices themselves. On the verifier path, T ORCH L EAN supports
conservative indexing patterns that admit a clean lowering to the IR (e.g., scalar/row gathers reduced to one-hot selection
and matmul); general integer-indexed gather/scatter, variable-shape slicing, and shape-changing data-dependent
indexing remain outside the verified IR.
Finally, state is modeled explicitly rather than implicitly. The verifier semantics and most proofs assume layers are pure
functions of their inputs (and any provided parameters), which is essential for treating the model as a mathematical
object with a stable denotation. This is straightforward for affine layers and activations, but it requires care for layers
with PyTorch style internal updates (e.g., BatchNorm running mean/variance). In T ORCH L EAN, such updates are
performed outside the backend-generic op set: batch statistics can be computed from data, and running buffers updated
explicitly in the imperative session layer. This design keeps the denotation used by verification free of hidden mutation,
and makes any remaining state/update assumptions and trust boundaries visible at the API level.

B.5   Autograd verification

Training and verification pipelines routinely rely on gradients: optimization steps, sensitivity analyses, and derivative-
based certificates (e.g., Lyapunov or PINN residual bounds) all assume that the computed derivatives match the
model’s intended semantics. In mainstream ML systems, backpropagation is trusted because it is heavily tested, but its
correctness is rarely stated as a theorem about the exact computation being executed. T ORCH L EAN makes this link
explicit: we prove, for any well-typed SSA/DAG computation graph, that reverse-mode backpropagation computes the
adjoint Fréchet derivative of the graph denotation. This turns gradient correctness into a semantic property of the same
graph that is executed and verified, enabling derivative-dependent guarantees to compose cleanly with the rest of the
framework rather than resting on an implicit trust assumption.
The proof is organized in two stages that separate algorithmic correctness from analytic interpretation. This structure
makes the development modular and reusable across different scalar domains.
Stage 1: Algebraic adjointness (backend-generic). We first prove a graph-level adjointness law that does not depend
on real analysis. The statement is parametric over an abstract scalar interface (our Context typeclass): any scalar
domain that supports the required ring/ordering operations (e.g., reals, floats, intervals) can instantiate the theorem. At
this level, reverse-mode backpropagation is characterized as computing a vector–Jacobian product (VJP) that is adjoint
to the Jacobian–vector product (JVP) with respect to a dot product on tensor contexts (i.e., heterogeneous tuples of
tensors matching the graph’s typed input interface). Intuitively: pushing a perturbation forward (JVP) and pushing a
cotangent backward (VJP) are dual operations, and their duality is captured by a single inner-product identity.
Contexts and dot products. Let ⟨·, ·⟩Γ denote the dot product on the input context Γ (a typed tuple of tensors), defined
by summing tensorwise dot products over all inputs/parameters. This dot product is bilinear and symmetric, which is
exactly the structure needed for adjointness statements.
Forward/JVP/VJP as programs on a graph. For a well-typed SSA/DAG graph G and input x, we define three
evaluation procedures: (i) forward evaluation EvalG (x), (ii) forward-mode JVP JVPG (x; δx), and (iii) reverse-mode
backprop/VJP VJPG (x; ȳ). All three follow the graph’s topological order (forward) and reverse-topological order
(backward).

# Forward evaluation (topological order)
Eval_G(x):
  for node i in topo_order(G):
    v[i] = op_i(v[parents(i)])
  return v[out]

# Forward-mode JVP (propagate tangents)
JVP_G(x; dx):
  (v, _) = Eval_G(x)            # reuse forward values
  dv[input] = dx; dv[others] = 0
  for node i in topo_order(G):
    dv[i] = J_op_i(v[parents(i)]) * dv[parents(i)]
  return dv[out]

# Reverse-mode VJP / backprop (propagate cotangents)
VJP_G(x; seed):



                                                            25
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                            A P REPRINT



  (v, _) = Eval_G(x)
  bar[out] = seed; bar[others] = 0
  for node i in reverse(topo_order(G)):
    for p in parents(i):
      bar[p] += VJP_op_i(p, v[parents(i)], bar[i])
  return bar[input]             # gradients w.r.t. inputs/params




  Theorem B.3: Graph adjointness (algebraic)

  For any well-typed SSA/DAG graph G (over any Context) and any x, δx, and cotangent seed ȳ,
                                          JVPG (x; δx), ȳ   =     δx, VJPG (x; ȳ) .

Stage 2: Analytic upgrade (real calculus). Stage 1 establishes a purely algebraic adjointness law over an abstract
scalar interface. In Stage 2 we specialize to R and connect that law to standard multivariate calculus. The key step is to
relate shape-indexed tensor spaces to finite-dimensional Euclidean spaces: for each tensor shape s, let n = size(s) and
identify tensors with vectors in Rn via a (total) vectorization map and its inverse. This lets us interpret graph evaluation
as a function EvalVecG : RNin → RNout between Euclidean spaces and use the usual Fréchet derivative (Jacobian as a
linear map).
Vectorization and inner products. Let vecs : Tensor(R, s) → Rsize(s) be the flattening map (with inverse unvecs ).
We define the tensor dot product ⟨a, b⟩s by summing coordinatewise products over the shape; the bridge theorem states
that this dot product coincides with the standard Euclidean inner product after vectorization.

# Conceptual definition (shape-indexed)
vec_s   : Tensor(R,s) -> R^{size(s)}      # flatten
unvec_s : R^{size(s)} -> Tensor(R,s)      # reshape

# Bridge property
< a, b >_s == < vec_s(a), vec_s(b) >_{R^{size(s)}}




  Theorem B.4: Tensor–vector inner-product bridge

  For any shape s and tensors a, b ∈ Tensor(R, s),
                                           ⟨a, b⟩s =    vecs (a), vecs (b) Rsize(s) .

From local calculus to graph calculus. For each primitive operator (node kind), we prove a standard calculus fact: its
forward-mode JVP coincides with applying its Fréchet derivative to a tangent vector at the current input (and similarly,
its VJP coincides with applying the adjoint of that derivative to a cotangent seed). Combining these node-level facts with
the SSA/DAG structure yields a global theorem for any well-typed graph. In finite dimensions, the adjoint of a linear
map is just the transpose with respect to the Euclidean inner product; operationally, this is exactly what reverse-mode
backprop computes.

  Theorem B.5: Backpropagation computes the adjoint derivative

  Let G be a well-typed SSA/DAG graph over R and let EvalVecG denote its vectorized denotation. Assume the
  graph satisfies the local differentiability hypotheses for its primitives (i.e., GraphFDerivCorrect G). Then for
  any input x and cotangent seed ȳ,
                                                                            ⊤
                                         VJPG (x; ȳ) = D EvalVecG (x) ȳ,
  where D EvalVecG (x) is the Fréchet derivative (Jacobian as a linear map) and (·)⊤ denotes its adjoint (transpose)
  with respect to the standard inner product.

Interpretation. The theorem states that reverse-mode backprop is not merely an implementation heuristic: it computes
the mathematically correct cotangent propagation associated with the derivative of the graph denotation. For non-smooth
or domain-sensitive primitives (e.g., ReLU at 0, log at nonpositive inputs), we use a pointwise variant with explicit side
conditions that rule out problematic points.


                                                             26
                                      T ORCH L EAN: Formalizing Neural Networks in Lean                                            A P REPRINT



               Algebraic layer                           Tensor–vector bridge                                 Global theorem
              α-generic tensors
            ⟨JVPG (x; δx), ȳ⟩ =
                                          vectors       Tensor(R, s) ∼
                                                                     = Rsize(s)             calculus          VJPG (x; ȳ) =
              ⟨δx, VJPG (x; ȳ)⟩                       ⟨a, b⟩s = ⟨vec(a), vec(b)⟩                           (D EvalVecG (x))⊤ ȳ


                                                              proved                                                   proved
                 proved



       Linear / shape ops                           Elementwise ops                                    Reductions / special
       • affine / linear layers                     • smooth: tanh, σ, exp                             • softmax/log-softmax (curated)
       • matmul, conv2d                             • pointwise: ReLU (off 0), log                     • losses: MSE, cross-entropy
       • reshape/permute/reductions                 (on > 0)                                           • normalization (curated)
                                                    • smooth surrogates: safe-log,
                                                    smooth-| · |
Figure 10: Two-stage autograd proof architecture with primitive coverage. Stage 1 proves adjointness between JVPG
and VJPG over abstract scalars; Stage 2 bridges tensors to Euclidean spaces and upgrades to the Fréchet-derivative
statement VJPG (x; ȳ) = (D EvalVecG (x))⊤ ȳ. Bottom row summarizes operator classes covered by local derivative
lemmas; see Table 4 for details.


B.6   Node correctness and primitive operation proofs

The global backprop theorem is proved once for SSA/DAG graphs by composing local facts about each primitive.
Accordingly, each primitive operator (node kind) must supply a correctness lemma connecting its implemented JVP/VJP
rules to the mathematical derivative of its forward map. We use two variants: a global form for primitives that are smooth
everywhere, and a pointwise form for non-smooth or domain-sensitive primitives (handled in the next paragraph).
  Theorem B.6: Global node correctness (smooth primitives)

  Let op be a primitive with forward map f : Rn → Rm , and implemented tangent and cotangent rules JVPop (x; δx)
  and VJPop (x; ȳ) (as used by the Stage 1 algorithms). We say op is globally correct if for every x there exists a
  (continuous) linear map Df (x) such that
                                         JVPop (x; δx) = Df (x) δx and
                                                                      ⊤
                                            VJPop (x; ȳ) = Df (x) ȳ
  for all tangents δx and cotangents ȳ. Equivalently, JVPop and VJPop satisfy the adjointness identity
  ⟨JVPop (x; δx), ȳ⟩ = ⟨δx, VJPop (x; ȳ)⟩ under the standard inner product.

This is the exact local hypothesis required by the Stage 2 upgrade: once each node kind used in a graph satisfies the
above property, the previously stated graph theorem (Theorem 2.1 / Theorem B.5) follows by SSA/DAG composition.
Example (affine layer). For f (x) = W x + b, the derivative is the constant linear map Df (x) = W . Our implemen-
tation sets JVPop (x; δx) = W δx and VJPop (x; ȳ) = W ⊤ ȳ, so the local theorem holds immediately. In Lean, the
differentiability fact is discharged using the standard lemma that affine maps have constant Fréchet derivatives (e.g.,
hasFDerivAt_affine), after which the equalities above reduce to linear-algebra identities.
Pointwise correctness and kink points. For non-smooth or domain-sensitive primitives we use a pointwise predicate
(our NodeFDerivCorrectAt): the same local condition as in Theorem B.6 holds, but only at a specific evaluation point
x under explicit side conditions that guarantee classical differentiability (e.g., ReLU requires all relevant coordinates
̸= 0; log requires inputs > 0; inv/div require nonzero denominators; max / min require no ties).
  Theorem B.7: Pointwise node correctness (non-smooth primitives)

  Let op be a primitive with forward map f : Rn → Rm and implemented rules JVPop (x; δx) and VJPop (x; ȳ).
  Fix a point x and assume an explicit side condition Hop (x) that guarantees classical differentiability at x (e.g., for
  ReLU: all relevant coordinates ̸= 0; for log: inputs > 0; for max / min: no ties). Then there exists a linear map
  Df (x) such that for all δx and ȳ,
                                              JVPop (x; δx) = Df (x) δx                 and
                                                                                 ⊤
                                                    VJPop (x; ȳ) =     Df (x)        ȳ.



                                                                   27
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                             A P REPRINT



  Equivalently,
                                        JVPop (x; δx), ȳ    =    δx, VJPop (x; ȳ) .

At kink points where the Fréchet derivative is undefined, we do not claim a calculus-level result; instead, the runtime still
defines a deterministic executable backprop convention (as in mainstream autodiff systems) and we justify these rules at
the algebraic level via the Stage 1 adjointness law, treating them as part of the internal semantics. Establishing that
such conventions correspond to valid generalized derivatives (e.g., Clarke subgradients) at the kink points encountered
during optimization is a separate, more delicate direction beyond Fréchet-derivative correctness.
Higher-order derivatives. Our proved autograd theorem is a first-derivative result: it characterizes reverse-mode as
computing the adjoint Fréchet derivative of the forward denotation. We do not obtain second derivatives by recursively
applying this theorem to the backward pass, since the backward graph can introduce non-smooth, branch-dependent
primitives (e.g., ReLU gates) that complicate a clean calculus-level story. In the PINN case studies, we instead bound
u′ and u′′ via derivative-aware bound propagation on the original operator-tagged forward graph (a directional first-
derivative pass and a dedicated second-derivative pass for low-dimensional inputs over the smooth operator subset used
in the demos), avoiding differentiation of the backward graph altogether. The runtime includes executable higher-order
utilities (e.g., forward-over-reverse/HVPs via dual-number techniques), but full higher-order correctness requires
extending the local node library and proof obligations to higher derivatives (including handling or excluding kinks), and
then lifting the same SSA/DAG composition arguments to those higher-order rules.
Primitive operation proofs. Figure 10 summarizes the local derivative lemmas that feed the global SSA/DAG theorem.
Rather than proving autograd correctness per model, we prove correctness per primitive and compose these facts along
the graph. The proof work falls into three recurring patterns.
(1) Linear primitives (affine maps). For primitives whose forward maps are affine/linear (e.g., linear, matmul,
conv2d), the derivative is the corresponding linear map, and the VJP is its adjoint (transpose), exactly matching standard
backprop rules. Conv2D is handled by viewing convolution as a linear operator on flattened tensors and proving that
our implemented backward rule coincides with the adjoint of that operator.
  Theorem B.8: Example: affine node rule

  For f (x) = W x + b, we have Df (x) = W and VJP(x; ȳ) = W ⊤ ȳ.

(2) Elementwise primitives (coordinatewise calculus). For coordinatewise nonlinearities (e.g., tanh, sigmoid, exp),
we lift scalar derivatives to tensors/vectors by showing that the derivative of the elementwise
                                                                                        √       map is diagonal in the
standard basis. For non-smooth or domain-sensitive elementwise ops (e.g., ReLU, log, ·, 1/x), we use the pointwise
variant away from kink/singularity points (as summarized in Table 4).
  Theorem B.9: Example: elementwise lifting (informal)

  If f : R → R is differentiable at each coordinate of x ∈ Rn , then D(f ⊙ )(x) is the diagonal linear map with entries
  f ′ (xi ).

(3) Reductions and normalization (coupled coordinates). Operations like softmax/log-softmax and normalization
layers couple coordinates via a shared denominator or statistics, so we prove their derivatives directly from their
defining formulas and show that the resulting VJP matches the implemented backward rule. Standard losses (e.g., MSE,
cross-entropy) then follow by composition: we treat them as maps from logits to a scalar and apply the chain rule on
top of the network’s derivative.
  Theorem B.10: Example: softmax differential (informal)
                                                               
  Let s = softmax(x). Then D softmax(x)[dx] = s ⊙ dx − ⟨s, dx⟩1 .

Together, these primitive proofs populate the local hypothesis used by the global SSA/DAG theorem; the detailed
coverage matrix (global vs. pointwise) appears in Table 4.

B.7   Graph-level composition and the reverse-mode algorithm

This subsection explains how the graph-level reverse-mode theorem (Theorem 2.1) is obtained from the local node
lemmas (Theorems B.6 and B.7) using SSA/DAG composition. The proof is modular: once each primitive node


                                                             28
                                     T ORCH L EAN: Formalizing Neural Networks in Lean                          A P REPRINT



kind is equipped with a correct JVP/VJP rule, correctness lifts automatically to any well-typed graph built from those
primitives.
Induction over SSA/DAG structure. A well-typed SSA/DAG graph admits a topological evaluation order, so its
denotation [[G]] can be seen as a composition of node-level functions applied to previously computed values. The global
proof proceeds by induction over the graph (equivalently, over the node list in SSA order): assume a prefix graph is
correct, then extend it by one locally-correct node. The forward denotation of the extended graph is a composition, so
its derivative follows by the chain rule, and the adjoint derivative follows by reversing the order of composition. This is
exactly what reverse-mode implements.
Reverse-mode algorithm (VJP form). To connect the theorem statement to familiar autodiff intuition, we write the
backpropagation procedure as a cotangent propagation on the DAG. The symbol seed (often written ȳ) denotes the
cotangent supplied at the graph output: it specifies which linear objective of the output we are differentiating. For
scalar losses, the seed is typically 1; for vector outputs (e.g. logits), the seed can be any cotangent vector and yields the
corresponding vector–Jacobian product.
# Forward pass (topological order)
Eval_G(x):
  for node i in topo_order(G):
    v[i] = op_i(v[parents(i)])
  return v, v[out]

# Reverse pass (cotangent propagation)
VJP_G(x; seed):
  (v, _) = Eval_G(x)
  bar[out] = seed; bar[others] = 0
  for node i in reverse(topo_order(G)):
    for p in parents(i):
      bar[p] += VJP_op_i(p, v[parents(i)], bar[i])
  return bar[input]      # gradients for inputs/params


Why accumulation is correct on DAGs. If a node value is used by multiple downstream nodes, it receives multiple
cotangent contributions in the reverse sweep. The algorithm therefore adds these contributions (the += line). This is not
an implementation detail: it is the mechanism that makes reverse-mode correct for graphs with shared subexpressions.
Algebraically, correctness follows from the adjointness identity in Stage 1 (Theorem B.3): the dot product is bilinear, so
contributions from different paths combine by summation.
From VJP to gradients (the scalar-loss special case). Many presentations restrict to scalar losses L : Rn → R
and identify reverse-mode with ∇L(x). Our statement is more general: for f : Rn → Rm and a cotangent seed
ȳ ∈ Rm , reverse-mode returns the adjoint derivative applied to the seed, (Df (x))⊤ ȳ, i.e. a vector–Jacobian product
(Theorem 2.1). The scalar-loss gradient is recovered by taking m = 1 and ȳ = 1 (or by composing a vector-valued
network with a scalar loss and applying the chain rule). This formulation is essential for ML workloads where
intermediate quantities are tensor-valued (e.g. logits, features, attention blocks), but training and verification often
require derivatives of particular scalar objectives derived from them.
Parameter handling (typed parameter packs). Modern models have heterogeneous parameter packs: a linear layer
carries a matrix and a bias vector, a Conv2D layer carries a 4D kernel and bias, and attention blocks carry multiple
projection matrices. T ORCH L EAN represents such packs as a shape-indexed heterogeneous list (a typed product) rather
than a string-keyed map. A parameter pack is typed by a list of shapes [s1 , . . . , sk ] and contains one tensor of each
corresponding shape; semantically this is the finite product space Tensor(α, s1 ) × · · · × Tensor(α, sk ). This choice
makes parameters part of the same typed interface as ordinary graph inputs: compilation treats them as additional
inputs to the SSA/DAG graph, and reverse-mode returns cotangents for both data inputs and parameters in the same
structured form. Optimizers then become shape-preserving transformations on parameter packs (e.g., a pointwise
update that zips parameters with their gradients), so a mismatch between a parameter tensor and its gradient is ruled
out by the typechecker rather than discovered at runtime. By contrast, common ML runtimes store parameters in
mutable, string-keyed containers for convenience, which pushes the shape contract into informal conventions; in
T ORCH L EAN, the shape contract is intrinsic, and entire classes of “wrong tensor paired with wrong gradient” bugs
become unrepresentable.

B.8   Core Definitions and IR Semantics

We focus on the core definitions that the rest of T ORCH L EAN builds on: (i) the shape-indexed tensor semantics used
as the reference meaning for proofs and verification, (ii) the common scalar interface, and (iii) the operator-tagged
SSA/DAG IR. We include these excerpts because extending T ORCH L EAN (adding ops, adding backends, or adding
verification rules) requires understanding the semantic core these components share.


                                                             29
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                            A P REPRINT



Shape-indexed tensors (why this representation). The most basic design decision is to make tensor shapes part of
the type. In mainstream ML systems, shapes are runtime values and shape mismatches appear late (as runtime errors
or, worse, silent broadcasting mistakes). In contrast, we want the shape contract to be an invariant of the logic: if an
expression typechecks, it cannot be ill-shaped. This yields cleaner theorem statements (no repeated “shape matches”
premises) and makes the semantic core robust to conventions that are easy to get wrong (layout, reshaping discipline,
implicit broadcasting).
Why functional tensors rather than flat arrays? For the semantic layer, we prioritize proof ergonomics and semantic
clarity. We represent a tensor structurally as a total indexing function: a tensor of shape dim n s is literally a function
Fin n -> Tensor a s. This makes theorems about tensor programs follow the same recursion as the datatype. For
example, commutativity of elementwise addition is proved by induction on the shape: the scalar case is immediate, and
the dim case reduces to the induction hypothesis pointwise. With a flat array representation, such proofs require explicit
index arithmetic and bounds reasoning, which is significantly harder to automate and more brittle as the operator library
grows. Finally, the spec layer intentionally does not commit to a concrete storage layout (row-major vs. column-major),
so it remains a stable reference meaning across execution backends.
                           Listing 6: Core shape-indexed tensor definitions (semantic layer).
namespace Spec

/-- Shapes: scalar, or "n copies of a subshape". -/
inductive Shape where
  | scalar : Shape
  | dim    : Nat -> Shape -> Shape

/-- Shape-indexed tensors, represented structurally. -/
inductive Tensor (a : Type) : Shape -> Type where
  | scalar : a -> Tensor a .scalar
  | dim    : forall {n s}, (Fin n -> Tensor a s) -> Tensor a (.dim n s)

How to read this definition. The constructor Tensor.scalar is a scalar value. The constructor Tensor.dim stores
an index function that returns the i-th subtensor. Thus:
                                   Tensor(α, dim n s) ≡ (Fin n → Tensor(α, s)),
i.e., a length-n vector of subtensors of shape s. This immediately gives canonical encodings of common ML shapes: a
vector of length n is dim n scalar; a matrix m × n is dim m (dim n scalar); and a batch of images (batch size
B, channels C, height H, width W ) is dim B (dim C (dim H (dim W scalar))).
Why this pays off in proofs. Most tensor operations are defined by recursion on shape, so proofs follow the same
structure. For instance, elementwise addition on dim n s tensors is defined pointwise on the Fin n index and then
recursively on s; extensional equality reduces tensor equality to pointwise equality of index functions. This makes basic
algebraic properties (associativity, commutativity, distributivity) and shape-preservation properties easy to state and to
prove.
Efficiency note (bridging to array-backed execution). The functional tensor representation is chosen for the semantic
reference used by proofs and verification; it is not intended as the fastest execution format. For executable workflows,
T ORCH L EAN additionally provides a materialized, array-backed representation and a semantics-preserving bridge
between the two, so programs can run efficiently while still referring to the same underlying meaning. We discuss this
representation, its compilation path, and the resulting performance trade-offs in Section C (and use it throughout the
runtime experiments).
Scalar polymorphism (one model, many semantics). Most specification-level definitions are polymorphic in the
scalar type a, so the same model code can be interpreted over multiple numeric domains: R for proof level reference
semantics, executable floating-point domains for runtime demos, and abstract/rounded domains for sound bounds
and error envelopes. To make this practical, T ORCH L EAN collects the numeric structure required by neural-network
operators into a single typeclass, Context a. Intuitively, Context a is “the interface a scalar type must implement to
run NN code.”
                                  Listing 7: Scalar interface for NN code (Context).
class Context (a : Type) extends
  Add a, Sub a, Mul a, Div a, Neg a,
  LT a, LE a, One a, Zero a,
  MathFunctions a, Numbers a where


                                                            30
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                             A P REPRINT



  decidable_gt : DecidableRel (fun x y : a => x > y)


This interface includes: (i) ring-like arithmetic (Add/Sub/Mul/Div/Neg) used throughout linear algebra and losses;
(ii) order structure (LT/LE and decidability) needed for conditionals and piecewise primitives (e.g., ReLU, max/min);
(iii) constants (Zero/One) and numeric literals (Numbers); and (iv) transcendental functions (MathFunctions, e.g.,
exp, log, tanh, sqrt, sin, cos). By making the required scalar operations explicit, we can state and reuse theorems
without committing to a particular numeric representation: a lemma proved for Context a specializes uniformly to R,
executable float models, and rounding/interval domains used by verification.
Graph IR structure (why SSA/DAG). Our verification substrate is an operator-tagged SSA/DAG intermediate
representation (IR) with explicit node kinds and output shapes. The IR is intentionally simple: it is the single semantic
target reused across execution, differentiation, and verification. More precisely, the IR is (i) operator-tagged so each
node carries an explicit primitive identifier (an opcode) and any parameters needed to interpret it, and (ii) in SSA/DAG
form so each intermediate value is defined exactly once and dataflow is acyclic.
Why a DAG? Most verifier pipelines (IBP/LiRPA/CROWN) operate on feedforward computation graphs: sound bounds
are propagated along edges, which requires a well-defined evaluation order. A DAG gives exactly this: nodes admit a
topological order, so evaluation and bound propagation are deterministic and total. This also makes proofs modular:
semantic properties can be established by induction over the node list (SSA order), and verification passes can be
defined as simple forward (or forward+backward) sweeps over the same graph object. Cycles and implicit control
flow, by contrast, require separate fixpoint semantics (and additional invariants) for both execution and verification;
T ORCH L EAN handles such behavior by reification into finite graphs when needed (e.g., unrolling a fixed-length
recurrent cell).
Why SSA? SSA (static single assignment) ensures every intermediate value has a unique definition. This simplifies both
implementation and reasoning: backpropagation and certificate checking can attach metadata (values, bounds, dual
variables) to node IDs without ambiguity, and gradient contributions from multiple consumers are accumulated by
summation in the reverse sweep. SSA therefore makes “what does this gradient/bound refer to?” a structural property
of the IR.
Core definition. Each node records: (i) an operation kind, (ii) the IDs of its parent nodes (its inputs), and (iii) a declared
output shape. OpKinds carry any parameters required for interpretation (e.g., conv2d stores channel counts, kernel size,
stride, padding; softmax stores an axis).

                                Listing 8: Operator tagged SSA/DAG IR (core excerpt).
inductive OpKind where
  | input
  | linear
  | relu
  | conv2d (inC outC kH kW stride padding : Nat)
  | softmax (axis : Nat)
  | layernorm (axis : Nat)
  | mse_loss

structure Node where
  id       : Nat
  parents : List Nat
  kind     : OpKind
  outShape : Spec.Shape


Typing and denotation. Well-typedness checks that each node’s parent shapes match what its OpKind expects and that
outShape matches the primitive’s output contract. The denotation [[G]] evaluates nodes in topological order (which is
well-defined because the graph is acyclic) and is total on well-typed graphs. This denotational semantics is the object
used by proofs (e.g., autograd correctness) and by verification passes (e.g., IBP/CROWN transfer rules): bounds and
certificates are interpreted against the same primitive meanings that execution uses.
Losses Much of the machine learning literature phrases training in terms of a scalar loss L(θ) and its gradient ∇θ L, but
in a tensor-typed setting, we found it important to make the “scalar” part explicit: losses are tensor programs followed
by reductions. This design choice makes the structure of losses clear and enables precise reasoning about gradients.
In the library, losses are ordinary T ORCH L EAN programs that compute a tensor-valued quantity and then reduce it
to a scalar. We provide both a primitive scalar loss (mse_loss) and a small Loss helper layer that mirrors common


                                                             31
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                          A P REPRINT



              Table 5: High-level comparison between PyTorch Paszke et al. [2019] and T ORCH L EAN.

Aspect                     PyTorch                                          T ORCH L EAN
Shapes                     Dynamic runtime shapes; many errors are          Shapes are part of types (Tensor α s);
                           runtime exceptions.                              many mismatches are untypeable.
Dtypes                     Many numeric and integer dtypes; mixed-          Scalar-polymorphic single-dtype graphs
                           dtype graphs are common.                         (one α per run); integer indices handled
                                                                            via a separate non-differentiable channel
                                                                            (NatRef/NatVecRef) in sessions.
Execution modes            Eager by default, with compilation/export        Eager tape backend and proof-linked com-
                           toolchains (TorchScript, ONNX, AOT).             piled SSA/DAG backend share one seman-
                                                                            tics; the compiled graph is the verifier target
                                                                            by construction.
Autograd status            Widely tested and trusted, but not formally      Reverse-mode correctness theorem for well-
                           proved correct.                                  typed SSA/DAG graphs; eager runs linked to
                                                                            proved graphs.
Indexing                   Tensor-valued indexing/slicing/gather/scatter    Typed indexing primitives and session-level
                           across dtypes (e.g. LongTensor).                 Nat channels for labels/indices; not yet
                                                                            PyTorch-complete for tensor-valued integer
                                                                            indices.
Breadth/performance        Very broad op surface and ecosystem; highly      Curated op surface focused on verification-
                           optimized CPU/GPU kernels.                       relevant primitives; extensible via a “new op”
                                                                            workflow; Lean execution prioritizes clari-
                                                                            ty/verification over performance.



PyTorch conventions: MSE, cross-entropy/negative-log-likelihood variants (one-hot targets and index-based targets),
and binary cross-entropy (including a stable “with logits” form), each with explicit reduction (mean or sum).
Extending T ORCH L EAN across the stack. Adding a new op is a predictable, checkable workflow rather than an ad
hoc engineering task. When we add a primitive to T ORCH L EAN, we treat it as a complete commitment: it should
have a spec meaning, a typing rule, and the transfer rules needed by theorems/verification. The workflow has five
steps: (1) Spec semantics: Define the operation as a total function on shape-indexed tensors in the spec layer, with
an explicit shape contract. If the operation is non-smooth or domain-sensitive (e.g. log, division, max), either define
a safe/smoothed variant intended for theorem statements, or adopt the pointwise hypothesis style and document the
required preconditions. (2) IR support: Add an op tag to the IR (OpKind) and define its typing rule (input and output
shapes). This is what makes compilation and verification passes recognize the op uniformly. (3) Autograd over R:
Provide local JVP/VJP rules and prove the local adjointness law (or the pointwise variant). Once this lemma exists, the
global theorem applies to any graph using the op. (4) Verification transfer rules: For IBP, define a sound transfer
function on boxes. For affine relaxations, either implement and prove the relaxation, or import bounds as certificates
and check the certificate constraints in Lean. (5) Numeric backends: Decide which execution backends support the op
(Float, IEEE32Exec), and (when relevant) add local rounding/error lemmas so the op participates in graph level NF
bounds.


B.9   T ORCH L EAN vs. PyTorch

This comparison focuses on goals. PyTorch is an industrial execution framework optimized for throughput, hardware
utilization, and ecosystem breadth; T ORCH L EAN is a semantic interface whose main objective is to make training code
and verifier-time artifacts coincide so that guarantees are stated about the executed artifact. Accordingly, T ORCH L EAN
does not attempt to compete with PyTorch on industrial-scale throughput; it prioritizes a precise semantic link between
user programs, IR graphs, runtime artifacts, and proofs. Optional CUDA kernels and fast runtime paths support
larger examples, but the key contribution is the semantic substrate: performance-oriented backends can be added
behind explicit contracts without changing what is being verified. T ORCH L EAN is also not “just an API”: the design
choices directly enable the verification story. Compilation is a first-class path that lowers programs to a well-typed
operator-tagged SSA/DAG IR, and eager execution records a tape that we prove corresponds to an equivalent well-typed
IR graph (Theorem B.2). Once a graph exists, whether it was obtained eagerly or via lowering, the same semantic
object is consumed by autograd theorems, bound-propagation passes, and certificate checkers.


                                                           32
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                         A P REPRINT



C     Modern workflow theory and semantics: CUDA, attention, RL, diffusion, probability,
      SSL, and model families
In this section, we spell out the contracts behind the workflow examples used in the paper. For each family, we name the
Lean object, write the equation or recurrence it denotes, and state what Lean checks versus what comes from a runtime
or external producer. Concretely, attention is a masked softmax equation, an RL rollout is a finite recurrence, diffusion
is a schedule plus a sampler step, and self-supervised learning is represented by a finite objective over masks or views.

C.1   CUDA/native FFI and runtime contracts

The CUDA path is an execution feature, not a second proof semantics. Lean’s kernel checks theorem terms and
definitions written in Lean; it does not inspect CUDA source code, GPU machine code, cuBLAS, cuFFT, driver
behavior, memory allocation, or the order in which floating-point reductions are scheduled. In T ORCH L EAN, a native
kernel is therefore attached to a Lean operator whose denotation is already defined at the specification or IR level. The
formal object remains the graph denotation; the native call is an optional implementation path.
For an operator tag τ with specification
                               [[τ ]]α : Tensorα (s1 ) × · · · × Tensorα (sk ) → Tensorα (s),
a CUDA-backed implementation is treated through a conformance statement of the form
                                      cudaτ (x1 , . . . , xk ) ≈ [[τ ]]Float32 (x1 , . . . , xk ),
under explicit preconditions about dtype, shape, layout, device memory, determinism, and precision mode. When this
relation is not proved in Lean, it is recorded as a runtime assumption and tested by conformance/regression checks.
Thus a theorem about [[G]] does not become a theorem about arbitrary GPU execution unless the needed conformance
hypothesis is supplied.
The implementation uses Lean’s FFI discipline: Lean declarations expose an opaque runtime handle, while C/CUDA
wrappers allocate device buffers, launch kernels, and copy results across the host/device boundary. The following
schematic code shows the shape of the interface; the real implementation fixes the buffer layout and performs the
corresponding runtime checks.
                        Listing 9: Schematic Lean-side boundary for a native CUDA primitive.
namespace Runtime.Autograd.Cuda

opaque Buffer : Type

@[extern "torchlean_cuda_bmm"]
opaque Buffer.bmm : Buffer -> Buffer -> IO Buffer

/-- Runtime-side check before calling the native kernel. -/
def bmmChecked (a b : TensorMeta) (ha : Buffer) (hb : Buffer) : IO Buffer := do
  checkMatmulShapes a.shape b.shape
  checkDType a.dtype .float32
  checkDType b.dtype .float32
  Buffer.bmm ha hb

end Runtime.Autograd.Cuda


       Listing 10: Schematic C/CUDA wrapper; memory safety and launch behavior are outside Lean’s kernel.
extern "C" LeanObj torchlean_cuda_bmm(LeanObj a, LeanObj b) {
  CudaBuffer* A = unwrap_buffer(a);
  CudaBuffer* B = unwrap_buffer(b);
  CudaBuffer* C = allocate_like_matmul(A, B);
  cublasSgemmStridedBatched(/* handles, shapes, strides, A, B, C */);
  return wrap_buffer(C);
}


This pattern is used for dense and batched matrix products, reductions, broadcasting, tensor views, convolution/pooling
and transposed-convolution kernels, FFT/spectral operators, softmax/log-softmax, normalization kernels, attention-
oriented and fused-attention paths, gather/scatter utilities, positional/RoPE helpers, selective-scan-style sequence


                                                                  33
                                T ORCH L EAN: Formalizing Neural Networks in Lean                          A P REPRINT



kernels, and other runtime paths used by the examples. Several backward and reduction kernels use floating-point
accumulation. Because floating-point addition is not associative, atomic accumulation can be mathematically standard
while still not being bit deterministic across schedules. T ORCH L EAN therefore exposes deterministic-reduction modes
for selected paths and treats remaining scheduling choices as part of the deployment boundary.
The same policy applies to fused attention. The Lean specification can state and prove that a formal FlashAttention
operator denotes standard masked scaled-dot-product attention. That equality is a statement about the mathematical
operator in Lean. It is not a verification of a particular CUDA implementation, tiled online-softmax schedule,
HBM/SRAM traffic pattern, or GPU kernel binary.

C.2   FlashAttention, masks, and fused-attention denotation

The attention specification is stated once, following the standard scaled-dot-product attention abstraction and the
FlashAttention denotational contract used in the codebase [Dao et al., 2022]. For query, key, and value tensors
Q ∈ αnq ×d , K ∈ αnk ×d , V ∈ αnk ×dv , and an optional Boolean mask M , standard scaled dot-product attention is the
relation
                                                                        QK ⊤
                                                                             
                                    SDPA(Q, K, V, M ) = softmaxM √               V.                                 (1)
                                                                            d
The mask semantics are part of the specification. In the formal definition, masked entries contribute zero probability
after the row-wise masked-softmax step; causal masks are therefore ordinary finite predicates over query/key positions,
not a convention hidden inside a backend call.
FlashAttention is modeled as a fused route to the same denotation. A configuration record stores scheduling metadata
such as query/key tile sizes, but these fields are intentionally ignored by the mathematical denotation: tiling changes
how a backend may compute the row, not what function the row denotes. At the spec level, T ORCH L EAN names an
online/tiled operator and proves the central equality
                  onlineSoftmaxTiledAttention(cfg, ctx ) = scaledDotProductAttention(ctx ).                         (2)
It also exposes the fused forward operator theorem
                           flashAttention(cfg, ctx ) = scaledDotProductAttention(ctx )                              (3)
and the corresponding VJP/backward contract
             flashAttentionBackward(cfg, ctx , ȳ) = scaledDotProductAttentionBackward(ctx , ȳ).                   (4)
These equalities are the formal content behind the paper’s statement that “FlashAttention equals ordinary attention” in
T ORCH L EAN: the claim is a denotational equality between a fused specification operator and the standard masked-
attention specification. It is deliberately not a proof that a particular CUDA source file implements Dao-style IO-aware
tiling correctly. The native CUDA path is regression-tested against the composed attention path and is documented as
an FFI trust boundary; the theorem surface stays inside the specification layer.
This split is useful for compiler style reasoning. A graph rewrite may replace a composed QK ⊤ -mask-softmax-P V
subgraph by a fused attention operator only if both sides share the same typed attention context and mask convention.
The theorem above is exactly the small equality such a rewrite needs.
           Listing 11: Schematic attention contract: the fused operator is checked against masked SDPA.
structure AttentionCtx (a : Type) where
  Q K V : Tensor a _
  mask : Option (Fin _ -> Fin _ -> Bool)
  scale : a

def sdpa (ctx : AttentionCtx a) : Tensor a _ :=
  maskedSoftmax (ctx.scale * (ctx.Q.matmul ctx.K.transpose)) ctx.mask
    |>.matmul ctx.V

def flashSpec (cfg : FlashCfg) (ctx : AttentionCtx a) : Tensor a _ :=
  -- The schedule fields in cfg affect the implementation, not the denotation.
  sdpa ctx

theorem flashSpec_eq_sdpa (cfg : FlashCfg) (ctx : AttentionCtx a) :
    flashSpec cfg ctx = sdpa ctx := rfl



                                                          34
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                           A P REPRINT



C.3   Reinforcement-learning semantics: returns, Bellman operators, MDPs, and GridWorld

RL adds an environment boundary to the usual model/runtime boundary, so the appendix follows the standard discounted-
dynamic-programming vocabulary of Bellman operators, MDPs, returns, and generalized advantage estimation [Bellman,
1957, Puterman, 1994, Sutton and Barto, 2018, Schulman et al., 2016]. T ORCH L EAN separates three levels: (i) pure
rollout algebra over lists and finite tensors, (ii) Lean based MDPs and environments, and (iii) external simulators that
emit trajectories through a checked artifact boundary. Runtime collectors, optimizers, replay buffers, logging, and
optional CUDA execution live outside this pure layer.

Rollout algebra.    For a terminal flag d, define the continuation mask
                                                        
                                                          0, d = true,
                                               m(d) =                                                                  (5)
                                                          1, d = false.
The one-step backup, TD target, and TD residual are
                                          Bγ (r, b, d) = r + γ m(d) b,                                                 (6)
                                                    yt = rt + γ m(dt )V (st+1 ),                                       (7)
                                                    δt = yt − V (st ).                                                 (8)
For a reward list r0 , . . . , rT −1 , discountedReturnsFrom is the right-fold recurrence
                                            GT = b,       Gt = rt + γGt+1 .                                            (9)
With done flags, the recurrence becomes
                                              Gt = rt + γm(dt )Gt+1 ,                                            (10)
so terminal episodes reset the bootstrap. Generalized advantage estimation is formalized by the reverse recurrence
                                               At = δt + γλm(dt )At+1 ,                                              (11)
where each AdvantageStep stores rt , V (st ), V (st+1 ), and dt . The corresponding return target is recovered by
Rt = At + V (st ). These definitions are intentionally over lists rather than fixed-shape tensors, because real rollouts
have variable length due to termination/truncation; fixed-horizon tensor variants can be built on top when needed.

Deterministic finite MDPs. The simplest MDP layer uses finite state and action types S = Fin(n) and A = Fin(m).
A deterministic finite MDP consists of an initial state, a total transition/reward/termination function
                                step : S × A → S × R × {terminated, truncated},                                      (12)
and a discount factor. For a value table v : S → α, the state-action value induced by one step is
                                     Qv (s, a) = r(s, a) + γm(d(s, a))v(s′ (s, a)).                                  (13)
The policy Bellman operator and optimality operator are
                                              (T π v)(s) = Qv (s, π(s)),                                             (14)
                                              (T ∗ v)(s) = max Qv (s, a),                                            (15)
                                                            a∈A

where the finite maximum is implemented with Finset.sup’ over a nonempty finite action space. Value functions and
action-value tables are typed tensors, so these operators can be used alongside the same tensor infrastructure as ordinary
neural models.

Finite stochastic MDPs. The finite stochastic layer replaces the deterministic successor with a typed transition row
P (· | s, a). A validity record requires nonnegative entries, rows summing to one, and 0 ≤ γ < 1. The expected next
value and Bellman action value are
                                                 X
                              E[v(s′ ) | s, a] =   P (s′ | s, a)v(s′ ),                                          (16)
                                              s′ ∈S
                                                                      X
                                  Qv (s, a) = r(s, a) + γm(d(s, a))           P (s′ | s, a)v(s′ ).                   (17)
                                                                      s′ ∈S

This layer gives the proof and runtime code a finite tensor representation for stochastic dynamics while avoiding the full
measure-theoretic overhead when the state space is finite.


                                                           35
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                            A P REPRINT



                               Listing 12: Schematic finite MDP and Bellman operator.
structure FiniteMDP (S A : Type) where
  reward : S -> A -> Float
  trans : S -> A -> S -> Float       -- row-stochastic transition table
  done   : S -> A -> Bool
  gamma : Float

def expectedNext (M : FiniteMDP S A) (v : S -> Float) (s : S) (a : A) : Float :=
  Finset.univ.sum (fun s’ => M.trans s a s’ * v s’)

def bellmanPi (M : FiniteMDP S A) (pi : S -> A) (v : S -> Float) (s : S) : Float :=
  let a := pi s
  M.reward s a + M.gamma * contMask (M.done s a) * expectedNext M v s a


Measure-theoretic Markov-kernel MDPs. For continuous or general measurable spaces, T ORCH L EAN defines an
MDP with measurable state space S, action space A, and a mathlib Markov kernel κ : S × A ⇝ S. The expected next
value is the integral                                   Z
                                     E[v(s′ ) | s, a] =   v(s′ ) dκ(s, a)(s′ ),                            (18)
                                                            S
and the Bellman policy operator is
                                                                      Z
                          (T π v)(s) = r(s, π(s)) + γm(d(s, π(s)))         v(s′ ) dκ(s, π(s))(s′ ).                   (19)
                                                                       S
The validity assumptions require κ to be a Markov kernel, reward and termination to be measurable, and 0 ≤ γ < 1. The
corresponding proof layer states standard discounted Bellman facts for bounded value functions, including monotonicity
and contraction in the sup metric:
                                           ∥T π v − T π w∥∞ ≤ γ∥v − w∥∞ ,                                         (20)
                                               ∗      ∗
                                            ∥T v − T w∥∞ ≤ γ∥v − w∥∞ .                                            (21)
Because γ < 1, these contraction theorems support uniqueness of the fixed point for the Bellman operator under the
stated metric assumptions.

GridWorld as a Lean based environment. The concrete GridWorld uses coordinate states (row, col), four actions
(up, down, left, right), border-clamped transitions, a goal cell, and a discount factor. Reaching the goal returns reward
0 and terminates; otherwise a transition receives reward −1. The environment has three views: a pure Env view
with explicit latent state, a deterministic finite MDP view obtained by flattening (row, col) to Fin(h · w), and a finite
stochastic view whose transition rows are one-hot. This gives the paper a small RL case where environment semantics,
Bellman operators, value tables, and rollout summaries all live inside Lean.

External simulators. For CartPole-, Pong-RAM-, or other Gymnasium-style workflows, the simulator is not hidden
inside a theorem. Python or another runtime produces observations, actions, rewards, log probabilities, and done/trun-
cation flags. Lean checks the rollout schema and then consumes the artifact for losses or graph properties. Thus the
verified object is a policy/value graph property, a Bellman/return calculation, or a checked rollout contract; the external
simulator remains a named producer.

C.4   Diffusion, sampling, probability-flow ODEs, and sampler stability

Diffusion models exercise a different kind of semantics from classifiers, so we separate deterministic sampler equations
from probability-law statements in the style of DDPM, DDIM, and score/probability-flow formulations [Ho et al., 2020,
Song et al., 2021a,b]. The objects of interest are schedules, noising maps, denoisers, reverse transitions, samplers, and
sometimes probability laws. T ORCH L EAN keeps these as scalar-polymorphic specification definitions so they can be
evaluated with Float, executable finite-precision models, intervals, or R, depending on the theorem or experiment.

Discrete VP schedules and forward noising. A discrete variance-preserving schedule of length T stores per-step
variances βt . The specification defines
                                               αt = 1 − β t ,                                             (22)
                                               ᾱ0 = 1,                                                   (23)
                                            ᾱt+1 = ᾱt αt .                                              (24)


                                                            36
                                   T ORCH L EAN: Formalizing Neural Networks in Lean                               A P REPRINT



The forward noising map qSample is the pure, total tensor function
                                                     √         √
                                       qt (x0 , ε) = ᾱt x0 + 1 − ᾱt ε.                                                    (25)
At this spec level ε is an explicit tensor input. The probabilistic interpretation ε ∼ N (0, I) belongs either to the
probability theory layer or to the runtime sampler that produces noise.
                           Listing 13: Schematic diffusion schedule and forward noising map.
structure VPSchedule where
  beta     : Nat -> Float
  alphaBar : Nat -> Float

def qSample (sch : VPSchedule) (t : Nat)
    (x0 eps : Tensor Float s) : Tensor Float s :=
  let c0 := sqrt (sch.alphaBar t)
  let c1 := sqrt (1.0 - sch.alphaBar t)
  Tensor.map2 (fun x e => c0 * x + c1 * e) x0 eps


Epsilon prediction and DDPM loss.           A denoising model is represented by an epsilon-prediction function
                                                        εθ : (x, t) 7→ εb.                                                  (26)
The standard epsilon-prediction training loss is a named wrapper around mean squared error:
                                                                                        2
                                        Lε (θ; x0 , t, ε) = ∥εθ (qt (x0 , ε), t/T ) − ε∥2 .                                 (27)
This does not require a special loss semantics: it reuses the existing tensor MSE definition but gives the diffusion
convention a domain-specific name.

DDPM reverse steps.        The epsilon-parameterized reconstruction is
                                                          √
                                                      xt − 1 − ᾱt εθ (xt , t/T )
                                        x
                                        b0 (xt , t) =          √                  ,                                         (28)
                                                                 ᾱt
with totalized safe division and nonnegative square-root wrappers in the executable definition. The reverse DDPM step
xt 7→ xt−1 uses
                                                                                   
                                                 1             βt
                                    µt (xt ) = √      xt − √          εθ (xt , t/T ) ,                           (29)
                                                 αt           1 − ᾱt
                                               1 − ᾱt−1
                                         βet =           βt ,                                                    (30)
                                                1 − ᾱt
                                                         q
                                      xt−1 = µt (xt ) + βet zt .                                                 (31)
The full sampler is a right fold over the finite time indices with an explicit noise stream zt , so stochasticity is not implicit
in the recursive definition.

DDIM and deterministic sampler semantics. The deterministic η = 0 DDIM step reuses the same x
                                                                                            b0 reconstruction
and recomposes the previous sample by
                                       √          p
                                              b0 + 1 − ᾱt−1 εθ (xt , t/T ).
                                 xt−1 = ᾱt−1 x                                                          (32)
T ORCH L EAN also exposes DDIM as a real-valued DynamicalSystem step. This is useful because the same trajectory,
fixed-point, Lipschitz, and contraction vocabulary used for state-space models can be applied to sampler transitions.

Probability-flow ODE.        For continuous time, a linear VP schedule stores β0 , β1 and defines
                                           β(t) = β0 + t(β1 − β0 ),                                                         (33)
                                                                           
                                                               1          2
                                           ᾱ(t) = exp −β0 t − (β1 − β0 )t ,                                                (34)
                                                               2
                                                   p
                                           σ(t) = 1 − ᾱ(t).                                                                (35)


                                                                37
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                             A P REPRINT



Under an epsilon parameterization, the probability-flow ODE right-hand side is specified as
                                                       1        β(t)
                                          fθ (x, t) = − β(t)x +      εθ (x, t).                                        (36)
                                                       2        σ(t)
The Euler step is the simple total tensor operation
                                              E∆t (x, t) = x + ∆t fθ (x, t),                                           (37)
and the sampler integrates backward on a uniform grid with negative ∆t. A fixed-time Euler step is exposed as a
DynamicalSystem, giving samplers a common interface with other discrete dynamical systems in T ORCH L EAN.

Sampler boundary and stability theorems. The sampler proof layer records small facts that are important for
checkers and model transformations. Zero-step samplers return the initial sample. DDIM and PF-ODE system adapters
reduce definitionally to the corresponding step functions. For Euler integration, a generic metric bound has the form
                              ∥E∆t (x) − E∆t (y)∥2 ≤ ∥x − y∥2 + |∆t| ∥f (x) − f (y)∥2 .                                (38)
If the right-hand side is L-Lipschitz, then one Euler step is (1 + |∆t|L)-Lipschitz. The same adapter pattern transports
Lipschitz or contractive-step facts to DDIM/PF-ODE systems. These theorems are deliberately modest: they do not
prove convergence of a trained denoiser, but they make sampler transformations and verification targets mathematically
explicit.

C.5   Probability-theory layer for Gaussian forward processes

The pure diffusion specification treats noise as an explicit input. The probability theory layer adds the mathematical law
when the noise is Gaussian. In a finite-dimensional Euclidean space E, let Z ∼ N (0, I) and define
                                                                  √             √
                                  Xt = c0 x0 + c1 Z,        c0 = ᾱt , c1 = 1 − ᾱt .                                 (39)
The formal object is the push-forward of the standard Gaussian measure under the affine map z 7→ c0 x0 + c1 z.
T ORCH L EAN proves that this forward law is a probability measure and records the corresponding Gaussian structure
for the affine image. Keeping this layer separate is important: tensor samplers can remain total and executable, while
probabilistic claims are made only where the relevant measure-theoretic assumptions are available.
This is also the template for future probabilistic generative models. A VAE, normalizing-flow, or stochastic-diffusion
theorem should distinguish (i) the deterministic tensor map used by the runtime, (ii) the distribution over the random
source, and (iii) the theorem connecting the push-forward or transition kernel to the intended probabilistic model.

C.6   Self-supervised objective algebra and anti-collapse guards

Self-supervised learning is formalized at the objective contract level, covering MAE, JEPA, VICReg, and Barlow-style
objective families [He et al., 2022, Assran et al., 2023, Bardes et al., 2022, Zbontar et al., 2021]. We do not try to
prove that self-supervised training discovers useful representations. Here we record the finite semantics of masks,
views, target branches, predictive losses, and geometry guards, so an experiment or theorem cannot silently change the
objective being optimized.

Finite masks and masked loss. For n patches or tokens, a mask is a predicate m : Fin(n) → Bool. The selected-
index form is a list I = [i1 , . . . , ik ], and the generic masked loss is
                                                                         X
                                                    maskedLoss(I, ℓ) =      ℓ(i).                        (40)
                                                                     i∈I

Lean proves the elementary list laws needed to treat the serialized mask as a finite objective: nil is zero, cons adds one
term, appending index lists adds losses, reversing the index list preserves the sum, and if every selected per-index loss is
zero then the masked loss is zero.
                     Listing 14: Schematic masked objective used by MAE and JEPA-style losses.
def maskedLoss (idxs : List (Fin n)) (lossAt : Fin n -> Float) : Float :=
  idxs.foldr (fun i acc => lossAt i + acc) 0.0

-- The concrete proof is by induction on xs.
theorem maskedLoss_append (xs ys : List (Fin n)) (lossAt : Fin n -> Float) :
    maskedLoss (xs ++ ys) lossAt = maskedLoss xs lossAt + maskedLoss ys lossAt



                                                            38
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                             A P REPRINT



MAE.     For a finite patch batch x : Fin(n) → Patch, predictions pi , and per-patch loss ℓ, the MAE objective is
                                                            X
                                            MAE(I, x, p) =      ℓ(xi , pi ).                                      (41)
                                                                 i∈I

The formal theorems state that this loss decomposes over appended mask lists, is invariant under reversal of I, is zero
when every selected patch loss is zero, and that identity decoding gives exact reconstruction. These are small facts,
but they pin down the intended semantics: masked reconstruction is a set-like objective over selected patches, not an
artifact of an arbitrary serialization order.

JEPA and target-branch extensionality. JEPA-style objectives separate a context representation c, target representa-
tions ti , a predictor p(c, i), and a representation loss d. The finite objective is
                                                                 X
                                             JEPA(I, c, t, p) =       d(ti , p(c, i)).                         (42)
                                                                 i∈I

The target branch is modeled as an ordinary value at the objective boundary, matching the stop-gradient design intent.
The theorem jepaLoss_target_ext states that if two target branches agree on selected indices, then the loss is
identical. Thus unselected target coordinates cannot influence the objective.

Predictive-view contract. The generic contract unifies MAE and JEPA. A PredictiveViewContract stores target
indices I, a context value, a target value at every finite index, a target encoder, a predictor, a per-index distance, and a
nonnegative geometry guard. The objective is
                                Obj(C) = PredictiveLoss(C) + GeometryGuard(C).                                         (43)
MAE is recovered by choosing the identity target encoder into patch/pixel space and zero geometry guard. JEPA is
recovered by choosing the latent target representation as the target space. Lean proves both instance theorems: the
predictive-view loss/objective reduces definitionally to the MAE or JEPA finite objective under these choices.

VICReg, Barlow-style guards, and view graphs. Geometry guards are added orthogonally to the prediction term.
VICReg-style summaries include invariance, variance-floor, and covariance/redundancy components with weights
(λ, µ, ν). Barlow-style summaries penalize off-diagonal redundancy and diagonal mismatch. The current finite theory
records local anti-collapse facts: collapsed coordinates pay a positive variance-floor penalty under a positive margin, the
identity correlation summary has zero redundancy loss, and collapsed diagonal summaries incur a positive Barlow-style
penalty. A view-graph energy layer represents finite alignment objectives
                                                           X
                                              EG (z) =            ∥zi − zj ∥2 ,                                       (44)
                                                       (i,j)∈E(G)

which is zero for collapsed representations but becomes useful only when paired with a spread or variance guard. This
makes the common SSL distinction precise: alignment alone permits collapse; the geometry guard is the formal object
that rules it out locally.

C.7   Sequence, generative, scientific, and diagnostic model families

The examples now cover more than the verifier core. The sequence layer includes causal attention, multi-head attention,
RoPE-style positional rotations, token/embedding boundaries, generation loops, recurrent layers, and selective-scan
primitives for Mamba/S4-style state-space models. The central semantic issue is causality: future tokens should not
change prefix outputs, cache offsets must agree with token positions, and chunked or fused scans should refine the
same recurrence. T ORCH L EAN exposes these as formal contracts and as regression tests. For state-space models, scan
composition lemmas connect optimized block scans to sequential recurrence, and prefix/non-anticipation lemmas state
that appending future inputs preserves emitted prefix outputs.
The generative and scientific layers use the same tensor language for different mathematical roles. Diffusion examples
expose schedules, denoisers, sampler states, and reverse transitions. VAE/VQ-VAE/GAN-style examples expose latent
variables, diagonal-Gaussian or KL terms, finite codebooks, nearest-code quantization, reconstruction losses, and
generator/discriminator objectives. FNO/PINN examples use spectral operators, derivatives, and residual constraints;
spline/ODE and Arb-backed workflows use external numerical producers followed by Lean-side certificate replay. We
include these examples to show that modern ML workflows can be assigned named semantic objects that are suitable
for later checking; the section is not a claim about leaderboard model quality.


                                                            39
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                          A P REPRINT



The diagnostic layer makes semantic boundary failures explicit. The Bug Zoo covers cases such as causal-mask
leakage, KV-cache/RoPE position drift, stable-loss boundaries, tokenizer/embedding mismatches, batch-invariance
bugs, normalization-state bugs, Float32 edge cases, padding conventions in native kernels, and certificate/IR import
mismatches. Each bug-shaped test is small on purpose: it isolates a boundary where a conventional ML system can
silently change semantics. In T ORCH L EAN, the corresponding property can be stated as a mask theorem, prefix-
invariance check, schema check, shape invariant, finite-precision contract, or certificate replay obligation.



D     Numerical Semantics

Motivation and trust boundaries. We make numerical semantics explicit because it is easy to prove theorems
about a real-valued model and then silently execute a Float32 implementation whose behavior differs at exactly the
corner cases that matter for verification (rounding, overflow/underflow, NaN/Inf propagation, signed zeros, and library
conventions). IEEE 754 is the de facto standard for floating-point arithmetic: it specifies binary/decimal formats,
rounding rules, and exception behavior (including NaNs/Infs and their default handling). In Lean, however, the built-in
runtime floating-point types are opaque to the kernel: they are intended for computation and are implemented by
external runtime code rather than reducible definitions in the logic Lean Prover Community [2025a]. As a result, we
treat the scalar type α as an explicit parameter and require every theorem or executable demo to declare which numeric
semantics it is using; this turns “what arithmetic are we reasoning about?” into part of the statement rather than an
implicit convention.
IEEE 754 (what it standardizes). IEEE 754 defines floating-point numbers as signed significands with bounded
exponents (e.g., binary32/Float32), together with rounding modes (typically round-to-nearest-even) and exceptional
values such as ±∞ and NaNs. It also specifies default behaviors for exceptional operations (e.g., division by zero,
invalid operations) and comparison/order conventions. For verification, many “real-analysis proofs” do not apply
verbatim in IEEE arithmetic: operations are rounded, may overflow/underflow, and may produce non-finite values
whose propagation rules are part of the semantics.
Motivation from Flocq. Our design is inspired by Flocq, a mature Coq library for reasoning about floating-point arith-
metic. Flocq cleanly separates (i) the format (which numbers are representable: radix, exponent bounds, subnormals)
from (ii) the rounding operator (how an exact real result is mapped to a representable value), and it provides theorem
infrastructure for compositional error bounds (Boldo and Melquiond, 2011). We adopt this same separation because
neural network verification needs both: (a) theorem-friendly “round-on-R” models to state and compose numerical
error envelopes, and (b) executable, bit-level semantics to make corner cases (NaNs, signed zeros, overflow) concrete
when running full demos and checkers.


    Summary: four numeric layers in T ORCH L EAN. We provide (i) trusted runtime floats for speed, (ii) an
    executable IEEE-754 model for explicit Float32 behavior, (iii) proof level rounding models for compositional
    error reasoning, and (iv) an external validated-numerics oracle for rigorous high-precision enclosures of difficult
    primitives (notably transcendentals).



    (A) Runtime execution: Float/Float32 (fast, but opaque). Lean exposes Float (binary64) and Float32
    (binary32) as runtime types intended for efficient execution. Their operations are implemented by external/runtime
    code (e.g., compiled to underlying machine/C operators) rather than by kernel-reducible definitions, so we treat
    them as an explicit trust boundary for proofs Lean Prover Community [2025a].



    (B) Executable Float32 semantics: IEEE32Exec (bit-level IEEE). For full demos that require explicit Float32
    behavior, we implement IEEE32Exec, a Lean-defined, bit-level IEEE-754 binary32 kernel. This model includes
    signed zeros, subnormals, NaNs/Infs, and the IEEE rounding/exception behavior for core arithmetic. It is executable
    inside Lean and therefore gives an explicit meaning to “Float32 execution” independent of a particular runtime
    implementation. The remaining “hardware gap” (showing a target platform refines this exact software model) is
    handled as an explicit conformance interface rather than being silently assumed.



                                                            40
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                              A P REPRINT



  (C) Proof-relevant rounding models: FP32/NF (round after each primitive). For theorem statements and error
  analysis, we use “round-on-R” models inspired by Flocq: each primitive is specified as “compute in R, then
  round” under a chosen format/rounding mode, enabling compositional error envelopes through entire graphs.
  FP32 instantiates this with IEEE-style binary32 rounding (finite-only, i.e., it does not model NaN/Inf), while NF
  generalizes the same idea to user-chosen radices/exponent functions/rounding operators.


  (D) Validated numerics oracle: Arb/FLINT (rigorous transcendental enclosures). For rigorous enclosures of
  transcendental functions (e.g., tanh, exp, log, √, sin, cos) at user-chosen precision, we integrate an Arb/FLINT
  backend via python-flint behind an explicit oracle boundary. The oracle returns certified ball/interval enclosures
  at a specified working precision (in bits), which we can consume as certificate-like artifacts in verification pipelines.
  This layer is not kernel-reducible and is treated as an external trust boundary; its role is to provide high-quality
  validated bounds where implementing tight transcendental enclosures natively is cumbersome, while keeping the
  trusted computing base explicit.


Why we implement both (bit-level and round-on-R). These layers serve different proof/verification needs: bit-level
execution (IEEE32Exec) is ideal for making “what happens on Float32?” concrete in checkers and demos, including
edge cases (NaNs, signed zeros) that real analysis ignores; round-on-R models (FP32/NF) are ideal for theorem
statements and compositional error envelopes because they expose the rounding operator as a mathematical object that
can be bounded and composed (in the style of Flocq (Boldo and Melquiond, 2011)). Together, they let us support both
the verification community (explicit executable semantics) and the floating-point proof community (compositional
rounding/error reasoning) under a single semantic umbrella.
Lean-specific note (why opacity matters). Because Lean’s runtime floats are not encoded in the logic, the kernel
cannot reduce or reason about them without additional axioms; in particular, floating-point operations are implemented
externally (and thus are not definitionally equal to any mathematical model inside Lean). This is why T ORCH L EAN
separates “fast execution” from “proved semantics” and makes the trust boundary explicit in both the main text and
Table 1.
One surface name, switchable semantics. To keep model code uniform while making numerical assumptions explicit,
T ORCH L EAN exposes a single surface notion of “Float32” with a selectable semantic mode. This lets the same
model/program be instantiated with (i) an executable bit-level IEEE-754 semantics for full runs, or (ii) a proof level
rounding model for theorem statements and compositional error envelopes, without rewriting the model.
                               Listing 15: Selecting Float32 semantics at the type level.
open TorchLean.Floats

-- Executable Float32 semantics (bit-level IEEE-754 binary32):
abbrev ExecF32 : Type := F32                 -- = IEEE32Exec

-- Proof Float32 semantics (round-on-R, finite-only):
abbrev ProofF32 : Type := F32 .fp32          -- = FP32

Why multiple float modes are necessary. No single floating-point representation serves all verification goals.
IEEE 754 defines the concrete behavior of deployed floating-point arithmetic, including rounding and exceptional
values (NaNs/Infs, signed zeros, subnormals). For executable demos and certificate checking where these corner cases
matter, we want an explicit, runnable model of binary32 semantics—hence IEEE32Exec. For theorem statements about
numerical stability and graph level error budgets, we instead want a proof-level “round after each primitive” model
over R that supports compositional error reasoning in the style of verified floating-point libraries such as Flocq—hence
FP32/NF. Finally, Lean’s built-in runtime floats (Float/Float32) are fast but opaque to the kernel and therefore live
on the explicit trust/validation side of the interface.
Float32 mode selection. At the API level we package this choice behind a small mode enum, so use sites are explicit
about which semantics they rely on:
                             Listing 16: A single “Float32” name with explicit semantics.
inductive Float32Mode where
  | fp32 | ieee754Exec

abbrev Float32 (mode : Float32Mode := .ieee754Exec) : Type :=


                                                            41
                                T ORCH L EAN: Formalizing Neural Networks in Lean                         A P REPRINT



  match mode with
  | .fp32         => FP32
  | .ieee754Exec => IEEE32Exec

Proof-level rounding model (NF). For graph level error bounds we use a proof level model that rounds after every
primitive operation. Conceptually, an NF value stores a real number together with a chosen format (radix and exponent
function) and rounding operator; each primitive is specified as “compute in R, then round,” and local rounding/error
lemmas compose over SSA/DAG graphs.
Practical rule of thumb. Use IEEE32Exec when you want executable Float32 behavior (including corner cases) to
match an IEEE-style semantics; use FP32/NF when you want theorem statements with explicit, compositional rounding
error envelopes; use runtime Float/Float32 for fast prototyping where the numeric backend is an explicitly trusted
assumption.

                     Listing 17: Schematic runtime conformance contract for deployed Float32.
-- A theorem using this class is conditional on the deployment target.
class RuntimeFloat32MatchesIEEE32Exec : Prop where
  add_finite : forall x y,
    finite x -> finite y -> finite (x + y) ->
    toIEEE32 (runtimeAdd x y) = IEEE32Exec.add (toIEEE32 x) (toIEEE32 y)
  mul_finite : forall x y,
    finite x -> finite y -> finite (x * y) ->
    toIEEE32 (runtimeMul x y) = IEEE32Exec.mul (toIEEE32 x) (toIEEE32 y)
  relu_exact : forall x,
    toIEEE32 (runtimeRelu x) = IEEE32Exec.max (toIEEE32 x) IEEE32Exec.posZero

We use this form intentionally. A graph theorem can be unconditional about IEEE32Exec, while a deployed-runtime
theorem carries a visible assumption such as RuntimeFloat32MatchesIEEE32Exec. The assumption records the
target configuration: rounding mode, denormal policy, fused operations, reduction order, and library implementation
choices.

D.1   Whole-graph NF bounds and hardware soundness

This section explains two complementary pieces of our numerical story: (i) how we compose per-operator rounding/error
lemmas into graph level error budgets in a “round after each primitive” model (NF), and (ii) how we connect an
executable bit-level Float32 semantics to that proof model on the finite (non-NaN/non-Inf) path, and what remains to
relate either of them to hardware execution.

Whole-graph NF bounds: local errors compose over SSA/DAG. NF is a proof level “round after each primitive”
semantics: each primitive is specified as “compute in R, then round” under a chosen format/rounding operator. We
relate NF values to real semantics via an explicit error relation ≈ε , and we prove graph level bounds by induction in
SSA/topological order (and analogously for backward sweeps when needed).

  Local-to-global error propagation (NF idea). Define a scalar approximation relation
                                        xnf ≈ε xR     ⇐⇒      |xnf − xR | ≤ ε,
  and lift it to tensors (pointwise or via a norm such as ℓ∞ ). Each primitive operator op comes with a lemma of the
  form:
                                 if uj ≈εj vj for all inputs j, then opnf (u) ≈ε′ opR (v),
  where the derived ε′ is computed from operator-specific stability bounds. For linear/affine primitives, ε′ follows
  from standard Lipschitz constants; for nonlinear primitives, it follows from local derivative bounds or global
  Lipschitz envelopes (on the region of interest). Whole-graph bounds are proved by induction over the SSA/DAG
  order: the induction hypothesis provides bounds for parent nodes, and the node lemma yields the bound for the
  current node.

Executable IEEE model → rounding-on-R model (internal refinement). NF/FP32-style reasoning is theorem-
friendly because rounding is an explicit mathematical operator on R, but it does not capture IEEE corner-case behavior
(NaNs/Infs, signed zeros, subnormals) directly. Conversely, a bit-level IEEE model is executable and makes those
corner cases concrete, but it is harder to use for compositional error proofs. We therefore establish an internal


                                                         42
                                   T ORCH L EAN: Formalizing Neural Networks in Lean                               A P REPRINT



refinement on the finite path: for the core Float32 arithmetic primitives (addition/subtraction/multiplication/division/sqrt
and min / max), we prove that interpreting the executable bit-level result as a real number agrees with applying the
corresponding round-to-Float32 operator to the real arithmetic result, under explicit side conditions that rule out NaN/Inf
and overflow-to-Inf.
  Theorem D.1: Internal refinement on the finite path

  Let ExecOp  √ 32 be a core Float32 primitive implemented by the executable bit-level IEEE model (e.g.,
  +, −, ×, /, ·, min / max), and let RealOp be the corresponding real operator. (For min / max on finite values,
  ExecOp32 (x, y) returns exactly one of its inputs, so the Round32 wrapper below is vacuous; we state the refine-
  ment uniformly for all listed primitives.) Let toReal interpret a finite Float32 value as a real number, and let
                                                                                                                
  Round32 be the IEEE-style round-to-Float32 operator on R. Define r(x, y) := RealOp toReal(x), toReal(y) .
  Assume the evaluation stays finite (no NaN/Inf and no overflow-to-Inf) on the considered inputs. Then for all
  inputs x, y in the finite domain,
                                                                                
                                    toReal ExecOp32 (x, y) = Round32 r(x, y) .
  Moreover, these per-primitive refinements compose: for any expression e built from the core primitives, interpreting
  the executable result with toReal agrees with evaluating the corresponding real expression and rounding at each
  primitive, under the same finiteness assumptions.

This bridge is necessary because it lets us run full demos under an explicit IEEE-754 semantics while still reusing the
cleaner FP32/NF error-envelope lemmas whenever the execution stays in the finite regime.

Hardware soundness: what remains and a pragmatic deployment path. IEEE 754 specifies formats, rounding
modes, and exception behavior, but real deployments can diverge through compilation and platform choices (e.g.,
flush-to-zero/denormals-are-zero, reassociation/“fast-math”, FMA contraction, or reduction order). To claim that
hardware Float32 execution inherits our theorems, one must additionally (a) fix a target semantics contract (rounding
mode, denormal policy such as FTZ/DAZ, contraction/reassociation policy, and reduction ordering), and (b) relate the
compiled runtime’s observable Float32 results to the chosen executable model (or to the rounding-on-R model) for the
operations actually used. This remains target-level future work.
Transcendentals and IEEE-754 (what is and is not specified). IEEE 754 precisely specifies formats and core
arithmetic (e.g., add/sub/mul/div, sqrt, comparisons, NaN/Inf behavior), but elementary/transcendental functions
(e.g., exp, log, sin, cos, tanh) are largely outside the standard’s required semantics and are typically provided by
system libm implementations. 2 As a result, even when two platforms are “IEEE compliant” for core arithmetic, their
transcendental results can differ across OS/compiler/libm versions or under different optimization flags. A deeper reason
is the table-maker’s dilemma: deciding the correctly-rounded result for an elementary function can require substantially
more precision than the target format in worst cases, which makes full bit-exact specification and implementation
nontrivial in practice [Brisebarre et al., 2025, Zimmermann, 2005].
Our deliberate split: executable IEEE core vs. explicit transcendental policy. Accordingly, T ORCH L EAN separates
concerns. For core IEEE arithmetic, IEEE32Exec provides a Lean-defined, bit-level model of binary32 behavior
(including signed zeros, subnormals, NaN/Inf propagation, and rounding), so the meaning of “Float32 execution” is
explicit inside the prover. For transcendental functions, we make the policy explicit rather than pretending it is uniquely
determined by IEEE:
• Deterministic in-kernel implementations for common ML primitives. For functions heavily used in ML pipelines
  (notably exp/log and hyperbolic functions used in activations and normalizers), we provide deterministic implemen-
  tations with a fixed rounding/approximation policy so that full executions are reproducible under IEEE32Exec.
• Explicit delegation when necessary. For functions outside the verified kernel surface (e.g., full trigonometric stacks),
  we may delegate to Lean runtime Float (or a chosen library implementation) and then round back to binary32,
  treating that choice as an explicit trust boundary rather than an implicit semantic fact.

Proof models cover transcendentals via “round the real function.” In parallel, the FP32/NF proof models include
transcendentals definitionally as “apply the real function, then round,” which supports theorem statements in terms
of explicit error envelopes and interval enclosures under stated hypotheses. This mirrors the classical verified-float
approach: instead of depending on a particular libm implementation, the semantics is a mathematical rounding operator
applied to the real function, enabling compositional reasoning [Brisebarre et al., 2025, Flocq Developers, 2025].
   2
    IEEE’s own background material explicitly notes that many programs rely on library elementary functions and that the standard
does not specify them.


                                                               43
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                              A P REPRINT



NaN payload caveat (why hardware conformance is subtle). IEEE 754 specifies NaN propagation at a high level
(operations produce NaN when given NaN inputs), but the choice of NaN payload (and some signaling-vs-quiet
details) is not fully uniform across real implementations IEEE Standards Association [2019]. Our executable kernel
fixes a deterministic policy (including a specific quieting/selection rule), and we prove properties about that policy.
Consequently, any claim that a concrete compiler/runtime/hardware Float32 implementation refines IEEE32Exec
must assume or establish compatibility with this concrete NaN policy (or adopt a quotienting notion of observational
equivalence that treats NaN payload differences as irrelevant for the target theorems).

E     CROWN verification: bounds, duality, and certificates
We expand Section 2.4 with implementation details for bound propagation and certificate checking.

E.1    IBP, CROWN/LiRPA, and certificate checking

Overview. Our verifier operates on the shared operator-tagged SSA/DAG IR and proves properties of the graph
denotation [[G]] by establishing sound enclosures for intermediate values and/or outputs. We support two complementary
verification modes: (i) native bound propagation implemented in Lean for demo-scale graphs, and (ii) certificate
checking, where an external verifier produces a bound/certificate that Lean checks against the same IR semantics.

    Acronyms.
    • IBP (Interval Bound Propagation): propagate interval boxes [l, u] forward through the network.
    • CROWN: propagate linear upper/lower bounds through nonlinearities to obtain tighter output bounds.
    • LiRPA (Linear Relaxation-based Perturbation Analysis): a general framework that derives/propagates linear
      relaxations (including CROWN- and DeepPoly-style rules) over general computational graphs.
    • α-CROWN: tightens CROWN bounds by optimizing relaxation parameters.
    • β-CROWN: incorporates split constraints (branch-and-bound) efficiently by encoding splits with optimizable
      parameters.


IBP (interval bound propagation). Interval Bound Propagation (IBP) is the simplest sound enclosure method
for neural computation graphs. Starting from an input region—typically an axis-aligned box [l0 , u0 ] (often used to
over-approximate an ℓ∞ ball)—IBP computes, for every node i in the graph, an interval enclosure [li , ui ] such that the
true node value satisfies vi (x) ∈ [li , ui ] for all admissible inputs x ∈ [l0 , u0 ]. The algorithm is a single forward sweep
in topological order: each primitive provides an interval transfer rule that maps parent bounds to a sound output bound,
maintaining the invariant “parents sound ⇒ child sound.” IBP is attractive because it is fast, compositional, and easy to
make formally sound, but it can be loose because plain intervals do not track correlations between coordinates (and thus
can over-approximate significantly after repeated mixing through linear layers).

    Example IBP transfer rules (sketch). All rules below are sound: they guarantee op(v) ∈ [l′ , u′ ] for all v ∈ [l, u].
    • Affine / linear y = W x + b (includes linear and flattened matmul cases). Write W = W + − W − with
      W + , W − ≥ 0 elementwise. Then
                                ly = W + lx − W − ux + b,                 uy = W + ux − W − lx + b,
      which is the standard interval-arithmetic enclosure for linear maps.
    • Monotone elementwise (e.g., ReLU, exp). Apply the function to endpoints:
                                        [ly , uy ] = [f (lx ), f (ux )]    (componentwise).
      For ReLU specifically, this yields ly = max(lx , 0) and uy = max(ux , 0).
    • Reductions (e.g., sum/mean over a fixed axis). Because reduction is linear, bounds reduce by summing/averaging
      endpoints along the axis:
                                              sum([l, u]) = [sum(l), sum(u)]
                                            mean([l, u]) = [mean(l), mean(u)].

                              Listing 18: Schematic interval objects and the linear IBP step.


                                                                 44
                                T ORCH L EAN: Formalizing Neural Networks in Lean                           A P REPRINT




structure Box (s : Shape) where
  lo : Tensor Float s
  hi : Tensor Float s

-- W = Wpos - Wneg, with Wpos,Wneg >= 0 elementwise.
def ibpLinear (W b : Tensor Float _) (x : Box inShape) : Box outShape :=
  let Wpos := Tensor.map (fun w => max w 0.0) W
  let Wneg := Tensor.map (fun w => max (-w) 0.0) W
  { lo := Wpos.matmul x.lo - Wneg.matmul x.hi + b,
    hi := Wpos.matmul x.hi - Wneg.matmul x.lo + b }

def ibpRelu (x : Box s) : Box s :=
  { lo := Tensor.map (fun z => max z 0.0) x.lo,
    hi := Tensor.map (fun z => max z 0.0) x.hi }


The Lean checker does not need to trust the producer’s explanation of how a bound was found. It recomputes the local
transfer step from parent boxes and compares the recomputed box with the claimed box. The following schematic
pattern is the core of the checker.

                               Listing 19: Schematic replay step for a node certificate.
def checkNode? (G : Graph) (cert : Cert) (st : CertState) (i : Nat) :
    Except CheckError CertState := do
  let node      <- G.node? i
  let parents   <- st.lookupAll node.parents
  let expected <- transfer node.kind parents
  let claimed   <- cert.boxFor i
  guard (sameShape expected claimed)
  guard (claimed.lo <= expected.lo + cert.tol)
  guard (expected.hi <= claimed.hi + cert.tol)
  pure (st.insert i claimed)


The inequalities are intentionally one-sided. A certificate may be looser than the recomputed bound and still be sound;
it may not claim a lower bound above the recomputed lower bound or an upper bound below the recomputed upper
bound unless the checker can prove that stronger claim.

IBP certificate soundness (graph dialect). To support certificate checking, we formulate IBP soundness for a safe
graph semantics that is explicitly partial: node evaluation fails when required parent values/parameters are missing
or when declared dimensions do not match. We then define a per-node IBP certificate step that deterministically
recomputes each node’s interval box from its parents’ boxes. The soundness proof follows the standard local-to-global
pattern: under a topological order and a supported operator subset, local semantic consistency and local certificate
consistency imply a global enclosure invariant.

  Theorem E.1: IBP certificate soundness
  Let G be a topologically sorted computation graph over a supported operator fragment, and fix a parameter store.
  Assume we are given: (i) a partial value semantics that computes node values by a one-step rule from parent values
  and parameters, and (ii) a one-step IBP rule that computes an interval box for each node from its parents’ boxes
  and parameters. Let (vi )i be any assignment of semantic node values that is locally consistent with the one-step
  value rule, and let (Bi )i be any assignment of certified interval boxes that is locally consistent with the one-step
  IBP rule. If each semantic input lies in its declared input box, then for every node i, whenever both vi and Bi are
  defined, the value vi lies in Bi componentwise.


Whole-graph IBP soundness for the concrete implementation. Beyond certificate soundness, we also connect
the theorem to the concrete implementations used in the demos. We define total “evaluate-by-id” and “propagate-by-
id” procedures, implemented by recursion on node id, and prove that they satisfy the local-consistency premises of
Theorem E.1. As a result, the computed IBP boxes enclose the computed semantic values whenever both procedures
return values:



                                                          45
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                             A P REPRINT



  Theorem E.2: Whole-graph IBP soundness for runIBP?

  Let evalGraphRec be the total value evaluator for G and runIBP? the corresponding total IBP propagation.
  Under the same structural assumptions (topological order, supported operators, and input enclosure), for every
  node i, whenever both procedures return a value vi and a box Bi , we have vi ∈ Bi componentwise.

Proof idea (both theorems). The enclosure invariant is preserved one node at a time: assuming all parent enclosures
hold, the operator-specific IBP transfer rule yields an enclosure for the current node consistent with its value semantics.
Topological order ensures that, at node i, all parent facts are already established, so the global result follows by induction
over node IDs/topological order.

CROWN and LiRPA (linear relaxations). CROWN tightens IBP by tracking affine bounds rather than pure intervals:
instead of only maintaining vi (x) ∈ [li , ui ] for each node, it maintains linear forms that bound each node as a function
of the input, e.g. a⊤ x + b ≤ vi (x) ≤ c⊤ x + d over the admissible input region. These affine bounds are obtained by
replacing nonlinear primitives with sound linear envelopes on the current pre-activation interval and propagating the
resulting affine forms through linear operators. For piecewise-linear activations such as ReLU, the envelope is given by
valid upper/lower lines on [l, u] (secant/tangent choices in the unstable regime l < 0 < u); for smooth activations (e.g.,
tanh, sigmoid), one uses tangent/secant bounds or other valid global/region-restricted linear relaxations, yielding a
strictly tighter enclosure whenever correlations between coordinates matter.
LiRPA is the unifying viewpoint: it treats bound propagation as computing and composing such linear relaxations
over general computational graphs (not just simple feedforward chains), subsuming CROWN- and DeepPoly-style
rules. Modern LiRPA implementations typically expose both (i) a forward pass that produces node wise affine
bounds and (ii) an objective-dependent backward/dual pass that tightens the bound for a specific linear objective
on the output (e.g., a robustness margin objective), since the best relaxation choices can depend on the downstream
objective. In T ORCH L EAN, our Lean based core mirrors this structure: we provide a proved-sound IBP layer and a
basic CROWN/LiRPA affine engine over the shared operator-tagged IR, with conservative fallbacks (e.g., deriving
constant affine bounds from IBP) when a specialized relaxation is not yet implemented, preserving soundness at the
cost of tightness.

  Example: ReLU linear relaxation (one neuron). Let z ∈ [l, u] and y = ReLU(z). A standard sound relaxation
  chooses linear bounds
                                        y ≥ λ L z + µL ,   y ≤ λU z + µ U ,
                                                                           u             ul
  with coefficients chosen so the lines bound ReLU on [l, u] (e.g., λU = u−l  , µU = − u−l   for the secant upper
  bound when l < 0 < u; and a valid lower bound selected from the admissible family in this regime). Propagating
  these envelopes yields affine bounds on downstream nodes and, ultimately, output enclosures.

                         Listing 20: Schematic ReLU relaxation coefficients used by CROWN.
structure ReluRelax where
  lowerSlope     : Array Float
  lowerIntercept : Array Float
  upperSlope     : Array Float
  upperIntercept : Array Float

def reluRelax (lo hi : Tensor Float s) : ReluRelax :=
  Id.run do
    let mut ls := #[]; let mut li := #[]
    let mut us := #[]; let mut ui := #[]
    for k in [:lo.numel] do
      let l := lo.data[k]!; let u := hi.data[k]!
      if 0.0 <= l then
        ls := ls.push 1.0; li := li.push 0.0
        us := us.push 1.0; ui := ui.push 0.0
      else if u <= 0.0 then
        ls := ls.push 0.0; li := li.push 0.0
        us := us.push 0.0; ui := ui.push 0.0
      else
        let secant := u / (u - l)
        let offset := -(l * u) / (u - l)
        -- Upper line is the secant. Lower line is chosen from


                                                             46
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                               A P REPRINT



         -- a sound family, possibly optimized by alpha-CROWN.
         us := us.push secant; ui := ui.push offset
         ls := ls.push 0.0;    li := li.push 0.0
     return { lowerSlope := ls, lowerIntercept := li,
              upperSlope := us, upperIntercept := ui }


α/β-CROWN as certificate-checked bound semantics (graph dialect). We implement an α/β-CROWN certificate
interface for the operator-tagged graph verifier dialect. Fix a compiled graph G (nodes i in topological order) and an
input box B. CROWN family bounds at each node are represented as affine enclosures over inputs: for a scalar node
value zi we enclose it by two affine functions of the input x,
                                                   zi (x) ∈ [Li (x), Ui (x)],
                                                  Li (x) = ⟨aL         L
                                                             i , x⟩ + bi ,
                                                  Ui (x) = ⟨aU         U
                                                             i , x⟩ + bi .

(For tensor nodes, the same form is applied componentwise.) Bounds are computed by a per-node step rule
                                         CrownStepNode? : S × i →
                                                          Option(AffBounds),
where S denotes the checker state (context plus parent bounds) and AffBounds abbreviates the pair of affine maps
above. This step extends α-CROWN by optionally incorporating β phase information at ReLU nodes: phase-fixed units
use exact linear behavior (slope 0 or 1), while unstable units fall back to standard CROWN/α-CROWN relaxations.

Certificate contents and the role of α and β. An α/β-CROWN certificate provides, for each node i: (i) an IBP
pre-activation interval [li , ui ] (a local box enclosure); (ii) affine bounds (lower and upper affine maps of the input); (iii)
α parameters for the unstable-ReLU lower relaxation; and (iv) an optional β phase vector for ReLU units. Intuitively,
α selects a member of a sound lower-envelope family in the unstable regime (l < 0 < u), while β encodes phase
constraints (active/inactive) that, when consistent with IBP, permit exact linear behavior on those units.

β phases and phase consistency. For a ReLU node with pre-activation z and post-activation y = ReLU(z), we
interpret β ∈ {−1, 0, 1} as
                                       
                                       −1 inactive (z ≤ 0),
                                  β≡     0 unstable (no constraint),
                                         1 active (0 ≤ z).
                                       

The step checks phase consistency against the IBP pre-activation interval [l, u]:
                                    Consistent(l, u, β) : ⇐⇒ (β = −1 ⇒ u ≤ 0)
                                                              ∧ (β = 1 ⇒ 0 ≤ l).
If consistent, inactive/active phases use exact linearization (slope 0 or 1). Unstable units (β = 0) fall back to the usual
CROWN upper relaxation and α-CROWN lower relaxation.

Phase-dependent ReLU relaxations. Write a linear bound as a pair (s, b) representing the function sz + b. Define
phase-dependent relaxations by
                                               
                                               (0, 0) if β = −1 and u ≤ 0,
                                    rβ (l, u) = (1, 0) if β = 1 and 0 ≤ l,
                                               
                                                 r(l, u) if β = 0,
                                               
                                               (0, 0)        if β = −1 and u ≤ 0,
                               rα,β (l, u, α) = (1, 0)        if β = 1 and 0 ≤ l,
                                               
                                                 rα (l, u, α) if β = 0.

Here r(l, u) is the standard CROWN triangular upper relaxation (secant in the crossing case), and rα (l, u, α) is the
α-CROWN lower relaxation family (with α ∈ [0, 1] used only when l < 0 < u). In the inactive/active cases the
relaxations reduce to the exact affine graphs of ReLU on the corresponding half-line.


                                                              47
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                              A P REPRINT




  Operator-level soundness (ReLU, β-aware). Let x ∈ [l, u] and assume Consistent(l, u, β). Let (s, b) = rβ (l, u) and
  (s, b) = rα,β (l, u, α) (with 0 ≤ α ≤ 1), the scalar relaxations satisfy:

                                       ReLU(x) ≤ s x + b and s x + b ≤ ReLU(x).




Certificate checking: replay-based producer/checker design. Certificate checking is the key mechanism for
obtaining tight bounds without enlarging the trusted computing base to include a complex optimizer. An external verifier
or solver acts purely as an untrusted producer: it searches for a certificate (bounds, affine envelopes, split structure, dual
variables) and serializes the result as a compact JSON artifact containing per-node IBP boxes, affine bound coefficients,
and optional per-node α and β data.
Lean then acts as the trusted checker: it parses the artifact, canonicalizes all numeric data to a fixed float grid, and recom-
putes each node’s bound via the same step semantics that defines [[G]], producing BiLean := CrownStepNode?(. . . , i) ∈
Option(AffBounds) for each node i in topological order. The checker accepts only if (i) provided bounds match the
recomputed bounds after canonicalization, (ii) parent bounds appear in topological order, and (iii) shapes and operator
tags are consistent with the IR. The external optimizer is never trusted: regardless of what search or heuristics it uses
internally, only the final artifact crosses the trust boundary, and every claim is independently replayed in Lean. This
reduces the trusted computing base to the IR denotation plus the small checker.




What the checker validates at each node. For each node i, the checker performs three checks in sequence. First, it
validates the schema: node i exists in the graph G, its declared input and output shapes match the IR typing, and
all required parent nodes have already been processed. Second, it validates local soundness: the certified bound
Bi is implied by the parent bounds and the OpKind-specific enclosure rule, confirmed by comparing Bi against the
recomputed BiLean after float-grid canonicalization. Third, after all nodes are processed, it validates goal reduction: the
target property (e.g., a robustness margin, a Lyapunov decrease condition, or a PINN residual bound) follows from
the certified output enclosure by a small, explicit Lean argument. If any check fails, the certificate is rejected and the
property is reported as unverified; the system never silently accepts a malformed artifact.




Certificate families. Certificates fall into two families:




• Node-wise enclosure certificates supply [li , ui ] and optionally affine forms Li (x), Ui (x) per node, sufficient to
  discharge an output-level property directly from the propagated enclosure. IBP and CROWN/LiRPA both fall here;
  the difference is whether bounds are intervals or affine functions of the input.




• Branch-and-bound leaf certificates partition the input region B into leaves, each with its own node wise certificate.
  The checker validates coverage, per-leaf soundness, and that the target property holds on every leaf; global validity
  follows by case analysis. This handles properties no single relaxation can certify, at the cost of a larger artifact and
  checking time linear in the number of leaves.


                                                             48
                                     T ORCH L EAN: Formalizing Neural Networks in Lean                                   A P REPRINT



    One ReLU neuron under α/β-CROWN.

    Let z ∈ [l, u] be the pre-activation and y = ReLU(z). The phase β ∈ {−1, 0, 1} encodes what the IBP interval tells us:
    provably off, provably on, or uncertain. Inactive (β=−1, u ≤ 0). The interval lies entirely in the non-positive half-line, so
    ReLU(z) = 0 everywhere on [l, u]. Both bounds are the exact zero line (sU , bU ) = (sL , bL ) = (0, 0); no relaxation gap
    is introduced. Active (β=1, 0 ≤ l). The interval lies entirely in the non-negative half-line, so ReLU(z) = z exactly. Both
    bounds are the identity (sU , bU ) = (sL , bL ) = (1, 0); again, zero gap and exact propagation.

    Unstable (β=0, l < 0 < u). The interval straddles zero and a linear relaxation is unavoidable. The upper bound is the
    CROWN secant connecting (l, 0) to (u, u), tight at both endpoints:
                                                           u                  −ul
                                                   sU =       ,        bU =       .
                                                          u−l                 u−l
    The lower bound is the α-CROWN family (sL , bL ) = (α, 0) with α ∈ [0, 1] chosen by the external optimizer to tighten the
    downstream objective. α=0 gives the trivial bound y ≥ 0; α=1 gives the identity y ≥ z, which is tightest when z is likely
    positive. Intermediate values trade local tightness against the global verification goal; in practice α is optimized by gradient
    ascent on the final bound, treating each neuron’s slope independently.

    Propagation. Affine forms compose exactly through linear layers using the W = W + − W − decomposition, where
    Wij+ = max(Wij , 0) and Wij− = max(−Wij , 0) route lower and upper input bounds to the correct output bound without
    case splits. Inactive and active neurons pass forms through without loss. Only unstable neurons accumulate gap, which
    shrinks as IBP intervals tighten. After processing all nodes in topological order, the output node carries certified bounds
    Lout (x), Uout (x) over the full input box B. The checker then discharges the target property—typically Lout,y (x) > Uout,k (x)
    for all k ̸= y—via a small explicit Lean argument whose only premises are the computed scalar bounds, keeping the trusted
    kernel minimal.


    What the Lean checker validates (conceptual checklist). Given a certificate and the IR graph:
    1. Schema + typing: node IDs exist; shapes match; per-node bound vectors have the right dimension.
    2. Local soundness per node: for each node i, the certified bound is implied by parent bounds and the OpKind-
       specific enclosure rule (interval rule or affine relaxation rule).
    3. Goal reduction: the final property (e.g., robustness margin, Lyapunov decrease) is derived from the certified
       output enclosure by a small, explicit argument in Lean (e.g., margin check or inequality chaining).
    4. Splitting (if present): each leaf region is within the root region; the claimed per-leaf bound is sound; and the
       set of leaves covers (or over-approximates) the target region according to the certificate’s declared semantics.


A concrete example (robustness margin). For a classifier with logits z(x) ∈ RK and a target label y, a standard
sufficient condition for certified ℓ∞ robustness on a region R is:
                                                           zy > max zk ,
                                                                   k̸=y

where (zk , zk ) are sound bounds on each logit over R. A certificate can therefore supply logit bounds (from
IBP/CROWN/LiRPA, optionally with splitting), and the Lean checker discharges robustness by checking the margin
inequality.

Certificate schemas (illustrative). Certificate-driven checking hinges on a stable schema: the artifact names the
graph and supplies node-indexed data. At a high level, a node wise enclosure certificate looks like:
{
    "graph_id": "...",
    "input_region": { ... },
    "bounds": {
      "node_id": { "lo": [...], "hi": [...] },
      ...
    }
}

More advanced artifacts may include affine coefficients, objectives, and branch-and-bound trees. The checker described
here focuses on validating the enclosure constraints needed to discharge the target theorem, rather than replaying the


                                                                  49
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                             A P REPRINT



optimizer’s full search/parameter-optimization internally. Planned extensions (e.g., richer dual-feasibility checks for
full solver internals) are described in Appendix E.3.

E.2   VNN-COMP / VNN-LIB interface (ONNX + VNNLIB)

VNN-COMP is an annual community competition designed to enable fair, objective comparison of neural network
verification tools by standardizing interfaces, benchmarks, and evaluation pipelines Brix et al. [2024], VNN-COMP
[2024]. VNN-COMP instances are packaged in standardized formats: networks are provided as ONNX models and
properties are specified in VNN-LIB, an SMT-LIB-style language that defines both syntax and semantics for satisfiability
queries over neural networks Brix et al. [2024], VNN-LIB [2021]. This regime is directly relevant to semantic drift:
most verifiers consume exported ONNX artifacts and interpret operator semantics outside the training framework, and
ONNX operator meaning is tied to explicit operator-set (opset) versioning. Our goal here is not to re-implement the
entire ONNX/VNN-LIB toolchain inside Lean, but to make the conversion boundary explicit and keep the trusted core
inside Lean.
Accordingly, we adopt a producer/checker workflow. A lightweight Python export step reads the ONNX network and
the VNN-LIB specification and emits a compact JSON bundle containing the network structure/weights (in a typed
graph form), the input region (typically an axis-aligned box), and the property matrices/constraints extracted from
VNN-LIB. Lean then compiles this bundle into our operator-tagged SSA/DAG IR and checks a sufficient UNSAT
condition by replaying IBP/CROWN style bounds against the shared IR semantics. For these suites we run the checker
under the fast runtime Float backend (binary64), since the objective is to demonstrate a semantic benchmarking
interface rather than Float32 deployment conformance.
The check we perform follows the standard sound-but-incomplete pattern used by bound-propagation verifiers: if the
propagated output enclosure implies that the VNN-LIB predicate cannot hold on the entire input region, we return safe
(UNSAT proved); otherwise we return unknown. Soundness is semantic: whenever Lean reports safe, the conclusion
is derived from the Lean denotation of the compiled IR, so the trusted computing base is the IR semantics plus the
small checker, with the export step treated as an explicit, auditable boundary.
Table 2 reports a small MNIST-FC slice under this interface. Lean IBP is conservative, while objective-dependent
CROWN refutes a subset of properties inside Lean. Importing optimized ReLU α slopes primarily improves runtime
rather than refutation count, suggesting that further tightness typically requires richer artifacts such as improved
intermediate bounds and/or splitting, consistent with broader lessons emphasized in VNN-COMP reports Brix et al.
[2024].
This interface follows the same certificate/checker style as the rest of T ORCH L EAN. The Lean runner replays native
IBP/CROWN style bounds on the shared IR; stronger untrusted producers (e.g., optimized α/β-CROWN bounds, split
certificates, or other solver artifacts) can be treated as certificate generators whose outputs are validated against the IR
semantics. This gives a concrete path toward theorem-prover participation in standardized verification benchmarks by
making semantics and checking the reference point, rather than re-implementing every optimizer heuristic in Lean Brix
et al. [2024], VNN-COMP [2024].

E.3   Case Studies

Certified robustness workflow (classifier). We illustrate the full verification pipeline on local certified robustness
for a classifier. Let f : Rd → RK denote the network’s logit function (so the predicted label is arg maxk fk (x)), and
fix a test input x0 with nominal label y = arg maxk fk (x0 ). Given a perturbation radius ε, we define the region of
interest R = {x : ∥x − x0 ∥∞ ≤ ε} (or an axis-aligned box that over-approximates it). Using IBP or CROWN/LiRPA,
we compute sound bounds (z k , z k ) such that fk (x) ∈ [z k , z k ] for all x ∈ R. IBP provides a fast interval enclosure
baseline, while CROWN/LiRPA tightens these bounds by propagating sound linear relaxations of nonlinearities and
(optionally) using objective-dependent back-substitution.

  Theorem E.3: Logit-margin robustness certificate

  Let f : Rd → RK be a classifier and R an input region. Assume we have sound logit bounds for all classes: for
  each k and all x ∈ R, fk (x) ∈ [z k , z k ]. If
                                                  z y > max z k ,
                                                             k̸=y

  then arg maxk fk (x) = y for all x ∈ R (i.e., the prediction is certified ℓ∞ -robust on R).



                                                            50
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                             A P REPRINT



How the certificate is checked. The certificate checking step is deliberately small and semantic: the checker validates
that the reported bounds are a sound enclosure of the IR semantics on R (shape-consistent, op-consistent, and region-
consistent), and then applies the margin lemma above to conclude label invariance. This is exactly the “infinite-to-finite”
reduction that makes bound propagation useful: instead of enumerating all x ∈ R, we certify robustness by a finite
set of inequalities on the computed output enclosure. (This margin-style condition is standard in certified robustness
pipelines.)
Structure of the example.

1. Model definition: define the classifier once in T ORCH L EAN.
2. Lowering: lower the same program to the shared operator-tagged SSA/DAG IR (the semantic target).
3. Bounding: run IBP or CROWN/LiRPA on the IR to obtain logit enclosures over R.
4. Checking: verify the enclosure constraints and discharge robustness via Lemma E.3.

The final claim is a Lean theorem about the denotation of the shared IR, not a post-hoc interpretation of a tool output:
external verifiers may produce bounds, but Lean checks that those bounds imply the semantic property of interest on the
executed artifact.
Physics-Informed Neural Networks (PINNs). PINNs enforce physics by penalizing a PDE residual built from a
neural field uθ and its derivatives. We fix (i) a residual operator R (e.g., for Burgers/heat-type equations), (ii) a domain
Ω, and (iii) a trained network uθ , and aim to certify a uniform residual bound supx∈Ω |R(uθ )(x)| ≤ ε. This is the
standard PINN correctness goal: the learned model approximately satisfies the governing PDE across the domain. The
verification step is derivative-dependent, so we combine (a) a proved first-order reverse-mode result that anchors the
meaning of ∇uθ to the graph semantics (under the usual smoothness/pointwise side conditions), with (b) derivative-
aware bound propagation on the shared operator-tagged graph that produces interval enclosures for uθ and the specific
derivatives appearing in R (including second derivatives for the low-dimensional smooth-operator subset used in the
demos). We do not obtain u′′ by differentiating the backward-pass graph; instead, we bound the required derivatives
directly via specialized bound-propagation passes on the forward graph, and then combine these enclosures to conclude
the residual inequality.
  Theorem E.4: Residual certificate pattern (PINNs)

  Let Ω be a domain and suppose we have sound interval enclosures on Ω for every term that appears in the residual
  R(uθ ) (e.g., bounds on uθ , ∂uθ /∂t, ∂uθ /∂x, ∂ 2 uθ /∂x2 ). If these enclosures imply |R(uθ )(x)| ≤ ε for all x ∈ Ω,
  then the PDE residual of uθ is certified within tolerance ε on Ω.

                  Listing 21: Schematic residual checker for a one-dimensional Burgers-style PINN.
structure DerivBounds where
  u    : Box scalar
  ut   : Box scalar
  ux   : Box scalar
  uxx : Box scalar

def burgersResidual (nu : Float) (b : DerivBounds) : Box scalar :=
  -- R(u) = u_t + u * u_x - nu * u_xx
  b.ut + intervalMul b.u b.ux - scaleBox nu b.uxx

def checkResidual? (nu eps : Float) (b : DerivBounds) : Bool :=
  let r := burgersResidual nu b
  r.lo >= -eps && r.hi <= eps

The checker separates two obligations. First, the derivative bound passes produce sound boxes for u, ut , ux , and uxx
over the verification region. Second, ordinary interval arithmetic combines those boxes according to the PDE residual
formula. This separation keeps the theorem statement short: any future residual operator can reuse the same pattern
once its derivative boxes and algebraic interval rules are available.
Neural controller (Lyapunov-style safety/stability). We also evaluate a two stage controller-verification workflow
common in learning-enabled control: Stage 1 (training/search) proposes a feedback controller u(x) together with a
Lyapunov candidate V (x); Stage 2 (certification) proves region-based inequalities that imply safety/stability (e.g.,
V (x) ≥ 0 and V̇ (x) ≤ −ρ(∥x∥) on a region). This aligns with recent neural-control verification pipelines that


                                                            51
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                          A P REPRINT



use bound propagation and α/β-CROWN-style tooling to certify Lyapunov conditions. In our setting, we compute
enclosures for V (x) and V̇ (x) = ∇V (x) · f (x, u(x)) over the region (with ∇V grounded by the same autograd
semantics as execution), and the final claim is discharged by checking the resulting inequalities as a theorem about the
shared IR denotation.
  Theorem E.5: Lyapunov certificate pattern (region-based)

  Let V be a candidate Lyapunov function for a closed-loop system ẋ = f (x, u(x)) on a region R. If certified
  bounds over R establish V (x) ≥ 0 (and V (x) = 0 only at the equilibrium) and V̇ (x) ≤ 0 (or a strict decrease
  condition) for all x ∈ R, then the corresponding safety/stability property holds on R under the chosen Lyapunov
  criterion.

                      Listing 22: Schematic Lyapunov inequality check over a certified region.
structure LyapBounds where
  Vlo   : Float
  Vhi   : Float
  VdotLo : Float
  VdotHi : Float

def checkLyapunovBox (b : LyapBounds) (rho : Float) : Bool :=
  -- Typical sufficient obligations on a box away from the equilibrium.
  (0.0 <= b.Vlo) && (b.VdotHi <= -rho)

def checkPartition (boxes : List LyapBounds) (rho : Float) : Bool :=
  boxes.all (fun b => checkLyapunovBox b rho)

This is the finite reduction used by the controller case study. The analytic Lyapunov criterion quantifies over a region;
the certificate partitions the region into finitely many boxes and provides bounds for V and V̇ on each box. Lean checks
the per-box inequalities and the coverage assumptions recorded in the certificate schema.
Hopfield networks and global dynamics (complementary case study). Hopfield networks are recurrent, energy-based
models whose core guarantees are global dynamical statements: rather than certifying a local property around one
input, we prove properties of entire trajectories generated by repeatedly applying an update rule (e.g., asynchronous
coordinate updates). Classically, one defines an energy/Lyapunov functional E(x) and proves that each update step
does not increase E; because the state space is finite, monotone energy then implies convergence to a fixed point (an
attractor) under standard symmetry and zero-diagonal conditions.
In the recent paper, Formalized Hopfield Networks and Boltzmann Machines Cipollina et al. [2025], the authors develop
a Lean 4 formalization aimed squarely at such global properties like convergence for deterministic Hopfield dynamics
and ergodicity for stochastic Boltzmann machines. They emphasize that many ML formalizations mirror modern
execution frameworks (sequential layers or DAG-style computational graphs), which is convenient for feedforward
computation but does not directly express recurrent update semantics; because their focus is convergence/ergodicity of
recurrent models, they adopt a graph-based dynamical-systems perspective (directed graphs/Markov kernels) integrated
with mathlib/PhysLean [The mathlib Community, 2020]. Their discussion highlights a real tradeoff: representations
optimized for feedforward dataflow can require extra machinery (unfolding or fixed-point semantics) to model recurrence
faithfully.
Our treatment is complementary: we express the Hopfield update operator and energy functional inside the same
typed tensor/program semantics used throughout T ORCH L EAN, and we prove the standard monotone-energy and
convergence-style results by reasoning about an explicit state-transition map (iteration) plus a Lyapunov decrease
argument. These results show that an SSA/DAG semantic core for computation can still support proofs about global
dynamical behavior.
  Theorem E.6: Hopfield energy decrease and convergence (informal template)

  Let x ∈ {−1, +1}n be the network state, with symmetric weights W = W ⊤ and zero diagonal, and thresholds θ.
  Define the energy
                                            E(x) = − 21 x⊤ W x + θ⊤ x.
  Consider asynchronous updates that flip a single coordinate xi according to the sign of its local field (W x − θ)i
  (with a fixed tie-handling convention). Then each update step satisfies E(xt+1 ) ≤ E(xt ), and hence any trajectory



                                                           52
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                           A P REPRINT



    produced by repeatedly applying the update rule reaches a fixed point in finitely many steps (a local minimum of
    E under the update dynamics).


F     Universal Approximation Theorems

Universal approximation (real-valued). A universal approximation theorem (UAT) formalizes the idea that a simple
network class can approximate any continuous function on a compact domain to arbitrary accuracy. Classic results
show that single-hidden-layer networks are dense in C(K) for compact K ⊆ Rd under mild activation assumptions
Cybenko [1989], Hornik [1991]; more recent work characterizes approximation rates for ReLU networks Yarotsky
[2017]. In T ORCH L EAN, we mechanize a standard real-valued ReLU UAT on compact domains and then specialize it
to boxes such as [−1, 1]d .

    Theorem F.1: ReLU universal approximation on compact sets

    For every compact K ⊆ Rd , every continuous f : K → R, and every ε > 0, there exist a width m and a
    single-hidden-layer ReLU network Nθ such that
                                               sup |Nθ (x) − f (x)| < ε.
                                               x∈K



F.1    Float32-execution Soundness

Why the Float32 setting is harder. Real-valued UATs reason about exact arithmetic, whereas deployed models
run under finite-precision float semantics. In this setting, even the “target function” must be interpreted carefully: the
executed program computes a rounded function, and abstract-interpretation semantics (e.g., intervals) must account for
rounding and finite-range effects. Recent work proves a floating-point analog of interval universal approximation (IUA),
showing that floating-point networks can capture the direct image map of a suitably rounded target function under
interval semantics Hwang et al. [2025]. In contrast, our goal in T ORCH L EAN is to build a compositional, checkable
foundation that supports practical verification workflows under explicit Float32 semantics, without claiming the full
“exact-hull direct image” property for arbitrary networks.
Our claims. We do not claim a full IUA theorem of the form “the interval semantics returns the exact output-range hull
for every input box” for arbitrary networks under Float32 execution. Instead, we mechanize three ingredients that are
sufficient for approximation-style arguments and verification pipelines:

• Executable Float32 semantics in the prover. An executable IEEE-754 binary32 model (IEEE32Exec) that gives a
  precise internal meaning to “Float32 execution” (including corner cases) for full demos and checking.
• Sound interval evaluation on a supported fragment. A theorem-ready specification of interval semantics and a
  proved-sound interval evaluator for a small ReLU-MLP fragment, enabling certified enclosures needed by robust-
  ness/PINN/controller checks.
• Error decomposition for Float32-execution approximation. Theorem templates that bound execution error by
  an explicit sum of terms: (real approximation error) + (parameter/representation error, e.g. quantization) + (IEEE
  rounding/execution error), under explicit finiteness/no-NaN/no-Inf hypotheses.

Note: Where Hwang et al. [2025] targets a floating-point IUA result that exactly matches the interval direct image
map of a rounded target function, our development emphasizes compositional error bounds and sound enclosures that
integrate cleanly with certificate checking and full verification workflows, without requiring the full exact-hull IUA
guarantee for all networks.

Notation for the theorems below. Let F32 denote IEEE-style Float32 values (excluding NaNs/Infs when we explicitly
assume finite execution), and let toReal : F32 → R interpret a finite float as a real number. A box B is an axis-aligned
product of Float32 intervals (a valid element of the interval domain), and γ(B) ⊆ Fd32 denotes its concretization
(the set of Float32 points represented by B). We write ν : Fd32 → F32 for point semantics (Float32 execution) and
ν ♯ : Boxd32 → Box32 for interval semantics (abstract interpretation over boxes).



                                                           53
                                  T ORCH L EAN: Formalizing Neural Networks in Lean                           A P REPRINT



  Theorem F.2: Exact-hull specification (Float32 interval semantics)

    Fix d ∈ N and a NaN-free target function fˆ : Fd32 → F32 . Assume a point semantics ν and an interval semantics
    ν ♯ such that ν ♯ (B) is a box output for any valid input box B. We say ν ♯ returns the exact hull of fˆ on B if, for
    every valid box B ⊆ [−1, 1]d , there exist witnesses m, M ∈ F32 satisfying:
    1. (Witnessed extrema) m and M witness the range of fˆ on the concretization: m ≤ fˆ(x) ≤ M for all x ∈ γ(B),
        and there exist xm , xM ∈ γ(B) such that fˆ(xm ) = m and fˆ(xM ) = M .
    2. (Hull equality) the concretization of the abstract output box is exactly the interval hull:
                                        γ(ν ♯ (B)) = { y ∈ F32 | m ≤ y ∧ y ≤ M }.

Why witnesses? This avoids committing to a particular implementation of float min/max at ties or NaN boundaries: the
statement only requires existence of range witnesses and equality to the induced hull, which is the robust “Eq.(14)-style”
specification used in float-IUA work.
  Theorem F.3: From real approximation to Float32-execution error (1D hinge template)

    Let f : [a, b] → R be a real target function and let hR be a hinge-style 1D network (or piecewise-linear ReLU
    template) parameterized by θ. Assume a real approximation bound
                                             sup |f (x) − hR (x; θ)| ≤ εapprox .
                                            x∈[a,b]

    Let h32 denote the corresponding Float32-executed program (same structure/parameters, executed in Float32) and
    assume finite execution on [a, b] (no NaN/Inf and no overflow-to-Inf along the evaluation). Then for every real
    input x ∈ [a, b] and any Float32 encoding x32 of x,
                                  f (x) − toReal(h32 (x32 ; θ)) ≤ εapprox + εexec (x),
  where εexec (x) is an explicit rounding/execution envelope for this template on [a, b] (e.g., a compositional bound
  obtained by summing per-primitive rounding terms under the finiteness hypothesis).

  Theorem F.4: Three-term Float32-execution error decomposition (single-hidden-layer ReLU MLP)

    Let f : K → R be a target function on a domain K ⊆ Rd and let NR (·; θR ) be a real single-hidden-layer ReLU
    MLP. Let N32 (·; θ32 ) be its Float32-executed counterpart with Float32 parameters θ32 , and let θR′ := toReal(θ32 )
    be the real interpretation of those float parameters. Assume:
    1. (Real approximation)
                                                 sup |f (x) − NR (x; θR )| ≤ εUAT
                                               x∈K

    2. (Parameter/representation gap)
                                           sup |NR (x; θR ) − NR (x; θR′ )| ≤ εparam
                                           x∈K

    3. (Float32 execution gap) for all admissible inputs (under a finiteness hypothesis),
                                        |NR (x; θR′ ) − toReal(N32 (x32 ; θ32 ))| ≤ εexec
  Then for all x ∈ K (with any Float32 encoding x32 ), where any input-encoding/quantization error can be bounded
  separately and added to the right-hand side (or folded into εexec ),
                                f (x) − toReal(N32 (x32 ; θ32 )) ≤ εUAT + εparam + εexec

G      Limitations and Discussion
Limitations and near-term roadmap. Execution vs. training at scale. T ORCH L EAN is semantic infrastructure, not
a throughput-optimized training stack. Lean execution and the optional CUDA backend prioritize a machine-checked
semantic link between (i) the program users write, (ii) the IR graph we reason about, and (iii) the artifacts we check,
rather than matching industrial training throughput. The CUDA path accelerates selected kernels and examples behind


                                                             54
                                 T ORCH L EAN: Formalizing Neural Networks in Lean                            A P REPRINT



explicit native runtime contracts; large-scale training can also be performed externally and imported as weights/structure,
with Lean used for semantic checking, certificate validation, and proof-carrying artifacts. Scaling the native backend,
kernel fusion, and internal bound optimization remains an engineering extension of the same semantic design.
Verification scope and certificates. Our native verification layer covers a curated IR fragment with a proved-sound IBP
core and a CROWN/LiRPA style affine engine, together with certificate checking infrastructure for externally produced
bound artifacts. We support an α/β-CROWN certificate dialect for the graph-based verifier: certificates may supply
IBP pre-activation boxes, affine bounds, α parameters for unstable-ReLU lower relaxations, and optional β phase
vectors that are checked for consistency and then replayed by the Lean step semantics. When strongest current tightness
is required beyond this interface, we rely on external optimizers as untrusted producers and check their exported
bounds/leaf certificates against the shared IR semantics, keeping the trusted computing base to the Lean checker plus
the IR denotation. Extending the checker to validate additional solver families (e.g., richer dual-feasibility conditions,
cutting-plane certificates, or SDP-based relaxations) is left to future extensions; Appendix E and Appendix E.3 document
the present schemas and extension points.
Float32 trust boundary (the “hardware gap”). We separate (i) real-valued reference semantics, (ii) proof level
rounding-on-R models (FP32/NF) for compositional error envelopes, and (iii) an executable bit-level Float32 kernel
(IEEE32Exec). What remains is a target-specific refinement from a deployed Float32 toolchain to the executable
model: one must fix a deployment configuration (rounding mode, denormal policy, contraction/ reassociation, and
reduction order constraints) and then discharge a conformance interface (by proof or explicit validation). Appendix D.1
summarizes the internal refinements we prove and the remaining target-level obligations.
Deployment and code generation. Inside Lean, we close the training and verification semantic gap by making the
operator-tagged IR the single semantic target. Deploying a verified model on an embedded target still introduces
a translation step: either run a small IR interpreter on-device, or generate C/Rust code from the IR and connect its
behavior back to the Lean denotation. Lean’s compilation pipeline and runtime already support efficient compiled code,
and there are emerging toolchains that bridge verified Lean reasoning with real systems languages (e.g., Rust-to-Lean
verification pipelines), suggesting concrete paths toward deployment pipelines.




                                                            55
