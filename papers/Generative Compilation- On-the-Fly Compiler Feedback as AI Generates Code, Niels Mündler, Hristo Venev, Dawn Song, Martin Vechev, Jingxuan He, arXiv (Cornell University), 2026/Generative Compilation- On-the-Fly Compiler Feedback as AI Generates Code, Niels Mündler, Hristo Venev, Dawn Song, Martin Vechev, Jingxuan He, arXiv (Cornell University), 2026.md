                                         Generative Compilation: On-the-Fly Compiler Feedback as AI
                                         Generates Code
                                         NIELS MÜNDLER-SASAHARA∗ , ETH Zurich, Switzerland
                                         HRISTO VENEV∗ , INSAIT and Sofia University “St. Kliment Ohridski”, Bulgaria
                                         DAWN SONG, University of California, Berkeley, USA
                                         MARTIN VECHEV, ETH Zurich, Switzerland
                                         JINGXUAN HE, University of California, Berkeley, USA
                                         Languages with rich static semantics, such as Rust, provide stronger guarantees for AI-generated code, but
                                         their strictness makes generation more difficult. Off-the-shelf compilers can provide useful feedback post-
                                         generation, but does not guide intermediate generation steps, such as those during autoregressive LLM
                                         decoding. Constrained decoding intervenes earlier by rejecting invalid tokens during sampling, but requires
                                         white-box model access and costly reimplementation for semantic constraints.
                                            We introduce generative compilation, the first approach to obtaining compiler feedback on partial programs
arXiv:2607.13921v2 [cs.PL] 16 Jul 2026




                                         during generation. The core technical device is a sealor: a lightweight, mostly syntax-guided transformation
                                         that converts partial programs into complete ones that standard compilers can diagnose. It is designed such
                                         that possible-to-complete partial programs are never rejected, while preserving enough code context to catch
                                         genuine dead ends early. We construct such a sealor on a core Rust-like calculus and prove that it satisfies
                                         these properties, all mechanized in Lean. We extend it to the first partial-program checker for real Rust.
                                            We evaluate our method on challenging repository-level Rust coding tasks, across both frontier black-box
                                         and open-weight models. We show that generative compilation reduces non-compiling outputs and improves
                                         functional correctness, relative to standard post-generation feedback. It does so by detecting a broad range
                                         of errors close to their source and early during generation, thereby reducing errors cascades and enabling
                                         focused diagnostics. More broadly, generative compilation is a step toward making compilers a first-class
                                         citizen of AI-assisted programming active during generation, rather than a separate post-generation check.

                                         1   Introduction
                                         AI has become a standard tool for code generation, driven by the growing capabilities of large
                                         language models (LLMs) and LLM-based coding agents [17]. Yet AI-generated code remains error-
                                         prone, threatening the correctness and security of downstream software systems [42, 54]. This
                                         makes languages with rich static semantics particularly valuable for AI-generated code. Rust, for
                                         example, uses its ownership and borrowing discipline to provide memory safety guarantees and
                                         prevent related reliability and security failures [19, 27]. At the same time, these guarantees are
                                         enforced through strict compile-time rules, making valid code harder to generate than in more
                                         permissive languages such as C [8, 20, 59]. Compiler feedback can help bridge this gap by identifying
                                         violations and guiding the model toward code that satisfies these rules.
                                         Post-Generation Compiler Feedback. The most common way to leverage compiler feedback is
                                         to wait until entire files are fully generated, run the compiler as is on the resulting program, and feed
                                         any diagnostics back to the model. This post-hoc feedback loop has important practical advantages:
                                         it works with black-box LLMs and benefits from the compiler’s guarantees and diagnostics with no
                                         ∗ Both authors contributed equally to this research.
                                         †We publicly release our proof mechanization, code implementation, benchmarks, and evaluation results: https://github.

                                         com/eth-sri/generative-compilation.

                                         Authors’ Contact Information: Niels Mündler-Sasahara, ETH Zurich, Zurich, Switzerland, niels.muendler@inf.ethz.ch; Hristo
                                         Venev, INSAIT and Sofia University “St. Kliment Ohridski”, Sofia, Bulgaria, hristo.venev@insait.ai; Dawn Song, University
                                         of California, Berkeley, Berkeley, CA, USA, dawnsong@berkeley.edu; Martin Vechev, ETH Zurich, Zurich, Switzerland,
                                         martin.vechev@inf.ethz.ch; Jingxuan He, University of California, Berkeley, Berkeley, CA, USA, jingxuan.he@berkeley.edu.
1:2                           Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


additional implementation cost [5, 9, 56]. However, it does not take advantage of the intermediate
outputs produced during generation. Feedback becomes available only after the complete program
has been produced, meaning that every token emitted after the first unrecoverable error may be
based on invalid assumptions and ultimately wasted. Moreover, since the feedback concerns the
entire output, the model receives a batch of accumulated diagnostics all at once, which can be large
enough to hinder model understanding [10, 24].
Constrained Decoding. Constrained decoding instead intervenes directly during generation. It
checks intermediate outputs of LLMs, accepting only tokens that keep the current output extendable
to a valid program [23, 31, 39, 43, 53]. Thus, if generation terminates, the final output is guaranteed
to be valid. However, for languages with expressive static semantics, achieving this guarantee
requires substantial language-specific reimplementation, making it effectively impractical to support
more than restricted fragments [29, 31, 34]. Moreover, token-level filtering is silent: the model is
steered away from invalid continuations, but never receives compiler-style explanations that could
help it revise the code. Finally, constrained decoding requires white-box access to the model’s
next-token distribution and sampling process, ruling out its application to frontier models exposed
only through black-box APIs [33, 53].
This Work: Generative Compilation. We introduce generative compilation, the first approach
to make compiler-style feedback available during code generation. It serves as a middle ground
between post-generation feedback and constrained decoding, addressing key limitations of both.
Like constrained decoding, a generative compiler processes partial programs while they are being
produced. Unlike constrained decoding, however, it provides compiler-style diagnostics upon
rejection. The model receives an explanation of what went wrong and can revise the generated
code, rather than being silently steered away from invalid tokens. Because the feedback is obtained
on partial code, it concerns only isolated coding mistakes and avoids contextual clutter. Further,
the technique works with black-box models and reuses existing compiler infrastructure.
   To enable generative compilation, the core new concept we introduce is a sealor: a transformation
that closes a partial program into a complete one by filling in missing syntactic structure and
inserting well-typed placeholders. The resulting sealed program can then be checked by an existing
compiler. The key challenge is designing the sealor to achieve both faithful feedback and error
coverage. Compiler rejection of the sealed program should guarantee that the partial program
truly requires revision. At the same time, sealing should expose as many dead ends as possible, so
that unrecoverable errors are caught early. We formalize these properties through corresponding
completeness and soundness guarantees.
   Our key insight is that a lightweight, mostly syntax-guided sealor can already meet the guarantees
we target, without reimplementing the target language’s type system. We first demonstrate this
on Featherweight Rust (FR), a compact calculus inspired by Rust’s ownership and borrowing
discipline [41]. We develop a sealor for FR and prove that it satisfies the desired properties, with the
full development mechanized in Lean. We then carry the same methodology to real Rust: the sealor
preserves generated syntax, inserts a small set of placeholders for missing code, and delegates type,
borrow, and lifetime reasoning to rustc, the Rust compiler.
   We perform an extensive evaluation across seven frontier black-box and open-weight LLMs.
We focus on two repository-level code generation tasks for Rust, designed to stress compiler
feedback: C-to-Rust translation and code generation against recently updated library APIs. The
results show that, compared with post-generation feedback, the on-the-fly feedback loop enabled
by generative compilation further reduces compiler errors and improves functional correctness
in most model-task configurations. We then analyze how: generative compilation provides more
focused diagnostics that are close to the error source and available well before file completion.
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                              1:3


Key Contributions. In summary, our main contributions are:
• We introduce generative compilation, a novel framework enabling off-the-shelf compilers to
  check partial programs during code generation. We define the notion of sealors and prove that
  their completeness and soundness lift to generative compilation. (§3)
• We instantiate generative compilation on FR, presenting a syntax-guided sealor that never rejects
  partial programs that admit valid completion and correctly flags an important class of partial
  programs with no valid extension. We fully mechanize FR, our sealor, and its guarantees in Lean,
  making a number of corrections to the original FR formalization in the process. (§4 and §5)
• We apply our methodology to real Rust and build the first partial-program checker for Rust.
  This is based on a practical sealor that delegates semantic checking to rustc while handling
  Rust-specific syntax, control flow, placeholders, and future-dependent errors. (§6)
• We evaluate our approach extensively on Rust coding tasks across frontier and open-weight
  models, showing that it reduces compiler errors, improves functional correctness, and detects
  various errors early during generation. (§7)

2   Motivation for Generative Compilation
Today’s AI-based code generation is largely powered by LLMs. However, LLM-generated code
provides no guarantee of respecting the target language’s static rules. Two existing strategies aim
to address this gap: post-generation compiler feedback and constrained decoding. In this section,
we present both strategies and use a running example to show their limitations, thereby motivating
generative compilation.

Code Generation with Language Models. Let 𝑀 denote an LLM that generates code autore-
gressively, one token at a time from left to right. These tokens are drawn from a fixed vocabulary Σ,
determined by 𝑀’s tokenizer. Modern LLM tokenizers are universal: any string can be constructed
from tokens in Σ [49]. We therefore take Σ∗ to be the domain of all strings.
   Given a prompt 𝑥 (a natural-language task, op- 1 fn fmt_msg(msg: &mut String) -> String {
tionally with reference code) and the code gen- 2 let tag = &msg[..HEADER_SIZE];
erated so far 𝑐, 𝑀 produces a next-token distri- 3 msg.drain(..HEADER_SIZE);
bution 𝑀 (· | 𝑥 ◦ 𝑐), where ◦ denotes string con- 4 let prio = tag.starts_with("HIGH");
catenation. A token 𝑡 ∼ 𝑀 (· | 𝑥 ◦ 𝑐) is sampled, 5 let body = msg;
appended to 𝑐, and generation repeats until a           6   let n = body.lines().count();
special end-of-sequence token EOS is produced. 7 format!("{} {}: {}", prio, n, body)
As discussed above, this process can generate           8 }
any string in Σ∗ . However, for a target language
𝐿 ⊆ Σ∗ , there is no a priori guarantee that the Fig. 1. Non-compilable LLM-generated Rust code.
final output lies in 𝐿. For example, when prompted to write a Rust function that strips a fixed-size
header from a message and formats the result for logging, an LLM might produce the code in Fig. 1.
Running the Rust compiler on this program reveals that it cannot be compiled.

Post-Generation Compiler Feedback. Most programming languages provide a practical checker
C that decides, for a given string 𝑐, whether it belongs to the language 𝐿, i.e., whether 𝑐 is syntacti-
cally well-formed and type checks. Although compilers perform many tasks, such as optimizing
code and emitting assembly, it is common to refer to this checking phase as “compiling”; following
this convention, we call the checker a “compiler” in this paper.
   Formally, we model the compiler as a function C : Σ∗ → B × Σ∗ , which maps an input string 𝑐 to a
pair (ok, err) consisting of a Boolean verdict and a textual diagnostic. If 𝑐 ∈ 𝐿, then C(𝑐) = (true, ""),
i.e., the textual diagnostic is empty; otherwise, C(𝑐) = (false, err), where err ≠ "" is an error
1:4                                Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


      error[E0502]: cannot borrow ‘*msg‘ as mutable because it is also borrowed as immutable
      2 |     let tag = &msg[..HEADER_SIZE];
       |                   --- immutable borrow occurs here
      3 |       msg.drain(..HEADER_SIZE);
       |        ^^^^^^^^^^^^^^^^^^^^^^^^ mutable borrow occurs here
      4 |       let prio = tag.starts_with("HIGH");
       |                     --- immutable borrow later used here

            Fig. 2. Error message returned by the Rust compiler after it rejects the program in Fig. 1.



message explaining why 𝑐 ∉ 𝐿, e.g., by highlighting a failed type check, and potentially suggesting
how to resolve the issue, e.g., by suggesting a type cast. The compiler can be naturally used in
a feedback loop for LLM-based code generation: after the model generates a full program 𝑐, we
obtain (ok, err) ≔ C(𝑐). If ok = true, generation terminates and 𝑐 is guaranteed to be an element of
𝐿. Otherwise, the model is asked to try again with the original prompt augmented by the generated
program and diagnostic, e.g., 𝑥 ◦ 𝑐 ◦ err.
   For the example program in Fig. 1, running the compiler returns (false, err), with err shown in
Figure 2. The error involves Rust’s ownership, borrowing, and lifetime discipline: a value may be
accessed through either shared immutable references or an exclusive mutable reference, but not
both during overlapping lifetimes. At Line 2, the slice tag is an immutable borrow of msg. The call
to msg.drain at Line 3 then attempts to mutably borrow msg while that immutable borrow is still
live, because tag is later used at Line 4. This diagnostic is then appended to the prompt, and the
model is asked to fix the error, either by regenerating the program from scratch or by editing the
existing program. Fig. 3 shows a valid outcome that fixes the error by making tag an owned copy
of the header rather than a borrow from msg. The temporary immutable borrow used to create this
copy ends before msg.drain takes a mutable borrow, so the two borrows do not overlap and the
program satisfies Rust’s rules.
   This feedback loop pays for its simplicity      1 fn fmt_msg(msg: &mut String) -> String {
through delayed feedback. In Fig. 1, the bor- 2 let tag = msg[..HEADER_SIZE].to_string();
row conflict already manifests at Line 4. How- 3 msg.drain(..HEADER_SIZE);
ever, compiler feedback is obtained only after     4    let prio = tag.starts_with("HIGH");
the model finishes generating the entire func- 5 let body = msg;
tion at Line 8. For longer programs in prac- 6 let n = body.lines().count();
tice, early mistakes can influence subsequent      7    format!("{} {}: {}", prio, n, body)
generation and snowball before the model           8 }
receives any signal from the compiler. As a
result, additional mistakes can be introduced Fig. 3. The regenerated Rust program above compiles
                                                 after a post-generation compiler feedback round.
and multiple errors may be reported together
in a single diagnostic bundle, making each repair attempt harder and slowing the overall trial-and-
error design process.

Constrained Decoding. Constrained decoding offers an alternative to compiler feedback loops.
It exploits the autoregressive nature of LLM generation by intervening during decoding, rather
than waiting until the entire program has been emitted. Specifically, constrained decoding relies on
a prefix checker P : Σ∗ → B, where P (𝑐) = true if the current output 𝑐 can still be extended into a
full program in 𝐿, or formally, if ∃𝑤 . 𝑐 ◦ 𝑤 ∈ 𝐿. At each decoding step, candidate tokens are filtered
through P, so that only tokens 𝑡 satisfying P (𝑐 ◦ 𝑡) = true may be selected. As a result, invalid
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                           1:5


continuations are ruled out as soon as they arise, and every generated partial program remains a
prefix of some valid program in 𝐿.
   Prefix checking solves a different problem from conventional compilation: the former must reason
about partial programs, whereas the latter assumes full programs as input. This creates a major
implementation burden. Existing compiler infrastructure cannot be used directly, so constrained
decoding systems must often reimplement the relevant language semantics for prefix checking. For
general-purpose programming languages, matching the behavior of the full compiler in this way
is impractical. For example, the compiler-related part of the Rust codebase alone contains more
than 600k lines of code [47]. As a result, existing constrained decoding systems either enforce only
syntax [4, 39, 53] or cover a restricted subset of typing [31, 34].
   Assume for now that a (well-implemented)            1 fn fmt_msg(msg: &mut String) -> String {
constrained decoding engine for Rust is avail- 2 let tag = &msg[..HEADER_SIZE];
able, and let us again examine the example pro- 3 msg.drain(..HEADER_SIZE);
gram in Fig. 1. Constrained decoding has no ef- 4 let prio = tag.
fect as long as each next token keeps the partial
output extendable to a valid program. Thus, the Fig. 4. Constrained decoding rejects . as it leads to a
                                                     dead-end program prefix.
model generates the same prefix up to let prio
= tag, shown in Fig. 4. This prefix is still valid: tag may refer to the prefix of an identifier to be
defined later, such as a function name. However, when selecting the next token, the . used in the
original program must be rejected by prefix checking. Choosing . commits tag to the existing
variable, which triggers the same borrow conflict. Therefore, to remain on a valid path, the model
must choose the unnatural use-before-definition continuation.
   This example exposes two further costs of constrained decoding. First, constrained decoding
silently filters out the token . and can only shape future continuations. The model is never told why
the token was rejected, nor can it revise the already generated prefix, as the repair in Fig. 3 would
require. The only way forward is to force the model onto the low-probability use-before-definition
path described above. This can degrade global generation quality, especially when the rejection is
due to non-local semantic constraints such as Rust’s borrow checking [4, 23, 39]. Second, filtering
and resampling tokens require white-box access to the model’s next-token distribution, which rules
out the closed-weight frontier models that currently dominate coding workflows in practice.


Generative Compilation on the Running Example. Prior work has made valuable progress on
addressing the limitations of constrained decoding from the perspective of probabilistic sampling [4,
12, 23, 25, 39, 45, 52]. In contrast, our generative compilation approach aims to explore a different
route. Like constrained decoding, it operates on partial programs rather than waiting for a full
program. Like conventional compilation, however, it produces textual feedback rather than altering
the sampling process. Crucially, it does so through a lightweight implementation that largely reuses
existing compiler infrastructure and supports black-box models available only through APIs. As a
result, generative compilation addresses the limitations of the two strategies above.
   We now use the running example to sketch how generative compilation handles partial programs.
The key idea behind it is to seal partial programs, turning them into full programs that can be
checked by a conventional compiler. From the discussion above, the error in Fig. 1 already manifests
when generation reaches the prefix in Fig. 4, including .. There, the program has committed to
referring tag to the previously defined variable, which violates Rust’s borrow-checking rules.
Through a series of rule applications, our sealor transforms this partial program into the full
program shown in Fig. 5. The sealed program preserves the access to tag at Line 4. It then inserts a
generic placeholder, holeval () at Line 5, which represents an arbitrary well-typed value. In this
1:6                           Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


example, it is a value of the function’s String return type. Finally, the sealor closes the function at
Line 6 such that the program is syntactically well-formed.
   Compiling the sealed program exposes the          1 fn fmt_msg(msg: &mut String) -> String {
same semantic issue as the full program in           2    let tag = &msg[..HEADER_SIZE];
Fig. 1: tag still borrows from msg across the call   3    msg.drain(..HEADER_SIZE);
to msg.drain. Thus, the Rust compiler rejects        4    &tag;
Fig. 5 with a similar borrow-checking diagnos- 5 hole ()
                                                              val
tic. Compared with the partial program in Fig. 4, 6 }
the sealed program has only inserted holeval (),
which does not introduce type errors, and com- Fig. 5. A full Rust program produced by our sealor.
pleted the missing syntax. Thus, the borrow-checking error reported on the sealed program reflects
a genuine error already committed by the partial program. This is one of the guarantees we aim
to obtain from the sealor: compiler errors on sealed programs should correspond to errors in the
original partial programs, rather than artifacts of sealing.
   We then map the diagnostic produced on the sealed program back to the partial program by
comparing source-code spans. The model receives the partial program together with the mapped
diagnostic, but never sees the sealed program itself. With this feedback, it ultimately produces the
same repaired program as in Fig. 3, making tag an owned copy rather than a borrow from msg.
Generative compilation therefore provides the relevant feedback four and a half lines earlier than
post-generation feedback, when the error first becomes unavoidable.

3     Generative Compilation
Next, we formally define generative compilation in a generic, language-agnostic form.

3.1    Generative Compilers and Sealors
Generative Compilers: Definition. A generative compiler is a function G : Σ∗ → B × Σ∗ . That
is, it has the same interface as a conventional compiler and returns a Boolean verdict ok together
with a textual diagnostic err. However, instead of checking whether a complete program belongs to
𝐿, it performs prefix checking, i.e., whether a partial program 𝑐 admits a valid completion. Unlike
constrained decoding, a generative compiler retains compiler diagnostics: err is empty whenever
ok = true and otherwise provides a textual explanation, rather than a silent rejection signal.
Generative Compilers: Completeness and Soundness. We say that a generative compiler
G accepts 𝑐 when it returns a positive verdict on 𝑐, i.e., when G(𝑐) = (true, ""). It is complete on a
class of programs X ⊆ Σ∗ if for all 𝑐 ∈ X, ∃𝑤 . 𝑐 ◦ 𝑤 ∈ 𝐿 implies that G accepts 𝑐. It is sound on X if
for all 𝑐 ∈ X, G accepts 𝑐 implies ∃𝑤 . 𝑐 ◦ 𝑤 ∈ 𝐿. Intuitively, completeness rules out rejecting partial
programs that admit valid extensions, whereas soundness rules out accepting dead-end partial
programs. We say G is globally complete or sound, when X = Σ∗ . G is exact on X iff it is sound
and complete on X. Note that the first output of G(𝑐) can be viewed as a prefix checker, inheriting
the corresponding notions of soundness and completeness [31].
Sealors: Definition. Generative compilation seeks to reuse the existing compiler to obtain rich
feedback and avoid costly reimplementation, while checking partial programs during generation.
This is achieved through a new notion of sealing, which we define now. A sealor is a lightweight,
language-specific transformation S : Σ∗ → Σ∗ that attempts to close the unfinished structure of
a partial program. Its goal is to produce a closed form that a conventional compiler can process,
thereby obtaining a verdict and diagnostic.
   Given a compiler C and a sealor S, the induced generative compiler is defined by GC,S (𝑐) ≔
C(S(𝑐)). This definition abstracts away a practical mismatch: diagnostics produced by C refer
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                          1:7


to the sealed program S(𝑐), whereas the model should receive feedback on the original partial
program 𝑐. This can be addressed by post-processing diagnostics, for example, by mapping source
spans in S(𝑐) back to their corresponding spans in 𝑐. We discuss this implementation detail for
Rust in §6.1; for simplicity, we assume for now that diagnostics are reported on the corresponding
spans of the partial program 𝑐.
Sealors: Completeness and Soundness. We define completeness and soundness for sealors
analogously to generative compilers.
  Definition 3.1 (Sealor Completeness and Soundness). A sealor S is complete on X ⊆ Σ∗ if, for every
𝑐 ∈ X, ∃𝑤 . 𝑐 ◦ 𝑤 ∈ 𝐿 implies S(𝑐) ∈ 𝐿. It is sound on X if, for every 𝑐 ∈ X, S(𝑐) ∈ 𝐿 implies
∃𝑤 . 𝑐 ◦ 𝑤 ∈ 𝐿. It is globally complete (resp. sound) when X = Σ∗ .
   Intuitively, completeness requires that sealing turns every prefix with a valid continuation into a
valid program, whereas soundness requires that sealing not make a dead-end prefix appear valid.
Assuming C is exact, the completeness and soundness of a sealor correspond directly to those of
its induced generative compiler.
  Theorem 3.2 (Sealor Completeness and Soundness lift to the Generative Compiler). Let
C be exact and X ⊆ Σ∗ . If S is complete on X, then GC,S is complete on X. Symmetrically, if S is
sound on X, then GC,S is sound on X.
   Proof. For completeness: take 𝑐 ∈ X such that ∃𝑤 . 𝑐 ◦ 𝑤 ∈ 𝐿. Completeness of S on X gives
S(𝑐) ∈ 𝐿; exactness of C then gives that C accepts S(𝑐), i.e., that GC,S accepts 𝑐. For soundness:
take 𝑐 ∈ X with GC,S accepting 𝑐, i.e., C accepts S(𝑐). Exactness of C gives S(𝑐) ∈ 𝐿; soundness
of S on X then gives ∃𝑤 . 𝑐 ◦ 𝑤 ∈ 𝐿.                                                            □
   These characterizations give semantic proof obligations for a sealor, which can be established
from the metatheory of the target language and then lifted to completeness or soundness of the
induced generative compiler. We dive deep into this for our FR sealor in §5.
Target Guarantees: Global Completeness and Selective Soundness. Achieving both global
completeness and global soundness amounts to exact prefix checking, which is undecidable in
general for expressive semantic constraints [34]. Constrained decoding faces this difficulty at every
decoding step. Because emitted tokens cannot be revisited, it typically requires global soundness
to inductively ensure that generation always remains on a path that admits a valid extension.
Token-level completeness is not required, but highly desirable: rejecting a token prematurely that
could still lead to a valid program may significantly degrade model performance under constraints
[4, 50]. Maintaining both properties token by token pushes constrained decoding toward exact
prefix checking. When constrained decoding should support rich static semantics, this causes
substantial reimplementation effort of the corresponding semantic analysis such as typing [31].
   For generative compilation, the priorities for soundness and completeness change, with incom-
pleteness becoming the more harmful failure mode. Rejecting a partial program that admits a valid
continuation causes the model to discard or revise a prefix from which a correct program could
still be generated, providing spurious feedback that can confuse the model. Meanwhile, soundness
can be relaxed. A rejection triggers revision: the model regenerates based on diagnostic feedback,
allowing to revise already generated tokens. Missing a soundness violation is thus tolerable: the
generative compiler may accept a dead-end prefix and allow generation to continue, but the error
can still be caught by a later check or by final compilation, when more code context is available.
Nevertheless, soundness remains valuable where it can be obtained cheaply, because it lets on-the-
fly feedback arrive as early as possible. Therefore, for generative compilation, we target global
completeness together with soundness on a selected class of programs X ⊊ Σ∗ .
1:8                            Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


                                                                    Generative Compilation
          LLM-Based Code Generation

                                                                  loop:
          whenever a prompt 𝑥 arrives:           prefix 𝑐
                                                                     𝑐 ← latest received prefix
            𝑐 ← ""
                                                                     (ok, err) ← GC,S (𝑐)
            repeat:
                                                                     if ¬ok:
              𝑡 ∼ 𝑀 (· | 𝑥 ◦ 𝑐)
                                                                        𝑥 ← 𝑥 ◦ 𝑐 ◦ err
              𝑐 ←𝑐 ◦𝑡
                                                                        send 𝑥
              send 𝑐
                                                                     if ok and 𝑐 ends with EOS:
            until 𝑡 = EOS                       prompt 𝑥
                                                                        return 𝑐

Fig. 6. We combine generative compilation and LLM-based code generation as two (concurrent) modules.
The LLM streams each generated prefix 𝑐 to the generative compiler; upon rejection, the generative compiler
returns an augmented prompt containing 𝑐 and its diagnostic err, causing generation to restart. The two
modules communicate only through plain text, supporting black-box LLM APIs.


3.2   Combining Generative Compilation and LLM-Based Code Generation
Fig. 6 shows the approach we use in this paper to combine generative compilation with LLM-
based code generation: the two run as (concurrent) modules that exchange only plain text. Other
integration strategies are possible; we discuss them in §8.
   The module on the left represents LLM-based code generation. It performs standard autoregres-
sive decoding, as discussed in §2. Generation is interrupted and restarted whenever the module
receives a new prompt 𝑥 from generative compilation. As token generation proceeds, the module
sends the latest partial program 𝑐 to generative compilation, stopping when EOS is emitted. This
module does not require access to 𝑀’s token distribution or control over its sampling procedure. It
only observes the current partial program 𝑐 as it is generated. For frontier black-box models, this
can be obtained through streaming API responses, where output is returned incrementally rather
than only after completion. Although Fig. 6 illustrates communication at token granularity, the
same design also works when the API returns larger chunks of text.
   The module on the right performs generative compilation. It checks received prefixes using a
latest-wins strategy: incoming prefixes do not interrupt ongoing validation, and prefixes received
during validation are coalesced so that only the newest one is retained. When validation of a
prefix 𝑐 finishes with (ok, err) ≔ GC,S (𝑐), the module acts on the verdict. If ¬ok, it augments
the prompt with 𝑐 and err and sends the revised prompt to the generator. If ok holds and 𝑐 ends
with EOS, it returns 𝑐 as the generated program. Otherwise, 𝑐 is a valid partial program, and the
module begins validating the latest buffered prefix, if one is available. In the common case where
the EOS-terminated prefix is already a complete program, the final check coincides with ordinary
post-generation compiler feedback. More generally, generative compilation and post-generation
feedback are complementary and can always be combined.
   When configured to run concurrently, generative compilation does not block token generation:
the LLM can continue producing code while one prefix is being validated. This avoids waiting for a
compiler result after every token when validation is slower than token sampling. The latest-wins
strategy then retains only the newest prefix generated during validation for the next check. As a
result, a rejection may arrive after the LLM has produced a few additional tokens. This extra work is
modest and limited to the short suffix generated during a single validation, and once the earlier prefix
is rejected, its continuation is discarded in the restarted attempt. When incremental compilation is
available, as in rustc, compilation speed can increase significantly. Generative compilation benefits
also from this, since it is built largely on existing compiler infrastructure.
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                               1:9


      𝑡 ::=               Term                                        𝑣 ::=      Value
         𝑣                  Value                                        𝜀         Unit value
          box 𝑡             Heap allocation                              𝑐         Integer constant
          copy 𝑤            Copy                                         ℓ•        Owning reference
         𝑤                  Move                                         ℓ◦        Borrowed reference
          & [mut] 𝑤         (Mutable) borrow
          {𝑙 𝑡 }            Block                                    𝑇˜ ::=      Partial type
          let mut 𝑥 = 𝑡     Declaration                                 𝑇          Type
         𝑤 =𝑡               Assignment                                  □ 𝑇˜       Partial box
                                                                         ⌊𝑇 ⌋      Moved-out slot
      𝑤 ::=               LVal
        𝑥                   Variable                                 𝑇 ::=       Type
        ∗𝑤                  Dereference                                𝜀           Unit type
                                                                       int         Integer type
      𝑣 ⊥ ::=             Partial value                                & mut 𝑤     Mutable borrow
         𝑣                  Value                                      &𝑤          Shared borrow
         ⊥                  Undefined                                  □𝑇          Box type

                                  Fig. 7. FR’s Syntax, following Pearce [41].


4     FR: A Core Calculus for Rust
In this section, we review Featherweight Rust [41], a compact calculus inspired by Rust’s borrow
system. We present the syntax (§4.1) and typing (§4.2) needed to demonstrate our generative
compilation approach in §5, omitting details that are not essential here. For the full calculus, we
refer readers to Pearce [41].
Why a Core Calculus. To present and analyze our approach formally, we need a language
formalization. Since our target is Rust, this means a formalization for Rust, and it must satisfy two
requirements. First, it should remain close to Rust’s surface syntax, because our approach directly
manipulates Rust source code. Second, it should provide a compact setting in which our approach
can be defined, analyzed, and understood, while still capturing Rust’s most prominent features.
   Existing Rust formalizations do not simultaneously meet these requirements. RustBelt [19],
RustHorn [28], and Aeneas [15] provide powerful foundations for semantic reasoning and verifica-
tion, but they operate at a level of abstraction that is not sufficiently close to the source syntax, and
their developments are necessarily substantial. Oxide [57] is closer to Rust’s surface syntax, but
still introduces significant machinery, making it more elaborate than needed for our purpose.
Why FR. Featherweight Rust (FR) [41] follows the philosophy of Featherweight Java [16]: provide
a concise and minimal proof of type soundness while preserving the essence of the soundness
argument for the full language. Concretely, FR remains close to Rust’s surface syntax and captures
many key aspects of Rust, including copy and move semantics, mutable and immutable borrows,
and lexical lifetimes. Moreover, FR is compact and establishes soundness guarantees.

4.1     Syntax
FR’s syntax is shown entirely in Fig. 7. We highlight some important details in order of appearance.
Move vs. Copy is Syntactic. In Rust, a use of 𝑤 is a copy if its type implements the Copy trait,
and a move otherwise. FR instead makes this distinction syntactically: 𝑤 denotes a move, whereas
copy 𝑤 denotes a copy. This design keeps the operational semantics independent of the type system.
The type system (defined in §4.2) then enforces that copies are only performed on copyable values:
1:10                           Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


copy 𝑤 is well typed only if 𝑤 has type 𝑇 satisfying copy(𝑇 ), FR’s analog of the Copy trait. In our
mechanization, the predicate holds for 𝜀, int, and shared borrows, but not for mutable borrows or
boxes. Treating unit as copyable is a small adaptation relative to Pearce [41].
Lifetimes are Lexical. A block {𝑙 𝑡 } is a sequence of terms separated by semicolons and annotated
by a lifetime. Lifetimes 𝑙, 𝑚 annotate every lexical block {𝑙 𝑡 }. Lifetimes form a partial order 𝑙 ⪰ 𝑚,
which means that 𝑚 is inside 𝑙. This holds exactly when 𝑚’s block is lexically nested inside 𝑙’s, e.g.,
{𝑙 {𝑚 𝑡 }}. We note that modern Rust uses non-lexical lifetimes (NLL), which let a borrow end at its
last use rather than at the enclosing block’s exit. FR’s lexical model admits a substantially simpler
metatheory while capturing the essence of lifetimes and remaining sound.
   The block’s lifetime is written after the opening brace, {𝑙 𝑡 }, rather than after the closing brace
as in Pearce [41] (i.e., {𝑡 }𝑙 ). The two notations denote the same abstract syntax, but placing the
lifetime up front makes it visible that the label is committed at block-entry rather than at block-exit.
This matters for several typing rules in §4.2, which type body terms against the block’s ambient
lifetime: the label must be fixed before the first body term is checked. It also matters for our partial
syntax in §5, where a partial block whose tail is being emitted must already carry its lifetime.
Reference Values Encode Drop Responsibility. Reference values come in two flavors: an
owning reference ℓ • and a borrowed reference ℓ ◦ . Dropping an ℓ • recursively drops the location it
refers to, whereas dropping a ℓ ◦ does not. Encoding this distinction at the value level keeps the
operational semantics independent of the type system. By contrast, the distinction between shared
and mutable references appears only in the type system, not at runtime. Both shared and mutable
borrows therefore evaluate to ℓ ◦ values, since they are non-owning references.
Borrow Types Name the Borrowed LVal. A reference type is either a shared borrow & 𝑤 or a
mutable borrow & mut 𝑤; we write & [mut] 𝑤 if either mode is allowed, where the target is a single
lval (e.g., & 𝑥). Naming the borrowed lval directly in the type allows validating borrow safety by
tracking overlaps and conflicts between borrowed and assigned lvals. In contrast to Pearce [41], we
adopt FR’s follow-up work [40], restricting the 𝑤 to a single lval instead of a set of lvals to establish
cycle-freeness of borrows. This formulation is sufficient in the absence of conditionals.
Partial Types and Values Track Moved-Out Storage. At runtime, a partial value 𝑣 ⊥ extends 𝑣
with the undefined marker ⊥, which marks a slot whose contents have been moved out. At the
type level, a partial type 𝑇˜ extends 𝑇 with □ 𝑇˜ (a box whose contents are themselves partial) and
⌊𝑇 ⌋ (a slot moved out but with its former shape remembered, e.g., ⌊& 𝑥⌋, so re-assignment can be
shape-checked). Every value is trivially a partial value, and every type a partial type. The converses
fail because only the partial forms admit moved-out markers.
Source-Level Fragment. The reference values ℓ • and ℓ ◦ arise only at runtime, as the results of
evaluating box and borrow expressions; a programmer never writes them directly. We call a term
source-level when no reference value appears as a subterm. The language does not require a distin-
guished surrounding block: a top-level program is any term typable from the empty environments
at the root lifetime 𝑙 root . Blocks remain the construct that introduces nested lexical lifetimes.

4.2    Typing
Fig. 8 presents the main typing rules of FR that we use in later sections. Next, we start by introducing
the typing contexts and judgments, followed by the auxiliary functions, and then explain the rules.
We close by stating FR’s type and borrow safety and summarizing our Lean mechanization.
Contexts and Judgments. Typing uses two contexts. The typing environment Γ maps each
declared variable 𝑥 to a slot type ⟨𝑇˜ ⟩𝑚 , recording its partial type 𝑇˜ and the lifetime 𝑚 in which 𝑥
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                                      1:11


                                       𝜎 ⊢𝑣 :𝑇                        Γ1 ⊢ ⟨𝑡 : 𝑇 ⟩𝜎𝑙 ⊣ Γ2
                   [T-Const]                            [T-Box]
                                   Γ ⊢ ⟨𝑣 : 𝑇 ⟩𝜎𝑙 ⊣ Γ              Γ1 ⊢ ⟨box 𝑡 : □𝑇 ⟩𝜎𝑙 ⊣ Γ2

                        Γ ⊢ 𝑤 : ⟨𝑇 ⟩𝑚 copy(𝑇 )                       Γ1 ⊢ 𝑤 : ⟨𝑇 ⟩𝑚 Γ2 = move(Γ1, 𝑤)
                        ¬readProhibited(Γ, 𝑤)                             ¬writeProhibited(Γ1, 𝑤)
            [T-Copy]                                    [T-Move]
                           Γ ⊢ ⟨copy 𝑤 : 𝑇 ⟩𝜎𝑙 ⊣ Γ                            Γ1 ⊢ ⟨𝑤 : 𝑇 ⟩𝜎𝑙 ⊣ Γ2

                               Γ ⊢ 𝑤 : ⟨𝑇 ⟩𝑚                                    Γ ⊢ 𝑤 : ⟨𝑇 ⟩𝑚 mut(Γ, 𝑤)
                           ¬readProhibited(Γ, 𝑤)                                 ¬writeProhibited(Γ, 𝑤)
     [T-ImmBorrow]                                      [T-MutBorrow]
                           Γ ⊢ ⟨& 𝑤 : & 𝑤⟩𝜎𝑙 ⊣ Γ                              Γ ⊢ ⟨& mut 𝑤 : & mut 𝑤⟩𝜎𝑙 ⊣ Γ

                              Γ1 ⊢ ⟨𝑡 1 : 𝑇1 ⟩𝜎𝑙 ⊣ Γ2
                                        ···                           𝑙 ⪰ imm 𝑚       Γ1 ⊢ ⟨𝑡 : 𝑇 ⟩𝜎𝑚 ⊣ Γ2
                             Γ𝑛 ⊢ ⟨𝑡𝑛 : 𝑇𝑛 ⟩𝜎𝑙 ⊣ Γ𝑛+1                  Γ2 ⊢ 𝑇 ⪰ 𝑙     Γ3 = drop(Γ2, 𝑚)
                 [T-Seq]                                [T-Block]
                              Γ1 ⊢ ⟨𝑡 : 𝑇𝑛 ⟩𝜎𝑙 ⊣ Γ𝑛+1                       Γ1 ⊢ ⟨{𝑚 𝑡 } : 𝑇 ⟩𝜎𝑙 ⊣ Γ3

                                                                      Γ1 ⊢ ⟨𝑡 : 𝑇2 ⟩𝜎𝑙 ⊣ Γ2 Γ2 ⊢ 𝑤 : ⟨𝑇˜1 ⟩𝑚
                           Γ1 ⊢ ⟨𝑡 : 𝑇 ⟩𝜎𝑙 ⊣ Γ2
                                                                           Γ2 ⊢ 𝑇˜1 ∼ 𝑇2 Γ2 ⊢ 𝑇2 ⪰ 𝑚
                             𝑥 ∉ dom(Γ2 )                                     Γ3 = write0 (Γ2, 𝑤,𝑇2 )
                        Γ3 = Γ2 [𝑥 ↦→ ⟨𝑇 ⟩𝑙 ]                               ¬writeProhibited(Γ3, 𝑤)
   [T-Declare]                                          [T-Assign]
                  Γ1 ⊢ ⟨let mut 𝑥 = 𝑡 : 𝜀⟩𝜎𝑙 ⊣ Γ3                              Γ1 ⊢ ⟨𝑤 = 𝑡 : 𝜀⟩𝜎𝑙 ⊣ Γ3

  Fig. 8. FR’s typing rules for terms [41]. Grey boxes highlight corrections made by our mechanization.




was declared. The store typing 𝜎 assigns types to runtime locations. 𝜎 is needed only when typing
intermediate execution states; source-level programs are typed under 𝜎 = ∅.
   The typing rules in Fig. 8 use one main judgment: Γ1 ⊢ ⟨𝑡 : 𝑇 ⟩𝜎𝑙 ⊣ Γ2 . It asserts that, in lifetime 𝑙,
the term 𝑡 has type 𝑇 , and that evaluating 𝑡 transforms the environment from Γ1 to Γ2 . Threading the
environment through the judgment in this input/output style makes the type system flow-sensitive.
For example, after moving from an lval 𝑤, the corresponding slot in Γ2 is marked moved out, so a
subsequent use of 𝑤 is rejected. Declarations and assignments similarly update the environment in
a way that affects subsequent typing decisions. These effects cannot be captured by a traditional
flow-insensitive type system, in which each variable has a single fixed type throughout its scope.
   Fig. 8 uses three auxiliary judgments only as premises of the main rules: LVal typing, type
well-formedness, and shape compatibility. LVal typing, Γ ⊢ 𝑤 : ⟨𝑇˜ ⟩𝑚 , determines the partial type of
𝑤 and the lifetime 𝑚 in which it can safely be used. Type well-formedness, Γ ⊢ 𝑇 ⪰ 𝑙, holds when
every borrow in 𝑇 targets storage that outlives 𝑙. Shape compatibility, Γ ⊢ 𝑇˜1 ∼ 𝑇˜2 , holds when two
partial types agree in structural shape modulo lifetimes and undefined components, while still
comparing the types beneath any undefined components. Each of these three has routine rules, so
we defer to [41] for their full definition.

Auxiliary Functions. The typing rules also use FR’s standard auxiliary functions [41]. Each is
defined by straightforward case analysis over its input so we summarize their roles rather than
reproduce the full definitions. Several auxiliary predicates characterize accessibility. copy(𝑇 ) holds
when 𝑇 admits copy semantics. readProhibited(Γ, 𝑤) holds when 𝑤 is currently mutably borrowed
in Γ, whereas writeProhibited(Γ, 𝑤) holds when it is borrowed in either mode. mut(Γ, 𝑤) holds
when 𝑤 is mutably accessible: no dereference in 𝑤 steps through an immutable borrow.
1:12                          Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


   Three update functions modify the environment. move(Γ, 𝑤) marks the value at 𝑤 as moved out
by replacing the corresponding component of its slot type with ⌊𝑇 ⌋, where 𝑇 is the component’s
former type. write0 (Γ, 𝑤,𝑇 ) updates Γ to reflect assigning a value of type 𝑇 through 𝑤. drop(Γ, 𝑚)
removes all bindings declared in lifetime 𝑚.

Typing Rules for Terms. Each rule in Fig. 8 types one corresponding term form from Fig. 7.
T-Const checks literals and runtime values against 𝜎 and leaves the environment unchanged. T-Box
assigns box 𝑡 the type □ 𝑇 when 𝑡 has type 𝑇 , while preserving any environment changes caused by
evaluating 𝑡. T-Copy and T-Move encode Rust’s familiar distinction between copy and move seman-
tics. T-Copy permits copying an lval only when its type satisfies copy and readProhibited is false.
T-Move returns the lval’s type, requires writeProhibited to be false, and marks the corresponding
component of its slot as moved out via move.
   T-ImmBorrow and T-MutBorrow simulate Rust’s distinction between shared and mutable
borrows, establishing their mutual exclusion. T-ImmBorrow creates a shared borrow only when 𝑤
is not currently mutably borrows, i.e., readProhibited(Γ, 𝑤) is false. This permits multiple shared
borrows while excluding simultaneous mutable borrows. T-MutBorrow creates a mutable borrow
only when 𝑤 is not currently borrowed in any way, i.e., writeProhibited(Γ, 𝑤) is false. This reflects
Rust’s requirement that mutable access excludes any simultaneous borrows. Additionally, 𝑤 must be
mutable. The borrow expression itself leaves the environment unchanged. Its borrow information
is recorded only when the resulting reference is stored through a declaration or assignment.
   T-Seq threads the environment through a sequence of terms from left to right and gives the
sequence the type of its last term. T-Block types {𝑚 𝑡 } in its own lifetime 𝑚. Its result type must
be well formed in the enclosing lifetime 𝑙, which prevents borrows of block-local storage from
escaping. After exiting the block, drop removes any bindings declared in 𝑚. The premise 𝑙 ⪰ imm 𝑚,
requiring 𝑚 to be the immediate child of 𝑙, corrects a missing assumption in FR’s typing that 𝑚 is
inside 𝑙. We specify this as an immediate-child relationship, as one can always choose an immediate
child 𝑚 in place of any assigned 𝑚 ′ inside 𝑙.
   T-Declare first types the initializer and then extends the resulting environment with a fresh
binding 𝑥 ↦→ ⟨𝑇 ⟩𝑙 . The freshness check is made in the post-initializer environment Γ2 , rather than
in Γ1 by Pearce [41]: otherwise an initializer can redeclare 𝑥 and return it to the environment before
the outer declaration installs its binding. T-Assign types the right-hand side to obtain Γ2 and 𝑇2 ,
then resolves the left-hand side in Γ2 . The lval-typing environment Γ2 is another correction to FR’s
typing, since evaluating the right-hand side may re-type the path under 𝑤 (e.g., ∗𝑝 = {𝑝; 𝑚𝑢𝑡 𝑤 }
moves 𝑝 out, thus making access to ∗𝑝 invalid). The rule then requires 𝑇2 to be shape-compatible
with the destination’s stored partial type and well formed for the destination’s declaration lifetime
𝑚, updates the environment via write0 , and requires writeProhibited(Γ3, 𝑤) to be false.

Type and Borrow Safety. Pearce [41] establish type and borrow safety for FR: a well-typed
program does not get stuck, and if it terminates, it does so in a store that respects the borrow
invariant, i.e., free of dangling or duplicated owning references and with at most one mutable
borrow per location. We leverage this result to treat FR as a meaningful proxy for a usefully complex
and expressive type system, motivating our choice of FR.

Mechanization and Corrections. We fully mechanize FR in Lean, including syntax, typing,
operational semantics, and type and borrow safety proofs. In this process, we corrected the stated
typing rules in several places. The main corrections to T-Block, T-Declare, and T-Assign are
marked with grey boxes in Fig. 8. Beyond these typing adaptations, we correct the rules for
unit values, align the runtime semantics with the reference implementation by Pearce [41], and
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                                  1:13

b𝑡 ::=             Partial term                                  b⇝𝑡                    any 𝑡
     b               Nothing decoded                             b𝑣 ⇝ 𝑣                 if b𝑣 is a prefix of 𝑣
    𝑡                Full term                                     𝑡 ⇝𝑡                 unconditionally
    b𝑣               Partial value                          box b𝑡 ⇝ box 𝑡              if b𝑡 ⇝ 𝑡
     box b𝑡          Partial heap allocation              copy 𝑤  b ⇝ copy 𝑤            if 𝑤 b ⇝𝑤
     copy 𝑤   b      Partial copy                                 b
                                                                  𝑤 ⇝𝑤                  if 𝑤 b ⇝𝑤
    𝑤b               Partial move, or assign LHS                  𝑤 ⇝𝑤 =𝑡
                                                                  b                     if 𝑤 b ⇝ 𝑤, any 𝑡
     & [mut] 𝑤  b    Partial (mutable) borrow          & [mut] 𝑤 ⇝ & [mut] 𝑤
                                                                  b                     if 𝑤 b ⇝𝑤
     {𝑙 𝑡; b𝑡        Unclosed block, partial tail          { 𝑡 0 ; 𝑡 ⇝ { 𝑡 0 ; 𝑡; 𝑡 1 }
                                                            𝑙      b    𝑙                  b
                                                                                        if 𝑡 ⇝ 𝑡, any 𝑡 1
     let mut 𝑥b      Declaration, partial name         let mut 𝑥b ⇝ let mut 𝑥 = 𝑡 if 𝑥b is a prefix of 𝑥, any 𝑡
     let mut 𝑥 = b𝑡 Declaration, partial init       let mut 𝑥 = b𝑡 ⇝ let mut 𝑥 = 𝑡 if b𝑡 ⇝ 𝑡
    𝑤 = b𝑡           Assignment, partial RHS                𝑤 = b𝑡 ⇝ 𝑤 = 𝑡              if b𝑡 ⇝ 𝑡
      Fig. 9. Our partial syntax for FR terms.       Fig. 10. Our realization relation for FR terms (b𝑡 ⇝ 𝑡).



strengthen the progress invariant with borrow safety and the linearizability property of Payet et al.
[40]. We refer to our extended writeup alongside our mechanization.

5     Instantiating Generative Compilation on FR
In this section, we instantiate the generic framework of generative compilation (§3) by defining a
concrete sealor for FR. We deliberately make this sealor syntax-guided, keeping both its implemen-
tation and its proof lightweight, thereby making the approach easier to adopt for real languages.
Despite this, we show that it is globally complete (§5.3) and sound on an important class of partial
programs (§5.4). The developments in this section are fully mechanized in Lean.

5.1      Partial Syntax and Realization for FR
We first define FR’s partial syntax, which lays the basis for the sealor definition. It describes prefixes
of syntactically valid FR programs. We then define realization, which relates a partial-syntax string
to a full-syntax string obtained by extending the partial string. This relation is useful because
completeness and soundness connect partial programs with their possible full programs.

Partial Syntax. We define partial syntax relative to FR’s full syntax in Fig. 7, focusing on source-
level terms that may arise during autoregressive generation. Fig. 9 gives the resulting grammar
of partial terms b𝑡, which extends over a full term by allowing one of its parts to be only partially
generated. The first two cases, b and 𝑡, respectively describe the two endpoints: no part of the
current term has yet been generated, and generation has produced a full term. Each remaining
production follows one term form from Fig. 7, replacing the component currently being generated
with its partial counterpart. For example, b𝑣 denotes a partial value, and copy 𝑤  b a copy term with a
partial lval. { 𝑡; 𝑡 represents an unclosed block with a partial tail. The lifetime label 𝑙 is an internal
               𝑙   b
annotation, fixed once the opening brace is generated, rather than text generated by the model.
The production 𝑤   b covers both moves and assignments, which share a prefix until an = is generated.
   Partial lvals 𝑤 and partial values b𝑣 complete the picture. They are not listed in Fig. 9 but are
                  b
described in prose next. A partial lval is either b, a full 𝑤, a partially generated variable name 𝑥,   b
or a dereference ∗𝑤 whose operand remains partial. A partial value 𝑣 is either a full value 𝑣 or a
                      b                                                   b
partially generated integer constant; the unit value 𝜀 is always full.
   For simplicity, we omit prefixes concerning only keywords, such as let mut, &mut, or prefixes
of either. Such prefixes contain no partially generated term, lval, or value for the sealor to preserve,
so we fold them into the case of b.
1:14                           Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


Realization of Partial Programs. Realization models autoregressive generation: decoding may
add text at the unfinished frontier, but cannot revise an earlier prefix. It differs from sealing, which
may discard or alter unfinished fragments. This distinction will be made concrete once we introduce
SFR . Our completeness result presented later in this section connects these two notions.
   We write b𝑡 ⇝ 𝑡 when 𝑡 realizes b𝑡, and define this relation case by case in Fig. 10. In most cases,
realization retains the term form already determined by the generated prefix and recurses on its
unfinished subterm. The two clauses for 𝑤    b make its Move/Assignment ambiguity explicit: once
𝑤 realizes an lval 𝑤, the term may realize either the move 𝑤 or an assignment 𝑤 = 𝑡 with any
b
                                           b ⇝ 𝑤 has four cases: b ⇝ 𝑤 for any 𝑤; 𝑤 ⇝ 𝑤; 𝑥b ⇝ 𝑥
right-hand side 𝑡. For lvals, the relation 𝑤
when 𝑥 is a prefix of 𝑥; and ∗𝑤 ⇝ ∗𝑤 when 𝑤
       b                        b              b ⇝ 𝑤.

                                                                  SFR (b𝑡) =
5.2    SFR : A Syntax-Guided Sealor for FR                          𝜀                      if b𝑡 = b
Fig. 11 defines our syntax-guided sealor SFR by case anal-          𝑡                      if b𝑡 = 𝑡
                                                                    𝜀                      if b𝑡 = b𝑣
ysis over partial syntax. It maps each partial term form
                                                                    SFR (𝑡b′ )             if b𝑡 = box 𝑡b′
to a full FR term. As required by the generic definition,           𝜀                      if b𝑡 = copy 𝑤   b
SFR is total. Prefixes outside the partial syntax are han-          𝜀                      if 𝑡 = 𝑤
                                                                                              b     b
dled separately by returning them unchanged, so that the            𝜀                      if b𝑡 = & [mut] 𝑤  b
underlying compiler may report a syntax error.                      {𝑙 𝑡; SFR (𝑡b′ ); 𝜀}   if b𝑡 = {𝑙 𝑡; 𝑡b′
   At a high level, SFR abstracts type checking through a           𝜀                      if b𝑡 = let mut 𝑥b
syntax-guided transformation. Rather than deciding ex-              SFR (𝑡b′ )             if b𝑡 = let mut 𝑥 = 𝑡b′
actly whether a partial term admits a well-typed comple-            SFR (𝑡b′ )             if b𝑡 = 𝑤 = 𝑡b′
tion, it constructs a term whose well-typedness is neces- Fig. 11. Our syntax-guided sealor SFR .
sary for that of every possible completion, thereby pre-
serving completeness. Accordingly, sealing preserves generated structure when it exposes useful
typing obligations, while abstracting away other obligations when they require information not yet
generated or analysis beyond syntax. Several cases therefore seal directly to 𝜀: copy 𝑤,b 𝑤,b & [mut] 𝑤,
                                                                                                      b
and let mut 𝑥. Their unfinished components must be resolved before the corresponding typing
               b
rules can establish useful premises. Here, 𝜀 provides a well-typed placeholder with no additional
typing obligations. Moreover, for let mut 𝑥 = b𝑡 and 𝑤 = b𝑡, SFR recurses only on b𝑡. It drops the
enclosing declaration or assignment, including the declared variable 𝑥 or assigned lval 𝑤, and hence
their associated typing obligations.
   This abstraction is deliberately not maximally aggressive. With completeness preserved, we
seek to retain as much soundness as possible. Fully generated terms are therefore unchanged,
including both a standalone 𝑡 and all already-full terms 𝑡 inside an unclosed block. Furthermore,
SFR preserves partial subterms that can themselves contain generated structure relevant to later
typing, rather than discarding them outright. Thus, it recurses on b𝑡 in box b𝑡, {𝑙 𝑡; b𝑡, let mut 𝑥 = b𝑡,
and 𝑤 = b𝑡. At the same time, we do not make SFR more sound at the cost of a lightweight design.
For instance, in let mut 𝑥 = b𝑡 or 𝑤 = b𝑡, one could use the type of 𝑥 or 𝑤 to further constrain b𝑡. We
do not pursue this in SFR , because it would require typing information beyond our syntax-guided
design. This would add implementation cost without substantial benefit, since SFR is already sound
on an important class of programs, as we show in §5.4.
   A few remaining cases complete the definition. b seals to 𝜀, since either no part of the current
term has been generated or the generated prefix consists only of keywords. An unfinished partial
value 𝑣b also seals to 𝜀. Although a partially generated integer already suggests type int, we choose
this simpler syntax-guided rule rather than recover that information, at a small cost to soundness.
The bare 𝑤 b production likewise seals to 𝜀: before an = is generated, it remains ambiguous between
a move and the left-hand side of an assignment, and sealing it as either would prematurely commit
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                                           1:15


to one interpretation. Finally, for {𝑙 𝑡; b𝑡, the sealor appends a trailing 𝜀 and the closing brace after
sealing b𝑡, ensuring that the result is a closed block.

5.3       Global Completeness of SFR
SFR ’s design was motivated by global completeness, which we formally prove next. We first show
that whenever a partial term realizes a well-typed full term, sealing the partial term with SFR also
yields a well-typed term.
  Theorem 5.1 (S Maintains Well-Typedness of Realizations). For all partial terms b𝑡, typing
                      FR
environments Γ, Γ ′ , types 𝑇 , lifetimes 𝑙, and store typings 𝜎:
              ∃𝑡 . b𝑡 ⇝ 𝑡 ∧ Γ ⊢ ⟨𝑡 : 𝑇 ⟩𝜎𝑙 ⊣ Γ ′ =⇒ ∃𝑇 ★, Γ★ . Γ ⊢ ⟨SFR (b𝑡) : 𝑇 ★⟩𝜎𝑙 ⊣ Γ★ .
   The proof follows Fig. 9 row by row, in order, naming each case after that row’s description.
   Proof. Fix b𝑡 and, using the hypothesis, a witness 𝑡 with b𝑡 ⇝ 𝑡 and Γ ⊢ ⟨𝑡 : 𝑇 ⟩𝜎𝑙 ⊣ Γ ′ . We proceed
by induction on the derivation of b𝑡 ⇝ 𝑡.
• Immediately sealed to 𝜀: b𝑡 = b, b𝑡 = b𝑣, b𝑡 = copy 𝑤, b b𝑡 = 𝑤,   b b𝑡 = & [mut] 𝑤,   b or b𝑡 = let mut 𝑥.  b In every
   case SFR (𝑡) = 𝜀 unconditionally, well-typed by T-Const.
             b
• Full term: b𝑡 = 𝑡. Here SFR (b𝑡) = 𝑡, and the conclusion follows immediately from the premise.
• Partial heap allocation: b𝑡 = box 𝑡b′ , so 𝑡 = box 𝑡 ′ with 𝑡b′ ⇝ 𝑡 ′ . By T-Box, 𝑡 ′ is well-typed in Γ; by
   the IH, so is SFR (b𝑡) = SFR (𝑡b′ ).
• Unclosed block with partial tail: b𝑡 = {𝑚 𝑡 1 ; . . . ; 𝑡𝑘 −1 ; b𝑡 𝑘 , so 𝑡 = {𝑚 𝑡 1 ; . . . ; 𝑡𝑛 } for some 𝑛 ≥ 𝑘 with
  b𝑡 ⇝ 𝑡 , and by definition S (b𝑡) = {𝑚 𝑡 ; . . . ; 𝑡 ; S (b𝑡 ); 𝜀}. Inverting the typing of 𝑡 via
      𝑘      𝑘                         FR             1        𝑘 −1    FR   𝑘
  T-Block and T-Seq gives contexts Γ = Γ0, Γ1, . . . , Γ𝑛 and types 𝑇1, . . . ,𝑇𝑛 with Γ𝑖 −1 ⊢ ⟨𝑡𝑖 : 𝑇𝑖 ⟩𝜎𝑚 ⊣ Γ𝑖
  for every 𝑖. By the IH, SFR (b𝑡 𝑘 ) is well-typed in Γ𝑘 −1 ; a final 𝜀 typed by T-Const closes the
  sequence by T-Seq, and T-Block then gives SFR (b𝑡) well-typed in Γ.
• Declaration, partial init: b𝑡 = let mut 𝑥 = 𝑡b′ , so 𝑡 = let mut 𝑥 = 𝑡 ′ with 𝑡b′ ⇝ 𝑡 ′ . By T-Declare, 𝑡 ′
  is well-typed in Γ; by the IH, so is SFR (b𝑡) = SFR (𝑡b′ ).
• Assignment, partial RHS: b𝑡 = 𝑤 = 𝑡b′ , so 𝑡 = 𝑤 = 𝑡 ′ with 𝑡b′ ⇝ 𝑡 ′ . By T-Assign, 𝑡 ′ is well-typed in
  Γ; by the IH, so is SFR (b𝑡) = SFR (𝑡b′ ).
                                                                                                              □
    Let 𝐿FR denote the set of well-typed top-level FR terms. As discussed in §4, FR’s top-level terms
are typed under the root lifetime 𝑙 root , empty typing environment, and empty store typing. That
is, 𝐿FR := { 𝑡 | ∃𝑇 , Γ. ∅ ⊢ ⟨𝑡 : 𝑇 ⟩∅
                                     𝑙 root
                                            ⊣ Γ }. Theorem 5.1 is stronger than the top-level result we
ultimately need: it permits arbitrary initial typing environments and store typings, as well as
lifetime. This allows the proof to apply to intermediate terms within larger programs. Specializing
it to top-level typing yields completeness for top-level partial syntax.
    Corollary 5.2 (S is Globally Complete for Partial Syntax). For every partial term b𝑡,
                           FR

                             ∃𝑡 . b𝑡 ⇝ 𝑡 ∧ 𝑡 ∈ 𝐿FR =⇒ SFR (b𝑡) ∈ 𝐿FR .
   Proof. Fix a partial term b𝑡 satisfying the premise, and choose a term 𝑡 such that b𝑡 ⇝ 𝑡 and
𝑡 ∈ 𝐿FR . By the definition of 𝐿FR , there exist 𝑇 and Γ such that ∅ ⊢ ⟨𝑡 : 𝑇 ⟩∅
                                                                               𝑙 root
                                                                                      ⊣ Γ. Applying
Theorem 5.1 with initial typing environment and store typing ∅ yields some 𝑇 ★ and Γ★ such that
                    𝑙 root
∅ ⊢ ⟨SFR (b𝑡) : 𝑇 ★⟩∅      ⊣ Γ★. Hence SFR (b𝑡) ∈ 𝐿FR .                                           □
  The generic framework defines global completeness over arbitrary strings rather than partial-
syntax terms, so we finally lift Theorem 5.2 to that setting.
1:16                                   Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


  Theorem 5.3 (SFR Is Globally Complete for Arbitrary Strings). The sealor SFR is globally
complete with respect to FR, for arbitrary strings as input, in the sense of Theorem 3.1.
   Proof. Let 𝑠 ∈ Σ∗ satisfy ∃𝑤 . 𝑠 ◦ 𝑤 ∈ 𝐿FR . As 𝑠 ◦ 𝑤 is a well-typed FR term, parsing 𝑠 yields a
partial term b𝑡, with keyword-only prefixes represented by b. And parsing 𝑠 ◦ 𝑤 yields a term 𝑡 such
that b𝑡 ⇝ 𝑡 and 𝑡 ∈ 𝐿FR . By Theorem 5.2, SFR (b𝑡) ∈ 𝐿FR . This is exactly the result of sealing 𝑠. Hence
SFR accepts every string with a well-typed FR continuation. If 𝑠 does not yield a partial term, then
it contains a syntax error and cannot satisfy ∃𝑤 . 𝑠 ◦ 𝑤 ∈ 𝐿FR . Here, SFR returns 𝑠 unchanged. □

  Finally, based on Theorem 3.2, the global completeness of the corresponding generative compiler
GFR (𝑠) ≔ CFR (SFR (𝑠)) follows from that of SFR and an exact compiler CFR for FR.

5.4    Selective Soundness of SFR
While SFR achieves global completeness, it also abstracts away information that soundness would
need in order to remain lightweight and syntax-guided. For instance, SFR (copy 𝑥)   b = 𝜀 is accepted
                                b
unconditionally, even when 𝑥 can only realize a moved-out variable. We nevertheless identify an
important class on which SFR is sound: statement boundaries, where generation has finished one or
more complete statements in a block and is about to begin the next. This is a useful guarantee in
practice because statement boundaries occur frequently during generation.
   We now give formal characterizations of this property. We call b𝑡 a statement boundary if b𝑡 = {𝑙 𝑡; b.
That is, after a series of full terms in a block, the model is exactly at the point immediately
after a semicolon, before any token of what follows has streamed in. Let Xstmt ≔ { {𝑙 𝑡; b |
𝑡 complete, 𝑙 a lifetime }, i.e., the class of statement boundaries.
   Lemma 5.4 (Statement Boundaries Realize S ’s Output). For every b𝑡 ∈ X , b𝑡 ⇝ S (b𝑡).
                                                               FR                                 stmt         FR

   Proof. Write b𝑡 = {𝑙 𝑡; b, such that SFR (b𝑡) = {𝑙 𝑡; SFR ( b); 𝜀} = {𝑙 𝑡; 𝜀; 𝜀}. Instantiate the unclosed
block case of realization ⇝ with b𝑡 = b completing to 𝑡 ≔ 𝜀 and 𝑡 1 ≔ 𝜀. This gives exactly
{𝑙 𝑡; b ⇝ {𝑙 𝑡; 𝜀; 𝜀}, i.e., b𝑡 ⇝ SFR (b𝑡).                                                                 □

  Theorem 5.5 (SFR Reflects Well-Typedness onto Realizations at Statement Boundaries).
For all b𝑡 ∈ Xstmt , typing environments Γ, Γ★, types 𝑇 ★, lifetimes 𝑙, and store typings 𝜎:
                    Γ ⊢ ⟨S (b𝑡) : 𝑇 ★⟩𝑙 ⊣ Γ★ =⇒ ∃𝑡,𝑇 , Γ ′ . b𝑡 ⇝ 𝑡 ∧ Γ ⊢ ⟨𝑡 : 𝑇 ⟩𝑙 ⊣ Γ ′ .
                           FR              𝜎                                               𝜎

   Proof. By Theorem 5.4, b𝑡 ⇝ SFR (b𝑡). By the hypothesis, SFR (b𝑡) is a well-typed completion.                    □

  As with Theorem 5.1, Theorem 5.5 is stronger than the top-level result we need. Specializing it
yields selective soundness at top level.
    Corollary 5.6 (SFR is Sound for Partial Syntax at Statement Boundaries). For every
b𝑡 ∈ X , S (b𝑡) ∈ 𝐿 =⇒ ∃𝑡 . b𝑡 ⇝ 𝑡 ∧ 𝑡 ∈ 𝐿 .
      stmt    FR            FR                         FR

    Proof. Fix 𝑡 ∈ Xstmt with SFR (𝑡) ∈ 𝐿FR . By the definition of 𝐿FR , there exist 𝑇 ★ and Γ★ such that
                 b                       b
                     𝑙 root
 ∅ ⊢ ⟨SFR (b𝑡) : 𝑇 ★⟩∅       ⊣ Γ★. Applying Theorem 5.5 with initial typing environment, store typing
 ∅, and ambient lifetime 𝑙      rootyields that b𝑡 ⇝ 𝑡 and ∅ ⊢ ⟨𝑡 : 𝑇 ⟩𝑙root ⊣ Γ ′ for some 𝑇 , Γ ′ . The latter is
                                                                            ∅
equivalent to 𝑡 ∈ 𝐿FR .                                                                                             □

   We lift Theorem 5.6 from partial-syntax terms to arbitrary strings.
  Theorem 5.7 (SFR Is Sound at Statement Boundaries, for Arbitrary Strings). The sealor
SFR is sound with respect to FR on Xstmt , for strings as input, in the sense of Theorem 3.1.
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                          1:17


  Proof. Let 𝑠 ∈ Xstmt satisfy SFR (𝑠) ∈ 𝐿FR . Since SFR (𝑠) is a well-typed FR term, parsing 𝑠 yields
a partial term b𝑡 ∈ Xstmt , with SFR (𝑠) = SFR (b𝑡). By Theorem 5.6, ∃𝑡 . b𝑡 ⇝ 𝑡 ∧ 𝑡 ∈ 𝐿FR . This 𝑡 is
realized by some string 𝑠 ◦ 𝑤. Hence 𝑠 is completable.                                              □
  Finally, based on Theorem 5.3 and Theorem 5.7, SFR is exact at statement boundaries. So is GFR
according to Theorem 3.2.

6     From FR to Real Rust
We now carry the methodology of §5 from FR to real Rust by presenting our Rust sealor, SRS .
Inherited from FR. We design SRS following the same principles as FR’s sealor SFR (§5.2). It
remains lightweight and syntax-guided in most cases, discards typing obligations when needed
for completeness, and adds targeted analysis where doing so improves soundness. It preserves
already-generated structure verbatim and recurses on the still-partial frontier. As with SFR , the
goal is global completeness together with selective soundness.
   For each Rust feature, we describe its syntactic shape, the partial forms the sealor may encounter,
and the sealor rules used to close those partial forms. For readability, we reuse FR’s notation where
applicable and introduce new notation only for constructs specific to Rust.
Not Inherited from FR. Two aspects of this section depart from §5. First, Rust is much larger
than FR. The Rust sealor must therefore handle constructs with no FR counterpart, as well as
constructs that resemble FR but differ in syntactic structure or typing behavior. We discuss a
representative selection of such features across this section. Second, we give informal, per-feature
arguments for typing behavior, completeness, and soundness, rather than the formal, mechanized
treatment we gave for the whole FR. This is because our goal for this section is to directly capture
the behaviors of rustc, the Rust compiler. Using an existing Rust formalization as an intermediate
target would make correctness depend on that formalization’s faithfulness to rustc, rather than on
rustc directly, which is especially undesirable as Rust continues to evolve. The global completeness
argument follows the same structure as §5.3: as long as each sealor case is complete with respect to
the corresponding rustc behavior, the entire sealor and the generative compiler are complete.

6.1    General Design Choices for Rust
We describe design choices recurring across Rust’s features, before per-feature treatment in §6.2.
Sealors SRS  𝑠 and S𝑒 . Since Rust distinguishes statements and expressions, we introduce two
                      RS
sealors: a statement sealor SRS
                              𝑠 that seals a partial statement (possibly an expression statement) into

a list of statements, and an expression sealor SRS𝑒 that seals a partial expression into an expression

with an unconstrained type. When an expression is desired, and its type can be inferred from
context, the expression sealor is used. In all other cases, we use the statement sealor.
Placeholders holediv () and holeval (). FR’s sealor closes every abstracted case with the single
unit placeholder 𝜀, since FR’s control-flow-free terms leave no other typing obligation to discharge.
rustc’s typing rules for branching and looping constructs additionally require reasoning about
multiple control-flow paths, e.g., that both branches of an if agree, or that a loop body’s effects are
consistent across iterations. To seal such constructs conveniently, we introduce two placeholders
with deliberately different typing behavior.
  The first placeholder, holediv (), is simply panic!() in our implementation. Statically, panic!()
has type !, the never type, whose expressions can be coerced to any expected type. It diverges:
executing it never returns normally. Because the continuation after a divergent expression is
unreachable, rustc does not require it to satisfy the usual borrow-checking obligations. This helps
1:18                             Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


preserve completeness; otherwise rustc might report borrow errors caused only by an intermediate
partial state, such as a variable being moved out before later generated code would reinitialize it.
This makes holediv () useful for sealing control flow branches that should not produce a value.
   The second, holeval (), instead behaves as if it produces a well-typed value without diverging.
We implement it as a call to a generic helper function: const fn holeval ()<𝑇 >() → 𝑇 { panic!() }.
The function body diverges at run time, but this divergence is not exposed at the call site. The call
expression holeval () has the declared return type 𝑇 , not the body type !. The type parameter 𝑇 is
instead resolved by type inference from the surrounding context. Thus, holeval () can instantiate
to any expected type in the surrounding code while keeping the borrow checker enabled.
   A more subtle reason not to use holediv () as the expression placeholder is Rust’s fallback for the
never type. When type inference is underconstrained, ! may fall back to the unit type (), causing
spurious type or trait mismatch errors. The type parameter 𝑇 in holeval () does not undergo this
fallback, making it a safe choice when sealed code must supply an expression value.
Suppressing Future-Dependent Errors During Generation. Sealing Rust sometimes requires
treating rustc errors more carefully than a simple accept-or-reject verdict. This is not a peculiarity of
our sealor, but a consequence of Rust features whose well-typedness can depend on code generated
later. For example, a partial trait implementation may not yet contain all required methods, a call
may refer to a function item declared later in the file, and an expression may have an ambiguous
type that is resolved only by a subsequent use. Such errors are required to be suppressed for
completeness. Otherwise the sealed program could be rejected even though the missing suffix
would make the final program well-typed. To limit the impact on soundness, we suppress errors
only in the scope where necessary. For instance, “missing trait items” is suppressed only if it occurs
inside the sealing of partial trait implementations and “type annotations needed” errors only inside
the sealing of partial function bodies. When we arrive at a fully generated program after the EOS
token, we clean out all suppressed errors, such that rustc could catch all errors.
Projecting Error Messages on Partial Programs. Since rustc checks the sealed program SRS (𝑐)
rather than the original partial program 𝑐, its diagnostics refer to SRS (𝑐). Feeding these diagnostics
directly to the model can be confusing, because SRS (𝑐) may differ from 𝑐, as in Figs. 4 and 5. We
therefore project diagnostics from SRS (𝑐) back to 𝑐. During sealing, we maintain a positional map
of code copied verbatim from 𝑐 into SRS (𝑐). We then re-render rustc’s diagnostics using 𝑐 as the
reference code, mapping the locations of diagnostic highlights from SRS (𝑐) back into 𝑐. Inserted
code such as holeval () has no source in 𝑐; diagnostics arising only from such code are suppressed
by the module described above.

6.2    SRS : Our Sealor for Rust
We now introduce the Rust sealor rules for expression and statement forms.
Blocks. A block in Rust, denoted 𝑏, consists of a sequence of statements 𝑠, optionally terminated
by an expression 𝑒. That is, 𝑏 ::= { 𝑠; 𝑒 ? }. A block is itself an expression, so it may appear wherever
an expression is expected. A block creates a lexical scope for bindings: variables defined inside are
not visible outside, and owned values are dropped at the end unless moved earlier. The type of a
block is the type of its tail expression, or the unit type if there isn’t one. Independently of that, a
block diverges if any of its statements or tail expression diverges. A block may end with a partial
expression or statement. Both are sealed identically:
       SRS
         𝑠 (𝑏)
             b =                                          SRS
                                                            𝑒 (𝑏)
                                                                b =
          { 𝑠; SRS
                𝑠 (𝑒); hole
                   b
                            div () }   if 𝑏 = { 𝑠 𝑒
                                          b       b          { 𝑠; SRS
                                                                    𝑠 (𝑒);
                                                                       b hole () } if 𝑏b = { 𝑠 𝑒b
                                                                               val
          { 𝑠; S𝑠 (𝑠); hole () } if 𝑏 = { 𝑠 𝑠
               RS
                   b
                           div
                                          b       b          { 𝑠; S𝑠 (𝑠); hole () } if 𝑏b = { 𝑠 b𝑠
                                                                   RS
                                                                       b
                                                                                val
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                                  1:19


The block sealors preserve the full statements 𝑠 and seal the partial component with SRS     𝑠 . The

statement sealor then appends holediv (), making the sealed block diverge to stop the control-flow
path (more on this later in this section when we discuss conditionals and loops). The expression
sealor instead appends holeval (), so the block produces a value of the type expected by its context.
   Completeness follows from two facts. First, preserving the completed statements 𝑠 and recursively
sealing the partial component (SRS 𝑠 (b
                                      𝑠)) mirrors FR’s completeness argument for unclosed blocks
(§5.3). That is, each piece is checked in exactly the environment it would occupy in any well-
typed completion. Second, the trailing placeholder never introduces a new failure: holediv () and
holeval () type check against any expected type, so appending them cannot make an otherwise
completable block fail to type check. For soundness, we preserve all of rustc’s checking on 𝑠 and on
the recursively sealed partial form, so any uncompletable prefix that fails these checks is rejected.

Fallback Sealors. For every feature discussed next, we present a bespoke statement sealor SRS         𝑠 .

We do not need a separate expression sealor SRS , since we automatically derive one from SRS
                                                    𝑒                                                 𝑠

via SRS (𝑒) ≔ { SRS (𝑒); holeval () }. This turns any sealing of 𝑒 from a list of statements into an
      𝑒  b        𝑠  b                                              b
expression that produces a value of the expected type. Both completeness and soundness of this
derivation are inherited directly from SRS 𝑠 : appending hole
                                                                 val () neither introduces nor discards
any typing obligation, since holeval () type checks against any expected type.
   When a construct has no specific rule for SRS 𝑠 (b
                                                    𝑠), we fall back to SRS𝑠 (b
                                                                              𝑠) ≔ (). This discards the
partial statement, preserving completeness by removing its typing obligations. Soundness may be
lost temporarily, but is recovered once the statement is fully generated and copied verbatim.

Conditionals. Conditionals in Rust are expressions: the condition is an expression, and the
branches are blocks; chaining multiple conditions with else if is allowed. That is, 𝑒 if ::= if 𝑒 𝑏 |
if 𝑒 𝑏 else 𝑏 | if 𝑒 𝑏 else 𝑒 if . rustc type checks the condition against bool, then type checks each
branch and merges the two states after them. When an else if chain is nested, the two-way merge
applies recursively from the innermost pair outward. A branch that diverges contributes nothing
to the merge: its result type and borrow state at the join point are unobservable, so the result type
and the borrow state after the if are entirely determined by the live branch.
   A partial component may appear inside the condition, inside the then-branch, or inside the
                        if ::= if 𝑒 | if 𝑒 𝑏 | if 𝑒 𝑏 else 𝑏 | if 𝑒 𝑏 else 𝑒 if . We close the missing
else-branch. That is, 𝑒c            b        b              b                c
branch with holediv (), so that it is diverging and the whole if is well-typed against the live side
alone. The statement sealor SRS   𝑠 for 𝑒c is defined below:
                                          if


          SRS
           𝑠 (𝑒c ) = S𝑠 (𝑒)
               if     RS
                           b                                      if 𝑒cif = if 𝑒
                                                                               b
                     if 𝑒 0 SRS   b else { hole () }
                               𝑠 (𝑏)
                                                 div              if 𝑒 if = if 𝑒 0 𝑏b
                                                                      c
                     if 𝑒 0 𝑏 1 else SRS
                                       𝑠 (𝑏)
                                           b                      if 𝑒cif = if 𝑒 0 𝑏 1 else 𝑏
                                                                                            b
                     if 𝑒 0 𝑏 1 else { SRS
                                         𝑠 (𝑒);
                                             b hole () }
                                                      div         if 𝑒cif = if 𝑒 0 𝑏 1 else if 𝑒
                                                                                               b
                     if 𝑒 0 𝑏 1 else SRS
                                       𝑠 (if 𝑒 . . .)
                                               1                  if 𝑒cif = if 𝑒 0 𝑏 1 else if 𝑒 1 . . .

A partial else if condition is sealed as an else body, closed with holediv () just like the missing
branch itself. Once the condition becomes full, we instead recurse via SRS
                                                                        𝑠 on the remaining if 𝑒 . . .
                                                                                                1
as a fresh partial if.
   Our sealor is complete for conditionals. Every partial component we recurse on inherits com-
pleteness from the inductive hypothesis on branch blocks and boolean conditions. Although we do
not separately discuss boolean conditions in detail, the completeness of sealing them should be easy
to achieve. The only other addition, holediv (), never introduces new obligations: since it diverges,
rustc excludes it from the branch-type merge, so it cannot constrain what the live side must satisfy.
1:20                             Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


For soundness, we preserve all of Rust’s checking up to the partial form, so any uncompletable
prefix that fails one of these checks is still rejected.
While Loops. A Rust while loop consists of a condition and a body block. That is, 𝑒 while ::=
while 𝑒 𝑏. A well-typed while loop requires that the loop body be well-typed as if it were executed
any number of times. Informally, the borrow and initialization state after one iteration must be
compatible with the state at the start of the next. Moving out of a variable in a loop body without
reinitialization is rejected, as the second iteration would read a moved-out slot. Rust waives this
obligation when the body diverges, because control never reaches a second iteration.
                                                              ::= while 𝑒b | while 𝑒 𝑏.
   Either the condition or the body may be partial, i.e., 𝑒 while                      b We force a
partial body to diverge by appending holediv () via SRS 𝑠 (𝑏),
                                                            b eliminating the “carries over between
iterations” obligation while still checking everything on the already-generated first iteration.
                        SRS
                          𝑠 (𝑒  ) = S𝑠 (𝑒)
                               while     RS
                                            b                  = while 𝑒b
                                                         if 𝑒 while
                                       while 𝑒 S (𝑏) if 𝑒  = while 𝑒 𝑏b
                                                 𝑠  b
                                                     RS              while

The other loop forms in Rust (for, unbounded loop) are handled analogously. For completeness,
the condition case is similar to if. For the body case, the sealed body diverges by construction, so
rustc does not enforce the second-iteration consistency check, and the first-iteration prefix (the
condition and the completed body prefix 𝑠) is checked against exactly the same environment it
would occupy in any well-typed completion. For soundness, we do not lose anything more than
what is lost in the partial term in the loop body, as the realization of 𝑏b can also diverge.
Function Calls. A function call consists of a callee and zero or more arguments. That is, 𝑒 call ::=
𝑒 (𝑒). At a call site 𝑒 0 (𝑒 1, . . . , 𝑒𝑛 ), rustc resolves 𝑒 0 to a signature, then type checks the arguments
left-to-right, threading each argument’s move/borrow effects into the environment used to check
the next. The number of arguments must equal the declared arity.
   A partial call has zero or more completed arguments followed by one partial argument. That is,
 call ::= 𝑒 (𝑒, 𝑒. If the callee is still partial, sealing reduces to handling whatever partial expression
𝑒              b
the callee is via its own rule, so we do not specifically discuss this case here. Our sealor first queries
rustc as an arity oracle: we invoke it on a sealing where 𝑒 0 is called with no arguments and inspect
its type. Once the arity 𝑛 is known, we pad with holeval () for the missing arguments: via SRS               𝑒 for

the partial argument, and directly for the ones not at all present in 𝑒 call .      

       SRS
        𝑠 (𝑒 ) = 𝑒 (𝑒 , . . . , 𝑒 , S𝑒 (𝑒),
              call      0 1              𝑘     RS
                                                  b hole (), . . . , hole () ) if 𝑒 = 𝑒 (𝑒 , . . . , 𝑒 , 𝑒b
                                                          val             val          call   0 1      𝑘
                                                     |           {z           }
                                                     𝑛−𝑘 −1 copies

   For completeness, our sealor places each completed argument 𝑒𝑖 in exactly the same environment
it would occupy in any well-typed completion (arguments before it are the same; then the partial
argument is sealed, and arguments after it are holeval (), which is generic and produces no effect
on the environment). This covers the case 𝑘 < 𝑛, i.e., fewer arguments have been generated so far
than the callee accepts. If instead 𝑘 ≥ 𝑛, the prefix already has more arguments than the callee’s
arity, our sealor still copies all of them rather than truncating, so rustc rejects the sealed call with a
genuine arity mismatch. This is not a false rejection, since no well-typed completion can exist once
too many arguments have already been committed. For soundness, we preserve rustc’s checking of
the callee 𝑒 0 and the completed arguments 𝑒 1, . . . , 𝑒𝑘 exactly as it would occur in the real program,
so any type or borrow error among them is still caught.
Field Accesses. A field access has the form 𝑒.𝑓 , where 𝑒 is an expression of record (or reference-to-
record) type and 𝑓 is an identifier naming one of its fields. That is, 𝑒 field ::= 𝑒.𝑓 . Field accesses are
lvals, so they participate in move, copy, borrow, and assignment on the same footing as variables.
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                              1:21


   The partial syntax rule is 𝑒 field
                                   ::= 𝑒. b𝑓 . In other words, the receiver is completed but the field
has been cut off mid-token. For 𝑒. b𝑓 , we only copy the receiver. We take a reference to avoid moving
out of 𝑒. This is necessary because the completion may be a method invocation (either on 𝑒 itself or
on a field) that takes self by reference. That is, SRS 𝑠 (𝑒. b
                                                             𝑓 ) = &𝑒.
   For completeness, the receiver of any partial field access is a strict sub-prefix of every completion,
so the receiver is well-typed if the completion is well-typed. In terms of borrow checking, we
need to suppress E0382 (borrow of moved value) because fields of the receiver (other than the
one accessed) could be uninitialized. Suppressing E0382 means we do not check if the field (or the
whole record) is initialized until later. For soundness, we preserve the type and borrow-checking of
the receiver in all cases. We do not attempt to check whether truncated identifiers can be extended
to a real field of the receiver’s type, as this goes beyond our syntax-guided design. Instead, we wait
until the field becomes full.
Other Expressions and Top-Level Items. We briefly summarize the remaining Rust constructs.
Aggregate literals, including tuples (𝑒), arrays [𝑒], and record expressions 𝑆 {𝑓 : 𝑒}, are sealed
by recursing on the trailing partial element with SRS 𝑒 and then closing the aggregate. For record

expressions, we suppress E0063 (missing field initializers). This preserves completeness because
already generated elements are checked in order, while missing fields may still be supplied later;
soundness is preserved for the fully generated elements.
   Closure expressions are sealed by sealing the body as an expression, using holeval () to close
value-producing positions. Closures with partial signatures are skipped until the signature is
complete, which delays checking of parameter types. Other expression forms, including unary
expressions, return, condition-local let, parenthesized expressions, try, ranges, indexing, and
casts, are handled uniformly: the sealor preserves fully generated components and recurses into the
partial one. Constructs without a bespoke expression rule use the fallback sealor described above.
   Top-level items are handled similarly. Function bodies are sealed like closure bodies. Item-
containing constructs, such as module definitions and impl blocks, preserve the enclosing definition
and all fully generated sub-items, then recursively seal the partial item at the frontier. For constructs
without bespoke rules, including type definitions, type aliases, constants, statics, extern blocks,
global asm!, and macros, fully generated instances are preserved verbatim, while partial instances
are discarded until enough syntax has been generated for a more specific rule to apply.
Example Revisited. Three rules seal the partial program in Fig. 4 into the full program in Fig. 5.
First, the function body is an unclosed block ending in the partial statement let prio = tag. b𝑓 , so
the block rule appends holeval (): SRS   𝑒 (𝑏)
                                            b = { 𝑠; S𝑠 (b𝑠); hole () }. Second, like the FR sealor (§5.2),
                                                      RS          val
the let rule drops the left-hand side and recurses on the partial right-hand side: SRS     𝑠 (let prio =

tag. 𝑓 ) = SRS (tag. 𝑓 ). Finally, the field-access rule closes the partial access as &tag.
     b       𝑠       b

7     Experimental Evaluation
In this section, we experimentally evaluate our generative compilation approach. We focus on two
core research questions: (R1) Can our generative compilation effectively support code generation?
and (R2) What are observable effects of generative compilation?

7.1    Experimental Setup
Models and Agent Harness. We evaluate seven recent coding models. The three frontier black-
box models, Claude Opus 4.8 [3], GPT 5.3 Codex [37], and Gemini 3.5 Flash [13], come from major
model providers and are explicitly advertised for coding. We also include four strong open-weight
models, Kimi K2.7 Code [30], GLM 5.2 [60], and two models from the Qwen 3.5 family, a large
1:22                           Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


397B-parameter model and a smaller 9B-parameter model [51]. This selection spans a broad range
of model categories and capabilities. We evaluate each model twice on every task, sampling with
temperature 0.6 whenever the provider permits configuring it.
   We use an agent harness with fixed control flow, similar in style to Agentless [58], to isolate the
effect of feedback and enable a clean comparison. The model generates files or structured edits,
while the harness deterministically writes them to disk, runs fixed compilation commands, and
feeds any diagnostics back into the next prompt.
Tasks and Benchmarks. We evaluate two repository-level tasks for which Rust compiler errors
occur frequently. Both tasks require filling a Rust skeleton that defines struct and function signatures.
We report two end-to-end metrics: compiler error rate and functional correctness. Compiler error
rate is the fraction of generated outputs for which the Rust compiler reports at least one error
diagnostic. Functional correctness is the fraction of generations that pass the task’s unit tests.
To better understand the results, we also measure runtime, the number of diagnostics in each
compiler-feedback report, whether errors are detected during generation, and how far detected
errors are from their original locations. We list prompts for both tasks in §C.
   The first task, denoted Translation, is based on CRUST-Bench [20], a benchmark for C-to-
Rust translation. Translation is based on a subset of 20 complex instances from CRUST-Bench.
The model is given the C implementation of a library and is tasked to translate it into Rust. We
ask the model to translate each C file at a time, such that it uses the specified interfaces. C to
Rust translation is an important topic, as Rust is considered a more memory-safe and similarly
performant alternative to C. At the same time, large translations are challenging: the model must
translate C data structures consistently and adapt them to Rust interfaces across files.
   The second task, denoted UpdatedAPI, evaluates whether models can adapt to changed Rust
library APIs. Each instance asks the model to implement a small command-line utility that re-
quires using a recently updated API function. This setting is relevant because LLMs always have
fixed training knowledge cutoffs and may therefore generate code against deprecated APIs. The
benchmark tests whether the model can use compiler feedback about the changed API to repair its
generation. We provide details about benchmark construction in §A.
Comparison. We compare three approaches. The first, LLM, samples directly from the LLM
without compiler feedback. The second, denoted PC for short, adds standard post-generation
compiler feedback: after each generated solution, the compiler is run, and any diagnostics are fed
back to the model. If compilation fails, the model may either edit its previous output or regenerate
a new solution from scratch. This process may repeat up to 𝑛 times. The third approach, denoted
GC, further incorporates on-the-fly feedback enabled by generative compilation (Fig. 6). This tests
whether generative compilation can improve over post-generation feedback by detecting errors
early. During generation, generative compilation may detect compiler errors on partial outputs
and restart generation, up to 𝑘 times. If the model has not produced a valid output after these
𝑘 restarts, we allow it to finish generating a full output and then apply up to 𝑛 − 𝑘 iterations of
post-generation compiler feedback. In our experiments, we set 𝑛 = 15 in UpdatedAPI and 𝑛 = 20
on Translation, and 𝑘 = 10 in both settings. We ablate over the budget choices in §A.5.
   Note that we cannot experimentally compare against constrained decoding because, to our
knowledge, no constrained decoding implementation exists for Rust. Although our approach can
check partial programs, it is not suitable for constrained decoding. This is because our approach
guarantees global completeness, whereas constrained decoding requires global soundness, as
discussed at the end of §3.1. Building a constrained decoder from scratch for real Rust would be
highly complex and costly, as discussed in §2. This contrast highlights a key benefit of generative
compilation: it is lightweight to implement and largely reuses existing compiler infrastructure.
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                                 1:23


Table 1. Comparison of LLM, PC, and GC on two repository-level coding tasks (Translation and UpdatedAPI).
Here, LLM denotes generation without compiler feedback, PC adds standard post-generation feedback, and
GC further incorporates on-the-fly feedback enabled by generative compilation. Overall, GC further reduces
compiler errors while improving functional correctness. We mark the best result in boldface and underline
results that are not significantly worse, determined by a paired difference test at significance level 𝛼 = 5%.
                              Translation                                        UpdatedAPI
               Compiler Errors (↓)      Functional Corr. (↑)    Compiler Errors (↓)    Functional Corr. (↑)
Model          LLM      PC      GC     LLM      PC       GC     LLM         PC    GC   LLM      PC      GC
Opus 4.8      51.8% 7.5% 2.6% 32.0% 61.0% 62.3% 51.7% 6.7% 0.0% 43.3% 85.0% 86.7%
GPT 5.3       46.1% 3.9% 1.8% 35.5% 61.0% 61.8% 65.0% 13.3% 3.3% 35.0% 75.0% 80.0%
Gemini 3.5    61.4% 14.0% 10.5% 23.7% 50.4% 52.2% 68.3% 16.7% 13.3% 26.7% 78.3% 80.0%
Kimi K2.7     65.8%   38.6%   11.0% 23.7% 39.9% 53.9% 58.3%             13.3% 3.3% 36.7% 76.7%         83.3%
GLM 5.2       60.5%   17.1%   15.4% 25.4% 51.3% 50.4% 80.0%             45.0% 16.7% 20.0% 53.3%        71.7%
Qwen 397B     64.5%   13.2%   12.7% 23.2% 54.8% 53.1% 73.3%             21.7% 15.0% 26.7% 68.3%        71.7%
Qwen 9B       85.5%   36.0%   35.1% 8.3% 30.3% 33.3% 90.0%              43.3% 43.3% 10.0% 48.3%        41.7%


Implementation Details. Our sealor is implemented in about 5k lines of Rust, which is orders
of magnitude less than the ∼600k lines in Rust’s compiler frontend [47]. It parses partial Rust code
using rust-analyzer [46], synthesizes sealed programs using the rules outlined in §6, and queries
rustc for compiler feedback. We apply minimal patches to rust-analyzer to improve its handling of
partial ASTs. The LLM-facing layer comprises about 3k lines of Python: it streams candidate tokens,
invokes the sealor and the Rust compiler through bindings, and implements the logic in Fig. 6.
For robustness, the implementation is covered by 329 Rust and Python tests spanning the sealor
and inference behavior. Finally, we include wrappers for different LLM inference APIs, evaluated
datasets, and inference and evaluation orchestration comprising another 8k lines of Python code.

7.2   Benefits for End-to-End Code Generation
We integrate our method into the code generation pipeline and measure its benefits, answering R1.
Reduced Compiler Errors and Improved Functional Correctness. As shown in Table 1,
LLM produces non-compilable outputs in up to 90.0% of cases. Post-generation compiler feedback
(PC) reduces the average compiler error rate from 65.9% to 20.7%, highlighting the strong repair
capabilities of state-of-the-art LLMs. Even so, adding on-the-fly feedback with GC reduces the error
rate further to 13.1%. Across all 14 model-dataset configurations, GC achieves a better compiler
error rate than PC and one tie; in 9 of the configurations, the improvement over PC is statistically
significant. Notably, GC eliminates compiler errors entirely for Opus 4.8 on UpdatedAPI (0.0% vs.
6.7% with PC) and reduces them from 13.3% to 3.3% for GPT 5.3 Codex.
   Reductions in compiler errors also transfer to improving functional correctness. GC attains the
best functional correctness in 11 of the 14 model-dataset configurations. The largest improvements
are visible on UpdatedAPI for GLM 5.2 (from 53.3% with PC to 71.7% with GC) and on Translation
for Kimi K2.7 (from 39.9% to 53.9%, respectively).
Decreased Runtime. Despite intervening during generation, GC decreases overall runtime. The
average overhead over LLM drops from 233 seconds (+283%) with PC to 135 seconds (+170%) with
GC. This reduction is driven by models that require many feedback rounds, namely Gemini 3.5 Flash
and the Qwen 3.5 models. For Qwen 9B, GC more than halves the average runtime on both datasets;
for example, on Translation, runtime drops from on average 879 to 357 seconds per sample. By
1:24                                                                          Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


                                                                                                                  40                                                                                100




                                                                                                                                                             Cumulative portion of rejections (%)
                                                                       PC                                                                           GC
                                   40
   Portion of error messages (%)




                                                                       GC                                                                           GCfn




                                                                                     Portion of diagnostics (%)
                                                                                                                                                    PC
                                                                                                                  30                                                                                 75
                                   30


                                                                                                                  20                                                                                 50
                                   20
                                                                                                                                                                                                                                    Oracle
                                                                                                                                                                                                                                    GC
                                                                                                                  10                                                                                 25
                                   10                                                                                                                                                                                               GCfn
                                                                                                                                                                                                                                    PC

                                    0                                                                              0                                                                                  0
                                                                                                                     0 1 2 4 8 6 2 4 8 6 2 4 8                                                            0     25       50        75        100
                                        ≤1 ≤2 ≤4 ≤8 ≤16 ≤32 ≤64≤128≤256≤512                                         ≤ ≤ ≤ ≤ ≤ ≤ 1 ≤ 3 ≤ 6 12 25 51 102 204
                                                                                                                                        ≤ ≤ ≤≤ ≤                                                              Relative file position (%)
                                               Number of diagnostics                                                      Error report delay in LoC

(a) Diagnostics per error message.                                                                                (b) Error report delays.                   (c) Cumulative error detection.
Fig. 12. Our analysis on the effects of generative compilation (GC). First (a), GC leads to smaller numbers
of diagnostics in error messages, compared to post-generation compilation (PC). Second (b), GC results in
smaller error report delays, compared with the function-level invariant GCfn and PC. Finally (c), GC detects
errors early, most of the time before file completion.




interrupting generation at the first unrecoverable error, GC avoids repeatedly completing files that
cannot compile. For Opus 4.8, and Kimi K2.7, which require on-the-fly feedback less frequently,
runtime remains essentially unchanged, increasing by 2 seconds (+6%) for former, and decreasing
11 seconds (−6%) for the latter.

7.3                                 Analysis: What Effects Does Generative Compilation Have?
Mitigated Error Snowballs. Looking more closely at GC, we find that most errors are resolved
during the early-feedback phase, i.e., within the first 𝑘 = 10 restarts. Overall, 85.3% of tasks complete
without ever switching back to post-generation compiler feedback, and 55.4% of all tasks are solved
correctly within the early-feedback phase. Weaker models require more restart: Qwen 9B takes
more than 10 restarts in 40.9% of tasks and Qwen 397B on 20.5%, compared to only 2.1% for GPT 5.3
Codex. We attribute this partly to weaker models unfamiliarity with the early compiler-feedback
format; in particular, they often regenerate the same erroneous prefix.
   Generative compilation also makes error reports smaller and more focused. When a completed
file is compiled, one core mistake can cascade into many follow-on diagnostics. By interrupting
generation at the first unrecoverable mistake, GC instead surfaces a reduced set of diagnostics that
focuses on the root cause. As shown in Fig. 12a, 65% of GC error reports contain only one or two
distinct diagnostics, with an average of 5.5 diagnostics per message. In contrast, only 40% of PC
reports are this succinct, averaging 13.8 diagnostics and, on Translation, sometimes reaching
several hundred. This reduction gives the model a smaller and more targeted repair signal, reducing
the burden of locating the relevant error within its context.

Reporting Errors Close to Their Source. To further assess the quality of GC’s error detection,
we measure how early it surfaces errors during generation. For each of the 961 erroneous files
generated by LLM and included in this analysis, we record the location of the first compiler error
returned by rustc in the completed program. We then replay the same file prefix by prefix against
GC and record where GC first reports an error. The replay feeds each file verbatim at 50 tokens per
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                                      1:25


second, a typical decoding speed for current frontier coding models1 , while running GC in parallel
without asking the model to repair errors.
   Oracle denotes the primary span of the first compiler error reported on the completed file. This
span is a lower bound on the earliest possible detection point for that error, but is generally not
achievable from a prefix alone: a prefix ending at the span may still admit a valid completion, for
example if the error refers to an item that could be defined later. We compare this oracle span with
those reported by GC. We also compare against two baselines: GCfn , a simpler variant that checks
only completed function bodies, and PC, which reports compiler feedback only after the full file
has been generated.
   In the median case, GC reports the error only 3 lines after the primary span of the eventual
compiler error, and in a quarter of all cases it reports the error exactly at that span. By contrast, GCfn
and PC report errors much later, with median delays of 14 and 89 lines after Oracle, respectively,
as shown in Fig. 12b. The delay distribution for GC is heavy-tailed, with a mean of 27.7 lines. This
is expected: our configuration deliberately tolerates references to not-yet-defined items, as they
may legitimately be introduced later in the file. Errors involving such items are therefore reported
only once such a later definition is ruled out, e.g., when the model signals the end of file generation.
Indeed, among errors in the top quartile of detection delay (≥ 25 lines; mean 99 lines), 90.5% involve
such items: unresolved names and imports (63.8%) or missing methods and functions (26.7%).
Errors are Detected Long before File Completion. Reporting errors close to their source
is most useful when those sources occur early in generation, since it prevents the model from
producing later code based on wrong assumptions. As shown in Fig. 12c, GC reports unrecoverable
errors at a mean detection point of 33.3% of the file, nearly matching the timing-free upper bound
of 32.7%. Thus, GC avoids generating the remaining 66.7% of unrecoverably non-compiling output.
By contrast, PC reports errors only after file completion by construction, while GCfn lags behind
with a mean detection point of 40.3%.
Detected Error Kinds. We categorize errors detected during mid-file restarts into syntax errors,
type errors, borrow-check and lifetime errors, and others. Most errors are type-system related; the
most frequent is type mismatch (E0308), which accounts for over a third of reports. Our method also
detects more intricate borrow-check and lifetime violations early, including conflicting borrows
(E0502) and moves out of borrowed values (E0507). A detailed breakdown appears in §A.4.

8   Discussion and Future Work
Modeling Error Messages. Our generative compiler returns both a verdict ok and a diagnostic
err. However, our completeness and soundness results concern only ok, and do not model err. In
particular, we do not formalize whether err describes a genuine defect in the original, unsealed
partial program rather than an artifact of sealing, but observe this behavior empirically. This
is due to two core reasons: First, we take active measures against reporting artifacts of sealing,
by suppressing errors that stem from sealing-inserted code using the expected-error machinery
described in §6.1. Second, in most cases, the placeholders that sealing introduces add no new
typing obligations of their own, leaving only already-generated code that is mostly preserved
verbatim. Formalizing that err represents a genuine defect in the partial prefix, building on prior
formal treatments of type-error localization [22, 48, 55], is future work. A related, open question
is how to design error messages for their consumer, for instance whether diagnostics should be
reformulated or supplemented with context to be more actionable. This has been studied for human
1 As reported by OpenRouter for Claude Opus 4.8 (https://openrouter.ai/anthropic/claude-opus-4.8) and GPT 5.3 Codex

(https://openrouter.ai/openai/gpt-5.3-codex).
1:26                          Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


programmers [26] and, more recently, for AI coding agents [21]. Our current rendering follows the
rustc diagnostic formatting, because we assume that models are most familiar with this feedback
based on their training corpus.

When and How to Invoke Generative Compilation. In §3.2, generative compilation is tied
to a fixed mechanism: invoke it whenever the previous check finishes, and on rejection, augment
the prompt and restart generation. Concurrency makes this loop practical, since validation runs
alongside token generation and adds only modest overhead. Decoupling generative compilation
from this hardwired decoding loop opens several directions. First, the invocation frequency could
be tuned to trade compiler overhead against wasted generation, since less frequent checks only
risk discarding a short suffix after rejection. Second, the decision of when and how to invoke
generative compilation could be delegated to the coding agent, alongside other tools it may call.
Third, our current use of generative compilation treats the LLM as a black box, leaving open whether
white-box model access could yield further improvements. Fourth, the diagnostics err produced on
rejection provide valuable training signals, suggesting the possibility of using them during training
rather than only at inference time. Finally, we highlight that generative compilation is a general
concept applicable beyond LLMs, and works with any code generation method that is steerable by
natural language prompts, and produces intermediate code outputs.

Automating Sealor Construction. The sealors in this paper, for both FR (§5) and Rust (§6), are
hand-written. For each construct, we manually derive a sealing rule and argue its completeness
and soundness. An open direction is to synthesize such rules automatically from a language’s
specification or reference implementation, rather than by hand. This is a challenging task, since
rules must be complete while achieving strong soundness, so synthesis would need to search under
these constraints rather than under well-formedness alone. Automating this construction could
help generative compilation scale even further: to languages beyond Rust, to languages as they
evolve, and even to new languages as they are designed and implemented. The latter two cases may
benefit most, since LLMs have little or no training data for such code, making direct and on-the-fly
compiler feedback especially valuable.

9      Related Work
Compiler Feedback. Compilers help programming in two distinct ways: they establish guaran-
tees, such as memory safety [18, 27] or information-flow security [32], and they provide feedback
that guides revision when those guarantees are violated. Such feedback, especially well-designed
error messages, has long helped human programmers from novices to professionals [22, 26, 48, 55].
Earlier research has brought this feedback into AI-assisted code generation, using it during train-
ing through supervised fine-tuning [56] or reinforcement learning [9], and at inference time to
iteratively refine generated programs [5]. Compiler feedback is now common in coding agents,
which run compilers through the command line or invoke them as tools, obtain diagnostics, and ac-
cordingly revise code [8]. These approaches all use the compiler after a complete program has been
generated. Generative compilation instead invokes the compiler during generation, on still-partial
programs, making it an earlier in-the-loop complement to post-generation feedback.

Constrained Decoding. Like generative compilation, constrained decoding checks programs
during autoregressive generation [1, 43]. The key difference is how the check is used. Constrained
decoding intervenes inside sampling, restricting next-token choices. Early approaches do so locally,
token by token, which can harm the final program [4, 39, 52]; later work makes sampling aware of
global constraints, but still operates at the sampling level [12, 23, 25, 45]. Constrained decoding for
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                          1:27


constraints beyond syntax typically requires significant reimplementation [31, 34], and a constrain-
ing system that only accepts a subset of the language (i.e., one that is incomplete) can degrade
performance [6]. For this reason no constrained decoding techniques exist for complex properties
such as the Rust borrow and lifetime system that we could compare generative compilation to.
Syntax- and Type-Guided Program Construction. Syntax and types have long guided the
program search, especially in synthesis from formal specifications [2, 11, 14, 38, 44]. Our work also
reasons about syntax and types, but targets LLM-based code generation.
   Designed for live programming environments like IDEs, typed holes [35, 36] are close in spirit
to our placeholders: 𝜀 for FR (§5.2), and holediv () and holeval () for Rust (§6.1). The purpose of
typed holes is also to make incomplete programs well-typed, permitting the extraction of static
type contexts [7]. The difference is where the hole lives. In contrast to our placeholders, typed
holes require an extension of the language: the hole in the program is made a first-class citizen of
the language, and the type system is extended to reason about it. Our placeholders instead leverage
existing elements of the language and are already handled by the language’s type system.

10   Conclusion
We introduced generative compilation, the first approach to bring compiler feedback into the
intermediate steps of LLM-based code generation. The central idea is to seal a partial program
into a complete program that a standard compiler can check, thereby turning an off-the-shelf
compiler into a prefix checker with diagnostics. This preserves the practical advantages of compiler
feedback: black-box model access, use of the real compiler, and rich error messages. At the same
time, we avoid the delayed feedback of post-generation checking and the implementation burden
of constrained decoding.
   We formalized this idea through sealors, proving that a sealor induces a generative compiler with
the same completeness and soundness guarantees, and instantiated the framework on Featherweight
Rust with a syntax-guided sealor satisfying this property, fully mechanized in Lean. We then carried
the same methodology to build the first prefix checker for real Rust, where the sealor handles
Rust-specific expression and statement structure, control flow, placeholders, and future-dependent
compiler errors while delegating type, borrow, and lifetime reasoning to rustc.
   Our evaluation on Rust code generation tasks shows that generative compilation detects many
errors close to their source and long before file completion, including type, borrow-check, and
lifetime errors. Integrated into code generation, this early feedback reduces non-compiling outputs
and improves functional correctness compared with standard post-hoc compiler feedback.

Acknowledgments
We thank Ralf Jung for his invaluable insights into the complexity of formalizing Rust and his
encouragement to pursue the project. We also thank Marius Arvinte, Cory Cornelius, and the other
members of Intel’s Security and Privacy Research Lab for helpful technical discussions. Dawn
Song and Jingxuan He were supported in part by the Defense Advanced Research Projects Agency
(DARPA) Translating All C To Rust (TRACTOR) program under Agreement No. HR00112590134.
Niels Mündler-Sasahara and Martin Vechev are supported by the grant SAFEAI (Certified Safe, Fair
and Robust Artificial Intelligence). The work has received funding from the Swiss State Secretariat
for Education, Research and Innovation (SERI), contract no. MB22.00088. Any opinions, findings,
and conclusions expressed in this material are those of the authors, and do not necessarily reflect the
views of the sponsoring entities. This research was partially funded by the Ministry of Education
and Science of Bulgaria (support for INSAIT, part of the Bulgarian National Roadmap for Research
Infrastructure).
1:28                               Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


References
 [1] Lakshya A. Agrawal, Aditya Kanade, Navin Goyal, Shuvendu K. Lahiri, and Sriram K. Rajamani. 2023. Monitor-Guided
     Decoding of Code LMs with Static Analysis of Repository Context. In NeurIPS.
 [2] Rajeev Alur, Rastislav Bodík, Garvit Juniwal, Milo M. K. Martin, Mukund Raghothaman, Sanjit A. Seshia, Rishabh
     Singh, Armando Solar-Lezama, Emina Torlak, and Abhishek Udupa. 2013. Syntax-guided synthesis. In FMCAD.
 [3] Anthropic. 2026.             Claude Opus 4.8 System Card.                          https://www-cdn.anthropic.com/
     0f0c97ad20d8005706296bd92aa1c27c6b2f4f61/Claude%20Opus%204.8%20System%20Card.pdf
 [4] Luca Beurer-Kellner, Marc Fischer, and Martin Vechev. 2024. Guiding LLMs The Right Way: Fast, Non-Invasive
     Constrained Generation. In ICML.
 [5] Zhangqian Bi, Yao Wan, Zheng Wang, Hongyu Zhang, Batu Guan, Fangxin Lu, Zili Zhang, Yulei Sui, Hai Jin, and
     Xuanhua Shi. 2024. Iterative Refinement of Project-Level Code Context for Precise Code Generation with Compiler
     Feedback. In Findings of ACL.
 [6] Matteo Biagiola, Jahrim Gabriele Cesario, Luca Di Grazia, George Zakhour, and Guido Salvaneschi. 2026. The Alignment
     Problem in Constrained Code Generation.
 [7] Andrew Blinn, Xiang Li, June Hyung Kim, and Cyrus Omar. 2024. Statically Contextualizing Large Language Models
     with Typed Holes. Proc. ACM Program. Lang. OOPSLA2 (2024).
 [8] Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, Rishi Poddar, and Aseem Rastogi. 2025. RustAssistant: Using LLMs
     to Fix Compilation Errors in Rust Code. In ICSE.
 [9] Shihan Dou, Yan Liu, Haoxiang Jia, Enyu Zhou, Limao Xiong, Junjie Shan, Caishuang Huang, Xiao Wang, Xiaoran Fan,
     Zhiheng Xi, Yuhao Zhou, Tao Ji, Rui Zheng, Qi Zhang, Tao Gui, and Xuanjing Huang. 2024. StepCoder: Improving
     Code Generation with Reinforcement Learning from Compiler Feedback. In ACL.
[10] Yufeng Du, Minyang Tian, Srikanth Ronanki, Subendhu Rongali, Sravan Babu Bodapati, Aram Galstyan, Azton Wells,
     Roy Schwartz, Eliu A Huerta, and Hao Peng. 2025. Context Length Alone Hurts LLM Performance Despite Perfect
     Retrieval. In Findings of EMNLP.
[11] Jonás Fiala, Shachar Itzhaky, Peter Müller, Nadia Polikarpova, and Ilya Sergey. 2023. Leveraging Rust Types for
     Program Synthesis. Proc. ACM Program. Lang. PLDI (2023).
[12] Emmanuel Anaya Gonzalez, Sairam Vaidya, Kanghee Park, Ruyi Ji, Taylor Berg-Kirkpatrick, and Loris D’Antoni. 2026.
     Constrained Sampling for Language Models Should Be Easy: An MCMC Perspective. In NeurIPS.
[13] Google DeepMind. 2026. Gemini 3.5 Flash Model Card. https://storage.googleapis.com/deepmind-media/Model-
     Cards/Gemini-3-5-Flash-Model-Card.pdf
[14] Tihomir Gvero, Viktor Kuncak, Ivan Kuraj, and Ruzica Piskac. 2013. Complete completion using types and weights. In
     PLDI.
[15] Son Ho and Jonathan Protzenko. 2022. Aeneas: Rust verification by functional translation. Proc. ACM Program. Lang.
     ICFP (2022).
[16] Atsushi Igarashi, Benjamin C. Pierce, and Philip Wadler. 2001. Featherweight Java: a minimal core calculus for Java
     and GJ. ACM Trans. Program. Lang. Syst. 23, 3 (2001), 396–450.
[17] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sung Hun Kim. 2026. A Survey on Large Language Models for
     Code Generation. ACM Trans. Softw. Eng. Methodol. 35, 2 (2026).
[18] Trevor Jim, J. Gregory Morrisett, Dan Grossman, Michael W. Hicks, James Cheney, and Yanling Wang. 2002. Cyclone:
     A Safe Dialect of C. In USENIX ATC.
[19] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2018. RustBelt: securing the foundations of
     the rust programming language. Proc. ACM Program. Lang. POPL (2018).
[20] Anirudh Khatry, Robert Zhang, Jia Pan, Ziteng Wang, Qiaochu Chen, Greg Durrett, and Isil Dillig. 2025. CRUST-Bench:
     A Comprehensive Benchmark for C-to-safe-Rust Transpilation. In COLM.
[21] Shriram Krishnamurthi and Matthew Flatt. 2026. Type-Error Ablation and AI Coding Agents. arXiv Preprint
     abs/2606.01522 (2026).
[22] Benjamin S. Lerner, Matthew Flower, Dan Grossman, and Craig Chambers. 2007. Searching for Type-Error Messages.
     In PLDI.
[23] Benjamin Lipkin, Benjamin LeBrun, Jacob Hoover Vigly, João Loula, David R. MacIver, Li Du, Jason Eisner, Ryan
     Cotterell, Vikash Mansinghka, Timothy J. O’Donnell, Alexander K. Lew, and Tim Vieira. 2025. Fast Controlled
     Generation from Language Models via Adaptive Weighted Rejection Sampling. In COLM.
[24] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2024.
     Lost in the Middle: How Language Models Use Long Contexts. TACL 12 (2024).
[25] João Loula, Benjamin LeBrun, Li Du, Ben Lipkin, Clemente Pasti, Gabriel Grand, Tianyu Liu, Yahya Emara, Marjorie
     Freedman, Jason Eisner, Ryan Cotterell, Vikash Mansinghka, Alexander K. Lew, Tim Vieira, and Timothy J. O’Donnell.
     2025. Syntactic and Semantic Control of Large Language Models via Sequential Monte Carlo. In The Thirteenth
     International Conference on Learning Representations.
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                                              1:29


[26] Guillaume Marceau, Kathi Fisler, and Shriram Krishnamurthi. 2011. Measuring the effectiveness of error messages
     designed for novice programmers. In SIGCSE.
[27] Nicholas D Matsakis and Felix S Klock. 2014. The rust language. ACM SIGAda Ada Letters 34, 3 (2014).
[28] Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. 2021. RustHorn: CHC-based Verification for Rust Programs.
     ACM Trans. Program. Lang. Syst. 4 (2021).
[29] Daniel Melcer, Nathan Fulton, Sanjay Krishna Gouda, and Haifeng Qian. 2024. Constrained Decoding for Fill-in-the-
     Middle Code Language Models via Efficient Left and Right Quotienting of Context-Sensitive Grammars.
[30] Moonshot AI. 2026. Kimi-K2.7-Code. https://huggingface.co/moonshotai/Kimi-K2.7-Code
[31] Niels Mündler, Jingxuan He, Hao Wang, Koushik Sen, Dawn Song, and Martin Vechev. 2025. Type-Constrained Code
     Generation with Language Models. Proc. ACM Program. Lang. PLDI (2025).
[32] Andrew C. Myers. 1999. JFlow: Practical Mostly-Static Information Flow Control. In POPL.
[33] Niels Mündler, Jasper Dekoninck, and Martin Vechev. 2026. Constrained Decoding of Diffusion LLMs with Context-Free
     Grammars. In ICLR.
[34] Shaan Nagy, Timothy Zhou, Nadia Polikarpova, and Loris D’Antoni. 2026. ChopChop: A Programmable Framework
     for Semantically Constraining the Output of Language Models. Proc. ACM Program. Lang. POPL (2026).
[35] Cyrus Omar, Ian Voysey, Ravi Chugh, and Matthew A. Hammer. 2019. Live functional programming with typed holes.
     Proc. ACM Program. Lang. POPL (2019).
[36] Cyrus Omar, Ian Voysey, Michael Hilton, Jonathan Aldrich, and Matthew A. Hammer. 2017. Hazelnut: a bidirectionally
     typed structure editor calculus. In POPL.
[37] OpenAI. 2026. GPT-5.3-Codex System Card. https://deploymentsafety.openai.com/gpt-5-3-codex
[38] Peter-Michael Osera and Steve Zdancewic. 2015. Type-and-example-directed program synthesis. In PLDI.
[39] Kanghee Park, Jiayu Wang, Taylor Berg-Kirkpatrick, Nadia Polikarpova, and Loris D’Antoni. 2024. Grammar-Aligned
     Decoding. In NeurIPS.
[40] Etienne Payet, David J. Pearce, and Fausto Spoto. 2022. On the Termination of Borrow Checking in Featherweight
     Rust. NASA Formal Methods (2022).
[41] David J. Pearce. 2021. A Lightweight Formalism for Reference Lifetimes and Borrowing in Rust. ACM Trans. Program.
     Lang. Syst. 43, 1 (2021).
[42] Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, and Ramesh Karri. 2022. Asleep at the
     Keyboard? Assessing the Security of GitHub Copilot’s Code Contributions. In IEEE S&P.
[43] Gabriel Poesia, Alex Polozov, Vu Le, Ashish Tiwari, Gustavo Soares, Christopher Meek, and Sumit Gulwani. 2022.
     Synchromesh: Reliable Code Generation from Pre-trained Language Models. In ICLR.
[44] Nadia Polikarpova, Ivan Kuraj, and Armando Solar-Lezama. 2016. Program synthesis from polymorphic refinement
     types. In PLDI.
[45] Henrijs Princis, Arindam Sharma, and Cristina David. 2026. TreeCoder: Systematic Exploration and Optimisation of
     Decoding and Constraints for LLM Code Generation. Proc. ACM Program. Lang. PLDI (2026).
[46] Rust Developers. 2026. rust-lang/rust-analyzer. https://github.com/rust-lang/rust-analyzer
[47] rust-lang. 2026. rust-lang/rust: Empowering everyone to build reliable and efficient software. https://github.com/rust-
     lang/rust
[48] Eric L. Seidel, Huma Sibghat, Kamalika Chaudhuri, Westley Weimer, and Ranjit Jhala. 2017. Learning to blame:
     localizing novice type errors with data-driven diagnosis. Proc. ACM Program. Lang. OOPSLA (2017).
[49] Rico Sennrich, Barry Haddow, and Alexandra Birch. 2016. Neural Machine Translation of Rare Words with Subword
     Units. In ACL.
[50] Zhi Rui Tam, Cheng-Kuang Wu, Yi-Lin Tsai, Chieh-Yen Lin, Hung yi Lee, and Yun-Nung Chen. 2024. Let Me Speak
     Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models.
[51] Qwen Team. 2026. Qwen3.5: Accelerating Productivity with Native Multimodal Agents. https://qwen.ai/blog?id=
     qwen3.5
[52] Shubham Ugare, Rohan Gumaste, Tarun Suresh, Gagandeep Singh, and Sasa Misailovic. 2025. IterGen: Iterative
     Semantic-aware Structured LLM Generation with Backtracking. In ICLR.
[53] Shubham Ugare, Tarun Suresh, Hangoo Kang, Sasa Misailovic, and Gagandeep Singh. 2025. SynCode: LLM Generation
     with Grammar Augmentation. TMLR (2025).
[54] Mark Vero, Niels Mündler, Victor Chibotaru, Veselin Raychev, Maximilian Baader, Nikola Jovanovic, Jingxuan He, and
     Martin Vechev. 2025. BaxBench: Can LLMs Generate Correct and Secure Backends?. In ICML.
[55] Mitchell Wand. 1986. Finding the Source of Type Errors. In POPL.
[56] Xin Wang, Yasheng Wang, Yao Wan, Fei Mi, Yitong Li, Pingyi Zhou, Jin Liu, Hao Wu, Xin Jiang, and Qun Liu. 2022.
     Compilable Neural Code Generation with Compiler Feedback. In Findings of ACL.
[57] Aaron Weiss, Daniel Patterson, Nicholas D. Matsakis, and Amal Ahmed. 2019. Oxide: The Essence of Rust. arXiv
     Preprint abs/1903.00982 (2019).
1:30                           Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He


[58] Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang. 2025. Demystifying LLM-Based Software
     Engineering Agents. Proc. ACM Softw. Eng. FSE (2025).
[59] Jiahong Xiang, Wenxiao He, Xihua Wang, Hongliang Tian, and Yuqun Zhang. 2026. Evaluating and Improving
     Automated Repository-Level Rust Issue Resolution with LLM-based Agents. In ICSE.
[60] Z.ai. 2026. GLM-5.2: Built for Long-Horizon Tasks. https://z.ai/blog/glm-5.2
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                           1:31


A     Experimental Details
A.1    Construction of UpdatedAPI
For the UpdatedAPI dataset, we construct a benchmark that requires LLMs to use third-party
libraries with API changes after their knowledge cutoff date. The benchmark is constructed as
follows. We first fetch the 100 most downloaded Rust crates that have had minor or major version
bumps in the previous 6 months at the time of writing. We then task Codex with GPT 5.3 to filter
out the packages that had changes to their public-facing API during this version bump. We then
task the model to construct realistic and sufficiently complex use cases of these libraries that require
the changed API. This step results in 30 single-file code projects that we manually assess to be
suitable for LLM evaluation. We then remove the implementation of the function that uses this
changed API, replacing it with unimplemented!(). The model is then tasked to regenerate the
entire file, including the corrected function bodies. The tasks require implementing an average
of 5.9 function bodies (maximum 15) and solutions averaging 3,142 characters (maximum 4,952),
which are verified by an average of 3.23 test cases.

A.2    Construction of Translation
The dataset is based on the CRUST-Bench benchmark [20], consisting of 100 C-to-Rust translation
tasks. We run GPT 5.3 and Claude Opus 4.8 on these tasks and observe that they are capable
of solving around 80 of these tasks zero-shot, without any compiler feedback. We focus on the
remaining 20 tasks. We split each task, which concerns translating an entire library, into individual
tasks for each file in the library. The final evaluation is performed by embedding the generated file
into a repository of golden solutions. Since interfaces and structures are fixed before compilation,
model generations for each file should be independent of the surrounding files. We list the prompts
used for generation in §C.

A.3    Experimental Setup Details
Rust Implementation. Our implementation is based on Rust 1.95.0 [47]. We apply a minimal
patch to the Rust compiler to access type inference results to reveal defined identifiers and available
functions and methods as well as the respective expected number of parameters. Our changes are
supplied with the implementation as a code patch.
Hyperparameters. The Qwen 3.5 models, GLM 5.2 and Kimi K2.7 are accessed through Open-
Router. Gemini 3.5 Flash is accessed directly through the Google Vertex API. GPT 5.3 Codex is
accessed through the OpenAI responses API. Claude Opus 4.8 is accessed directly through the
Anthropic API. For Opus, since the API endpoint does not permit setting a temperature, we omit it
in requests. For all other models we set it to 0.6. The maximum token output for the UpdatedAPI
task is 20,000 tokens; for the Translation task, it is 30,000 tokens. We retry model inference errors
up to 10 times with a timeout of 600 seconds. Beyond this point we consider inference for a task as
failed. This occurs rarely and affects 0.8% of files in Translation and 0.2% of files in UpdatedAPI.
We further observe that such failures occur for the same instances, which have extremely long input
sizes. The verifier and compilation are run on a server with 2 AMD EPYC 9655 96-core processors,
totaling 192 physical and 384 logical cores.

A.4 Detailed Analysis of Detected Error Kinds
We categorize the error codes reported during mid-file restarts in §7.3 into syntactic errors (Syntax),
type violations (Type), borrow-check and lifetime violations (Borrow & Lifetime), and others (Other),
denoting errors without an associated error code as *. Fig. 13 shows the resulting histogram per
dataset.
1:32                                                                                       Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He

            103
                      Syntax                                                        Type                                                                              Borrow & Lifetime                                                                                                 Other
Frequency




                 2
            10

            101

            100
                     *




                                                                                                                                                 *




                                                                                                                                                                                                                                                                                                              *
                         E0070
                                 E0782
                                         E0308
                                                 E0609
                                                         E0061
                                                                 E0369
                                                                         E0107
                                                                                 E0559
                                                                                         E0560
                                                                                                 E0689
                                                                                                         E0624
                                                                                                                 E0605
                                                                                                                         E0603
                                                                                                                                 E0015
                                                                                                                                         other


                                                                                                                                                     E0502
                                                                                                                                                             E0382
                                                                                                                                                                     E0499
                                                                                                                                                                                              E0596
                                                                                                                                                                                                      E0507
                                                                                                                                                                                                              E0503
                                                                                                                                                                                                                      E0621
                                                                                                                                                                                                                              E0106
                                                                                                                                                                                                                                      E0310
                                                                                                                                                                                                                                              E0506
                                                                                                                                                                                                                                                      E0515
                                                                                                                                                                                                                                                              other
                                                                                                                                                                                                                                                                      E0255
                                                                                                                                                                                                                                                                              E0658
                                                                                                                                                                                                                                                                                      E0133
                                                                                                                                                                                                                                                                                              E0117
                                                                                                                                                                                                                                                                                                      E0583


                                                                                                                                                                                                                                                                                                                   other
Fig. 13. The error kinds detected during rollbacks span syntax errors, type errors, borrow-check and lifetime
violations, and others.


   The most frequent error on both datasets is a mismatch between an expression and its expected
type (E0308), accounting for 38.2% of reports on Translation and 37.4% on UpdatedAPI. On
Translation, it is followed by accesses to unknown fields (9.5%, E0609), reflecting the difficulty of
faithfully porting C data layouts to the provided Rust skeletons. On UpdatedAPI, the subsequent
errors are calls with a wrong number of arguments (18.1%, E0061), uses of a wrong number of
generic arguments (7.2%, E0107), initializations with nonexistent fields (7.2%, E0559), and accesses
to unknown fields (5.4%, E0609), errors that arise when a library’s public API evolves, matching the
dataset design.

A.5                   Restart Budget and Token Limit
To confirm that the restart budgets of 15 (UpdatedAPI)     100                                    8
and 20 (Translation) restarts and the token lim-
                                                                                                                                                                     Compilable Outputs (%)




                                                                                                                                                                                                                                                                                                                  Output length (k chars)
its of 20, 000 and 30, 000 tokens do not constrain                                                7
the results in §7.2, we pool the generations of all
evaluated models on both datasets and measure the           80                                    6
fraction of compilable outputs attainable within a                                                5
given number of restarts (Fig. 14). Both methods im-
prove steeply over the first few restarts and then          60                                    4
flatten: increasing the budget from 15 to 20 restarts
raises the fraction of compilable outputs by at most                                     PC       3
2.1 percentage points for either method (84.9% to                                        GC
                                                            40                                    2
87.0% for GC, 79.2% to 80.5% for PC). Per restart,             0       5       10     15      20
PC initially gains more, as each of its restarts has all                   Rollbacks
compiler errors in context at once; from four restarts
onward, however, GC surpasses it. At seven restarts, Fig. 14. Fraction of compilable outputs by restart
GC resolves 4.4 percentage points more generations budget. Both methods flatten well before 20
within the same budget. Moreover, the generated restarts. The output length (bars) stays far be-
outputs stay far below our token limits of 20, 000 low the token limit.
and 30, 000 at every restart count. We conclude that neither the restart budgets of 15 and 20 nor the
token limits constrain the compared methods.

B                    End-to-End Example
The excerpt in Fig. 15 is from the UpdatedAPI task for rustls-webpki, obtained with Claude Opus
4.8. The model is asked to update a small certificate-validation crate to a new version of the library
while filling the missing implementation in src/lib.rs. During generation, the model constructs
a certificate wrapper as a temporary and stores a trust anchor that borrows from it. Our setup
detects that the temporary would be dropped while the borrow remains live and returns the E0716
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                            1:33


diagnostic immediately. After receiving this feedback, the model binds the certificate wrapper
to a local variable, extending its lifetime; and is otherwise correct as well. The early feedback
was provided in line 4 of a 32 line function, thus preventing potentially wasteful generation of a
significant number of following code.

C     Inference Prompts
The inference code sends one user message containing the dataset prompt. The required prefix
for grading is either prefilled as the beginning of the assistant answer (open-weight models) or
appended to the user message as an instruction to start with that exact text (black-box models).

C.1    Generic Inference Wrappers
Since we require a specific prefix for grading of results but cannot prefill assistant answers for black-
box models, we append the short instruction shown in Figure 16 that specifies the required answer
prefix; it appears instantiated at the end of the dataset prompts in Figures 19 and 20. Figure 17 is the
user message appended by Generative Compilation after a rejected partial output; the rejected
output itself is added to the prompt history as an assistant message, and generation restarts from
the prefilled prefix. Figure 18 is the corresponding user message used by Post Compilation after a
rejected complete output. Here, the model responds with complete replacement files, patches in a
unified diff-like format, or a combination of both, which are applied to the previous output and
re-checked. If a returned patch fails to apply, a follow-up user message reports the patch application
error and repeats the format instructions.

C.2    UpdatedAPI
Figure 19 is the generation prompt used for UpdatedAPI inference. It is sent as the user message
for each crate instance, with the concrete file list and incomplete src/lib.rs substituted into the
placeholders.

C.3    Translation
Figure 20 is the user prompt used for Translation inference. It is instantiated with the C sources
and the incomplete Rust interface of the target file.
1:34                                         Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He



       You are given a Rust crate.                                                                                                 Prompt
       Implement only `src/lib.rs` based on the crate's documentation comments, inline comments, and tests.
       [...]
       /// Validates a certificate chain for server use.
       pub fn validate_server_usage(
            end_entity_der: &[u8], trust_anchor_der: &[u8], intermediate_ders: &[Vec<u8>]
       ) -> Result<CheckReport, CheckError> {
            unimplemented!();
       }




       [...]                                                                                                                      Assistant
       pub fn validate_server_usage(
           end_entity_der: &[u8], trust_anchor_der: &[u8], intermediate_ders: &[Vec<u8>]
       ) -> Result<CheckReport, CheckError> {
           let intermediates_seen = intermediate_ders.len();


            let ee_der = CertificateDer::from(end_entity_der);
            let end_entity = EndEntityCert::try_from(&ee_der).map_err(CheckError::Certificate)?;


            let trust_anchor = webpki::anchor_from_trusted_cert(&CertificateDer::from(trust_anchor_der))
                .map_err(CheckError::Certificate)?;
            let trust_anchors: Vec<TrustAnchor> = vec![trust_anchor];


            let intermediate_certs: Vec




       Your previous partial output was rejected by the compiler.                                                       Compiler Feedback
       Compiler error details:
       error[E0716]: temporary value dropped while borrowed
       --> src/lib.rs:155:43
            |
       155 |           webpki::anchor_from_trusted_cert(&CertificateDer::from(trust_anchor_der))
            |                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ creates a temporary value which
            |                                                                                       is freed while still in use
       156 |            .map_err(CheckError::Certificate)?;
            |                                           - temporary value is freed at the end of this statement
       157 |        let trust_anchors: Vec<TrustAnchor> = vec![trust_anchor];
            |                                                 ------------ borrow later used here
           = help: consider using a `let` binding to create a longer lived value


       Restart the generation.




       [...]                                                                                                                      Assistant
       pub fn validate_server_usage(
           end_entity_der: &[u8], trust_anchor_der: &[u8], intermediate_ders: &[Vec<u8>]
       ) -> Result<CheckReport, CheckError> {
           let intermediates_seen = intermediate_ders.len();


            let ee_der = CertificateDer::from(end_entity_der);
            let end_entity = EndEntityCert::try_from(&ee_der).map_err(CheckError::Certificate)?;


            let trust_anchor_cert = CertificateDer::from(trust_anchor_der);
            let trust_anchor = webpki::anchor_from_trusted_cert(
                &trust_anchor_cert
            ).map_err(CheckError::Certificate)?;
            let trust_anchors: Vec<TrustAnchor> = vec![trust_anchor];


            let intermediate_certs: Vec<CertificateDer> = intermediate_ders
                .iter()
                .map(|der| CertificateDer::from(der.as_slice()))
                .collect();


            let now = unix_time_now()?;
            let policy = UsagePolicy::server();
            [...]




Fig. 15. End-to-end excerpt from a GC run by Claude Opus 4.8 on the rustls-webpki API-update task. The
partial output borrows from a temporary CertificateDer and is rejected with E0716. After receiving the
diagnostic, the model introduces the longer-lived trust_anchor_cert binding and generates semantically
valid code.
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                                         1:35



    Start your response with this exact prefix:
    {prefilled_answer}




Fig. 16. Instruction appended to the user message when inference is run with an empty initial assistant
answer. It replaces the usual prefilled assistant prefix by requiring the model to emit that prefix itself.


    Your previous partial output was rejected by the compiler.
    Compiler error details:
    {rendered_compiler_details}


    Restart the generation.




Fig. 17. Feedback message used by Generative Compilation. The prompt history first receives the rejected
partial assistant output {prefix}{code}, followed by this user message with rendered compiler diagnostics.


    Your previous output was rejected by the compiler.
    Compiler error details:
    {rendered_compiler_details}


    Return only the changes needed to fix the current project output. You may use any combination of these two
          formats in the same answer:


    1. Regenerate complete Rust files that should replace files from the current project state. Use this format
          for each regenerated file:
    {path/to/file.rs}
    ```rust
    // complete replacement Rust file
    ```

    2. Return one or more patches that edit the previous output. Use this exact patch format:
    *** Begin Patch
    *** Update File: path/to/file.rs
    @@
    -old line
    +new line
    *** End Patch


    Omitted files stay fixed exactly as currently generated.




Fig. 18. Feedback message used by Post Compilation. The prompt history first receives the rejected complete
assistant output, followed by this user message with the rendered compiler diagnostics. The model may
respond with full replacement files, patches, or a combination; the result is applied and re-checked.
1:36                                   Niels Mündler-Sasahara, Hristo Venev, Dawn Song, Martin Vechev, and Jingxuan He



       You are given a Rust crate.
       Implement only `{interface_path}` based on the crate's documentation comments, inline comments, and tests.


       Please follow these instructions:
         - Implement all `unimplemented!()` sections in `{interface_path}`.
         - Keep function signatures unchanged.
         - Produce compiling Rust code.
         - Do not use `unsafe`.
         - Return only the completed `{interface_path}` file contents.


       Return only:
         {interface_path}
        ```rust
         // completed Rust code
        ```

       These are the files:


       {path_1}
       ```{language_1}
       {code_1}
       ```

       ...


       {path_n}
       ```{language_n}
       {code_n}
       ```

       {interface_path} (incomplete)
       ```rust
       {interface_code}
       ```

       Start your response with this exact prefix:
       {interface_path}
       ```rust




Fig. 19. User prompt for UpdatedAPI. The model receives the crate files, including tests and comments, and
is asked to implement only the incomplete interface file; {interface_path} is instantiated with src/lib.rs.
The trailing prefix instruction replaces the prefilled assistant answer for black-box models (§C.1).
Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code                                           1:37



    You are an expert at converting C To Rust.
    You will be provided with C source files in the format:


    {filename.c / filename.h}
    ```c
    // Input C code
    ```

    You will also be given the Rust Interface definition corresponding to the C file that you must implement by
            filling in the unimplemented!() parts based on the C code.
    The Rust Interface file will be in the format:


    {filename.rs}
    ```rust
    // Rust Interface code
    ```

    I need you to transpile the provided code files from C to Rust.
    Please follow the instructions provided below:
      - Each C file I provide MUST be transpiled into a corresponding Rust file.
      - You MUST use the same name as the Rust interface file name, when generating the transpiled Rust Code
      - You MUST always implement the Rust Interface files using the C code as reference.
      - You MUST ensure that you implement ALL unimplemented!() parts strictly.
      - You MUST NOT change the function signatures of the Rust code.
      - Each transpiled Rust file MUST compile.
      - The transpiled Rust code MUST be observationally equivalent to the C code.
      - The transpiled Rust code MUST NOT contain Foreign Function Interface calls, such as the libc library.
      - The transpiled Rust code MUST NOT contain unsafe blocks.
      - You must ensure that you import the required files that are referenced in each Rust file.
      - You may derive traits for the data types that are defined, to elicit required behavior during
                implementation. For instance you can add #[derive(Clone)] for structs when the Clone trait is required
                 for implementation.
      - All imports in the rust file must be in the following format -
          ```rust
            use crate::file_name::module;
          ```

    Please think step-by-step and return your final solution for the transpiled file in the following format:


      {filename.rs}
      ```rust
      // Generated Rust Code
      ```


            These are the files:
    {c_sources}


    {interface_path} (incomplete)
    ```rust
    {interface_code}
    ```

    Start your response with this exact prefix:
    {interface_path}
    ```rust




Fig. 20. User prompt for Translation. It gives the C sources and the incomplete Rust interface of the target
file. The trailing prefix instruction replaces the prefilled assistant answer for black-box models (§C.1).
