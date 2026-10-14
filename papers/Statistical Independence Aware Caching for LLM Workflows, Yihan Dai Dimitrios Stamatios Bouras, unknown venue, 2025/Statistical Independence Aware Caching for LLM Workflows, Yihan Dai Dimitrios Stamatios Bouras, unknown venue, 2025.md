                                             Statistical Independence Aware Caching for LLM Workflows
                                                                       Yihan Dai                                                Dimitrios Stamatios Bouras
                                                               yhdai25@stu.pku.edu.cn                                               2501112125@stu.pku.edu.cn
                                                                  Peking University                                                     Peking University
                                                                   Beijing, China                                                         Beijing, China

                                                                    Haoxiang Jia                                                         Sergey Mechtaev
                                                             haoxiangjia@stu.pku.edu.cn                                                mechtaev@pku.edu.cn
                                                                  Peking University                                                     Peking University
                                                                   Beijing, China                                                         Beijing, China
arXiv:2511.22118v1 [cs.SE] 27 Nov 2025




                                         Abstract                                                                single LLM response. Whenever the same prompt is encountered
                                         Large language models (LLMs) inference is both expensive and slow.      again, the cached response is returned instead of generating a new
                                         Local caching of responses offers a practical solution to reduce the    one. This design conflicts with statistical independence required
                                         cost and latency of LLM queries. In research contexts, caching also     by many algorithms. In LLMs for code, widely adopted metrics like
                                         enhances reproducibility and provides flexibility for experimenta-      Pass@k [6] rely on generating statistically independent samples to
                                         tion. However, naive reuse of cached responses compromises statis-      estimate the probability of a solution’s success. Similarly, methods
                                         tical independence, a critical property for probabilistic workflows.    for calibrating model uncertainty [11, 15, 17], as well as iterative
                                         In applications of LLM for code, it underpins performance metrics       repair and refinement pipelines [12, 16, 20], inherently depend on
                                         such as Pass@k and uncertainty estimation, as well as algorithms        the model’s ability to produce varied outputs for the same prompt.
                                         like program repair loops and retries. Existing LLM caching sys-        Meanwhile, a naive cache collapses this necessary variation.
                                         tems lack ways to enforce statistical independence constraints. To          A straightforward approach to address this problem is to cache
                                         address this, we introduce Mnimi, a cache design pattern that sup-      a sequence of independent responses for each prompt and replay
                                         ports modular LLM workflows while ensuring statistical integrity        them during every application run, instead of caching a single re-
                                         at the component level. Its core innovation lies in encapsulating       sponse. While this ensures statistical independence within each
                                         statistical constraints within the type of LLM references, allow-       run, it has practical drawbacks. First, it is inefficient because it does
                                         ing users to manage and transform these types according to the          not reuse samples within the run. Second, it undermines repro-
                                         scope and requirements of their algorithm. We implemented this          ducibility and debugging, as even small changes to the program can
                                         design pattern in Python using a combination of decorators and          disrupt the sequence of responses being replayed. Cache Saver [18]
                                         iterators over infinite sequences. A case study on SpecFix, an recent   alleviated this issue by introducing explicit namespaces, where
                                         automated program specification repair system, highlights how           each namespace stores independent responses for a given prompt.
                                         Mnimi improves reproducibility, ease of debugging, time and cost        However, this approach prohibits reuse within a namespace by
                                         efficiency while preserving statistical correctness.                    design, limiting flexibility for users in controlling granularity of
                                                                                                                 sample reuse. Furthermore, LLM workflows are often modular and
                                         CCS Concepts                                                            deeply nested and therefore sampling constraints are also modu-
                                                                                                                 lar and nested. The requirement to explicitly maintain statistical
                                         • Computing methodologies → Natural language processing;
                                                                                                                 independence namespaces harms modularity.
                                         • Software and its engineering → Abstraction, modeling and
                                                                                                                     To address these limitations, we introduce Mnimi1 , a new caching
                                         modularity; Designing software.
                                                                                                                 design pattern that supports modular LLM workflows, while ensur-
                                                                                                                 ing statistical integrity at the component level. At its core, the idea
                                         Keywords                                                                is to encapsulate statistical independence constraints as types of
                                         Large language models, cache, statistical independence                  LLM references: Repeatable, ensuring repeated responses for each
                                                                                                                 LLM query, and Independent, ensuring independent responses for
                                         1   Introduction                                                        each query. This design pattern promotes modularity by enabling
                                         The use of LLMs in software engineering is rapidly expanding, how-      transformations of LLM reference types through decorators [8],
                                         ever this comes with substantial costs in time, money, and energy       effectively allowing the user to specify statistical constraints as
                                         due to LLM inference. LLM backend optimizations [14] alleviate          easily as “wrapping a gift”. These layers form a coherent hierarchy
                                         these issues but are model-specific, requiring extensive engineering    governing stability within a program scope, diversity across scopes,
                                         or proprietary hardware access. A practical alternative is client-      and continuity across runs — capturing the complete statistical
                                         side caching of LLM responses [2, 10, 18], which avoids redundant       semantics that a typical application requires.
                                         queries, improving speed, cost-efficiency, and enabling determin-
                                         istic debugging, without altering the LLM. In research contexts, it
                                                                                                                 1 Mnimi derives from the Greek word μνήμη (mnēmē), meaning “memory.” In Greek
                                         enhances reproducibility and facilitates experimentation.
                                                                                                                 mythology, Mnēmē is one of the three primordial Muses, symbolizing remembrance,
                                            A typical client-side caching approach, as implemented in the        the foundation of knowledge and creativity. This aligns our goal to bring structured
                                         popular LangChain framework [5], associates each prompt with a          memory to LLM workflows, balancing reuse and independence.
                                                                                                                                                Dai et al.




Figure 1: An example showing the different behaviors of Independent vs. Repeatable. In the “Iterator State Transition” column,
the first sub-row of it shows the sequence state returned by calling sample and the second sub-row shows the state after iterating
to retrieve elements, while “→” denotes the pointer to the next element inside the iterator.

   To show Mnimi’s applicability in the context of LLM for code, we   key characteristic of the input users is that it may include duplicate
conducted a case study on SpecFix [12], a recent tool for repairing   usernames (e.g., 'Alice'), reflecting the scenario where a single
ambiguous programming problem descriptions. Its heavy reliance        user engages with multiple distinct games.
on stochastic LLM calls makes runs expensive and hard-to-replicate,      The critical issue lies in whether the responses for duplicated
with variations in generated tests, programs, and repaired descrip-   usernames (e.g., Alice’s first and third entries) are repeated or in-
tion. A naive LLM caching cannot be adopted, because of SpecFix’s     dependent, as this directly impacts Alice’s strategy for guessing
reliance on semantic entropy [13] and Pass@k computation, as          the number. Assume that a fair game requires that responses are
well as its main repair loop, all requiring independent samples. To   independent, that is, every time an integer is requested from the
resolve this tension, we replaced the original LLM calls in SpecFix   LLM for a specific user, it will ensure that the response for this
with Mnimi, while carefully encoding the statistical independence     time is independent of all previous responses2 . However, if the
constraints via the type of references to the LLM object. Experi-     application is changed to use a naive cache that simply returns a
ments show that Mnimi improves execution time and inference           cached response to the same prompt, the responses will then be
cost over the original tool, and enables bit-reproducibility, while   repeated. Since statistical independence is a prerequisite of the pro-
requiring only minor changes to SpecFix source code.                  gram above, using naive cache contradicts the intended semantics.
   A Python implementation of Mnimi, that supports multiple           Thus, the use of a cache in this scenario requires encoding and
providers, cache slicing (extracting a subset of cache), and batch    respecting algorithm’s sample independence constraints.
sampling, as well as our SpecFix integration are available at            Let’s extend the example so that each user play several rounds
               https://github.com/msv-lab/mnimi                       of the game, possibly guessing numbers from different intervals:
                                                                       ints = ["[1, 1000]", "[1001, 2000]", "[1, 1000]"]
2   Mnimi                                                              for user in users:
                                                                         for interval in ints:
The challenge with statistical independence arises when an applica-        prompt = template.format(user=user,interval=interval)
tion repeatedly queries an LLM using the same prompt, i.e. samples         response = model.sample(prompt)
multiple values from the same distribution. The following Python           responses.append(response)
snippet illustrates an LLM-based guessing game
                                                                         Assume we ensured independence across the outer loop itera-
 template = "Choose an integer from {interval} for {user} to
                                                                      tions; a new question arises: within a single iteration of the outer
 ↩→ guess."
                                                                      loop, should the responses across rounds be independent for the
 user = ['Alice', 'Bob', 'Alice']
 interval = "[1, 1000]"
                                                                      same interval, e.g. for the repeated interval [1,1000]? Let the game
 responses = []                                                       dictate that across the rounds, users must always guess the same
 for user in users:                                                   number if the interval remains unchanged. In other words, sam-
   prompt = template.format(user=user, interval=interval)             pling within each iteration should be repeatable. To achieve this, an
   response = model.sample(prompt) # queries an LLM                   ad-hoc caching mechanism could be implemented, such as main-
   responses.append(response)                                         taining a dictionary to store the samples corresponding to each
                                                                      element in ints, reusing them when they appear a second time.
In this example, a shared prompt template is used across different
games to generate guessing numbers within the given interval. A       2 note that independence does not imply uniqueness because of stochasticity
Statistical Independence Aware Caching for LLM Workflows




Figure 2: Structure of Mnimi design pattern that combines decorators and iterators over infinite sequences of responses to
encode statistical independence constraints in a modular fashion. Mnimi provides two concrete implementations of Repeatable:
an in-memory cache InMemory and an on-disk cache Persistent.

However, this approach compromises readability and modularity,              Finally, to achieve statistical independence, we introduce a dec-
as it tightly couples the program logic to the cache implementation.     orator Independent. In contrast to Repeatable, it ensures that
Additionally, if different rounds require different numbers of sam-      each call to sample produce an independent sequence of responses.
ples, the complexity would increase further, potentially introducing     To achieve that, the implementation of sample for Independent
bugs. Thus, to ensure consistent use of cached samples, one must         merely always returns the same iterator for the same prompt. Since
specify scopes of the algorithm in which samples are expected to         the iterator is shared, it is consumptive — responses used by one
repeat, or be independent.                                               call will not be reused by others, making the effect stateful. Impor-
                                                                         tantly, Independent itself neither generates nor stores responses;
2.1     Cache Design Pattern                                             rather, it only defines a strategy for consuming them from the inner
                                                                         model. The use of Independent in Figure 1 in Line 8 ensures that
At Mnimi’s core is the Model interface providing a single method
                                                                         since n5_list has already used "131" and "561", the iterator for
def sample(self, prompt: str) -> Iterator[str]                           n6_list skips them and resamples, yielding "452" and "980".
which takes in a prompt and returns an infinite sequence of i.i.d.
responses from an LLM. The independence of samples within the            2.2    Design Pattern Application Examples
sequence must be guaranteed by all implementation of this inter-         Here, we extend the example from the beginning of this section to
face. In particular, we introduce three implementations of Model         three cases, illustrating how our design pattern elegantly handles
shown in Figure 2. Firstly, ModelService returns an iterator that        successive changes in sampling constraints. At first, we assume
queries the model provider for new samples, without caching. In          that we have already cached a sequence of independent responses
this context, sample independence must be ensured by the provider.       for each prompt (showing prompt template parameters only):
   Secondly, to realize a caching mechanism, we introduce a dec-
                                                                         template("Alice", "[1, 1000]"):         ["2", "68", "109", "12"]
orator Repeatable. It wraps an existing model so that its sample         template("Bob",   "[1, 1000]"):         ["297", "573"]
method produces a specialized type of iterator, GetOldSample. This       template("Alice", "[1001, 2000]"):      ["1393", "1002"]
iterator retrieves responses from a cache associated with each           template("Bob",   "[1001, 2000]"):      ["1740"]
prompt; in case of cache misses, samples are obtained from the
                                                                           First, assume the user must be given the same number in every
inner model, and added to the cache. Importantly, Repeatable still
                                                                         round, even in different games:
ensures independence of responses in the lazy sequence from a
single call of sample. Instead, the repeatability is guaranteed across    model = Persistent(model, "/cache/path")
different calls of sample. To achieve that, Repeatable returns a          responses = []
new iterator over the same sequence for each call of sample with          for user in users:
the same prompt. Figure 1 illustrates the impact of repeatability           for interval in ints:
(Line 5), where even though n3 has consumed "131", the iterator re-           prompt = template.format(user=user,interval=interval)
                                                                              response = next(model.sample(prompt))
turned to n4_list still begins at "131". While Repeatable serves
                                                                              responses.append(response)
as an implementation of Model, it also abstracts the storage layer
                                                                          assert responses == ["2", "1393", "2", "297", "1740",
through the store and load methods, which must be implemented
                                                                          ↩→ "297", "2", "1393", "2"]
by concrete cache backends in ConcreteCacheImplementation.
                                                                                                                                       Dai et al.


where Persistent is an subclass of Repeatable that caches re-               We applied Mnimi to SpecFix’s source code, systematically en-
sponses on-disk. Now, assume a user is given an independent num-         coding the required statistical independence constraints using LLM
ber every time they request one:                                         reference types. Each caching layer in SpecFix serves a distinct se-
 model = Persistent(model, "/cache/path")                                mantic purpose tailored to the statistical requirements of the repair
 model = Independent(model)                                              process. Listing 1 presents a simplified version of SpecFix’s repair
 responses = []                                                          loop, which iteratively refines a given description over a maximum
 for user in users:                                                      of max_attempts. If the score for a repaired description fails to
   for interval in ints:                                                 improve, the repair is discarded. This last aspect of the algorithm in-
     prompt = template.format(user=user,interval=interval)               troduces specific requirements for statistical independence in LLM
     response = next(model.sample(prompt))                               samples. While stable score computation for each description is
     responses.append(response)                                          desirable — achieved through the Persistent caching layer, which
 assert responses == ["2", "1393", "68", "297", "1740",
                                                                         consistently provides the same sets of programs and tests for the
 ↩→ "573", "109", "1002", "12"]
                                                                         same description — each repair attempt must remain independent.
                                                                         This independence is crucial to prevent the algorithm from becom-
    While the two examples above show trivial caching semantics
                                                                         ing stuck in repeated unsuccessful attempts when the score fails to
supported by previous systems, Mnimi provides more fine-grained
                                                                         improve. Thus, we utilize an Independent model reference, which
control over sample independence. To show it, assume a user must
                                                                         guarantees that each repair attempt explores fresh samples.
be given the same number in every round for the same interval, but
across different games, corresponding to different iterations of the
outer loop, numbers given to the same user must be independent,          def specfix(problem, model, C=20, E=10, max_attempts=3):
it requires composing repeatable and independent layers:                     rep_model = Persistent(model, "/cache/path")
                                                                             ind_model = Independent(rep_model)
 model = Persistent(model, "/cache/path")
 model = Independent(model)                                                   def score(D):
 responses = []                                                                   prompt = CODE_GEN_TMPL.format(description=D)
 for user in users:                                                               # generate C programs, always the same
   rep_model = InMemory(model)                                                    # for the same requirements
   for interval in ints:                                                          progs = islice(rep_model.sample(prompt), C)
     prompt = template.format(user=user,interval=interval)
     response = next(rep_model.sample(prompt))                                    prompt = TEST_GEN_TMPL.format(description=D)
     responses.append(response)                                                   # generate E tests, always the same
 assert responses == ["2", "1393", "2", "297", "1740",                            # for the same requirements
 ↩→ "297", "68", "1002", "68"]                                                    tests = islice(rep_model.sample(prompt), E)

where InMemory, a subclass of Repeatable with in-memory cache,                    clusters = cluster(progs, tests)
ensures deterministic reuse within the loop, Independent ensures                  return evaluate_entropy_and_consistency(clusters)
independent sampling across loop iterations, and Persistent pro-
vides on-disk cache for reproducibility across runs. Here, statistical        D = problem.description
independence constraints are elegantly encoded through LLM ref-
                                                                              for attempt in range(max_attempts):
erence types. In contrast, systems like Cache Saver that reply on
                                                                                  prompt = REPAIR_TMPL.format(description=D)
explicit namespaces prohibit intra-namespace reuse of samples,
                                                                                  # repairs are always independent, but the sequence
which prevents expressing repeatability within each loop iteration.               # of repairs is cached on disk, and replayed
                                                                                  D2 = next(ind_model.sample(prompt))
3   Case Study: Mnimi Integration in SpecFix
SpecFix [12] automatically repairs ambiguous programming prob-                    if score(D2) > score(D):
lem descriptions to improve LLM-based code generation. It samples                     D = D2
multiple candidate programs based on a given natural-language                     if score(D) >= THRESHOLD:
                                                                                      return D
description, clusters their behaviors, and evaluates interpretive
                                                                              return D
ambiguity using metrics such as semantic entropy and example
consistency. The pipeline consists of several stages: test generation,   Listing 1: Statistical independence constraints in SpecFix
program sampling, and iterative repair, all of which rely heavily        repair loop encoded via Mnimi decorators.
on a large number of stochastic LLM calls. As a result, the process
can produce varying outputs — including tests, programs, and final           To quantify Mnimi’s impact on SpecFix, we conducted eight con-
repaired descriptions — across different runs, making it expensive       trolled runs on 100 randomly selected HumanEval+ problems using
to reproduce and hard to debug. Meanwhile, the metrics driving           gpt-4.1-mini at temperature 1.0. Each run varied the caching con-
SpecFix, such as semantic entropy and Pass@K, are fundamentally          figuration and the program sample size (𝐶) and test sample size (𝐸),
statistical and depend on independent samples. Furthermore, Spec-        which estimate behavioral diversity, as summarized in Table 1. The
Fix’s repair loop necessitates generation of independent repairs.        first run, labeled Baseline, mirrors the original SpecFix behavior as
These aspects make naive caching not applicable for SpecFix.             no cached responses are used, with the small change of writing all
Statistical Independence Aware Caching for LLM Workflows


Table 1: Token usage, runtime, and cost of LLM queries in SpecFix with and without Mnimi caching (100 HumanEval+ tasks,
gpt-4.1-mini, temperature 1.0). C is the number of generated programs, E is the number of generated test. Baseline does
not read from the cache but records all responses for future reuse, with its results reflecting how Specfix behaved originally.
No cache runs ignore caching entirely (no reads or writes). First cached reuses stored results from the baseline, paying only for
unseen generations, and Cached replay deterministically replays all queries at zero cost.

          Run configuration                  Prompt tokens           Completion tokens    Total tokens      API time (s)    Total cost ($)
          Baseline (𝑐=20, 𝑒=10)                             97,669              319,814          417,483          1,716.1              1.10
          Cached replay (𝑐=20, 𝑒=10)                            0                     0                0              0.0              0.00
          No cache (𝑐=40, 𝑒=10)                            100,733              500,792          601,525          2,344.9              1.68
          First cached (𝑐=40, 𝑒=10)                         50,885              250,349          301,234            867.5              0.84
          Cached replay (𝑐=40, 𝑒=10)                            0                     0                0              0.0              0.00
          No cache (𝑐=20, 𝑒=20)                             94,207              402,743          496,950          2,234.6              1.36
          First cached (𝑐=20, 𝑒=20)                          2,941               32,872           35,813             93.9              0.11
          Cached replay (𝑐=20, 𝑒=20)                            0                     0                0              0.0              0.00


outputs to the cache for future reuse. No-cache runs, in contrast,              with high prompt diversity, and although disk-based persistence is
ignore caching entirely (no reads or writes), incurring full cost and           efficient, long-term cache management and eviction remain manual.
runtime on every execution and forfeiting reproducibility.
   Enabling reading from the baseline’s cached responses immedi-                5   Related Work
ately reduced query cost to zero on the next run, replaying results                Traditional Caching. Caching is crucial for system optimiza-
byte-for-byte. When the program sample size increased from 𝐶=20                 tion but is challenging to implement correctly. Besnard et al. [3]
to 𝐶=40, or from 𝐸=10 to 𝐸=20 the First cached run incurred ad-                 highlighted that caching non-deterministic functions can alter pro-
ditional cost only for the 20 new programs and the 10 extra tests               gram behavior and proposed memoizing only pure, deterministic
respectively. The next Cached replays again dropped to zero cost,               computations. This principle extends to web systems, where HTTP
demonstrating perfect reuse once the cache was complete. With-                  caching and CDN policies often exclude dynamic content. Bos
out caching, all generations are recomputed from scratch, greatly               et al. [4] introduced CacheCard, a NIC-level caching system that
increasing both cost and runtime. This confirms Mnimi ’s incre-                 avoids caching dynamic web pages unless dependencies are explic-
mental cost model: identical workloads replay deterministically                 itly tracked. In databases, Garrod et al. [9] described a distributed
at zero cost, and only new generations trigger additional queries.              query result cache that ensures semantic correctness through in-
Moreover, reproducible cached runs allowed all experiments to be                validation triggered by database writes.
re-run in seconds without recontacting the API.
   Reproducibility is a critical challenge in empirical computer                    Probabilistic Sampling and Lazy Evaluation. Functional pro-
science, especially for tools like SpecFix that rely on stochastic              gramming research has explored how to represent stochastic com-
processes such as sampling from LLMs. Without mechanisms like                   putations as reproducible, composable data structures. Scibior et
caching and deterministic replay, researchers must rerun entire                 al. [19] formalize probabilistic sampling as lazy sequences, enabling
experiments from scratch, making replication studies prohibitively              repeatable access to random draws within purely functional pro-
expensive in time and cost, and exacerbating the replication crisis             grams. This serves as an inspiration for Mnimi that uses infinite lazy
in the field [7]. Local caching addresses this issue by reducing com-           sequences to implement composable layers representing different
putational overhead, enabling stable and deterministic outcomes,                statistical independence constraints.
and facilitating data sharing for validation and comparison.                       Frameworks for LLM Programming and LLM Caching. Due
                                                                                to existence of LLM-related implementations, LLM-integrated scripts
4    Discussion                                                                 are facing challenges in terms of performance, modularity, and read-
While Mnimi enhances reproducibility and reduces costs at negligi-              ability. Wang [21] proposed the use of composable effect handling
ble overhead, several challenges remain open. Future extensions                 to separate workflow logic from LLM-related effectful operations,
could integrate semantic caching [10], allowing re-use across para-             thereby enabling modularity without sacrificing the potential for
phrased or structurally equivalent prompts while still preserving               performance optimization. Consistent with this, our work also aims
statistical guarantees. Introducing concurrency-aware cache ac-                 to benefit LLM programming by decoupling LLM caching from core
cess would further accelerate large-scale multi-threaded workflows,             program logic. Frameworks like LangChain [5] use string-based
enabling safe parallelism across repair attempts and datasets.                  caching, where identical prompts return stored outputs to avoid
   The current implementation has limitations. Its correctness relies           redundant queries, improving efficiency but lacking control over
on deterministic serialization of prompts and settings; any nonde-              statistical independence. Meanwhile, MeanCache [10] and GPT-
terminism, such as API-side randomness or floating-point ordering,              Cache [2] extend caching to semantically similar prompts, com-
can introduce subtle drift. Cache storage may grow large for tasks              plementing Mnimi. Frameworks like FloTorch [1] optimize agentic
                                                                                                                                                                    Dai et al.


workflows by caching intermediate steps with per-step policies.                              Methods in Large Language Models. arXiv:2510.20460 [cs.CL] https://arxiv.org/
Low-level optimizations, such as vLLM’s key–value cache [14], ac-                            abs/2510.20460
                                                                                        [12] Haoxiang Jia, Robbie Morris, He Ye, Federica Sarro, and Sergey Mechtaev. 2025.
celerate token-level computation reuse but do not provide statistical                        Automated Repair of Ambiguous Problem Descriptions for LLM-Based Code
independence control. Cache Saver [18] introduces “namespaces”,                              Generation. arXiv:2505.07270 [cs.SE] https://arxiv.org/abs/2505.07270
                                                                                        [13] Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. 2023. Semantic uncertainty:
where samples labelled with the same namespace are guaranteed                                Linguistic invariances for uncertainty estimation in natural language generation.
to be independent. Section 2.2 shows examples that are hard to                               arXiv preprint arXiv:2302.09664 (2023).
express using namespaces, but are concisely expressible in Mnimi.                       [14] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng,
                                                                                             Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica. 2023. Efficient
                                                                                             Memory Management for Large Language Model Serving with PagedAttention.
6    Conclusion                                                                              arXiv:2309.06180 [cs.LG] https://arxiv.org/abs/2309.06180
                                                                                        [15] Qing Lyu, Kumar Shridhar, Chaitanya Malaviya, Li Zhang, Yanai Elazar, Niket
This work introduces Mnimi, a cache design pattern that ensures                              Tandon, Marianna Apidianaki, Mrinmaya Sachan, and Chris Callison-Burch.
statistical integrity while supporting modular LLM workflows. It en-                         2025. Calibrating large language models with sample consistency. In Proceedings
codes statistical independence constraints through reference types:                          of the AAAI Conference on Artificial Intelligence, Vol. 39. 19260–19268.
                                                                                        [16] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah
repeatable model references yield identical sequences of responses                           Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank
for a given prompt, while independent references produce fresh,                              Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir
                                                                                             Yazdanbakhsh, and Peter Clark. 2023. Self-Refine: Iterative Refinement with
independent sequences of responses. By allowing flexible transfor-                           Self-Feedback. arXiv:2303.17651 [cs.CL] https://arxiv.org/abs/2303.17651
mations between reference types, Mnimi simplifies maintaining                           [17] Potsawee Manakul, Adian Liusie, and Mark J. F. Gales. 2023. SelfCheckGPT: Zero-
statistical integrity across algorithm scopes. A case study on the                           Resource Black-Box Hallucination Detection for Generative Large Language
                                                                                             Models. arXiv:2303.08896 [cs.CL] https://arxiv.org/abs/2303.08896
SpecFix tool demonstrates how Mnimi reduces research costs while                        [18] Nearchos Potamitis, Lars Henning Klein, Chongyang Xu, Attreyee Mukherjee,
enhancing reproducibility and experimentation.                                               Bardia Mohammadi, Niket Tandon, Laurent Bindschaedler, and Akhil Arora.
                                                                                             [n. d.]. Cache Saver: A Modular Framework for Efficient, Affordable, and Re-
                                                                                             producible LLM Inference. In ES-FoMo III: 3rd Workshop on Efficient Systems for
References                                                                                   Foundation Models.
 [1] 2025. FloTorch: Agent-Aware Caching and Modular AI Pipelines. https://flotorch.    [19] Adam Ścibior, Zoubin Ghahramani, and Andrew D Gordon. 2015. Practical
     ai. Accessed: 2025-10-13.                                                               probabilistic programming with monads. In Proceedings of the 2015 ACM SIGPLAN
 [2] Fu Bang. 2023. GPTCache: An Open-Source Semantic Cache for LLM Appli-                   Symposium on Haskell. 165–176.
     cations Enabling Faster Answers and Cost Savings. In Proceedings of the 3rd        [20] Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik
     Workshop for Natural Language Processing Open Source Software (NLP-OSS 2023),           Narasimhan, and Shunyu Yao. 2023. Reflexion: Language Agents with Verbal
     Liling Tan, Dmitrijs Milajevs, Geeticka Chauhan, Jeremy Gwinnup, and Elijah             Reinforcement Learning. arXiv:2303.11366 [cs.AI] https://arxiv.org/abs/2303.
     Rippeth (Eds.). Association for Computational Linguistics, Singapore, 212–218.          11366
     doi:10.18653/v1/2023.nlposs-1.24                                                   [21] Di Wang. 2025. Composable Effect Handling for Programming LLM-Integrated
 [3] Loïc Besnard, Pedro Pinto, Imane Lasri, João Bispo, Erven Rohou, and João M.P.          Scripts. In Language Models and Programming Languages (LMPL’25). doi:10.1145/
     Cardoso. 2019. A framework for automatic and parameterizable memoization.               3759425.3763396
     SoftwareX 10 (2019), 100322. doi:10.1016/j.softx.2019.100322
 [4] Herbert Bos and Kaiming Huang. 2009. CacheCard: caching static and dynamic
     content on the NIC. In Proceedings of the 5th ACM/IEEE Symposium on Archi-
     tectures for Networking and Communications Systems (Princeton, New Jersey)
     (ANCS ’09). Association for Computing Machinery, New York, NY, USA, 1–10.
     doi:10.1145/1882486.1882491
 [5] Harrison Chase. 2023. LangChain: Building applications with large language
     models through composability. https://python.langchain.com. Accessed: 2025-
     10-13.
 [6] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de
     Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
     Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf,
     Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail
     Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter,
     Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fo-
     tios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex
     Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji,
     Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike,
     Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight,
     Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario
     Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. 2021. Eval-
     uating Large Language Models Trained on Code. arXiv:2107.03374 [cs.LG]
     https://arxiv.org/abs/2107.03374
 [7] Andy Cockburn, Pierre Dragicevic, Lonni Besançon, and Carl Gutwin. 2020.
     Threats of a replication crisis in empirical computer science. Commun. ACM 63,
     8 (2020), 70–79.
 [8] Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides. 1995. Design
     patterns: elements of reusable object-oriented software. Pearson Deutschland
     GmbH.
 [9] Charles Garrod, Amit Manjhi, Anastasia Ailamaki, Bruce Maggs, Todd Mowry,
     Christopher Olston, and Anthony Tomasic. 2008. Scalable query result caching
     for web applications. Proc. VLDB Endow. 1, 1 (Aug. 2008), 550–561. doi:10.14778/
     1453856.1453917
[10] Waris Gill, Mohamed Elidrisi, Pallavi Kalapatapu, Ammar Ahmed, Ali Anwar, and
     Muhammad Ali Gulzar. 2025. MeanCache: User-Centric Semantic Caching for
     LLM Web Services. In 2025 IEEE International Parallel and Distributed Processing
     Symposium (IPDPS). IEEE, 1298–1310. doi:10.1109/ipdps64566.2025.00117
[11] Christian Hobelsberger, Theresa Winner, Andreas Nawroth, Oliver Mitevski, and
     Anna-Carolina Haensch. 2025. Systematic Evaluation of Uncertainty Estimation
