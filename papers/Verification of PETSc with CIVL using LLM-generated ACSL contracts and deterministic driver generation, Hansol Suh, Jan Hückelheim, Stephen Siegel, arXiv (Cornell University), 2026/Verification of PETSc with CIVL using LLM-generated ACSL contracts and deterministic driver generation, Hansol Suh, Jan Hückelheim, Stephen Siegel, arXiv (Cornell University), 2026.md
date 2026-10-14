                                               Verification of PETSc with CIVL using
                                            LLM-generated ACSL contracts and deterministic
                                                           driver generation
                                                                                 Hansol Suh∗ , Jan Hückelheim∗ , Stephen Siegel†
                                                                                ∗ Argonne National Laboratory, Lemont, Illinois, USA

                                                                                            {hsuh,jhueckelheim}@anl.gov
                                                                                ORCID: 0000-0001-8875-4074; 0000-0003-3479-6361
                                                                                 † University of Delaware, Newark, Delaware, USA

                                                                                                   siegel@udel.edu
arXiv:2609.31687v1 [cs.CL] 16 Sep 2026




                                                                                         Corresponding author: Hansol Suh



                                            Abstract—Parallel numerical libraries such as PETSc are             silently compromise the correctness of many other functions
                                         widely used in science and engineering applications where wrong        that use them. Formal verification can help detect bugs that
                                         results can have costly consequences. Despite this, numerical          occur only in corner cases and provide additional confidence
                                         libraries are rarely formally verified. One of the challenges is the
                                         need for an expert to hand-write a specification and manually          in the computed results. With the CIVL model checker [2], one
                                         apply a verification tool, often requiring the development of          writes, for a given function, a driver that constructs symbolic
                                         a harness or driver, all of which can contain additional bugs          inputs, runs a CIVL-compatible port of the implementation,
                                         that lead to false positives or false negatives during verification.   and compares the result against a reference model; CIVL then
                                         With recent advancements in large language models (LLMs),              checks that the two agree over all inputs within bounds. Here,
                                         it is tempting to generate such drivers and reference models
                                         automatically, but one-shot generation based on a simple prompt        a CIVL-compatible port preserves the implementation paths
                                         is brittle and leads to additional unverified code that needs to       being verified while removing unsupported features, such as
                                         be audited. In this paper, we present an approach to use LLMs          sparse storage.
                                         in a limited setting to generate a small, human-certifiable ACSL          In the past, CIVL has been used to verify parts of PETSc’s
                                         contract from the function’s documentation, combined with a            vector module [3], and it found two previously undiscovered
                                         deterministic toolchain that supports a restricted ACSL profile
                                         and generates a driver that uses the CIVL verifier to check            bugs. That result required hand-written drivers, reference mod-
                                         the implementation against the contract and, when available, an        els, and supporting artifacts for each function, which does not
                                         existing reference model. We demonstrate the pipeline end-to-end       scale to a code base the size of PETSc.
                                         on three PETSc functions: MatAXPY (reference model already                To address this scaling problem, large language mod-
                                         exists), MatAYPX (no reference model, so the certified contract is     els (LLMs) are an obvious temptation: PETSc has exten-
                                         the sole oracle), and the non-compressing mode of MatFilter
                                         (no reference model, with more complex, conditional behavior).         sive documentation, which makes one-shot documentation-
                                         With this pipeline, we were able to discover a bug in PETSc’s          to-driver generation via LLM plausible. However, such an
                                         MatAYPX function that was previously undiscovered and had              LLM-generated driver is itself unverified code. Auditing the
                                         been present in the code since 1997.                                   symbolic inputs, MPI setup, and oracle logic still requires
                                            Index Terms—PETSc, CIVL, model checking, formal verifica-           the same domain knowledge needed to write a driver, and an
                                         tion, ACSL contracts, large language models, high-performance
                                         computing                                                              unaudited driver that passes verification is worse than no driver
                                                                                                                at all, as it results in misplaced confidence in the underlying
                                                                                                                code.
                                                                I. I NTRODUCTION
                                                                                                                   To fully exploit the scalability of the LLM while mini-
                                            The Portable, Extensible Toolkit for Scientific Computation         mizing the LLM-written code that a human must manually
                                         (PETSc) [1] is a widely used numerical library in com-                 inspect, we separate the stochastic output of the LLM from
                                         putational science, supplying parallel linear and nonlinear            the parts that can be produced deterministically. Instead of
                                         solvers, ODE integrators, and optimization routines on which           asking the LLM to emit a full driver, we ask it only for a
                                         application codes in domains as varied as aerodynamics,                short formal contract, written in a restricted ACSL profile,
                                         combustion, cardiology, and subsurface flow are built. Because         derived from the function’s documentation. A human reviewer
                                         many high-consequence applications depend on PETSc, it is              with PETSc expertise then validates the contract using the
                                         tested extensively: its continuous-integration pipelines exercise      documentation, API semantics, and implementation where
                                         tens of thousands of tests on every code change. Yet even high-        necessary, recording the rationale for any decisions not settled
                                         coverage test suites can miss subtle defects, and a bug in a           by the documentation. Only a certified contract proceeds. To
                                         core module, such as the vector (Vec) or matrix (Mat), may             turn the certified contract into an executable driver without
reintroducing unverified code, we present acsl2civl, a                                  PETSc documentation and prototype
deterministic tool that translates the certified contract into a
CIVL verification driver. This approach is less automated than
                                                                                               Stage 1: LLM (untrusted)
generating the driver directly from the specification via an                                      generate a candidate
LLM, but it concentrates human review on a short contract                                        PETSc–ACSL contract
instead of requiring the reviewer to audit an entire generated                                 using the supported ACSL
                                                                                             and custom PETSc predicates
driver. This paper contributes:
                                                                                                               candidate contract
   1) the three-stage pipeline (LLM → manual review →
                                                                                        Stage 2: PETSc-aware human review
       deterministic compiler) to turn natural-language docu-                                   check documented be-
       mentation into a machine-verifiable driver (§II);                                      havior; resolve and record
   2) a restricted PETSc-ACSL profile over a dense logical                                     documentation gaps us-
                                                                                                 ing relevant evidence
       image of PETSc objects (§II-A), and a manual review
       step for evolving the profile (§III-B);
   3) acsl2civl, a deterministic compiler that generates                                no
                                                                                                         certified?
       a CIVL driver from the human-certified contract. The
       driver checks the implementation against the con-                                                       yes: certified contract
       tract’s ACSL formulas and, when available, also checks
       agreement with a separately authored reference model                              Stage 3: acsl2civl (deterministic)
                                                                                             parse and check supported
       (§II-D);                                                                                constructs; derive cases;
   4) an evaluation on three operations: (i) MatAXPY, verified                                  generate CIVL driver(s)
       against a specification and reference model (§III-A);                                                   generated driver(s)
       (ii) MatAYPX, verified only against a LLM-generated                                           civl verify
       and human-checked contract and exposing the afore-                                      check the CIVL-compatible
       mentioned PETSc bug (§III-C); and (iii) the non-                                            PETSc port against
                                                                                             contract assertions and, when
       compressing mode of MatFilter, which demonstrates                                      available, a reference model
       a more complicated postcondition using conditionals
       (§III-D).
                                                                                                 verified within bounds
A. Background on the CIVL model checker                                                          or     counterexample

   CIVL [2] is a symbolic execution and model checking
                                                                    Fig. 1. The three-stage pipeline: LLM-generated contract, human certification,
framework for CIVL-C, a superset of C with first-class concur-      and deterministic CIVL driver generation.
rency and verification primitives, with faithful semantics for
a subset of MPI [4]. Given a program with symbolic inputs,
CIVL explores its state space in order to verify properties         behind opaque handles and dynamic dispatch. These features
over all interleavings, within user-specified bounds on inputs      make PETSc a valuable verification target, but they also
and the number of processes. It discharges assertions with          make direct verification difficult: a driver must construct legal
automated theorem provers, reporting either a counterexample        symbolic objects, respect collective semantics, and observe
trace or that the chosen fault classes are absent on all exe-       the logical mathematical object rather than incidental storage
cutions. The line of work behind CIVL includes verification         layout.
of collective operations [5] and contract-based verification of        This work builds on an existing CIVL–PETSc verification
MPI programs [6].                                                   infrastructure [3]. That infrastructure provides an abstract
   To verify a library function f with CIVL, one writes a           CIVL model of PETSc Vec/Mat objects and, for many op-
verification driver. The driver constructs appropriate symbolic     erations, three hand-written per-function artifacts: a reference
inputs for f , and then calls both the actual implementation of     model <Func>_spec, a CIVL-compilable port <Func>.c
f and a trusted reference model for f , when available. The         of the PETSc interface function, and a driver that executes
driver then compares the two results symbolically, reporting        the port and checks its result against the reference model.
an error if it fails to prove they are equivalent. The driver and   Our pipeline keeps the CIVL–PETSc object model and PETSc
the reference model have, until now, been written by hand for       porting discipline, but replaces the hand-written driver with
every function.                                                     one generated deterministically from a human-certified con-
                                                                    tract. When no reference model exists, as for MatAYPX, the
B. PETSc                                                            certified contract becomes the sole oracle checked by CIVL
   PETSc [1] is a widely used open-source library for large-        (§II-D).
scale scientific computing on parallel, distributed-memory
systems. Its solvers and time integrators are built on core ab-                                  II. A PPROACH
stractions such as Vec and Mat, whose implementations hide             One-shot LLM driver generation bundles three distinct
distributed storage, assembly state, and type-specific kernels      tasks: (i) identifying the behavior documented by a PETSc
manual page, (ii) encoding that behavior in a symbolic con-                                     TABLE I
tract, and (iii) engineering the symbolic-MPI harness needed           C USTOM PETS C PREDICATES FOR A C S L 2 C I V L . T HESE UNESCAPED
                                                                              NAMES EXTEND THE SUPPORTED ACSL FRAGMENT.
to check it. The first two require language and modeling
judgment, where using an LLM can be useful. The third is             Symbol                   Stipulated meaning in the PETSc
mechanical and should be deterministic: when generated by                                     model
an LLM, it is also the hardest to audit, because a driver mixes      valid_mat(M)             M is a matrix handle whose modeled di-
object construction, case splitting, frame checks, reference-                                 mensions, communicator, assembly state,
model calls, and CIVL-specific plumbing. Our design principle                                 and dense global image are consistent.
is therefore to separate the stochastic step from the determin-      valid_vec(v)             v is a vector handle whose modeled size,
istic ones, joined by manual inspection of a small, reviewable                                communicator, assembly state, and dense
artifact (Figure 1):                                                                          global image are consistent.
   1) Stage 1 (stochastic, LLM): the LLM turns PETSc                 separated_mat(A,         A and B are distinct matrix objects with
       documentation into a small candidate contract in the          B)                       disjoint modeled storage.
       fixed PETSc-ACSL profile (§II-A); this contract is the        separated_vec(x,         x and y are distinct vector objects with
       only artifact the LLM generates.                              y)                       disjoint modeled storage.
   2) Stage 2 (human certification): a PETSc-aware expert            same_comm(x,y)           The modeled PETSc objects use the same
       checks the candidate against the documentation and,                                    MPI communicator.
       if necessary, resolves gaps in the documentation by           assembled(x)             The modeled object has no pending as-
       reviewing the API and implementation, or asking the                                    sembly updates.
       PETSc developers for clarification; failure returns the       logically_               Corresponds    to    PETSc’s   Petsc
       contract to Stage 1, and certification sends it to Stage 3.   collective(x,a)          ValidLogicalCollective{Real,
   3) Stage 3 (deterministic, no LLM): acsl2civl trans-                                       Scalar}. All ranks in x’s communicator
       lates the certified contract into CIVL driver(s) or rejects                            provide the same value for a.
       it if it contains unsupported constructs.                     scalar_conj(z)           The complex conjugate of z; the identity
   CIVL then checks each generated driver against the CIVL-                                   for real PetscScalar.
compilable port of the PETSc implementation for the function
being verified. This division limits LLM output to the reviewed
contract; every step afterwards is performed by deterministic,       s as an escape hatch, §III-B); terms over \old, \forall
reviewable tools.                                                    , scalar arithmetic, \abs, ordered comparisons, and condi-
                                                                     tional expressions; PetscScalar, PetscReal, and pinned
A. Symbolic representation: a PETSc contract language
                                                                     PetscBool parameters; and object (in)equality (== / !=).
   We express contracts using a supported fragment of                Reductions (\sum, norms, dot products) are not yet supported.
ACSL [7], [8], a behavioral specification language for C that
provides clauses such as requires, assigns, and ensures.
                                                                     B. Stage 1: from documentation to a candidate contract
We augment this fragment with the custom PETSc predicates
listed in Table I. acsl2civl interprets these extensions and            Stage 1 uses the LLM to turn a PETSc manual page into
translates the contracts into CIVL-C driver code. ACSL was           a candidate contract in the profile of §II-A. This contract is
chosen for three reasons: (i) ACSL allows the formulation of         the only artifact the LLM authors, and the LLM does not
postconditions in a format understandable by the subsequent          see the PETSc source code repository. This is done to avoid
verification pipeline, (ii) ACSL can be naturally added to C,        the generation of a contract that is influenced by (possibly
which is the language PETSc is written in and that CIVL              erroneous) implementation choices. The LLM only views the
understands, so contracts can sit in documentation comments          function’s documentation, the PETSc function prototype, and
beside the PETSc prototypes they describe and remain read-           the profile definition of §II-A. We acknowledge that, due to
able to both the human reviewer and the remaining toolchain,         the popularity of PETSc, the LLM may nevertheless contain
(iii) ACSL leaves a path to Frama-C-based mechanical checks          knowledge of PETSc source code, but we postulate that
as future work (§V). While proof assistants such as Lean [9]         excluding the source code from the context and prompt will
or Rocq [10] may also be useful, the authors believe it is           nevertheless increase the likelihood of obtaining specifications
preferable to keep the contract easily accessible to PETSc           that are grounded in the natural-language documentation as
developers, who are accustomed to C.                                 opposed to the implementation.
   For verification, we model each distributed PETSc vector             The documentation supplies the behavioral content the
or matrix as a dense, row-major global image, regardless             contract is meant to formalize: the operation’s intended effect
of its actual storage format, written M->data[k] for 0 <=            and the documented parameter semantics. When the documen-
k < M->rmap->N * M->cmap->N. Distributed storage or MPI              tation does not specify behavior for a case, such as parameter
communication are abstracted away.                                   aliasing, the contract must make that gap and any resulting
   The supported ACSL fragment is deliberately small:                assumption explicit. Stage 1 may be repeated multiple times
requires / assigns / ensures clauses (plus named behavior            based on feedback from Stages 2 and 3.
   The Stage 1 prompt is a self-contained Markdown document                                    TABLE II
(§A). It contains the current profile definition, a generic           T RANSLATION FROM SUPPORTED CONTRACT CONSTRUCTS TO CIVL-C
                                                                                             DRIVER CODE .
output skeleton, and the target function’s documentation and
prototype. The profile evolves between runs as Stage 3 gains         Contract construct       Generated driver behavior
new capabilities. Each prompt is piped to Claude Code using
                                                                     Supported requires       constrains symbolic dimensions or pa-
Claude Opus 4.8, with session persistence, external setting          equality                 rameter values during driver construction.
sources, and tools disabled.1 The CLI therefore has no repos-
itory access. For each run, the complete prompt and resulting        Custom PETSc predi-      emits corresponding CIVL assumptions,
                                                                     cate                     construction constraints, or generated
contract are archived with the artifact; any corrections made                                 cases.
during Stage 2 human review are reflected in the certified
                                                                     assigns over mod-        records pre-call values outside the
contract.                                                            eled data                assignable set and checks that those
                                                                                              values remain unchanged after the call.
C. Stage 2: human-certification
                                                                     Supported ensures        translated into elementwise CIVL asser-
   A PETSc-aware expert reviews the candidate contract                                        tions over the gathered global image; \
against the documentation and relevant API and implementa-                                    old terms refer to recorded pre-call val-
                                                                                              ues.
tion. Behavioral formulas must match explicit documentation;
where the documentation is unclear, the reviewer must make
and record a justified policy decision rather than hiding it as an
unstated assumption. Relevant preconditions outside the profile      the driver compares the implementation result with the ref-
are likewise recorded. For example, MatAXPY(Y, a, X,                 erence model result, and separately checks the contract-
str)’s manpage does not mention aliasing. A human reviewer           derived assertions. No reference models exist for MatAYPX
can inspect the documentation of similar functions (such as          or MatFilter, so their contract-derived assertions provide
MatAYPX), determine that aliasing is typically allowed and           the correctness criteria. Table II summarizes how supported
handled correctly, and record the decision to admit X ==             contract constructs are translated into these checks.
Y as an allowable input. The documentation also marks the            E. Trust boundaries
operation logically collective, so the certified contract records
                                                                        For a generated verification driver, the key question is which
that obligation as requires logically_collective(Y, a).
                                                                     artifacts are trusted and which are checked. The trusted pieces
Rejected contracts are revised or regenerated before another
                                                                     are (i) CIVL itself, (ii) the hand-written CIVL–PETSc module,
review pass; accepted contracts are stamped CERTIFIED with
                                                                     (iii) CIVL-compatible ports <Func>.c, whose fidelity to
a revision number, date, and certifier, then released to Stage 3.
                                                                     PETSc source is trusted, and (iv) acsl2civl. The LLM
   Certification is complemented by the mechanical profile
                                                                     is untrusted. The human-certified contract is trusted to state
checks performed by acsl2civl before driver generation
                                                                     the intended behavior. With --contract-assert, CIVL
(§II-D) to enforce syntactic well-formedness.
                                                                     checks both the contract and the reference model. With
                                                                     --no-spec, as for MatAYPX, the contract postconditions
D. Stage 3: deterministic translation to a CIVL driver
                                                                     and frame conditions are the only correctness checks.
   Stage 3 is implemented by acsl2civl (written in Python
using the Lark parsing toolkit). The tool extracts the function                              III. E VALUATION
signature and ACSL block, parses the contract into a small              We study three successive Stage 1 runs. MatAXPY es-
specification IR, derives the admissible cases (§III-B), and         tablishes the baseline contract form and motivates derived
emits one CIVL driver per case. It can also emit Makefiles           aliasing cases; MatAYPX applies that extension in contract-
that are then used to run the experiments and check expected         only mode; and the non-compressing mode of MatFilter
results. There is no LLM in this stage. Contracts that fail to       exercises a conditional postcondition. Unless stated otherwise,
run for any reason are rejected and passed back to the previous      the reported small experiments exhaustively explore all
stages.                                                              executions and symbolic inputs with MPI process counts 1 and
   The generated drivers run a CIVL-compatible port                  2 and global matrix dimensions M, N from 1 to 3 within the
<Func>.c of the PETSc implementation under test. The                 CIVL–PETSc model and the modes admitted by each certified
port preserves the implementation paths being verified while         contract.
removing currently unsupported features, such as sparse matrix          Table     III     reports  fresh    measurements.2      For
data type. Earlier CIVL–PETSc work manually implemented              MatAXPY          and     MatAYPX,      D     and      U    de-
reference models for selected operations. Of our three ex-           note          DIFFERENT_NONZERO_PATTERN                    and
amples, only MatAXPY has such a model. For MatAXPY,                  UNKNOWN_NONZERO_PATTERN, respectively. The aliased
                                                                     MatAYPX rows terminate at the provable contract violation.
  1 The   exact   command    was    cat $PROMPT_DIR/
Mat<Func>-prompt.md              | claude -p --model                   2 Measured on a laptop with an Intel Core Ultra 7 258V processor and
claude-opus-4-8             --no-session-persistence                 32 GiB of memory, using OpenJDK 21.0.11, CIVL 2.0 (2026-07-16), Z3
--setting-sources "" --allowed-tools "".                             4.8.12, and CVC4 1.8.
                               TABLE III                                               /*@ requires valid_mat(Y);
           CIVL VERIFICATION COST FOR THE S M A L L EXPERIMENTS .                          requires valid_mat(X);
                                                                                           requires assembled(Y);
Function         Case       str    Time (s)     Mem. (GiB)       States      Trans.
                                                                                           requires assembled(X);
                                                                                           requires same_comm(X, Y);
MatAXPY          aliased    D        27.01            2.27      79,599      162,530        requires separated_mat(X, Y) ;
MatAXPY          aliased    U        29.09            2.36      79,599      162,530
MatAXPY          distinct   D        36.73            2.27     102,082      206,215        requires Y->rmap->N == X->rmap->N;
MatAXPY          distinct   U        34.36            2.27     102,082      206,215        requires Y->cmap->N == X->cmap->N;
MatAYPX          aliased†   D         6.75            1.30       1,615        3,460        requires logically_collective(Y, a);
MatAYPX          aliased†   U         7.06            1.71       1,615        3,460        requires str == DIFFERENT_NONZERO_PATTERN
MatAYPX          distinct   D        29.16            2.27      71,429      149,142              || str == UNKNOWN_NONZERO_PATTERN;
MatAYPX          distinct   U        29.72            2.27      71,429      149,142        assigns Y->data[0 .. Y->rmap->N*Y->cmap->N -
MatFilter        —          —        18.29            1.30      20,502       40,062        1];
 † assertion violation for the aliasing bug.                                               ensures \forall integer i;
                                                                                             0 <= i < Y->rmap->N*Y->cmap->N ==>
                                                                                             Y->data[i] == a * \old(X->data[i])
                                 TABLE IV                                                                + \old(Y->data[i]);
                    A RTIFACT SIZE BY REVIEW STRATEGY.                                     ensures \result == 0; @*/
                                                                                       PetscErrorCode MatAXPY(Mat Y, PetscScalar a,
Function                PETSc body            Port     Drivers            Contract                            Mat X, MatStructure str);

MatAXPY                     39                 23        176                14                       Listing 2. Stage-1 output for MatAXPY
MatAYPX                     4                  4         152                13
MatFilter                   72                 24         38                 8
                                                                                      X = Y , but PETSc’s same-handle path ignores the hint en-
                                                                                      tirely. Stage 3 therefore retains this case rather than imposing
   Table IV compares three review strategies by counting                              an undocumented restriction. The dense model checks the
lines of code, excluding blank and comment-only lines. The                            resulting matrix values, not the sparse-pattern claim itself.
columns count the original PETSc body, its CIVL-compatible                               A clean-context Stage-1 run for MatAXPY produces the
port, all generated case drivers, and the ACSL clauses in the                         contract of Listing 2. The LLM transcribes the value relation
certified contract.                                                                   Y = aX + Y over the dense image and, finding the documen-
   These counts do not measure review time. They nevertheless                         tation silent on whether X = Y (aliasing) is allowed, takes
expose the immediate review surface: 8–14 contract lines                              a conservative position: it excludes aliasing with a requires
instead of 38–176 generated-driver lines per function.                                separated_mat(X, Y) clause and records that choice for the
A. Worked example: MatAXPY                                                            reviewer. Its certification notes go further: they observe that
                                                                                      the value relation still holds under aliasing (\old captures the
   Consider the PETSc documentation for MatAXPY, ex-
                                                                                      pre-state, so X = Y gives Y = (1 + a)Y ) and that the
cerpted in Listing 1. It states the value update and lists the
                                                                                      separated_mat restriction is therefore model-generated, not
str nonzero-pattern hints, but it does not specify whether the
                                                                                      documented.
input matrices may alias.
                                                                                         The formula holding under aliasing, however, does not settle
   The str argument is a nonzero-pattern hint used by PETSc
                                                                                      the question: X = Y is a different code path, not a special
for internal optimization. The contract admits DIFFERENT_
                                                                                      value of the same one, because the MatAXPY implementation
NONZERO_PATTERN and UNKNOWN_NONZERO_PATTERN,
                                                                                      branches on the aliased case with if (Y == X) MatScale(Y
and Stage 3 tests both with distinct and aliased han-
                                                                                      , 1+a) (a comparison of pointers / memory addresses, not
dles. We exclude SAME_NONZERO_PATTERN and SUBSET_
                                                                                      values). A driver over symbolic matrix values never reaches
NONZERO_PATTERN because the current dense model
                                                                                      that branch, because it allocates X and Y as two objects, so
cannot represent or check their structural preconditions.
                                                                                      the pointer test Y == X is false regardless of the values CIVL
DIFFERENT_NONZERO_PATTERN is not meaningful when
                                                                                      explores.
                                                                                         Only a same-handle driver for X and Y exercises it. We
 MatAXPY - Computes Y = a*X + Y.                                                      therefore treat the issue as a profile/tooling gap rather than
                                                                                      asking the LLM to generate an aliased case not specified by
 Logically Collective
                                                                                      the documentation. The fix is to encode two aliasing cases in
 Input Parameters:                                                                    the PETSc-ACSL profile: the same handle and distinct handles
 + a   - the scalar multiplier                                                        with disjoint storage. We then update acsl2civl to derive
 . X   - the first matrix
 . Y   - the second matrix                                                            those cases from a contract. With that derivation in place, the
 - str - either SAME_NONZERO_PATTERN,                                                 human reviewer certifies a revised contract with the Stage-1-
         DIFFERENT_NONZERO_PATTERN,                                                   generated separated_mat clause removed. acsl2civl then
         UNKNOWN_NONZERO_PATTERN, or
         SUBSET_NONZERO_PATTERN                                                       generates one driver for each combination of aliasing case
         (nonzeros of X is a subset of Y’s)                                           and admitted str value. Listing 2 shows the raw Stage-1
                                                                                      proposal; the artifact contains the corrected and certified Stage-
            Listing 1. PETSc documentation excerpt for MatAXPY.
                                                                                      2 contract.
MatAXPY_spec(exp_Y, a, p_X,                                           PetscErrorCode MatAYPX(Mat Y, PetscScalar a, Mat X,
    DIFFERENT_NONZERO_PATTERN);                                                              MatStructure str)
PetscErrorCode err = MatAXPY(p_Y,a,p_X,                               {
    DIFFERENT_NONZERO_PATTERN);                                         PetscFunctionBegin;
$assert(err == 0);                                                      PetscCall(MatScale(Y, a));
debug_print_matrix_result(ctx, p_Y, exp_Y);                             PetscCall(MatAXPY(Y, 1.0, X, str));
                                                                        PetscFunctionReturn(PETSC_SUCCESS);
verify_matrix_result(ctx, p_Y, exp_Y,                                 }
  "MatAXPY [distinct_different] postcondition on Y
    ");                                                                          Listing 4. PETSc implementation of MatAYPX.

verify_matrix_result(ctx, p_X, exp_X,
  "MatAXPY [distinct_different] frame on X");
                                                                     B. Evolving the profile
/* certified-contract assertions (--contract-assert
     mode): */                                                          The PETSc-ACSL profile is extensible through a human-
$mat img_Y = CIVL_PetscToCivlMat(p_Y);                               in-the-loop process. When the same contract structure appears
$mat img_X = CIVL_PetscToCivlMat(p_X);
if (ctx.rank == 0) {                                                 repeatedly, we move it into the profile and let Stage 3 generate
  STYPE X_pre[M * N];                                                it mechanically. We illustrate this refinement loop with the
  STYPE Y_pre[M * N];                                                MatAXPY aliasing split.
    for (int k = 0; k < M * N; k++) {                                  1) Inspect. The clean-context Stage 1 run emits one
      X_pre[k] = scalar_make(X_Real[k],                                   contract (Listing 2). It excludes X = Y with
      IMAG_SCALAR_INPUT_IDX(X, k));
      Y_pre[k] = scalar_make(Y_Real[k],                                   separated_mat(X, Y), but notes that the \old-based
      IMAG_SCALAR_INPUT_IDX(Y, k));                                       postcondition remains coherent under X = Y , thereby
    }                                                                     flagging the ambiguity without inventing a case split.
    for (int k = 0; k < (M * N); k++)                                  2) Identify. Retaining the clause would leave the imple-
      $assert(scalar_eq(img_Y.data[k],                                    mentation-supported X = Y branch unverified.
        scalar_add(scalar_mul(a, X_pre[k]), Y_pre[k])                  3) Decide, not re-prompt. Because the manpage is silent
      ),
        "MatAXPY [distinct_different] certified                           on aliasing, re-prompting would ask the LLM to invent
      ensures #1                                                          undocumented semantics. Based on implementation ev-
         on Y violated");                                                 idence, human intervention is required to decide the
    for (int k = 0; k < M * N; k++)                                       correct action, in this case removal of the generated
      $assert(scalar_eq(img_X.data[k], X_pre[k]),                         separated_mat clause, admitting X = Y without au-
        "MatAXPY [distinct_different] certified frame                     thoring a separate behavior.
         on X violated");
}                                                                      4) Mechanize. A developer extends acsl2civl with an
                                                                          aliased-or-distinct derivation rule. Stage 3 then generates
    Listing 3. Excerpt of the generated distinct_different driver.        a distinct, disjoint-storage driver and an aliased (X = Y )
                                                                          driver from the amended contract.
                                                                        Further applications may identify additional recurring pat-
                                                                     terns suitable for explicit Stage 3 rules, making acsl2civl
                                                                     more capable and reusable.
   Once the separated_mat clause is removed, Stage 3
generates     four     drivers:     distinct_different,              C. Contract-only verification: MatAYPX and an aliasing bug
distinct_unknown,             aliased_different,         and
aliased_unknown, where distinct means X, Y                              MatAYPX (Y ← aY + X) has no reference model in the
are different objects while aliased says they are the                CIVL–PETSc module, so its certified contract serves as the
same. Here, different and unknown abbreviate the                     only oracle. Because the documentation does not require X
corresponding str values in Listing 1. Listing 3 shows the           and Y to differ, the evolved profile leaves aliasing unrestricted.
core of the distinct_different driver: a reference-                  Stage 2 corrected the missing \old in the postcondition. It also
model oracle call, a call to the ported PETSc implementation,        expanded the tested str values from UNKNOWN_NONZERO_
whole-image comparison against the reference result, an              PATTERN to include DIFFERENT_NONZERO_PATTERN,
assigns-derived frame check on X, and certified postcondition        ensuring that every hint admitted by the certified contract is
assertions enabled by --contract-assert.                             exercised. The dense model checks only the numerical result,
                                                                     not the associated sparse-pattern claim. The manual review
   The other functions studied in this paper — MatAYPX and           certified the amended contract, from which Stage 3 derived
MatFilter — follow the same artifact pattern, so we do not           distinct and aliased drivers.
include their full contracts and generated drivers in the main          The distinct drivers pass in contract-only mode, but the
text. Their prompts, raw Stage 1 outputs, certified contracts,       aliased drivers produce a PROVABLE assertion violation. List-
generated drivers, and CIVL-compatible ports are included in         ing 4 shows the PETSc implementation: it scales Y and then
the accompanying artifact (§A).                                      adds X to the result.
                                                                                          3. Update acsl2civl
                                                                                          represent new operations in a form
                  1. Identify unsupported            2. Extend profile
                                                     Profile: allow symbolic PetscReal    that acsl2civl can understand.
                  semantics
                  MatFilter requires a               tol.                                 emit tol as a symbolic CIVL
                  symbolic real tolerance and        Parser: recognize \abs, ordered      input.
                  the conditional update             comparisons, and conditional         \abs(e) 7→ scalar_abs(e).
                  |Aold [i]| ≤ tol ? 0 : Aold [i].   expressions.                         support comparison and condi-
                                                                                          tional expression in the generated
                                                                                          assertion.


                               Fig. 2. Extending the PETSc-ACSL profile and acsl2civl to support MatFilter.



   When X = Y , the second call reads the already-scaled                     Reimplementing PETSc’s stash and assembly machinery
matrix and produces 2aYold instead of the documented (1 +                 in CIVL duplicates complex state and communication logic,
a)Yold . In contrast, MatAXPY explicitly handles aliased inputs           creating another place for bugs that could mask or manufacture
and satisfies its documented equation. Because MatAYPX                    verification failures. Such model code therefore requires its
documents no aliasing restriction, its inconsistent aliased result        own focused drivers and cross-checks, enlarging the codebase
is a bug, not a reason to weaken the contract with requires               that must be carefully reviewed and trusted. Until that valida-
Y != X.                                                                   tion is complete, matrix insertion and assembly remain outside
                                                                          the verification claim.
D. A conditional operation: MatFilter
   We verify the dense, and non-compressing mode of                                            V. R ELATED W ORK
MatFilter(A, tol, compress, keep), which zeroes                              Recent work has investigated whether LLMs can translate
every entry of A whose magnitude is at most tol and                       natural-language intent into formal specifications. Endres et
preserves every other entry. The two Boolean parameters                   al. [11] evaluate generated postconditions and show both the
compress and keep indicate whether to compress the                        promise of the approach and the need for semantic validation.
matrix and keep the diagonal entries after filtering. We do               Cao et al. [12] decompose translation from natural-language
not yet support those modes, so we set both parameters                    requirements into six formal-verification tasks and provide
to false. To express and translate this behavior, we added                training and evaluation data spanning five languages, including
support for symbolic PetscReal parameters, \abs, relational               ACSL. Clover [13] places generation in a closed loop with a
comparisons, and conditional expressions. Figure 2 shows the              formal verifier, using verification feedback to improve gener-
steps we took to extend the profile and update acsl2civl                  ated programs and proofs. ATLAS [14] similarly synthesizes
to support MatFilter.                                                     Dafny contracts, programs, and proofs from programming
   A clean-context Stage 1 run produced the elementwise post-             problems, reference implementations, and tests; it uses test-
condition A->data[i] ==(\abs(\old(A->data[i])) <= tol                     derived checks to detect inconsistent or weak specifications.
? 0 : \old(A->data[i])), which Stage 3 lowers directly to                 Our pipeline shares the goal of using formal tooling to
an elementwise CIVL-C assertion. The generated driver treats              constrain stochastic generation, but addresses existing PETSc
tol as a symbolic input.                                                  implementations and assigns the LLM a narrower role: it
                                                                          proposes a compact contract from library documentation that
                IV. S COPE AND LIMITATIONS                                a domain expert certifies before any driver is generated.
     a) Assembly and model fidelity: Elementwise algebraic                The LLM output is never executed as a verification harness;
routines such as MatAXPY admit direct relations between the               after human certification, the trusted deterministic compiler
pre- and post-state logical images. Assembly is harder because            generates the driver.
calls such as VecSetValues() and MatSetValues()                              ACSL provides C-level contracts, and Frama-C parses and
may apply locally owned updates immediately while placing                 analyzes those contracts [7], [8]. Our PETSc-ACSL profile de-
off-process updates in VecStash or MatStash objects.                      liberately supports only the fragment for which acsl2civl
The globally assembled object is established only after the               has explicit lowering rules. This is not general contract in-
corresponding AssemblyBegin/AssemblyEnd pair com-                         ference or full ACSL verification. It is a restricted interface
municates and combines those pending updates.                             between natural-language PETSc documentation and bounded
   The CIVL–PETSc module implements the scalar                            CIVL models, with unsupported constructs rejected rather than
VecStash path needed to exercise VecAssemblyBegin/                        approximated.
VecAssemblyEnd, including off-process communication                          A Frama-C plug-in could replace part of the custom profile
and insertion-mode reconciliation. Extending the same support             parser. The plug-in could reuse Frama-C’s ACSL front end
to matrices is ongoing work. Dense matrices are comparatively             to check syntax, typing, binding, and profile membership,
direct, but sparse matrices couple the stash protocol to row-             then export a valid contract representation for acsl2civl.
wise sparse storage, preallocation, duplicate entries, and                This would replace part of the current custom parsing path
insertion-mode rules, making a faithful MatStash model                    with checks grounded in the ACSL implementation itself
substantially more difficult to specify.                                  and make profile violations easier to diagnose before human
certification. It would not eliminate the human review: Frama-    this paper were edited with assistance from GPT 5.6 Sol, and
C can establish that a contract is well formed, but not that it   Claude Opus 4.8.
faithfully captures incomplete PETSc documentation or that a         This report was prepared as an account of work sponsored by an
reviewer made the right policy decision for an undocumented       agency of the United States Government. Neither the United States
case.                                                             Government nor any agency thereof, nor any of their employees,
                                                                  makes any warranty, express or implied, or assumes any legal liability
                     VI. C ONCLUSIONS                             or responsibility for the accuracy, completeness, or usefulness of any
   We presented a disciplined pipeline for LLM-assisted ver-      information, apparatus, product, or process disclosed, or represents
ification of PETSc operations: the LLM generates only a           that its use would not infringe privately owned rights. Reference
small behavioral contract in a restricted ACSL profile, a         herein to any specific commercial product, process, or service by trade
PETSc-aware human reviewer checks documented behavior             name, trademark, manufacturer, or otherwise does not necessarily
and records justified resolutions of documentation gaps, and      constitute or imply its endorsement, recommendation, or favoring by
a deterministic compiler lowers the certified contract to CIVL    the United States Government or any agency thereof. The views and
drivers. The contract and an optional, separately authored        opinions of authors expressed herein do not necessarily state or reflect
reference model contain the behavior specification. The design    those of the United States Government or any agency thereof.
confines direct review of LLM output to a compact contract,
                                                                                               R EFERENCES
and the tool refuses anything outside its profile rather than
guessing.                                                          [1] S. Balay, S. Abhyankar, M. F. Adams, S. Benson, J. Brown, P. Brune,
                                                                       K. Buschelman, E. M. Constantinescu, L. Dalcin, A. Dener et al.,
   Our evaluation covers MatAXPY, MatAYPX, and the                     “Petsc/tao users manual revision 3.25,” Argonne National Laboratory
non-compressing mode of MatFilter. Applying the                        (ANL), Argonne, IL (United States), Tech. Rep., 03 2026. [Online].
pipeline across these routines also drove two extensions to            Available: https://www.osti.gov/biblio/3025790
                                                                   [2] S. F. Siegel, M. Zheng, Z. Luo, T. K. Zirkel, A. V. Marianiello, J. G.
acsl2civl: derived aliasing cases and, for MatFilter’s                 Edenhofner, M. B. Dwyer, and M. S. Rogers, “Civl: the concurrency
non-compressing mode, conditional postconditions over real             intermediate verification language,” in Proceedings of the International
parameters. The derived aliased case exposed a bug in                  Conference for High Performance Computing, Networking, Storage and
                                                                       Analysis, 2015, pp. 1–12.
MatAYPX that had remained undetected since 1997, which             [3] V. Dhavala, J. Hückelheim, P. D. Hovland, and S. F. Siegel, “Verifying
produces 2aY rather than (1 + a)Y when its operands are the            petsc vector components using civl,” in International Conference on
same handle.                                                           Computer Aided Verification. Springer, 2025, pp. 148–161.
                                                                   [4] Z. Luo, M. Zheng, and S. F. Siegel, “Verification of mpi programs using
   Future work will extend matrix assembly support to                  civl,” in Proceedings of the 24th European MPI Users’ Group Meeting,
MatStash and sparse storage; broaden the profile to addi-              2017, pp. 1–11.
tional Mat operations and Vec reductions; lower supported          [5] S. F. Siegel and T. K. Zirkel, “Collective assertions,” in International
                                                                       Workshop on Verification, Model Checking, and Abstract Interpretation.
requires clauses into driver assumptions; and develop the              Springer, 2011, pp. 387–402.
Frama-C profile-checking plug-in described in §V.                  [6] Z. Luo and S. F. Siegel, “Collective contracts for message-passing
                                                                       parallel programs,” in Computer Aided Verification (CAV 2024), ser.
                       A PPENDIX A                                     Lecture Notes in Computer Science, A. Gurfinkel and V. Ganesh, Eds.,
                                                                       vol. 14682. Cham: Springer, 2024, pp. 44–68.
             A RTIFACT AND R EPRODUCIBILITY                        [7] P. Baudin, J.-C. Filliâtre, C. Marché, B. Monate, Y. Moy, and V. Pre-
   The artifact records the three versioned Stage 1 prompts—           vosto, “Acsl: Ansi/iso c specification,” URL https://frama-c. com/htm-
                                                                       l/acsl. html, 2021.
one for each profile iteration—and the resulting contracts,        [8] F. Kirchner, N. Kosmatov, V. Prevosto, J. Signoles, and B. Yakobowski,
corrected as needed during the Stage 2 human review and                “Frama-c: A software analysis perspective,” Formal aspects of comput-
then certified. Contracts were authored with Claude (An-               ing, vol. 27, no. 3, pp. 573–609, 2015.
                                                                   [9] L. d. Moura and S. Ullrich, “The lean 4 theorem prover and program-
thropic); the human review stamps (revision, date, certi-              ming language,” in International Conference on Automated Deduction.
fier) are in each contract’s header. The Stage-3 compiler              Springer, 2021, pp. 625–635.
(tools/acsl2civl, Python + Lark) and the CIVL–PETSc               [10] T. R. D. Team, “The rocq prover,” Sep. 2025. [Online]. Available:
                                                                       https://doi.org/10.5281/zenodo.17473943
module it presupposes are part of the same repository.            [11] M. Endres, S. Fakhoury, S. Chakraborty, and S. K. Lahiri, “Can large
                                                                       language models transform natural language intent into formal method
                        A PPENDIX B                                    postconditions?” Proc. ACM Softw. Eng., vol. 1, no. FSE, Jul. 2024.
                  A RTIFACT AVAILABILITY                               [Online]. Available: https://doi.org/10.1145/3660791
                                                                  [12] J. Cao, Y. Lu, M. Li, H. Ma, H. Li, M. He, C. Wen, L. Sun, H. Zhang,
   The artifact is submitted as supplementary material with the        S. Qin et al., “From informal to formal–incorporating and evaluating
paper. A public archival URL will be added to the camera-              llms on natural language requirements to verifiable formal proofs,”
                                                                       in Proceedings of the 63rd Annual Meeting of the Association for
ready version.                                                         Computational Linguistics (Volume 1: Long Papers), 2025, pp. 26 984–
                                                                       27 003.
                    ACKNOWLEDGMENT                                [13] C. Sun, Y. Sheng, O. Padon, and C. Barrett, “Clover: Closed-loop ver
                                                                       ifiable code generation,” in International Symposium on AI Verification.
  This material is based upon work supported by the U.S.               Springer, 2024, pp. 134–155.
National Science Foundation under Award Number CCF-               [14] M. Baksys, S. Zetzsche, O. Bouissou, R. Delmas, S. Kong, and
2446130, and by the U.S. Department of Energy, Office of               S. B. Holden, “Atlas: Automated toolkit for large-scale verified code
                                                                       synthesis,” 2026. [Online]. Available: https://arxiv.org/abs/2512.10173
Science, Advanced Scientific Computing Research (ASCR)
Program, under Award Number DE-SC0025953. Portions of
