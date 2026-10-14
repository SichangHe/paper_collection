                                        RustCompCert: A Verified and Verifying Compiler for
                                                  a Sequential Subset of Rust
                                                                        Jinhua Wu∗ , Yuting Wang∗ , Liukun Yu∗ , Linglong Meng§
                                                                        Shanghai Jiao Tong University, China∗ University of Minnesota, USA§
                                                                                             yuting.wang@sjtu.edu.cn

                                        1    Introduction                                                          RAII and ownership semantics, (im)mutable references with
                                        We aim to develop an end-to-end verified Rust compiler. It                 region (or lifetime) annotations, as well as the composition
                                        should provide two guarantees: one is semantics preserva-                  of safe and unsafe modules (e.g., safe Rust and C). The main
                                        tion, i.e., the behaviors of source code includes the behav-               unsupported features include concurrency, polymorphism,
                                        iors of target code, with which the properties verified at                 traits, and higher-order functions (e.g., closures).
arXiv:2602.07455v1 [cs.PL] 7 Feb 2026




                                        the source can be preserved down to the target; the other is                  How we present it. We plan to present our work in 20–25
                                        memory safety ensured by the verifying compilation [6]—the                 minutes, with an additional 5–10 minutes reserved for Q&A.
                                        borrow checking pass [20], which can simplify the verifica-                The presentation will broadly follow the structure of this
                                        tion of Rust programs, e.g., by allowing the verification tools            paper. We will begin by introducing the compilation passes of
                                        focus on the functional correctness [2–5, 10, 13].                         RustCompCert and its main correctness theorems in §2. We
                                           However, there are significant challenges in verifying the              will then focus on how we formalize and verify the borrow
                                        Rust compiler. Some Rust compilation and checking passes,                  checking algorithm as described in §3. Due to time and space
                                        such as Drop Elaboration [15] and Borrow Checking [20],                    limits, we may not cover our approach to supporting unsafe
                                        involve complicated program analysis algorithms. It is non-                code; interested readers can refer to this paper [23]. Our
                                        trivial to formalize and verify these analyses within existing             ongoing formalization is publicly available at https://github.
                                        frameworks for verified compilers. Existing formalizations of              com/SJTU-PLV/CompCert/tree/rust-verified-compiler.
                                        Rust [7, 22] primarily focus on verifying its type soundness,
                                        rather than verifying the analysis algorithms themselves.                  2   Overview of RustCompCert
                                        Aeneas [4, 5] proposes a promising borrow checking algo-
                                                                                                                   The internal structure of the RustCompCert frontend is
                                        rithm based on a borrow-centric semantics, but we focus
                                                                                                                   shown in Fig. 2. We follow the design of the standard Rust
                                        on another direction—verifying the algorithms used in the
                                                                                                                   compiler (i.e., rustc) to structure our compilation pipeline.
                                        standard Rust compiler, namely NLL [1] or Polonius [19].
                                                                                                                   The syntax of Rustlight is close to that of surface Rust. We
                                                                                                                   design an intermediate representation called RustIR, whose
                                                Parser                RustCompCert                CompCert
                                         Rust            Rustlight                       Clight              Asm   syntax is similar to MIR. The first pass lowers Rustlight to
                                                                         frontend                 backend          RustIR in preparation for subsequent analyses, correspond-
                                                                                                                   ing to the MIR construction in rustc [16]. We then perform
                                            Figure 1. Structure of RustCompCert (green: verified)                  Drop Elaboration [15], which is a key pass in rustc that
                                                                                                                   realizes the mechanism of automatic resource management.
                                           We present our ongoing work on verifying a Rust compiler                This pass determines which drop operations (i.e., destruc-
                                        frontend in Rocq and connecting it with CompCert [11, 12]                  tors) should be executed by analyzing the initialization status
                                        to build an end-to-end verified Rust compiler, which we call               of variables. Consequently, the correctness of this pass cru-
                                        RustCompCert. Its overall structure is illustrated in Fig. 1,              cially relies on the soundness of this program analysis.
                                        which consists of three components: (1) an unverified parser
                                        that translates source Rust code into Rustlight, a sequential                                                   Borrow Checking
                                        subset of Rust formalized in Rocq; (2) a verified frontend that
                                                                                                                                Lower               Drop                  Clight
                                        compiles Rustlight to Clight, including Rust-specific passes                Rustlight           RustIR                 RustIR                Clight
                                                                                                                                                 Elaboration            Generation
                                        such as Drop Elaboration and Borrow Checking; and (3) a
                                        verified backend based on CompCert, an optimizing compiler
                                                                                                                         Figure 2. Structure of RustCompCert Frontend
                                        that compiles Clight to assembly1 .
                                           Verifying all features of Rust is not realistic. We therefore             We then perform borrow checking on RustIR. The bor-
                                        focus on a core subset of the language, which we formalize as              row checker consists of two components: a move checking
                                        Rustlight. Rustlight supports algebraic data types (i.e., struct           pass [17], which ensures that each variable is not used after
                                        and enum), automatic memory management for Box via                         being moved, and a borrow checking pass based on Polo-
                                        1We use the framework of CompCertO [9, 24], an extension of CompCert,      nius [19]. Compare to NLL [1], the stable borrow checker in
                                        to support verified compositional compilation.                             rustc which interprets regions as “sets of program points
                                                                                             Jinhua Wu∗ , Yuting Wang∗ , Liukun Yu∗ , Linglong Meng§


that a loan may live”, Polonius can be seen as an alias anal-                     complex graph construction and solving algorithms [18],
ysis, which is more suitable to implement in the program                          this approach would be difficult to verify in Rocq in practice.
analysis framework provided by CompCert. Its interpreta-                          We instead implement it within the Kildall framework [8]
tion of regions as “sets of places that a reference may point                     in CompCert by defining its abstract domain and transfer
to” aligns naturally with the values that may be stored in                        functions. The result of Polonius is then obtained as a fixpoint
references in the program semantics. The Clight Generation                        computed by the Kildall solver.
pass serves as the code generation phase. For example, it                            Abstract Domain. The naive definition is a loans map from
translates enum types into tagged unions and generates drop                       regions to set of loans (the terminology representing bor-
glue functions for types that require destructors.                                rowed places). However, borrow checking relies on variance
                                                                                  rules [21] to maintain equality relationships between regions.
  Compiler Correctness. Like CompCert providing end-to-
                                                                                  The analysis must therefore not only propagate loans across
end semantics preservation for Clight programs, RustCom-
                                                                                  regions and program points, but also propagate the equal-
pCert also provides this guarantee for Rustlight programs:
                                                                                  ity relation between regions. If two regions are recorded as
∀ (𝑀𝑠 : Rustlight) (𝑀𝑡 : Asm),                                                    equal, they must contain the same set of loans. We achieve
    RustCompCert(𝑀𝑠 ) = 𝑀𝑡 ⇒ J𝑀𝑡 K ⩽ J𝑀𝑠 K                                        this by maintaining region equality in the abstract domain
                                                                                  using a union–find structure. To access the loans associated
Here J𝑀𝑡 K ⩽ J𝑀𝑠 K is defined as a standard backward sim-
                                                                                  with a region, we use its representative in the union–find to
ulation, meaning that the behaviors of source program is
                                                                                  index the loans map instead of using the region itself. As a re-
included in the behaviors of target program.
                                                                                  sult, the abstract domain is a pair of type (𝑀 × 𝑈 ) consisting
   Soundness of Borrow Checking. The memory safety en-                            of a mapping from regions to loans and a union–find struc-
sured by the borrow checking has been utilized by many Rust                       ture. To integrate this domain into the Kildall framework,
verification tools [2–5, 10, 13] to simplify the verification at                  we further prove that it forms a semi-lattice.
the source level, e.g., by focusing on its functional correct-                       Transfer Function. A transfer function 𝐹 : N → (𝑀 ×𝑈 ) →
ness. To provide such guarantee, we extract a functional                          (𝑀 × 𝑈 ) describes how the abstract state of type (𝑀 × 𝑈 )
specification called RustIRspec which abstracts the low-level                     evolves for an instruction at node 𝑛 ∈ N. It mainly specifies
CompCert memory of the RustIR semantics into a structured                         how loans flow from one region (e.g., the assigner) to another
memory model. The soundness of borrow checking is then                            (e.g., the assignee). Moreover, new equality relations between
formalized as a refinement between RustIRspec and RustIR:                         regions may be established (e.g., by variance rules [21]). Con-
∀ (𝑀 : RustIR), BorrowCheck(𝑀) ✓ ⇒
                                                                                  versely, some relations may need to be removed when one
                                                                                  of the regions in the relation becomes dead (i.e., will no
    J𝑀KRustIR ⩽ J𝑀KRustIRspec ∧ safe J𝑀KRustIRspec                                longer be used). We design the transfer function following
For programs passing the borrow checking, we can conclude                         the subtyping and reborrow rules in the NLL RFC [1] and
that its specification is safe, i.e., it has no undefined behav-                  their implementation in rustc.
iors. 2 The predicate safe can be seen as a definition of par-                       Verification of Polonius. Recall that we define the sound-
tial correctness [23]. When the programs are open, it would                       ness of borrow checking as a refinement between RustIRspec
specify pre- and post-conditions to support composition.                          and RustIR. To prove this refinement for any program that
                                                                                  passes borrow checking, the key steps are: (1) to establish an
  End-to-end Verification. By combining the soundness of
                                                                                  approximation relation between the abstract state produced
borrow checking and the compiler correctness, the properties
                                                                                  by the borrow-checking analysis and the concrete state (i.e.,
verified in RustIRspec can be preserved to the assembly:
                                                                                  the memory model) in the semantics, and (2) to show that
∀ (𝑀𝑠 : RustIR) (𝑀𝑡 : Asm),                                                       under this relation every operation in the structured memory
    RustCompCert(𝑀𝑠 ) = 𝑀𝑡 ⇒ safe J𝑀𝑠 KRustIRspec ⇒ safe J𝑀𝑡 KAsm                 model of RustIRspec can correspond to a non-stuck opera-
                                                                                  tion in the CompCert memory model of RustIR. In particular,
3     Formalization and Verification of the                                       this implies the absence of memory errors. The first step is
      Borrow Checking Algorithm                                                   the more challenging one. With Polonius viewed as a form
                                                                                  of alias analysis, we can relate each region to the set of
   Formalization of Polonius. One possible strategy is to
                                                                                  memory locations that may alias with the places containing
re-implement the current Polonius in Rocq, for instance by
                                                                                  this region, a property that is much easier to formalize [14].
porting its code from rustc. However, because it relies on
                                                                                  This abstraction relation also guides potential improvements
2 In fact, we cannot show that the borrow checker rules out all undefined
                                                                                  to the Polonius algorithm in terms of precision and perfor-
behaviors. For example, division-by-zero is a typical UB that borrow check-       mance. For instance, we can relax the alias sets to reduce
ing cannot prevent. Therefore, the safety ensured by the borrow checker is
partial safety: some UBs may still occur in the semantics. To obtain total        precision in exchange for better performance (e.g., by mak-
safety (absence of all UBs), it remains the prover’s responsibility to rule out   ing Polonius field-insensitive), while still being able to prove
these UBs.                                                                        soundness using the same proof technique.
RustCompCert: A Verified and Verifying Compiler for a Sequential Subset of Rust


References                                                                        [19] Rémy Rakic and Niko Matsakis on behalf of The Polonius Working
 [1] Aaron Turon, Konrad Borowski, Hidehito Yabuuchi, and Dan Aloni.                   Group. 2023. Polonius Update. https://blog.rust-lang.org/inside-
     2017. Non-Lexical Lifetimes. https://rust-lang.github.io/rfcs/2094-               rust/2023/10/06/polonius-update.html Accessed Ocotober 12, 2025.
     nll.html Accessed Ocotober 12, 2025.                                         [20] The Rust Team. 2025. MIR borrow check. https://rustc-dev-guide.rust-
 [2] Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J.                lang.org/borrow_check.html
     Summers. 2019. Leveraging rust types for modular specification and           [21] The Rust team. 2025. Subtyping and Variance. https://doc.rust-
     verification. Proc. ACM Program. Lang. 3, OOPSLA, Article 147 (Oct.               lang.org/nomicon/subtyping.html
     2019), 30 pages. doi:10.1145/3360573                                         [22] Aaron Weiss, Olek Gierczak, Daniel Patterson, and Amal Ahmed. 2019.
 [3] Xavier Denis, Jacques-Henri Jourdan, and Claude Marché. 2022.                     Oxide: The essence of rust. arXiv preprint arXiv:1903.00982 (2019).
     Creusot: A Foundry for the Deductive Verification of Rust Programs.          [23] Jinhua Wu, Yuting Wang, Liukun Yu, and Linglong Meng. 2025. End-
     In Formal Methods and Software Engineering: 23rd International Con-               to-end Compositional Verification of Program Safety through Verified
     ference on Formal Engineering Methods, ICFEM 2022, Madrid, Spain, Oc-             and Verifying Compilation. arXiv:2510.10015 [cs.PL] https://arxiv.
     tober 24–27, 2022, Proceedings (Madrid, Spain). Springer-Verlag, Berlin,          org/abs/2510.10015
     Heidelberg, 90–105. doi:10.1007/978-3-031-17244-1_6                          [24] Ling Zhang, Yuting Wang, Jinhua Wu, Jérémie Koenig, and Zhong
 [4] Son Ho, Aymeric Fromherz, and Jonathan Protzenko. 2024. Sound                     Shao. 2024. Fully Composable and Adequate Verified Compilation
     Borrow-Checking for Rust via Symbolic Semantics. Proc. ACM Pro-                   with Direct Refinements between Open Modules. Proc. ACM Program.
     gram. Lang. 8, ICFP, Article 251 (Aug. 2024), 29 pages. doi:10.1145/              Lang. 8, POPL, Article 72 (Jan. 2024), 31 pages. doi:10.1145/3632914
     3674640
 [5] Son Ho and Jonathan Protzenko. 2022. Aeneas: Rust verification by
     functional translation. Proc. ACM Program. Lang. 6, ICFP, Article 116
     (Aug. 2022), 31 pages. doi:10.1145/3547647
 [6] Tony Hoare. 2003. The verifying compiler: A grand challenge for
     computing research. J. ACM 50, 1 (Jan. 2003), 63–69. doi:10.1145/
     602382.602403
 [7] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer.
     2017. RustBelt: securing the foundations of the Rust programming
     language. Proc. ACM Program. Lang. 2, POPL, Article 66 (Dec. 2017),
     34 pages. doi:10.1145/3158154
 [8] Gary A. Kildall. 1973. A unified approach to global program opti-
     mization. In Proceedings of the 1st Annual ACM SIGACT-SIGPLAN
     Symposium on Principles of Programming Languages (Boston, Mas-
     sachusetts) (POPL ’73). Association for Computing Machinery, New
     York, NY, USA, 194–206. doi:10.1145/512927.512945
 [9] Jérémie Koenig and Zhong Shao. 2021. CompCertO: Compiling Certi-
     fied Open C Components. In Proc. 2021 ACM Conference on Program-
     ming Language Design and Implementation (PLDI’21). ACM, New York,
     NY, USA, 1095–1109. doi:10.1145/3453483.3454097
[10] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha
     Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel.
     2023. Verus: Verifying Rust Programs using Linear Ghost Types. Proc.
     ACM Program. Lang. 7, OPSLA1, Article 85 (April 2023), 30 pages.
     doi:10.1145/3586037
[11] Xavier Leroy. 2009. Formal Verification of a Realistic Compiler. Com-
     mun. ACM 52, 7 (2009), 107–115. doi:10.1145/1538788.1538814
[12] Xavier Leroy. 2009. A Formally Verified Compiler Back-end. Journal
     of Automated Reasoning 43, 4 (2009), 363–446. doi:10.1007/s10817-009-
     9155-4
[13] Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. 2021.
     RustHorn: CHC-based Verification for Rust Programs. ACM Trans.
     Program. Lang. Syst. 43, 4, Article 15 (Oct. 2021), 54 pages. doi:10.1145/
     3462205
[14] Valentin Robert and Xavier Leroy. 2012. A Formally-Verified Alias
     Analysis. In Certified Programs and Proofs, Chris Hawblitzel and Dale
     Miller (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 11–26.
[15] Rust Compiler Team. 2025. Drop elaboration. https://rustc-dev-
     guide.rust-lang.org/mir/drop-elaboration.html
[16] Rust Compiler Team. 2025. MIR construction. https://rustc-dev-
     guide.rust-lang.org/mir/construction.html
[17] Rust Compiler Team. 2025.             Tracking moves and initializa-
     tion. https://rustc-dev-guide.rust-lang.org/borrow_check/moves_
     and_initialization.html
[18] Rust contributors. 2026. Implementation of Polonius in Rust com-
     piler. https://github.com/rust-lang/rust/tree/main/compiler/rustc_
     borrowck/src/polonius Accessed February 2, 2026.
