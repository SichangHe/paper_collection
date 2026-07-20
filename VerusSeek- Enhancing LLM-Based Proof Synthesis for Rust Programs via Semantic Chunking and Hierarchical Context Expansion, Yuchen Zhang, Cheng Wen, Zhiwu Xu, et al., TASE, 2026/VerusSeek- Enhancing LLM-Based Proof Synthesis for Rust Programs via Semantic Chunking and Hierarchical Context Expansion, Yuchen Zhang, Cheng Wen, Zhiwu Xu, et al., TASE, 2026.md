# VerusSeek: Enhancing LLM-Based Proof Synthesis for Rust Programs via Semantic Chunking and Hierarchical Context Expansion

## Collection record

- Record type: publisher metadata and abstract only; this is not a full-paper extraction.
- Supplied source: https://dl.acm.org/doi/abs/10.1007/978-3-032-30693-7_6
- Publication status: accepted chapter in the 2026 TASE proceedings.
- Access note: the publisher PDF was not available through the configured browser session. Its public preview contained front matter and the table of contents, not the chapter. A third-party host presented a security challenge, which was not bypassed.

## Abstract-level evidence

- Motivation: the abstract says that “retrieving coarse-grained entire files or functions introduces noise.”
- Method: VerusSeek divides programs into semantic chunks based on typed program constructs, then expands context hierarchically to retrieve proof-relevant information for Rust/Verus proof synthesis.
- Reported result: on 150 VerusBench problems, the abstract reports improvements of 76.7% over AutoVerus and 43.4% over RagVerus.
- Uncertainty: without the full chapter, the absolute success rates, precise metric denominator, ablations, prompt/model details, and failure analysis could not be checked. These numbers should therefore be cited as publisher-abstract claims, not independently verified full-paper results.
