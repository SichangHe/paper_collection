# A Critical Analysis of the Largest Source for Generative AI Training Data: Common Crawl
(authored by agents unless marked 🧑)

- primary PDF: local collection PDF
- publication: FAccT 2024
- DOI: https://doi.org/10.1145/3630106.3659033
- URL: https://facctconference.org/static/papers24/facct24-62.pdf

## abstract (verbatim)
> Common Crawl is the largest freely available collection of web crawl data and one of the most important sources of pre-training data for large language models (LLMs). It is used so frequently and makes up such large proportions of the overall pre-training data in many cases that it arguably has become a foundational building block for LLM development, and subsequently generative AI products built on top of LLMs. Despite its pivotal role, Common Crawl itself is not widely understood, nor is there much reflection evident among LLM builders about the implications of using Common Crawl’s data. ... We find that Common Crawl’s popularity has contributed to making generative AI more transparent to scrutiny in many ways ... At the same time, many LLM builders have used Common Crawl as a source for training data in ways that are problematic: for instance, with lack of care and transparency for how Common Crawl’s massive crawl data was filtered for harmful content before the pre-training, often by relying on rudimentary automated filtering techniques.

## relevance to DeGenTWeb
This documents the web-crawl ecosystem from which both online content and AI training data are drawn. Its analysis of crawl coverage, filtering, and accountability helps frame why measuring AI-generated pages on the open web matters and why detector-based estimates depend on corpus composition.
