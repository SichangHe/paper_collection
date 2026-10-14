                                             Constant-Time Foundations for the New Spectre Era
                                                                      Sunjay Cauligi† Craig Disselkoen† Klaus v. Gleissenthall†
                                                                     Dean Tullsen† Deian Stefan† Tamara Rezk⋆ Gilles Barthe♠♣
                                                                                 † UC San Diego, USA              ⋆ INRIA Sophia Antipolis, France
                                                                    ♠ MPI for Security and Privacy, Germany                  ♣ IMDEA Software Institute, Spain


                                        Abstract                                                                             Unfortunately, these guarantees are moot for most modern
                                        The constant-time discipline is a software-based countermea-                      hardware: Spectre [20], Meltdown [22], ZombieLoad [29],
                                        sure used for protecting high assurance cryptographic imple-                      RIDL [32], and Fallout [5] are all dramatic examples of attacks
arXiv:1910.01755v3 [cs.CR] 8 May 2020




                                        mentations against timing side-channel attacks. Constant-                         that exploit microarchitectural features. These attacks reveal
                                        time is effective (it protects against many known attacks),                       that code that is deemed constant-time in the usual sense
                                        rigorous (it can be formalized using program semantics), and                      may, in fact, leak information on processors with microar-
                                        amenable to automated verification. Yet, the advent of micro-                     chitectural features. The decade-old constant-time recipes
                                        architectural attacks makes constant-time as it exists today                      are no longer enough.2
                                        far less useful.                                                                     In this work, we lay the foundations for constant-time in
                                           This paper lays foundations for constant-time program-                         the presence of microarchitectural features that have been
                                        ming in the presence of speculative and out-of-order exe-                         exploited in recent attacks: out-of-order and speculative ex-
                                        cution. We present an operational semantics and a formal                          ecution. We focus on constant-time for two key reasons.
                                        definition of constant-time programs in this extended setting.                    First, impact: constant-time programming is largely used in
                                        Our semantics eschews formalization of microarchitectural                         real-world crypto libraries—and high-assurance code—where
                                        features (that are instead assumed under adversary control),                      developers already go to great lengths to eliminate leaks via
                                        and yields a notion of constant-time that retains the ele-                        side-channels. Second, foundations: constant-time program-
                                        gance and tractability of the usual notion. We demonstrate                        ming is already rooted in foundations, with well-defined
                                        the relevance of our semantics in two ways: First, by con-                        semantics [4, 8]. These semantics consider very powerful
                                        trasting existing Spectre-like attacks with our definition of                     attackers—e.g., attackers in [4] have control over the cache
                                        constant-time. Second, by implementing a static analysis                          and the scheduler. An advantage of considering powerful
                                        tool, Pitchfork, which detects violations of our extended                         attackers is that the semantics can overlook many hardware
                                        constant-time property in real world cryptographic libraries.                     details—e.g., since the cache is adversarially controlled, there
                                                                                                                          is no point in modeling it precisely—making constant-time
                                        Keywords: Spectre; speculative execution; semantics; static                       amenable to automated verification and enforcement.
                                        analysis
                                                                                                                          Contributions. We first define a semantics for an abstract,
                                                                                                                          three-stage (fetch, execute, and retire) machine. Our machine
                                        1     Introduction                                                                supports out-of-order and speculative execution by model-
                                        Protecting secrets in software is hard. Security and cryptog-                     ing reorder buffers and transient instructions, respectively.
                                        raphy engineers must write programs that protect secrets,                         We assume that attackers have complete control over mi-
                                        both at the source level and when they execute on real hard-                      croarchitectural features (e.g., the branch target predictor)
                                        ware. Unfortunately, hardware too easily divulges informa-                        when executing a victim program and model the attacker’s
                                        tion about a program’s execution via timing side-channels—                        control over predictors using directives. This keeps our se-
                                        e.g., an attacker can learn secrets by simply observing (via                      mantics simple yet powerful: our semantics abstracts over
                                        timing) the effects of a program on the hardware cache [16].                      all predictors when proving security—of course, assuming
                                           The most robust way to deal with timing side-channels                          that predictors themselves do not leak secrets. We further
                                        is via constant-time programming—the paradigm used to im-                         show how our semantics can be extended to capture new
                                        plement almost all modern cryptography [2, 11, 12, 26, 27].                       predictors—e.g., a hypothetical memory aliasing predictor.
                                        Constant-time programs can neither branch on secrets nor                             We then define speculative constant-time, an extension of
                                        access memory based on secret data.1 These restrictions                           constant-time for machines with out-of-order and specula-
                                        ensure that programs do not leak secrets via timing side-                         tive execution. This definition allows us to discover microar-
                                        channels on hardware without microarchitectural features.                         chitectural side channels in a principled way—all four classes
                                        1 More generally, constant-time programs cannot use secret data as input to       of Spectre attacks as classified by Canella et al. [6], for ex-
                                        any variable-time operation—e.g., floating-point multiplication.                  ample, manifest as violations of our constant-time property.
                                        ,,                                                                                2 OpenSSL found this situation so hopeless that they recently updated their

                                        .                                                                                 security model to explicitly exclude “physical system side channels” [25].
                                                                                                                      1
,,                                                          S. Cauligi, C. Disselkoen, K. v. Gleissenthall, D. Tullsen, D. Stefan, T. Rezk, and G. Barthe


   We further use our semantics as the basis for a prototype                            Registers                           Program
analysis tool, Pitchfork, built on top of the angr symbolic                        r      ρ(r )                   n    µ(n)
execution engine [30]. Like other symbolic analysis tools,                        ra      9pub                    1    br(>, (4, r a ), 2, 4)
                                                                                        Memory                    2    (rb = load([40, r a ], 3))
Pitchfork suffers from path explosion, which limits the depth
                                                                                  a       µ(a)                    3    (rc = load([44, rb ], 4))
of speculation we can analyze. Nevertheless, we are able to                       40..43 array Apub               4    ...
use Pitchfork to detect multiple Spectre bugs in real code.                       44..47 array Bpub
We use Pitchfork to detect leaks in the well-known Kocher                         48..4B array Keysec
test cases [19] for Spectre v1, as well as our more exten-
sive test suite which includes Spectre v1.1 variants. More                                           Speculative execution:
significantly, we use Pitchfork to analyze—and find leaks                          Directive       Effect on reorder buffer        Leakage
in—real cryptographic code from the libsodium, OpenSSL,                            fetch: true     1 7→ br(>, (4, r a ), 2, (2, 4))
and curve25519-donna libraries.                                                    fetch           2 7→ (rb = load([40, r a ]))
Open source. Pitchfork and our test suites are open source                         fetch           3 7→ (rc = load([44, rb ]))
and available at https://pitchfork.programming.systems.                            execute 2       2 7→ (rb = Key[1]sec )           read 49pub
                                                                                   execute 3       3 7→ (rc = X )                   read a sec
                                                                                                   where a = Key[1]sec + 44
2    Motivating Examples
In this section, we show why classical constant-time pro-                  Figure 1. Example demonstrating a Spectre v1 attack. The
gramming is insufficient when attackers can exploit microar-               branch at 1 acts as bounds check for array A. The execution
chitectural features. We do this via two example attacks and               speculatively ignores the bounds check, and leaks a byte of
show how these attacks are captured by our semantics.                      the secret Key.
Classical constant time is not enough. Our first example
consists of 3 lines of code, shown in Figure 1 (top right). The
program, a variant of the classical Spectre v1 attack [20],                information (see Table 1). For instance, the transient version
branches on the value of register r a (line 1). If r a ’s value            of the branch instruction records which branch has been
is smaller than 4, the program jumps to program location                   speculatively taken.
2, where it uses r a to index into a public array A, saves the                In our example, the attacker next instructs the model to
value into register rb , and uses rb to index into another public          execute the first load, using the directive execute 2. Because
array B. If r a is larger than or equal to 4 (i.e., the index is out       the bounds check has not yet been executed, the load reads
of bounds), the program skips the two load instructions and                from the secret element Key[1], placing the value in rb . The
jumps to location 4. In a sequential execution, this program               attacker then issues directive execute 3 to execute the fol-
neither loads nor branches on secret values. It thus trivially             lowing load; this load’s address is calculated as 44 + Key[1].
satisfies the constant-time discipline.                                    Accessing this address affects externally visible cache state,
   However, modern processors do not execute sequentially.                 allowing the attacker to recover Key[1] through a cache side-
Instead, they continue fetching instructions before prior                  channel attack [16]. This is encoded by the leakage observa-
instructions are complete. In particular, a processor may                  tion shown in red on the bottom right. Though this secret
continue fetching instructions beyond a conditional branch,                leakage cannot happen under sequential execution, our se-
before evaluating the branch condition. In that case, the pro-             mantics clearly highlights the possible leak when we account
cessor guesses which branch will be taken. For example, the                for microarchitectural features.
processor may erroneously guess that the branch condition                  Modeling hypothetical attacks. Next, we give an example
at line 1 evaluates to true, even though r a contains value 9. It          of a hypothetical class of Spectre attack captured by our
will therefore continue down the “true” branch speculatively.              extended semantics. The attack is based on a microarchi-
In hardware, such guesses are made by a branch prediction                  tectural feature which would allow processors to speculate
unit, which may have been mistrained by an adversary.                      whether a store and load pair might operate on the same
   These guesses, as well as additional choices such as exe-               address, and forward values between them [18, 28].
cution order, are directly supplied by the adversary in our                   We demonstrate this attack in Figure 2. The reorder buffer,
semantics. We model this through a series of directives, as                after all instructions have been fetched, is shown in the top
shown on the bottom left of Figure 1. The directive fetch: true            right. The program stores the value of register rb into the
instructs our model to speculatively follow the true branch                secretKeysec array and eventually loads two values from pub-
and to place the fetched instruction at index 1 in the reorder             lic arrays. The attacker first issues the directive execute 2 :
buffer. Similarly, the two following fetch directives place the            value; this results in a buffer where the store instruction at 2
loads at indices 2 and 3 in the buffer. The instructions in the            has been modified to record the resolved value x sec . Next, the
reorder buffer, called transient instructions, do not necessarily          attacker issues the directive execute 7 : fwd 2, which causes
match the original instructions, but can contain additional                the model to mispredict that the load at 7 aliases with the
                                                                       2
Constant-Time Foundations for the New Spectre Era                                                                                              ,,


               Registers                    Reorder buffer
          r       ρ(r )                i   buf (i)
                                                                                                
                                                                                                
                                                                                                vℓ   if max(j) < i : buf (j) = (r = _) ∧
                                                                                                            buf (j) = (r = v ℓ )
                                                                                                
         ra                                store(rb , [40, r a ])
                                                                                                
                                                                             (buf +i ρ)(r ) =
                  2pub                 2                                                        
                                                                                                
         rb      x sec                     ...                                                
                                                                                               ρ(r ) if ∀j  < i : buf (j) , (r = _)
                                           (rc = load([45]))
                                                                                              
               Memory                  7                                                      
                                                                                              ⊥      otherwise
         a        µ(a)                     (rc = load([48, rc ]))
                                       8
                                                                                              
         40..43 secretKeysec
         44..47 pubArrApub                                                         Figure 3. Definition of the register resolve function.
         48..4B pubArrBpub

                        Speculative execution                                Values and labels. As a convention, we use n for memory
    Directive           Effect on buf                       Leakage          addresses that map to instructions, and a for addresses that
    execute 2 : value   2 7→ store(x sec , [40, r a ])                       map to data. Each value is annotated with a label from a
    execute 7 : fwd 2   7 7→ (rc = load([45], x sec , 2))                    lattice of security labels with join operator ⊔. For brevity,
    execute 8           8 7→ (rc = X {⊥, a})                read a sec       we sometimes omit public label annotation on values.
    execute 2 : addr    2 7→ store(rb , 42pub )             fwd 42pub
                                                                                Using labels, we define an equivalence ≃pub on configura-
                                                            rollback,
    execute 7           {7, 8} < buf                                         tions. We say that two configurations are equivalent if they
                                                            fwd 45pub
                         where a = x sec + 48                                coincide on public values in registers and memories.
                                                                             Reorder buffer. The reorder buffer maps buffer indices (nat-
Figure 2. Example demonstrating a hypothetical attack abus-                  ural numbers) to transient instructions. We write buf (i) to
ing an aliasing predictor. This attack differs from prior spec-              denote the instruction at index i in buffer buf , if i is in buf ’s
ulative data forwarding attacks in that branch misprediction                 domain. We write buf [i 7→ instr] to denote the result of ex-
is not needed.                                                               tending buf with the mapping from i to instr, and buf \buf (i)
                                                                             for the function formed by removing i from buf ’s domain.
                                                                             We write buf [j : j < i] to denote the restriction of buf ’s
                                                                             domain to all indices j, s.t. j < i (i.e., removing all map-
store at 2, and thus to forward the value x sec to the load. The
                                                                             pings at indices i and greater). Our rules add and remove
forwarded value x sec is then used in the address a = 48 + x sec
                                                                             indices in a way that ensures that buf ’s domain will always
of the load instruction at index 8. There, the loaded value X
                                                                             be contiguous.
is irrelevant, but the address a is leaked to the attacker, al-
lowing them to recover the secret value x sec . The speculative              Notation. We let MIN(M) (resp. MAX(M)) denote the mini-
execution continues and rolls back when the misprediction                    mum (maximum) index in the domain of a mapping M. We de-
is detected (details on this are given in Section 3), but at this            note the empty mapping as ∅ and let MIN(∅) = MAX(∅) = 0.
point, the secret has already been leaked.                                      For a formula φ, we may discuss the bounded highest
   As with the example in Figure 1, the program in this ex-                  (lowest) index for which a formula holds. We write max(j) <
ample follows the (sequential) constant-time discipline, yet                 i : φ(j) to mean that j is the highest index less than i for
leaks during speculative execution. But, both examples are                   which φ holds, and define min(j) > i : φ(j) analogously.
insecure under our new notion of speculative constant-time                   Register resolve function. In Figure 3, we define the register
as we discuss next.                                                          resolve function, which we use to determine the value of
                                                                             a register in the presence of transient instructions in the
3     Speculative Semantics and Security                                     reorder buffer. For index i and register r , the function may
In this section we define the notion of speculative constant                 (1) return the latest assignment to r prior to position i in the
time, and propose a speculative semantics that models exe-                   buffer, if the corresponding operation is already resolved;
cution on modern processors. We start by laying the ground-                  (2) return the value from the register map ρ, if there are no
work for our definitions and semantics.                                      pending assignments to r in the buffer; or (3) be undefined.
                                                                             Note that if the latest assignment to r is yet unresolved then
Configurations. A configuration C ∈ Confs represents the                     (buf +i ρ)(r ) = ⊥. We extend this definition to values by
state of execution at a given step. It is defined as a tuple                 defining (buf +i ρ)(v ℓ ) = v ℓ for all v ℓ ∈ V, and lift it to lists
(ρ, µ, n, buf ) where:                                                       of registers or values using a pointwise lifting.
     ▶ ρ : R ⇀ V is a map from a finite set of register names
       R to values;                                                          3.1     Speculative Constant-Time
     ▶ µ : V ⇀ V is a memory;                                                We present our new notion of constant-time security in terms
     ▶ n : V is the current program point;                                   of a small-step semantics, which relates program configura-
     ▶ buf : N ⇀ TransInstr is the reorder buffer.                           tions, observations, and attacker directives.
                                                                         3
,,                                                            S. Cauligi, C. Disselkoen, K. v. Gleissenthall, D. Tullsen, D. Stefan, T. Rezk, and G. Barthe


                                       Table 1. Instructions and their transient instruction form.

                             Instruction               Transient form(s)
     arithmetic operation                              (r = op(op, −rv))
                                                                    −−−−
                                                                      ⃗                         (unresolved op)
                           (r = op(op, −rv,
                                        −−−− ′
                                          ⃗ n ))
     (op specifies opcode)                             (r = v ℓ )                               (resolved value)
                                                       br(op, −rv,
                                                               −−−−
                                                                 ⃗ n 0 , (n true , n false ))   (unresolved conditional)
      conditional branch br(op, −rv,
                                 −−−− true false
                                   ⃗ n ,n )
                                                       jump n 0                                 (resolved conditional)
                                                                    −−−− n
                                                       (r = load(−rv))⃗                         (unresolved load)
            memory load                                (r = load(rv,  ⃗ (v ℓ , j)))n
                                                                   −−−−−
                                                                                                (partially resolved load with dependency on j)
                          (r = load(−rv,
                                     −−−− ′
                                       ⃗ n ))
     (at program point n)                              (r = v ℓ {⊥, a})n                        (resolved load without dependencies)
                                                       (r = v ℓ {j, a})n                        (resolved load with dependency on j)
                                                       store(rv, −rv)
                                                                  −−−−
                                                                    ⃗                           (unresolved store)
            memory store store(rv, −rv,
                                    −−−− ′
                                      ⃗n)
                                                       store(v ℓ , a ℓ )                        (resolved store)
            indirect jump jmpi(−rv)
                                −−−−
                                  ⃗                    jmpi(−rv,
                                                             −−−−
                                                               ⃗ n0 )                           (unresolved jump predicted to n 0 )
                             call(n f , n ret )        call                                     (unresolved call)
            function calls
                             ret                       ret                                      (unresolved return)
        speculation fence    fence n                   fence                                    (no resolution step)


   Our semantics does not directly model caches, nor any                       retired instructions, i.e., N = #{d ∈ D | d = retire}. When
of the predictors used by speculative semantics. Rather, we                    such a big step from C to C ′ is possible, we say D is a well-
model externally visible effects—memory accesses and con-                      formed schedule of directives for C. We omit D, N , or O when
trol flow—by producing a sequence of observations. We can                      not used.
thus reason about any possible cache implementation, as
any cache eviction policy can be expressed as a function of                    Definition 3.1 (Speculative constant-time). We say a config-
the sequence of observations. Furthermore, exposing control                    uration C with schedule D satisfies speculative constant-time
flow observations directly in our semantics makes it unnec-                    (SCT) with respect to a low-equivalence relation ≃pub iff for
essary for us to track various other side channels. Indeed,                    every C ′ such that C ≃pub C ′:
while channels such as port contention or register renaming                          C D⇓O C 1 iff C ′ D⇓O ′ C 1′ and C 1 ≃pub C 1′ and O = O ′ .
produce distinct measurable effects [20], they only serve to
leak the path taken through the code—and thus modeling                         A program satisfies SCT iff every initial configuration satis-
these observations separately would be redundant. For the                      fies SCT under any schedule.
same reason, we do not model a particular branch predic-
tion strategy; we instead let the attacker resolve scheduling                  Aside, on sequential execution. Processors work hard to
non-determinism by supplying a series of directives.                           create the illusion that assembly instructions are executed
   This approach has two important consequences. First, the                    sequentially. We validate our semantics by proving equiv-
use of observations and directives allows our semantics to                     alence with respect to sequential execution. Formally, we
remain tractable and amenable to verification. For instance,                   define sequential schedules as schedules that execute and re-
we do not need to model the behavior of the cache or any                       tire instructions immediately upon fetching them. We attach
branch predictor. Second, our notion of speculative constant-                  to each program a canonical sequential schedule and write
                                                                                   N
time is robust, i.e., it holds for all possible branch predictors              C ⇓seq C ′ to model execution under this canonical schedule.
and replacement policies—assuming that they do not leak                        Our sequential validation is defined relative to an equiva-
secrets directly, a condition that is achieved by all practical                lence ≈ on configurations. Informally, two configurations
hardware implementations.                                                      are equivalent if their memories and register files are equal,
                                                  o
   Given an attacker directive d, we use C ,→     d
                                                    C ′ to denote              even if their speculative states may be different.
the execution step from configuration C to configuration C ′
that produces observation o. Program execution is defined                      Theorem 3.2 (Sequential equivalence). Let C be an initial
                                                                                                                                       N
from the small-step semantics in the usual style. We use                       configuration and D a well-formed schedule for C. If C ⇓D C1 ,
      N ′                                                                              N
C O⇓D   C to denote a sequence of execution steps from C to                    then C ⇓seq C 2 and C 1 ≈ C 2 .
C ′. Here D and O are the concatenation of the single-step
directives and leakages, respectively; N is the number of                        Complete definitions, more properties, and proofs are
                                                                               given in Appendix B.
                                                                           4
Constant-Time Foundations for the New Spectre Era                                                                                                   ,,


3.2    Overview of the Semantics                                           a branch predictor chooses which branch to execute; in our
As shown in Table 1, each instruction has a physical form                  semantics, the directives fetch: true and fetch: false deter-
and one or more transient forms. Our semantics operates on                 mine which of the rules to execute. This allows us to abstract
these instructions similar to a multi-stage processor pipeline.            over all possible predictor implementations.
Physical instructions are fetched from memory and become                   Execute. Next, we describe the rules for the execute stage.
transient instructions in the reorder buffer. They are then                         cond-execute-correct
executed until they are fully resolved. Finally they are retired,                         buf (i) = br(op, −rv,  −−−−
                                                                                                                   ⃗ n 0 , (n true , n false ))
updating the non-speculative state in the configuration.                                         ∀j < i : buf (j) , fence
   In the rest of this section, we show how we model specula-                        (buf +i ρ)(−rv)
                                                                                                   −−−−
                                                                                                     ⃗ = −v−−−⃗ℓ−−        Jop(−v−−−⃗ℓ−−)K = trueℓ
tive execution (Section 3.3), memory operations (Section 3.4),                      n true
                                                                                           = n0         buf = buf [i 7→ jump n true ]
                                                                                                            ′
aliasing prediction (Section 3.5), and fence instructions (Sec-                                             jump n true
                                                                                                                   ℓ
tion 3.6). We also briefly describe indirect jumps and function                         (ρ, µ, n, buf ) ,−−−−−−−→ (ρ, µ, n, buf ′)
                                                                                                             execute i
calls (Section 3.7), which are presented in full in Appendix A.
                                                                               cond-execute-incorrect
   Our semantics captures a variety of existing Spectre vari-
                                                                                         buf (i) = br(op, −rv,  −−−−
                                                                                                                  ⃗ n 0 , (ntrue , n false ))
ants, including v1 (Figure 1), v1.1 (Figure 6), and v4 (Figure 7),
as well as a new hypothetical variant (Figure 2). Additional                                    ∀j < i : buf (j) , fence
variants (e.g., v2 and ret2spec) can be expressed with the ex-                        (buf +i ρ)(−rv)
                                                                                                  −−−−
                                                                                                    ⃗ = −v−−−⃗ℓ−−        Jop(−v−−−⃗ℓ−−)K = trueℓ
tended semantics given in Appendix A. Our semantics shows                      n true
                                                                                      , n0      buf = buf [j : j < i][i 7→ jump n true ]
                                                                                                      ′

that these attacks violate SCT by producing observations                                            rollback,jump n true
                                                                                                                    ℓ
depending on secrets.                                                            (ρ, µ, n, buf ) ,−−−−−−−−−−−−−−−→ (ρ, µ, ntrue , buf ′)
                                                                                                          execute i
                                                                           Both rules evaluate the condition op via an evaluation func-
3.3    Speculative Execution
                                                                           tion J·K. In both, the function produces true; but the false
We start with the semantics for conditional branches which                 rules are analogous. The rules then compare the actual branch
introduce speculative execution.                                           target n true against the speculatively chosen target n 0 from
Conditional branching. The physical instruction for con-                   the fetch stage.
ditional branches has the form br(op, −rv,     −−−− true false
                                                 ⃗ n , n ), where             If the correct path was chosen during speculation, i.e., n 0
op is a Boolean operator whose result determines whether                   agrees with the correct branch ntrue , rule cond-execute-
or not to execute the jump, −rv      −−−−
                                       ⃗ are the operands to op, and       correct updates buf with the fully resolved jump instruc-
n true and n   false  are the program points for the true and false        tion and emits an observation: jump n trueℓ . This models an
branches, respectively.                                                    attacker that can observe control flow, e.g., by timing execu-
    We show br’s transient counterparts in Table 1. The unre-              tions along different paths. The leaked observation n true has
solved form extends the physical instruction with a program                label ℓ, propagated from the evaluation of the condition.
point n 0 , which is used to record the branch that is executed               In case the wrong path was taken during speculation, i.e.,
(n true or n false ) speculatively, and may or may not correspond          the calculated branch ntrue disagrees with n 0 , the semantics
to the branch that is actually taken once op is resolved. The              must roll back all execution steps along the erroneous path.
resolved form contains the final jump target.                              For this, rule cond-execute-incorrect removes all entries
Fetch. We give the rule for the fetch stage below.                         in buf that are newer than the current instruction (i.e., all
      cond-fetch
                                                                           entries j ≥ i), sets the program point n to the correct branch,
      µ(n) = br(op, −rv,
                     −−−− true false
                       ⃗ n ,n )            i = MAX(buf ) + 1               and updates buf at index i with correct value for the resolved
         buf = buf [i 7→ br(op, −rv,
            ′                      −−−− true
                                     ⃗ n , (ntrue , nfalse ))]             jump instruction. Since an attacker can observer misspec-
                                                                           ulation through instruction timing [20], the rule issues a
            (ρ, µ, n, buf ) ,−−−−−−−→ (ρ, µ, n true , buf ′)               rollback observation in addition to the jump observation.
                            fetch: true

The cond-fetch rule speculatively executes the branch de-                  Retire. The rule for the retire stage is shown below; its only
termined by a Boolean value b given by the directive. We                   effect is to remove the jump instruction from the buffer.
show the case for b = true; the case for false is analogous.                        jump-retire
The rule updates the current program point n, allowing exe-                                        MIN(buf ) = i
cution to continue along the specified branch. The rule then                         buf (i) = jump n 0  buf ′ = buf \ buf (i)
records the chosen branch n true (resp. n false ) in the transient                         (ρ, µ, n, buf ) ,−−−−→ (ρ, µ, n, buf ′)
                                                                                                               retire
jump instruction.
   This semantics models the behavior of most modern pro-                  Examples. Figure 4 shows how branch prediction affects the
cessors. Since the target of the branch cannot be resolved                 reorder buffer. In part (a), the branch at index 4 is predicted
in the fetch stage, speculation allows execution to continue               correctly. The jump instruction is resolved, and execution
and not stall until the branch target is resolved. In hardware,            proceeds as normal. In part (b), the branch at index 4 is
                                                                       5
,,                                                                 S. Cauligi, C. Disselkoen, K. v. Gleissenthall, D. Tullsen, D. Stefan, T. Rezk, and G. Barthe

                         (a) Predicted correctly                                     To model these store forwarding semantics, we use an-
       i    Initial buf (i)              buf (i) after execute 4                  notations to recall if a load was resolved from memory or
            (rb = 4)                     (rb = 4)
       3
                                                                                  forwarding. A resolved load has the form (r = v ℓ {j, a})n ,
            br(<, (2, r a ), 9, (9, 12)) jump 9
                                                                                  where the index j records either the buffer index of the store
       4
       5    (rc = op(+, (1, rb )))       (rc = op(+, (1, rb )))
                                                                                  instruction that forwarded its value to the load, or ⊥ if the
                       (b) Predicted incorrectly                                  value was taken from memory. We also record the memory
       i   Initial buf (i)               buf (i) after execute 4                  address a associated with the data, and retain the program
       3   (rb = 4)                      (rb = 4)                                 point n of the load instruction that generated the value in-
       4   br(<, (2, r a ), 12, (9, 12)) jump 9                                   struction. The resolved load otherwise behaves as a resolved
       5   (rd = op(*, (rд , rh )))      -                                        value instruction (e.g., for the register resolve function).
                                                                                  Fetch. We now discuss the inference rules for memory oper-
Figure 4. Correct and incorrect branch prediction. Initially,                     ations, starting with the fetch stage.
r a = 3. In (b), the misprediction causes a rollback to 4.                           simple-fetch
                                                                                       µ(n) ∈ {op, load, store, fence }     n ′ = next(µ(n))
incorrectly predicted. Upon executing the branch, the mis-                           i = MAX(buf ) + 1       buf = buf [i 7→ transient(µ(n))]
                                                                                                                 ′

prediction is detected, and buf is rolled back to index 4.                                          (ρ, µ, n, buf ) ,−−−→ (ρ, µ, n ′, buf ′)
                                                                                                                     fetch
3.4   Memory Operations                                                           Given a fetch directive, rule simple-fetch extends the re-
The physical instruction for loads is (r = load(−rv,
                                                  −−−− ′
                                                    ⃗ n )), while                 order buffer buf with a new transient instruction (see Ta-
                                  −−−−− ′
the form for stores is store(rv, rv, ⃗ n ). As before, n ′ is the                 ble 1). Other than load and store, the rule also applies to
program point of the next instruction. For loads, r is the                        op and fence instructions. The transient(·) function simply
register receiving the result; for stores, rv is the register or                  translates the physical instruction at µ(n) to its unresolved
value to be stored. For both loads and stores, −rv −−−−
                                                     ⃗ is a list of               transient form. It inserts the new, transient instruction at the
operands (registers and values) which are used to calculate                       first empty index in buf , and sets the current program point
the operation’s target address.                                                   to the next instruction n ′. Note that transient(·) annotates
   Transient counterparts of load and store are given in Ta-                      the transient load instruction with its program point.
ble 1. We annotate unresolved load instructions with the                          Load execution. Next, we cover the rules for the load exe-
program point of the physical instruction that generated                          cute stage.
them; we omit annotations whenever not used. Unresolved                               load-execute-nodep
and resolved store instructions share the same syntax, but                                                   −−−− n
                                                                                       buf (i) = (r = load(−rv))
                                                                                                               ⃗          ∀j < i : buf (j) , fence
for resolved stores, both address and operand are required                                                −−−−−    −−−−−−
                                                                                               (buf +i ρ)(rv)⃗ = v⃗ℓ       Jaddr(−v−−−⃗ℓ−−)K = a
to be single values.                                                                                 −−−
                                                                                              ℓa = ⊔ℓ ⃗      ∀j < i : buf (j) , store(_, a)
Address calculation. We assume an arithmetic operator                                     µ(a) = v ℓ     buf ′ = buf [i 7→ (r = v ℓ {⊥, a})n ]
addr which calculates target addresses for stores and loads                                                         read a ℓa
from its operands. We leave this operation abstract in order to                                   (ρ, µ, n, buf ) ,−−−−−−→ (ρ, µ, n, buf ′)
                                                                                                                    execute i
model a large variety of architectures. For example, in a sim-
                            −−−
ple addressing mode, Jaddr(v)K
                             ⃗ might compute the sum of its                          load-execute-forward
                                                                                                               −−−− n
operands; in an x86-style address mode, Jaddr([v 1 , v 2 , v 3 ])K                    buf (i) = (r = load(−rv))  ⃗        ∀j < i : buf (j) , fence
                                                                                                   −−−−−  −−−−−−                                  −−−
might instead compute v 1 + v 2 · v 3 .                                                (buf +i ρ)(rv) ⃗ = v⃗ℓ         Jaddr(−v−−−⃗ℓ−−)K = a ℓa = ⊔⃗ℓ
Store forwarding. Multiple transient load and store instruc-                         max(j) < i : buf (j) = store(_, a) ∧ buf (j) = store(v ℓ , a,)
tions may exist concurrently in the reorder buffer. In par-                                       buf ′ = buf [i 7→ (r = v ℓ {j, a})n ]
ticular, there may be unresolved loads and stores that will                                                          fwd a ℓa
                                                                                                  (ρ, µ, n, buf ) ,−−−−−−→ (ρ, µ, n, buf ′)
read or write to the same address in memory. Under a naive                                                          execute i
model, we must wait to execute load instructions until all                           Given an execute directive for buffer index i, under the
prior store instructions have been retired, in case they write                    condition that i points to an unresolved load, rule load-
to the address we will load from. Indeed, some real-world                         execute-nodep applies if there are no prior store instruc-
processors behave exactly this way [10].                                          tions in buf that have a resolved, matching address. The rule
   For performance, most modern processors implement store-                       first resolves the operand list −rv
                                                                                                                   −−−−
                                                                                                                     ⃗ into a list of values −v−−−⃗ℓ−−, and
                                                                                             −−−−−−
forwarding for memory operations: if a load reads from the                        then uses v⃗ℓ to calculate the target address a. It then retrieves
same address as a prior store and the store has already been                      the current value v ℓ at address a from memory, and finally
resolved, the processor can forward the resolved value to                         adds to the buffer a resolved value instruction assigning v ℓ to
the load. The load can then proceed without waiting for the                       the target register r . We annotate the value instruction with
store to commit to memory [34].                                                   the address a and ⊥, signifying that the value comes from
                                                                              6
Constant-Time Foundations for the New Spectre Era                                                                                                 ,,


memory. Finally, the rule produces the observation read a ℓa ,                  Registers           ρ(r a ) = 40pub
which renders the memory read at address a with label ℓa                        Directives          D= execute 4; execute 3 : addr
visible to an attacker.                                                         Leakage for D       fwd 43pub ; rollback, fwd 43pub
   Rule load-execute-forward applies if the most recent                   starting buf             buf after execute 4      buf after D
store instruction in buf with a resolved, matching address                2 store(12, 43pub )      2 store(12, 43pub )      2 store(12, 43pub )
has a resolved data value. Instead of accessing memory, the               3 store(20, [3, r a ])   3 store(20, [3, r a ])   3 store(20, 43pub )
rule forwards the value from the store instruction, annotat-              4 (rc = load([43]))      4 (rc = 12{2, 43})
ing the new value instruction with the calculated address
a and the index j of the originating store instruction. The             Figure 5. Store hazard caused by late execution of store
rule produces a fwd observation with the labeled address a ℓa .         addresses. The store address for 3 is resolved too late, causing
This observation captures that the attacker can determine               the later load instruction to forward from the wrong store.
(e.g., by observing the absence of memory access using a                When 3’s address is resolved, the execution must be rolled
cache timing attack) that a forwarded value from address a              back. In this example, Jaddr(·)K adds its arguments.
was found in the buffer instead of loaded from memory.
   Importantly, neither of the rules has to wait for prior stores
to be resolved and can proceed speculatively. This can lead             (ak = a ⇒ jk ≥ i). We define ⊥ < n for any index n—that is,
to memory hazards when a more recent store to the load’s                if a future load matches the address of the current store but
address has not been resolved yet; we show how to deal with             loaded its value from memory, we consider this a hazard.
hazards in the rules for the store instruction.                            If there is indeed a hazard, i.e., if there was a resolved
                                                                        load with an outdated value, the rule store-execute-addr-
Store execution. We show the rules for stores below.
                                                                        hazard picks the earliest such instruction (index k) and
   store-execute-value
                                                                        restarts execution by resetting the instruction pointer to
     buf (i) = store(rv, −rv)
                          −−−−
                            ⃗      ∀j < i : buf (j) , fence
                                                                        the program point nk of this instruction. It then discards all
   (buf +i ρ)(rv) = v ℓ        buf = buf [i 7→ store(v ℓ , −rv)]
                                  ′                         −−−−
                                                              ⃗         transient instructions at indices at least k from the reorder
           (ρ, µ, n, buf ) ,−−−−−−−−−−−→ (ρ, µ, n, buf ′)               buffer. As in the case of misspeculation, the rule issues a
                           execute i: value
                                                                        rollback observation.
    store-execute-addr-ok
                                                                        Retire. Resolved loads are retired using the following rule.
     buf (i) = store(rv, −rv)
                            −−−−
                              ⃗     ∀j < i : buf (j) , fence
                −−−−−  −−−−−−                                 −−−
    (buf +i ρ)(rv) ⃗ = v⃗ℓ       Jaddr(−v−−−⃗ℓ−−)K = a  ℓa = ⊔⃗ℓ
                                                                                   value-retire
                                                                                      MIN(buf ) = i           buf (i) = (r = v ℓ )
             ∀k > i : buf (k) = (r = . . . {jk , ak }) :
                                                                                   ρ ′ = ρ[r 7→ v ℓ ]         buf ′ = buf \ buf (i)
           (ak = a ⇒ jk ≥ i) ∧ (jk = i ⇒ ak = a)
                                                                                        (ρ, µ, n, buf ) ,−−−−→ (ρ ′, µ, n, buf ′)
                buf ′ = buf [i 7→ store(rv, a ℓa )]                                                      retire
                              fwd a ℓa                                  This is the same retire rule used for simple value instructions
           (ρ, µ, n, buf ) ,−−−−−−−−−−→ (ρ, µ, n, buf ′)
                           execute i: addr                              (e.g., resolved op instructions). The rule updates the register
    store-execute-addr-hazard                                           map ρ with the new value, and removes the instruction from
     buf (i) = store(rv, −rv)−−−−
                               ⃗     ∀j < i : buf (j) , fence           the reorder buffer.
                 −−−−−  −−−−−−                                −−−
    (buf +i ρ)(rv)  ⃗ = v⃗ℓ       Jaddr(−v−−−⃗ℓ−−)K = a ℓa = ⊔⃗ℓ           Stores are retired using the rule below.
         min(k) > i : buf (k) = (r = . . . {jk , ak })nk :                        store-retire
            (ak = a ∧ jk < i) ∨ (jk = i ∧ ak , a)                                 MIN(buf ) = i            buf (i) = store(v ℓ , a ℓa )
                                                                                  µ ′ = µ[a 7→ v ℓ ]         buf ′ = buf \ buf (i)
           buf ′ = buf [j : j < k][i 7→ store(rv, a ℓa )]
                                                                                                       write a ℓa
                         rollback,fwd a ℓa                                           (ρ, µ, n, buf ) ,−−−−−−−→ (ρ, µ ′, n, buf ′)
         (ρ, µ, n, buf ) ,−−−−−−−−−−−−−→ (ρ, µ, nk , buf )  ′
                                                                                                         retire
                          execute i: addr
The execution of store is split into two steps: value resolution,       A fully resolved store instruction retires similarly to a value
represented by the directive execute i : value, and address             instruction. However, instead of updating the register map
resolution, represented by the directive execute i : addr;              ρ, rule store-retire updates the memory µ. Since an at-
a schedule may have either step first. Either step may be               tacker can observe memory writes, the rule produces the
skipped if data or address are already in immediate form.               observation write a ℓa with the labeled address of the store.
   Rule store-execute-addr-ok applies if no misprediction               Example. Figure 5 gives an example of store-to-load for-
has been detected, i.e., if no load instruction forwarded data          warding. In the starting configuration, the store at index
from an outdated store. We check this by requiring that all             2 is fully resolved, while the store at index 3 has an unre-
value instructions after the current index (indices k > i)              solved address. The first directive executes the load at 4. This
with an address a matching the current store must be using              load accesses address 43, which matches the store at index
a value forwarded from a store at least as recent as this one           2. Since this is the most recent such store and has a resolved
                                                                    7
,,                                                                     S. Cauligi, C. Disselkoen, K. v. Gleissenthall, D. Tullsen, D. Stefan, T. Rezk, and G. Barthe


             Registers                    Reorder buffer                              pubArrA. This value is then used as the address of another
        r       ρ(r )               i    buf (i)                                      load instruction, causing x sec to leak.
       ra       5pub                1    br(>, (4, r a ), 2, (2, 4))                     Figure 7 shows a Spectre v4 vulnerability caused when a
       rb      x sec                2    store(rb , [40, r a ])                       store fails to forward to a future load. In this example, the
             Memory                      ...
                                                                                      load at index 3 executes before the store at 2 calculates its
       a        µ(a)                 7   (rc = load([45]))
                                                                                      address. As a result, this execution loads the outdated secret
       40..43 secretKeysec           8   (rc = load([48, rc ]))
       44..47 pubArrApub                                                              value at address 43 and leaks it, instead of using the public
       48..4B pubArrBpub                                                              zeroed-out value that would be written.

     Directive            Effect on buf                  Leakage
     execute 2 : addr     2 7→ store(rb , 45pub )        fwd 45pub                    3.5     Aliasing Prediction
     execute 2 : value    2 7→ store(x sec , 45pub )                                  We extend the memory semantics from the previous section
     execute 7            7 7→ (rc = x sec {2, 45})      fwd 45pub                    to model aliasing prediction by introducing a new transient
     execute 8            8 7→ (rc = X {⊥, a})            read a sec                  instruction (r = load(−rv, ⃗ (v ℓ , j)))n . This instruction repre-
                                                                                                               −−−−
                         where a = x sec + 48
                                                                                      sents a partially resolved load with speculatively forwarded
Figure 6. Example demonstrating a store-to-load Spectre                               data. As before, r is the target register, −rv −−−−
                                                                                                                                       ⃗ is the list of argu-
v1.1 attack. A speculatively stored value is forwarded and                            ments for address calculation, and n is the program point
then leaked using a subsequent load instruction.                                      of the physical load instruction. The new parameters are v ℓ ,
                                                                                      the forwarded data, and j, the index of the originating store.
             Registers                    Reorder buffer
        r       ρ(r )               i    buf (i)                                      Forwarding via prediction.
       ra       40pub               2    store(0, [3, r a ])
             Memory                 3    (rc = load([43]))
       a        µ(a)                4    (rc = load([44, rc ]))                             load-execute-forwarded-guessed
                                                                                                                          −−−− n
       40..43 secretKeysec                                                                           buf (i) = (r = load(−rv))
                                                                                                                            ⃗           j <i
       44..47 pubArrApub                                                                    ∀k < i : buf (k) , fence         buf (j) = store(v ℓ , −rv
                                                                                                                                                    −−−−
                                                                                                                                                      ⃗j )
                                                                                                                                −−−−−           n
 Directive         Effect on buf                               Leakage                           buf = buf [i 7→ (r = load(rv,
                                                                                                      ′
                                                                                                                                   ⃗ (v ℓ , j))) ]
 execute 3         3 7→ (rc = secretKey[3]{⊥, 43})             read 43pub
                                                                                                   (ρ, µ, n, buf ) ,−−−−−−−−−−−→ (ρ, µ, n, buf ′)
 execute 4         4 7→ (rc = X {⊥, a})                        read a sec                                            execute i: fwd j
                   {3, 4} < buf                                rollback,
 execute 2 : addr
                   2 7→ store(0, 43pub )                       fwd 43pub
                 where a = secretKey[3]sec + 44
                                                                                      Rule load-execute-forwarded-guessed implements for-
Figure 7. Example demonstrating a v4 Spectre attack. The                              warding in the presence of unresolved target addresses. In-
store is executed too late, causing later load instructions to                        stead of forwarding the value from a store with a matching
use outdated values.                                                                  address, as in Section 3.4, the attacker can now freely choose
                                                                                      to forward from any store with a resolved value—even if its
                                                                                      target address is not known yet. Given a choice of which
value, the load gets the value 12 from this store. The follow-                        store j to forward from—supplied via directive—the rule up-
ing directive resolves the address of the store at index 3. This                      dates the reorder buffer with the new partially resolved load
store also matches address 43. As this store is more recent                           and records both the forwarded value vl and the buffer index
than store 2, this directive triggers a hazard for the load at 4,                     j of the store instruction.
leading to the rollback of the load from the reorder buffer.
Capturing Spectre. We now have enough machinery to                                    Register resolve function. We extend the register resolve
capture several variants of Spectre attacks.                                          function (buf +i ρ) to allow using values from partially re-
   We discussed how our semantics model Spectre v1 in Sec-                            solved loads. In particular, whenever the register resolve
tion 2 (Figure 1). Figure 6 shows a simple disclosure gadget                          function computes the latest resolved assignment to some
using forwarding from an out-of-bounds write. In this exam-                           register r , it now considers not only fully resolved value
ple, a secret value x sec is supposed to be written to secretKey                      instructions, but also our new partially resolved load: when-
at an index r a as long as r a is within bounds. However, due                         ever the latest assignment in the buffer is a partially resolved
to branch misprediction, the store instruction is executed                            load, the register resolve function returns its value.
despite r a being too large. The load instruction at index                               We now discuss the execution rules, where partially re-
7, normally benign, now aliases with the store at index 2,                            solved loads may fully resolve against either the originating
and receives the secret x sec instead of a public value from                          store or against memory.
                                                                                  8
Constant-Time Foundations for the New Spectre Era                                                                                                  ,,


Resolving when originating store is in the reorder buffer.
                                                                                  load-execute-addr-mem-match
                                                                                                buf (i) = (r = load(−rv, ⃗ v ℓ , j))n
                                                                                                                       −−−−
                                                                                                                 −−−−−                     −−−
 load-execute-addr-ok                                                               j < buf          (buf +i ρ)(rv) ⃗ = −v−−−⃗ℓ−−    ℓa = ⊔⃗ℓ
               buf (i) = (r = load(−rv,  ⃗ (v ℓ , j)))n
                                       −−−−
                                                                                         −−−−−−
                                                                                  Jaddr(v⃗ℓ )K = a          ∀k < i : buf (k) , store(_, a)
                       −−−−−  −−−−−−
           (buf +i ρ)(rv) ⃗ = v⃗ℓ        Jaddr(−v−−−⃗ℓ−−)K = a                    µ(a) = v ℓ          buf ′ = buf [i 7→ (r = v ℓ {⊥, a})n ]
       −−−
 ℓa = ⊔⃗ℓ     buf (j) = store(v ℓ , rv⃗j ) ∧ (−rv
                                     −
                                     −−−−       −−−−
                                                  ⃗j = a ′ ⇒ a ′ = a)
                                                                                                            read a ℓa
            ∀k : (j < k < i) : buf (k) , store(_, a)                                      (ρ, µ, n, buf ) ,−−−−−−→ (ρ, µ, n, buf ′)
                                                                                                            execute i
              buf ′ = buf [i 7→ (r = v ℓ {j, a})n ]
                               fwd a ℓa                                           load-execute-addr-mem-hazard
                                                                                                                          ⃗ v ℓ , j))n
                                                                                                                                   ′
             (ρ, µ, n, buf ) ,−−−−−−→ (ρ, µ, n, buf ′)                                        buf (i) = (r = load(−rv,  −−−−
                              execute i                                                                           −−−−−                      −−−
                                                                                    j < buf         (buf +i ρ)(rv)   ⃗ = −v−−−⃗ℓ−−     ℓa = ⊔⃗ℓ
                                                                                         −−−
                                                                                  Jaddr(v ⃗ℓ )K = a          ∀k < i : buf (k) , store(_, a)
                                                                                  µ(a) = v ℓ′ ′      v ℓ′ ′ , v ℓ       buf ′ = buf [j : j < i]
                                                                                                      rollback,read a ℓa
       load-execute-addr-hazard                                                     (ρ, µ, n, buf ) ,−−−−−−−−−−−−−−→ (ρ, µ, n ′, buf ′)
                                                    n′                                                     execute i
                buf (i) = (r = load(−rv,
                                      −−−−
                                        ⃗ (v ℓ , j)))
                        −−−−−  −−−−−−
           (buf +i ρ)(rv)  ⃗ = v⃗ℓ       Jaddr(−v−−−⃗ℓ−−)K = a                 If the originating store has retired, and no intervening
              −−−
       ℓa = ⊔ℓ ⃗      (buf (j) = store(v ℓ , a ′) ∧ a ′ , a) ∨              stores match the same address, we must load the value from
            (∃k : j < k < i ∧ buf (k) = store(_, a))                        memory to ensure we were originally forwarded the correct
                       buf ′ = buf [j : j < i]                              value. If the value loaded from memory matches the value we
                         rollback,fwd a ℓa
                                                                            were forwarded, we update the reorder buffer with a resolved
         (ρ, µ, n, buf ) ,−−−−−−−−−−−−−→ (ρ, µ, n ′, buf ′)                 load annotated as if it had been loaded from memory (rule
                             execute i
                                                                            load-execute-addr-mem-match).
                                                                               If a store different from the originating store overwrote the
To resolve (r = load(−rv,  ⃗ (v ℓ , j)))n when its originating store
                         −−−−                                               originally forwarded value, the value loaded from memory
is still in buf , we calculate the load’s actual target address a           may not match the value we were originally forwarded. In
and compare it against the target address of the originating                this case we roll back execution to just before the load (rule
store at buf (j). If the store is not followed by later stores to a,        load-execute-addr-mem-hazard).
and either (1) the store’s address is resolved and its address                 We demonstrate these semantics in the attack shown in
is indeed a, or (2) the store’s address is still unresolved, we             Figure 2. An earlier draft of this paper [7] incorrectly claimed
update the reorder buffer with an annotated value instruction               to have a proof-of-concept exploit for this attack on real
(rule load-execute-addr-ok).                                                hardware.
   If, however, either the originating store resolved to a differ-
ent address (mispredicted aliasing) or a later store resolved               3.6   Speculation Barriers
to the same address (hazard), we roll back our execution to                 We extend our semantics with a speculation barrier instruc-
just before the load (rule load-execute-addr-hazard).                       tion, fence n, that prevents further speculative execution
   We allow the load to execute even if the originating store               until all prior instructions have been retired.
has not yet resolved its address. When the store does fi-
nally resolve its address, it must check that the addresses                 fence-retire
match and that the forwarding was correct. The gray formu-                   MIN(buf ) = i          buf (i) = fence          buf ′ = buf \ buf (i)
las in store-execute-addr-ok and store-execute-addr-                                        (ρ, µ, n, buf ) ,−−−−→ (ρ, µ, n, buf ′)
hazard (Section 3.4) perform these checks: For forwarding                                                    retire

to be correct, all values forwarded from a store at buf (i) must               The fence instruction uses simple-fetch as its fetch rule,
have a matching annotated address (∀k > i : jk = i ⇒ ak =                   and its rule for retire only removes the instruction from
a). Otherwise, if any value annotation has a mismatched                     the buffer. It does not have an execute rule. However, fence
address, then the instruction is rolled back (jk = i ∧ ak , a).             instructions affect the execution of all instructions in the re-
                                                                            order buffer that come after them. In prior sections, execute
Resolving when originating store is not in the buffer.                      rules have the highlighted condition ∀j < i : buf (j) , fence.
We must also consider the case where we have delayed re-                    This condition ensures that as long as a fence instruction re-
solving the load address to the point where the originating                 mains in buf , any instructions fetched after the fence cannot
store has already retired, and is no longer available in buf .              be executed.
If this is the case, and no other prior store instructions have                We use fence instructions to restrict out-of-order execu-
a matching address, then we must check the forwarded data                   tion in our semantics. Notably, we can use it to prevent
against memory.                                                             attacks of the forms shown in Figures 1, 6 and 7.
                                                                        9
,,                                                             S. Cauligi, C. Disselkoen, K. v. Gleissenthall, D. Tullsen, D. Stefan, T. Rezk, and G. Barthe


                 Before executing 1                 After                      4     Detecting Violations
             i    buf [i]                       i    buf [i]
                                                                               We develop a tool Pitchfork based on our semantics to check
             1    br(>, (4, r a ), 2, (2, 5))   1    jump 5
             2    fence
                                                                               for SCT violations. Pitchfork first generates a set of sched-
             3    (rb = load([40, r a ]))                                      ules representing various worst-case attackers. This set of
             4    (rc = load([44, rb ]))                                       schedules is far smaller than the set of all possible sched-
                                                                               ules for the program, but is nonetheless sound: if there is an
Figure 8. Example demonstrating fencing mitigation against                     SCT violation in any possible schedule, then there will be an
Spectre v1 attacks. The fence instruction prevents the load                    SCT violation in one of the worst-case schedules. Pitchfork
instructions from executing before the br.                                     then checks for secret leakage by symbolically executing the
                                                                               program under each schedule.
                                                                                  Pitchfork only exercises a subset of our semantics; it does
                                                                               not detect SCT violations based on alias prediction, indirect
Example. The example in Figure 8 shows how placing a                           jumps, or return stack buffers (Sections 3.5 and 3.7). Doing
fence instruction just after the br instruction prevents the                   so would require it to generate a prohibitively large number
Spectre v1 attack from Figure 1. The fence in this example                     of schedules. Nevertheless, Pitchfork still exposes attacks
prevents the load instructions at 2 and 3 from executing and                   based on Spectre variants 1, 1.1, and 4.
forces the br to be resolved first. Evaluating the br exposes                     We describe our schedule generation in Section 4.1, and
the misprediction and causes the two loads (as well as the                     evaluate Pitchfork on several crypto libraries in Section 4.2.
fence) to be rolled back.
                                                                               4.1    Schedule Generation
3.7   Indirect Jumps and Return Address Prediction                             Given a program, Pitchfork generates a set of schedules rep-
Finally, we briefly discuss two additional extensions to our                   resenting various worst-case attackers. Pitchfork’s schedule
semantics. First, we extend our semantics with indirect jumps.                 generation is parametrized by a speculation bound, which
Rather than specifying jump targets directly as with the                       limits the size of the reorder buffer, and thus the depth of
br instruction in Section 3.3, indirect jumps compute the                      speculation.
target from a list of argument operands. The indirect jump                        In general, Pitchfork constructs worst-case schedules to
instruction has the form jmpi(−rv),     −−−−
                                          ⃗ where −rv−−−−
                                                       ⃗ is the list of        maximize speculation. These schedules eagerly fetch instruc-
operands for calculating the jump target. The transient form                   tions until the reorder buffer is full, i.e., the size of the reorder
of jmpi is jmpi(−rv,
                   −−−−
                     ⃗ n 0 ), where n 0 is the predicted jump target.          buffer equals the speculation bound. Once the reorder buffer
To fetch a jmpi instruction, we use fetch: n ′, where n ′ is                   is full, the schedules only retire instructions as necessary to
the speculated jump target. In all other respects, the rules                   fetch new ones.
for indirect jump instructions are similar to the rules for                       When conditional branches are to be fetched, Pitchfork
conditional branches.                                                          constructs schedules containing both possible outcomes: one
    Second, we extend our semantics with call and ret instruc-                 where the branch is guessed true (fetch: true) and one where
tions. The call instruction has the form call(n f , n ret ), where             the branch is guessed false (fetch: false). For the mispredicted
n f is the callee program point and n ret is the program point to              outcome, Pitchfork’s schedules execute the branch as late as
return to. The return instruction is simply ret. Both the call                 possible (i.e., it is the oldest instruction in the reorder buffer
and ret instructions have the simple transient forms call and                  and the reorder buffer is full), which delays the rollback of
ret. However, when fetched, they are unpacked into multiple                    mispredicted paths.
transient instructions. Fetching a call produces the call tran-                   To account for the load-store forwarding hazards described
sient instruction as well as transient instructions which will                 in Section 3.4, Pitchfork constructs schedules containing
increment a stack pointer and store the return program point                   all possible forwarding outcomes. For every load instruc-
to memory. Fetching a ret produces a corresponding load,                       tion l in the program, Pitchfork finds all prior stores si
decrement, and jump as well as the ret transient instruction.                  within the speculation bound that would resolve to the same
Furthermore, the call and ret instructions respectively push                   address. Then, for each such store, Pitchfork constructs a
and pop program points to an additional configuration state                    schedule that would cause that store to forward its data to l.
representing the return stack buffer (RSB). The RSB is used                    That is, Pitchfork constructs separate schedules [execute s 1 :
to predict the new program point upon fetching a ret.                          addr; execute l], [execute s 2 : addr; execute l], and so on.
    In Appendix A, we present detailed rules for indirect                      Additionally, Pitchfork constructs a schedule where none of
jumps, functions calls, and returns. We also show how both                     the prior stores si have resolved addresses, forcing the load
Spectre v2 [20] and ret2spec [23] attacks can be expressed in                  instruction to read from memory.
our semantics, as well as the retpoline mitigation [31] against                   For all instructions other than conditional branches and
Spectre v2 attacks.                                                            memory operations, Pitchfork only constructs schedules
                                                                          10
Constant-Time Foundations for the New Spectre Era                                                                                      ,,


where these instructions are executed eagerly and in or-               Table 2. A indicates Pitchfork found an SCT violation. A
                                                                         f indicates the violation was found only with forwarding
der. Reordering of these instructions is uninteresting: either
the instructions naturally commute, or data dependencies               hazard detection.
prevent the reordering (i.e., the reordered schedule is invalid
for the program). This intuition matches with the property                       Case Study                         C    FaCT
that any out-of-order execution of a given program has the
same final result regardless of its schedule.                                    curve25519-donna                   ✓      ✓
   We formalize the soundness of Pitchfork’s schedule con-                       libsodium secretbox                       ✓
                                                                                 OpenSSL ssl3 record validate                f
struction in more detail in Appendix B.3.                                                                                    f
                                                                                 OpenSSL MEE-CBC
4.2   Implementation and Evaluation
We implement Pitchfork on top of the angr binary-analysis              1    for (int cnt = nlist - 1; cnt >= 0; --cnt) {
tool [30]. Pitchfork uses angr to symbolically execute a given         2      iov[cnt].iov_base = (char *) list->str;
                                                                       3        // ...
program according to each of its worst-case schedules, flag-
                                                                       4      list = list->next;
ging any resulting secret leakage.                                     5    }
   To sanity check Pitchfork, we create and analyze a set
of Spectre v1 and v1.1 test cases, and ensure we flag their                Figure 9. Vulnerable snippet from __libc__message().4
SCT violations. Our test cases are based off the well-known
Kocher Spectre v1 examples [19]. Since many of the Kocher
examples exhibit violations even during sequential execution,          a reduced bound of 20 instructions. The reduced bound en-
we create a new set of Spectre v1 test cases which only exhibit        sured that the analysis was tractable.
violations when executed speculatively. We also develop a              4.2.2 Detected Violations. Table 2 shows our results. Pitch-
similar set of test cases for Spectre v1.1 data attacks.               fork did not flag any SCT violations in the curve25519-donna
   Pitchfork necessarily inherits the limitations of angr’s            implementations; this is not surprising, as the curve25519-
symbolic execution. For instance, angr concretizes addresses           donna library is a straightforward implementation of crypto
for memory operations instead of keeping them symbolic.                primitives. Pitchfork did, however, find SCT violations (with-
Furthermore, exploring every speculative branch and poten-             out forwarding hazard detection) in both the libsodium and
tial store-forward within a given speculation bound leads              OpenSSL codebases. Specifically, Pitchfork found violations
to an explosion in state space. In our tests, we were able to          in the C implementations of these libraries, in code ancillary
support speculation bounds of up to 20 instructions. We were           to the core crypto routines. This aligns with our intuition
able to increase this bound to 250 instructions when we dis-           that crypto primitives will not themselves be vulnerable to
abled checking for store-forwarding hazards. Though these              Spectre attacks, but higher-level code that interfaces with
bounds do not capture the speculation depth of some mod-               these primitives may still leak secrets. Such higher-level code
ern processors, Pitchfork still correctly finds SCT violations         is not present in the corresponding FaCT implementations,
in all our test cases, as well as SCT violations in real-world         and Pitchfork did not find any violations in the FaCT code
crypto code. We consider the design and implementation of              with these settings. However, with forwarding hazard detec-
a more scalable tool future work.                                      tion, Pitchfork was able to find vulnerabilities even in the
4.2.1 Evaluation Procedure. To evaluate Pitchfork on                   FaCT versions of the OpenSSL implementations. We describe
real-world crypto implementations, we use the same case                two of the violations Pitchfork flagged next.
studies as FaCT [8], a domain-specific language and compiler           C libsodium secretbox. The libsodium codebase compiles
for constant-time crypto code. We use FaCT’s case studies for          with stack protection [15] turned on by default. This means
two reasons: these implementations have been verified to be            that, for certain functions (e.g., functions with stack allocated
(sequentially) constant-time, and their inputs have already            char buffers), the compiler inserts code in the function epi-
been annotated by the FaCT authors with secrecy labels.3               logue to check if the stack was “smashed”. If so, the program
   We analyzed both the FaCT-generated binaries and the cor-           displays an error message and aborts. As part of printing the
responding C binaries for the case studies. For each binary,           error message, the program calls a function __libc_message,
we ran Pitchfork without forwarding hazard detection—only              which does printf-style string formatting.
looking for Spectre v1 and v1.1 violations—and with a spec-               Figure 9 shows a snippet from this function which tra-
ulation bound of 250 instructions. If Pitchfork did not flag           verses a linked list. When running the C secretbox imple-
any violations, we re-enabled forwarding hazard detection—             mentation speculatively, the processor may misspeculate on
looking for Spectre v4 violations—and ran Pitchfork with               the stack tampering check and jump into the error handling
                                                                       4 Code  snippet taken from https://github.com/lattera/glibc/blob/
3 https://github.com/PLSysSec/fact-eval                                895ef79e04a953cac1493863bcae29ad85657ee1/sysdeps/posix/libc_fatal.c
                                                                  11
,,                                                      S. Cauligi, C. Disselkoen, K. v. Gleissenthall, D. Tullsen, D. Stefan, T. Rezk, and G. Barthe


1    aesni_cbc_encrypt(/* ... */);                                     of microarchitectural features, considering them to be adver-
2    // (len _out) is in %r14                                          sarially controlled.
3    secret mut uint32 pad = _out[len _out - 1];                           Disselkoen et al. [13] explore speculation and out-of-order
4    public uint32 maxpad = tmppad > 255 ? 255 : tmppad;
                                                                       effects through a relaxed memory model. Their semantics sits
5    if (pad > maxpad) {
                                                                       at a higher level, and is orthogonal to our approach. They do
6      pad = maxpad;
7      ret = 0; // overwrites %r14                                     not define a semantic notion of security that prevents Spectre-
8    }                                                                 like attacks, and do not provide support for verification.
9    // ...                                                                Mcilroy et al. [24] reason about micro-architectural attacks
10   _sha1_update(/* ... */); // can return to line 3                  using a multi-stage pipeline semantics (though they do not
                                                                       define a formal security property). Their semantics models
Figure 10. Vulnerable snippet from the FaCT OpenSSL MEE                branch predictor and cache state explicitly. However, they
implementation.5                                                       do not model the effects of speculative barriers, nor other
                                                                       microarchitecture features such as store-forwarding. Thus,
                                                                       their semantics can only capture Spectre v1 attacks.
code, eventually calling __libc_message. Again due to mis-
                                                                           Both Guarnieri et al. [17] and Cheang et al. [9] define spec-
speculation, the processor may incorrectly proceed through
                                                                       ulative semantics that are supported by tools. Their seman-
the loop extra times, traversing non-existent links, eventu-
                                                                       tics handle speculation through branch prediction—where
ally causing secret data to be stored into list instead of
                                                                       the predictor is left abstract—but do not capture more general
a valid address (line 4). On the following iteration of the
                                                                       out-of-order execution nor other types of speculation. These
loop, dereferencing list (line 2) causes a secret-dependent
                                                                       works also propose new semantic notions of security (differ-
memory access.
                                                                       ent from SCT); both essentially require that the speculative
FaCT OpenSSL MEE. In Figure 10, we show the code from                  execution of a program not leak more than its sequential
the FaCT port of OpenSSL’s authenticated encryption imple-             execution. If a program is sequentially constant-time, this
mentation. The FaCT compiler transforms the branch at lines            additional security property is equivalent to our notion of
5-7 into straight-line constant-time code, since the variable          speculative constant-time. Though our property is stronger,
pad is considered secret.                                              it is also simpler to verify: we can directly check SCT without
   Initially, register %r14 holds the length of the array _out.        first checking if a program is sequentially constant-time. And
The processor leaks this value due to the array access on              since we focus on cryptographic code, we directly require
line 3; this is not a security violation, as the length is pub-        the stronger SCT property.
lic. On line 7, the value of %r14 is overwritten with 0 if                 Balliu et al. [3] define a semantics in a style similar to ours.
pad > maxpad, or 1 (the initial value of ret) otherwise. After-        Their semantics captures various Spectre attacks, including
wards, the processor calls _sha1_update.                               an attack similar to our alias prediction example (Figure 2),
   To return from _sha1_update, the processor must first load          and a new attack based on their memory ordering semantics,
the return address from memory. When forwarding hazard                 which our semantics cannot capture.
detection is enabled, Pitchfork allows this load to specula-               Finally, several tools detect Spectre vulnerabilities, but
tively receive data from stores older than the most recent             do not present semantics. The oo7 static analysis tool [33],
store to that address (see Section 3.4). Specifically, it may          for example, uses taint tracking to find Spectre attacks and
receive the prior value that was stored at that location: the          automatically insert mitigations for several variants. Wu
return address for the call to aesni_cbc_encrypt.                      and Wang [35], on the other hand, perform cache analysis
   After the speculative return, the processor executes line 3         of LLVM programs under speculative execution, capturing
a second time. This time, %r14 does not hold the public value          Spectre v1 attacks.
len _out; it instead holds the value of ret, which was de-
rived from the secret condition pad > maxpad. The processor
thus accesses either _out[0] or _out[-1], leaking informa-
tion about the secret value of pad via cache state.                    6     Conclusion
                                                                       We introduced a semantics for reasoning about side-channels
5    Related Work                                                      under adversarially controlled out-of-order and speculative
Prior work on modeling speculative or out-of-order execu-              execution. Our semantics capture existing transient execu-
tion is concerned with correctness rather than security [1,            tion attacks—namely Spectre—but can be extended to fu-
21]. We instead focus on security and model side-channel               ture hardware predictors and potential attacks. We also de-
leakage explicitly. Moreover, we abstract away the specifics           fined a new notion of constant-time code under speculation—
5 Code    snippet taken from https://github.com/PLSysSec/fact-         speculative constant-time (SCT)—and implemented a proto-
eval/blob/888bc6c6898a06cef54170ea273de91868ea621e/openssl-            type tool to check if code is SCT. Our prototype, Pitchfork,
mee/20170717_latest.fact                                               discovered new vulnerabilities in real-world crypto libraries.
                                                                  12
Constant-Time Foundations for the New Spectre Era                                                                                                             ,,


   There are several directions for future work. Our imme-                         [11] Cryptography Coding Standard. 2016. Coding Rules. Retrieved June
diate plan is to use our semantics to prove the effectiveness                           9, 2017 from https://cryptocoding.net/index.php/Coding_rules
of existing countermeasures (e.g., retpolines) and to justify                      [12] Frank Denis. 2019. libsodium. Retrieved May 16, 2018 from https:
                                                                                        //github.com/jedisct1/libsodium
new countermeasures.                                                               [13] Craig Disselkoen, Radha Jagadeesan, Alan Jeffrey, and James Riely.
                                                                                        2019. The Code That Never Ran: Modeling Attacks on Speculative
                                                                                        Evaluation. In 40th IEEE Symposium on Security and Privacy. IEEE.
Acknowledgments                                                                    [14] Dmitry Evtyushkin, Ryan Riley, Nael Abu-Ghazaleh, and Dmitry Pono-
We thank the anonymous PLDI and PLDI AEC reviewers                                      marev. 2018. BranchScope: A New Side-Channel Attack on Directional
and our shepherd James Bornholt for their suggestions and                               Branch Predictor. In 23rd International Conference on Architectural
                                                                                        Support for Programming Languages and Operating Systems. ACM.
insightful comments. We thank David Kaplan from AMD
                                                                                   [15] GCC Team. 2019. Using the GNU Compiler Collection (GCC): In-
for his detailed analysis of our proof-of-concept exploit that                          strumentation Options. Retrieved November 21, 2019 from https:
we incorrectly thought to be abusing an aliasing predictor.                             //gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html
We also thank Natalie Popescu for her aid in editing and                           [16] Qian Ge, Yuval Yarom, David Cock, and Gernot Heiser. 2018. A survey
formatting this paper. This work was supported in part by                               of microarchitectural timing attacks and countermeasures on contem-
                                                                                        porary hardware. Journal of Cryptographic Engineering (2018).
gifts from Cisco and Fastly, by the NSF under Grant Number
                                                                                   [17] Marco Guarnieri, Boris Köpf, José F. Morales, Jan Reineke, and Andrés
CCF-1918573, by ONR Grant N000141512750, and by the                                     Sánchez. 2020. SPECTECTOR: Principled Detection of Speculative
CONIX Research Center, one of six centers in JUMP, a Semi-                              Information Flows. In 41st IEEE Symposium on Security and Privacy.
conductor Research Corporation (SRC) program sponsored                                  IEEE.
by DARPA.                                                                          [18] Saad Islam, Ahmad Moghimi, Ida Bruhns, Moritz Krebbel, Berk Gulme-
                                                                                        zoglu, Thomas Eisenbarth, and Berk Sunar. 2019. SPOILER: Speculative
                                                                                        Load Hazards Boost Rowhammer and Cache Attacks. In 28th USENIX
References                                                                              Security Symposium. USENIX Association.
                                                                                   [19] Paul Kocher. 2018. Spectre mitigations in Microsoft’s C/C++ com-
 [1] Jade Alglave, Anthony Fox, Samin Ishtiaq, Magnus O. Myreen, Susmit                 piler. Retrieved April 6, 2020 from https://www.paulkocher.com/doc/
     Sarkar, Peter Sewell, and Francesco Zappa Nardelli. 2009. The Seman-               MicrosoftCompilerSpectreMitigation.html
     tics of Power and ARM Multiprocessor Machine Code. In Proceedings             [20] Paul Kocher, Jann Horn, Anders Fogh, Daniel Genkin, Daniel Gruss,
     of the 4th Workshop on Declarative Aspects of Multicore Programming.               Werner Haas, Mike Hamburg, Moritz Lipp, Stefan Mangard, Thomas
 [2] Arm Mbed. [n.d.]. mbed TLS. Retrieved May 16, 2018 from https:                     Prescher, Michael Schwarz, and Yuval Yarom. 2019. Spectre Attacks:
     //github.com/armmbed/mbedtls                                                       Exploiting Speculative Execution. In 40th IEEE Symposium on Security
 [3] Musard Balliu, Mads Dam, and Roberto Guanciale. 2019. InSpectre:                   and Privacy. IEEE.
     Breaking and Fixing Microarchitectural Vulnerabilities by Formal Anal-        [21] Shuvendu K. Lahiri, Sanjit A. Seshia, and Randal E. Bryant. 2002. Mod-
     ysis. arXiv:1911.00868 [cs.CR]                                                     eling and Verification of Out-of-Order Microprocessors in UCLID. In
 [4] Gilles Barthe, Gustavo Betarte, Juan Campo, Carlos Luna, and David                 International Conference on Formal Methods in Computer-Aided Design.
     Pichardie. 2014. System-level non-interference for constant-time cryp-             Springer.
     tography. In Proceedings of the 2014 ACM SIGSAC Conference on Com-            [22] Moritz Lipp, Michael Schwarz, Daniel Gruss, Thomas Prescher, Werner
     puter and Communications Security. ACM.                                            Haas, Anders Fogh, Jann Horn, Stefan Mangard, Paul Kocher, Daniel
 [5] Claudio Canella, Daniel Genkin, Lukas Giner, Daniel Gruss, Moritz                  Genkin, Yuval Yarom, and Mike Hamburg. 2018. Meltdown: Reading
     Lipp, Marina Minkin, Daniel Moghimi, Frank Piessens, Michael                       Kernel Memory from User Space. In 27th USENIX Security Symposium.
     Schwarz, Berk Sunar, Jo Van Bulck, and Yuval Yarom. 2019. Fallout:                 USENIX Association.
     Leaking Data on Meltdown-resistant CPUs. In Proceedings of the 2019
                                                                                   [23] Giorgi Maisuradze and Christian Rossow. 2018. ret2spec: Speculative
     ACM SIGSAC Conference on Computer and Communications Security.                     Execution Using Return Stack Buffers. In Proceedings of the 2018 ACM
     ACM.                                                                               SIGSAC Conference on Computer and Communications Security. ACM.
 [6] Claudio Canella, Jo Van Bulck, Michael Schwarz, Moritz Lipp, Ben-             [24] Ross McIlroy, Jaroslav Sevcik, Tobias Tebbi, Ben L. Titzer, and Toon
     jamin von Berg, Philipp Ortner, Frank Piessens, Dmitry Evtyushkin,                 Verwaest. 2019. Spectre is here to stay: An analysis of side-channels and
     and Daniel Gruss. 2019. A Systematic Evaluation of Transient Ex-                   speculative execution. arXiv:1902.05178
     ecution Attacks and Defenses. In 28th USENIX Security Symposium.              [25] OpenSSL. 2019. Security Policy. Retrieved April 6, 2020 from https:
     USENIX Association.                                                                //www.openssl.org/policies/secpolicy.html
 [7] Sunjay Cauligi, Craig Disselkoen, Klaus von Gleissenthall, Dean               [26] Thomas Pornin. 2016. Why Constant-Time Crypto?                  Retrieved
     Tullsen, Deian Stefan, Tamara Rezk, and Gilles Barthe. 2019. Towards               November 15, 2018 from https://www.bearssl.org/constanttime.html
     Constant-Time Foundations for the New Spectre Era. arXiv:1910.01755v2         [27] Thomas Pornin. 2018. Constant-Time Toolkit. Retrieved November
 [8] Sunjay Cauligi, Gary Soeller, Brian Johannesmeyer, Fraser Brown,                   15, 2018 from https://github.com/pornin/CTTK
     Riad S. Wahby, John Renner, Benjamin Gregoire, Gilles Barthe, Ranjit          [28] Michael Schwarz, Claudio Canella, Lukas Giner, and Daniel Gruss.
     Jhala, and Deian Stefan. 2019. FaCT: A DSL for timing-sensitive com-               2019. Store-to-Leak Forwarding: Leaking Data on Meltdown-resistant
     putation. In 40th ACM SIGPLAN Conference on Programming Language                   CPUs. arXiv:1905.05725
     Design and Implementation. ACM.                                               [29] Michael Schwarz, Moritz Lipp, Daniel Moghimi, Jo Van Bulck, Julian
 [9] Kevin Cheang, Cameron Rasmussen, Sanjit Seshia, and Pramod Subra-                  Stecklina, Thomas Prescher, and Daniel Gruss. 2019. ZombieLoad:
     manyan. 2019. A Formal Approach to Secure Speculation. Cryptology                  Cross-Privilege-Boundary Data Sampling. In Proceedings of the 2019
     ePrint Archive, Report 2019/310.                                                   ACM SIGSAC Conference on Computer and Communications Security.
[10] Tien-Fu Chen and Jean-Loup Baer. 1992. Reducing Memory Latency                     ACM.
     via Non-blocking and Prefetching Caches. In 5th ACM International             [30] Yan Shoshitaishvili, Ruoyu Wang, Christopher Salls, Nick Stephens,
     Conference on Architectural Support for Programming Languages and                  Mario Polino, Audrey Dutcher, John Grosen, Siji Feng, Christophe
     Operating Systems. ACM.
                                                                              13
,,                                                                      S. Cauligi, C. Disselkoen, K. v. Gleissenthall, D. Tullsen, D. Stefan, T. Rezk, and G. Barthe


     Hauser, Christopher Kruegel, and Giovanni Vigna. 2016. SoK: (State                            Registers                           Program
     of) The Art of War: Offensive Techniques in Binary Analysis. In 37th                     r      ρ(r )                    n   µ(n)
     IEEE Symposium on Security and Privacy. IEEE.                                           ra      1pub                     1   (rc = load([48, ra ], 2))
[31] Paul Turner. 2019. Retpoline: a software construct for preventing                       rb      8pub                     2   fence 3
     branch-target-injection. Retrieved April 6, 2020 from https://support.                        Memory                     3   jmpi([12, rb ])
     google.com/faqs/answer/7625886                                                          a       µ(a)                         ...
[32] Stephan van Schaik, Alyssa Milburn, Sebastian Österlund, Pietro Frigo,
                                                                                             44..47 array Bpub               16   fence 17
     Giorgi Maisuradze, Kaveh Razavi, Herbert Bos, and Cristiano Giuffrida.
     2019. RIDL: Rogue In-Flight Data Load. In 40th IEEE Symposium on                        48..4B array Keysec             17   (rd = load([44, rc ], 18))
     Security and Privacy. IEEE.                                                                   Directive   Effect on buf             Leakage
[33] Guanhua Wang, Sudipta Chattopadhyay, Ivan Gotovchits, Tulika Mitra,
                                                                                                   fetch       1 7→ rc = load(48 + r a )
     and Abhik Roychoudhury. 2019. oo7: Low-overhead Defense against
     Spectre Attacks via Program Analysis. IEEE Transactions on Software
                                                                                                   fetch       2 7→ fence
     Engineering (2019).                                                                           execute 1   1 7→ rc = Key[1]sec       read 49pub
[34] Henry Wong. 2014. Store-to-Load Forwarding and Memory Dis-                                    fetch: 17   3 7→ jmpi([12, rb ], 17)
     ambiguation in X86 Processors.        Retrieved April 6, 2020 from                            fetch       4 7→ rd = load([44, rc ])
     https://blog.stuffedcow.net/2014/01/x86-memory-disambiguation/                                retire      1 < buf
[35] Meng Wu and Chao Wang. 2019. Abstract Interpretation under Spec-                              retire      2 < buf
     ulative Execution. In 40th SIGPLAN ACM Conference on Programming
                                                                                                   execute 4   4 7→ rd = X               read a sec
     Language Design and Implementation. ACM.
                                                                                                               where a = Key[1]sec + 40

A        Extended semantics                                                            Figure 11. Example demonstrating Spectre v2 attack from
A.1       Indirect jumps                                                               a mistrained indirect branch predictor. Speculation barriers
                                                                                       are not a useful defense against this style of attack.
Semantics. The semantics for jmpi are given below:
       jmpi-fetch
                         µ(n) = jmpi(−rv)
                                      −−−−
                                        ⃗                                              the resolved jump to the correct address, and set the next
       i = MAX(buf ) + 1      buf = bu f [i 7→ jmpi(−rv,
                                 ′                   −−−− ′
                                                       ⃗ n )]                          instruction.
                                                                                         Like conditional branch instructions, indirect jumps leak
                  (ρ, µ, n, buf ) ,−−−−−−→ (ρ, µ, n ′, buf ′)
                                    fetch: n
                                         ′                                             the calculated jump target.
jmpi-execute-correct                                                                   Examples. The example in Figure 11 shows how a mistrained
                      buf (i) = jmpi(−rv,
                                      −−−−
                                        ⃗ n0 )                                         indirect branch predictor can lead to disclosure vulnerabil-
       ∀j < i : buf (j) , fence       (buf +i ρ)(−rv)
                                                  −−−−
                                                    ⃗ = −v−−−⃗ℓ−−                      ities. After loading a secret value into r c at program point
      −−−            −
                     −−−
                       −−
 ℓ = ⊔⃗ℓ     Jaddr(v⃗ℓ )K = n 0     buf = buf [i 7→ jump n 0 ]
                                           ′                                           1, the program makes an indirect jump. An adversary can
                                    jump n 0 ℓ
                                                                                       mistrain the predictor to send execution to 17 instead of the
                  (ρ, µ, n, buf ) ,−−−−−−→ (ρ, µ, n, buf ′)                            intended branch target, where the secret value in r c is im-
                                    execute i
                                                                                       mediately leaked. Because indirect jumps can have arbitrary
 jmpi-execute-incorrect                                                                branch target locations, fence instructions do not prevent
         buf (i) = jmpi(−rv,  −−−−
                                ⃗ n0 )     ∀j < i : buf [j] , fence                    these kinds of attacks; an adversary can simply retarget the
                 −−−−−   −−−−−−           −−−
     (buf +i ρ)(rv) ⃗ = v⃗ℓ          ℓ = ⊔⃗ℓ     Jaddr(−v−−−⃗ℓ−−)K = n ′ , n 0         indirect jump to the instruction after the fence, as is seen in
                 buf = buf [j : j < i][ i 7→ jump n ′]
                       ′
                                                                                       this example.
                               rollback,jump n ′ℓ
             (ρ, µ, n, buf ) ,−−−−−−−−−−−−−→ (ρ, µ, n ′, buf ′)                        A.2        Return address prediction
                                    execute i
                                                                                       Next, we discuss how our semantics models function calls.
   When fetching a jmpi instruction, the schedule guesses
the jump target n ′. The rule records the operands and the                             Instructions. We introduce the following two physical in-
guessed program point in a new buffer entry. In a real proces-                         structions: call(n f , n ret ), where n f is the target program point
sors, the jump target guess is supplied by an indirect branch                          of the call and n ret is the return program point; and the return
predictor; as branch predictors can be arbitrarily influenced                          instruction ret. Their transient forms are simply call and ret.
by an adversary [14], we model the guess as an attacker                                Call stack. To track control flow in the presence of function
directive.                                                                             calls, our semantics explicitly maintains a call stack in mem-
   In the execute stage, we calculate the actual jump target                           ory. For this, we use a dedicated register r sp which points to
and compare it to the guess. If the actual target and the                              the top of the call stack, and which we call the stack pointer
guess match, we update the entry in the reorder buffer to the                          register.
resolved jump instruction jump n 0 . If actual target and the                             On fetching a call instruction, we update r sp to point to
guess do not match, we roll back the execution by removing                             the address of the next element of the stack using an ab-
all buffer entries larger or equal to i, update the buffer with                        stract operation succ. It then saves the return address to the
                                                                                  14
Constant-Time Foundations for the New Spectre Era                                                                                              ,,


                         n       1            2     3                        Calling.
               Program
                         µ(n)    call(3, 2)   ret   ret
   Directive    n        buf                              σ
   fetch        1→3      1 7→ call                        1 7→ push 2            call-direct-fetch
                         2 7→ r sp = op(succ, r sp )                                   µ(n) = call(n f , n ret )  i = MAX(buf ) + 1
                         3 7→ store(2, [r sp ])                                   buf 1 = buf [i 7→ call][i + 1 7→ (r sp = op(succ, r sp ))]
   fetch        3→2      4 7→ ret                         4 7→ pop                       buf ′ = buf 1 [i + 2 7→ store(n ret , [r sp ])]
                         5 7→ r tmp = load([r sp ])                                        σ ′ = σ [i 7→ push n ret ]    n ′ = nf
                         6 7→ r sp = op(pred, r sp )                                    (ρ, µ, n, buf , σ ) ,−−−→ (ρ, µ, n ′, buf ′, σ ′)
                         7 7→ jmpi([r tmp ], 2)                                                              fetch
   fetch: n     2→n      8 7→ ret                         8 7→ pop
                         9 7→ r tmp = load([r sp ])
                         10 7→ r sp = op(pred, r sp )
                         11 7→ jmpi([r tmp ], n)
                                                                                  call-retire
                                                                                                      MIN(buf ) = i
Figure 12. Example demonstrating a ret2spec-style at-                                  buf (i) = call       buf (i + 1) = (r sp = v ℓ )
tack [23]. The attacker is able to send (speculative) execution                   buf (i + 2) = store(n ret , a ℓa )   ρ ′ = ρ[r sp 7→ v ℓ ]
to an arbitrary program point, shown in red.                                        µ = µ[a 7→ n ret ]
                                                                                     ′
                                                                                                              buf = buf [j : j > i + 2]
                                                                                                                    ′

                                                                                                          write a ℓa
                                                                                      (ρ, µ, n, buf , σ ) ,−−−−−−−→ (ρ ′, µ ′, n, buf ′, σ )
                                                                                                             retire



                                                                                On fetching a call instruction, we add three transient in-
newly computed address. On returning from a function call,                   structions to the reorder buffer to model pushing the return
our semantics transfers control to the return address at r sp ,              address to the in-memory stack. The first transient instruc-
and then updates r sp to point to the address of the previ-                  tion, call, simply serves as an indication that the following
ous element using a function pred. This step makes use of a                  two instructions come from fetching a call instruction. The
temporary register r tmp .                                                   remaining two instructions advance r sp to point to a new
   Using abstract operations succ and pred rather than com-                  stack entry, then store the return address n ret in the new en-
mitting to a concrete implementation allows our semantics                    try. Neither of these transient instructions are fully resolved—
to capture different stack designs. For example, on a 32-bit                 they will need to be executed in later steps. We next add a
x86 processor with a downward-growing stack, op(succ, r sp )                 new entry to the RSB, signifying a push of the return ad-
would be implemented as r sp − 4, while op(pred, r sp ) would                dress n ret to the RSB. Finally, we set our program point to
be implemented as r sp + 4; on an upward growing system,                     the target of the call n f .
the reverse would be true.                                                      When retiring a call, all three instructions generated dur-
   Note that the stack register r sp is not protected from illegal           ing the fetch are retired together. The register file is updated
access and can be updated freely.                                            with the new value of r sp , and the return address is written
                                                                             to physical memory, producing the corresponding leakage.
Return stack buffer. For performance, modern processors                         The semantics for direct calls can be extended to cover
speculatively predict return addresses. To model this, we                    indirect calls in a straightforward manner by imitating the
extend configurations with a new piece of state called the re-               semantics for indirect jumps. We omit them for brevity.
turn stack buffer (RSB), written as σ . The return stack buffer
contains the expected return address at any execution point.                 Evaluating the RSB. We define a function top(σ ) that re-
Its implementation is simple: for a call instruction, the se-                trieves the value at the top of the RSB stack. For this, we let
mantics pushes the return address to the RSB, while for a                    Jσ K be a function that transforms the RSB stack σ into a stack
ret instruction, the semantics pops the address at the top                   in the form of a partial map (st : N ⇀ V) from the natural
of the RSB. Similar to the reorder buffer, we address the                    numbers to program points, as follows: the function J·K ap-
RSB through indices and roll it back on misspeculation or                    plies the commands for each value in the domain of σ , in the
memory hazards.                                                              order of the indices. For a push n it adds n to the lowest empty
   We model return prediction directly through the return                    index of st. For pop, it and removes the value with the highest
stack buffer rather than relying on attacker directives, as                  index in st, if it exists. We then define top(σ ) as st(MAX(st)),
most processors follow this simple strategy, and the predic-                 where st = Jσ K, and ⊥, if the domain of st is empty. For exam-
tions therefore cannot be influenced by an attacker.                         ple, if σ is given as ∅[1 7→ push 4][2 7→ push 5][3 7→ pop],
   We now present the step rules for our semantics.                          then Jσ K = ∅[1 7→ 4], and top(σ ) = 4.
                                                                        15
,,                                                                  S. Cauligi, C. Disselkoen, K. v. Gleissenthall, D. Tullsen, D. Stefan, T. Rezk, and G. Barthe


Returning.                                                                                       Registers                     Program
                                                                                                r    ρ(r )         n    µ(n)
          ret-fetch-rsb                                                                        rb 8pub             3    call(5, 4)
                    µ(n) = ret        top(σ ) = n ′                                            r sp 7Cpub          4    fence 4
          i = MAX(buf ) + 1           buf 1 = buf [i 7→ ret]                                                       5    rd = op(addr, [12, rb ], 6)
            buf 2 = buf 1 [i + 1 7→ (r tmp = load([r sp ]))]                                                       6    store(rd , [r sp ], 7)
           buf 3 = buf 2 [i + 2 7→ (r sp = op(pred, r sp ))]                                                       7    ret
              buf 4 = buf 3 [i + 3 7→ jmpi([r tmp ], n ′)]
                          σ ′ = σ [i 7→ pop]                                                     Effect of successive fetch directives
            (ρ, µ, n, buf , σ ) ,−−−→ (ρ, µ, n ′, buf 4 , σ ′)                              n     buf                             σ
                                  fetch                                                     3→5   3 7→ call                       3 7→ push 4
                                                                                                  4 7→ r sp = op(succ, r sp )
          ret-fetch-rsb-empty
                                                                                                  5 7→ store(4, [r sp ])
                    µ(n) = ret         top(σ ) = ⊥
                                                                                            5 → 6 6 7→ rd = op(addr, [12, rb ])
          i = MAX(buf ) + 1           buf 1 = buf [i 7→ ret]
                                                                                            6 → 7 7 7→ store(rd , [r sp ])
            buf 2 = buf 1 [i + 1 7→ (r tmp = load([r sp ]))]
                                                                                            7 → 4 8 7→ ret                        8 7→ pop
           buf 3 = buf 2 [i + 2 7→ (r sp = op(pred, r sp ))]                                      9 7→ r tmp = load([r sp ])
              buf 4 = buf 3 [i + 3 7→ jmpi([r tmp ], n ′)]                                        10 7→ r sp = op(pred, r sp )
                          σ ′ = σ [i 7→ pop]                                                      11 7→ jmpi([r tmp ], 4)
           (ρ, µ, n, buf , σ ) ,−−−−−−→′ (ρ, µ, n ′, buf 4 , σ ′)                           4 → 4 12 7→ fence
                                fetch: n
                                                                                           Directive              Effect on buf             Leakage
      ret-retire                                                                           execute 4              4 7→ r sp = 7B
                           MIN(buf ) = i
                                                                                           execute 6              6 7→ rd = 20
          buf (i) = ret       buf (i + 1) = (r tmp = v 1ℓ1 )                               execute 7 : value      7 7→ store(20, [r sp ])
      buf (i + 2) = (r sp = v 2ℓ2 )     buf (i + 3) = jump n ′                             execute 7 : addr       7 7→ store(20, 7B)        fwd 7B
       ρ = ρ[r sp 7→ v 2ℓ2 ]
        ′
                                    buf = buf [j : j > i + 3]
                                       ′
                                                                                           execute 9              9 7→ r tmp = 20           fwd 7B
             (ρ, µ, n, buf , σ ) ,−−−→ (ρ ′, µ, n, buf ′, σ )                              execute 11
                                                                                                                  12 < buf                  rollback,
                                  retire                                                                          11 7→ jump 20             jump 20
   On a fetch of ret, the next program point is set to the pre-
dicted return address, i.e., the top value of the RSB, top(σ ).                    Figure 13. Example demonstrating “retpoline” mitigation
Just as with call, we add the transient ret instruction to the                     against Spectre v2 attack. The program is able to jump to
reorder buffer, followed by the following (unresolved) in-                         program point 12 +rb = 20 without the schedule influencing
structions: we load the value at address r sp into a temporary                     prediction.
register r tmp , we “pop” r sp to point back to the previous stack
entry, and then add an indirect jump to the program point
given by r tmp . Finally, we add a pop entry to the RSB. As with                   Examples. We present an example of an RSB underflow at-
call instructions, the set of instructions generated by a ret                      tack in Figure 12. After fetching a call and paired ret instruc-
fetch are retired all at once.                                                     tion, the RSB will be “empty”. When one more (unmatched)
   When the RSB is empty, the attacker can supply a specu-                         ret instruction is fetched, since top(σ ) = ⊥, the program
lative return address via the directive fetch: n ′. This is con-                   point n is no longer set by the RSB, and is instead set by the
sistent with the behavior of existing processors. In practice,                     (attacker-controlled) schedule.
there are several variants on what processors actually do                          Retpoline mitigation. A mitigation for Spectre v2 attacks
when the RSB is empty [23]:                                                        is to replace indirect jumps with retpolines [31]. Figure 13
     ▶ AMD processors refuse to speculate. This can be mod-                        shows a retpoline construction that would replace the indi-
       eled by defining top(σ ) to be a failing predicate if it                    rect jump in Figure 11. The call sends execution to program
       would result in ⊥.                                                          point 5, while adding 4 to the RSB. The next two instructions
     ▶ Intel Skylake/Broadwell processors fall back to using                       at 5 and 6 calculate the same target as the indirect jump in
       their branch target predictor. This can be modeled by                       Figure 11 and overwrite the return address in memory with
       allowing arbitrary n ′ for the fetch: n ′ directive for the                 this jump target. When executed speculatively, the ret at 7
       ret-fetch-rsb-empty rule.                                                   will pop the top value off the RSB, 4, and jump there, landing
     ▶ “Most” Intel processors treat the RSB as a circular                         on a fence instruction that loops back on itself. Thus spec-
       buffer, taking whichever value is produced when the                         ulative execution cannot proceed beyond this point. When
       RSB over- or underflows. This can be modeled by hav-                        the transient instructions in the ret sequence finally execute,
       ing top(σ ) always produce an according value, and                          the indirect jump target 20 is loaded from memory, causing a
       never producing ⊥.                                                          roll back. However, execution is then directed to the proper
                                                                              16
Constant-Time Foundations for the New Spectre Era                                                                                                       ,,


jump target. Notably, at no point is an attacker able to hijack                      will result in the same configuration since they inde-
the jump target via misprediction.                                                   pendently resolve the components of the store.
                                                                                  ▶ For br, D 1′′ and D 2′′ may have different guesses for their
B     Full proofs                                                                    initial fetch directives. However, both cond-execute-
B.1    Consistency                                                                   correct and cond-execute-incorrect will result in
                                         o′              o ′′                        the same configuration regardless of the initial guess,
Lemma B.1 (Determinism). If C ,−
                               → C ′ and C ,−→ C ′′ then                             as the br is the only instruction in the buffer. Similarly
                                         d               d
C ′ = C ′′ and o ′ = o ′′.                                                           for jmpi.
                                                                                  ▶ For call and ret, the ordering of execution of the re-
Proof. The tuple (C, d) fully determines which rule of the                           sulting transient instructions does not affect the final
semantics can be executed.                               □                           configuration.
Definition B.2 (Initial/terminal configuration). A configu-                       Thus for all cases we have C 1 = C 2 .                      □
ration C is an initial (or terminal) configuration if |C.buf | =
                                                                                  To make our discussion easier, we will say that a directive
0.                                                                                                                                       o
                                                                               d applies to a buffer index i if when executing a step C ,−
                                                                                                                                        → C ′:
Definition B.3 (Sequential schedule). Given a configura-                                                                                            d

tion C, we say a schedule D is sequential if every instruction                    ▶ d is a fetch directive, and would fetch an instruction
that is fetched is executed and retired before further instruc-                      into index i in buf .
tions are fetched.                                                                ▶ d is an execute directive, and would execute the in-
                                                                                     struction at index i in buf .
                                                 N ′
Definition B.4 (Sequential execution). C O⇓D       C is a sequen-                 ▶ d is a retire directive, and would retire the instruction
tial execution if C is an initial configuration, D is a sequential                   at index i in buf .
schedule for C, and C ′ is a terminal configuration.                              We would like to reason about schedules that do not con-
                 N
    We write C O⇓seq C ′ if we execute sequentially.                           tain misspeculated steps, i.e., directives that are superfluous
                                                                               due to their effects getting wiped away by rollbacks.
                                                      N
Lemma B.5 (Sequential equivalence). If C O 1⇓D             C 1 is se-
                   N
                                                         1                     Definition B.6 (Misspeculated steps). Given an execution
quential and C O 2⇓D 2 C 2 is sequential, then C 1 = C 2 .                          N ′
                                                                               C O⇓D  C , we say that D contains misspeculated steps if there
                                                                                                                            N
Proof. Suppose N = 0. Then neither D 1 nor D 2 may contain                     exists d ∈ D such that D ′ = D \ d and C O ′⇓D ′C
                                                                                                                                 ′′ = C ′ .

any retire directives. Since we assume that both C 1 .buf and                                              N ′
                                                                                  Given an execution C O⇓D   C that may contain rollbacks,
C 2 .buf have size 0, neither D 1 nor D 2 may contain any fetch
                                                                               we can create an alternate schedule D ∗ without any rollbacks
directives. Therefore, both D 1 and D 2 are empty; both C 1 and
                                                                               by removing all misspeculated steps. Note that sequential
C 2 are equal to C.
                                                                               schedules have no misspeculated steps6 as defined in Defini-
    We proceed by induction on N .
                                                                               tion B.6.
    Let D 1′ be a sequential prefix of D 1 up to the N − 1th retire,
and let D 1′′ be the remainder of D 1 . That is, #{d ∈ D 1′ | d =              Theorem B.7 (Equivalence to sequential execution). Let C
retire} = N − 1 and D 1′ ∥D 1′′ = D 1 . Let D 2′ and D 2′′ be similarly        be an initial configuration and D a well-formed schedule for
                                                                                           N                  N
defined.                                                                       C. If C O 1⇓D C 1 , then C O 2⇓seq C 2 and C 1 ≈ C 2 . Furthermore, if
                                                           N −1 ′
    By our induction hypothesis, we know C O 1′⇓D            ′  C and          C 1 is terminal then C 1 = C 2 .
                                                             1
       N −1 ′
C O 2′⇓D ′ C for some C ′. Since D 1′ (resp. D 2′ ) is sequential             Proof. Since we can always remove all misspeculated steps
         2
and |C .buf | = 0, the first directive in D 1′′ (resp. D 2′′) must be
         ′
                                                                              from any well-formed execution without affecting the final
a fetch directive. Furthermore, C ′ O 1′′⇓1D ′′ C 1 and C ′ O 2′′⇓1D ′′ C 2 . configuration, we assume D 1 has no misspeculated steps.
                                                                                 Suppose N = 0. Then the theorem is trivially true. We
                                             1                       2
   We can now proceed by cases on C .µ[C .n], the final
                                                ′     ′

instruction to be fetched.                                                    proceed   by induction on N .
    ▶ For op, the only valid sequence of directives is (fetch,                   Let D ′ be the subsequence of D containing the first N − 1
                                                                                       1                         1

        execute i, retire) where i is the sole valid index in the             retire directives and the directives that apply to the same
        buffer. Similarly for fence, with the sequence {fetch, retire}. indices of the first        N − 1 retire directives. Let D 1′′ be the
    ▶ For load, alias prediction is not possible, as no prior                 complement of D 1 with respect to D 1 . All directives in D 1′′
                                                                                                  ′

        stores exist in the buffer. Therefore, just as with op, the           apply to indices later than any directive in D 1′ , and thus
        only valid sequence of directives is (fetch, execute i,               cannot affect the execution of directives in D 1′ . Thus D 1′ is a
                                                                                                                                      N −1 ′
        retire).                                                              well-formed schedule and produces execution C O 1′⇓D     ′    C1 .
                                                                                                                                                1
    ▶ For store, the only possible difference between D 1′′                    6 Sequential schedules may still misspeculate on conditional branches but
      and D 2′′ is the ordering of the execute i : value and                   the rollback does not imply removal of any reorder buffer instructions as
      execute i : addr directives. However, both orderings                     defined in Definition B.6.
                                                                          17
,,                                                                      S. Cauligi, C. Disselkoen, K. v. Gleissenthall, D. Tullsen, D. Stefan, T. Rezk, and G. Barthe


    Since D 1 contains no misspeculated steps, the directives                            D seq
                                                                                           ′′ (with trace O ′′ ) as the subsequence of D ′′ of directives
                                                                                                              2                              1
in D 1′′ can be reordered after the directives in D 1′ . Thus                            applying to the remaining instruction to be retired. As noted
D 1′′ is a well-formed schedule for C 1′ , producing execution                           before, executing the subsequence of a schedule produces
C 1′ O 1′′⇓1D ′′ C 1′′ with C 1′′ ≈ C 1 . If C 1 is terminal, then C 1′′ is also         the corresponding subsequence of the original trace; hence
                                                                                         ∀o ∈ O 2′′ : ℓ < o.
              1
terminal and C 1′′ = C 1 .
    By our induction hypothesis, we know there exists D seq                   ′             The trace of the final (sequential) schedule D seq = D seq
                                                                                                                                                    ′ ∥D ′′
                                                                                                                                                         seq
such that C O 2′⇓D seq    N −1
                            ′   C 2 . Since D 1 contains equal numbers of
                                  ′            ′                                         is O 2 ∥O 2 . Since O 2 satisfies the label stability property via
                                                                                               ′   ′′          ′

                                                                                         the induction hypothesis, we have ∀o ∈ O 2′ ∥O 2′′ : ℓ < o.
fetch and retire directives, ends with a retire, and contains
                                                                                                                                                         □
no misspeculated steps, C 1′ is terminal. Thus C 1′ = C 2′ .
    Let D seq  ′′ be the subsequence of D ′′ containing the retire
                                                        1                                   By letting ℓ be the label secret, we get the following corol-
directive in D 1′′ and the directives that apply to the same                             lary:
index. D seq     ′′ is sequential with respect to C ′ and produces
                                                                                         Corollary B.10 (Secrecy). If speculative execution of C under
                                                              1
execution C 1′ O 2′′⇓1D seq   ′′ C 2 with C 2 ≈ C 1 ≈ C 1 . If C 1 is terminal,
                                    ′′        ′′       ′′         ′′
                                                                                         schedule D produces a trace O that contains no secret labels,
then D seq   ′′ = D ′′ and thus C ′′ = C ′′ = C .
                        1                 2       1       1                              then sequential execution of C will never produce a trace that
    Let D seq = D seq      ′ ∥D ′′ . D
                                    seq    seq is thus itself sequential and             contains any secret labels.
                                               N
produces execution C (O 2′ ∥O 2′′ )⇓seq           C 2′′, completing our proof.
                                                                                □           With this, we can prove the following proposition:

Corollary B.8 (General consistency). Let C be an initial                                 Proposition B.11. For a given initial configuration C and
                        N
configuration. If C O 1⇓D                 N
                            C 1 and C O 2⇓D   C 2 , then C 1 ≈ C 2 .                     well-formed schedule D, if C is SCT with respect to D, and
                          1                 2
Furthermore, if C 1 and C 2 are both terminal then C 1 = C 2 .                           execution of C with D results in a terminal configuration C 1 ,
                                                                                         then C is also sequentially constant-time.
Proof. By Theorem B.7, there exists D seq
                                       ′  such that execut-
ing with C produces C 1 ≈ C 1 (resp. C 1′ = C 1 ). Similarly,
                        ′                                                                Proof. Since C is SCT, we know that for all C ′ ≃pub C, we
                                                                                                       N                 N ′
there exists D seq
               ′′ that produces C ′ ≈ C (resp. C ′ = C ). By
                                        2             2
                                                                                         have C O⇓D      C 1 and C ′ O ′⇓D C 1 where C 1 ≃pub C 1′ and O = O ′.
                                  2              2
Lemma B.5, we have C 1′ = C 2′ . Thus C 1 ≈ C 2 (resp. C 1 =                             By Theorem B.7, we know there exist sequential executions
                                                                                                               N                      N
C 2 ).                                                     □                             such that C O seq⇓seq    C 2 and C ′ O seq
                                                                                                                                 ′ ⇓
                                                                                                                                      seq C 2 . Note that the two
                                                                                                                                            ′

                                                                                         sequential schedules need not be the same.
B.2     Security                                                                            C 1 is terminal by hypothesis. Execution of C ′ uses the same
Theorem B.9 (Label stability). Let ℓ be a label in the lattice                           schedule D, so C 1′ is also terminal. Since we have C 1 = C 2
            N
L. If C O 1⇓D                                        N
                C 1 and ∀o ∈ O 1 : ℓ < o, then C O 2⇓seq C 2 and                         and C 1′ = C 2′ , we can lift C 1 ≃pub C 1′ to get C 2 ≃pub C 2′ .
              1
∀o ∈ O 2 : ℓ < o.                                                                           To prove the trace property O seq = O seq           ′ , we note that if

                                                                                         O seq , O seq , then since C 2 ≃pub C 2 , it must be the case that
                                                                                                     ′                              ′
Proof. Let D 1∗ be the schedule given by removing all mis-                               there exists some o ∈ O seq such that secret ∈ O seq . Since
speculated steps from D 1 . The corresponding trace O 1∗ is a                            this is also true for O and O ′, we know that there exist no
subsequence of O 1 , and hence ∀o ∈ O 1∗ : ℓ < o. We thus                                observations in either O or O ′ that contain secret labels.
proceed assuming that execution of D 1 contains no misspec-                              By Corollary B.10, it follows that no secret labels appear in
ulated steps.                                                                            either O seq or O seq′ , and thus O
                                                                                                                               seq = O seq .
                                                                                                                                          ′                      □
   Our proof closely follows that of Theorem B.7. When
constructing D 1′ and D 1′′ from D 1 in the inductive step, we                           B.3    Soundness of Pitchfork
know that all directives in D 1′′ apply to indices later than any                        Definition B.12 (Affecting an index). We say a directive d
directive in D 1′ , and cannot affect execution of any directive                         affects an index i if:
in D 1′ . This implies that O 1′ is the subsequence of O 1 that
                                                                                             ▶ d is a fetch-type directive and would produce a new
corresponds to the mapping of D 1′ to D 1 .
                                                                                                mapping in buf at index i.
   Reordering the directives in D 1′′ after D 1′ do not affect the
                                                                                             ▶ d is an execute-type directive and specifies index i
observations produced by most directives. The exceptions to
                                                                                                directly (e.g., execute i).
this are execute directives for load instructions that would
                                                                                             ▶ d is a retire directive and would cause the instruction
have received a forwarded value: after reordering, the store
                                                                                                at i in buf to be removed.
instruction they forwarded from may have been retired, and
they must fetch their value from memory. However, even in                                Definition B.13 (Path function). The function Path(C, D)
this case, the address a ℓa attached to the observation does                             produces the sequence of branch choice (from fetching br
not change. Thus ∀o ∈ O 2′′ : ℓ < o.                                                     instructions) and store-forwarding information (when exe-
   Continuing the proof as in Theorem B.7, we create sched-                              cuting load instructions) when executing D with initial con-
ule D seq
        ′ (with trace O ′ ) from the induction hypothesis and
                          2                                                              figuration C. That is, for a schedule D without misspeculated
                                                                                    18
Constant-Time Foundations for the New Spectre Era                                                                                             ,,


steps:                                                                          same register dependencies. For each register dependency
    Path(C, ∅) = []                                                             r , if the register was calculated by a transient instruction at
                                                                                a prior index j, we can create prefixes D 1, j and D 2, j of D 1
                
                
                 Path(C, D); (i, b),         d = fetch: b                      and D 2 respectively that end at the execute directive that
                Path(C, D); (i, j),          d produces v ℓ {j, a}             resolves r at buffer index j. By our induction hypothesis,
                
                
Path(C, D ∥d) =
                
                Path(C, D); (i, ⊥),          d produces v ℓ {⊥, a}             both D 1, j and D 2, j calculate the same value v ℓ for r .
                
                
                Path(C, D),
                                                                                   We now proceed by cases on the transient instruction
                                              otherwise
                                                                               being executed.
where d affects index i. If D has misspeculated steps, then                     Op, Store (value). Since all dependencies calculate the same
Path(C, D) = Path(C, D ∗ ) where D ∗ is the subset of D with                    values, both instructions calculate the same value.
misspeculated steps removed. We write simply Path(D) when
                                                                                Store (address). Both instructions calculate the same address.
C is obvious.
                                                                                Since Path(D 1 ) = Path(D 2 ), both schedules have the same
   For the Lemmas B.14, B.16 and B.17, we start with the                        pattern of store-forwarding behavior. Thus execution of d 1
following shared assumptions:                                                   causes a hazard if and only if d 2 causes a hazard.
    ▶ C is an initial configuration.                                            Load. Both instructions calculate the same address, pro-
    ▶ D 1 and D 2 are nonempty schedules.                                       ducing the same observations o 1 and o 2 . Since Path(D 1 ) =
    ▶ C D 1⇓O 1 C 1 and C D 2⇓O 2 C 2 .                                         Path(D 2 ), either d 1 and d 2 cause the values to be retrieved
    ▶ Path(C, D 1 ) = Path(C, D 2 ).                                            from the same prior stores, or they both load values from the
    ▶ D 1 = D 1′ ∥d 1 and D 2 = D 2′ ∥d 2 and d 1 = d 2 .                       same address in memory. By our induction hypothesis, these
    ▶ d 1 and d 2 affect the same index i in the their respective               values will be the same, so both instructions will resolve to
       reorder buffers.                                                         the same value.
Let o 1 (resp. o 2 ) be the observation produced during execu-                  Branch. Both instructions calculate the same branch con-
tion of d 1 (resp. d 2 ).                                                       dition, producing the same observations o 1 and o 2 . Since
                                                                                Path(D 1 ) = Path(D 2 ), execution of d 1 causes a misspecu-
Lemma B.14 (Fetch). If d 1 and d 2 are both fetch-type direc-                   lation hazard if and only if d 2 also causes misspeculation
tives, then C 1 .n = C 2 .n and C 1 .buf [i] = C 2 .buf [i].                    hazard.                                                       □
Proof. Since fetches happen in-order, the index i of a given                    Lemma B.17. If d 1 and d 2 are both retire directives, then
physical instruction along a control flow path is deterministic.                o1 = o2 .
Both D 1 and D 2 both have the same (control flow) path. Since
by hypothesis both d 1 and d 2 affect the same index i, d 1                     Proof. From Lemmas B.14 and B.16 we know that for both
and d 2 must necessarily both be fetching the same physical                     d 1 and d 2 , the transient instructions to be retired are the
instruction. Furthermore, since Path(D 1 ) = Path(D 2 ), if the                 same. Thus the produced observations o 1 and o 2 are also the
fetched instruction is a br instruction, then both d 1 and d 2                  same.                                                        □
must have made the same guess. The lemma statements all                            We now formally define the set of schedules examined by
hold accordingly.                                             □                 Pitchfork:
Corollary B.15. If D 1∗ and D 2∗ are nonempty schedules such                    Definition B.18 (Tool schedules). Given an initial configu-
that C D 1∗⇓ C 1∗ and C D 2∗⇓ C 2∗ and Path(C, D 1∗ ) = Path(C, D 2∗ ),         ration C and a speculative window size n, we define the set
then: For any i ∈ C 1∗ .buf , if i ∈ C 2∗ .buf , then both C 1∗ .buf [i]        of tool schedules DT (n) recursively as follows: The empty
and C 2∗ .buf [i] were derived from the same physical instruction.              schedule ∅ is in DT (n). If D 0 ∈ DT (n) and C D 0⇓ C 0 and
Proof. Let D 1 be the prefix of D 1∗ such that the final directive              |C 0 .buf | < n, then based on the next instruction to be fetched
in D 1 is the latest fetch that affects i. Let D 2 be similarly                 (and where i is the index of the fetched instruction):
defined w.r.t. D 2∗ . Then by Lemma B.14, D 1 and D 2 both fetch                     ▶ op: D 0 ∥fetch; execute i ∈ DT (n).
the same physical instruction to index i.                        □                   ▶ load: D 0 ∥fetch; execute i ∈ DT (n).
                                                                                     ▶ store: D 0 ∥fetch; execute i : value ∈ DT (n) and
Lemma B.16. If d 1 and d 2 are both execute-type directives,                            D 0 ∥fetch; execute i : value; execute i : addr ∈ DT (n).
then C 1 .buf [i] = C 2 .buf [i] and o 1 = o 2 .                                     ▶ br: Let b be the “correct” path for the branch condition.
Proof. We proceed by full induction on the size of D 1 .                                Then D 0 ∥fetch: b; execute i ∈ DT (n) and
   For the base case: if |D 1 | = 1, then the lemma statements                          D 0 ∥fetch: ¬b ∈ DT (n).
are trivial regardless of the directive d 1 .                                   Otherwise, if |C 0 .buf | = n, then we instead extend based
   We know from Corollary B.15 that since d 1 and d 2 both                      on the oldest instruction in the reorder buffer. If the oldest
affect the same index i, the two transient instruction must be                  instruction is a store with an unresolved address, and will
derived from the same physical instruction, and thus has the                    not cause a hazard, then D 0 ∥execute i : addr; retire ∈ DT (n).
                                                                           19
,,                                                      S. Cauligi, C. Disselkoen, K. v. Gleissenthall, D. Tullsen, D. Stefan, T. Rezk, and G. Barthe


Otherwise, if the oldest instruction is fully resolved, then
D 0 ∥retire ∈ DT (n).
Proposition B.19 (Path coverage). If D 1 is a well-formed
schedule for C whose reorder buffer never grows beyond size n,
then ∃D 2 : Path(D 1 ) = Path(D 2 ) ∧ D 2 ∈ DT (n).
Proof. The proof stems directly from the definition of DT (n);
at every branch, both branches are added to the set of sched-
ules, and every load is able to “skip” any combination of prior
stores.                                                      □
Theorem B.20 (Soundness of tool). If speculative execution
of C under a schedule D with speculation bound n produces
a trace O that contains at least one secret label, then there
exists a schedule D t ∈ DT (n) that produces a trace O t that
also contains at least one secret label.
Proof. We can truncate D to a schedule D ∗ that ends at the
first directive to produce a secret observation. By Propo-
sition B.19 there exists a schedule D 0 ∈ DT (n) such that
Path(D t ) = Path(D ∗ ). By following construction of tool
schedules as given in Definition B.18, we can find a schedule
D t ∈ DT (n) that satisfies the preconditions for Lemma B.16.
Then by that same lemma, D t produces the same final obser-
vation as D ∗ , which contains a secret label.             □




                                                                  20
